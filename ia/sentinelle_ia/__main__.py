"""Point d'entrée : python -m sentinelle_ia --config configs/sentinelle.yaml [--source video.mp4]."""

import argparse
import json
import logging

from .capture import Capture
from .config import charger, chemin
from .pipeline import Pipeline


def main():
    parser = argparse.ArgumentParser(prog="sentinelle_ia", description="Module d'IA embarquée Sentinelle Aérienne")
    parser.add_argument("--config", default="configs/sentinelle.yaml")
    parser.add_argument("--source", help="remplace capture.source (vidéo, index caméra, rtsp://, picamera2)")
    parser.add_argument("--moteur", choices=["hailo", "onnx", "ultralytics", "factice"], help="remplace detecteur.moteur")
    parser.add_argument("--modele", help="remplace detecteur.modele")
    parser.add_argument("--sequence", help="identifiant de séquence (vol, essai)")
    parser.add_argument("--sortie-video", help="enregistre une vidéo annotée (démonstration)")
    parser.add_argument("--duree", type=float, help="durée maximale d'exécution (s)")
    parser.add_argument("-v", "--verbeux", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.verbeux else logging.INFO,
                        format="%(asctime)s %(levelname)s %(message)s")
    surcharges = {"capture": {}, "detecteur": {}, "mission": {}}
    if args.source is not None:
        surcharges["capture"]["source"] = args.source
    if args.moteur:
        surcharges["detecteur"]["moteur"] = args.moteur
    if args.modele:
        surcharges["detecteur"]["modele"] = args.modele
    if args.sequence:
        surcharges["mission"]["sequence_id"] = args.sequence
    config = charger(args.config, surcharges)

    cc = config["capture"]
    source = cc["source"]
    if isinstance(source, str) and not source.isdigit() and "://" not in source and "!" not in source \
            and source != "picamera2":
        source = chemin(config, source)
    capture = Capture(source, cc.get("largeur"), cc.get("hauteur"), config["mission"]["sequence_id"],
                      cc.get("cadence_max"), cc.get("boucle", False))
    pipeline = Pipeline(config)
    resume = pipeline.executer(capture, args.sortie_video, args.duree)
    capture.fermer()
    resume["evenements"] = pipeline.evenements
    resume["en_attente"] = pipeline.journal.compter("en_attente")
    print(json.dumps(resume, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
