"""Exporte le meilleur modèle en ONNX avec une forme d'entrée fixée (étape avant compilation Hailo).

- forme fixe 1x3xNxN (la compilation Hailo l'exige) ;
- pas de NMS dans le graphe : la post-NMS est ajoutée par la chaîne Hailo ;
- opset 11, graphe simplifié.

Usage : python outils/exporter_onnx.py --poids modeles/sentinelle_yolov8s.pt --imgsz 640
"""

import argparse
import shutil
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--poids", required=True)
    parser.add_argument("--imgsz", type=int, default=640)
    parser.add_argument("--opset", type=int, default=11)
    parser.add_argument("--sortie", default=None, help="chemin .onnx (par défaut à côté des poids)")
    args = parser.parse_args()

    from ultralytics import YOLO

    chemin = YOLO(args.poids).export(format="onnx", imgsz=args.imgsz, opset=args.opset, simplify=True,
                                    dynamic=False, nms=False)
    if args.sortie:
        Path(args.sortie).parent.mkdir(parents=True, exist_ok=True)
        shutil.move(chemin, args.sortie)
        chemin = args.sortie

    import onnx

    modele = onnx.load(chemin)
    onnx.checker.check_model(modele)
    entree = modele.graph.input[0]
    forme = [d.dim_value for d in entree.type.tensor_type.shape.dim]
    sortie = [d.dim_value for d in modele.graph.output[0].type.tensor_type.shape.dim]
    print(f"ONNX : {chemin}  entrée {entree.name} {forme}  sortie {sortie}")


if __name__ == "__main__":
    main()
