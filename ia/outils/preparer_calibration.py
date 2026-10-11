"""Prépare le jeu de calibration INT8 pour la quantification Hailo.

Sélectionne des images représentatives (lumières, altitudes, scènes vides et chargées)
dans l'ensemble d'ENTRAÎNEMENT — jamais dans le test — et les met au format d'entrée du
modèle (letterbox NxN, RGB). Sortie : un dossier d'images (hailomz --calib-path) et un
fichier .npy (N, H, W, 3) uint8 (DFC : --calib-set-path).

Usage : python outils/preparer_calibration.py --images travail/jeu_complet/images/train --n 1024
"""

import argparse
import random
import sys
from pathlib import Path

import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from sentinelle_ia.detecteurs.yolo import letterbox  # noqa: E402


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--images", required=True)
    parser.add_argument("--n", type=int, default=1024)
    parser.add_argument("--imgsz", type=int, default=640)
    parser.add_argument("--sortie", default="travail/calibration")
    parser.add_argument("--graine", type=int, default=0)
    args = parser.parse_args()

    images = sorted(p for p in Path(args.images).rglob("*") if p.suffix.lower() in {".jpg", ".jpeg", ".png"})
    if "test" in Path(args.images).parts:
        sys.exit("Refus : la calibration ne doit pas utiliser le jeu de test.")
    random.Random(args.graine).shuffle(images)
    images = images[:args.n]
    sortie = Path(args.sortie)
    (sortie / "images").mkdir(parents=True, exist_ok=True)
    lot = np.zeros((len(images), args.imgsz, args.imgsz, 3), np.uint8)
    for i, p in enumerate(images):
        carre, _, _ = letterbox(cv2.imread(str(p)), args.imgsz)
        cv2.imwrite(str(sortie / "images" / p.name), carre)
        lot[i] = carre[:, :, ::-1]
    np.save(sortie / "calibration.npy", lot)
    print(f"{len(images)} images de calibration -> {sortie}")


if __name__ == "__main__":
    main()
