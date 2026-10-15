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
    # Zooms sur des parties du drone (coordonnées dans les captures sources).
    profil = Image.open(SOURCES / "profil_gauche.png").convert("RGB")
    dessus = Image.open(SOURCES / "dessus.png").convert("RGB")
    face = Image.open(SOURCES / "face.png").convert("RGB")
    sorties.update({
        "z_nacelle": profil.crop((150, 230, 400, 400)),         # moteur avant, servo de basculement, nez
        "z_mat_gnss": profil.crop((400, 225, 620, 365)),        # mât GNSS
        "z_queue": profil.crop((700, 200, 1150, 470)),          # empennage en V, moteur arrière
        "z_dessus_avant": dessus.crop((380, 90, 880, 320)),     # nacelles et moteurs avant
        "z_dessus_arriere": dessus.crop((420, 400, 820, 640)),  # moteur arrière et empennage en V
        "z_face_centre": face.crop((300, 200, 880, 380)),       # fuselage et moteurs, vue de face
    })
    for nom, im in sorties.items():
        im.save(DOSSIER / f"{nom}.png")
        print(nom, im.size)


if __name__ == "__main__":
    main()
