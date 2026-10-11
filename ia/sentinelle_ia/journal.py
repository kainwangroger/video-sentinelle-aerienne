"""Journal local des événements (SQLite) et file d'attente de transmission.

Hors connexion, l'analyse continue : chaque événement est d'abord écrit ici, puis
transmis quand la liaison sécurisée est disponible. Les événements en attente survivent
à un redémarrage du Raspberry Pi.
"""

import json
import sqlite3
import threading
import time
from dataclasses import asdict
from pathlib import Path


class Journal:
    def __init__(self, chemin):
        Path(chemin).parent.mkdir(parents=True, exist_ok=True)
        self._verrou = threading.Lock()
        self.base = sqlite3.connect(str(chemin), check_same_thread=False)
        self.base.execute("PRAGMA journal_mode=WAL")
        self.base.execute("""
            CREATE TABLE IF NOT EXISTS evenements (
                id TEXT PRIMARY KEY,
                horodatage TEXT NOT NULL,
                sequence_id TEXT,
                statut TEXT,
                classe TEXT,
                contenu TEXT NOT NULL,
                statut_transmission TEXT NOT NULL DEFAULT 'en_attente',
                tentatives INTEGER NOT NULL DEFAULT 0,
                transmis_le REAL
            )""")
        self.base.commit()

    def ajouter(self, evenement):
        with self._verrou:
            self.base.execute(
                "INSERT OR REPLACE INTO evenements (id, horodatage, sequence_id, statut, classe, contenu) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (evenement.id, evenement.horodatage, evenement.sequence_id, evenement.statut, evenement.classe,
                 json.dumps(asdict(evenement), ensure_ascii=False)))
            self.base.commit()

    def en_attente(self, limite=20):
        with self._verrou:
            lignes = self.base.execute(
                "SELECT contenu FROM evenements WHERE statut_transmission = 'en_attente' "
                "ORDER BY horodatage LIMIT ?", (limite,)).fetchall()
        return [json.loads(c) for (c,) in lignes]

    def marquer_transmis(self, identifiant):
        with self._verrou:
            self.base.execute("UPDATE evenements SET statut_transmission = 'transmis', transmis_le = ? WHERE id = ?",
                              (time.time(), identifiant))
            self.base.commit()

    def marquer_echec(self, identifiant):
        with self._verrou:
            self.base.execute("UPDATE evenements SET tentatives = tentatives + 1 WHERE id = ?", (identifiant,))
            self.base.commit()

    def compter(self, statut_transmission=None):
        with self._verrou:
            if statut_transmission:
                return self.base.execute("SELECT COUNT(*) FROM evenements WHERE statut_transmission = ?",
                                         (statut_transmission,)).fetchone()[0]
            return self.base.execute("SELECT COUNT(*) FROM evenements").fetchone()[0]

    def tous(self):
        with self._verrou:
            return [json.loads(c) for (c,) in self.base.execute("SELECT contenu FROM evenements ORDER BY horodatage")]

    def fermer(self):
        self.base.close()
