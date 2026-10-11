"""Génère les schémas PNG de la fiche technique avec le moteur graphique des vidéos.

Usage : python3 drone/outils/generer_schemas.py   -> drone/schemas/*.png
"""

import math
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RACINE / "video"))

from PIL import ImageDraw  # noqa: E402

import timeline  # noqa: E402
from az import contenu  # noqa: E402
from az.visuels import SCENES_VISUELLES  # noqa: E402
from gfx import (AMBRE, BLANC, CYAN, CYAN_SOMBRE, GRIS, ROUGE, VERT, avec_alpha, cercle, fleche, fond, largeur,  # noqa: E402
                 ligne_pointillee, panneau, paragraphe, texte)
from visuels_projet import vtol_dessus, vtol_profil  # noqa: E402

SORTIE = RACINE / "drone" / "schemas"

# scènes de la vidéo reprises comme schémas : titre de scène -> (nom de fichier, instant relatif)
SCENES = {
    "Les quatre forces du vol": ("forces_du_vol.png", 1.0),
    "Comment une aile porte": ("portance_aile.png", 1.0),
    "Les trois familles de drones": ("familles_de_drones.png", 1.0),
    "Le sens de rotation": ("sens_des_helices.png", 0.6),
    "Le moteur sans balais": ("moteur_sans_balais.png", 1.0),
    "La distribution électrique": ("distribution_electrique.png", 1.0),
    "La fusion des capteurs": ("fusion_des_capteurs.png", 1.0),
    "La transition, en image": ("transition.png", 0.62),
    "Deux liaisons radio": ("liaisons_radio.png", 1.0),
    "La chaîne de détection": ("chaine_ia.png", 1.0),
    "Détection d'un débris": ("simulation_detection.png", 0.35),
    "Le bilan de masse": ("bilan_de_masse.png", 1.0),
}


def titre(d, texte_titre):
    d.rectangle((80, 120, 88, 186), fill=avec_alpha(CYAN, 1))
    texte(d, (110, 153), texte_titre, "titre", 58, BLANC, 1, "lm")


def vue_annotee():
    """Vue de dessus du SA-1 avec le nom de chaque composant."""
    img = fond()
    d = ImageDraw.Draw(img, "RGBA")
    titre(d, "Sentinelle Aérienne SA-1 — vue de dessus")
    c = (820, 590)
    vtol_dessus(d, c, 1.05, CYAN, 1, 0.3)
    s = 1.05
    reperes = [
        ("Aile (2,0 m, 0,56 m²)", (c[0] - 260 * s, c[1] + 10 * s), (180, 330)),
        ("Aileron", (c[0] - 240 * s, c[1] + 33 * s), (180, 860)),
        ("Moteur VTOL avant gauche", (c[0] - 120 * s, c[1] - 140 * s), (180, 250)),
        ("Poutre carbone Ø 20 mm", (c[0] - 120 * s, c[1] + 60 * s), (180, 760)),
        ("Nez : nacelle caméra jour/nuit", (c[0], c[1] - 120 * s), (1300, 250)),
        ("Fuselage : batterie, avionique, IA", (c[0], c[1] - 30 * s), (1300, 360)),
        ("Mât GNSS + compas", (c[0], c[1] - 85 * s), (1300, 470)),
        ("Moteur VTOL arrière droit", (c[0] + 120 * s, c[1] + 180 * s), (1300, 900)),
        ("Hélice propulsive 13 × 8", (c[0], c[1] + 120 * s), (1300, 690)),
        ("Empennage en H (profondeur, directions)", (c[0] + 60 * s, c[1] + 188 * s), (1300, 800)),
        ("Tube de Pitot (vitesse air)", (c[0] + 280 * s, c[1] + 5 * s), (1300, 580)),
    ]
    for nom, cible, (x, y) in reperes:
        d.line([cible, (x - 10 if x > c[0] else x + largeur(nom, "demi", 28) + 12, y)], fill=avec_alpha(AMBRE, 0.8), width=2)
        cercle(d, cible, 7, AMBRE, 1, plein=True)
        texte(d, (x, y), nom, "demi", 28, BLANC, 1, "lm")
    texte(d, (960, 1040), "Schéma de principe — proportions indicatives", "normal", 22, GRIS, 1, "mm")
    return img


def profil_annote():
    img = fond()
    d = ImageDraw.Draw(img, "RGBA")
    titre(d, "Sentinelle Aérienne SA-1 — vue de côté")
    c = (900, 560)
    vtol_profil(d, c, 6.0, CYAN, 1)
    notes = [("Rotors de sustentation (vol vertical)", (c[0] - 210, c[1] - 120), (260, 300)),
             ("Aile (croisière)", (c[0], c[1] - 12), (260, 820)),
             ("Fuselage", (c[0] + 150, c[1]), (1350, 760)),
             ("Dérive", (c[0] - 380, c[1] - 140), (260, 420))]
    for nom, cible, (x, y) in notes:
        d.line([cible, (x + (largeur(nom, "demi", 30) + 12 if x < c[0] else -10), y)], fill=avec_alpha(AMBRE, 0.8), width=2)
        cercle(d, cible, 7, AMBRE, 1, plein=True)
        texte(d, (x, y), nom, "demi", 30, BLANC, 1, "lm")
    paragraphe(d, (960, 940), "En vol vertical, les quatre rotors portent le drone ; en croisière, l'aile porte "
               "et les rotors s'arrêtent.", "normal", 28, GRIS, 1, 1500, 1.3, "ma")
    return img


def architecture():
    """Schéma d'architecture : énergie (rouge), commandes (cyan), données de mission (vert)."""
    img = fond()
    d = ImageDraw.Draw(img, "RGBA")
    titre(d, "Architecture du SA-1")
    blocs = {
        "bat": ("Batterie LiPo 6S", (90, 260)), "pm": ("Module de puissance", (90, 420)),
        "escv": ("4 ESC 40 A", (470, 230)), "mv": ("4 moteurs VTOL", (850, 230)),
        "escc": ("ESC 60 A", (470, 330)), "mc": ("Moteur de croisière", (850, 330)),
        "bec1": ("BEC servos", (470, 430)), "servo": ("4 servos gouvernes", (850, 430)),
        "fc": ("Contrôleur de vol (ArduPilot)", (470, 600)), "bec2": ("BEC 5 V / 5 A", (90, 600)),
        "pi": ("Raspberry Pi 5 + AI HAT+", (90, 900)), "cam": ("Nacelle jour/nuit", (470, 900)),
        "gnss": ("GNSS + compas", (1250, 520)), "pitot": ("Vitesse air", (1250, 600)),
        "lidar": ("Télémètre laser", (1250, 680)), "rc": ("Récepteur RC", (1250, 760)),
        "tel": ("Radio télémétrie", (720, 790)), "gcs": ("Station sol", (1430, 900)),
    }
    larg, haut = 330, 60
    pos = {}
    for cle, (nom, (x, y)) in blocs.items():
        couleur = VERT if cle in ("pi", "cam", "gcs") else CYAN if cle in ("fc", "tel") else CYAN_SOMBRE
        panneau(d, (x, y, x + larg, y + haut), 1, couleur, rayon=10)
        texte(d, (x + larg / 2, y + haut / 2), nom, "demi", 22, BLANC, 1, "mm")
        pos[cle] = (x, y)

    def relier(a, b, couleur, pointille=False):
        (xa, ya), (xb, yb) = pos[a], pos[b]
        p1 = (xa + larg, ya + haut / 2) if xb > xa else (xa + larg / 2, ya + haut)
        p2 = (xb, yb + haut / 2) if xb > xa else (xb + larg / 2, yb)
        if pointille:
            ligne_pointillee(d, p1, p2, couleur, 1, 3)
        else:
            fleche(d, p1, p2, couleur, 1, 3, 12)

    for a, b in [("bat", "pm"), ("pm", "escv"), ("pm", "escc"), ("pm", "bec1"), ("pm", "bec2"), ("pm", "fc")]:
        relier(a, b, ROUGE)
    for a, b in [("escv", "mv"), ("escc", "mc"), ("bec1", "servo"), ("bec2", "pi")]:
        relier(a, b, ROUGE)
    for capteur in ("gnss", "pitot", "lidar", "rc"):
        (xa, ya), (xf, yf) = pos[capteur], pos["fc"]
        fleche(d, (xa, ya + haut / 2), (xf + larg, yf + haut / 2), CYAN, 1, 3, 12)
    # bus de commande : du contrôleur vers les ESC et les servos, par la droite des blocs
    (xf, yf) = pos["fc"]
    d.line([(xf + larg, yf + 15), (xf + larg + 22, yf + 15), (xf + larg + 22, pos["escv"][1] + 48)],
           fill=avec_alpha(CYAN, 1), width=3)
    for cible in ("escv", "escc", "bec1"):
        (xc, yc) = pos[cible]
        fleche(d, (xf + larg + 22, yc + 48), (xc + larg + 2, yc + 48), CYAN, 1, 3, 10)
    fleche(d, (pos["cam"][0], pos["cam"][1] + haut / 2), (pos["pi"][0] + larg, pos["pi"][1] + haut / 2), VERT, 1, 3, 12)
    fleche(d, (pos["pi"][0] + larg / 2, pos["pi"][1]), (pos["fc"][0], pos["fc"][1] + haut), VERT, 1, 3, 12)
    fleche(d, (pos["fc"][0] + larg / 2, pos["fc"][1] + haut), (pos["tel"][0], pos["tel"][1] + haut / 2), CYAN, 1, 3, 12)
    ligne_pointillee(d, (pos["tel"][0] + larg, pos["tel"][1] + haut / 2), (pos["gcs"][0], pos["gcs"][1] + haut / 2),
                     CYAN, 1, 3, 14, 10)
    texte(d, (1250, 940), "liaison chiffrée et signée", "normal", 22, CYAN, 1, "mm")
    for k, (nom, couleur) in enumerate([("Énergie", ROUGE), ("Commande et capteurs de vol", CYAN), ("Mission (caméra, IA)", VERT)]):
        d.line([(1280, 260 + k * 50), (1330, 260 + k * 50)], fill=avec_alpha(couleur, 1), width=5)
        texte(d, (1345, 260 + k * 50), nom, "demi", 24, BLANC, 1, "lm")
    return img


def main():
    SORTIE.mkdir(parents=True, exist_ok=True)
    plan, _, _ = timeline.construire(contenu.SCENES, None)
    for p in plan:
        scene = p["scene"]
        if scene["titre"] not in SCENES:
            continue
        nom, f = SCENES[scene["titre"]]
        img = fond()
        d = ImageDraw.Draw(img, "RGBA")
        titre(d, scene["titre"])
        marques = [debut for _, debut, _ in p["phrases"]]
        SCENES_VISUELLES[scene.get("visuel", scene["id"])](d, p["duree"] * f, p["duree"], marques, scene)
        img.save(SORTIE / nom)
        print(nom)
    vue_annotee().save(SORTIE / "vue_de_dessus_annotee.png")
    architecture().save(SORTIE / "architecture.png")
    profil_annote().save(SORTIE / "vue_de_cote.png")
    print("vue_de_dessus_annotee.png, vue_de_cote.png")


if __name__ == "__main__":
    main()
