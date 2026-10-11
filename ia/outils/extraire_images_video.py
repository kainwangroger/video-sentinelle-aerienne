"""Extrait des images à annoter depuis les vidéos de la caméra du projet.

Chaque vidéo est une séquence : les images portent le préfixe de la séquence
(<sequence>_<numero>.jpg) pour que la séparation entraînement / validation / test se
fasse par séquence et non image par image (pas d'images presque identiques de part et
d'autre). Les images trop floues sont écartées (variance du laplacien).

Usage :
    python outils/extraire_images_video.py --videos videos_essais/*.mp4 --sortie travail/a_annoter --pas 15
"""

import argparse
import csv
import re
from pathlib import Path

import cv2


def nom_sequence(chemin):
    return re.sub(r"[^A-Za-z0-9-]+", "-", Path(chemin).stem).strip("-")


def extraire(video, sortie, pas=15, seuil_flou=60.0):
    cap = cv2.VideoCapture(str(video))
    seq = nom_sequence(video)
    gardees, floues, i = 0, 0, 0
    lignes = []
    while True:
        ok, image = cap.read()
        if not ok:
            break
        if i % pas == 0:
            nettete = cv2.Laplacian(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), cv2.CV_64F).var()
            if nettete < seuil_flou:
                floues += 1
            else:
                nom = f"{seq}_{i:06d}.jpg"
                cv2.imwrite(str(sortie / nom), image, [cv2.IMWRITE_JPEG_QUALITY, 95])
                lignes.append({"image": nom, "sequence": seq, "video": str(video), "image_video": i,
                               "nettete": round(nettete, 1)})
                gardees += 1
        i += 1
    cap.release()
    return seq, gardees, floues, lignes


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--videos", nargs="+", required=True)
    parser.add_argument("--sortie", default="travail/a_annoter")
    parser.add_argument("--pas", type=int, default=15, help="garder une image sur N")
    parser.add_argument("--seuil-flou", type=float, default=60.0)
    args = parser.parse_args()
    sortie = Path(args.sortie)
    sortie.mkdir(parents=True, exist_ok=True)
    inventaire = []
    for video in args.videos:
        seq, n, floues, lignes = extraire(video, sortie, args.pas, args.seuil_flou)
        inventaire += lignes
        print(f"{seq} : {n} images gardées, {floues} écartées (floues)")
    with open(sortie / "inventaire_images.csv", "w", newline="", encoding="utf-8") as f:
        ecrivain = csv.DictWriter(f, ["image", "sequence", "video", "image_video", "nettete"])
        ecrivain.writeheader()
        ecrivain.writerows(inventaire)


if __name__ == "__main__":
    main()
