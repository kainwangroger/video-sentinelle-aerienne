"""Convertit FOD-A (format Pascal VOC) au format YOLO des trois classes v1.

Toutes les catégories FOD-A (boulons, écrous, outils, pièces, cailloux…) sont regroupées
dans la classe « debris » (indice 2) pour ne pas disperser les exemples entre des classes
rares ; le nom d'origine est conservé dans notes_annotations.csv.

Entrée attendue (archive « FOD-A Version 2.1 Pascal VOC ») :
    <fod_a>/Annotations/*.xml
    <fod_a>/JPEGImages/*.jpg
    <fod_a>/ImageSets/Main/{train,val}.txt   (séparation fournie par FOD-A)

Sortie : <sortie>/images/{train,val}/, <sortie>/labels/{train,val}/, notes_annotations.csv.
Le jeu de test final ne doit PAS venir de FOD-A seul : il est constitué de séquences
du projet tenues à l'écart (voir donnees/README.md).

Usage : python outils/preparer_fod_a.py --fod-a /chemin/FOD-A_VOC --sortie travail/fod_a_yolo
"""

import argparse
import csv
import shutil
import xml.etree.ElementTree as ET
from pathlib import Path

INDICE_DEBRIS = 2


def lire_voc(chemin_xml):
    racine = ET.parse(chemin_xml).getroot()
    taille = racine.find("size")
    w, h = int(taille.find("width").text), int(taille.find("height").text)
    objets = []
    for obj in racine.findall("object"):
        boite = obj.find("bndbox")
        x1, y1, x2, y2 = (float(boite.find(k).text) for k in ("xmin", "ymin", "xmax", "ymax"))
        objets.append((obj.find("name").text.strip(), max(0, x1), max(0, y1), min(w, x2), min(h, y2)))
    return racine.findtext("filename"), w, h, objets


def convertir(fod_a, sortie, copier=True):
    fod_a, sortie = Path(fod_a), Path(sortie)
    splits = {}
    for split in ("train", "val"):
        fichier = fod_a / "ImageSets" / "Main" / f"{split}.txt"
        if fichier.exists():
            for ligne in fichier.read_text().split():
                splits[ligne.strip()] = split
    notes = []
    compte = {"train": 0, "val": 0, "ignorees": 0}
    for xml in sorted((fod_a / "Annotations").glob("*.xml")):
        identifiant = xml.stem
        split = splits.get(identifiant, "train")
        nom_image, w, h, objets = lire_voc(xml)
        image = fod_a / "JPEGImages" / (nom_image or f"{identifiant}.jpg")
        if not image.exists():
            image = fod_a / "JPEGImages" / f"{identifiant}.jpg"
        if not image.exists():
            compte["ignorees"] += 1
            continue
        (sortie / "images" / split).mkdir(parents=True, exist_ok=True)
        (sortie / "labels" / split).mkdir(parents=True, exist_ok=True)
        cible = sortie / "images" / split / f"foda_{identifiant}{image.suffix}"
        if copier:
            shutil.copy2(image, cible)
        elif not cible.exists():
            cible.symlink_to(image.resolve())
        lignes = []
        for nom, x1, y1, x2, y2 in objets:
            if x2 <= x1 or y2 <= y1:
                continue
            lignes.append(f"{INDICE_DEBRIS} {(x1 + x2) / 2 / w:.6f} {(y1 + y2) / 2 / h:.6f} {(x2 - x1) / w:.6f} {(y2 - y1) / h:.6f}")
            notes.append({"image": cible.name, "classe_v1": "debris", "categorie_fod_a": nom})
        (sortie / "labels" / split / f"foda_{identifiant}.txt").write_text("\n".join(lignes) + ("\n" if lignes else ""))
        compte[split] += 1
    with open(sortie / "notes_annotations.csv", "w", newline="", encoding="utf-8") as f:
        ecrivain = csv.DictWriter(f, ["image", "classe_v1", "categorie_fod_a"])
        ecrivain.writeheader()
        ecrivain.writerows(notes)
    return compte


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--fod-a", required=True, help="dossier FOD-A au format Pascal VOC")
    parser.add_argument("--sortie", default="travail/fod_a_yolo")
    parser.add_argument("--liens", action="store_true", help="liens symboliques au lieu de copier les images")
    args = parser.parse_args()
    print(convertir(args.fod_a, args.sortie, copier=not args.liens))


if __name__ == "__main__":
    main()
