"""Récepteur de démonstration côté station au sol (pour l'intégration avec le lot station sol).

Reçoit les événements POST /api/evenements (JSON), vérifie le jeton porteur, enregistre
les événements et leurs images, et affiche la liste sur http://<hôte>:<port>/.
Ce n'est PAS la station sol du projet : c'est un banc d'essai du format de message.

Usage : SENTINELLE_JETON=secret python outils/station_sol_demo.py --port 8080 --dossier travail/station
        (côté drone : liaison.type https, url http://<pc>:8080/api/evenements pour un essai en clair)
"""

import argparse
import base64
import html
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


def fabrique(dossier, jeton):
    dossier = Path(dossier)
    (dossier / "images").mkdir(parents=True, exist_ok=True)

    class Gestionnaire(BaseHTTPRequestHandler):
        def _repondre(self, code, contenu=b"", type_="application/json"):
            self.send_response(code)
            self.send_header("Content-Type", type_)
            self.send_header("Content-Length", str(len(contenu)))
            self.end_headers()
            self.wfile.write(contenu)

        def do_POST(self):
            if self.path != "/api/evenements":
                return self._repondre(404)
            if jeton and self.headers.get("Authorization") != f"Bearer {jeton}":
                return self._repondre(401, b'{"erreur": "jeton invalide"}')
            longueur = int(self.headers.get("Content-Length", 0))
            if longueur > 1_000_000:
                return self._repondre(413)
            try:
                evenement = json.loads(self.rfile.read(longueur))
                identifiant = str(evenement["id"])
            except (ValueError, KeyError):
                return self._repondre(400, b'{"erreur": "message invalide"}')
            image = evenement.pop("image_preuve_jpeg_base64", None)
            if image:
                (dossier / "images" / f"{identifiant}.jpg").write_bytes(base64.b64decode(image))
            (dossier / f"{identifiant}.json").write_text(json.dumps(evenement, ensure_ascii=False, indent=1),
                                                         encoding="utf-8")
            print(f"Événement reçu : {evenement.get('statut')} {evenement.get('classe')} {evenement.get('horodatage')}")
            self._repondre(201, b'{"ok": true}')

        def do_GET(self):
            if self.path.startswith("/images/"):
                chemin = dossier / "images" / Path(self.path).name
                if chemin.exists():
                    return self._repondre(200, chemin.read_bytes(), "image/jpeg")
                return self._repondre(404)
            evenements = sorted((json.loads(p.read_text(encoding="utf-8")) for p in dossier.glob("*.json")),
                                key=lambda e: e.get("horodatage", ""), reverse=True)
            lignes = []
            for e in evenements:
                img = f"/images/{e['id']}.jpg"
                etiquette = e.get("classe") or "objet"
                if e.get("statut") == "a_verifier":
                    etiquette += " — à vérifier"
                lignes.append(f"<tr><td>{html.escape(e.get('horodatage', ''))}</td><td>{html.escape(etiquette)}</td>"
                              f"<td>{e.get('score')}</td><td>{html.escape(str(e.get('sequence_id')))}</td>"
                              f"<td><img src='{img}' height='120'></td></tr>")
            page = ("<!doctype html><meta charset='utf-8'><title>Station sol (démo)</title>"
                    "<style>body{font-family:sans-serif;background:#0b1428;color:#e8f1fa}td{padding:6px 12px}"
                    "</style><h1>Événements reçus</h1><table><tr><th>Heure</th><th>Classe</th><th>Score</th>"
                    "<th>Séquence</th><th>Preuve</th></tr>" + "".join(lignes) + "</table>")
            self._repondre(200, page.encode("utf-8"), "text/html; charset=utf-8")

        def log_message(self, *args):
            pass

    return Gestionnaire


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--hote", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8080)
    parser.add_argument("--dossier", default="travail/station")
    args = parser.parse_args()
    serveur = ThreadingHTTPServer((args.hote, args.port), fabrique(args.dossier, os.environ.get("SENTINELLE_JETON")))
    print(f"Station sol de démonstration sur http://{args.hote}:{args.port}/")
    serveur.serve_forever()


if __name__ == "__main__":
    main()
