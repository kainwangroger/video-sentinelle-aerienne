"""Suivi vidéo léger : relie les détections d'une image à l'autre.

Ce n'est pas un second modèle d'IA : association gloutonne par recouvrement (IoU), avec
repli sur la distance des centres quand le drone se déplace vite. Une piste est
« confirmée » quand l'objet persiste sur plusieurs images ; elle produit alors une seule
alerte, jamais répétée. Un objet immobile reste suivi tant qu'il est revu.

Seuls les candidats « suffisamment crédibles » (score moyen >= seuil_a_verifier) sont
signalés ; ce seuil se règle sur un jeu de validation contenant des scènes vides et difficiles.

Statut d'une piste confirmée :
- classe_confirmee : une classe domine les votes avec un score moyen suffisant ;
- a_verifier : candidat crédible mais sans classe stable ou fiable (ou issu de la
  détection d'anomalie) -> signalé prudemment comme « présence à vérifier ».
"""

import itertools
from collections import Counter
from dataclasses import dataclass, field

from . import STATUT_A_VERIFIER, STATUT_CONFIRME
from .types import iou


@dataclass
class ParametresSuivi:
    iou_min: float = 0.2              # recouvrement minimal pour associer
    distance_max: float = 1.5         # sinon : distance des centres / taille de la boîte
    images_confirmation: int = 3      # persistance requise avant alerte
    fenetre_confirmation: int = 6     # ... parmi ces dernières images
    images_perdues_max: int = 15      # piste supprimée après ce nombre d'images sans détection
    seuil_classe: float = 0.5         # score moyen minimal pour une classe confirmée
    seuil_a_verifier: float = 0.3     # score moyen minimal pour signaler un candidat « à vérifier »
    marge_bord: float = 0.03          # objet touchant le bord (fraction de l'image) : on attend qu'il entre
    images_max_au_bord: int = 12      # ... sauf s'il reste au bord aussi longtemps
    part_classe_min: float = 0.6      # part des votes de la classe majoritaire


@dataclass
class Piste:
    id: int
    boite: tuple
    derniere_image: int
    historique: list = field(default_factory=list)   # (numero_image, classe, score, source)
    alerte_emise: bool = False
    meilleure_detection: object = None

    def ajouter(self, numero, detection):
        self.boite = detection.boite
        self.derniere_image = numero
        self.historique.append((numero, detection.classe, detection.score, detection.source))
        self.historique = self.historique[-50:]
        if self.meilleure_detection is None or detection.score >= self.meilleure_detection.score:
            self.meilleure_detection = detection

    def score_moyen(self):
        return sum(sc for *_, sc, _ in self.historique) / len(self.historique) if self.historique else 0.0

    def vu_recemment(self, numero, fenetre):
        return sum(1 for n, *_ in self.historique if n > numero - fenetre)

    def classe_et_statut(self, p: ParametresSuivi):
        votes = Counter(c for _, c, _, s in self.historique if s == "detecteur")
        if not votes:
            return None, STATUT_A_VERIFIER, max((sc for *_, sc, _ in self.historique), default=0.0)
        classe, n = votes.most_common(1)[0]
        scores = [sc for _, c, sc, s in self.historique if c == classe and s == "detecteur"]
        moyenne = sum(scores) / len(scores)
        stable = n / sum(votes.values()) >= p.part_classe_min
        if stable and moyenne >= p.seuil_classe:
            return classe, STATUT_CONFIRME, moyenne
        return classe, STATUT_A_VERIFIER, moyenne


class Suivi:
    def __init__(self, parametres: ParametresSuivi = None):
        self.p = parametres or ParametresSuivi()
        self.pistes = {}
        self._ids = itertools.count(1)

    def _cout(self, piste, detection):
        """Plus petit = meilleur ; None si l'association est impossible."""
        recouvrement = iou(piste.boite, detection.boite)
        if recouvrement >= self.p.iou_min:
            return 1 - recouvrement
        px, py = (piste.boite[0] + piste.boite[2]) / 2, (piste.boite[1] + piste.boite[3]) / 2
        dx, dy = detection.centre
        taille = max(piste.boite[2] - piste.boite[0], piste.boite[3] - piste.boite[1], 1.0)
        distance = ((px - dx) ** 2 + (py - dy) ** 2) ** 0.5 / taille
        if distance <= self.p.distance_max:
            return 1 + distance
        return None

    def _au_bord(self, boite, taille):
        if not taille:
            return False
        w, h = taille
        mx, my = self.p.marge_bord * w, self.p.marge_bord * h
        return boite[0] < mx or boite[1] < my or boite[2] > w - mx or boite[3] > h - my

    def mettre_a_jour(self, numero, detections, taille_image=None):
        """Associe les détections de l'image `numero` ; renvoie les pistes nouvellement confirmées.

        `taille_image` (largeur, hauteur) permet d'attendre qu'un objet entrant soit entier
        dans l'image avant de le confirmer : meilleure preuve et meilleure classification.
        """
        couples = []
        for pid, piste in self.pistes.items():
            for j, det in enumerate(detections):
                cout = self._cout(piste, det)
                if cout is not None:
                    couples.append((cout, pid, j))
        couples.sort()
        pistes_prises, dets_prises = set(), set()
        for cout, pid, j in couples:
            if pid in pistes_prises or j in dets_prises:
                continue
            self.pistes[pid].ajouter(numero, detections[j])
            pistes_prises.add(pid)
            dets_prises.add(j)
        for j, det in enumerate(detections):
            if j not in dets_prises:
                pid = next(self._ids)
                piste = Piste(pid, det.boite, numero)
                piste.ajouter(numero, det)
                self.pistes[pid] = piste

        for pid in [pid for pid, pi in self.pistes.items() if numero - pi.derniere_image > self.p.images_perdues_max]:
            del self.pistes[pid]

        confirmees = []
        for piste in self.pistes.values():
            if not piste.alerte_emise and piste.derniere_image == numero and \
                    piste.vu_recemment(numero, self.p.fenetre_confirmation) >= self.p.images_confirmation and \
                    piste.score_moyen() >= self.p.seuil_a_verifier and \
                    (not self._au_bord(piste.boite, taille_image) or len(piste.historique) >= self.p.images_max_au_bord):
                piste.alerte_emise = True
                confirmees.append(piste)
        return confirmees
