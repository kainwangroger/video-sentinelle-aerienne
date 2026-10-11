"""Voix off hors-ligne avec Piper (voix française « siwis », CC-BY 4.0)."""

import numpy as np

from prononciation import texte_parle


class VoixOff:
    def __init__(self, modele, length_scale=1.0):
        from piper import PiperVoice, SynthesisConfig

        self.voix = PiperVoice.load(modele)
        self.config = SynthesisConfig(length_scale=length_scale, noise_scale=0.6, noise_w_scale=0.7)
        self.sample_rate = self.voix.config.sample_rate

    def phrase(self, texte):
        """Renvoie l'audio float32 (mono) d'une phrase, silences de bord retirés."""
        morceaux = [c.audio_int16_array for c in self.voix.synthesize(texte_parle(texte), self.config)]
        audio = np.concatenate(morceaux).astype(np.float32) / 32768.0
        return _rogner_silence(audio)


def _rogner_silence(audio, seuil=0.01):
    actifs = np.flatnonzero(np.abs(audio) > seuil)
    if actifs.size == 0:
        return audio
    marge = 400
    return audio[max(0, actifs[0] - marge): actifs[-1] + marge]
