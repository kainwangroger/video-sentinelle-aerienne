// Génère pitch/sentinelle_aerienne_pitch_v2.pptx (9 diapos) et pitch/notes_oral_v2.md.
// Usage : node pitch/outils/generer_pitch_v2.js   (modules : pptxgenjs, react, react-dom, react-icons, sharp)

const path = require("path");
const fs = require("fs");
const pptxgen = require("pptxgenjs");
const React = require("react");
const ReactDOMServer = require("react-dom/server");
const sharp = require("sharp");
const fa = require("react-icons/fa");
const { INTERVENANTS, ORDRE, DIAPOS } = require("./contenu_pitch_v2");

const RACINE = path.resolve(__dirname, "..");
const ASSETS = path.join(RACINE, "assets");
const SORTIE = path.join(RACINE, "sentinelle_aerienne_pitch_v2.pptx");

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
pres.layout = "LAYOUT_WIDE";
pres.title = "Sentinelle Aérienne — Pitch CECFD 2026";
pres.author = "SkyVision Togo";
pres.company = "SkyVision Togo";
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
const C = pres.SchemeColor;

const W = 13.333, H = 7.5, M = 0.6;
const img = (n) => path.join(ASSETS, n + ".png");

async function icone(nom, couleur = HEX.lt1) {
  const svg = ReactDOMServer.renderToStaticMarkup(React.createElement(fa[nom], { color: "#" + couleur, size: 256 }));
  return "image/png;base64," + (await sharp(Buffer.from(svg)).png().toBuffer()).toString("base64");
}

pres.defineSlideMaster({ title: "COUVERTURE", background: { path: img("fond") }, objects: [] });
pres.defineSlideMaster({
  title: "CONTENU",
  background: { path: img("fond") },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: M, y: 0.45, w: 8.6, h: 0.8, fontSize: 32, bold: true, color: C.text1, align: "left", valign: "middle", margin: 0 }, text: "" } },
    { text: { text: "SkyVision Togo · Sentinelle Aérienne · CECFD 2026 — ANAC", options: { x: M, y: H - 0.45, w: 7, h: 0.3, fontSize: 10, color: C.text2, margin: 0 } } },
  ],
  slideNumber: { x: W - M - 0.5, y: H - 0.45, w: 0.5, h: 0.3, fontSize: 10, color: C.text2, align: "right" },
});

const icQui = {};

function carte(s, x, y, w, h, nom, opts = {}) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.12, fill: { color: opts.fill || C.background2, transparency: opts.transparency ?? 10 }, line: { color: opts.line || C.accent5, width: opts.lw || 1 }, objectName: nom });
}

function rond(s, data, x, y, d, couleur = C.accent1) {
  s.addShape(pres.shapes.OVAL, { x, y, w: d, h: d, fill: { color: couleur }, line: { type: "none" } });
  const i = d * 0.52;
  s.addImage({ data, x: x + (d - i) / 2, y: y + (d - i) / 2, w: i, h: i });
}

function puce(s, qui, x) {
  const p = INTERVENANTS[qui], y = 0.5, w = 2.75;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h: 0.7, rectRadius: 0.35, fill: { color: C.background2 }, line: { color: C.accent5, width: 1 }, objectName: "Intervenant " + p.court });
  rond(s, icQui[qui], x + 0.1, y + 0.1, 0.5);
  s.addText([
    { text: p.court, options: { bold: true, fontSize: 14, color: C.text1, breakLine: true } },
    { text: p.puce, options: { fontSize: 10, color: C.text2 } },
  ], { x: x + 0.72, y: y + 0.06, w: w - 0.8, h: 0.58, margin: 0, valign: "middle", isTextBox: true });
}

const D = Object.fromEntries(DIAPOS.map((d) => [d.id, d]));
function notes(s, d) {
  const qui = d.duo ? `${INTERVENANTS[d.qui].court} puis ${INTERVENANTS[d.duo].court}` : INTERVENANTS[d.qui].court;
  s.addNotes(`[${qui} — ≈ ${d.duree} s]\n\n${d.notes}`);
}
function nouvelle(id, titre, section) {
  const d = D[id];
  const s = pres.addSlide({ masterName: "CONTENU", sectionTitle: section });
  s.addText(titre, { placeholder: "title" });
  if (d.duo) { puce(s, d.qui, W - M - 2 * 2.75 - 0.15); puce(s, d.duo, W - M - 2.75); }
  else puce(s, d.qui, W - M - 2.75);
  notes(s, d);
  return s;
}

function puces(lignes, opts = {}) {
  return lignes.map((t, i, a) => ({ text: t, options: { bullet: true, breakLine: i < a.length - 1, ...opts } }));
}

async function main() {
  for (const q of ORDRE) icQui[q] = await icone(INTERVENANTS[q].icone);
  const ic = (n, c) => icone(n, c);

  // 1. Titre & équipe
  pres.addSection({ title: "Introduction" });
  {
    const s = pres.addSlide({ masterName: "COUVERTURE", sectionTitle: "Introduction" });
    s.addText("SKYVISION TOGO  ·  CECFD 2026 — ANAC", { x: M, y: 0.7, w: 6.5, h: 0.4, fontSize: 14, bold: true, color: C.accent1, charSpacing: 3, margin: 0, isTextBox: true });
    s.addText("Sentinelle Aérienne", { x: M, y: 1.25, w: 6.4, h: 1.1, fontSize: 52, bold: true, color: C.text1, margin: 0, isTextBox: true });
    s.addText("Drone hybride VTOL à IA embarquée pour la sécurité aéroportuaire et la surveillance des zones sensibles", { x: M, y: 2.45, w: 5.6, h: 1.0, fontSize: 19, color: C.text2, margin: 0, isTextBox: true });
    s.addImage({ path: img("3d_sa1_assemble"), x: M - 0.1, y: 3.75, w: 5.6, h: 2.77 });
    const x = 7.0, w = W - M - x;
    s.addText("L'équipe", { x, y: 0.7, w, h: 0.4, fontSize: 16, bold: true, color: C.accent2, margin: 0, isTextBox: true });
    for (let i = 0; i < ORDRE.length; i++) {
      const q = ORDRE[i], p = INTERVENANTS[q], y = 1.25 + i * 1.12;
      carte(s, x, y, w, 0.95, "Membre " + p.court);
      rond(s, icQui[q], x + 0.18, y + 0.16, 0.63);
      s.addText([
        { text: p.nom, options: { bold: true, fontSize: 15, color: C.text1, breakLine: true } },
        { text: p.pole, options: { fontSize: 12, color: C.text2 } },
      ], { x: x + 1.0, y: y + 0.08, w: w - 1.15, h: 0.8, margin: 0, valign: "middle", isTextBox: true });
    }
    notes(s, D.titre);
  }

  // 2. Besoin
  pres.addSection({ title: "Besoin et conception" });
  {
    const s = nouvelle("besoin", "Le besoin : des pistes sûres, en permanence", "Besoin et conception");
    const risques = [
      ["FaExclamationTriangle", "Débris sur piste (FOD)", "Boulon, fragment de pneu, outil : aspiré par un réacteur ou cause d'éclatement de pneu."],
      ["FaBinoculars", "Abords et clôtures", "Zones étendues à inspecter régulièrement, souvent peu visibles depuis le sol."],
      ["FaUserSecret", "Intrusions", "Personnes ou véhicules non autorisés près des pistes et des taxiways."],
    ];
    for (let i = 0; i < 3; i++) {
      const y = 1.65 + i * 1.5, w = 6.6;
      carte(s, M, y, w, 1.3, risques[i][1]);
      rond(s, await ic(risques[i][0]), M + 0.25, y + 0.28, 0.75, C.accent4);
      s.addText([
        { text: risques[i][1], options: { bold: true, fontSize: 18, color: C.text1, breakLine: true } },
        { text: risques[i][2], options: { fontSize: 14, color: C.text2 } },
      ], { x: M + 1.25, y: y + 0.1, w: w - 1.45, h: 1.1, margin: 0, valign: "middle", isTextBox: true });
    }
    const x = 7.6, w = W - M - x;
    carte(s, x, 1.65, w, 2.75, "Limites");
    s.addText("Inspections manuelles : leurs limites", { x: x + 0.3, y: 1.8, w: w - 0.6, h: 0.45, fontSize: 17, bold: true, color: C.accent2, margin: 0, isTextBox: true });
    s.addText(puces(["Lentes et mobilisant la piste", "Dépendantes de l'attention humaine", "Difficiles la nuit et sur grandes surfaces", "Traçabilité limitée des constats"]),
      { x: x + 0.3, y: 2.3, w: w - 0.6, h: 1.95, fontSize: 15, color: C.text2, margin: 0, paraSpaceAfter: 6, valign: "top", isTextBox: true });
    carte(s, x, 4.6, w, 1.85, "Besoin", { line: C.accent1, lw: 1.5 });
    rond(s, await ic("FaCheck"), x + 0.3, 4.95, 0.6, C.accent3);
    s.addText([
      { text: "Notre réponse", options: { bold: true, fontSize: 17, color: C.accent3, breakLine: true } },
      { text: "Une autonomie intelligente : inspecter vite, depuis les airs, et alerter immédiatement.", options: { fontSize: 15, color: C.text1 } },
    ], { x: x + 1.1, y: 4.7, w: w - 1.3, h: 1.65, margin: 0, valign: "middle", isTextBox: true });
  }

  // 3. Conception
  {
    const s = nouvelle("conception", "Conception aéronautique : VTOL hybride", "Besoin et conception");
    s.addImage({ path: img("3d_sa1_assemble"), x: 6.35, y: 1.5, w: 6.4, h: 3.16 });
    s.addText(puces([
      "Modélisation 3D complète sous SolidWorks",
      "Voilure fixe pour la croisière",
      "Rotors verticaux pour décollage et atterrissage",
      "Propulsion de croisière bimoteur sur poutres",
      "Cellule carbone / composite ; antennes en zones fibre de verre",
      "Cartes de distribution et câblage conçus par l'équipe",
    ]), { x: M, y: 1.6, w: 5.2, h: 3.4, fontSize: 16, color: C.text1, margin: 0, paraSpaceAfter: 8, valign: "top", isTextBox: true });
    const av = [["FaArrowUp", "Décollage vertical sans piste", "Depuis toute zone dégagée, même confinée", C.accent1], ["FaRoute", "Grande autonomie en croisière", "L'aile porte le drone : 30–45 min visées", C.accent2]];
    for (let i = 0; i < 2; i++) {
      const x = M + i * 6.15, y = 5.25, w = 5.95;
      carte(s, x, y, w, 1.2, av[i][1]);
      rond(s, await ic(av[i][0]), x + 0.25, y + 0.25, 0.7, av[i][3]);
      s.addText([
        { text: av[i][1], options: { bold: true, fontSize: 17, color: C.text1, breakLine: true } },
        { text: av[i][2], options: { fontSize: 14, color: C.text2 } },
      ], { x: x + 1.15, y: y + 0.12, w: w - 1.3, h: 0.96, margin: 0, valign: "middle", isTextBox: true });
    }
    s.addText("Maquette 3D de conception du SA-1", { x: 6.0, y: 4.8, w: 6.8, h: 0.3, fontSize: 11, italic: true, color: C.text2, align: "right", margin: 0, isTextBox: true });
  }

  // 4. Architecture double cœur
  pres.addSection({ title: "Technologies" });
  {
    const s = nouvelle("avionique", "Architecture avionique : la sécurité d'abord", "Technologies");
    const bw = 5.0, y = 1.6, bh = 2.85;
    const blocs = [
      { x: M, titre: "Cœur 1 — Vol temps réel", sous: "STM32H743 · Cortex-M7 · 480 MHz", ico: "FaMicrochip", c: C.accent1, l: ["Stabilisation et gestion des moteurs", "Fail-safe matériel", "Retour automatique (RTH)", "Fonctionne seul, sans l'IA"] },
      { x: W - M - bw, titre: "Cœur 2 — Vision IA", sous: "Raspberry Pi 5 + Hailo-8 (26 TOPS)", ico: "FaBrain", c: C.accent2, l: ["Détection YOLOv8s à bord", "Suivi et preuves d'alerte", "Journal hors connexion", "Ne commande jamais les moteurs"] },
    ];
    for (const b of blocs) {
      carte(s, b.x, y, bw, bh, b.titre, { line: b.c, lw: 1.5 });
      rond(s, await ic(b.ico), b.x + 0.3, y + 0.3, 0.8, b.c);
      s.addText([
        { text: b.titre, options: { bold: true, fontSize: 19, color: C.text1, breakLine: true } },
        { text: b.sous, options: { fontSize: 14, color: b.c } },
      ], { x: b.x + 1.3, y: y + 0.25, w: bw - 1.5, h: 0.9, margin: 0, valign: "middle", isTextBox: true });
      s.addText(puces(b.l), { x: b.x + 0.35, y: y + 1.35, w: bw - 0.6, h: 1.4, fontSize: 15, color: C.text2, margin: 0, paraSpaceAfter: 4, valign: "top", isTextBox: true });
    }
    const mx = M + bw + 0.15, mw = W - 2 * M - 2 * bw - 0.3;
    s.addShape(pres.shapes.LEFT_RIGHT_ARROW, { x: mx, y: y + 1.05, w: mw, h: 0.6, fill: { color: C.accent5 }, line: { type: "none" } });
    s.addText("MAVLink", { x: mx, y: y + 0.55, w: mw, h: 0.4, fontSize: 14, bold: true, color: C.text1, align: "center", margin: 0, isTextBox: true });
    s.addText("position → IA\nalertes → sol", { x: mx, y: y + 1.75, w: mw, h: 0.7, fontSize: 12, color: C.text2, align: "center", margin: 0, isTextBox: true });
    s.addText("Pourquoi séparer ?", { x: M, y: 4.75, w: 6, h: 0.45, fontSize: 18, bold: true, color: C.text1, margin: 0, isTextBox: true });
    const why = [["FaShieldAlt", "Une panne, un plantage ou une surchauffe de l'IA n'affecte pas le vol"], ["FaClock", "Le contrôleur garde un temps réel garanti, sans charge parasite"], ["FaHome", "RTH et fail-safe restent actifs même module IA éteint"]];
    for (let i = 0; i < 3; i++) {
      const x = M + i * 4.1, yy = 5.3;
      rond(s, await ic(why[i][0]), x, yy + 0.05, 0.6, C.accent3);
      s.addText(why[i][1], { x: x + 0.75, y: yy, w: 3.2, h: 0.75, fontSize: 14, color: C.text2, margin: 0, valign: "middle", isTextBox: true });
    }
    s.addText("Contrôleur du commerce compatible (type Pixhawk / Matek H743) conservé en secours.", { x: M, y: 6.3, w: 12, h: 0.3, fontSize: 11, italic: true, color: C.text2, margin: 0, isTextBox: true });
  }

  // 5. IA
  {
    const s = nouvelle("ia", "Module d'IA embarquée (Edge AI)", "Technologies");
    s.addImage({ path: img("chaine_ia_bande"), x: 0.2, y: 1.4, w: 12.9, h: 2.28 });
    const st = [
      ["26 TOPS", "Raspberry Pi 5 + AI HAT+ (NPU Hailo-8)", C.accent1],
      ["YOLOv8s", "fine-tuning FOD-A (30 000+ débris) + images locales", C.accent1],
      ["0 internet", "inférence et journal des preuves à bord", C.accent3],
      ["« À vérifier »", "objet inconnu signalé avec son image", C.accent2],
    ];
    const cw = 2.86, gap = 0.2, y = 3.95, h = 1.85;
    for (let i = 0; i < 4; i++) {
      const x = M + i * (cw + gap);
      carte(s, x, y, cw, h, st[i][0]);
      s.addText(st[i][0], { x: x + 0.25, y: y + 0.2, w: cw - 0.5, h: 0.75, fontSize: st[i][0].length > 9 ? 26 : 32, bold: true, color: st[i][2], margin: 0, isTextBox: true });
      s.addText(st[i][1], { x: x + 0.25, y: y + 0.98, w: cw - 0.5, h: 0.75, fontSize: 13, color: C.text2, margin: 0, valign: "top", isTextBox: true });
    }
    s.addText("Détecte personnes, véhicules et débris au sol · une alerte par objet suivi · la décision reste humaine.", { x: M, y: 6.1, w: 12.1, h: 0.4, fontSize: 15, italic: true, color: C.accent1, margin: 0, isTextBox: true });
  }

  // 6. Logiciel, station sol, communications
  {
    const s = nouvelle("logiciel", "Station sol et communications", "Technologies");
    const cols = [
      { x: M, titre: "Logiciel et station sol", ico: "FaDesktop", c: C.accent1, l: [
        "Station sol Flutter / web",
        "ArduPilot personnalisé avec délimitation de zone",
        "Télémétrie MAVLink en direct",
        "Alertes IA avec image + enregistrement vidéo",
        "Back-end : API REST, base MySQL, journal des vols",
      ] },
      { x: M + 6.15, titre: "Sécurité des communications", ico: "FaLock", c: C.accent2, l: [
        "Liaison chiffrée, messages MAVLink signés",
        "Détection du brouillage",
        "Anti-leurrage GPS par comparaison des sources",
        "Canal d'urgence indépendant (RTH, coupure)",
        "Télémétrie satellite de secours : en test",
      ] },
    ];
    for (const c of cols) {
      const w = 5.95, y = 1.6, h = 4.85;
      carte(s, c.x, y, w, h, c.titre);
      rond(s, await ic(c.ico), c.x + 0.3, y + 0.3, 0.8, c.c);
      s.addText(c.titre, { x: c.x + 1.3, y: y + 0.4, w: w - 1.5, h: 0.6, fontSize: 20, bold: true, color: C.text1, margin: 0, valign: "middle", isTextBox: true });
      s.addText(puces(c.l), { x: c.x + 0.35, y: y + 1.4, w: w - 0.6, h: 3.25, fontSize: 16, color: C.text2, margin: 0, paraSpaceAfter: 10, valign: "top", isTextBox: true });
    }
  }

  // 7. Innovations
  pres.addSection({ title: "Valeur ajoutée" });
  {
    const s = nouvelle("innovations", "Quatre innovations clés", "Valeur ajoutée");
    const inn = [
      ["FaMicrochip", "Architecture hybride double cœur", "STM32H7 pour le vol, Hailo-8 pour la vision : dissociation étanche entre avionique critique et IA."],
      ["FaPlane", "VTOL hybride intelligent", "Décollage vertical autonome, conversion automatique en croisière longue distance."],
      ["FaBolt", "Inférence en périphérie à 26 TOPS", "Images analysées à bord, en temps réel, sans aucune dépendance au cloud."],
      ["FaShieldAlt", "Sécurisation multicouche", "Chiffrement et signature MAVLink, anti-brouillage et anti-leurrage GPS, canal de secours."],
    ];
    const cw = 5.95, ch = 2.3, gx = 0.25, gy = 0.3;
    for (let i = 0; i < 4; i++) {
      const x = M + (i % 2) * (cw + gx), y = 1.6 + Math.floor(i / 2) * (ch + gy);
      carte(s, x, y, cw, ch, inn[i][1], { line: C.accent2, lw: 1.5 });
      s.addText(String(i + 1).padStart(2, "0"), { x: x + 0.3, y: y + 0.25, w: 1.2, h: 0.8, fontSize: 44, bold: true, color: C.accent2, margin: 0, isTextBox: true });
      rond(s, await ic(inn[i][0]), x + cw - 1.05, y + 0.3, 0.75, C.accent1);
      s.addText(inn[i][1], { x: x + 0.3, y: y + 1.0, w: cw - 0.6, h: 0.45, fontSize: 20, bold: true, color: C.text1, margin: 0, isTextBox: true });
      s.addText(inn[i][2], { x: x + 0.3, y: y + 1.48, w: cw - 0.6, h: 0.7, fontSize: 14, color: C.text2, margin: 0, valign: "top", isTextBox: true });
    }
  }

  // 8. Applications
  {
    const s = nouvelle("applications", "Polyvalence : un drone, cinq secteurs", "Valeur ajoutée");
    const dom = [
      ["FaPlaneDeparture", "Aviation civile", ["Inspection de piste", "Détection de débris (FOD)", "Surveillance des clôtures"], C.accent1],
      ["FaSeedling", "Agriculture et environnement", ["Surveillance des cultures", "Suivi environnemental", "Feux de brousse"], C.accent3],
      ["FaBolt", "Infrastructures critiques", ["Lignes électriques, pylônes", "Ponts", "Port de Lomé"], C.accent2],
      ["FaBoxOpen", "Aide humanitaire", ["Petits colis médicaux", "Zones enclavées", "Sans piste grâce au VTOL"], C.accent4],
      ["FaMapMarkedAlt", "Cartographie", ["Orthophotographie", "Relevés topographiques", "Basse altitude"], C.accent6],
    ];
    const cw = 2.27, gap = 0.2, y = 1.6, h = 4.0;
    for (let i = 0; i < 5; i++) {
      const x = M + i * (cw + gap);
      carte(s, x, y, cw, h, dom[i][1]);
      rond(s, await ic(dom[i][0]), x + (cw - 0.95) / 2, y + 0.3, 0.95, dom[i][3]);
      s.addText(dom[i][1], { x: x + 0.15, y: y + 1.4, w: cw - 0.3, h: 0.8, fontSize: 16, bold: true, color: C.text1, align: "center", valign: "top", margin: 0, isTextBox: true });
      s.addText(puces(dom[i][2]), { x: x + 0.2, y: y + 2.25, w: cw - 0.35, h: 1.6, fontSize: 14, color: C.text2, margin: 0, paraSpaceAfter: 6, valign: "top", isTextBox: true });
    }
    s.addText("Même drone, même station, même back-end : seuls la charge utile et le modèle d'IA changent.", { x: M, y: 5.9, w: 12.1, h: 0.4, fontSize: 15, italic: true, color: C.accent1, margin: 0, isTextBox: true });
  }

  // 9. Conclusion
  pres.addSection({ title: "Conclusion" });
  {
    const s = nouvelle("conclusion", "Avancement et prochaines étapes", "Conclusion");
    const et = [
      ["Août – sept.", "Conception et dossier soumis", "fait"],
      ["Octobre", "Prototypage, intégration, banc d'essai", "ici"],
      ["Novembre", "Essais au sol, en vol et de sécurité", ""],
      ["Décembre 2026", "Finale : démonstration et oral", ""],
    ];
    const y0 = 2.55, x0 = 1.75, pas = 3.25;
    s.addShape(pres.shapes.LINE, { x: x0, y: y0, w: pas * 3, h: 0, line: { color: C.accent5, width: 3 } });
    for (let i = 0; i < et.length; i++) {
      const x = x0 + i * pas, st = et[i][2];
      s.addShape(pres.shapes.OVAL, { x: x - 0.25, y: y0 - 0.25, w: 0.5, h: 0.5, fill: { color: st === "fait" ? C.accent3 : st === "ici" ? C.accent2 : C.background2 }, line: { color: st === "ici" ? C.accent2 : C.accent5, width: 2 } });
      s.addText(et[i][0], { x: x - 1.3, y: y0 + 0.4, w: 2.6, h: 0.45, fontSize: 17, bold: true, color: st === "ici" ? C.accent2 : C.text1, align: "center", margin: 0, isTextBox: true });
      s.addText(et[i][1], { x: x - 1.3, y: y0 + 0.85, w: 2.6, h: 0.7, fontSize: 14, color: C.text2, align: "center", valign: "top", margin: 0, isTextBox: true });
    }
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: x0 + pas - 1.0, y: y0 - 1.0, w: 2.0, h: 0.5, rectRadius: 0.25, fill: { color: C.accent2 }, line: { type: "none" } });
    s.addText("Nous sommes ici", { x: x0 + pas - 1.0, y: y0 - 1.0, w: 2.0, h: 0.5, fontSize: 14, bold: true, color: C.background1, align: "center", valign: "middle", margin: 0, isTextBox: true });
    carte(s, M, 4.5, W - 2 * M, 1.9, "Remerciements", { line: C.accent1, lw: 1.5 });
    s.addText([
      { text: "Merci à l'ANAC et aux organisateurs du CECFD 2026", options: { fontSize: 20, bold: true, color: C.text1, breakLine: true } },
      { text: "Questions / Réponses : toute l'équipe SkyVision Togo est à votre écoute.", options: { fontSize: 18, color: C.accent2 } },
    ], { x: M + 0.4, y: 4.65, w: W - 2 * M - 0.8, h: 1.6, margin: 0, valign: "middle", isTextBox: true });
  }

  await pres.writeFile({ fileName: SORTIE });
  if (process.env.APPLY_THEME) await require(process.env.APPLY_THEME).applyTheme(SORTIE, THEME);
  ecrireNotes();
  console.log("ok", SORTIE);
}

function ecrireNotes() {
  const total = DIAPOS.reduce((a, d) => a + d.duree, 0);
  const L = ["# Pitch « Sentinelle Aérienne » (version 9 diapos) — notes d'oral", "",
    "Support : `sentinelle_aerienne_pitch_v2.pptx`. Les mêmes notes sont dans les **notes de l'orateur** de chaque diapo.", "",
    `Durée indicative : **${Math.floor(total / 60)} min ${String(total % 60).padStart(2, "0")}**.`, "",
    "| Diapo | Intervenant | Durée |", "|---|---|---|"];
  DIAPOS.forEach((d, i) => L.push(`| ${i + 1} | ${INTERVENANTS[d.qui].nom}${d.duo ? " puis " + INTERVENANTS[d.duo].nom : ""} | ≈ ${d.duree} s |`));
  L.push("");
  DIAPOS.forEach((d, i) => {
    L.push(`## Diapo ${i + 1} — ${INTERVENANTS[d.qui].court}${d.duo ? " puis " + INTERVENANTS[d.duo].court : ""}`, "");
    for (const p of d.notes.split("\n")) L.push(`> ${p}`, ">");
    L.pop(); L.push("");
  });
  fs.writeFileSync(path.join(RACINE, "notes_oral_v2.md"), L.join("\n"));
}

main().catch((e) => { console.error(e); process.exit(1); });
