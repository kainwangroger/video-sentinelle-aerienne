// Présentation « Avantages, risques, réglementation et sécurité » (7 diapos).
const INTERVENANTS = require("./intervenants");

const DIAPOS = [
  {
    type: "couverture", section: "Introduction", qui: "israel", duree: 30,
    titre: "Sentinelle Aérienne",
    ligne: "SkyVision Togo · CECFD 2026 · ANAC",
    sous: "Avantages, risques, réglementation et sécurité",
    image: "cao_iso",
    bas: "Drone VTOL de surveillance avec intelligence artificielle embarquée",
    notes: `Bonjour. Dans cette partie, nous vous présentons ce que notre drone apporte, les risques que nous avons identifiés, le cadre réglementaire que nous respectons, et les mesures de sécurité prévues.`,
  },
  {
    type: "tableau", section: "Avantages", qui: "israel", duree: 60,
    titre: "Les avantages",
    entetes: ["Avantage", "Ce que ça change"],
    colW: [4.2, 7.833], rowH: 0.62, taille: 16,
    lignes: [
      ["Décollage vertical", "Pas besoin de piste : il part de n'importe quelle zone dégagée"],
      ["Vol sur l'aile", "Grande autonomie (30 à 45 min visées) et grandes surfaces couvertes"],
      ["IA à bord", "Alerte immédiate pendant le vol, sans internet ni cloud"],
      ["Liaison sécurisée", "Données chiffrées, ordres signés, résistance au brouillage"],
      ["Moins de risques humains", "Les agents ne parcourent plus la piste à pied ou en véhicule"],
      ["Plateforme modulaire", "Aéroports, infrastructures, agriculture, cartographie, humanitaire"],
    ],
    notes: `Notre drone décolle à la verticale, donc il n'a pas besoin de piste. En croisière, c'est l'aile qui le porte : il vole longtemps et couvre de grandes surfaces.
L'IA à bord donne l'alerte pendant le vol, sans internet. La liaison est sécurisée. Les agents n'ont plus à parcourir la piste eux-mêmes. Et la même plateforme peut servir à d'autres missions en changeant la charge utile.`,
  },
  {
    type: "tableau", section: "Risques", qui: "israel", duo: "makafui", duree: 90,
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
    notes: `Nous avons listé les risques principaux, et pour chacun une réponse.
Si la liaison radio est perdue, le drone rentre seul au point de départ et atterrit à la verticale. Si la batterie devient faible, il rentre ; si elle est critique, il atterrit immédiatement.
Le moment le plus délicat, c'est le vol vertical : on le garde court, à faible hauteur, au-dessus d'une zone dégagée. Les servos qui font basculer les moteurs sont contrôlés à chaque check-list.
[Makafui] Côté radio, contre le brouillage et le leurrage GPS, nous comparons deux GPS avec les autres capteurs. Contre le piratage, la liaison est chiffrée et les ordres sont signés. Le géorepérage empêche de sortir de la zone autorisée.
Enfin, l'IA peut se tromper : un objet incertain est signalé « à vérifier », et c'est toujours l'humain qui décide.`,
  },
  {
    type: "deux_colonnes", section: "Réglementation", qui: "cedric", duree: 75,
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
    notes: `Côté réglementation, nous respectons deux grandes familles de règles.
Pour le vol : nous ne volons qu'avec l'autorisation de l'ANAC, en vue directe du télépilote sauf autorisation particulière, dans une zone et à une hauteur limitées, que le géorepérage fait respecter. Pas de vol au-dessus de la foule ni près d'un aérodrome sans accord. Le télépilote est formé et suit des check-lists.
Pour les ondes et les données : nos fréquences radio doivent être autorisées par l'ARCEP. Comme le drone peut filmer des personnes, nous respectons la loi togolaise sur la protection des données personnelles : pas de reconnaissance faciale, on ne garde que les images d'alerte, et l'accès est réservé aux personnes autorisées.
Enfin, les essais sur un vrai site se font uniquement avec l'accord de l'exploitant.`,
  },
  {
    type: "deux_colonnes", section: "Sécurité", qui: "makafui", duree: 75,
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
    notes: `Bonjour, je m'appelle de MEDEIROS Makafui. La sécurité se joue à deux niveaux.
D'abord la sécurité du vol. Le contrôleur de vol est séparé du module IA, donc une panne de l'IA ne touche pas le vol. En cas de perte de radio, de batterie faible ou de GPS dégradé, le drone applique automatiquement une procédure de secours : retour au point de départ ou atterrissage. Le géorepérage limite la zone et la hauteur, et une coupure d'urgence reste toujours possible. Avant le décollage, le drone vérifie lui-même que tout est prêt.
Ensuite la cybersécurité. La liaison est chiffrée, et chaque message est signé avec une clé secrète chargée au sol : un faux ordre est rejeté. Nous détectons le brouillage, nous comparons les sources de position contre le leurrage GPS, et les journaux de vol sont signés pour qu'on ne puisse pas les modifier.`,
  },
  {
    type: "fin", section: "Conclusion", qui: "israel", duree: 35,
    titre: "En résumé",
    puces: [
      "Un drone utile : rapide, autonome, sans piste",
      "Des risques identifiés, chacun avec une réponse",
      "Un cadre respecté : ANAC, ARCEP, données personnelles",
      "Une sécurité pensée dès la conception",
    ],
    image: "cao_iso",
    merci: "Merci pour votre attention",
    bas: "Nous sommes prêts à répondre à vos questions.",
    notes: `Pour résumer : notre drone est utile, il est rapide, autonome et n'a pas besoin de piste. Nous avons identifié ses risques et prévu une réponse pour chacun. Nous respectons le cadre de l'ANAC, de l'ARCEP et la protection des données. Et la sécurité est pensée dès la conception. Merci, nous sommes prêts pour vos questions.`,
  },
];

module.exports = { INTERVENANTS, DIAPOS };
