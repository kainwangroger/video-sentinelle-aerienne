"""Maquette 3D du SA-1 (proportions de la fiche technique), pièce par pièce.

Chaque pièce a un nom, une position assemblée et un décalage « éclaté » d'où elle arrive
pendant l'animation. Dimensions en mètres : envergure 2,0 m, corde 0,28 m, poutres
carbone à ±0,32 m, hélices verticales 15 pouces, hélice propulsive 13 pouces.
"""

from .moteur3d import boite, cylindre, fuselage, helice, rotation, sphere, surface_portante

CARBONE = (60, 66, 76)
COMPOSITE = (210, 218, 228)
IMPRESSION = (240, 140, 40)
MOTEUR = (40, 44, 52)
CUIVRE = (190, 110, 60)
PCB_VERT = (40, 130, 80)
PCB_BLEU = (40, 90, 160)
BATTERIE = (230, 190, 40)
ROUGE = (210, 60, 60)
NOIR = (30, 30, 34)

Y_POUTRE = 0.32
Z_POUTRE = 0.035
X_MOTEURS = (0.36, -0.40)
Z_AILE = 0.07


def pieces():
    """Renvoie un dict nom -> (maillage assemblé, décalage éclaté (dx, dy, dz))."""
    p = {}
    p["fuselage"] = (fuselage(1.0, 0.15, 0.15, COMPOSITE, nez_x=0.45), (0, 0, 0))
    p["trappe"] = (boite(0.40, 0.11, 0.012, (190, 200, 214), centre=(0.10, 0, 0.078)), (0, 0, 0.35))
    p["aile_centrale"] = (surface_portante(-0.30, 0.30, 0.28, 0.10, Z_AILE, COMPOSITE), (0, 0, 0.5))
    p["aile_gauche"] = (surface_portante(-1.0, -0.30, 0.26, 0.09, Z_AILE, COMPOSITE), (0, -0.6, 0.2))
    p["aile_droite"] = (surface_portante(0.30, 1.0, 0.26, 0.09, Z_AILE, COMPOSITE), (0, 0.6, 0.2))
    p["aileron_gauche"] = (surface_portante(-0.95, -0.55, 0.06, -0.12, Z_AILE - 0.003, IMPRESSION, 0.08, 0.0), (-0.3, -0.2, 0.15))
    p["aileron_droit"] = (surface_portante(0.55, 0.95, 0.06, -0.12, Z_AILE - 0.003, IMPRESSION, 0.08, 0.0), (-0.3, 0.2, 0.15))
    p["longeron"] = (cylindre(0.008, 1.9, CARBONE, axe="y", centre=(0.0, 0, Z_AILE + 0.004)), (0, 0, 0.8))
    for cote, y in (("gauche", -Y_POUTRE), ("droite", Y_POUTRE)):
        p[f"poutre_{cote}"] = (cylindre(0.011, 1.20, CARBONE, axe="x", centre=(-0.20, y, Z_POUTRE)), (0, y * 1.2, -0.35))
        p[f"support_av_{cote}"] = (boite(0.05, 0.05, 0.02, IMPRESSION, centre=(X_MOTEURS[0], y, Z_POUTRE + 0.018)), (0, 0, 0.3))
        p[f"support_ar_{cote}"] = (boite(0.05, 0.05, 0.02, IMPRESSION, centre=(X_MOTEURS[1], y, Z_POUTRE + 0.018)), (0, 0, 0.3))
        p[f"derive_{cote}"] = (surface_portante(Z_POUTRE, Z_POUTRE + 0.14, 0.13, -0.66, y, COMPOSITE, 0.09, 0.0, vertical=True),
                               (-0.3, y * 0.6, 0.3))
        p[f"esc_av_{cote}"] = (boite(0.06, 0.025, 0.012, ROUGE, centre=(0.22, y, Z_POUTRE - 0.018)), (0, 0, -0.25))
        p[f"esc_ar_{cote}"] = (boite(0.06, 0.025, 0.012, ROUGE, centre=(-0.27, y, Z_POUTRE - 0.018)), (0, 0, -0.25))
        for i, x in enumerate(X_MOTEURS):
            pos = "av" if i == 0 else "ar"
            p[f"moteur_{pos}_{cote}"] = (cylindre(0.028, 0.032, MOTEUR, centre=(x, y, Z_POUTRE + 0.044)), (0, 0, 0.35))
            p[f"helice_{pos}_{cote}"] = (helice(0.19, (35, 38, 44), centre=(x, y, Z_POUTRE + 0.066),
                                                angle=0.4 if (i + (cote == "droite")) % 2 else 1.2), (0, 0, 0.45))
    p["stabilisateur"] = (surface_portante(-Y_POUTRE, Y_POUTRE, 0.11, -0.66, Z_POUTRE + 0.14, COMPOSITE, 0.09, 0.0), (-0.3, 0, 0.4))
    p["profondeur"] = (surface_portante(-Y_POUTRE + 0.02, Y_POUTRE - 0.02, 0.045, -0.775, Z_POUTRE + 0.138, IMPRESSION, 0.07, 0.0),
                       (-0.4, 0, 0.45))
    p["moteur_croisiere"] = (cylindre(0.026, 0.04, MOTEUR, axe="x", centre=(-0.58, 0, 0.0)), (-0.4, 0, 0))
    p["helice_croisiere"] = (helice(0.165, (35, 38, 44), axe="x", centre=(-0.615, 0, 0.0), angle=0.7), (-0.6, 0, 0))
    p["nacelle"] = (sphere(0.045, (50, 56, 66), centre=(0.36, 0, -0.085)), (0.2, 0, -0.3))
    p["camera"] = (cylindre(0.016, 0.03, NOIR, axe="x", centre=(0.40, 0, -0.088)), (0.35, 0, -0.3))
    p["mat_gnss"] = (cylindre(0.005, 0.12, CARBONE, centre=(-0.18, 0, 0.13)), (0, 0, 0.4))
    p["gnss"] = (cylindre(0.035, 0.015, (230, 230, 235), centre=(-0.18, 0, 0.195)), (0, 0, 0.55))
    p["pitot"] = (cylindre(0.004, 0.18, (220, 220, 225), axe="x", centre=(0.18, 0.75, Z_AILE)), (0.3, 0.1, 0))
    p["servo_gauche"] = (boite(0.03, 0.012, 0.025, PCB_BLEU, centre=(-0.05, -0.72, Z_AILE - 0.005)), (0, 0, -0.25))
    p["servo_droit"] = (boite(0.03, 0.012, 0.025, PCB_BLEU, centre=(-0.05, 0.72, Z_AILE - 0.005)), (0, 0, -0.25))
    # intérieur du fuselage
    p["batterie"] = (boite(0.19, 0.075, 0.06, BATTERIE, centre=(0.18, 0, -0.01)), (0, 0, 0.45))
    p["controleur"] = (boite(0.085, 0.05, 0.018, (20, 30, 50), centre=(-0.05, 0, 0.02)), (0, 0, 0.45))
    p["module_puissance"] = (boite(0.04, 0.03, 0.012, PCB_VERT, centre=(0.02, -0.035, 0.03)), (0, 0, 0.4))
    p["raspberry"] = (boite(0.085, 0.056, 0.02, PCB_VERT, centre=(-0.17, 0, 0.0)), (0, 0, 0.45))
    p["hat_ia"] = (boite(0.065, 0.056, 0.012, PCB_BLEU, centre=(-0.17, 0, 0.018)), (0, 0, 0.55))
    p["radio"] = (boite(0.05, 0.03, 0.012, (20, 30, 50), centre=(-0.30, 0, 0.0)), (0, 0, 0.4))
    p["antenne_g"] = (cylindre(0.003, 0.09, NOIR, centre=(-0.33, -0.05, -0.1)), (0, 0, -0.3))
    p["antenne_d"] = (cylindre(0.003, 0.09, NOIR, centre=(-0.33, 0.05, -0.1)), (0, 0, -0.3))
    return p


GROUPES = {
    "cellule": ["fuselage", "trappe", "aile_centrale", "aile_gauche", "aile_droite", "aileron_gauche", "aileron_droit",
                "longeron", "poutre_gauche", "poutre_droite", "derive_gauche", "derive_droite", "stabilisateur", "profondeur"],
    "propulsion": ["support_av_gauche", "support_ar_gauche", "support_av_droite", "support_ar_droite",
                   "moteur_av_gauche", "moteur_ar_gauche", "moteur_av_droite", "moteur_ar_droite",
                   "helice_av_gauche", "helice_ar_gauche", "helice_av_droite", "helice_ar_droite",
                   "moteur_croisiere", "helice_croisiere", "esc_av_gauche", "esc_ar_gauche", "esc_av_droite", "esc_ar_droite"],
    "interieur": ["batterie", "controleur", "module_puissance", "raspberry", "hat_ia", "radio", "antenne_g", "antenne_d"],
    "capteurs": ["mat_gnss", "gnss", "pitot", "servo_gauche", "servo_droit", "nacelle", "camera"],
}
HELICES = [n for n in GROUPES["propulsion"] if n.startswith("helice")]

_CACHE = None


def catalogue():
    global _CACHE
    if _CACHE is None:
        _CACHE = pieces()
    return _CACHE


def rotation_helice(nom, maillage, angle):
    """Fait tourner une hélice autour de son propre axe (animation)."""
    import numpy as np

    from .moteur3d import Maillage
    c = maillage.sommets.mean(0)
    r = np.asarray(rotation(rx=angle) if nom == "helice_croisiere" else rotation(rz=angle))
    return Maillage((maillage.sommets - c) @ r.T + c, maillage.faces, maillage.couleur, maillage.double_face)
