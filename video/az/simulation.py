"""Simulation animée d'une mission complète du SA-1 (carte + instruments + IA).

Une mission continue est décrite par des images clés en temps de mission (minutes).
Chaque scène de simulation couvre une phase : le temps de mission avance linéairement
pendant la scène, ce qui garde la continuité d'une scène à l'autre.
Toutes les valeurs affichées sont SIMULÉES (cohérentes avec le dimensionnement).
"""

import math

from gfx import (AMBRE, ASPHALTE, BLANC, CYAN, CYAN_SOMBRE, GRIS, PANNEAU, ROUGE, VERT, apparition, avec_alpha, borne,
                 cercle, coche, debris, ligne_pointillee, panneau, rectangle_pointille, texte)

CARTE = (110, 240, 1150, 900)
HOME = (330, 800)

# phases : (début, fin) en minutes de mission
PHASES = {
    "preparation": (-4.0, 0.0),
    "decollage": (0.0, 0.8),
    "transition": (0.8, 1.6),
    "croisiere": (1.6, 12.0),
    "detection": (12.0, 18.0),
    "perte_liaison": (18.0, 24.0),
    "retour": (24.0, 33.0),
    "atterrissage": (33.0, 35.0),
    "apres_vol": (35.0, 36.0),
}

# trajectoire : (minute, x, y) — balayage en allers-retours le long de la piste
ROUTE = [(0.0, *HOME), (1.6, 330, 640), (3.5, 560, 300), (6.0, 560, 840), (7.0, 640, 840), (9.5, 640, 300),
         (10.5, 720, 300), (13.0, 720, 840), (14.0, 800, 840), (16.5, 800, 300), (17.5, 880, 300), (20.0, 880, 840),
         (21.0, 960, 840), (23.5, 960, 300), (24.0, 960, 280), (31.0, 380, 700), (33.0, *HOME), (36.0, *HOME)]
DETECTION = (720, 560)       # débris repéré pendant la phase de détection
MINUTE_DETECTION = 13.4
ALERTES = [(8.2, "personne", "classe_confirmee", "Personne près du taxiway"),
           (MINUTE_DETECTION, "débris", "classe_confirmee", "Débris sur la piste"),
           (19.5, "objet", "a_verifier", "Objet à vérifier, bord de piste"),
           (22.1, "véhicule", "classe_confirmee", "Véhicule de service")]
PERTE_LIAISON = (19.0, 22.6)


def position(minute):
    if minute <= ROUTE[0][0]:
        return ROUTE[0][1:], 0.0
    for (t0, x0, y0), (t1, x1, y1) in zip(ROUTE, ROUTE[1:]):
        if t0 <= minute <= t1:
            f = (minute - t0) / (t1 - t0) if t1 > t0 else 0
            return (x0 + (x1 - x0) * f, y0 + (y1 - y0) * f), math.atan2(y1 - y0, x1 - x0)
    return ROUTE[-1][1:], 0.0


def etat(minute):
    """Valeurs simulées des instruments à un instant de la mission."""
    e = {"minute": minute, "arme": 0.0 <= minute < 35.0}
    if minute < 0:
        e.update(mode="QLOITER (désarmé)", alt=0, va=0, vs=0)
    elif minute < 0.8:
        e.update(mode="AUTO · décollage vertical", alt=40 * minute / 0.8, va=0, vs=0)
    elif minute < 1.6:
        f = (minute - 0.8) / 0.8
        e.update(mode="AUTO · transition", alt=40 + 20 * f, va=19 * f, vs=19 * f)
    elif minute < 24.0:
        e.update(mode="AUTO · mission", alt=60, va=19 + math.sin(minute * 3) * 0.6, vs=17 + math.sin(minute * 2) * 2)
    elif minute < 33.0:
        e.update(mode="RTL · retour", alt=60, va=19, vs=21)
    elif minute < 35.0:
        f = (minute - 33.0) / 2.0
        e.update(mode="QLAND · atterrissage vertical" if f > 0.25 else "RTL · retour en vertical",
                 alt=60 * (1 - f), va=max(0, 19 * (1 - f * 4)), vs=max(0, 19 * (1 - f * 4)))
    else:
        e.update(mode="Désarmé", alt=0, va=0, vs=0)
    # batterie : 100 % au décollage, ≈ 1 %/min en croisière, plus en stationnaire
    if minute <= 0:
        conso = 0
    else:
        stationnaire = min(minute, 1.6) + max(0, min(minute, 35) - 33)
        conso = stationnaire * 4.9 + max(0, min(minute, 33) - 1.6) * 1.32
    e["batterie"] = max(0, 100 - conso)
    e["tension"] = 25.1 - (25.1 - 21.6) * (100 - e["batterie"]) / 100
    e["courant"] = 0 if not e["arme"] else (47 if (minute < 1.6 or minute > 33.4) else 12.6)
    e["sats"] = 17
    e["liaison"] = not (PERTE_LIAISON[0] <= minute < PERTE_LIAISON[1])
    emises = [al for al in ALERTES if al[0] <= minute]
    e["alertes"] = emises
    e["en_attente"] = [al for al in emises if PERTE_LIAISON[0] <= al[0] and minute < PERTE_LIAISON[1]]
    e["recues"] = [al for al in emises if al not in e["en_attente"]]
    return e


# ------------------------------------------------------------------ dessin de la carte

def _carte(d, minute, a):
    x0, y0, x1, y1 = CARTE
    d.rectangle(CARTE, fill=avec_alpha((34, 70, 48), a))
    for k in range(0, x1 - x0, 80):
        d.line([(x0 + k, y0), (x0 + k, y1)], fill=avec_alpha((44, 84, 58), a), width=1)
    d.rectangle((640, y0 + 20, 760, y1 - 20), fill=avec_alpha(ASPHALTE, a))  # piste
    for y in range(y0 + 40, y1 - 40, 60):
        d.line([(700, y), (700, y + 30)], fill=avec_alpha(BLANC, a * 0.8), width=4)
    d.rectangle((800, 420, 830, 700), fill=avec_alpha((70, 76, 86), a))  # taxiway
    d.rectangle((830, 520, 1000, 640), fill=avec_alpha((80, 86, 96), a))  # aire de stationnement
    for bx, by in [(1030, 500), (1030, 600), (1080, 700)]:
        d.rectangle((bx, by, bx + 60, by + 70), fill=avec_alpha((110, 110, 120), a))
    texte(d, (700, y0 + 6), "PISTE", "gras", 18, BLANC, a * 0.7, "ma")
    # géorepérage (polygone autorisé)
    rectangle_pointille(d, (x0 + 30, y0 + 22, x1 - 30, y1 - 30), ROUGE, a * 0.7, 2)
    texte(d, (x1 - 40, y0 + 40), "géorepérage", "normal", 18, ROUGE, a * 0.9, "rm")
    # plan de vol
    for (_, xa, ya), (_, xb, yb) in zip(ROUTE, ROUTE[1:]):
        ligne_pointillee(d, (xa, ya), (xb, yb), CYAN_SOMBRE, a * 0.8, 2, 8, 8)
    # point de départ
    cercle(d, HOME, 18, AMBRE, a, 3)
    texte(d, HOME, "H", "gras", 20, AMBRE, a, "mm")
    # trace parcourue
    if minute > 0:
        pts = [position(minute * k / 60)[0] for k in range(61)]
        d.line(pts, fill=avec_alpha(CYAN, a), width=3)
    if minute >= MINUTE_DETECTION:
        cercle(d, DETECTION, 14, AMBRE, a, plein=True)
        cercle(d, DETECTION, 26 + 6 * math.sin(minute * 20), AMBRE, a * 0.6, 3)
    (x, y), cap = position(minute)
    # drone : flèche orientée
    pts = [(x + 18 * math.cos(cap), y + 18 * math.sin(cap)), (x + 12 * math.cos(cap + 2.5), y + 12 * math.sin(cap + 2.5)),
           (x + 12 * math.cos(cap - 2.5), y + 12 * math.sin(cap - 2.5))]
    d.polygon(pts, fill=avec_alpha(BLANC, a), outline=avec_alpha(CYAN, a))
    if 12.0 <= minute < 24.0:  # empreinte de la caméra
        d.ellipse((x - 46, y - 46, x + 46, y + 46), outline=avec_alpha(CYAN, a * 0.5), width=2)
    d.rectangle(CARTE, outline=avec_alpha(CYAN_SOMBRE, a), width=2)
    texte(d, (x0 + 14, y1 - 18), "Simulation — valeurs illustratives", "normal", 18, GRIS, a, "lm")


# ------------------------------------------------------------------ instruments

def _instruments(d, e, a):
    x0, y0 = 1190, 240
    panneau(d, (x0, y0, 1810, 640), a, CYAN_SOMBRE, rayon=14)
    texte(d, (x0 + 24, y0 + 30), e["mode"], "gras", 28, AMBRE if "RTL" in e["mode"] or "QLAND" in e["mode"] else CYAN,
          a, "lm")
    minute = e["minute"]
    texte(d, (1786, y0 + 30), f"T+{int(max(0, minute)):02d}:{int(max(0, minute) % 1 * 60):02d}", "demi", 24, GRIS, a, "rm")
    valeurs = [("Altitude", f"{e['alt']:.0f} m"), ("Vitesse air", f"{e['va']:.1f} m/s"), ("Vitesse sol", f"{e['vs']:.1f} m/s"),
               ("Batterie", f"{e['batterie']:.0f} %  ·  {e['tension']:.1f} V"), ("Courant", f"{e['courant']:.1f} A"),
               ("GNSS", f"{e['sats']} satellites · 3D fix")]
    for k, (cle, val) in enumerate(valeurs):
        y = y0 + 72 + k * 38
        texte(d, (x0 + 24, y), cle, "normal", 24, GRIS, a, "lm")
        couleur = AMBRE if cle == "Batterie" and e["batterie"] < 35 else BLANC
        texte(d, (1786, y), val, "demi", 26, couleur, a, "rm")
    y = y0 + 72 + 6 * 38
    texte(d, (x0 + 24, y), "Télémétrie", "normal", 24, GRIS, a, "lm")
    texte(d, (1786, y), "chiffrée · signée" if e["liaison"] else "PERDUE", "gras", 26, VERT if e["liaison"] else ROUGE, a, "rm")
    y += 38
    texte(d, (x0 + 24, y), "IA embarquée", "normal", 24, GRIS, a, "lm")
    attente = f" · {len(e['en_attente'])} en attente" if e["en_attente"] else ""
    texte(d, (1786, y), f"{len(e['alertes'])} alertes{attente}", "demi", 26, AMBRE if e["en_attente"] else BLANC, a, "rm")
    # barre de batterie
    d.rounded_rectangle((x0 + 24, 616, 1786, 630), 6, fill=avec_alpha(PANNEAU, a))
    d.rounded_rectangle((x0 + 24, 616, x0 + 24 + (1786 - x0 - 24) * e["batterie"] / 100, 630), 6,
                        fill=avec_alpha(VERT if e["batterie"] > 35 else AMBRE, a))


def _alertes_station(d, e, a, minute):
    x0, y0 = 1190, 660
    panneau(d, (x0, y0, 1810, 900), a, CYAN_SOMBRE, rayon=14)
    texte(d, (x0 + 24, y0 + 28), "STATION SOL · ALERTES REÇUES", "gras", 22, CYAN, a, "lm")
    recues = e["recues"][-3:]
    if not recues:
        texte(d, (x0 + 24, y0 + 80), "aucune alerte", "normal", 24, GRIS, a, "lm")
    for k, (m0, classe, statut, libelle) in enumerate(reversed(recues)):
        y = y0 + 72 + k * 56
        couleur = AMBRE if statut == "a_verifier" else VERT
        cercle(d, (x0 + 34, y + 4), 8, couleur, a, plein=True)
        texte(d, (x0 + 54, y + 4), libelle, "demi", 24, BLANC, a, "lm")
        texte(d, (1786, y + 4), f"T+{int(m0):02d}:{int(m0 % 1 * 60):02d}", "normal", 22, GRIS, a, "rm")


def _vue_camera(d, minute, a):
    """Incrustation de la vue caméra au moment de la détection."""
    x0, y0, x1, y1 = 140, 270, 520, 520
    panneau(d, (x0 - 6, y0 - 6, x1 + 6, y1 + 6), a, CYAN, rayon=8, opacite_fond=1)
    d.rectangle((x0, y0, x1, y1), fill=avec_alpha((40, 46, 54), a))
    for k in range(5):
        yy = y0 + ((k * 60 + minute * 400) % 260)
        if yy < y1 - 30:
            d.line([(330, yy), (330, yy + 30)], fill=avec_alpha(BLANC, a * 0.8), width=6)
    dy = (minute - MINUTE_DETECTION) * 300
    cx, cy = 280, 330 + dy
    if y0 + 20 < cy < y1 - 20:
        debris(d, (cx, cy), 1.4, (200, 205, 215), a)
        rectangle_pointille(d, (cx - 30, cy - 26, cx + 34, cy + 26), AMBRE, a, 3, minute * 200)
        texte(d, (cx - 30, cy - 40), "débris 0,81", "gras", 18, AMBRE, a, "lm")
    texte(d, (x0 + 8, y1 - 14), "Caméra + IA à bord", "demi", 18, CYAN, a, "lm")


def simulation(d, t, D, m, scene):
    phase = scene["donnees"]["phase"]
    debut, fin = PHASES[phase]
    u = borne((t - 0.4) / max(1.0, D - 1.2))
    minute = debut + (fin - debut) * u
    a = apparition(t, 0.0, 0.6)
    _carte(d, minute, a)
    e = etat(minute)
    _instruments(d, e, a)
    _alertes_station(d, e, a, minute)
    if phase == "detection" and MINUTE_DETECTION - 0.3 <= minute <= MINUTE_DETECTION + 1.2:
        _vue_camera(d, minute, apparition(t, 0.3, 0.5))
    if phase == "preparation":
        controles = ["GNSS : 17 satellites", "Batterie 25,1 V", "Compas cohérent", "Liaison chiffrée et signée",
                     "Fail-safes vérifiés", "IA : message de test reçu"]
        for k, ctl in enumerate(controles):
            a2 = apparition(t, 1.0 + k * (D - 3) / len(controles), 0.4)
            y = 290 + k * 46
            d.rounded_rectangle((140, y - 18, 560, y + 18), 8, fill=avec_alpha(PANNEAU, a2 * 0.9))
            coche(d, (165, y), 22, VERT, a2)
            texte(d, (190, y), ctl, "demi", 22, BLANC, a2, "lm")
    if phase == "perte_liaison" and not e["liaison"]:
        d.rounded_rectangle((300, 260, 980, 320), 10, fill=avec_alpha((90, 20, 20), a * 0.9))
        texte(d, (640, 290), "Liaison perdue : mission poursuivie, alertes stockées à bord", "demi", 22, BLANC, a, "mm")
    if phase == "apres_vol":
        lignes = ["Durée de vol : 35 min", "Distance parcourue : ≈ 35 km", "Batterie restante : 41 %",
                  "4 alertes, toutes reçues", "Journaux téléchargés"]
        panneau(d, (300, 420, 960, 760), a, VERT)
        for k, ligne in enumerate(lignes):
            texte(d, (340, 470 + k * 56), ligne, "demi", 30, BLANC, apparition(t, 0.5 + k * 0.6, 0.4), "lm")


SIMULATION = {"simulation": simulation}
