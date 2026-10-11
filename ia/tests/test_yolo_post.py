import numpy as np

from sentinelle_ia.detecteurs.tuiles import DetecteurTuiles
from sentinelle_ia.detecteurs.yolo import decoder_yolov8, letterbox, nms, vers_image_origine
from sentinelle_ia.types import Detection


def test_nms_supprime_les_doublons():
    boites = np.array([[0, 0, 10, 10], [1, 1, 11, 11], [50, 50, 60, 60]], np.float32)
    scores = np.array([0.9, 0.8, 0.7])
    assert list(nms(boites, scores, 0.5)) == [0, 2]


def test_decodage_sortie_yolov8():
    nc, n = 3, 5
    sortie = np.zeros((1, 4 + nc, n), np.float32)
    sortie[0, :4, 0] = [100, 100, 20, 20]   # cx cy w h
    sortie[0, 4 + 2, 0] = 0.9               # classe debris
    sortie[0, :4, 1] = [101, 101, 20, 20]   # doublon
    sortie[0, 4 + 2, 1] = 0.6
    sortie[0, :4, 2] = [300, 300, 40, 40]
    sortie[0, 4 + 0, 2] = 0.1               # sous le seuil
    boites, scores, classes = decoder_yolov8(sortie, seuil_score=0.15)
    assert len(boites) == 1 and classes[0] == 2
    assert np.allclose(boites[0], [90, 90, 110, 110])


def test_letterbox_aller_retour():
    image = np.zeros((360, 1280, 3), np.uint8)
    carre, echelle, decalage = letterbox(image, 640)
    assert carre.shape == (640, 640, 3)
    boite = np.array([[decalage[0] + 64 * echelle * 10, decalage[1] + 0, decalage[0] + 640, decalage[1] + 100]], np.float32)
    origine = vers_image_origine(boite, echelle, decalage, 1280, 360)
    assert np.allclose(origine[0, [0, 2]], [640, 1280], atol=1)


class _Fixe:
    """Détecteur qui trouve un objet à une position absolue fixe."""

    def __init__(self, boite_absolue, taille_image):
        self.boite, self.taille = boite_absolue, taille_image
        self.appels = []

    def detecter(self, image):
        self.appels.append(image.shape)
        if image.shape[:2] == self.taille:
            return [Detection("debris", 0.6, self.boite)]
        return [Detection("debris", 0.8, (5, 5, 15, 15))]


def test_tuiles_recalent_et_fusionnent():
    base = _Fixe((6, 6, 16, 16), (400, 400))
    det = DetecteurTuiles(base, (2, 2), 0.2, image_entiere=True)
    resultat = det.detecter(np.zeros((400, 400, 3), np.uint8))
    assert len(base.appels) == 5
    # la tuile en haut à gauche retrouve l'objet de l'image entière -> fusion par NMS
    assert any(abs(d.boite[0] - 5) < 1e-6 for d in resultat)
    assert len(resultat) == 4
