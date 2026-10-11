"""Chapitres 8 à 13 : électricité, avionique et IA, logiciel, contrôles au sol, essais en vol, validation."""

from az.chapitres_1 import S

from .chapitres_a import SANS_HELICES

ESC = ["esc_av_gauche", "esc_ar_gauche", "esc_av_droite", "esc_ar_droite"]
# demi-ailes et équipements d'aile retirés pour travailler à l'intérieur du fuselage
AILES_RETIREES = ["longeron", "aile_gauche", "aile_droite", "aileron_gauche", "aileron_droit", "pitot", "servo_gauche", "servo_droit"]

CHAPITRES = [
    # ------------------------------------------------------------------ 8
    {
        "id": "integration_electrique", "titre": "L'intégration électrique", "titre_court": "ÉLECTRICITÉ",
        "sous_titre": "Puissance, distribution et câblage", "picto": "batterie_icone",
        "sommaire": ["ESC, batterie et module de puissance", "La distribution", "Les règles de câblage", "La première mise sous tension"],
        "introduction": [
            "La mécanique est en place. Il faut maintenant amener l'énergie à chaque composant.",
            "C'est l'étape où une erreur peut détruire du matériel : on avance lentement et on contrôle tout.",
        ],
        "scenes": [
            S("ESC, batterie et module de puissance", "assemblage3d", [
                "Les quatre ESC des moteurs verticaux se fixent sur les poutres, juste sous les moteurs : le souffle des hélices les refroidit en vol.",
                "Leurs câbles de puissance cheminent le long des poutres, maintenus tous les dix centimètres, jusqu'au fuselage.",
                "La batterie se place sur son rail, à l'avant du fuselage, avec un connecteur XT90 anti-étincelle.",
                "Le module de puissance s'insère entre la batterie et la distribution : il mesure la tension et le courant, et alimente le contrôleur de vol.",
            ], base=SANS_HELICES, transparent=True, masquer=AILES_RETIREES,
              ajouts=[{"phrase": 0, "pieces": ESC, "label": "ESC refroidis par le souffle"},
                      {"phrase": 2, "pieces": ["batterie"], "label": "LiPo 6S sur rail, XT90-S"},
                      {"phrase": 3, "pieces": ["module_puissance"], "label": "Module de puissance"}],
              etapes=[("ESC sur les poutres", "sous les moteurs"), ("Câbles le long des poutres", "attachés tous les 10 cm"),
                      ("Batterie sur rail", "XT90 anti-étincelle"), ("Module de puissance", "mesure V et A")],
              camera={"az": (0.8, 1.3), "el": 0.65, "dist": 2.6, "cible": (-0.15, 0, 0)}),
            S("La distribution", "distribution", [
                "Voici le schéma de distribution. Les ESC des moteurs verticaux reçoivent directement la tension de la batterie, par des câbles épais de 12 à 14 AWG.",
                "L'ESC du moteur de croisière aussi.",
                "Le contrôleur de vol est alimenté par le module de puissance.",
                "Les servos ont leur propre convertisseur, un BEC de 5 à 6 volts.",
                "Le Raspberry Pi et son accélérateur ont un BEC dédié de 5 volts et 5 ampères.",
                "Et la nacelle a sa propre alimentation, pour éviter les parasites dans l'image.",
            ]),
            S("Les règles de câblage", "puces", [
                "Quelques règles font la différence entre un drone fiable et un drone capricieux. On sépare les câbles de puissance des câbles de signal.",
                "On torsade les paires de fils qui transportent du courant fort, pour limiter les perturbations magnétiques.",
                "On éloigne tous les câbles de puissance du compas, sinon le cap devient faux.",
                "Et on soude proprement, on gaine chaque soudure, et aucun câble ne doit pouvoir toucher une hélice.",
            ], points=[("Puissance ≠ signal", "Chemins séparés"), ("Paires torsadées", "Moins de champ magnétique"),
                       ("Loin du compas", "Sinon le cap est faux"), ("Soudures gainées", "Aucun câble près des hélices")],
              picto="esc", echelle=1.4),
            S("La première mise sous tension", "flux", [
                "Avant la première mise sous tension, on contrôle au multimètre la continuité de chaque liaison, et l'absence de court-circuit entre le plus et le moins.",
                "Puis on alimente le drone à travers un limiteur de courant, ou avec une petite batterie : en cas d'erreur, rien ne brûle.",
                "On vérifie que chaque élément s'allume, et que le contrôleur de vol lit une tension correcte.",
                "Toujours sans hélices, bien sûr.",
            ], etapes=[("Continuité", "multimètre"), ("Pas de court-circuit", "plus / moins"), ("Limiteur de courant", "ou petite batterie"),
                       ("Tout s'allume", "tension lue par le FC"), ("Sans hélices", "toujours")],
              apparitions=[0, 0, 1, 2, 3]),
        ],
    },
    # ------------------------------------------------------------------ 9
    {
        "id": "avionique_ia", "titre": "Avionique, caméra et IA à bord", "titre_court": "AVIONIQUE ET IA",
        "sous_titre": "Installer le cerveau, les sens et les yeux du drone", "picto": "controleur",
        "sommaire": ["Contrôleur de vol et radio", "L'ordinateur IA", "Les points de montage"],
        "introduction": [
            "Il reste à installer l'électronique de bord : le contrôleur de vol, la radio, et l'ordinateur d'intelligence artificielle.",
            "Leur position compte autant que leur branchement.",
        ],
        "scenes": [
            S("Contrôleur de vol, radio et IA", "assemblage3d", [
                "Le contrôleur de vol se place au plus près du centre de gravité, sur une mousse anti-vibration, sa flèche tournée vers l'avant.",
                "La radio de télémétrie se place à l'arrière, ses antennes dirigées vers le bas, hors des pièces en carbone, qui font écran aux ondes radio.",
                "Le Raspberry Pi 5 et sa carte AI HAT plus prennent place dans la baie arrière, avec un ventilateur.",
                "Il est relié à la caméra, à son BEC de 5 volts, et au contrôleur de vol par une liaison série MAVLink.",
            ], base=SANS_HELICES + ESC + ["batterie", "module_puissance"], transparent=True, masquer=AILES_RETIREES,
              ajouts=[{"phrase": 0, "pieces": ["controleur"], "label": "FC au CG, flèche vers l'avant"},
                      {"phrase": 1, "pieces": ["radio", "antenne_g", "antenne_d"], "label": "Antennes hors du carbone"},
                      {"phrase": 2, "pieces": ["raspberry", "hat_ia"], "label": "Pi 5 + AI HAT+ ventilés"}],
              etapes=[("Contrôleur de vol", "au CG, sur mousse"), ("Radio de télémétrie", "antennes dégagées"),
                      ("Raspberry Pi 5 + AI HAT+", "baie arrière ventilée"), ("Liaisons", "caméra, BEC 5 V, MAVLink")],
              camera={"az": (1.0, 1.4), "el": 0.75, "dist": 1.9, "cible": (-0.08, 0, 0)}),
            S("Les points de montage", "tableau", [
                "Récapitulons les points de montage à vérifier.",
                "Le contrôleur de vol au centre de gravité, flèche vers l'avant ; le GNSS en haut de son mât, flèche vers l'avant aussi.",
                "Le capteur de vitesse air relié au Pitot par des tubes sans pincement, le télémètre laser sous le fuselage avec une vue dégagée.",
                "Les antennes de la radiocommande à 90 degrés l'une de l'autre, jamais masquées par le carbone ; l'interrupteur de sécurité et le buzzer accessibles.",
            ], colonnes=["Élément", "Montage", "Point clé"], largeurs=[460, 620, 600],
              lignes=[["Contrôleur de vol", "Au CG, sur mousse", "Flèche vers l'avant"], ["GNSS + compas", "Haut du mât, arrière", "Loin des ESC et batterie"],
                      ["Vitesse air", "Capteur + tubes", "Tubes sans pincement"], ["Télémètre laser", "Sous le fuselage", "Vue dégagée"],
                      ["Récepteur RC", "Antennes à 90°", "Jamais derrière le carbone"], ["Sécurité, buzzer, feux", "Accessibles", "Visibles au sol"]],
              apparitions=[1, 1, 2, 2, 3, 3]),
        ],
    },
    # ------------------------------------------------------------------ 10
    {
        "id": "configuration", "titre": "La configuration logicielle", "titre_court": "LOGICIEL",
        "sous_titre": "Donner vie au drone", "picto": "ordinateur",
        "sommaire": ["Installer ArduPilot", "Les calibrations", "Le test des moteurs", "Sécurité et IA"],
        "introduction": [
            "Le drone est complet. Il faut maintenant lui apprendre à voler : c'est la configuration logicielle.",
            "Tout se fait depuis la station au sol, drone attaché, et toujours sans hélices.",
        ],
        "scenes": [
            S("Installer et paramétrer ArduPilot", "flux", [
                "On installe d'abord ArduPlane sur le contrôleur de vol, depuis le logiciel Mission Planner.",
                "On charge le fichier de paramètres de départ du SA-1, disponible dans le dépôt, et on active le mode quadplane.",
                "Après redémarrage, on affecte chaque sortie du contrôleur : quatre moteurs verticaux, le moteur de croisière et les servos, selon le câblage réel.",
            ], etapes=[("Installer ArduPlane", "Mission Planner"), ("Paramètres de départ", "sentinelle_sa1.param"), ("Activer le quadplane", "Q_ENABLE = 1"),
                       ("Affecter les sorties", "moteurs et servos"), ("Redémarrer et vérifier", "messages d'erreur")],
              apparitions=[0, 1, 1, 2, 2]),
            S("Les calibrations", "tableau", [
                "Viennent ensuite les calibrations. Les accéléromètres se calibrent en posant le drone dans six positions successives.",
                "Le compas se calibre en faisant tourner le drone dans tous les sens, loin de tout objet métallique.",
                "On calibre aussi la radiocommande, les ESC si nécessaire, et le zéro du capteur de vitesse air.",
            ], colonnes=["Calibration", "Méthode"], largeurs=[520, 1160],
              lignes=[["Accéléromètres", "Six positions : à plat, sur chaque côté, nez haut, nez bas, dos"], ["Compas", "Rotation dans tous les sens, loin du métal"],
                      ["Radiocommande", "Course complète de chaque manche et interrupteur"], ["ESC", "Si protocole PWM (inutile en DShot)"],
                      ["Vitesse air", "Zéro au sol, Pitot protégé du vent"]],
              apparitions=[0, 1, 2, 2, 2]),
            S("Le test des moteurs", "sens_helices", [
                "Sans hélices, on teste chaque moteur, un par un, depuis la station : on vérifie que le bon moteur tourne, dans le bon sens.",
                "Deux moteurs doivent tourner dans le sens horaire, et deux dans le sens antihoraire, en diagonale ; on inverse deux fils de phase si un moteur tourne à l'envers.",
                "On vérifie aussi le sens des gouvernes : en mode avion assisté, on incline le drone à la main, et chaque gouverne doit réagir pour le redresser.",
            ]),
            S("Sécurité et intelligence artificielle", "puces", [
                "On configure ensuite tous les fail-safes : radiocommande, station au sol, batterie basse et critique, et la coupure d'urgence sur un interrupteur protégé.",
                "On définit le géorepérage et on active la signature MAVLink, en partageant la clé secrète entre le drone et la station.",
                "Enfin, on installe le logiciel de l'intelligence artificielle sur le Raspberry Pi, avec les pilotes Hailo, le modèle compilé et le service de détection.",
            ], points=[("Fail-safes", "Radio, station, batterie, coupure d'urgence"), ("Géorepérage et signature", "Zone autorisée, clé MAVLink partagée"),
                       ("Logiciel IA", "Pilotes Hailo, modèle HEF, service sentinelle-ia")], picto="bouclier"),
        ],
    },
    # ------------------------------------------------------------------ 11
    {
        "id": "controles_sol", "titre": "Les contrôles au sol", "titre_court": "CONTRÔLES AU SOL",
        "sous_titre": "Tout vérifier avant de quitter le sol", "picto": "outil",
        "sommaire": ["Masse et centre de gravité", "Banc de poussée", "Fail-safes et portée radio"],
        "introduction": [
            "Avant le premier vol, on vérifie tout au sol.",
            "Chaque contrôle a un critère clair : s'il n'est pas atteint, on ne vole pas.",
        ],
        "scenes": [
            S("Masse et centre de gravité", "assemblage3d", [
                "On pèse d'abord le drone complet, batterie comprise : il ne doit pas dépasser 6,4 kilos.",
                "On vérifie ensuite le centre de gravité, en posant le drone sur deux doigts sous l'aile, au repère de 25 à 30 pour cent de la corde.",
                "Il doit être en équilibre, ou très légèrement nez bas. Sinon, on fait glisser la batterie sur son rail jusqu'au bon équilibre.",
            ], base=["tout"], cg=True, camera={"az": (1.1, 1.4), "el": (0.45, 0.5), "dist": (3.2, 2.9)}),
            S("Le banc de poussée", "puces", [
                "Chaque moteur vertical, avec son hélice et la batterie de vol, est mesuré sur un banc de poussée.",
                "On relève la poussée, le courant et la température, du ralenti jusqu'au plein gaz.",
                "Le critère : au moins 2,9 kilogrammes-force par moteur. C'est la confirmation, ou la correction, de tout le dimensionnement.",
            ], points=[("Chaque moteur + hélice", "Avec la batterie de vol"), ("Poussée, courant, température", "Du ralenti au plein gaz"),
                       ("Critère : ≥ 2,9 kgf", "Confirme le dimensionnement")], picto="moteur", echelle=1.4),
            S("Les autres contrôles", "tableau", [
                "D'autres contrôles complètent la liste. Les gouvernes : débattements, sens et absence de jeu.",
                "Les vibrations : moteurs en marche, drone attaché, on lit le journal de la centrale inertielle.",
                "La portée radio : en mode portée réduite, à 30 mètres, le contrôle doit être maintenu.",
                "Et les fail-safes, hélices démontées : on coupe la radiocommande, on débranche la télémétrie, et le mode doit changer comme prévu. Enfin, l'IA doit envoyer son message de test.",
            ], colonnes=["Contrôle", "Méthode", "Critère"], largeurs=[400, 700, 580],
              lignes=[["Gouvernes", "Débattements, sens, jeu", "Aucun jeu, bon sens"], ["Vibrations", "Moteurs en marche, drone attaché", "Sous les seuils ArduPilot"],
                      ["Portée radio", "Mode portée réduite à 30 m", "Contrôle maintenu"], ["Fail-safes", "Couper RC et télémétrie, sans hélices", "Mode conforme"],
                      ["IA", "Message de test", "Alerte reçue à la station"]],
              apparitions=[0, 1, 2, 3, 3]),
        ],
    },
    # ------------------------------------------------------------------ 12
    {
        "id": "essais_vol", "titre": "Les essais en vol", "titre_court": "ESSAIS EN VOL",
        "sous_titre": "Progressivement, un objectif à la fois", "picto": "vtol_profil",
        "sommaire": ["Le premier stationnaire", "Le plan d'essais", "La première transition", "L'analyse des journaux"],
        "introduction": [
            "Le grand moment arrive : les premiers vols.",
            "Ils se font sur un terrain dégagé et autorisé, sans public, avec les check-lists, et en augmentant la difficulté pas à pas.",
        ],
        "scenes": [
            S("Le premier stationnaire", "vol3d", [
                "Premier vol : un simple stationnaire, à deux ou trois mètres de hauteur, pendant une minute, en mode QHOVER.",
                "Le télépilote observe : le drone doit être stable, sans oscillation, et le bruit régulier.",
                "On atterrit, on télécharge le journal, et on vérifie les vibrations et la consommation avant de continuer.",
            ], hauteur=0.8, mode="QHOVER", camera={"az": (0.7, 1.5), "el": 0.25, "dist": 3.4}),
            S("Le plan d'essais", "tableau", [
                "Le plan d'essais avance par étapes. Après le premier stationnaire, le réglage automatique du vol vertical, puis la tenue de position.",
                "Vient ensuite la première transition, à au moins 40 mètres de hauteur, puis le réglage automatique en avion et la calibration de la vitesse air.",
                "Ensuite, les missions automatiques, les fail-safes testés en vol, et des vols de plus en plus longs.",
                "Et enfin, les vols avec la caméra et l'intelligence artificielle.",
            ], colonnes=["Vol", "Objectif", "Critère"], largeurs=[200, 820, 660],
              lignes=[["1", "Stationnaire 2–3 m (QHOVER)", "Stable, vibrations faibles"], ["2–3", "Réglage vertical, tenue de position", "PID stables, dérive < 1 m"],
                      ["4", "Première transition à ≥ 40 m", "Transition propre"], ["5–6", "Réglage avion, vitesse air, mission courte", "Trajectoire suivie"],
                      ["7", "Fail-safes en vol", "Réaction conforme"], ["8", "Endurance 10, 20, 30 min", "Réserve ≥ 20 %"],
                      ["9", "Caméra et IA en vol", "Alertes exploitables"]],
              apparitions=[0, 0, 1, 1, 2, 2, 3]),
            S("La première transition", "vol3d", [
                "La première transition est l'essai le plus délicat. Le drone monte à la verticale à une hauteur de sécurité.",
                "Puis le moteur de croisière démarre, le drone accélère, et l'aile prend progressivement le relais des moteurs verticaux.",
                "Le télépilote garde le doigt sur l'interrupteur de retour en vertical : au moindre doute, les moteurs verticaux reprennent la main.",
            ], hauteur=1.0, transition=True, mode="QHOVER → FBWA", etat="Vitesse air : en hausse",
              camera={"az": (1.3, 1.9), "el": 0.22, "dist": (3.6, 4.4)}),
            S("Analyser chaque vol", "puces", [
                "Après chaque vol, on analyse les journaux du contrôleur : vibrations, consommation, qualité du GPS, comportement pendant la transition.",
                "On compare les mesures aux estimations de la conception, et on met à jour le dimensionnement.",
                "Et on ne passe à l'essai suivant que si tous les critères de l'essai précédent sont atteints.",
            ], points=[("Journaux de vol", "Vibrations, énergie, GPS, transition"), ("Mesures contre calculs", "Mise à jour du dimensionnement"),
                       ("Un critère, une étape", "On ne brûle aucune étape")], picto="ordinateur"),
        ],
    },
    # ------------------------------------------------------------------ 13
    {
        "id": "validation", "titre": "Validation et démonstration", "titre_court": "VALIDATION",
        "sous_titre": "Le SA-1 prêt pour le CECFD 2026", "picto": "bouclier",
        "sommaire": ["La conformité", "Le dossier", "Le drone terminé"],
        "introduction": [
            "Dernière étape : prouver que le drone répond au cahier des charges.",
        ],
        "scenes": [
            S("La conformité", "tableau", [
                "Chaque exigence du concours est vérifiée et documentée : navigation GPS avec retour automatique, coupure d'urgence, liaison sécurisée.",
                "L'autonomie est mesurée en vol, la charge utile est validée, et la documentation de conception est complète.",
                "Le dossier rassemble les plans, le dimensionnement, les performances mesurées, l'analyse de sécurité et les journaux de vol.",
            ], colonnes=["Exigence", "Preuve"], largeurs=[700, 980],
              lignes=[["GPS + retour automatique", "Essais RTL enregistrés"], ["Coupure d'urgence", "Test au sol et procédure"],
                      ["Liaison sécurisée", "Chiffrement et signature actifs"], ["Autonomie", "Vol d'endurance mesuré"],
                      ["Charge utile", "Vols caméra et IA"], ["Documentation", "Dossier complet"]],
              colonne_accent=1, apparitions=[0, 0, 0, 1, 1, 2]),
            S("Le SA-1 terminé", "assemblage3d", [
                "Et voici le SA-1 terminé : conçu sur ordinateur, fabriqué en atelier, assemblé pièce par pièce, configuré, contrôlé et testé en vol.",
                "Il décolle partout, vole loin et longtemps, voit de jour comme de nuit, et alerte l'opérateur grâce à son intelligence artificielle embarquée.",
                "Rendez-vous la semaine du 7 décembre 2026 pour la démonstration. Le guide complet de conception et d'assemblage se trouve dans le dépôt du projet, dans le dossier drone. Merci de votre attention.",
            ], base=["tout"], rotation=8, camera={"az": (2.0, 4.4), "el": (0.35, 0.5), "dist": (3.0, 2.4)}),
        ],
    },
]
