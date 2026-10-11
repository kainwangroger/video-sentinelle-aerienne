"""Transmission des événements vers la station au sol.

Le transport réel, l'authentification et le chiffrement sont définis par le lot réseau
et sécurité ; ce module fournit l'interface et deux implémentations :
- HTTPS : POST JSON vers la station, jeton porteur lu dans une variable d'environnement,
  vérification TLS (certificat de la station ou autorité interne) ;
- dossier : dépôt de fichiers JSON dans un répertoire (liaison simulée, tests, ou relais
  par un autre processus du lot réseau).

Un fil d'envoi vide la file d'attente du journal en tâche de fond ; en cas d'échec,
l'événement reste « en_attente » et sera retenté (attente exponentielle).
"""

import json
import os
import ssl
import threading
import time
import urllib.error
import urllib.request
from pathlib import Path


class LiaisonHttps:
    def __init__(self, url, variable_jeton="SENTINELLE_JETON", certificat_ca=None, delai=5.0, taille_max=256_000):
        self.url = url
        self.jeton = os.environ.get(variable_jeton)
        self.delai = delai
        self.taille_max = taille_max
        self.contexte = ssl.create_default_context(cafile=certificat_ca) if url.startswith("https") else None

    def envoyer(self, message):
        corps = json.dumps(message, ensure_ascii=False).encode("utf-8")
        if len(corps) > self.taille_max:
            message = {k: v for k, v in message.items() if k != "image_preuve_jpeg_base64"}
            corps = json.dumps(message, ensure_ascii=False).encode("utf-8")
        requete = urllib.request.Request(self.url, data=corps, method="POST",
                                         headers={"Content-Type": "application/json"})
        if self.jeton:
            requete.add_header("Authorization", f"Bearer {self.jeton}")
        with urllib.request.urlopen(requete, timeout=self.delai, context=self.contexte) as reponse:
            return 200 <= reponse.status < 300


class LiaisonDossier:
    def __init__(self, dossier):
        self.dossier = Path(dossier)
        self.dossier.mkdir(parents=True, exist_ok=True)
        self.disponible = True  # basculable pour simuler une coupure

    def envoyer(self, message):
        if not self.disponible:
            raise ConnectionError("liaison simulée coupée")
        (self.dossier / f"{message['id']}.json").write_text(json.dumps(message, ensure_ascii=False, indent=1),
                                                             encoding="utf-8")
        return True


def creer_liaison(config):
    if not config or config.get("type") in (None, "aucune"):
        return None
    if config["type"] == "https":
        return LiaisonHttps(config["url"], config.get("variable_jeton", "SENTINELLE_JETON"),
                            config.get("certificat_ca"), float(config.get("delai", 5.0)),
                            int(config.get("taille_max", 256_000)))
    if config["type"] == "dossier":
        return LiaisonDossier(config["dossier"])
    raise ValueError(f"Type de liaison inconnu : {config['type']}")


class Emetteur(threading.Thread):
    """Fil d'envoi : vide la file d'attente du journal dès que la liaison répond."""

    def __init__(self, journal, liaison, inclure_image=True, periode=1.0, attente_max=30.0):
        super().__init__(daemon=True, name="emetteur")
        self.journal = journal
        self.liaison = liaison
        self.inclure_image = inclure_image
        self.periode = periode
        self.attente_max = attente_max
        self._arret = threading.Event()
        self._reveil = threading.Event()
        self.liaison_ok = None

    def signaler(self):
        self._reveil.set()

    def vider(self):
        """Tente d'envoyer tout ce qui est en attente ; renvoie le nombre d'événements transmis."""
        from .alerte import Evenement

        transmis = 0
        for donnees in self.journal.en_attente():
            evenement = Evenement(**donnees)
            try:
                ok = self.liaison.envoyer(evenement.message(self.inclure_image))
            except (OSError, urllib.error.URLError, ConnectionError):
                ok = False
            if not ok:
                self.journal.marquer_echec(evenement.id)
                self.liaison_ok = False
                return transmis
            self.journal.marquer_transmis(evenement.id)
            transmis += 1
        self.liaison_ok = True
        return transmis

    def run(self):
        attente = self.periode
        while not self._arret.is_set():
            self.vider()
            attente = self.periode if self.liaison_ok else min(self.attente_max, attente * 2)
            self._reveil.wait(attente)
            self._reveil.clear()

    def arreter(self):
        self._arret.set()
        self._reveil.set()
        self.join(timeout=5)
        self.vider()
