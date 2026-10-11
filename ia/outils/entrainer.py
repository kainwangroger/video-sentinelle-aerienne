"""Fine-tuning de YOLOv8s pré-entraîné sur les classes de la mission (sur ordinateur, pas sur le Pi).

Les poids pré-entraînés (COCO) fournissent les caractéristiques visuelles générales ;
le fine-tuning les adapte aux petits objets, à la caméra et à l'angle de vue du drone.
La tête de classification passe à 3 classes : personne, vehicule, debris.

Usage :
    python outils/entrainer.py --data travail/jeu_complet/data.yaml --epochs 100 --imgsz 640
    python outils/entrainer.py --data donnees/echantillon_synthetique/jeu_yolo/data.yaml --epochs 3 --essai
"""

import argparse
import json
import shutil
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--data", required=True, help="data.yaml (train/val/test, 3 classes)")
    parser.add_argument("--poids", default="yolov8s.pt", help="poids de départ (pré-entraînés)")
    parser.add_argument("--epochs", type=int, default=100)
    parser.add_argument("--imgsz", type=int, default=640, help="taille d'entrée ; doit être celle compilée pour Hailo")
    parser.add_argument("--batch", type=int, default=16)
    parser.add_argument("--device", default=None, help="0 pour le GPU, cpu sinon")
    parser.add_argument("--nom", default="sentinelle_yolov8s")
    parser.add_argument("--projet", default="runs")
    parser.add_argument("--essai", action="store_true", help="essai rapide sur CPU (vérification de la chaîne)")
    parser.add_argument("--sortie", default="modeles", help="dossier où copier best.pt")
    args = parser.parse_args()

    from ultralytics import YOLO

    modele = YOLO(args.poids)
    options = dict(data=args.data, epochs=args.epochs, imgsz=args.imgsz, batch=args.batch, project=args.projet,
                   name=args.nom, exist_ok=True, seed=0, deterministic=True,
                   # augmentations adaptées à la vue aérienne : rotations et retournements possibles,
                   # pas de déformation de perspective forte
                   fliplr=0.5, flipud=0.5, degrees=10.0, scale=0.5, mosaic=1.0, hsv_v=0.4)
    if args.device is not None:
        options["device"] = args.device
    if args.essai:
        options.update(batch=4, workers=0, device="cpu", plots=False, val=True)
    modele.train(**options)

    meilleur = Path(modele.trainer.save_dir) / "weights" / "best.pt"
    Path(args.sortie).mkdir(parents=True, exist_ok=True)
    cible = Path(args.sortie) / f"{args.nom}.pt"
    shutil.copy2(meilleur, cible)
    resume = {"poids": str(cible), "data": args.data, "imgsz": args.imgsz, "epochs": args.epochs,
              "depart": args.poids}
    (Path(args.sortie) / f"{args.nom}.json").write_text(json.dumps(resume, indent=1), encoding="utf-8")
    print(f"Meilleurs poids : {cible}")


if __name__ == "__main__":
    main()
