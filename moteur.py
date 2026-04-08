from faits import faits, ajouter_fait, fait_existe, reinitialiser, afficher_faits
from base_connaissance import REGLES

agenda=[]
regles_deja_declenchees=set()

#Etape1: match
def match():
    """Re toune la liste des règles applicables"""
    candidates=[]
    for regle in REGLES:
        if regle["id"] in regles_deja_declenchees:
            continue
        if all(fait_existe(c) for c in regle["conditions"]):
            candidates.append(regle)
    return candidates

#Etape2: conflict resolution, on choisit la règle
def conflict_resolution(candidates):
    if not candidates:
        return None
    max_conds=max(len(r["conditions"]) for r in candidates)
    filtrees=[r for r in candidates if len(r["conditions"])==max_conds]

    filtrees.sort(key=lambda r: int(r["id"][1:]))
    return filtrees[0]

#Etape3:ACT
def act(regle, verbose=True):
    """Exécuter les règles choisies"""
    conclusion=regle["conclusion"]
    solution=regle["solution"]
    if verbose:
        print(f"\n Règle{regle['id']} déclenchée")
        print(f"Conditions: {regle['conditions']}")
        print(f" Diagnostic: {conclusion}")
        print(f" Solution: {solution}")

    ajouter_fait(conclusion)
    regles_deja_declenchees.add(regle["id"])

#Lancement du moteur
def lancer_moteur(verbose=True):
    """Le cycle d'inférence en chaînage avant en régime irrévocable"""

    iteration = 0

    if verbose:
        print("DEMARRAGE DU MOTEUR D'INFERENCE")

    while True:                          
        iteration += 1
        if verbose:
            print(f"\n── Itération {iteration} ──────────────────────────")

        candidates = match()
        if verbose:
            ids = [r["id"] for r in candidates]
            print(f"[MATCH] Règles applicables: {ids if ids else 'aucune'}")

        regle_choisie = conflict_resolution(candidates)
        if verbose and candidates:
            print(f"[CR] Règle choisie: {regle_choisie['id'] if regle_choisie else 'aucune'}")

        if regle_choisie is None:        
            if verbose:
                print("\n Arrêt moteur car agenda vide")
            break

        act(regle_choisie, verbose=verbose)

    if verbose:                          
        print("FIN DU CYCLE D'INFERENCE")
        afficher_faits()

#Réinitialisation entre deux sessions
def reinitialiser_moteur():
    reinitialiser()
    agenda.clear()
    regles_deja_declenchees.clear()


if __name__ == "__main__":
 
    # ── Scénario 1 : PC ne démarre pas avec bip 
    print("  \n SCÉNARIO 1 : PC ne démarre pas + bip sonore")
    reinitialiser_moteur()
    ajouter_fait("pc_ne_demarre_pas")
    ajouter_fait("bip_sonore")
    lancer_moteur()
 
    # ── Scénario 2 : PC lent — plusieurs causes possibles ─
    print("  \nSCÉNARIO 2 : PC lent (RAM faible + programmes suspects)")
    reinitialiser_moteur()
    ajouter_fait("pc_lent")
    ajouter_fait("ram_insuffisante")
    ajouter_fait("programmes_inconnus")
    lancer_moteur()
 
    # ── Scénario 3 : Pas de connexion internet
    print("  \n SCÉNARIO 3 : Pas de connexion, Wi-Fi activé")
    reinitialiser_moteur()
    ajouter_fait("pas_de_connexion")
    ajouter_fait("wifi_active")
    lancer_moteur()
 
    # ── Scénario 4 : Laptop + batterie + surchauffe 
    print("  \n SCÉNARIO 4 : Laptop — batterie + extinction brusque")
    reinitialiser_moteur()
    ajouter_fait("laptop")
    ajouter_fait("batterie_ne_charge_pas")
    ajouter_fait("pc_eteint_brusquement")
    ajouter_fait("temperature_elevee")
    lancer_moteur()
 
    # ── Scénario 5 : Chaînage en cascade 
    print("  \n SCÉNARIO 5 : Chaînage en cascade (écran + pilotes)")
    reinitialiser_moteur()
    ajouter_fait("ecran_clignote")
    ajouter_fait("pilotes_anciens")
    lancer_moteur()

                    
