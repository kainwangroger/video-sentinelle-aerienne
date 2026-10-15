# Pitch Sentinelle Aérienne : script oral (6 diapos)

Support : `sentinelle_aerienne_risques_securite.pptx`. Le même texte se trouve dans les notes de l'orateur de chaque diapo.

Durée indicative : environ 6 minutes.

| Diapo | Titre | Qui parle | Durée |
|---|---|---|---|
| 1 | Sentinelle Aérienne | Israel AWADE | 30 s |
| 2 | Les avantages | Israel AWADE | 60 s |
| 3 | Les risques et nos réponses | Israel AWADE puis Makafui de MEDEIROS | 90 s |
| 4 | La réglementation | Cédric KODJOVI | 75 s |
| 5 | La sécurité | Makafui de MEDEIROS | 75 s |
| 6 | En résumé | Israel AWADE | 35 s |

## 1. Sentinelle Aérienne (Israel AWADE)

Bonjour. Dans cette partie, nous vous présentons ce que notre drone apporte, les risques que nous avons identifiés, le cadre réglementaire que nous respectons, et les mesures de sécurité prévues.

## 2. Les avantages (Israel AWADE)

Notre drone décolle à la verticale, donc il n'a pas besoin de piste. En croisière, c'est l'aile qui le porte : il vole longtemps et couvre de grandes surfaces.

L'IA à bord donne l'alerte pendant le vol, sans internet. La liaison est sécurisée. Les agents n'ont plus à parcourir la piste eux-mêmes. Et la même plateforme peut servir à d'autres missions en changeant la charge utile.

## 3. Les risques et nos réponses (Israel AWADE puis Makafui de MEDEIROS)

Nous avons listé les risques principaux, et pour chacun une réponse.

Si la liaison radio est perdue, le drone rentre seul au point de départ et atterrit à la verticale. Si la batterie devient faible, il rentre ; si elle est critique, il atterrit immédiatement.

Le moment le plus délicat, c'est le vol vertical : on le garde court, à faible hauteur, au-dessus d'une zone dégagée. Les servos qui font basculer les moteurs sont contrôlés à chaque check-list.

[Makafui] Côté radio, contre le brouillage et le leurrage GPS, nous comparons deux GPS avec les autres capteurs. Contre le piratage, la liaison est chiffrée et les ordres sont signés. Le géorepérage empêche de sortir de la zone autorisée.

Enfin, l'IA peut se tromper : un objet incertain est signalé « à vérifier », et c'est toujours l'humain qui décide.

## 4. La réglementation (Cédric KODJOVI)

Côté réglementation, nous respectons deux grandes familles de règles.

Pour le vol : nous ne volons qu'avec l'autorisation de l'ANAC, en vue directe du télépilote sauf autorisation particulière, dans une zone et à une hauteur limitées, que le géorepérage fait respecter. Pas de vol au-dessus de la foule ni près d'un aérodrome sans accord. Le télépilote est formé et suit des check-lists.

Pour les ondes et les données : nos fréquences radio doivent être autorisées par l'ARCEP. Comme le drone peut filmer des personnes, nous respectons la loi togolaise sur la protection des données personnelles : pas de reconnaissance faciale, on ne garde que les images d'alerte, et l'accès est réservé aux personnes autorisées.

Enfin, les essais sur un vrai site se font uniquement avec l'accord de l'exploitant.

## 5. La sécurité (Makafui de MEDEIROS)

Bonjour, je m'appelle de MEDEIROS Makafui. La sécurité se joue à deux niveaux.

D'abord la sécurité du vol. Le contrôleur de vol est séparé du module IA, donc une panne de l'IA ne touche pas le vol. En cas de perte de radio, de batterie faible ou de GPS dégradé, le drone applique automatiquement une procédure de secours : retour au point de départ ou atterrissage. Le géorepérage limite la zone et la hauteur, et une coupure d'urgence reste toujours possible. Avant le décollage, le drone vérifie lui-même que tout est prêt.

Ensuite la cybersécurité. La liaison est chiffrée, et chaque message est signé avec une clé secrète chargée au sol : un faux ordre est rejeté. Nous détectons le brouillage, nous comparons les sources de position contre le leurrage GPS, et les journaux de vol sont signés pour qu'on ne puisse pas les modifier.

## 6. En résumé (Israel AWADE)

Pour résumer : notre drone est utile, il est rapide, autonome et n'a pas besoin de piste. Nous avons identifié ses risques et prévu une réponse pour chacun. Nous respectons le cadre de l'ANAC, de l'ARCEP et la protection des données. Et la sécurité est pensée dès la conception. Merci, nous sommes prêts pour vos questions.
