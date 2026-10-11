"""Capture du flux caméra réellement fourni et horodatage des images.

Sources acceptées (clé `capture.source` de la configuration) :
- chemin d'une vidéo enregistrée (validation sur vidéos) ;
- entier : index d'un périphérique V4L2 (/dev/videoN), ex. carte d'acquisition HDMI/USB
  reliée à la sortie de la nacelle ;
- URL rtsp:// ou udp:// : flux réseau fourni par l'encodeur de la caméra ;
- chaîne GStreamer (contenant « ! ») ;
- "picamera2" : module caméra CSI du Raspberry Pi (Picamera2).
"""

import time

from .types import Image


class Capture:
    def __init__(self, source, largeur=None, hauteur=None, sequence_id="SEQ", cadence_max=None, boucle=False):
        self.source = source
        self.sequence_id = sequence_id
        self.cadence_max = cadence_max
        self.boucle = boucle
        self.numero = 0
        self._dernier = 0.0
        self.images_perdues = 0
        self._picam = None
        if source == "picamera2":
            from picamera2 import Picamera2

            self._picam = Picamera2()
            taille = (largeur or 1920, hauteur or 1080)
            self._picam.configure(self._picam.create_video_configuration(main={"size": taille, "format": "BGR888"}))
            self._picam.start()
        else:
            import cv2

            self.cv2 = cv2
            if isinstance(source, str) and source.isdigit():
                source = int(source)
            api = cv2.CAP_GSTREAMER if isinstance(source, str) and "!" in source else cv2.CAP_ANY
            self._cap = cv2.VideoCapture(source, api)
            if not self._cap.isOpened():
                raise RuntimeError(f"Impossible d'ouvrir la source vidéo : {self.source}")
            if largeur and hauteur and isinstance(source, int):
                self._cap.set(cv2.CAP_PROP_FRAME_WIDTH, largeur)
                self._cap.set(cv2.CAP_PROP_FRAME_HEIGHT, hauteur)

    @property
    def fps_source(self):
        if self._picam is not None:
            return None
        fps = self._cap.get(self.cv2.CAP_PROP_FPS)
        return fps if fps and fps > 0 else None

    def lire(self):
        """Renvoie la prochaine Image, ou None en fin de flux."""
        if self.cadence_max:
            attente = 1.0 / self.cadence_max - (time.monotonic() - self._dernier)
            if attente > 0:
                time.sleep(attente)
        if self._picam is not None:
            pixels = self._picam.capture_array()
        else:
            ok, pixels = self._cap.read()
            if not ok and self.boucle:
                self._cap.set(self.cv2.CAP_PROP_POS_FRAMES, 0)
                ok, pixels = self._cap.read()
            if not ok:
                return None
        self._dernier = time.monotonic()
        image = Image(pixels, self.numero, time.time(), self._dernier, self.sequence_id)
        self.numero += 1
        return image

    def fermer(self):
        if self._picam is not None:
            self._picam.stop()
        else:
            self._cap.release()
