"""Calcule la durée des scènes et place chaque phrase dans le temps.

Avec voix off, la durée d'une phrase est celle de l'audio synthétisé.
Sans voix off, elle est estimée à partir du nombre de caractères (lecture
confortable des sous-titres).
"""

import numpy as np

ENTREE = 0.6       # silence au début de chaque scène (s)
ENTRE_PHRASES = 0.3
SORTIE = 0.8       # silence à la fin de chaque scène (s)
CARACTERES_PAR_SECONDE = 15.0


def construire(scenes, voix=None):
    """Renvoie (plan, audio, sample_rate).

    plan : liste de dicts {scene, debut, duree, phrases: [(texte, debut_rel, fin_rel)]}
    audio : tableau float32 de toute la bande son (ou None sans voix).
    """
    sr = voix.sample_rate if voix else 22050
    plan, pistes = [], []
    t = 0.0
    for scene in scenes:
        curseur = ENTREE
        phrases = []
        for texte in scene["phrases"]:
            if voix:
                son = voix.phrase(texte)
                duree = len(son) / sr
                pistes.append((t + curseur, son))
            else:
                duree = max(2.0, len(texte) / CARACTERES_PAR_SECONDE)
            phrases.append((texte, curseur, curseur + duree))
            curseur += duree + ENTRE_PHRASES
        duree_scene = curseur - ENTRE_PHRASES + SORTIE
        plan.append({"scene": scene, "debut": t, "duree": duree_scene, "phrases": phrases})
        t += duree_scene

    audio = None
    if voix:
        audio = np.zeros(int(np.ceil(t * sr)) + sr, dtype=np.float32)
        for debut, son in pistes:
            i = int(debut * sr)
            audio[i:i + len(son)] += son
        audio = np.clip(audio * 0.95, -1, 1)
    return plan, audio, sr
