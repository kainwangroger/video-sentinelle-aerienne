"""Contenu de la vidéo « Le drone Sentinelle Aérienne SA-1 de A à Z ».

Chaque chapitre commence par une scène d'ouverture ; chaque scène choisit un gabarit ou
une animation (clé « visuel ») et ses données. Les chiffres viennent de
drone/calculs/dimensionnement.py et de drone/fiche_technique_complete.md.
"""

from .chapitres_1 import CHAPITRES as C1
from .chapitres_2 import CHAPITRES as C2
from .chapitres_3 import CHAPITRES as C3


def _assembler(chapitres):
    scenes = []
    for numero, chap in enumerate(chapitres, 1):
        ouverture = {
            "id": f"c{numero:02d}_ouverture", "titre": chap["titre"], "visuel": "ouverture", "sans_bandeau": True,
            "phrases": chap["introduction"],
            "donnees": {"numero": numero, "titre": chap["titre"], "sous_titre": chap.get("sous_titre"),
                        "sommaire": chap.get("sommaire", []), "picto": chap.get("picto")},
            "description": f"ouverture du chapitre {numero} : {chap['titre']}",
        }
        for k, scene in enumerate([ouverture] + chap["scenes"]):
            scene.setdefault("id", f"c{numero:02d}_s{k:02d}")
            scene["chapitre"] = numero
            scene["chapitre_id"] = chap["id"]
            scene["repere"] = f"CHAPITRE {numero:02d} · {chap['titre_court']}"
            scene.setdefault("donnees", {})
            scene.setdefault("description", f"{scene['visuel']} — {scene['titre']}")
            scenes.append(scene)
    return scenes


CHAPITRES = C1 + C2 + C3
SCENES = _assembler(CHAPITRES)
DESCRIPTIONS = {}
