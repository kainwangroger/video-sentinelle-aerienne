# Données du module IA

Ce dossier décrit **toutes les sources de données** du lot IA, comment les obtenir et comment
les préparer. Les jeux réels (plusieurs Go) ne sont pas versionnés dans Git : seuls
l'inventaire, les règles d'annotation et un petit échantillon synthétique le sont.

| Dossier / fichier | Contenu |
|---|---|
| `inventaire_sources.csv` | Inventaire des sources : usage, licence, état d'accès |
| `guide_annotation.md` | Classes v1 et règles d'annotation (à suivre dans CVAT) |
| `echantillon_synthetique/` | Données **dessinées** pour tester la chaîne (voir plus bas) |
| `../outils/telecharger_donnees.sh` | Téléchargement de FOD-A et des poids YOLOv8s |

## 1. Sources

| Source | Rôle | Limites |
|---|---|---|
| **FOD-A** (Munyer et al., 2021) | Départ public pour les débris de piste : 31 catégories, plus de 30 000 instances, vues piste/taxiway, conditions de lumière et météo | Vues au sol rapprochées : ne remplacent pas la vue aérienne de la caméra du projet |
| **Images propres au projet** | Indispensables : hauteur, angle, stabilisation, résolution et lumière de la mission | À filmer avec la caméra retenue, sur une surface d'essai autorisée, objets placés à distances contrôlées |
| **YOLO-URD (2026)** | Collecte UAV de débris à 2–6 m, ~6 000 images brutes | Accès et licence à vérifier avant usage ; le dispositif n'en dépend pas |
| **Exemples négatifs** | Piste vide, marquages, ombres, reflets, flaques, herbe, salissures, objets hors zone | Réduisent les fausses alertes ; à collecter avec les mêmes séquences |
| **Poids pré-entraînés YOLOv8s (COCO)** | Personnes et véhicules : caractéristiques générales | Licence AGPL-3.0 d'Ultralytics à respecter |

### FOD-A

- Dépôt : https://github.com/FOD-UNOmaha/FOD-data
- Version recommandée : **FOD-A v2.1 au format Pascal VOC** (412 Mo, images 300×300, séparation train/val fournie).
- Article : https://arxiv.org/abs/2110.03072
- Conversion : `python outils/preparer_fod_a.py --fod-a <dossier_VOC> --sortie travail/fod_a_yolo`
  (toutes les catégories → classe `debris`, nom d'origine gardé dans `notes_annotations.csv`).

## 2. Chaîne de préparation

```bash
# 1. Images du projet : vidéos -> images à annoter (préfixe = séquence, images floues écartées)
python outils/extraire_images_video.py --videos videos_essais/*.mp4 --sortie travail/a_annoter --pas 15

# 2. Annotation dans CVAT (rectangles, 3 classes), export « YOLO 1.1 » -> travail/annotees/{images,labels}

# 3. Répartition PAR SÉQUENCE ; le test final contient des conditions jamais vues au réglage
python outils/repartir_sequences.py --source travail/annotees --sortie travail/jeu_projet \
    --val 0.15 --test 0.2 --test-impose vol-nuit-01 essai-pluie-01

# 4. FOD-A converti, ajouté à l'entraînement et à la validation uniquement
python outils/preparer_fod_a.py --fod-a ~/FOD-A_VOC --sortie travail/fod_a_yolo
#    puis lister les deux sources dans un data.yaml (voir configs/data_mission.yaml)

# 5. Contrôles avant entraînement (format, classes, doublons, fuite entre ensembles, taille des objets)
python outils/verifier_dataset.py --data travail/jeu_projet
```

Règles de séparation (fiche technique, §5.2) :
- les vidéos sont réparties **par séquence ou session** : entraînement, validation et test ne
  contiennent pas d'images presque identiques d'une même séquence ;
- le **jeu de test final reste isolé** jusqu'à l'évaluation et inclut des conditions et des
  objets qui n'ont pas servi au réglage ;
- la **calibration INT8** n'utilise que des images d'entraînement.

## 3. Échantillon synthétique

`echantillon_synthetique/` est produit par `outils/generer_donnees_synthetiques.py` :

- `jeu_yolo/` : 120 images 640×640 de piste vue du ciel, 12 séquences séparées en
  train/val/test, avec personnes, véhicules, débris et scènes négatives ;
- `demo/piste_demo.mp4` : survol de 24 s avec la vérité terrain par image (`piste_demo_annotations.json`) ;
- `demo/reference_piste_libre.jpg` : référence pour la branche d'anomalie.

**Ces images sont dessinées.** Elles servent à vérifier les outils et la chaîne logicielle
(tests, démonstration, essai d'entraînement), **jamais** à entraîner ou évaluer le modèle de
mission. Aucun résultat obtenu dessus ne doit être présenté comme une performance.

## 4. Collecte sur site

La collecte sur un site aéronautique réel se fait uniquement avec l'autorisation du site et
selon ses consignes de sécurité. Les premières mises en scène se font sur une surface contrôlée.
