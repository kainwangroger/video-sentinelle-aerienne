"""Outils de dessin : palette, polices, animation, formes et pictogrammes.

Tout est dessiné avec Pillow sur une image RGB via ImageDraw en mode « RGBA »,
ce qui mélange chaque forme avec le fond selon sa transparence.
"""

import math
from functools import lru_cache
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 1920, 1080

# Palette bleu nuit / cyan
FOND_HAUT = (9, 20, 42)
FOND_BAS = (2, 7, 18)
CYAN = (0, 212, 255)
CYAN_SOMBRE = (0, 120, 165)
BLANC = (232, 241, 250)
GRIS = (138, 160, 188)
PANNEAU = (13, 31, 58)
AMBRE = (255, 186, 40)
ROUGE = (255, 95, 95)
VERT = (60, 220, 150)
ASPHALTE = (36, 46, 62)

_DOSSIERS_POLICES = [Path("/usr/share/fonts/opentype/inter"), Path("/usr/share/fonts/truetype/dejavu")]
_POLICES = {
    "titre": ["InterDisplay-Bold.otf", "DejaVuSans-Bold.ttf"],
    "gras": ["Inter-Bold.otf", "DejaVuSans-Bold.ttf"],
    "demi": ["Inter-SemiBold.otf", "DejaVuSans-Bold.ttf"],
    "normal": ["Inter-Regular.otf", "DejaVuSans.ttf"],
    "moyen": ["Inter-Medium.otf", "DejaVuSans.ttf"],
    "symbole": ["DejaVuSans-Bold.ttf"],
}


@lru_cache(maxsize=None)
def police(style, taille):
    for nom in _POLICES[style]:
        for dossier in _DOSSIERS_POLICES:
            chemin = dossier / nom
            if chemin.exists():
                return ImageFont.truetype(str(chemin), taille)
    return ImageFont.load_default(taille)


# ---------------------------------------------------------------- animation

def borne(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def sortie_cubique(x):
    x = borne(x)
    return 1 - (1 - x) ** 3


def apparition(t, debut, duree=0.5):
    """0 avant `debut`, puis montée douce jusqu'à 1 en `duree` secondes."""
    return sortie_cubique((t - debut) / duree)


def avec_alpha(couleur, alpha):
    return (*couleur[:3], int(255 * borne(alpha)))


def melange(c1, c2, k):
    return tuple(int(a + (b - a) * k) for a, b in zip(c1, c2))


# ---------------------------------------------------------------- fond

def fond():
    """Dégradé bleu nuit, grille fine et vignettage (calculé une seule fois)."""
    y = np.linspace(0, 1, H)[:, None, None]
    img = np.array(FOND_HAUT, float) * (1 - y) + np.array(FOND_BAS, float) * y
    img = np.repeat(img, W, axis=1)
    pas = 60
    img[::pas, :, :] += np.array([0, 18, 28]) * 0.55
    img[:, ::pas, :] += np.array([0, 18, 28]) * 0.55
    yy, xx = np.mgrid[0:H, 0:W]
    d = np.sqrt(((xx - W / 2) / (W * 0.62)) ** 2 + ((yy - H / 2) / (H * 0.62)) ** 2)
    img *= (1 - 0.45 * np.clip(d - 0.35, 0, 1))[:, :, None]
    return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8), "RGB")


# ---------------------------------------------------------------- texte

def texte(d, xy, s, style="normal", taille=32, couleur=BLANC, alpha=1.0, ancre="la"):
    if alpha <= 0.003:
        return
    d.text(xy, s, font=police(style, taille), fill=avec_alpha(couleur, alpha), anchor=ancre)


def largeur(s, style, taille):
    return police(style, taille).getlength(s)


def couper(s, style, taille, largeur_max):
    lignes = []
    for paragraphe in s.split("\n"):
        mots, ligne = paragraphe.split(" "), ""
        for mot in mots:
            essai = (ligne + " " + mot).strip()
            if largeur(essai, style, taille) <= largeur_max or not ligne:
                ligne = essai
            else:
                lignes.append(ligne)
                ligne = mot
        lignes.append(ligne)
    return lignes


def paragraphe(d, xy, s, style="normal", taille=30, couleur=BLANC, alpha=1.0,
               largeur_max=600, interligne=1.3, ancre="la"):
    """Texte sur plusieurs lignes ; ancre « ma » pour centrer. Renvoie la hauteur."""
    x, y = xy
    lignes = couper(s, style, taille, largeur_max)
    for i, ligne in enumerate(lignes):
        texte(d, (x, y + i * taille * interligne), ligne, style, taille, couleur, alpha, ancre)
    return len(lignes) * taille * interligne


# ---------------------------------------------------------------- formes

def panneau(d, boite, alpha=1.0, bord=CYAN_SOMBRE, fond_couleur=PANNEAU, rayon=18, epaisseur=2,
            opacite_fond=0.85):
    if alpha <= 0.003:
        return
    d.rounded_rectangle(boite, rayon, fill=avec_alpha(fond_couleur, opacite_fond * alpha),
                        outline=avec_alpha(bord, alpha), width=epaisseur)


def fleche(d, p0, p1, couleur=CYAN, alpha=1.0, epaisseur=4, pointe=16):
    if alpha <= 0.003:
        return
    x0, y0 = p0
    x1, y1 = p1
    ang = math.atan2(y1 - y0, x1 - x0)
    bx, by = x1 - pointe * math.cos(ang), y1 - pointe * math.sin(ang)
    d.line([(x0, y0), (bx, by)], fill=avec_alpha(couleur, alpha), width=epaisseur)
    gauche = (bx + pointe * 0.6 * math.cos(ang + math.pi / 2), by + pointe * 0.6 * math.sin(ang + math.pi / 2))
    droite = (bx + pointe * 0.6 * math.cos(ang - math.pi / 2), by + pointe * 0.6 * math.sin(ang - math.pi / 2))
    d.polygon([(x1, y1), gauche, droite], fill=avec_alpha(couleur, alpha))


def ligne_pointillee(d, p0, p1, couleur=GRIS, alpha=1.0, epaisseur=3, tiret=14, espace=10, decalage=0.0):
    x0, y0 = p0
    x1, y1 = p1
    longueur = math.hypot(x1 - x0, y1 - y0)
    if longueur == 0:
        return
    ux, uy = (x1 - x0) / longueur, (y1 - y0) / longueur
    s = -(decalage % (tiret + espace))
    while s < longueur:
        a, b = max(0, s), min(longueur, s + tiret)
        if b > a:
            d.line([(x0 + ux * a, y0 + uy * a), (x0 + ux * b, y0 + uy * b)],
                   fill=avec_alpha(couleur, alpha), width=epaisseur)
        s += tiret + espace


def rectangle_pointille(d, boite, couleur=GRIS, alpha=1.0, epaisseur=3, decalage=0.0):
    x0, y0, x1, y1 = boite
    for p, q in [((x0, y0), (x1, y0)), ((x1, y0), (x1, y1)), ((x1, y1), (x0, y1)), ((x0, y1), (x0, y0))]:
        ligne_pointillee(d, p, q, couleur, alpha, epaisseur, 12, 8, decalage)


def cercle(d, c, r, couleur=CYAN, alpha=1.0, epaisseur=3, plein=False):
    if alpha <= 0.003 or r <= 0:
        return
    boite = (c[0] - r, c[1] - r, c[0] + r, c[1] + r)
    if plein:
        d.ellipse(boite, fill=avec_alpha(couleur, alpha))
    else:
        d.ellipse(boite, outline=avec_alpha(couleur, alpha), width=epaisseur)


def puce_numero(d, c, n, alpha=1.0, couleur=CYAN, r=26, actif=True):
    cercle(d, c, r, couleur if actif else GRIS, alpha * (1 if actif else 0.6), 3)
    if actif:
        cercle(d, c, r - 6, couleur, alpha * 0.25, plein=True)
    texte(d, c, str(n), "gras", int(r * 1.05), BLANC if actif else GRIS, alpha, "mm")


def coche(d, c, taille=30, couleur=VERT, alpha=1.0):
    x, y = c
    s = taille
    d.line([(x - s * 0.5, y), (x - s * 0.12, y + s * 0.4), (x + s * 0.55, y - s * 0.45)],
           fill=avec_alpha(couleur, alpha), width=max(3, int(s * 0.16)), joint="curve")


def croix(d, c, taille=30, couleur=ROUGE, alpha=1.0):
    x, y = c
    s = taille * 0.45
    e = max(3, int(taille * 0.16))
    d.line([(x - s, y - s), (x + s, y + s)], fill=avec_alpha(couleur, alpha), width=e)
    d.line([(x - s, y + s), (x + s, y - s)], fill=avec_alpha(couleur, alpha), width=e)


# ---------------------------------------------------------------- pictogrammes

def drone(d, c, s=1.0, couleur=CYAN, alpha=1.0, t=0.0):
    """Quadricoptère vu de dessus ; les hélices tournent avec t."""
    x, y = c
    bras = 70 * s
    for k in range(4):
        a = math.pi / 4 + k * math.pi / 2
        px, py = x + bras * math.cos(a), y + bras * math.sin(a)
        d.line([(x, y), (px, py)], fill=avec_alpha(couleur, alpha), width=max(2, int(7 * s)))
        cercle(d, (px, py), 34 * s, couleur, alpha * 0.9, max(2, int(3 * s)))
        rot = t * 18 + k
        for h in range(2):
            b = rot + h * math.pi
            d.line([(px - 28 * s * math.cos(b), py - 28 * s * math.sin(b)),
                    (px + 28 * s * math.cos(b), py + 28 * s * math.sin(b))],
                   fill=avec_alpha(BLANC, alpha * 0.55), width=max(2, int(3 * s)))
    d.rounded_rectangle((x - 30 * s, y - 30 * s, x + 30 * s, y + 30 * s), int(10 * s),
                        fill=avec_alpha(PANNEAU, alpha), outline=avec_alpha(couleur, alpha), width=max(2, int(4 * s)))
    cercle(d, (x, y), 9 * s, couleur, alpha, plein=True)


def personne(d, c, s=1.0, couleur=BLANC, alpha=1.0):
    x, y = c
    cercle(d, (x, y - 30 * s), 11 * s, couleur, alpha, plein=True)
    d.rounded_rectangle((x - 13 * s, y - 16 * s, x + 13 * s, y + 18 * s), int(6 * s), fill=avec_alpha(couleur, alpha))
    d.line([(x - 6 * s, y + 16 * s), (x - 8 * s, y + 40 * s)], fill=avec_alpha(couleur, alpha), width=max(2, int(8 * s)))
    d.line([(x + 6 * s, y + 16 * s), (x + 8 * s, y + 40 * s)], fill=avec_alpha(couleur, alpha), width=max(2, int(8 * s)))


def vehicule(d, c, s=1.0, couleur=BLANC, alpha=1.0):
    x, y = c
    d.rounded_rectangle((x - 46 * s, y - 8 * s, x + 46 * s, y + 18 * s), int(7 * s), fill=avec_alpha(couleur, alpha))
    d.polygon([(x - 26 * s, y - 8 * s), (x - 16 * s, y - 28 * s), (x + 18 * s, y - 28 * s), (x + 30 * s, y - 8 * s)],
              fill=avec_alpha(couleur, alpha))
    for dx in (-26, 26):
        cercle(d, (x + dx * s, y + 20 * s), 10 * s, ASPHALTE, alpha, plein=True)
        cercle(d, (x + dx * s, y + 20 * s), 10 * s, couleur, alpha, max(2, int(3 * s)))


def debris(d, c, s=1.0, couleur=BLANC, alpha=1.0):
    x, y = c
    pts = [(-20, -6), (-6, -18), (14, -12), (22, 4), (8, 16), (-14, 12)]
    d.polygon([(x + px * s, y + py * s) for px, py in pts], fill=avec_alpha(couleur, alpha))
    d.line([(x + 26 * s, y + 10 * s), (x + 38 * s, y + 4 * s)], fill=avec_alpha(couleur, alpha), width=max(2, int(5 * s)))


def camera(d, c, s=1.0, couleur=CYAN, alpha=1.0):
    x, y = c
    d.rounded_rectangle((x - 40 * s, y - 26 * s, x + 30 * s, y + 26 * s), int(8 * s),
                        outline=avec_alpha(couleur, alpha), width=max(2, int(4 * s)))
    d.polygon([(x + 30 * s, y - 10 * s), (x + 50 * s, y - 22 * s), (x + 50 * s, y + 22 * s), (x + 30 * s, y + 10 * s)],
              outline=avec_alpha(couleur, alpha), width=max(2, int(4 * s)))
    cercle(d, (x - 5 * s, y), 13 * s, couleur, alpha, max(2, int(4 * s)))


def puce_electronique(d, c, s=1.0, couleur=CYAN, alpha=1.0):
    x, y = c
    for k in range(-2, 3):
        for (ax, ay, bx, by) in [(k * 12, -40, k * 12, -30), (k * 12, 30, k * 12, 40),
                                 (-40, k * 12, -30, k * 12), (30, k * 12, 40, k * 12)]:
            d.line([(x + ax * s, y + ay * s), (x + bx * s, y + by * s)], fill=avec_alpha(couleur, alpha),
                   width=max(2, int(4 * s)))
    d.rounded_rectangle((x - 30 * s, y - 30 * s, x + 30 * s, y + 30 * s), int(6 * s),
                        fill=avec_alpha(PANNEAU, alpha), outline=avec_alpha(couleur, alpha), width=max(2, int(4 * s)))
    d.rectangle((x - 12 * s, y - 12 * s, x + 12 * s, y + 12 * s), fill=avec_alpha(couleur, alpha * 0.8))


def nuage(d, c, s=1.0, couleur=GRIS, alpha=1.0):
    x, y = c
    for dx, dy, r in [(-28, 6, 22), (0, -8, 30), (30, 6, 22)]:
        cercle(d, (x + dx * s, y + dy * s), r * s, couleur, alpha, max(2, int(4 * s)))
    d.rectangle((x - 30 * s, y + 6 * s, x + 30 * s, y + 28 * s), fill=avec_alpha(PANNEAU, alpha))
    d.line([(x - 50 * s, y + 28 * s), (x + 52 * s, y + 28 * s)], fill=avec_alpha(couleur, alpha), width=max(2, int(4 * s)))


def antenne(d, c, s=1.0, couleur=CYAN, alpha=1.0):
    x, y = c
    d.line([(x, y - 10 * s), (x - 24 * s, y + 40 * s)], fill=avec_alpha(couleur, alpha), width=max(2, int(4 * s)))
    d.line([(x, y - 10 * s), (x + 24 * s, y + 40 * s)], fill=avec_alpha(couleur, alpha), width=max(2, int(4 * s)))
    cercle(d, (x, y - 14 * s), 7 * s, couleur, alpha, plein=True)
    for r in (22, 36):
        d.arc((x - r * s, y - 14 * s - r * s, x + r * s, y - 14 * s + r * s), 210, 330,
              fill=avec_alpha(couleur, alpha), width=max(2, int(3 * s)))


def epingle(d, c, s=1.0, couleur=AMBRE, alpha=1.0):
    x, y = c
    cercle(d, (x, y - 30 * s), 20 * s, couleur, alpha, max(2, int(4 * s)))
    d.line([(x - 15 * s, y - 18 * s), (x, y + 6 * s), (x + 15 * s, y - 18 * s)],
           fill=avec_alpha(couleur, alpha), width=max(2, int(4 * s)))
    cercle(d, (x, y - 30 * s), 6 * s, couleur, alpha, plein=True)


def stockage(d, c, s=1.0, couleur=CYAN, alpha=1.0):
    x, y = c
    for k in range(3):
        oy = (k - 1) * 22 * s
        d.ellipse((x - 36 * s, y + oy - 10 * s, x + 36 * s, y + oy + 10 * s),
                  fill=avec_alpha(PANNEAU, alpha), outline=avec_alpha(couleur, alpha), width=max(2, int(3 * s)))


def piste_perspective(d, boite, alpha=1.0, decalage=0.0):
    """Piste vue en perspective dans la boîte (x0, y0, x1, y1)."""
    x0, y0, x1, y1 = boite
    cx = (x0 + x1) / 2
    haut = (x1 - x0) * 0.16
    poly = [(cx - haut, y0), (cx + haut, y0), (x1, y1), (x0, y1)]
    d.polygon(poly, fill=avec_alpha(ASPHALTE, alpha))
    d.line([poly[0], poly[3]], fill=avec_alpha(BLANC, alpha * 0.8), width=4)
    d.line([poly[1], poly[2]], fill=avec_alpha(BLANC, alpha * 0.8), width=4)
    # ligne axiale pointillée, défilant vers le spectateur
    n = 12
    for k in range(n):
        u0 = ((k + decalage) % n) / n
        u1 = u0 + 0.035
        if u1 > 1:
            continue
        ya, yb = y0 + (y1 - y0) * u0 ** 1.6, y0 + (y1 - y0) * u1 ** 1.6
        d.line([(cx, ya), (cx, yb)], fill=avec_alpha(BLANC, alpha * 0.7), width=max(2, int(2 + 6 * u0)))
    # seuil
    for k in range(-5, 6):
        if k == 0:
            continue
        xa = cx + k * (x1 - x0) * 0.075
        d.line([(xa, y1 - 50), (xa, y1 - 8)], fill=avec_alpha(BLANC, alpha * 0.6), width=9)
    return poly


def point_sur_piste(boite, u, v):
    """Coordonnées écran d'un point (u : -1..1 en largeur, v : 0..1 en profondeur)."""
    x0, y0, x1, y1 = boite
    cx = (x0 + x1) / 2
    demi_haut = (x1 - x0) * 0.16
    demi = demi_haut + ((x1 - x0) / 2 - demi_haut) * v
    return cx + u * demi, y0 + (y1 - y0) * v, 0.45 + 0.75 * v
