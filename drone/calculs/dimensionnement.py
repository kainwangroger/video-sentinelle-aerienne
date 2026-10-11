"""Dimensionnement de référence du drone Sentinelle Aérienne SA-1 (VTOL quadplane).

Ce script calcule, à partir d'hypothèses écrites en clair, les grandeurs de la fiche
technique : masses, surface d'aile, vitesse de décrochage, poussée et puissance en vol
stationnaire, puissance en croisière, énergie et autonomie estimée.

Ce sont des ESTIMATIONS de conception (ordre de grandeur) : elles doivent être confirmées
par les essais (banc de poussée, pesée, vols d'essai). Usage :

    python drone/calculs/dimensionnement.py            # affiche le résumé
    python drone/calculs/dimensionnement.py --markdown # écrit drone/calculs/resultats.md
"""

import argparse
import math
from pathlib import Path

G = 9.81

# ------------------------------------------------------------------ hypothèses (modifiables)

# Conditions : Togo, chaud et humide, près du niveau de la mer.
TEMPERATURE_C = 35.0
ALTITUDE_M = 100.0

# Bilan de masse (kg) : composants de référence, à remplacer par les pesées réelles.
MASSES = {
    "Cellule : aile, fuselage, poutres, empennage (carbone/composite)": 1.90,
    "4 moteurs de sustentation (classe 4014, ~150 g)": 0.62,
    "4 contrôleurs ESC 40 A": 0.16,
    "4 hélices de sustentation 15 pouces carbone": 0.08,
    "Moteur de croisière (classe 3520) + ESC 60 A + hélice 13 pouces": 0.29,
    "4 servomoteurs de gouvernes": 0.12,
    "Batterie LiPo 6S 16 000 mAh": 2.05,
    "Contrôleur de vol + module de puissance": 0.10,
    "GNSS + compas, capteur de vitesse air, télémètre laser": 0.10,
    "Radio télémétrie + récepteur RC + antennes": 0.06,
    "Raspberry Pi 5 + AI HAT+ 26 TOPS + boîtier ventilé": 0.12,
    "Nacelle gyrostabilisée + caméra visible + module thermique": 0.35,
    "Câblage, connecteurs, BEC, fixations": 0.25,
}
MARGE_MASSE_KG = 0.20          # réserve pour les imprévus d'intégration

# Aile
ENVERGURE_M = 2.00
CORDE_MOYENNE_M = 0.28
CL_MAX = 1.3                    # profil avec volets neutres
FINESSE_CROISIERE = 8.5         # L/D estimée, prudente (poutres, rotors arrêtés et nacelle ajoutent de la traînée)
VITESSE_CROISIERE_MS = 19.0

# Sustentation verticale
NB_ROTORS = 4
DIAMETRE_HELICE_M = 0.381       # 15 pouces
FIGURE_MERITE = 0.60            # efficacité aérodynamique d'une hélice en stationnaire
RENDEMENT_MOTEUR_ESC = 0.80
RAPPORT_POUSSEE_POIDS = 1.8     # marge pour les rafales et le contrôle
DUREE_STATIONNAIRE_S = 120      # décollage + atterrissage + marges

# Croisière
RENDEMENT_PROPULSION_CROISIERE = 0.55   # hélice x moteur x ESC
PUISSANCE_ELECTRONIQUE_W = 25.0         # FC, radio, Pi 5 + HAT, nacelle, capteurs

# Batterie
CELLULES = 6
TENSION_NOMINALE_CELLULE = 3.7
CAPACITE_AH = 16.0
PART_UTILISABLE = 0.80          # on ne vide jamais une LiPo sous ~20 %
RESERVE_ATTERRISSAGE_WH = 15.0  # énergie gardée pour un atterrissage vertical de secours


# ------------------------------------------------------------------ calculs

def densite_air(temperature_c, altitude_m):
    """Atmosphère standard corrigée de la température (kg/m³)."""
    pression = 101325 * (1 - 2.25577e-5 * altitude_m) ** 5.25588
    return pression / (287.05 * (temperature_c + 273.15))


def calculer():
    r = {}
    rho = densite_air(TEMPERATURE_C, ALTITUDE_M)
    r["densite_air"] = rho
    masse_composants = sum(MASSES.values())
    masse = masse_composants + MARGE_MASSE_KG
    poids = masse * G
    r.update(masse_composants=masse_composants, masse_totale=masse, poids_n=poids)

    surface = ENVERGURE_M * CORDE_MOYENNE_M
    r["surface_aile"] = surface
    r["allongement"] = ENVERGURE_M ** 2 / surface
    r["charge_alaire"] = masse / surface
    r["vitesse_decrochage"] = math.sqrt(2 * poids / (rho * surface * CL_MAX))
    r["vitesse_transition_min"] = 1.25 * r["vitesse_decrochage"]
    r["cl_croisiere"] = 2 * poids / (rho * VITESSE_CROISIERE_MS ** 2 * surface)

    # stationnaire : théorie de la quantité de mouvement (disque sustentateur)
    aire_disque = NB_ROTORS * math.pi * (DIAMETRE_HELICE_M / 2) ** 2
    puissance_ideale = poids ** 1.5 / math.sqrt(2 * rho * aire_disque)
    r["poussee_max_par_moteur_kgf"] = masse * RAPPORT_POUSSEE_POIDS / NB_ROTORS
    r["puissance_stationnaire_w"] = puissance_ideale / (FIGURE_MERITE * RENDEMENT_MOTEUR_ESC) + PUISSANCE_ELECTRONIQUE_W
    r["courant_stationnaire_a"] = r["puissance_stationnaire_w"] / (CELLULES * TENSION_NOMINALE_CELLULE)

    # croisière : traînée = poids / finesse
    trainee = poids / FINESSE_CROISIERE
    r["trainee_croisiere_n"] = trainee
    r["puissance_croisiere_w"] = trainee * VITESSE_CROISIERE_MS / RENDEMENT_PROPULSION_CROISIERE + PUISSANCE_ELECTRONIQUE_W
    r["courant_croisiere_a"] = r["puissance_croisiere_w"] / (CELLULES * TENSION_NOMINALE_CELLULE)

    energie = CELLULES * TENSION_NOMINALE_CELLULE * CAPACITE_AH
    utilisable = energie * PART_UTILISABLE
    stationnaire_wh = r["puissance_stationnaire_w"] * DUREE_STATIONNAIRE_S / 3600
    croisiere_wh = utilisable - stationnaire_wh - RESERVE_ATTERRISSAGE_WH
    r.update(energie_wh=energie, energie_utilisable_wh=utilisable, energie_stationnaire_wh=stationnaire_wh)
    r["autonomie_croisiere_min"] = croisiere_wh / r["puissance_croisiere_w"] * 60
    r["autonomie_totale_min"] = r["autonomie_croisiere_min"] + DUREE_STATIONNAIRE_S / 60
    r["distance_km"] = VITESSE_CROISIERE_MS * r["autonomie_croisiere_min"] * 60 / 1000
    r["c_rate_stationnaire"] = r["courant_stationnaire_a"] / CAPACITE_AH
    return r


def resume(r):
    lignes = [
        ("Densité de l'air (35 °C)", f"{r['densite_air']:.3f} kg/m³"),
        ("Masse des composants", f"{r['masse_composants']:.2f} kg"),
        ("Masse maximale au décollage (avec marge)", f"{r['masse_totale']:.2f} kg"),
        ("Surface alaire", f"{r['surface_aile']:.2f} m²"),
        ("Allongement", f"{r['allongement']:.1f}"),
        ("Charge alaire", f"{r['charge_alaire']:.1f} kg/m²"),
        ("Vitesse de décrochage", f"{r['vitesse_decrochage']:.1f} m/s ({r['vitesse_decrochage'] * 3.6:.0f} km/h)"),
        ("Vitesse minimale de fin de transition (1,25 × décrochage)", f"{r['vitesse_transition_min']:.1f} m/s"),
        ("Coefficient de portance en croisière", f"{r['cl_croisiere']:.2f}"),
        ("Poussée maximale requise par moteur VTOL", f"{r['poussee_max_par_moteur_kgf']:.1f} kgf"),
        ("Puissance en vol stationnaire", f"{r['puissance_stationnaire_w']:.0f} W ({r['courant_stationnaire_a']:.0f} A, {r['c_rate_stationnaire']:.1f} C)"),
        ("Traînée en croisière", f"{r['trainee_croisiere_n']:.1f} N"),
        ("Puissance en croisière", f"{r['puissance_croisiere_w']:.0f} W ({r['courant_croisiere_a']:.1f} A)"),
        ("Énergie de la batterie", f"{r['energie_wh']:.0f} Wh (utilisable {r['energie_utilisable_wh']:.0f} Wh)"),
        ("Énergie du vol stationnaire (2 min)", f"{r['energie_stationnaire_wh']:.0f} Wh"),
        ("Autonomie estimée (croisière + stationnaire)", f"{r['autonomie_totale_min']:.0f} min"),
        ("Distance parcourable en croisière", f"{r['distance_km']:.0f} km"),
    ]
    return lignes


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--markdown", action="store_true")
    args = parser.parse_args()
    r = calculer()
    lignes = resume(r)
    for k, v in lignes:
        print(f"{k:<62} {v}")
    if args.markdown:
        md = ["# Résultats du dimensionnement (estimations)", "",
              "Généré par `python drone/calculs/dimensionnement.py --markdown`. Hypothèses en tête du script.", "",
              "| Grandeur | Valeur |", "|---|---|"] + [f"| {k} | {v} |" for k, v in lignes]
        md += ["", "## Bilan de masse", "", "| Élément | Masse (kg) |", "|---|---|"]
        md += [f"| {k} | {v:.2f} |" for k, v in MASSES.items()]
        md += [f"| Marge d'intégration | {MARGE_MASSE_KG:.2f} |", f"| **Total** | **{r['masse_totale']:.2f}** |", "",
               "L'autonomie estimée dépasse la cible du concours (30–45 min) : la marge couvre le vent, la chaleur, "
               "le vieillissement de la batterie et les écarts entre estimation et réalité. Seuls les essais en vol font foi."]
        sortie = Path(__file__).with_name("resultats.md")
        sortie.write_text("\n".join(md) + "\n", encoding="utf-8")
        print(f"\nÉcrit : {sortie}")


if __name__ == "__main__":
    main()
