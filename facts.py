# facts.py - Base de faits et traductions du système expert SEMI
# Système Expert de Maintenance Informatique
#
# Ce fichier centralise :
#   1. La base de faits courante (état de la session)
#   2. QUESTIONS   : fait interne  → question posée à l'utilisateur
#   3. DIAGNOSTICS : conclusion    → libellé affiché dans la carte de résultat
#   4. MOTS_CLES   : texte libre   → liste de faits déclenchés
#   5. CATEGORIES  : clé interne   → libellé de catégorie
#   6. label_certitude() : float   → label textuel de confiance

# ══════════════════════════════════════════════════════════════════════════════
#  BASE DE FAITS (état courant de la session)
# ══════════════════════════════════════════════════════════════════════════════

faits: list = []

def ajouter_fait(fait: str) -> None:
    """Ajoute un fait s'il n'existe pas déjà."""
    if fait not in faits:
        faits.append(fait)

def fait_existe(fait: str) -> bool:
    """Retourne True si le fait est présent dans la base."""
    return fait in faits

def reinitialiser() -> None:
    """Vide entièrement la base de faits."""
    faits.clear()

def afficher_faits() -> None:
    """Affiche tous les faits connus (debug console)."""
    print("Faits connus :", faits)

def tous_les_faits() -> list:
    """Retourne une copie de la liste des faits courants."""
    return list(faits)


# ══════════════════════════════════════════════════════════════════════════════
#  QUESTIONS — fait interne → question posée à l'utilisateur
# ══════════════════════════════════════════════════════════════════════════════

QUESTIONS = {

    # ── Démarrage ─────────────────────────────────────────────────────────────
    "pc_ne_demarre_pas":               "Le PC ne démarre pas du tout ?",
    "pc_allume":                       "Le PC s'allume correctement ?",
    "ventilateur_tourne":              "Le ventilateur tourne au démarrage ?",
    "ventilateur_ne_tourne_pas":       "Le ventilateur ne tourne pas du tout ?",
    "bip_sonore":                      "Vous entendez des bips au démarrage ?",
    "bip_sonore_absent":               "Aucun bip sonore au démarrage ?",
    "voyant_alim_allume":              "Le voyant d'alimentation est allumé ?",
    "voyant_alim_eteint":              "Le voyant d'alimentation est éteint ?",
    "odeur_brulee":                    "Vous sentez une odeur de brûlé ?",
    "demarrage_boucle":                "Le PC redémarre en boucle sans finir de booter ?",
    "demarrage_partiel":               "Le PC démarre partiellement puis se bloque ?",
    "post_echoue":                     "L'auto-test au démarrage (POST) échoue ?",
    "grub_manquant":                   "L'écran de démarrage (GRUB / BCD) est absent ?",
    "message_disk_error":              "Un message 'Disk boot failure' ou 'No bootable device' apparaît ?",
    "pc_ne_demarre_pas_apres_coupure": "Le PC ne redémarre plus après une coupure de courant ?",
    "condensateurs_gonfles":           "Des condensateurs gonflés sont visibles sur la carte mère ?",
    "bouton_power_sans_reponse":       "Le bouton d'alimentation ne répond pas du tout ?",
    "heure_systeme_incorrecte":        "L'heure système est incorrecte à chaque redémarrage ?",
    "alimentation_instable":           "L'alimentation électrique est instable (coupures, variations) ?",

    # ── Affichage ─────────────────────────────────────────────────────────────
    "ecran_noir":                      "L'écran reste noir alors que le PC est allumé ?",
    "ecran_bleu":                      "Vous avez un écran bleu (BSOD) ?",
    "ecran_clignote":                  "L'écran clignote ou scintille ?",
    "resolution_incorrecte":           "La résolution d'écran est incorrecte ou floue ?",
    "cable_endommage":                 "Le câble d'affichage est endommagé ou douteux ?",
    "pilotes_anciens":                 "Les pilotes graphiques sont anciens ou non à jour ?",
    "pilote_recemment_installe":       "Un pilote a été installé très récemment ?",
    "artefacts_visuels":               "Des artefacts (pixels morts, lignes, taches) sont visibles à l'écran ?",
    "double_ecran_probleme":           "Le second moniteur n'est pas détecté ou mal affiché ?",
    "luminosite_nulle":                "La luminosité est nulle même au maximum ?",

    # ── Performance ───────────────────────────────────────────────────────────
    "pc_lent":                         "Le PC est lent ?",
    "cpu_usage_eleve":                 "L'utilisation CPU dépasse 90 % en permanence ?",
    "ram_insuffisante":                "La mémoire RAM est insuffisante ou saturée ?",
    "disque_lent":                     "Le disque dur met beaucoup de temps à répondre ?",
    "demarrage_lent":                  "Le démarrage de Windows est très long ?",
    "programmes_demarrage_nombreux":   "De nombreux programmes se lancent automatiquement au démarrage ?",
    "freeze_aleatoire":                "Le PC se fige aléatoirement sans raison apparente ?",
    "lag_souris":                      "La souris lag ou les animations sont saccadées ?",
    "swap_eleve":                      "Le fichier d'échange (pagefile) est très sollicité ?",
    "temperature_cpu_elevee":          "La température du processeur dépasse 90 °C ?",
    "pc_lent_apres_maj":               "La lenteur est apparue après une mise à jour Windows ?",

    # ── Stockage ──────────────────────────────────────────────────────────────
    "disque_plein":                    "Le disque dur est presque plein (< 5 % libres) ?",
    "fichiers_inaccessibles":          "Des fichiers sont inaccessibles ou corrompus ?",
    "bruits_disque":                   "Vous entendez des bruits anormaux provenant du disque dur ?",
    "erreurs_systeme_fichiers":        "Des erreurs de système de fichiers apparaissent ?",
    "smart_alerte":                    "Un outil SMART (CrystalDiskInfo) signale des erreurs disque ?",
    "secteurs_defectueux":             "Des secteurs défectueux ont été détectés ?",
    "disque_non_reconnu":              "Le disque dur n'est pas reconnu par le BIOS ou Windows ?",
    "transfert_lent_usb":              "Les transferts vers un disque USB externe sont anormalement lents ?",
    "ssd_degradation":                 "Le SSD montre des signes de dégradation (endurance proche du max) ?",

    # ── Réseau ────────────────────────────────────────────────────────────────
    "pas_de_connexion":                "Vous n'avez aucune connexion internet ?",
    "connexion_lente":                 "La connexion internet est très lente ?",
    "wifi_desactive":                  "Le Wi-Fi est désactivé dans les paramètres ?",
    "wifi_active":                     "Le Wi-Fi est activé mais ne fonctionne pas ?",
    "autres_appareils_connectes":      "D'autres appareils se connectent normalement au même réseau ?",
    "ping_ok_mais_web_ko":             "Le ping fonctionne mais les pages web ne s'ouvrent pas ?",
    "connexion_coupee_periodiquement": "La connexion se coupe régulièrement de façon intermittente ?",
    "ip_conflit":                      "Un message de conflit d'adresses IP est affiché ?",
    "vpn_actif":                       "Un VPN est actuellement actif ?",
    "pare_feu_bloque":                 "Le pare-feu ou l'antivirus semble bloquer la connexion ?",
    "ethernet_connecte":               "Un câble Ethernet est physiquement connecté ?",
    "ethernet_non_reconnu":            "La connexion Ethernet n'est pas reconnue par Windows ?",

    # ── Système / OS ──────────────────────────────────────────────────────────
    "plantage_frequent":               "Le système plante fréquemment ?",
    "programmes_inconnus":             "Des programmes inconnus sont présents dans les applications ?",
    "maj_windows_bloque":              "Les mises à jour Windows se bloquent ou échouent ?",
    "erreur_demarrage_winload":        "Une erreur 'winload.exe' ou 'bootmgr' est signalée ?",
    "profil_utilisateur_corrompu":     "Le profil utilisateur Windows est corrompu ?",
    "tache_planifiee_suspecte":        "Des tâches planifiées inconnues sont présentes ?",
    "ecran_noir_apres_login":          "L'écran reste noir après la saisie du mot de passe ?",
    "explorer_plante":                 "L'explorateur Windows (explorer.exe) plante en boucle ?",
    "redemarrage_spontane":            "Le PC redémarre spontanément sans action de votre part ?",

    # ── Thermique ─────────────────────────────────────────────────────────────
    "temperature_elevee":              "La température générale du PC est excessive ?",
    "pc_eteint_brusquement":           "Le PC s'éteint brusquement sans avertissement ?",
    "ventilation_bruyante":            "Les ventilateurs tournent très fort en permanence ?",
    "pate_thermique_seche":            "La pâte thermique est ancienne (> 3 ans) ou sèche ?",
    "filtre_poussiere_bouche":         "Les filtres anti-poussière sont très encrassés ?",
    "laptop_chauffe_sous_charge":      "Le laptop surchauffe lors des tâches lourdes ?",

    # ── Batterie / Laptop ─────────────────────────────────────────────────────
    "laptop":                          "Vous utilisez un ordinateur portable ?",
    "batterie_ne_charge_pas":          "La batterie ne se charge pas du tout ?",
    "batterie_decharge_rapide":        "La batterie se décharge très rapidement (< 1 heure) ?",
    "batterie_gonflee":                "La batterie est gonflée ou déformée ?",
    "chargeur_non_reconnu":            "Le chargeur n'est pas reconnu par le système ?",
    "batterie_pourcentage_bloque":     "Le pourcentage de batterie est toujours bloqué ?",

    # ── Périphériques ─────────────────────────────────────────────────────────
    "clavier_non_detecte":             "Le clavier n'est pas détecté ?",
    "souris_non_detectee":             "La souris n'est pas détectée ?",
    "imprimante_non_detectee":         "L'imprimante n'est pas détectée ?",
    "peripherique_usb_non_detecte":    "Un périphérique USB n'est pas détecté ?",
    "port_usb_chauffe":                "Le port USB chauffe anormalement ?",
    "touches_clavier_erronees":        "Certaines touches produisent de mauvais caractères ?",
    "souris_saute":                    "Le curseur de la souris saute ou disparaît ?",
    "webcam_non_detectee":             "La webcam n'est pas détectée ?",
    "bluetooth_non_fonctionnel":       "Le Bluetooth ne fonctionne pas ?",
    "ecran_tactile_insensible":        "L'écran tactile ne répond pas ou est mal calibré ?",

    # ── Audio ─────────────────────────────────────────────────────────────────
    "pas_de_son":                      "Il n'y a pas de son du tout ?",
    "pilotes_audio_absents":           "Les pilotes audio sont absents ou non installés ?",
    "peripherique_audio_non_detecte":  "Le périphérique audio n'est pas détecté ?",
    "son_grele":                       "Le son est grêle, crachotant ou très distordu ?",
    "micro_non_detecte":               "Le microphone n'est pas détecté ?",
    "son_coupe_periodiquement":        "Le son se coupe par intermittence ?",
    "casque_non_reconnu":              "Le casque audio n'est pas reconnu à la connexion ?",

    # ── Sécurité ──────────────────────────────────────────────────────────────
    "popups_intempestifs":             "Des fenêtres publicitaires apparaissent en permanence ?",
    "navigateur_redirige":             "Le navigateur redirige vers des sites inconnus ?",
    "fichiers_chiffres":               "Des fichiers ont été chiffrés ou renommés bizarrement ?",
    "message_rancon":                  "Un message demandant une rançon est apparu ?",
    "antivirus_desactive":             "L'antivirus est désactivé de force ou ne s'ouvre plus ?",
    "pare_feu_desactive":              "Le pare-feu Windows est désactivé ?",
    "connexions_suspectes":            "Des connexions réseau suspectes sont visibles (netstat) ?",
    "fichiers_systeme_modifies":       "Des fichiers système ont été altérés (SFC signale des erreurs) ?",
    "email_spam_envoye":               "Des e-mails non sollicités sont envoyés depuis votre compte ?",

    # ── Logiciel ──────────────────────────────────────────────────────────────
    "application_crashe":              "Une application se ferme brutalement sans message d'erreur ?",
    "application_ne_demarre_pas":      "Une application refuse de se lancer ?",
    "erreur_dll_manquante":            "Un message d'erreur mentionne une DLL manquante ?",
    "erreur_vcredist":                 "Un message d'erreur Visual C++ Redistributable est affiché ?",
    "erreur_net_framework":            "Un message d'erreur .NET Framework est affiché ?",
    "installation_bloquee":            "Une installation de logiciel est bloquée ou échoue ?",
}


# ══════════════════════════════════════════════════════════════════════════════
#  DIAGNOSTICS — conclusion interne → libellé affiché dans la carte
# ══════════════════════════════════════════════════════════════════════════════

DIAGNOSTICS = {

    # Démarrage
    "probleme_ram":                       "Problème RAM",
    "probleme_alimentation":              "Problème d'alimentation",
    "erreur_bios":                        "Erreur BIOS / Code bip",
    "probleme_carte_mere":                "Carte mère défaillante",
    "composant_grille":                   "Composant grillé",
    "boucle_demarrage":                   "Boucle de démarrage",
    "maj_windows_corrompue":              "Mise à jour Windows corrompue",
    "disque_non_bootable":                "Disque non amorçable",
    "disque_defaillant_boot":             "Disque défaillant (boot impossible)",
    "alimentation_sans_tension":          "Alimentation sans tension",
    "probleme_alimentation_post_coupure": "Problème d'alimentation post-coupure",
    "composant_defaillant_post":          "Composant défaillant (POST échoué)",
    "pile_cmos_morte":                    "Pile CMOS hors service",
    "chargeur_demarrage_absent":          "Chargeur de démarrage absent (GRUB/BCD)",
    "bouton_power_defaillant":            "Bouton d'alimentation défaillant",
    "carte_mere_condensateurs_hs":        "Carte mère — condensateurs HS",

    # Affichage
    "probleme_carte_graphique":           "Carte graphique défaillante",
    "pilotes_graphiques_obsoletes":       "Pilotes graphiques obsolètes",
    "probleme_cable_affichage":           "Câble d'affichage défaillant",
    "pilotes_affichage_manquants":        "Pilotes d'affichage manquants",
    "gpu_surchauffe":                     "Surchauffe GPU",
    "gpu_defaillant":                     "GPU défaillant",
    "dalle_lcd_defaillante":              "Dalle LCD défaillante",
    "pilotes_multi_ecran_defaillants":    "Pilotes multi-écran défaillants",
    "retro_eclairage_hs":                 "Rétroéclairage hors service",

    # Performance
    "surchauffe_processeur":              "Surchauffe du processeur",
    "manque_memoire":                     "Mémoire insuffisante",
    "virus_malware":                      "Virus ou malware",
    "virus_cryptomineur":                 "Cryptomineur détecté",
    "disque_hdd_vieillissant":            "Disque dur vieillissant",
    "surcharge_demarrage":                "Surcharge au démarrage",
    "saturation_memoire_virtuelle":       "Saturation mémoire virtuelle",
    "maj_windows_problematique":          "Mise à jour Windows problématique",
    "ressources_saturees":                "Ressources système saturées",
    "instabilite_memoire":                "Instabilité mémoire (RAM)",
    "disque_goulot_etranglement":         "Disque — goulot d'étranglement",

    # Réseau
    "wifi_eteint":                        "Wi-Fi désactivé",
    "probleme_routeur":                   "Problème routeur / box",
    "probleme_carte_wifi":                "Carte Wi-Fi défaillante",
    "interference_wifi":                  "Interférence Wi-Fi",
    "probleme_dns":                       "Problème DNS",
    "instabilite_signal_wifi":            "Signal Wi-Fi instable",
    "conflit_adresse_ip":                 "Conflit d'adresse IP",
    "pilotes_ethernet_manquants":         "Pilotes Ethernet manquants",
    "vpn_bloque_connexion":               "VPN bloquant la connexion",
    "pare_feu_bloque_reseau":             "Pare-feu bloquant le réseau",

    # Stockage
    "espace_insuffisant":                 "Espace disque insuffisant",
    "disque_defaillant":                  "Disque dur défaillant",
    "corruption_systeme_fichiers":        "Corruption du système de fichiers",
    "disque_smart_defaillant":            "Alerte SMART — disque à remplacer",
    "disque_critique":                    "⚠ DISQUE EN PANNE IMMINENTE",
    "ssd_usure_avancee":                  "SSD — usure avancée",
    "port_usb_mode_lent":                 "Port USB en mode lent (USB 2.0)",

    # Système
    "bsod":                               "Écran bleu (BSOD)",
    "pilote_incompatible":                "Pilote incompatible",
    "windows_update_defaillant":          "Windows Update défaillant",
    "bcd_corrompu":                       "Base de démarrage (BCD) corrompue",
    "profil_windows_corrompu":            "Profil utilisateur Windows corrompu",
    "explorer_ne_demarre_pas":            "Explorer.exe ne démarre pas",
    "explorer_instable":                  "Explorer.exe instable",
    "redemarrage_surchauffe":             "Redémarrage dû à la surchauffe",
    "redemarrage_alimentation":           "Redémarrage dû à l'alimentation instable",

    # Thermique
    "surchauffe_generale":                "Surchauffe générale",
    "surchauffe_laptop":                  "Surchauffe laptop",
    "ventilateur_insuffisant":            "Ventilation insuffisante",
    "pate_thermique_a_remplacer":         "Pâte thermique à remplacer",
    "encrassement_thermique":             "Encrassement thermique",
    "caloduc_laptop_defaillant":          "Caloduc laptop défaillant",

    # Batterie
    "probleme_batterie":                  "Problème de batterie",
    "batterie_usee":                      "Batterie usée",
    "batterie_dangereuse":                "⚠ Batterie gonflée — DANGER",
    "chargeur_incompatible":              "Chargeur incompatible",
    "calibration_batterie_requise":       "Calibration batterie requise",

    # Périphériques
    "probleme_clavier":                   "Problème clavier",
    "probleme_souris":                    "Problème souris",
    "probleme_imprimante":                "Problème imprimante",
    "probleme_port_usb":                  "Problème port USB",
    "port_usb_endommage":                 "Port USB endommagé",
    "disposition_clavier_incorrecte":     "Disposition clavier incorrecte",
    "pilotes_webcam_manquants":           "Pilotes webcam manquants",
    "probleme_bluetooth":                 "Problème Bluetooth",
    "pilotes_ecran_tactile_obsoletes":    "Pilotes écran tactile obsolètes",
    "souris_surface_incompatible":        "Souris — surface incompatible",

    # Audio
    "probleme_audio":                     "Problème audio",
    "mauvais_peripherique_audio":         "Mauvais périphérique audio sélectionné",
    "interference_audio":                 "Interférence audio",
    "micro_desactive_ou_absent":          "Microphone désactivé ou absent",
    "jack_audio_defaillant":              "Jack audio défaillant",

    # Sécurité
    "adware_hijacker":                    "Adware / Piratage navigateur",
    "ransomware":                         "🔒 RANSOMWARE",
    "malware_desactive_antivirus":        "Malware ayant désactivé l'antivirus",
    "infection_active_reseau":            "Infection active avec activité réseau",
    "integrite_systeme_compromise":       "Intégrité système compromise",
    "persistance_malware":                "Persistance de malware (tâche planifiée)",
    "compte_ou_pc_compromis":             "Compte ou PC compromis",
    "protection_systeme_desactivee":      "Protection système désactivée",

    # Logiciel
    "dependance_logicielle_manquante":    "Dépendance logicielle manquante",
    "vcredist_manquant":                  "Visual C++ Redistributable manquant",
    "dotnet_corrompu":                    ".NET Framework corrompu",
    "installation_bloquee_par_politique": "Installation bloquée par politique système",
    "ressources_insuffisantes_app":       "Ressources insuffisantes pour l'application",
}


# ══════════════════════════════════════════════════════════════════════════════
#  MOTS-CLÉS — texte saisi librement → liste de faits internes déclenchés
# ══════════════════════════════════════════════════════════════════════════════

MOTS_CLES = {

    # Démarrage
    "ne démarre pas":              ["pc_ne_demarre_pas"],
    "ne demarre pas":              ["pc_ne_demarre_pas"],
    "pas démarrer":                ["pc_ne_demarre_pas"],
    "pas demarrer":                ["pc_ne_demarre_pas"],
    "démarrage":                   ["pc_ne_demarre_pas"],
    "demarrage":                   ["pc_ne_demarre_pas"],
    "bip":                         ["bip_sonore", "pc_ne_demarre_pas"],
    "redémarre en boucle":         ["demarrage_boucle"],
    "redemarre en boucle":         ["demarrage_boucle"],
    "boucle":                      ["demarrage_boucle"],
    "no bootable":                 ["message_disk_error"],
    "disk error":                  ["message_disk_error"],
    "boot failure":                ["message_disk_error"],
    "condensateur":                ["condensateurs_gonfles"],
    "pile cmos":                   ["heure_systeme_incorrecte"],
    "heure incorrecte":            ["heure_systeme_incorrecte"],
    "coupure courant":             ["pc_ne_demarre_pas_apres_coupure"],
    "après coupure":               ["pc_ne_demarre_pas_apres_coupure"],
    "apres coupure":               ["pc_ne_demarre_pas_apres_coupure"],
    "odeur":                       ["odeur_brulee"],
    "brûlé":                       ["odeur_brulee"],
    "brule":                       ["odeur_brulee"],
    "grub":                        ["grub_manquant"],
    "winload":                     ["erreur_demarrage_winload"],
    "bootmgr":                     ["erreur_demarrage_winload"],

    # Affichage
    "écran noir":                  ["pc_allume", "ecran_noir"],
    "ecran noir":                  ["pc_allume", "ecran_noir"],
    "écran bleu":                  ["ecran_bleu"],
    "ecran bleu":                  ["ecran_bleu"],
    "bsod":                        ["ecran_bleu", "plantage_frequent"],
    "clignote":                    ["ecran_clignote"],
    "scintille":                   ["ecran_clignote"],
    "résolution":                  ["resolution_incorrecte"],
    "resolution":                  ["resolution_incorrecte"],
    "artefact":                    ["artefacts_visuels"],
    "pixels morts":                ["artefacts_visuels"],
    "double écran":                ["double_ecran_probleme"],
    "second écran":                ["double_ecran_probleme"],
    "luminosité":                  ["luminosite_nulle"],
    "rétroéclairage":              ["luminosite_nulle"],

    # Performance
    "lent":                        ["pc_lent"],
    "lenteur":                     ["pc_lent"],
    "rame":                        ["pc_lent"],
    "freeze":                      ["freeze_aleatoire"],
    "se fige":                     ["freeze_aleatoire"],
    "lag":                         ["lag_souris", "pc_lent"],
    "saccade":                     ["lag_souris"],
    "swap":                        ["swap_eleve"],
    "pagefile":                    ["swap_eleve"],
    "après maj":                   ["pc_lent_apres_maj"],
    "apres mise a jour":           ["pc_lent_apres_maj", "maj_windows_bloque"],
    "mise à jour":                 ["maj_windows_bloque"],
    "mise a jour":                 ["maj_windows_bloque"],

    # Stockage
    "disque plein":                ["disque_plein", "pc_lent"],
    "espace":                      ["disque_plein"],
    "fichier inaccessible":        ["fichiers_inaccessibles"],
    "fichier corrompu":            ["fichiers_inaccessibles", "erreurs_systeme_fichiers"],
    "bruit disque":                ["bruits_disque"],
    "cliquetis":                   ["bruits_disque"],
    "smart":                       ["smart_alerte"],
    "secteur":                     ["secteurs_defectueux"],
    "ssd":                         ["ssd_degradation", "disque_lent"],
    "transfert lent":              ["transfert_lent_usb"],

    # Réseau
    "pas de connexion":            ["pas_de_connexion"],
    "pas internet":                ["pas_de_connexion"],
    "plus internet":               ["pas_de_connexion"],
    "connexion lente":             ["connexion_lente", "wifi_active"],
    "internet lent":               ["connexion_lente", "wifi_active"],
    "wifi":                        ["pas_de_connexion", "wifi_active"],
    "se déconnecte":               ["connexion_coupee_periodiquement"],
    "se deconnecte":               ["connexion_coupee_periodiquement"],
    "conflit ip":                  ["ip_conflit"],
    "dns":                         ["ping_ok_mais_web_ko"],
    "vpn":                         ["vpn_actif"],
    "ethernet":                    ["ethernet_connecte", "ethernet_non_reconnu"],
    "câble réseau":                ["ethernet_connecte"],

    # Système
    "plantage":                    ["plantage_frequent"],
    "plante":                      ["plantage_frequent"],
    "crash":                       ["plantage_frequent"],
    "redémarre tout seul":         ["redemarrage_spontane"],
    "redemarre tout seul":         ["redemarrage_spontane"],
    "explorer":                    ["explorer_plante"],
    "profil corrompu":             ["profil_utilisateur_corrompu"],
    "écran noir login":            ["ecran_noir_apres_login"],
    "ecran noir connexion":        ["ecran_noir_apres_login"],

    # Thermique
    "chauffe":                     ["temperature_elevee"],
    "surchauffe":                  ["temperature_elevee", "pc_eteint_brusquement"],
    "s'éteint":                    ["pc_eteint_brusquement"],
    "s'eteint":                    ["pc_eteint_brusquement"],
    "éteint tout seul":            ["pc_eteint_brusquement"],
    "eteint tout seul":            ["pc_eteint_brusquement"],
    "ventilateur bruyant":         ["ventilation_bruyante"],
    "ventilo fort":                ["ventilation_bruyante"],
    "pâte thermique":              ["pate_thermique_seche"],
    "poussière":                   ["filtre_poussiere_bouche"],

    # Batterie
    "batterie":                    ["laptop", "batterie_ne_charge_pas"],
    "charge pas":                  ["batterie_ne_charge_pas"],
    "ne charge":                   ["batterie_ne_charge_pas"],
    "décharge":                    ["batterie_decharge_rapide"],
    "decharge":                    ["batterie_decharge_rapide"],
    "batterie gonflée":            ["batterie_gonflee"],
    "batterie gonflee":            ["batterie_gonflee"],
    "chargeur":                    ["chargeur_non_reconnu"],
    "portable":                    ["laptop"],
    "laptop":                      ["laptop"],

    # Périphériques
    "clavier":                     ["clavier_non_detecte"],
    "touche":                      ["touches_clavier_erronees"],
    "souris":                      ["souris_non_detectee"],
    "curseur saute":               ["souris_saute"],
    "imprimante":                  ["imprimante_non_detectee"],
    "usb":                         ["peripherique_usb_non_detecte"],
    "webcam":                      ["webcam_non_detectee"],
    "bluetooth":                   ["bluetooth_non_fonctionnel"],
    "écran tactile":               ["ecran_tactile_insensible"],
    "tactile":                     ["ecran_tactile_insensible"],

    # Audio
    "son":                         ["pas_de_son"],
    "audio":                       ["pas_de_son", "pilotes_audio_absents"],
    "muet":                        ["pas_de_son"],
    "micro":                       ["micro_non_detecte"],
    "microphone":                  ["micro_non_detecte"],
    "casque":                      ["casque_non_reconnu"],
    "grésille":                    ["son_grele"],
    "gresille":                    ["son_grele"],

    # Sécurité
    "virus":                       ["programmes_inconnus", "pc_lent"],
    "malware":                     ["programmes_inconnus", "pc_lent"],
    "ransomware":                  ["fichiers_chiffres", "message_rancon"],
    "rançon":                      ["fichiers_chiffres", "message_rancon"],
    "rancon":                      ["fichiers_chiffres", "message_rancon"],
    "chiffré":                     ["fichiers_chiffres"],
    "chiffre":                     ["fichiers_chiffres"],
    "pub":                         ["popups_intempestifs"],
    "popup":                       ["popups_intempestifs"],
    "publicité":                   ["popups_intempestifs", "navigateur_redirige"],
    "publicite":                   ["popups_intempestifs", "navigateur_redirige"],
    "redirigé":                    ["navigateur_redirige"],
    "redirige":                    ["navigateur_redirige"],
    "antivirus désactivé":         ["antivirus_desactive"],
    "antivirus desactive":         ["antivirus_desactive"],
    "pare-feu":                    ["pare_feu_desactive"],
    "spam":                        ["email_spam_envoye"],

    # Logiciel
    "application crash":           ["application_crashe"],
    "appli crash":                 ["application_crashe"],
    "dll":                         ["erreur_dll_manquante"],
    "visual c++":                  ["erreur_vcredist"],
    "vcredist":                    ["erreur_vcredist"],
    ".net":                        ["erreur_net_framework"],
    "dotnet":                      ["erreur_net_framework"],
    "installation échoue":         ["installation_bloquee"],
    "installation bloquée":        ["installation_bloquee"],

    # Générique
    "ram":                         ["ram_insuffisante"],
    "mémoire":                     ["ram_insuffisante"],
    "memoire":                     ["ram_insuffisante"],
    "cpu":                         ["cpu_usage_eleve"],
    "processeur":                  ["cpu_usage_eleve"],
    "ventilateur":                 ["ventilateur_tourne"],
    "ventilo":                     ["ventilateur_tourne"],
    "démarre lentement":           ["demarrage_lent"],
    "demarre lentement":           ["demarrage_lent"],
    "long au démarrage":           ["demarrage_lent", "programmes_demarrage_nombreux"],
}


# ══════════════════════════════════════════════════════════════════════════════
#  CATÉGORIES — clé interne → libellé affiché
# ══════════════════════════════════════════════════════════════════════════════

CATEGORIES = {
    "demarrage":    "Démarrage",
    "affichage":    "Affichage",
    "performance":  "Performance",
    "reseau":       "Réseau",
    "stockage":     "Stockage",
    "systeme":      "Système",
    "thermique":    "Thermique",
    "batterie":     "Batterie",
    "peripherique": "Périphérique",
    "audio":        "Audio",
    "securite":     "Sécurité",
    "logiciel":     "Logiciel",
}


# ══════════════════════════════════════════════════════════════════════════════
#  LABEL DE CERTITUDE — float → texte lisible
# ══════════════════════════════════════════════════════════════════════════════

def label_certitude(certitude: float) -> str:
    """Retourne un libellé textuel selon le niveau de certitude calculé."""
    if certitude >= 0.95:
        return "Quasi certain"
    elif certitude >= 0.85:
        return "Très probable"
    elif certitude >= 0.70:
        return "Probable"
    elif certitude >= 0.55:
        return "Possible"
    else:
        return "À vérifier"


# ══════════════════════════════════════════════════════════════════════════════
#  MOTEUR NLP — Reconnaissance de symptômes en langage naturel
#  Fonctionne sans bibliothèque externe (unicodedata + re uniquement)
#
#  Pipeline :
#    1. Normalisation  : minuscules + suppression des accents + ponctuation
#    2. Stemming FR    : réduction des mots à leur racine approximative
#    3. SYNONYMES      : table racine → liste de faits
#    4. MOTS_CLES      : correspondance exacte (fallback rapide)
#    5. Agrégation     : union des faits détectés, sans doublons
# ══════════════════════════════════════════════════════════════════════════════

import unicodedata as _ud
import re as _re


# ── 1. Normalisation ──────────────────────────────────────────────────────────

def _normaliser(texte: str) -> str:
    """Minuscules, suppression des accents, ponctuation → espace."""
    texte = texte.lower()
    texte = ''.join(
        c for c in _ud.normalize('NFD', texte)
        if _ud.category(c) != 'Mn'
    )
    texte = _re.sub(r"[^\w\s]", ' ', texte)
    return _re.sub(r'\s+', ' ', texte).strip()


# ── 2. Stemmer français minimaliste ──────────────────────────────────────────

_SUFFIXES = [
    'issements', 'issement', 'ifications', 'ification',
    'ionnement', 'ionnements',
    'ements', 'ement', 'ations', 'ation',
    'issant', 'issants', 'issante',
    'erait', 'eront', 'aient', 'erais',
    'eurs', 'eur', 'euse', 'euses',
    'ables', 'able', 'ibles', 'ible',
    'iques', 'ique',
    'ants', 'ant', 'entes', 'ente', 'ents', 'ent',
    'ions', 'ion', 'age', 'ages',
    'ers', 'er', 'ir', 'ez', 'es', 'e', 's',
]

def _stem(mot: str) -> str:
    """Réduit un mot à sa racine approximative (longueur minimale : 4 chars)."""
    if len(mot) <= 4:
        return mot
    for suf in _SUFFIXES:
        if mot.endswith(suf) and len(mot) - len(suf) >= 4:
            return mot[:-len(suf)]
    return mot


# ── 3. Table de synonymes (racine normalisée → faits internes) ────────────────
#
#  Les clés sont des RACINES (après normalisation + stemming) ou des
#  tokens exacts normalisés. On peut mettre plusieurs tokens séparés
#  par un espace pour une règle multi-mots (les deux doivent être présents).
#
#  Format :  "token_ou_racine" : ["fait1", "fait2", ...]
#  Format 2  : ("token1", "token2") : [...]  → les deux tokens doivent être présents

SYNONYMES: dict = {

    # ── Démarrage ──────────────────────────────────────────────────────────
    "demarr":         ["pc_ne_demarre_pas"],
    "boot":           ["pc_ne_demarre_pas"],
    "allum":          ["pc_ne_demarre_pas"],
    "start":          ["pc_ne_demarre_pas"],
    "lanc":           ["pc_ne_demarre_pas"],
    "redemar":        ["demarrage_boucle"],
    "rebout":         ["demarrage_boucle"],
    "boucl":          ["demarrage_boucle"],
    "loop":           ["demarrage_boucle"],
    "bip":            ["bip_sonore", "pc_ne_demarre_pas"],
    "beep":           ["bip_sonore", "pc_ne_demarre_pas"],
    "odeur":          ["odeur_brulee"],
    "brul":           ["odeur_brulee"],
    "grill":          ["odeur_brulee", "composant_grille"],
    "condensat":      ["condensateurs_gonfles"],
    "gonfl":          ["condensateurs_gonfles"],
    "cmos":           ["heure_systeme_incorrecte"],
    "horloge":        ["heure_systeme_incorrecte"],
    "heur":           ["heure_systeme_incorrecte"],
    "grub":           ["grub_manquant"],
    "winload":        ["erreur_demarrage_winload"],
    "bootmgr":        ["erreur_demarrage_winload"],
    "post":           ["post_echoue"],
    "coupure":        ["pc_ne_demarre_pas_apres_coupure"],
    "secteur":        ["pc_ne_demarre_pas_apres_coupure", "secteurs_defectueux"],

    # ── Affichage ──────────────────────────────────────────────────────────
    "noir":           ["ecran_noir"],
    "blank":          ["ecran_noir"],
    "bleu":           ["ecran_bleu"],
    "bsod":           ["ecran_bleu", "plantage_frequent"],
    "cligno":         ["ecran_clignote"],
    "scintill":       ["ecran_clignote"],
    "papillonn":      ["ecran_clignote"],
    "tremblo":        ["ecran_clignote"],
    "resolut":        ["resolution_incorrecte"],
    "pixel":          ["artefacts_visuels"],
    "artefact":       ["artefacts_visuels"],
    "lignes":         ["artefacts_visuels"],
    "luminosit":      ["luminosite_nulle"],
    "retroclair":     ["luminosite_nulle"],
    "backlight":      ["luminosite_nulle"],
    "dalle":          ["dalle_lcd_defaillante"],
    "moniteur":       ["probleme_carte_graphique"],
    "affichag":       ["probleme_carte_graphique"],
    "hdmi":           ["cable_endommage"],
    "displayport":    ["cable_endommage"],
    "vga":            ["cable_endommage"],
    "cable":          ["cable_endommage"],

    # ── Performance ────────────────────────────────────────────────────────
    "lent":           ["pc_lent"],
    "lenteur":        ["pc_lent"],
    "ram":            ["pc_lent", "ram_insuffisante"],
    "rame":           ["pc_lent"],
    "lag":            ["pc_lent", "lag_souris"],
    "lagu":           ["pc_lent", "lag_souris"],
    "freeze":         ["freeze_aleatoire"],
    "fige":           ["freeze_aleatoire"],
    "bloqu":          ["freeze_aleatoire"],
    "hang":           ["freeze_aleatoire"],
    "saccad":         ["lag_souris"],
    "lent":           ["pc_lent"],
    "pagefil":        ["swap_eleve"],
    "swap":           ["swap_eleve"],
    "memoir":         ["ram_insuffisante"],
    "memory":         ["ram_insuffisante"],
    "cpu":            ["cpu_usage_eleve"],
    "processeur":     ["cpu_usage_eleve"],
    "proc":           ["cpu_usage_eleve"],

    # ── Stockage ───────────────────────────────────────────────────────────
    "disqu":          ["disque_lent", "bruits_disque"],
    "espac":          ["disque_plein"],
    "plein":          ["disque_plein"],
    "stock":          ["disque_plein"],
    "fichier":        ["fichiers_inaccessibles"],
    "corromp":        ["fichiers_inaccessibles", "erreurs_systeme_fichiers"],
    "corrupt":        ["fichiers_inaccessibles", "erreurs_systeme_fichiers"],
    "inaccess":       ["fichiers_inaccessibles"],
    "bruit":          ["bruits_disque"],
    "cliquetis":      ["bruits_disque"],
    "grince":         ["bruits_disque"],
    "smart":          ["smart_alerte"],
    "ssd":            ["ssd_degradation"],
    "transfert":      ["transfert_lent_usb"],

    # ── Réseau ─────────────────────────────────────────────────────────────
    "internet":       ["pas_de_connexion"],
    "connect":        ["pas_de_connexion"],
    "connect":        ["pas_de_connexion"],
    "reseau":         ["pas_de_connexion"],
    "network":        ["pas_de_connexion"],
    "wifi":           ["pas_de_connexion", "wifi_active"],
    "wi-fi":          ["pas_de_connexion", "wifi_active"],
    "routeur":        ["probleme_routeur"],
    "box":            ["probleme_routeur"],
    "dns":            ["ping_ok_mais_web_ko"],
    "deconnect":      ["connexion_coupee_periodiquement"],
    "coupure":        ["connexion_coupee_periodiquement"],
    "vpn":            ["vpn_actif"],
    "ethernet":       ["ethernet_connecte", "ethernet_non_reconnu"],
    "rj45":           ["ethernet_connecte"],
    "ip":             ["ip_conflit"],

    # ── Système ────────────────────────────────────────────────────────────
    "plant":          ["plantage_frequent"],
    "crash":          ["plantage_frequent"],
    "tomb":           ["plantage_frequent"],
    "bug":            ["plantage_frequent"],
    "explorateur":    ["explorer_plante"],
    "explorer":       ["explorer_plante"],
    "profil":         ["profil_utilisateur_corrompu"],
    "registr":        ["registre_corrompu"],
    "miseajour":      ["maj_windows_bloque"],
    "updat":          ["maj_windows_bloque"],
    "spontan":        ["redemarrage_spontane"],
    "ecran":          ["ecran_noir"],  # générique

    # ── Thermique ──────────────────────────────────────────────────────────
    "chaud":          ["temperature_elevee"],
    "chauffe":        ["temperature_elevee"],
    "surchauff":      ["temperature_elevee", "pc_eteint_brusquement"],
    "temperat":       ["temperature_elevee"],
    "ventilat":       ["ventilation_bruyante"],
    "ventilo":        ["ventilation_bruyante"],
    "fan":            ["ventilation_bruyante"],
    "poussier":       ["filtre_poussiere_bouche"],
    "encr":           ["filtre_poussiere_bouche"],
    "pate":           ["pate_thermique_seche"],
    "thermique":      ["pate_thermique_seche", "temperature_elevee"],
    "eteint":         ["pc_eteint_brusquement"],
    "extinction":     ["pc_eteint_brusquement"],
    "caloduc":        ["laptop_chauffe_sous_charge"],

    # ── Batterie / Laptop ──────────────────────────────────────────────────
    "batter":         ["laptop", "batterie_ne_charge_pas"],
    "laptop":         ["laptop"],
    "portable":       ["laptop"],
    "noteboo":        ["laptop"],
    "charg":          ["batterie_ne_charge_pas"],
    "dechar":         ["batterie_decharge_rapide"],
    "vide":           ["batterie_decharge_rapide"],
    "gonfl":          ["batterie_gonflee"],
    "chargeur":       ["chargeur_non_reconnu"],
    "adaptateur":     ["chargeur_non_reconnu"],
    "pourcentag":     ["batterie_pourcentage_bloque"],

    # ── Périphériques ──────────────────────────────────────────────────────
    "clavier":        ["clavier_non_detecte"],
    "keyboard":       ["clavier_non_detecte"],
    "touche":         ["touches_clavier_erronees"],
    "souris":         ["souris_non_detectee"],
    "mouse":          ["souris_non_detectee"],
    "curseur":        ["souris_saute"],
    "pointeur":       ["souris_saute"],
    "imprimant":      ["imprimante_non_detectee"],
    "printer":        ["imprimante_non_detectee"],
    "usb":            ["peripherique_usb_non_detecte"],
    "cle usb":        ["peripherique_usb_non_detecte"],
    "webcam":         ["webcam_non_detectee"],
    "camera":         ["webcam_non_detectee"],
    "bluetooth":      ["bluetooth_non_fonctionnel"],
    "tactile":        ["ecran_tactile_insensible"],
    "manette":        ["manette_non_reconnue"],

    # ── Audio ──────────────────────────────────────────────────────────────
    "son":            ["pas_de_son"],
    "audio":          ["pas_de_son", "pilotes_audio_absents"],
    "muet":           ["pas_de_son"],
    "silenc":         ["pas_de_son"],
    "sound":          ["pas_de_son"],
    "micro":          ["micro_non_detecte"],
    "microphone":     ["micro_non_detecte"],
    "casque":         ["casque_non_reconnu"],
    "headset":        ["casque_non_reconnu"],
    "gresill":        ["son_grele"],
    "grincant":       ["son_grele"],
    "distord":        ["son_grele"],
    "coupe":          ["son_coupe_periodiquement"],

    # ── Sécurité ───────────────────────────────────────────────────────────
    "virus":          ["programmes_inconnus", "pc_lent"],
    "malware":        ["programmes_inconnus", "pc_lent"],
    "trojan":         ["programmes_inconnus", "pc_lent"],
    "ransomwar":      ["fichiers_chiffres", "message_rancon"],
    "rancon":         ["fichiers_chiffres", "message_rancon"],
    "chiffr":         ["fichiers_chiffres"],
    "crypter":        ["fichiers_chiffres"],
    "rançon":         ["message_rancon"],
    "popup":          ["popups_intempestifs"],
    "publicite":      ["popups_intempestifs", "navigateur_redirige"],
    "pub":            ["popups_intempestifs"],
    "redirig":        ["navigateur_redirige"],
    "antivirus":      ["antivirus_desactive"],
    "defend":         ["antivirus_desactive"],
    "pare-feu":       ["pare_feu_desactive"],
    "firewall":       ["pare_feu_desactive"],
    "hacke":          ["compte_compromis"],
    "pirat":          ["compte_compromis"],
    "spam":           ["email_spam_envoye"],

    # ── Logiciel ───────────────────────────────────────────────────────────
    "appli":          ["application_crashe"],
    "applicat":       ["application_crashe"],
    "logiciel":       ["application_crashe"],
    "program":        ["application_crashe", "programmes_inconnus"],
    "dll":            ["erreur_dll_manquante"],
    "visual":         ["erreur_vcredist"],
    "vcredist":       ["erreur_vcredist"],
    "dotnet":         ["erreur_net_framework"],
    "framework":      ["erreur_net_framework"],
    "install":        ["installation_bloquee"],
}

# ── Stopwords français à ignorer ──────────────────────────────────────────────
_STOPWORDS = {
    'le', 'la', 'les', 'un', 'une', 'des', 'du', 'de', 'au', 'aux',
    'je', 'tu', 'il', 'elle', 'nous', 'vous', 'ils', 'elles',
    'mon', 'ma', 'mes', 'ton', 'ta', 'tes', 'son', 'sa', 'ses',
    'ce', 'cet', 'cette', 'ces', 'qui', 'que', 'quoi', 'dont', 'ou',
    'et', 'ou', 'ni', 'car', 'mais', 'donc', 'or',
    'est', 'sont', 'a', 'ont', 'ete', 'sera', 'serait',
    'sur', 'sous', 'dans', 'avec', 'sans', 'par', 'pour', 'vers',
    'plus', 'tres', 'bien', 'mal', 'tout', 'rien', 'ne', 'pas',
    'se', 'si', 'ca', 'ça', 'ya', 'ai', 'eu',
    'mon', 'pc', 'ordinateur', 'ordi', 'machine', 'appareil',
    'depuis', 'hier', 'aujourd', 'hui', 'matin', 'soir',
    'quand', 'comment', 'pourquoi', 'quel', 'quelle',
}


# ── Fonction principale de détection ─────────────────────────────────────────

def detecter_faits(texte: str) -> dict:
    """
    Analyse un texte en langage naturel et retourne un dict :
      {
        'faits'    : list[str]   — faits détectés (sans doublons),
        'labels'   : list[str]   — libellés lisibles,
        'methode'  : list[str]   — 'exact' ou 'nlp' pour chaque fait,
        'tokens'   : list[str]   — tokens après normalisation+stemming,
      }

    Pipeline :
      1. Correspondance exacte sur MOTS_CLES (rapide, prioritaire)
      2. Tokenisation + stemming + matching sur SYNONYMES
    """
    texte_norm = _normaliser(texte)
    faits_detectes: list = []
    methodes:       list = []

    # ── Étape 1 : correspondance exacte (MOTS_CLES) ───────────────────────
    for kw, facts_list in MOTS_CLES.items():
        kw_norm = _normaliser(kw)
        if kw_norm and kw_norm in texte_norm:
            for f in facts_list:
                if f not in faits_detectes:
                    faits_detectes.append(f)
                    methodes.append('exact')

    # ── Étape 2 : tokenisation + stemming (SYNONYMES) ─────────────────────
    tokens_bruts = texte_norm.split()
    tokens       = [t for t in tokens_bruts if t not in _STOPWORDS and len(t) > 2]
    stems        = [_stem(t) for t in tokens]

    for stem in stems:
        if stem in SYNONYMES:
            for f in SYNONYMES[stem]:
                if f not in faits_detectes:
                    faits_detectes.append(f)
                    methodes.append('nlp')

    # ── Étape 3 : matching de bigrammes (deux mots consécutifs) ───────────
    for i in range(len(stems) - 1):
        bigram = stems[i] + ' ' + stems[i + 1]
        if bigram in SYNONYMES:
            for f in SYNONYMES[bigram]:
                if f not in faits_detectes:
                    faits_detectes.append(f)
                    methodes.append('nlp-bigram')

    labels = [QUESTIONS.get(f, f.replace('_', ' ')).replace(' ?', '') for f in faits_detectes]

    return {
        'faits':   faits_detectes,
        'labels':  labels,
        'methode': methodes,
        'tokens':  stems,
    }


# ── Test rapide si exécuté directement ────────────────────────────────────────

if __name__ == '__main__':
    tests = [
        "Mon ordinateur ne veut plus démarrer du tout",
        "L'écran reste noir mais le pc s'allume",
        "Ça rame énormément depuis la dernière mise à jour",
        "Je n'arrive plus à me connecter à internet, le wifi est actif",
        "La batterie se vide super vite et chauffe beaucoup",
        "Mon PC s'éteint tout seul sans prévenir",
        "J'entends un bruit bizarre qui vient du disque dur",
        "Impossible d'installer mon logiciel, ça échoue à chaque fois",
        "Il y a des publicités partout et mon navigateur est redirigé",
        "Des fichiers ont été chiffrés et un message demande une rançon",
    ]
    print("=== TEST detecter_faits() ===\n")
    for t in tests:
        result = detecter_faits(t)
        print(f'  Phrase  : "{t}"')
        print(f'  Tokens  : {result["tokens"]}')
        print(f'  Faits   : {result["faits"]}')
        print(f'  Méthode : {result["methode"]}')
        print()
