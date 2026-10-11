"""Vidéo « fiche technique » : scènes, textes à l'écran et narration.

Chaque scène contient une liste de phrases. Le texte affiché en sous-titre est
la phrase telle qu'écrite ici ; la voix off lit la même phrase après passage
dans prononciation.py (sigles, chiffres, anglicismes).
Tout le contenu est tiré de fiche_technique.docx.
"""

SCENES = [
    {
        "id": "titre",
        "titre": "Sentinelle Aérienne",
        "sous_titre": "Module d'intelligence artificielle embarquée",
        "phrases": [
            "Sentinelle Aérienne : conception du module d'intelligence artificielle embarquée.",
            "Projet SkyVision Togo, CECFD 2026, soumis à l'ANAC.",
        ],
    },
    {
        "id": "mission",
        "titre": "La mission",
        "phrases": [
            "Sur une piste, un débris, une personne ou un véhicule imprévu représente un danger.",
            "Sentinelle Aérienne aide à l'inspection depuis un drone, en analysant les images directement à bord.",
        ],
    },
    {
        "id": "decision",
        "titre": "Décision de conception",
        "phrases": [
            "Le cœur du système : un Raspberry Pi 5 associé à un AI HAT+ de 26 TOPS.",
            "Il analyse localement le flux de la caméra stabilisée et détecte trois familles : personnes, véhicules, et débris au sol.",
            "Un suivi vidéo léger relie les détections et évite les alertes répétées.",
        ],
    },
    {
        "id": "perimetre",
        "titre": "Périmètre fonctionnel",
        "phrases": [
            "L'inférence se fait à bord : aucune image n'est envoyée vers le cloud.",
            "Limite assumée : l'IA aide l'inspection, mais ne certifie pas qu'une piste est libre et ne commande pas l'aéronef.",
        ],
    },
    {
        "id": "architecture",
        "titre": "Architecture retenue",
        "phrases": [
            "L'architecture forme une chaîne unique.",
            "Caméra stabilisée, Raspberry Pi 5, détecteur YOLOv8s compilé pour Hailo.",
            "Puis suivi et contrôle de zone, événement et preuve locale, liaison sécurisée, jusqu'à la station au sol.",
        ],
    },
    {
        "id": "choix",
        "titre": "Pourquoi un détecteur compact ?",
        "phrases": [
            "La tâche exige une sortie stable, localisée et rapide sur de petites cibles.",
            "Ni modèle génératif, ni segmentation : des rectangles suffisent, pour un coût bien plus faible.",
        ],
    },
    {
        "id": "modele",
        "titre": "Le détecteur YOLOv8s",
        "phrases": [
            "Un YOLOv8s pré-entraîné est adapté par fine-tuning aux images de la mission.",
            "Pour chaque candidat, il renvoie une classe, un score et un rectangle.",
            "Premier essai en 640 × 640 pixels, avec découpage en tuiles si les débris sont trop petits.",
        ],
    },
    {
        "id": "inconnus",
        "titre": "Objets sans classe connue",
        "phrases": [
            "Un candidat crédible sans classe fiable devient un objet « à vérifier », avec son image.",
            "Une détection d'anomalie, comparée à une piste libre, sera testée si l'alignement est fiable.",
            "Le suivi confirme la persistance sur plusieurs images, sans revendiquer une détection universelle.",
        ],
    },
    {
        "id": "donnees",
        "titre": "Données d'entraînement",
        "phrases": [
            "FOD-A : 31 catégories et plus de 30 000 objets annotés.",
            "Des images propres au projet, filmées avec la caméra retenue.",
            "Et des exemples négatifs : ombres, reflets, marquages, pour réduire les fausses alertes.",
        ],
    },
    {
        "id": "protocole",
        "titre": "Entraînement et conversion",
        "phrases": [
            "Six étapes : préparer, adapter, évaluer.",
            "Puis exporter en ONNX, compiler au format HEF, quantifier en INT8, et déployer sur le Raspberry Pi.",
            "Le critère : le rappel des petits objets et les fausses alertes, pas un score global.",
        ],
    },
    {
        "id": "alerte",
        "titre": "Traitement embarqué et alerte",
        "phrases": [
            "Chaque détection confirmée produit un événement : heure, classe ou statut « à vérifier », score, rectangle et image de preuve.",
            "Hors connexion, l'analyse continue et les événements sont stockés localement.",
            "La position au sol ne sera ajoutée qu'après calibration de la caméra.",
        ],
    },
    {
        "id": "materiel",
        "titre": "Matériel embarqué",
        "phrases": [
            "Côté matériel : Raspberry Pi 5, AI HAT+ 26 TOPS avec NPU Hailo-8, et la caméra stabilisée du projet.",
        ],
    },
    {
        "id": "validation",
        "titre": "Validation",
        "phrases": [
            "La validation progresse en trois temps : vidéos enregistrées, caméra sur banc, puis plateforme au sol.",
            "Rappel par classe, fausses alertes, latence, température : aucun taux ne sera annoncé avant mesure.",
        ],
    },
    {
        "id": "conclusion",
        "titre": "Sentinelle Aérienne",
        "phrases": [
            "Sentinelle Aérienne : une IA embarquée, sobre et mesurable, au service de la sécurité des pistes.",
            "Un travail d'équipe, intégré avec les lots mécanique, station sol, back-end et réseau.",
        ],
    },
]

# Description des visuels, reprise dans le storyboard.
DESCRIPTIONS = {
    "titre": "drone vu de dessus avec ondes radar, titre animé, crédits SkyVision Togo / CECFD 2026 — ANAC.",
    "mission": "piste en perspective, apparition d'un débris, d'une personne et d'un véhicule signalés ; un drone survole la piste avec son cône de caméra.",
    "decision": "cartes Raspberry Pi 5 + AI HAT+ 26 TOPS, caméra vers les trois familles détectées, suivi d'un objet image après image (1 objet = 1 alerte).",
    "perimetre": "tableau du périmètre : zone analysée, classes v1, traitement à bord (cloud barré), limite en ambre.",
    "architecture": "schéma fonctionnel en 7 blocs apparaissant au fil de la narration, paquet de données circulant, légende accélérateur / logiciel.",
    "choix": "trois cartes : détecteur compact (retenu), modèle génératif / vision-langage et segmentation (non retenus).",
    "modele": "vue aérienne schématique avec rectangles de détection étiquetés, grille de tuiles 640×640, étapes YOLOv8s → fine-tuning → sortie.",
    "inconnus": "candidat inconnu encadré en pointillés avec « ? », trois niveaux : objet à vérifier, détection d'anomalie, suivi multi-images.",
    "donnees": "quatre cartes de sources : FOD-A (compteurs 31 catégories / 30 000+ instances), images du projet, YOLO-URD, exemples négatifs.",
    "protocole": "frise en 6 étapes qui s'allument (préparer → déployer) et encadré du critère de sélection.",
    "alerte": "fiche d'événement (exemple fictif) qui se remplit, liaison drone-station coupée puis stockage local, position au sol après calibration.",
    "materiel": "empilement matériel (alimentation, Raspberry Pi 5, AI HAT+, caméra) et notes : repli 13 TOPS, stockage, outils.",
    "validation": "trois étapes de validation puis essai en vol autorisé, six mesures, bandeau « aucun taux annoncé avant mesure ».",
    "conclusion": "titre final, slogan et les cinq lots de l'équipe avec leurs responsables.",
}
