import customtkinter as ctk
import tkinter as tk
from tkinter import font as tkfont
import threading
import time
import sys
import os

# ── Ajouter le dossier des modules au path ──────────────────────────────────
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from faits import faits, ajouter_fait, fait_existe, reinitialiser
from base_connaissance import REGLES
from moteur import lancer_moteur, reinitialiser_moteur

# ══════════════════════════════════════════════════════════════════════════════
#  PALETTE DE COULEURS
# ══════════════════════════════════════════════════════════════════════════════
DARK = {
    "bg":           "#0F1117",
    "surface":      "#1A1D27",
    "surface2":     "#22263A",
    "border":       "#2E3250",
    "accent":       "#4F8EF7",
    "accent2":      "#7C5CFC",
    "user_bubble":  "#1E3A5F",
    "bot_bubble":   "#1C1F2E",
    "text":         "#E8EAF6",
    "text_dim":     "#7B82A8",
    "success":      "#43D9A2",
    "warning":      "#F7C948",
    "error":        "#F76E6E",
    "input_bg":     "#181B28",
    "button":       "#4F8EF7",
    "button_hover": "#3A78E0",
    "yes_btn":      "#2ECC71",
    "no_btn":       "#E74C3C",
    "tag_bg":       "#2A2E45",
}

LIGHT = {
    "bg":           "#F0F4FF",
    "surface":      "#FFFFFF",
    "surface2":     "#E8EEFF",
    "border":       "#C5CCED",
    "accent":       "#3B72E8",
    "accent2":      "#6B4FE0",
    "user_bubble":  "#3B72E8",
    "bot_bubble":   "#FFFFFF",
    "text":         "#1A1D35",
    "text_dim":     "#6B7280",
    "success":      "#27AE60",
    "warning":      "#F39C12",
    "error":        "#E74C3C",
    "input_bg":     "#F8F9FF",
    "button":       "#3B72E8",
    "button_hover": "#2A5FD0",
    "yes_btn":      "#27AE60",
    "no_btn":       "#E74C3C",
    "tag_bg":       "#E2E7FF",
}


# ══════════════════════════════════════════════════════════════════════════════
#  MOTEUR D'INFÉRENCE — wrapper pour l'interface
# ══════════════════════════════════════════════════════════════════════════════

# Dictionnaire de traduction des faits internes → questions lisibles
QUESTIONS_MAP = {
    "pc_ne_demarre_pas":        "Le PC ne démarre pas ?",
    "pc_allume":                "Le PC s'allume ?",
    "pc_lent":                  "Le PC est lent ?",
    "ventilateur_tourne":       "Le ventilateur tourne ?",
    "ventilateur_ne_tourne_pas":"Le ventilateur ne tourne pas du tout ?",
    "ecran_noir":               "L'écran reste noir ?",
    "ecran_bleu":               "Vous avez un écran bleu (BSOD) ?",
    "ecran_clignote":           "L'écran clignote ?",
    "cpu_usage_eleve":          "L'utilisation CPU est très élevée ?",
    "ram_insuffisante":         "Vous manquez de mémoire RAM ?",
    "disque_plein":             "Le disque dur est presque plein ?",
    "fichiers_inaccessibles":   "Des fichiers sont inaccessibles ?",
    "bruits_disque":            "Vous entendez des bruits provenant du disque dur ?",
    "pas_de_connexion":         "Vous n'avez pas de connexion internet ?",
    "wifi_desactive":           "Le Wi-Fi est désactivé ?",
    "wifi_active":              "Le Wi-Fi est activé mais ça ne marche pas ?",
    "plantage_frequent":        "Le système plante fréquemment ?",
    "programmes_inconnus":      "Il y a des programmes inconnus dans la liste des apps ?",
    "clavier_non_detecte":      "Le clavier n'est pas détecté ?",
    "imprimante_non_detectee":  "L'imprimante n'est pas détectée ?",
    "pc_eteint_brusquement":    "Le PC s'éteint brusquement tout seul ?",
    "temperature_elevee":       "La température du PC est très élevée ?",
    "bip_sonore":               "Vous entendez des bips au démarrage ?",
    "laptop":                   "Vous utilisez un ordinateur portable (laptop) ?",
    "batterie_ne_charge_pas":   "La batterie ne se charge pas ?",
    "pilotes_anciens":          "Les pilotes graphiques sont anciens / pas à jour ?",
    "peripherique_usb_non_detecte": "Un périphérique USB n'est pas détecté ?",
    "pas_de_son":               "Il n'y a pas de son ?",
    "pilotes_audio_absents":    "Les pilotes audio sont absents / non installés ?",
}

# Traduction des diagnostics → texte lisible
DIAGNOSTICS_FR = {
    "probleme_ram":                  "🔧 Problème RAM détecté",
    "probleme_alimentation":         "⚡ Problème d'alimentation",
    "probleme_carte_graphique":      "🖥️ Problème de carte graphique",
    "surchauffe_processeur":         "🌡️ Surchauffe du processeur",
    "manque_memoire":                "💾 Mémoire insuffisante",
    "wifi_eteint":                   "📶 Wi-Fi désactivé",
    "probleme_routeur":              "🌐 Problème routeur/box",
    "espace_insuffisant":            "💿 Espace disque insuffisant",
    "disque_defaillant":             "💥 Disque dur défaillant",
    "bsod":                          "💻 Écran bleu (BSOD)",
    "virus_malware":                 "🦠 Virus ou malware détecté",
    "probleme_clavier":              "⌨️ Problème clavier",
    "probleme_imprimante":           "🖨️ Problème imprimante",
    "surchauffe_generale":           "🔥 Surchauffe générale",
    "erreur_bios":                   "⚙️ Erreur BIOS",
    "probleme_batterie":             "🔋 Problème batterie",
    "pilotes_graphiques_obsoletes":  "🎮 Pilotes graphiques obsolètes",
    "probleme_port_usb":             "🔌 Problème port USB",
    "probleme_audio":                "🔊 Problème audio",
}

def get_all_conditions():
    """Retourne tous les faits possibles (conditions de toutes les règles)"""
    all_conds = set()
    for r in REGLES:
        for c in r["conditions"]:
            all_conds.add(c)
    return all_conds

def get_pending_questions():
    """Retourne les conditions non encore connues qui pourraient déclencher de nouvelles règles"""
    pending = []
    known = set(faits)
    for regle in REGLES:
        conds = regle["conditions"]
        # Si certaines conditions sont déjà vraies, demander les autres
        known_in_rule = [c for c in conds if c in known]
        unknown_in_rule = [c for c in conds if c not in known]
        if len(known_in_rule) >= 0 and unknown_in_rule:
            for u in unknown_in_rule:
                if u not in pending:
                    pending.append(u)
    return pending


# ══════════════════════════════════════════════════════════════════════════════
#  FENÊTRE PRINCIPALE
# ══════════════════════════════════════════════════════════════════════════════

class ExpertChatbot(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.theme = "dark"
        self.C = DARK

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.title("DiagnoPC — Système Expert")
        self.geometry("900x700")
        self.minsize(700, 500)
        self.configure(fg_color=self.C["bg"])

        # État de la session
        self.session_faits = []
        self.asked_questions = set()
        self.diagnostics_trouves = []
        self.mode_guide = True   # True = questions guidées actif
        self.question_en_cours = None

        self._build_ui()
        self._welcome()

    # ──────────────────────────────────────────────────────────────────────────
    #  CONSTRUCTION DE L'INTERFACE
    # ──────────────────────────────────────────────────────────────────────────
    def _build_ui(self):
        C = self.C

        # ── HEADER ────────────────────────────────────────────────────────────
        self.header = ctk.CTkFrame(self, fg_color=C["surface"], corner_radius=0, height=64)
        self.header.pack(fill="x", side="top")
        self.header.pack_propagate(False)

        # Logo + titre
        logo_frame = ctk.CTkFrame(self.header, fg_color="transparent")
        logo_frame.pack(side="left", padx=20, pady=10)

        self.icon_label = ctk.CTkLabel(
            logo_frame,
            text="🖥️",
            font=ctk.CTkFont(size=28),
        )
        self.icon_label.pack(side="left", padx=(0, 10))

        title_block = ctk.CTkFrame(logo_frame, fg_color="transparent")
        title_block.pack(side="left")
        ctk.CTkLabel(
            title_block,
            text="DiagnoPC",
            font=ctk.CTkFont(family="Helvetica", size=18, weight="bold"),
            text_color=C["text"],
        ).pack(anchor="w")
        ctk.CTkLabel(
            title_block,
            text="Système Expert en Maintenance Informatique",
            font=ctk.CTkFont(size=11),
            text_color=C["text_dim"],
        ).pack(anchor="w")

        # Boutons header (droite)
        btn_frame = ctk.CTkFrame(self.header, fg_color="transparent")
        btn_frame.pack(side="right", padx=16, pady=10)

        self.theme_btn = ctk.CTkButton(
            btn_frame,
            text="☀️  Mode clair",
            width=120, height=32,
            corner_radius=16,
            fg_color=C["surface2"],
            hover_color=C["border"],
            text_color=C["text"],
            font=ctk.CTkFont(size=12),
            command=self._toggle_theme,
        )
        self.theme_btn.pack(side="right", padx=6)

        self.reset_btn = ctk.CTkButton(
            btn_frame,
            text="↺  Nouvelle session",
            width=140, height=32,
            corner_radius=16,
            fg_color=C["surface2"],
            hover_color=C["border"],
            text_color=C["text"],
            font=ctk.CTkFont(size=12),
            command=self._reset_session,
        )
        self.reset_btn.pack(side="right", padx=0)

        # ── ZONE DE CHAT ──────────────────────────────────────────────────────
        chat_outer = ctk.CTkFrame(self, fg_color=C["bg"])
        chat_outer.pack(fill="both", expand=True, padx=12, pady=(8, 0))

        self.chat_frame = ctk.CTkScrollableFrame(
            chat_outer,
            fg_color=C["bg"],
            scrollbar_button_color=C["border"],
            scrollbar_button_hover_color=C["accent"],
            corner_radius=12,
        )
        self.chat_frame.pack(fill="both", expand=True)

        # ── ZONE DE TAGS (faits actifs) ───────────────────────────────────────
        self.tags_outer = ctk.CTkFrame(self, fg_color=C["surface"], corner_radius=0, height=44)
        self.tags_outer.pack(fill="x", side="bottom", before=chat_outer)
        self.tags_outer.pack_forget()  # caché au départ

        self.tags_label = ctk.CTkLabel(
            self.tags_outer,
            text="Symptômes détectés :",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=C["text_dim"],
        )
        self.tags_label.pack(side="left", padx=(12, 6), pady=10)

        self.tags_frame = ctk.CTkFrame(self.tags_outer, fg_color="transparent")
        self.tags_frame.pack(side="left", fill="x", expand=True, pady=6)

        # ── PANNEAU D'ENTRÉE ──────────────────────────────────────────────────
        input_panel = ctk.CTkFrame(self, fg_color=C["surface"], corner_radius=0, height=80)
        input_panel.pack(fill="x", side="bottom")
        input_panel.pack_propagate(False)

        input_inner = ctk.CTkFrame(input_panel, fg_color="transparent")
        input_inner.pack(fill="both", expand=True, padx=16, pady=12)

        # Boutons Oui/Non (cachés par défaut)
        self.yn_frame = ctk.CTkFrame(input_inner, fg_color="transparent")
        self.yn_frame.pack(side="right", padx=(8, 0))

        self.yes_btn = ctk.CTkButton(
            self.yn_frame, text="✓  Oui", width=90, height=42,
            corner_radius=10,
            fg_color=C["yes_btn"], hover_color="#27AE60",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=lambda: self._answer_yn(True),
        )
        self.yes_btn.pack(side="left", padx=4)

        self.no_btn = ctk.CTkButton(
            self.yn_frame, text="✗  Non", width=90, height=42,
            corner_radius=10,
            fg_color=C["no_btn"], hover_color="#C0392B",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=lambda: self._answer_yn(False),
        )
        self.no_btn.pack(side="left", padx=4)

        self.yn_frame.pack_forget()

        # Champ de texte libre
        self.input_entry = ctk.CTkEntry(
            input_inner,
            placeholder_text="Décrivez votre problème ou tapez un symptôme...",
            height=42,
            corner_radius=10,
            fg_color=C["input_bg"],
            border_color=C["border"],
            text_color=C["text"],
            placeholder_text_color=C["text_dim"],
            font=ctk.CTkFont(size=13),
        )
        self.input_entry.pack(side="left", fill="x", expand=True)
        self.input_entry.bind("<Return>", lambda e: self._send_free_text())

        self.send_btn = ctk.CTkButton(
            input_inner,
            text="→",
            width=48, height=42,
            corner_radius=10,
            fg_color=C["button"],
            hover_color=C["button_hover"],
            font=ctk.CTkFont(size=20, weight="bold"),
            command=self._send_free_text,
        )
        self.send_btn.pack(side="left", padx=(8, 0))

    # ──────────────────────────────────────────────────────────────────────────
    #  BULLES DE MESSAGE
    # ──────────────────────────────────────────────────────────────────────────
    def _add_bot_message(self, text, color=None, delay=0):
        """Ajoute un message du bot avec animation de frappe"""
        def _do():
            if delay > 0:
                time.sleep(delay)
            C = self.C
            row = ctk.CTkFrame(self.chat_frame, fg_color="transparent")
            row.pack(fill="x", pady=(4, 2), padx=8)

            avatar = ctk.CTkLabel(
                row, text="🤖", font=ctk.CTkFont(size=20),
                width=36,
            )
            avatar.pack(side="left", anchor="n", padx=(0, 8), pady=4)

            bubble = ctk.CTkFrame(
                row,
                fg_color=color or C["bot_bubble"],
                corner_radius=14,
                border_width=1,
                border_color=C["border"],
            )
            bubble.pack(side="left", anchor="w", padx=(0, 80))

            lbl = ctk.CTkLabel(
                bubble,
                text=text,
                font=ctk.CTkFont(size=13),
                text_color=C["text"],
                wraplength=520,
                justify="left",
                padx=14, pady=10,
            )
            lbl.pack()
            self._scroll_bottom()
        if delay > 0:
            threading.Thread(target=_do, daemon=True).start()
        else:
            _do()

    def _add_user_message(self, text):
        C = self.C
        row = ctk.CTkFrame(self.chat_frame, fg_color="transparent")
        row.pack(fill="x", pady=(4, 2), padx=8)

        bubble = ctk.CTkFrame(
            row,
            fg_color=C["user_bubble"],
            corner_radius=14,
        )
        bubble.pack(side="right", anchor="e", padx=(80, 0))

        ctk.CTkLabel(
            bubble,
            text=text,
            font=ctk.CTkFont(size=13),
            text_color="#FFFFFF" if self.theme == "dark" else "#FFFFFF",
            wraplength=480,
            justify="right",
            padx=14, pady=10,
        ).pack()

        avatar = ctk.CTkLabel(
            row, text="👤", font=ctk.CTkFont(size=20),
            width=36,
        )
        avatar.pack(side="right", anchor="n", padx=(8, 0), pady=4)
        self._scroll_bottom()

    def _add_diagnostic_card(self, conclusion, solution, rule_id):
        C = self.C
        row = ctk.CTkFrame(self.chat_frame, fg_color="transparent")
        row.pack(fill="x", pady=(6, 2), padx=8)

        avatar = ctk.CTkLabel(row, text="🔍", font=ctk.CTkFont(size=20), width=36)
        avatar.pack(side="left", anchor="n", padx=(0, 8), pady=4)

        card = ctk.CTkFrame(
            row,
            fg_color=C["surface2"],
            corner_radius=14,
            border_width=2,
            border_color=C["accent"],
        )
        card.pack(side="left", anchor="w", padx=(0, 80), fill="x", expand=False)

        # Titre du diagnostic
        diag_fr = DIAGNOSTICS_FR.get(conclusion, conclusion.replace("_", " ").title())
        ctk.CTkLabel(
            card,
            text=diag_fr,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=C["accent"],
            padx=14, pady=(10, 2),
        ).pack(anchor="w")

        # Badge règle
        badge_row = ctk.CTkFrame(card, fg_color="transparent")
        badge_row.pack(anchor="w", padx=14, pady=(0, 4))
        ctk.CTkLabel(
            badge_row,
            text=f" {rule_id} ",
            font=ctk.CTkFont(size=10, weight="bold"),
            fg_color=C["tag_bg"],
            text_color=C["text_dim"],
            corner_radius=6,
            padx=4, pady=2,
        ).pack(side="left")

        # Séparateur visuel
        sep = ctk.CTkFrame(card, fg_color=C["border"], height=1)
        sep.pack(fill="x", padx=14, pady=4)

        # Solution
        ctk.CTkLabel(
            card,
            text=f"💡  {solution}",
            font=ctk.CTkFont(size=12),
            text_color=C["text"],
            wraplength=480,
            justify="left",
            padx=14, pady=(2, 12),
        ).pack(anchor="w")

        self._scroll_bottom()

    def _add_separator(self, label=""):
        C = self.C
        sep_row = ctk.CTkFrame(self.chat_frame, fg_color="transparent")
        sep_row.pack(fill="x", pady=8, padx=24)
        line_l = ctk.CTkFrame(sep_row, fg_color=C["border"], height=1)
        line_l.pack(side="left", fill="x", expand=True, pady=6)
        if label:
            ctk.CTkLabel(sep_row, text=f"  {label}  ", font=ctk.CTkFont(size=10), text_color=C["text_dim"]).pack(side="left")
            line_r = ctk.CTkFrame(sep_row, fg_color=C["border"], height=1)
            line_r.pack(side="left", fill="x", expand=True, pady=6)

    def _scroll_bottom(self):
        self.after(80, lambda: self.chat_frame._parent_canvas.yview_moveto(1.0))

    # ──────────────────────────────────────────────────────────────────────────
    #  LOGIQUE CHATBOT
    # ──────────────────────────────────────────────────────────────────────────
    def _welcome(self):
        self._add_bot_message("Bonjour ! 👋 Je suis **DiagnoPC**, votre assistant de diagnostic informatique.")
        self._add_bot_message(
            "Je peux vous aider à identifier les pannes et problèmes de votre ordinateur.\n\n"
            "Vous pouvez :\n"
            "  • Répondre à mes questions guidées (Oui / Non)\n"
            "  • Taper librement votre problème dans la zone de texte",
            delay=0.5
        )
        self._add_bot_message("Par où souhaitez-vous commencer ?", delay=1.0)
        self.after(1100, self._show_start_options)

    def _show_start_options(self):
        """Affiche les boutons de démarrage"""
        C = self.C
        row = ctk.CTkFrame(self.chat_frame, fg_color="transparent")
        row.pack(fill="x", pady=(4, 8), padx=50)

        btn1 = ctk.CTkButton(
            row,
            text="🔍  Diagnostic guidé (questions Oui/Non)",
            height=40, corner_radius=10,
            fg_color=C["accent"], hover_color=C["button_hover"],
            font=ctk.CTkFont(size=13),
            command=lambda: self._start_guided(row),
        )
        btn1.pack(fill="x", pady=3)

        btn2 = ctk.CTkButton(
            row,
            text="⌨️  Décrire mon problème librement",
            height=40, corner_radius=10,
            fg_color=C["surface2"], hover_color=C["border"],
            text_color=C["text"],
            font=ctk.CTkFont(size=13),
            command=lambda: self._start_free(row),
        )
        btn2.pack(fill="x", pady=3)
        self._scroll_bottom()

    def _start_guided(self, start_row):
        start_row.destroy()
        self._add_user_message("🔍 Diagnostic guidé")
        self._add_bot_message("Parfait ! Je vais vous poser quelques questions.\nRépondez simplement par **Oui** ou **Non**.")
        self.after(400, self._ask_next_question)

    def _start_free(self, start_row):
        start_row.destroy()
        self._add_user_message("⌨️ Décrire mon problème")
        self._add_bot_message(
            "D'accord ! Décrivez votre problème dans le champ en bas.\n\n"
            "Exemples : *« mon PC ne démarre pas »*, *« PC très lent »*, *« pas de son »*..."
        )
        self.input_entry.focus()

    def _ask_next_question(self):
        """Trouve et pose la prochaine question pertinente"""
        C = self.C
        # Trouver les conditions non encore questionnées
        for regle in REGLES:
            for cond in regle["conditions"]:
                if cond not in self.asked_questions and cond not in self.C:
                    # Choisir une question prioritaire (conditions partiellement satisfaites d'abord)
                    break

        # Chercher les questions les plus pertinentes
        scores = {}
        for regle in REGLES:
            known = [c for c in regle["conditions"] if fait_existe(c)]
            unknown = [c for c in regle["conditions"] if not fait_existe(c) and c not in self.asked_questions]
            if unknown:
                score = len(known)  # plus de conditions déjà connues = plus pertinent
                for u in unknown:
                    scores[u] = max(scores.get(u, 0), score)

        if not scores:
            self._run_inference()
            return

        # Poser la question la plus pertinente
        best = max(scores, key=scores.get)
        self.asked_questions.add(best)
        self.question_en_cours = best

        question_text = QUESTIONS_MAP.get(best, best.replace("_", " ").title() + " ?")
        self._add_bot_message(question_text)
        self.yn_frame.pack(side="right", padx=(8, 0))
        self.input_entry.pack_forget()
        self.send_btn.pack_forget()

    def _answer_yn(self, yes: bool):
        """Traite la réponse Oui/Non"""
        self.yn_frame.pack_forget()
        self.input_entry.pack(side="left", fill="x", expand=True)
        self.send_btn.pack(side="left", padx=(8, 0))

        question_text = QUESTIONS_MAP.get(self.question_en_cours, self.question_en_cours)
        self._add_user_message("✓ Oui" if yes else "✗ Non")

        if yes:
            ajouter_fait(self.question_en_cours)
            self._update_tags()
            # Déléguer entièrement au moteur d'inférence dédié
            new_results = lancer_moteur(verbose=False)
            for regle in new_results:
                self._show_diagnostic(regle)
            if new_results:
                self._add_bot_message("Je continue à chercher d'autres problèmes potentiels...", delay=0.3)

        # Décider si on continue les questions
        remaining = self._count_remaining_questions()
        if remaining > 0 and len(self.diagnostics_trouves) < 5:
            self.after(300, self._ask_next_question)
        else:
            self.after(300, self._run_inference)

    def _count_remaining_questions(self):
        count = 0
        for regle in REGLES:
            for cond in regle["conditions"]:
                if cond not in self.asked_questions and not fait_existe(cond):
                    count += 1
                    break
        return count

    def _send_free_text(self):
        """Traite la saisie libre de l'utilisateur"""
        text = self.input_entry.get().strip()
        if not text:
            return
        self.input_entry.delete(0, "end")
        self._add_user_message(text)

        # Correspondance mots-clés → faits
        text_lower = text.lower()
        detected = []

        mapping = {
            "ne démarre pas":       ["pc_ne_demarre_pas"],
            "ne demarre pas":       ["pc_ne_demarre_pas"],
            "démarrage":            ["pc_ne_demarre_pas"],
            "lent":                 ["pc_lent"],
            "lenteur":              ["pc_lent"],
            "écran noir":           ["pc_allume", "ecran_noir"],
            "ecran noir":           ["pc_allume", "ecran_noir"],
            "écran bleu":           ["ecran_bleu"],
            "ecran bleu":           ["ecran_bleu"],
            "bsod":                 ["ecran_bleu", "plantage_frequent"],
            "ventilateur":          ["ventilateur_tourne"],
            "ventilo":              ["ventilateur_tourne"],
            "pas de connexion":     ["pas_de_connexion"],
            "pas internet":         ["pas_de_connexion"],
            "internet ne":          ["pas_de_connexion"],
            "wifi":                 ["pas_de_connexion", "wifi_active"],
            "son":                  ["pas_de_son"],
            "audio":                ["pas_de_son", "pilotes_audio_absents"],
            "clavier":              ["clavier_non_detecte"],
            "imprimante":           ["imprimante_non_detectee"],
            "usb":                  ["peripherique_usb_non_detecte"],
            "batterie":             ["laptop", "batterie_ne_charge_pas"],
            "charge pas":           ["batterie_ne_charge_pas"],
            "chauffe":              ["temperature_elevee"],
            "surchauffe":           ["temperature_elevee", "pc_eteint_brusquement"],
            "bip":                  ["bip_sonore", "pc_ne_demarre_pas"],
            "virus":                ["virus_malware", "programmes_inconnus", "pc_lent"],
            "malware":              ["programmes_inconnus", "pc_lent"],
            "disque":               ["bruits_disque", "fichiers_inaccessibles"],
            "fichier":              ["fichiers_inaccessibles"],
            "plantage":             ["plantage_frequent"],
            "plante":               ["plantage_frequent"],
            "s'éteint":             ["pc_eteint_brusquement"],
            "s'eteint":             ["pc_eteint_brusquement"],
            "écran clignote":       ["ecran_clignote"],
            "ecran clignote":       ["ecran_clignote"],
            "portable":             ["laptop"],
            "laptop":               ["laptop"],
            "ram":                  ["ram_insuffisante"],
            "mémoire":              ["ram_insuffisante"],
            "memoire":              ["ram_insuffisante"],
            "cpu":                  ["cpu_usage_eleve"],
            "processeur":           ["cpu_usage_eleve"],
            "disque plein":         ["disque_plein", "pc_lent"],
            "espace":               ["disque_plein"],
        }

        for keyword, facts_list in mapping.items():
            if keyword in text_lower:
                for f in facts_list:
                    if not fait_existe(f):
                        ajouter_fait(f)
                        detected.append(f)

        if detected:
            detected_fr = [QUESTIONS_MAP.get(d, d.replace("_", " ")) for d in detected]
            self._add_bot_message(f"J'ai détecté les symptômes suivants :\n• " + "\n• ".join(detected_fr))
            self._update_tags()
            self.after(300, self._run_inference)
        else:
            self._add_bot_message(
                "Je n'ai pas reconnu de symptôme précis. Essayez des termes comme :\n"
                "  *lent, écran noir, pas internet, bip, surchauffe, batterie...*\n\n"
                "Ou utilisez le **diagnostic guidé** pour répondre à mes questions."
            )
            self.after(500, self._show_start_options)

    def _run_inference(self):
        """Lance le moteur d'inférence et affiche les résultats"""
        self._add_separator("Analyse en cours...")
        self._add_bot_message("🔄 Analyse de votre problème...")

        def _process():
            time.sleep(0.6)
            # Délégation complète au moteur d'inférence dédié
            results = lancer_moteur(verbose=False)
            self.after(0, lambda: self._show_results(results))

        threading.Thread(target=_process, daemon=True).start()

    def _show_diagnostic(self, regle):
        if regle["id"] not in [r["id"] for r in self.diagnostics_trouves]:
            self.diagnostics_trouves.append(regle)
            self._add_diagnostic_card(regle["conclusion"], regle["solution"], regle["id"])

    def _show_results(self, new_results):
        # Filtrer ceux déjà affichés
        already = {r["id"] for r in self.diagnostics_trouves}
        fresh = [r for r in new_results if r["id"] not in already]

        if fresh:
            self._add_separator(f"{len(fresh)} diagnostic(s) trouvé(s)")
            for regle in fresh:
                self.diagnostics_trouves.append(regle)
                self._add_diagnostic_card(regle["conclusion"], regle["solution"], regle["id"])
                time.sleep(0.1)
            self._add_bot_message(
                f"✅ Diagnostic terminé. J'ai identifié **{len(self.diagnostics_trouves)} problème(s)**.\n"
                "Consultez les cartes ci-dessus pour les solutions recommandées.",
                delay=0.3
            )
        elif self.diagnostics_trouves:
            self._add_bot_message("✅ L'analyse est complète. Consultez les diagnostics trouvés ci-dessus.")
        else:
            self._add_bot_message(
                "🤔 Je n'ai pas pu identifier de problème précis avec les informations fournies.\n"
                "Essayez d'ajouter plus de symptômes ou relancez un diagnostic guidé."
            )

        self._add_bot_message("Souhaitez-vous démarrer une nouvelle session ?", delay=0.8)
        self.after(900, self._show_new_session_btn)

    def _show_new_session_btn(self):
        C = self.C
        row = ctk.CTkFrame(self.chat_frame, fg_color="transparent")
        row.pack(fill="x", pady=(4, 8), padx=50)
        ctk.CTkButton(
            row,
            text="↺  Nouvelle session",
            height=38, corner_radius=10,
            fg_color=C["surface2"], hover_color=C["border"],
            text_color=C["text"],
            font=ctk.CTkFont(size=13),
            command=self._reset_session,
        ).pack(fill="x")
        self._scroll_bottom()

    # ──────────────────────────────────────────────────────────────────────────
    #  GESTION DES TAGS
    # ──────────────────────────────────────────────────────────────────────────
    def _update_tags(self):
        C = self.C
        # Vider les tags existants
        for widget in self.tags_frame.winfo_children():
            widget.destroy()

        # Afficher seulement les faits "symptômes" (conditions des règles)
        symptomes = [f for f in faits if f in QUESTIONS_MAP]
        if symptomes:
            self.tags_outer.pack(fill="x", side="bottom", before=self.chat_frame.master)
            for s in symptomes[:8]:  # max 8 tags
                label = QUESTIONS_MAP.get(s, s).replace(" ?", "")
                tag = ctk.CTkLabel(
                    self.tags_frame,
                    text=f"  {label}  ",
                    font=ctk.CTkFont(size=10),
                    fg_color=C["tag_bg"],
                    text_color=C["accent"],
                    corner_radius=10,
                    padx=2, pady=2,
                )
                tag.pack(side="left", padx=3)

    # ──────────────────────────────────────────────────────────────────────────
    #  RESET & THÈME
    # ──────────────────────────────────────────────────────────────────────────
    def _reset_session(self):
        reinitialiser_moteur()
        self.asked_questions.clear()
        self.diagnostics_trouves.clear()
        self.question_en_cours = None
        for widget in self.chat_frame.winfo_children():
            widget.destroy()
        for widget in self.tags_frame.winfo_children():
            widget.destroy()
        self.tags_outer.pack_forget()
        self._welcome()

    def _toggle_theme(self):
        if self.theme == "dark":
            self.theme = "light"
            self.C = LIGHT
            ctk.set_appearance_mode("light")
            self.theme_btn.configure(text="🌙  Mode sombre")
        else:
            self.theme = "dark"
            self.C = DARK
            ctk.set_appearance_mode("dark")
            self.theme_btn.configure(text="☀️  Mode clair")
        # Relancer l'UI (rebuild)
        self._rebuild_ui()

    def _rebuild_ui(self):
        """Recrée l'UI avec les nouvelles couleurs"""
        for widget in self.winfo_children():
            widget.destroy()
        self.configure(fg_color=self.C["bg"])
        self._build_ui()
        self._reset_session()


# ══════════════════════════════════════════════════════════════════════════════
#  POINT D'ENTRÉE
# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    app = ExpertChatbot()
    app.mainloop()
