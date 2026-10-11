# Protocole de validation

Trois conditions représentatives, dans l'ordre, **avant tout essai en vol autorisé** :

1. **Vidéos enregistrées** (PC puis Pi) : `outils/evaluer.py` sur le test isolé, `python -m sentinelle_ia --source video.mp4`.
2. **Caméra sur banc** : caméra réelle → Pi + HAT, `outils/mesurer_embarque.py`.
3. **Plateforme au sol** : module monté sur le drone au sol, liaison vers la station, essais hors connexion.

Les résultats annoncés correspondent aux mesures obtenues avec **le modèle compilé, la
résolution et le matériel définitifs**. Aucun taux de précision ou de détection n'est annoncé
avant mesure. Les seuils chiffrés sont fixés après le premier test de référence.

| Mesure | Méthode | Outil |
|---|---|---|
| Rappel par classe | Part des personnes, véhicules, débris annotés détectés ; petits objets et conditions difficiles isolés | `outils/evaluer.py` |
| Fausses alertes | Alertes sur scènes vides, marquages, ombres, reflets, végétation, rapportées à la durée | `outils/evaluer.py --videos-vides` |
| Latence et débit | Délai image → alerte et images traitées par seconde avec le flux caméra réel | `outils/mesurer_embarque.py` |
| Stabilité | Température, consommation, mémoire, pertes d'images, fonctionnement prolongé | `outils/mesurer_embarque.py`, instrument du banc |
| Hors connexion | L'analyse et l'enregistrement local continuent liaison coupée ; les événements en attente sont récupérés | `tests/test_alerte_journal_liaison.py`, essai sur plateforme (débrancher la liaison) |
| Alerte exploitable | Un opérateur retrouve-t-il rapidement l'objet avec l'image, la classe, l'heure et la zone ? | `outils/station_sol_demo.py`, essai avec opérateur |

## Réglages à faire sur la validation

- `suivi.seuil_classe` et `suivi.seuil_a_verifier` : compromis rappel / fausses alertes, sur
  un jeu de validation contenant des scènes vides et difficiles.
- `suivi.images_confirmation` : persistance minimale (réduit les artefacts d'une image).
- `detecteur.taille_entree` / `detecteur.tuiles` : selon la taille des débris en pixels.
- `zone_interet.polygone` : piste et abords dans le champ de la caméra.

## Position au sol

La position GPS du drone ne donne pas à elle seule la position de l'objet. Le champ
`position` des événements reste `null` tant que la calibration de la caméra (intrinsèques,
orientation de la nacelle, altitude, géométrie de la scène) n'a pas été faite **et**
que l'erreur de géolocalisation n'a pas été mesurée.
