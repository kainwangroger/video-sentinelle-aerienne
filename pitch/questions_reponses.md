# Préparation au jury : 10 questions par personne

Pitch « Sentinelle Aérienne » · SkyVision Togo · CECFD 2026 — ANAC

**Comment l'utiliser**

- Chacun lit ses 10 questions, puis s'entraîne à répondre **à voix haute en 30 secondes maximum**, sans lire.
- Les réponses s'appuient sur la fiche projet, la fiche technique IA, la CAO SolidWorks (VTOL à rotors basculants, empennage en V) et le code `ia/`.
- La mention **[à confirmer]** signale un choix que l'équipe doit encore figer. Si c'est le cas le jour J, on le dit franchement : « c'est en cours de validation, voici notre piste ».
- Règle d'or : **ne jamais inventer un chiffre**. « Nous le mesurerons sur banc » vaut mieux qu'un chiffre faux.

---

## 1. AWADE Constantin Israel — Mécanique, électronique, conception 3D

**1. Pourquoi un VTOL à rotors basculants plutôt qu'un multirotor ou un avion ?**
Le multirotor décolle partout mais porte tout son poids avec ses moteurs : il vole peu de temps. L'avion vole longtemps mais il lui faut une piste. Notre drone fait les deux. Et contrairement à un quadplane, qui transporte en croisière quatre moteurs arrêtés, nos deux moteurs avant servent au décollage **et** à la croisière : moins de masse inutile, moins de traînée.

**2. Pourquoi trois moteurs et pas quatre ?**
C'est plus léger et ça consomme moins. En vol stationnaire, le contrôle du lacet (rotation sur lui-même) se fait en inclinant légèrement les deux moteurs avant en sens opposé : pas besoin d'un quatrième moteur. La contrepartie, c'est qu'il n'y a pas de redondance en stationnaire. On limite donc cette phase au décollage et à l'atterrissage.

**3. Comment fonctionne le basculement des moteurs ?**
Chaque nacelle a un servomoteur commandé par le contrôleur de vol. Les moteurs passent progressivement de la position verticale à la position horizontale pendant la transition. Nous choisissons des servos à engrenages métal, avec une bonne marge de couple, et nous les testons au banc avant le vol.

**4. Et si un servo de basculement se bloque ?**
C'est le point critique de cette configuration, et nous le traitons sérieusement. Le débattement des servos est vérifié à chaque check-list avant vol. Si un servo se bloque en position verticale, le drone reste en mode multirotor et atterrit à la verticale. Les essais de transition se font d'abord à hauteur de sécurité, au-dessus d'une zone dégagée.

**5. Pourquoi un empennage en V ?**
Deux surfaces au lieu de trois (dérive + profondeur), donc moins de masse, moins de traînée et moins de servos. Chaque gouverne agit à la fois en profondeur et en direction ; ArduPilot fait ce mélange automatiquement. Et cette forme laisse la place au moteur arrière sous la queue.

**6. Quelles sont les dimensions et la masse du drone ?**
**[à compléter avec les valeurs SolidWorks]** : envergure, longueur, masse au décollage. Préparez une réponse chiffrée et sachez dire comment la masse a été obtenue (bilan composant par composant + masses calculées par SolidWorks).

**7. Comment arrivez-vous à 30–45 minutes d'autonomie ?**
En croisière, c'est l'aile qui porte : la puissance nécessaire est bien plus faible qu'en stationnaire. On prend l'énergie utilisable de la batterie (environ 80 % de sa capacité), on retire les phases de décollage, transition et atterrissage, et on divise par la puissance de croisière. Nous gardons une marge pour le vent et la chaleur. Seuls les essais en vol feront foi. **[à compléter : capacité de la batterie retenue]**

**8. Où est le centre de gravité ?**
En croisière, il doit se trouver vers 25 à 30 % de la corde de l'aile. En stationnaire, il doit être équilibré entre les deux moteurs avant et le moteur arrière. La batterie est placée de façon à pouvoir être avancée ou reculée pour régler le centrage, vérifié avant chaque premier vol.

**9. Quelles cartes électroniques concevez-vous ?**
La distribution de puissance, le câblage et l'intégration du contrôleur de vol STM32H743 : 5 V propre pour les radios, alimentation dédiée 5 V / 5 A pour le Raspberry Pi, assez de ports série et les sorties pour les servos de basculement. En secours, un contrôleur du commerce (Matek H743 ou Pixhawk).

**10. Quels matériaux, et quelles conditions de vol ?**
Composite et carbone pour la rigidité, avec les antennes placées hors des zones en carbone, qui bloquent les ondes. Le mât sur le dos éloigne le GPS des perturbations. Pas de vol sous la pluie pour le prototype ; les limites de vent seront fixées après les essais.

---

## 2. LOGO ADANTO Angelo — Logiciel embarqué et station sol

**1. Pourquoi ArduPilot plutôt qu'un code de vol écrit de zéro ?**
ArduPilot est éprouvé sur des milliers d'appareils et gère nativement le QuadPlane : stationnaire, transition et croisière. Réécrire un autopilote serait risqué et ne serait pas validable avant décembre. Nous concentrons nos efforts sur ce qui est propre à notre mission.

**2. Qu'avez-vous personnalisé dans ArduPilot ?**
La description matérielle de notre carte STM32H743, la configuration à rotors basculants (tricoptère avec deux moteurs avant inclinables), le mélange de l'empennage en V, la délimitation de zone et les règles de sécurité : retour si la liaison est perdue, atterrissage vertical si la batterie est critique, retour si la zone est franchie.

**3. Comment fonctionne la délimitation de zone ?**
On définit un cercle maximal (800 m dans notre configuration), une altitude maximale de 120 m et éventuellement un polygone autour de la zone autorisée. Si le drone sort de cette zone, ArduPilot déclenche automatiquement un retour au point de départ.

**4. Comment se passe la transition entre vol vertical et vol horizontal ?**
Les deux moteurs avant basculent progressivement vers l'avant : le drone accélère et l'aile commence à porter. Quand la vitesse air mesurée par le tube de Pitot est suffisante, les moteurs avant sont à l'horizontale et le moteur arrière s'arrête. À l'atterrissage, c'est l'inverse. Si la vitesse chute en croisière, ArduPilot peut ramener les moteurs vers le haut pour éviter le décrochage.

**5. Pourquoi Flutter pour la station sol ?**
Avec un seul code, on obtient une application mobile (tablette de terrain), desktop et web. C'est idéal pour une petite équipe. Les fonctions critiques de vol restent compatibles avec Mission Planner ou QGroundControl, qui servent de solution de secours.

**6. Que voit l'opérateur sur la station ?**
La carte avec la position du drone, l'altitude, la vitesse, la batterie et l'état des liaisons. La liste des alertes de l'IA avec leur image de preuve. La vidéo en direct, qui est enregistrée. Et les boutons de mission : départ, pause, retour.

**7. Et si la station sol plante ou si la tablette s'éteint ?**
Le drone ne dépend pas de la station pour voler : il poursuit sa mission ou applique la sécurité prévue en cas de perte de la station. Le télépilote garde aussi le canal d'urgence indépendant pour ordonner un retour ou une coupure.

**8. Comment testez-vous votre logiciel sans risquer le drone ?**
Avec SITL, le simulateur officiel d'ArduPilot : le vrai code de vol tourne sur PC avec un drone virtuel, et il existe un modèle de tricoptère à rotors basculants proche du nôtre. On y teste les missions, la transition, la délimitation de zone, les sécurités et la station sol avant tout vol réel. On passe ensuite aux tests sur table, puis aux essais en vol.

**9. Comment les alertes de l'IA arrivent-elles sur la station ?**
Le module IA produit un événement au format commun (schéma JSON) : classe, score, heure, zone et image. Le texte de l'alerte transite par la liaison de données ; l'image est réduite ou passe par le lien vidéo selon le débit disponible. **[à confirmer avec Makafui]** : le format MAVLink exact.

**10. Quelle est la latence entre la détection et l'affichage ?**
Elle se mesure en essai : temps d'inférence, plus le passage par le journal, plus la liaison radio. Nous ne donnons pas de chiffre avant de l'avoir mesuré. Notre objectif est une alerte en quelques secondes, donc pendant le vol.

---

## 3. KODJOVI Eli Cédric Ankou — Back-end, programme de vol, documentation

**1. Quel est le rôle du back-end ?**
Recevoir et archiver les données de chaque vol : télémétrie, alertes de l'IA avec leurs images et journaux de vol. Il les rend ensuite consultables par une API REST pour la station et pour l'analyse après le vol. Rien ne doit se perdre.

**2. ASP.NET Core ou Flask : lequel et pourquoi ?**
**[à confirmer]** : choisissez-en un seul avant le jury. Une piste de réponse : « Flask pour prototyper vite en Python, la même langue que le module IA ; ASP.NET Core si l'on vise la robustesse et la montée en charge. » L'important est de ne pas présenter les deux comme utilisés en même temps.

**3. Comment est organisée la base MySQL ?**
Des tables pour les vols (date, drone, pilote, durée), la télémétrie horodatée, les alertes (classe, score, statut, référence de l'image) et les utilisateurs. Les images sont stockées en fichiers ; la base ne garde que leur chemin et leur empreinte.

**4. Que veut dire « journal de vol signé » ?**
Chaque journal reçoit une empreinte numérique (hachage) et une signature avec une clé de l'équipe. Si quelqu'un modifie une seule ligne après le vol, la vérification échoue. C'est important pour prouver ce qui s'est passé en cas d'incident.

**5. Qui peut accéder aux données ?**
Uniquement les comptes autorisés, avec des rôles (opérateur, analyste, administrateur) et une connexion chiffrée en HTTPS. Les images de personnes sont des données sensibles : accès restreint et durée de conservation limitée.

**6. Qu'appelez-vous « programme de vol » ?**
La préparation et le déroulé d'une mission : le plan (points de passage, grille d'inspection de la piste, altitude, vitesse, zone autorisée), les check-lists avant et après le vol et la procédure d'urgence. Le plan est vérifié en simulation, puis envoyé au drone.

**7. Que se passe-t-il si la connexion au back-end est coupée pendant le vol ?**
Rien ne se perd. Le drone stocke ses alertes à bord et la station garde les siennes en local. Tout est synchronisé dès que la connexion revient, sans doublon : chaque événement a un identifiant unique.

**8. Comment répondez-vous aux exigences minimales du concours ?**
GPS avec retour automatique au point de départ, coupure d'urgence, liaison chiffrée et authentifiée, autonomie de 30 à 45 minutes visée, charge utile (caméra jour/nuit et IA) et dossier technique complet. Chaque exigence correspond à une fonction et à un test.

**9. Quelle documentation avez-vous produite ?**
Le dossier de conception (schémas, dimensionnement, analyse de sécurité), la CAO SolidWorks, les check-lists et procédures d'urgence, et le code du module IA avec son protocole de validation. Tout est versionné sur notre dépôt.

**10. Pourquoi les débris sur piste (FOD) sont-ils un vrai problème ?**
Un débris peut être aspiré par un réacteur, crever un pneu au décollage ou être projeté sur l'avion. Les inspections actuelles sont surtout visuelles, à bord d'un véhicule : elles sont longues, mobilisent la piste et dépendent de l'attention humaine.

---

## 4. de MEDEIROS Makafui Komlan Léopoldo — Réseaux, télémétrie, sécurité

**1. Quelles liaisons radio utilisez-vous ?**
Trois liaisons indépendantes : un lien vidéo HD (10 à 15 km), une radio longue portée chiffrée pour la télémétrie et les ordres, et un canal d'urgence ExpressLRS réservé au retour et à la coupure. Un lien qui tombe ne coupe pas les autres.

**2. Quelles fréquences, et sont-elles autorisées au Togo ?**
**[à confirmer]** : bandes envisagées en sous-GHz (433/868 MHz) pour la télémétrie et 2,4/5,8 GHz pour la vidéo, en séparant les bandes pour éviter les interférences. La demande est en cours auprès de l'ANAC et de l'ARCEP : nous n'émettrons qu'avec les autorisations.

**3. Quelle est la différence entre chiffrement et signature ?**
Le chiffrement empêche de **lire** les messages : c'est l'AES sur la radio. La signature MAVLink 2 empêche de **falsifier** un ordre : chaque message porte une signature calculée avec une clé secrète de 32 octets et un horodatage. Un ordre sans signature valide, ou rejoué plus tard, est rejeté.

**4. Comment gérez-vous les clés ?**
La clé est chargée par câble au sol avant le vol ; elle ne transite jamais par radio. L'objectif est une clé différente pour chaque vol : si une clé fuit, seul ce vol est concerné.

**5. Comment détectez-vous le brouillage ?**
En surveillant la qualité des liens : niveau du signal, bruit et taux de paquets perdus. Une chute brutale du rapport signal/bruit sur tous les canaux à la fois est typique d'un brouillage. Le drone bascule alors sur un autre lien ; si tout est perdu, il rentre seul.

**6. Comment résistez-vous au leurrage GPS ?**
Nous utilisons deux récepteurs GNSS multi-constellations. Le filtre de navigation d'ArduPilot (EKF3) compare en permanence le GPS à la centrale inertielle et au baromètre. Un saut de position incohérent, ou un désaccord entre les deux GPS, fait rejeter la source suspecte. Certains récepteurs signalent aussi eux-mêmes une suspicion de leurrage.

**7. Que fait le drone s'il perd la liaison ?**
Après 1,5 s, il est en alerte. Après 5 s, il rentre automatiquement au point de départ à 60 m d'altitude et atterrit à la verticale. Si la batterie est critique, il atterrit immédiatement à la verticale.

**8. Et si le GPS est brouillé, comment peut-il rentrer ?**
Sans GPS fiable, le drone ne peut pas naviguer précisément. Le filtre continue brièvement à l'estime grâce à la centrale inertielle et à la vitesse air, puis le drone passe en atterrissage sécurisé. Le télépilote garde le canal d'urgence pour reprendre la main à vue.

**9. Pourquoi la liaison satellite n'est-elle qu'« en test » ?**
Elle coûte cher (matériel et abonnement), elle est lente et son débit est faible. Nous l'étudions comme secours de télémétrie pour les longues distances, mais le système ne dépend pas d'elle. La 4G a été écartée, car sa couverture n'est pas garantie dans les zones visées.

**10. Comment allez-vous tester la sécurité des liaisons ?**
D'abord sur table : envoi d'ordres non signés ou rejoués (ils doivent être rejetés) et coupure volontaire de chaque lien (le comportement doit correspondre à celui attendu). Ensuite, des essais de portée sur le terrain. Les tests de brouillage se font seulement en environnement contrôlé et autorisé.

---

## 5. KAINWANG Roger — Intelligence artificielle et données

**1. Pourquoi YOLOv8s ?**
C'est un détecteur rapide, qui donne une sortie stable et localisée (rectangle, classe, score), et il est pris en charge par la chaîne de compilation Hailo. La version « s » est un compromis : plus précise que la « n » sur les petits objets, assez légère pour le temps réel. Un grand modèle génératif serait trop lent et moins fiable pour cette tâche.

**2. Qu'est-ce que le fine-tuning et pourquoi ne pas entraîner de zéro ?**
On part de poids déjà entraînés sur des millions d'images, qui savent reconnaître des formes, et on les adapte à nos classes et à notre caméra. Il faut beaucoup moins de données et de temps, et le résultat est meilleur avec un petit jeu de données.

**3. Sur quelles données entraînez-vous le modèle ?**
FOD-A, une base publique de débris de piste : 31 catégories et plus de 30 000 objets annotés. Nous la complétons avec des images prises par la caméra du drone, pour coller à son angle de vue, et avec des scènes vides pour réduire les fausses alertes. Entraînement, validation et test sont séparés par séquence vidéo, pour ne pas tricher.

**4. Quelle est la précision de votre IA ?**
Nous ne l'annonçons pas avant de l'avoir mesurée. Le protocole est prêt : rappel par classe (surtout pour les petits objets), fausses alertes par minute, latence et cadence, tout cela sur un jeu de test isolé. Un chiffre annoncé sans mesure n'aurait aucune valeur.

**5. Que fait l'IA avec un objet qu'elle n'a jamais vu ?**
Un détecteur ne reconnaît que ce qu'il a appris. Tout candidat crédible mais sans classe fiable est donc signalé « à vérifier », avec son image, et c'est l'opérateur qui décide. Nous testons aussi une comparaison avec une image de référence de la piste vide.

**6. Un débris de 5 cm est-il visible depuis le drone ?**
Tout dépend de l'altitude et de la caméra. À 30 m d'altitude, avec un capteur Full HD et un grand champ de vision, un pixel couvre environ 2 cm au sol : un débris de 5 cm ne fait que 2 à 3 pixels, ce qui est trop peu. Pour les petits débris, il faut donc voler plus bas, zoomer ou découper l'image en tuiles. C'est un réglage de mission que nous mesurerons.

**7. Pourquoi un Raspberry Pi 5 + Hailo-8, et pas un Jetson ?**
L'AI HAT+ fournit 26 TOPS pour une consommation faible et une masse d'environ 120 g pour l'ensemble, avec une intégration officielle sur le Pi 5. C'est moins cher et plus léger qu'un Jetson. La cadence réelle sera mesurée avec notre caméra et notre modèle compilé.

**8. L'IA peut-elle faire tomber le drone ?**
Non. Elle tourne sur un processeur séparé du contrôleur de vol. Elle lit la position du drone et envoie des alertes, mais elle ne commande jamais les moteurs. Si elle plante, le vol continue normalement.

**9. Avez-vous déjà des résultats ?**
Répondre sur ce qui est vrai : « La chaîne complète est en place : code de détection, de suivi et d'alerte, conversion pour le Hailo, journal hors connexion et protocole de test. Les chiffres que nous présenterons seront ceux mesurés avec le modèle final, sur les images de notre caméra. » Ne pas annoncer de score ni de vitesse.

**10. Et sans réseau ? La nuit ? La vie privée ?**
Sans réseau, tout se fait à bord et les alertes sont gardées puis renvoyées. La nuit, il faut la caméra thermique et adapter le modèle à ces images : c'est une étape suivante. Pour la vie privée, on détecte « une personne », jamais son identité, et seules les images d'alerte sont conservées.

---

## Questions pour toute l'équipe (qui répond : Israel, sauf indication)

**1. Combien coûte le drone ?**
Le budget de la fiche projet est de 730 000 à 1 400 000 FCFA, plus 120 000 à 160 000 FCFA pour le module IA. **[à confirmer]** : un renforcement des liaisons est en arbitrage. Donnez le chiffre validé par l'équipe.

**2. Où en est le drone ?**
« La conception CAO est terminée. Nous sommes en phase de prototypage et d'intégration, et les essais au sol puis en vol sont prévus en novembre. » Ne pas annoncer un vol ou une mesure qui n'a pas eu lieu.

**3. Quel est votre plus grand risque technique ?** (Israel / Makafui)
La transition en vol, avec le basculement des moteurs, et les délais de livraison des composants. Nos réponses : simulation SITL, essais progressifs (d'abord en stationnaire, puis transitions à hauteur de sécurité), contrôleur du commerce en secours et commandes passées en priorité.

**4. Qu'est-ce qui vous distingue des autres équipes ?**
Une IA réellement embarquée, sans cloud. Un contrôleur de vol séparé de l'IA pour la sécurité. Une liaison sécurisée dès la conception. Et une documentation complète et reproductible.

**5. Après le concours ?**
Des essais avec un aéroport partenaire, si on obtient l'autorisation. Puis l'adaptation à d'autres missions grâce à la charge utile modulaire : cartographie, infrastructures, agriculture.
