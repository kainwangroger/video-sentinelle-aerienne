"""Contenu de la vidéo « SA-1 : de la conception au premier vol » (suit drone/guide_conception_assemblage.md)."""

from az.contenu import _assembler

from .chapitres_a import CHAPITRES as CA
from .chapitres_b import CHAPITRES as CB

CHAPITRES = CA + CB
SCENES = _assembler(CHAPITRES)
DESCRIPTIONS = {}
