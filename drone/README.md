# Dossier drone — Sentinelle Aérienne SA-1

Documentation complète du drone hybride VTOL, écrite pour être comprise par un débutant.

| Fichier | Contenu |
|---|---|
| [`fiche_technique_complete.md`](fiche_technique_complete.md) | **La fiche technique complète** : bases, chaque composant expliqué, performances, mission, sécurité, budget |
| [`fiche_technique_complete.docx`](fiche_technique_complete.docx) / [`.pdf`](fiche_technique_complete.pdf) | Même contenu au format Word et PDF (imprimable, schémas inclus) |
| [`glossaire.md`](glossaire.md) | Tous les termes techniques expliqués |
| [`calculs/dimensionnement.py`](calculs/dimensionnement.py) | Calcul des masses, portance, puissances et autonomie (hypothèses modifiables) |
| [`calculs/resultats.md`](calculs/resultats.md) | Résultats du calcul |
| [`parametres_ardupilot/sentinelle_sa1.param`](parametres_ardupilot/sentinelle_sa1.param) | Paramètres de départ du contrôleur de vol (commentés) |
| [`checklists/`](checklists/) | Avant vol, après vol, procédures d'urgence |
| [`schemas/`](schemas/) | 15 schémas : vues du drone, architecture, forces, moteur, transition, énergie, capteurs, liaisons, IA… |
| [`outils/`](outils/) | `generer_schemas.py` (schémas PNG) et `md_vers_docx.py` (Markdown → Word) |

La vidéo longue « Le SA-1 de A à Z » (`output/sa1_de_a_a_z/`, 16 chapitres) reprend ce contenu,
avec une mission simulée complète.

Régénérer : `python3 drone/calculs/dimensionnement.py --markdown`, `python3 drone/outils/generer_schemas.py`,
`python3 drone/outils/md_vers_docx.py` (puis `soffice --headless --convert-to pdf` pour le PDF).

Les chiffres sont des **estimations de conception** à confirmer par les essais.
