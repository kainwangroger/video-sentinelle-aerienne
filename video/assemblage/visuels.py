"""Table des animations de la vidéo « SA-1 : de la conception au premier vol »."""

from az.animations import ANIMATIONS
from az.gabarits import GABARITS

from .scenes3d import SCENES_3D

AVEC_SCENE = True
SCENES_VISUELLES = {**GABARITS, **ANIMATIONS, **SCENES_3D}
