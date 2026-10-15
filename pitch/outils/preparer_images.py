"""Recadre les captures SolidWorks du drone (pitch/assets/cao/sources) pour les présentations.

Usage : python3 pitch/outils/preparer_images.py   -> pitch/assets/cao/cao_*.png
"""

from pathlib import Path

import numpy as np
from PIL import Image

DOSSIER = Path(__file__).resolve().parents[1] / "assets" / "cao"
SOURCES = DOSSIER / "sources"


def serre(im, marge):
    """Recadre au plus près du drone (pixels plus sombres que le fond), avec une marge."""
    a = np.asarray(im.convert("L")).astype(int)
    ys, xs = np.where(a < 205)
    w, h = im.size
    return im.crop((max(0, xs.min() - marge), max(0, ys.min() - marge), min(w, xs.max() + marge), min(h, ys.max() + marge)))


def main():
    vues = Image.open(SOURCES / "vues_multiples.png").convert("RGB")
    sorties = {
        "cao_iso": serre(vues.crop((840, 470, 1586, 858)), 40),  # vue isométrique (quart bas droit)
        "cao_dessus": serre(Image.open(SOURCES / "dessus.png").convert("RGB"), 35),
        "cao_profil": serre(Image.open(SOURCES / "profil_gauche.png").convert("RGB"), 35),
        "cao_face": serre(Image.open(SOURCES / "face.png").convert("RGB"), 35),
    }
    for nom, im in sorties.items():
        im.save(DOSSIER / f"{nom}.png")
        print(nom, im.size)


if __name__ == "__main__":
    main()
