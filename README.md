# Sentinelle Aérienne — SkyVision Togo (CECFD 2026 — ANAC)

Ce dépôt regroupe :

1. **La fiche technique complète du drone pour débutants** (`drone/`) : chaque composant
   expliqué, calculs de dimensionnement, paramètres ArduPilot, check-lists, schémas, Word et PDF ;
2. **Le module d'IA embarquée** (`ia/`) : implémentation de la fiche technique du lot IA
   (code, outils, données, configuration, déploiement, tests) ;
3. **Quatre vidéos** générées par code (`video/`, `output/`), dont « Le SA-1 de A à Z »
   (chaque composant, simulation de mission) et « De la conception au premier vol »
   (fabrication et assemblage animés en 3D).

| Source | Contenu |
|---|---|
| [`fiche_technique.docx`](fiche_technique.docx) | Conception du module d'IA embarquée |
| [`fiche_projet.docx`](fiche_projet.docx) | Drone hybride VTOL : concept, technique, équipe, calendrier, budget |

## 1. Le drone expliqué de A à Z → [`drone/README.md`](drone/README.md)

| Document | Contenu |
|---|---|
| [`drone/fiche_technique_complete.md`](drone/fiche_technique_complete.md) ([Word](drone/fiche_technique_complete.docx), [PDF](drone/fiche_technique_complete.pdf)) | Les bases du vol, puis chaque composant : à quoi il sert, comment il marche, notre choix et pourquoi |
| [`drone/guide_conception_assemblage.md`](drone/guide_conception_assemblage.md) ([Word](drone/guide_conception_assemblage.docx), [PDF](drone/guide_conception_assemblage.pdf)) | De la conception au premier vol : fabrication, assemblage, câblage, configuration, essais |
| [`drone/glossaire.md`](drone/glossaire.md) | Tous les termes techniques expliqués |
| [`drone/calculs/`](drone/calculs/) | Masse, portance, puissance, autonomie (script + résultats) |
| [`drone/parametres_ardupilot/`](drone/parametres_ardupilot/) | Paramètres de départ du contrôleur de vol |
| [`drone/checklists/`](drone/checklists/) | Avant vol, après vol, urgences |

## 2. Module d'IA embarquée → [`ia/README.md`](ia/README.md)

Raspberry Pi 5 + AI HAT+ 26 TOPS (Hailo-8), détecteur YOLOv8s fine-tuné (personne, véhicule,
débris), suivi léger, zone d'intérêt, statut « à vérifier » pour les objets sans classe fiable,
événements avec image de preuve, journal hors connexion et liaison sécurisée vers la station sol.

```bash
cd ia
pip install -r requirements-dev.txt
python -m pytest -q tests                                  # 26 tests
python -m sentinelle_ia --config configs/demo.yaml         # démonstration sur vidéo synthétique
```

Données : [`ia/donnees/README.md`](ia/donnees/README.md) (FOD-A, images du projet, négatifs,
guide d'annotation, échantillon synthétique). Conversion Hailo :
[`ia/docs/conversion_hailo.md`](ia/docs/conversion_hailo.md). Déploiement :
[`ia/docs/deploiement_raspberry.md`](ia/docs/deploiement_raspberry.md).

## 3. Vidéos

| Vidéo | Durée | Storyboard |
|---|---|---|
| [`output/sentinelle_aerienne.mp4`](output/sentinelle_aerienne.mp4) — fiche technique du module IA | 3 min 08 | [`storyboard.md`](storyboard.md) |
| [`output/sentinelle_aerienne_projet.mp4`](output/sentinelle_aerienne_projet.mp4) — fiche projet (drone VTOL) | 2 min 47 | [`storyboard_projet.md`](storyboard_projet.md) |
| [`output/sa1_de_a_a_z/`](output/sa1_de_a_a_z/) — **le SA-1 de A à Z**, 16 chapitres + vidéo complète | 36 min 26 | [`storyboard_sa1_de_a_a_z.md`](storyboard_sa1_de_a_a_z.md) |
| [`output/sa1_conception_assemblage/`](output/sa1_conception_assemblage/) — **de la conception au premier vol**, assemblage animé en 3D, 13 chapitres | 19 min 41 | [`storyboard_sa1_conception_assemblage.md`](storyboard_sa1_conception_assemblage.md) |

1920×1080, 30 fps, H.264 + AAC, voix off française hors-ligne (Piper) et sous-titres incrustés.
Tout est dessiné par code (Pillow) : aucune image, vidéo ou musique téléchargée.

### Régénérer

Prérequis : Python 3.10+, ffmpeg, de préférence la police Inter (sinon DejaVu).

```bash
pip install -r requirements.txt
./scripts/get_voice.sh                         # voix française « siwis » (≈ 60 Mo) dans voices/
python3 video/build.py                         # fiche technique → output/sentinelle_aerienne.mp4
python3 video/build.py --fiche projet          # fiche projet  → output/sentinelle_aerienne_projet.mp4
python3 video/build.py --fiche az              # SA-1 de A à Z → output/sa1_de_a_a_z/ (≈ 1 h de rendu)
python3 video/build.py --fiche az --chapitres 15   # un seul chapitre
python3 video/build.py --fiche assemblage      # conception et assemblage 3D → output/sa1_conception_assemblage/
```

| Option | Effet |
|---|---|
| `--apercu` | une image PNG par scène dans `output/apercu_<fiche>/` |
| `--sans-voix` | sous-titres seuls (durées estimées sur le texte) |
| `--vitesse 1.0` | voix plus lente (0.9 par défaut) |
| `--crf 18` | meilleure qualité, fichier plus lourd |

| Fichier | Rôle |
|---|---|
| `video/contenu_technique.py`, `video/contenu_projet.py` | scènes et narration (= sous-titres) |
| `video/visuels_technique.py`, `video/visuels_projet.py` | animation de chaque scène |
| `video/prononciation.py` | prononciation des sigles par la voix off |
| `video/gfx.py` | palette bleu nuit / cyan, polices, formes, pictogrammes |
| `video/az/` | longue vidéo : chapitres (`chapitres_*.py`), gabarits de scènes, pictogrammes, animations, simulation de mission |
| `video/assemblage/` | moteur 3D (`moteur3d.py`), maquette du SA-1 pièce par pièce (`modele_sa1.py`), scènes d'assemblage animées |
| `video/timeline.py`, `video/tts.py`, `video/build.py` | minutage, synthèse vocale, rendu et encodage |

### Voix off : limite connue

La voix « siwis » utilisée (Piper v0.0.2, CC-BY 4.0) est une ancienne version : elle a été
entraînée sans le signe de nasalisation, les sons « on / an / in » peuvent sonner moins
nasals. Pour une narration studio, enregistrer sa voix sur le storyboard puis :

```bash
ffmpeg -i output/sentinelle_aerienne.mp4 -i ma_voix.wav -map 0:v -map 1:a -c:v copy -c:a aac -shortest sortie.mp4
```
