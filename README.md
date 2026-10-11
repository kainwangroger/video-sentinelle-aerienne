# Sentinelle Aérienne — vidéo explicative

Vidéo en motion design (≈ 3 min, 1920×1080, 30 fps, H.264 + AAC) présentant la fiche technique
du module d'IA embarquée **Sentinelle Aérienne** (SkyVision Togo, CECFD 2026 — ANAC).

- Vidéo : [`output/sentinelle_aerienne.mp4`](output/sentinelle_aerienne.mp4)
- Storyboard (14 scènes, durées exactes) : [`storyboard.md`](storyboard.md)
- Source : [`fiche_technique.docx`](fiche_technique.docx), extraite en Markdown dans `output/fiche_extraite.md`

Tout est généré par code : aucune image, vidéo ou musique téléchargée. Les visuels (drone, piste,
schémas, pictogrammes) sont dessinés avec Pillow ; la voix off française est synthétisée hors-ligne
avec [Piper](https://github.com/rhasspy/piper) ; ffmpeg assemble le tout.

## Régénérer la vidéo

Prérequis : Python 3.10+, ffmpeg, et de préférence la police Inter (sinon DejaVu est utilisée).

```bash
pip install -r requirements.txt
./scripts/get_voice.sh            # voix française « siwis » (≈ 60 Mo) dans voices/
python3 src/build.py              # → output/sentinelle_aerienne.mp4 + storyboard.md
```

Options utiles :

| Commande | Effet |
|---|---|
| `python3 src/build.py --apercu` | une image PNG par scène dans `output/apercu/` (rapide, pour vérifier la mise en page) |
| `python3 src/build.py --sans-voix` | vidéo sous-titrée sans voix off (durées estimées à partir du texte) |
| `python3 src/build.py --vitesse 1.0` | voix plus lente (0.9 par défaut ; plus petit = plus rapide) |
| `python3 src/build.py --crf 18` | meilleure qualité vidéo, fichier plus lourd |
| `python3 src/extract_docx.py` | ré-extrait le docx dans `output/fiche_extraite.md` |

Le rendu prend quelques minutes sur 4 cœurs.

## Modifier le contenu

| Fichier | Rôle |
|---|---|
| `src/content.py` | titres des scènes et phrases de narration (= sous-titres) ; dictionnaire de prononciation pour les sigles (YOLOv8s, ONNX, HAT+…) |
| `src/visuels.py` | animation de chaque scène ; les éléments apparaissent au début de la phrase qui en parle |
| `src/gfx.py` | palette bleu nuit / cyan, polices, formes et pictogrammes |
| `src/timeline.py` | minutage : la durée de chaque scène suit la durée réelle de la voix off |
| `src/tts.py` | synthèse vocale Piper |
| `src/build.py` | rendu des images (multiprocessus), sous-titres, fondus, encodage ffmpeg, storyboard |

Pour changer une phrase, modifier `src/content.py` puis relancer `python3 src/build.py` : le minutage,
les sous-titres et `storyboard.md` se recalent automatiquement.

## Voix off : limites connues

La voix « siwis » utilisée est la version publiée dans les releases GitHub de Piper (v0.0.2,
licence CC-BY 4.0, jeu de données SIWIS). Les versions plus récentes de cette voix sont hébergées sur
Hugging Face, inaccessible depuis l'environnement de génération. Cette ancienne version a été
entraînée sans le signe de nasalisation : les voyelles nasales (« on », « an », « in ») peuvent
sonner légèrement moins nasales que dans une voix humaine. Pour une narration de qualité studio,
enregistrer sa propre voix sur `storyboard.md` et remplacer la piste audio :

```bash
ffmpeg -i output/sentinelle_aerienne.mp4 -i ma_voix.wav -map 0:v -map 1:a -c:v copy -c:a aac -shortest sortie.mp4
```

Les sous-titres sont incrustés dans l'image et restent donc lisibles sans le son.

## Contenu fidèle à la fiche

La vidéo reprend les engagements de prudence de la fiche : l'IA est une aide à l'inspection,
aucun taux de performance n'est annoncé avant mesure, la position au sol n'est ajoutée qu'après
calibration et les objets inconnus sont signalés « à vérifier » sans détection universelle revendiquée.
Les valeurs de la fiche d'événement (scène 11) sont un exemple fictif, signalé comme tel à l'écran.
