"""Détecteur factice : rejoue les annotations d'une vidéo synthétique.

Permet de tester toute la chaîne (zone, suivi, alerte, journal, liaison) sans modèle
entraîné. Il ajoute du bruit, des oublis et des fausses détections pour exercer le
filtrage. Ne mesure en aucun cas la qualité d'un vrai détecteur.
"""

import json
import random

from ..types import Detection


class DetecteurFactice:
    def __init__(self, config):
        with open(config["annotations"], encoding="utf-8") as f:
            self.annotations = {int(k): v for k, v in json.load(f).items()}
        self.taux_oubli = float(config.get("taux_oubli", 0.1))
        self.taux_fausse = float(config.get("taux_fausse_detection", 0.05))
        self.rng = random.Random(config.get("graine", 0))
        self.numero = 0

    def detecter(self, image):
        h, w = image.shape[:2]
        sortie = []
        for objet in self.annotations.get(self.numero, []):
            if self.rng.random() < self.taux_oubli:
                continue
            x1, y1, x2, y2 = objet["boite"]
            bruit = lambda: self.rng.uniform(-2, 2)  # noqa: E731
            score = objet.get("score", self.rng.uniform(0.55, 0.95))
            sortie.append(Detection(objet["classe"], score, (x1 + bruit(), y1 + bruit(), x2 + bruit(), y2 + bruit())))
        if self.rng.random() < self.taux_fausse:  # artefact isolé (reflet, ombre)
            x, y = self.rng.uniform(0, w - 40), self.rng.uniform(0, h - 40)
            sortie.append(Detection("debris", self.rng.uniform(0.2, 0.45), (x, y, x + 30, y + 30)))
        self.numero += 1
        return sortie
