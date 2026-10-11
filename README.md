# Sentinelle Aérienne — SkyVision Togo (CECFD 2026 — ANAC)

Ce dépôt regroupe :

1. **Le module d'IA embarquée** (`ia/`) : implémentation de la fiche technique du lot IA
   (code, outils, données, configuration, déploiement, tests) ;
2. **Deux vidéos explicatives** générées par code (`video/`, `output/`).

| Source | Contenu |
|---|---|
| [`fiche_technique.docx`](fiche_technique.docx) | Conception du module d'IA embarquée |
| [`fiche_projet.docx`](fiche_projet.docx) | Drone hybride VTOL : concept, technique, équipe, calendrier, budget |

## 1. Module d'IA embarquée → [`ia/README.md`](ia/README.md)

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

## 2. Vidéos explicatives

| Vidéo | Durée | Storyboard |
|---|---|---|
| [`output/sentinelle_aerienne.mp4`](output/sentinelle_aerienne.mp4) — fiche technique du module IA | 3 min 08 | [`storyboard.md`](storyboard.md) |
| [`output/sentinelle_aerienne_projet.mp4`](output/sentinelle_aerienne_projet.mp4) — fiche projet (drone VTOL) | 2 min 47 | [`storyboard_projet.md`](storyboard_projet.md) |

1920×1080, 30 fps, H.264 + AAC, voix off française hors-ligne (Piper) et sous-titres incrustés.
Tout est dessiné par code (Pillow) : aucune image, vidéo ou musique téléchargée.

### Régénérer

Prérequis : Python 3.10+, ffmpeg, de préférence la police Inter (sinon DejaVu).

```bash
pip install -r requirements.txt
./scripts/get_voice.sh                         # voix française « siwis » (≈ 60 Mo) dans voices/
python3 video/build.py                         # fiche technique → output/sentinelle_aerienne.mp4
python3 video/build.py --fiche projet          # fiche projet  → output/sentinelle_aerienne_projet.mp4
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
| `video/timeline.py`, `video/tts.py`, `video/build.py` | minutage, synthèse vocale, rendu et encodage |

### Voix off : limite connue

La voix « siwis » utilisée (Piper v0.0.2, CC-BY 4.0) est une ancienne version : elle a été
entraînée sans le signe de nasalisation, les sons « on / an / in » peuvent sonner moins
nasals. Pour une narration studio, enregistrer sa voix sur le storyboard puis :

```bash
ffmpeg -i output/sentinelle_aerienne.mp4 -i ma_voix.wav -map 0:v -map 1:a -c:v copy -c:a aac -shortest sortie.mp4
```
