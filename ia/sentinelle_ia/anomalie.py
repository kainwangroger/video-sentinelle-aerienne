"""Branche expérimentale : détection d'anomalie par rapport à une piste libre de référence.

Les images d'une piste libre forment la référence d'apparence. Comme le drone se
déplace, l'image observée est d'abord recalée sur la référence (ECC, transformation
affine). La comparaison n'est faite que si l'alignement est jugé fiable (coefficient de
corrélation ECC au-dessus du seuil) ; sinon la branche ne produit rien.

Les zones qui diffèrent fortement de la référence deviennent des candidats « à vérifier ».
Cette fonction ne garantit pas la reconnaissance de tout objet inconnu : elle est
désactivée par défaut et doit être validée sur les séquences du projet.
"""

import numpy as np

from .types import Detection


class DetecteurAnomalie:
    def __init__(self, reference, seuil_alignement=0.85, seuil_difference=40, aire_min=80, echelle=0.5):
        import cv2

        self.cv2 = cv2
        self.echelle = echelle
        ref = cv2.imread(reference) if isinstance(reference, str) else reference
        if ref is None:
            raise FileNotFoundError(f"Référence de piste introuvable : {reference}")
        self.reference = self._preparer(ref)
        self.seuil_alignement = seuil_alignement
        self.seuil_difference = seuil_difference
        self.aire_min = aire_min
        self.dernier_coefficient = None

    def _preparer(self, image):
        cv2 = self.cv2
        gris = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        petit = cv2.resize(gris, None, fx=self.echelle, fy=self.echelle, interpolation=cv2.INTER_AREA)
        return cv2.GaussianBlur(petit, (5, 5), 0)

    def detecter(self, image):
        cv2 = self.cv2
        courante = self._preparer(image)
        if courante.shape != self.reference.shape:
            courante = cv2.resize(courante, self.reference.shape[::-1])
        transformation = np.eye(2, 3, dtype=np.float32)
        try:
            coefficient, transformation = cv2.findTransformECC(
                self.reference, courante, transformation, cv2.MOTION_AFFINE,
                (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 50, 1e-4), None, 5)
        except cv2.error:
            self.dernier_coefficient = 0.0
            return []
        self.dernier_coefficient = float(coefficient)
        if coefficient < self.seuil_alignement:
            return []  # alignement pas assez fiable : on ne compare pas
        h, w = self.reference.shape
        recalee = cv2.warpAffine(courante, transformation, (w, h), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)
        valide = cv2.warpAffine(np.full_like(courante, 255), transformation, (w, h),
                                flags=cv2.INTER_NEAREST + cv2.WARP_INVERSE_MAP)
        diff = cv2.absdiff(recalee, self.reference)
        diff[valide == 0] = 0
        _, masque = cv2.threshold(diff, self.seuil_difference, 255, cv2.THRESH_BINARY)
        masque = cv2.morphologyEx(masque, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
        masque = cv2.dilate(masque, np.ones((5, 5), np.uint8))
        contours, _ = cv2.findContours(masque, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        sortie = []
        for c in contours:
            if cv2.contourArea(c) < self.aire_min * self.echelle ** 2:
                continue
            x, y, bw, bh = cv2.boundingRect(c)
            coins = np.array([[x, y], [x + bw, y], [x, y + bh], [x + bw, y + bh]], np.float32)
            # ECC : un point p de la référence correspond à transformation(p) dans l'image courante
            coins = cv2.transform(coins[None], transformation)[0] / self.echelle
            x1, y1 = coins.min(0)
            x2, y2 = coins.max(0)
            score = float(min(1.0, diff[y:y + bh, x:x + bw].mean() / 255 * 2))
            sortie.append(Detection("inconnu", score, (float(x1), float(y1), float(x2), float(y2)), source="anomalie"))
        return sortie
