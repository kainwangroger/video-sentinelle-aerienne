"""Répartit un jeu annoté (format YOLO) en entraînement / validation / test PAR SÉQUENCE.

La séquence d'une image est le préfixe de son nom avant le dernier « _ » (convention de
outils/extraire_images_video.py), ou fournie par un CSV image -> sequence. Toutes les
images d'une séquence vont dans le même ensemble. Les séquences listées dans
--test-impose (conditions ou objets non vus au réglage) vont d'office au test final.

Entrée : <source>/images/*.jpg et <source>/labels/*.txt (export CVAT « YOLO 1.1 » ou équivalent).
Sortie : <sortie>/images/{train,val,test}, <sortie>/labels/{train,val,test}, data.yaml.

Usage :
    python outils/repartir_sequences.py --source travail/annotees --sortie travail/jeu_projet \
        --val 0.15 --test 0.15 --test-impose vol-nuit-03 essai-pluie-01
"""

import argparse
import csv
import json
import random
import shutil
from collections import defaultdict
from pathlib import Path

EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp"}


def sequence_de(nom):
    stem = Path(nom).stem
    return stem.rsplit("_", 1)[0] if "_" in stem else stem


def repartir(source, sortie, part_val=0.15, part_test=0.15, test_impose=(), graine=0, correspondance=None):
    source, sortie = Path(source), Path(sortie)
    images = [p for p in sorted((source / "images").rglob("*")) if p.suffix.lower() in EXTENSIONS]
    groupes = defaultdict(list)
    for img in images:
        seq = (correspondance or {}).get(img.name) or sequence_de(img.name)
        groupes[seq].append(img)
    sequences = sorted(groupes)
    rng = random.Random(graine)
    rng.shuffle(sequences)
    total = len(images)
    affectation = {s: "test" for s in sequences if s in set(test_impose)}
    compte = {"train": 0, "val": 0, "test": sum(len(groupes[s]) for s in affectation)}
    for s in sequences:
        if s in affectation:
            continue
        if compte["test"] < part_test * total:
            split = "test"
        elif compte["val"] < part_val * total:
            split = "val"
        else:
            split = "train"
        affectation[s] = split
        compte[split] += len(groupes[s])
    for seq, split in affectation.items():
        for img in groupes[seq]:
            (sortie / "images" / split).mkdir(parents=True, exist_ok=True)
            (sortie / "labels" / split).mkdir(parents=True, exist_ok=True)
            shutil.copy2(img, sortie / "images" / split / img.name)
            label = source / "labels" / f"{img.stem}.txt"
            cible = sortie / "labels" / split / f"{img.stem}.txt"
            if label.exists():
                shutil.copy2(label, cible)
            else:
                cible.write_text("")  # image sans objet : exemple négatif
    (sortie / "repartition_sequences.json").write_text(json.dumps(affectation, indent=1, ensure_ascii=False),
                                                         encoding="utf-8")
    (sortie / "data.yaml").write_text(
        "# chemins relatifs au dossier de ce fichier\ntrain: images/train\nval: images/val\ntest: images/test\n"
        "names:\n  0: personne\n  1: vehicule\n  2: debris\n", encoding="utf-8")
    return compte, affectation


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--source", required=True)
    parser.add_argument("--sortie", required=True)
    parser.add_argument("--val", type=float, default=0.15)
    parser.add_argument("--test", type=float, default=0.15)
    parser.add_argument("--test-impose", nargs="*", default=[])
    parser.add_argument("--sequences-csv", help="CSV avec colonnes image,sequence (sinon déduit du nom)")
    parser.add_argument("--graine", type=int, default=0)
    args = parser.parse_args()
    correspondance = None
    if args.sequences_csv:
        with open(args.sequences_csv, encoding="utf-8") as f:
            correspondance = {r["image"]: r["sequence"] for r in csv.DictReader(f)}
    compte, affectation = repartir(args.source, args.sortie, args.val, args.test, args.test_impose, args.graine,
                                   correspondance)
    print(f"Images : {compte}")
    print(f"Séquences : { {s: sum(1 for v in affectation.values() if v == s) for s in ('train', 'val', 'test')} }")


if __name__ == "__main__":
    main()
