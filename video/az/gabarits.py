"""Gabarits de scènes réutilisables : signature f(d, t, D, m, scene).

Les données viennent de scene["donnees"]. Les éléments apparaissent au début de la
phrase qui en parle (m = instants de début des phrases), ou régulièrement sinon.
"""

import math

from gfx import (AMBRE, BLANC, CYAN, CYAN_SOMBRE, GRIS, PANNEAU, ROUGE, VERT, W, apparition, avec_alpha, cercle,
                 coche, couper, croix, fleche, largeur, paragraphe, panneau, puce_numero, sortie_cubique, texte)

from .pictos import dessiner

HAUT = 250      # haut de la zone de contenu (sous le titre)
BAS = 900       # bas de la zone utile (au-dessus des sous-titres)

COULEURS = {"cyan": CYAN, "ambre": AMBRE, "vert": VERT, "rouge": ROUGE, "gris": GRIS, "blanc": BLANC}


def instants(m, D, n, apparitions=None, decalage=0.3):
    """Instant d'apparition de chacun des n éléments."""
    if apparitions:  # indice de phrase, ou (indice, retard en s)
        sortie = []
        for a in apparitions:
            i, retard = a if isinstance(a, (list, tuple)) else (a, 0.0)
            sortie.append(m[min(i, len(m) - 1)] + decalage + retard)
        return sortie
    if n <= len(m):
        return [m[k] + decalage for k in range(n)]
    debut, fin = m[0] + 0.5, max(m[0] + 1.0, D - 3.0)
    return [debut + (fin - debut) * k / max(1, n - 1) for k in range(n)]


def _glisse(a, distance=30):
    return (1 - a) * distance


def _couleur(nom, defaut=CYAN):
    return COULEURS.get(nom, defaut) if isinstance(nom, str) else (nom or defaut)


# ------------------------------------------------------------------ ouverture de chapitre

def ouverture(d, t, D, m, scene):
    don = scene["donnees"]
    a = apparition(t, 0.1, 0.8)
    texte(d, (140, 330 - _glisse(a, -30)), f"CHAPITRE {don['numero']:02d}", "gras", 40, CYAN, a, "lm")
    h = paragraphe(d, (140, 390), don["titre"], "titre", 92, BLANC, apparition(t, 0.4, 0.8), 1000, 1.05)
    y_sous = 390 + h + 55
    if don.get("sous_titre"):
        texte(d, (140, y_sous), don["sous_titre"], "moyen", 34, GRIS, apparition(t, 0.9, 0.8), "lm")
    points = don.get("sommaire", [])
    ts = instants(m, D, len(points), decalage=0.6)
    for k, (point, debut) in enumerate(zip(points, ts)):
        a2 = apparition(t, debut, 0.5)
        y = y_sous + 70 + k * 46
        cercle(d, (152, y), 7, CYAN, a2, plein=True)
        texte(d, (175, y), point, "moyen", 30, BLANC, a2, "lm")
    if don.get("picto"):
        a3 = apparition(t, 0.3, 1.0)
        for k in range(2):
            phase = (t * 0.35 + k / 2) % 1
            cercle(d, (1450, 520), 200 + phase * 160, CYAN, 0.25 * (1 - phase) * a3, 2)
        dessiner(d, don["picto"], (1450, 520), don.get("echelle", 1.6), a3, t)


# ------------------------------------------------------------------ puces

def puces(d, t, D, m, scene):
    don = scene["donnees"]
    points = don["points"]
    picto = don.get("picto")
    largeur_texte = 900 if picto else 1600
    ts = instants(m, D, len(points), don.get("apparitions"))
    hauteur_point = min(150, (BAS - HAUT - 20) // max(1, len(points)))
    for k, (point, debut) in enumerate(zip(points, ts)):
        titre, detail = point if isinstance(point, (list, tuple)) else (point, "")
        a = apparition(t, debut, 0.5)
        y = HAUT + 30 + k * hauteur_point
        couleur = _couleur(don.get("couleurs", {}).get(k), CYAN) if don.get("couleurs") else CYAN
        if don.get("numeros"):
            puce_numero(d, (170, y + 26), k + 1, a, couleur, 24)
        else:
            cercle(d, (170, y + 26), 9, couleur, a, plein=True)
        texte(d, (210 + _glisse(a, -20), y + 26), titre, "gras", 36, BLANC, a, "lm")
        if detail:
            paragraphe(d, (210, y + 52), detail, "normal", 28, GRIS, a, largeur_texte, 1.3)
    if picto:
        a = apparition(t, 0.2, 0.8)
        cx = 1440
        cercle(d, (cx, 560), 240, CYAN_SOMBRE, 0.35 * a, 2)
        dessiner(d, picto, (cx, 560), don.get("echelle", 1.4), a, t)
        if don.get("legende"):
            texte(d, (cx, 850), don["legende"], "demi", 28, CYAN, a, "mm")


# ------------------------------------------------------------------ fiche composant

BLOCS = [("role", "À quoi ça sert"), ("principe", "Comment ça marche"), ("choix", "Notre choix"),
         ("pourquoi", "Pourquoi")]


def composant(d, t, D, m, scene):
    don = scene["donnees"]
    a = apparition(t, 0.1, 0.8)
    panneau(d, (110, HAUT, 700, BAS), a, CYAN_SOMBRE)
    dessiner(d, don["picto"], (405, 470), don.get("echelle", 1.5), a, t)
    texte(d, (405, 690), don["nom"], "gras", 36, BLANC, a, "mm")
    for k, (cle, valeur) in enumerate(don.get("fiche", [])):
        a2 = apparition(t, 0.6 + k * 0.4, 0.5)
        y = 745 + k * 40
        texte(d, (150, y), cle, "normal", 24, GRIS, a2, "lm")
        texte(d, (660, y), valeur, "demi", 24, CYAN, a2, "rm")
    blocs = [(titre, don[cle]) for cle, titre in BLOCS if don.get(cle)]
    ts = instants(m, D, len(blocs), don.get("apparitions"))
    y = HAUT
    hauteur = (BAS - HAUT - 15 * (len(blocs) - 1)) / max(1, len(blocs))
    for k, ((titre, contenu), debut) in enumerate(zip(blocs, ts)):
        a3 = apparition(t, debut, 0.5)
        couleur = AMBRE if titre == "Notre choix" else CYAN
        panneau(d, (750 + _glisse(a3, -30), y, 1810, y + hauteur), a3, couleur if titre == "Notre choix" else CYAN_SOMBRE)
        texte(d, (785, y + 34), titre.upper(), "gras", 24, couleur, a3, "lm")
        paragraphe(d, (785, y + 58), contenu, "normal", 28, BLANC, a3, 990, 1.28)
        y += hauteur + 15


# ------------------------------------------------------------------ tableau

def tableau(d, t, D, m, scene):
    don = scene["donnees"]
    colonnes, lignes = don["colonnes"], don["lignes"]
    largeurs = don.get("largeurs") or [1680 // len(colonnes)] * len(colonnes)
    x0, y0 = 120, HAUT + 10
    h_ligne = min(86, (BAS - y0 - 60) // max(1, len(lignes)))
    a = apparition(t, 0.1, 0.6)
    d.rectangle((x0, y0, x0 + sum(largeurs), y0 + 56), fill=avec_alpha((12, 55, 90), a))
    x = x0
    for k, col in enumerate(colonnes):
        texte(d, (x + 20, y0 + 28), col, "gras", 26, CYAN, a, "lm")
        x += largeurs[k]
    ts = instants(m, D, len(lignes), don.get("apparitions"))
    for i, (ligne, debut) in enumerate(zip(lignes, ts)):
        a2 = apparition(t, debut, 0.4)
        y = y0 + 56 + i * h_ligne
        d.rectangle((x0, y, x0 + sum(largeurs), y + h_ligne - 4), fill=avec_alpha(PANNEAU, 0.75 * a2))
        x = x0
        for k, cellule in enumerate(ligne):
            style = "demi" if k == 0 else "normal"
            couleur = BLANC if k == 0 else (AMBRE if don.get("colonne_accent") == k else GRIS)
            lignes_txt = couper(str(cellule), style, 26, largeurs[k] - 36)[:2]
            for j, lt in enumerate(lignes_txt):
                texte(d, (x + 20, y + h_ligne / 2 - 2 + (j - (len(lignes_txt) - 1) / 2) * 30), lt, style, 26, couleur,
                      a2, "lm")
            x += largeurs[k]


# ------------------------------------------------------------------ formule

def formule(d, t, D, m, scene):
    don = scene["donnees"]
    ts = instants(m, D, 3, don.get("apparitions"))
    a = apparition(t, ts[0], 0.6)
    panneau(d, (220, HAUT + 10, 1700, HAUT + 200), a, CYAN, epaisseur=3)
    texte(d, (960, HAUT + 105), don["formule"], "titre", don.get("taille", 72), BLANC, a, "mm")
    termes = don.get("termes", [])
    a2 = apparition(t, ts[1], 0.6)
    for k, (symbole, sens) in enumerate(termes):
        col, lig = k % 2, k // 2
        x, y = 260 + col * 760, HAUT + 260 + lig * 62
        texte(d, (x, y), symbole, "gras", 32, CYAN, a2, "lm")
        texte(d, (x + max(110, largeur(symbole, "gras", 32) + 24), y), sens, "normal", 28, BLANC, a2, "lm")
    a3 = apparition(t, ts[2], 0.6)
    if don.get("exemple"):
        y = HAUT + 300 + ((len(termes) + 1) // 2) * 62
        panneau(d, (220, y, 1700, y + 120), a3, AMBRE)
        texte(d, (260, y + 36), "EXEMPLE SA-1", "gras", 22, AMBRE, a3, "lm")
        texte(d, (260, y + 80), don["exemple"], "demi", 32, BLANC, a3, "lm")


# ------------------------------------------------------------------ comparaison

def comparaison(d, t, D, m, scene):
    don = scene["donnees"]
    colonnes = don["colonnes"]
    n = len(colonnes)
    largeur_col = (1680 - 40 * (n - 1)) / n
    ts = instants(m, D, n, don.get("apparitions"))
    for k, (col, debut) in enumerate(zip(colonnes, ts)):
        a = apparition(t, debut, 0.6)
        x = 120 + k * (largeur_col + 40)
        statut = col.get("statut")
        couleur = VERT if statut == "ok" else ROUGE if statut == "ko" else CYAN_SOMBRE
        b = (x, HAUT + _glisse(a, 30), x + largeur_col, BAS - 10 + _glisse(a, 30))
        panneau(d, b, a, couleur, epaisseur=3 if statut == "ok" else 2)
        cx = x + largeur_col / 2
        if col.get("picto"):
            dessiner(d, col["picto"], (cx, b[1] + 150), col.get("echelle", 0.9), a, t)
        texte(d, (cx, b[1] + 300), col["titre"], "gras", 36, BLANC, a, "mm")
        y = b[1] + 350
        for point in col.get("points", []):
            hauteur = paragraphe(d, (cx, y), point, "normal", 26, GRIS, a, largeur_col - 60, 1.3, "ma")
            y += hauteur + 10
        if statut == "ok":
            coche(d, (x + largeur_col - 40, b[1] + 40), 36, VERT, a)
        elif statut == "ko":
            croix(d, (x + largeur_col - 40, b[1] + 40), 32, ROUGE, a)


# ------------------------------------------------------------------ flux

def flux(d, t, D, m, scene):
    don = scene["donnees"]
    etapes = don["etapes"]
    n = len(etapes)
    ts = instants(m, D, n, don.get("apparitions"))
    vertical = don.get("vertical", n > 5)
    if vertical:
        h = min(120, (BAS - HAUT - 10 * (n - 1)) / n)
        for k, ((titre, detail), debut) in enumerate(zip(etapes, ts)):
            a = apparition(t, debut, 0.5)
            y = HAUT + k * (h + 10)
            panneau(d, (220, y, 1700, y + h), a, CYAN if k == n - 1 and don.get("final") else CYAN_SOMBRE, rayon=14)
            puce_numero(d, (170, y + h / 2), k + 1, a, CYAN, 24)
            texte(d, (255, y + h / 2 - (14 if detail else 0)), titre, "gras", 30, BLANC, a, "lm")
            if detail:
                texte(d, (255, y + h / 2 + 22), detail, "normal", 24, GRIS, a, "lm")
    else:
        larg = (1700 - 50 * (n - 1)) / n
        for k, ((titre, detail), debut) in enumerate(zip(etapes, ts)):
            a = apparition(t, debut, 0.5)
            x = 110 + k * (larg + 50)
            b = (x, 420 + _glisse(a, 30), x + larg, 680 + _glisse(a, 30))
            panneau(d, b, a, CYAN_SOMBRE)
            puce_numero(d, (x + larg / 2, b[1] + 50), k + 1, a, CYAN, 26)
            paragraphe(d, (x + larg / 2, b[1] + 100), titre, "gras", 28, BLANC, a, larg - 30, 1.15, "ma")
            if detail:
                paragraphe(d, (x + larg / 2, b[1] + 170), detail, "normal", 22, GRIS, a, larg - 30, 1.25, "ma")
            if k:
                fleche(d, (x - 46, 550), (x - 6, 550), CYAN, a, 4, 14)


# ------------------------------------------------------------------ chiffres clés

def chiffres(d, t, D, m, scene):
    don = scene["donnees"]
    tuiles = don["tuiles"]
    n = len(tuiles)
    colonnes = don.get("colonnes", min(4, n))
    lignes = math.ceil(n / colonnes)
    larg = (1680 - 30 * (colonnes - 1)) / colonnes
    haut = min(300, (BAS - HAUT - 30 * (lignes - 1)) / lignes)
    marge_haut = (BAS - HAUT - lignes * haut - 30 * (lignes - 1)) * 0.35
    ts = instants(m, D, n, don.get("apparitions"))
    for k, ((valeur, unite, libelle), debut) in enumerate(zip(tuiles, ts)):
        a = apparition(t, debut, 0.5)
        x = 120 + (k % colonnes) * (larg + 30)
        y = HAUT + marge_haut + (k // colonnes) * (haut + 30)
        panneau(d, (x, y + _glisse(a), x + larg, y + haut + _glisse(a)), a, CYAN_SOMBRE)
        p = sortie_cubique((t - debut) / 1.2)
        if isinstance(valeur, (int, float)):
            decimales = len(repr(valeur).split(".")[1]) if isinstance(valeur, float) and valeur % 1 else 0
            v = f"{valeur * p:,.{decimales}f}".replace(",", " ").replace(".", ",")
        else:
            v = valeur
        texte(d, (x + 30, y + haut * 0.42), v, "titre", 76 if lignes == 1 else 64, BLANC, a, "lm")
        texte(d, (x + 30 + largeur(v, "titre", 76 if lignes == 1 else 64) + 12, y + haut * 0.42 + 14), unite, "demi", 30,
              CYAN, a, "lm")
        paragraphe(d, (x + 30, y + haut * 0.66), libelle, "normal", 26, GRIS, a, larg - 60, 1.25)


GABARITS = {f.__name__: f for f in [ouverture, puces, composant, tableau, formule, comparaison, flux, chiffres]}
