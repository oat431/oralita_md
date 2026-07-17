// pptxgenjs deck template — copy and customize per deck
const pptxgen = require("pptxgenjs");

const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.author = "OraMesLita";
pres.title = "DECK TITLE";

// ── Colors (pick palette per topic domain) ──
const C = {
  darkBg: "0D1117", primary: "238636", secondary: "2EA043", accent: "3FB950",
  lightBg: "F0F7F0", white: "FFFFFF", dark: "1B1F23", muted: "656D76",
  cardBg: "FFFFFF", tableBg: "DAFBE1", tableHead: "238636",
};
const HF = "Georgia", BF = "Calibri";

const mkShadow = () => ({ type: "outer", color: "000000", blur: 4, offset: 2, angle: 135, opacity: 0.1 });

function darkSlide(title, sub) {
  const s = pres.addSlide();
  s.background = { color: C.darkBg };
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.06, fill: { color: C.accent } });
  s.addText(title, { x: 0.8, y: 1.5, w: 8.4, h: 1.2, fontSize: 40, fontFace: HF, color: C.white, bold: true });
  if (sub) s.addText(sub, { x: 0.8, y: 2.8, w: 8.4, h: 0.8, fontSize: 18, fontFace: BF, color: C.accent });
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 5.4, w: 10, h: 0.225, fill: { color: C.accent } });
  return s;
}

function lightSlide(title) {
  const s = pres.addSlide();
  s.background = { color: C.lightBg };
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 0.08, h: 5.625, fill: { color: C.primary } });
  s.addText(title, { x: 0.5, y: 0.25, w: 9, h: 0.6, fontSize: 26, fontFace: HF, color: C.primary, bold: true, margin: 0 });
  s.addShape(pres.shapes.LINE, { x: 0.5, y: 0.9, w: 3, h: 0, line: { color: C.accent, width: 2 } });
  return s;
}

function addCard(s, x, y, w, h, accentColor, items) {
  s.addShape(pres.shapes.RECTANGLE, { x, y, w, h, fill: { color: C.cardBg }, shadow: mkShadow() });
  s.addShape(pres.shapes.RECTANGLE, { x, y, w: 0.06, h, fill: { color: accentColor } });
  s.addText(items, { x: x + 0.2, y: y + 0.1, w: w - 0.35, h: h - 0.2, valign: "top", margin: 0 });
}

// ── Slides go here ──

pres.writeFile({ fileName: "OUTPUT_PATH.pptx" })
  .then(() => console.log("✅ Created: FILENAME.pptx"))
  .catch(err => console.error("❌ Error:", err));
