"""Petit moteur de rendu 3D (numpy + Pillow) pour les animations d'assemblage.

Maillages polygonaux, projection perspective, élimination des faces arrière,
éclairage de Lambert et tri du peintre. Style « CAO » : faces ombrées et arêtes fines.
Repère : x vers l'avant du drone, y vers la droite, z vers le haut (mètres).
"""

import math
from dataclasses import dataclass, field

import numpy as np

from gfx import W, H, avec_alpha


# ------------------------------------------------------------------ maillages

@dataclass
class Maillage:
    sommets: np.ndarray            # (N, 3)
    faces: list                    # listes d'indices, sens trigonométrique vu de l'extérieur
    couleur: tuple = (120, 160, 200)
    double_face: bool = True   # orientation des faces non garantie : on éclaire les deux côtés

    def transforme(self, matrice=None, translation=(0, 0, 0)):
        s = self.sommets if matrice is None else self.sommets @ np.asarray(matrice).T
        return Maillage(s + np.asarray(translation, float), self.faces, self.couleur, self.double_face)


def rotation(rx=0.0, ry=0.0, rz=0.0):
    cx, sx, cy, sy, cz, sz = math.cos(rx), math.sin(rx), math.cos(ry), math.sin(ry), math.cos(rz), math.sin(rz)
    mx = np.array([[1, 0, 0], [0, cx, -sx], [0, sx, cx]])
    my = np.array([[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]])
    mz = np.array([[cz, -sz, 0], [sz, cz, 0], [0, 0, 1]])
    return mz @ my @ mx


def boite(lx, ly, lz, couleur, centre=(0, 0, 0)):
    x, y, z = lx / 2, ly / 2, lz / 2
    s = np.array([[-x, -y, -z], [x, -y, -z], [x, y, -z], [-x, y, -z],
                  [-x, -y, z], [x, -y, z], [x, y, z], [-x, y, z]], float) + centre
    faces = [[0, 3, 2, 1], [4, 5, 6, 7], [0, 1, 5, 4], [2, 3, 7, 6], [1, 2, 6, 5], [0, 4, 7, 3]]
    return Maillage(s, faces, couleur)


def cylindre(rayon, longueur, couleur, axe="z", n=16, rayon2=None, centre=(0, 0, 0)):
    """Cylindre (ou tronc de cône si rayon2) centré, le long de l'axe donné."""
    rayon2 = rayon if rayon2 is None else rayon2
    s = []
    for k in range(n):
        a = 2 * math.pi * k / n
        s.append([rayon * math.cos(a), rayon * math.sin(a), -longueur / 2])
    for k in range(n):
        a = 2 * math.pi * k / n
        s.append([rayon2 * math.cos(a), rayon2 * math.sin(a), longueur / 2])
    s = np.array(s, float)
    faces = [[k, (k + 1) % n, n + (k + 1) % n, n + k] for k in range(n)]
    faces.append(list(range(n - 1, -1, -1)))
    faces.append(list(range(n, 2 * n)))
    if axe == "x":
        s = s[:, [2, 0, 1]]
    elif axe == "y":
        s = s[:, [1, 2, 0]]
    return Maillage(s + np.asarray(centre, float), faces, couleur)


def sphere(rayon, couleur, n=12, centre=(0, 0, 0), aplatissement=(1, 1, 1)):
    s, faces = [], []
    for i in range(n + 1):
        phi = math.pi * i / n
        for j in range(n):
            th = 2 * math.pi * j / n
            s.append([rayon * math.sin(phi) * math.cos(th) * aplatissement[0],
                      rayon * math.sin(phi) * math.sin(th) * aplatissement[1], rayon * math.cos(phi) * aplatissement[2]])
    for i in range(n):
        for j in range(n):
            a, b = i * n + j, i * n + (j + 1) % n
            faces.append([a, a + n, b + n, b][::-1])
    return Maillage(np.array(s) + np.asarray(centre, float), faces, couleur)


def profil_naca(n=14, epaisseur=0.12, cambrure=0.04):
    """Points (x le long de la corde de 0 à 1, z) du contour, extrados puis intrados."""
    haut, bas = [], []
    for k in range(n + 1):
        u = (1 - math.cos(math.pi * k / n)) / 2
        yc = cambrure / 0.16 * (0.8 * u - u * u) if u < 0.4 else cambrure / 0.36 * (0.2 + 0.8 * u - u * u)
        yt = 5 * epaisseur * (0.2969 * math.sqrt(u) - 0.126 * u - 0.3516 * u ** 2 + 0.2843 * u ** 3 - 0.1015 * u ** 4)
        haut.append((u, yc + yt))
        bas.append((u, yc - yt))
    return haut + bas[::-1][1:-1]


def surface_portante(y0, y1, corde, bord_attaque_x, z, couleur, epaisseur=0.12, cambrure=0.04, vertical=False):
    """Aile (ou empennage) extrudée de y0 à y1. vertical=True : dérive (extrusion selon z)."""
    contour = profil_naca(12, epaisseur, cambrure)
    n = len(contour)
    s = []
    for y in (y0, y1):
        for u, h in contour:
            if vertical:
                s.append([bord_attaque_x - u * corde, h * corde, y])
            else:
                s.append([bord_attaque_x - u * corde, y, z + h * corde])
    s = np.array(s, float)
    if vertical:
        s[:, 1] += z  # z sert ici de position latérale
    faces = [[k, (k + 1) % n, n + (k + 1) % n, n + k] for k in range(n)]
    faces.append(list(range(n)))
    faces.append(list(range(2 * n - 1, n - 1, -1)))
    m = Maillage(s, faces, couleur)
    m.double_face = True
    return m


def fuselage(longueur, largeur, hauteur, couleur, nez_x, n=12, sections=9):
    """Fuselage profilé : sections super-elliptiques le long de x, nez arrondi, queue effilée."""
    s = []
    xs = []
    for i in range(sections):
        u = i / (sections - 1)
        x = nez_x - u * longueur
        if u < 0.25:
            f = math.sin(u / 0.25 * math.pi / 2) ** 0.6
        elif u > 0.8:
            f = 0.45 + 0.55 * (1 - (u - 0.8) / 0.2)
        else:
            f = 1.0
        xs.append(x)
        for j in range(n):
            a = 2 * math.pi * j / n
            c, sn = math.cos(a), math.sin(a)
            s.append([x, largeur / 2 * f * math.copysign(abs(c) ** 0.6, c), hauteur / 2 * f * math.copysign(abs(sn) ** 0.6, sn)])
    s = np.array(s, float)
    faces = []
    for i in range(sections - 1):
        for j in range(n):
            a, b = i * n + j, i * n + (j + 1) % n
            faces.append([a, b, b + n, a + n])
    faces.append(list(range(n - 1, -1, -1)))
    faces.append(list(range((sections - 1) * n, sections * n)))
    return Maillage(s, faces, couleur)


def helice(rayon, couleur, axe="z", pales=2, largeur=0.022, angle=0.0, centre=(0, 0, 0)):
    s, faces = [], []
    for p in range(pales):
        a = angle + 2 * math.pi * p / pales
        ca, sa = math.cos(a), math.sin(a)
        base = len(s)
        for r, l in [(0.01, largeur * 0.6), (rayon * 0.35, largeur), (rayon, largeur * 0.4)]:
            for cote in (-1, 1):
                s.append([r * ca - cote * l / 2 * sa, r * sa + cote * l / 2 * ca, 0.0])
        faces += [[base, base + 2, base + 3, base + 1], [base + 2, base + 4, base + 5, base + 3]]
    s = np.array(s, float)
    if axe == "x":
        s = s[:, [2, 0, 1]]
    m = Maillage(s + np.asarray(centre, float), faces, couleur)
    m.double_face = True
    return m


# ------------------------------------------------------------------ caméra et rendu

@dataclass
class Camera:
    azimut: float = 0.8           # rad, autour de z
    elevation: float = 0.45       # rad
    distance: float = 3.2         # m
    cible: tuple = (0.0, 0.0, 0.0)
    focale: float = 1500.0        # px
    centre_ecran: tuple = (W / 2, H / 2 + 20)

    def repere(self):
        ce, se, ca, sa = math.cos(self.elevation), math.sin(self.elevation), math.cos(self.azimut), math.sin(self.azimut)
        oeil = np.array(self.cible) + self.distance * np.array([ce * ca, ce * sa, se])
        avant = np.array(self.cible) - oeil
        avant /= np.linalg.norm(avant)
        droite = np.cross(avant, [0, 0, 1])
        droite /= np.linalg.norm(droite)
        haut = np.cross(droite, avant)
        return oeil, avant, droite, haut

    def projeter(self, points):
        oeil, avant, droite, haut = self.repere()
        rel = np.asarray(points, float) - oeil
        prof = rel @ avant
        prof = np.maximum(prof, 0.05)
        x = self.centre_ecran[0] + self.focale * (rel @ droite) / prof
        y = self.centre_ecran[1] - self.focale * (rel @ haut) / prof
        return np.stack([x, y], -1), prof


LUMIERE = np.array([0.4, -0.5, 0.75])
LUMIERE = LUMIERE / np.linalg.norm(LUMIERE)


@dataclass
class Objet:
    maillage: Maillage
    alpha: float = 1.0
    surbrillance: float = 0.0     # 0..1 : teinte ambre
    filaire: bool = False
    aretes: bool = True
    nom: str = ""
    extra: dict = field(default_factory=dict)


def rendre(d, camera, objets, sol=True):
    """Dessine les objets sur l'ImageDraw (mode RGBA)."""
    if sol:
        _grille_sol(d, camera)
    polys = []
    oeil, _, _, _ = camera.repere()
    for obj in objets:
        if obj.alpha <= 0.01:
            continue
        m = obj.maillage
        p2, prof = camera.projeter(m.sommets)
        for f in m.faces:
            pts3 = m.sommets[f]
            normale = np.cross(pts3[1] - pts3[0], pts3[2] - pts3[0])
            nn = np.linalg.norm(normale)
            if nn < 1e-12:
                continue
            normale /= nn
            centre = pts3.mean(0)
            vers_oeil = oeil - centre
            visible = normale @ vers_oeil > 0
            if not visible:
                if not m.double_face:
                    continue
                normale = -normale
            lum = 0.35 + 0.65 * max(0.0, normale @ LUMIERE)
            polys.append((prof[f].mean(), p2[f], lum, obj))
    polys.sort(key=lambda p: -p[0])
    for _, pts, lum, obj in polys:
        base = np.array(obj.maillage.couleur, float)
        if obj.surbrillance > 0:
            base = base * (1 - obj.surbrillance) + np.array([255, 186, 40]) * obj.surbrillance
        couleur = tuple(int(min(255, c * lum)) for c in base)
        pts = [tuple(p) for p in pts]
        if obj.filaire:
            d.polygon(pts, outline=avec_alpha((0, 212, 255), obj.alpha * 0.8))
            continue
        d.polygon(pts, fill=avec_alpha(couleur, obj.alpha),
                  outline=avec_alpha((0, 60, 90), obj.alpha * 0.35) if obj.aretes else None)


def _grille_sol(d, camera, z=-0.25, pas=0.25, etendue=2.0):
    k = int(etendue / pas)
    for i in range(-k, k + 1):
        for a, b in [((i * pas, -etendue, z), (i * pas, etendue, z)), ((-etendue, i * pas, z), (etendue, i * pas, z))]:
            p, _ = camera.projeter([a, b])
            d.line([tuple(p[0]), tuple(p[1])], fill=(0, 140, 190, 40), width=1)
