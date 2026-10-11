# FICHE TECHNIQUE

Conception du module d’intelligence artificielle embarquée


Sentinelle Aérienne  |  SkyVision Togo  |  CECFD 2026 — ANAC


Responsable du lot : KAINWANG Roger


## 1. Décision de conception


La solution de référence repose sur un Raspberry Pi 5 associé à un Raspberry Pi AI HAT+ 26 TOPS. Il analysera localement le flux de la caméra stabilisée et détectera simultanément trois familles prioritaires : les personnes, les véhicules et les objets ou débris au sol. Un suivi vidéo léger reliera les détections d’une image à l’autre et évitera de répéter la même alerte.


Le modèle retenu est un détecteur YOLOv8s pré-entraîné, adapté par fine-tuning sur des images de débris de piste et des séquences aériennes représentatives. Le fine-tuning est privilégié par rapport à un entraînement depuis zéro : les poids pré-entraînés fournissent déjà des caractéristiques visuelles utiles, tandis que les données propres à la mission serviront à adapter le modèle aux petits objets, à la caméra et à l’angle de vue du drone. Le modèle sera entraîné sur ordinateur, converti pour l’accélérateur Hailo, puis mesuré sur le Raspberry Pi.


La détection des objets connus constitue la première fonction. Pour les objets jamais rencontrés, le système produira un signal prudent « présence à vérifier » si un candidat est repéré sans classe fiable. Une détection d’anomalie fondée sur une référence de piste libre pourra compléter ce mécanisme après validation de l’alignement des images. Cette fonction ne constitue pas une reconnaissance garantie de tout objet inconnu.


Cette conception met en œuvre les engagements déjà soumis à l’ANAC : traitement d’images à bord, détection d’anomalies et d’objets, caméra stabilisée jour/nuit et fonctionnement sans dépendre en permanence d’une connexion. La cartographie reste une extension prévue dans la fiche projet; elle n’est pas requise pour le premier démonstrateur IA.


## 2. Périmètre fonctionnel


## 3. Architecture retenue


Le module forme une chaîne unique de capture, d’inférence et d’alerte. La détection est réalisée sur l’accélérateur; le suivi vidéo, le contrôle de zone et la journalisation sont des traitements logiciels légers exécutés par le Raspberry Pi.


Schéma fonctionnel : caméra stabilisée → Raspberry Pi 5 → YOLOv8s compilé pour Hailo → suivi et contrôle de zone → événement et preuve locale → liaison sécurisée → station au sol.


Un modèle génératif ou un grand modèle vision-langage n’est pas retenu comme détecteur principal. La tâche exige une sortie stable, localisée et rapide sur de petites cibles; un détecteur compact est plus directement mesurable et adapté à l’accélération disponible. La segmentation n’est pas retenue pour la première version : des rectangles suffisent pour repérer et signaler les objets, avec un coût de calcul et d’annotation plus faible.


## 4. Modèle et traitement des objets inconnus


### 4.1 Détecteur multi-catégories


Un détecteur YOLOv8s unique est retenu pour les trois classes initiales. Le modèle prendra une image en entrée et renverra, pour chaque candidat, une classe, un score et un rectangle. Les personnes et véhicules bénéficient du pré-entraînement général; les objets de piste nécessitent une adaptation avec FOD-A et les images recueillies depuis la caméra du projet.


Le premier essai utilisera une entrée de 640 × 640 pixels afin de comparer débit et qualité. Si les petits objets occupent trop peu de pixels, une entrée plus grande ou le découpage de la zone de piste en tuiles sera évalué. Ce réglage ne sera retenu que si la compilation Hailo et la cadence mesurée restent compatibles avec la mission.


### 4.2 Objets sans classe connue


Un détecteur supervisé ne sait reconnaître que ce que les exemples et les classes lui apprennent. Le cas des objets inconnus sera traité à deux niveaux :

- Pendant la première version, toute proposition suffisamment crédible mais sans classe stable sera journalisée comme « objet à vérifier », accompagnée de son image. Le seuil sera réglé sur un jeu de validation contenant des scènes vides et difficiles.
- En complément, une détection d’anomalie sera testée sur la surface de la piste : les images d’une piste libre formeront la référence d’apparence. Comme le drone se déplace, cette comparaison ne sera activée que si la stabilisation et l’alignement entre l’image observée et la référence sont suffisamment fiables.
- Le suivi vidéo confirmera la persistance spatiale d’un candidat sur plusieurs images. Il réduira les alertes causées par un seul artefact sans écarter immédiatement un objet immobile.

Cette approche distingue la détection des classes connues du signalement d’une présence inhabituelle. Elle permet de présenter honnêtement ce qui est mesuré et ce qui reste à valider.


## 5. Données d’entraînement et protocole


### 5.1 Sources de données


### 5.2 Collecte et annotation


Le jeu local sera constitué à partir de séquences distinctes couvrant les distances, les angles, l’éclairage et les objets que la mission doit traiter. Chaque image retenue sera annotée par rectangles et par classe. Les images trop floues ou sur lesquelles la cible est indiscernable seront écartées ou marquées comme non évaluables, plutôt que transformées en exemples trompeurs.

- Catégories v1 : personne, véhicule, débris/objet au sol; l’objet précis peut être conservé dans une note d’annotation sans créer prématurément une classe rare.
- Chaque objet visible est annoté, y compris les personnes et véhicules en arrière-plan; les scènes sans objet sont conservées comme exemples négatifs.
- Les vidéos sont réparties par séquence ou session : entraînement, validation et test ne contiendront pas des images presque identiques de la même séquence.
- Un jeu de test final reste isolé jusqu’à l’évaluation. Il inclut des conditions et objets qui n’ont pas servi au réglage du modèle.
- La collecte sur un site aéronautique réel est réalisée uniquement avec l’autorisation du site et selon les consignes de sécurité. Les premières mises en scène se font sur une surface contrôlée.

### 5.3 Entraînement et conversion


Le fine-tuning partira des poids pré-entraînés de YOLOv8s et les adaptera aux catégories et aux images de la mission. Les expériences seront conduites sur ordinateur; l’entraînement sur Raspberry Pi n’est ni nécessaire ni recommandé. La sélection du modèle reposera sur le rappel des petits objets et le nombre de fausses alertes, et non sur un score global seul.


La conversion personnalisée dépend des versions de Hailo Dataflow Compiler, du Model Zoo et du modèle exporté. La compilation d’un modèle YOLOv8s de test précédera l’entraînement complet. En cas d’incompatibilité, un détecteur de la famille officiellement prise en charge par la version Hailo installée sera retenu pour la même tâche.


## 6. Traitement embarqué et format d’alerte


La position GPS du drone ne donne pas à elle seule la position précise de l’objet vu au sol. Le calcul dépend de l’orientation de la caméra, de sa calibration, de l’altitude et de la géométrie de la scène. Aucune coordonnée ne sera présentée comme exacte avant validation de cette chaîne.


## 7. Matériel et logiciels nécessaires


Le HAT+ 26 TOPS est recommandé pour conserver une marge de calcul sur les images détaillées et permettre, si les essais le justifient, un traitement complémentaire. Cette capacité ne garantit pas un débit donné : seule la mesure avec la caméra et le modèle compilé établira la cadence réelle.


## 8. Validation et critères de réussite


La validation suivra trois conditions représentatives : vidéos enregistrées, caméra sur banc, puis plateforme au sol avant tout essai en vol autorisé. Les résultats annoncés correspondront aux mesures obtenues avec le modèle compilé, la résolution et le matériel définitifs.


Les seuils chiffrés seront établis après le premier test de référence, à partir du débit vidéo et des contraintes de mission réellement confirmés. Aucun taux de précision ou de détection ne sera annoncé avant mesure.


## 9. Risques techniques et réponses prévues


## 10. Interfaces avec les autres lots


Le lot IA couvre le modèle, les données, l’application d’inférence, le filtrage et les mesures de performance. Son intégration s’appuie sur les interfaces matérielles et logicielles des lots concernés.


## 11. Livrables du lot IA

- Code du pipeline de capture, détection, suivi, contrôle de zone, alerte et journalisation.
- Jeu de données v1 ou inventaire des sources, guide des classes, annotations et règles de séparation des séquences.
- Poids entraînés, modèle compilé pour le Hailo retenu et procédure de déploiement sur Raspberry Pi.
- Format du message d’alerte et exemple d’événement avec image de preuve.
- Rapport d’évaluation sur données séparées, avec rappel par classe, fausses alertes, latence, débit, consommation, température et limites observées.
- Démonstration reproductible sur vidéo, puis sur caméra quand l’interface matérielle est disponible.

## 12. Références techniques


Ces références documentent les données étudiées, la plateforme embarquée et la chaîne de conversion du modèle.

- FOD-A — dépôt du jeu de données
- Étude FOD-A — description scientifique du jeu de données
- YOLO-URD — étude récente sur la détection FOD par UAV
- Raspberry Pi — AI HAT+ et variantes 13/26 TOPS
- Raspberry Pi — logiciel IA sur Raspberry Pi 5
- Hailo Apps — exemple officiel de réentraînement YOLOv8 et conversion HEF

### Tableau 1

| Fonction | Réalisation retenue |
|---|---|
| Zone analysée | Piste et abords visibles dans la caméra, à l’intérieur d’une zone d’intérêt définie dans l’image ou fournie par l’interface de mission. |
| Classes du premier modèle | Personne; véhicule; objet/débris au sol. La classe débris regroupe d’abord les objets afin d’éviter de disperser les exemples entre trop de catégories rares. |
| Événement transmis | Classe proposée, score, rectangle de détection, image de preuve, heure et statut de transmission. La position au sol est ajoutée seulement si la géométrie caméra-sol permet de la calculer avec une précision évaluée. |
| Traitement | Inférence à bord, sans envoi d’image vers un service cloud. La liaison sert à transmettre les alertes à la station au sol. |
| Limite | L’IA fournit une aide à l’inspection. Elle ne certifie pas qu’une piste est libre et ne commande pas l’aéronef. |

### Tableau 2

| Bloc | Rôle dans le système |
|---|---|
| Caméra stabilisée du projet | Fournir un flux visible exploitable par le programme. L’interface vidéo réelle sera raccordée à l’entrée correspondante du Raspberry Pi ou à un encodeur/flux intermédiaire déjà prévu par le projet. |
| Raspberry Pi 5 | Recevoir les images, exécuter le programme de vision, appliquer la zone d’intérêt, horodater et journaliser les événements. |
| AI HAT+ 26 TOPS | Exécuter le réseau de détection compatible localement. La variante 26 TOPS laisse davantage de marge pour les images détaillées et les traitements parallèles; elle sera vérifiée sur le flux réel avant intégration mécanique. |
| Suivi et règle de zone | Associer les détections successives, confirmer qu’un objet persiste et éviter les alertes répétées. Le suivi n’est pas un second modèle d’IA. |
| Journal et liaison | Conserver une preuve locale et transmettre un message structuré à la station via l’interface sécurisée définie par le lot réseau. |

### Tableau 3

| Source | Usage prévu et limites |
|---|---|
| FOD-A | Source publique de départ pour les objets étrangers de piste : 31 catégories annoncées et plus de 30 000 instances annotées. Les vues piste/taxiway et les conditions lumière/météo sont utiles pour apprendre les débris; elles ne remplacent pas les vues aériennes de la caméra du projet. |
| Images propres au projet | Source indispensable pour adapter le modèle à la hauteur, à l’angle, à la stabilisation, à la résolution et aux conditions lumineuses de la mission. Les séquences seront filmées avec la caméra retenue, sur une surface d’essai autorisée, avec objets placés à des distances contrôlées. |
| Données aériennes publiées | L’étude YOLO-URD de 2026 décrit une collecte UAV de FOD à 2–6 m et environ 6 000 images brutes extraites. L’accès et les conditions de réutilisation seront vérifiés avant son intégration; le dispositif ne dépend pas de la disponibilité de ces données. |
| Exemples négatifs | Piste vide, marquages, ombres, reflets, flaques, herbe, salissures et objets hors de la zone. Ils servent à réduire les fausses alertes. |

### Tableau 4

| Étape | Résultat contrôlé |
|---|---|
| 1. Préparer | Convertir les annotations vers le format du détecteur, vérifier les classes, les boîtes, les doublons et la séparation par séquence. |
| 2. Adapter | Fine-tuner YOLOv8s pré-entraîné avec FOD-A et les images locales; comparer une version avec données aériennes supplémentaires seulement si leur accès et leur licence le permettent. |
| 3. Évaluer | Mesurer précision, rappel et erreurs par classe; examiner séparément les petits objets, les scènes vides et les conditions d’éclairage. |
| 4. Exporter | Exporter le meilleur modèle en ONNX avec une forme d’entrée fixée, puis le compiler au format HEF pour le Hailo visé à l’aide de la chaîne Hailo compatible. |
| 5. Quantifier et contrôler | Utiliser des images représentatives pour la calibration INT8; comparer le modèle compilé au modèle d’origine sur le même jeu de test et vérifier que la baisse de rappel reste acceptable. |
| 6. Déployer | Installer le HEF et l’application de capture/alerte sur Raspberry Pi 5; mesurer débit, latence, température, consommation et pertes d’images avec la caméra réelle. |

### Tableau 5

| Traitement | Comportement retenu |
|---|---|
| Capture | Lire le flux caméra réellement fourni et horodater les images. |
| Inférence | Envoyer les images préparées au modèle compilé sur Hailo et récupérer classe, score et rectangle. |
| Zone et suivi | Limiter l’analyse utile à la piste et à ses abords; relier les détections proches dans le temps pour éviter les répétitions. |
| Alerte | Créer un événement contenant heure, classe ou statut « à vérifier », score, rectangle, identifiant de séquence et image de preuve. |
| Position | N’ajouter une coordonnée au sol qu’après calibration de la caméra et association avec l’altitude, l’orientation et la position du drone. |
| Hors connexion | Poursuivre l’inférence et stocker les événements localement; les transmettre quand la liaison sécurisée est disponible. |

### Tableau 6

| Élément | Configuration de référence |
|---|---|
| Calcul embarqué | Raspberry Pi 5, mémoire suffisante pour l’OS, le flux caméra et la journalisation; configuration mémoire finalisée après essai de charge. |
| Accélérateur | Raspberry Pi AI HAT+ 26 TOPS avec NPU Hailo-8. Le format compact 13 TOPS reste un repli possible si un test démontre qu’il tient la cadence requise. |
| Caméra | Caméra stabilisée déjà prévue au projet; vérifier le flux vidéo disponible, la résolution, le champ de vision, la latence et le rendu des petits objets. |
| Alimentation et montage | Convertisseur régulé depuis la batterie, refroidissement du Pi, fixation anti-vibration et câblage protégé. Le bilan de masse et de courant doit être vérifié avec la cellule. |
| Stockage | Carte microSD fiable pour le système et le journal; conserver les images d’alerte et non la vidéo complète en permanence, sauf besoin d’essai défini. |
| Développement | Python, OpenCV, PyTorch/Ultralytics pour l’adaptation YOLOv8s, format ONNX, outils Hailo pour compilation/quantification, et CVAT ou outil équivalent pour les annotations. |
| Banc d’essai | Ordinateur de développement, vidéos, caméra, Raspberry Pi, HAT, alimentation régulée, refroidissement et instruments pour observer courant et température. |

### Tableau 7

| Mesure | Méthode de vérification |
|---|---|
| Rappel par classe | Part des personnes, véhicules et débris annotés effectivement détectés; isoler les petits objets et les conditions difficiles. |
| Fausses alertes | Nombre d’alertes sur scènes vides, marquages, ombres, reflets et végétation, rapporté à la durée de la séquence. |
| Latence et débit | Délai image-alerte et images traitées par seconde avec le flux caméra réel. |
| Stabilité | Température, consommation, mémoire, pertes d’images et fonctionnement prolongé sur le Raspberry Pi. |
| Hors connexion | Vérifier que l’analyse et l’enregistrement local se poursuivent lorsque la liaison est coupée, puis que les événements en attente sont récupérables. |
| Alerte exploitable | Faire vérifier si l’image, la classe, l’heure et la zone permettent à un opérateur de retrouver rapidement l’objet. |

### Tableau 8

| Risque | Réponse de conception |
|---|---|
| Débris trop petits dans l’image | Vérifier leur taille en pixels avec la caméra et la hauteur prévues; ajuster optique, résolution ou zone découpée avant de conclure sur le modèle. |
| Écart entre les images publiques et la vue drone | Fine-tuner avec des images propres à la caméra et garder des séquences aériennes indépendantes pour le test. |
| Objet inconnu non reconnu | Produire un candidat « à vérifier » et tester une branche d’anomalie sur référence alignée; ne pas revendiquer une détection universelle. |
| Fausses alertes dues aux ombres ou marquages | Ajouter des scènes négatives, contrôler la zone d’intérêt, suivre les candidats dans plusieurs images et régler les seuils sur validation. |
| Modèle incompatible ou trop lent sur Hailo | Compiler un modèle de test tôt, comparer les versions 640/plus détaillée et retenir un réseau compatible après mesure embarquée. |
| Vibration, chaleur ou alimentation insuffisante | Mesurer sur banc puis plateforme, refroidir et faire valider masse, courant et fixation avant le vol. |
| Position d’alerte imprécise | Transmettre l’image et la zone caméra; n’ajouter la géolocalisation qu’après calibration et validation d’erreur. |

### Tableau 9

| Lot concerné | Interface attendue pour l’intégration |
|---|---|
| Mécanique et électronique — AWADE Constantin Israel | Point de fixation, masse disponible, alimentation régulée, refroidissement et maintien contre les vibrations. |
| Embarqué et station sol — LOGO ADANTO Angelo | Mode de lancement du module, réception de l’événement, affichage de l’image et journal côté station. |
| Back-end et documentation — KODJOVI Eli Cédric Ankou | Schéma du message d’événement et règles de conservation des preuves. |
| Réseau et sécurité — de MEDEIROS Makafui Komlan Léopoldo | Transport de l’événement, authentification/chiffrement existants, limite de taille et comportement en perte de liaison. |
