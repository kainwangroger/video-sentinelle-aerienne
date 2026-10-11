"""Pictogrammes des composants du drone, tous avec la signature f(d, centre, echelle, alpha, t)."""

import math

from gfx import (AMBRE, ASPHALTE, BLANC, CYAN, CYAN_SOMBRE, GRIS, PANNEAU, ROUGE, VERT, antenne, avec_alpha,
                 camera, cercle, debris, drone, personne, puce_electronique, stockage, texte, vehicule)
from visuels_projet import avion, batterie, bouclier, cadenas, satellite, vtol_dessus, vtol_profil


def _e(s, base=3):
    return max(2, int(base * s))


def p_vtol(d, c, s, a, t):
    vtol_dessus(d, c, 0.55 * s, CYAN, a, t)


def p_vtol_profil(d, c, s, a, t):
    vtol_profil(d, c, 1.6 * s, CYAN, a)


def p_quad(d, c, s, a, t):
    drone(d, c, 1.1 * s, GRIS, a, t)


def p_avion(d, c, s, a, t):
    avion(d, c, 1.0 * s, GRIS, a)


def p_moteur(d, c, s, a, t):
    """Moteur sans balais vu de côté : cloche tournante, stator, axe."""
    x, y = c
    col = avec_alpha(CYAN, a)
    d.rounded_rectangle((x - 60 * s, y - 40 * s, x + 60 * s, y + 40 * s), int(10 * s), fill=avec_alpha(PANNEAU, a),
                        outline=col, width=_e(s, 4))
    for k in range(6):  # stries de la cloche qui défilent
        u = ((t * 2 + k / 6) % 1)
        xx = x - 55 * s + 110 * s * u
        d.line([(xx, y - 36 * s), (xx, y + 36 * s)], fill=avec_alpha(CYAN_SOMBRE, a * 0.8), width=_e(s, 3))
    d.rectangle((x - 70 * s, y + 40 * s, x + 70 * s, y + 52 * s), fill=col)
    d.rectangle((x - 6 * s, y - 75 * s, x + 6 * s, y - 40 * s), fill=avec_alpha(BLANC, a))


def p_helice(d, c, s, a, t, sens=1):
    x, y = c
    ang = sens * t * 10
    for k in range(2):
        b = ang + k * math.pi
        bx, by = math.cos(b), math.sin(b)
        nx, ny = -by, bx
        pts = [(x + nx * 6 * s, y + ny * 6 * s), (x + bx * 90 * s + nx * 12 * s, y + by * 90 * s + ny * 12 * s),
               (x + bx * 100 * s, y + by * 100 * s), (x + bx * 90 * s - nx * 6 * s, y + by * 90 * s - ny * 6 * s),
               (x - nx * 6 * s, y - ny * 6 * s)]
        d.polygon(pts, fill=avec_alpha(BLANC, a * 0.85))
    cercle(d, c, 12 * s, CYAN, a, plein=True)
    cercle(d, c, 105 * s, CYAN_SOMBRE, a * 0.35, 2)


def p_esc(d, c, s, a, t):
    x, y = c
    d.rounded_rectangle((x - 70 * s, y - 35 * s, x + 70 * s, y + 35 * s), int(8 * s), fill=avec_alpha((20, 60, 90), a),
                        outline=avec_alpha(CYAN, a), width=_e(s))
    texte(d, (x, y), "ESC", "gras", int(30 * s), BLANC, a, "mm")
    for k, couleur in enumerate([ROUGE, (30, 30, 30)]):  # fils batterie
        d.line([(x - 70 * s, y - 12 * s + 24 * s * k), (x - 110 * s, y - 12 * s + 24 * s * k)],
               fill=avec_alpha(couleur if couleur != (30, 30, 30) else GRIS, a), width=_e(s, 5))
    for k in range(3):  # trois phases vers le moteur
        d.line([(x + 70 * s, y - 18 * s + 18 * s * k), (x + 110 * s, y - 18 * s + 18 * s * k)],
               fill=avec_alpha(AMBRE, a), width=_e(s, 4))


def p_servo(d, c, s, a, t):
    x, y = c
    d.rounded_rectangle((x - 50 * s, y - 25 * s, x + 50 * s, y + 25 * s), int(6 * s), fill=avec_alpha(PANNEAU, a),
                        outline=avec_alpha(CYAN, a), width=_e(s))
    d.rectangle((x - 70 * s, y - 6 * s, x + 70 * s, y + 6 * s), outline=avec_alpha(CYAN_SOMBRE, a), width=_e(s, 2))
    ang = math.sin(t * 2) * 0.6
    cercle(d, (x + 25 * s, y - 25 * s), 8 * s, BLANC, a, plein=True)
    d.line([(x + 25 * s, y - 25 * s), (x + 25 * s + 45 * s * math.sin(ang), y - 25 * s - 45 * s * math.cos(ang))],
           fill=avec_alpha(BLANC, a), width=_e(s, 5))


def p_batterie(d, c, s, a, t):
    x, y = c
    for k in range(6):
        xx = x - 150 * s + k * 50 * s
        d.rounded_rectangle((xx, y - 45 * s, xx + 42 * s, y + 45 * s), int(5 * s), fill=avec_alpha((30, 70, 60), a),
                            outline=avec_alpha(VERT, a), width=_e(s, 2))
        texte(d, (xx + 21 * s, y), "3,7V", "demi", int(14 * s), BLANC, a, "mm")
    texte(d, (x, y + 70 * s), "6S = 22,2 V", "gras", int(26 * s), VERT, a, "mm")


def p_batterie_icone(d, c, s, a, t):
    batterie(d, c, 1.4 * s, 0.75, VERT, a)


def p_controleur(d, c, s, a, t):
    x, y = c
    d.rounded_rectangle((x - 90 * s, y - 60 * s, x + 90 * s, y + 60 * s), int(14 * s), fill=avec_alpha((15, 45, 80), a),
                        outline=avec_alpha(CYAN, a), width=_e(s, 4))
    texte(d, (x, y - 10 * s), "FC", "titre", int(44 * s), BLANC, a, "mm")
    texte(d, (x, y + 32 * s), "ArduPilot", "normal", int(18 * s), CYAN, a, "mm")
    for k in range(5):
        d.line([(x - 60 * s + k * 30 * s, y + 60 * s), (x - 60 * s + k * 30 * s, y + 75 * s)],
               fill=avec_alpha(GRIS, a), width=_e(s, 3))
    cercle(d, (x + 70 * s, y - 42 * s), 6 * s, VERT if (t * 2) % 1 < 0.5 else CYAN_SOMBRE, a, plein=True)


def p_gnss(d, c, s, a, t):
    x, y = c
    d.line([(x, y + 20 * s), (x, y + 90 * s)], fill=avec_alpha(GRIS, a), width=_e(s, 6))
    cercle(d, (x, y), 48 * s, CYAN, a, _e(s, 4))
    cercle(d, (x, y), 36 * s, (15, 45, 80), a, plein=True)
    texte(d, (x, y), "GNSS", "gras", int(20 * s), BLANC, a, "mm")
    for k in range(3):
        satellite(d, (x - 120 * s + k * 120 * s, y - 120 * s - 20 * s * (k % 2)), 0.6 * s, CYAN_SOMBRE, a)
        d.line([(x - 120 * s + k * 120 * s, y - 108 * s - 20 * s * (k % 2)), (x, y - 50 * s)],
               fill=avec_alpha(CYAN_SOMBRE, a * 0.5), width=1)


def p_pitot(d, c, s, a, t):
    x, y = c
    d.rectangle((x - 120 * s, y - 6 * s, x + 60 * s, y + 6 * s), fill=avec_alpha(BLANC, a))
    d.polygon([(x - 120 * s, y - 6 * s), (x - 140 * s, y), (x - 120 * s, y + 6 * s)], fill=avec_alpha(BLANC, a))
    d.rounded_rectangle((x + 60 * s, y - 30 * s, x + 130 * s, y + 30 * s), int(6 * s), fill=avec_alpha(PANNEAU, a),
                        outline=avec_alpha(CYAN, a), width=_e(s))
    for k in range(4):
        u = (t * 1.5 + k / 4) % 1
        xx = x - 330 * s + 180 * s * u
        d.line([(xx, y - 30 * s + k * 20 * s), (xx + 40 * s, y - 30 * s + k * 20 * s)],
               fill=avec_alpha(CYAN_SOMBRE, a * (1 - u)), width=_e(s, 2))


def p_lidar(d, c, s, a, t):
    x, y = c
    d.rounded_rectangle((x - 40 * s, y - 25 * s, x + 40 * s, y + 25 * s), int(6 * s), fill=avec_alpha(PANNEAU, a),
                        outline=avec_alpha(CYAN, a), width=_e(s))
    u = (t * 1.2) % 1
    d.line([(x, y + 25 * s), (x, y + 25 * s + 140 * s * u)], fill=avec_alpha(ROUGE, a * (1 - u * 0.5)), width=_e(s, 3))
    d.line([(x - 120 * s, y + 175 * s), (x + 120 * s, y + 175 * s)], fill=avec_alpha(GRIS, a), width=_e(s, 3))


def p_imu(d, c, s, a, t):
    x, y = c
    puce_electronique(d, (x, y), 1.0 * s, CYAN, a)
    for k, (dx, dy, nom) in enumerate([(1, 0, "X"), (0, -1, "Z"), (-0.7, 0.7, "Y")]):
        d.line([(x, y), (x + dx * 110 * s, y + dy * 110 * s)], fill=avec_alpha([ROUGE, VERT, AMBRE][k], a), width=_e(s, 4))
        texte(d, (x + dx * 130 * s, y + dy * 130 * s), nom, "gras", int(24 * s), [ROUGE, VERT, AMBRE][k], a, "mm")


def p_barometre(d, c, s, a, t):
    x, y = c
    cercle(d, (x, y), 60 * s, CYAN, a, _e(s, 4))
    ang = -math.pi * 0.75 + math.pi * 1.5 * (0.5 + 0.3 * math.sin(t * 0.8))
    d.line([(x, y), (x + 45 * s * math.cos(ang), y + 45 * s * math.sin(ang))], fill=avec_alpha(AMBRE, a), width=_e(s, 4))
    texte(d, (x, y + 30 * s), "hPa", "demi", int(18 * s), GRIS, a, "mm")


def p_compas(d, c, s, a, t):
    x, y = c
    cercle(d, (x, y), 60 * s, CYAN, a, _e(s, 4))
    ang = math.sin(t * 0.6) * 0.3 - math.pi / 2
    pts = [(x + 50 * s * math.cos(ang), y + 50 * s * math.sin(ang)),
           (x + 10 * s * math.cos(ang + math.pi / 2), y + 10 * s * math.sin(ang + math.pi / 2)),
           (x + 10 * s * math.cos(ang - math.pi / 2), y + 10 * s * math.sin(ang - math.pi / 2))]
    d.polygon(pts, fill=avec_alpha(ROUGE, a))
    texte(d, (x, y - 80 * s), "N", "gras", int(24 * s), BLANC, a, "mm")


def p_radio(d, c, s, a, t):
    x, y = c
    d.rounded_rectangle((x - 60 * s, y - 30 * s, x + 60 * s, y + 30 * s), int(8 * s), fill=avec_alpha(PANNEAU, a),
                        outline=avec_alpha(CYAN, a), width=_e(s))
    antenne(d, (x + 40 * s, y - 60 * s), 0.8 * s, CYAN, a)
    texte(d, (x - 10 * s, y), "433/868", "demi", int(16 * s), BLANC, a, "mm")


def p_radiocommande(d, c, s, a, t):
    x, y = c
    d.rounded_rectangle((x - 110 * s, y - 60 * s, x + 110 * s, y + 60 * s), int(30 * s), fill=avec_alpha(PANNEAU, a),
                        outline=avec_alpha(CYAN, a), width=_e(s, 4))
    for dx in (-55, 55):
        cercle(d, (x + dx * s, y), 28 * s, GRIS, a, _e(s))
        ox, oy = 12 * math.sin(t * 1.3 + dx), 12 * math.cos(t * 1.1 + dx)
        d.line([(x + dx * s, y), (x + (dx + ox) * s, y + oy * s)], fill=avec_alpha(BLANC, a), width=_e(s, 5))
    d.line([(x + 80 * s, y - 60 * s), (x + 100 * s, y - 120 * s)], fill=avec_alpha(GRIS, a), width=_e(s, 5))
    d.rectangle((x - 105 * s, y - 75 * s, x - 85 * s, y - 60 * s), fill=avec_alpha(ROUGE, a))


def p_ordinateur(d, c, s, a, t):
    x, y = c
    d.rounded_rectangle((x - 110 * s, y - 75 * s, x + 110 * s, y + 55 * s), int(8 * s), fill=avec_alpha((15, 40, 70), a),
                        outline=avec_alpha(CYAN, a), width=_e(s, 4))
    d.polygon([(x - 140 * s, y + 65 * s), (x + 140 * s, y + 65 * s), (x + 120 * s, y + 55 * s), (x - 120 * s, y + 55 * s)],
              fill=avec_alpha(GRIS, a))
    d.line([(x - 80 * s, y + 20 * s), (x - 30 * s, y - 20 * s), (x + 20 * s, y), (x + 80 * s, y - 40 * s)],
           fill=avec_alpha(AMBRE, a), width=_e(s, 3))


def p_nacelle(d, c, s, a, t):
    x, y = c
    osc = 0.25 * math.sin(t * 1.6)
    d.line([(x, y - 110 * s), (x, y - 70 * s)], fill=avec_alpha(GRIS, a), width=_e(s, 8))
    d.arc((x - 100 * s, y - 100 * s, x + 100 * s, y + 100 * s), 200 + math.degrees(osc), 340 + math.degrees(osc),
          fill=avec_alpha(GRIS, a), width=_e(s, 8))
    cercle(d, (x, y), 75 * s, CYAN, a, _e(s, 4))
    camera(d, (x + 5 * s, y), 1.2 * s, CYAN, a)


def p_raspberry(d, c, s, a, t):
    x, y = c
    d.rounded_rectangle((x - 110 * s, y - 70 * s, x + 110 * s, y + 70 * s), int(10 * s), fill=avec_alpha((20, 70, 50), a),
                        outline=avec_alpha(VERT, a), width=_e(s, 3))
    puce_electronique(d, (x - 30 * s, y), 0.9 * s, VERT, a)
    d.rounded_rectangle((x + 30 * s, y - 50 * s, x + 95 * s, y + 50 * s), int(6 * s), fill=avec_alpha(PANNEAU, a),
                        outline=avec_alpha(CYAN, a), width=_e(s, 2))
    texte(d, (x + 62 * s, y), "HAT+", "gras", int(16 * s), CYAN, a, "mm")


def p_cellule(d, c, s, a, t):
    vtol_dessus(d, c, 0.55 * s, CYAN, a, t, rotors=False, helice=False)


def p_bouclier(d, c, s, a, t):
    bouclier(d, c, 1.6 * s, VERT, a)


def p_cadenas(d, c, s, a, t):
    cadenas(d, c, 1.6 * s, CYAN, a)


def p_avertissement(d, c, s, a, t):
    x, y = c
    d.polygon([(x, y - 80 * s), (x + 90 * s, y + 70 * s), (x - 90 * s, y + 70 * s)], outline=avec_alpha(AMBRE, a),
              width=_e(s, 6))
    texte(d, (x, y + 15 * s), "!", "gras", int(80 * s), AMBRE, a, "mm")


def p_outil(d, c, s, a, t):
    x, y = c
    d.line([(x - 70 * s, y + 70 * s), (x + 40 * s, y - 40 * s)], fill=avec_alpha(GRIS, a), width=_e(s, 16))
    cercle(d, (x + 55 * s, y - 55 * s), 35 * s, GRIS, a, _e(s, 12))
    d.polygon([(x + 55 * s, y - 55 * s), (x + 100 * s, y - 70 * s), (x + 70 * s, y - 100 * s)], fill=avec_alpha(PANNEAU, 1))


def p_document(d, c, s, a, t):
    x, y = c
    d.rounded_rectangle((x - 70 * s, y - 95 * s, x + 70 * s, y + 95 * s), int(8 * s), fill=avec_alpha(PANNEAU, a),
                        outline=avec_alpha(CYAN, a), width=_e(s, 3))
    for k in range(6):
        d.line([(x - 45 * s, y - 60 * s + k * 26 * s), (x + 45 * s - (k % 3) * 15 * s, y - 60 * s + k * 26 * s)],
               fill=avec_alpha(GRIS, a), width=_e(s, 3))


def p_terrain(d, c, s, a, t):
    x, y = c
    d.rectangle((x - 160 * s, y - 100 * s, x + 160 * s, y + 100 * s), fill=avec_alpha((40, 80, 55), a))
    d.rectangle((x - 40 * s, y - 100 * s, x + 40 * s, y + 100 * s), fill=avec_alpha(ASPHALTE, a))
    for k in range(5):
        d.line([(x, y - 90 * s + k * 40 * s), (x, y - 75 * s + k * 40 * s)], fill=avec_alpha(BLANC, a), width=_e(s, 3))


def p_personne(d, c, s, a, t):
    personne(d, c, 1.6 * s, BLANC, a)


def p_vehicule(d, c, s, a, t):
    vehicule(d, c, 1.6 * s, BLANC, a)


def p_debris(d, c, s, a, t):
    debris(d, c, 2.2 * s, BLANC, a)


def p_stockage(d, c, s, a, t):
    stockage(d, c, 1.5 * s, CYAN, a)


def p_station(d, c, s, a, t):
    p_ordinateur(d, (c[0] + 30 * s, c[1]), 0.8 * s, a, t)
    antenne(d, (c[0] - 120 * s, c[1] - 20 * s), 1.0 * s, CYAN, a)


PICTOS = {nom[2:]: f for nom, f in globals().items() if nom.startswith("p_") and callable(f)}


def dessiner(d, nom, c, s=1.0, a=1.0, t=0.0):
    if nom:
        PICTOS[nom](d, c, s, a, t)


__all__ = ["PICTOS", "dessiner"]
