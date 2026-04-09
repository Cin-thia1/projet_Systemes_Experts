# gui.py - Interface graphique du système expert SEMI
# Système Expert de Maintenance Informatique

import customtkinter as ctk
import threading
import time
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from facts import faits, fait_existe, QUESTIONS, DIAGNOSTICS, CATEGORIES, label_certitude, MOTS_CLES, detecter_faits
from rules import REGLES
from inference_engine import (
    lancer_moteur, reinitialiser_moteur, get_certitude,
    assert_fact, ajouter_fait_moteur, diagnostics_possibles
)

# ══════════════════════════════════════════════════════════════════════════════
#  PALETTES DE COULEURS
# ══════════════════════════════════════════════════════════════════════════════

DARK = {
    "bg":           "#0F1117",
    "surface":      "#1A1D27",
    "surface2":     "#22263A",
    "border":       "#2E3250",
    "accent":       "#4F8EF7",
    "user_bubble":  "#1E3A5F",
    "bot_bubble":   "#1C1F2E",
    "text":         "#E8EAF6",
    "text_dim":     "#7B82A8",
    "success":      "#43D9A2",
    "warning":      "#F7C948",
    "danger":       "#E74C3C",
    "input_bg":     "#181B28",
    "button":       "#4F8EF7",
    "button_hover": "#3A78E0",
    "yes_btn":      "#2ECC71",
    "no_btn":       "#E74C3C",
    "tag_bg":       "#2A2E45",
    "card_border":  "#4F8EF7",
}

LIGHT = {
    "bg":           "#F0F4FF",
    "surface":      "#FFFFFF",
    "surface2":     "#E8EEFF",
    "border":       "#C5CCED",
    "accent":       "#3B72E8",
    "user_bubble":  "#3B72E8",
    "bot_bubble":   "#FFFFFF",
    "text":         "#1A1D35",
    "text_dim":     "#6B7280",
    "success":      "#27AE60",
    "warning":      "#F39C12",
    "danger":       "#C0392B",
    "input_bg":     "#F8F9FF",
    "button":       "#3B72E8",
    "button_hover": "#2A5FD0",
    "yes_btn":      "#27AE60",
    "no_btn":       "#E74C3C",
    "tag_bg":       "#E2E7FF",
    "card_border":  "#3B72E8",
}

CERTITUDE_COULEURS = {
    "Quasi certain": "#E74C3C",
    "Très probable": "#E67E22",
    "Probable":      "#F1C40F",
    "Possible":      "#2ECC71",
    "À vérifier":   "#95A5A6",
}


# ══════════════════════════════════════════════════════════════════════════════
#  FENÊTRE PRINCIPALE
# ══════════════════════════════════════════════════════════════════════════════

class SEMI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.theme = "dark"
        self.C     = DARK

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.title("SEMI — Système Expert de Maintenance Informatique")
        self.geometry("920x720")
        self.minsize(720, 520)
        self.configure(fg_color=self.C["bg"])

        self.asked_questions     = set()
        self.diagnostics_trouves = []
        self.question_en_cours   = None

        self._build_ui()
        self._welcome()

    # ──────────────────────────────────────────────────────────────────────────
    #  CONSTRUCTION DE L'INTERFACE
    # ──────────────────────────────────────────────────────────────────────────

    def _build_ui(self):
        C = self.C

        # ── EN-TÊTE ───────────────────────────────────────────────────────────
        self.header = ctk.CTkFrame(self, fg_color=C["surface"], corner_radius=0, height=62)
        self.header.pack(fill="x", side="top")
        self.header.pack_propagate(False)

        left = ctk.CTkFrame(self.header, fg_color="transparent")
        left.pack(side="left", padx=20, pady=10)

        ctk.CTkLabel(
            left, text="SEMI",
            font=ctk.CTkFont(family="Helvetica", size=19, weight="bold"),
            text_color=C["accent"],
        ).pack(side="left", padx=(0, 10))

        ctk.CTkLabel(
            left, text="Système Expert de Maintenance Informatique",
            font=ctk.CTkFont(size=11),
            text_color=C["text_dim"],
        ).pack(side="left")

        right = ctk.CTkFrame(self.header, fg_color="transparent")
        right.pack(side="right", padx=16)

        self.theme_btn = ctk.CTkButton(
            right, text="Mode clair", width=110, height=30, corner_radius=14,
            fg_color=C["surface2"], hover_color=C["border"], text_color=C["text"],
            font=ctk.CTkFont(size=12), command=self._toggle_theme,
        )
        self.theme_btn.pack(side="right", padx=6)

        ctk.CTkButton(
            right, text="Nouvelle session", width=130, height=30, corner_radius=14,
            fg_color=C["surface2"], hover_color=C["border"], text_color=C["text"],
            font=ctk.CTkFont(size=12), command=self._reset_session,
        ).pack(side="right")

        # ── ZONE DE SAISIE (packée en bottom en premier) ─────────────────────
        input_panel = ctk.CTkFrame(self, fg_color=C["surface"], corner_radius=0, height=72)
        input_panel.pack(fill="x", side="bottom")
        input_panel.pack_propagate(False)

        # ── BARRE DE SYMPTÔMES (bottom, au-dessus de input) ───────────────────
        self.tags_outer = ctk.CTkFrame(self, fg_color=C["surface"], corner_radius=0, height=40)
        self.tags_outer.pack_propagate(False)
        ctk.CTkLabel(
            self.tags_outer, text="Symptômes :",
            font=ctk.CTkFont(size=11), text_color=C["text_dim"],
        ).pack(side="left", padx=(12, 6))
        self.tags_frame = ctk.CTkFrame(self.tags_outer, fg_color="transparent")
        self.tags_frame.pack(side="left", fill="x", expand=True, pady=5)
        # NE PAS packer tags_outer ici — il sera affiché par _update_tags

        # ── ZONE DE CHAT (fill restant) ───────────────────────────────────────
        self.chat_frame = ctk.CTkScrollableFrame(
            self, fg_color=C["bg"],
            scrollbar_button_color=C["border"],
            scrollbar_button_hover_color=C["accent"],
            corner_radius=0,
        )
        self.chat_frame.pack(fill="both", expand=True, padx=12, pady=(8, 0))

        inner = ctk.CTkFrame(input_panel, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=16, pady=14)

        # Boutons Oui / Non
        self.yn_frame = ctk.CTkFrame(inner, fg_color="transparent")
        ctk.CTkButton(
            self.yn_frame, text="✔ Oui", width=84, height=40, corner_radius=8,
            fg_color=C["yes_btn"], hover_color="#27AE60",
            font=ctk.CTkFont(size=13, weight="bold"),
            command=lambda: self._answer_yn(True),
        ).pack(side="left", padx=4)
        ctk.CTkButton(
            self.yn_frame, text="✘ Non", width=84, height=40, corner_radius=8,
            fg_color=C["no_btn"], hover_color="#C0392B",
            font=ctk.CTkFont(size=13, weight="bold"),
            command=lambda: self._answer_yn(False),
        ).pack(side="left", padx=4)
        self.yn_frame.pack_forget()

        # Champ texte libre
        self.input_entry = ctk.CTkEntry(
            inner,
            placeholder_text="Décrivez votre problème (ex : PC lent, écran noir, pas de son…)",
            height=40, corner_radius=8,
            fg_color=C["input_bg"], border_color=C["border"],
            text_color=C["text"], placeholder_text_color=C["text_dim"],
            font=ctk.CTkFont(size=13),
        )
        self.input_entry.pack(side="left", fill="x", expand=True)
        self.input_entry.bind("<Return>", lambda e: self._send_free_text())

        ctk.CTkButton(
            inner, text="Envoyer", width=90, height=40, corner_radius=8,
            fg_color=C["button"], hover_color=C["button_hover"],
            font=ctk.CTkFont(size=13),
            command=self._send_free_text,
        ).pack(side="left", padx=(8, 0))

    # ──────────────────────────────────────────────────────────────────────────
    #  MESSAGES CHAT
    # ──────────────────────────────────────────────────────────────────────────

    def _add_bot_message(self, text, delay=0):
        def _do():
            if delay > 0:
                time.sleep(delay)
            C   = self.C
            row = ctk.CTkFrame(self.chat_frame, fg_color="transparent")
            row.pack(fill="x", pady=(3, 1), padx=8)

            ctk.CTkLabel(
                row, text="SEMI",
                font=ctk.CTkFont(size=10, weight="bold"),
                text_color=C["accent"], width=40,
            ).pack(side="left", anchor="n", padx=(0, 6), pady=6)

            bubble = ctk.CTkFrame(row, fg_color=C["bot_bubble"], corner_radius=12,
                                  border_width=1, border_color=C["border"])
            bubble.pack(side="left", anchor="w", padx=(0, 80))

            ctk.CTkLabel(
                bubble, text=text,
                font=ctk.CTkFont(size=13), text_color=C["text"],
                wraplength=520, justify="left", padx=12, pady=8,
            ).pack()
            self._scroll_bottom()

        if delay > 0:
            threading.Thread(target=_do, daemon=True).start()
        else:
            _do()

    def _add_user_message(self, text):
        C   = self.C
        row = ctk.CTkFrame(self.chat_frame, fg_color="transparent")
        row.pack(fill="x", pady=(3, 1), padx=8)

        bubble = ctk.CTkFrame(row, fg_color=C["user_bubble"], corner_radius=12)
        bubble.pack(side="right", anchor="e", padx=(80, 0))

        ctk.CTkLabel(
            bubble, text=text,
            font=ctk.CTkFont(size=13), text_color="#FFFFFF",
            wraplength=480, justify="right", padx=12, pady=8,
        ).pack()

        ctk.CTkLabel(
            row, text="Vous",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=C["text_dim"], width=44,
        ).pack(side="right", anchor="n", padx=(6, 0), pady=6)
        self._scroll_bottom()

    def _add_diagnostic_card(self, regle):
        C = self.C

        conclusion    = regle["conclusion"]
        solution      = regle["solution"]
        rule_id       = regle["id"]
        categorie     = regle.get("categorie", "")
        certitude_val = regle.get("_certitude_calculee", regle.get("certitude", 0.5))
        label_cert    = label_certitude(certitude_val)
        couleur_cert  = CERTITUDE_COULEURS.get(label_cert, "#95A5A6")
        diag_fr       = DIAGNOSTICS.get(conclusion, conclusion.replace("_", " ").title())
        cat_fr        = CATEGORIES.get(categorie, categorie)

        # Couleur de la bordure selon le niveau de certitude
        border_color = couleur_cert if certitude_val >= 0.88 else C["card_border"]

        row = ctk.CTkFrame(self.chat_frame, fg_color="transparent")
        row.pack(fill="x", pady=(4, 2), padx=8)
        ctk.CTkLabel(row, text="", width=46).pack(side="left", anchor="n")

        card = ctk.CTkFrame(row, fg_color=C["surface2"], corner_radius=12,
                            border_width=2, border_color=border_color)
        card.pack(side="left", anchor="w", padx=(0, 80), fill="x", expand=True)

        # En-tête : diagnostic + badge certitude
        header = ctk.CTkFrame(card, fg_color="transparent")
        header.pack(fill="x", padx=12, pady=(10, 2))

        ctk.CTkLabel(
            header, text=diag_fr,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=C["accent"],
        ).pack(side="left")

        ctk.CTkLabel(
            header,
            text=f"  {label_cert} — {certitude_val:.0%}  ",
            font=ctk.CTkFont(size=10, weight="bold"),
            fg_color=couleur_cert, text_color="#FFFFFF",
            corner_radius=6, padx=4, pady=2,
        ).pack(side="right")

        # Badges : règle + catégorie
        badges = ctk.CTkFrame(card, fg_color="transparent")
        badges.pack(anchor="w", padx=12, pady=(0, 4))
        for txt in [rule_id, cat_fr]:
            ctk.CTkLabel(
                badges, text=f"  {txt}  ",
                font=ctk.CTkFont(size=10),
                fg_color=C["tag_bg"], text_color=C["text_dim"],
                corner_radius=5, padx=2, pady=1,
            ).pack(side="left", padx=(0, 4))

        # Séparateur
        ctk.CTkFrame(card, fg_color=C["border"], height=1).pack(fill="x", padx=12, pady=3)

        # Solution
        ctk.CTkLabel(
            card, text=solution,
            font=ctk.CTkFont(size=12), text_color=C["text"],
            wraplength=500, justify="left", padx=12, pady=(2, 10),
        ).pack(anchor="w")

        self._scroll_bottom()

    def _add_separator(self, label=""):
        C   = self.C
        row = ctk.CTkFrame(self.chat_frame, fg_color="transparent")
        row.pack(fill="x", pady=6, padx=24)
        ctk.CTkFrame(row, fg_color=C["border"], height=1).pack(
            side="left", fill="x", expand=True, pady=5)
        if label:
            ctk.CTkLabel(
                row, text=f"  {label}  ",
                font=ctk.CTkFont(size=10), text_color=C["text_dim"],
            ).pack(side="left")
            ctk.CTkFrame(row, fg_color=C["border"], height=1).pack(
                side="left", fill="x", expand=True, pady=5)

    def _scroll_bottom(self):
        self.after(80, lambda: self.chat_frame._parent_canvas.yview_moveto(1.0))

    # ──────────────────────────────────────────────────────────────────────────
    #  LOGIQUE CHATBOT
    # ──────────────────────────────────────────────────────────────────────────

    def _welcome(self):
        self._add_bot_message(
            "Bonjour. Je suis SEMI, votre assistant de diagnostic informatique.\n\n"
            "Décrivez votre problème librement dans le champ de saisie, "
            "ou utilisez le diagnostic guidé pour répondre à mes questions."
        )
        self.after(600, self._show_start_options)

    def _show_start_options(self):
        C   = self.C
        row = ctk.CTkFrame(self.chat_frame, fg_color="transparent")
        row.pack(fill="x", pady=(4, 8), padx=60)

        ctk.CTkButton(
            row, text="🔍  Démarrer le diagnostic guidé",
            height=38, corner_radius=8,
            fg_color=C["button"], hover_color=C["button_hover"],
            font=ctk.CTkFont(size=13),
            command=lambda: self._start_guided(row),
        ).pack(fill="x", pady=3)

        ctk.CTkButton(
            row, text="✏  Décrire mon problème librement",
            height=38, corner_radius=8,
            fg_color=C["surface2"], hover_color=C["border"],
            text_color=C["text"], font=ctk.CTkFont(size=13),
            command=lambda: self._start_free(row),
        ).pack(fill="x", pady=3)

        self._scroll_bottom()

    def _start_guided(self, start_row):
        start_row.destroy()
        self._add_user_message("Diagnostic guidé")
        self._add_bot_message(
            "Je vais vous poser des questions une par une.\n"
            "Répondez simplement par Oui ou Non."
        )
        self.after(400, self._ask_next_question)

    def _start_free(self, start_row):
        start_row.destroy()
        self._add_user_message("Saisie libre")
        self._add_bot_message(
            "Décrivez votre problème dans le champ en bas.\n"
            "Exemples : « PC lent », « écran noir », « pas de son », « batterie ne charge pas »…"
        )
        self.input_entry.focus()

    def _ask_next_question(self):
        """
        Choisit la prochaine question à poser en privilégiant le fait inconnu
        qui débloque le plus de règles partiellement satisfaites.
        """
        scores = {}
        for regle in REGLES:
            known   = [c for c in regle["conditions"] if fait_existe(c)]
            unknown = [c for c in regle["conditions"]
                       if not fait_existe(c) and c not in self.asked_questions]
            for u in unknown:
                scores[u] = max(scores.get(u, 0), len(known))

        if not scores:
            self._run_inference()
            return

        best = max(scores, key=scores.get)
        self.asked_questions.add(best)
        self.question_en_cours = best

        question_text = QUESTIONS.get(best, best.replace("_", " ").capitalize() + " ?")
        self._add_bot_message(question_text)

        self.yn_frame.pack(side="right", padx=(8, 0))
        self.input_entry.pack_forget()

    def _answer_yn(self, yes: bool):
        self.yn_frame.pack_forget()
        self.input_entry.pack(side="left", fill="x", expand=True)
        self._add_user_message("Oui" if yes else "Non")

        if yes:
            assert_fact(self.question_en_cours)
            self._update_tags()
            new_results = lancer_moteur(verbose=False)
            for regle in new_results:
                self._show_diagnostic(regle)
            if new_results:
                self._add_bot_message(
                    "Diagnostic intermédiaire trouvé. Je continue l'analyse.", delay=0.2
                )

        remaining = self._count_remaining_questions()
        if remaining > 0 and len(self.diagnostics_trouves) < 10:
            self.after(300, self._ask_next_question)
        else:
            self.after(300, self._finaliser_diagnostic)

    def _count_remaining_questions(self):
        for regle in REGLES:
            for cond in regle["conditions"]:
                if cond not in self.asked_questions and not fait_existe(cond):
                    return 1
        return 0

    def _send_free_text(self):
        text = self.input_entry.get().strip()
        if not text:
            return
        self.input_entry.delete(0, "end")
        self._add_user_message(text)

        # Utilise le moteur NLP (normalisation + stemming + synonymes + mots-clés)
        result   = detecter_faits(text)
        detected = []
        for f in result["faits"]:
            if not fait_existe(f):
                assert_fact(f)
                detected.append(f)

        if detected:
            labels = result["labels"][:len(detected)]
            nlp_note = " (NLP)" if any(m == "nlp" for m in result["methode"]) else ""
            self._add_bot_message(
                f"Symptômes détectés{nlp_note} :\n— " + "\n— ".join(labels)
            )
            self._update_tags()
            self.after(300, self._run_inference)
        else:
            # Afficher les tokens pour aider l'utilisateur
            tokens_info = ""
            if result["tokens"]:
                tokens_info = f"\nMots analysés : {', '.join(result['tokens'][:8])}"
            self._add_bot_message(
                "Aucun symptôme reconnu dans votre description." + tokens_info + "\n\n"
                "Essayez des termes plus directs comme :\n"
                "« lent », « ne démarre pas », « écran noir », « pas internet »,\n"
                "« batterie », « surchauffe », « virus », « son »…\n\n"
                "Ou utilisez le diagnostic guidé."
            )
            self.after(500, self._show_start_options)

    def _finaliser_diagnostic(self):
        """
        Fin du mode guidé : résume les diagnostics déjà trouvés en temps réel.
        Ne relance PAS lancer_moteur() pour éviter le retour vide (bug).
        """
        if self.diagnostics_trouves:
            total = len(self.diagnostics_trouves)
            self._add_separator(f"Diagnostic terminé — {total} problème(s)")
            self._add_bot_message(
                "Analyse complète — " + str(total) + " problème(s) identifié(s).\n"
                "Consultez les cartes ci-dessus pour les solutions.",
                delay=0.3
            )
        else:
            self._add_separator("Fin de l'analyse")
            self._add_bot_message(
                "Aucun problème identifié avec les réponses fournies.\n"
                "Essayez la saisie libre ou recommencez le diagnostic guidé.",
                delay=0.3
            )
        self.after(800, self._show_new_session_btn)

    def _run_inference(self):
        """Utilisé uniquement en mode saisie libre."""
        self._add_separator("Analyse en cours")
        self._add_bot_message("Analyse en cours…")

        def _process():
            time.sleep(0.5)
            results = lancer_moteur(verbose=False)
            self.after(0, lambda: self._show_results(results))

        threading.Thread(target=_process, daemon=True).start()

    def _show_diagnostic(self, regle):
        if regle["id"] not in [r["id"] for r in self.diagnostics_trouves]:
            self.diagnostics_trouves.append(regle)
            self._add_diagnostic_card(regle)

    def _show_results(self, new_results):
        already = {r["id"] for r in self.diagnostics_trouves}
        fresh   = [r for r in new_results if r["id"] not in already]

        if fresh:
            self._add_separator(f"{len(fresh)} diagnostic(s) trouvé(s)")
            for regle in fresh:
                self.diagnostics_trouves.append(regle)
                self._add_diagnostic_card(regle)
            total = len(self.diagnostics_trouves)
            self._add_bot_message(
                f"Analyse terminée — {total} problème(s) identifié(s).\n"
                "Consultez les cartes ci-dessus pour les solutions.",
                delay=0.3
            )
        elif self.diagnostics_trouves:
            self._add_bot_message("Analyse complète. Consultez les diagnostics ci-dessus.")
        else:
            self._add_bot_message(
                "Aucun problème identifié avec les informations fournies.\n"
                "Ajoutez d'autres symptômes ou relancez le diagnostic guidé."
            )

        self.after(800, self._show_new_session_btn)

    def _show_new_session_btn(self):
        C   = self.C
        row = ctk.CTkFrame(self.chat_frame, fg_color="transparent")
        row.pack(fill="x", pady=(4, 8), padx=60)
        ctk.CTkButton(
            row, text="Nouvelle session",
            height=36, corner_radius=8,
            fg_color=C["surface2"], hover_color=C["border"],
            text_color=C["text"], font=ctk.CTkFont(size=13),
            command=self._reset_session,
        ).pack(fill="x")
        self._scroll_bottom()

    # ──────────────────────────────────────────────────────────────────────────
    #  TAGS & THÈME
    # ──────────────────────────────────────────────────────────────────────────

    def _update_tags(self):
        C = self.C
        for w in self.tags_frame.winfo_children():
            w.destroy()

        symptomes = [f for f in faits if f in QUESTIONS]
        if symptomes:
            self.tags_outer.pack(fill="x", side="bottom")
            for s in symptomes[:12]:
                label = QUESTIONS.get(s, s).replace(" ?", "")
                ctk.CTkLabel(
                    self.tags_frame,
                    text=f"  {label}  ",
                    font=ctk.CTkFont(size=10),
                    fg_color=C["tag_bg"], text_color=C["accent"],
                    corner_radius=8, padx=2, pady=1,
                ).pack(side="left", padx=2)

    def _reset_session(self):
        reinitialiser_moteur()
        self.asked_questions.clear()
        self.diagnostics_trouves.clear()
        self.question_en_cours = None
        for w in self.chat_frame.winfo_children():
            w.destroy()
        for w in self.tags_frame.winfo_children():
            w.destroy()
        self.tags_outer.pack_forget()
        self._welcome()

    def _toggle_theme(self):
        if self.theme == "dark":
            self.theme = "light"
            self.C     = LIGHT
            ctk.set_appearance_mode("light")
            self.theme_btn.configure(text="Mode sombre")
        else:
            self.theme = "dark"
            self.C     = DARK
            ctk.set_appearance_mode("dark")
            self.theme_btn.configure(text="Mode clair")
        self._rebuild_ui()

    def _rebuild_ui(self):
        for w in self.winfo_children():
            w.destroy()
        self.configure(fg_color=self.C["bg"])
        self._build_ui()
        self._reset_session()


# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    app = SEMI()
    app.mainloop()
