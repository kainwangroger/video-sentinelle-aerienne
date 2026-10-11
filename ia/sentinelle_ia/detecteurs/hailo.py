"""Détecteur exécuté sur l'accélérateur Hailo (Raspberry Pi AI HAT+, NPU Hailo-8).

Utilise HailoRT (paquet Python `hailo_platform`, installé sur Raspberry Pi OS par
`sudo apt install hailo-all`). Le HEF est produit par outils/compiler_hailo.sh avec la
post-NMS Hailo intégrée : la sortie est, pour chaque classe, une liste de
[y_min, x_min, y_max, x_max, score] normalisés dans l'image d'entrée (carrée, letterbox).

À valider sur la cible : la version de HailoRT doit correspondre à celle du Dataflow
Compiler utilisé pour compiler le HEF (voir docs/conversion_hailo.md).
"""

import numpy as np

from ..types import Detection
from .yolo import letterbox, vers_image_origine


class DetecteurHailo:
    def __init__(self, config):
        from hailo_platform import (HEF, ConfigureParams, FormatType, HailoSchedulingAlgorithm, HailoStreamInterface,
                                    InferVStreams, InputVStreamParams, OutputVStreamParams, VDevice)

        self.classes = list(config["classes"])
        self.seuil_candidat = float(config.get("seuil_candidat", 0.15))
        self.hef = HEF(config["modele"])
        params = VDevice.create_params()
        params.scheduling_algorithm = HailoSchedulingAlgorithm.NONE
        self.device = VDevice(params)
        configure = ConfigureParams.create_from_hef(self.hef, interface=HailoStreamInterface.PCIe)
        self.reseau = self.device.configure(self.hef, configure)[0]
        self.params_reseau = self.reseau.create_params()
        self.params_entree = InputVStreamParams.make(self.reseau, format_type=FormatType.UINT8)
        self.params_sortie = OutputVStreamParams.make(self.reseau, format_type=FormatType.FLOAT32)
        info = self.hef.get_input_vstream_infos()[0]
        self.nom_entree = info.name
        self.taille = int(info.shape[0])
        self._activation = self.reseau.activate(self.params_reseau)
        self._activation.__enter__()
        self._flux = InferVStreams(self.reseau, self.params_entree, self.params_sortie)
        self._flux.__enter__()

    def detecter(self, image):
        h, w = image.shape[:2]
        carre, echelle, decalage = letterbox(image, self.taille)
        rgb = np.ascontiguousarray(carre[:, :, ::-1])[None]
        resultats = self._flux.infer({self.nom_entree: rgb})
        sortie = next(iter(resultats.values()))[0]  # liste par classe
        boites, scores, classes = [], [], []
        for c, detections_classe in enumerate(sortie):
            for y1, x1, y2, x2, score in np.asarray(detections_classe).reshape(-1, 5):
                if score >= self.seuil_candidat:
                    boites.append([x1 * self.taille, y1 * self.taille, x2 * self.taille, y2 * self.taille])
                    scores.append(score)
                    classes.append(c)
        if not boites:
            return []
        boites = vers_image_origine(np.array(boites), echelle, decalage, w, h)
        return [Detection(self.classes[c], float(s), tuple(float(v) for v in b))
                for b, s, c in zip(boites, scores, classes)]

    def fermer(self):
        self._flux.__exit__(None, None, None)
        self._activation.__exit__(None, None, None)
        self.device.release()
