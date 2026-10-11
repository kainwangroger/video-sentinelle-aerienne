"""Animation des scènes de la vidéo « fiche projet » (drone hybride VTOL).

Même convention que visuels_technique.py : f(d, t, D, m), où m contient les
instants de début des phrases de narration.
"""

import math

from gfx import (AMBRE, ASPHALTE, BLANC, CYAN, CYAN_SOMBRE, GRIS, PANNEAU, ROUGE, VERT, W,
                 antenne, apparition, avec_alpha, borne, camera, cercle, coche, croix, debris, drone,
                 fleche, ligne_pointillee, melange, panneau, paragraphe, puce_electronique, puce_numero,
                 rectangle_pointille, sortie_cubique, stockage, texte)


def _m(m, i, decalage=0.0):
    return m[min(i, len(m) - 1)] + decalage


def _glisse(a, distance=30):
    return (1 - a) * distance


# ------------------------------------------------------------------ pictogrammes VTOL

def vtol_dessus(d, c, s=1.0, couleur=CYAN, alpha=1.0, t=0.0, rotors=True, helice=True):
    """Drone hybride vu de dessus : fuselage, aile, poutres, 4 rotors de sustentation, hélice propulsive."""
    if alpha <= 0.003:
        return
    x, y = c
    col = avec_alpha(couleur, alpha)
    fond_col = avec_alpha(PANNEAU, alpha)
    e = max(2, int(3 * s))
    # aile
    d.polygon([(x - 300 * s, y - 10 * s), (x + 300 * s, y - 10 * s), (x + 290 * s, y + 35 * s), (x - 290 * s, y + 35 * s)],
              fill=fond_col, outline=col, width=e)
    # poutres
    for bx in (-120, 120):
        d.rounded_rectangle((x + (bx - 7) * s, y - 150 * s, x + (bx + 7) * s, y + 190 * s), int(6 * s), fill=fond_col,
                            outline=col, width=e)
    # empennage
    d.polygon([(x - 135 * s, y + 175 * s), (x + 135 * s, y + 175 * s), (x + 125 * s, y + 200 * s), (x - 125 * s, y + 200 * s)],
              fill=fond_col, outline=col, width=e)
    # fuselage
    d.rounded_rectangle((x - 26 * s, y - 120 * s, x + 26 * s, y + 110 * s), int(24 * s), fill=fond_col, outline=col, width=e)
    cercle(d, (x, y - 85 * s), 11 * s, couleur, alpha, plein=True)
    # hélice propulsive
    if helice:
        a = t * 14
        d.line([(x - 36 * s * math.cos(a), y + 120 * s), (x + 36 * s * math.cos(a), y + 120 * s)],
               fill=avec_alpha(BLANC, alpha * 0.8), width=max(2, int(5 * s)))
    # rotors de sustentation
    if rotors:
        for bx in (-120, 120):
            for by in (-140, 180):
                px, py = x + bx * s, y + by * s
                cercle(d, (px, py), 48 * s, couleur, alpha * 0.8, e)
                for h in range(2):
                    b = t * 16 + h * math.pi + bx
                    d.line([(px - 40 * s * math.cos(b), py - 40 * s * math.sin(b)),
                            (px + 40 * s * math.cos(b), py + 40 * s * math.sin(b))],
                           fill=avec_alpha(BLANC, alpha * 0.5), width=max(2, int(3 * s)))


def vtol_profil(d, c, s=1.0, couleur=CYAN, alpha=1.0, inclinaison=0.0, sens=1):
    """Petit profil latéral : fuselage + aile, pour les animations de trajectoire."""
    if alpha <= 0.003:
        return
    x, y = c
    ca, sa = math.cos(inclinaison), math.sin(inclinaison)

    def r(px, py):
        px *= sens
        return (x + (px * ca - py * sa) * s, y + (px * sa + py * ca) * s)

    corps = [r(-60, -8), r(50, -8), r(66, 0), r(50, 8), r(-60, 8)]
    d.polygon(corps, fill=avec_alpha(PANNEAU, alpha), outline=avec_alpha(couleur, alpha), width=3)
    d.polygon([r(-58, -8), r(-70, -30), r(-48, -8)], fill=avec_alpha(couleur, alpha))
    d.line([r(-20, -2), r(20, -2)], fill=avec_alpha(couleur, alpha), width=max(2, int(6 * s)))
    for px in (-35, 35):
        d.line([r(px, -8), r(px, -20)], fill=avec_alpha(couleur, alpha), width=3)
        d.line([r(px - 18, -20), r(px + 18, -20)], fill=avec_alpha(BLANC, alpha * 0.7), width=3)


def cadenas(d, c, s=1.0, couleur=CYAN, alpha=1.0):
    x, y = c
    d.arc((x - 22 * s, y - 50 * s, x + 22 * s, y - 6 * s), 180, 360, fill=avec_alpha(couleur, alpha), width=max(2, int(6 * s)))
    d.line([(x - 22 * s, y - 28 * s), (x - 22 * s, y - 6 * s)], fill=avec_alpha(couleur, alpha), width=max(2, int(6 * s)))
    d.line([(x + 22 * s, y - 28 * s), (x + 22 * s, y - 6 * s)], fill=avec_alpha(couleur, alpha), width=max(2, int(6 * s)))
    d.rounded_rectangle((x - 34 * s, y - 8 * s, x + 34 * s, y + 40 * s), int(8 * s), fill=avec_alpha(couleur, alpha))
    cercle(d, (x, y + 14 * s), 7 * s, PANNEAU, alpha, plein=True)


def bouclier(d, c, s=1.0, couleur=VERT, alpha=1.0):
    x, y = c
    pts = [(x, y - 50 * s), (x + 42 * s, y - 34 * s), (x + 38 * s, y + 10 * s), (x, y + 50 * s),
           (x - 38 * s, y + 10 * s), (x - 42 * s, y - 34 * s)]
    d.polygon(pts, fill=avec_alpha(PANNEAU, alpha), outline=avec_alpha(couleur, alpha), width=max(2, int(4 * s)))
    coche(d, (x, y), 34 * s, couleur, alpha)


def batterie(d, c, s=1.0, niveau=0.7, couleur=VERT, alpha=1.0):
    x, y = c
    d.rounded_rectangle((x - 50 * s, y - 24 * s, x + 44 * s, y + 24 * s), int(6 * s), outline=avec_alpha(BLANC, alpha),
                        width=max(2, int(4 * s)))
    d.rectangle((x + 44 * s, y - 10 * s, x + 52 * s, y + 10 * s), fill=avec_alpha(BLANC, alpha))
    d.rectangle((x - 42 * s, y - 16 * s, x - 42 * s + 78 * s * niveau, y + 16 * s), fill=avec_alpha(couleur, alpha))


def satellite(d, c, s=1.0, couleur=CYAN, alpha=1.0):
    x, y = c
    d.rectangle((x - 14 * s, y - 14 * s, x + 14 * s, y + 14 * s), fill=avec_alpha(couleur, alpha))
    for dx in (-1, 1):
        d.rectangle((x + dx * 22 * s - 18 * s, y - 9 * s, x + dx * 22 * s + 18 * s, y + 9 * s) if dx > 0 else
                    (x - 58 * s, y - 9 * s, x - 22 * s, y + 9 * s), outline=avec_alpha(couleur, alpha), width=max(2, int(3 * s)))
    d.rectangle((x + 22 * s, y - 9 * s, x + 58 * s, y + 9 * s), outline=avec_alpha(couleur, alpha), width=max(2, int(3 * s)))


def avion(d, c, s=1.0, couleur=GRIS, alpha=1.0):
    x, y = c
    col = avec_alpha(couleur, alpha)
    d.rounded_rectangle((x - 12 * s, y - 70 * s, x + 12 * s, y + 70 * s), int(12 * s), fill=col)
    d.polygon([(x - 110 * s, y), (x + 110 * s, y), (x + 100 * s, y + 22 * s), (x - 100 * s, y + 22 * s)], fill=col)
    d.polygon([(x - 40 * s, y + 55 * s), (x + 40 * s, y + 55 * s), (x + 36 * s, y + 68 * s), (x - 36 * s, y + 68 * s)], fill=col)


# ------------------------------------------------------------------ 1. titre

def titre(d, t, D, m):
    c = (W // 2, 320)
    for k in range(3):
        phase = (t * 0.45 + k / 3) % 1
        cercle(d, c, 140 + phase * 260, CYAN, 0.4 * (1 - phase) * apparition(t, 0.1, 1.0), 2)
    a = apparition(t, 0.0, 0.9)
    vtol_dessus(d, (c[0], c[1] + _glisse(a, 40)), 0.62, CYAN, a, t)
    a = apparition(t, 0.35, 0.8)
    texte(d, (W // 2, 590 + _glisse(a)), "SENTINELLE AÉRIENNE", "titre", 118, BLANC, a, "mm")
    a = apparition(t, 0.9, 0.8)
    texte(d, (W // 2, 690 + _glisse(a, 20)), "Drone hybride VTOL de surveillance des zones sensibles", "moyen", 44, CYAN, a, "mm")
    largeur_trait = 520 * apparition(t, 1.2, 1.0)
    d.line([(W // 2 - largeur_trait / 2, 752), (W // 2 + largeur_trait / 2, 752)], fill=avec_alpha(CYAN_SOMBRE, 1), width=2)
    a = apparition(t, _m(m, 1), 0.7)
    texte(d, (W // 2, 800), "SkyVision Togo  ·  CECFD 2026 — ANAC", "demi", 34, BLANC, a, "mm")
    texte(d, (W // 2, 850), "Thématique : Surveillance & Sécurité  ·  Chef d'équipe : AWADE Constantin Israel",
          "normal", 28, GRIS, a, "mm")


# ------------------------------------------------------------------ 2. concept

def concept(d, t, D, m):
    cartes = [
        ("Multirotor", "Décollage vertical, mais autonomie limitée", ROUGE, 0.3),
        ("Avion", "Grande autonomie, mais besoin d'une piste", ROUGE, _m(m, 0, 2.6)),
        ("Hybride VTOL", "Décollage vertical + croisière à grande autonomie", VERT, _m(m, 1)),
    ]
    for k, (nom, desc, couleur, debut) in enumerate(cartes):
        a = apparition(t, debut, 0.6)
        x = 140 + k * 560
        b = (x, 280 + _glisse(a, 40), x + 520, 860 + _glisse(a, 40))
        panneau(d, b, a, couleur if k == 2 else CYAN_SOMBRE, epaisseur=3 if k == 2 else 2)
        cy = b[1] + 190
        if k == 0:
            drone(d, (x + 260, cy), 1.1, GRIS, a, t)
        elif k == 1:
            avion(d, (x + 260, cy - 10), 1.1, GRIS, a)
        else:
            vtol_dessus(d, (x + 260, cy - 20), 0.42, CYAN, a, t)
        texte(d, (x + 260, b[1] + 390), nom, "gras", 42, BLANC, a, "mm")
        paragraphe(d, (x + 260, b[1] + 440), desc, "normal", 28, GRIS, a, 430, 1.35, "ma")
        if k < 2:
            croix(d, (x + 470, b[1] + 50), 34, ROUGE, a)
        else:
            coche(d, (x + 470, b[1] + 50), 40, VERT, a)


# ------------------------------------------------------------------ 3. profil de vol

SOL, ALLER, RETOUR = 780, 520, 380


def _trajectoire(u):
    """Point (x, y, sens) du profil de mission pour u de 0 à 1 ; sens = 1 vers la droite, -1 au retour."""
    if u < 0.14:  # décollage vertical
        return 240, SOL - (SOL - ALLER) * sortie_cubique(u / 0.14), 1
    if u < 0.22:  # transition vers le vol horizontal
        k = (u - 0.14) / 0.08
        return 240 + 160 * k * k, ALLER, 1
    if u < 0.55:  # croisière aller
        k = (u - 0.22) / 0.33
        return 400 + 1150 * k, ALLER, 1
    if u < 0.63:  # demi-tour après la perte de signal
        k = (u - 0.55) / 0.08
        a = -math.pi / 2 + math.pi * k
        r = (ALLER - RETOUR) / 2
        return 1550 + r * math.cos(a), (ALLER + RETOUR) / 2 - r * math.sin(a), 1 if k < 0.5 else -1
    if u < 0.88:  # retour automatique
        k = (u - 0.63) / 0.25
        return 1550 - 1310 * k, RETOUR, -1
    k = (u - 0.88) / 0.12  # atterrissage vertical au point de départ
    return 240, RETOUR + (SOL - RETOUR) * sortie_cubique(k), -1


def profil(d, t, D, m):
    a = apparition(t, 0.2, 0.6)
    d.line([(120, SOL + 20), (1800, SOL + 20)], fill=avec_alpha(GRIS, a), width=3)
    d.polygon([(180, SOL + 20), (300, SOL + 20), (290, SOL), (190, SOL)], fill=avec_alpha(ASPHALTE, a))
    texte(d, (240, SOL + 55), "Terrain confiné", "moyen", 26, GRIS, a, "mm")
    etapes = [(330, 660, "Décollage vertical", "aucune piste", _m(m, 0), "la"),
              (900, 570, "Croisière horizontale", "grandes zones, économie d'énergie", _m(m, 1, 1.0), "ma"),
              (900, 245, "Retour automatique", "Return To Home", _m(m, 2, 1.0), "ma"),
              (1660, 380, "Perte de signal", "demi-tour", _m(m, 2), "la")]
    for x, y, nom, desc, debut, ancre in etapes:
        a2 = apparition(t, debut, 0.5)
        couleur = AMBRE if nom == "Perte de signal" else CYAN
        texte(d, (x, y), nom, "demi", 30, couleur, a2, ancre)
        texte(d, (x, y + 40), desc, "normal", 25, GRIS, a2, ancre)
    debut, fin = _m(m, 0), D - 0.6
    u = borne((t - debut) / max(1.0, fin - debut))
    if t > debut:
        pts = [_trajectoire(k / 300 * u)[:2] for k in range(301)]
        d.line(pts, fill=avec_alpha(CYAN_SOMBRE, 0.9), width=3)
    x, y, sens = _trajectoire(u)
    vtol_profil(d, (x, y), 1.4, CYAN, apparition(t, 0.3, 0.6), sens=sens)


# ------------------------------------------------------------------ 4. innovation IA

def innovation_ia(d, t, D, m):
    a = apparition(t, 0.2, 0.6)
    x = 600 + 120 * math.sin(t * 0.4)
    d.polygon([(x, 330), (x - 260, 820), (x + 260, 820)], fill=avec_alpha(CYAN, 0.10 * a))
    d.rectangle((150, 820, 1100, 860), fill=avec_alpha(ASPHALTE, a))
    vtol_profil(d, (x, 320), 1.6, CYAN, a)
    a2 = apparition(t, _m(m, 1, 0.6), 0.4)
    debris(d, (640, 800), 1.4, BLANC, a)
    rectangle_pointille(d, (580, 740, 710, 850), AMBRE, a2, 4, t * 30)
    texte(d, (645, 715), "anomalie", "gras", 26, AMBRE, a2, "mm")
    a3 = apparition(t, _m(m, 1, 1.6), 0.5)
    panneau(d, (1180, 360, 1780, 560), a3, AMBRE)
    texte(d, (1220, 410), "ALERTE IMMÉDIATE", "gras", 34, AMBRE, a3, "lm")
    texte(d, (1220, 470), "Analyse à bord, en temps réel", "moyen", 30, BLANC, a3, "lm")
    texte(d, (1220, 515), "Sans connexion ni traitement différé", "normal", 28, GRIS, a3, "lm")
    a4 = apparition(t, _m(m, 0, 0.5), 0.5)
    puce_electronique(d, (1260, 700), 1.2, CYAN, a4)
    texte(d, (1330, 690), "Vision par ordinateur", "demi", 32, BLANC, a4, "lm")
    texte(d, (1330, 735), "embarquée dans le drone", "normal", 28, GRIS, a4, "lm")


# ------------------------------------------------------------------ 5. innovation liaison

def innovation_liaison(d, t, D, m):
    a = apparition(t, 0.2, 0.6)
    vtol_profil(d, (330, 450), 1.8, CYAN, a)
    antenne(d, (1600, 430), 1.6, CYAN, a)
    texte(d, (1600, 540), "Station de contrôle", "moyen", 28, GRIS, a, "mm")
    ligne_pointillee(d, (460, 450), (1530, 450), CYAN, a, 5, 18, 12, -t * 80)
    a2 = apparition(t, _m(m, 1), 0.5)
    panneau(d, (850, 380, 1110, 520), a2, CYAN)
    cadenas(d, (980, 440), 1.0, CYAN, a2)
    texte(d, (980, 560), "Chiffrée et authentifiée", "demi", 30, BLANC, a2, "mm")
    menaces = [("Brouillage radio", _m(m, 1, 2.2)), ("Leurrage GPS (spoofing)", _m(m, 1, 3.2))]
    for k, (nom, debut) in enumerate(menaces):
        a3 = apparition(t, debut, 0.5)
        x = 420 + k * 640
        panneau(d, (x, 680, x + 560, 820), a3, VERT)
        bouclier(d, (x + 80, 750), 1.0, VERT, a3)
        texte(d, (x + 150, 730), nom, "gras", 32, BLANC, a3, "lm")
        texte(d, (x + 150, 775), "détecté et signalé", "normal", 26, GRIS, a3, "lm")


# ------------------------------------------------------------------ 6. configuration

def configuration(d, t, D, m):
    c = (700, 560)
    a = apparition(t, 0.2, 0.7)
    vtol_dessus(d, c, 0.95, CYAN, a, t)
    reperes = [("Aile fixe", "vol de croisière", (c[0] - 285, c[1] + 12), (1180, 330), _m(m, 0, 0.3)),
               ("4 rotors de sustentation", "décollage et atterrissage verticaux", (c[0] + 114, c[1] - 133), (1180, 480), _m(m, 0, 2.3)),
               ("Moteur de propulsion", "croisière tractive ou propulsive", (c[0], c[1] + 114), (1180, 630), _m(m, 0, 4.6)),
               ("Transition automatique", "pilotée par le contrôleur de vol", None, (1180, 780), _m(m, 1))]
    for nom, desc, cible, (x, y), debut in reperes:
        a2 = apparition(t, debut, 0.5)
        if cible:
            d.line([cible, (x - 20, y)], fill=avec_alpha(AMBRE, a2 * 0.8), width=2)
            cercle(d, cible, 8, AMBRE, a2, plein=True)
        texte(d, (x, y - 18), nom, "gras", 34, AMBRE if cible else CYAN, a2, "lm")
        texte(d, (x, y + 24), desc, "normal", 28, GRIS, a2, "lm")


# ------------------------------------------------------------------ 7. structure

def structure(d, t, D, m):
    a = apparition(t, 0.2, 0.6)
    b = (150, 290, 860, 860)
    panneau(d, b, a, CYAN_SOMBRE)
    # trame de fibre de carbone
    for gx in range(b[0] + 20, b[2] - 20, 36):
        for gy in range(b[1] + 20, b[3] - 20, 36):
            sens = ((gx - b[0]) // 36 + (gy - b[1]) // 36) % 2
            d.line([(gx, gy + (24 if sens else 0)), (gx + 24, gy + (0 if sens else 24))],
                   fill=avec_alpha(CYAN_SOMBRE, a * 0.3), width=2)
    vtol_dessus(d, (505, 560), 0.55, CYAN, a, t)
    texte(d, (505, 810), "Fibre de carbone / composite · SolidWorks", "demi", 28, BLANC, a, "mm")
    chaine = [("Masse en charge", "et profil de mission"), ("Moteurs", "puissance et poussée"),
              ("ESC", "variateurs adaptés"), ("Hélices", "diamètre et pas")]
    for k, (nom, desc) in enumerate(chaine):
        a2 = apparition(t, _m(m, 1, k * 0.9), 0.5)
        y = 300 + k * 140
        panneau(d, (1000, y, 1760, y + 105), a2, CYAN if k == 0 else CYAN_SOMBRE)
        texte(d, (1040, y + 36), nom, "gras", 34, CYAN if k == 0 else BLANC, a2, "lm")
        texte(d, (1040, y + 76), desc, "normal", 26, GRIS, a2, "lm")
        if k:
            fleche(d, (1380, y - 34), (1380, y - 2), CYAN_SOMBRE, a2, 3, 10)


# ------------------------------------------------------------------ 8. avionique

def avionique(d, t, D, m):
    c = (960, 560)
    a = apparition(t, 0.2, 0.6)
    panneau(d, (c[0] - 170, c[1] - 90, c[0] + 170, c[1] + 90), a, CYAN, epaisseur=3)
    texte(d, (c[0], c[1] - 30), "Contrôleur de vol", "gras", 32, BLANC, a, "mm")
    texte(d, (c[0], c[1] + 20), "Pixhawk · ArduPilot / PX4", "normal", 26, CYAN, a, "mm")
    texte(d, (c[0], c[1] + 56), "multirotor · aile fixe · transition", "normal", 22, GRIS, a, "mm")
    satellites = [
        ("IMU", "centrale inertielle", (400, 340), _m(m, 0, 2.5), CYAN),
        ("Baromètre", "altitude", (400, 560), _m(m, 0, 3.6), CYAN),
        ("Magnétomètre", "cap", (400, 780), _m(m, 0, 4.4), CYAN),
        ("GPS / GNSS", "Return To Home", (1520, 340), _m(m, 1, 0.2), VERT),
        ("Fail-safe", "coupure, descente sécurisée", (1520, 560), _m(m, 1, 2.0), ROUGE),
        ("Batterie LiPo", "tension supervisée, alerte critique", (1520, 780), _m(m, 1, 3.4), AMBRE),
    ]
    for nom, desc, (x, y), debut, couleur in satellites:
        a2 = apparition(t, debut, 0.5)
        cote = -1 if x < c[0] else 1
        d.line([(c[0] + cote * 170, c[1]), (x - cote * 210, y)], fill=avec_alpha(couleur, a2 * 0.6), width=3)
        panneau(d, (x - 210, y - 65, x + 210, y + 65), a2, couleur)
        texte(d, (x, y - 18), nom, "gras", 32, BLANC, a2, "mm")
        texte(d, (x, y + 24), desc, "normal", 23, GRIS, a2, "mm")


# ------------------------------------------------------------------ 9. charge utile

def charge_utile(d, t, D, m):
    a = apparition(t, 0.2, 0.6)
    c = (520, 520)
    # nacelle gyrostabilisée : le support oscille, la caméra reste horizontale
    osc = 0.25 * math.sin(t * 1.6)
    d.line([(c[0], 300), (c[0], c[1] - 70)], fill=avec_alpha(GRIS, a), width=8)
    d.arc((c[0] - 120, c[1] - 120, c[0] + 120, c[1] + 120), 200 + math.degrees(osc), 340 + math.degrees(osc),
          fill=avec_alpha(GRIS, a), width=8)
    cercle(d, c, 95, CYAN, a, 4)
    camera(d, (c[0] + 5, c[1]), 1.5, CYAN, a)
    texte(d, (c[0], 690), "Nacelle gyrostabilisée", "demi", 30, BLANC, a, "mm")
    modes = [("Visible", "jour", BLANC, _m(m, 0, 1.2)), ("Infrarouge / thermique", "nuit", AMBRE, _m(m, 0, 2.2))]
    for k, (nom, desc, couleur, debut) in enumerate(modes):
        a2 = apparition(t, debut, 0.5)
        x = 300 + k * 260
        cercle(d, (x - 30, 780), 14, couleur, a2, plein=True)
        texte(d, (x - 6, 768), nom, "demi", 24, BLANC, a2, "lm")
        texte(d, (x - 6, 800), desc, "normal", 22, GRIS, a2, "lm")
    modules = [("Surveillance", "caméra jour / nuit + IA", CYAN, _m(m, 0)),
               ("Cartographie", "orthophotos, nuages de points", CYAN_SOMBRE, _m(m, 1, 1.6)),
               ("Aide humanitaire", "charge utile adaptée", CYAN_SOMBRE, _m(m, 1, 2.6))]
    for k, (nom, desc, couleur, debut) in enumerate(modules):
        a2 = apparition(t, debut, 0.5)
        y = 300 + k * 180
        panneau(d, (1000 + _glisse(a2, -40), y, 1760, y + 140), a2, couleur, epaisseur=3 if k == 0 else 2)
        texte(d, (1050, y + 50), nom, "gras", 36, CYAN if k == 0 else BLANC, a2, "lm")
        texte(d, (1050, y + 98), desc, "normal", 28, GRIS, a2, "lm")
        texte(d, (1720, y + 70), "actif" if k == 0 else "extension", "demi", 22, VERT if k == 0 else GRIS, a2, "rm")


# ------------------------------------------------------------------ 10. station

def station(d, t, D, m):
    a = apparition(t, 0.2, 0.6)
    b = (150, 280, 1150, 860)
    panneau(d, b, a, CYAN, rayon=24, epaisseur=3)
    d.rectangle((b[0] + 3, b[1] + 3, b[2] - 3, b[1] + 55), fill=avec_alpha((10, 50, 80), a))
    texte(d, (b[0] + 30, b[1] + 29), "Station sol — Sentinelle Aérienne", "demi", 24, BLANC, a, "lm")
    texte(d, (b[2] - 30, b[1] + 29), "MAVLink · liaison chiffrée", "normal", 22, VERT, a, "rm")
    # carte de mission
    carte = (b[0] + 30, b[1] + 80, b[0] + 620, b[3] - 30)
    a2 = apparition(t, _m(m, 0, 4.2), 0.5)
    d.rectangle(carte, fill=avec_alpha((18, 40, 60), a), outline=avec_alpha(CYAN_SOMBRE, a), width=2)
    pts = [(250, 760), (300, 450), (600, 420), (700, 650), (480, 740)]
    d.line(pts + [pts[0]], fill=avec_alpha(AMBRE, a2), width=3)
    for p in pts:
        cercle(d, p, 9, AMBRE, a2, plein=True)
    u = (t * 0.08) % 1
    seg = u * len(pts)
    i = int(seg)
    p0, p1 = pts[i % len(pts)], pts[(i + 1) % len(pts)]
    k = seg - i
    cercle(d, (p0[0] + (p1[0] - p0[0]) * k, p0[1] + (p1[1] - p0[1]) * k), 12, CYAN, a2, plein=True)
    texte(d, (carte[0] + 16, carte[1] + 24), "Plan de mission", "demi", 22, GRIS, a, "lm")
    # télémétrie
    a3 = apparition(t, _m(m, 0, 2.2), 0.5)
    tele = [("Altitude", f"{120 + 4 * math.sin(t):.0f} m"), ("Vitesse", f"{17 + math.sin(t * 0.7):.1f} m/s"),
            ("Batterie", f"{max(20, 86 - t * 0.8):.0f} %"), ("Liaison", "chiffrée")]
    for k, (cle, val) in enumerate(tele):
        y = b[1] + 110 + k * 75
        texte(d, (b[0] + 660, y), cle, "normal", 24, GRIS, a3, "lm")
        texte(d, (b[2] - 30, y), val, "demi", 28, VERT if cle == "Liaison" else BLANC, a3, "rm")
    texte(d, (b[0] + 660, b[3] - 70), "valeurs simulées", "normal", 20, GRIS, a3, "lm")
    elements = [("Télémétrie", _m(m, 0, 2.2)), ("Planification de mission", _m(m, 0, 4.2)),
                ("Journal et archivage des vols", _m(m, 0, 5.5)), ("Liaison MAVLink chiffrée", _m(m, 1))]
    for k, (nom, debut) in enumerate(elements):
        a4 = apparition(t, debut, 0.5)
        y = 330 + k * 130
        panneau(d, (1240, y, 1780, y + 100), a4, VERT if k == 3 else CYAN_SOMBRE)
        coche(d, (1290, y + 50), 30, VERT if k == 3 else CYAN, a4)
        texte(d, (1330, y + 50), nom, "demi", 28, BLANC, a4, "lm")


# ------------------------------------------------------------------ 11. conformité

EXIGENCES = [("Navigation GPS avec retour de position (RTH)", "GPS/GNSS + contrôleur de vol, Return To Home"),
             ("Coupure d'urgence (fail-safe)", "Interrupteur moteurs + descente sécurisée"),
             ("Lien sécurisé drone / station", "Liaison chiffrée avec authentification"),
             ("Autonomie minimale en vol", "LiPo haute capacité + croisière horizontale"),
             ("Emport de charge utile", "Caméra jour/nuit sur nacelle + modularité"),
             ("Documentation technique", "Schémas, dimensionnement, performances, sécurité")]


def conformite(d, t, D, m):
    for k, (exigence, solution) in enumerate(EXIGENCES):
        a = apparition(t, 0.3 + k * 0.45, 0.4)
        y = 270 + k * 92
        panneau(d, (140, y, 1330, y + 78), a, CYAN_SOMBRE, rayon=12)
        coche(d, (185, y + 39), 30, VERT, a)
        texte(d, (225, y + 26), exigence, "demi", 27, BLANC, a, "lm")
        texte(d, (225, y + 56), solution, "normal", 23, GRIS, a, "lm")
    # jauge d'autonomie
    a = apparition(t, _m(m, 1), 0.6)
    c = (1600, 560)
    cercle(d, c, 170, CYAN_SOMBRE, a * 0.6, 18)
    p = sortie_cubique((t - _m(m, 1)) / 1.6)
    d.arc((c[0] - 170, c[1] - 170, c[0] + 170, c[1] + 170), -90, -90 + 270 * p, fill=avec_alpha(CYAN, a), width=18)
    texte(d, (c[0], c[1] - 20), "30–45", "titre", 72, BLANC, a, "mm")
    texte(d, (c[0], c[1] + 45), "minutes visées", "moyen", 28, GRIS, a, "mm")
    texte(d, (c[0], c[1] + 230), "Autonomie cible", "demi", 30, CYAN, a, "mm")


# ------------------------------------------------------------------ 12. équipe

MEMBRES = [("AWADE Constantin Israel", "Chef d'équipe", "Mécanique, structure, intégration électronique, qualité"),
           ("LOGO ADANTO Angelo", "Logiciel embarqué", "Logiciel embarqué et interface de la station sol"),
           ("KODJOVI Eli Cédric Ankou", "Back-end", "Embarqué, back-end de supervision, documentation"),
           ("de MEDEIROS Makafui Komlan Léopoldo", "Réseau & sécurité", "Liaison radio, télémétrie, communications sécurisées"),
           ("KAINWANG Roger", "Intelligence artificielle", "Traitement des données, détection d'anomalies, vision")]


def equipe(d, t, D, m):
    for k, (nom, pole, role) in enumerate(MEMBRES):
        a = apparition(t, _m(m, 0, 0.3 + k * 0.9) if k else _m(m, 1, 0), 0.5)
        if k == 0:
            a = max(a, apparition(t, 0.3, 0.5))
        y = 270 + k * 125
        chef = k == 0
        panneau(d, (140 + _glisse(a, -40), y, 1780, y + 105), a, AMBRE if chef else CYAN_SOMBRE, epaisseur=3 if chef else 2)
        cercle(d, (205, y + 52), 30, AMBRE if chef else CYAN, a, 3)
        initiales = "".join(p[0] for p in nom.replace("de ", "").split()[:2])
        texte(d, (205, y + 52), initiales, "gras", 22, BLANC, a, "mm")
        texte(d, (260, y + 34), nom, "gras", 30, BLANC, a, "lm")
        texte(d, (260, y + 74), role, "normal", 25, GRIS, a, "lm")
        texte(d, (1740, y + 52), pole.upper(), "gras", 22, AMBRE if chef else CYAN, a, "rm")


# ------------------------------------------------------------------ 13. calendrier

JALONS = [("15–30 août 2026", "Candidature et cahier des charges"),
          ("Septembre 2026", "Conception détaillée : 3D, composants, logiciel"),
          ("30 septembre 2026", "Soumission du dossier de conception"),
          ("Octobre – novembre", "Prototypage, intégration, essais sol et vol"),
          ("Semaine du 7 décembre", "Démonstration, oral et remise des prix")]


def calendrier(d, t, D, m):
    xs = [220 + k * 370 for k in range(5)]
    y = 470
    debuts = [0.3, 1.0, _m(m, 0), _m(m, 1), _m(m, 2)]
    d.line([(xs[0], y), (xs[-1], y)], fill=avec_alpha(CYAN_SOMBRE, apparition(t, 0.2, 0.5) * 0.6), width=4)
    prog = sum(apparition(t, debuts[k], 0.6) for k in range(1, 5))
    d.line([(xs[0], y), (xs[0] + (xs[-1] - xs[0]) * prog / 4, y)], fill=avec_alpha(CYAN, 1), width=6)
    for k, (date, etape) in enumerate(JALONS):
        a = apparition(t, debuts[k], 0.5)
        final = k == 4
        couleur = AMBRE if final else CYAN
        cercle(d, (xs[k], y), 22, couleur, max(a, 0.3), 4)
        if a > 0.5:
            cercle(d, (xs[k], y), 12, couleur, a, plein=True)
        texte(d, (xs[k], y - 70), date, "gras", 28, couleur, max(a, 0.25), "mm")
        paragraphe(d, (xs[k], y + 50), etape, "normal", 26, BLANC, a, 320, 1.3, "ma")
    a = apparition(t, _m(m, 2, 0.5), 0.5)
    panneau(d, (610, 760, 1310, 860), a, AMBRE, rayon=50, epaisseur=3)
    texte(d, (960, 810), "Objectif : démonstration en vol", "gras", 34, AMBRE, a, "mm")


# ------------------------------------------------------------------ 14. budget

POSTES = [("Cellule, moteurs, ESC, hélices", 200, 350), ("Contrôleur de vol + GPS + capteurs", 200, 350),
          ("Caméra + nacelle stabilisée", 120, 300), ("Batteries et alimentation", 80, 150),
          ("Liaison radio / télémétrie", 80, 150), ("Consommables et divers", 50, 100)]


def budget(d, t, D, m):
    x0, x1 = 760, 1600
    echelle = (x1 - x0) / 400
    a0 = apparition(t, 0.2, 0.5)
    for v in range(0, 401, 100):
        x = x0 + v * echelle
        d.line([(x, 275), (x, 820)], fill=avec_alpha(CYAN_SOMBRE, a0 * 0.35), width=1)
        texte(d, (x, 840), f"{v} k", "normal", 22, GRIS, a0, "mm")
    for k, (nom, mini, maxi) in enumerate(POSTES):
        a = apparition(t, 0.4 + k * 0.4, 0.5)
        y = 300 + k * 85
        texte(d, (720, y + 20), nom, "moyen", 27, BLANC, a, "rm")
        p = sortie_cubique((t - 0.4 - k * 0.4) / 0.9)
        d.rounded_rectangle((x0, y + 4, x0 + maxi * echelle * p, y + 36), 8, fill=avec_alpha(CYAN_SOMBRE, a * 0.55))
        d.rounded_rectangle((x0, y + 4, x0 + mini * echelle * p, y + 36), 8, fill=avec_alpha(CYAN, a))
        texte(d, (x0 + maxi * echelle + 16, y + 20), f"{mini}–{maxi} k", "demi", 24, GRIS, a * p, "lm")
    a2 = apparition(t, _m(m, 0, 0.5), 0.6)
    texte(d, (1800, 210), "Total : 730 000 – 1 400 000 FCFA", "gras", 36, AMBRE, a2, "rm")
    a3 = apparition(t, 1.0, 0.5)
    d.rounded_rectangle((760, 870, 790, 890), 4, fill=avec_alpha(CYAN, a3))
    texte(d, (800, 880), "estimation basse", "normal", 22, GRIS, a3, "lm")
    d.rounded_rectangle((1010, 870, 1040, 890), 4, fill=avec_alpha(CYAN_SOMBRE, a3 * 0.55))
    texte(d, (1050, 880), "estimation haute (milliers de FCFA)", "normal", 22, GRIS, a3, "lm")


# ------------------------------------------------------------------ 15. conclusion

def conclusion(d, t, D, m):
    a = apparition(t, 0.0, 0.8)
    vtol_dessus(d, (960, 280), 0.42, CYAN, a, t)
    texte(d, (960, 450), "SENTINELLE AÉRIENNE", "titre", 96, BLANC, a, "mm")
    mots = ["Décoller partout.", "Surveiller loin.", "Alerter immédiatement."]
    for k, mot in enumerate(mots):
        a2 = apparition(t, _m(m, 0, 1.2 + k * 0.9), 0.5)
        texte(d, (560 + k * 400, 560), mot, "demi", 38, CYAN, a2, "mm")
    a = apparition(t, _m(m, 1), 0.6)
    texte(d, (960, 680), "SkyVision Togo  ·  CECFD 2026 — ANAC", "demi", 32, BLANC, a, "mm")
    texte(d, (960, 730), "Surveillance & Sécurité des zones sensibles", "normal", 28, GRIS, a, "mm")


SCENES_VISUELLES = {f.__name__: f for f in [titre, concept, profil, innovation_ia, innovation_liaison, configuration,
                                             structure, avionique, charge_utile, station, conformite, equipe,
                                             calendrier, budget, conclusion]}
