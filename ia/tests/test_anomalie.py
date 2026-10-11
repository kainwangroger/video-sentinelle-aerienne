import cv2
import numpy as np

from sentinelle_ia.anomalie import DetecteurAnomalie


def _piste(rng):
    img = np.full((360, 640, 3), 95, np.uint8)
    img = np.clip(img + rng.normal(0, 6, img.shape), 0, 255).astype(np.uint8)
    img = cv2.GaussianBlur(img, (3, 3), 0)
    for y in range(0, 360, 60):
        cv2.rectangle(img, (316, y), (324, y + 30), (230, 230, 230), -1)
    cv2.rectangle(img, (100, 0), (106, 360), (220, 220, 220), -1)
    cv2.rectangle(img, (534, 0), (540, 360), (220, 220, 220), -1)
    return img


def test_objet_nouveau_detecte_apres_recalage():
    rng = np.random.default_rng(0)
    reference = _piste(rng)
    courante = np.roll(reference, (6, 4), axis=(0, 1)).copy()   # léger déplacement du drone
    cv2.circle(courante, (420, 200), 14, (30, 30, 30), -1)       # objet inconnu
    det = DetecteurAnomalie(reference, seuil_alignement=0.6, aire_min=60)
    resultats = det.detecter(courante)
    assert det.dernier_coefficient > 0.6
    assert any(r.boite[0] <= 420 <= r.boite[2] and r.boite[1] <= 200 <= r.boite[3] for r in resultats)
    assert all(r.source == "anomalie" for r in resultats)


def test_pas_de_comparaison_si_alignement_douteux():
    rng = np.random.default_rng(0)
    det = DetecteurAnomalie(_piste(rng), seuil_alignement=0.95)
    autre = np.random.default_rng(5).integers(0, 255, (360, 640, 3), dtype=np.uint8)
    assert det.detecter(autre) == []
