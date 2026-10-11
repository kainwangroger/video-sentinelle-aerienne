"""Scènes 3D : assemblage animé, CAO, contrôles et vols. Signature f(d, t, D, m, scene)."""

import math

import numpy as np

from gfx import (AMBRE, BLANC, CYAN, CYAN_SOMBRE, GRIS, VERT, apparition, avec_alpha, borne, cercle, panneau, paragraphe,
                 puce_numero, sortie_cubique, texte)

from .modele_sa1 import GROUPES, HELICES, catalogue, rotation_helice
from .moteur3d import Camera, Maillage, Objet, rendre, rotation

TOUT = [n for g in GROUPES.values() for n in g]
TRANSPARENTS = {"fuselage", "trappe", "aile_centrale"}


def developper(noms):
    sortie = []
    for n in noms or []:
        if n == "tout":
            sortie += TOUT
        elif n in GROUPES:
            sortie += GROUPES[n]
        else:
            sortie.append(n)
    return sortie


def _interp(valeur, u):
    if isinstance(valeur, (list, tuple)) and len(valeur) == 2 and not isinstance(valeur[0], (list, tuple)):
        return valeur[0] + (valeur[1] - valeur[0]) * u
    return valeur


def camera_scene(don, t, D, centre_ecran):
    cam = don.get("camera", {})
    u = sortie_cubique(t / max(1.0, D)) * 0.5 + (t / max(1.0, D)) * 0.5
    return Camera(azimut=_interp(cam.get("az", (0.7, 1.1)), u), elevation=_interp(cam.get("el", 0.42), u),
                  distance=_interp(cam.get("dist", 2.6), u), cible=tuple(cam.get("cible", (-0.12, 0, 0))),
                  focale=cam.get("focale", 1500), centre_ecran=centre_ecran)


def _objets(don, t, m, deplacement=(0, 0, 0), assiette=0.0, vitesse_helices=None):
    """Construit la liste d'objets de la scène et les étiquettes actives."""
    cat = catalogue()
    base = set(developper(don.get("base", [])))
    masquer = set(developper(don.get("masquer", [])))
    transparent = don.get("transparent", False)
    objets, etiquettes = [], []
    ajouts = don.get("ajouts", [])
    debuts = [m[min(a.get("phrase", 0), len(m) - 1)] + a.get("retard", 0.3) for a in ajouts]
    arrives = {}
    for k, (a, debut) in enumerate(zip(ajouts, debuts)):
        p = sortie_cubique((t - debut) / a.get("duree", 1.8))
        for nom in developper(a["pieces"]):
            arrives[nom] = (p, t - debut)
        if a.get("label") and p > 0.6:
            fin = debuts[k + 1] if k + 1 < len(debuts) else 1e9
            if t < fin + 0.3:
                etiquettes.append((developper(a["pieces"]), a["label"], apparition(t, debut + 1.0, 0.4)))
    angle_h = (t * vitesse_helices) if vitesse_helices else None
    rot = np.asarray(rotation(ry=assiette))
    for nom, (maillage, eclate) in cat.items():
        if nom in masquer and nom not in arrives:
            continue
        if nom in arrives:
            p, ecoule = arrives[nom]
            if p <= 0:
                continue
            decal = np.asarray(eclate, float) * (1 - p)
            surbrillance = 1.0 if p < 1 else max(0.0, 1 - (ecoule - 1.8) / 2.0)
            alpha = min(1.0, p * 4)
        elif nom in base:
            decal, surbrillance, alpha = np.zeros(3), 0.0, 1.0
        else:
            continue
        mm = maillage
        if angle_h is not None and nom in HELICES:
            sens = 1 if nom in ("helice_av_gauche", "helice_ar_droite", "helice_croisiere") else -1
            mm = rotation_helice(nom, mm, angle_h * sens)
        mm = Maillage(mm.sommets @ rot.T + decal + np.asarray(deplacement, float), mm.faces, mm.couleur, mm.double_face)
        filaire = transparent and nom in TRANSPARENTS
        objets.append(Objet(mm, alpha=0.35 if filaire else alpha, surbrillance=surbrillance, filaire=filaire, nom=nom))
    return objets, etiquettes


def _etiquettes(d, camera, objets, etiquettes, zone_x0):
    par_nom = {o.nom: o for o in objets}
    for k, (noms, label, a) in enumerate(etiquettes):
        pts = [par_nom[n].maillage.sommets.mean(0) for n in noms if n in par_nom]
        if not pts:
            continue
        p2, _ = camera.projeter([np.mean(pts, 0)])
        x, y = p2[0]
        lx = max(zone_x0 + 40, min(1500, x + 160))
        ly = max(260, y - 170 - 60 * k)
        d.line([(x, y), (lx, ly + 18)], fill=avec_alpha(AMBRE, a), width=2)
        cercle(d, (x, y), 7, AMBRE, a, plein=True)
        larg = 18 + len(label) * 14
        d.rounded_rectangle((lx, ly, lx + larg, ly + 38), 8, fill=avec_alpha((40, 30, 10), a * 0.85),
                            outline=avec_alpha(AMBRE, a), width=2)
        texte(d, (lx + 10, ly + 19), label, "demi", 24, AMBRE, a, "lm")


def _panneau_etapes(d, t, m, etapes):
    actif = max(0, sum(1 for x in m if x <= t + 0.2) - 1)
    actif = min(actif, len(etapes) - 1)
    h = min(130, (880 - 250) / max(1, len(etapes)))
    for k, etape in enumerate(etapes):
        titre, detail = etape if isinstance(etape, (list, tuple)) else (etape, "")
        a = apparition(t, 0.2 + k * 0.15, 0.4)
        y = 250 + k * h
        on = k == actif
        fait = k < actif
        panneau(d, (100, y, 600, y + h - 12), a * (1 if on else 0.6), AMBRE if on else CYAN_SOMBRE, rayon=12,
                epaisseur=3 if on else 2)
        puce_numero(d, (140, y + 32), k + 1, a, VERT if fait else (AMBRE if on else CYAN), 20, on or fait)
        texte(d, (175, y + 32), titre, "gras", 26, BLANC if on else GRIS, a, "lm")
        if detail and h > 70:
            paragraphe(d, (175, y + 52), detail, "normal", 21, GRIS if not on else BLANC, a, 400, 1.25)


def assemblage3d(d, t, D, m, scene):
    don = scene["donnees"]
    etapes = don.get("etapes")
    centre = (1230, 570) if etapes else (960, 570)
    camera = camera_scene(don, t, D, centre)
    objets, etiquettes = _objets(don, t, m, vitesse_helices=don.get("rotation"))
    rendre(d, camera, objets)
    if don.get("cg"):
        _centre_gravite(d, camera, t, m)
    if don.get("disques"):
        _disques_helices(d, camera, t)
    _etiquettes(d, camera, objets, etiquettes, 620 if etapes else 120)
    if etapes:
        _panneau_etapes(d, t, m, etapes)
    if don.get("note"):
        a = apparition(t, 0.8, 0.5)
        texte(d, (1880, 900), don["note"], "normal", 22, GRIS, a, "rm")


def _centre_gravite(d, camera, t, m):
    a = apparition(t, m[min(1, len(m) - 1)], 0.5)
    cg = np.array([0.03, 0, 0.02])  # ≈ 27 % de la corde de l'aile
    p, _ = camera.projeter([cg])
    x, y = p[0]
    r = 22
    cercle(d, (x, y), r, BLANC, a, 3)
    d.pieslice((x - r, y - r, x + r, y + r), 0, 90, fill=avec_alpha(BLANC, a))
    d.pieslice((x - r, y - r, x + r, y + r), 180, 270, fill=avec_alpha(BLANC, a))
    texte(d, (x + 34, y - 30), "CG ≈ 27 % de la corde", "gras", 26, BLANC, a, "lm")
    # repère de corde
    p2, _ = camera.projeter([[0.10, 0.36, 0.07], [-0.18, 0.36, 0.07]])
    d.line([tuple(p2[0]), tuple(p2[1])], fill=avec_alpha(CYAN, a), width=3)


def _disques_helices(d, camera, t):
    from .modele_sa1 import X_MOTEURS, Y_POUTRE, Z_POUTRE
    a = apparition(t, 0.5, 0.6)
    for x in X_MOTEURS:
        for y in (-Y_POUTRE, Y_POUTRE):
            pts = [[x + 0.19 * math.cos(k / 32 * 2 * math.pi), y + 0.19 * math.sin(k / 32 * 2 * math.pi), Z_POUTRE + 0.066]
                   for k in range(33)]
            p, _ = camera.projeter(pts)
            d.line([tuple(q) for q in p], fill=avec_alpha(VERT, a), width=2)


# ------------------------------------------------------------------ CAO : du filaire au volume

def cao(d, t, D, m, scene):
    don = scene["donnees"]
    camera = camera_scene(don, t, D, (1150, 570))
    cat = catalogue()
    ordre = ["cellule", "propulsion", "capteurs", "interieur"]
    objets = []
    debuts = [m[min(k, len(m) - 1)] + 0.3 for k in range(len(ordre))]
    for groupe, debut in zip(ordre, debuts):
        a = apparition(t, debut, 0.8)
        solide = apparition(t, debut + 2.5, 1.2)
        for nom in GROUPES[groupe]:
            maillage, _ = cat[nom]
            if a <= 0:
                continue
            if solide < 1:
                objets.append(Objet(maillage, alpha=a * (1 - solide), filaire=True, nom=nom))
            if solide > 0:
                objets.append(Objet(maillage, alpha=solide, nom=nom))
    rendre(d, camera, objets)
    etapes = don.get("etapes", [])
    for k, (titre, detail) in enumerate(etapes):
        a = apparition(t, debuts[min(k, len(debuts) - 1)], 0.5)
        y = 260 + k * 150
        panneau(d, (100, y, 560, y + 130), a, CYAN_SOMBRE, rayon=12)
        texte(d, (130, y + 34), titre, "gras", 28, CYAN, a, "lm")
        paragraphe(d, (130, y + 60), detail, "normal", 22, GRIS, a, 400, 1.25)
    texte(d, (1880, 905), "Maquette numérique — proportions du SA-1", "normal", 22, GRIS, apparition(t, 0.5, 0.5), "rm")


# ------------------------------------------------------------------ vol d'essai

def vol3d(d, t, D, m, scene):
    """Décollage vertical puis stationnaire (et option transition) au-dessus d'une aire."""
    don = scene["donnees"]
    u = borne((t - m[0]) / max(1.0, D - 1.5 - m[0]))
    hauteur = don.get("hauteur", 0.9) * sortie_cubique(min(1.0, u / 0.5))
    avance = 0.0
    assiette = 0.0
    if don.get("transition"):
        f = borne((u - 0.5) / 0.5)
        avance = 2.2 * f * f
        assiette = -0.06 * math.sin(f * math.pi)
    camera = camera_scene(don, t, D, (960, 560))
    camera.focale = 1150
    camera.cible = (-0.1 + avance * 0.6, 0, (hauteur - 0.25) / 2)
    objets, _ = _objets({"base": ["tout"], "masquer": don.get("masquer", [])}, t, m,
                        deplacement=(avance, 0, hauteur), assiette=assiette, vitesse_helices=25)
    # aire de décollage
    pts = [[0.45 * math.cos(k / 40 * 2 * math.pi), 0.45 * math.sin(k / 40 * 2 * math.pi), -0.25] for k in range(41)]
    p, _ = camera.projeter(pts)
    d.line([tuple(q) for q in p], fill=avec_alpha(AMBRE, 0.7), width=3)
    pc, _ = camera.projeter([[0, 0, -0.25]])
    texte(d, tuple(pc[0]), "H", "gras", 40, AMBRE, 0.8, "mm")
    rendre(d, camera, objets)
    if don.get("hud", True):
        a = apparition(t, 0.3, 0.5)
        panneau(d, (1400, 250, 1830, 470), a, CYAN_SOMBRE, rayon=12)
        mode = don.get("mode", "QHOVER")
        texte(d, (1430, 285), mode, "gras", 30, AMBRE, a, "lm")
        texte(d, (1430, 340), f"Hauteur : {hauteur * 3.4:.1f} m", "demi", 26, BLANC, a, "lm")
        texte(d, (1430, 385), "Vibrations : OK", "demi", 26, VERT, a, "lm")
        texte(d, (1430, 430), don.get("etat", "Stabilité : bonne"), "demi", 26, BLANC, a, "lm")


SCENES_3D = {f.__name__: f for f in [assemblage3d, cao, vol3d]}
