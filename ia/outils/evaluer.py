"""Évaluation sur données séparées : rappel par classe, petits objets, fausses alertes, latence.

Deux niveaux, conformes au protocole de la fiche technique :

1. Détecteur, image par image, sur un jeu au format YOLO (ensemble de test isolé) :
   précision et rappel par classe à IoU 0,5 au seuil de décision, rappel des petits
   objets séparé (aire < --petit px² dans l'image d'origine), détections sur images
   vides (négatifs), latence d'inférence.
2. Chaîne complète (avec suivi) sur des vidéos de scènes VIDES : nombre d'alertes
   rapporté à la durée -> fausses alertes par minute.

Le même script compare les moteurs (ultralytics .pt, onnx, hailo .hef) sur le même jeu :
vérifier que la baisse de rappel après quantification reste acceptable.

Usage :
    python outils/evaluer.py --data travail/jeu_projet --split test --moteur onnx --modele modeles/x.onnx
    python outils/evaluer.py ... --videos-vides videos/piste_vide_*.mp4 --rapport rapports/onnx_test.md
"""

import argparse
import json
import sys
import time
from collections import defaultdict
from pathlib import Path

import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from sentinelle_ia import CLASSES  # noqa: E402
from sentinelle_ia.detecteurs import creer_detecteur  # noqa: E402
from sentinelle_ia.types import iou  # noqa: E402


def lire_labels(chemin, w, h):
    verites = []
    if chemin.exists():
        for ligne in chemin.read_text().split("\n"):
            if ligne.strip():
                c, x, y, bw, bh = ligne.split()[:5]
                x, y, bw, bh = float(x) * w, float(y) * h, float(bw) * w, float(bh) * h
                verites.append((CLASSES[int(c)], (x - bw / 2, y - bh / 2, x + bw / 2, y + bh / 2)))
    return verites


def evaluer_images(detecteur, dossier, split, seuil, petit=32 * 32, iou_min=0.5, limite=None):
    images = sorted(p for p in (Path(dossier) / "images" / split).glob("*") if p.suffix.lower() in {".jpg", ".png", ".jpeg"})
    if limite:
        images = images[:limite]
    vp, fp, fn = defaultdict(int), defaultdict(int), defaultdict(int)
    petits_total, petits_trouves = defaultdict(int), defaultdict(int)
    negatives, detections_sur_negatives = 0, 0
    latences = []
    for chemin in images:
        img = cv2.imread(str(chemin))
        h, w = img.shape[:2]
        verites = lire_labels(Path(dossier) / "labels" / split / f"{chemin.stem}.txt", w, h)
        t0 = time.perf_counter()
        dets = [d for d in detecteur.detecter(img) if d.score >= seuil]
        latences.append((time.perf_counter() - t0) * 1000)
        if not verites:
            negatives += 1
            detections_sur_negatives += len(dets)
        utilisees = set()
        for classe, boite in verites:
            meilleure, j_meilleur = 0.0, None
            for j, d in enumerate(dets):
                if j in utilisees or d.classe != classe:
                    continue
                r = iou(boite, d.boite)
                if r > meilleure:
                    meilleure, j_meilleur = r, j
            est_petit = (boite[2] - boite[0]) * (boite[3] - boite[1]) < petit
            petits_total[classe] += est_petit
            if meilleure >= iou_min:
                utilisees.add(j_meilleur)
                vp[classe] += 1
                petits_trouves[classe] += est_petit
            else:
                fn[classe] += 1
        for j, d in enumerate(dets):
            if j not in utilisees:
                fp[d.classe] += 1
    par_classe = {}
    for c in CLASSES:
        n = vp[c] + fn[c]
        par_classe[c] = {
            "objets": n, "rappel": round(vp[c] / n, 3) if n else None,
            "precision": round(vp[c] / (vp[c] + fp[c]), 3) if vp[c] + fp[c] else None,
            "petits_objets": petits_total[c],
            "rappel_petits": round(petits_trouves[c] / petits_total[c], 3) if petits_total[c] else None,
        }
    return {
        "images": len(images), "seuil": seuil, "par_classe": par_classe,
        "images_vides": negatives, "detections_sur_images_vides": detections_sur_negatives,
        "latence_ms_p50": round(float(np.percentile(latences, 50)), 1) if latences else None,
        "latence_ms_p95": round(float(np.percentile(latences, 95)), 1) if latences else None,
    }


def evaluer_videos_vides(config_base, videos):
    """Fausses alertes par minute de la chaîne complète (suivi compris) sur des scènes sans objet."""
    import tempfile

    from sentinelle_ia.capture import Capture
    from sentinelle_ia.config import fusionner
    from sentinelle_ia.pipeline import Pipeline

    total_alertes, total_secondes = 0, 0.0
    details = []
    for video in videos:
        with tempfile.TemporaryDirectory() as tmp:
            config = fusionner(config_base, {"journal": {"base": f"{tmp}/j.sqlite"},
                                             "alerte": {"dossier_preuves": f"{tmp}/preuves"},
                                             "liaison": {"type": "aucune"}, "metriques": {"csv": None}})
            capture = Capture(video)
            fps = capture.fps_source or 25
            pipeline = Pipeline(config)
            pipeline.executer(capture, afficher_progression=False)
            capture.fermer()
            secondes = capture.numero / fps
            details.append({"video": str(video), "secondes": round(secondes, 1), "alertes": pipeline.evenements})
            total_alertes += pipeline.evenements
            total_secondes += secondes
    return {"videos": details, "fausses_alertes_par_minute":
            round(total_alertes / (total_secondes / 60), 3) if total_secondes else None}


def rapport_markdown(resultat):
    r = resultat["images"]
    lignes = [f"# Évaluation — moteur {resultat['moteur']}", "",
              f"Modèle : `{resultat['modele']}` · jeu : `{resultat['data']}` ({resultat['split']}) · "
              f"{r['images']} images · seuil {r['seuil']}", "",
              "| Classe | Objets | Rappel | Précision | Petits objets | Rappel petits |", "|---|---|---|---|---|---|"]
    for c, v in r["par_classe"].items():
        lignes.append(f"| {c} | {v['objets']} | {v['rappel']} | {v['precision']} | {v['petits_objets']} | {v['rappel_petits']} |")
    lignes += ["", f"Images vides : {r['images_vides']}, détections sur ces images : {r['detections_sur_images_vides']}",
               f"Latence d'inférence : p50 {r['latence_ms_p50']} ms, p95 {r['latence_ms_p95']} ms"]
    if resultat.get("videos_vides"):
        lignes.append(f"Fausses alertes (chaîne complète, scènes vides) : "
                      f"{resultat['videos_vides']['fausses_alertes_par_minute']} par minute")
    lignes += ["", "Mesures valables uniquement pour ce modèle, cette résolution et ce matériel."]
    return "\n".join(lignes) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--data", required=True, help="dossier du jeu YOLO (images/<split>, labels/<split>)")
    parser.add_argument("--split", default="test")
    parser.add_argument("--moteur", default="onnx", choices=["onnx", "ultralytics", "hailo"])
    parser.add_argument("--modele", required=True)
    parser.add_argument("--imgsz", type=int, default=640)
    parser.add_argument("--seuil", type=float, default=0.5, help="seuil de décision évalué")
    parser.add_argument("--petit", type=float, default=32 * 32, help="aire (px²) sous laquelle un objet est « petit »")
    parser.add_argument("--videos-vides", nargs="*", default=[])
    parser.add_argument("--config", default="configs/sentinelle.yaml", help="config de la chaîne pour les vidéos vides")
    parser.add_argument("--rapport", help="fichier Markdown du rapport")
    parser.add_argument("--json", help="fichier JSON des résultats")
    args = parser.parse_args()

    config_det = {"moteur": args.moteur, "modele": args.modele, "classes": list(CLASSES), "taille_entree": args.imgsz,
                  "seuil_candidat": min(0.15, args.seuil)}
    detecteur = creer_detecteur(config_det)
    resultat = {"moteur": args.moteur, "modele": args.modele, "data": args.data, "split": args.split,
                "images": evaluer_images(detecteur, args.data, args.split, args.seuil, args.petit)}
    if args.videos_vides:
        from sentinelle_ia.config import charger
        config = charger(args.config, {"detecteur": config_det})
        resultat["videos_vides"] = evaluer_videos_vides(config, args.videos_vides)
    print(json.dumps(resultat, ensure_ascii=False, indent=1))
    if args.json:
        Path(args.json).parent.mkdir(parents=True, exist_ok=True)
        Path(args.json).write_text(json.dumps(resultat, ensure_ascii=False, indent=1), encoding="utf-8")
    if args.rapport:
        Path(args.rapport).parent.mkdir(parents=True, exist_ok=True)
        Path(args.rapport).write_text(rapport_markdown(resultat), encoding="utf-8")


if __name__ == "__main__":
    main()
