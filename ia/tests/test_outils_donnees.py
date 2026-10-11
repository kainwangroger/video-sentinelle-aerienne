import numpy as np

from generer_donnees_synthetiques import generer_jeu
from preparer_fod_a import convertir
from repartir_sequences import repartir
from verifier_dataset import verifier

VOC = """<annotation><filename>{nom}.jpg</filename><size><width>300</width><height>300</height><depth>3</depth></size>
<object><name>Bolt</name><bndbox><xmin>10</xmin><ymin>20</ymin><xmax>40</xmax><ymax>50</ymax></bndbox></object>
<object><name>Wrench</name><bndbox><xmin>100</xmin><ymin>100</ymin><xmax>160</xmax><ymax>130</ymax></bndbox></object>
</annotation>"""


def test_conversion_fod_a_vers_debris(tmp_path):
    from PIL import Image

    for d in ("Annotations", "JPEGImages", "ImageSets/Main"):
        (tmp_path / "foda" / d).mkdir(parents=True)
    for nom in ("a1", "a2"):
        (tmp_path / "foda" / "Annotations" / f"{nom}.xml").write_text(VOC.format(nom=nom))
        Image.new("RGB", (300, 300)).save(tmp_path / "foda" / "JPEGImages" / f"{nom}.jpg")
    (tmp_path / "foda" / "ImageSets" / "Main" / "train.txt").write_text("a1\n")
    (tmp_path / "foda" / "ImageSets" / "Main" / "val.txt").write_text("a2\n")
    compte = convertir(tmp_path / "foda", tmp_path / "yolo")
    assert compte == {"train": 1, "val": 1, "ignorees": 0}
    lignes = (tmp_path / "yolo" / "labels" / "train" / "foda_a1.txt").read_text().split("\n")
    assert all(l.startswith("2 ") for l in lignes if l)  # tout FOD-A -> debris
    x, y, w, h = map(float, lignes[0].split()[1:])
    assert abs(x - 25 / 300) < 1e-5 and abs(w - 30 / 300) < 1e-5
    assert "Wrench" in (tmp_path / "yolo" / "notes_annotations.csv").read_text()


def test_repartition_par_sequence_sans_fuite(tmp_path):
    from PIL import Image

    (tmp_path / "src" / "images").mkdir(parents=True)
    (tmp_path / "src" / "labels").mkdir(parents=True)
    rng = np.random.default_rng(0)
    for s in range(10):
        for k in range(5):
            nom = f"vol-{s:02d}_{k:06d}"
            Image.fromarray(rng.integers(0, 255, (32, 32, 3), dtype=np.uint8)).save(tmp_path / "src" / "images" / f"{nom}.jpg")
            (tmp_path / "src" / "labels" / f"{nom}.txt").write_text("2 0.5 0.5 0.1 0.1\n" if k % 2 else "")
    compte, affectation = repartir(tmp_path / "src", tmp_path / "jeu", 0.2, 0.2, test_impose=["vol-07"])
    assert affectation["vol-07"] == "test"
    assert sum(compte.values()) == 50
    erreurs, _, _ = verifier(tmp_path / "jeu", 640)
    assert erreurs == []


def test_verificateur_detecte_fuite_et_erreurs(tmp_path):
    from PIL import Image

    for split in ("train", "test"):
        (tmp_path / "images" / split).mkdir(parents=True)
        (tmp_path / "labels" / split).mkdir(parents=True)
    img = np.random.default_rng(0).integers(0, 255, (64, 64, 3), dtype=np.uint8)
    Image.fromarray(img).save(tmp_path / "images" / "train" / "vol-a_000001.png")
    Image.fromarray(img).save(tmp_path / "images" / "test" / "vol-a_000002.png")
    (tmp_path / "labels" / "train" / "vol-a_000001.txt").write_text("7 0.5 0.5 0.1 0.1\n")
    (tmp_path / "labels" / "test" / "vol-a_000002.txt").write_text("2 0.99 0.5 0.2 0.1\n")
    erreurs, _, _ = verifier(tmp_path, 640)
    texte = "\n".join(erreurs)
    assert "classe 7" in texte and "hors de l'image" in texte
    assert "Séquence vol-a" in texte and "identique" in texte


def test_jeu_synthetique_valide(tmp_path):
    stats = generer_jeu(tmp_path, 6, 4, 320, np.random.default_rng(3))
    assert stats["train"] + stats["val"] + stats["test"] == 24
    erreurs, _, _ = verifier(tmp_path, 320)
    assert erreurs == []
