# Préparation au jury : 10 questions par personne

Pitch « Sentinelle Aérienne » · SkyVision Togo · CECFD 2026 — ANAC

**Comment l'utiliser**

- Chacun lit ses 10 questions, puis s'entraîne à répondre **à voix haute en 30 secondes maximum**, sans lire.
- Les réponses s'appuient sur nos documents : la fiche projet, la fiche technique IA, `drone/fiche_technique_complete.md`, les paramètres ArduPilot et le code `ia/`.
- La mention **[à confirmer]** signale un choix que l'équipe doit encore figer. Si c'est le cas le jour J, on le dit franchement : « c'est en cours de validation, voici notre piste ».
- Règle d'or : **ne jamais inventer un chiffre**. « Nous le mesurerons sur banc » vaut mieux qu'un chiffre faux.

---

## 1. AWADE Constantin Israel — Mécanique, électronique, conception 3D

**1. Pourquoi un VTOL hybride plutôt qu'un multirotor ou un avion ?**
Le multirotor décolle partout, mais il porte tout son poids avec ses moteurs : environ 1 000 W en stationnaire pour le SA-1. L'avion vole sur son aile, environ 280 W en croisière, mais il lui faut une piste. L'hybride décolle sans piste, puis vole 3 à 4 fois plus économiquement. C'est indispensable pour viser 30 à 45 minutes.

**2. Quelles sont les dimensions et la masse du drone ?**
Envergure de 2,0 m, surface alaire de 0,56 m² et environ 6,4 kg au décollage. Cette masse comprend une marge d'intégration de 200 g. La batterie pèse à elle seule 2,05 kg, soit environ un tiers de la masse.

**3. Comment avez-vous dimensionné les moteurs verticaux ?**
On part de la masse maximale et on exige une réserve de poussée pour contrôler le drone par vent et en cas de rafale, soit environ 2,9 kgf par moteur. Avec des hélices de 15 pouces, on choisit un moteur et un ESC de 40 A qui fournissent cette poussée en 6S. Le calcul se trouve dans `drone/calculs/dimensionnement.py`.

**4. Comment calculez-vous l'autonomie ?**
La batterie est une LiPo 6S de 16 000 mAh, soit 355 Wh, dont environ 80 % sont utilisables. On soustrait l'énergie du décollage, de la transition et de l'atterrissage, puis on divise le reste par la puissance de croisière (≈ 280 W). On obtient environ 50 minutes en théorie. Nous annonçons 30 à 45 minutes pour couvrir le vent, la chaleur et le vieillissement de la batterie. Seul l'essai en vol fera foi.

**5. Pourquoi deux moteurs de croisière sur les poutres ?**
Pour la redondance : si un moteur s'arrête, le drone peut encore rejoindre sa zone de retour. La poussée est aussi mieux répartie, et le fuselage arrière reste libre. **[à confirmer]** : notre maquette d'étude avait un seul moteur propulsif. La configuration finale est celle de la CAO SolidWorks, et nous devons présenter la même partout.

**6. Où est le centre de gravité et comment le contrôlez-vous ?**
Il doit se situer à environ 25-30 % de la corde de l'aile, et aussi au centre des 4 moteurs verticaux. La batterie est montée sur un rail réglable : on l'avance ou on la recule. On vérifie le centrage en suspendant le drone avant chaque premier vol.

**7. Pourquoi le carbone, et quel est son inconvénient ?**
Le carbone est très rigide et léger, ce qui est idéal pour les poutres et le longeron. Son défaut : il est conducteur et bloque les ondes radio. Nous plaçons donc les antennes dans des zones en fibre de verre, ou bien à l'extérieur.

**8. Que se passe-t-il si un moteur vertical tombe en panne ?**
En croisière, aucun impact, puisque l'aile porte le drone. En stationnaire, un quadri perd une partie de son contrôle. On limite donc le temps passé en stationnaire au strict décollage et atterrissage, et on le fait à faible hauteur, au-dessus d'une zone dégagée. La check-list d'urgence décrit la conduite à tenir.

**9. Quelles cartes électroniques concevez-vous vous-mêmes ?**
La carte de distribution de puissance, le câblage et l'intégration du contrôleur de vol STM32H743. Celle-ci comprend un 5 V propre pour les radios, un BEC dédié de 5 V / 5 A pour le Raspberry Pi et assez de ports série. En secours, nous gardons un contrôleur du commerce (Pixhawk / Matek H743).

**10. Quelles conditions météo le drone supporte-t-il ?**
Visé : un vent jusqu'à environ 8 m/s et des températures jusqu'à 40 °C. Pas de vol sous la pluie pour le prototype, car l'électronique n'est pas étanche. Ces limites seront validées en essai, pas seulement sur le papier.

---

## 2. LOGO ADANTO Angelo — Logiciel embarqué et station sol

**1. Pourquoi ArduPilot plutôt qu'un code de vol écrit de zéro ?**
ArduPilot est éprouvé sur des milliers d'appareils et gère nativement le QuadPlane : stationnaire, transition et croisière. Réécrire un autopilote serait risqué et ne serait pas validable avant décembre. Nous concentrons nos efforts sur ce qui est propre à notre mission.

**2. Qu'avez-vous personnalisé dans ArduPilot ?**
La configuration de la carte STM32H743 (son fichier de description matérielle), les paramètres du SA-1, la délimitation de zone et les règles de sécurité. Ces dernières : retour si la liaison est perdue, atterrissage vertical si la batterie est critique, retour si la zone est franchie. Tout est versionné dans `sentinelle_sa1.param`.

**3. Comment fonctionne la délimitation de zone ?**
On définit un cercle maximal (800 m dans notre configuration), une altitude maximale de 120 m et éventuellement un polygone autour de la zone autorisée. Si le drone sort de cette zone, ArduPilot déclenche automatiquement un retour au point de départ.

**4. Comment se passe la transition entre vol vertical et vol horizontal ?**
Le moteur de croisière accélère pendant que les moteurs verticaux maintiennent l'altitude. Au-dessus de 15 m/s de vitesse air, la transition se termine et les moteurs verticaux s'arrêtent. En croisière, si la vitesse redescend sous 13 m/s, les moteurs verticaux reviennent aider automatiquement : c'est l'assistance anti-décrochage.

**5. Pourquoi Flutter pour la station sol ?**
Avec un seul code, on obtient une application mobile (tablette de terrain), desktop et web. C'est idéal pour une petite équipe. Les fonctions critiques de vol restent compatibles avec Mission Planner ou QGroundControl, qui servent de solution de secours.

**6. Que voit l'opérateur sur la station ?**
La carte avec la position du drone, l'altitude, la vitesse, la batterie et l'état des liaisons. La liste des alertes de l'IA avec leur image de preuve. La vidéo en direct, qui est enregistrée. Et les boutons de mission : départ, pause, retour.

**7. Et si la station sol plante ou si la tablette s'éteint ?**
Le drone ne dépend pas de la station pour voler : il poursuit sa mission ou applique la sécurité prévue en cas de perte de la station. Le télépilote garde aussi le canal d'urgence indépendant pour ordonner un retour ou une coupure.

**8. Comment testez-vous votre logiciel sans risquer le drone ?**
Avec SITL, le simulateur officiel d'ArduPilot : le vrai code de vol tourne sur PC avec un drone virtuel. On y teste les missions, la délimitation de zone, les sécurités et la station sol avant tout vol réel. On passe ensuite aux tests sur table, puis aux essais en vol.

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
Une fiche technique complète qui explique chaque composant, un guide de conception et d'assemblage, les calculs de dimensionnement, les paramètres ArduPilot, les check-lists, des vidéos explicatives et le code de l'IA avec son protocole de validation. Tout est versionné sur notre dépôt.

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
FOD-A, une base publique de débris de piste : 31 catégories et plus de 30 000 objets annotés. Nous la complétons avec nos propres images filmées avec la caméra du drone, et avec des scènes vides pour réduire les fausses alertes. Entraînement, validation et test sont séparés par séquence vidéo, pour ne pas tricher.

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

**9. Que se passe-t-il sans réseau ?**
L'inférence se fait entièrement à bord, sans cloud. Les alertes sont enregistrées dans un journal local (SQLite) et envoyées automatiquement quand la liaison revient. Nos tests le vérifient en coupant volontairement la liaison.

**10. Et la nuit ? Et la vie privée ?**
La nuit, il faut la caméra thermique, et le modèle doit être adapté avec des images thermiques : c'est une étape suivante, que nous n'annonçons pas comme acquise. Pour la vie privée, nous détectons « une personne », jamais son identité : pas de reconnaissance faciale. Seules les images d'alerte sont conservées, avec un accès restreint.

---

## Questions pour toute l'équipe (qui répond : Israel, sauf indication)

**1. Combien coûte le drone ?**
Le budget de la fiche projet est de 730 000 à 1 400 000 FCFA, plus 120 000 à 160 000 FCFA pour le module IA. **[à confirmer]** : un renforcement des liaisons est en arbitrage. Donnez le chiffre validé par l'équipe.

**2. Qu'est-ce qui est déjà fabriqué ou testé ?**
Répondez avec l'état réel au jour du pitch (pièces imprimées ou découpées, cartes reçues, tests sur banc). Il vaut mieux dire honnêtement « en cours » qu'annoncer un vol qui n'a pas eu lieu.

**3. Quel est votre plus grand risque technique ?** (Israel / Makafui)
La transition en vol et les délais de livraison des composants radio. Nos réponses : simulation SITL et essais progressifs, contrôleur du commerce en secours, commandes passées en priorité.

**4. Qu'est-ce qui vous distingue des autres équipes ?**
Une IA réellement embarquée, sans cloud. Un contrôleur de vol séparé de l'IA pour la sécurité. Une liaison sécurisée dès la conception. Et une documentation complète et reproductible.

**5. Après le concours ?**
Des essais avec un aéroport partenaire, si on obtient l'autorisation. Puis l'adaptation à d'autres missions grâce à la charge utile modulaire : cartographie, infrastructures, agriculture.
