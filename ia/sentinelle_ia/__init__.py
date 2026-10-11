"""Module d'IA embarquée Sentinelle Aérienne.

Chaîne : capture -> détection (YOLOv8s, Hailo/ONNX/PyTorch) -> zone d'intérêt -> suivi
-> événement et preuve locale -> file d'attente -> liaison vers la station au sol.
"""

__version__ = "0.1.0"

CLASSES = ("personne", "vehicule", "debris")
STATUT_A_VERIFIER = "a_verifier"
STATUT_CONFIRME = "classe_confirmee"
