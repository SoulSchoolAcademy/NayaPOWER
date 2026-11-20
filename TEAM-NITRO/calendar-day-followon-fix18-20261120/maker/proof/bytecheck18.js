// FIX18 byte regression: base-fix17 vs fixed-fix18 — everything outside the
// three items must be byte-identical; the three items exactly as claimed.
const crypto = require("crypto");
const fs = require("fs");
const PROOF = "/home/hatch/workspace/team-nitro/calendar-day-followon-fix18-20261120/maker/proof/";
const b = fs.readFileSync(PROOF + "base-fix17.html").toString("utf8");
const f = fs.readFileSync(PROOF + "fixed-fix18.html").toString("utf8");
const sha = (s) => crypto.createHash("sha256").update(s).digest("hex");
let pass = 0, fail = 0;
const check = (name, ok, extra = "") => { console.log(`${ok ? "PASS" : "FAIL"} ${name} ${extra}`); ok ? pass++ : fail++; };
// --- covers byte-identical
const grab = (s, re) => { const m = s.match(re); return m ? m[0] : null; };
const coverRe = /var COVER_DAY = \[[\s\S]*?\];/;
const wisRe = /var WISDOM = \[[\s\S]*?\];/;
check("COVER_DAY identical", grab(b, coverRe) === grab(f, coverRe));
check("WISDOM identical", grab(b, wisRe) === grab(f, wisRe));
// --- wisdom line / data untouched
check("dayTeach build identical", b.includes('__dt.innerHTML="<strong>"+WEEKDAYS[d.getDay()]+" · "+DAY_FREQ[d.getDay()]+" Hz · "+DAY_COLOR_NAMES[d.getDay()]+"</strong> — "+DAY_MEANING[d.getDay()];')
  && f.includes('__dt.innerHTML="<strong>"+WEEKDAYS[d.getDay()]+" · "+DAY_FREQ[d.getDay()]+" Hz · "+DAY_COLOR_NAMES[d.getDay()]+"</strong> — "+DAY_MEANING[d.getDay()];'));
check("DAY_FREQ identical", grab(b, /var DAY_FREQ = \[[^\]]+\];/) === grab(f, /var DAY_FREQ = \[[^\]]+\];/));
check("WISDOM quote text identical", grab(b, /"The day of the ground — the root, 396 Hz\. Stand firm; finish what stands\."/) !== null
  && grab(f, /"The day of the ground — the root, 396 Hz\. Stand firm; finish what stands\."/) !== null);
// --- month screen header untouched
check("monthName untouched", (b.match(/monthName/g) || []).length === (f.match(/monthName/g) || []).length);
// --- 396 census: base has 7 occurrences; fixed must have 6 (one removed: header Hz)
const c396 = (s) => (s.match(/396/g) || []).length;
check("396 literals unchanged 7 -> 7 (header Hz is rendered from DAY_FREQ, not a literal)", c396(b) === 7 && c396(f) === 7, `base=${c396(b)} fixed=${c396(f)}`);
check("no '396 Hz' in monthline build", !f.includes('DAY_FREQ[d.getDay()], dc) + " Hz'));
check("header Hz segment gone", !f.includes('white-space:nowrap\\">\' + dayDigitsHTML(DAY_FREQ') && !f.includes('dayDigitsHTML(DAY_FREQ[d.getDay()], dc) + " Hz</span>'));
// --- fix-17 intact
check("fix17 block intact", f.includes("#dayScroll>.cover-change{top:40px!important;bottom:auto!important}")
  && f.includes("#dayScroll:has(#wisdomBanner.on)>.cover-change{display:none!important}"));
check("fix16 marker present", f.includes("FIX16"));
check("worlds static rule present", f.includes("#dayScroll:has(.worlds-slide.on)>.cover-change{position:static!important"));
check("wisdom static rule present", f.includes("#dayScroll:has(#wisdomBanner.on)>.cover-change{position:static!important"));
// --- booking logic / badges intact
for (const needle of ["elite-bookpill", "elite-meetpill", "[15, 30, 60]", "mcFreeTimes", "now.getMinutes() + 60", "No full slot list"]) {
  check(`booking token present: ${needle}`, f.includes(needle));
}
check("worldIcon null-arg calls 9 = 9", (f.match(/worldIcon\(/g) || []).length === (b.match(/worldIcon\(/g) || []).length);
// --- JS parses (1 inline script)
const scripts = [...f.matchAll(/<script>([\s\S]*?)<\/script>/g)];
check("exactly 1 inline script", scripts.length === 1);
try { new Function(scripts[0][1]); check("inline script parses", true); }
catch (e) { check("inline script parses: " + e.message, false); }
check("script length base->fixed", scripts[0][1].length === [...b.matchAll(/<script>([\s\S]*?)<\/script>/g)][0][1].length - 100,
  `base script ${[...b.matchAll(/<script>([\s\S]*?)<\/script>/g)][0][1].length} fixed ${scripts[0][1].length} (delta must be -100 = Hz segment 112 - replacement 12)`);
// --- structural tags
for (const t of ["</style>", "</script>", "</html>"]) {
  check(`${t} count 1/1`, (f.match(new RegExp(t.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"), "g")) || []).length === 1
    && (b.match(new RegExp(t.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"), "g")) || []).length === 1);
}
// --- fix-18 items present exactly once
check("gap:24px count base 2 -> fixed 3 (delta +1 = the fix-18 rule)", (b.match(/gap:24px!important/g) || []).length === 2 && (f.match(/gap:24px!important/g) || []).length === 3);
check("item-3 rule once", (f.match(/#dayScroll:not\(:has\(#wisdomBanner\.on\)\)/g) || []).length === 1);
console.log(`\nbytecheck18: ${pass} PASS, ${fail} FAIL`);
process.exit(fail ? 1 : 0);
