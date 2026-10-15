# Pitch Sentinelle Aérienne : script oral (24 diapos)

Support : `sentinelle_aerienne_presentation_complete.pptx`. Le même texte se trouve dans les notes de l'orateur de chaque diapo.

Durée indicative : environ 22 minutes.

| Diapo | Titre | Qui parle | Durée |
|---|---|---|---|
| 1 | Sentinelle Aérienne | Israel AWADE | 60 s |
| 2 | Le besoin : la sécurité des pistes | Cédric KODJOVI | 60 s |
| 3 | Notre réponse : un VTOL à rotors basculants | Israel AWADE | 45 s |
| 4 | Les parties du drone | Israel AWADE | 70 s |
| 5 | Les moteurs avant basculants | Israel AWADE | 60 s |
| 6 | Le moteur arrière et l'empennage en V | Israel AWADE | 50 s |
| 7 | Caractéristiques principales | Israel AWADE | 40 s |
| 8 | Le vol : du décollage vertical à la croisière | Angelo LOGO ADANTO | 60 s |
| 9 | Les capteurs de navigation | Angelo LOGO ADANTO | 50 s |
| 10 | Architecture électronique : la sécurité d'abord | Makafui de MEDEIROS | 65 s |
| 11 | Énergie, pilotage et mission | Israel AWADE | 55 s |
| 12 | Les principaux composants | Israel AWADE | 60 s |
| 13 | Le module d'intelligence artificielle | Roger KAINWANG | 70 s |
| 14 | Données et fiabilité de l'IA | Roger KAINWANG | 60 s |
| 15 | Station sol et back-end | Angelo LOGO ADANTO | 50 s |
| 16 | Trois liaisons indépendantes | Makafui de MEDEIROS | 55 s |
| 17 | Les avantages | Israel AWADE | 50 s |
| 18 | Les risques et nos réponses | Israel AWADE puis Makafui de MEDEIROS | 90 s |
| 19 | La réglementation | Cédric KODJOVI | 70 s |
| 20 | La sécurité | Makafui de MEDEIROS | 65 s |
| 21 | Domaines d'application | Cédric KODJOVI | 55 s |
| 22 | Calendrier | Cédric KODJOVI | 35 s |
| 23 | Budget prévisionnel | Israel AWADE | 35 s |
| 24 | En résumé | Israel AWADE | 35 s |

## 1. Sentinelle Aérienne (Israel AWADE)

Bonjour Mesdames et Messieurs les membres du jury. Je m'appelle AWADE Constantin Israel, je suis le chef de l'équipe SkyVision Togo et je m'occupe de la mécanique, de l'électronique et de la conception 3D.

Notre projet s'appelle Sentinelle Aérienne : un drone qui décolle à la verticale, vole ensuite comme un avion, et analyse lui-même les images de sa caméra pour repérer ce qui ne va pas, en particulier sur une piste d'aéroport.

Nous sommes cinq : Angelo au logiciel embarqué et à la station sol, Cédric au back-end, au programme de vol et à la documentation, Makafui aux réseaux, à la télémétrie et à la sécurité, et Roger à l'intelligence artificielle. Cédric commence par le besoin.

## 2. Le besoin : la sécurité des pistes (Cédric KODJOVI)

Merci Israel. Bonjour, je m'appelle KODJOVI Eli Cédric Ankou, je m'occupe du back-end, du programme de vol et de la documentation.

Sur une piste, un petit objet peut avoir de grosses conséquences : un boulon ou un morceau de pneu peut être aspiré par un réacteur ou faire éclater un pneu au décollage. On parle de FOD, pour Foreign Object Debris. Il faut aussi surveiller les abords, les clôtures, et repérer les personnes ou les véhicules qui n'ont rien à faire là.

Aujourd'hui, ce contrôle se fait surtout à la main, en véhicule. Ça prend du temps, la piste est bloquée, et le résultat dépend de l'attention des agents, surtout la nuit.

Notre objectif : inspecter depuis les airs, plus vite, et signaler tout de suite ce qui est anormal. Israel va vous présenter le drone.

## 3. Notre réponse : un VTOL à rotors basculants (Israel AWADE)

Merci Cédric. Notre réponse, c'est un VTOL à rotors basculants. Il décolle à la verticale comme un multirotor, depuis n'importe quel terrain dégagé. Ensuite, ses deux moteurs avant basculent vers l'avant et il vole comme un avion : c'est l'aile qui le porte, ce qui consomme beaucoup moins d'énergie.

À cette plateforme, nous ajoutons deux choses : une intelligence artificielle qui analyse les images à bord, et une liaison radio sécurisée.

## 4. Les parties du drone (Israel AWADE)

Voici les parties du drone, vues de dessus.

À l'avant, le nez porte le tube de Pitot, qui mesure la vitesse de l'air : c'est indispensable pour savoir quand l'aile porte assez. De chaque côté, un moteur monté en nacelle sur l'aile, avec un servomoteur qui le fait pivoter.

Au centre, le fuselage contient la batterie, l'électronique et le module d'intelligence artificielle. Sur le dos, le mât porte le GPS, loin des perturbations électriques.

À l'arrière, le moteur arrière ne sert qu'au vol vertical, et l'empennage en V gère à la fois la profondeur et la direction. Je vais détailler les deux parties les plus importantes.

## 5. Les moteurs avant basculants (Israel AWADE)

Les deux moteurs avant sont la pièce maîtresse du drone. Chacun est monté dans une nacelle, avec un servomoteur qui le fait pivoter. Au décollage, il pousse vers le haut ; en croisière, il tire vers l'avant.

L'avantage, c'est que les mêmes moteurs servent au décollage et à la croisière : on ne transporte pas de moteurs inutiles en vol, donc on gagne de la masse et de l'autonomie.

Comme le basculement est critique, nous choisissons des servos à engrenages métal, avec une bonne marge, et leur débattement est vérifié avant chaque vol.

## 6. Le moteur arrière et l'empennage en V (Israel AWADE)

À l'arrière, le moteur est logé sous la queue. Avec les deux moteurs avant, il forme un triangle qui tient le drone en équilibre en vol vertical. En croisière, il s'arrête.

L'empennage en V remplace la dérive et la profondeur classiques. Avec deux surfaces au lieu de trois, on a moins de masse, moins de traînée et moins de servos. Chaque gouverne agit à la fois en profondeur et en direction, et c'est le contrôleur de vol qui fait le mélange.

## 7. Caractéristiques principales (Israel AWADE)

En résumé pour la partie drone : trois moteurs, dont deux basculants, un empennage en V, et une autonomie visée de 30 à 45 minutes. Le contrôleur de vol est une carte STM32H743 sous ArduPilot, le module IA un Raspberry Pi 5 avec une puce Hailo-8, et la charge utile une caméra stabilisée jour et nuit. Angelo va vous expliquer comment le drone vole.

## 8. Le vol : du décollage vertical à la croisière (Angelo LOGO ADANTO)

Merci Israel. Bonjour, je m'appelle LOGO ADANTO Angelo, je m'occupe du logiciel embarqué et de la station sol.

Le vol se fait en quatre phases. Au décollage, les moteurs avant sont tournés vers le haut et, avec le moteur arrière, ils soulèvent le drone. Pendant la transition, les moteurs avant basculent petit à petit vers l'avant : le drone accélère et l'aile commence à porter. En croisière, le moteur arrière s'arrête : les moteurs avant tirent le drone et l'aile le porte. À l'atterrissage, on fait l'inverse.

C'est ArduPilot qui gère tout ça automatiquement, à partir de la vitesse air mesurée par le tube de Pitot.

## 9. Les capteurs de navigation (Angelo LOGO ADANTO)

Pour savoir où il est et comment il vole, le drone utilise plusieurs capteurs. Deux récepteurs GPS sur le mât donnent la position. Le tube de Pitot, dans le nez, mesure la vitesse de l'air. La centrale inertielle mesure les accélérations et les rotations, le baromètre l'altitude, et le compas la direction.

Le contrôleur de vol combine toutes ces mesures. Si une source donne une valeur qui ne colle pas avec les autres, par exemple un GPS brouillé, elle est écartée. Makafui va vous présenter l'architecture électronique.

## 10. Architecture électronique : la sécurité d'abord (Makafui de MEDEIROS)

Merci Angelo. Bonjour, je m'appelle de MEDEIROS Makafui Komlan Léopoldo, je m'occupe des réseaux, de la télémétrie et de la sécurité.

Pour nous, le vol passe avant tout. Nous avons donc mis deux calculateurs dans le drone. Le contrôleur de vol, sur une carte STM32H743, stabilise le drone, commande les moteurs et le basculement, et gère les sécurités. Le module d'intelligence artificielle, sur un Raspberry Pi 5, analyse les images.

Ils communiquent en MAVLink : l'IA reçoit la position et renvoie ses alertes, mais elle ne peut pas commander les moteurs. Si elle plante, le drone continue de voler et peut toujours rentrer seul. Nous gardons aussi un contrôleur du commerce en secours.

## 11. Énergie, pilotage et mission (Israel AWADE)

[Israel] Voici comment l'électronique est organisée, en trois chaînes.

L'énergie : la batterie lithium-polymère alimente un module de puissance qui mesure la tension et le courant, puis trois variateurs qui règlent la vitesse des trois moteurs.

Le pilotage : les capteurs envoient leurs mesures au contrôleur de vol, qui commande les servos de basculement et les gouvernes de l'empennage, et communique par les liaisons radio.

La mission : la caméra envoie ses images au Raspberry Pi, qui produit les alertes envoyées à la station sol.

Nous prévoyons des alimentations séparées : une pour les radios, et une dédiée au Raspberry Pi, pour qu'aucune ne perturbe l'autre.

## 12. Les principaux composants (Israel AWADE)

Voici à quoi ressemblent les principaux composants. Pour l'énergie : la batterie lithium-polymère, le module de puissance, les variateurs et les moteurs sans balais. Pour le pilotage : le contrôleur de vol à STM32H743, le module GNSS avec son compas, le tube de Pitot, la radio longue portée et la radiocommande. Et pour la mission : le Raspberry Pi 5, sa carte d'accélération Hailo-8, et la caméra.

Ce sont des composants standards, faciles à trouver et à remplacer. Roger va vous présenter le module d'intelligence artificielle.

## 13. Le module d'intelligence artificielle (Roger KAINWANG)

Merci Israel. Bonjour, je m'appelle KAINWANG Roger, je m'occupe de l'intelligence artificielle et des données.

Le module IA, c'est un Raspberry Pi 5 avec une carte AI HAT+ qui porte une puce Hailo-8 de 26 TOPS. Tout le calcul se fait à bord : aucune image ne part sur internet.

La caméra filme. Le détecteur YOLOv8s repère les personnes, les véhicules et les débris au sol. On ne garde que ce qui est dans la zone utile, la piste et ses abords. Un suivi relie les détections d'une image à l'autre pour qu'un objet ne déclenche qu'une seule alerte. Puis l'alerte part vers la station sol avec une photo de preuve.

## 14. Données et fiabilité de l'IA (Roger KAINWANG)

Pour le modèle, nous ne partons pas de zéro : nous prenons un YOLOv8s déjà entraîné et nous l'adaptons à notre mission, avec FOD-A, une base publique de plus de 30 000 débris de piste annotés, et des images prises avec notre caméra, vues d'en haut. Nous ajoutons des scènes vides avec des ombres et des marquages pour éviter les fausses alertes.

Si l'IA voit un objet qu'elle ne sait pas classer, elle le signale « à vérifier », avec l'image. Si la liaison est coupée, elle garde ses alertes. Et c'est toujours l'humain qui décide : l'IA ne commande jamais le drone. Angelo va vous montrer la station sol.

## 15. Station sol et back-end (Angelo LOGO ADANTO)

Merci Roger. Au sol, nous développons la station en Flutter, avec une version mobile et une version web. L'opérateur prépare sa mission, définit la zone autorisée, suit la télémétrie en direct, et reçoit les alertes de l'IA avec leur image. La vidéo est enregistrée.

Toutes ces données sont archivées par le back-end de Cédric : une API REST et une base MySQL, avec l'historique des vols et des alertes, et des journaux de vol signés. Makafui va vous présenter les liaisons.

## 16. Trois liaisons indépendantes (Makafui de MEDEIROS)

Merci Angelo. Notre principe : ne jamais dépendre d'un seul lien. Nous avons trois liaisons séparées. Un lien vidéo HD pour voir ce que voit le drone. Une radio longue portée chiffrée pour la télémétrie, les ordres et les alertes de l'IA. Et un canal d'urgence indépendant, qui sert uniquement à faire revenir le drone ou à couper les moteurs.

La 4G est écartée car la couverture n'est pas garantie, et le satellite est à l'essai comme secours. Les antennes sont placées hors des zones en carbone, qui bloquent les ondes.

## 17. Les avantages (Israel AWADE)

[Israel] Pour résumer ce que notre drone apporte : il n'a pas besoin de piste, il vole longtemps grâce à son aile, et ses moteurs basculants servent aux deux phases de vol. L'IA à bord donne l'alerte pendant le vol, sans internet. La liaison est sécurisée. Les agents n'ont plus à parcourir la piste eux-mêmes. Et la même plateforme peut servir à d'autres missions.

## 18. Les risques et nos réponses (Israel AWADE puis Makafui de MEDEIROS)

Nous avons aussi listé les risques, avec une réponse pour chacun.

Si la liaison radio est perdue, le drone rentre seul et atterrit à la verticale. Si la batterie devient faible, il rentre ; si elle est critique, il atterrit immédiatement. Le moment le plus délicat est le vol vertical : on le garde court, à faible hauteur. Les servos de basculement sont contrôlés à chaque check-list.

[Makafui] Contre le brouillage et le leurrage GPS, nous comparons deux GPS avec les autres capteurs. Contre le piratage, la liaison est chiffrée et les ordres sont signés. Le géorepérage empêche de sortir de la zone. Et si l'IA hésite, elle signale « à vérifier » : c'est l'humain qui décide.

## 19. La réglementation (Cédric KODJOVI)

[Cédric] Côté réglementation, deux familles de règles.

Pour le vol : nous ne volons qu'avec l'autorisation de l'ANAC, en vue directe du télépilote sauf autorisation particulière, dans une zone et à une hauteur limitées que le géorepérage fait respecter. Pas de vol au-dessus de la foule ni près d'un aérodrome sans accord. Le télépilote est formé et suit des check-lists.

Pour les ondes et les données : nos fréquences doivent être autorisées par l'ARCEP. Comme le drone peut filmer des personnes, nous respectons la loi togolaise sur la protection des données : pas de reconnaissance faciale, on ne garde que les images d'alerte, et l'accès est réservé aux personnes autorisées.

## 20. La sécurité (Makafui de MEDEIROS)

[Makafui] La sécurité se joue à deux niveaux.

La sécurité du vol : le contrôleur est séparé de l'IA ; en cas de perte de radio, de batterie faible ou de GPS dégradé, le drone applique automatiquement une procédure de secours ; le géorepérage limite la zone et la hauteur ; une coupure d'urgence reste toujours possible ; et avant le décollage, le drone vérifie lui-même que tout est prêt.

La cybersécurité : la liaison est chiffrée, chaque message est signé avec une clé chargée au sol, donc un faux ordre est rejeté. Nous détectons le brouillage, nous comparons les sources de position contre le leurrage GPS, et les journaux de vol sont signés.

## 21. Domaines d'application (Cédric KODJOVI)

[Cédric] Notre premier usage, c'est l'aéroport. Mais la même plateforme peut servir en agriculture et pour l'environnement, par exemple pour repérer des départs de feux de brousse, pour inspecter des lignes électriques, des ponts ou le port de Lomé, pour livrer de petits colis médicaux dans des zones enclavées avec une version adaptée, ou pour la cartographie. À chaque fois, on change seulement la charge utile et le modèle d'IA.

## 22. Calendrier (Cédric KODJOVI)

Côté calendrier, la candidature a été validée en août, la conception faite en septembre et le dossier déposé. Nous sommes en phase de prototypage et d'intégration. En novembre viendront les essais au sol, en vol et de sécurité, pour être prêts pour la finale en décembre. Je rends la parole à Israel.

## 23. Budget prévisionnel (Israel AWADE)

Merci Cédric. Notre budget est estimé entre 730 000 et 1 400 000 francs CFA pour le drone, avec en plus 120 000 à 160 000 francs pour le module d'intelligence artificielle. Nous avons choisi des composants courants, faciles à trouver et à remplacer.

## 24. En résumé (Israel AWADE)

Pour résumer, la Sentinelle Aérienne décolle partout, vole longtemps grâce à son aile, analyse ses images à bord et communique de façon sécurisée. Ses risques sont identifiés et traités, et elle respecte le cadre réglementaire.

Merci à l'ANAC et aux organisateurs du CECFD. Merci pour votre attention, nous sommes prêts à répondre à vos questions.
