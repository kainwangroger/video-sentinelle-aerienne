"""Chargement de la configuration YAML, avec valeurs par défaut."""

import copy
from pathlib import Path

import yaml

DEFAUT = {
    "mission": {"sequence_id": "SEQ"},
    "capture": {"source": 0, "largeur": None, "hauteur": None, "cadence_max": None, "boucle": False},
    "detecteur": {
        "moteur": "onnx",
        "modele": "modeles/sentinelle_yolov8s.onnx",
        "classes": ["personne", "vehicule", "debris"],
        "taille_entree": 640,
        "seuil_candidat": 0.15,   # en dessous : ignoré
        "seuil_iou": 0.45,
    },
    "zone_interet": {"polygone": None},
    "suivi": {},
    "anomalie": {"active": False, "reference": None, "seuil_alignement": 0.85, "seuil_difference": 40,
                 "aire_min": 80},
    "alerte": {"dossier_preuves": "travail/preuves", "inclure_image_dans_message": True},
    "journal": {"base": "travail/journal.sqlite"},
    "liaison": {"type": "aucune"},
    "metriques": {"csv": "travail/metriques.csv", "periode": 5.0},
}


def fusionner(base, ajout):
    resultat = copy.deepcopy(base)
    for cle, valeur in (ajout or {}).items():
        if isinstance(valeur, dict) and isinstance(resultat.get(cle), dict):
            resultat[cle] = fusionner(resultat[cle], valeur)
        else:
            resultat[cle] = valeur
    return resultat


def charger(chemin=None, surcharges=None):
    """Charge le YAML ; les chemins relatifs sont résolus depuis le dossier du fichier."""
    donnees = {}
    racine = Path.cwd()
    if chemin:
        chemin = Path(chemin)
        donnees = yaml.safe_load(chemin.read_text(encoding="utf-8")) or {}
        racine = chemin.resolve().parent.parent if chemin.resolve().parent.name == "configs" else chemin.resolve().parent
    config = fusionner(fusionner(DEFAUT, donnees), surcharges)
    config["_racine"] = str(racine)
    return config


def chemin(config, valeur):
    """Résout un chemin de la configuration par rapport à la racine du module (dossier ia/)."""
    if valeur is None:
        return None
    p = Path(valeur)
    return str(p if p.is_absolute() else Path(config["_racine"]) / p)
