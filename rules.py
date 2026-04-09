# rules.py - Base de règles du système expert SEMI
# Système Expert de Maintenance Informatique
#
# Structure d'une règle :
#   id         : identifiant unique (R1, R2, …)
#   categorie  : domaine fonctionnel (voir CATEGORIES dans facts.py)
#   conditions : liste de faits qui doivent TOUS être présents (ET logique)
#   conclusion : fait déduit si toutes les conditions sont satisfaites
#   certitude  : degré de confiance du diagnostic (0.0 à 1.0)
#   solution   : action corrective recommandée à l'utilisateur

REGLES = [

    # ══════════════════════════════════════════════════════════════════════════
    #  DÉMARRAGE
    # ══════════════════════════════════════════════════════════════════════════
    {
        "id": "R1", "categorie": "demarrage",
        "conditions": ["pc_ne_demarre_pas", "ventilateur_tourne"],
        "conclusion": "probleme_ram", "certitude": 0.80,
        "solution": "Réinsérer ou remplacer les barrettes RAM. Tester chaque barrette une par une dans le slot A1."
    },
    {
        "id": "R2", "categorie": "demarrage",
        "conditions": ["pc_ne_demarre_pas", "ventilateur_ne_tourne_pas"],
        "conclusion": "probleme_alimentation", "certitude": 0.90,
        "solution": "Vérifier le câble d'alimentation, le disjoncteur et le bouton arrière du bloc. Tester avec un autre bloc si possible."
    },
    {
        "id": "R3", "categorie": "demarrage",
        "conditions": ["pc_ne_demarre_pas", "bip_sonore"],
        "conclusion": "erreur_bios", "certitude": 0.85,
        "solution": "Consulter le manuel de la carte mère pour décoder le code bip. Peut indiquer un problème RAM, GPU ou carte mère."
    },
    {
        "id": "R4", "categorie": "demarrage",
        "conditions": ["pc_ne_demarre_pas", "voyant_alim_allume", "bip_sonore_absent"],
        "conclusion": "probleme_carte_mere", "certitude": 0.70,
        "solution": "Tester avec le strict minimum (CPU + 1 RAM, sans GPU dédié). Inspecter visuellement les condensateurs."
    },
    {
        "id": "R5", "categorie": "demarrage",
        "conditions": ["pc_ne_demarre_pas", "odeur_brulee"],
        "conclusion": "composant_grille", "certitude": 0.95,
        "solution": "Arrêter immédiatement. Ne pas rallumer. Inspecter alimentation, carte mère et GPU pour un composant calciné."
    },
    {
        "id": "R6", "categorie": "demarrage",
        "conditions": ["pc_ne_demarre_pas", "voyant_alim_eteint"],
        "conclusion": "alimentation_sans_tension", "certitude": 0.88,
        "solution": "Tester la prise avec un autre appareil. Vérifier le câble secteur et l'interrupteur arrière du bloc d'alimentation."
    },
    {
        "id": "R7", "categorie": "demarrage",
        "conditions": ["demarrage_boucle"],
        "conclusion": "boucle_demarrage", "certitude": 0.75,
        "solution": "Accéder aux options avancées (F8/F11). Tenter une réparation automatique Windows. Vérifier la RAM et le disque."
    },
    {
        "id": "R8", "categorie": "demarrage",
        "conditions": ["demarrage_boucle", "maj_windows_bloque"],
        "conclusion": "maj_windows_corrompue", "certitude": 0.88,
        "solution": "Démarrer en mode sans échec et lancer : dism /online /cleanup-image /restorehealth puis sfc /scannow."
    },
    {
        "id": "R9", "categorie": "demarrage",
        "conditions": ["message_disk_error"],
        "conclusion": "disque_non_bootable", "certitude": 0.90,
        "solution": "Vérifier l'ordre de boot dans le BIOS. Réparer le MBR/BCD avec bootrec /fixmbr et bootrec /rebuildbcd depuis la récupération Windows."
    },
    {
        "id": "R10", "categorie": "demarrage",
        "conditions": ["message_disk_error", "disque_non_reconnu"],
        "conclusion": "disque_defaillant_boot", "certitude": 0.92,
        "solution": "Le disque est probablement défaillant. Tester sur un autre PC via boîtier USB. Sauvegarder immédiatement si encore accessible."
    },
    {
        "id": "R11", "categorie": "demarrage",
        "conditions": ["pc_ne_demarre_pas_apres_coupure"],
        "conclusion": "probleme_alimentation_post_coupure", "certitude": 0.80,
        "solution": "Débrancher 30 secondes pour décharger les condensateurs. Vérifier l'alimentation. Envisager un onduleur (UPS)."
    },
    {
        "id": "R12", "categorie": "demarrage",
        "conditions": ["demarrage_partiel", "post_echoue"],
        "conclusion": "composant_defaillant_post", "certitude": 0.82,
        "solution": "Retirer les composants non essentiels (cartes PCI, disques supplémentaires) et tester avec le strict minimum pour isoler la panne."
    },
    {
        "id": "R13", "categorie": "demarrage",
        "conditions": ["heure_systeme_incorrecte"],
        "conclusion": "pile_cmos_morte", "certitude": 0.85,
        "solution": "Remplacer la pile CMOS CR2032 sur la carte mère (< 2 €). Régler ensuite la date et l'heure dans le BIOS."
    },
    {
        "id": "R14", "categorie": "demarrage",
        "conditions": ["grub_manquant"],
        "conclusion": "chargeur_demarrage_absent", "certitude": 0.87,
        "solution": "Réparer GRUB via un live USB Linux, ou reconstruire le BCD Windows avec bootrec /rebuildbcd depuis le mode récupération."
    },
    {
        "id": "R15", "categorie": "demarrage",
        "conditions": ["bouton_power_sans_reponse", "voyant_alim_eteint"],
        "conclusion": "bouton_power_defaillant", "certitude": 0.78,
        "solution": "Court-circuiter les broches POWER SW sur la carte mère avec un tournevis isolé pour tester. Remplacer le bouton si défaillant."
    },
    {
        "id": "R16", "categorie": "demarrage",
        "conditions": ["condensateurs_gonfles"],
        "conclusion": "carte_mere_condensateurs_hs", "certitude": 0.93,
        "solution": "Des condensateurs gonflés indiquent une carte mère en fin de vie. Remplacement nécessaire."
    },

    # ══════════════════════════════════════════════════════════════════════════
    #  AFFICHAGE
    # ══════════════════════════════════════════════════════════════════════════
    {
        "id": "R17", "categorie": "affichage",
        "conditions": ["pc_allume", "ecran_noir"],
        "conclusion": "probleme_carte_graphique", "certitude": 0.75,
        "solution": "Vérifier le câble HDMI/DisplayPort/VGA. Tester sur un autre moniteur. Réinsérer la carte graphique dans son slot PCIe."
    },
    {
        "id": "R18", "categorie": "affichage",
        "conditions": ["ecran_clignote", "pilotes_anciens"],
        "conclusion": "pilotes_graphiques_obsoletes", "certitude": 0.83,
        "solution": "Mettre à jour les pilotes graphiques depuis le site officiel (NVIDIA, AMD ou Intel)."
    },
    {
        "id": "R19", "categorie": "affichage",
        "conditions": ["ecran_clignote", "cable_endommage"],
        "conclusion": "probleme_cable_affichage", "certitude": 0.87,
        "solution": "Remplacer le câble HDMI/DisplayPort. Sur laptop, le câble de la dalle peut être desserré (ouverture du châssis nécessaire)."
    },
    {
        "id": "R20", "categorie": "affichage",
        "conditions": ["resolution_incorrecte", "pilotes_anciens"],
        "conclusion": "pilotes_affichage_manquants", "certitude": 0.90,
        "solution": "Installer les pilotes graphiques adaptés. Windows utilise un pilote générique VESA en leur absence, d'où la résolution incorrecte."
    },
    {
        "id": "R21", "categorie": "affichage",
        "conditions": ["artefacts_visuels", "temperature_elevee"],
        "conclusion": "gpu_surchauffe", "certitude": 0.85,
        "solution": "Nettoyer le ventilateur du GPU. Vérifier les températures avec MSI Afterburner. Renouveler la pâte thermique du GPU."
    },
    {
        "id": "R22", "categorie": "affichage",
        "conditions": ["artefacts_visuels", "pc_allume"],
        "conclusion": "gpu_defaillant", "certitude": 0.78,
        "solution": "Tester avec le GPU intégré ou un GPU de remplacement. Les artefacts persistants à froid indiquent souvent une VRAM défaillante."
    },
    {
        "id": "R23", "categorie": "affichage",
        "conditions": ["luminosite_nulle", "laptop"],
        "conclusion": "dalle_lcd_defaillante", "certitude": 0.80,
        "solution": "Brancher un écran externe. Si l'image y apparaît, le rétroéclairage ou l'onduleur de la dalle est défaillant."
    },
    {
        "id": "R24", "categorie": "affichage",
        "conditions": ["double_ecran_probleme", "pilotes_anciens"],
        "conclusion": "pilotes_multi_ecran_defaillants", "certitude": 0.76,
        "solution": "Mettre à jour les pilotes graphiques. Vérifier dans Paramètres > Affichage > Détecter. Tester un autre câble ou port."
    },
    {
        "id": "R25", "categorie": "affichage",
        "conditions": ["ecran_noir", "laptop", "luminosite_nulle"],
        "conclusion": "retro_eclairage_hs", "certitude": 0.82,
        "solution": "Éclairer l'écran avec une lampe torche à 45°. Si une image est visible en fond, l'onduleur CCFL ou le rétroéclairage LED est hors service."
    },

    # ══════════════════════════════════════════════════════════════════════════
    #  PERFORMANCE
    # ══════════════════════════════════════════════════════════════════════════
    {
        "id": "R26", "categorie": "performance",
        "conditions": ["pc_lent", "cpu_usage_eleve"],
        "conclusion": "surchauffe_processeur", "certitude": 0.78,
        "solution": "Nettoyer le ventirad CPU. Renouveler la pâte thermique. Vérifier que le radiateur est correctement fixé."
    },
    {
        "id": "R27", "categorie": "performance",
        "conditions": ["pc_lent", "ram_insuffisante"],
        "conclusion": "manque_memoire", "certitude": 0.82,
        "solution": "Ajouter une barrette RAM ou libérer de la mémoire. Vérifier l'absence de fuite mémoire dans le Gestionnaire des tâches."
    },
    {
        "id": "R28", "categorie": "securite",
        "conditions": ["pc_lent", "programmes_inconnus"],
        "conclusion": "virus_malware", "certitude": 0.75,
        "solution": "Lancer un scan complet avec Windows Defender et Malwarebytes. Vérifier les tâches planifiées et les extensions navigateur."
    },
    {
        "id": "R29", "categorie": "performance",
        "conditions": ["pc_lent", "cpu_usage_eleve", "programmes_inconnus"],
        "conclusion": "virus_cryptomineur", "certitude": 0.88,
        "solution": "CPU élevé + programmes inconnus = probable cryptomineur. Scanner avec Malwarebytes, inspecter les processus et les tâches planifiées."
    },
    {
        "id": "R30", "categorie": "performance",
        "conditions": ["pc_lent", "disque_lent"],
        "conclusion": "disque_hdd_vieillissant", "certitude": 0.72,
        "solution": "Défragmenter si HDD. Vérifier l'état SMART avec CrystalDiskInfo si SSD. Un disque vieillissant doit être remplacé préventivement."
    },
    {
        "id": "R31", "categorie": "systeme",
        "conditions": ["demarrage_lent", "programmes_demarrage_nombreux"],
        "conclusion": "surcharge_demarrage", "certitude": 0.88,
        "solution": "Désactiver les programmes inutiles au démarrage via le Gestionnaire des tâches (onglet Démarrage) ou msconfig."
    },
    {
        "id": "R32", "categorie": "performance",
        "conditions": ["pc_lent", "swap_eleve", "ram_insuffisante"],
        "conclusion": "saturation_memoire_virtuelle", "certitude": 0.85,
        "solution": "Augmenter la RAM physique. Temporairement, agrandir le fichier d'échange dans Paramètres système avancés > Performance."
    },
    {
        "id": "R33", "categorie": "performance",
        "conditions": ["pc_lent_apres_maj"],
        "conclusion": "maj_windows_problematique", "certitude": 0.80,
        "solution": "Désinstaller la mise à jour récente via Paramètres > Windows Update > Afficher l'historique > Désinstaller les mises à jour."
    },
    {
        "id": "R34", "categorie": "performance",
        "conditions": ["lag_souris", "cpu_usage_eleve"],
        "conclusion": "ressources_saturees", "certitude": 0.77,
        "solution": "Fermer les applications en arrière-plan. Vérifier si un processus système (SearchIndexer, WMI Provider Host) consomme anormalement."
    },
    {
        "id": "R35", "categorie": "performance",
        "conditions": ["freeze_aleatoire", "ram_insuffisante"],
        "conclusion": "instabilite_memoire", "certitude": 0.80,
        "solution": "Tester la RAM avec MemTest86 (minimum deux cycles complets). Remplacer toute barrette présentant des erreurs."
    },
    {
        "id": "R36", "categorie": "performance",
        "conditions": ["freeze_aleatoire", "disque_lent"],
        "conclusion": "disque_goulot_etranglement", "certitude": 0.75,
        "solution": "Vérifier l'état SMART du disque. Un remplacement par SSD apportera une amélioration très significative des performances."
    },

    # ══════════════════════════════════════════════════════════════════════════
    #  RÉSEAU
    # ══════════════════════════════════════════════════════════════════════════
    {
        "id": "R37", "categorie": "reseau",
        "conditions": ["pas_de_connexion", "wifi_desactive"],
        "conclusion": "wifi_eteint", "certitude": 0.98,
        "solution": "Activer le Wi-Fi dans Paramètres > Réseau ou via le raccourci clavier (Fn + touche Wi-Fi)."
    },
    {
        "id": "R38", "categorie": "reseau",
        "conditions": ["pas_de_connexion", "wifi_active"],
        "conclusion": "probleme_routeur", "certitude": 0.70,
        "solution": "Redémarrer le routeur (débrancher 30 secondes). Tester avec un DNS manuel : 8.8.8.8 (Google) ou 1.1.1.1 (Cloudflare)."
    },
    {
        "id": "R39", "categorie": "reseau",
        "conditions": ["pas_de_connexion", "wifi_active", "autres_appareils_connectes"],
        "conclusion": "probleme_carte_wifi", "certitude": 0.80,
        "solution": "Si les autres appareils se connectent, la carte Wi-Fi du PC est défaillante. Mettre à jour ses pilotes ou la remplacer."
    },
    {
        "id": "R40", "categorie": "reseau",
        "conditions": ["connexion_lente", "wifi_active"],
        "conclusion": "interference_wifi", "certitude": 0.65,
        "solution": "Changer le canal Wi-Fi dans le routeur (canaux 1, 6 ou 11 en 2.4 GHz). Passer en 5 GHz ou se rapprocher du routeur."
    },
    {
        "id": "R41", "categorie": "reseau",
        "conditions": ["ping_ok_mais_web_ko"],
        "conclusion": "probleme_dns", "certitude": 0.90,
        "solution": "Changer les serveurs DNS (8.8.8.8 ou 1.1.1.1). Vider le cache DNS avec la commande : ipconfig /flushdns."
    },
    {
        "id": "R42", "categorie": "reseau",
        "conditions": ["connexion_coupee_periodiquement", "wifi_active"],
        "conclusion": "instabilite_signal_wifi", "certitude": 0.75,
        "solution": "Désactiver la gestion d'alimentation Wi-Fi : Gestionnaire de périphériques > Carte Wi-Fi > Propriétés > Gestion de l'alimentation."
    },
    {
        "id": "R43", "categorie": "reseau",
        "conditions": ["ip_conflit"],
        "conclusion": "conflit_adresse_ip", "certitude": 0.93,
        "solution": "Exécuter ipconfig /release puis ipconfig /renew pour obtenir une nouvelle IP. Configurer une IP statique si le conflit persiste."
    },
    {
        "id": "R44", "categorie": "reseau",
        "conditions": ["pas_de_connexion", "ethernet_connecte", "ethernet_non_reconnu"],
        "conclusion": "pilotes_ethernet_manquants", "certitude": 0.85,
        "solution": "Télécharger et réinstaller les pilotes Ethernet depuis le site du fabricant de la carte mère."
    },
    {
        "id": "R45", "categorie": "reseau",
        "conditions": ["pas_de_connexion", "vpn_actif"],
        "conclusion": "vpn_bloque_connexion", "certitude": 0.80,
        "solution": "Désactiver le VPN temporairement pour tester. Si la connexion revient, reconfigurer le VPN ou changer de serveur."
    },
    {
        "id": "R46", "categorie": "reseau",
        "conditions": ["pas_de_connexion", "pare_feu_bloque"],
        "conclusion": "pare_feu_bloque_reseau", "certitude": 0.82,
        "solution": "Vérifier les règles du pare-feu et de l'antivirus. Réinitialiser les paramètres réseau avec : netsh winsock reset."
    },

    # ══════════════════════════════════════════════════════════════════════════
    #  STOCKAGE
    # ══════════════════════════════════════════════════════════════════════════
    {
        "id": "R47", "categorie": "stockage",
        "conditions": ["pc_lent", "disque_plein"],
        "conclusion": "espace_insuffisant", "certitude": 0.85,
        "solution": "Libérer de l'espace : vider la corbeille, supprimer %temp%, désinstaller les logiciels inutilisés, ou ajouter un disque."
    },
    {
        "id": "R48", "categorie": "stockage",
        "conditions": ["fichiers_inaccessibles", "bruits_disque"],
        "conclusion": "disque_defaillant", "certitude": 0.92,
        "solution": "Sauvegarder immédiatement les données. Vérifier l'état SMART avec CrystalDiskInfo et remplacer le disque sans attendre."
    },
    {
        "id": "R49", "categorie": "stockage",
        "conditions": ["fichiers_inaccessibles", "erreurs_systeme_fichiers"],
        "conclusion": "corruption_systeme_fichiers", "certitude": 0.82,
        "solution": "Lancer chkdsk /f /r depuis une invite de commandes administrateur. Un redémarrage est nécessaire pour l'exécution."
    },
    {
        "id": "R50", "categorie": "stockage",
        "conditions": ["smart_alerte"],
        "conclusion": "disque_smart_defaillant", "certitude": 0.90,
        "solution": "Une alerte SMART est un signe précurseur de panne. Sauvegarder immédiatement et planifier le remplacement du disque."
    },
    {
        "id": "R51", "categorie": "stockage",
        "conditions": ["smart_alerte", "secteurs_defectueux"],
        "conclusion": "disque_critique", "certitude": 0.97,
        "solution": "PANNE IMMINENTE. Sauvegarder MAINTENANT sur un autre support. Le disque doit être remplacé immédiatement."
    },
    {
        "id": "R52", "categorie": "stockage",
        "conditions": ["ssd_degradation", "disque_lent"],
        "conclusion": "ssd_usure_avancee", "certitude": 0.85,
        "solution": "Vérifier la durée de vie résiduelle (TBW) du SSD avec CrystalDiskInfo. Remplacer si l'endurance d'écriture est atteinte."
    },
    {
        "id": "R53", "categorie": "stockage",
        "conditions": ["transfert_lent_usb"],
        "conclusion": "port_usb_mode_lent", "certitude": 0.72,
        "solution": "Vérifier que le port et le disque sont tous deux USB 3.x. Réinstaller les pilotes du contrôleur USB xHCI dans le Gestionnaire de périphériques."
    },

    # ══════════════════════════════════════════════════════════════════════════
    #  SYSTÈME / OS
    # ══════════════════════════════════════════════════════════════════════════
    {
        "id": "R54", "categorie": "systeme",
        "conditions": ["ecran_bleu", "plantage_frequent"],
        "conclusion": "bsod", "certitude": 0.80,
        "solution": "Lire le code d'erreur du BSOD. Mettre à jour les pilotes GPU et chipset. Tester la RAM avec MemTest86."
    },
    {
        "id": "R55", "categorie": "systeme",
        "conditions": ["ecran_bleu", "plantage_frequent", "pilote_recemment_installe"],
        "conclusion": "pilote_incompatible", "certitude": 0.90,
        "solution": "Désinstaller le pilote récemment installé via le Gestionnaire de périphériques. Utiliser 'Restaurer le pilote précédent' si disponible."
    },
    {
        "id": "R56", "categorie": "systeme",
        "conditions": ["maj_windows_bloque"],
        "conclusion": "windows_update_defaillant", "certitude": 0.78,
        "solution": "Exécuter le dépanneur Windows Update. Vider le dossier SoftwareDistribution et relancer le service Windows Update."
    },
    {
        "id": "R57", "categorie": "systeme",
        "conditions": ["erreur_demarrage_winload"],
        "conclusion": "bcd_corrompu", "certitude": 0.87,
        "solution": "Démarrer sur le support d'installation Windows et exécuter : bootrec /fixmbr, bootrec /fixboot, bootrec /rebuildbcd."
    },
    {
        "id": "R58", "categorie": "systeme",
        "conditions": ["profil_utilisateur_corrompu"],
        "conclusion": "profil_windows_corrompu", "certitude": 0.83,
        "solution": "Créer un nouveau profil utilisateur local et migrer les données. Vérifier HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\ProfileList."
    },
    {
        "id": "R59", "categorie": "systeme",
        "conditions": ["ecran_noir_apres_login"],
        "conclusion": "explorer_ne_demarre_pas", "certitude": 0.80,
        "solution": "Ouvrir le Gestionnaire des tâches (Ctrl+Shift+Esc) > Fichier > Nouvelle tâche > taper explorer.exe."
    },
    {
        "id": "R60", "categorie": "systeme",
        "conditions": ["explorer_plante"],
        "conclusion": "explorer_instable", "certitude": 0.77,
        "solution": "Lancer sfc /scannow en administrateur. Vérifier les extensions de shell avec ShellExView et désactiver les extensions tierces suspectes."
    },
    {
        "id": "R61", "categorie": "systeme",
        "conditions": ["redemarrage_spontane", "temperature_elevee"],
        "conclusion": "redemarrage_surchauffe", "certitude": 0.88,
        "solution": "Windows déclenche un redémarrage de protection thermique. Nettoyer la ventilation et renouveler la pâte thermique."
    },
    {
        "id": "R62", "categorie": "systeme",
        "conditions": ["redemarrage_spontane", "alimentation_instable"],
        "conclusion": "redemarrage_alimentation", "certitude": 0.84,
        "solution": "L'alimentation est insuffisante ou instable. Vérifier le bloc d'alimentation (wattage, condensateurs). Investir dans un onduleur."
    },

    # ══════════════════════════════════════════════════════════════════════════
    #  THERMIQUE
    # ══════════════════════════════════════════════════════════════════════════
    {
        "id": "R63", "categorie": "thermique",
        "conditions": ["pc_eteint_brusquement", "temperature_elevee"],
        "conclusion": "surchauffe_generale", "certitude": 0.88,
        "solution": "Nettoyer les filtres anti-poussière et les ventilateurs. Vérifier le flux d'air du boîtier (entrée avant, sortie arrière/haut)."
    },
    {
        "id": "R64", "categorie": "thermique",
        "conditions": ["pc_eteint_brusquement", "temperature_elevee", "laptop"],
        "conclusion": "surchauffe_laptop", "certitude": 0.90,
        "solution": "Utiliser le laptop sur surface dure. Nettoyer les grilles à l'air comprimé. Utiliser un pad de refroidissement."
    },
    {
        "id": "R65", "categorie": "thermique",
        "conditions": ["ventilation_bruyante", "temperature_elevee"],
        "conclusion": "ventilateur_insuffisant", "certitude": 0.80,
        "solution": "Le ventilateur tourne au maximum sans refroidir suffisamment. Renouveler la pâte thermique et nettoyer les ailettes du radiateur."
    },
    {
        "id": "R66", "categorie": "thermique",
        "conditions": ["pate_thermique_seche", "temperature_cpu_elevee"],
        "conclusion": "pate_thermique_a_remplacer", "certitude": 0.92,
        "solution": "Démonter le ventirad, nettoyer l'ancienne pâte avec de l'alcool isopropylique et appliquer une nouvelle pâte (ex : Arctic MX-4)."
    },
    {
        "id": "R67", "categorie": "thermique",
        "conditions": ["filtre_poussiere_bouche", "temperature_elevee"],
        "conclusion": "encrassement_thermique", "certitude": 0.90,
        "solution": "Nettoyer l'intérieur du boîtier à l'air comprimé (à l'extérieur). Nettoyer filtres, radiateur CPU et GPU."
    },
    {
        "id": "R68", "categorie": "thermique",
        "conditions": ["laptop_chauffe_sous_charge", "ventilation_bruyante"],
        "conclusion": "caloduc_laptop_defaillant", "certitude": 0.78,
        "solution": "Le caloduc (heatpipe) peut être encrassé ou défaillant. Nettoyage professionnel recommandé, voire remplacement du caloduc."
    },

    # ══════════════════════════════════════════════════════════════════════════
    #  BATTERIE
    # ══════════════════════════════════════════════════════════════════════════
    {
        "id": "R69", "categorie": "batterie",
        "conditions": ["laptop", "batterie_ne_charge_pas"],
        "conclusion": "probleme_batterie", "certitude": 0.78,
        "solution": "Tester avec un autre chargeur compatible. Si le problème persiste, la batterie ou le port de charge est défaillant."
    },
    {
        "id": "R70", "categorie": "batterie",
        "conditions": ["laptop", "batterie_decharge_rapide"],
        "conclusion": "batterie_usee", "certitude": 0.85,
        "solution": "Générer un rapport avec powercfg /batteryreport. Remplacer si la capacité est inférieure à 60 % de la valeur d'origine."
    },
    {
        "id": "R71", "categorie": "batterie",
        "conditions": ["laptop", "batterie_gonflee"],
        "conclusion": "batterie_dangereuse", "certitude": 0.99,
        "solution": "DANGER : Ne pas utiliser. Une batterie gonflée risque l'inflammation. La retirer immédiatement et la déposer en point de collecte DEEE."
    },
    {
        "id": "R72", "categorie": "batterie",
        "conditions": ["laptop", "chargeur_non_reconnu"],
        "conclusion": "chargeur_incompatible", "certitude": 0.82,
        "solution": "Utiliser exclusivement le chargeur officiel ou un chargeur certifié avec la même tension et le même ampérage."
    },
    {
        "id": "R73", "categorie": "batterie",
        "conditions": ["laptop", "batterie_pourcentage_bloque"],
        "conclusion": "calibration_batterie_requise", "certitude": 0.75,
        "solution": "Décharger complètement puis recharger à 100 % sans interruption. Ou recalibrer via les outils BIOS du constructeur."
    },

    # ══════════════════════════════════════════════════════════════════════════
    #  PÉRIPHÉRIQUES
    # ══════════════════════════════════════════════════════════════════════════
    {
        "id": "R74", "categorie": "peripherique",
        "conditions": ["clavier_non_detecte"],
        "conclusion": "probleme_clavier", "certitude": 0.80,
        "solution": "Rebrancher sur un autre port USB. Sur laptop, vérifier les pilotes HID dans le Gestionnaire de périphériques."
    },
    {
        "id": "R75", "categorie": "peripherique",
        "conditions": ["souris_non_detectee"],
        "conclusion": "probleme_souris", "certitude": 0.80,
        "solution": "Tester sur un autre port ou un autre PC. Vérifier la pile si souris sans fil. Réinstaller les pilotes HID."
    },
    {
        "id": "R76", "categorie": "peripherique",
        "conditions": ["imprimante_non_detectee"],
        "conclusion": "probleme_imprimante", "certitude": 0.80,
        "solution": "Réinstaller les pilotes depuis le site du fabricant. Vérifier que le service 'Spouleur d'impression' est actif dans services.msc."
    },
    {
        "id": "R77", "categorie": "peripherique",
        "conditions": ["peripherique_usb_non_detecte"],
        "conclusion": "probleme_port_usb", "certitude": 0.75,
        "solution": "Tester sur un autre port USB. Réinstaller les pilotes du contrôleur USB depuis le Gestionnaire de périphériques."
    },
    {
        "id": "R78", "categorie": "peripherique",
        "conditions": ["peripherique_usb_non_detecte", "port_usb_chauffe"],
        "conclusion": "port_usb_endommage", "certitude": 0.88,
        "solution": "Ne plus utiliser ce port. Utiliser un hub USB alimenté ou faire réparer/ressouder le port sur la carte mère."
    },
    {
        "id": "R79", "categorie": "peripherique",
        "conditions": ["touches_clavier_erronees"],
        "conclusion": "disposition_clavier_incorrecte", "certitude": 0.85,
        "solution": "Vérifier la langue du clavier dans Paramètres > Heure et langue > Langue. Supprimer les dispositions incorrectes (AZERTY/QWERTY)."
    },
    {
        "id": "R80", "categorie": "peripherique",
        "conditions": ["webcam_non_detectee"],
        "conclusion": "pilotes_webcam_manquants", "certitude": 0.78,
        "solution": "Vérifier dans le Gestionnaire de périphériques (Périphériques d'images). Réinstaller les pilotes depuis le site du fabricant."
    },
    {
        "id": "R81", "categorie": "peripherique",
        "conditions": ["bluetooth_non_fonctionnel"],
        "conclusion": "probleme_bluetooth", "certitude": 0.77,
        "solution": "Activer le Bluetooth dans Paramètres > Périphériques. Mettre à jour les pilotes Bluetooth dans le Gestionnaire de périphériques."
    },
    {
        "id": "R82", "categorie": "peripherique",
        "conditions": ["ecran_tactile_insensible", "pilotes_anciens"],
        "conclusion": "pilotes_ecran_tactile_obsoletes", "certitude": 0.80,
        "solution": "Désinstaller et réinstaller le pilote HID-Compliant Touch Screen dans le Gestionnaire de périphériques, puis recalibrer."
    },
    {
        "id": "R83", "categorie": "peripherique",
        "conditions": ["souris_saute"],
        "conclusion": "souris_surface_incompatible", "certitude": 0.70,
        "solution": "Nettoyer le capteur optique. Utiliser un tapis de souris opaque non brillant. Si persistant, vérifier les pilotes ou remplacer la souris."
    },

    # ══════════════════════════════════════════════════════════════════════════
    #  AUDIO
    # ══════════════════════════════════════════════════════════════════════════
    {
        "id": "R84", "categorie": "audio",
        "conditions": ["pas_de_son", "pilotes_audio_absents"],
        "conclusion": "probleme_audio", "certitude": 0.85,
        "solution": "Réinstaller les pilotes audio depuis le site du fabricant de la carte mère ou via le Gestionnaire de périphériques."
    },
    {
        "id": "R85", "categorie": "audio",
        "conditions": ["pas_de_son", "peripherique_audio_non_detecte"],
        "conclusion": "mauvais_peripherique_audio", "certitude": 0.88,
        "solution": "Clic droit sur l'icône son > Paramètres du son > Choisir le bon périphérique de sortie. Vérifier qu'il n'est pas 'désactivé'."
    },
    {
        "id": "R86", "categorie": "audio",
        "conditions": ["son_grele", "son_coupe_periodiquement"],
        "conclusion": "interference_audio", "certitude": 0.75,
        "solution": "Éloigner le câble audio des câbles d'alimentation. Tester avec un casque USB plutôt qu'un casque jack pour éliminer les interférences."
    },
    {
        "id": "R87", "categorie": "audio",
        "conditions": ["micro_non_detecte"],
        "conclusion": "micro_desactive_ou_absent", "certitude": 0.82,
        "solution": "Vérifier dans Paramètres > Son > Entrée que le microphone est sélectionné. Autoriser l'accès au micro dans les paramètres de confidentialité."
    },
    {
        "id": "R88", "categorie": "audio",
        "conditions": ["casque_non_reconnu"],
        "conclusion": "jack_audio_defaillant", "certitude": 0.80,
        "solution": "Tester avec un autre casque. Vérifier dans Realtek HD Audio Manager le type de prise détecté. Nettoyer le jack avec de l'air comprimé."
    },

    # ══════════════════════════════════════════════════════════════════════════
    #  SÉCURITÉ
    # ══════════════════════════════════════════════════════════════════════════
    {
        "id": "R89", "categorie": "securite",
        "conditions": ["popups_intempestifs", "navigateur_redirige"],
        "conclusion": "adware_hijacker", "certitude": 0.87,
        "solution": "Réinitialiser les paramètres du navigateur. Désinstaller les extensions inconnues. Scanner avec AdwCleaner (Malwarebytes)."
    },
    {
        "id": "R90", "categorie": "securite",
        "conditions": ["fichiers_chiffres", "message_rancon"],
        "conclusion": "ransomware", "certitude": 0.99,
        "solution": "Déconnecter immédiatement du réseau. Ne pas payer la rançon. Contacter un spécialiste cybersécurité et restaurer depuis une sauvegarde saine."
    },
    {
        "id": "R91", "categorie": "securite",
        "conditions": ["antivirus_desactive", "programmes_inconnus"],
        "conclusion": "malware_desactive_antivirus", "certitude": 0.92,
        "solution": "Démarrer en mode sans échec avec réseau, télécharger et exécuter Malwarebytes. Réactiver Windows Defender ensuite."
    },
    {
        "id": "R92", "categorie": "securite",
        "conditions": ["connexions_suspectes", "programmes_inconnus"],
        "conclusion": "infection_active_reseau", "certitude": 0.88,
        "solution": "Déconnecter du réseau immédiatement. Scanner avec Malwarebytes en mode sans échec. Analyser les connexions avec netstat -ano."
    },
    {
        "id": "R93", "categorie": "securite",
        "conditions": ["fichiers_systeme_modifies"],
        "conclusion": "integrite_systeme_compromise", "certitude": 0.85,
        "solution": "Exécuter sfc /scannow puis dism /online /cleanup-image /restorehealth. Si les fichiers ne peuvent être réparés, réinstaller Windows."
    },
    {
        "id": "R94", "categorie": "securite",
        "conditions": ["tache_planifiee_suspecte", "programmes_inconnus"],
        "conclusion": "persistance_malware", "certitude": 0.87,
        "solution": "Supprimer les tâches inconnues dans le Planificateur. Vérifier HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run dans le registre."
    },
    {
        "id": "R95", "categorie": "securite",
        "conditions": ["email_spam_envoye", "connexions_suspectes"],
        "conclusion": "compte_ou_pc_compromis", "certitude": 0.90,
        "solution": "Changer immédiatement les mots de passe depuis un autre appareil sain. Activer l'authentification à deux facteurs. Scanner le PC."
    },
    {
        "id": "R96", "categorie": "securite",
        "conditions": ["pare_feu_desactive", "antivirus_desactive"],
        "conclusion": "protection_systeme_desactivee", "certitude": 0.88,
        "solution": "Réactiver le pare-feu et Windows Defender depuis le Panneau de configuration. Si impossible, utiliser un antivirus live USB (Kaspersky Rescue Disk)."
    },

    # ══════════════════════════════════════════════════════════════════════════
    #  LOGICIEL / APPLICATIONS
    # ══════════════════════════════════════════════════════════════════════════
    {
        "id": "R97", "categorie": "logiciel",
        "conditions": ["application_crashe", "erreur_dll_manquante"],
        "conclusion": "dependance_logicielle_manquante", "certitude": 0.88,
        "solution": "Installer les redistribuables requis : Visual C++ Redistributable, .NET Framework, DirectX selon l'erreur (disponibles sur Microsoft)."
    },
    {
        "id": "R98", "categorie": "logiciel",
        "conditions": ["application_ne_demarre_pas", "erreur_vcredist"],
        "conclusion": "vcredist_manquant", "certitude": 0.90,
        "solution": "Télécharger et installer le package Visual C++ Redistributable 2015-2022 (x64 et x86) depuis le site officiel Microsoft."
    },
    {
        "id": "R99", "categorie": "logiciel",
        "conditions": ["application_crashe", "erreur_net_framework"],
        "conclusion": "dotnet_corrompu", "certitude": 0.87,
        "solution": "Réparer .NET Framework via le Panneau de configuration > Programmes. Ou utiliser l'outil de réparation .NET Framework de Microsoft."
    },
    {
        "id": "R100", "categorie": "logiciel",
        "conditions": ["installation_bloquee", "antivirus_desactive"],
        "conclusion": "installation_bloquee_par_politique", "certitude": 0.75,
        "solution": "Vérifier si une politique de groupe (gpedit.msc) bloque l'installation. Essayer en tant qu'administrateur avec UAC désactivé temporairement."
    },
    {
        "id": "R101", "categorie": "logiciel",
        "conditions": ["application_crashe", "pc_lent", "ram_insuffisante"],
        "conclusion": "ressources_insuffisantes_app", "certitude": 0.80,
        "solution": "L'application manque de ressources système. Fermer les autres applications, augmenter la RAM ou vérifier les prérequis matériels minimaux."
    },
]
