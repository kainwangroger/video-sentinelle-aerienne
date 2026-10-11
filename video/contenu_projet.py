"""Vidéo « fiche projet » : scènes, textes à l'écran et narration.

Tout le contenu est tiré de fiche_projet.docx (drone hybride VTOL, CECFD 2026).
"""

SCENES = [
    {
        "id": "titre",
        "titre": "Sentinelle Aérienne",
        "phrases": [
            "Sentinelle Aérienne : un drone hybride VTOL pour la surveillance des zones sensibles au Togo.",
            "Un projet de l'équipe SkyVision Togo pour le Concours Étudiant de Conception et de Fabrication de Drones, CECFD 2026.",
        ],
    },
    {
        "id": "concept",
        "titre": "Le concept",
        "phrases": [
            "Les multirotors sont limités par leur autonomie, les avions par le besoin d'une piste.",
            "Sentinelle Aérienne combine le meilleur des deux mondes.",
        ],
    },
    {
        "id": "profil",
        "titre": "Profil de vol",
        "phrases": [
            "Elle décolle à la verticale depuis n'importe quel terrain, même confiné.",
            "Puis elle bascule en vol de croisière horizontal, pour couvrir de vastes zones en économisant son énergie.",
            "En cas de perte de signal, elle revient automatiquement à son point de départ.",
        ],
    },
    {
        "id": "innovation_ia",
        "titre": "Innovation 1 : IA embarquée",
        "phrases": [
            "Première innovation : une IA embarquée de détection en temps réel.",
            "Les images sont analysées à bord, avec une alerte immédiate en cas d'anomalie, sans dépendre d'une connexion.",
        ],
    },
    {
        "id": "innovation_liaison",
        "titre": "Innovation 2 : liaison sécurisée",
        "phrases": [
            "Deuxième innovation : une liaison sécurisée par conception.",
            "Communication chiffrée et authentifiée, avec détection du brouillage et du leurrage GPS.",
        ],
    },
    {
        "id": "configuration",
        "titre": "Configuration hybride VTOL",
        "phrases": [
            "Une aile fixe pour la croisière, des rotors de sustentation pour le vol vertical, et un moteur de propulsion dédié.",
            "Le contrôleur de vol pilote automatiquement la transition entre les deux modes.",
        ],
    },
    {
        "id": "structure",
        "titre": "Structure et propulsion",
        "phrases": [
            "La cellule, en fibre de carbone et composite, est modélisée sous SolidWorks.",
            "Moteurs, ESC et hélices sont dimensionnés selon la masse en charge et le profil de mission.",
        ],
    },
    {
        "id": "avionique",
        "titre": "Avionique et sécurité",
        "phrases": [
            "Un contrôleur de vol de type Pixhawk, sous ArduPilot ou PX4, avec centrale inertielle, baromètre et magnétomètre.",
            "GPS avec retour automatique, coupure d'urgence fail-safe, et supervision de la batterie LiPo.",
        ],
    },
    {
        "id": "charge_utile",
        "titre": "Charge utile modulaire",
        "phrases": [
            "Une caméra jour et nuit, visible et thermique, sur nacelle gyrostabilisée.",
            "L'architecture modulaire ouvre d'autres missions : cartographie, aide humanitaire.",
        ],
    },
    {
        "id": "station",
        "titre": "Station de contrôle au sol",
        "phrases": [
            "Au sol, une application mobile ou web affiche la télémétrie, planifie la mission et journalise les vols.",
            "La télémétrie MAVLink circule sur une liaison chiffrée et supervisée.",
        ],
    },
    {
        "id": "conformite",
        "titre": "Conformité aux exigences",
        "phrases": [
            "Les six exigences minimales du concours sont couvertes.",
            "L'autonomie visée est de 30 à 45 minutes, grâce au vol de croisière.",
        ],
    },
    {
        "id": "equipe",
        "titre": "L'équipe SkyVision Togo",
        "phrases": [
            "Cinq membres, cinq pôles : mécanique, logiciel embarqué, back-end, réseau, et intelligence artificielle.",
            "Sous la conduite du chef d'équipe, AWADE Constantin Israel.",
        ],
    },
    {
        "id": "calendrier",
        "titre": "Calendrier prévisionnel",
        "phrases": [
            "Le dossier de conception est soumis le 30 septembre 2026.",
            "Viennent ensuite le prototypage et les essais, en octobre et novembre.",
            "Démonstration finale : la semaine du 7 décembre 2026.",
        ],
    },
    {
        "id": "budget",
        "titre": "Budget prévisionnel indicatif",
        "phrases": [
            "Le budget est estimé entre 730 000 et 1 400 000 FCFA.",
            "La cellule, la propulsion et l'avionique en représentent la plus grande part.",
        ],
    },
    {
        "id": "conclusion",
        "titre": "Sentinelle Aérienne",
        "phrases": [
            "Sentinelle Aérienne : décoller partout, surveiller loin, alerter immédiatement.",
            "SkyVision Togo, au service de la sécurité des zones sensibles.",
        ],
    },
]

# Description des visuels, reprise dans le storyboard.
DESCRIPTIONS = {
    "titre": "silhouette du drone VTOL vue de dessus avec ondes radar, titre, équipe et concours.",
    "concept": "comparaison multirotor (autonomie limitée) / avion (piste nécessaire) → drone hybride VTOL.",
    "profil": "profil de mission animé : décollage vertical, transition, croisière, retour automatique au point de départ.",
    "innovation_ia": "drone en vol avec cône caméra, cadre de détection sur une anomalie au sol et alerte immédiate.",
    "innovation_liaison": "liaison drone-station chiffrée (cadenas), boucliers anti-brouillage et anti-leurrage GPS.",
    "configuration": "plan du drone : aile fixe, 4 rotors de sustentation, moteur de croisière, transition automatique.",
    "structure": "cellule carbone/composite et chaîne de dimensionnement moteurs → ESC → hélices.",
    "avionique": "contrôleur de vol au centre, capteurs IMU/baromètre/magnétomètre, GPS RTH, fail-safe, batterie LiPo.",
    "charge_utile": "nacelle gyrostabilisée visible + thermique, modules interchangeables (cartographie, humanitaire).",
    "station": "écran de station au sol : télémétrie, plan de mission, journal de vol, liaison MAVLink chiffrée.",
    "conformite": "les 6 exigences minimales du concours cochées une à une, jauge d'autonomie 30–45 min.",
    "equipe": "les cinq membres de l'équipe et leurs responsabilités.",
    "calendrier": "frise d'août à décembre 2026 avec les cinq jalons.",
    "budget": "barres de fourchettes par poste (FCFA) et total estimé.",
    "conclusion": "slogan final et signature SkyVision Togo — CECFD 2026.",
}
