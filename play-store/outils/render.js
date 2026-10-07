// Rend les fichiers HTML (image de presentation, icones) en PNG avec Chromium.
// Usage : node render.js   (depuis n'importe quel dossier)
const path = require("path");
const { chromium } = require("playwright");

const ROOT = path.resolve(__dirname, "..");
const jobs = [
  { html: "feature_fr.html", w: 1024, h: 500, out: "assets/feature-graphic/feature_fr_1024x500.png" },
  { html: "feature_en.html", w: 1024, h: 500, out: "assets/feature-graphic/feature_en_1024x500.png" },
  { html: "icon_a_bulle.html", w: 512, h: 512, out: "assets/icon/icon_a_bulle_512.png" },
  { html: "icon_b_enclume.html", w: 512, h: 512, out: "assets/icon/icon_b_enclume_512.png" },
];

(async () => {
  const browser = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" + "", args: ["--no-sandbox"] }).catch(() => chromium.launch({ args: ["--no-sandbox"] }));
  for (const j of jobs) {
    const page = await browser.newPage({ viewport: { width: j.w, height: j.h }, deviceScaleFactor: 1 });
    await page.goto("file://" + path.join(__dirname, j.html));
    await page.waitForTimeout(300);
    await page.screenshot({ path: path.join(ROOT, j.out), type: "png", omitBackground: false });
    await page.close();
    console.log("ok", j.out);
  }
  await browser.close();
})();
