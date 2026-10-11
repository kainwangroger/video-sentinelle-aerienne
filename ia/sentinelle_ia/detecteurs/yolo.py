"""Pré- et post-traitement YOLOv8 communs (redimensionnement avec bandes, décodage, NMS)."""

import numpy as np


def letterbox(image, taille=640, couleur=114):
    """Redimensionne en conservant les proportions et complète par des bandes.

    Renvoie (image_carree, echelle, (decalage_x, decalage_y)).
    """
    import cv2

    h, w = image.shape[:2]
    echelle = min(taille / w, taille / h)
    nw, nh = int(round(w * echelle)), int(round(h * echelle))
    redim = cv2.resize(image, (nw, nh), interpolation=cv2.INTER_LINEAR)
    sortie = np.full((taille, taille, 3), couleur, dtype=np.uint8)
    dx, dy = (taille - nw) // 2, (taille - nh) // 2
    sortie[dy:dy + nh, dx:dx + nw] = redim
    return sortie, echelle, (dx, dy)


def vers_image_origine(boites, echelle, decalage, largeur, hauteur):
    """Ramène des boîtes (N, 4) du repère letterbox au repère de l'image d'origine."""
    b = boites.copy().astype(np.float32)
    b[:, [0, 2]] = (b[:, [0, 2]] - decalage[0]) / echelle
    b[:, [1, 3]] = (b[:, [1, 3]] - decalage[1]) / echelle
    b[:, [0, 2]] = b[:, [0, 2]].clip(0, largeur)
    b[:, [1, 3]] = b[:, [1, 3]].clip(0, hauteur)
    return b


def nms(boites, scores, seuil_iou=0.45):
    """Suppression des non-maxima (boîtes x1 y1 x2 y2). Renvoie les indices gardés."""
    if len(boites) == 0:
        return np.zeros(0, dtype=int)
    x1, y1, x2, y2 = boites.T
    aires = (x2 - x1) * (y2 - y1)
    ordre = scores.argsort()[::-1]
    gardes = []
    while ordre.size:
        i = ordre[0]
        gardes.append(i)
        xx1 = np.maximum(x1[i], x1[ordre[1:]])
        yy1 = np.maximum(y1[i], y1[ordre[1:]])
        xx2 = np.minimum(x2[i], x2[ordre[1:]])
        yy2 = np.minimum(y2[i], y2[ordre[1:]])
        inter = np.clip(xx2 - xx1, 0, None) * np.clip(yy2 - yy1, 0, None)
        recouvrement = inter / (aires[i] + aires[ordre[1:]] - inter + 1e-9)
        ordre = ordre[1:][recouvrement <= seuil_iou]
    return np.array(gardes, dtype=int)


def decoder_yolov8(sortie, seuil_score=0.15, seuil_iou=0.45, max_det=100):
    """Décode la sortie brute YOLOv8 (1, 4 + nc, N) : cx, cy, w, h puis un score par classe.

    NMS par classe (décalage des boîtes). Renvoie (boites x1y1x2y2, scores, classes).
    """
    pred = np.squeeze(sortie, 0).T  # (N, 4 + nc)
    scores_classes = pred[:, 4:]
    classes = scores_classes.argmax(1)
    scores = scores_classes[np.arange(len(pred)), classes]
    garder = scores >= seuil_score
    pred, scores, classes = pred[garder], scores[garder], classes[garder]
    if len(pred) == 0:
        return np.zeros((0, 4), np.float32), np.zeros(0, np.float32), np.zeros(0, int)
    cx, cy, w, h = pred[:, 0], pred[:, 1], pred[:, 2], pred[:, 3]
    boites = np.stack([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], 1)
    decalees = boites + classes[:, None] * 4096.0
    gardes = nms(decalees, scores, seuil_iou)[:max_det]
    return boites[gardes], scores[gardes], classes[gardes]
