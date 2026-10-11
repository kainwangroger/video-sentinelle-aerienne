#!/usr/bin/env bash
# Télécharge les données publiques et les poids de départ dans ia/travail/ et ia/modeles/.
#   - poids YOLOv8s pré-entraînés (GitHub Ultralytics) ;
#   - FOD-A v2.1 Pascal VOC (Google Drive, 412 Mo) via gdown si disponible.
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p modeles travail

if [ ! -f modeles/yolov8s.pt ]; then
  curl -fL -o modeles/yolov8s.pt https://github.com/ultralytics/assets/releases/download/v8.3.0/yolov8s.pt
fi
echo "Poids : modeles/yolov8s.pt"

FOD_ID="1RdErcq8PGRXZUOGauaACkQG44T-QyZ4x"   # FOD-A v2.1, Pascal VOC (lien du dépôt FOD-UNOmaha/FOD-data)
if [ ! -d travail/FOD-A ]; then
  if command -v gdown >/dev/null || pip install -q gdown; then
    gdown "$FOD_ID" -O travail/FOD-A_VOC.zip && mkdir -p travail/FOD-A && \
      (cd travail/FOD-A && unzip -q ../FOD-A_VOC.zip) || \
      echo "Échec : télécharger manuellement https://drive.google.com/file/d/$FOD_ID/view et décompresser dans travail/FOD-A"
  fi
fi
echo "Puis : python outils/preparer_fod_a.py --fod-a travail/FOD-A/<dossier_VOC> --sortie travail/fod_a_yolo"
