from sentinelle_ia import STATUT_A_VERIFIER, STATUT_CONFIRME
from sentinelle_ia.suivi import ParametresSuivi, Suivi
from sentinelle_ia.types import Detection, iou
from sentinelle_ia.zone import ZoneInteret


def test_iou():
    assert iou((0, 0, 10, 10), (0, 0, 10, 10)) == 1
    assert iou((0, 0, 10, 10), (20, 20, 30, 30)) == 0
    assert abs(iou((0, 0, 10, 10), (5, 0, 15, 10)) - 1 / 3) < 1e-6


def test_zone_point_au_sol():
    zone = ZoneInteret([(0.25, 0), (0.75, 0), (0.75, 1), (0.25, 1)])
    dedans = Detection("debris", 0.9, (90, 40, 110, 60))
    dehors = Detection("debris", 0.9, (10, 40, 30, 60))
    assert zone.filtrer([dedans, dehors], 200, 100) == [dedans]


def test_zone_par_defaut_toute_image():
    assert ZoneInteret().contient(Detection("x", 1, (1, 1, 5, 5)), 100, 100)


def _det(x, classe="debris", score=0.8):
    return Detection(classe, score, (x, 50, x + 20, 70))


def test_une_seule_alerte_par_objet_persistant():
    suivi = Suivi(ParametresSuivi(images_confirmation=3))
    alertes = []
    for n in range(30):
        alertes += suivi.mettre_a_jour(n, [_det(100 + n * 2)])  # objet qui glisse dans l'image (drone en mouvement)
    assert len(alertes) == 1
    classe, statut, _ = alertes[0].classe_et_statut(suivi.p)
    assert (classe, statut) == ("debris", STATUT_CONFIRME)


def test_artefact_isole_sans_alerte():
    suivi = Suivi(ParametresSuivi(images_confirmation=3))
    alertes = suivi.mettre_a_jour(0, [_det(300)])
    for n in range(1, 10):
        alertes += suivi.mettre_a_jour(n, [])
    assert alertes == []


def test_objet_immobile_reste_suivi_sans_repetition():
    suivi = Suivi(ParametresSuivi(images_confirmation=2, images_perdues_max=5))
    alertes = []
    for n in range(50):
        alertes += suivi.mettre_a_jour(n, [_det(200)] if n % 3 else [])  # oublis réguliers
    assert len(alertes) == 1


def test_classe_instable_donne_a_verifier():
    suivi = Suivi(ParametresSuivi(images_confirmation=4, part_classe_min=0.7))
    alertes = []
    for n, classe in enumerate(["debris", "vehicule", "debris", "personne", "vehicule"]):
        alertes += suivi.mettre_a_jour(n, [_det(100, classe)])
    assert len(alertes) == 1
    assert alertes[0].classe_et_statut(suivi.p)[1] == STATUT_A_VERIFIER


def test_score_faible_donne_a_verifier():
    suivi = Suivi(ParametresSuivi(images_confirmation=3, seuil_classe=0.5))
    alertes = []
    for n in range(4):
        alertes += suivi.mettre_a_jour(n, [_det(100, score=0.4)])
    assert alertes[0].classe_et_statut(suivi.p)[1] == STATUT_A_VERIFIER


def test_deux_objets_deux_alertes():
    suivi = Suivi(ParametresSuivi(images_confirmation=3))
    alertes = []
    for n in range(6):
        alertes += suivi.mettre_a_jour(n, [_det(100), _det(400, "personne")])
    assert sorted(a.classe_et_statut(suivi.p)[0] for a in alertes) == ["debris", "personne"]


def test_candidat_trop_faible_ignore():
    suivi = Suivi(ParametresSuivi(images_confirmation=3, seuil_a_verifier=0.3))
    alertes = []
    for n in range(10):
        alertes += suivi.mettre_a_jour(n, [_det(100, score=0.18)])
    assert alertes == []


def test_attend_objet_entier_avant_confirmation():
    suivi = Suivi(ParametresSuivi(images_confirmation=3, marge_bord=0.05, images_max_au_bord=20))
    alertes, confirmation = [], None
    for n in range(15):
        y = -10 + n * 8                                   # l'objet entre par le haut de l'image
        nouvelles = suivi.mettre_a_jour(n, [Detection("debris", 0.8, (100, y, 120, y + 20))], (400, 300))
        if nouvelles and confirmation is None:
            confirmation = n
        alertes += nouvelles
    assert len(alertes) == 1
    assert alertes[0].boite[1] >= 0.05 * 300            # confirmé une fois entier dans l'image
