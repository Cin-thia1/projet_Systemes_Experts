# inference_engine.py - Moteur d'inférence du système expert SEMI
# Système Expert de Maintenance Informatique
#
# Architecture inspirée de CLIPS / experta :
#   - Faits typés avec horodatage (Fact)
#   - Agenda avec priorité explicite
#   - Résolution de conflits : spécificité > certitude > recency > ordre
#   - Cycle MATCH → CONFLICT-RESOLUTION → ACT en boucle
#   - Chaînage avant ET chaînage arrière
#   - Propagation des certitudes : certitude_règle × min(certitudes conditions)
#
# CORRECTION BUG GUI :
#   lancer_moteur() retourne UNIQUEMENT les règles déclenchées lors de CET appel.
#   L'état persiste entre les appels (regles_deja_declenchees) donc pas de doublon.
#   Chaque appel ne retourne que ses nouvelles déductions, ce qui permet
#   d'appeler lancer_moteur() incrémentalement après chaque nouveau fait.

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional
import time as _time

from facts import faits, ajouter_fait, fait_existe, reinitialiser, afficher_faits
from rules import REGLES


# ══════════════════════════════════════════════════════════════════════════════
#  FAIT TYPÉ  (inspiré Fact de CLIPS)
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class Fact:
    """Fait avec certitude et horodatage monotone d'insertion."""
    nom:       str
    certitude: float = 1.0
    timestamp: int   = field(default_factory=lambda: _time.monotonic_ns())

    def __hash__(self):
        return hash(self.nom)

    def __eq__(self, other):
        return self.nom == (other.nom if isinstance(other, Fact) else other)


# ══════════════════════════════════════════════════════════════════════════════
#  ACTIVATION  (entrée de l'agenda)
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class Activation:
    """
    Règle activée avec sa clé de priorité.
    Priorité (décroissant) :
      1. Spécificité (nombre de conditions)
      2. Certitude déclarée
      3. Recency (timestamp max des faits déclencheurs)
      4. Numéro d'id (ordre de définition, tie-breaker)
    """
    regle:    dict
    facts_in: list

    @property
    def specificite(self) -> int:
        return len(self.regle["conditions"])

    @property
    def certitude_regle(self) -> float:
        return self.regle.get("certitude", 0.5)

    @property
    def recency(self) -> int:
        return max((f.timestamp for f in self.facts_in), default=0)

    @property
    def id_num(self) -> int:
        return int(self.regle["id"][1:])

    def priority_key(self):
        return (-self.specificite, -self.certitude_regle, -self.recency, self.id_num)


# ══════════════════════════════════════════════════════════════════════════════
#  ÉTAT INTERNE DU MOTEUR
# ══════════════════════════════════════════════════════════════════════════════

_fact_store:               dict  = {}   # nom -> Fact
_regles_deja_declenchees:  set   = set()
_agenda:                   list  = []


# ══════════════════════════════════════════════════════════════════════════════
#  GESTION DES FAITS TYPÉS
# ══════════════════════════════════════════════════════════════════════════════

def assert_fact(nom: str, certitude: float = 1.0) -> Fact:
    """
    Ajoute un fait typé dans le store et dans la liste legacy (facts.py).
    Si le fait existe déjà, met à jour sa certitude si la nouvelle est plus haute.
    """
    if nom in _fact_store:
        existing = _fact_store[nom]
        if certitude > existing.certitude:
            _fact_store[nom] = Fact(nom, certitude, existing.timestamp)
        return _fact_store[nom]

    f = Fact(nom, certitude)
    _fact_store[nom] = f
    ajouter_fait(nom)   # maintien liste legacy pour compatibilité GUI
    return f


def get_certitude(nom: str) -> float:
    """Retourne la certitude d'un fait (1.0 par défaut)."""
    f = _fact_store.get(nom)
    return f.certitude if f else 1.0


def set_certitude(nom: str, valeur: float) -> None:
    valeur = max(0.0, min(1.0, valeur))
    if nom in _fact_store:
        _fact_store[nom] = Fact(nom, valeur, _fact_store[nom].timestamp)
    else:
        assert_fact(nom, valeur)


# Alias pour compatibilité avec facts.py / GUI
def ajouter_fait_moteur(nom: str, certitude: float = 1.0) -> None:
    """Point d'entrée principal pour ajouter un fait depuis la GUI."""
    assert_fact(nom, certitude)


# ══════════════════════════════════════════════════════════════════════════════
#  ÉTAPE 1 — MATCH
# ══════════════════════════════════════════════════════════════════════════════

def _match() -> list:
    """Retourne toutes les activations applicables non encore déclenchées."""
    activations = []
    for regle in REGLES:
        if regle["id"] in _regles_deja_declenchees:
            continue
        if all(c in _fact_store for c in regle["conditions"]):
            facts_in = [_fact_store[c] for c in regle["conditions"]]
            activations.append(Activation(regle, facts_in))
    return activations


# ══════════════════════════════════════════════════════════════════════════════
#  ÉTAPE 2 — CONFLICT RESOLUTION
# ══════════════════════════════════════════════════════════════════════════════

def _conflict_resolution(activations: list) -> Optional[Activation]:
    """Sélectionne l'activation de plus haute priorité."""
    if not activations:
        return None
    return min(activations, key=lambda a: a.priority_key())


# ══════════════════════════════════════════════════════════════════════════════
#  ÉTAPE 3 — ACT
# ══════════════════════════════════════════════════════════════════════════════

def _act(activation: Activation, verbose: bool = True) -> float:
    """
    Exécute une activation :
      certitude_out = certitude_règle × min(certitudes des faits déclencheurs)
    """
    regle    = activation.regle
    conc     = regle["conclusion"]
    cert_r   = regle.get("certitude", 0.5)
    min_cert = min(f.certitude for f in activation.facts_in) if activation.facts_in else 1.0
    cert_out = round(cert_r * min_cert, 3)

    if verbose:
        print(f"\n  [{regle['id']}] {regle.get('categorie','?').upper()}")
        print(f"  Conditions : {regle['conditions']}")
        print(f"  Conclusion : {conc}")
        print(f"  Certitude  : {cert_out:.0%}  "
              f"(règle {cert_r:.0%} × min_conds {min_cert:.0%})")
        print(f"  Solution   : {regle['solution']}")

    assert_fact(conc, cert_out)
    _regles_deja_declenchees.add(regle["id"])
    return cert_out


# ══════════════════════════════════════════════════════════════════════════════
#  CHAÎNAGE AVANT
# ══════════════════════════════════════════════════════════════════════════════

def lancer_moteur(verbose: bool = False) -> list:
    """
    Cycle MATCH → CR → ACT jusqu'à épuisement de l'agenda.

    Retourne UNIQUEMENT les règles déclenchées lors de CET appel.
    L'état persiste entre les appels : les règles déjà déclenchées
    lors d'appels précédents ne seront jamais redéclenchées.
    """
    iteration           = 0
    declenchees_ce_run  = []

    if verbose:
        print("=" * 55)
        print("  MOTEUR D'INFÉRENCE — CHAÎNAGE AVANT (CLIPS-like)")
        print("=" * 55)

    while True:
        iteration  += 1
        activations = _match()

        if verbose:
            ids = [a.regle["id"] for a in activations]
            print(f"\n  Iter {iteration} | Agenda : {ids if ids else '∅'}")

        chosen = _conflict_resolution(activations)

        if chosen is None:
            if verbose:
                print("  Arrêt : agenda vide.")
            break

        if verbose:
            print(f"  Choix  : {chosen.regle['id']} "
                  f"(spéc={chosen.specificite}, "
                  f"cert={chosen.certitude_regle:.0%})")

        cert = _act(chosen, verbose=verbose)
        declenchees_ce_run.append({**chosen.regle, "_certitude_calculee": cert})

    if verbose:
        print("\n" + "=" * 55)
        print(f"  FIN — {len(declenchees_ce_run)} règle(s) ce cycle")
        print("=" * 55)
        afficher_faits()

    return declenchees_ce_run


# ══════════════════════════════════════════════════════════════════════════════
#  CHAÎNAGE ARRIÈRE
# ══════════════════════════════════════════════════════════════════════════════

def chainer_arriere(but: str, profondeur: int = 0, visites: set = None) -> bool:
    """
    Prouve un but par chaînage arrière récursif.
    Retourne True si le but est prouvable depuis les faits courants.
    """
    if visites is None:
        visites = set()

    if but in _fact_store:
        return True
    if but in visites:
        return False
    visites.add(but)

    for regle in REGLES:
        if regle["conclusion"] != but:
            continue
        if all(chainer_arriere(c, profondeur + 1, visites) for c in regle["conditions"]):
            if regle["id"] not in _regles_deja_declenchees:
                facts_in = [_fact_store.get(c, Fact(c)) for c in regle["conditions"]]
                _act(Activation(regle, facts_in), verbose=False)
            return True

    return False


def diagnostiquer_par_but(conclusion: str) -> Optional[dict]:
    """Diagnostic ciblé via chaînage arrière."""
    if chainer_arriere(conclusion):
        regle = next((r for r in REGLES if r["conclusion"] == conclusion), None)
        if regle:
            return {**regle, "_certitude_calculee": get_certitude(conclusion)}
    return None


# ══════════════════════════════════════════════════════════════════════════════
#  UTILITAIRES D'ANALYSE
# ══════════════════════════════════════════════════════════════════════════════

def conditions_manquantes(conclusion: str) -> list:
    """Retourne les conditions non satisfaites pour une conclusion donnée."""
    manquantes = []
    for regle in REGLES:
        if regle["conclusion"] != conclusion:
            continue
        for cond in regle["conditions"]:
            if cond not in _fact_store and cond not in manquantes:
                manquantes.append(cond)
    return manquantes


def diagnostics_possibles() -> list:
    """
    Règles partiellement satisfaites (>= 1 condition vraie),
    triées par taux de progression décroissant.
    """
    possibles = []
    for regle in REGLES:
        if regle["id"] in _regles_deja_declenchees:
            continue
        nb_ok = sum(1 for c in regle["conditions"] if c in _fact_store)
        if nb_ok > 0:
            possibles.append({
                "regle":                  regle,
                "conditions_satisfaites": nb_ok,
                "conditions_totales":     len(regle["conditions"]),
                "progression":            nb_ok / len(regle["conditions"]),
            })
    possibles.sort(key=lambda x: -x["progression"])
    return possibles


def statistiques_moteur() -> dict:
    return {
        "faits_connus":       len(_fact_store),
        "regles_declenchees": len(_regles_deja_declenchees),
        "regles_totales":     len(REGLES),
        "regles_restantes":   len(REGLES) - len(_regles_deja_declenchees),
    }


# ══════════════════════════════════════════════════════════════════════════════
#  RÉINITIALISATION
# ══════════════════════════════════════════════════════════════════════════════

def reinitialiser_moteur() -> None:
    """Remet à zéro l'intégralité de l'état du moteur."""
    reinitialiser()
    _fact_store.clear()
    _regles_deja_declenchees.clear()
    _agenda.clear()


# ══════════════════════════════════════════════════════════════════════════════
#  TESTS INTÉGRÉS
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":

    print("\n=== TEST 1 : Appels incrémentaux (simulation mode guidé) ===")
    reinitialiser_moteur()

    print("\n-- Ajout: pc_lent --")
    assert_fact("pc_lent")
    r = lancer_moteur(verbose=False)
    print(f"   Résultats ce run: {[x['id'] for x in r]}")

    print("\n-- Ajout: cpu_usage_eleve --")
    assert_fact("cpu_usage_eleve")
    r = lancer_moteur(verbose=False)
    print(f"   Résultats ce run: {[x['id'] for x in r]}")

    print("\n-- Ajout: programmes_inconnus --")
    assert_fact("programmes_inconnus")
    r = lancer_moteur(verbose=False)
    print(f"   Résultats ce run: {[x['id'] for x in r]}")

    print("\n-- Appel redondant (doit retourner []) --")
    r = lancer_moteur(verbose=False)
    print(f"   Résultats ce run: {[x['id'] for x in r]}  ← attendu: []")

    print("\n=== TEST 2 : Chaînage arrière — ransomware ===")
    reinitialiser_moteur()
    assert_fact("fichiers_chiffres")
    assert_fact("message_rancon")
    res = diagnostiquer_par_but("ransomware")
    print(f"   {res['conclusion']} — {res['_certitude_calculee']:.0%}" if res else "   Non trouvé")

    print("\n=== TEST 3 : Batterie gonflée (verbose) ===")
    reinitialiser_moteur()
    assert_fact("laptop")
    assert_fact("batterie_gonflee")
    lancer_moteur(verbose=True)

    print("\n=== TEST 4 : Statistiques ===")
    print(f"   {statistiques_moteur()}")

    print("\n=== TEST 5 : Conditions manquantes pour virus_cryptomineur ===")
    reinitialiser_moteur()
    assert_fact("pc_lent")
    print(f"   {conditions_manquantes('virus_cryptomineur')}")
