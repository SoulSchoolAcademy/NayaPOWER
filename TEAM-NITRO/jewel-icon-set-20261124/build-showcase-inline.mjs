// build-showcase-inline.mjs — fix round 2026-11-24 (checker item 1, BLOCKER).
// The proof host serves one file per ?file= URL: relative refs inside the
// showcase (59 <img> + jewel-icons.css) resolve to the host root WITHOUT
// the ?file=/ref=/cb= params and 400 — the staged page as linked showed
// ZERO icons. So the STAGED showcase is a single self-contained file:
// every SVG and the CSS inlined into showcase.html.
// The human-editable template stays in showcase-template.html (same refs,
// readable); re-run this script after any template edit:
//   node build-showcase-inline.mjs
// The standalone SVG files remain the consumable assets — inlining is
// staging-only, so consumers still take the files, not the showcase.
// Note: the same icon file is inlined several times (mail in §1 and §2,
// type-chat-sm five times in the ladder). Its gradient ids repeat
// verbatim — the definitions are byte-identical, so the render is the
// same; only the first copy's ids resolve, which is harmless here.
import { readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = dirname(fileURLToPath(import.meta.url));
let html = readFileSync(join(ROOT, "showcase-template.html"), "utf8");

// Inline the touch-contract CSS.
const css = readFileSync(join(ROOT, "jewel-icons.css"), "utf8");
if (!html.includes('<link rel="stylesheet" href="jewel-icons.css">'))
  throw new Error("css link not found in template");
html = html.replace('<link rel="stylesheet" href="jewel-icons.css">',
  `<style>\n${css}\n</style>`);

// Inline every real <img src="icons/...">. The escaped &lt;img example in
// the §5 text is not a tag and is left alone.
const imgRe = /<img src="(icons\/[^"]+\.svg)" alt="([^"]*)">/g;
let n = 0;
const missing = [];
html = html.replace(imgRe, (m, src) => {
  try {
    n++;
    return readFileSync(join(ROOT, src), "utf8").trim();
  } catch {
    missing.push(src);
    return m;
  }
});
if (missing.length) throw new Error("missing SVGs: " + missing.join(", "));
if (/<img src="icons\//.test(html))
  throw new Error("un-inlined img refs remain");
if (html.includes('href="jewel-icons.css"'))
  throw new Error("css link remains");

html = html.replace("</head>",
  "<!-- Staged showcase: self-contained — all icons + jewel-icons.css inlined (the proof host serves one ?file= URL; relative refs 400 there). Edit showcase-template.html, then re-run: node build-showcase-inline.mjs. -->\n</head>");
writeFileSync(join(ROOT, "showcase.html"), html);
console.log(`showcase.html written: ${html.length}B, ${n} SVGs inlined, 0 external refs`);
