// Fabrique les deux PDF a importer dans NotebookLM :
//   video/brief-video-appforge.pdf  (le brief markdown, converti par pandoc)
//   video/visuels-appforge.pdf      (les captures, l'image de presentation, l'exemple Ping Crepuscule)
// Usage : node make_video_pdfs.js
const fs = require("fs");
const path = require("path");
const { execSync } = require("child_process");
const { chromium } = require("playwright");

const ROOT = path.resolve(__dirname, "..");
const VID = path.join(ROOT, "video");
const ASSETS = path.join(ROOT, "assets");

const CSS = `
  @page { size: A4; margin: 16mm; }
  html, body { margin: 0; padding: 0; }
  body { font-family: "Inter", "Inter Display", system-ui, sans-serif; color: #1a1a2e; font-size: 11pt; line-height: 1.45; }
  h1 { font-size: 22pt; line-height: 1.15; margin: 0 0 10pt; color: #2E2A8C; }
  h2 { font-size: 15pt; margin: 18pt 0 6pt; color: #4F46E5; page-break-after: avoid; }
  h3 { font-size: 12pt; margin: 12pt 0 4pt; page-break-after: avoid; }
  p, li { orphans: 3; widows: 3; }
  blockquote { margin: 0 0 10pt; padding: 6pt 10pt; border-left: 3px solid #C7D2FE; background: #F5F3FF; color: #333; }
  table { border-collapse: collapse; width: 100%; margin: 6pt 0 10pt; font-size: 9.5pt; page-break-inside: auto; }
  th, td { border: 1px solid #D4D4E8; padding: 4pt 6pt; vertical-align: top; text-align: left; }
  th { background: #EEF2FF; }
  tr { page-break-inside: avoid; }
  pre { background: #F5F5FA; border: 1px solid #E0E0EE; padding: 8pt; white-space: pre-wrap; font-size: 9.5pt; page-break-inside: avoid; }
  code { font-family: "DejaVu Sans Mono", monospace; font-size: 9.5pt; }
  hr { border: 0; border-top: 1px solid #E0E0EE; margin: 14pt 0; }
  /* document des visuels */
  .page { page-break-after: always; height: 262mm; display: flex; flex-direction: column; }
  .page:last-child { page-break-after: auto; }
  .page h2 { margin: 0 0 6pt; }
  .page .use { font-size: 10pt; color: #444; margin: 0 0 8pt; }
  .page .img { flex: 1; display: flex; align-items: center; justify-content: center; min-height: 0; }
  .page .img img { max-height: 225mm; max-width: 100%; object-fit: contain; border-radius: 6px; box-shadow: 0 2px 10px rgba(0,0,0,.15); }
  .page .wide img { max-height: 110mm; }
  .cover { background: linear-gradient(135deg, #2E2A8C 0%, #4F46E5 52%, #7E3AED 100%); color: #fff; padding: 22mm 18mm; border-radius: 10px; }
  .cover h1 { color: #fff; font-size: 30pt; }
  .cover p { font-size: 13pt; }
  .cover ol { font-size: 12pt; }
  .duo { display: flex; gap: 12mm; align-items: center; justify-content: center; }
  .duo img { max-height: 90mm; max-width: 45%; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,.15); }
`;

function wrap(lang, body) {
  return `<!doctype html><html lang="${lang}"><head><meta charset="utf-8"><style>${CSS}</style></head><body>${body}</body></html>`;
}

async function renderPdf(browser, html, out) {
  const tmp = out.replace(/\.pdf$/, ".html");
  fs.writeFileSync(tmp, html);
  const page = await browser.newPage();
  await page.goto("file://" + tmp);
  await page.waitForTimeout(300);
  await page.pdf({ path: out, format: "A4", printBackground: true, margin: { top: "16mm", bottom: "16mm", left: "16mm", right: "16mm" } });
  await page.close();
  fs.unlinkSync(tmp);
  console.log("ok", path.relative(ROOT, out));
}

(async () => {
  const browser = await chromium.launch({ args: ["--no-sandbox"] });

  // 1) Le brief
  const md = path.join(VID, "brief-video-appforge.md");
  const body = execSync(`pandoc "${md}" -f gfm -t html5`).toString();
  await renderPdf(browser, wrap("fr", body), path.join(VID, "brief-video-appforge.pdf"));

  // 2) Les visuels
  const shots = [
    { f: "screenshots-fr/01-hero.png", n: "Capture 1", t: "Décrivez votre app. Recevez-la, prête à installer.", u: "Vue d'ensemble : la demande et la livraison côte à côte. Script 75 s : 0-5 s." },
    { f: "screenshots-fr/02-decrivez-prix-fixe.png", n: "Capture 2", t: "Décrivez votre application. Le prix est fixé avant de lancer.", u: "Étapes « demande » et « prix fixe » : la demande ChantierPro, la carte « Prix ferme de cette demande » et le bouton Confirmer. Script 30 s : 0-8 s." },
    { f: "screenshots-fr/03-recevez-installez.png", n: "Capture 3", t: "Recevez-la, prête à installer.", u: "Étape « livraison » : « C'est prêt ! », 192 tests automatiques réussis, bouton de téléchargement. Script 30 s : 14-20 s." },
    { f: "screenshots-fr/04-premiere-app-offerte.png", n: "Capture 4", t: "Votre première app est offerte. Mes projets : fabrication en cours.", u: "Étape « fabrication » et étape « offre » : liste des projets (ChantierPro en fabrication, Réservations Restaurant, Quiz Code de la route, Suivi Salle de sport). Script 30 s : 8-14 s." },
    { f: "screenshots-fr/05-exemple-gantt.png", n: "Capture 5", t: "Exemple réel ChantierPro : Gantt et chemin critique.", u: "Étape « exemples ». Script 30 s : 20-26 s." },
    { f: "screenshots-fr/06-exemple-tableau-de-bord.png", n: "Capture 6", t: "Exemple réel ChantierPro : le chantier d'un coup d'œil.", u: "Étape « exemples ». Script 75 s : 38-55 s." },
    { f: "screenshots-fr/07-exemple-plans.png", n: "Capture 7", t: "Exemple réel ChantierPro : plans annotés sur le terrain.", u: "Étape « exemples ». Script 30 s : 20-26 s." },
    { f: "screenshots-fr/08-jeu-3d.png", n: "Capture 8", t: "Même des jeux 3D : Ping Crépuscule, créé avec AppForge.", u: "Étape « exemples » (« et même des jeux 3D »). Capture réelle du jeu, placée dans le cadre des autres captures. Script 30 s : 20-26 s ; script 75 s : 55-63 s." },
    { f: "screenshots-fr/extras/exemple-rapport-signe.png", n: "Extra", t: "Exemple réel ChantierPro : rapport journalier signé.", u: "Étape « exemples », si un plan de plus est utile. Script 75 s : 38-55 s." },
  ];
  let pages = `
  <div class="page"><div class="cover">
    <h1>AppForge<br>Visuels pour la vidéo de présentation</h1>
    <p>Décrivez votre app. Recevez-la, prête à installer. Conçue, fabriquée et testée pour vous. Sans coder.</p>
    <p>Chaque page montre une image à utiliser dans la vidéo, avec l'étape du script à laquelle elle correspond. Les images sont les captures réelles de la fiche Google Play d'AppForge (package com.tipro).</p>
    <ol>
      <li>Vous décrivez votre application en une phrase.</li>
      <li>Un prix fixe vous est annoncé avant de commencer ; rien n'est déduit si vous refusez.</li>
      <li>L'application est fabriquée et testée automatiquement.</li>
      <li>Vous la recevez dans la discussion, prête à installer.</li>
      <li>Vous demandez des retouches dans le même fil.</li>
      <li>Gestion de chantier, visites immobilières, outils du quotidien, jeux 3D : sans écrire une ligne de code.</li>
      <li>Votre première application est offerte. AppForge, sur Google Play.</li>
    </ol>
  </div></div>`;
  for (const s of shots) {
    pages += `<div class="page"><h2>${s.n} — ${s.t}</h2><p class="use">À utiliser pour : ${s.u}</p><div class="img"><img src="file://${path.join(ASSETS, s.f)}"></div></div>`;
  }
  const jeu = ["sources/ping-crepuscule-02.jpg", "sources/ping-crepuscule-04.jpg", "sources/ping-crepuscule-05-cinematique.jpg"].map(f => path.join(ASSETS, f)).filter(fs.existsSync);
  if (jeu.length) {
    pages += `<div class="page"><h2>Ping Crépuscule en jeu — captures brutes du téléphone</h2><p class="use">À utiliser pour : un plan de 2 à 3 secondes de jeu réel à l'étape « exemples » (« et même des jeux 3D »). Jeu de ping-pong 3D au coucher du soleil, public animé, adversaire contrôlé par l'application. Script 30 s : 20-26 s ; script 75 s : 55-63 s.</p><div class="img"><div class="duo">${jeu.map(j => `<img src="file://${j}">`).join("")}</div></div></div>`;
  }
  pages += `<div class="page"><h2>Image de présentation — logo et slogan</h2><p class="use">À utiliser pour : l'étape « offre », la fin de la vidéo (« Votre première application est offerte. AppForge, sur Google Play. »). Script 30 s : 26-30 s.</p><div class="img wide"><img src="file://${path.join(ASSETS, "feature-graphic/feature_fr_1024x500.png")}"></div></div>`;
  const galerie = path.join(ASSETS, "screenshots-fr/09-galerie-exemples.png");
  if (fs.existsSync(galerie)) {
    pages += `<div class="page"><h2>Capture 9 — Déjà fabriquées avec AppForge (galerie d'exemples)</h2><p class="use">À utiliser pour : l'étape « exemples » (« gestion de chantier, conseiller d'achat, jeux 3D… et la vôtre ? »). Les trois icônes sont celles des applications réellement livrées : ChantierPro (gestion de chantier), Bon Choix (conseiller d'achat) et Ping Crépuscule (jeu de ping-pong 3D). Script 30 s : 20-26 s ; script 75 s : 55-63 s.</p><div class="img"><img src="file://${galerie}"></div></div>`;
  }
  await renderPdf(browser, wrap("fr", pages), path.join(VID, "visuels-appforge.pdf"));

  await browser.close();
})();
