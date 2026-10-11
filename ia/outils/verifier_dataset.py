"""Contrôle d'un jeu YOLO avant entraînement.

Vérifie :
- format des fichiers d'annotation, indices de classe, boîtes dans l'image et non vides ;
- images sans annotation (négatifs) et annotations sans image ;
- doublons exacts (erreur s'ils sont dans deux ensembles) et quasi-doublons
  (empreinte perceptuelle, signalés pour contrôle visuel) ;
- fuite entre ensembles : une même séquence présente dans plusieurs ensembles ;
- statistiques par classe et taille des objets en pixels (repérer les débris trop petits).

Code de retour 1 si une erreur bloquante est trouvée.

Usage : python outils/verifier_dataset.py --data travail/jeu_projet [--imgsz 640]
"""

import argparse
import hashlib
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
from PIL import Image

NOMS = ["personne", "vehicule", "debris"]
EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp"}


def empreinte(chemin, taille=16):
    """Empreinte de différence (dHash) 256 bits : repère les quasi-doublons."""
    img = Image.open(chemin).convert("L").resize((taille + 1, taille), Image.BILINEAR)
    a = np.asarray(img, dtype=np.float32)
    return np.packbits((a[:, 1:] > a[:, :-1]).flatten()).tobytes()


def sequence_de(nom):
    stem = Path(nom).stem
    return stem.rsplit("_", 1)[0] if "_" in stem else stem


def verifier(dossier, imgsz=640, petit_px=16):
    dossier = Path(dossier)
    erreurs, avertissements = [], []
    compte = defaultdict(Counter)
    tailles = defaultdict(list)
    empreintes = defaultdict(list)
    identiques = defaultdict(list)
    sequences = defaultdict(set)
    negatifs = Counter()
    splits = [s for s in ("train", "val", "test") if (dossier / "images" / s).exists()]
    if not splits:
        return [f"Aucun dossier images/train|val|test dans {dossier}"], [], {}
    for split in splits:
        images = [p for p in sorted((dossier / "images" / split).glob("*")) if p.suffix.lower() in EXTENSIONS]
        noms_images = {p.stem for p in images}
        for label in (dossier / "labels" / split).glob("*.txt"):
            if label.stem not in noms_images:
                avertissements.append(f"{split}: annotation sans image {label.name}")
        for p in images:
            sequences[sequence_de(p.name)].add(split)
            empreintes[empreinte(p)].append((split, p.name))
            identiques[hashlib.md5(p.read_bytes()).hexdigest()].append((split, p.name))
            with Image.open(p) as im:
                w, h = im.size
            echelle = imgsz / max(w, h)
            label = dossier / "labels" / split / f"{p.stem}.txt"
            if not label.exists() or not label.read_text().strip():
                negatifs[split] += 1
                continue
            for n, ligne in enumerate(label.read_text().splitlines(), 1):
                if not ligne.strip():
                    continue
                champs = ligne.split()
                if len(champs) != 5:
                    erreurs.append(f"{split}/{label.name}:{n} : 5 valeurs attendues")
                    continue
                c, x, y, bw, bh = int(float(champs[0])), *map(float, champs[1:])
                if c not in range(len(NOMS)):
                    erreurs.append(f"{split}/{label.name}:{n} : classe {c} hors de 0..{len(NOMS) - 1}")
                    continue
                if bw <= 0 or bh <= 0:
                    erreurs.append(f"{split}/{label.name}:{n} : boîte vide")
                    continue
                if not (0 <= x - bw / 2 + 1e-3 and x + bw / 2 <= 1 + 1e-3 and 0 <= y - bh / 2 + 1e-3 and y + bh / 2 <= 1 + 1e-3):
                    erreurs.append(f"{split}/{label.name}:{n} : boîte hors de l'image")
                compte[split][NOMS[c]] += 1
                tailles[NOMS[c]].append(min(bw * w, bh * h) * echelle)
    for occurrences in identiques.values():
        if len(occurrences) > 1:
            message = ", ".join(f"{s}/{n}" for s, n in occurrences[:4])
            if len({s for s, _ in occurrences}) > 1:
                erreurs.append(f"Image identique dans plusieurs ensembles : {message}")
            else:
                avertissements.append(f"Doublon exact : {message}")
    for occurrences in empreintes.values():
        if len(occurrences) > 1 and len({s for s, _ in occurrences}) > 1:
            message = ", ".join(f"{s}/{n}" for s, n in occurrences[:4])
            avertissements.append(f"Quasi-doublon entre ensembles (à contrôler) : {message}")
    for seq, ensembles in sequences.items():
        if len(ensembles) > 1:
            erreurs.append(f"Séquence {seq} présente dans {sorted(ensembles)} : séparer par séquence")
    stats = {
        "objets": {s: dict(c) for s, c in compte.items()},
        "negatifs": dict(negatifs),
        "taille_min_px_a_l_entree": {c: {"mediane": round(float(np.median(v)), 1),
                                          f"part_sous_{petit_px}px": round(float(np.mean(np.array(v) < petit_px)), 3)}
                                      for c, v in tailles.items() if v},
    }
    for c, v in stats["taille_min_px_a_l_entree"].items():
        if v[f"part_sous_{petit_px}px"] > 0.3:
            avertissements.append(f"{c} : {v[f'part_sous_{petit_px}px']:.0%} des objets font moins de {petit_px} px à "
                                  f"l'entrée {imgsz} -> envisager entrée plus grande ou tuiles")
    return erreurs, avertissements, stats


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--data", required=True)
    parser.add_argument("--imgsz", type=int, default=640)
    args = parser.parse_args()
    erreurs, avertissements, stats = verifier(args.data, args.imgsz)
    print("Statistiques :", stats)
    for a in avertissements[:50]:
        print("AVERTISSEMENT", a)
    for e in erreurs[:100]:
        print("ERREUR", e)
    print(f"{len(erreurs)} erreur(s), {len(avertissements)} avertissement(s)")
    sys.exit(1 if erreurs else 0)


if __name__ == "__main__":
    main()
