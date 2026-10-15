// Génère les présentations du pitch à partir des fichiers de contenu.
//   node pitch/outils/generer.js            -> les deux versions
//   node pitch/outils/generer.js court      -> version 9 diapos seulement
// Modules : pptxgenjs, sharp. APPLY_THEME=<chemin de apply_theme.js> pour écrire les couleurs du thème.
//
// Style volontairement sobre : fond blanc, captures SolidWorks, une seule couleur d'accent,
// pas de pictogrammes décoratifs.

const path = require("path");
const fs = require("fs");
const pptxgen = require("pptxgenjs");
const sharp = require("sharp");

const RACINE = path.resolve(__dirname, "..");
const CAO = path.join(RACINE, "assets", "cao");

const VERSIONS = {
  court: { contenu: "./contenu_court", pptx: "sentinelle_aerienne_pitch_court.pptx", script: "script_oral_court.md" },
  complet: { contenu: "./contenu_complet", pptx: "sentinelle_aerienne_pitch_complet.pptx", script: "script_oral_complet.md" },
  risques: { contenu: "./contenu_risques", pptx: "sentinelle_aerienne_risques_securite.pptx", script: "script_oral_risques.md" },
};

const THEME = {
  name: "Sentinelle Aerienne",
  headFontFace: "Calibri",
  bodyFontFace: "Calibri",
  colors: {
    dk1: "1F2933", lt1: "FFFFFF", dk2: "5B6770", lt2: "F2F4F6",
    accent1: "0B6E4F", accent2: "D9A400", accent3: "B5322E", accent4: "2F5D8A",
    accent5: "D3D9DE", accent6: "8A98A4", hlink: "0B6E4F", folHlink: "2F5D8A",
  },
};
const HEX = THEME.colors;
const W = 13.333, H = 7.5, M = 0.65;

async function construire(cle) {
  const v = VERSIONS[cle];
  const { INTERVENANTS, DIAPOS } = require(v.contenu);
  const pres = new pptxgen();
  pres.layout = "LAYOUT_WIDE";
  pres.title = "Sentinelle Aérienne, SkyVision Togo";
  pres.author = "SkyVision Togo";
  pres.company = "SkyVision Togo";
  pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
  const C = pres.SchemeColor;

  // Tailles des images, pour les placer sans les déformer.
  const tailles = {};
  for (const f of fs.readdirSync(CAO).filter((f) => f.endsWith(".png"))) {
    const m = await sharp(path.join(CAO, f)).metadata();
    tailles[f.replace(".png", "")] = m.width / m.height;
  }

  pres.defineSlideMaster({ title: "COUVERTURE", background: { color: C.background1 }, objects: [] });
  pres.defineSlideMaster({
    title: "CONTENU",
    background: { color: C.background1 },
    margin: [0.4, M, 0.7, M],
    objects: [
      { placeholder: { options: { name: "title", type: "title", x: M, y: 0.45, w: W - 2 * M, h: 0.75, fontSize: 30, bold: true, color: C.text1, align: "left", valign: "middle", margin: 0 }, text: "" } },
      { line: { x: M, y: H - 0.62, w: W - 2 * M, h: 0, line: { color: C.accent5, width: 0.75 } } },
      { text: { text: "SkyVision Togo · Sentinelle Aérienne · CECFD 2026", options: { x: M, y: H - 0.52, w: 6, h: 0.3, fontSize: 10, color: C.text2, margin: 0 } } },
    ],
    slideNumber: { x: W - M - 0.4, y: H - 0.52, w: 0.4, h: 0.3, fontSize: 10, color: C.text2, align: "right", margin: 0 },
  });

  // ---------- briques ----------
  const texte = (s, t, o) => s.addText(t, { margin: 0, isTextBox: true, ...o });

  function puces(items, taille = 17, couleur = C.text1) {
    // item : "texte" (puce) ou ["en gras", "suite"] (paragraphe sans puce, début en gras)
    return items.map((it, i) => {
      const fin = i < items.length - 1;
      if (Array.isArray(it)) {
        return [
          { text: it[0], options: { bold: true, color: couleur, fontSize: taille } },
          { text: " : " + it[1], options: { color: couleur, fontSize: taille, breakLine: fin } },
        ];
      }
      return [{ text: it, options: { color: couleur, fontSize: taille, bullet: { indent: 18 }, breakLine: fin } }];
    }).flat();
  }

  function blocPuces(s, x, y, w, h, titre, items, taille = 17) {
    let y0 = y;
    if (titre) {
      texte(s, titre, { x, y, w, h: 0.4, fontSize: 18, bold: true, color: C.accent1 });
      y0 += 0.5;
    }
    texte(s, puces(items, taille), { x, y: y0, w, h: h - (y0 - y), valign: "top", paraSpaceAfter: 8 });
  }

  function image(s, nom, x, y, w, h, legende, cadre = true) {
    // Ajuste l'image dans la boîte (x, y, w, h) en gardant ses proportions, centrée.
    const r = tailles[nom];
    let iw = w, ih = w / r;
    if (ih > h) { ih = h; iw = h * r; }
    const ix = x + (w - iw) / 2, iy = y + (h - ih) / 2;
    s.addImage({ path: path.join(CAO, nom + ".png"), x: ix, y: iy, w: iw, h: ih, altText: legende || "Vue CAO du drone" });
    if (cadre) s.addShape(pres.shapes.RECTANGLE, { x: ix, y: iy, w: iw, h: ih, fill: { type: "none" }, line: { color: C.accent5, width: 0.75 }, objectName: "Cadre " + nom });
    if (legende) texte(s, legende, { x: ix, y: iy + ih + 0.06, w: iw, h: 0.28, fontSize: 11, color: C.text2, italic: true });
  }

  function boite(s, x, y, w, h, nom) {
    s.addShape(pres.shapes.RECTANGLE, { x, y, w, h, fill: { color: C.background2 }, line: { color: C.accent5, width: 0.75 }, objectName: nom });
  }

  function fleche(s, x, y, w, double = false) {
    s.addShape(pres.shapes.LINE, { x, y, w, h: 0, line: { color: C.text2, width: 1.5, endArrowType: "triangle", beginArrowType: double ? "triangle" : undefined } });
  }

  function tableau(s, entetes, lignes, o) {
    const e = entetes.map((t) => ({ text: t, options: { bold: true, color: C.accent1, fill: { color: C.background2 } } }));
    const corps = lignes.map((l) => l.map((t, j) => ({ text: t, options: { color: C.text1, bold: j === 0 && o.premiereGras !== false } })));
    s.addTable([e, ...corps], {
      x: o.x ?? M, y: o.y, w: o.w ?? W - 2 * M, colW: o.colW, fontSize: o.taille ?? 15, rowH: o.rowH ?? 0.5,
      valign: "middle", margin: [0.04, 0.12, 0.04, 0.12],
      border: [{ type: "none" }, { type: "none" }, { type: "solid", pt: 0.75, color: HEX.accent5 }, { type: "none" }],
    });
  }

  function frise(s, etapes, y0) {
    const n = etapes.length, x0 = M + 1.3, pas = (W - 2 * M - 2.6) / (n - 1);
    s.addShape(pres.shapes.LINE, { x: x0, y: y0, w: pas * (n - 1), h: 0, line: { color: C.accent5, width: 2 } });
    etapes.forEach(([date, txt, etat], i) => {
      const x = x0 + i * pas;
      const plein = etat === "fait" ? C.accent1 : etat === "ici" ? C.accent2 : C.background1;
      s.addShape(pres.shapes.OVAL, { x: x - 0.14, y: y0 - 0.14, w: 0.28, h: 0.28, fill: { color: plein }, line: { color: etat ? plein : C.accent6, width: 1.5 } });
      texte(s, date + (etat === "ici" ? " (en cours)" : ""), { x: x - 1.25, y: y0 + 0.3, w: 2.5, h: 0.4, fontSize: 16, bold: true, color: C.text1, align: "center" });
      texte(s, txt, { x: x - 1.25, y: y0 + 0.72, w: 2.5, h: 0.9, fontSize: 14, color: C.text2, align: "center", valign: "top" });
    });
  }

  function chaine(s, etapes, y, h = 1.15) {
    const n = etapes.length, gap = 0.32, bw = (W - 2 * M - gap * (n - 1)) / n;
    etapes.forEach(([t, d], i) => {
      const x = M + i * (bw + gap);
      boite(s, x, y, bw, h, "Étape " + (i + 1));
      texte(s, [
        { text: t, options: { bold: true, fontSize: 15, color: C.text1, breakLine: true } },
        { text: d, options: { fontSize: 12, color: C.text2 } },
      ], { x: x + 0.1, y: y + 0.08, w: bw - 0.2, h: h - 0.16, align: "center", valign: "middle" });
      if (i < n - 1) fleche(s, x + bw + 0.04, y + h / 2, gap - 0.08);
    });
  }

  function intervenant(s, d) {
    const noms = [d.qui, d.duo].filter(Boolean).map((q) => INTERVENANTS[q].nomCourt);
    texte(s, noms.join(" et "), { x: W - M - 5.0, y: H - 0.52, w: 4.45, h: 0.3, fontSize: 10, color: C.text2, align: "right" });
  }

  function notes(s, d) {
    const qui = [d.qui, d.duo].filter(Boolean).map((q) => INTERVENANTS[q].nomCourt).join(" puis ");
    s.addNotes(`${qui} (environ ${d.duree} s)\n\n${d.notes}`);
  }

  // ---------- types de diapos ----------
  const RENDU = {
    couverture(s, d) {
      texte(s, d.ligne, { x: M, y: 0.7, w: 7, h: 0.35, fontSize: 14, bold: true, color: C.accent1 });
      texte(s, d.titre, { x: M, y: 1.15, w: 7, h: 1.0, fontSize: 48, bold: true, color: C.text1 });
      texte(s, d.sous, { x: M, y: 2.2, w: 5.9, h: 1.2, fontSize: 20, color: C.text2, valign: "top" });
      if (d.equipe) image(s, d.image, 7.0, 0.6, W - M - 7.0, 3.0, null, false);
      else image(s, d.image, 7.0, 0.9, W - M - 7.0, 5.2, null, false);
      if (d.equipe) {
        const lignes = d.equipe.map((q) => [INTERVENANTS[q].nom, INTERVENANTS[q].pole]);
        tableau(s, ["Équipe", "Pôle"], lignes, { y: 3.85, colW: [4.6, W - 2 * M - 4.6], rowH: 0.48, taille: 14 });
      }
      if (d.bas) texte(s, d.bas, { x: M, y: 6.6, w: W - 2 * M, h: 0.4, fontSize: 14, color: C.text2 });
    },
    deux_colonnes(s, d) {
      const w = (W - 2 * M - 0.6) / 2, h = d.hColonnes || (d.bas ? 3.6 : 4.9);
      d.colonnes.forEach((c, i) => blocPuces(s, M + i * (w + 0.6), 1.55, w, h, c.titre, c.puces, c.taille || 17));
      if (d.bas) {
        const yb = 1.55 + h + 0.2;
        boite(s, M, yb, W - 2 * M, 0.75, "Encadré");
        texte(s, d.bas, { x: M + 0.25, y: yb, w: W - 2 * M - 0.5, h: 0.75, fontSize: 17, color: C.text1, valign: "middle" });
      }
      if (d.tableau) {
        const t = d.tableau, yt = 1.55 + h + 0.25;
        texte(s, t.titre, { x: M, y: yt, w: W - 2 * M, h: 0.4, fontSize: 18, bold: true, color: C.accent1 });
        tableau(s, t.entetes, t.lignes, { y: yt + 0.5, colW: t.colW, rowH: 0.45, taille: 14 });
      }
    },
    texte_image(s, d) {
      const wt = d.largeurTexte || 5.6;
      let y = 1.55;
      for (const b of d.blocs) {
        blocPuces(s, M, y, wt, b.h, b.titre, b.puces, b.taille || 17);
        y += b.h + 0.15;
      }
      const xi = M + wt + 0.45, wi = W - M - xi;
      const n = d.images.length, hi = (4.95 - (n - 1) * 0.45) / n;
      d.images.forEach((im, i) => image(s, im.f, xi, 1.55 + i * (hi + 0.45), wi, hi - 0.3, im.legende));
    },
    double_coeur(s, d) {
      const bw = 5.0, y = 1.55, bh = 2.9;
      d.blocs.forEach((b, i) => {
        const x = i === 0 ? M : W - M - bw;
        boite(s, x, y, bw, bh, b.titre);
        texte(s, [
          { text: b.titre, options: { bold: true, fontSize: 19, color: C.accent1, breakLine: true } },
          { text: b.sous, options: { fontSize: 14, color: C.text2 } },
        ], { x: x + 0.25, y: y + 0.15, w: bw - 0.5, h: 0.8 });
        texte(s, puces(b.puces, 15), { x: x + 0.25, y: y + 1.05, w: bw - 0.5, h: bh - 1.15, valign: "top", paraSpaceAfter: 4 });
      });
      const mx = M + bw + 0.25, mw = W - 2 * M - 2 * bw - 0.5;
      texte(s, d.lien, { x: mx, y: y + 0.75, w: mw, h: 0.35, fontSize: 15, bold: true, color: C.text1, align: "center" });
      fleche(s, mx, y + 1.25, mw, true);
      texte(s, d.lienDetail, { x: mx, y: y + 1.4, w: mw, h: 0.9, fontSize: 12, color: C.text2, align: "center", valign: "top" });
      blocPuces(s, M, 4.7, W - 2 * M, 1.6, d.basTitre, d.basPuces, 16);
      if (d.note) texte(s, d.note, { x: M, y: 6.45, w: W - 2 * M, h: 0.3, fontSize: 12, italic: true, color: C.text2 });
    },
    chaine(s, d) {
      chaine(s, d.etapes, 1.6);
      const w = (W - 2 * M - 0.6) / 2;
      d.colonnes.forEach((c, i) => blocPuces(s, M + i * (w + 0.6), 3.15, w, 3.3, c.titre, c.puces, 16));
    },
    liste_num(s, d) {
      const wt = d.image ? 7.0 : W - 2 * M;
      d.items.forEach(([t, desc], i) => {
        const y = 1.6 + i * 1.18;
        texte(s, String(i + 1), { x: M, y, w: 0.5, h: 0.5, fontSize: 26, bold: true, color: C.accent1 });
        texte(s, [
          { text: t, options: { bold: true, fontSize: 19, color: C.text1, breakLine: true } },
          { text: desc, options: { fontSize: 15, color: C.text2 } },
        ], { x: M + 0.6, y: y + 0.02, w: wt - 0.6, h: 1.05, valign: "top" });
      });
      if (d.image) image(s, d.image.f, M + wt + 0.35, 1.7, W - 2 * M - wt - 0.35, 3.6, d.image.legende);
    },
    tableau(s, d) {
      let y = 1.6;
      if (d.intro) { texte(s, d.intro, { x: M, y, w: W - 2 * M, h: 0.5, fontSize: 17, color: C.text2 }); y += 0.65; }
      const wt = d.image ? 7.6 : W - 2 * M;
      tableau(s, d.entetes, d.lignes, { y, w: wt, colW: d.colW, rowH: d.rowH, taille: d.taille, premiereGras: d.premiereGras });
      if (d.image) image(s, d.image.f, M + wt + 0.4, y, W - 2 * M - wt - 0.4, 3.2, d.image.legende);
      const yFin = y + (d.rowH ?? 0.5) * (d.lignes.length + 1);
      if (d.bas) texte(s, d.bas, { x: M, y: yFin + 0.35, w: W - 2 * M, h: 0.45, fontSize: 16, color: C.text2 });
      if (d.imageBas) {
        const yi = yFin + (d.bas ? 1.0 : 0.4);
        image(s, d.imageBas.f, M, yi, W - 2 * M, H - 0.75 - yi - 0.4, d.imageBas.legende);
      }
    },
    frise(s, d) {
      frise(s, d.etapes, 2.3);
      if (d.fin) {
        boite(s, M, 4.6, W - 2 * M, 1.6, "Remerciements");
        texte(s, [
          { text: d.fin[0], options: { bold: true, fontSize: 21, color: C.text1, breakLine: true } },
          { text: d.fin[1], options: { fontSize: 17, color: C.text2 } },
        ], { x: M + 0.35, y: 4.6, w: W - 2 * M - 0.7, h: 1.6, valign: "middle" });
      }
    },
    fin(s, d) {
      texte(s, d.titre, { x: M, y: 1.0, w: 6.2, h: 0.8, fontSize: 36, bold: true, color: C.text1 });
      texte(s, puces(d.puces, 20), { x: M, y: 2.0, w: 6.0, h: 2.6, valign: "top", paraSpaceAfter: 10 });
      image(s, d.image, 7.0, 1.0, W - M - 7.0, 3.6, null, false);
      texte(s, d.merci, { x: M, y: 5.3, w: W - 2 * M, h: 0.6, fontSize: 26, bold: true, color: C.accent1 });
      if (d.bas) texte(s, d.bas, { x: M, y: 5.95, w: W - 2 * M, h: 0.4, fontSize: 16, color: C.text2 });
    },
  };

  let section = null;
  for (const d of DIAPOS) {
    if (d.section && d.section !== section) { section = d.section; pres.addSection({ title: section }); }
    const couverture = d.type === "couverture" || d.type === "fin";
    const s = pres.addSlide({ masterName: couverture ? "COUVERTURE" : "CONTENU", sectionTitle: section });
    if (!couverture) { s.addText(d.titre, { placeholder: "title" }); intervenant(s, d); }
    RENDU[d.type](s, d);
    notes(s, d);
  }

  const sortie = path.join(RACINE, v.pptx);
  await pres.writeFile({ fileName: sortie });
  if (process.env.APPLY_THEME) await require(process.env.APPLY_THEME).applyTheme(sortie, THEME);
  ecrireScript(v, INTERVENANTS, DIAPOS);
  console.log("ok", sortie);
}

function ecrireScript(v, INTERVENANTS, DIAPOS) {
  const total = DIAPOS.reduce((a, d) => a + d.duree, 0);
  const L = [`# Pitch Sentinelle Aérienne : script oral (${DIAPOS.length} diapos)`, "",
    `Support : \`${v.pptx}\`. Le même texte se trouve dans les notes de l'orateur de chaque diapo.`, "",
    `Durée indicative : environ ${Math.round(total / 60)} minutes.`, "",
    "| Diapo | Titre | Qui parle | Durée |", "|---|---|---|---|"];
  DIAPOS.forEach((d, i) => L.push(`| ${i + 1} | ${d.titre} | ${[d.qui, d.duo].filter(Boolean).map((q) => INTERVENANTS[q].nomCourt).join(" puis ")} | ${d.duree} s |`));
  L.push("");
  DIAPOS.forEach((d, i) => {
    L.push(`## ${i + 1}. ${d.titre} (${[d.qui, d.duo].filter(Boolean).map((q) => INTERVENANTS[q].nomCourt).join(" puis ")})`, "");
    for (const p of d.notes.split("\n")) L.push(p, "");
  });
  fs.writeFileSync(path.join(RACINE, v.script), L.join("\n"));
}

(async () => {
  const demande = process.argv[2];
  for (const cle of Object.keys(VERSIONS)) if (!demande || demande === cle) await construire(cle);
})().catch((e) => { console.error(e); process.exit(1); });
