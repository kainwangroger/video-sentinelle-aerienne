# Pitch « Sentinelle Aérienne »

| Fichier | Contenu |
|---|---|
| `sentinelle_aerienne_pitch.pptx` | Présentation PowerPoint (17 diapos). Le script de chaque intervenant est dans les **notes de l'orateur**. |
| `script_oral.md` / `script_oral.docx` | Script oral complet par intervenant, ordre de passage, minutage (≈ 13 min) et questions probables du jury. |
| `sentinelle_aerienne_pitch_v2.pptx` | **Version 9 diapos** (plan de l'équipe : double cœur STM32H7 + Hailo, innovations, polyvalence), notes d'oral dans chaque diapo. |
| `notes_oral_v2.md` / `notes_oral_v2.docx` | Notes d'oral de la version 9 diapos (≈ 10 min). |
| `assets/` | Images utilisées (maquette 3D du SA-1, schémas du dépôt). |
| `outils/` | Générateurs : `preparer_images.py` (images), `contenu_pitch.js` (textes et script), `generer_pitch.js` (PowerPoint + script). |

Ordre de passage : Israel → Angelo → Makafui → Roger → Cédric → Israel (budget et conclusion).
Chaque intervenant commence par se présenter.

Régénérer :

```bash
python3 pitch/outils/preparer_images.py
node pitch/outils/generer_pitch.js          # version 17 diapos
node pitch/outils/generer_pitch_v2.js       # version 9 diapos ; modules : pptxgenjs react react-dom react-icons sharp
python3 drone/outils/md_vers_docx.py pitch/script_oral.md pitch/script_oral.docx
```
