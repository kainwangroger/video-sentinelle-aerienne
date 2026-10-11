"""Mesures embarquées : latence image-alerte, débit, température, mémoire, pertes d'images.

Les valeurs sont écrites dans un CSV pour le rapport d'évaluation. Aucune performance
n'est supposée : seule la mesure sur le matériel et le modèle définitifs fait foi.
"""

import csv
import os
import time
from collections import deque
from pathlib import Path


def temperature_soc():
    """Température du SoC en °C (Raspberry Pi / Linux), ou None."""
    try:
        return int(Path("/sys/class/thermal/thermal_zone0/temp").read_text()) / 1000.0
    except (OSError, ValueError):
        return None


def memoire_disponible_mo():
    try:
        for ligne in Path("/proc/meminfo").read_text().splitlines():
            if ligne.startswith("MemAvailable"):
                return int(ligne.split()[1]) / 1024
    except OSError:
        pass
    return None


def charge_cpu():
    try:
        return os.getloadavg()[0]
    except OSError:
        return None


class Metriques:
    def __init__(self, chemin_csv=None, periode=5.0):
        self.latences_inference = deque(maxlen=500)
        self.latences_totales = deque(maxlen=500)
        self.instants = deque(maxlen=120)
        self.periode = periode
        self._derniere_ecriture = 0.0
        self.images = 0
        self.chemin = Path(chemin_csv) if chemin_csv else None
        if self.chemin:
            self.chemin.parent.mkdir(parents=True, exist_ok=True)
            nouveau = not self.chemin.exists()
            self._fichier = open(self.chemin, "a", newline="", encoding="utf-8")
            self._csv = csv.writer(self._fichier)
            if nouveau:
                self._csv.writerow(["horodatage", "images", "fps", "inference_ms_p50", "inference_ms_p95",
                                    "image_a_decision_ms_p50", "image_a_decision_ms_p95", "temperature_c",
                                    "memoire_dispo_mo", "charge_cpu", "evenements", "en_attente"])

    def enregistrer(self, duree_inference, duree_totale):
        self.images += 1
        self.latences_inference.append(duree_inference * 1000)
        self.latences_totales.append(duree_totale * 1000)
        self.instants.append(time.monotonic())

    @staticmethod
    def _centile(valeurs, q):
        if not valeurs:
            return None
        v = sorted(valeurs)
        return round(v[min(len(v) - 1, int(q * (len(v) - 1) + 0.5))], 1)

    @property
    def fps(self):
        if len(self.instants) < 2:
            return None
        return round((len(self.instants) - 1) / (self.instants[-1] - self.instants[0]), 2)

    def resume(self):
        return {
            "images": self.images, "fps": self.fps,
            "inference_ms_p50": self._centile(self.latences_inference, 0.5),
            "inference_ms_p95": self._centile(self.latences_inference, 0.95),
            "image_a_decision_ms_p50": self._centile(self.latences_totales, 0.5),
            "image_a_decision_ms_p95": self._centile(self.latences_totales, 0.95),
            "temperature_c": temperature_soc(), "memoire_dispo_mo": memoire_disponible_mo(), "charge_cpu": charge_cpu(),
        }

    def peut_ecrire(self):
        return self.chemin and time.monotonic() - self._derniere_ecriture >= self.periode

    def ecrire(self, evenements=0, en_attente=0):
        if not self.chemin:
            return
        r = self.resume()
        self._csv.writerow([time.strftime("%Y-%m-%dT%H:%M:%S"), r["images"], r["fps"], r["inference_ms_p50"],
                            r["inference_ms_p95"], r["image_a_decision_ms_p50"], r["image_a_decision_ms_p95"],
                            r["temperature_c"], r["memoire_dispo_mo"], r["charge_cpu"], evenements, en_attente])
        self._fichier.flush()
        self._derniere_ecriture = time.monotonic()

    def fermer(self):
        if self.chemin:
            self._fichier.close()
