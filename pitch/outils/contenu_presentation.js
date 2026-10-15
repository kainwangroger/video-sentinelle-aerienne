// Présentation complète (23 diapos) : drone et composants, technologies, avantages,
// risques, réglementation, sécurité, applications, calendrier, budget.
const INTERVENANTS = require("./intervenants");

const DIAPOS = [
  // ---------------------------------------------------------------- introduction
  {
    type: "couverture", section: "Introduction", qui: "israel", duree: 60,
    titre: "Sentinelle Aérienne",
    ligne: "SkyVision Togo · CECFD 2026 · ANAC",
    sous: "Drone VTOL de surveillance avec intelligence artificielle embarquée",
    image: "cao_iso",
    equipe: ["israel", "angelo", "cedric", "makafui", "roger"],
    notes: `Bonjour Mesdames et Messieurs les membres du jury. Je m'appelle AWADE Constantin Israel, je suis le chef de l'équipe SkyVision Togo et je m'occupe de la mécanique, de l'électronique et de la conception 3D.
Notre projet s'appelle Sentinelle Aérienne : un drone qui décolle à la verticale, vole ensuite comme un avion, et analyse lui-même les images de sa caméra pour repérer ce qui ne va pas, en particulier sur une piste d'aéroport.
Nous sommes cinq : Angelo au logiciel embarqué et à la station sol, Cédric au back-end, au programme de vol et à la documentation, Makafui aux réseaux, à la télémétrie et à la sécurité, et Roger à l'intelligence artificielle. Cédric commence par le besoin.`,
  },
  {
    type: "deux_colonnes", qui: "cedric", duree: 60,
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
Aujourd'hui, ce contrôle se fait surtout à la main, en véhicule. Ça prend du temps, la piste est bloquée, et le résultat dépend de l'attention des agents, surtout la nuit.
Notre objectif : inspecter depuis les airs, plus vite, et signaler tout de suite ce qui est anormal. Israel va vous présenter le drone.`,
  },

  // ---------------------------------------------------------------- le drone
  {
    type: "texte_image", section: "Le drone", qui: "israel", duree: 45,
    titre: "Notre réponse : un VTOL à rotors basculants",
    blocs: [
      { h: 2.5, titre: "Le principe", puces: [
        "Décollage vertical, comme un multirotor",
        "Les deux moteurs avant basculent vers l'avant",
        "En croisière, l'aile porte le drone",
      ] },
      { h: 2.2, titre: "Nos deux priorités", puces: [
        "Une IA qui analyse les images à bord, pendant le vol",
        "Une liaison sécurisée dès la conception",
      ] },
    ],
    images: [{ f: "cao_iso", legende: "Vue en perspective (SolidWorks)" }],
    notes: `Merci Cédric. Notre réponse, c'est un VTOL à rotors basculants. Il décolle à la verticale comme un multirotor, depuis n'importe quel terrain dégagé. Ensuite, ses deux moteurs avant basculent vers l'avant et il vole comme un avion : c'est l'aile qui le porte, ce qui consomme beaucoup moins d'énergie.
À cette plateforme, nous ajoutons deux choses : une intelligence artificielle qui analyse les images à bord, et une liaison radio sécurisée.`,
  },
  {
    type: "annotee", qui: "israel", duree: 70,
    titre: "Les parties du drone",
    image: "cao_dessus",
    etiquettes: [
      { t: "Nez et tube de Pitot", d: "mesure la vitesse air", fx: 0.504, fy: 0.07, cote: "g", ly: 1.75 },
      { t: "Moteur avant gauche", d: "basculant, en nacelle", fx: 0.374, fy: 0.197, cote: "g", ly: 2.6 },
      { t: "Aile", d: "porte le drone en croisière", fx: 0.17, fy: 0.42, cote: "g", ly: 3.6 },
      { t: "Empennage en V", d: "profondeur et direction", fx: 0.40, fy: 0.85, cote: "g", ly: 5.6 },
      { t: "Moteur avant droit", d: "basculant, en nacelle", fx: 0.629, fy: 0.19, cote: "d", ly: 1.75 },
      { t: "Servo de basculement", d: "fait pivoter le moteur", fx: 0.63, fy: 0.30, cote: "d", ly: 2.6 },
      { t: "Mât GNSS", d: "GPS éloigné des perturbations", fx: 0.504, fy: 0.432, cote: "d", ly: 3.6 },
      { t: "Moteur arrière", d: "vol vertical uniquement", fx: 0.50, fy: 0.675, cote: "d", ly: 4.6 },
      { t: "Fuselage", d: "batterie, électronique, module IA", fx: 0.52, fy: 0.56, cote: "g", ly: 4.6 },
    ],
    notes: `Voici les parties du drone, vues de dessus.
À l'avant, le nez porte le tube de Pitot, qui mesure la vitesse de l'air : c'est indispensable pour savoir quand l'aile porte assez. De chaque côté, un moteur monté en nacelle sur l'aile, avec un servomoteur qui le fait pivoter.
Au centre, le fuselage contient la batterie, l'électronique et le module d'intelligence artificielle. Sur le dos, le mât porte le GPS, loin des perturbations électriques.
À l'arrière, le moteur arrière ne sert qu'au vol vertical, et l'empennage en V gère à la fois la profondeur et la direction. Je vais détailler les deux parties les plus importantes.`,
  },
  {
    type: "texte_image", qui: "israel", duree: 60,
    titre: "Les moteurs avant basculants",
    blocs: [
      { h: 2.9, titre: "Comment ça marche", puces: [
        "Un moteur et son hélice dans chaque nacelle",
        "Un servomoteur fait pivoter l'ensemble",
        "Vers le haut au décollage, vers l'avant en croisière",
        "Les mêmes moteurs servent aux deux phases",
      ] },
      { h: 1.8, titre: "Nos choix", puces: [
        "Servos à engrenages métal, avec marge de couple",
        "Débattement vérifié à chaque check-list",
      ] },
    ],
    images: [{ f: "moteur_brushless", legende: "Moteur sans balais (brushless)" }, { f: "esc_moteur", legende: "Variateur (ESC) relié à un moteur" }],
    notes: `Les deux moteurs avant sont la pièce maîtresse du drone. Chacun est monté dans une nacelle, avec un servomoteur qui le fait pivoter. Au décollage, il pousse vers le haut ; en croisière, il tire vers l'avant.
L'avantage, c'est que les mêmes moteurs servent au décollage et à la croisière : on ne transporte pas de moteurs inutiles en vol, donc on gagne de la masse et de l'autonomie.
Comme le basculement est critique, nous choisissons des servos à engrenages métal, avec une bonne marge, et leur débattement est vérifié avant chaque vol.`,
  },
  {
    type: "texte_image", qui: "israel", duree: 50,
    titre: "Le moteur arrière et l'empennage en V",
    blocs: [
      { h: 2.3, titre: "Moteur arrière", puces: [
        "Logé sous la queue du fuselage",
        "Équilibre le drone en vol vertical",
        "Arrêté en croisière",
      ] },
      { h: 2.4, titre: "Empennage en V", puces: [
        "Deux surfaces au lieu de trois",
        "Chaque gouverne agit en profondeur et en direction",
        "Moins de masse et de traînée",
      ] },
    ],
    images: [{ f: "gouverne_servo", legende: "Gouverne d'empennage en V et sa commande par servo" }],
    notes: `À l'arrière, le moteur est logé sous la queue. Avec les deux moteurs avant, il forme un triangle qui tient le drone en équilibre en vol vertical. En croisière, il s'arrête.
L'empennage en V remplace la dérive et la profondeur classiques. Avec deux surfaces au lieu de trois, on a moins de masse, moins de traînée et moins de servos. Chaque gouverne agit à la fois en profondeur et en direction, et c'est le contrôleur de vol qui fait le mélange.`,
  },
  {
    type: "tableau", qui: "israel", duree: 40,
    titre: "Caractéristiques principales",
    entetes: ["Élément", "Choix retenu"],
    colW: [3.6, 8.433], rowH: 0.56, taille: 16,
    lignes: [
      ["Configuration", "VTOL à rotors basculants, trois moteurs"],
      ["Propulsion", "2 moteurs avant basculants + 1 moteur arrière"],
      ["Empennage", "En V"],
      ["Autonomie visée", "30 à 45 minutes"],
      ["Contrôleur de vol", "STM32H743 sous ArduPilot"],
      ["Module IA", "Raspberry Pi 5 + AI HAT+ (Hailo-8)"],
      ["Charge utile", "Caméra stabilisée jour/nuit"],
      ["Liaisons", "Vidéo HD, radio chiffrée, canal d'urgence"],
    ],
    notes: `En résumé pour la partie drone : trois moteurs, dont deux basculants, un empennage en V, et une autonomie visée de 30 à 45 minutes. Le contrôleur de vol est une carte STM32H743 sous ArduPilot, le module IA un Raspberry Pi 5 avec une puce Hailo-8, et la charge utile une caméra stabilisée jour et nuit. Angelo va vous expliquer comment le drone vole.`,
  },

  // ---------------------------------------------------------------- technologies
  {
    type: "tableau", section: "Technologies", qui: "angelo", duree: 60,
    titre: "Le vol : du décollage vertical à la croisière",
    entetes: ["Phase", "Moteurs avant", "Moteur arrière", "Ce qui porte le drone"],
    colW: [2.6, 3.4, 2.6, 3.433], rowH: 0.7, taille: 17,
    lignes: [
      ["Décollage", "Vers le haut", "En marche", "Les trois moteurs"],
      ["Transition", "Basculent progressivement", "En marche", "Les moteurs, puis l'aile"],
      ["Croisière", "Vers l'avant, ils tirent", "Arrêté", "L'aile"],
      ["Atterrissage", "Reviennent vers le haut", "En marche", "Les trois moteurs"],
    ],
    bas: "La transition est gérée automatiquement par ArduPilot, à partir de la vitesse air mesurée par le tube de Pitot.",
    notes: `Merci Israel. Bonjour, je m'appelle LOGO ADANTO Angelo, je m'occupe du logiciel embarqué et de la station sol.
Le vol se fait en quatre phases. Au décollage, les moteurs avant sont tournés vers le haut et, avec le moteur arrière, ils soulèvent le drone. Pendant la transition, les moteurs avant basculent petit à petit vers l'avant : le drone accélère et l'aile commence à porter. En croisière, le moteur arrière s'arrête : les moteurs avant tirent le drone et l'aile le porte. À l'atterrissage, on fait l'inverse.
C'est ArduPilot qui gère tout ça automatiquement, à partir de la vitesse air mesurée par le tube de Pitot.`,
  },
  {
    type: "texte_image", qui: "angelo", duree: 50,
    titre: "Les capteurs de navigation",
    blocs: [
      { h: 4.8, puces: [
        ["GNSS (GPS)", "deux récepteurs sur le mât, pour la position"],
        ["Tube de Pitot", "dans le nez, pour la vitesse air"],
        ["Centrale inertielle", "accélérations et rotations du drone"],
        ["Baromètre", "altitude"],
        ["Compas", "direction du nez"],
        ["Fusion des capteurs", "le contrôleur combine tout pour savoir où il est"],
      ] },
    ],
    images: [{ f: "gnss", legende: "Module GNSS avec compas intégré" }, { f: "pitot", legende: "Tube de Pitot (prises de pression)" }],
    notes: `Pour savoir où il est et comment il vole, le drone utilise plusieurs capteurs. Deux récepteurs GPS sur le mât donnent la position. Le tube de Pitot, dans le nez, mesure la vitesse de l'air. La centrale inertielle mesure les accélérations et les rotations, le baromètre l'altitude, et le compas la direction.
Le contrôleur de vol combine toutes ces mesures. Si une source donne une valeur qui ne colle pas avec les autres, par exemple un GPS brouillé, elle est écartée. Makafui va vous présenter l'architecture électronique.`,
  },
  {
    type: "double_coeur", qui: "makafui", duree: 65,
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
    notes: `Merci Angelo. Bonjour, je m'appelle de MEDEIROS Makafui Komlan Léopoldo, je m'occupe des réseaux, de la télémétrie et de la sécurité.
Pour nous, le vol passe avant tout. Nous avons donc mis deux calculateurs dans le drone. Le contrôleur de vol, sur une carte STM32H743, stabilise le drone, commande les moteurs et le basculement, et gère les sécurités. Le module d'intelligence artificielle, sur un Raspberry Pi 5, analyse les images.
Ils communiquent en MAVLink : l'IA reçoit la position et renvoie ses alertes, mais elle ne peut pas commander les moteurs. Si elle plante, le drone continue de voler et peut toujours rentrer seul. Nous gardons aussi un contrôleur du commerce en secours.`,
  },
  {
    type: "rangees", qui: "israel", duree: 55,
    titre: "Énergie, pilotage et mission",
    rangees: [
      { titre: "Énergie", etapes: [["Batterie LiPo", "source d'énergie"], ["Module de puissance", "mesure tension et courant"], ["Variateurs (ESC) ×3", "règlent la vitesse"], ["Moteurs ×3", "2 avant, 1 arrière"]] },
      { titre: "Pilotage", etapes: [["Capteurs", "GNSS ×2, Pitot, IMU"], ["Contrôleur de vol", "STM32H743, ArduPilot"], ["Servos", "basculement ×2, empennage V ×2"], ["Liaisons radio", "vidéo, télémétrie, urgence"]] },
      { titre: "Mission", etapes: [["Caméra", "stabilisée jour/nuit"], ["Raspberry Pi 5", "+ Hailo-8"], ["Alerte", "image de preuve"], ["Station sol", "opérateur"]] },
    ],
    bas: "Alimentations séparées : 5 V propre pour les radios, 5 V / 5 A dédié au Raspberry Pi.",
    notes: `[Israel] Voici comment l'électronique est organisée, en trois chaînes.
L'énergie : la batterie lithium-polymère alimente un module de puissance qui mesure la tension et le courant, puis trois variateurs qui règlent la vitesse des trois moteurs.
Le pilotage : les capteurs envoient leurs mesures au contrôleur de vol, qui commande les servos de basculement et les gouvernes de l'empennage, et communique par les liaisons radio.
La mission : la caméra envoie ses images au Raspberry Pi, qui produit les alertes envoyées à la station sol.
Nous prévoyons des alimentations séparées : une pour les radios, et une dédiée au Raspberry Pi, pour qu'aucune ne perturbe l'autre.`,
  },
  {
    type: "galerie", qui: "israel", duree: 60,
    titre: "Les principaux composants",
    colonnesGrille: 6,
    photos: [
      { f: "batterie_lipo", t: "Batterie LiPo", d: "réserve d'énergie" },
      { f: "module_puissance", t: "Module de puissance", d: "mesure tension et courant" },
      { f: "esc_moteur", t: "Variateurs (ESC)", d: "règlent la vitesse des moteurs" },
      { f: "moteur_brushless", t: "Moteurs brushless", d: "2 avant basculants, 1 arrière" },
      { f: "controleur_h743", t: "Contrôleur de vol", d: "STM32H743 sous ArduPilot" },
      { f: "gnss", t: "Module GNSS", d: "position et compas" },
      { f: "pitot", t: "Tube de Pitot", d: "vitesse air" },
      { f: "radio_longue_portee", t: "Radio longue portée", d: "télémétrie chiffrée" },
      { f: "radios_rc", t: "Radiocommande", d: "pilotage et canal d'urgence" },
      { f: "raspberry_pi5", t: "Raspberry Pi 5", d: "ordinateur du module IA" },
      { f: "ai_hat_plus", t: "AI HAT+ (Hailo-8)", d: "accélérateur d'IA, 26 TOPS" },
      { f: "camera", t: "Caméra", d: "images pour l'IA" },
    ],
    notes: `Voici à quoi ressemblent les principaux composants. Pour l'énergie : la batterie lithium-polymère, le module de puissance, les variateurs et les moteurs sans balais. Pour le pilotage : le contrôleur de vol à STM32H743, le module GNSS avec son compas, le tube de Pitot, la radio longue portée et la radiocommande. Et pour la mission : le Raspberry Pi 5, sa carte d'accélération Hailo-8, et la caméra.
Ce sont des composants standards, faciles à trouver et à remplacer. Roger va vous présenter le module d'intelligence artificielle.`,
  },
  {
    type: "chaine", qui: "roger", duree: 70,
    titre: "Le module d'intelligence artificielle",
    etapes: [
      ["Caméra", "images horodatées"],
      ["Détection", "YOLOv8s sur Hailo-8"],
      ["Zone d'intérêt", "piste et abords"],
      ["Suivi", "un objet, une alerte"],
      ["Alerte", "avec image de preuve"],
      ["Station sol", "par la liaison sécurisée"],
    ],
    colonnes: [
      { titre: "Matériel", puces: [
        "Raspberry Pi 5",
        "AI HAT+ 26 TOPS (puce Hailo-8)",
        "Séparé du contrôleur de vol",
      ] },
      { titre: "Ce qu'il détecte", puces: [
        "Personnes",
        "Véhicules",
        "Débris et objets au sol",
      ] },
    ],
    images: [{ f: "raspberry_pi5", legende: "Raspberry Pi 5" }, { f: "ai_hat_plus", legende: "AI HAT+ (puce Hailo-8) monté sur le Pi" }],
    notes: `Merci Israel. Bonjour, je m'appelle KAINWANG Roger, je m'occupe de l'intelligence artificielle et des données.
Le module IA, c'est un Raspberry Pi 5 avec une carte AI HAT+ qui porte une puce Hailo-8 de 26 TOPS. Tout le calcul se fait à bord : aucune image ne part sur internet.
La caméra filme. Le détecteur YOLOv8s repère les personnes, les véhicules et les débris au sol. On ne garde que ce qui est dans la zone utile, la piste et ses abords. Un suivi relie les détections d'une image à l'autre pour qu'un objet ne déclenche qu'une seule alerte. Puis l'alerte part vers la station sol avec une photo de preuve.`,
  },
  {
    type: "deux_colonnes", qui: "roger", duree: 60,
    titre: "Données et fiabilité de l'IA",
    colonnes: [
      { titre: "Le modèle et ses données", puces: [
        "YOLOv8s pré-entraîné, adapté par fine-tuning",
        "FOD-A : plus de 30 000 débris de piste annotés",
        "Images prises avec notre caméra, à l'angle de vue du drone",
        "Scènes vides et pièges (ombres, marquages) contre les fausses alertes",
      ] },
      { titre: "Ce que l'IA fait, et ne fait pas", puces: [
        "Un objet inconnu est signalé « à vérifier », avec son image",
        "Sans liaison, les alertes sont gardées à bord puis envoyées",
        "Elle aide l'opérateur, la décision reste humaine",
        "Elle ne commande jamais le drone",
      ] },
    ],
    notes: `Pour le modèle, nous ne partons pas de zéro : nous prenons un YOLOv8s déjà entraîné et nous l'adaptons à notre mission, avec FOD-A, une base publique de plus de 30 000 débris de piste annotés, et des images prises avec notre caméra, vues d'en haut. Nous ajoutons des scènes vides avec des ombres et des marquages pour éviter les fausses alertes.
Si l'IA voit un objet qu'elle ne sait pas classer, elle le signale « à vérifier », avec l'image. Si la liaison est coupée, elle garde ses alertes. Et c'est toujours l'humain qui décide : l'IA ne commande jamais le drone. Angelo va vous montrer la station sol.`,
  },
  {
    type: "deux_colonnes", qui: "angelo", duree: 50,
    titre: "Station sol et back-end",
    colonnes: [
      { titre: "La station sol (Angelo)", puces: [
        "Flutter : version mobile et web",
        "Préparation de la mission et zone autorisée",
        "Télémétrie MAVLink en direct",
        "Alertes de l'IA avec image, vidéo enregistrée",
      ] },
      { titre: "Le back-end (Cédric)", puces: [
        "API REST et base MySQL",
        "Historique des vols, télémétrie et alertes",
        "Format d'alerte commun à toute l'équipe",
        "Journaux de vol signés",
      ] },
    ],
    hColonnes: 3.3,
    bas: "L'opérateur n'a pas à fixer la vidéo : le drone lui signale ce qu'il faut regarder.",
    notes: `Merci Roger. Au sol, nous développons la station en Flutter, avec une version mobile et une version web. L'opérateur prépare sa mission, définit la zone autorisée, suit la télémétrie en direct, et reçoit les alertes de l'IA avec leur image. La vidéo est enregistrée.
Toutes ces données sont archivées par le back-end de Cédric : une API REST et une base MySQL, avec l'historique des vols et des alertes, et des journaux de vol signés. Makafui va vous présenter les liaisons.`,
  },
  {
    type: "tableau", qui: "makafui", duree: 55,
    titre: "Trois liaisons indépendantes",
    entetes: ["Liaison", "Ce qu'elle transporte", "Portée visée"],
    colW: [4.0, 5.0, 3.033], rowH: 0.5, taille: 16,
    lignes: [
      ["Vidéo HD", "Image de la caméra et informations de vol", "10 à 15 km"],
      ["Radio longue portée chiffrée", "Télémétrie, ordres et alertes de l'IA", "30 à 50 km (théorique)"],
      ["Canal d'urgence ExpressLRS", "Retour au point de départ, coupure des moteurs", "Indépendant des autres"],
      ["Écartée : 4G", "Couverture incertaine ; satellite à l'essai en secours", ""],
    ],
    imageBas: [{ f: "radio_longue_portee", legende: "Radio de télémétrie longue portée (type RFD900)" }, { f: "radios_rc", legende: "Radiocommandes et récepteurs" }],
    notes: `Merci Angelo. Notre principe : ne jamais dépendre d'un seul lien. Nous avons trois liaisons séparées. Un lien vidéo HD pour voir ce que voit le drone. Une radio longue portée chiffrée pour la télémétrie, les ordres et les alertes de l'IA. Et un canal d'urgence indépendant, qui sert uniquement à faire revenir le drone ou à couper les moteurs.
La 4G est écartée car la couverture n'est pas garantie, et le satellite est à l'essai comme secours. Les antennes sont placées hors des zones en carbone, qui bloquent les ondes.`,
  },

  // ---------------------------------------------------------------- avantages, risques, réglementation, sécurité
  {
    type: "tableau", section: "Avantages et risques", qui: "israel", duree: 50,
    titre: "Les avantages",
    entetes: ["Avantage", "Ce que ça change"],
    colW: [4.2, 7.833], rowH: 0.62, taille: 16,
    lignes: [
      ["Décollage vertical", "Pas besoin de piste : il part de n'importe quelle zone dégagée"],
      ["Vol sur l'aile", "Grande autonomie (30 à 45 min visées) et grandes surfaces couvertes"],
      ["Moteurs basculants", "Les mêmes moteurs pour décoller et voler : moins de masse inutile"],
      ["IA à bord", "Alerte immédiate pendant le vol, sans internet ni cloud"],
      ["Liaison sécurisée", "Données chiffrées, ordres signés, résistance au brouillage"],
      ["Moins de risques humains", "Les agents ne parcourent plus la piste eux-mêmes"],
      ["Plateforme modulaire", "Aéroports, infrastructures, agriculture, cartographie, humanitaire"],
    ],
    notes: `[Israel] Pour résumer ce que notre drone apporte : il n'a pas besoin de piste, il vole longtemps grâce à son aile, et ses moteurs basculants servent aux deux phases de vol. L'IA à bord donne l'alerte pendant le vol, sans internet. La liaison est sécurisée. Les agents n'ont plus à parcourir la piste eux-mêmes. Et la même plateforme peut servir à d'autres missions.`,
  },
  {
    type: "tableau", qui: "israel", duo: "makafui", duree: 90,
    titre: "Les risques et nos réponses",
    entetes: ["Risque", "Notre réponse"],
    colW: [3.9, 8.133], rowH: 0.5, taille: 14,
    lignes: [
      ["Perte de la liaison radio", "Retour automatique au point de départ, puis atterrissage vertical"],
      ["Batterie faible ou défaillante", "Surveillance de la tension ; retour, puis atterrissage immédiat si critique"],
      ["Panne en vol stationnaire", "Phase verticale courte, à faible hauteur, au-dessus d'une zone dégagée"],
      ["Servo de basculement bloqué", "Servos à engrenages métal, contrôle à chaque check-list, essais progressifs"],
      ["Brouillage ou leurrage GPS", "Deux GPS comparés aux autres capteurs ; atterrissage sécurisé si doute"],
      ["Piratage, faux ordres", "Liaison chiffrée, messages signés, canal d'urgence indépendant"],
      ["Sortie de zone autorisée", "Géorepérage : demi-tour automatique"],
      ["Erreur de l'IA", "Objet incertain signalé « à vérifier » ; l'humain décide, l'IA ne pilote pas"],
      ["Météo (vent, pluie)", "Pas de vol hors des limites fixées après essais"],
    ],
    notes: `Nous avons aussi listé les risques, avec une réponse pour chacun.
Si la liaison radio est perdue, le drone rentre seul et atterrit à la verticale. Si la batterie devient faible, il rentre ; si elle est critique, il atterrit immédiatement. Le moment le plus délicat est le vol vertical : on le garde court, à faible hauteur. Les servos de basculement sont contrôlés à chaque check-list.
[Makafui] Contre le brouillage et le leurrage GPS, nous comparons deux GPS avec les autres capteurs. Contre le piratage, la liaison est chiffrée et les ordres sont signés. Le géorepérage empêche de sortir de la zone. Et si l'IA hésite, elle signale « à vérifier » : c'est l'humain qui décide.`,
  },
  {
    type: "deux_colonnes", section: "Réglementation et sécurité", qui: "cedric", duree: 70,
    titre: "La réglementation",
    colonnes: [
      { titre: "Le vol", taille: 16, puces: [
        "Autorisation de l'ANAC Togo avant tout vol",
        "Vol en vue directe du télépilote, sauf autorisation",
        "Hauteur et zone limitées, géorepérage activé",
        "Pas de vol au-dessus de la foule ni près d'un aérodrome sans accord",
        "Télépilote formé, check-lists avant et après vol",
      ] },
      { titre: "Les ondes et les données", taille: 16, puces: [
        "Fréquences radio autorisées par l'ARCEP",
        "Protection des données personnelles (loi togolaise de 2019)",
        "Pas de reconnaissance faciale, images d'alerte seulement",
        "Accès aux données réservé aux personnes autorisées",
        "Essais sur site uniquement avec l'accord de l'exploitant",
      ] },
    ],
    bas: "Nous ne volons qu'avec les autorisations nécessaires, et nous respectons le règlement du concours.",
    notes: `[Cédric] Côté réglementation, deux familles de règles.
Pour le vol : nous ne volons qu'avec l'autorisation de l'ANAC, en vue directe du télépilote sauf autorisation particulière, dans une zone et à une hauteur limitées que le géorepérage fait respecter. Pas de vol au-dessus de la foule ni près d'un aérodrome sans accord. Le télépilote est formé et suit des check-lists.
Pour les ondes et les données : nos fréquences doivent être autorisées par l'ARCEP. Comme le drone peut filmer des personnes, nous respectons la loi togolaise sur la protection des données : pas de reconnaissance faciale, on ne garde que les images d'alerte, et l'accès est réservé aux personnes autorisées.`,
  },
  {
    type: "deux_colonnes", qui: "makafui", duree: 65,
    titre: "La sécurité",
    colonnes: [
      { titre: "Sécurité du vol", taille: 16, puces: [
        "Contrôleur de vol séparé du module IA",
        "Retour automatique au point de départ (RTH)",
        "Fail-safe radio, batterie et GPS",
        "Coupure d'urgence des moteurs",
        "Géorepérage : zone et hauteur maximales",
        "Vérifications automatiques avant décollage",
      ] },
      { titre: "Cybersécurité", taille: 16, puces: [
        "Liaison chiffrée",
        "Messages MAVLink signés : faux ordres rejetés",
        "Clé secrète chargée au sol avant le vol",
        "Détection du brouillage",
        "Anti-leurrage GPS par comparaison des sources",
        "Journaux de vol signés : toute modification se voit",
      ] },
    ],
    bas: "En dernier recours, le canal d'urgence indépendant permet toujours de faire revenir le drone ou de couper les moteurs.",
    notes: `[Makafui] La sécurité se joue à deux niveaux.
La sécurité du vol : le contrôleur est séparé de l'IA ; en cas de perte de radio, de batterie faible ou de GPS dégradé, le drone applique automatiquement une procédure de secours ; le géorepérage limite la zone et la hauteur ; une coupure d'urgence reste toujours possible ; et avant le décollage, le drone vérifie lui-même que tout est prêt.
La cybersécurité : la liaison est chiffrée, chaque message est signé avec une clé chargée au sol, donc un faux ordre est rejeté. Nous détectons le brouillage, nous comparons les sources de position contre le leurrage GPS, et les journaux de vol sont signés.`,
  },

  // ---------------------------------------------------------------- applications et projet
  {
    type: "tableau", section: "Applications et projet", qui: "cedric", duree: 55,
    titre: "Domaines d'application",
    entetes: ["Secteur", "Utilisations", "Ce qu'on adapte"],
    colW: [3.3, 5.4, 3.333], rowH: 0.62, taille: 15,
    lignes: [
      ["Aviation civile", "Inspection de piste, débris (FOD), clôtures", "Caméra + IA de détection"],
      ["Agriculture et environnement", "Suivi des cultures, environnement, feux de brousse", "Caméra thermique ou multispectrale"],
      ["Infrastructures", "Lignes électriques, pylônes, ponts, port de Lomé", "Caméra zoom, IA de défauts"],
      ["Aide humanitaire", "Petits colis médicaux vers des zones enclavées", "Soute de largage (version adaptée)"],
      ["Cartographie", "Orthophotos, relevés topographiques", "Appareil photo de cartographie"],
    ],
    bas: "Le drone, la station sol et le back-end restent les mêmes ; on change la charge utile et le modèle d'IA.",
    notes: `[Cédric] Notre premier usage, c'est l'aéroport. Mais la même plateforme peut servir en agriculture et pour l'environnement, par exemple pour repérer des départs de feux de brousse, pour inspecter des lignes électriques, des ponts ou le port de Lomé, pour livrer de petits colis médicaux dans des zones enclavées avec une version adaptée, ou pour la cartographie. À chaque fois, on change seulement la charge utile et le modèle d'IA.`,
  },
  {
    type: "frise", qui: "cedric", duree: 35,
    titre: "Calendrier",
    etapes: [
      ["Août", "Candidature et cahier des charges", "fait"],
      ["Septembre", "Conception détaillée et dossier", "fait"],
      ["Octobre", "Prototypage et intégration", "ici"],
      ["Novembre", "Essais au sol, en vol et de sécurité", ""],
      ["Décembre 2026", "Finale et démonstration", ""],
    ],
    notes: `Côté calendrier, la candidature a été validée en août, la conception faite en septembre et le dossier déposé. Nous sommes en phase de prototypage et d'intégration. En novembre viendront les essais au sol, en vol et de sécurité, pour être prêts pour la finale en décembre. Je rends la parole à Israel.`,
  },
  {
    type: "tableau", qui: "israel", duree: 35,
    titre: "Budget prévisionnel",
    entetes: ["Poste", "Estimation (FCFA)"],
    colW: [8.0, 4.033], rowH: 0.5, taille: 15,
    lignes: [
      ["Cellule, moteurs, ESC, hélices", "200 000 à 350 000"],
      ["Contrôleur de vol, GPS, capteurs", "200 000 à 350 000"],
      ["Caméra et nacelle stabilisée", "120 000 à 300 000"],
      ["Batteries et alimentation", "80 000 à 150 000"],
      ["Liaison radio et télémétrie", "80 000 à 150 000"],
      ["Consommables et divers", "50 000 à 100 000"],
      ["Total (fiche projet)", "730 000 à 1 400 000"],
    ],
    bas: "À ajouter : le module IA (Raspberry Pi 5 + AI HAT+), 120 000 à 160 000 FCFA.",
    notes: `Merci Cédric. Notre budget est estimé entre 730 000 et 1 400 000 francs CFA pour le drone, avec en plus 120 000 à 160 000 francs pour le module d'intelligence artificielle. Nous avons choisi des composants courants, faciles à trouver et à remplacer.`,
  },
  {
    type: "fin", section: "Conclusion", qui: "israel", duree: 35,
    titre: "En résumé",
    puces: [
      "Il décolle partout, sans piste",
      "Il vole longtemps grâce à son aile",
      "Il analyse ses images à bord",
      "Il communique de façon sécurisée",
    ],
    image: "cao_iso",
    merci: "Merci pour votre attention",
    bas: "Merci à l'ANAC et aux organisateurs du CECFD 2026. Nous répondons à vos questions.",
    notes: `Pour résumer, la Sentinelle Aérienne décolle partout, vole longtemps grâce à son aile, analyse ses images à bord et communique de façon sécurisée. Ses risques sont identifiés et traités, et elle respecte le cadre réglementaire.
Merci à l'ANAC et aux organisateurs du CECFD. Merci pour votre attention, nous sommes prêts à répondre à vos questions.`,
  },
];

module.exports = { INTERVENANTS, DIAPOS };
