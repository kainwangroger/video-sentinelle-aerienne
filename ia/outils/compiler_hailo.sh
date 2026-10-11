#!/usr/bin/env bash
# Compile le modèle ONNX en HEF pour l'accélérateur Hailo-8 (AI HAT+ 26 TOPS).
#
# À exécuter sur un PC x86_64 Linux (Ubuntu 22.04 conseillé) où sont installés le Hailo
# Dataflow Compiler (DFC) et le Hailo Model Zoo (hailomz), téléchargeables depuis le
# Hailo Developer Zone (compte gratuit). PAS sur le Raspberry Pi.
#
# Les versions doivent être cohérentes : DFC / Model Zoo utilisés pour compiler et HailoRT
# installé sur le Pi (`hailortcli fw-control identify`). Voir docs/conversion_hailo.md.
#
# Étapes réalisées par hailomz compile :
#   1. parse     : ONNX -> HAR (réseau Hailo), coupe aux 6 convolutions de sortie de YOLOv8 ;
#   2. optimize  : quantification INT8 avec le jeu de calibration (images d'entraînement) ;
#   3. compile   : HAR optimisé -> HEF, avec post-NMS YOLOv8 Hailo pour N classes.
#
# Usage : outils/compiler_hailo.sh modeles/sentinelle_yolov8s.onnx travail/calibration/images [hailo8|hailo8l]
set -euo pipefail

ONNX="${1:?chemin du modèle ONNX}"
CALIB="${2:?dossier d'images de calibration (outils/preparer_calibration.py)}"
ARCH="${3:-hailo8}"            # hailo8 = AI HAT+ 26 TOPS ; hailo8l = AI HAT+ 13 TOPS
CLASSES="${CLASSES:-3}"
SORTIE="${SORTIE:-modeles}"

command -v hailomz >/dev/null || { echo "hailomz introuvable : installer le Hailo Model Zoo et le DFC"; exit 1; }
mkdir -p "$SORTIE"

# Essai de compilation conseillé AVANT l'entraînement complet : lancer ce script sur un
# YOLOv8s exporté sans fine-tuning pour vérifier la compatibilité des versions.
hailomz compile yolov8s \
  --ckpt "$ONNX" \
  --hw-arch "$ARCH" \
  --calib-path "$CALIB" \
  --classes "$CLASSES" \
  --performance

HEF="yolov8s.hef"
[ -f "$HEF" ] || { echo "HEF non produit"; exit 1; }
mv "$HEF" "$SORTIE/sentinelle_yolov8s_${ARCH}.hef"
echo "HEF : $SORTIE/sentinelle_yolov8s_${ARCH}.hef"
echo "Copier ce fichier sur le Raspberry Pi dans ia/modeles/ puis lancer outils/evaluer.py --moteur hailo"
echo "pour comparer au modèle ONNX d'origine sur le même jeu de test."
