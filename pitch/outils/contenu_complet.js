// Présentation complète (17 diapos). Notes d'oral dans « notes ».
const INTERVENANTS = require("./intervenants");

const DIAPOS = [
  {
    type: "couverture", section: "Introduction", qui: "israel", duree: 40,
    titre: "Sentinelle Aérienne",
    ligne: "SkyVision Togo · CECFD 2026 · ANAC",
    sous: "Drone VTOL de surveillance des zones sensibles, avec intelligence artificielle embarquée et liaison sécurisée",
    image: "cao_iso",
    bas: "Thématique : Surveillance et sécurité",
    notes: `Bonjour Mesdames et Messieurs les membres du jury. Je m'appelle AWADE Constantin Israel, je suis le chef de l'équipe SkyVision Togo, et je m'occupe de la mécanique, de l'électronique et de la conception 3D.
Nous vous présentons la Sentinelle Aérienne : un drone qui décolle à la verticale, vole ensuite comme un avion, et analyse lui-même ses images pour repérer ce qui est anormal, en particulier sur les pistes d'aéroport.`,
  },
  {
    type: "tableau", qui: "israel", duree: 35,
    titre: "L'équipe et l'ordre de passage",
    entetes: ["", "Membre", "Pôle", "Partie présentée"],
    colW: [0.6, 4.0, 4.3, 3.133], rowH: 0.62, taille: 15, premiereGras: false,
    lignes: [
      ["1", "AWADE Constantin Israel", "Chef d'équipe, mécanique, électronique, 3D", "Besoin, conception, budget"],
      ["2", "LOGO ADANTO Angelo", "Logiciel embarqué et station sol", "Vol, transition, station sol"],
      ["3", "de MEDEIROS Makafui Komlan Léopoldo", "Réseaux, télémétrie et sécurité", "Liaisons et sécurité"],
      ["4", "KAINWANG Roger", "Intelligence artificielle et données", "Module IA"],
      ["5", "KODJOVI Eli Cédric Ankou", "Back-end, programme de vol, documentation", "Supervision, conformité, calendrier"],
    ],
    notes: `Nous sommes cinq, et chacun est responsable d'une partie du système.
Je vais vous présenter le besoin et le drone. Angelo parlera du vol et de la station sol, Makafui des liaisons radio et de la sécurité, Roger de l'intelligence artificielle, et Cédric de la supervision, de la conformité et du calendrier. Je reviendrai à la fin pour le budget et la conclusion.`,
  },
  {
    type: "tableau", section: "Le drone", qui: "israel", duree: 45,
    titre: "Le besoin",
    intro: "Surveiller une piste, une frontière ou un site sensible, c'est couvrir de grandes surfaces, souvent sans piste disponible.",
    entetes: ["Solution actuelle", "Point fort", "Limite"],
    colW: [3.4, 4.2, 4.433], rowH: 0.7, taille: 16,
    lignes: [
      ["Inspection en véhicule", "Simple, sans équipement spécial", "Lente, bloque la piste, difficile la nuit"],
      ["Drone multirotor", "Décolle n'importe où", "Vole peu de temps, en général 20 à 30 min"],
      ["Drone avion", "Vole longtemps et vite", "A besoin d'une piste ou d'une catapulte"],
    ],
    bas: "Et dans la plupart des cas, les images sont analysées après le vol, quand il est déjà tard.",
    notes: `Partons du besoin. Sur une piste, un débris comme un boulon ou un morceau de pneu peut être aspiré par un réacteur. Il faut aussi surveiller les abords et repérer les intrusions.
Aujourd'hui, l'inspection se fait surtout en véhicule : c'est lent, la piste est bloquée, et c'est difficile la nuit. Les drones existants ont chacun leur défaut : le multirotor décolle partout mais vole peu de temps, l'avion vole longtemps mais il lui faut une piste.
Et souvent, les images ne sont regardées qu'après le vol.`,
  },
  {
    type: "texte_image", qui: "israel", duree: 45,
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
    notes: `Notre réponse, c'est un VTOL à rotors basculants. Il décolle à la verticale comme un multirotor, depuis n'importe quel terrain dégagé. Ensuite, ses deux moteurs avant basculent vers l'avant et il vole comme un avion : c'est l'aile qui le porte, ce qui consomme beaucoup moins d'énergie.
À cette plateforme, nous ajoutons deux choses qui répondent directement au thème surveillance et sécurité : une intelligence artificielle qui analyse les images à bord, et une liaison radio sécurisée.`,
  },
  {
    type: "tableau", qui: "israel", duree: 45,
    titre: "Caractéristiques principales",
    entetes: ["Élément", "Choix retenu"],
    colW: [3.0, 4.6], rowH: 0.5, taille: 15,
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
    image: { f: "cao_dessus", legende: "Vue de dessus (SolidWorks)" },
    notes: `Voici les grandes lignes du drone. C'est une configuration à trois moteurs : deux moteurs avant qui basculent, et un moteur arrière qui ne sert qu'au vol vertical. L'empennage est en V.
Nous visons 30 à 45 minutes d'autonomie. Le contrôleur de vol est une carte STM32H743 sous ArduPilot, et le module IA un Raspberry Pi 5 avec un accélérateur Hailo-8. La charge utile, c'est une caméra stabilisée jour et nuit, et le drone communique par trois liaisons séparées.`,
  },
  {
    type: "texte_image", qui: "israel", duree: 50,
    titre: "Structure et conception",
    blocs: [
      { h: 4.8, puces: [
        "Modélisation complète sous SolidWorks",
        "Fuselage : batterie, électronique et module IA",
        "Nacelles d'aile avec servomoteur de basculement",
        "Moteur arrière logé dans le fuselage",
        "Empennage en V : deux gouvernes au lieu de trois",
        "Mât GNSS sur le dos, tube de Pitot dans le nez",
        "Antennes placées hors des zones en carbone",
      ] },
    ],
    images: [{ f: "cao_profil", legende: "Vue de profil (SolidWorks)" }, { f: "cao_face", legende: "Vue de face (SolidWorks)" }],
    notes: `Côté structure, tout a été modélisé sous SolidWorks.
Le fuselage reçoit la batterie, l'électronique et le module IA. Les deux moteurs avant sont montés dans des nacelles sur l'aile, avec un servomoteur qui les fait pivoter. Le moteur arrière est logé dans le fuselage, sous la queue.
L'empennage en V remplace la dérive et la profondeur classiques : deux surfaces au lieu de trois, donc moins de servos et moins de masse. Le GPS est sur un mât au-dessus du fuselage, pour l'éloigner des perturbations, et un tube de Pitot dans le nez mesure la vitesse air. Enfin, on a fait attention à placer les antennes hors des zones en carbone, qui bloquent les ondes.
Angelo va maintenant vous expliquer comment le drone vole.`,
  },
  {
    type: "tableau", section: "Vol et station sol", qui: "angelo", duree: 60,
    titre: "Le vol : du décollage vertical à la croisière",
    entetes: ["Phase", "Moteurs avant", "Moteur arrière", "Ce qui porte le drone"],
    colW: [2.6, 3.4, 2.6, 3.433], rowH: 0.52, taille: 16,
    lignes: [
      ["Décollage", "Vers le haut", "En marche", "Les trois moteurs"],
      ["Transition", "Basculent progressivement", "En marche", "Les moteurs, puis l'aile"],
      ["Croisière", "Vers l'avant, ils tirent", "Arrêté", "L'aile"],
      ["Atterrissage", "Reviennent vers le haut", "En marche", "Les trois moteurs"],
    ],
    imageBas: { f: "cao_profil", legende: "Moteur avant basculant à gauche, moteur arrière sous la queue (SolidWorks)" },
    notes: `Bonjour, je m'appelle LOGO ADANTO Angelo, je m'occupe du logiciel embarqué et de la station sol.
Le vol se fait en quatre phases. Au décollage, les deux moteurs avant sont tournés vers le haut et, avec le moteur arrière, ils soulèvent le drone. Pendant la transition, les moteurs avant basculent petit à petit vers l'avant : le drone accélère et l'aile commence à porter. Une fois la vitesse suffisante, le moteur arrière s'arrête et on est en croisière : les deux moteurs avant tirent le drone, et l'aile le porte. À l'atterrissage, on fait l'inverse.
C'est ArduPilot qui gère tout ça automatiquement, à partir de la vitesse air mesurée par le tube de Pitot.`,
  },
  {
    type: "deux_colonnes", qui: "angelo", duree: 45,
    titre: "La station sol",
    colonnes: [
      { titre: "Avant et pendant le vol", puces: [
        "Préparation de la mission sur la carte",
        "Zone autorisée : le drone ne peut pas en sortir",
        "Télémétrie MAVLink en direct",
        "Enregistrement de la vidéo",
      ] },
      { titre: "Les alertes de l'IA", puces: [
        "Classe de l'objet, heure et position dans l'image",
        "Image de preuve",
        "Historique conservé par le back-end",
      ] },
    ],
    hColonnes: 2.6,
    bas: "Développée en Flutter : une version mobile et une version web avec le même code.",
    notes: `Au sol, nous développons la station en Flutter, ce qui donne une version mobile et une version web avec le même code.
Avant le vol, l'opérateur prépare sa mission sur la carte et définit la zone autorisée : si le drone en sort, il fait demi-tour automatiquement. Pendant le vol, il suit la télémétrie en direct et la vidéo est enregistrée.
Surtout, il reçoit les alertes de l'IA avec leur image. Il n'a pas besoin de fixer la vidéo en permanence : c'est le drone qui lui signale ce qu'il faut regarder. Je laisse la parole à Makafui pour les liaisons.`,
  },
  {
    type: "tableau", section: "Liaisons et sécurité", qui: "makafui", duree: 55,
    titre: "Trois liaisons indépendantes",
    entetes: ["Liaison", "Ce qu'elle transporte", "Portée visée"],
    colW: [4.0, 5.0, 3.033], rowH: 0.65, taille: 16,
    lignes: [
      ["Vidéo HD", "Image de la caméra et informations de vol", "10 à 15 km"],
      ["Radio longue portée chiffrée", "Télémétrie, ordres et alertes de l'IA", "30 à 50 km (théorique)"],
      ["Canal d'urgence ExpressLRS", "Retour au point de départ, coupure des moteurs", "Indépendant des autres"],
    ],
    bas: "Écartés : la 4G (couverture incertaine) ; la liaison satellite est à l'essai comme secours.",
    imageBas: { f: "cao_face", legende: "Mât GNSS sur le dos, antennes hors des zones en carbone (SolidWorks)" },
    notes: `Bonjour, je m'appelle de MEDEIROS Makafui Komlan Léopoldo, je m'occupe des réseaux, de la télémétrie et de la sécurité.
Notre principe : ne jamais dépendre d'un seul lien. Nous avons trois liaisons séparées. Un lien vidéo HD pour voir ce que voit le drone. Une radio longue portée chiffrée, qui transporte la télémétrie, les ordres et les alertes de l'IA. Et un canal d'urgence indépendant, qui sert uniquement à faire revenir le drone ou à couper les moteurs.
Nous avons écarté la 4G, parce que la couverture n'est pas garantie dans les zones visées. Le satellite, lui, est à l'essai comme liaison de secours.`,
  },
  {
    type: "tableau", qui: "makafui", duree: 55,
    titre: "Sécurité des communications",
    entetes: ["Menace", "Notre réponse"],
    colW: [3.6, 8.433], rowH: 0.62, taille: 16,
    lignes: [
      ["Écoute des données", "Liaison chiffrée"],
      ["Faux ordres", "Messages MAVLink signés : un ordre sans la bonne clé est ignoré"],
      ["Brouillage", "Surveillance de la qualité des liens, bascule sur un autre lien"],
      ["Leurrage GPS", "Deux récepteurs comparés aux autres capteurs ; la source incohérente est écartée"],
      ["Perte de toutes les liaisons", "Retour automatique au point de départ, puis atterrissage vertical"],
      ["Dernier recours", "Coupure des moteurs par le canal d'urgence"],
    ],
    notes: `Pour la sécurité, nous avons pensé à chaque menace. Les données sont chiffrées, donc on ne peut pas les lire. Chaque message MAVLink est signé : si quelqu'un essaie d'envoyer un ordre sans la bonne clé, le drone l'ignore.
Contre le brouillage, on surveille la qualité des liens et on bascule sur un autre. Contre le leurrage GPS, on utilise deux récepteurs et on compare leur position avec les autres capteurs du drone : si une source ne colle pas, elle est écartée.
Et si tout est perdu, le drone rentre seul et atterrit à la verticale. En dernier recours, on peut couper les moteurs. Roger va vous présenter l'intelligence artificielle.`,
  },
  {
    type: "chaine", section: "Intelligence artificielle", qui: "roger", duree: 70,
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
    notes: `Bonjour, je m'appelle KAINWANG Roger, je m'occupe de l'intelligence artificielle et des données.
Le module IA, c'est un Raspberry Pi 5 avec une carte AI HAT+ qui porte une puce Hailo-8 de 26 TOPS. Il est séparé du contrôleur de vol, donc il ne peut pas mettre le vol en danger. Et tout le calcul se fait à bord : aucune image ne part sur internet.
La chaîne est simple. La caméra fournit les images. Le détecteur YOLOv8s repère les personnes, les véhicules et les débris au sol. On ne garde que ce qui est dans la zone utile, la piste et ses abords. Un suivi relie les détections d'une image à l'autre pour qu'un objet ne déclenche qu'une seule alerte. Puis l'alerte part vers la station sol avec une image de preuve.`,
  },
  {
    type: "deux_colonnes", qui: "roger", duree: 60,
    titre: "Données et fiabilité",
    colonnes: [
      { titre: "Le modèle et ses données", puces: [
        "YOLOv8s pré-entraîné, adapté par fine-tuning",
        "FOD-A : plus de 30 000 débris de piste annotés",
        "Images prises avec notre caméra, à l'angle de vue du drone",
        "Scènes vides et pièges (ombres, marquages) pour limiter les fausses alertes",
      ] },
      { titre: "Ce que l'IA fait, et ne fait pas", puces: [
        "Un objet inconnu est signalé « à vérifier », avec son image",
        "Sans liaison, les alertes sont gardées à bord puis envoyées",
        "Elle aide l'opérateur, la décision reste humaine",
        "Elle ne commande jamais le drone",
      ] },
    ],
    notes: `Pour le modèle, nous ne partons pas de zéro. Nous prenons un YOLOv8s déjà entraîné sur un grand nombre d'images, et nous l'adaptons à notre mission. Pour ça, nous utilisons FOD-A, une base publique de plus de 30 000 débris de piste annotés, et des images prises avec notre caméra, pour coller à l'angle de vue du drone. Nous ajoutons aussi des scènes vides, avec des ombres et des marquages, pour éviter les fausses alertes.
Si l'IA voit quelque chose qu'elle ne sait pas classer, elle ne devine pas : elle le signale comme « à vérifier », avec l'image. Si la liaison est coupée, elle continue à travailler et garde ses alertes à bord.
Enfin, c'est un outil d'aide : la décision reste à l'opérateur, et l'IA ne commande jamais le drone. Cédric va vous parler de la supervision.`,
  },
  {
    type: "chaine", section: "Supervision et conformité", qui: "cedric", duree: 50,
    titre: "Supervision et documentation",
    etapes: [
      ["Drone", "journal à bord"],
      ["Station sol", "affichage et contrôle"],
      ["Back-end", "API REST, base MySQL"],
      ["Archives", "journaux de vol signés"],
    ],
    colonnes: [
      { titre: "Le back-end", puces: [
        "Enregistre les vols, la télémétrie et les alertes",
        "Format d'alerte commun à toute l'équipe",
        "Journaux signés : toute modification se voit",
      ] },
      { titre: "Le programme de vol et le dossier", puces: [
        "Plans de mission et check-lists avant et après vol",
        "Procédures d'urgence",
        "Dossier de conception : schémas, dimensionnement, sécurité",
      ] },
    ],
    notes: `Bonjour, je m'appelle KODJOVI Eli Cédric Ankou, je m'occupe du back-end, du programme de vol et de la documentation.
Mon rôle, c'est que rien ne se perde. Le back-end enregistre chaque vol : la télémétrie, les alertes de l'IA avec leur image, et les journaux de vol. Toute l'équipe utilise le même format d'alerte. Les journaux sont signés : si quelqu'un modifie une ligne après coup, on le voit.
Je prépare aussi le programme de vol : les plans de mission, les check-lists avant et après le vol, et les procédures d'urgence. Et je tiens à jour le dossier de conception.`,
  },
  {
    type: "tableau", qui: "cedric", duree: 40,
    titre: "Conformité aux exigences du concours",
    entetes: ["Exigence", "Notre solution"],
    colW: [5.0, 7.033], rowH: 0.62, taille: 16,
    lignes: [
      ["Navigation GPS et retour au point de départ", "GNSS relié au contrôleur de vol, retour automatique"],
      ["Coupure d'urgence", "Coupure des moteurs et mode de descente sécurisée"],
      ["Lien sécurisé drone / station", "Liaison chiffrée et messages signés"],
      ["Autonomie minimale", "30 à 45 minutes visées"],
      ["Charge utile adaptée", "Caméra jour/nuit stabilisée et module IA"],
      ["Documentation technique", "Dossier de conception complet"],
    ],
    notes: `Voici comment nous répondons aux exigences du concours. La navigation GPS avec retour automatique est gérée par le contrôleur de vol. La coupure d'urgence est prévue, avec une descente sécurisée. Le lien est chiffré et les messages sont signés. Nous visons 30 à 45 minutes d'autonomie. La charge utile, c'est la caméra jour et nuit et le module IA. Et la documentation, c'est le dossier de conception.`,
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
    notes: `Côté calendrier, la candidature a été validée en août, la conception détaillée faite en septembre, et le dossier déposé fin septembre.
Nous sommes maintenant dans la phase de prototypage et d'intégration. En novembre viendront les essais au sol, en vol et de sécurité, pour être prêts pour la finale en décembre. Je rends la parole à Israel.`,
  },
  {
    type: "tableau", section: "Conclusion", qui: "israel", duree: 35,
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
    notes: `Un mot sur le budget. Notre estimation se situe entre 730 000 et 1 400 000 francs CFA pour le drone, avec en plus 120 000 à 160 000 francs pour le module d'intelligence artificielle. Nous avons choisi des composants courants, qu'on peut trouver et remplacer facilement.`,
  },
  {
    type: "fin", qui: "israel", duree: 35,
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
    notes: `Pour résumer, la Sentinelle Aérienne décolle partout, vole longtemps grâce à son aile, analyse ses images à bord et communique de façon sécurisée. Nous l'avons pensée pour la sécurité de nos aéroports et de nos sites sensibles, et elle peut ensuite servir à la cartographie ou à l'aide humanitaire.
Merci à l'ANAC et aux organisateurs du CECFD. Merci pour votre attention, nous sommes prêts à répondre à vos questions.`,
  },
];

module.exports = { INTERVENANTS, DIAPOS };
