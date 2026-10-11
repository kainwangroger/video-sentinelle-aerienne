"""Animation de chaque scène.

Chaque fonction reçoit :
  d : ImageDraw en mode RGBA sur l'image de la frame
  t : temps écoulé dans la scène (s)
  D : durée de la scène (s)
  m : instants de début de chaque phrase de narration (s, relatifs à la scène)
Les éléments apparaissent au moment où la voix off en parle.
"""

import math

from gfx import (AMBRE, ASPHALTE, BLANC, CYAN, CYAN_SOMBRE, GRIS, PANNEAU, ROUGE, VERT, W,
                 antenne, apparition, avec_alpha, borne, camera, cercle, coche, croix, debris, drone,
                 epingle, fleche, ligne_pointillee, melange, nuage, panneau, paragraphe, personne,
                 piste_perspective, point_sur_piste, puce_electronique, puce_numero, rectangle_pointille,
                 sortie_cubique, stockage, texte, vehicule)

HAUT_CONTENU = 250


def _m(m, i, decalage=0.0):
    """Instant de la phrase i (ou de la dernière si i dépasse)."""
    return m[min(i, len(m) - 1)] + decalage


def _glisse(a, distance=30):
    return (1 - a) * distance


# ------------------------------------------------------------------ 1. titre

def titre(d, t, D, m):
    c = (W // 2, 330)
    for k in range(3):
        phase = (t * 0.45 + k / 3) % 1
        cercle(d, c, 90 + phase * 260, CYAN, 0.45 * (1 - phase) * apparition(t, 0.1, 1.0), 2)
    a = apparition(t, 0.0, 0.9)
    drone(d, (c[0], c[1] + _glisse(a, 40)), 1.25, CYAN, a, t)

    a = apparition(t, 0.35, 0.8)
    texte(d, (W // 2, 590 + _glisse(a)), "SENTINELLE AÉRIENNE", "titre", 118, BLANC, a, "mm")
    a = apparition(t, 0.9, 0.8)
    texte(d, (W // 2, 690 + _glisse(a, 20)), "Module d'intelligence artificielle embarquée", "moyen", 46, CYAN, a, "mm")
    largeur_trait = 520 * apparition(t, 1.2, 1.0)
    d.line([(W // 2 - largeur_trait / 2, 752), (W // 2 + largeur_trait / 2, 752)], fill=avec_alpha(CYAN_SOMBRE, 1), width=2)

    a = apparition(t, _m(m, 1), 0.7)
    texte(d, (W // 2, 800), "SkyVision Togo  ·  CECFD 2026 — ANAC", "demi", 34, BLANC, a, "mm")
    texte(d, (W // 2, 850), "Responsable du lot IA : KAINWANG Roger", "normal", 30, GRIS, a, "mm")


# ------------------------------------------------------------------ 2. mission

def mission(d, t, D, m):
    boite = (980, 300, 1800, 900)
    a = apparition(t, 0.2, 0.8)
    piste_perspective(d, boite, a, t * 0.6)

    objets = [(debris, -0.35, 0.55, "Débris", ROUGE), (personne, 0.45, 0.35, "Personne", AMBRE),
              (vehicule, 0.1, 0.8, "Véhicule", AMBRE)]
    for k, (picto, u, v, nom, couleur) in enumerate(objets):
        a = apparition(t, 0.9 + k * 0.7, 0.5)
        x, y, s = point_sur_piste(boite, u, v)
        picto(d, (x, y), s, BLANC, a)
        pulse = (t * 1.2 + k * 0.3) % 1
        cercle(d, (x, y), (55 + 40 * pulse) * s, couleur, a * (1 - pulse) * 0.9, 3)
        texte(d, (x + 60 * s, y - 50 * s), nom, "demi", 26, couleur, a, "lm")

    # le drone passe au-dessus de la piste avec son cône de caméra
    a = apparition(t, _m(m, 1), 0.6)
    if a > 0:
        p = borne((t - _m(m, 1)) / max(1.0, D - _m(m, 1)))
        x = 1050 + 650 * p
        y = 250 + 20 * math.sin(t * 2)
        d.polygon([(x, y), (x - 160, y + 420), (x + 160, y + 420)], fill=avec_alpha(CYAN, 0.12 * a))
        drone(d, (x, y), 0.6, CYAN, a, t)

    a = apparition(t, 0.2, 0.7)
    paragraphe(d, (140, 330 + _glisse(a)), "Une piste doit rester libre.", "titre", 64, BLANC, a, 760)
    points = ["Inspection depuis un drone", "Analyse des images à bord",
              "Sans dépendre en permanence d'une connexion"]
    for k, s in enumerate(points):
        a = apparition(t, _m(m, 1, 0.3 + k * 0.9), 0.5)
        y = 560 + k * 90
        cercle(d, (156, y), 9, CYAN, a, plein=True)
        texte(d, (185 - _glisse(a, -20), y), s, "moyen", 36, BLANC, a, "lm")


# ------------------------------------------------------------------ 3. décision

def decision(d, t, D, m):
    cartes = [((150, 280, 870, 470), "Raspberry Pi 5", "Capture, vision, journalisation"),
              ((1050, 280, 1770, 470), "AI HAT+ 26 TOPS", "Accélérateur Hailo : détection locale")]
    for k, (b, nom, desc) in enumerate(cartes):
        a = apparition(t, 0.3 + k * 0.8, 0.6)
        b = (b[0], b[1] + _glisse(a), b[2], b[3] + _glisse(a))
        panneau(d, b, a, CYAN if k else CYAN_SOMBRE)
        puce_electronique(d, (b[0] + 90, (b[1] + b[3]) // 2), 1.1, CYAN, a)
        texte(d, (b[0] + 175, b[1] + 70), nom, "gras", 44, BLANC, a, "lm")
        texte(d, (b[0] + 175, b[1] + 125), desc, "normal", 27, GRIS, a, "lm")
    texte(d, (960, 375), "+", "gras", 80, CYAN, apparition(t, 0.9, 0.5), "mm")

    # caméra -> trois familles
    a = apparition(t, _m(m, 1), 0.6)
    camera(d, (240, 640), 1.3, CYAN, a)
    texte(d, (240, 720), "Caméra stabilisée", "moyen", 26, GRIS, a, "mm")
    familles = [(personne, "Personnes"), (vehicule, "Véhicules"), (debris, "Débris au sol")]
    for k, (picto, nom) in enumerate(familles):
        a2 = apparition(t, _m(m, 1, 1.6 + k * 0.7), 0.5)
        x = 640 + k * 420
        if k == 0:
            fleche(d, (330, 640), (x - 110, 640), CYAN_SOMBRE, a2 * 0.8, 3)
        panneau(d, (x - 100, 580, x + 270, 700), a2, CYAN_SOMBRE)
        picto(d, (x - 30, 645), 1.0, BLANC, a2)
        texte(d, (x + 40, 640), nom, "demi", 30, BLANC, a2, "lm")

    # suivi : un même objet relié d'image en image
    a = apparition(t, _m(m, 2), 0.6)
    if a > 0:
        n = 6
        for k in range(n):
            x = 300 + k * 190
            panneau(d, (x, 780, x + 150, 880), a, CYAN_SOMBRE, rayon=10, opacite_fond=0.6)
            px, py = x + 50 + k * 10, 835 - k * 4
            if k < n - 1:
                d.line([(px, py), (px + 200, py - 4)], fill=avec_alpha(CYAN, a * 0.7), width=3)
            cercle(d, (px, py), 10, CYAN, a, plein=True)
        texte(d, (1470, 830), "1 objet = 1 alerte", "gras", 34, CYAN, a, "lm")


# ------------------------------------------------------------------ 4. périmètre

def perimetre(d, t, D, m):
    lignes = [
        ("Zone analysée", "Piste et abords visibles, dans une zone d'intérêt définie", BLANC, 0.3),
        ("Classes v1", "Personne · véhicule · objet / débris au sol", BLANC, 0.9),
        ("Traitement", "Inférence à bord, aucune image envoyée vers un service cloud", BLANC, _m(m, 0, 1.8)),
        ("Limite", "Aide à l'inspection : ne certifie pas qu'une piste est libre, ne commande pas l'aéronef",
         AMBRE, _m(m, 1)),
    ]
    for k, (cle, valeur, couleur, debut) in enumerate(lignes):
        a = apparition(t, debut, 0.6)
        y = 290 + k * 150
        bord = AMBRE if couleur == AMBRE else CYAN_SOMBRE
        panneau(d, (140 - _glisse(a, 40), y, 1780, y + 125), a, bord)
        texte(d, (190, y + 62), cle, "gras", 36, CYAN if couleur != AMBRE else AMBRE, a, "lm")
        paragraphe(d, (560, y + (44 if len(valeur) < 70 else 26)), valeur, "moyen", 32, BLANC, a, 1150)
    a = apparition(t, _m(m, 0, 2.3), 0.5)
    nuage(d, (1690, 640), 0.7, GRIS, a)
    croix(d, (1690, 652), 44, ROUGE, a)


# ------------------------------------------------------------------ 5. architecture

BLOCS = ["Caméra\nstabilisée", "Raspberry\nPi 5", "YOLOv8s\ncompilé Hailo", "Suivi &\ncontrôle de zone",
         "Événement &\npreuve locale", "Liaison\nsécurisée", "Station\nau sol"]


def architecture(d, t, D, m):
    larg, haut, ecart, x0, y0 = 214, 220, 40, 82, 360
    debuts = [_m(m, 0, 0.3), _m(m, 1, 0.3), _m(m, 1, 1.5), _m(m, 1, 2.8),
              _m(m, 2, 0.6), _m(m, 2, 1.9), _m(m, 2, 3.2)]
    centres = []
    for k, nom in enumerate(BLOCS):
        a = apparition(t, debuts[k], 0.5)
        x = x0 + k * (larg + ecart)
        b = (x, y0 + _glisse(a, 30), x + larg, y0 + haut + _glisse(a, 30))
        npu = k == 2
        panneau(d, b, a, CYAN if npu else CYAN_SOMBRE, fond_couleur=(10, 60, 90) if npu else PANNEAU,
                epaisseur=4 if npu else 2)
        texte(d, (x + 22, b[1] + 22), f"{k + 1:02d}", "gras", 22, CYAN, a)
        for i, ligne in enumerate(nom.split("\n")):
            texte(d, (x + larg / 2, b[1] + 115 + i * 34), ligne, "demi", 24, BLANC, a, "mm")
        centres.append((x, y0 + haut / 2))
        if k > 0:
            fleche(d, (x - ecart + 4, y0 + haut / 2), (x - 4, y0 + haut / 2), CYAN, a, 4, 14)

    # paquet de données qui circule une fois la chaîne complète
    a = apparition(t, debuts[-1] + 0.4, 0.4)
    if a > 0:
        u = ((t - debuts[-1]) * 0.35) % 1
        xp = x0 + larg / 2 + u * (6 * (larg + ecart))
        cercle(d, (xp, y0 - 40), 12, CYAN, a, plein=True)
        cercle(d, (xp, y0 - 40), 22, CYAN, a * 0.4, 2)
        d.line([(x0 + larg / 2, y0 - 40), (x0 + larg / 2 + 6 * (larg + ecart), y0 - 40)],
               fill=avec_alpha(CYAN_SOMBRE, a * 0.5), width=2)

    a = apparition(t, _m(m, 1, 1.5), 0.6)
    d.rounded_rectangle((140, 680, 176, 716), 6, fill=avec_alpha((10, 60, 90), a), outline=avec_alpha(CYAN, a), width=4)
    texte(d, (195, 698), "Détection exécutée sur l'accélérateur Hailo", "moyen", 30, BLANC, a, "lm")
    a = apparition(t, _m(m, 2, 1.0), 0.6)
    d.rounded_rectangle((140, 750, 176, 786), 6, fill=avec_alpha(PANNEAU, a), outline=avec_alpha(CYAN_SOMBRE, a), width=2)
    texte(d, (195, 768), "Suivi, zone et journalisation : traitements légers sur le Raspberry Pi",
          "moyen", 30, BLANC, a, "lm")


# ------------------------------------------------------------------ 6. choix

def choix(d, t, D, m):
    cartes = [
        ("Détecteur compact", "Retenu", "Sortie stable, localisée et rapide sur de petites cibles. Mesurable et adapté à l'accélérateur.", True, _m(m, 0, 0.2)),
        ("Modèle génératif ou vision-langage", "Non retenu", "Pas comme détecteur principal : moins stable et plus coûteux à bord.", False, _m(m, 1, 0.3)),
        ("Segmentation", "Non retenue en v1", "Des rectangles suffisent pour repérer et signaler, avec moins de calcul et d'annotation.", False, _m(m, 1, 2.0)),
    ]
    for k, (nom, statut, desc, ok, debut) in enumerate(cartes):
        a = apparition(t, debut, 0.6)
        x = 140 + k * 560
        b = (x, 300 + _glisse(a, 40), x + 520, 860 + _glisse(a, 40))
        panneau(d, b, a, VERT if ok else (90, 105, 130), epaisseur=3 if ok else 2)
        cercle(d, (x + 260, b[1] + 120), 62, VERT if ok else ROUGE, a * 0.9, 4)
        (coche if ok else croix)(d, (x + 260, b[1] + 122), 64, VERT if ok else ROUGE, a)
        paragraphe(d, (x + 260, b[1] + 220), nom, "gras", 38, BLANC, a, 440, 1.2, "ma")
        texte(d, (x + 260, b[1] + 345), statut.upper(), "gras", 24, VERT if ok else ROUGE, a, "mm")
        paragraphe(d, (x + 260, b[1] + 395), desc, "normal", 27, GRIS, a, 430, 1.35, "ma")


# ------------------------------------------------------------------ 7. modèle

def _vue_aerienne(d, b, a, t):
    x0, y0, x1, y1 = b
    d.rectangle(b, fill=avec_alpha((26, 34, 46), a))
    d.rectangle((x0 + 120, y0, x1 - 120, y1), fill=avec_alpha(ASPHALTE, a))
    for y in range(int(y0) + 20, int(y1), 90):
        d.line([((x0 + x1) / 2, y), ((x0 + x1) / 2, y + 45)], fill=avec_alpha(BLANC, a * 0.7), width=6)
    d.line([(x0 + 135, y0), (x0 + 135, y1)], fill=avec_alpha(BLANC, a * 0.6), width=4)
    d.line([(x1 - 135, y0), (x1 - 135, y1)], fill=avec_alpha(BLANC, a * 0.6), width=4)
    d.rectangle(b, outline=avec_alpha(CYAN_SOMBRE, a), width=2)


def modele(d, t, D, m):
    b = (150, 270, 750, 870)
    a = apparition(t, 0.2, 0.6)
    _vue_aerienne(d, b, a, t)
    cibles = [(personne, (300, 420), "personne", AMBRE), (vehicule, (560, 700), "véhicule", AMBRE),
              (debris, (420, 560), "débris", ROUGE)]
    for k, (picto, (x, y), nom, couleur) in enumerate(cibles):
        picto(d, (x, y), 0.9, BLANC, a)
        a2 = apparition(t, _m(m, 1, 0.4 + k * 0.6), 0.35)
        boite = (x - 60, y - 60, x + 60, y + 50)
        d.rectangle(boite, outline=avec_alpha(couleur, a2), width=4)
        lt = 22
        lw = 18 + len(nom) * 13
        d.rectangle((boite[0] - 2, boite[1] - 34, boite[0] + lw, boite[1]), fill=avec_alpha(couleur, a2))
        texte(d, (boite[0] + 8, boite[1] - 17), nom, "gras", lt, (10, 15, 25), a2, "lm")
    texte(d, (b[0], b[3] + 22), "Illustration schématique", "normal", 22, GRIS, a)

    a3 = apparition(t, _m(m, 2, 1.8), 0.6)
    if a3 > 0:
        for i in (1, 2):
            x = b[0] + (b[2] - b[0]) * i / 3
            ligne_pointillee(d, (x, b[1]), (x, b[3]), CYAN, a3, 3)
            y = b[1] + (b[3] - b[1]) * i / 3
            ligne_pointillee(d, (b[0], y), (b[2], y), CYAN, a3, 3)
    texte(d, (b[2] - 10, b[1] + 26), "640 × 640", "gras", 28, CYAN, apparition(t, _m(m, 2), 0.5), "rm")

    etapes = [("YOLOv8s pré-entraîné", "Caractéristiques visuelles générales", 0.4),
              ("Fine-tuning", "FOD-A + images de la caméra du projet", _m(m, 0, 2.2)),
              ("Sortie par candidat", "classe  ·  score  ·  rectangle", _m(m, 1, 0.2)),
              ("Petits objets", "Entrée plus grande ou découpage en tuiles, si Hailo tient la cadence", _m(m, 2, 1.8))]
    for k, (nom, desc, debut) in enumerate(etapes):
        a = apparition(t, debut, 0.5)
        y = 290 + k * 150
        panneau(d, (860, y, 1780, y + 120), a, CYAN if k == 2 else CYAN_SOMBRE)
        texte(d, (900, y + 40), nom, "gras", 34, CYAN if k == 2 else BLANC, a, "lm")
        texte(d, (900, y + 85), desc, "normal", 27, GRIS, a, "lm")
        if k:
            fleche(d, (1320, y - 28), (1320, y - 2), CYAN_SOMBRE, a, 3, 10)


# ------------------------------------------------------------------ 8. objets inconnus

def inconnus(d, t, D, m):
    b = (150, 300, 700, 850)
    a = apparition(t, 0.1, 0.6)
    d.rectangle(b, fill=avec_alpha(ASPHALTE, a))
    for y in range(b[1] + 30, b[3], 100):
        d.line([(425, y), (425, y + 50)], fill=avec_alpha(BLANC, a * 0.6), width=6)
    d.polygon([(300, 540), (330, 510), (360, 530), (352, 572), (310, 575)], fill=avec_alpha((170, 180, 195), a))
    pulse = 0.5 + 0.5 * math.sin(t * 4)
    rectangle_pointille(d, (255, 470, 405, 615), AMBRE, a, 4, t * 30)
    texte(d, (330, 430), "?", "gras", 64, AMBRE, a * (0.6 + 0.4 * pulse), "mm")
    texte(d, (150, 875), "Candidat sans classe fiable", "moyen", 26, GRIS, a)

    niveaux = [("Objet « à vérifier »", "Candidat crédible sans classe stable : journalisé avec son image.", AMBRE, _m(m, 0)),
               ("Détection d'anomalie", "Comparaison avec une piste libre de référence, testée si l'alignement est fiable.", CYAN, _m(m, 1)),
               ("Suivi multi-images", "Confirme la persistance et écarte les artefacts isolés.", CYAN, _m(m, 2))]
    for k, (nom, desc, couleur, debut) in enumerate(niveaux):
        a = apparition(t, debut, 0.6)
        y = 300 + k * 175
        panneau(d, (800 + _glisse(a, -40), y, 1780, y + 150), a, couleur if k == 0 else CYAN_SOMBRE)
        puce_numero(d, (865, y + 75), k + 1, a, couleur)
        texte(d, (920, y + 48), nom, "gras", 36, couleur if k == 0 else BLANC, a, "lm")
        paragraphe(d, (920, y + 80), desc, "normal", 27, GRIS, a, 840, 1.25)
    a = apparition(t, _m(m, 2, 2.2), 0.6)
    texte(d, (1290, 860), "Pas de reconnaissance garantie de tout objet inconnu", "demi", 28, AMBRE, a, "mm")


# ------------------------------------------------------------------ 9. données

def _compteur(t, debut, valeur, duree=1.4):
    return int(round(valeur * sortie_cubique((t - debut) / duree)))


def donnees(d, t, D, m):
    cartes = [(150, 270, "FOD-A", "Jeu public de débris de piste", 0.2),
              (990, 270, "Images du projet", "Hauteur, angle, stabilisation et lumière réelles de la mission", _m(m, 1)),
              (150, 600, "Données aériennes publiées", "YOLO-URD (2026) : drone à 2–6 m, ~6 000 images · accès et licence à vérifier", _m(m, 1, 2.0)),
              (990, 600, "Exemples négatifs", "Piste vide, ombres, reflets, marquages, flaques, herbe", _m(m, 2))]
    for k, (x, y, nom, desc, debut) in enumerate(cartes):
        a = apparition(t, debut, 0.6)
        panneau(d, (x, y + _glisse(a), x + 780, y + 290 + _glisse(a)), a, CYAN if k == 0 else CYAN_SOMBRE)
        texte(d, (x + 40, y + 55), nom, "gras", 40, CYAN if k == 0 else BLANC, a, "lm")
        if k == 0:
            n1 = _compteur(t, _m(m, 0, 0.6), 31)
            n2 = _compteur(t, _m(m, 0, 1.6), 30000)
            texte(d, (x + 40, y + 150), f"{n1}", "titre", 84, BLANC, a, "lm")
            texte(d, (x + 40, y + 220), "catégories", "moyen", 28, GRIS, a, "lm")
            texte(d, (x + 330, y + 150), f"{n2:,}+".replace(",", " "), "titre", 84, BLANC, a, "lm")
            texte(d, (x + 330, y + 220), "instances annotées", "moyen", 28, GRIS, a, "lm")
        else:
            paragraphe(d, (x + 40, y + 110), desc, "normal", 30, GRIS, a, 690, 1.35)
        if k == 3:
            croix(d, (x + 720, y + 55), 34, ROUGE, a)


# ------------------------------------------------------------------ 10. protocole

ETAPES = [("Préparer", "Annotations, classes,\nséparation par séquence"), ("Adapter", "Fine-tuning YOLOv8s"),
          ("Évaluer", "Précision, rappel,\nerreurs par classe"), ("Exporter", "ONNX → HEF"),
          ("Quantifier", "Calibration INT8"), ("Déployer", "Raspberry Pi 5\n+ Hailo")]


def protocole(d, t, D, m):
    xs = [210 + k * 300 for k in range(6)]
    y = 430
    debuts = [_m(m, 0, 1.0 + k * 0.7) for k in range(3)] + [_m(m, 1, 0.8 + k * 1.6) for k in range(3)]
    progression = sum(apparition(t, debuts[k], 0.6) for k in range(1, 6))
    d.line([(xs[0], y), (xs[-1], y)], fill=avec_alpha(CYAN_SOMBRE, apparition(t, 0.2, 0.6) * 0.5), width=4)
    xf = xs[0] + (xs[-1] - xs[0]) * progression / 5
    d.line([(xs[0], y), (xf, y)], fill=avec_alpha(CYAN, 1), width=6)
    for k, (nom, desc) in enumerate(ETAPES):
        a = apparition(t, debuts[k], 0.5)
        a0 = apparition(t, 0.2, 0.6)
        puce_numero(d, (xs[k], y), k + 1, max(a, a0 * 0.6), CYAN, 38, a > 0.5)
        texte(d, (xs[k], y + 85), nom, "gras", 36, BLANC, max(a, a0 * 0.35), "mm")
        for i, ligne in enumerate(desc.split("\n")):
            texte(d, (xs[k], y + 135 + i * 34), ligne, "normal", 26, GRIS, a, "mm")
    a = apparition(t, _m(m, 2), 0.6)
    panneau(d, (310, 740, 1610, 870), a, AMBRE)
    texte(d, (960, 785), "Critère de sélection", "gras", 30, AMBRE, a, "mm")
    texte(d, (960, 830), "Rappel des petits objets + fausses alertes — pas un score global seul",
          "moyen", 32, BLANC, a, "mm")


# ------------------------------------------------------------------ 11. alerte

def alerte(d, t, D, m):
    a = apparition(t, _m(m, 0), 0.6)
    b = (140, 280, 900, 880)
    panneau(d, b, a, AMBRE)
    texte(d, (180, 330), "ÉVÉNEMENT", "gras", 30, AMBRE, a, "lm")
    texte(d, (870, 330), "exemple fictif", "normal", 22, GRIS, a, "rm")
    champs = [("Heure", "14:32:07"), ("Classe", "« à vérifier »"), ("Score", "0,62"),
              ("Rectangle", "x 812 · y 404 · 96 × 70"), ("Séquence", "SEQ-0042"), ("Preuve", "")]
    for k, (cle, val) in enumerate(champs):
        a2 = apparition(t, _m(m, 0, 1.6 + k * 0.6), 0.4)
        y = 400 + k * 68
        texte(d, (180, y), cle, "moyen", 30, GRIS, a2, "lm")
        texte(d, (430, y), val, "demi", 30, BLANC, a2, "lm")
    a2 = apparition(t, _m(m, 0, 1.6 + 5 * 0.6), 0.4)
    d.rectangle((430, 718, 640, 848), fill=avec_alpha(ASPHALTE, a2), outline=avec_alpha(AMBRE, a2), width=3)
    debris(d, (535, 783), 1.2, BLANC, a2)

    # liaison drone -> station, coupée puis reprise
    a = apparition(t, 0.3, 0.6)
    drone(d, (1130, 380), 0.65, CYAN, a, t)
    antenne(d, (1660, 360), 1.2, CYAN, a)
    texte(d, (1660, 450), "Station au sol", "moyen", 26, GRIS, a, "mm")
    coupure = apparition(t, _m(m, 1), 0.3)
    lien = melange(CYAN, ROUGE, coupure)
    if coupure < 0.5:
        ligne_pointillee(d, (1210, 380), (1600, 380), lien, a, 4, 16, 12, -t * 60)
    else:
        ligne_pointillee(d, (1210, 380), (1360, 380), ROUGE, a, 4, 16, 12)
        ligne_pointillee(d, (1450, 380), (1600, 380), ROUGE, a, 4, 16, 12)
        croix(d, (1405, 380), 44, ROUGE, a)
        texte(d, (1405, 440), "Liaison coupée", "demi", 26, ROUGE, a * coupure, "mm")
    a3 = apparition(t, _m(m, 1, 0.8), 0.5)
    stockage(d, (1130, 600), 1.2, CYAN, a3)
    n = min(3, max(0, int((t - _m(m, 1, 1.0)) / 0.9) + 1)) if t > _m(m, 1, 1.0) else 0
    texte(d, (1200, 580), "Analyse et stockage local", "gras", 30, BLANC, a3, "lm")
    texte(d, (1200, 625), f"{n} événement{'s' if n > 1 else ''} en attente d'envoi", "moyen", 28, CYAN, a3, "lm")

    a4 = apparition(t, _m(m, 2), 0.5)
    epingle(d, (1130, 810), 1.1, AMBRE, a4)
    texte(d, (1200, 770), "Position au sol", "gras", 30, AMBRE, a4, "lm")
    texte(d, (1200, 815), "Ajoutée seulement après calibration caméra", "moyen", 28, BLANC, a4, "lm")


# ------------------------------------------------------------------ 12. matériel

def materiel(d, t, D, m):
    couches = [("Alimentation régulée · fixation anti-vibration", GRIS),
               ("Raspberry Pi 5", CYAN_SOMBRE),
               ("AI HAT+ 26 TOPS · NPU Hailo-8", CYAN),
               ("Caméra stabilisée jour / nuit", CYAN_SOMBRE)]
    for k, (nom, couleur) in enumerate(couches):
        a = apparition(t, _m(m, 0, 0.4 + k * 1.3), 0.6)
        y = 760 - k * 140 - _glisse(a, -40)
        x = 170 + k * 30
        d.polygon([(x, y), (x + 760, y), (x + 820, y - 50), (x + 60, y - 50)], fill=avec_alpha(melange(PANNEAU, couleur, 0.35), a),
                  outline=avec_alpha(couleur, a), width=3)
        d.rectangle((x, y, x + 760, y + 50), fill=avec_alpha(PANNEAU, a * 0.9), outline=avec_alpha(couleur, a), width=3)
        texte(d, (x + 380, y + 25), nom, "demi", 28, BLANC, a, "mm")
    notes = [("Repli possible", "HAT+ 13 TOPS si la cadence requise est tenue"),
             ("Stockage", "microSD : images d'alerte plutôt que vidéo complète"),
             ("Développement", "Python, OpenCV, Ultralytics, ONNX, outils Hailo, CVAT")]
    for k, (cle, val) in enumerate(notes):
        a = apparition(t, _m(m, 0, 3.0 + k * 1.2), 0.6)
        y = 330 + k * 175
        texte(d, (1150, y), cle, "gras", 32, CYAN, a, "lm")
        paragraphe(d, (1150, y + 30), val, "normal", 28, BLANC, a, 640, 1.3)


# ------------------------------------------------------------------ 13. validation

def validation(d, t, D, m):
    etapes = ["Vidéos\nenregistrées", "Caméra\nsur banc", "Plateforme\nau sol", "Essai en vol\nautorisé"]
    for k, nom in enumerate(etapes):
        a = apparition(t, _m(m, 0, 2.4 + k * 1.1) if k < 3 else _m(m, 0, 6.0), 0.5)
        x = 150 + k * 420
        futur = k == 3
        pts = [(x, 290), (x + 360, 290), (x + 400, 360), (x + 360, 430), (x, 430), (x + 40, 360)]
        d.polygon(pts, fill=avec_alpha(PANNEAU if futur else (10, 55, 85), a), outline=avec_alpha(GRIS if futur else CYAN, a), width=3)
        for i, ligne in enumerate(nom.split("\n")):
            texte(d, (x + 210, 340 + i * 38), ligne, "demi", 30, GRIS if futur else BLANC, a, "mm")
    texte(d, (1620, 460), "ensuite", "normal", 22, GRIS, apparition(t, _m(m, 0, 6.0), 0.5), "mm")

    mesures = ["Rappel par classe", "Fausses alertes", "Latence et débit", "Température et énergie",
               "Hors connexion", "Alerte exploitable"]
    for k, nom in enumerate(mesures):
        a = apparition(t, _m(m, 1, k * 0.45), 0.5)
        x = 150 + (k % 3) * 550
        y = 530 + (k // 3) * 110
        panneau(d, (x, y, x + 510, y + 85), a, CYAN_SOMBRE, rayon=14)
        coche(d, (x + 45, y + 43), 28, CYAN, a)
        texte(d, (x + 85, y + 43), nom, "moyen", 29, BLANC, a, "lm")
    a = apparition(t, _m(m, 1, 3.6), 0.5)
    panneau(d, (560, 790, 1360, 880), a, AMBRE, rayon=45, epaisseur=3)
    texte(d, (960, 835), "Aucun taux annoncé avant mesure", "gras", 36, AMBRE, a, "mm")


# ------------------------------------------------------------------ 14. conclusion

def conclusion(d, t, D, m):
    a = apparition(t, 0.0, 0.8)
    drone(d, (960, 250), 0.8, CYAN, a, t)
    texte(d, (960, 400), "SENTINELLE AÉRIENNE", "titre", 96, BLANC, a, "mm")
    a = apparition(t, 0.8, 0.8)
    texte(d, (960, 480), "Une IA embarquée, sobre et mesurable, au service de la sécurité des pistes",
          "moyen", 36, CYAN, a, "mm")
    lots = [("Lot IA", "KAINWANG Roger"), ("Mécanique & électronique", "AWADE Constantin Israel"),
            ("Embarqué & station sol", "LOGO ADANTO Angelo"), ("Back-end & documentation", "KODJOVI Eli Cédric Ankou"),
            ("Réseau & sécurité", "de MEDEIROS Makafui Komlan Léopoldo")]
    for k, (lot, nom) in enumerate(lots):
        a = apparition(t, _m(m, 1, k * 0.5), 0.5)
        x = 80 + k * 356
        panneau(d, (x, 590, x + 336, 760), a, CYAN if k == 0 else CYAN_SOMBRE)
        paragraphe(d, (x + 168, 620), lot, "gras", 26, CYAN if k == 0 else BLANC, a, 300, 1.2, "ma")
        paragraphe(d, (x + 168, 690), nom, "normal", 24, GRIS, a, 300, 1.25, "ma")
    a = apparition(t, _m(m, 1, 3.0), 0.6)
    texte(d, (960, 830), "SkyVision Togo  ·  CECFD 2026 — ANAC", "demi", 30, GRIS, a, "mm")


SCENES_VISUELLES = {f.__name__: f for f in [titre, mission, decision, perimetre, architecture, choix, modele,
                                             inconnus, donnees, protocole, alerte, materiel, validation, conclusion]}
