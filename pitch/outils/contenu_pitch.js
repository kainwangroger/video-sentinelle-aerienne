// Contenu du pitch « Sentinelle Aérienne » : intervenants, diapos et script oral.
// Utilisé par generer_pitch.js (PowerPoint + script_oral.md).

const INTERVENANTS = {
  israel: { nom: "AWADE Constantin Israel", court: "Israel", role: "Chef d'équipe · Mécanique, structure, intégration", puce: "Chef d'équipe" },
  angelo: { nom: "LOGO ADANTO Angelo", court: "Angelo", role: "Logiciel embarqué · Station de contrôle au sol", puce: "Logiciel et station sol" },
  makafui: { nom: "de MEDEIROS Makafui Komlan Léopoldo", court: "Makafui", role: "Liaisons radio · Télémétrie · Cybersécurité", puce: "Réseau et sécurité" },
  roger: { nom: "KAINWANG Roger", court: "Roger", role: "Données · Vision par ordinateur · IA embarquée", puce: "IA embarquée" },
  cedric: { nom: "KODJOVI Eli Cédric Ankou", court: "Cédric", role: "Embarqué · Back-end de supervision · Documentation", puce: "Back-end et documentation" },
};

const ORDRE = ["israel", "angelo", "makafui", "roger", "cedric"];

// Durée indicative de chaque diapo (secondes), pour le minutage.
const DIAPOS = [
  {
    id: "titre", qui: "israel", duree: 40,
    script: `Bonjour Mesdames et Messieurs les membres du jury.
Je m'appelle AWADE Constantin Israel, je suis le chef de l'équipe SkyVision Togo. Je m'occupe de la conception mécanique, de la structure du drone, de l'intégration électronique et du contrôle qualité.
Nous sommes cinq passionnés de drones résidant au Togo, et nous avons le plaisir de vous présenter notre projet pour le CECFD 2026 : la Sentinelle Aérienne, un drone hybride à décollage vertical, dédié à la surveillance et à la sécurisation des zones sensibles.`,
  },
  {
    id: "equipe", qui: "israel", duree: 35,
    script: `Avant d'entrer dans le détail, voici notre équipe et l'ordre dans lequel nous allons intervenir.
Je vais vous présenter le besoin et le drone lui-même. Angelo vous parlera ensuite du logiciel embarqué et de la station au sol. Makafui présentera les liaisons radio et la cybersécurité. Roger vous montrera l'intelligence artificielle embarquée. Enfin, Cédric présentera la supervision, la documentation, notre conformité et notre calendrier.
Chaque membre est responsable d'un lot, mais tout converge vers un seul système.`,
  },
  {
    id: "probleme", qui: "israel", duree: 45,
    script: `Partons du besoin. Surveiller un aéroport, une frontière ou un site industriel, c'est couvrir de grandes surfaces, souvent loin de toute piste et sans connexion fiable.
Aujourd'hui, on a deux familles de drones, et chacune a un défaut. Le multirotor décolle n'importe où, mais il consomme énormément pour rester en l'air : 20 à 30 minutes en général. L'avion à voilure fixe vole longtemps et vite, mais il lui faut une piste ou une catapulte.
Et dans les deux cas, les images sont souvent analysées après le vol : quand on découvre l'anomalie, il est déjà trop tard.`,
  },
  {
    id: "solution", qui: "israel", duree: 45,
    script: `Notre réponse, c'est la Sentinelle Aérienne SA-1 : un drone hybride VTOL, de type « quadplane ».
Quatre moteurs verticaux le font décoller et atterrir comme un hélicoptère, depuis n'importe quel terrain, même confiné. Une fois en l'air, il bascule en vol horizontal : c'est l'aile qui le porte, et un moteur propulsif à l'arrière le fait avancer. Il couvre alors de grandes zones en économisant son énergie.
Et nous ajoutons deux innovations qui sont au cœur de la thématique Surveillance et Sécurité : une intelligence artificielle qui analyse les images à bord, en temps réel, et une liaison sécurisée dès la conception, chiffrée, authentifiée et résistante au brouillage.`,
  },
  {
    id: "identite", qui: "israel", duree: 45,
    script: `Voici la carte d'identité du SA-1, issue de notre dimensionnement.
Deux mètres d'envergure, 6,4 kilos au décollage, marge comprise. Une batterie lithium-polymère 6S de 16 000 milliampères-heure, soit 355 wattheures.
En stationnaire, le drone consomme environ 1 000 watts ; en croisière, moins de 300. C'est tout l'intérêt de l'hybride. Le calcul donne environ 50 minutes de vol théorique ; nous annonçons volontairement 30 à 45 minutes, pour garder une marge face au vent, à la chaleur et au vieillissement de la batterie.
Croisière à 68 kilomètres-heure. Seuls les essais en vol feront foi, et ils sont prévus.`,
  },
  {
    id: "structure", qui: "israel", duree: 50,
    script: `Côté structure, la cellule est en fibre de carbone et composite, modélisée sous SolidWorks.
On a un fuselage central qui reçoit la batterie, l'avionique et le module IA ; une aile en trois parties, démontable pour le transport ; deux poutres en carbone qui portent les moteurs verticaux et un empennage en H.
Les zones où passent les antennes sont en fibre de verre, car le carbone bloque les ondes radio.
Ici, vous voyez la vue éclatée : chaque pièce a été dimensionnée, pesée et placée pour que le centre de gravité tombe au bon endroit. Le bilan de masse complet est dans notre dossier technique.
Je passe maintenant la parole à Angelo pour le cerveau du drone.`,
  },
  {
    id: "avionique", qui: "angelo", duree: 55,
    script: `Merci Israel. Bonjour à tous, je m'appelle LOGO ADANTO Angelo. Dans l'équipe, je suis responsable du développement logiciel embarqué et de l'interface de la station de contrôle au sol.
Le cerveau du SA-1, c'est un contrôleur de vol sous ArduPilot, en mode QuadPlane. Il fusionne en permanence les capteurs : centrale inertielle, baromètre, compas, GPS, vitesse air et télémètre laser.
Le moment critique d'un VTOL, c'est la transition. Le drone décolle à la verticale, puis le moteur de croisière accélère. Tant que l'aile ne porte pas assez, les moteurs verticaux continuent d'aider. Quand la vitesse air dépasse le seuil de sécurité, environ 15 mètres par seconde, les moteurs verticaux s'arrêtent et l'aile prend le relais. À l'atterrissage, c'est l'inverse.
Tout cela est automatique et paramétré : le fichier de paramètres est déjà prêt.`,
  },
  {
    id: "station", qui: "angelo", duree: 45,
    script: `Au sol, l'opérateur dispose d'une station de contrôle.
Avant le vol, il dessine la mission sur la carte : points de passage, altitude, zone autorisée, point d'atterrissage.
Pendant le vol, il suit la télémétrie : position, vitesse, batterie, état des liaisons.
Et surtout, il reçoit les alertes de l'IA en direct : la classe de l'objet, l'heure, la zone, et une image de preuve. L'opérateur n'a pas à regarder la vidéo en continu : c'est le drone qui lui signale ce qui mérite son attention.
Je laisse la parole à Makafui, qui va vous expliquer comment toutes ces données voyagent en sécurité.`,
  },
  {
    id: "liaisons", qui: "makafui", duree: 55,
    script: `Merci Angelo. Bonjour, je suis de MEDEIROS Makafui Komlan Léopoldo. Je suis responsable des liaisons radio, de la télémétrie, de la sécurisation des communications et de l'architecture réseau.
Notre principe : ne jamais dépendre d'un seul lien. Nous avons trois liaisons indépendantes.
Un lien vidéo HD, pour voir ce que voit le drone, avec les informations de vol, sur 10 à 15 kilomètres.
Une radio longue portée, chiffrée, pour les messages et les ordres, sans vidéo : c'est elle qui porte la télémétrie et les alertes.
Et un canal d'urgence totalement indépendant, de type ExpressLRS, qui sert uniquement à reprendre la main : retour au point de départ ou coupure des moteurs.
Nous avons écarté le satellite et la 4G : trop chers, ou pas disponibles partout dans les zones visées.`,
  },
  {
    id: "securite", qui: "makafui", duree: 50,
    script: `La sécurité, c'est notre deuxième innovation, et elle est intégrée dès la conception.
Toutes les données sont chiffrées, et chaque message MAVLink est signé : un ordre qui ne porte pas la bonne signature est rejeté par le drone.
Contre le brouillage, nous surveillons la qualité des liaisons et nous basculons sur un autre lien si nécessaire.
Contre le leurrage GPS, nous utilisons deux récepteurs et nous comparons leurs positions avec la centrale inertielle : si une source ment, elle est écartée.
Et si tout tombe, le drone rentre seul au point de départ. En dernier recours, la coupure d'urgence arrête les moteurs.
Je passe la parole à Roger pour l'intelligence artificielle.`,
  },
  {
    id: "ia", qui: "roger", duree: 60,
    script: `Merci Makafui. Bonjour à tous, je m'appelle KAINWANG Roger. Dans l'équipe, je suis responsable du traitement des données, de la vision par ordinateur et de la détection d'anomalies par intelligence artificielle.
Notre IA tourne à bord, sur un Raspberry Pi 5 équipé d'un accélérateur AI HAT+ de 26 TOPS. Aucune image n'est envoyée vers un cloud.
La chaîne est simple. La caméra fournit des images horodatées. Un détecteur YOLOv8s, affiné sur nos données, repère trois familles : les personnes, les véhicules et les objets ou débris au sol. On ne garde que ce qui est dans la zone d'intérêt, par exemple la piste et ses abords. Un suivi relie les détections d'une image à l'autre, pour qu'un même objet ne génère qu'une seule alerte. Puis on crée l'alerte avec son image de preuve, on l'enregistre à bord et on l'envoie à la station.
Et si la liaison est coupée, l'IA continue : les alertes sont stockées et envoyées dès que la liaison revient.`,
  },
  {
    id: "ia_donnees", qui: "roger", duree: 50,
    script: `Quelques points sur la méthode.
Pour les données, nous partons de FOD-A, une base publique de plus de 30 000 objets de piste annotés, complétée par nos propres images filmées avec la caméra du drone. Le modèle est entraîné sur ordinateur, puis compilé pour l'accélérateur.
Pour les objets inconnus, nous sommes honnêtes : un détecteur ne reconnaît que ce qu'il a appris. Donc tout candidat crédible mais sans classe fiable est signalé « à vérifier », avec son image.
Et l'IA reste une aide à l'inspection : elle ne certifie pas qu'une piste est libre, et elle ne pilote jamais le drone. Aucun taux de précision ne sera annoncé avant d'avoir été mesuré.
Le code, les outils et le protocole de test sont déjà dans notre dépôt. Je laisse la parole à Cédric.`,
  },
  {
    id: "supervision", qui: "cedric", duree: 50,
    script: `Merci Roger. Bonjour, je m'appelle KODJOVI Eli Cédric Ankou. Je travaille sur le développement embarqué, le back-end de supervision et la documentation du projet.
Mon rôle, c'est que rien ne se perde. Chaque alerte de l'IA suit un format commun, décrit dans un schéma : classe, score, heure, zone, image de preuve. Le back-end les reçoit, les archive avec la télémétrie, et conserve les journaux de vol, qui sont signés pour garantir qu'ils n'ont pas été modifiés.
Côté documentation, le dossier est déjà fourni : une fiche technique complète qui explique chaque composant, un guide de conception et d'assemblage, les calculs de dimensionnement, les paramètres ArduPilot, les check-lists avant vol, après vol et d'urgence, et des vidéos explicatives.`,
  },
  {
    id: "conformite", qui: "cedric", duree: 40,
    script: `Voici comment nous répondons aux exigences minimales du concours.
La navigation GPS avec retour automatique au point de départ : c'est fait par le contrôleur de vol.
La coupure d'urgence : un interrupteur de coupure moteurs et un mode de descente sécurisée.
Le lien sécurisé : chiffré et authentifié, comme l'a montré Makafui.
L'autonomie : 30 à 45 minutes visées.
La charge utile : une caméra jour et nuit stabilisée, plus le module IA.
Et la documentation technique : c'est le dossier que je viens de vous présenter.`,
  },
  {
    id: "calendrier", qui: "cedric", duree: 35,
    script: `Notre calendrier. La candidature a été validée en août, la conception détaillée faite en septembre et le dossier soumis le 30 septembre.
Nous sommes aujourd'hui dans la phase de prototypage : assemblage, intégration électronique, puis essais au sol, en vol et de sécurité jusqu'à fin novembre.
Et nous serons prêts pour la démonstration de la semaine du 7 décembre.
Je rends la parole à Israel pour conclure.`,
  },
  {
    id: "budget", qui: "israel", duree: 35,
    script: `Merci Cédric. Un mot sur le budget.
Notre budget prévisionnel se situe entre 730 000 et 1 400 000 francs CFA : la cellule et les moteurs, l'avionique, la caméra, l'énergie, les liaisons et les consommables. Le module d'intelligence artificielle embarquée représente 120 000 à 160 000 francs supplémentaires.
Chaque poste est justifié par notre dimensionnement, et nous privilégions des composants standards, disponibles et réparables.`,
  },
  {
    id: "conclusion", qui: "israel", duree: 35,
    script: `Pour conclure : la Sentinelle Aérienne, c'est un drone qui décolle partout, qui vole longtemps, qui voit et comprend ce qu'il voit, et qui communique en sécurité.
C'est une solution pensée au Togo, pour les besoins de surveillance de nos zones sensibles, et extensible demain à la cartographie ou à l'aide humanitaire.
Merci pour votre attention. Toute l'équipe est à votre disposition pour répondre à vos questions.`,
  },
];

module.exports = { INTERVENANTS, ORDRE, DIAPOS };
