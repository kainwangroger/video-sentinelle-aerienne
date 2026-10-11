"""Génère la vidéo explicative « Sentinelle Aérienne ».

Usage (depuis la racine du dépôt) :
    python3 src/build.py                      # vidéo complète avec voix off
    python3 src/build.py --sans-voix          # sous-titres seuls
    python3 src/build.py --apercu             # une image PNG par scène dans output/apercu/
"""

import argparse
import logging
import subprocess
import sys
import wave
from multiprocessing import Pool
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent))

import timeline  # noqa: E402
from content import SCENES  # noqa: E402
from gfx import (BLANC, CYAN, CYAN_SOMBRE, GRIS, H, W, apparition, avec_alpha, borne, couper, fond,  # noqa: E402
                 police, texte)
from visuels import SCENES_VISUELLES  # noqa: E402

RACINE = Path(__file__).resolve().parent.parent
SORTIE = RACINE / "output"
VOIX_PAR_DEFAUT = RACINE / "voices" / "fr-siwis-medium.onnx"
FPS = 30
FONDU = 0.45  # fondu au noir entre les scènes (s)

_FOND = None
_PLAN = None
_TOTAL = None


def _init(plan, total):
    global _FOND, _PLAN, _TOTAL
    _FOND, _PLAN, _TOTAL = fond(), plan, total


def _scene_a(t):
    for i, p in enumerate(_PLAN):
        if t < p["debut"] + p["duree"] or i == len(_PLAN) - 1:
            return i, p


def _bandeau(d, i, n, t_local, scene):
    a = apparition(t_local, 0.0, 0.5)
    texte(d, (80, 58), "SENTINELLE AÉRIENNE", "gras", 22, CYAN, a, "lm")
    texte(d, (80 + police("gras", 22).getlength("SENTINELLE AÉRIENNE") + 18, 58), "|  IA EMBARQUÉE",
          "moyen", 22, GRIS, a, "lm")
    texte(d, (W - 80, 58), f"{i + 1:02d} / {n:02d}", "gras", 22, GRIS, a, "rm")
    a = apparition(t_local, 0.15, 0.6)
    d.rectangle((80, 120, 88, 186), fill=avec_alpha(CYAN, a))
    texte(d, (110 + (1 - a) * 30, 153), scene["titre"], "titre", 58, BLANC, a, "lm")


def _sous_titre(d, phrases, t_local):
    for texte_phrase, debut, fin in phrases:
        if debut - 0.1 <= t_local <= fin + 0.25:
            a = min(apparition(t_local, debut - 0.1, 0.2), 1 - borne((t_local - fin) / 0.25))
            lignes = couper(texte_phrase, "moyen", 34, 1500)
            hauteur = len(lignes) * 46 + 30
            y0 = H - 50 - hauteur
            larg = max(police("moyen", 34).getlength(lg) for lg in lignes) + 60
            d.rounded_rectangle((W / 2 - larg / 2, y0, W / 2 + larg / 2, y0 + hauteur), 12,
                                fill=(0, 6, 16, int(185 * a)))
            for k, lg in enumerate(lignes):
                texte(d, (W / 2, y0 + 15 + 23 + k * 46), lg, "moyen", 34, BLANC, a, "mm")


def image(numero_frame):
    t = numero_frame / FPS
    i, p = _scene_a(t)
    t_local = t - p["debut"]
    scene = p["scene"]
    img = _FOND.copy()
    d = ImageDraw.Draw(img, "RGBA")
    marques = [debut for _, debut, _ in p["phrases"]]
    SCENES_VISUELLES[scene["id"]](d, t_local, p["duree"], marques)
    if scene["id"] not in ("titre", "conclusion"):
        _bandeau(d, i, len(_PLAN), t_local, scene)
    _sous_titre(d, p["phrases"], t_local)
    # barre de progression globale
    d.rectangle((0, H - 6, W * t / _TOTAL, H), fill=avec_alpha(CYAN_SOMBRE, 0.9))

    # fondu au noir en entrée et en sortie de scène
    k = min(borne(t_local / FONDU), borne((p["duree"] - t_local) / FONDU))
    if k < 1:
        arr = (np.asarray(img, dtype=np.float32) * (k * k * (3 - 2 * k))).astype(np.uint8)
        return arr.tobytes()
    return img.tobytes()


def ecrire_wav(chemin, audio, sr):
    with wave.open(str(chemin), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes((np.clip(audio, -1, 1) * 32767).astype(np.int16).tobytes())


def ecrire_storyboard(plan, chemin):
    lignes = ["# Storyboard — Sentinelle Aérienne", "",
              "Vidéo explicative 1920×1080, 30 fps. Ce fichier est régénéré par `src/build.py` :",
              "les durées correspondent exactement à la vidéo produite.", "",
              "| # | Début | Durée | Scène | Narration / sous-titres |", "|---|---|---|---|---|"]
    for i, p in enumerate(plan):
        narration = "<br>".join(t for t, _, _ in p["phrases"])
        lignes.append(f"| {i + 1} | {int(p['debut'] // 60)}:{p['debut'] % 60:04.1f} | {p['duree']:.1f} s | "
                      f"**{p['scene']['titre']}** | {narration} |")
    total = sum(p["duree"] for p in plan)
    lignes += ["", f"Durée totale : {int(total // 60)} min {total % 60:.0f} s", "",
               "## Contenu visuel par scène", ""]
    for i, p in enumerate(plan):
        lignes.append(f"{i + 1}. **{p['scene']['titre']}** — {VISUELS[p['scene']['id']]}")
    chemin.write_text("\n".join(lignes) + "\n", encoding="utf-8")


VISUELS = {
    "titre": "drone vu de dessus avec ondes radar, titre animé, crédits SkyVision Togo / CECFD 2026 — ANAC.",
    "mission": "piste en perspective, apparition d'un débris, d'une personne et d'un véhicule signalés ; un drone survole la piste avec son cône de caméra.",
    "decision": "cartes Raspberry Pi 5 + AI HAT+ 26 TOPS, caméra vers les trois familles détectées, suivi d'un objet image après image (1 objet = 1 alerte).",
    "perimetre": "tableau du périmètre : zone analysée, classes v1, traitement à bord (cloud barré), limite en ambre.",
    "architecture": "schéma fonctionnel en 7 blocs apparaissant au fil de la narration, paquet de données circulant, légende accélérateur / logiciel.",
    "choix": "trois cartes : détecteur compact (retenu), modèle génératif / vision-langage et segmentation (non retenus).",
    "modele": "vue aérienne schématique avec rectangles de détection étiquetés, grille de tuiles 640×640, étapes YOLOv8s → fine-tuning → sortie.",
    "inconnus": "candidat inconnu encadré en pointillés avec « ? », trois niveaux : objet à vérifier, détection d'anomalie, suivi multi-images.",
    "donnees": "quatre cartes de sources : FOD-A (compteurs 31 catégories / 30 000+ instances), images du projet, YOLO-URD, exemples négatifs.",
    "protocole": "frise en 6 étapes qui s'allument (préparer → déployer) et encadré du critère de sélection.",
    "alerte": "fiche d'événement (exemple fictif) qui se remplit, liaison drone-station coupée puis stockage local, position au sol après calibration.",
    "materiel": "empilement matériel (alimentation, Raspberry Pi 5, AI HAT+, caméra) et notes : repli 13 TOPS, stockage, outils.",
    "validation": "trois étapes de validation puis essai en vol autorisé, six mesures, bandeau « aucun taux annoncé avant mesure ».",
    "conclusion": "titre final, slogan et les cinq lots de l'équipe avec leurs responsables.",
}


def main():
    logging.disable(logging.WARNING)  # avertissements de phonèmes de Piper
    parser = argparse.ArgumentParser()
    parser.add_argument("--voix", default=str(VOIX_PAR_DEFAUT), help="modèle Piper .onnx")
    parser.add_argument("--sans-voix", action="store_true")
    parser.add_argument("--vitesse", type=float, default=0.9, help="length_scale Piper (< 1 = plus rapide)")
    parser.add_argument("--apercu", action="store_true", help="exporter une image par scène au lieu de la vidéo")
    parser.add_argument("--processus", type=int, default=4)
    parser.add_argument("--crf", type=int, default=21)
    args = parser.parse_args()

    SORTIE.mkdir(exist_ok=True)
    voix = None
    if not args.sans_voix:
        if Path(args.voix).exists():
            from tts import VoixOff
            voix = VoixOff(args.voix, length_scale=args.vitesse)
        else:
            print(f"Modèle de voix introuvable ({args.voix}) : vidéo sans voix off. "
                  "Lancez scripts/get_voice.sh pour l'installer.")
    print("Synthèse et minutage…")
    plan, audio, sr = timeline.construire(SCENES, voix)
    total = sum(p["duree"] for p in plan)
    ecrire_storyboard(plan, RACINE / "storyboard.md")
    print(f"Durée : {total:.1f} s, {len(plan)} scènes")

    if args.apercu:
        _init(plan, total)
        dossier = SORTIE / "apercu"
        dossier.mkdir(exist_ok=True)
        for i, p in enumerate(plan):
            n = int((p["debut"] + p["duree"] - 1.2) * FPS)
            Image.frombytes("RGB", (W, H), image(n)).save(dossier / f"{i + 1:02d}_{p['scene']['id']}.png")
        print(f"Aperçus dans {dossier}")
        return

    commande = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                "-r", str(FPS), "-i", "-"]
    if audio is not None:
        wav = SORTIE / "voix_off.wav"
        ecrire_wav(wav, audio, sr)
        commande += ["-i", str(wav), "-c:a", "aac", "-b:a", "128k", "-ar", "44100"]
    commande += ["-c:v", "libx264", "-preset", "medium", "-crf", str(args.crf), "-pix_fmt", "yuv420p",
                 "-movflags", "+faststart", "-shortest" if audio is not None else "-an",
                 str(SORTIE / "sentinelle_aerienne.mp4")]

    n_frames = int(round(total * FPS))
    print(f"Rendu de {n_frames} images…")
    ff = subprocess.Popen(commande, stdin=subprocess.PIPE)
    with Pool(args.processus, initializer=_init, initargs=(plan, total)) as pool:
        for k, octets in enumerate(pool.imap(image, range(n_frames), chunksize=8)):
            ff.stdin.write(octets)
            if k % (FPS * 10) == 0:
                print(f"  {k / FPS:5.0f} s / {total:.0f} s", flush=True)
    ff.stdin.close()
    if ff.wait() != 0:
        sys.exit("ffmpeg a échoué")
    print(f"Vidéo écrite : {SORTIE / 'sentinelle_aerienne.mp4'}")


if __name__ == "__main__":
    main()
