# Interfaces avec les autres lots

| Lot | Ce que le lot IA fournit | Ce que le lot IA attend |
|---|---|---|
| Mécanique et électronique — AWADE Constantin Israel | Masse et consommation mesurées du Pi + HAT | Point de fixation, masse disponible, alimentation régulée, refroidissement, anti-vibration |
| Embarqué et station sol — LOGO ADANTO Angelo | Service `sentinelle-ia`, format des événements, récepteur de démonstration (`outils/station_sol_demo.py`) | Mode de lancement du module, réception de l'événement, affichage de l'image, journal côté station, télémétrie (position/attitude) pour le champ `telemetrie` |
| Back-end et documentation — KODJOVI Eli Cédric Ankou | Schéma `schemas/evenement.schema.json` (v1.0), journal SQLite local | Validation du schéma, règles de conservation des preuves |
| Réseau et sécurité — de MEDEIROS Makafui Komlan Léopoldo | Interface `liaison.py` (HTTPS + jeton, ou dossier de dépôt), taille maximale configurable, file d'attente hors connexion | Transport, authentification et chiffrement retenus, limite de taille des messages, comportement en perte de liaison |

## Télémétrie

`Pipeline(config, fournisseur_telemetrie=f)` : `f()` renvoie un dict (latitude, longitude,
altitude, cap, attitude de la nacelle…) fourni par le lot embarqué (ex. lecture MAVLink).
Il est joint tel quel à chaque événement dans `telemetrie`, sans en déduire une position au sol.
