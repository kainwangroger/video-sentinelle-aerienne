"""Chaîne complète sur une petite vidéo synthétique avec le détecteur factice."""

import json

import pytest

from sentinelle_ia.capture import Capture
from sentinelle_ia.config import charger
from sentinelle_ia.pipeline import Pipeline


@pytest.fixture(scope="module")
def donnees(tmp_path_factory):
    import numpy as np
    from generer_donnees_synthetiques import generer_demo

    dossier = tmp_path_factory.mktemp("synth")
    generer_demo(dossier, np.random.default_rng(1), duree=6, fps=10, largeur=640, hauteur=360)
    return dossier


def test_chaine_complete(donnees, tmp_path):
    annotations = json.loads((donnees / "piste_demo_annotations.json").read_text())
    objets_vus = {tuple(o["boite"]) for v in annotations.values() for o in v}
    config = charger(None, {
        "capture": {"source": str(donnees / "piste_demo.mp4")},
        "detecteur": {"moteur": "factice", "annotations": str(donnees / "piste_demo_annotations.json"),
                      "taux_oubli": 0.1, "taux_fausse_detection": 0.2},
        "alerte": {"dossier_preuves": str(tmp_path / "preuves")},
        "journal": {"base": str(tmp_path / "j.sqlite")},
        "liaison": {"type": "dossier", "dossier": str(tmp_path / "station")},
        "metriques": {"csv": str(tmp_path / "m.csv")},
    })
    capture = Capture(config["capture"]["source"], sequence_id="TEST")
    pipeline = Pipeline(config)
    pipeline.executer(capture, afficher_progression=False)
    assert capture.numero == 60
    assert pipeline.evenements >= 1
    assert pipeline.journal.compter("en_attente") == 0
    assert len(list((tmp_path / "station").glob("*.json"))) == pipeline.evenements
    assert len(list((tmp_path / "preuves").glob("*.jpg"))) == pipeline.evenements
    assert (tmp_path / "m.csv").read_text().count("\n") >= 2
    assert objets_vus  # la vidéo contient bien des objets
