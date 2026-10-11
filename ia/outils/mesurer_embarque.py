"""Mesure sur la cible : débit, latence, température, mémoire, pertes d'images, sur une durée donnée.

À lancer sur le Raspberry Pi 5 + AI HAT+ avec la caméra réelle (ou une vidéo sur banc).
Produit un CSV de mesures périodiques et un résumé Markdown. Pour la consommation,
relever le courant avec l'instrument du banc (le Pi ne la mesure pas lui-même).

Usage : python outils/mesurer_embarque.py --config configs/sentinelle.yaml --duree 1800 --rapport rapports/banc_30min.md
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from sentinelle_ia.capture import Capture  # noqa: E402
from sentinelle_ia.config import charger, chemin  # noqa: E402
from sentinelle_ia.pipeline import Pipeline  # noqa: E402


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--config", default="configs/sentinelle.yaml")
    parser.add_argument("--source")
    parser.add_argument("--duree", type=float, default=600, help="secondes")
    parser.add_argument("--csv", default="travail/mesures_embarquees.csv")
    parser.add_argument("--rapport", default="travail/mesures_embarquees.md")
    args = parser.parse_args()

    surcharges = {"metriques": {"csv": args.csv, "periode": 5}}
    if args.source:
        surcharges["capture"] = {"source": args.source}
    config = charger(args.config, surcharges)
    cc = config["capture"]
    source = cc["source"]
    if isinstance(source, str) and Path(chemin(config, source)).exists():
        source = chemin(config, source)
    capture = Capture(source, cc.get("largeur"), cc.get("hauteur"), "MESURE", boucle=True)
    pipeline = Pipeline(config)
    resume = pipeline.executer(capture, duree_max=args.duree)
    capture.fermer()
    resume["duree_s"] = args.duree
    resume["evenements"] = pipeline.evenements
    lignes = ["# Mesures embarquées", "", f"Configuration : `{args.config}` · source : `{source}` · "
              f"modèle : `{config['detecteur']['modele']}` ({config['detecteur']['moteur']})", "",
              "| Mesure | Valeur |", "|---|---|"]
    lignes += [f"| {k} | {v} |" for k, v in resume.items()]
    lignes += ["", f"Série temporelle : `{args.csv}`. Consommation : à relever sur l'instrument du banc."]
    Path(args.rapport).parent.mkdir(parents=True, exist_ok=True)
    Path(args.rapport).write_text("\n".join(lignes) + "\n", encoding="utf-8")
    print(json.dumps(resume, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
