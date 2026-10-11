# Résultats du dimensionnement (estimations)

Généré par `python drone/calculs/dimensionnement.py --markdown`. Hypothèses en tête du script.

| Grandeur | Valeur |
|---|---|
| Densité de l'air (35 °C) | 1.132 kg/m³ |
| Masse des composants | 6.20 kg |
| Masse maximale au décollage (avec marge) | 6.40 kg |
| Surface alaire | 0.56 m² |
| Allongement | 7.1 |
| Charge alaire | 11.4 kg/m² |
| Vitesse de décrochage | 12.3 m/s (44 km/h) |
| Vitesse minimale de fin de transition (1,25 × décrochage) | 15.4 m/s |
| Coefficient de portance en croisière | 0.55 |
| Poussée maximale requise par moteur VTOL | 2.9 kgf |
| Puissance en vol stationnaire | 1045 W (47 A, 2.9 C) |
| Traînée en croisière | 7.4 N |
| Puissance en croisière | 280 W (12.6 A) |
| Énergie de la batterie | 355 Wh (utilisable 284 Wh) |
| Énergie du vol stationnaire (2 min) | 35 Wh |
| Autonomie estimée (croisière + stationnaire) | 52 min |
| Distance parcourable en croisière | 57 km |

## Bilan de masse

| Élément | Masse (kg) |
|---|---|
| Cellule : aile, fuselage, poutres, empennage (carbone/composite) | 1.90 |
| 4 moteurs de sustentation (classe 4014, ~150 g) | 0.62 |
| 4 contrôleurs ESC 40 A | 0.16 |
| 4 hélices de sustentation 15 pouces carbone | 0.08 |
| Moteur de croisière (classe 3520) + ESC 60 A + hélice 13 pouces | 0.29 |
| 4 servomoteurs de gouvernes | 0.12 |
| Batterie LiPo 6S 16 000 mAh | 2.05 |
| Contrôleur de vol + module de puissance | 0.10 |
| GNSS + compas, capteur de vitesse air, télémètre laser | 0.10 |
| Radio télémétrie + récepteur RC + antennes | 0.06 |
| Raspberry Pi 5 + AI HAT+ 26 TOPS + boîtier ventilé | 0.12 |
| Nacelle gyrostabilisée + caméra visible + module thermique | 0.35 |
| Câblage, connecteurs, BEC, fixations | 0.25 |
| Marge d'intégration | 0.20 |
| **Total** | **6.40** |

L'autonomie estimée dépasse la cible du concours (30–45 min) : la marge couvre le vent, la chaleur, le vieillissement de la batterie et les écarts entre estimation et réalité. Seuls les essais en vol font foi.
