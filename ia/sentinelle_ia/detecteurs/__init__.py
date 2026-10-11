"""Détecteurs interchangeables. Tous renvoient une liste de Detection en pixels de l'image d'origine.

- hailo       : modèle HEF compilé, exécuté sur l'AI HAT+ (Raspberry Pi 5) — cible embarquée ;
- onnx        : modèle ONNX exporté, exécuté par onnxruntime (PC ou Pi sans accélérateur) ;
- ultralytics : poids PyTorch .pt (PC de développement) ;
- factice     : lit les annotations d'une vidéo synthétique (tests et démonstration).
"""


def creer_detecteur(config):
    """Crée le détecteur ; `tuiles: [colonnes, lignes]` active l'inférence par tuiles."""
    detecteur = _creer_moteur(config)
    if config.get("tuiles"):
        from .tuiles import DetecteurTuiles
        return DetecteurTuiles(detecteur, tuple(config["tuiles"]), float(config.get("recouvrement_tuiles", 0.2)))
    return detecteur


def _creer_moteur(config):
    moteur = config["moteur"]
    if moteur == "hailo":
        from .hailo import DetecteurHailo
        return DetecteurHailo(config)
    if moteur == "onnx":
        from .onnx import DetecteurOnnx
        return DetecteurOnnx(config)
    if moteur == "ultralytics":
        from .ultralytics import DetecteurUltralytics
        return DetecteurUltralytics(config)
    if moteur == "factice":
        from .factice import DetecteurFactice
        return DetecteurFactice(config)
    raise ValueError(f"Moteur de détection inconnu : {moteur}")
