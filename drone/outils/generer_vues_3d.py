"""Vues 3D du SA-1 pour le guide d'assemblage (même maquette que la vidéo).

Usage : python3 drone/outils/generer_vues_3d.py   -> drone/schemas/3d_*.png
"""

import sys
from pathlib import Path

import numpy as np

RACINE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RACINE / "video"))

from PIL import ImageDraw  # noqa: E402

from assemblage.modele_sa1 import GROUPES, catalogue  # noqa: E402
from assemblage.moteur3d import Camera, Maillage, Objet, rendre  # noqa: E402
from gfx import BLANC, CYAN, avec_alpha, fond, texte  # noqa: E402

SORTIE = RACINE / "drone" / "schemas"


def titre(d, t):
    d.rectangle((80, 120, 88, 186), fill=avec_alpha(CYAN, 1))
    texte(d, (110, 153), t, "titre", 58, BLANC, 1, "lm")


def vue(nom, titre_vue, camera, eclatement=0.0, transparent=False, masquer=()):
    img = fond()
    d = ImageDraw.Draw(img, "RGBA")
    titre(d, titre_vue)
    objets = []
    for n, (m, decal) in catalogue().items():
        if n in masquer:
            continue
        s = m.sommets + np.asarray(decal, float) * eclatement
        filaire = transparent and n in ("fuselage", "trappe", "aile_centrale")
        objets.append(Objet(Maillage(s, m.faces, m.couleur), alpha=0.35 if filaire else 1, filaire=filaire, nom=n))
    rendre(d, camera, objets)
    img.save(SORTIE / nom)
    print(nom)


def main():
    SORTIE.mkdir(parents=True, exist_ok=True)
    vue("3d_sa1_assemble.png", "SA-1 assemblé", Camera(0.8, 0.45, 3.0, (-0.12, 0, 0)))
    vue("3d_vue_eclatee.png", "Vue éclatée du SA-1", Camera(0.9, 0.5, 3.6, (-0.12, 0, 0.1)), eclatement=1.0)
    ailes = ["longeron", "aile_gauche", "aile_droite", "aileron_gauche", "aileron_droit", "pitot", "servo_gauche", "servo_droit"]
    vue("3d_interieur_fuselage.png", "Intérieur du fuselage (demi-ailes retirées)", Camera(1.2, 0.75, 1.9, (-0.08, 0, 0)),
        transparent=True, masquer=ailes + [n for n in GROUPES["propulsion"] if n.startswith("helice")])


if __name__ == "__main__":
    main()
