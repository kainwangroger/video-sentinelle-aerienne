"""Animations spécifiques des notions du drone : signature f(d, t, D, m, scene)."""

import math

from gfx import (AMBRE, ASPHALTE, BLANC, CYAN, CYAN_SOMBRE, GRIS, PANNEAU, ROUGE, VERT, W, antenne, apparition,
                 avec_alpha, borne, cercle, coche, croix, fleche, ligne_pointillee, melange, panneau, paragraphe,
                 sortie_cubique, texte)
from visuels_projet import cadenas, satellite, vtol_dessus, vtol_profil

from .gabarits import BAS, HAUT, instants
from .pictos import dessiner


def _m(m, i, decalage=0.0):
    return m[min(i, len(m) - 1)] + decalage


def _progression(t, m, D, i0=0):
    """0 -> 1 entre le début de la phrase i0 et la fin de la scène."""
    debut = _m(m, i0)
    return borne((t - debut) / max(1.0, D - 1.0 - debut))


def _jauge(d, x, y, larg, valeur, vmax, libelle, unite, couleur=CYAN, a=1.0, seuils=()):
    d.rounded_rectangle((x, y, x + larg, y + 26), 8, fill=avec_alpha(PANNEAU, a), outline=avec_alpha(CYAN_SOMBRE, a), width=2)
    d.rounded_rectangle((x, y, x + larg * borne(valeur / vmax), y + 26), 8, fill=avec_alpha(couleur, a))
    for k, (s, nom) in enumerate(seuils):
        xs = x + larg * s / vmax
        d.line([(xs, y - 8), (xs, y + 34)], fill=avec_alpha(AMBRE, a), width=3)
        texte(d, (xs, y + 48 + 22 * k), nom, "normal", 18, AMBRE, a, "rm" if k == 0 else "lm")
    texte(d, (x, y - 22), libelle, "demi", 24, GRIS, a, "lm")
    texte(d, (x + larg, y - 22), f"{valeur:.1f} {unite}", "gras", 24, BLANC, a, "rm")


# ------------------------------------------------------------------ forces

def forces(d, t, D, m, scene):
    a = apparition(t, 0.2, 0.7)
    c = (960, 560)
    vtol_profil(d, c, 3.0, CYAN, a)
    fl = [("PORTANCE", (0, -1), CYAN, 0), ("POIDS", (0, 1), AMBRE, 1), ("POUSSÉE", (1, 0), VERT, 2),
          ("TRAÎNÉE", (-1, 0), ROUGE, 3)]
    ts = instants(m, D, 4, scene["donnees"].get("apparitions"))
    for (nom, (dx, dy), couleur, k), debut in zip(fl, ts):
        a2 = apparition(t, debut, 0.6)
        l = (190 if dy else 230) * sortie_cubique((t - debut) / 0.8)
        if l < 5:
            continue
        ox, oy = c[0] + dx * 80, c[1] + dy * 40
        fleche(d, (ox, oy), (ox + dx * l, oy + dy * l), couleur, a2, 8, 26)
        if dy:
            texte(d, (ox + 30, oy + dy * (l - 20)), nom, "gras", 34, couleur, a2, "lm")
        else:
            texte(d, (ox + dx * (l + 90), oy), nom, "gras", 34, couleur, a2, "mm")
    a3 = apparition(t, _m(m, len(m) - 1, 0.5), 0.6)
    texte(d, (960, 890), "Palier stable :  portance = poids   et   poussée = traînée", "demi", 34, BLANC, a3, "mm")


# ------------------------------------------------------------------ axes

def axes(d, t, D, m, scene):
    noms = [("ROULIS", "ailes qui penchent", ROUGE), ("TANGAGE", "nez qui monte ou descend", VERT),
            ("LACET", "nez qui tourne", AMBRE)]
    ts = instants(m, D, 3, scene["donnees"].get("apparitions"))
    for k, ((nom, desc, couleur), debut) in enumerate(zip(noms, ts)):
        a = apparition(t, debut, 0.6)
        x = 330 + k * 630
        actif = debut <= t < (ts[k + 1] if k < 2 else D)
        panneau(d, (x - 280, HAUT + 20, x + 280, BAS - 40), a, couleur if actif else CYAN_SOMBRE, epaisseur=3 if actif else 2)
        osc = math.sin((t - debut) * 2.2) * 0.35 if actif else 0
        cy = 520
        if k == 0:  # vue de face : ailes qui penchent
            ca, sa = math.cos(osc), math.sin(osc)
            pts = [(-200, -6), (200, -6), (200, 6), (-200, 6)]
            d.polygon([(x + px * ca - py * sa, cy + px * sa + py * ca) for px, py in pts], fill=avec_alpha(CYAN, a))
            cercle(d, (x, cy), 30, CYAN, a, plein=True)
        elif k == 1:  # vue de côté : tangage
            vtol_profil(d, (x, cy), 2.2, CYAN, a, osc)
        else:  # vue de dessus : lacet
            if not actif:
                vtol_dessus(d, (x, cy), 0.42, CYAN, a, t, rotors=False)
            else:
                # rotation de la vue de dessus : on dessine le profil tourné faute de rotation d'image
                ca, sa = math.cos(osc), math.sin(osc)
                corps = [(-20, -120), (20, -120), (20, 110), (-20, 110)]
                aile = [(-200, -10), (200, -10), (200, 30), (-200, 30)]
                for forme in (aile, corps):
                    d.polygon([(x + px * ca - py * sa, cy + px * sa + py * ca) for px, py in forme], fill=avec_alpha(CYAN, a))
        texte(d, (x, HAUT + 80), nom, "titre", 44, couleur, a, "mm")
        texte(d, (x, BAS - 100), desc, "moyen", 28, BLANC, a, "mm")


# ------------------------------------------------------------------ portance d'une aile

def portance_aile(d, t, D, m, scene):
    a = apparition(t, 0.2, 0.7)
    c = (900, 560)
    angle = math.radians(4 + 6 * _progression(t, m, D, 1))
    ca, sa = math.cos(-angle), math.sin(-angle)
    dessus, dessous = [], []
    for k in range(41):  # profil NACA 4412 (cambrure 4 %, à 40 %, épaisseur 12 %)
        u = (k / 40) ** 1.5
        yc = 0.04 / 0.16 * (0.8 * u - u * u) if u < 0.4 else 0.04 / 0.36 * (0.2 + 0.8 * u - u * u)
        yt = 0.6 * (0.2969 * math.sqrt(u) - 0.126 * u - 0.3516 * u ** 2 + 0.2843 * u ** 3 - 0.1015 * u ** 4)
        dessus.append((u, yc + yt))
        dessous.append((u, yc - yt))
    corde = 700

    def ecran(u, y):
        px, py = (u - 0.3) * corde, -y * corde
        return c[0] + px * ca - py * sa, c[1] + px * sa + py * ca

    d.polygon([ecran(u, y) for u, y in dessus] + [ecran(u, y) for u, y in reversed(dessous)],
              fill=avec_alpha(PANNEAU, a), outline=avec_alpha(CYAN, a), width=4)
    for k in range(7):  # lignes de courant
        y0 = c[1] - 240 + k * 80
        decal = (t * 220 + k * 40) % 120
        courbe = []
        for x in range(150, 1700, 12):
            infl = math.exp(-((x - c[0]) / 380) ** 2) * (60 if y0 < c[1] else 25) * (1 if y0 < c[1] else -0.3)
            dev = (x - c[0]) / 900 * 90 if x > c[0] else 0
            courbe.append((x, y0 - infl + dev * 0.6))
        for i in range(0, len(courbe) - 1, 2):
            if (i * 12 + decal) % 120 < 70:
                d.line([courbe[i], courbe[i + 1]], fill=avec_alpha(CYAN_SOMBRE, a * 0.8), width=3)
    a2 = apparition(t, _m(m, 1), 0.6)
    fleche(d, (c[0], c[1] - 40), (c[0], c[1] - 300), CYAN, a2, 8, 26)
    texte(d, (c[0] + 30, c[1] - 280), "PORTANCE", "gras", 32, CYAN, a2, "lm")
    texte(d, (1450, 300), f"angle d'attaque : {math.degrees(angle):.0f}°", "demi", 30, AMBRE, a2, "mm")
    a3 = apparition(t, _m(m, 2), 0.6)
    panneau(d, (1180, 760, 1800, 870), a3, CYAN)
    texte(d, (1490, 815), "L = ½ · ρ · V² · S · CL", "titre", 44, BLANC, a3, "mm")


# ------------------------------------------------------------------ intérieur d'un moteur sans balais

def moteur_interne(d, t, D, m, scene):
    a = apparition(t, 0.2, 0.7)
    c = (720, 560)
    rot = t * 1.4
    nb = 12
    actif = int((t * 1.4 * 14 / (2 * math.pi)) * 3) % 3
    for k in range(nb):  # dents du stator + bobines
        ang = 2 * math.pi * k / nb
        phase = k % 3
        couleur = [ROUGE, VERT, AMBRE][phase]
        allume = phase == actif
        x1, y1 = c[0] + 70 * math.cos(ang), c[1] + 70 * math.sin(ang)
        x2, y2 = c[0] + 170 * math.cos(ang), c[1] + 170 * math.sin(ang)
        d.line([(x1, y1), (x2, y2)], fill=avec_alpha(couleur, a * (1 if allume else 0.35)), width=34)
    cercle(d, c, 70, GRIS, a, plein=True)
    for k in range(14):  # aimants du rotor (cloche)
        ang = rot + 2 * math.pi * k / 14
        couleur = CYAN if k % 2 else BLANC
        d.arc((c[0] - 215, c[1] - 215, c[0] + 215, c[1] + 215), math.degrees(ang) - 10, math.degrees(ang) + 10,
              fill=avec_alpha(couleur, a), width=28)
        texte(d, (c[0] + 215 * math.cos(ang), c[1] + 215 * math.sin(ang)), "N" if k % 2 else "S", "gras", 16,
              (10, 20, 40), a, "mm")
    cercle(d, c, 240, CYAN_SOMBRE, a, 4)
    legendes = [("Stator : bobines fixes (3 phases)", AMBRE, 0), ("Rotor : cloche à aimants qui tourne", CYAN, 1),
                ("L'ESC alimente les bobines à tour de rôle", VERT, 2)]
    ts = instants(m, D, 3, scene["donnees"].get("apparitions"))
    for (txt, couleur, k), debut in zip(legendes, ts):
        a2 = apparition(t, debut, 0.5)
        y = 380 + k * 120
        cercle(d, (1110, y), 12, couleur, a2, plein=True)
        paragraphe(d, (1140, y - 20), txt, "demi", 32, BLANC, a2, 680)


# ------------------------------------------------------------------ sens des hélices

def sens_helices(d, t, D, m, scene):
    a = apparition(t, 0.2, 0.7)
    c = (700, 560)
    positions = [(-1, -1, 1), (1, -1, -1), (1, 1, 1), (-1, 1, -1)]
    lacet = math.sin(max(0, t - _m(m, 2)) * 1.5) * 0.25 if t > _m(m, 2) else 0
    for k, (sx, sy, sens) in enumerate(positions):
        ang = lacet
        px, py = sx * 170, sy * 170
        x = c[0] + px * math.cos(ang) - py * math.sin(ang)
        y = c[1] + px * math.sin(ang) + py * math.cos(ang)
        dessiner(d, "helice", (x, y), 0.95, a, t * sens)
        couleur = CYAN if sens > 0 else AMBRE
        d.arc((x - 125, y - 125, x + 125, y + 125), -60, 30, fill=avec_alpha(couleur, a), width=5)
        bout = (x + 125 * math.cos(math.radians(30 if sens > 0 else -60)), y + 125 * math.sin(math.radians(30 if sens > 0 else -60)))
        cercle(d, bout, 10, couleur, a, plein=True)
    d.line([(c[0] - 170, c[1] - 170), (c[0] + 170, c[1] + 170)], fill=avec_alpha(GRIS, a), width=8)
    d.line([(c[0] + 170, c[1] - 170), (c[0] - 170, c[1] + 170)], fill=avec_alpha(GRIS, a), width=8)
    lignes = [("Deux hélices tournent dans le sens horaire", CYAN), ("Deux dans le sens antihoraire, en diagonale", AMBRE),
              ("Déséquilibrer les couples fait tourner le drone (lacet)", BLANC)]
    ts = instants(m, D, 3, scene["donnees"].get("apparitions"))
    for k, ((txt, couleur), debut) in enumerate(zip(lignes, ts)):
        a2 = apparition(t, debut, 0.5)
        paragraphe(d, (1150, 360 + k * 150), txt, "demi", 34, couleur, a2, 650)


# ------------------------------------------------------------------ transition vertical -> avion

def transition(d, t, D, m, scene):
    sens = scene["donnees"].get("sens", "aller")
    p = _progression(t, m, D, 0)
    if sens == "retour":
        p = 1 - p
    a = apparition(t, 0.1, 0.6)
    sol = 800
    d.line([(100, sol), (1820, sol)], fill=avec_alpha(GRIS, a), width=3)
    # phases : montée verticale (0-0.25), accélération (0.25-0.75), croisière (0.75-1)
    hauteur = 300 * sortie_cubique(min(1, p / 0.25))
    x = 260 + 820 * borne((p - 0.2) / 0.8) ** 1.5
    vitesse = 0 if p < 0.25 else min(19.0, 19 * (p - 0.25) / 0.5)
    vtol_profil(d, (x, sol - 40 - hauteur), 2.0, CYAN, a)
    part_rotors = 1.0 if vitesse < 13 else max(0.0, 1 - (vitesse - 13) / 3)
    if part_rotors > 0.02:
        for dx in (-35, 35):
            for k in range(3):
                yy = sol - 40 - hauteur + 20 + k * 22 + (t * 80) % 22
                d.line([(x + dx * 2.0 - 15, yy), (x + dx * 2.0 + 15, yy)],
                       fill=avec_alpha(CYAN_SOMBRE, a * part_rotors * 0.8), width=3)
    x0 = 1240
    panneau(d, (x0 - 30, 240, 1830, 560), a, CYAN_SOMBRE)
    _jauge(d, x0, 300, 540, vitesse, 25, "Vitesse air", "m/s", CYAN, a, [(13, "Q_ASSIST"), (15.4, "fin de transition")])
    _jauge(d, x0, 440, 540, part_rotors * 100, 100, "Poids porté par les moteurs verticaux", "%", AMBRE, a)
    etat = "VERTICAL" if vitesse < 1 else "TRANSITION" if part_rotors > 0.02 else "AVION"
    couleur = AMBRE if etat == "TRANSITION" else VERT if etat == "AVION" else CYAN
    texte(d, (x0 + 270, 525), f"Mode : {etat}", "gras", 28, couleur, a, "mm")


# ------------------------------------------------------------------ distribution électrique

def distribution(d, t, D, m, scene):
    a = apparition(t, 0.2, 0.6)
    dessiner(d, "batterie", (330, 330), 0.9, a, t)
    branches = [("4 ESC + moteurs VTOL", "22,2 V · jusqu'à 47 A", ROUGE), ("ESC + moteur de croisière", "22,2 V · ≈ 12 A", ROUGE),
                ("Contrôleur de vol", "module de puissance 5,3 V", CYAN), ("Servos", "BEC 5–6 V", AMBRE),
                ("Raspberry Pi 5 + AI HAT+", "BEC 5 V / 5 A", VERT), ("Nacelle et caméras", "BEC 12 V ou 5 V", CYAN)]
    ts = instants(m, D, len(branches), scene["donnees"].get("apparitions"))
    for k, ((nom, detail, couleur), debut) in enumerate(zip(branches, ts)):
        a2 = apparition(t, debut, 0.5)
        y = 270 + k * 100
        d.line([(520, 330), (700, 330), (700, y + 35), (900, y + 35)], fill=avec_alpha(couleur, a2 * 0.7), width=4)
        u = (t * 0.7 + k * 0.17) % 1
        pts = [(520, 330), (700, 330), (700, y + 35), (900, y + 35)]
        longueurs = [math.dist(pts[i], pts[i + 1]) for i in range(3)]
        s = u * sum(longueurs)
        for i in range(3):
            if s <= longueurs[i]:
                f = s / longueurs[i] if longueurs[i] else 0
                cercle(d, (pts[i][0] + (pts[i + 1][0] - pts[i][0]) * f, pts[i][1] + (pts[i + 1][1] - pts[i][1]) * f), 8,
                       couleur, a2, plein=True)
                break
            s -= longueurs[i]
        panneau(d, (910, y, 1780, y + 72), a2, couleur, rayon=12)
        texte(d, (940, y + 36), nom, "demi", 30, BLANC, a2, "lm")
        texte(d, (1750, y + 36), detail, "normal", 26, GRIS, a2, "rm")
    texte(d, (330, 470), "Batterie LiPo 6S", "demi", 28, BLANC, a, "mm")


# ------------------------------------------------------------------ fusion des capteurs (EKF)

def fusion(d, t, D, m, scene):
    capteurs = [("IMU", "rapide, dérive"), ("GPS", "précis, lent"), ("Baromètre", "altitude, sensible au vent"),
                ("Compas", "cap"), ("Vitesse air", "pour l'aile"), ("Télémètre", "distance au sol")]
    ts = instants(m, D, 3, scene["donnees"].get("apparitions"))
    a = apparition(t, ts[0], 0.5)
    for k, (nom, detail) in enumerate(capteurs):
        y = 270 + k * 100
        panneau(d, (120, y, 560, y + 78), a, CYAN_SOMBRE, rayon=12)
        texte(d, (150, y + 26), nom, "gras", 28, BLANC, a, "lm")
        texte(d, (150, y + 56), detail, "normal", 22, GRIS, a, "lm")
        pts = [(560 + i * 8, y + 39 + math.sin(t * 6 + i * 0.7 + k) * 10 * (1 if k in (0, 2) else 0.4)) for i in range(25)]
        d.line(pts, fill=avec_alpha(AMBRE, a * 0.8), width=2)
        fleche(d, (760, y + 39), (860, 560), CYAN_SOMBRE, a * 0.6, 3, 10)
    a2 = apparition(t, ts[1], 0.6)
    panneau(d, (870, 450, 1170, 670), a2, CYAN, epaisseur=4)
    texte(d, (1020, 530), "EKF", "titre", 64, BLANC, a2, "mm")
    texte(d, (1020, 600), "filtre de Kalman", "normal", 24, CYAN, a2, "mm")
    a3 = apparition(t, ts[2], 0.6)
    fleche(d, (1175, 560), (1290, 560), CYAN, a3, 5, 16)
    panneau(d, (1300, 400, 1800, 720), a3, VERT)
    for k, ligne in enumerate(["Position", "Vitesse", "Altitude", "Attitude", "Cap", "Alertes d'incohérence"]):
        texte(d, (1340, 445 + k * 48), ligne, "demi" if k < 5 else "normal", 28, BLANC if k < 5 else AMBRE, a3, "lm")
    pts = [(1560 + i * 9, 600 + math.sin(t * 2 + i * 0.3) * 3) for i in range(24)]
    d.line(pts, fill=avec_alpha(VERT, a3), width=3)


# ------------------------------------------------------------------ GNSS : trilatération

def gnss(d, t, D, m, scene):
    c = (760, 640)
    ts = instants(m, D, 3, scene["donnees"].get("apparitions"))
    sats = [(380, 280), (760, 230), (1150, 300), (560, 330)]
    for k, (sx, sy) in enumerate(sats):
        a = apparition(t, ts[0] + k * 0.4, 0.5)
        satellite(d, (sx, sy), 1.0, CYAN, a)
        r = math.dist((sx, sy), c)
        pulse = ((t - ts[0]) * 0.5 + k * 0.25) % 1
        d.arc((sx - r, sy - r, sx + r, sy + r), 40, 140, fill=avec_alpha(CYAN_SOMBRE, a * 0.7), width=2)
        rr = r * pulse
        d.arc((sx - rr, sy - rr, sx + rr, sy + rr), 40, 140, fill=avec_alpha(CYAN, a * (1 - pulse)), width=3)
    a2 = apparition(t, ts[1], 0.6)
    cercle(d, c, 16, AMBRE, a2, plein=True)
    cercle(d, c, 40 + 10 * math.sin(t * 3), AMBRE, a2 * 0.6, 3)
    texte(d, (c[0], c[1] + 70), "position calculée", "demi", 28, AMBRE, a2, "mm")
    a3 = apparition(t, ts[2], 0.6)
    panneau(d, (1300, 360, 1800, 760), a3, CYAN_SOMBRE)
    for k, (nom, couleur) in enumerate([("GPS (États-Unis)", CYAN), ("Galileo (Europe)", VERT), ("GLONASS (Russie)", AMBRE),
                                         ("BeiDou (Chine)", ROUGE)]):
        cercle(d, (1340, 420 + k * 70), 10, couleur, a3, plein=True)
        texte(d, (1365, 420 + k * 70), nom, "demi", 28, BLANC, a3, "lm")
    texte(d, (1550, 720), "plus de satellites = plus robuste", "normal", 24, GRIS, a3, "mm")


# ------------------------------------------------------------------ liaisons sécurisées

def liaisons(d, t, D, m, scene):
    a = apparition(t, 0.2, 0.6)
    vtol_profil(d, (360, 380), 2.2, CYAN, a)
    dessiner(d, "station", (1560, 440), 1.0, a, t)
    dessiner(d, "radiocommande", (1560, 760), 0.8, a, t)
    ts = instants(m, D, 4, scene["donnees"].get("apparitions"))
    a1 = apparition(t, ts[0], 0.5)
    ligne_pointillee(d, (470, 400), (1380, 440), CYAN, a1, 4, 16, 10, -t * 80)
    texte(d, (920, 380), "Télémétrie MAVLink · 433/868 MHz", "demi", 26, CYAN, a1, "mm")
    a2 = apparition(t, ts[1], 0.5)
    ligne_pointillee(d, (1440, 730), (470, 430), AMBRE, a2, 3, 10, 10, t * 80)
    texte(d, (900, 640), "Radiocommande de sécurité · 2,4 GHz", "demi", 26, AMBRE, a2, "mm")
    a3 = apparition(t, ts[2], 0.5)
    u = (t * 0.4) % 1
    px, py = 470 + 910 * u, 400 + 40 * u
    panneau(d, (px - 45, py - 70, px + 45, py - 10), a3, CYAN, rayon=8)
    cadenas(d, (px, py - 44), 0.55, CYAN, a3)
    texte(d, (920, 470), "chiffrement AES + signature MAVLink 2", "normal", 24, VERT, a3, "mm")
    a4 = apparition(t, ts[3], 0.5)
    if a4 > 0:
        cercle(d, (920, 220), 40, ROUGE, a4, 4)
        texte(d, (920, 220), "?", "gras", 44, ROUGE, a4, "mm")
        fleche(d, (880, 250), (520, 360), ROUGE, a4, 3, 14)
        croix(d, (700, 305), 60, ROUGE, a4)
        texte(d, (1000, 210), "faux ordre non signé : rejeté", "demi", 26, ROUGE, a4, "lm")


# ------------------------------------------------------------------ brouillage et leurrage

def brouillage(d, t, D, m, scene):
    ts = instants(m, D, 3, scene["donnees"].get("apparitions"))
    a = apparition(t, ts[0], 0.6)
    panneau(d, (120, HAUT, 930, BAS - 20), a, ROUGE)
    texte(d, (525, HAUT + 50), "BROUILLAGE", "titre", 44, ROUGE, a, "mm")
    for k in range(60):
        x = 170 + k * 12
        y = 470 + math.sin(t * 9 + k * 1.7) * 60 * math.sin(k * 0.3 + t)
        d.line([(x, 470), (x, y)], fill=avec_alpha(ROUGE, a * 0.6), width=4)
    paragraphe(d, (525, 620), "Un émetteur noie le signal sous du bruit. Détection : qualité du signal (RSSI), "
               "indicateur d'interférence du GNSS. Réaction : fail-safe de liaison.", "normal", 26, BLANC, a, 720, 1.3, "ma")
    a2 = apparition(t, ts[1], 0.6)
    panneau(d, (990, HAUT, 1800, BAS - 20), a2, AMBRE)
    texte(d, (1395, HAUT + 50), "LEURRAGE GPS", "titre", 44, AMBRE, a2, "mm")
    vraie, fausse = (1250, 470), (1250 + 300 * borne((t - ts[1]) / 4), 400)
    cercle(d, vraie, 14, VERT, a2, plein=True)
    texte(d, (vraie[0], vraie[1] + 40), "position estimée (IMU, baro, vitesse air)", "normal", 20, VERT, a2, "mm")
    cercle(d, fausse, 14, ROUGE, a2, plein=True)
    texte(d, (fausse[0], fausse[1] - 34), "GPS falsifié", "normal", 20, ROUGE, a2, "mm")
    a3 = apparition(t, ts[2], 0.6)
    ligne_pointillee(d, vraie, fausse, AMBRE, a3, 3)
    paragraphe(d, (1395, 620), "L'EKF détecte l'incohérence, rejette le GPS et alerte la station.", "normal", 26, BLANC, a3,
               720, 1.3, "ma")


# ------------------------------------------------------------------ barres de masse / énergie

def barres(d, t, D, m, scene):
    don = scene["donnees"]
    items = don["items"]
    vmax = don.get("max") or max(v for _, v, *_ in items)
    ts = instants(m, D, len(items), don.get("apparitions"))
    h = min(62, (BAS - HAUT - 40) / len(items))
    for k, (item, debut) in enumerate(zip(items, ts)):
        nom, valeur = item[0], item[1]
        couleur = item[2] if len(item) > 2 else CYAN
        a = apparition(t, debut, 0.4)
        y = HAUT + 10 + k * h
        p = sortie_cubique((t - debut) / 0.8)
        texte(d, (700, y + h / 2 - 4), nom, "moyen", 26, BLANC, a, "rm")
        d.rounded_rectangle((730, y + 8, 730 + 900 * valeur / vmax * p, y + h - 14), 6, fill=avec_alpha(couleur, a))
        texte(d, (745 + 900 * valeur / vmax * p, y + h / 2 - 4), don.get("format", "{:.2f}").format(valeur) + " " +
              don.get("unite", ""), "demi", 24, GRIS, a * p, "lm")
    if don.get("total"):
        a = apparition(t, ts[-1] + 1.0, 0.6)
        texte(d, (1800, BAS - 30), don["total"], "gras", 36, AMBRE, a, "rm")


ANIMATIONS = {f.__name__: f for f in [forces, axes, portance_aile, moteur_interne, sens_helices, transition, distribution,
                                       fusion, gnss, liaisons, brouillage, barres]}
