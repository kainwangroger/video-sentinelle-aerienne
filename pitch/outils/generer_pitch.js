// Génère pitch/sentinelle_aerienne_pitch.pptx et pitch/script_oral.md.
// Usage : node pitch/outils/generer_pitch.js   (modules : pptxgenjs, react, react-dom, react-icons, sharp)

const path = require("path");
const fs = require("fs");
const pptxgen = require("pptxgenjs");
const React = require("react");
const ReactDOMServer = require("react-dom/server");
const sharp = require("sharp");
const fa = require("react-icons/fa");
const { INTERVENANTS, ORDRE, DIAPOS } = require("./contenu_pitch");

const RACINE = path.resolve(__dirname, "..");
const ASSETS = path.join(RACINE, "assets");
const SORTIE = path.join(RACINE, "sentinelle_aerienne_pitch.pptx");
const APPLY_THEME = process.env.APPLY_THEME;

// Thème sombre, assorti aux schémas du dépôt (fond nuit, cyan, ambre).
const THEME = {
  name: "Sentinelle Aerienne",
  headFontFace: "Calibri",
  bodyFontFace: "Calibri",
  colors: {
    dk1: "E8F1FA", lt1: "050C1B", dk2: "9DB2C9", lt2: "0F2140",
    accent1: "00D4FF", accent2: "F2A541", accent3: "3CDC96", accent4: "FF5F5F",
    accent5: "1D3B63", accent6: "7AA7FF", hlink: "00D4FF", folHlink: "7AA7FF",
  },
};
const HEX = THEME.colors;

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13,33 x 7,5 pouces
pres.title = "Sentinelle Aérienne — Pitch CECFD 2026";
pres.author = "SkyVision Togo";
pres.company = "SkyVision Togo";
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
const C = pres.SchemeColor;

const W = 13.333, H = 7.5, M = 0.6;
const fond = path.join(ASSETS, "fond.png");
const img = (n) => path.join(ASSETS, n + ".png");

// ---------- icônes ----------
async function icone(nom, couleur, taille = 256) {
  const svg = ReactDOMServer.renderToStaticMarkup(React.createElement(fa[nom], { color: "#" + couleur, size: taille }));
  const buf = await sharp(Buffer.from(svg)).png().toBuffer();
  return "image/png;base64," + buf.toString("base64");
}

// ---------- gabarits ----------
const pied = { text: "SkyVision Togo · Sentinelle Aérienne · CECFD 2026 — ANAC", options: { x: M, y: H - 0.45, w: 7, h: 0.3, fontSize: 10, color: C.text2, margin: 0 } };

pres.defineSlideMaster({
  title: "COUVERTURE",
  background: { path: fond },
  objects: [],
});
pres.defineSlideMaster({
  title: "CONTENU",
  background: { path: fond },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: M, y: 0.45, w: 9.0, h: 0.8, fontSize: 32, bold: true, color: C.text1, align: "left", valign: "middle", margin: 0 }, text: "" } },
    { text: pied },
  ],
  slideNumber: { x: W - M - 0.5, y: H - 0.45, w: 0.5, h: 0.3, fontSize: 10, color: C.text2, align: "right" },
});

// ---------- éléments récurrents ----------
const ICONE_QUI = { israel: "FaTools", angelo: "FaLaptopCode", makafui: "FaBroadcastTower", roger: "FaBrain", cedric: "FaDatabase" };
const icones = {};

function puceIntervenant(slide, qui) {
  // Pastille en haut à droite : qui parle.
  const p = INTERVENANTS[qui];
  const x = W - M - 3.0, y = 0.5;
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w: 3.0, h: 0.7, rectRadius: 0.35, fill: { color: C.background2 }, line: { color: C.accent5, width: 1 }, objectName: "Intervenant" });
  slide.addShape(pres.shapes.OVAL, { x: x + 0.1, y: y + 0.1, w: 0.5, h: 0.5, fill: { color: C.accent1 }, line: { type: "none" } });
  slide.addImage({ data: icones[qui + "_sombre"], x: x + 0.22, y: y + 0.22, w: 0.26, h: 0.26 });
  slide.addText([
    { text: p.court, options: { bold: true, fontSize: 14, color: C.text1, breakLine: true } },
    { text: p.puce, options: { fontSize: 10, color: C.text2 } },
  ], { x: x + 0.72, y: y + 0.06, w: 2.2, h: 0.58, margin: 0, valign: "middle", isTextBox: true });
}

function carte(slide, x, y, w, h, nom) {
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.12, fill: { color: C.background2, transparency: 10 }, line: { color: C.accent5, width: 1 }, objectName: nom });
}

function rondIcone(slide, data, x, y, d, couleur = C.accent1) {
  slide.addShape(pres.shapes.OVAL, { x, y, w: d, h: d, fill: { color: couleur }, line: { type: "none" } });
  const i = d * 0.52;
  slide.addImage({ data, x: x + (d - i) / 2, y: y + (d - i) / 2, w: i, h: i });
}

function nouvelle(diapo, titre, section) {
  const s = pres.addSlide({ masterName: "CONTENU", sectionTitle: section });
  s.addText(titre, { placeholder: "title" });
  puceIntervenant(s, diapo.qui);
  s.addNotes(`[${INTERVENANTS[diapo.qui].court} — ≈ ${diapo.duree} s]\n\n${diapo.script}`);
  return s;
}

const D = Object.fromEntries(DIAPOS.map((d) => [d.id, d]));
const SECTION = { israel: "Le drone", angelo: "Avionique et station sol", makafui: "Liaisons et sécurité", roger: "Intelligence artificielle", cedric: "Supervision et conformité" };

async function main() {
  for (const q of ORDRE) icones[q + "_sombre"] = await icone(ICONE_QUI[q], HEX.lt1);
  const ic = async (n, c = HEX.lt1) => icone(n, c);

  // 1. Couverture
  pres.addSection({ title: "Ouverture" });
  {
    const d = D.titre;
    const s = pres.addSlide({ masterName: "COUVERTURE", sectionTitle: "Ouverture" });
    s.addImage({ path: img("3d_sa1_assemble"), x: 6.4, y: 2.9, w: 6.5, h: 3.21 });
    s.addText("SKYVISION TOGO  ·  CECFD 2026 — ANAC", { x: M, y: 0.7, w: 8, h: 0.4, fontSize: 14, bold: true, color: C.accent1, charSpacing: 3, margin: 0, isTextBox: true });
    s.addText("Sentinelle Aérienne", { x: M, y: 1.3, w: 7, h: 1.2, fontSize: 54, bold: true, color: C.text1, margin: 0, isTextBox: true });
    s.addText("Drone hybride VTOL de surveillance des zones sensibles, avec IA embarquée et liaison sécurisée", { x: M, y: 2.55, w: 5.6, h: 1.1, fontSize: 20, color: C.text2, margin: 0, isTextBox: true });
    s.addText([
      { text: "Thématique : ", options: { bold: true, color: C.accent2 } },
      { text: "Surveillance & Sécurité", options: { color: C.text1 } },
    ], { x: M, y: 4.0, w: 6, h: 0.4, fontSize: 16, margin: 0, isTextBox: true });
    s.addText(ORDRE.map((q, i) => ({ text: INTERVENANTS[q].nom, options: { breakLine: i < ORDRE.length - 1 } })),
      { x: M, y: 5.0, w: 6.5, h: 1.7, fontSize: 14, color: C.text2, margin: 0, paraSpaceAfter: 2, isTextBox: true });
    s.addText("Présenté par Israel (chef d'équipe)", { x: 7.6, y: 6.55, w: 5.1, h: 0.35, fontSize: 12, italic: true, color: C.text2, align: "right", margin: 0, isTextBox: true });
    s.addNotes(`[Israel — ≈ ${d.duree} s]\n\n${d.script}`);
  }

  // 2. Équipe
  {
    const s = nouvelle(D.equipe, "Une équipe, cinq lots, un seul système", "Ouverture");
    const cw = 2.24, gap = 0.17, y = 1.75, h = 4.3;
    for (let i = 0; i < ORDRE.length; i++) {
      const q = ORDRE[i], p = INTERVENANTS[q];
      const x = M + i * (cw + gap);
      carte(s, x, y, cw, h, "Membre " + p.court);
      rondIcone(s, icones[q + "_sombre"], x + (cw - 1.0) / 2, y + 0.35, 1.0);
      s.addText(String(i + 1), { x: x + 0.15, y: y + 0.15, w: 0.4, h: 0.4, fontSize: 14, bold: true, color: C.accent2, margin: 0, isTextBox: true });
      s.addText(p.nom, { x: x + 0.15, y: y + 1.55, w: cw - 0.3, h: 1.0, fontSize: 15, bold: true, color: C.text1, align: "center", valign: "top", margin: 0, isTextBox: true });
      s.addText(p.role.split(" · ").map((r, k, a) => ({ text: r, options: { breakLine: k < a.length - 1 } })),
        { x: x + 0.15, y: y + 2.6, w: cw - 0.3, h: 1.8, fontSize: 13, color: C.text2, align: "center", valign: "top", margin: 0, paraSpaceAfter: 4, isTextBox: true });
    }
    s.addText("Les numéros indiquent l'ordre de passage.", { x: M, y: 6.5, w: 8, h: 0.3, fontSize: 11, italic: true, color: C.text2, margin: 0, isTextBox: true });
  }

  // 3. Problème
  pres.addSection({ title: SECTION.israel });
  {
    const s = nouvelle(D.probleme, "Surveiller loin, longtemps, sans piste", SECTION.israel);
    const items = [
      ["FaHelicopter", "Multirotor", "Décolle partout, mais vole peu : 20 à 30 min en général, car il porte tout son poids avec ses moteurs."],
      ["FaPlane", "Avion à voilure fixe", "Vole longtemps et vite, mais a besoin d'une piste ou d'une catapulte pour décoller et se poser."],
      ["FaHourglassHalf", "Analyse après le vol", "Les images sont souvent examinées au retour : l'anomalie est découverte trop tard."],
    ];
    const cw = 3.85, gap = 0.3, y = 1.8, h = 3.9;
    for (let i = 0; i < 3; i++) {
      const x = M + i * (cw + gap);
      carte(s, x, y, cw, h, "Limite " + (i + 1));
      rondIcone(s, await ic(items[i][0]), x + 0.35, y + 0.4, 0.9, i === 2 ? C.accent4 : C.accent2);
      s.addText(items[i][1], { x: x + 0.35, y: y + 1.5, w: cw - 0.7, h: 0.5, fontSize: 20, bold: true, color: C.text1, margin: 0, isTextBox: true });
      s.addText(items[i][2], { x: x + 0.35, y: y + 2.1, w: cw - 0.7, h: 1.6, fontSize: 15, color: C.text2, margin: 0, valign: "top", isTextBox: true });
    }
    s.addText("Zones visées : aéroports et pistes, frontières, sites industriels et sensibles du Togo.", { x: M, y: 6.0, w: 12, h: 0.4, fontSize: 15, italic: true, color: C.accent1, margin: 0, isTextBox: true });
  }

  // 4. Solution
  {
    const s = nouvelle(D.solution, "Notre réponse : un hybride VTOL", SECTION.israel);
    s.addImage({ path: img("3d_sa1_assemble"), x: 5.9, y: 1.55, w: 6.9, h: 3.4 });
    const pts = [
      ["FaArrowUp", "Décollage et atterrissage verticaux", "4 moteurs de sustentation : aucune piste nécessaire."],
      ["FaArrowRight", "Croisière sur l'aile", "1 moteur propulsif : grande vitesse, faible consommation."],
      ["FaRobot", "Transition automatique", "Gérée par le contrôleur de vol."],
    ];
    for (let i = 0; i < 3; i++) {
      const y = 1.6 + i * 1.15;
      rondIcone(s, await ic(pts[i][0]), M, y, 0.7);
      s.addText(pts[i][1], { x: M + 0.95, y: y - 0.02, w: 4.0, h: 0.4, fontSize: 17, bold: true, color: C.text1, margin: 0, isTextBox: true });
      s.addText(pts[i][2], { x: M + 0.95, y: y + 0.38, w: 4.0, h: 0.4, fontSize: 14, color: C.text2, margin: 0, isTextBox: true });
    }
    const inno = [["FaBrain", "Innovation 1", "IA embarquée de détection en temps réel"], ["FaShieldAlt", "Innovation 2", "Liaison sécurisée dès la conception"]];
    for (let i = 0; i < 2; i++) {
      const x = M + i * 6.15, y = 5.3, w = 5.95, h = 1.05;
      carte(s, x, y, w, h, inno[i][1]);
      rondIcone(s, await ic(inno[i][0]), x + 0.25, y + 0.2, 0.65, C.accent2);
      s.addText([
        { text: inno[i][1], options: { fontSize: 12, bold: true, color: C.accent2, breakLine: true } },
        { text: inno[i][2], options: { fontSize: 16, bold: true, color: C.text1 } },
      ], { x: x + 1.1, y: y + 0.12, w: w - 1.3, h: 0.8, margin: 0, valign: "middle", isTextBox: true });
    }
  }

  // 5. Fiche d'identité
  {
    const s = nouvelle(D.identite, "Le SA-1 en chiffres", SECTION.israel);
    const stats = [
      ["2,0 m", "d'envergure", C.accent1], ["6,4 kg", "au décollage (marge comprise)", C.accent1], ["30–45 min", "d'autonomie visée (≈ 50 min calculées)", C.accent2],
      ["68 km/h", "vitesse de croisière", C.accent1], ["355 Wh", "batterie LiPo 6S 16 000 mAh", C.accent1], ["1 000 → 280 W", "stationnaire → croisière", C.accent3],
    ];
    const cw = 3.85, gap = 0.3, ch = 2.15;
    for (let i = 0; i < 6; i++) {
      const x = M + (i % 3) * (cw + gap), y = 1.75 + Math.floor(i / 3) * (ch + 0.3);
      carte(s, x, y, cw, ch, "Chiffre " + (i + 1));
      s.addText(stats[i][0], { x: x + 0.3, y: y + 0.3, w: cw - 0.6, h: 1.0, fontSize: stats[i][0].length > 10 ? 34 : 44, bold: true, color: stats[i][2], margin: 0, isTextBox: true });
      s.addText(stats[i][1], { x: x + 0.3, y: y + 1.35, w: cw - 0.6, h: 0.6, fontSize: 15, color: C.text2, margin: 0, isTextBox: true });
    }
    s.addText("Estimations de dimensionnement : seuls les essais en vol font foi.", { x: M, y: 6.55, w: 8, h: 0.3, fontSize: 11, italic: true, color: C.text2, margin: 0, isTextBox: true });
  }

  // 6. Structure
  {
    const s = nouvelle(D.structure, "Structure et assemblage", SECTION.israel);
    s.addImage({ path: img("3d_vue_eclatee"), x: 1.2, y: 1.45, w: 5.4, h: 4.18 });
    const pts = [
      ["Cellule", "Fibre de carbone et composite, modélisée sous SolidWorks"],
      ["Fuselage", "Batterie, avionique et module IA ; trappe d'accès"],
      ["Aile en 3 parties", "Démontable pour le transport ; 0,56 m²"],
      ["Double poutre", "Porte les 4 moteurs verticaux et l'empennage en H"],
      ["Antennes", "Zones en fibre de verre : le carbone bloque les ondes"],
    ];
    s.addText(pts.map((p, i) => [
      { text: p[0], options: { bold: true, color: C.text1, fontSize: 16, breakLine: true } },
      { text: p[1], options: { color: C.text2, fontSize: 14, breakLine: i < pts.length - 1 } },
    ]).flat(), { x: 8.4, y: 1.6, w: 4.35, h: 4.6, margin: 0, valign: "top", paraSpaceAfter: 6, isTextBox: true });
    s.addText("Vue éclatée issue de notre maquette 3D (guide de conception et d'assemblage).", { x: M, y: 5.75, w: 7.4, h: 0.3, fontSize: 11, italic: true, color: C.text2, margin: 0, isTextBox: true });
    s.addText("→ Bilan de masse détaillé, pièce par pièce, dans le dossier technique.", { x: M, y: 6.15, w: 7.4, h: 0.35, fontSize: 14, color: C.accent1, margin: 0, isTextBox: true });
  }

  // 7. Avionique / transition
  pres.addSection({ title: SECTION.angelo });
  {
    const s = nouvelle(D.avionique, "Le cerveau : ArduPilot QuadPlane", SECTION.angelo);
    carte(s, 5.65, 1.5, 7.08, 3.5, "Cadre transition");
    s.addImage({ path: img("transition"), x: 5.75, y: 1.6, w: 6.88, h: 2.97 });
    s.addText("Capteurs fusionnés en permanence", { x: M, y: 1.6, w: 4.9, h: 0.4, fontSize: 17, bold: true, color: C.text1, margin: 0, isTextBox: true });
    s.addText(["Centrale inertielle (IMU)", "Baromètre et compas", "GNSS multi-constellation", "Vitesse air (Pitot)", "Télémètre laser"].map((t, i, a) => ({ text: t, options: { bullet: true, breakLine: i < a.length - 1 } })),
      { x: M, y: 2.05, w: 4.9, h: 2.2, fontSize: 15, color: C.text2, margin: 0, paraSpaceAfter: 4, isTextBox: true });
    const etapes = [["1", "Stationnaire", "moteurs verticaux"], ["2", "Transition", "l'aile prend le relais vers ≈ 15 m/s"], ["3", "Croisière", "moteur propulsif seul"]];
    const cw = 3.85, gap = 0.3, y = 5.3;
    for (let i = 0; i < 3; i++) {
      const x = M + i * (cw + gap);
      carte(s, x, y, cw, 1.1, "Phase " + etapes[i][0]);
      s.addShape(pres.shapes.OVAL, { x: x + 0.25, y: y + 0.25, w: 0.6, h: 0.6, fill: { color: i === 1 ? C.accent2 : C.accent1 }, line: { type: "none" } });
      s.addText(etapes[i][0], { x: x + 0.25, y: y + 0.25, w: 0.6, h: 0.6, fontSize: 18, bold: true, color: C.background1, align: "center", valign: "middle", margin: 0, isTextBox: true });
      s.addText([
        { text: etapes[i][1], options: { bold: true, fontSize: 16, color: C.text1, breakLine: true } },
        { text: etapes[i][2], options: { fontSize: 13, color: C.text2 } },
      ], { x: x + 1.05, y: y + 0.12, w: cw - 1.2, h: 0.86, margin: 0, valign: "middle", isTextBox: true });
    }
  }

  // 8. Station sol
  {
    const s = nouvelle(D.station, "La station de contrôle au sol", SECTION.angelo);
    carte(s, M, 1.5, 7.2, 3.15, "Cadre simulation");
    s.addImage({ path: img("simulation_detection"), x: M + 0.1, y: 1.6, w: 7.0, h: 2.82 });
    const pts = [["FaMapMarkedAlt", "Avant le vol", "Planifier : points de passage, altitude, zone autorisée, atterrissage"], ["FaTachometerAlt", "Pendant le vol", "Suivre la télémétrie : position, vitesse, batterie, liaisons"], ["FaBell", "Alertes IA en direct", "Classe, heure, zone et image de preuve"]];
    for (let i = 0; i < 3; i++) {
      const y = 1.55 + i * 1.3;
      rondIcone(s, await ic(pts[i][0]), 8.1, y, 0.75, i === 2 ? C.accent2 : C.accent1);
      s.addText(pts[i][1], { x: 9.05, y: y - 0.05, w: 3.7, h: 0.4, fontSize: 17, bold: true, color: C.text1, margin: 0, isTextBox: true });
      s.addText(pts[i][2], { x: 9.05, y: y + 0.35, w: 3.7, h: 0.75, fontSize: 13, color: C.text2, margin: 0, valign: "top", isTextBox: true });
    }
    s.addText("L'opérateur ne surveille plus la vidéo en continu : le drone lui signale ce qui compte.", { x: M, y: 5.6, w: 12, h: 0.5, fontSize: 18, italic: true, color: C.accent1, margin: 0, isTextBox: true });
    s.addText("Logiciel de vol Mission Planner / QGroundControl + application de supervision web/mobile. Image : simulation, valeurs illustratives.", { x: M, y: 6.15, w: 12, h: 0.3, fontSize: 11, color: C.text2, margin: 0, isTextBox: true });
  }

  // 9. Liaisons
  pres.addSection({ title: SECTION.makafui });
  {
    const s = nouvelle(D.liaisons, "Trois liaisons indépendantes", SECTION.makafui);
    const l = [
      ["FaVideo", "Vidéo HD", "10 – 15 km", "Image de la caméra et informations de vol.", C.accent1],
      ["FaBroadcastTower", "Radio longue portée chiffrée", "30 – 50 km (théorique)", "Télémétrie, ordres et alertes. Sans vidéo.", C.accent1],
      ["FaLifeRing", "Canal d'urgence ELRS", "Indépendant", "Reprise en main : retour au point de départ ou coupure moteurs.", C.accent4],
    ];
    const cw = 3.85, gap = 0.3, y = 1.75, h = 3.9;
    for (let i = 0; i < 3; i++) {
      const x = M + i * (cw + gap);
      carte(s, x, y, cw, h, l[i][1]);
      rondIcone(s, await ic(l[i][0]), x + 0.35, y + 0.4, 0.9, l[i][4]);
      s.addText(l[i][1], { x: x + 0.35, y: y + 1.5, w: cw - 0.7, h: 0.8, fontSize: 20, bold: true, color: C.text1, margin: 0, valign: "top", isTextBox: true });
      s.addText(l[i][2], { x: x + 0.35, y: y + 2.3, w: cw - 0.7, h: 0.45, fontSize: 18, bold: true, color: C.accent2, margin: 0, isTextBox: true });
      s.addText(l[i][3], { x: x + 0.35, y: y + 2.8, w: cw - 0.7, h: 0.95, fontSize: 14, color: C.text2, margin: 0, valign: "top", isTextBox: true });
    }
    s.addText("Écartés : satellite (coût) et 4G (couverture incertaine dans les zones visées).", { x: M, y: 6.0, w: 12, h: 0.4, fontSize: 15, italic: true, color: C.text2, margin: 0, isTextBox: true });
  }

  // 10. Sécurité
  {
    const s = nouvelle(D.securite, "La sécurité dès la conception", SECTION.makafui);
    const r = [
      ["FaLock", "Chiffrement et authentification", "Données chiffrées ; messages MAVLink 2 signés : un ordre non signé est rejeté.", C.accent1],
      ["FaWaveSquare", "Anti-brouillage", "Surveillance de la qualité des liens et bascule automatique.", C.accent1],
      ["FaSatellite", "Anti-leurrage GPS", "Deux récepteurs comparés à la centrale inertielle : la source qui ment est écartée.", C.accent1],
      ["FaHome", "Retour automatique (RTH)", "Perte de liaison, batterie faible ou GPS dégradé : le drone rentre seul.", C.accent3],
      ["FaPowerOff", "Coupure d'urgence", "En dernier recours, arrêt des moteurs sur ordre du canal d'urgence.", C.accent4],
    ];
    for (let i = 0; i < r.length; i++) {
      const y = 1.6 + i * 0.98, x = M, w = W - 2 * M;
      carte(s, x, y, w, 0.82, r[i][1]);
      rondIcone(s, await ic(r[i][0]), x + 0.2, y + 0.11, 0.6, r[i][3]);
      s.addText(r[i][1], { x: x + 1.05, y: y + 0.1, w: 3.9, h: 0.62, fontSize: 17, bold: true, color: C.text1, margin: 0, valign: "middle", isTextBox: true });
      s.addText(r[i][2], { x: x + 5.0, y: y + 0.1, w: w - 5.2, h: 0.62, fontSize: 15, color: C.text2, margin: 0, valign: "middle", isTextBox: true });
    }
  }

  // 11. IA chaîne
  pres.addSection({ title: SECTION.roger });
  {
    const s = nouvelle(D.ia, "L'IA analyse les images à bord", SECTION.roger);
    s.addImage({ path: img("chaine_ia_bande"), x: 0.2, y: 1.55, w: 12.9, h: 2.28 });
    const st = [["26 TOPS", "Raspberry Pi 5 + AI HAT+ (Hailo-8)"], ["YOLOv8s", "détecteur affiné sur nos données"], ["3 classes", "personnes, véhicules, débris au sol"], ["0 cloud", "tout à bord ; stockage si liaison coupée"]];
    const cw = 2.86, gap = 0.2, y = 4.35, h = 1.75;
    for (let i = 0; i < 4; i++) {
      const x = M + i * (cw + gap);
      carte(s, x, y, cw, h, st[i][0]);
      s.addText(st[i][0], { x: x + 0.25, y: y + 0.2, w: cw - 0.5, h: 0.75, fontSize: 32, bold: true, color: i === 3 ? C.accent3 : C.accent1, margin: 0, isTextBox: true });
      s.addText(st[i][1], { x: x + 0.25, y: y + 0.95, w: cw - 0.5, h: 0.65, fontSize: 13, color: C.text2, margin: 0, valign: "top", isTextBox: true });
    }
    s.addText("Une alerte = classe, score, heure, zone et image de preuve. Un même objet suivi ne déclenche qu'une alerte.", { x: M, y: 6.3, w: 12, h: 0.4, fontSize: 14, italic: true, color: C.accent1, margin: 0, isTextBox: true });
  }

  // 12. IA méthode
  {
    const s = nouvelle(D.ia_donnees, "Une IA mesurée et honnête", SECTION.roger);
    const col = [
      ["FaDatabase", "Données", C.accent1, ["FOD-A : plus de 30 000 objets de piste annotés", "Images filmées avec la caméra du drone", "Scènes vides et pièges (ombres, marquages) contre les fausses alertes"]],
      ["FaQuestionCircle", "Objets inconnus", C.accent2, ["Candidat crédible sans classe fiable → « à vérifier »", "Image de preuve jointe", "Pas de prétention à tout reconnaître"]],
      ["FaBalanceScale", "Limites assumées", C.accent4, ["Aide à l'inspection, pas une certification", "L'IA ne pilote jamais le drone", "Aucun score annoncé avant mesure"]],
    ];
    const cw = 3.85, gap = 0.3, y = 1.75, h = 4.3;
    for (let i = 0; i < 3; i++) {
      const x = M + i * (cw + gap);
      carte(s, x, y, cw, h, col[i][1]);
      rondIcone(s, await ic(col[i][0]), x + 0.35, y + 0.35, 0.8, col[i][2]);
      s.addText(col[i][1], { x: x + 1.35, y: y + 0.5, w: cw - 1.6, h: 0.5, fontSize: 20, bold: true, color: C.text1, margin: 0, isTextBox: true });
      s.addText(col[i][3].map((t, k, a) => ({ text: t, options: { bullet: true, breakLine: k < a.length - 1 } })),
        { x: x + 0.35, y: y + 1.45, w: cw - 0.6, h: 2.7, fontSize: 15, color: C.text2, margin: 0, valign: "top", paraSpaceAfter: 8, isTextBox: true });
    }
    s.addText("Code, outils, données d'exemple et protocole de validation : disponibles dans notre dépôt.", { x: M, y: 6.3, w: 12, h: 0.4, fontSize: 14, italic: true, color: C.accent1, margin: 0, isTextBox: true });
  }

  // 13. Supervision et documentation
  pres.addSection({ title: SECTION.cedric });
  {
    const s = nouvelle(D.supervision, "Rien ne se perd : supervision et dossier", SECTION.cedric);
    const flux = [["FaPlane", "Drone", "Journal à bord"], ["FaDesktop", "Station sol", "Affichage des alertes"], ["FaServer", "Back-end", "Archivage + journaux signés"]];
    const bw = 3.44, y = 1.75;
    for (let i = 0; i < 3; i++) {
      const x = M + i * (bw + 0.9);
      carte(s, x, y, bw, 1.5, flux[i][1]);
      rondIcone(s, await ic(flux[i][0]), x + 0.25, y + 0.4, 0.7);
      s.addText([
        { text: flux[i][1], options: { bold: true, fontSize: 17, color: C.text1, breakLine: true } },
        { text: flux[i][2], options: { fontSize: 13, color: C.text2 } },
      ], { x: x + 1.1, y: y + 0.2, w: bw - 1.2, h: 1.1, margin: 0, valign: "middle", isTextBox: true });
      if (i < 2) s.addShape(pres.shapes.RIGHT_ARROW, { x: x + bw + 0.15, y: y + 0.55, w: 0.6, h: 0.4, fill: { color: C.accent1 }, line: { type: "none" } });
    }
    s.addText("Format d'alerte commun (schéma JSON) : classe, score, heure, zone, image.", { x: M, y: 3.45, w: 10.5, h: 0.4, fontSize: 15, italic: true, color: C.accent1, margin: 0, isTextBox: true });
    s.addText("Dossier déjà livré", { x: M, y: 4.1, w: 6, h: 0.45, fontSize: 18, bold: true, color: C.text1, margin: 0, isTextBox: true });
    const docs = ["Fiche technique complète (chaque composant expliqué)", "Guide de conception et d'assemblage", "Calculs de dimensionnement", "Paramètres ArduPilot du SA-1", "Check-lists avant vol, après vol, urgences", "Vidéos explicatives et code du module IA"];
    const half = [docs.slice(0, 3), docs.slice(3)];
    for (let c = 0; c < 2; c++)
      s.addText(half[c].map((t, k, a) => ({ text: t, options: { bullet: true, breakLine: k < a.length - 1 } })),
        { x: M + c * 6.1, y: 4.65, w: 5.9, h: 1.6, fontSize: 15, color: C.text2, margin: 0, valign: "top", paraSpaceAfter: 6, isTextBox: true });
  }

  // 14. Conformité
  {
    const s = nouvelle(D.conformite, "Conformité aux exigences du concours", SECTION.cedric);
    const lignes = [
      ["Navigation GPS + retour au point de départ (RTH)", "GNSS couplé au contrôleur de vol, RTH automatique"],
      ["Coupure d'urgence (fail-safe)", "Interrupteur de coupure moteurs + descente sécurisée"],
      ["Lien sécurisé drone / station", "Liaison chiffrée et authentifiée, messages signés"],
      ["Autonomie minimale", "30 – 45 min visées (≈ 50 min calculées)"],
      ["Charge utile adaptée", "Caméra jour/nuit stabilisée + module IA"],
      ["Documentation technique", "Schémas, dimensionnement, performances, sécurité"],
    ];
    const entete = (t) => ({ text: t, options: { bold: true, color: C.background1, fill: { color: C.accent1 }, fontSize: 15 } });
    const rows = [[entete("Exigence"), entete("Notre solution"), entete("")]];
    for (const [a, b] of lignes) rows.push([
      { text: a, options: { bold: true, color: C.text1 } },
      { text: b, options: { color: C.text2 } },
      { text: "✓", options: { bold: true, color: C.accent3, align: "center", fontSize: 20 } },
    ]);
    s.addTable(rows, { x: M, y: 1.65, w: W - 2 * M, colW: [5.2, 6.1, 0.833], fontSize: 15, fill: { color: C.background2 }, border: { type: "solid", pt: 1, color: HEX.accent5 }, rowH: 0.72, valign: "middle", margin: [0, 0.15, 0, 0.15] });
  }

  // 15. Calendrier
  {
    const s = nouvelle(D.calendrier, "Calendrier", SECTION.cedric);
    const et = [
      ["15 – 30 août", "Candidature validée, cahier des charges", true],
      ["Septembre", "Conception détaillée : 3D, composants, dimensionnement", true],
      ["30 septembre", "Dossier de conception soumis", true],
      ["Octobre – novembre", "Prototypage, assemblage, essais au sol, en vol et de sécurité", false],
      ["Semaine du 7 décembre", "Démonstration, présentation orale, remise des prix", false],
    ];
    const y0 = 3.4, x0 = 1.75, pas = 2.45;
    s.addShape(pres.shapes.LINE, { x: x0, y: y0, w: pas * 4, h: 0, line: { color: C.accent5, width: 3 } });
    for (let i = 0; i < et.length; i++) {
      const x = x0 + i * pas, fait = et[i][2], ici = i === 3;
      s.addShape(pres.shapes.OVAL, { x: x - 0.25, y: y0 - 0.25, w: 0.5, h: 0.5, fill: { color: fait ? C.accent3 : ici ? C.accent2 : C.background2 }, line: { color: ici ? C.accent2 : C.accent5, width: 2 } });
      s.addText(et[i][0], { x: x - 1.15, y: y0 + 0.45, w: 2.3, h: 0.5, fontSize: 16, bold: true, color: ici ? C.accent2 : C.text1, align: "center", margin: 0, isTextBox: true });
      s.addText(et[i][1], { x: x - 1.15, y: y0 + 0.95, w: 2.3, h: 1.4, fontSize: 13, color: C.text2, align: "center", valign: "top", margin: 0, isTextBox: true });
    }
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: x0 + 3 * pas - 1.0, y: y0 - 1.25, w: 2.0, h: 0.55, rectRadius: 0.27, fill: { color: C.accent2 }, line: { type: "none" } });
    s.addText("Nous sommes ici", { x: x0 + 3 * pas - 1.0, y: y0 - 1.25, w: 2.0, h: 0.55, fontSize: 14, bold: true, color: C.background1, align: "center", valign: "middle", margin: 0, isTextBox: true });
    s.addText("Étapes terminées en vert.", { x: M, y: 6.3, w: 6, h: 0.3, fontSize: 11, italic: true, color: C.text2, margin: 0, isTextBox: true });
  }

  // 16. Budget
  pres.addSection({ title: "Conclusion" });
  {
    const s = nouvelle(D.budget, "Budget prévisionnel", "Conclusion");
    const postes = [
      ["Cellule, moteurs, ESC, hélices", "200 000 – 350 000"],
      ["Contrôleur de vol + GPS + capteurs", "200 000 – 350 000"],
      ["Caméra + nacelle stabilisée", "120 000 – 300 000"],
      ["Batteries et alimentation", "80 000 – 150 000"],
      ["Liaison radio / télémétrie", "80 000 – 150 000"],
      ["Consommables et divers", "50 000 – 100 000"],
    ];
    const entete = (t, a = "left") => ({ text: t, options: { bold: true, color: C.background1, fill: { color: C.accent1 }, align: a } });
    const rows = [[entete("Poste"), entete("FCFA", "right")]];
    for (const [a, b] of postes) rows.push([{ text: a, options: { color: C.text1 } }, { text: b, options: { color: C.text2, align: "right" } }]);
    rows.push([{ text: "Total (fiche projet)", options: { bold: true, color: C.text1 } }, { text: "730 000 – 1 400 000", options: { bold: true, color: C.text1, align: "right" } }]);
    s.addTable(rows, { x: M, y: 1.65, w: 7.4, colW: [4.6, 2.8], fontSize: 15, fill: { color: C.background2 }, border: { type: "solid", pt: 1, color: HEX.accent5 }, rowH: 0.52, valign: "middle", margin: [0, 0.15, 0, 0.15] });
    const x = 8.4, w = W - M - x;
    carte(s, x, 1.65, w, 2.0, "Module IA");
    s.addText([
      { text: "+ 120 000 – 160 000", options: { fontSize: 26, bold: true, color: C.accent2, breakLine: true } },
      { text: "Module IA embarqué (Raspberry Pi 5 + AI HAT+)", options: { fontSize: 14, color: C.text2 } },
    ], { x: x + 0.3, y: 1.8, w: w - 0.6, h: 1.7, margin: 0, valign: "middle", isTextBox: true });
    carte(s, x, 3.95, w, 2.2, "Principes");
    s.addText(["Chaque poste justifié par le dimensionnement", "Composants standards, disponibles, réparables"].map((t, k, a) => ({ text: t, options: { bullet: true, breakLine: k < a.length - 1 } })),
      { x: x + 0.3, y: 4.15, w: w - 0.6, h: 1.8, fontSize: 15, color: C.text2, margin: 0, valign: "middle", paraSpaceAfter: 8, isTextBox: true });
  }

  // 17. Conclusion
  {
    const d = D.conclusion;
    const s = pres.addSlide({ masterName: "COUVERTURE", sectionTitle: "Conclusion" });
    s.addImage({ path: img("3d_sa1_assemble"), x: 6.5, y: 2.1, w: 6.4, h: 3.16 });
    s.addText("Sentinelle Aérienne", { x: M, y: 0.7, w: 8, h: 0.5, fontSize: 18, bold: true, color: C.accent1, margin: 0, isTextBox: true });
    const mots = ["Décolle partout", "Vole longtemps", "Voit et comprend", "Communique en sécurité"];
    s.addText(mots.map((t, i) => ({ text: t, options: { breakLine: i < mots.length - 1, color: i % 2 ? C.text1 : C.text1 } })),
      { x: M, y: 1.5, w: 6, h: 3.2, fontSize: 36, bold: true, margin: 0, valign: "top", paraSpaceAfter: 6, isTextBox: true });
    s.addText("Pensé au Togo pour nos zones sensibles · extensible à la cartographie et à l'aide humanitaire", { x: M, y: 4.9, w: 5.4, h: 0.8, fontSize: 15, color: C.text2, margin: 0, isTextBox: true });
    s.addText("Merci — vos questions", { x: M, y: 6.0, w: 8, h: 0.7, fontSize: 30, bold: true, color: C.accent2, margin: 0, isTextBox: true });
    s.addNotes(`[Israel — ≈ ${d.duree} s]\n\n${d.script}`);
  }

  await pres.writeFile({ fileName: SORTIE });
  if (APPLY_THEME) await require(APPLY_THEME).applyTheme(SORTIE, THEME);
  ecrireScript();
  console.log("ok", SORTIE);
}

function mmss(s) { return `${Math.floor(s / 60)} min ${String(s % 60).padStart(2, "0")}`; }

function ecrireScript() {
  const total = DIAPOS.reduce((a, d) => a + d.duree, 0);
  const L = [];
  L.push("# Pitch « Sentinelle Aérienne » — script oral", "");
  L.push("SkyVision Togo · CECFD 2026 — ANAC", "");
  L.push(`Support : \`sentinelle_aerienne_pitch.pptx\` (17 diapos). Le même texte est dans les **notes de l'orateur** de chaque diapo.`, "");
  L.push(`Durée totale indicative : **${mmss(total)}** à un rythme posé.`, "");
  L.push("## Ordre de passage", "", "| # | Intervenant | Rôle | Diapos | Temps |", "|---|---|---|---|---|");
  ORDRE.forEach((q, i) => {
    const nums = DIAPOS.map((d, k) => (d.qui === q ? k + 1 : null)).filter(Boolean);
    const t = DIAPOS.filter((d) => d.qui === q).reduce((a, d) => a + d.duree, 0);
    L.push(`| ${i + 1} | ${INTERVENANTS[q].nom} | ${INTERVENANTS[q].role} | ${nums.join(", ")} | ${mmss(t)} |`);
  });
  L.push("", "Israel ouvre et conclut (diapos 16 et 17). Chaque intervenant commence par se présenter, puis termine en passant la parole au suivant.", "");
  L.push("## Conseils", "",
    "- Parler au jury, pas à l'écran : la diapo illustre, le script porte le message.",
    "- Les phrases de passage (« Je passe la parole à… ») rendent l'enchaînement fluide : les garder.",
    "- Si le temps est limité à 10 min : raccourcir les diapos 3, 6, 13 et 16 (≈ 20 s chacune).",
    "- Avoir le dossier technique et la vidéo d'assemblage prêts pour les questions.", "");
  let courant = null;
  DIAPOS.forEach((d, k) => {
    if (d.qui !== courant) {
      courant = d.qui;
      L.push(`## ${INTERVENANTS[d.qui].nom}`, "", `*${INTERVENANTS[d.qui].role}*`, "");
    }
    L.push(`### Diapo ${k + 1} — ≈ ${d.duree} s`, "");
    for (const p of d.script.split("\n")) L.push(`> ${p}`, ">");
    L.pop();
    L.push("");
  });
  L.push("## Questions probables du jury (pistes de réponse)", "",
    "| Question | Qui répond | Piste |", "|---|---|---|",
    "| Pourquoi un quadplane plutôt qu'un tiltrotor ? | Israel | Mécaniquement plus simple et plus fiable : pas de moteur basculant, transition gérée par ArduPilot. |",
    "| Que se passe-t-il si un moteur vertical tombe en panne ? | Angelo | En croisière, l'aile porte le drone ; en stationnaire, l'autopilote stabilise au mieux et la procédure d'urgence s'applique (check-list urgences). |",
    "| Comment empêchez-vous un pirate de prendre le contrôle ? | Makafui | Messages MAVLink 2 signés : un ordre sans la bonne clé est rejeté ; canal d'urgence indépendant. |",
    "| Quelle est la précision de votre IA ? | Roger | Nous ne l'annonçons pas avant mesure : protocole de validation prêt (rappel par classe, fausses alertes, latence) sur données séparées. |",
    "| L'IA fonctionne-t-elle sans réseau ? | Roger | Oui : tout est à bord ; les alertes sont stockées puis renvoyées quand la liaison revient. |",
    "| Les fréquences sont-elles autorisées ? | Makafui | Demande en cours auprès de l'ANAC et de l'ARCEP ; bandes choisies pour limiter les interférences. |",
    "| Comment garantissez-vous l'intégrité des données ? | Cédric | Format d'alerte commun, archivage, journaux de vol signés. |",
    "| Quand volera-t-il ? | Israel | Essais au sol puis en vol en octobre–novembre, avant la démonstration de décembre. |", "");
  fs.writeFileSync(path.join(RACINE, "script_oral.md"), L.join("\n"));
}

main().catch((e) => { console.error(e); process.exit(1); });
