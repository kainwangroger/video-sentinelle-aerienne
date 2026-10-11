"""Événement d'alerte et image de preuve.

Un événement contient : heure, classe ou statut « à vérifier », score, rectangle,
identifiant de séquence et image de preuve. La position au sol n'est ajoutée que si la
géométrie caméra-sol a été calibrée et validée (voir `position`) : par défaut elle vaut
null et l'opérateur retrouve l'objet grâce à l'image et à la zone caméra.
Le schéma JSON correspondant est dans schemas/evenement.schema.json.
"""

import base64
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from . import STATUT_A_VERIFIER, __version__

VERSION_SCHEMA = "1.0"


@dataclass
class Evenement:
    id: str
    horodatage: str                 # ISO 8601 UTC de l'image de confirmation
    sequence_id: str
    piste_id: int
    numero_image: int
    statut: str                     # "classe_confirmee" | "a_verifier"
    classe: str = None              # classe proposée (peut exister même si statut = a_verifier)
    score: float = 0.0
    boite: list = field(default_factory=list)          # [x1, y1, x2, y2] en pixels
    taille_image: list = field(default_factory=list)   # [largeur, hauteur]
    source: str = "detecteur"       # "detecteur" | "anomalie"
    image_preuve: str = None        # chemin local de la preuve (JPEG)
    position: dict = None           # null tant que la chaîne caméra-sol n'est pas validée
    telemetrie: dict = None         # position/attitude du drone au moment de l'image, si fournie
    statut_transmission: str = "en_attente"
    version_schema: str = VERSION_SCHEMA
    version_logiciel: str = __version__

    def message(self, inclure_image=False, taille_max_image=60_000):
        """Message structuré envoyé à la station au sol."""
        donnees = asdict(self)
        donnees.pop("statut_transmission")
        if inclure_image and self.image_preuve and Path(self.image_preuve).exists():
            octets = Path(self.image_preuve).read_bytes()
            if len(octets) <= taille_max_image:
                donnees["image_preuve_jpeg_base64"] = base64.b64encode(octets).decode("ascii")
        return donnees


def creer_evenement(piste, image, suivi_params, telemetrie=None):
    classe, statut, score = piste.classe_et_statut(suivi_params)
    det = piste.meilleure_detection
    w, h = image.taille
    return Evenement(
        id=str(uuid.uuid4()),
        horodatage=datetime.fromtimestamp(image.horodatage, timezone.utc).isoformat(timespec="milliseconds"),
        sequence_id=image.sequence_id,
        piste_id=piste.id,
        numero_image=image.numero,
        statut=statut,
        classe=classe,
        score=round(float(score), 3),
        boite=[round(float(v), 1) for v in piste.boite],
        taille_image=[w, h],
        source=det.source if det else "detecteur",
        telemetrie=telemetrie,
    )


def enregistrer_preuve(evenement, image, dossier, marge=0.6, largeur_max=640, qualite=80, contexte_min=(480, 320)):
    """Sauve une image de preuve : contexte autour de l'objet, rectangle et légende dessinés."""
    import cv2

    dossier = Path(dossier)
    dossier.mkdir(parents=True, exist_ok=True)
    pixels = image.pixels.copy()
    h, w = pixels.shape[:2]
    x1, y1, x2, y2 = [int(v) for v in evenement.boite]
    couleur = (0, 190, 255) if evenement.statut == STATUT_A_VERIFIER else (60, 220, 150)
    cv2.rectangle(pixels, (x1, y1), (x2, y2), couleur, 3)
    legende = (evenement.classe or "objet") + (" - a verifier" if evenement.statut == STATUT_A_VERIFIER else "")
    cv2.putText(pixels, f"{legende} {evenement.score:.2f}", (x1, max(20, y1 - 8)), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                couleur, 2, cv2.LINE_AA)
    # recadrage centré sur l'objet, avec assez de contexte pour que l'opérateur reconnaisse l'endroit
    cw = min(w, max(int((x2 - x1) * (1 + 2 * marge * 3)), contexte_min[0]))
    ch = min(h, max(int((y2 - y1) * (1 + 2 * marge * 3)), contexte_min[1]))
    cx1 = min(max(0, (x1 + x2) // 2 - cw // 2), w - cw)
    cy1 = min(max(0, (y1 + y2) // 2 - ch // 2), h - ch)
    recadre = pixels[cy1:cy1 + ch, cx1:cx1 + cw]
    if recadre.shape[1] > largeur_max:
        f = largeur_max / recadre.shape[1]
        recadre = cv2.resize(recadre, None, fx=f, fy=f, interpolation=cv2.INTER_AREA)
    chemin = dossier / f"{evenement.horodatage[:10]}_{evenement.sequence_id}_{evenement.id[:8]}.jpg"
    cv2.imwrite(str(chemin), recadre, [cv2.IMWRITE_JPEG_QUALITY, qualite])
    evenement.image_preuve = str(chemin)
    return chemin
