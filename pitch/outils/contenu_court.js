// Présentation courte (9 diapos), selon le plan de l'équipe. Notes d'oral dans « notes ».
const INTERVENANTS = require("./intervenants");

const DIAPOS = [
  {
    type: "couverture", section: "Introduction", qui: "israel", duree: 60,
    titre: "Sentinelle Aérienne",
    ligne: "SkyVision Togo · CECFD 2026 · ANAC",
    sous: "Drone VTOL de surveillance avec intelligence artificielle embarquée",
    image: "cao_iso",
    equipe: ["israel", "angelo", "cedric", "makafui", "roger"],
    notes: `Bonjour Mesdames et Messieurs les membres du jury. Je m'appelle AWADE Constantin Israel, je suis le chef de l'équipe SkyVision Togo et je m'occupe de la mécanique, de l'électronique et de la conception 3D.
Notre projet s'appelle Sentinelle Aérienne. C'est un drone qui décolle à la verticale, vole ensuite comme un avion, et analyse lui-même les images de sa caméra pour repérer ce qui ne va pas, en particulier sur une piste d'aéroport.
Nous sommes cinq. Angelo s'occupe du logiciel embarqué et de la station sol, Cédric du back-end, du programme de vol et de la documentation, Makafui des réseaux, de la télémétrie et de la sécurité, et Roger de l'intelligence artificielle.
Chacun va vous présenter sa partie. Cédric commence par le besoin.`,
  },
  {
    type: "deux_colonnes", section: "Besoin et conception", qui: "cedric", duree: 60,
    titre: "Le besoin : la sécurité des pistes",
    colonnes: [
      { titre: "Ce qui menace une piste", puces: [
        ["Débris (FOD)", "boulons, morceaux de pneu, outils oubliés, qui peuvent être aspirés par un réacteur ou faire éclater un pneu"],
        ["Abords et clôtures", "de grandes surfaces à contrôler régulièrement"],
        ["Intrusions", "personnes ou véhicules non autorisés près des pistes"],
      ] },
      { titre: "Les limites de l'inspection manuelle", puces: [
        "Elle se fait en véhicule et prend du temps",
        "La piste n'est pas disponible pendant le contrôle",
        "Le résultat dépend de l'attention de l'agent",
        "Elle est difficile la nuit et sur de grandes surfaces",
      ] },
    ],
    bas: "Notre objectif : inspecter depuis les airs, rapidement, et signaler tout de suite ce qui est anormal.",
    notes: `Merci Israel. Bonjour, je m'appelle KODJOVI Eli Cédric Ankou, je m'occupe du back-end, du programme de vol et de la documentation.
Sur une piste, un petit objet peut avoir de grosses conséquences : un boulon ou un morceau de pneu peut être aspiré par un réacteur ou faire éclater un pneu au décollage. On parle de FOD, pour Foreign Object Debris. Il faut aussi surveiller les abords, les clôtures, et repérer les personnes ou les véhicules qui n'ont rien à faire là.
Aujourd'hui, ce contrôle se fait surtout à la main : une équipe parcourt la piste en véhicule. Ça prend du temps, la piste est bloquée pendant ce temps, et le résultat dépend de l'attention des agents, surtout la nuit.
C'est de là qu'est parti notre projet : inspecter depuis les airs, plus vite, et signaler immédiatement ce qui est anormal. Israel va vous présenter le drone.`,
  },
  {
    type: "texte_image", qui: "israel", duree: 65,
    titre: "Conception du drone",
    blocs: [
      { h: 2.85, titre: "Configuration", puces: [
        "Conçu entièrement sous SolidWorks",
        "Voilure fixe et empennage en V",
        "Deux moteurs avant basculants, montés en nacelle sur l'aile",
        "Un moteur arrière pour le vol vertical, arrêté en croisière",
      ] },
      { h: 1.8, titre: "Ce que ça apporte", puces: [
        "Décollage et atterrissage verticaux, sans piste",
        "En croisière, c'est l'aile qui porte : 30 à 45 min visées",
      ] },
    ],
    images: [{ f: "cao_dessus", legende: "Vue de dessus (SolidWorks)" }, { f: "cao_profil", legende: "Vue de profil (SolidWorks)" }],
    notes: `Merci Cédric. Voici notre drone, tel que nous l'avons conçu sous SolidWorks.
C'est un VTOL à rotors basculants. Les deux moteurs avant sont montés en nacelle sur l'aile, avec un servomoteur qui les fait pivoter. Au décollage, ils sont tournés vers le haut et, avec le moteur arrière, ils soulèvent le drone comme un tricoptère.
Une fois en l'air, les deux moteurs avant basculent progressivement vers l'avant. Le drone prend de la vitesse, l'aile commence à porter, et le moteur arrière s'arrête. En croisière, ce sont les deux moteurs avant qui tirent l'appareil, et l'aile qui le porte. C'est ce qui nous permet de viser 30 à 45 minutes de vol.
Nous avons choisi un empennage en V : deux surfaces au lieu de trois, et il laisse de la place au moteur arrière. Le mât sur le dos porte le GPS, loin des perturbations, et le tube de Pitot dans le nez mesure la vitesse air.
Makafui va vous expliquer comment l'électronique est organisée.`,
  },
  {
    type: "double_coeur", section: "Technologies", qui: "makafui", duree: 70,
    titre: "Architecture électronique : la sécurité d'abord",
    blocs: [
      { titre: "Contrôleur de vol", sous: "STM32H743, Cortex-M7 à 480 MHz", puces: [
        "Stabilisation, moteurs et basculement",
        "Fail-safe matériel",
        "Retour automatique au point de départ (RTH)",
        "Fonctionne sans le module IA",
      ] },
      { titre: "Module IA", sous: "Raspberry Pi 5 + AI HAT+ (Hailo-8, 26 TOPS)", puces: [
        "Analyse des images à bord",
        "Alertes avec image de preuve",
        "Journal local des détections",
        "Ne commande jamais les moteurs",
      ] },
    ],
    lien: "MAVLink",
    lienDetail: "position vers le module IA\nalertes vers le sol",
    basTitre: "Pourquoi deux calculateurs séparés ?",
    basPuces: [
      "Si le module IA plante ou chauffe, le vol n'est pas touché",
      "Le contrôleur de vol garde des temps de réponse garantis",
      "Le retour automatique reste disponible même si l'IA est éteinte",
    ],
    note: "En secours : contrôleur du commerce compatible ArduPilot (Matek H743 ou Pixhawk).",
    notes: `Merci Israel. Bonjour, je m'appelle de MEDEIROS Makafui Komlan Léopoldo, je m'occupe des réseaux, de la télémétrie et de la sécurité.
Pour nous, la règle de base, c'est que le vol passe avant tout. Nous avons donc mis deux calculateurs dans le drone.
Le premier, c'est le contrôleur de vol, sur une carte STM32H743, un Cortex-M7 à 480 mégahertz. Il stabilise le drone, commande les moteurs et le basculement, et gère les sécurités : fail-safe et retour automatique au point de départ.
Le second, c'est le module d'intelligence artificielle, sur un Raspberry Pi 5.
Les deux communiquent en MAVLink : le module IA reçoit la position du drone et renvoie ses alertes. Mais il ne peut pas commander les moteurs. Si l'IA plante ou surchauffe, le drone continue de voler normalement, et il peut toujours rentrer seul.
Nous gardons aussi un contrôleur du commerce compatible en secours. Roger va vous présenter le module IA.`,
  },
  {
    type: "chaine", qui: "roger", duree: 75,
    titre: "Module d'intelligence artificielle embarquée",
    etapes: [
      ["Caméra", "images horodatées"],
      ["Détection", "YOLOv8s sur Hailo-8"],
      ["Zone d'intérêt", "piste et abords"],
      ["Suivi", "un objet, une alerte"],
      ["Alerte", "avec image de preuve"],
      ["Station sol", "par la liaison sécurisée"],
    ],
    colonnes: [
      { titre: "Matériel et modèle", puces: [
        "Raspberry Pi 5 + AI HAT+ 26 TOPS (Hailo-8)",
        "Détecteur YOLOv8s adapté par fine-tuning sur FOD-A et sur des images de notre caméra",
        "Trois classes : personnes, véhicules, débris au sol",
      ] },
      { titre: "Fonctionnement", puces: [
        "Tout le traitement se fait à bord, sans internet",
        "Un objet inconnu est signalé « à vérifier » avec son image",
        "Si la liaison est coupée, les alertes sont gardées à bord puis envoyées",
      ] },
    ],
    notes: `Merci Makafui. Bonjour, je m'appelle KAINWANG Roger, je m'occupe de l'intelligence artificielle et des données.
Le module IA, c'est un Raspberry Pi 5 avec une carte AI HAT+ qui porte une puce Hailo-8 de 26 TOPS. Tout le calcul se fait à bord : aucune image n'est envoyée sur internet.
Le traitement suit une chaîne simple. La caméra fournit les images. Le détecteur, un YOLOv8s, repère trois familles d'objets : les personnes, les véhicules et les débris au sol. On ne garde que ce qui se trouve dans la zone qui nous intéresse, la piste et ses abords. Ensuite, un suivi relie les détections d'une image à l'autre, pour qu'un même objet ne déclenche qu'une seule alerte. Enfin, l'alerte part vers la station sol avec une image de preuve.
Pour le modèle, nous partons d'un YOLOv8s pré-entraîné, que nous adaptons avec FOD-A, une base publique de plus de 30 000 débris de piste annotés, et avec des images prises par notre propre caméra, pour coller à l'angle de vue du drone.
Si l'IA voit quelque chose qu'elle ne sait pas classer, elle ne devine pas : elle le signale comme « à vérifier », avec l'image, et c'est l'opérateur qui décide. Et si la liaison radio est coupée, les alertes sont gardées à bord et envoyées dès qu'elle revient.
Angelo va vous montrer ce que voit l'opérateur au sol.`,
  },
  {
    type: "deux_colonnes", qui: "angelo", duo: "makafui", duree: 75,
    titre: "Station sol et communications",
    colonnes: [
      { titre: "Logiciel et station sol", taille: 16, puces: [
        "Station sol en Flutter, version mobile et web",
        "ArduPilot adapté à notre drone, avec délimitation de zone",
        "Télémétrie MAVLink en direct",
        "Alertes de l'IA avec leur image, enregistrement vidéo",
        "Historique des vols : API REST et base MySQL",
      ] },
      { titre: "Sécurité des communications", taille: 16, puces: [
        "Liaison chiffrée, messages MAVLink signés",
        "Détection du brouillage",
        "Contrôle de cohérence du GPS contre le leurrage",
        "Canal d'urgence indépendant : retour ou coupure",
        "Liaison satellite de secours en cours d'essai",
      ] },
    ],
    hColonnes: 2.75,
    tableau: {
      titre: "Trois liaisons indépendantes",
      entetes: ["Liaison", "Ce qu'elle transporte", "Portée visée"],
      colW: [4.0, 5.0, 3.033],
      lignes: [
        ["Vidéo HD", "Image de la caméra et informations de vol", "10 à 15 km"],
        ["Radio longue portée chiffrée", "Télémétrie, ordres et alertes de l'IA", "30 à 50 km (théorique)"],
        ["Canal d'urgence ExpressLRS", "Retour au point de départ, coupure des moteurs", "Indépendant des autres"],
      ],
    },
    notes: `Merci Roger. Bonjour, je m'appelle LOGO ADANTO Angelo, je m'occupe du logiciel embarqué et de la station sol.
Dans le drone, nous utilisons ArduPilot, que nous adaptons à notre configuration à rotors basculants. Nous y avons ajouté une délimitation de zone : si le drone sort de l'espace autorisé, il fait demi-tour automatiquement.
Au sol, nous développons la station en Flutter, ce qui nous donne une version mobile et une version web avec le même code. L'opérateur y prépare sa mission, suit la télémétrie en direct, voit arriver les alertes de l'IA avec leur image, et la vidéo est enregistrée. Tout l'historique des vols est stocké par le back-end de Cédric, avec une API REST et une base MySQL.
[Makafui] Pour transporter tout ça, nous avons trois liaisons indépendantes : un lien vidéo HD, une radio longue portée chiffrée pour la télémétrie et les ordres, et un canal d'urgence séparé. Les données passent par une liaison chiffrée. Chaque message MAVLink est signé : si quelqu'un envoie un ordre sans la bonne clé, le drone l'ignore. On surveille la qualité des liaisons pour repérer un brouillage, et on vérifie la cohérence du GPS avec les autres capteurs pour détecter un leurrage. En dernier recours, un canal d'urgence indépendant permet toujours de faire revenir le drone ou de couper les moteurs. Nous essayons aussi une liaison satellite en secours.`,
  },
  {
    type: "liste_num", section: "Valeur ajoutée", qui: "israel", duree: 65,
    titre: "Ce que notre drone apporte de nouveau",
    items: [
      ["Deux calculateurs séparés", "Le STM32H7 gère le vol, le Hailo-8 gère la vision. Une panne de l'IA ne met pas l'appareil en danger."],
      ["Un VTOL à rotors basculants", "Il décolle à la verticale, puis ses deux moteurs avant basculent pour la croisière."],
      ["L'IA à bord, sans cloud", "Les images sont analysées pendant le vol : l'alerte arrive tout de suite, pas au retour."],
      ["Une sécurité en plusieurs niveaux", "Chiffrement et signature MAVLink, anti-brouillage, anti-leurrage GPS et canal de secours."],
    ],
    image: { f: "cao_iso", legende: "Vue en perspective (SolidWorks)" },
    notes: `Si on résume ce qui fait la différence de notre projet, il y a quatre points.
D'abord, les deux calculateurs séparés. Le vol et la vision ne tournent pas sur la même carte. C'est un choix de sécurité : une panne de l'IA ne fait pas tomber le drone.
Ensuite, la configuration à rotors basculants. Les mêmes moteurs servent au décollage et à la croisière, donc on transporte moins de moteurs inutiles en vol, et on gagne en autonomie.
Troisième point, l'IA est à bord. On n'a pas besoin de réseau ni de cloud : l'alerte arrive pendant le vol, au moment où l'objet est vu.
Enfin, la sécurité des communications est pensée dès le départ, avec plusieurs niveaux de protection.
Et le drone ne sert pas qu'aux aéroports. Cédric va vous montrer les autres usages possibles.`,
  },
  {
    type: "tableau", qui: "cedric", duree: 65,
    titre: "Domaines d'application",
    entetes: ["Secteur", "Utilisations", "Ce qu'on adapte"],
    colW: [3.3, 5.4, 3.333],
    rowH: 0.62, taille: 15,
    lignes: [
      ["Aviation civile", "Inspection de piste, débris (FOD), clôtures", "Caméra + IA de détection"],
      ["Agriculture et environnement", "Suivi des cultures, environnement, feux de brousse", "Caméra thermique ou multispectrale"],
      ["Infrastructures", "Lignes électriques, pylônes, ponts, port de Lomé", "Caméra zoom, IA de défauts"],
      ["Aide humanitaire", "Petits colis médicaux vers des zones enclavées", "Soute de largage (version adaptée)"],
      ["Cartographie", "Orthophotos, relevés topographiques", "Appareil photo de cartographie"],
    ],
    bas: "Le drone, la station sol et le back-end restent les mêmes ; on change la charge utile et le modèle d'IA.",
    notes: `Notre premier cas d'usage, c'est l'aéroport : inspection de piste, recherche de débris et surveillance des clôtures.
Mais la même plateforme peut servir ailleurs. En agriculture et pour l'environnement, avec une caméra thermique ou multispectrale, on peut suivre les cultures ou repérer des départs de feux de brousse. Pour les infrastructures, on peut inspecter des lignes électriques, des pylônes, des ponts, ou les installations du port de Lomé.
Pour l'aide humanitaire, comme le drone n'a pas besoin de piste, une version adaptée peut livrer de petits colis, par exemple des médicaments, dans des zones difficiles d'accès. Et en cartographie, il peut faire des relevés photo à basse altitude.
À chaque fois, le drone, la station et le back-end restent les mêmes. On change la charge utile et on entraîne le modèle d'IA pour la nouvelle tâche. Israel va conclure.`,
  },
  {
    type: "frise", section: "Conclusion", qui: "israel", duree: 50,
    titre: "Avancement et prochaines étapes",
    etapes: [
      ["Août – sept.", "Conception et dossier de candidature", "fait"],
      ["Octobre", "Prototypage et intégration", "ici"],
      ["Novembre", "Essais au sol, en vol et de sécurité", ""],
      ["Décembre 2026", "Finale : démonstration", ""],
    ],
    fin: ["Merci à l'ANAC et aux organisateurs du CECFD 2026.", "Nous sommes prêts à répondre à vos questions."],
    notes: `Pour finir, où en sommes-nous ? La conception est faite et le dossier a été déposé. Nous sommes maintenant dans la phase de prototypage et d'intégration. En novembre viendront les essais au sol, puis en vol, et les tests de sécurité, pour être prêts pour la finale en décembre.
Nous remercions l'ANAC et les organisateurs du CECFD pour ce concours, qui nous permet de travailler sur un vrai problème de sécurité aérienne, ici au Togo.
Merci pour votre attention. Nous sommes prêts à répondre à vos questions.`,
  },
];

module.exports = { INTERVENANTS, DIAPOS };
