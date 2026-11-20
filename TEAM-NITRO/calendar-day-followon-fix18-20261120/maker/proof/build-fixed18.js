// FIX18 build: fixed = base-fix17 + fix18-block before </style> + Hz-segment
// deletion from the hl-monthline build string (Buffer ops, exact bytes).
const crypto = require("crypto");
const fs = require("fs");
const PROOF = "/home/hatch/workspace/team-nitro/calendar-day-followon-fix18-20261120/maker/proof/";
const base = fs.readFileSync(PROOF + "base-fix17.html");
const block = fs.readFileSync(PROOF + "fix18-block.css");
const shaOf = (b) => crypto.createHash("sha256").update(b).digest("hex");
console.log(`BASE ${base.length} sha256=${shaOf(base)}`);
if (shaOf(base) !== "1f798b65dfa557a4e4e20472e3d56e2bda29fd69912481338b3bb6b2bc602887") {
  console.error("BASE SHA MISMATCH — stop"); process.exit(1);
}
// --- Item 2: delete the Hz segment from the monthline build (base line 4219).
// File bytes (JS source):  + " \u00b7 <span style=\"white-space:nowrap\">" +
//   dayDigitsHTML(DAY_FREQ[d.getDay()], dc) + " Hz</span></span>"
// Replaced with:  + '</span>'   (closes .hl-monthline; the space after the
// script </span> is kept — harmless in the flex monthline, graceful if CSS fails).
const HZ_OLD = ' + " \\u00b7 <span style=\\"white-space:nowrap\\">" + dayDigitsHTML(DAY_FREQ[d.getDay()], dc) + " Hz</span></span>"';
const HZ_NEW = " + '</span>'";
const oldBuf = Buffer.from(HZ_OLD, "utf8");
let count = 0, pos = -1;
while ((pos = base.indexOf(oldBuf, pos + 1)) !== -1) count++;
console.log("Hz-segment occurrences in base:", count);
if (count !== 1) { console.error("Hz segment must occur exactly once — stop"); process.exit(1); }
const noHz = Buffer.concat([base.subarray(0, base.indexOf(oldBuf)), Buffer.from(HZ_NEW, "utf8"),
  base.subarray(base.indexOf(oldBuf) + oldBuf.length)]);
console.log(`after Hz deletion: ${noHz.length} B (base ${base.length} - ${oldBuf.length} + ${Buffer.from(HZ_NEW).length})`);
// --- Items 1+3: append the fix-18 CSS block before </style> (after fix-17 block).
const marker = Buffer.from("</style>");
const idx = noHz.lastIndexOf(marker);
if (idx < 0) { console.error("no </style>"); process.exit(1); }
const fixed = Buffer.concat([noHz.subarray(0, idx), block, Buffer.from("\n"), noHz.subarray(idx)]);
console.log(`FIXED ${fixed.length} sha256=${shaOf(fixed)}`);
// --- Scope proof: fixed minus block, with Hz segment re-inserted, == base.
const minusBlock = Buffer.concat([fixed.subarray(0, idx), fixed.subarray(idx + block.length + 1)]);
// Re-insert the Hz segment at the UNIQUE year anchor (plain " + '</span>'"
// occurs 17 times in the file; the year anchor occurs once).
const YEAR_ANCHOR = Buffer.from("dayDigitsHTML(d.getFullYear(), dc) + '</span>'", "utf8");
const anchorAt = minusBlock.indexOf(YEAR_ANCHOR);
if (anchorAt < 0) { console.error("year anchor not found — stop"); process.exit(1); }
const reinsertAt = anchorAt + Buffer.from("dayDigitsHTML(d.getFullYear(), dc)", "utf8").length;
const rebuilt = Buffer.concat([minusBlock.subarray(0, reinsertAt), oldBuf,
  minusBlock.subarray(reinsertAt + Buffer.from(HZ_NEW, "utf8").length)]);
console.log("fixed-minus-block + Hz-reinsert == base:", rebuilt.equals(base));
const s = fixed.toString("utf8"), b = base.toString("utf8");
console.log("FIX18 marker count:", (s.match(/FIX18/g) || []).length);
console.log("Hz segment in fixed:", (s.match(/DAY_FREQ\[d\.getDay\(\)\], dc\) \+ " Hz/g) || []).length, "(must be 0)");
console.log("monthline build in fixed has year only:", s.includes("dayDigitsHTML(d.getFullYear(), dc) + '</span>'"));
console.log("fix-17 block intact:", s.includes("#dayScroll>.cover-change{top:40px!important;bottom:auto!important}"));
console.log("wisdom hide intact:", s.includes("#dayScroll:has(#wisdomBanner.on)>.cover-change{display:none!important}"));
console.log("gap rule present:", (s.match(/\.hl-center \.hl-monthline\{display:inline-flex!important;align-items:center!important;gap:24px!important;white-space:nowrap!important\}/g) || []).length);
console.log("item-3 rule present:", (s.match(/#dayScroll:not\(:has\(#wisdomBanner\.on\)\):not\(:has\(\.worlds-slide\.on\)\)>\.cover-change\{display:none!important\}/g) || []).length);
console.log("script tags fixed/base:", (s.match(/<script/g) || []).length, (b.match(/<script/g) || []).length);
fs.writeFileSync(PROOF + "fixed-fix18.html", fixed);
const reread = fs.readFileSync(PROOF + "fixed-fix18.html");
console.log("wrote fixed-fix18.html:", reread.length, "sha match:", shaOf(reread) === shaOf(fixed));
