# Pitch Sentinelle Aérienne : script oral (17 diapos)

Support : `sentinelle_aerienne_pitch_complet.pptx`. Le même texte se trouve dans les notes de l'orateur de chaque diapo.

Durée indicative : environ 13 minutes.

| Diapo | Titre | Qui parle | Durée |
|---|---|---|---|
| 1 | Sentinelle Aérienne | Israel AWADE | 40 s |
| 2 | L'équipe et l'ordre de passage | Israel AWADE | 35 s |
| 3 | Le besoin | Israel AWADE | 45 s |
| 4 | Notre réponse : un VTOL à rotors basculants | Israel AWADE | 45 s |
| 5 | Caractéristiques principales | Israel AWADE | 45 s |
| 6 | Structure et conception | Israel AWADE | 50 s |
| 7 | Le vol : du décollage vertical à la croisière | Angelo LOGO ADANTO | 60 s |
| 8 | La station sol | Angelo LOGO ADANTO | 45 s |
| 9 | Trois liaisons indépendantes | Makafui de MEDEIROS | 55 s |
| 10 | Sécurité des communications | Makafui de MEDEIROS | 55 s |
| 11 | Le module d'intelligence artificielle | Roger KAINWANG | 70 s |
| 12 | Données et fiabilité | Roger KAINWANG | 60 s |
| 13 | Supervision et documentation | Cédric KODJOVI | 50 s |
| 14 | Conformité aux exigences du concours | Cédric KODJOVI | 40 s |
| 15 | Calendrier | Cédric KODJOVI | 35 s |
| 16 | Budget prévisionnel | Israel AWADE | 35 s |
| 17 | En résumé | Israel AWADE | 35 s |

## 1. Sentinelle Aérienne (Israel AWADE)

Bonjour Mesdames et Messieurs les membres du jury. Je m'appelle AWADE Constantin Israel, je suis le chef de l'équipe SkyVision Togo, et je m'occupe de la mécanique, de l'électronique et de la conception 3D.

Nous vous présentons la Sentinelle Aérienne : un drone qui décolle à la verticale, vole ensuite comme un avion, et analyse lui-même ses images pour repérer ce qui est anormal, en particulier sur les pistes d'aéroport.

## 2. L'équipe et l'ordre de passage (Israel AWADE)

Nous sommes cinq, et chacun est responsable d'une partie du système.

Je vais vous présenter le besoin et le drone. Angelo parlera du vol et de la station sol, Makafui des liaisons radio et de la sécurité, Roger de l'intelligence artificielle, et Cédric de la supervision, de la conformité et du calendrier. Je reviendrai à la fin pour le budget et la conclusion.

## 3. Le besoin (Israel AWADE)

Partons du besoin. Sur une piste, un débris comme un boulon ou un morceau de pneu peut être aspiré par un réacteur. Il faut aussi surveiller les abords et repérer les intrusions.

Aujourd'hui, l'inspection se fait surtout en véhicule : c'est lent, la piste est bloquée, et c'est difficile la nuit. Les drones existants ont chacun leur défaut : le multirotor décolle partout mais vole peu de temps, l'avion vole longtemps mais il lui faut une piste.

Et souvent, les images ne sont regardées qu'après le vol.

## 4. Notre réponse : un VTOL à rotors basculants (Israel AWADE)

Notre réponse, c'est un VTOL à rotors basculants. Il décolle à la verticale comme un multirotor, depuis n'importe quel terrain dégagé. Ensuite, ses deux moteurs avant basculent vers l'avant et il vole comme un avion : c'est l'aile qui le porte, ce qui consomme beaucoup moins d'énergie.

À cette plateforme, nous ajoutons deux choses qui répondent directement au thème surveillance et sécurité : une intelligence artificielle qui analyse les images à bord, et une liaison radio sécurisée.

## 5. Caractéristiques principales (Israel AWADE)

Voici les grandes lignes du drone. C'est une configuration à trois moteurs : deux moteurs avant qui basculent, et un moteur arrière qui ne sert qu'au vol vertical. L'empennage est en V.

Nous visons 30 à 45 minutes d'autonomie. Le contrôleur de vol est une carte STM32H743 sous ArduPilot, et le module IA un Raspberry Pi 5 avec un accélérateur Hailo-8. La charge utile, c'est une caméra stabilisée jour et nuit, et le drone communique par trois liaisons séparées.

## 6. Structure et conception (Israel AWADE)

Côté structure, tout a été modélisé sous SolidWorks.

Le fuselage reçoit la batterie, l'électronique et le module IA. Les deux moteurs avant sont montés dans des nacelles sur l'aile, avec un servomoteur qui les fait pivoter. Le moteur arrière est logé dans le fuselage, sous la queue.

L'empennage en V remplace la dérive et la profondeur classiques : deux surfaces au lieu de trois, donc moins de servos et moins de masse. Le GPS est sur un mât au-dessus du fuselage, pour l'éloigner des perturbations, et un tube de Pitot dans le nez mesure la vitesse air. Enfin, on a fait attention à placer les antennes hors des zones en carbone, qui bloquent les ondes.

Angelo va maintenant vous expliquer comment le drone vole.

## 7. Le vol : du décollage vertical à la croisière (Angelo LOGO ADANTO)

Bonjour, je m'appelle LOGO ADANTO Angelo, je m'occupe du logiciel embarqué et de la station sol.

Le vol se fait en quatre phases. Au décollage, les deux moteurs avant sont tournés vers le haut et, avec le moteur arrière, ils soulèvent le drone. Pendant la transition, les moteurs avant basculent petit à petit vers l'avant : le drone accélère et l'aile commence à porter. Une fois la vitesse suffisante, le moteur arrière s'arrête et on est en croisière : les deux moteurs avant tirent le drone, et l'aile le porte. À l'atterrissage, on fait l'inverse.

C'est ArduPilot qui gère tout ça automatiquement, à partir de la vitesse air mesurée par le tube de Pitot.

## 8. La station sol (Angelo LOGO ADANTO)

Au sol, nous développons la station en Flutter, ce qui donne une version mobile et une version web avec le même code.

Avant le vol, l'opérateur prépare sa mission sur la carte et définit la zone autorisée : si le drone en sort, il fait demi-tour automatiquement. Pendant le vol, il suit la télémétrie en direct et la vidéo est enregistrée.

Surtout, il reçoit les alertes de l'IA avec leur image. Il n'a pas besoin de fixer la vidéo en permanence : c'est le drone qui lui signale ce qu'il faut regarder. Je laisse la parole à Makafui pour les liaisons.

## 9. Trois liaisons indépendantes (Makafui de MEDEIROS)

Bonjour, je m'appelle de MEDEIROS Makafui Komlan Léopoldo, je m'occupe des réseaux, de la télémétrie et de la sécurité.

Notre principe : ne jamais dépendre d'un seul lien. Nous avons trois liaisons séparées. Un lien vidéo HD pour voir ce que voit le drone. Une radio longue portée chiffrée, qui transporte la télémétrie, les ordres et les alertes de l'IA. Et un canal d'urgence indépendant, qui sert uniquement à faire revenir le drone ou à couper les moteurs.

Nous avons écarté la 4G, parce que la couverture n'est pas garantie dans les zones visées. Le satellite, lui, est à l'essai comme liaison de secours.

## 10. Sécurité des communications (Makafui de MEDEIROS)

Pour la sécurité, nous avons pensé à chaque menace. Les données sont chiffrées, donc on ne peut pas les lire. Chaque message MAVLink est signé : si quelqu'un essaie d'envoyer un ordre sans la bonne clé, le drone l'ignore.

Contre le brouillage, on surveille la qualité des liens et on bascule sur un autre. Contre le leurrage GPS, on utilise deux récepteurs et on compare leur position avec les autres capteurs du drone : si une source ne colle pas, elle est écartée.

Et si tout est perdu, le drone rentre seul et atterrit à la verticale. En dernier recours, on peut couper les moteurs. Roger va vous présenter l'intelligence artificielle.

## 11. Le module d'intelligence artificielle (Roger KAINWANG)

Bonjour, je m'appelle KAINWANG Roger, je m'occupe de l'intelligence artificielle et des données.

Le module IA, c'est un Raspberry Pi 5 avec une carte AI HAT+ qui porte une puce Hailo-8 de 26 TOPS. Il est séparé du contrôleur de vol, donc il ne peut pas mettre le vol en danger. Et tout le calcul se fait à bord : aucune image ne part sur internet.

La chaîne est simple. La caméra fournit les images. Le détecteur YOLOv8s repère les personnes, les véhicules et les débris au sol. On ne garde que ce qui est dans la zone utile, la piste et ses abords. Un suivi relie les détections d'une image à l'autre pour qu'un objet ne déclenche qu'une seule alerte. Puis l'alerte part vers la station sol avec une image de preuve.

## 12. Données et fiabilité (Roger KAINWANG)

Pour le modèle, nous ne partons pas de zéro. Nous prenons un YOLOv8s déjà entraîné sur un grand nombre d'images, et nous l'adaptons à notre mission. Pour ça, nous utilisons FOD-A, une base publique de plus de 30 000 débris de piste annotés, et des images prises avec notre caméra, pour coller à l'angle de vue du drone. Nous ajoutons aussi des scènes vides, avec des ombres et des marquages, pour éviter les fausses alertes.

Si l'IA voit quelque chose qu'elle ne sait pas classer, elle ne devine pas : elle le signale comme « à vérifier », avec l'image. Si la liaison est coupée, elle continue à travailler et garde ses alertes à bord.

Enfin, c'est un outil d'aide : la décision reste à l'opérateur, et l'IA ne commande jamais le drone. Cédric va vous parler de la supervision.

## 13. Supervision et documentation (Cédric KODJOVI)

Bonjour, je m'appelle KODJOVI Eli Cédric Ankou, je m'occupe du back-end, du programme de vol et de la documentation.

Mon rôle, c'est que rien ne se perde. Le back-end enregistre chaque vol : la télémétrie, les alertes de l'IA avec leur image, et les journaux de vol. Toute l'équipe utilise le même format d'alerte. Les journaux sont signés : si quelqu'un modifie une ligne après coup, on le voit.

Je prépare aussi le programme de vol : les plans de mission, les check-lists avant et après le vol, et les procédures d'urgence. Et je tiens à jour le dossier de conception.

## 14. Conformité aux exigences du concours (Cédric KODJOVI)

Voici comment nous répondons aux exigences du concours. La navigation GPS avec retour automatique est gérée par le contrôleur de vol. La coupure d'urgence est prévue, avec une descente sécurisée. Le lien est chiffré et les messages sont signés. Nous visons 30 à 45 minutes d'autonomie. La charge utile, c'est la caméra jour et nuit et le module IA. Et la documentation, c'est le dossier de conception.

## 15. Calendrier (Cédric KODJOVI)

Côté calendrier, la candidature a été validée en août, la conception détaillée faite en septembre, et le dossier déposé fin septembre.

Nous sommes maintenant dans la phase de prototypage et d'intégration. En novembre viendront les essais au sol, en vol et de sécurité, pour être prêts pour la finale en décembre. Je rends la parole à Israel.

## 16. Budget prévisionnel (Israel AWADE)

Un mot sur le budget. Notre estimation se situe entre 730 000 et 1 400 000 francs CFA pour le drone, avec en plus 120 000 à 160 000 francs pour le module d'intelligence artificielle. Nous avons choisi des composants courants, qu'on peut trouver et remplacer facilement.

## 17. En résumé (Israel AWADE)

Pour résumer, la Sentinelle Aérienne décolle partout, vole longtemps grâce à son aile, analyse ses images à bord et communique de façon sécurisée. Nous l'avons pensée pour la sécurité de nos aéroports et de nos sites sensibles, et elle peut ensuite servir à la cartographie ou à l'aide humanitaire.

Merci à l'ANAC et aux organisateurs du CECFD. Merci pour votre attention, nous sommes prêts à répondre à vos questions.
