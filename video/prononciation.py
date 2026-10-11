"""Prononciation de la voix off : remplacements appliqués au seul texte lu."""

# Remplacements appliqués uniquement au texte lu par la voix off.
# L'ordre compte : les expressions longues avant les plus courtes.
PRONONCIATION = [
    ("730 000 et 1 400 000 FCFA", "sept cent trente mille et un million quatre cent mille francs CFA"),
    ("30 à 45 minutes", "trente à quarante-cinq minutes"),
    ("30 septembre 2026", "trente septembre deux mille vingt-six"),
    ("7 décembre 2026", "sept décembre deux mille vingt-six"),
    ("AWADE Constantin Israel", "Awadé Constantin Israël"),
    ("VTOL", "vétol"),
    ("SolidWorks", "Solide-Worx"),
    ("ESC", "E S C"),
    ("Pixhawk", "Pixe-hok"),
    ("ArduPilot", "Ardou-pilote"),
    ("PX4", "P X quatre"),
    ("MAVLink", "Mave-linque"),
    ("LiPo", "Lipo"),
    ("fail-safe", "faïl-sèfe"),
    ("GPS", "G P S"),
    ("2026", "deux mille vingt-six"),
    ("640 × 640", "six cent quarante par six cent quarante"),
    ("AI HAT+", "A I Hatte plus"),
    ("26 TOPS", "vingt-six tops"),
    ("NPU Hailo-8", "N P U Haïlo huit"),
    ("Hailo", "Haïlo"),
    ("Raspberry Pi 5", "Raspberry Paï cinq"),
    ("Raspberry Pi", "Raspberry Paï"),
    ("YOLOv8s", "Yolo vé huit esse"),
    ("FOD-A", "Fod A"),
    ("ONNX", "Onix"),
    ("HEF", "H E F"),
    ("INT8", "entiers huit bits"),
    ("SkyVision", "Skaï Vision"),
    ("CECFD", "C E C F D"),
    ("ANAC", "Anac"),
    ("30 000", "trente mille"),
    ("fine-tuning", "affinage"),
    ("back-end", "bak-ènde"),
    ("cloud", "claoude"),
    ("l'IA", "l'I A"),
    ("une IA", "une I A"),
    ("« à vérifier »", "à vérifier"),
]


def texte_parle(phrase: str) -> str:
    for ecrit, dit in PRONONCIATION:
        phrase = phrase.replace(ecrit, dit)
    return phrase
