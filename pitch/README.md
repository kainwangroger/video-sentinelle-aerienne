# Pitch « Sentinelle Aérienne »

| Fichier | Contenu |
|---|---|
| `sentinelle_aerienne_pitch_court.pptx` | **Version 9 diapos**, selon le plan de l'équipe (≈ 10 min). Notes d'oral dans chaque diapo. |
| `sentinelle_aerienne_pitch_complet.pptx` | Version 17 diapos (≈ 13 min), plus détaillée. Notes d'oral dans chaque diapo. |
| `script_oral_court.md` / `.docx` | Script oral de la version 9 diapos, par intervenant. |
| `script_oral_complet.md` / `.docx` | Script oral de la version 17 diapos. |
| `questions_reponses.md` / `.docx` | 10 questions probables du jury par personne, avec réponses. |
| `assets/cao/` | Captures SolidWorks du drone (`sources/`) et versions recadrées. |
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
