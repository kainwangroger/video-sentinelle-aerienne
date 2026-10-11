# Guide d'annotation — classes v1

Outil conseillé : **CVAT** (ou équivalent), annotation par **rectangles**, export **YOLO 1.1**.

## Classes

| Indice | Classe | Inclut | N'inclut pas |
|---|---|---|---|
| 0 | `personne` | Toute personne visible, debout, accroupie, partiellement cachée | Ombre seule d'une personne |
| 1 | `vehicule` | Voiture, camion, véhicule de piste, moto, engin, chariot tracté | Aéronef stationné hors zone (à noter en commentaire) |
| 2 | `debris` | Tout objet étranger au sol : boulon, écrou, outil, pièce métallique ou plastique, caillou, bagage, étiquette, canette, bois… | Marquages, joints, taches, flaques, herbe, ombres |

La classe `debris` regroupe tous les objets pour ne pas disperser les exemples entre des
classes rares. **Le type précis** (ex. « clé plate ») va dans l'attribut ou le commentaire de
l'annotation, sans créer de nouvelle classe.

## Règles

1. **Annoter chaque objet visible**, y compris les personnes et véhicules en arrière-plan.
2. Rectangle **serré** autour de la partie visible de l'objet (pas de l'ombre).
3. Objet coupé par le bord de l'image : annoter la partie visible si au moins ~30 % de l'objet est visible.
4. **Scènes sans objet : les conserver** comme exemples négatifs (fichier d'annotation vide).
5. Image trop floue ou cible indiscernable : **écarter l'image** ou la marquer « non évaluable »
   (attribut), plutôt que d'en faire un exemple trompeur.
6. En cas de doute sur la classe d'un objet au sol : `debris` + commentaire « doute ».
7. Une même vidéo = une même séquence : ne pas renommer les fichiers (le préfixe sert à la séparation).

## Contrôle qualité

- Double vérification d'un échantillon de 10 % des images par un second annotateur.
- `python outils/verifier_dataset.py --data <jeu>` avant chaque entraînement.
