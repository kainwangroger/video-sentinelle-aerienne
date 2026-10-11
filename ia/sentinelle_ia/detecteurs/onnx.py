"""Détecteur YOLOv8 exporté en ONNX, exécuté avec onnxruntime (référence pour comparer au HEF)."""

import numpy as np

from ..types import Detection
from .yolo import decoder_yolov8, letterbox, vers_image_origine


class DetecteurOnnx:
    def __init__(self, config):
        import onnxruntime as ort

        self.classes = list(config["classes"])
        self.taille = int(config.get("taille_entree", 640))
        self.seuil_candidat = float(config.get("seuil_candidat", 0.15))
        self.seuil_iou = float(config.get("seuil_iou", 0.45))
        options = ort.SessionOptions()
        options.intra_op_num_threads = int(config.get("threads", 4))
        self.session = ort.InferenceSession(config["modele"], options, providers=["CPUExecutionProvider"])
        self.entree = self.session.get_inputs()[0].name

    def detecter(self, image):
        h, w = image.shape[:2]
        carre, echelle, decalage = letterbox(image, self.taille)
        tenseur = carre[:, :, ::-1].transpose(2, 0, 1)[None].astype(np.float32) / 255.0  # BGR -> RGB, NCHW
        sortie = self.session.run(None, {self.entree: np.ascontiguousarray(tenseur)})[0]
        boites, scores, classes = decoder_yolov8(sortie, self.seuil_candidat, self.seuil_iou)
        boites = vers_image_origine(boites, echelle, decalage, w, h)
        return [Detection(self.classes[c], float(s), tuple(float(v) for v in b))
                for b, s, c in zip(boites, scores, classes)]
