"""Détecteur PyTorch via Ultralytics (poste de développement)."""

from ..types import Detection


class DetecteurUltralytics:
    def __init__(self, config):
        from ultralytics import YOLO

        self.modele = YOLO(config["modele"])
        self.classes = list(config["classes"])
        self.taille = int(config.get("taille_entree", 640))
        self.seuil_candidat = float(config.get("seuil_candidat", 0.15))
        self.seuil_iou = float(config.get("seuil_iou", 0.45))

    def detecter(self, image):
        r = self.modele.predict(image, imgsz=self.taille, conf=self.seuil_candidat, iou=self.seuil_iou, verbose=False)[0]
        sortie = []
        for b, s, c in zip(r.boxes.xyxy.cpu().numpy(), r.boxes.conf.cpu().numpy(), r.boxes.cls.cpu().numpy()):
            sortie.append(Detection(self.classes[int(c)], float(s), tuple(float(v) for v in b)))
        return sortie
