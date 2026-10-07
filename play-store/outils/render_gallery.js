// 1) Rend les icones SVG des apps exemples en PNG 512.
// 2) Compose la capture « galerie d'exemples » (1440x2560) en FR et en EN.
// Usage : node render_gallery.js   (apres make_app_icons.py)
const fs = require("fs");
const path = require("path");
const { chromium } = require("playwright");

const ROOT = path.resolve(__dirname, "..");
const ICONS = path.join(ROOT, "assets", "exemples", "icones");

const APPS = [
  { id: "chantierpro", nom: "ChantierPro",
    fr: "Gestion de chantier : planning Gantt, plans annotés, pointage et paie, rapport journalier signé. 100 % hors ligne.",
    en: "Construction management: Gantt planning, annotated plans, timekeeping and payroll, signed daily report. Fully offline." },
  { id: "bonchoix", nom: "Bon Choix",
    fr: "Conseiller d'achat : photographiez l'étiquette ou collez un lien, il compare les offres et vous dit quoi acheter.",
    en: "Shopping advisor: snap the shelf label or paste a link, it compares offers and tells you what to buy." },
  { id: "ping", nom: "Ping Crépuscule",
    fr: "Jeu de ping-pong en 3D au coucher du soleil, avec l'ambiance du public.",
    en: "3D table-tennis game at sunset, crowd sounds included." },
];

const TEXT = {
  fr: { title: "Déjà fabriquées avec AppForge", sub: "De vraies applications, livrées à de vrais clients.", yours: "La vôtre ?", yoursSub: "Décrivez-la. Recevez-la, prête à installer.", out: "assets/screenshots-fr/09-galerie-exemples.png" },
  en: { title: "Already built with AppForge", sub: "Real apps, delivered to real customers.", yours: "Yours?", yoursSub: "Describe it. Get it, ready to install.", out: "assets/screenshots-en/09-gallery-en.png" },
};

function galleryHtml(lang) {
  const t = TEXT[lang];
  const cards = APPS.filter(a => fs.existsSync(path.join(ICONS, a.id + ".svg"))).map(a => `
    <div class="card">
      <img class="ico" src="file://${path.join(ICONS, a.id + ".svg")}">
      <div class="txt"><div class="nom">${a.nom}</div><div class="desc">${a[lang]}</div></div>
    </div>`).join("");
  return `<!doctype html><html lang="${lang}"><head><meta charset="utf-8"><style>
    html,body{margin:0;padding:0}
    body{width:1440px;height:2560px;overflow:hidden;position:relative;color:#fff;
         background:linear-gradient(170deg,#2E2A8C 0%,#4A42D4 50%,#7E3AED 100%);
         font-family:"Inter Display","Inter",system-ui,sans-serif}
    h1{position:absolute;left:0;right:0;top:150px;margin:0;text-align:center;font-size:78px;font-weight:700;letter-spacing:-1px}
    .sub{position:absolute;left:0;right:0;top:262px;text-align:center;font-size:42px;font-weight:500;color:#E8E5FF}
    .cards{position:absolute;left:100px;right:100px;top:520px;display:flex;flex-direction:column;gap:44px}
    .card{display:flex;align-items:center;gap:52px;background:rgba(255,255,255,.96);color:#1A1A2E;border-radius:44px;padding:56px 64px;
          box-shadow:0 30px 60px rgba(10,8,60,.35)}
    .ico{width:220px;height:220px;flex:none}
    .nom{font-size:54px;font-weight:700;margin-bottom:14px;color:#2E2A8C}
    .desc{font-size:34px;line-height:1.3;font-weight:500;color:#3C3C55}
    .yours{border:5px dashed rgba(255,255,255,.75);background:rgba(255,255,255,.10);color:#fff;box-shadow:none}
    .yours .plus{width:220px;height:220px;flex:none;display:flex;align-items:center;justify-content:center;border-radius:48px;background:rgba(255,255,255,.18)}
    .yours .nom{color:#fff}.yours .desc{color:#E8E5FF}
  </style></head><body>
    <h1>${t.title}</h1>
    <div class="sub">${t.sub}</div>
    <div class="cards">${cards}
      <div class="card yours">
        <div class="plus"><svg width="130" height="130" viewBox="0 0 100 100"><path d="M50 14v72M14 50h72" stroke="#fff" stroke-width="12" stroke-linecap="round"/></svg></div>
        <div class="txt"><div class="nom">${t.yours}</div><div class="desc">${t.yoursSub}</div></div>
      </div>
    </div>
  </body></html>`;
}

(async () => {
  const browser = await chromium.launch({ args: ["--no-sandbox"] });
  // 1) icones PNG
  for (const f of fs.readdirSync(ICONS).filter(n => n.endsWith(".svg"))) {
    const page = await browser.newPage({ viewport: { width: 512, height: 512 } });
    const tmp = path.join(ICONS, "_" + f + ".html");
    fs.writeFileSync(tmp, `<html><body style="margin:0;background:transparent"><img src="file://${path.join(ICONS, f)}" width="512" height="512"></body></html>`);
    await page.goto("file://" + tmp);
    await page.waitForTimeout(200);
    await page.screenshot({ path: path.join(ICONS, f.replace(".svg", ".png")), omitBackground: true });
    await page.close();
    fs.unlinkSync(tmp);
    console.log("ok", path.relative(ROOT, path.join(ICONS, f.replace(".svg", ".png"))));
  }
  // 2) galerie FR / EN
  for (const lang of ["fr", "en"]) {
    const tmp = path.join(__dirname, `_gallery_${lang}.html`);
    fs.writeFileSync(tmp, galleryHtml(lang));
    const page = await browser.newPage({ viewport: { width: 1440, height: 2560 }, deviceScaleFactor: 1 });
    await page.goto("file://" + tmp);
    await page.waitForTimeout(300);
    const out = path.join(ROOT, TEXT[lang].out);
    await page.screenshot({ path: out });
    await page.close();
    fs.unlinkSync(tmp);
    console.log("ok", TEXT[lang].out);
  }
  await browser.close();
})();
