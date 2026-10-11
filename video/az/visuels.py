"""Table des fonctions d'animation de la vidéo « SA-1 de A à Z »."""

from .animations import ANIMATIONS
from .gabarits import GABARITS
from .simulation import SIMULATION

AVEC_SCENE = True  # chaque fonction reçoit aussi la scène (et ses données)
SCENES_VISUELLES = {**GABARITS, **ANIMATIONS, **SIMULATION}
