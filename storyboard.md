# Storyboard — Sentinelle Aérienne

Vidéo explicative 1920×1080, 30 fps. Ce fichier est régénéré par `python3 video/build.py` :
les durées correspondent exactement à la vidéo produite.

| # | Début | Durée | Scène | Narration / sous-titres |
|---|---|---|---|---|
| 1 | 0:00.0 | 9.9 s | **Sentinelle Aérienne** | Sentinelle Aérienne : conception du module d'intelligence artificielle embarquée.<br>Projet SkyVision Togo, CECFD 2026, soumis à l'ANAC. |
| 2 | 0:09.9 | 11.4 s | **La mission** | Sur une piste, un débris, une personne ou un véhicule imprévu représente un danger.<br>Sentinelle Aérienne aide à l'inspection depuis un drone, en analysant les images directement à bord. |
| 3 | 0:21.3 | 16.7 s | **Décision de conception** | Le cœur du système : un Raspberry Pi 5 associé à un AI HAT+ de 26 TOPS.<br>Il analyse localement le flux de la caméra stabilisée et détecte trois familles : personnes, véhicules, et débris au sol.<br>Un suivi vidéo léger relie les détections et évite les alertes répétées. |
| 4 | 0:38.0 | 11.1 s | **Périmètre fonctionnel** | L'inférence se fait à bord : aucune image n'est envoyée vers le cloud.<br>Limite assumée : l'IA aide l'inspection, mais ne certifie pas qu'une piste est libre et ne commande pas l'aéronef. |
| 5 | 0:49.1 | 15.4 s | **Architecture retenue** | L'architecture forme une chaîne unique.<br>Caméra stabilisée, Raspberry Pi 5, détecteur YOLOv8s compilé pour Hailo.<br>Puis suivi et contrôle de zone, événement et preuve locale, liaison sécurisée, jusqu'à la station au sol. |
| 6 | 1:04.6 | 11.5 s | **Pourquoi un détecteur compact ?** | La tâche exige une sortie stable, localisée et rapide sur de petites cibles.<br>Ni modèle génératif, ni segmentation : des rectangles suffisent, pour un coût bien plus faible. |
| 7 | 1:16.1 | 15.7 s | **Le détecteur YOLOv8s** | Un YOLOv8s pré-entraîné est adapté par fine-tuning aux images de la mission.<br>Pour chaque candidat, il renvoie une classe, un score et un rectangle.<br>Premier essai en 640 × 640 pixels, avec découpage en tuiles si les débris sont trop petits. |
| 8 | 1:31.8 | 16.9 s | **Objets sans classe connue** | Un candidat crédible sans classe fiable devient un objet « à vérifier », avec son image.<br>Une détection d'anomalie, comparée à une piste libre, sera testée si l'alignement est fiable.<br>Le suivi confirme la persistance sur plusieurs images, sans revendiquer une détection universelle. |
| 9 | 1:48.7 | 13.0 s | **Données d'entraînement** | FOD-A : 31 catégories et plus de 30 000 objets annotés.<br>Des images propres au projet, filmées avec la caméra retenue.<br>Et des exemples négatifs : ombres, reflets, marquages, pour réduire les fausses alertes. |
| 10 | 2:01.7 | 16.6 s | **Entraînement et conversion** | Six étapes : préparer, adapter, évaluer.<br>Puis exporter en ONNX, compiler au format HEF, quantifier en INT8, et déployer sur le Raspberry Pi.<br>Le critère : le rappel des petits objets et les fausses alertes, pas un score global. |
| 11 | 2:18.3 | 15.8 s | **Traitement embarqué et alerte** | Chaque détection confirmée produit un événement : heure, classe ou statut « à vérifier », score, rectangle et image de preuve.<br>Hors connexion, l'analyse continue et les événements sont stockés localement.<br>La position au sol ne sera ajoutée qu'après calibration de la caméra. |
| 12 | 2:34.1 | 9.0 s | **Matériel embarqué** | Côté matériel : Raspberry Pi 5, AI HAT+ 26 TOPS avec NPU Hailo-8, et la caméra stabilisée du projet. |
| 13 | 2:43.1 | 13.0 s | **Validation** | La validation progresse en trois temps : vidéos enregistrées, caméra sur banc, puis plateforme au sol.<br>Rappel par classe, fausses alertes, latence, température : aucun taux ne sera annoncé avant mesure. |
| 14 | 2:56.0 | 11.7 s | **Sentinelle Aérienne** | Sentinelle Aérienne : une IA embarquée, sobre et mesurable, au service de la sécurité des pistes.<br>Un travail d'équipe, intégré avec les lots mécanique, station sol, back-end et réseau. |

Durée totale : 3 min 8 s

## Contenu visuel par scène

1. **Sentinelle Aérienne** — drone vu de dessus avec ondes radar, titre animé, crédits SkyVision Togo / CECFD 2026 — ANAC.
2. **La mission** — piste en perspective, apparition d'un débris, d'une personne et d'un véhicule signalés ; un drone survole la piste avec son cône de caméra.
3. **Décision de conception** — cartes Raspberry Pi 5 + AI HAT+ 26 TOPS, caméra vers les trois familles détectées, suivi d'un objet image après image (1 objet = 1 alerte).
4. **Périmètre fonctionnel** — tableau du périmètre : zone analysée, classes v1, traitement à bord (cloud barré), limite en ambre.
5. **Architecture retenue** — schéma fonctionnel en 7 blocs apparaissant au fil de la narration, paquet de données circulant, légende accélérateur / logiciel.
6. **Pourquoi un détecteur compact ?** — trois cartes : détecteur compact (retenu), modèle génératif / vision-langage et segmentation (non retenus).
7. **Le détecteur YOLOv8s** — vue aérienne schématique avec rectangles de détection étiquetés, grille de tuiles 640×640, étapes YOLOv8s → fine-tuning → sortie.
8. **Objets sans classe connue** — candidat inconnu encadré en pointillés avec « ? », trois niveaux : objet à vérifier, détection d'anomalie, suivi multi-images.
9. **Données d'entraînement** — quatre cartes de sources : FOD-A (compteurs 31 catégories / 30 000+ instances), images du projet, YOLO-URD, exemples négatifs.
10. **Entraînement et conversion** — frise en 6 étapes qui s'allument (préparer → déployer) et encadré du critère de sélection.
11. **Traitement embarqué et alerte** — fiche d'événement (exemple fictif) qui se remplit, liaison drone-station coupée puis stockage local, position au sol après calibration.
12. **Matériel embarqué** — empilement matériel (alimentation, Raspberry Pi 5, AI HAT+, caméra) et notes : repli 13 TOPS, stockage, outils.
13. **Validation** — trois étapes de validation puis essai en vol autorisé, six mesures, bandeau « aucun taux annoncé avant mesure ».
14. **Sentinelle Aérienne** — titre final, slogan et les cinq lots de l'équipe avec leurs responsables.
