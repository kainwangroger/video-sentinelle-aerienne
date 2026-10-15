// Pitch v2 (9 diapos, accent innovations et polyvalence) : intervenants, textes et notes d'oral.

const INTERVENANTS = {
  israel: { nom: "AWADE Constantin Israel", court: "Israel", pole: "Chef d'équipe · Mécanique, électronique et conception 3D", puce: "Chef d'équipe", icone: "FaTools" },
  angelo: { nom: "LOGO ADANTO Angelo", court: "Angelo", pole: "Logiciel embarqué et station sol", puce: "Logiciel et station sol", icone: "FaLaptopCode" },
  cedric: { nom: "KODJOVI Eli Cédric Ankou", court: "Cédric", pole: "Back-end, programme de vol et documentation", puce: "Back-end et programme de vol", icone: "FaDatabase" },
  makafui: { nom: "de MEDEIROS Makafui Komlan Léopoldo", court: "Makafui", pole: "Réseaux, télémétrie et sécurité", puce: "Réseaux et sécurité", icone: "FaBroadcastTower" },
  roger: { nom: "KAINWANG Roger", court: "Roger", pole: "Intelligence artificielle et données", puce: "IA et données", icone: "FaBrain" },
};

const ORDRE = ["israel", "angelo", "cedric", "makafui", "roger"];

// qui : intervenant principal ; duo : second intervenant éventuel sur la même diapo.
const DIAPOS = [
  {
    id: "titre", qui: "israel", duree: 60,
    notes: `Bonjour Mesdames et Messieurs les membres du jury.
Je m'appelle AWADE Constantin Israel, chef de l'équipe SkyVision Togo. Je m'occupe de la mécanique, de l'électronique et de la conception 3D du drone.
Nous vous présentons la Sentinelle Aérienne : un drone hybride à décollage vertical, conçu pour la sécurité des aéroports et la surveillance des zones sensibles.
Notre équipe compte cinq pôles. Angelo, au logiciel embarqué et à la station sol. Cédric, au back-end, au programme de vol et à la documentation. Makafui, aux réseaux, à la télémétrie et à la sécurité. Et Roger, à l'intelligence artificielle et aux données.
Chacun va vous présenter la partie dont il est responsable. Je laisse d'abord Cédric vous expliquer le besoin.`,
  },
  {
    id: "besoin", qui: "cedric", duree: 60,
    notes: `Merci Israel. Bonjour, je suis KODJOVI Eli Cédric Ankou, responsable du back-end, du programme de vol et de la documentation.
Partons du terrain. Sur une piste, un simple débris, un boulon, un morceau de pneu, un outil oublié, peut être aspiré par un réacteur ou crever un pneu au décollage. C'est ce qu'on appelle les FOD, Foreign Object Debris.
À cela s'ajoutent l'inspection des abords et le risque d'intrusion de personnes ou de véhicules.
Aujourd'hui, ces contrôles sont surtout manuels : une équipe parcourt la piste en véhicule. C'est long, ça mobilise la piste, ça dépend de l'attention humaine, et c'est difficile la nuit ou sur de grandes surfaces.
Notre besoin est donc clair : un moyen aérien, autonome et intelligent, qui inspecte vite et signale immédiatement ce qu'il trouve. Israel va vous présenter la plateforme.`,
  },
  {
    id: "conception", qui: "israel", duree: 60,
    notes: `Merci Cédric. La plateforme, c'est un VTOL hybride, modélisé sous SolidWorks.
Il combine une voilure fixe, des rotors verticaux pour le décollage et l'atterrissage, et une propulsion de croisière bimoteur montée sur les poutres.
Concrètement : il décolle à la verticale, comme un multirotor, depuis n'importe quelle zone dégagée, sans piste. Puis il bascule en vol horizontal : c'est l'aile qui le porte, ce qui consomme beaucoup moins d'énergie. On garde la souplesse du multirotor et l'autonomie de l'avion.
La cellule est en carbone et composite, avec des zones en fibre de verre là où passent les antennes. Pour l'électronique, nous concevons nos propres cartes de distribution et le câblage.
Makafui va maintenant vous expliquer l'architecture avionique, pensée d'abord pour la sécurité.`,
  },
  {
    id: "avionique", qui: "makafui", duree: 70,
    notes: `Merci Israel. Bonjour, je suis de MEDEIROS Makafui Komlan Léopoldo, responsable des réseaux, de la télémétrie et de la sécurité.
Notre principe de base : le vol passe avant tout. Nous avons donc séparé le drone en deux cerveaux.
Le premier, c'est le contrôleur de vol : une carte STM32H743, un Cortex-M7 à 480 mégahertz. Il fait une seule chose, et il la fait en temps réel : stabiliser le drone, piloter les moteurs, et déclencher les sécurités, le fail-safe et le retour automatique au point de départ.
Le second, c'est le module d'IA, sur un Raspberry Pi 5.
Pourquoi les séparer ? Parce que si le traitement d'image plante, chauffe ou ralentit, le vol n'est pas affecté. L'IA lit la position du drone et envoie des alertes, mais elle ne commande jamais les moteurs. Le retour automatique fonctionne même si le module IA est éteint.
Et en secours, nous gardons un contrôleur du commerce compatible. Roger va vous présenter ce second cerveau.`,
  },
  {
    id: "ia", qui: "roger", duree: 75,
    notes: `Merci Makafui. Bonjour à tous, je m'appelle KAINWANG Roger, responsable de l'intelligence artificielle et des données.
Notre IA tourne entièrement à bord, sur un Raspberry Pi 5 équipé d'un accélérateur AI HAT+ de 26 TOPS, avec une puce Hailo-8. Aucune image ne part vers internet.
Le détecteur est un YOLOv8s, que nous adaptons par fine-tuning sur FOD-A, une base publique de plus de 30 000 débris annotés, et sur nos propres images filmées avec la caméra du drone. Il repère trois familles : les personnes, les véhicules et les débris au sol.
Un suivi relie les détections d'une image à l'autre, pour qu'un objet ne déclenche qu'une seule alerte. Chaque alerte est enregistrée à bord avec son image de preuve, puis envoyée à la station.
Et pour un objet jamais vu, nous ne prétendons pas le reconnaître : il est signalé « à vérifier », avec son image. L'IA est une aide à l'inspection : la décision reste humaine. Angelo va vous montrer comment ces alertes arrivent au sol.`,
  },
  {
    id: "logiciel", qui: "angelo", duo: "makafui", duree: 70,
    notes: `Merci Roger. Bonjour, je m'appelle LOGO ADANTO Angelo, responsable du logiciel embarqué et de la station sol.
Côté drone, nous utilisons une version personnalisée d'ArduPilot, avec une délimitation de zone : le drone ne peut pas sortir de l'espace autorisé.
Côté sol, nous développons une station en Flutter et en version web. L'opérateur y planifie la mission, suit la télémétrie MAVLink en direct, voit les alertes de l'IA avec leur image, et la vidéo est enregistrée. Les vols et les alertes sont archivés par le back-end de Cédric, via une API REST et une base MySQL.
[Makafui] Toutes ces données circulent sur une liaison chiffrée, et chaque message MAVLink est signé : un ordre non authentifié est rejeté. Nous détectons le brouillage et le leurrage GPS en comparant plusieurs sources de position. Un canal d'urgence indépendant permet toujours de faire revenir le drone, et nous testons une liaison satellite en secours.`,
  },
  {
    id: "innovations", qui: "israel", duree: 70,
    notes: `Ce qui fait la différence de la Sentinelle Aérienne, ce sont quatre innovations.
Un : une architecture double cœur. Le STM32H7 gère le vol, le Hailo gère la vision. Les deux sont séparés de façon étanche : une panne de l'IA ne met jamais l'aéronef en danger.
Deux : un VTOL hybride intelligent. Il décolle seul à la verticale, bascule automatiquement en croisière et couvre de grandes distances, sans piste.
Trois : l'inférence en périphérie, à 26 TOPS. L'image est analysée à bord, en temps réel, sans cloud et sans réseau : l'alerte arrive pendant le vol, pas après.
Quatre : une sécurité multicouche. Chiffrement et signature des messages, protection contre le brouillage et le leurrage GPS, et canal de secours indépendant.
Et cette plateforme ne sert pas qu'aux aéroports : Cédric va vous montrer sa polyvalence.`,
  },
  {
    id: "applications", qui: "cedric", duree: 70,
    notes: `Grâce à sa charge utile modulaire, la Sentinelle Aérienne s'adapte à de nombreux secteurs.
En aviation civile, c'est notre mission première : inspection des pistes, détection des débris et surveillance des clôtures.
En agriculture et en environnement : surveillance des cultures, suivi environnemental et détection précoce des feux de brousse.
Pour les infrastructures critiques : lignes électriques, pylônes, ponts, ou encore le port de Lomé.
Pour l'aide humanitaire : grâce au décollage vertical, une version adaptée peut acheminer de petits colis, comme des médicaments, vers des zones enclavées.
Et en cartographie : relevés orthophotographiques et topographiques à basse altitude.
Le même drone, la même station, le même back-end : seule la charge utile et le modèle d'IA changent. Israel va conclure.`,
  },
  {
    id: "conclusion", qui: "israel", duree: 55,
    notes: `Où en sommes-nous ? La conception est terminée et le dossier a été soumis. Nous sommes en phase de prototypage : assemblage, intégration électronique et essais sur banc. Viendront ensuite les essais au sol, puis en vol, et les tests de sécurité, en octobre et novembre, pour être prêts pour la finale de décembre 2026.
Nous remercions l'ANAC et les organisateurs du CECFD pour cette opportunité, qui permet à de jeunes Togolais de concevoir des solutions aéronautiques pour leur pays.
Merci pour votre attention. Toute l'équipe est à votre disposition pour vos questions.`,
  },
];

module.exports = { INTERVENANTS, ORDRE, DIAPOS };
