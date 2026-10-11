"""Inférence par tuiles : découpe l'image en grille avec recouvrement pour les petits objets.

Chaque tuile passe dans le détecteur à la taille d'entrée du modèle, ce qui grossit les
petits débris en pixels. Coût : une inférence par tuile (+ l'image entière si
`image_entiere`). À ne retenir que si la cadence mesurée sur Hailo reste compatible.
"""

import numpy as np

from ..types import Detection
from .yolo import nms


class DetecteurTuiles:
    def __init__(self, base, grille=(2, 2), recouvrement=0.2, image_entiere=True, seuil_iou=0.5):
        self.base = base
        self.colonnes, self.lignes = grille
        self.recouvrement = recouvrement
        self.image_entiere = image_entiere
        self.seuil_iou = seuil_iou

    def tuiles(self, largeur, hauteur):
        tw = largeur / (self.colonnes - (self.colonnes - 1) * self.recouvrement)
        th = hauteur / (self.lignes - (self.lignes - 1) * self.recouvrement)
        for j in range(self.lignes):
            for i in range(self.colonnes):
                x0 = int(round(i * tw * (1 - self.recouvrement)))
                y0 = int(round(j * th * (1 - self.recouvrement)))
                yield x0, y0, min(largeur, int(round(x0 + tw))), min(hauteur, int(round(y0 + th)))

    def detecter(self, image):
        h, w = image.shape[:2]
        toutes = list(self.base.detecter(image)) if self.image_entiere else []
        for x0, y0, x1, y1 in self.tuiles(w, h):
            for d in self.base.detecter(np.ascontiguousarray(image[y0:y1, x0:x1])):
                bx1, by1, bx2, by2 = d.boite
                toutes.append(Detection(d.classe, d.score, (bx1 + x0, by1 + y0, bx2 + x0, by2 + y0), d.source))
        if not toutes:
            return []
        classes = sorted({d.classe for d in toutes})
        boites = np.array([d.boite for d in toutes], np.float32)
        decalage = np.array([classes.index(d.classe) * 1e5 for d in toutes], np.float32)[:, None]
        scores = np.array([d.score for d in toutes], np.float32)
        return [toutes[i] for i in nms(boites + decalage, scores, self.seuil_iou)]

    def fermer(self):
        if hasattr(self.base, "fermer"):
            self.base.fermer()
