"""Structures de données partagées par toute la chaîne."""

from dataclasses import dataclass, field

import numpy as np


@dataclass
class Detection:
    """Sortie d'un détecteur pour un candidat : classe, score, rectangle (pixels, x1 y1 x2 y2)."""

    classe: str
    score: float
    boite: tuple
    source: str = "detecteur"  # "detecteur" ou "anomalie"

    @property
    def centre(self):
        x1, y1, x2, y2 = self.boite
        return (x1 + x2) / 2, (y1 + y2) / 2

    @property
    def aire(self):
        x1, y1, x2, y2 = self.boite
        return max(0.0, x2 - x1) * max(0.0, y2 - y1)


@dataclass
class Image:
    """Image capturée et horodatée."""

    pixels: np.ndarray          # BGR, uint8, HxWx3
    numero: int
    horodatage: float           # time.time() à la capture (s, UTC)
    monotone: float             # time.monotonic() à la capture, pour les latences
    sequence_id: str = "SEQ"
    meta: dict = field(default_factory=dict)

    @property
    def taille(self):
        h, w = self.pixels.shape[:2]
        return w, h


def iou(a, b):
    """Intersection sur union de deux rectangles (x1, y1, x2, y2)."""
    x1, y1 = max(a[0], b[0]), max(a[1], b[1])
    x2, y2 = min(a[2], b[2]), min(a[3], b[3])
    inter = max(0.0, x2 - x1) * max(0.0, y2 - y1)
    union = (a[2] - a[0]) * (a[3] - a[1]) + (b[2] - b[0]) * (b[3] - b[1]) - inter
    return inter / union if union > 0 else 0.0
