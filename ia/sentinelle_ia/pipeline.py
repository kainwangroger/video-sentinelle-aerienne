"""Chaîne unique : capture -> inférence -> zone -> suivi -> événement et preuve -> journal -> liaison."""

import logging
import time

from . import STATUT_A_VERIFIER
from .alerte import creer_evenement, enregistrer_preuve
from .config import chemin
from .detecteurs import creer_detecteur
from .journal import Journal
from .liaison import Emetteur, creer_liaison
from .metriques import Metriques
from .suivi import ParametresSuivi, Suivi
from .zone import ZoneInteret

log = logging.getLogger("sentinelle_ia")


class Pipeline:
    def __init__(self, config, detecteur=None, liaison=None, fournisseur_telemetrie=None):
        self.config = config
        cd = dict(config["detecteur"])
        for cle in ("modele", "annotations"):
            if cd.get(cle):
                cd[cle] = chemin(config, cd[cle])
        self.detecteur = detecteur or creer_detecteur(cd)
        self.zone = ZoneInteret(config["zone_interet"].get("polygone"))
        self.parametres_suivi = ParametresSuivi(**config["suivi"])
        self.suivi = Suivi(self.parametres_suivi)
        self.anomalie = None
        ca = config["anomalie"]
        if ca.get("active"):
            from .anomalie import DetecteurAnomalie
            self.anomalie = DetecteurAnomalie(chemin(config, ca["reference"]), ca["seuil_alignement"],
                                              ca["seuil_difference"], ca["aire_min"])
        self.dossier_preuves = chemin(config, config["alerte"]["dossier_preuves"])
        self.journal = Journal(chemin(config, config["journal"]["base"]))
        cl = dict(config["liaison"])
        if cl.get("dossier"):
            cl["dossier"] = chemin(config, cl["dossier"])
        self.liaison = liaison if liaison is not None else creer_liaison(cl)
        self.emetteur = None
        if self.liaison is not None:
            self.emetteur = Emetteur(self.journal, self.liaison, config["alerte"].get("inclure_image_dans_message", True))
        cm = config["metriques"]
        self.metriques = Metriques(chemin(config, cm.get("csv")), cm.get("periode", 5.0))
        self.fournisseur_telemetrie = fournisseur_telemetrie
        self.evenements = 0
        self.dernieres_detections = []

    def traiter(self, image):
        """Traite une image ; renvoie la liste des événements créés."""
        t0 = time.monotonic()
        w, h = image.taille
        detections = self.detecteur.detecter(image.pixels)
        duree_inference = time.monotonic() - t0
        if self.anomalie is not None:
            detections += self.anomalie.detecter(image.pixels)
        detections = self.zone.filtrer(detections, w, h)
        self.dernieres_detections = detections
        confirmees = self.suivi.mettre_a_jour(image.numero, detections, (w, h))

        crees = []
        for piste in confirmees:
            telemetrie = self.fournisseur_telemetrie() if self.fournisseur_telemetrie else None
            evenement = creer_evenement(piste, image, self.parametres_suivi, telemetrie)
            enregistrer_preuve(evenement, image, self.dossier_preuves)
            self.journal.ajouter(evenement)
            crees.append(evenement)
            self.evenements += 1
            etiquette = evenement.classe if evenement.statut != STATUT_A_VERIFIER else f"à vérifier ({evenement.classe})"
            log.info("Alerte %s : %s, score %.2f, image %d", evenement.id[:8], etiquette, evenement.score, image.numero)
        if crees and self.emetteur is not None:
            self.emetteur.signaler()
        # latence image -> décision (alerte écrite dans le journal) depuis la capture
        self.metriques.enregistrer(duree_inference, time.monotonic() - image.monotone)
        if self.metriques.peut_ecrire():
            self.metriques.ecrire(self.evenements, self.journal.compter("en_attente"))
        return crees

    def executer(self, capture, sortie_video=None, duree_max=None, afficher_progression=True):
        """Boucle principale ; s'arrête en fin de flux, après duree_max secondes ou sur Ctrl+C."""
        if self.emetteur is not None:
            self.emetteur.start()
        ecrivain = None
        debut = time.monotonic()
        try:
            while True:
                image = capture.lire()
                if image is None or (duree_max and time.monotonic() - debut > duree_max):
                    break
                self.traiter(image)
                if sortie_video:
                    ecrivain = ecrivain or _ouvrir_video(sortie_video, image, capture.fps_source or 25)
                    ecrivain.write(self.annoter(image))
                if afficher_progression and image.numero % 100 == 0:
                    r = self.metriques.resume()
                    log.info("image %d | %s img/s | inférence p50 %s ms | %d alertes", image.numero, r["fps"],
                             r["inference_ms_p50"], self.evenements)
        except KeyboardInterrupt:
            log.info("Arrêt demandé")
        finally:
            if ecrivain is not None:
                ecrivain.release()
            self.fermer()
        return self.metriques.resume()

    def annoter(self, image):
        """Image annotée pour la démonstration : zone, détections, pistes confirmées."""
        import cv2
        import numpy as np

        sortie = image.pixels.copy()
        w, h = image.taille
        cv2.polylines(sortie, [np.array(self.zone.en_pixels(w, h), np.int32)], True, (255, 200, 0), 2)
        for d in self.dernieres_detections:
            x1, y1, x2, y2 = [int(v) for v in d.boite]
            cv2.rectangle(sortie, (x1, y1), (x2, y2), (180, 180, 180), 1)
        for piste in self.suivi.pistes.values():
            if piste.alerte_emise and piste.derniere_image == image.numero:
                classe, statut, score = piste.classe_et_statut(self.parametres_suivi)
                couleur = (0, 190, 255) if statut == STATUT_A_VERIFIER else (60, 220, 150)
                x1, y1, x2, y2 = [int(v) for v in piste.boite]
                cv2.rectangle(sortie, (x1, y1), (x2, y2), couleur, 2)
                texte = f"#{piste.id} {classe or 'objet'}" + (" ?" if statut == STATUT_A_VERIFIER else "")
                cv2.putText(sortie, texte, (x1, max(15, y1 - 6)), cv2.FONT_HERSHEY_SIMPLEX, 0.55, couleur, 2, cv2.LINE_AA)
        cv2.putText(sortie, f"alertes: {self.evenements}  en attente: {self.journal.compter('en_attente')}",
                    (10, h - 12), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2, cv2.LINE_AA)
        return sortie

    def fermer(self):
        if self.emetteur is not None and self.emetteur.is_alive():
            self.emetteur.arreter()
        if hasattr(self.detecteur, "fermer"):
            self.detecteur.fermer()
        self.metriques.ecrire(self.evenements, self.journal.compter("en_attente"))
        self.metriques.fermer()


def _ouvrir_video(chemin_sortie, image, fps):
    import cv2

    w, h = image.taille
    return cv2.VideoWriter(str(chemin_sortie), cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))
