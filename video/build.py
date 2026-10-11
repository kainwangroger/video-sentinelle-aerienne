"""Génère les vidéos explicatives « Sentinelle Aérienne ».

Usage (depuis la racine du dépôt) :
    python3 video/build.py                    # fiche technique du module IA
    python3 video/build.py --fiche projet     # fiche projet (drone VTOL)
    python3 video/build.py --fiche az         # longue vidéo « le SA-1 de A à Z », un fichier par chapitre
    python3 video/build.py --sans-voix        # sous-titres seuls
    python3 video/build.py --apercu           # une image PNG par scène dans output/apercu_<fiche>/
"""

import argparse
import importlib
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
from gfx import (BLANC, CYAN, CYAN_SOMBRE, GRIS, H, W, apparition, avec_alpha, borne, couper, fond,  # noqa: E402
                 police, texte)

RACINE = Path(__file__).resolve().parent.parent
SORTIE = RACINE / "output"
VOIX_PAR_DEFAUT = RACINE / "voices" / "fr-siwis-medium.onnx"
FPS = 30  # remplacé par la clé « fps » d'une fiche
FONDU = 0.45  # fondu au noir entre les scènes (s)

# Une entrée par vidéo : modules de contenu et d'animation, fichiers produits.
FICHES = {
    "technique": {"contenu": "contenu_technique", "visuels": "visuels_technique", "bandeau": "IA EMBARQUÉE",
                  "video": "sentinelle_aerienne.mp4", "storyboard": "storyboard.md",
                  "titre_storyboard": "Storyboard — Sentinelle Aérienne (fiche technique du module IA)"},
    "projet": {"contenu": "contenu_projet", "visuels": "visuels_projet", "bandeau": "DRONE HYBRIDE VTOL",
               "video": "sentinelle_aerienne_projet.mp4", "storyboard": "storyboard_projet.md",
               "titre_storyboard": "Storyboard — Sentinelle Aérienne (fiche projet)"},
    "az": {"contenu": "az.contenu", "visuels": "az.visuels", "bandeau": "LE SA-1 DE A À Z",
           "dossier": "sa1_de_a_a_z", "video": "sa1_de_a_a_z_complet.mp4", "storyboard": "storyboard_sa1_de_a_a_z.md",
           "titre_storyboard": "Storyboard — Le drone Sentinelle Aérienne SA-1 de A à Z", "fps": 25,
           "crf": 27, "audio": ["-b:a", "64k", "-ac", "1"], "vitesse": 1.0},
}
SANS_BANDEAU = ("titre", "conclusion")

_FOND = None
_PLAN = None
_TOTAL = None
_VISUELS = None
_AVEC_SCENE = False
_BANDEAU = None


def _init(plan, total, fiche):
    global _FOND, _PLAN, _TOTAL, _VISUELS, _AVEC_SCENE, _BANDEAU, FPS
    _FOND, _PLAN, _TOTAL = fond(), plan, total
    module = importlib.import_module(FICHES[fiche]["visuels"])
    _VISUELS = module.SCENES_VISUELLES
    _AVEC_SCENE = getattr(module, "AVEC_SCENE", False)  # les fonctions reçoivent aussi la scène
    _BANDEAU = FICHES[fiche]["bandeau"]
    FPS = FICHES[fiche].get("fps", 30)


def _scene_a(t):
    for i, p in enumerate(_PLAN):
        if t < p["debut"] + p["duree"] or i == len(_PLAN) - 1:
            return i, p


def _bandeau(d, i, n, t_local, scene):
    a = apparition(t_local, 0.0, 0.5)
    texte(d, (80, 58), "SENTINELLE AÉRIENNE", "gras", 22, CYAN, a, "lm")
    texte(d, (80 + police("gras", 22).getlength("SENTINELLE AÉRIENNE") + 18, 58), f"|  {_BANDEAU}",
          "moyen", 22, GRIS, a, "lm")
    repere = scene.get("repere") or f"{i + 1:02d} / {n:02d}"
    texte(d, (W - 80, 58), repere, "gras", 22, GRIS, a, "rm")
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
    if _AVEC_SCENE:
        _VISUELS[scene.get("visuel", scene["id"])](d, t_local, p["duree"], marques, scene)
    else:
        _VISUELS[scene["id"]](d, t_local, p["duree"], marques)
    if scene["id"] not in SANS_BANDEAU and not scene.get("sans_bandeau"):
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


def ecrire_storyboard(plan, chemin, titre, descriptions, commande):
    lignes = [f"# {titre}", "",
              f"Vidéo explicative 1920×1080. Ce fichier est régénéré par `{commande}` :",
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
        description = descriptions.get(p["scene"]["id"]) or p["scene"].get("description", "")
        lignes.append(f"{i + 1}. **{p['scene']['titre']}** — {description}")
    chemin.write_text("\n".join(lignes) + "\n", encoding="utf-8")




def main():
    logging.disable(logging.WARNING)  # avertissements de phonèmes de Piper
    parser = argparse.ArgumentParser()
    parser.add_argument("--fiche", choices=sorted(FICHES), default="technique")
    parser.add_argument("--voix", default=str(VOIX_PAR_DEFAUT), help="modèle Piper .onnx")
    parser.add_argument("--sans-voix", action="store_true")
    parser.add_argument("--vitesse", type=float, default=None,
                        help="length_scale Piper (< 1 = plus rapide ; défaut 0.9, 1.0 pour la fiche az)")
    parser.add_argument("--apercu", action="store_true", help="exporter une image par scène au lieu de la vidéo")
    parser.add_argument("--processus", type=int, default=4)
    parser.add_argument("--crf", type=int, default=None)
    parser.add_argument("--chapitres", help="ne rendre que ces chapitres (ex. 1,3-5) — fiche az")
    args = parser.parse_args()

    SORTIE.mkdir(exist_ok=True)
    config = FICHES[args.fiche]
    contenu = importlib.import_module(config["contenu"])
    voix = None
    if not args.sans_voix:
        if Path(args.voix).exists():
            from tts import VoixOff
            voix = VoixOff(args.voix, length_scale=args.vitesse or config.get("vitesse", 0.9))
        else:
            print(f"Modèle de voix introuvable ({args.voix}) : vidéo sans voix off. "
                  "Lancez scripts/get_voice.sh pour l'installer.")
    print("Synthèse et minutage…")
    plan, audio, sr = timeline.construire(contenu.SCENES, voix)
    total = sum(p["duree"] for p in plan)
    commande = "python3 video/build.py" + ("" if args.fiche == "technique" else f" --fiche {args.fiche}")
    ecrire_storyboard(plan, RACINE / config["storyboard"], config["titre_storyboard"], contenu.DESCRIPTIONS, commande)
    print(f"Durée : {total:.1f} s, {len(plan)} scènes")

    _init(plan, total, args.fiche)  # fixe aussi FPS dans ce processus
    crf = args.crf if args.crf is not None else config.get("crf", 21)
    if args.apercu:
        dossier = SORTIE / f"apercu_{args.fiche}"
        dossier.mkdir(exist_ok=True)
        for i, p in enumerate(plan):
            n = int((p["debut"] + p["duree"] * 0.85) * FPS)
            Image.frombytes("RGB", (W, H), image(n)).save(dossier / f"{i + 1:02d}_{p['scene']['id']}.png")
        print(f"Aperçus dans {dossier}")
        return

    if config.get("dossier"):
        rendre_par_chapitre(plan, audio, sr, total, args, config, crf)
        return
    sortie = SORTIE / config["video"]
    wav = None
    if audio is not None:
        wav = SORTIE / f"voix_off_{args.fiche}.wav"
        ecrire_wav(wav, audio, sr)
    encoder(range(int(round(total * FPS))), wav, sortie, plan, total, args, config, crf)
    print(f"Vidéo écrite : {sortie}")


def encoder(numeros, wav, sortie, plan, total, args, config, crf):
    """Rend les images `numeros` et les encode (avec la piste audio `wav` si fournie)."""
    commande = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                "-r", str(FPS), "-i", "-"]
    if wav is not None:
        commande += ["-i", str(wav), "-c:a", "aac", *config.get("audio", ["-b:a", "128k"]), "-ar", "44100"]
    commande += ["-c:v", "libx264", "-preset", "medium", "-crf", str(crf), "-pix_fmt", "yuv420p",
                 "-movflags", "+faststart", "-shortest" if wav is not None else "-an", str(sortie)]
    print(f"Rendu de {len(numeros)} images -> {sortie.name}")
    ff = subprocess.Popen(commande, stdin=subprocess.PIPE)
    with Pool(args.processus, initializer=_init, initargs=(plan, total, args.fiche)) as pool:
        for k, octets in enumerate(pool.imap(image, numeros, chunksize=8)):
            ff.stdin.write(octets)
            if k % (FPS * 30) == 0:
                print(f"  {k / FPS:5.0f} s / {len(numeros) / FPS:.0f} s", flush=True)
    ff.stdin.close()
    if ff.wait() != 0:
        sys.exit("ffmpeg a échoué")


def _selection(texte_chapitres, n):
    if not texte_chapitres:
        return set(range(1, n + 1))
    choix = set()
    for morceau in texte_chapitres.split(","):
        a, _, b = morceau.partition("-")
        choix.update(range(int(a), int(b or a) + 1))
    return choix


def rendre_par_chapitre(plan, audio, sr, total, args, config, crf):
    """Un MP4 par chapitre, puis assemblage sans réencodage en une vidéo complète."""
    dossier = SORTIE / config["dossier"]
    dossier.mkdir(parents=True, exist_ok=True)
    chapitres = {}
    for p in plan:
        chapitres.setdefault(p["scene"]["chapitre"], []).append(p)
    choix = _selection(args.chapitres, len(chapitres))
    fichiers = []
    for numero, scenes in sorted(chapitres.items()):
        debut = scenes[0]["debut"]
        fin = scenes[-1]["debut"] + scenes[-1]["duree"]
        nom = f"{numero:02d}_{scenes[0]['scene']['chapitre_id']}.mp4"
        fichiers.append(dossier / nom)
        if numero not in choix:
            continue
        wav = None
        if audio is not None:
            wav = dossier / f"voix_{numero:02d}.wav"
            ecrire_wav(wav, audio[int(debut * sr):int(fin * sr)], sr)
        numeros = range(int(round(debut * FPS)), int(round(fin * FPS)))
        encoder(numeros, wav, dossier / nom, plan, total, args, config, crf)
        if wav:
            wav.unlink()
    if all(f.exists() for f in fichiers):
        liste = dossier / "liste.txt"
        liste.write_text("".join(f"file '{f.name}'\n" for f in fichiers))
        complet = dossier / config["video"]
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(liste),
                        "-c", "copy", "-movflags", "+faststart", str(complet)], check=True)
        liste.unlink()
        print(f"Vidéo complète : {complet}")


if __name__ == "__main__":
    main()
