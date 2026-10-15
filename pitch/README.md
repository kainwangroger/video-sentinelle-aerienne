# Pitch « Sentinelle Aérienne »

| Fichier | Contenu |
|---|---|
| `sentinelle_aerienne_presentation_complete.pptx` + `script_oral_presentation_complete.docx` | **Présentation complète, 24 diapos (≈ 20 min)** : drone et composants (vues SolidWorks annotées et zooms), technologies, IA, liaisons, avantages, risques, réglementation, sécurité, applications, calendrier, budget. |
| `sentinelle_aerienne_pitch_court.pptx` | **Version 9 diapos**, selon le plan de l'équipe (≈ 10 min). Notes d'oral dans chaque diapo. |
| `sentinelle_aerienne_pitch_complet.pptx` | Version 17 diapos (≈ 13 min), plus détaillée. Notes d'oral dans chaque diapo. |
| `script_oral_court.md` / `.docx` | Script oral de la version 9 diapos, par intervenant. |
| `script_oral_complet.md` / `.docx` | Script oral de la version 17 diapos. |
| `sentinelle_aerienne_risques_securite.pptx` + `script_oral_risques.docx` | Avantages, risques, réglementation et sécurité (7 diapos, ≈ 6 min). |
| `questions_reponses.md` / `.docx` | 10 questions probables du jury par personne, avec réponses. |
| `assets/cao/` | Captures SolidWorks du drone (`sources/`) et versions recadrées. |
| `assets/composants/` | Photos d'exemples de composants, avec sources et licences (`SOURCES.md`). |
| `outils/` | `preparer_images.py` (recadrage), `intervenants.js`, `contenu_court.js`, `contenu_complet.js` (textes et notes), `generer.js` (PowerPoint + scripts). |

Le drone présenté est celui de la CAO SolidWorks : VTOL à rotors basculants (deux moteurs avant
basculants en nacelle, un moteur arrière pour le vol vertical), empennage en V.

Régénérer :

```bash
python3 pitch/outils/preparer_images.py
node pitch/outils/generer.js            # modules : pptxgenjs, sharp
for f in script_oral_court script_oral_complet questions_reponses; do
  python3 drone/outils/md_vers_docx.py pitch/$f.md pitch/$f.docx; done
```
