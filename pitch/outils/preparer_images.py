"""Prépare les images du pitch (pitch/assets) à partir des schémas et de la maquette 3D du SA-1.

Usage : python3 pitch/outils/preparer_images.py
"""

import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

RACINE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RACINE / "video"))

from assemblage.modele_sa1 import catalogue  # noqa: E402
from assemblage.moteur3d import Camera, Maillage, Objet, rendre  # noqa: E402
from gfx import fond  # noqa: E402

SCHEMAS = RACINE / "drone" / "schemas"
SORTIE = RACINE / "pitch" / "assets"

# Zones utiles des schémas (sans leur titre incrusté).
RECADRAGES = {
    "transition": (400, 200, 1880, 840),
    "simulation_detection": (80, 210, 1840, 920),
    "chaine_ia_bande": ("chaine_ia", (0, 380, 1920, 720)),
}


def vue_3d(nom, camera, eclatement=0.0):
    """Rendu 3D sur fond transparent, rogné au plus près."""
    camera.centre_ecran = (1600, 1100)
    img = Image.new("RGBA", (3200, 2200), (0, 0, 0, 0))
    d = ImageDraw.Draw(img, "RGBA")
    objets = []
    for n, (m, decal) in catalogue().items():
        s = m.sommets + np.asarray(decal, float) * eclatement
        objets.append(Objet(Maillage(s, m.faces, m.couleur), nom=n))
    rendre(d, camera, objets, sol=False)
    img.crop(img.getbbox()).save(SORTIE / f"{nom}.png")
    print(nom)


def main():
    SORTIE.mkdir(parents=True, exist_ok=True)
    fond().convert("RGB").save(SORTIE / "fond.png")
    for nom, spec in RECADRAGES.items():
        src, boite = spec if isinstance(spec[0], str) else (nom, spec)
        Image.open(SCHEMAS / f"{src}.png").convert("RGB").crop(boite).save(SORTIE / f"{nom}.png")
        print(nom)
    vue_3d("3d_sa1_assemble", Camera(0.8, 0.45, 3.0, (-0.12, 0, 0), focale=2800))
    vue_3d("3d_vue_eclatee", Camera(0.9, 0.5, 3.6, (-0.12, 0, 0.1), focale=2600), eclatement=1.0)


if __name__ == "__main__":
    main()
