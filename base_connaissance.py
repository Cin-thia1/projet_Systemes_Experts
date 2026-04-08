# base_connaissance.py - Toutes les règles

REGLES = [
    # --- DEMARRAGE ---
    {
        "id": "R1",
        "conditions": ["pc_ne_demarre_pas", "ventilateur_tourne"],
        "conclusion": "probleme_ram",
        "solution": "Réinsérer ou remplacer les barrettes RAM"
    },
    {
        "id": "R2",
        "conditions": ["pc_ne_demarre_pas", "ventilateur_ne_tourne_pas"],
        "conclusion": "probleme_alimentation",
        "solution": "Vérifier le câble d'alimentation ou remplacer le bloc d'alimentation"
    },
    {
        "id": "R3",
        "conditions": ["pc_allume", "ecran_noir"],
        "conclusion": "probleme_carte_graphique",
        "solution": "Vérifier le câble HDMI/VGA ou tester une autre carte graphique"
    },
    # --- PERFORMANCE ---
    {
        "id": "R4",
        "conditions": ["pc_lent", "cpu_usage_eleve"],
        "conclusion": "surchauffe_processeur",
        "solution": "Nettoyer le ventilateur et renouveler la pâte thermique"
    },
    {
        "id": "R5",
        "conditions": ["pc_lent", "ram_insuffisante"],
        "conclusion": "manque_memoire",
        "solution": "Ajouter une barrette RAM ou fermer les programmes inutiles"
    },
    # --- RESEAU ---
    {
        "id": "R6",
        "conditions": ["pas_de_connexion", "wifi_desactive"],
        "conclusion": "wifi_eteint",
        "solution": "Activer le Wi-Fi dans les paramètres réseau"
    },
    {
        "id": "R7",
        "conditions": ["pas_de_connexion", "wifi_active"],
        "conclusion": "probleme_routeur",
        "solution": "Redémarrer le routeur ou contacter le fournisseur internet"
    },
    # --- STOCKAGE ---
    {
        "id": "R8",
        "conditions": ["pc_lent", "disque_plein"],
        "conclusion": "espace_insuffisant",
        "solution": "Supprimer des fichiers inutiles ou ajouter un disque dur"
    },
    {
        "id": "R9",
        "conditions": ["fichiers_inaccessibles", "bruits_disque"],
        "conclusion": "disque_defaillant",
        "solution": "Sauvegarder les données et remplacer le disque dur"
    },
    # --- SYSTEME ---
    {
        "id": "R10",
        "conditions": ["ecran_bleu", "plantage_frequent"],
        "conclusion": "bsod",
        "solution": "Mettre à jour les pilotes ou réinstaller Windows"
    },
    {
        "id": "R11",
        "conditions": ["pc_lent", "programmes_inconnus"],
        "conclusion": "virus_malware",
        "solution": "Lancer un antivirus et supprimer les programmes suspects"
    },
    # --- PERIPHERIQUES ---
    {
        "id": "R12",
        "conditions": ["clavier_non_detecte"],
        "conclusion": "probleme_clavier",
        "solution": "Rebrancher le clavier ou tester sur un autre port USB"
    },
    {
        "id": "R13",
        "conditions": ["imprimante_non_detectee"],
        "conclusion": "probleme_imprimante",
        "solution": "Réinstaller les pilotes de l'imprimante"
    },
    # --- SURCHAUFFE ---
    {
        "id": "R14",
        "conditions": ["pc_eteint_brusquement", "temperature_elevee"],
        "conclusion": "surchauffe_generale",
        "solution": "Vérifier la ventilation du boîtier et nettoyer les filtres"
    },

    # --- BIOS ---
    {
        "id": "R15",
        "conditions": ["pc_ne_demarre_pas", "bip_sonore"],
        "conclusion": "erreur_bios",
        "solution": "Consulter le manuel de la carte mère pour décoder les bips"
    },

    # --- BATTERIE (laptop) ---
    {
        "id": "R16",
        "conditions": ["laptop", "batterie_ne_charge_pas"],
        "conclusion": "probleme_batterie",
        "solution": "Remplacer la batterie ou vérifier le chargeur"
    },

    # --- ECRAN ---
    {
        "id": "R17",
        "conditions": ["ecran_clignote", "pilotes_anciens"],
        "conclusion": "pilotes_graphiques_obsoletes",
        "solution": "Mettre à jour les pilotes de la carte graphique"
    },

    # --- USB ---
    {
        "id": "R18",
        "conditions": ["peripherique_usb_non_detecte"],
        "conclusion": "probleme_port_usb",
        "solution": "Tester un autre port USB ou réinstaller les pilotes USB"
    },

    # --- SON ---
    {
        "id": "R19",
        "conditions": ["pas_de_son", "pilotes_audio_absents"],
        "conclusion": "probleme_audio",
        "solution": "Réinstaller les pilotes audio depuis le site du fabricant"
    },
]