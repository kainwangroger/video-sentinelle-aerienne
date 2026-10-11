# Entraînement, export et compilation pour Hailo

Chaîne : **YOLOv8s pré-entraîné → fine-tuning (PC) → ONNX → HEF (PC avec Hailo DFC) → Raspberry Pi 5 + AI HAT+**.
L'entraînement sur Raspberry Pi n'est ni nécessaire ni recommandé.

## 0. Essai de compatibilité, avant l'entraînement complet

La conversion dépend des versions du Hailo Dataflow Compiler, du Model Zoo et du modèle
exporté. **Compiler d'abord un YOLOv8s de test** :

```bash
python outils/exporter_onnx.py --poids modeles/yolov8s.pt --imgsz 640      # YOLOv8s COCO, sans fine-tuning
CLASSES=80 outils/compiler_hailo.sh modeles/yolov8s.onnx travail/calibration/images hailo8
```

Si la compilation échoue avec la version Hailo installée, retenir un détecteur de la famille
officiellement prise en charge par cette version (voir la liste du Hailo Model Zoo) pour la même tâche.

## 1. Fine-tuning (PC, GPU conseillé)

```bash
pip install -r requirements-dev.txt
outils/telecharger_donnees.sh                   # yolov8s.pt + FOD-A
python outils/verifier_dataset.py --data travail/jeu_projet
python outils/entrainer.py --data configs/data_mission.yaml --poids modeles/yolov8s.pt --epochs 100 --imgsz 640 --device 0
```

Sélection du modèle : **rappel des petits objets** et **nombre de fausses alertes** sur la
validation, pas un score global seul (`outils/evaluer.py`).

Si les débris occupent trop peu de pixels (avertissement de `verifier_dataset.py`) :
- entraîner/compiler une entrée plus grande (`--imgsz 960`), ou
- inférence par tuiles (`detecteur.tuiles: [2, 2]` dans la config) avec le modèle 640.
Ne retenir l'option que si la compilation Hailo et la cadence mesurée restent compatibles.

## 2. Export ONNX

```bash
python outils/exporter_onnx.py --poids modeles/sentinelle_yolov8s.pt --imgsz 640
```
Forme d'entrée fixe `1×3×640×640`, sans NMS (ajoutée par Hailo), opset 11.

## 3. Calibration INT8 et compilation HEF

Sur un PC x86_64 Linux avec le **Hailo Dataflow Compiler** et le **Hailo Model Zoo**
(Hailo Developer Zone) :

```bash
python outils/preparer_calibration.py --images travail/jeu_projet/images/train --n 1024
outils/compiler_hailo.sh modeles/sentinelle_yolov8s.onnx travail/calibration/images hailo8
```

- `hailo8` : AI HAT+ **26 TOPS** (référence) ; `hailo8l` : AI HAT+ 13 TOPS (repli).
- Calibration avec des images **représentatives** de l'entraînement (jamais du test).
- Le HEF contient la post-NMS Hailo pour 3 classes ; `sentinelle_ia/detecteurs/hailo.py` lit sa sortie.

## 4. Contrôle du modèle compilé

Comparer le HEF au modèle d'origine **sur le même jeu de test** :

```bash
# sur le PC
python outils/evaluer.py --data travail/jeu_projet --split test --moteur onnx  --modele modeles/sentinelle_yolov8s.onnx --rapport rapports/onnx.md
# sur le Raspberry Pi
python outils/evaluer.py --data travail/jeu_projet --split test --moteur hailo --modele modeles/sentinelle_yolov8s_hailo8.hef --rapport rapports/hef.md
```

Vérifier que la **baisse de rappel** due à la quantification reste acceptable, classe par
classe et pour les petits objets. Sinon : plus d'images de calibration, calibration plus
représentative, ou optimisation de niveau supérieur dans le Model Zoo.

## Vérification réalisée dans ce dépôt

Sur l'échantillon **synthétique** (3 époques sur CPU, uniquement pour tester les outils),
la chaîne entraînement → export ONNX → évaluation a été exécutée. Le détecteur ONNX du
module (`detecteurs/onnx.py`, pré/post-traitement maison) donne **exactement** les mêmes
rappels et précisions qu'Ultralytics sur le même jeu, ce qui valide le décodage. La
compilation HEF et le détecteur Hailo n'ont pas pu être exécutés ici (pas de DFC ni
d'accélérateur) : ils sont à valider sur la cible.
