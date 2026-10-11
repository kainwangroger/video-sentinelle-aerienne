"""Génère des données synthétiques de piste vue du ciel (tests, démonstration, essai de la chaîne).

ATTENTION : ces images dessinées ne remplacent pas les données réelles (FOD-A, images de
la caméra du projet). Elles servent uniquement à vérifier que les outils fonctionnent de
bout en bout : conversion, séparation par séquence, entraînement, export, pipeline.

Produit, dans le dossier de sortie :
- jeu_yolo/ : images/{train,val,test} + labels au format YOLO, séparés par séquence,
  avec des scènes négatives (ombres, flaques, marquages, sans objet) et data.yaml ;
- demo/piste_demo.mp4 : vidéo d'un survol avec objets posés au sol ;
- demo/piste_demo_annotations.json : vérité terrain par image (détecteur factice) ;
- demo/reference_piste_libre.jpg : image de référence de piste libre (branche anomalie).

Usage : python outils/generer_donnees_synthetiques.py --sortie donnees/echantillon_synthetique
"""

import argparse
import json
import math
import random
from pathlib import Path

import cv2
import numpy as np

CLASSES = ["personne", "vehicule", "debris"]


# ------------------------------------------------------------------ monde : grande piste vue de dessus

def creer_monde(largeur, hauteur, rng):
    """Grande image de terrain : herbe, piste, marquages, salissures."""
    monde = np.zeros((hauteur, largeur, 3), np.uint8)
    bruit = rng.normal(0, 1, (hauteur // 8, largeur // 8)).astype(np.float32)
    bruit = cv2.resize(cv2.GaussianBlur(bruit, (0, 0), 3), (largeur, hauteur))
    herbe = np.stack([60 + 12 * bruit, 105 + 20 * bruit, 75 + 12 * bruit], -1)
    monde[:] = np.clip(herbe, 0, 255).astype(np.uint8)
    x0, x1 = int(largeur * 0.3), int(largeur * 0.7)
    grain = rng.normal(0, 7, (hauteur, x1 - x0)).astype(np.float32)
    asphalte = 92 + cv2.GaussianBlur(grain, (0, 0), 1.2)
    monde[:, x0:x1] = np.clip(np.stack([asphalte, asphalte + 2, asphalte + 4], -1), 0, 255).astype(np.uint8)
    cx = (x0 + x1) // 2
    for y in range(0, hauteur, 160):
        cv2.rectangle(monde, (cx - 5, y), (cx + 5, y + 80), (225, 225, 225), -1)
    cv2.rectangle(monde, (x0 + 14, 0), (x0 + 22, hauteur), (220, 220, 220), -1)
    cv2.rectangle(monde, (x1 - 22, 0), (x1 - 14, hauteur), (220, 220, 220), -1)
    for _ in range(int(hauteur / 60)):  # salissures, traces de pneus
        y = rng.integers(0, hauteur)
        x = rng.integers(x0, x1)
        cv2.ellipse(monde, (int(x), int(y)), (int(rng.integers(10, 60)), int(rng.integers(3, 12))),
                    float(rng.uniform(0, 180)), 0, 360, (70, 72, 75), -1)
    return monde, (x0, x1)


def ajouter_negatifs(monde, piste, rng, n):
    """Éléments trompeurs : ombres, flaques, reflets. Non annotés : ils servent de négatifs."""
    h, w = monde.shape[:2]
    x0, x1 = piste
    for _ in range(n):
        x, y = int(rng.integers(x0, x1)), int(rng.integers(0, h))
        type_ = rng.integers(0, 3)
        calque = monde.copy()
        if type_ == 0:  # ombre
            cv2.ellipse(calque, (x, y), (int(rng.integers(20, 70)), int(rng.integers(8, 25))), float(rng.uniform(0, 180)),
                        0, 360, (40, 42, 45), -1)
            monde[:] = cv2.addWeighted(calque, 0.45, monde, 0.55, 0)
        elif type_ == 1:  # flaque
            cv2.ellipse(calque, (x, y), (int(rng.integers(15, 45)), int(rng.integers(10, 30))), float(rng.uniform(0, 180)),
                        0, 360, (120, 105, 95), -1)
            monde[:] = cv2.addWeighted(calque, 0.6, monde, 0.4, 0)
        else:  # reflet
            cv2.circle(calque, (x, y), int(rng.integers(4, 10)), (245, 245, 245), -1)
            monde[:] = cv2.addWeighted(calque, 0.7, monde, 0.3, 0)


def dessiner_objet(img, classe, cx, cy, echelle, rng):
    """Dessine un objet vu de dessus ; renvoie sa boîte (x1, y1, x2, y2)."""
    if classe == "personne":
        r = int(7 * echelle)
        couleur = tuple(int(c) for c in rng.choice([(40, 40, 160), (160, 60, 30), (30, 140, 200), (200, 200, 200)]))
        cv2.ellipse(img, (cx, cy), (int(r * 1.6), r), float(rng.uniform(0, 180)), 0, 360, couleur, -1)
        cv2.circle(img, (cx, cy), int(r * 0.65), (60, 80, 110), -1)
        cv2.ellipse(img, (cx + int(r * 1.2), cy + int(r * 1.2)), (int(r * 1.6), int(r * 0.6)), 35, 0, 360, (45, 48, 52), -1)
        return cx - int(r * 1.8), cy - int(r * 1.8), cx + int(r * 2.6), cy + int(r * 2.6)
    if classe == "vehicule":
        lw, lh = int(rng.uniform(14, 18) * echelle), int(rng.uniform(30, 40) * echelle)
        angle = float(rng.uniform(-30, 30))
        couleur = tuple(int(c) for c in rng.choice([(30, 200, 240), (240, 240, 240), (40, 40, 40), (50, 50, 200)]))
        rect = ((cx, cy), (lw, lh), angle)
        pts = cv2.boxPoints(rect).astype(np.int32)
        cv2.fillPoly(img, [pts + np.array([int(3 * echelle), int(4 * echelle)])], (45, 48, 52))
        cv2.fillPoly(img, [pts], couleur)
        vitre = cv2.boxPoints(((cx, cy - lh * 0.15), (lw * 0.7, lh * 0.25), angle)).astype(np.int32)
        cv2.fillPoly(img, [vitre], (70, 60, 50))
        x, y, w, h = cv2.boundingRect(pts)
        return x, y, x + w, y + h
    # débris : petit objet irrégulier (pièce métallique, bloc, outil)
    n = int(rng.integers(5, 8))
    r = rng.uniform(3, 7) * echelle
    pts = np.array([[cx + r * rng.uniform(0.6, 1.3) * math.cos(2 * math.pi * k / n),
                     cy + r * rng.uniform(0.6, 1.3) * math.sin(2 * math.pi * k / n)] for k in range(n)], np.int32)
    couleur = tuple(int(c) for c in rng.choice([(180, 180, 185), (60, 120, 200), (40, 40, 40), (200, 210, 220)]))
    cv2.fillPoly(img, [pts], couleur)
    x, y, w, h = cv2.boundingRect(pts)
    return x - 1, y - 1, x + w + 1, y + h + 1


def placer_objets(monde, piste, rng, n, echelle):
    h, w = monde.shape[:2]
    x0, x1 = piste
    objets = []
    for _ in range(n):
        classe = rng.choice(CLASSES, p=[0.25, 0.2, 0.55])
        if classe == "debris":
            cx, cy = int(rng.integers(x0 + 30, x1 - 30)), int(rng.integers(40, h - 40))
        else:
            cx, cy = int(rng.integers(x0 - 80, x1 + 80)), int(rng.integers(40, h - 40))
        boite = dessiner_objet(monde, classe, cx, cy, echelle, rng)
        objets.append({"classe": str(classe), "boite": [int(v) for v in boite]})
    return objets


def degrader(img, rng):
    """Variations d'éclairage, flou de mouvement léger, bruit capteur."""
    gain = rng.uniform(0.7, 1.25)
    sortie = np.clip(img.astype(np.float32) * gain + rng.uniform(-15, 15), 0, 255)
    if rng.random() < 0.3:
        k = int(rng.integers(3, 6))
        noyau = np.zeros((k, k), np.float32)
        noyau[k // 2] = 1.0 / k
        sortie = cv2.filter2D(sortie, -1, noyau)
    sortie += rng.normal(0, 3, sortie.shape)
    return np.clip(sortie, 0, 255).astype(np.uint8)


# ------------------------------------------------------------------ jeu YOLO séparé par séquence

def generer_jeu(sortie, n_sequences, images_par_sequence, taille, rng):
    repartition = {}
    sequences = [f"synth{s:03d}" for s in range(n_sequences)]
    rng.shuffle(sequences)
    n_test = max(1, n_sequences // 6)
    n_val = max(1, n_sequences // 6)
    for i, seq in enumerate(sequences):
        repartition[seq] = "test" if i < n_test else "val" if i < n_test + n_val else "train"
    stats = {"train": 0, "val": 0, "test": 0, "negatives": 0}
    for seq in sorted(sequences):
        split = repartition[seq]
        (sortie / "images" / split).mkdir(parents=True, exist_ok=True)
        (sortie / "labels" / split).mkdir(parents=True, exist_ok=True)
        echelle = rng.uniform(0.8, 1.6)  # simule l'altitude de la séquence
        monde, piste = creer_monde(taille * 2, taille * 4, rng)
        ajouter_negatifs(monde, piste, rng, 25)
        objets = placer_objets(monde, piste, rng, int(rng.integers(6, 14)), echelle)
        for k in range(images_par_sequence):
            negative = rng.random() < 0.15
            y0 = int(rng.integers(0, monde.shape[0] - taille))
            x0 = int(rng.integers(0, monde.shape[1] - taille))
            if negative:  # zone sans objet : on cherche une fenêtre vide
                for _ in range(30):
                    if not any(_dans(o["boite"], x0, y0, taille) for o in objets):
                        break
                    y0 = int(rng.integers(0, monde.shape[0] - taille))
            vue = degrader(monde[y0:y0 + taille, x0:x0 + taille], rng)
            lignes = []
            for o in objets:
                b = _recadrer(o["boite"], x0, y0, taille)
                if b:
                    x1, y1, x2, y2 = b
                    lignes.append(f"{CLASSES.index(o['classe'])} {(x1 + x2) / 2 / taille:.6f} {(y1 + y2) / 2 / taille:.6f} "
                                  f"{(x2 - x1) / taille:.6f} {(y2 - y1) / taille:.6f}")
            nom = f"{seq}_{k:04d}"
            cv2.imwrite(str(sortie / "images" / split / f"{nom}.jpg"), vue, [cv2.IMWRITE_JPEG_QUALITY, 85])
            (sortie / "labels" / split / f"{nom}.txt").write_text("\n".join(lignes) + ("\n" if lignes else ""))
            stats[split] += 1
            stats["negatives"] += 0 if lignes else 1
    (sortie / "data.yaml").write_text(
        "# Jeu SYNTHÉTIQUE : uniquement pour tester la chaîne, pas pour entraîner le modèle de mission.\n"
        "# chemins relatifs au dossier de ce fichier\ntrain: images/train\nval: images/val\ntest: images/test\n"
        "names:\n  0: personne\n  1: vehicule\n  2: debris\n", encoding="utf-8")
    (sortie / "repartition_sequences.json").write_text(json.dumps(repartition, indent=1), encoding="utf-8")
    return stats


def _dans(boite, x0, y0, taille):
    return boite[2] > x0 and boite[0] < x0 + taille and boite[3] > y0 and boite[1] < y0 + taille


def _recadrer(boite, x0, y0, taille, visible_min=0.6):
    x1, y1, x2, y2 = boite
    cx1, cy1 = max(x1 - x0, 0), max(y1 - y0, 0)
    cx2, cy2 = min(x2 - x0, taille), min(y2 - y0, taille)
    if cx2 <= cx1 or cy2 <= cy1:
        return None
    if (cx2 - cx1) * (cy2 - cy1) < visible_min * (x2 - x1) * (y2 - y1):
        return None
    return cx1, cy1, cx2, cy2


# ------------------------------------------------------------------ vidéo de démonstration

def generer_demo(sortie, rng, duree=24, fps=15, largeur=1280, hauteur=720):
    sortie.mkdir(parents=True, exist_ok=True)
    monde, piste = creer_monde(largeur + 400, hauteur * 5, rng)
    reference = monde.copy()
    ajouter_negatifs(monde, piste, rng, 40)
    objets = placer_objets(monde, piste, rng, 9, 2.0)
    n = duree * fps
    chemin = sortie / "piste_demo.mp4"
    ecrivain = cv2.VideoWriter(str(chemin), cv2.VideoWriter_fourcc(*"mp4v"), fps, (largeur, hauteur))
    annotations = {}
    course = monde.shape[0] - hauteur
    for i in range(n):
        y0 = int(course * (1 - i / (n - 1)))  # le drone remonte la piste
        x0 = int(200 + 60 * math.sin(i / fps * 0.7))
        vue = degrader(monde[y0:y0 + hauteur, x0:x0 + largeur], rng)
        ecrivain.write(vue)
        visibles = []
        for o in objets:
            x1, y1, x2, y2 = o["boite"]
            if x2 > x0 and x1 < x0 + largeur and y2 > y0 and y1 < y0 + hauteur:
                visibles.append({"classe": o["classe"], "boite": [x1 - x0, y1 - y0, x2 - x0, y2 - y0]})
        annotations[i] = visibles
    ecrivain.release()
    _reencoder_h264(chemin)
    (sortie / "piste_demo_annotations.json").write_text(json.dumps(annotations), encoding="utf-8")
    cv2.imwrite(str(sortie / "reference_piste_libre.jpg"), reference[course:course + hauteur, 200:200 + largeur],
                [cv2.IMWRITE_JPEG_QUALITY, 90])
    return chemin, n


def _reencoder_h264(chemin):
    """Réencode en H.264 (plus léger, lisible partout) si ffmpeg est disponible."""
    import shutil
    import subprocess

    if not shutil.which("ffmpeg"):
        return
    tmp = chemin.with_suffix(".h264.mp4")
    r = subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(chemin), "-c:v", "libx264", "-crf", "26",
                        "-pix_fmt", "yuv420p", str(tmp)])
    if r.returncode == 0:
        tmp.replace(chemin)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--sortie", default="donnees/echantillon_synthetique")
    parser.add_argument("--sequences", type=int, default=12)
    parser.add_argument("--images-par-sequence", type=int, default=10)
    parser.add_argument("--taille", type=int, default=640)
    parser.add_argument("--graine", type=int, default=2026)
    parser.add_argument("--sans-video", action="store_true")
    args = parser.parse_args()
    rng = np.random.default_rng(args.graine)
    random.seed(args.graine)
    sortie = Path(args.sortie)
    stats = generer_jeu(sortie / "jeu_yolo", args.sequences, args.images_par_sequence, args.taille, rng)
    print(f"Jeu YOLO synthétique : {stats}")
    if not args.sans_video:
        chemin, n = generer_demo(sortie / "demo", rng)
        print(f"Vidéo de démonstration : {chemin} ({n} images)")


if __name__ == "__main__":
    main()
