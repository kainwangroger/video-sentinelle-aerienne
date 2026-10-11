import json
import time

import numpy as np

from sentinelle_ia import STATUT_CONFIRME
from sentinelle_ia.alerte import creer_evenement, enregistrer_preuve
from sentinelle_ia.journal import Journal
from sentinelle_ia.liaison import Emetteur, LiaisonDossier
from sentinelle_ia.suivi import ParametresSuivi, Suivi
from sentinelle_ia.types import Detection, Image


def _evenement(tmp_path):
    suivi = Suivi(ParametresSuivi(images_confirmation=2))
    pixels = np.full((360, 640, 3), 90, np.uint8)
    confirmees = []
    for n in range(3):
        image = Image(pixels, n, time.time(), time.monotonic(), "TEST-1")
        confirmees += suivi.mettre_a_jour(n, [Detection("debris", 0.8, (300, 150, 330, 170))])
        if confirmees:
            break
    ev = creer_evenement(confirmees[0], image, suivi.p)
    enregistrer_preuve(ev, image, tmp_path / "preuves")
    return ev


def test_evenement_complet(tmp_path):
    ev = _evenement(tmp_path)
    assert ev.statut == STATUT_CONFIRME and ev.classe == "debris"
    assert ev.position is None  # pas de position au sol sans calibration
    message = ev.message(inclure_image=True)
    for cle in ("horodatage", "classe", "statut", "score", "boite", "sequence_id", "image_preuve_jpeg_base64"):
        assert cle in message
    assert "statut_transmission" not in message


def test_conforme_au_schema(tmp_path):
    import jsonschema  # noqa: F401  (optionnel)
    from pathlib import Path
    schema = json.loads((Path(__file__).resolve().parent.parent / "schemas" / "evenement.schema.json").read_text())
    jsonschema.validate(_evenement(tmp_path).message(inclure_image=True), schema)


def test_hors_connexion_puis_reprise(tmp_path):
    journal = Journal(tmp_path / "j.sqlite")
    liaison = LiaisonDossier(tmp_path / "station")
    liaison.disponible = False
    emetteur = Emetteur(journal, liaison)
    for _ in range(3):
        journal.ajouter(_evenement(tmp_path))
    assert emetteur.vider() == 0
    assert journal.compter("en_attente") == 3      # stockés localement pendant la coupure
    liaison.disponible = True
    assert emetteur.vider() == 3
    assert journal.compter("en_attente") == 0
    assert len(list((tmp_path / "station").glob("*.json"))) == 3


def test_journal_persiste_apres_redemarrage(tmp_path):
    j = Journal(tmp_path / "j.sqlite")
    j.ajouter(_evenement(tmp_path))
    j.fermer()
    assert Journal(tmp_path / "j.sqlite").compter("en_attente") == 1
