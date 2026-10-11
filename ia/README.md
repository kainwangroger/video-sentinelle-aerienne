# Module d'IA embarquée — Sentinelle Aérienne

Implémentation du lot IA décrit dans `../fiche_technique.docx` (SkyVision Togo, CECFD 2026 — ANAC,
responsable du lot : KAINWANG Roger).

**Chaîne unique** : caméra stabilisée → Raspberry Pi 5 → YOLOv8s compilé pour Hailo → suivi et
contrôle de zone → événement et preuve locale → liaison sécurisée → station au sol.

```
ia/
├── sentinelle_ia/            application embarquée (python -m sentinelle_ia)
│   ├── capture.py            flux caméra horodaté (V4L2, RTSP, GStreamer, Picamera2, vidéo)
│   ├── detecteurs/           hailo (HEF, cible) · onnx · ultralytics · factice · tuiles
│   ├── zone.py               zone d'intérêt (piste et abords)
│   ├── suivi.py              suivi léger, persistance, 1 objet = 1 alerte, statut « à vérifier »
│   ├── anomalie.py           branche expérimentale : écart à une piste libre recalée (désactivée)
│   ├── alerte.py             événement + image de preuve
│   ├── journal.py            journal SQLite local et file d'attente hors connexion
│   ├── liaison.py            envoi HTTPS (jeton, TLS) ou dossier ; reprise automatique
│   ├── metriques.py          débit, latence, température, mémoire (CSV)
│   └── pipeline.py           boucle principale
├── outils/                   données, entraînement, conversion, évaluation, banc, station de démo
├── configs/                  sentinelle.yaml (Pi + Hailo), pc_onnx.yaml, demo.yaml, data_mission.yaml
├── donnees/                  sources, guide d'annotation, inventaire, échantillon synthétique
├── schemas/                  evenement.schema.json (format du message d'alerte)
├── deploiement/              installation Raspberry Pi + service systemd
├── docs/                     conversion Hailo, déploiement, protocole de validation, interfaces
└── tests/                    26 tests (pytest)
```

## Démarrage rapide (PC, sans modèle entraîné)

```bash
cd ia
pip install -r requirements-dev.txt
python -m pytest -q tests                                   # 26 tests
python -m sentinelle_ia --config configs/demo.yaml --sortie-video travail/demo/annotee.mp4
```

La démonstration rejoue une vidéo **synthétique** de survol avec le détecteur factice : elle
exerce zone, suivi, alertes, preuves, journal et liaison (fichiers JSON dans
`travail/demo/station_sol/`). Résultat attendu : 9 objets posés → 9 alertes, artefacts isolés
filtrés. Vidéo annotée : `docs/demo_chaine_factice.mp4`, exemple de message :
`docs/exemple_evenement.json`, exemple de preuve : `docs/exemple_preuve.jpg`.

## Du jeu de données au Raspberry Pi

| Étape | Commande | Où |
|---|---|---|
| Données publiques et poids | `outils/telecharger_donnees.sh` | PC |
| Images du projet → à annoter | `outils/extraire_images_video.py --videos ...` | PC |
| Annotation (CVAT, 3 classes) | voir `donnees/guide_annotation.md` | PC |
| Séparation par séquence | `outils/repartir_sequences.py --source ... --test-impose ...` | PC |
| FOD-A → YOLO (classe débris) | `outils/preparer_fod_a.py --fod-a ...` | PC |
| Contrôles du jeu | `outils/verifier_dataset.py --data ...` | PC |
| Fine-tuning YOLOv8s | `outils/entrainer.py --data configs/data_mission.yaml` | PC (GPU) |
| Export ONNX (forme fixe) | `outils/exporter_onnx.py --poids ...` | PC |
| Calibration INT8 | `outils/preparer_calibration.py --images .../train` | PC |
| Compilation HEF | `outils/compiler_hailo.sh modele.onnx calib/ hailo8` | PC + Hailo DFC |
| Évaluation (rappel, petits objets, fausses alertes) | `outils/evaluer.py --moteur onnx\|hailo ...` | PC / Pi |
| Installation | `deploiement/installer_pi.sh` | Pi |
| Mesures sur banc | `outils/mesurer_embarque.py --duree 1800` | Pi |
| Banc de réception station sol | `outils/station_sol_demo.py --port 8080` | PC station |

Détails : `docs/conversion_hailo.md`, `docs/deploiement_raspberry.md`,
`docs/protocole_validation.md`, `docs/integration_lots.md`, `donnees/README.md`.

## Ce qui a été vérifié, et ce qui reste à valider

Vérifié dans ce dépôt (PC x86, sans accélérateur) :
- 26 tests : suivi (persistance, 1 alerte par objet, artefacts filtrés, objet immobile,
  classe instable ou score faible → « à vérifier », attente qu'un objet entrant soit entier),
  zone d'intérêt, décodage YOLOv8 et NMS, tuiles, branche anomalie, événement conforme au
  schéma, **coupure de liaison puis reprise** sans perte, journal persistant, outils de
  données (FOD-A, séparation par séquence, détection de fuite), chaîne complète ;
- chaîne **entraînement → export ONNX → évaluation** exécutée sur l'échantillon synthétique
  (3 époques CPU) : le détecteur ONNX du module reproduit exactement les résultats
  d'Ultralytics sur le même jeu.

À valider sur la cible (impossible ici : ni Raspberry Pi, ni AI HAT+, ni Hailo DFC) :
- compilation HEF avec la version Hailo installée, et `detecteurs/hailo.py` sur l'AI HAT+ ;
- capture depuis la sortie vidéo réelle de la nacelle ;
- toutes les performances : **aucun taux n'est annoncé avant mesure** avec le modèle
  compilé, la résolution et le matériel définitifs.

Les modèles entraînés ne sont pas versionnés ; le modèle d'essai sur données synthétiques
n'a aucune valeur opérationnelle.

## Limites assumées

L'IA fournit une **aide à l'inspection** : elle ne certifie pas qu'une piste est libre et ne
commande pas l'aéronef. Les objets inconnus sont signalés « à vérifier » quand un candidat
crédible n'a pas de classe fiable ; aucune détection universelle n'est revendiquée. La position
au sol n'est jamais transmise avant calibration et mesure de l'erreur.

Licences : Ultralytics YOLOv8 est sous AGPL-3.0 ; FOD-A impose la citation de ses auteurs.
