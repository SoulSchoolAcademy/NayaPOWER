/* Acceptance harness for mission-view.html — runs the page's OWN render code
   (extracted from the artifact) against the real published WORK-ITEMS.json
   plus adversarial fixtures. No DOM, no network. Exit 1 on any failure. */
"use strict";
const fs = require("fs");
const vm = require("vm");
const path = require("path");

const HERE = __dirname;
const html = fs.readFileSync(path.join(HERE, "mission-view.html"), "utf8");
const data = JSON.parse(fs.readFileSync((process.argv[2] || path.join(HERE, "work-items.snapshot.json")), "utf8"));

let pass = 0, fail = 0;
function ok(name, cond, extra) {
  if (cond) { pass++; console.log("PASS  " + name); }
  else { fail++; console.log("FAIL  " + name + (extra ? "  -- " + extra : "")); }
}

/* ---------- artifact-level invariants ---------- */
ok("title is the canonical room title", html.includes("<title>Mission — NayaNET Intelligent Hub</title>"));
ok("self-contained: no external script/link resources",
   !/<script[^>]+src=/.test(html) && !/<link[^>]+href=/.test(html));
ok("no baked registry data in the artifact (no silent fallback possible)",
   !html.includes("LL-015") && !html.includes("GT-039 — fitted"));
ok("data URL is the state-core published WORK-ITEMS.json",
   html.includes("raw.githubusercontent.com/SoulSchoolAcademy/NayaPOWER/live/mission-state/WORK-ITEMS.json"));

/* ---------- load the page's render code ---------- */
const m = html.match(/<script>([\s\S]*?)<\/script>/);
ok("script block extractable", !!m);
const ctx = vm.createContext({ console, setInterval: () => {}, fetch: () => Promise.reject(new Error("no net in harness")) });
vm.runInContext(m[1], ctx);
ok("buildHTML exposed", typeof ctx.buildHTML === "function");
ok("errorHTML exposed", typeof ctx.errorHTML === "function");

const GEN = Date.parse(data.generated_utc); // 2026-10-23T01:07:00Z
const NOW = GEN + 5 * 60 * 1000;            // 5 minutes after publish = fresh

/* ---------- scenario 1: real published data, fresh ---------- */
const h = ctx.buildHTML(data, NOW, "All");
const articles = (h.match(/<article class="item/g) || []).length;
ok("renders every item (32 in sections + 5 up-next repeats = 37)", articles === 37, "got " + articles);
data.items.forEach(i => ok("renders title " + i.id, h.includes(ctx.esc(i.title))));
ok("freshness line names the publisher timestamp", h.includes("2026-10-23 01:07 UTC") && h.includes("5 minutes ago"));
ok("no STALE banner when fresh", /data-part="stale" class=""/.test(h));
const countsOk = [["QUEUED",15],["IN PROGRESS",7],["VERIFYING",3],["DONE+PROVEN",3],["BLOCKED",2],["NEEDS SHAWN",2],["CLAIMED",0]]
  .every(([s,n]) => h.includes("<b>" + n + "</b>" + s));
ok("counts strip matches the registry counts", countsOk);
/* done items carry resolving proof links */
["2945","2946","2947"].forEach(pr =>
  ok("DONE proof link present for PR #" + pr,
     h.includes('<a href="https://github.com/SoulSchoolAcademy/NayaPOWER/pull/' + pr + '">')));
/* blocked items name blocker + owner */
ok("LL-001 blocker + owner rendered",
   h.includes("Fitted per-table policies not yet delivered") && h.includes("Unblock owner:</b> Nitro lane"));
ok("LL-010 blocker + owner rendered",
   h.includes("registered twice with different content hashes") && h.includes("Unblock owner:</b> Kappa lane"));
/* up-next is the top of the queue, in rank order */
const upNext = h.split('data-section="needs"')[0];
const order = ["LL-001","GT-039","Production tap","Accountability Ledger","THE LIVING LIST","Command + universal"];
let last = -1, ordered = true;
["GT-039 — fitted", "Production tap — apply", "Accountability Ledger — database", "THE LIVING LIST — this registry", "Command + universal search"]
  .forEach(t => { const i = upNext.indexOf(t); if (i < last) ordered = false; last = i; });
ok("Up Next strip is ranks 1-5 in order", ordered && upNext.includes('data-part="counts"'));
/* stalled + drift are loud */
ok("stalled claim flagged", h.includes("STALLED — no movement for 2h+"));
ok("drift flagged (PR #2939 merged-but-IN-PROGRESS)", h.includes("pr-merged-state-lags: PR #2939 is MERGED"));
/* events stream renders */
ok("recent movement renders state changes", h.includes("Recent movement") && h.includes("IN PROGRESS") && h.includes("→"));

/* ---------- scenario 2: stale publisher ---------- */
const hStale = ctx.buildHTML(data, GEN + 2 * 60 * 60 * 1000, "All");
ok("STALE banner shows when publisher is 2h old", /data-part="stale" class="show"/.test(hStale) && hStale.includes("STALE —"));

/* ---------- scenario 3: DONE without proof (registry-law violation) ---------- */
const bad = JSON.parse(JSON.stringify(data));
bad.items.find(i => i.id === "LL-015").proof = null;
const hBad = ctx.buildHTML(bad, NOW, "All");
ok("DONE without proof renders UNVERIFIED + law flag",
   hBad.includes("Registry law violated: marked DONE+PROVEN without a resolving proof link") && hBad.includes(">UNVERIFIED<"));
ok("law-breaking item loses the proven styling", hBad.includes('class="item s-law"'));
const bad2 = JSON.parse(JSON.stringify(data));
bad2.items.find(i => i.id === "LL-001").blocker_owner = null;
ok("BLOCKED without owner renders law flag",
   ctx.buildHTML(bad2, NOW, "All").includes("Registry law violated: BLOCKED without a named blocker and owner."));

/* ---------- scenario 4: program filter = THE LIST (#2953) set ---------- */
const hBob = ctx.buildHTML(data, NOW, "Best-of-Best");
const bobArticles = (hBob.match(/<article class="item/g) || []).length;
ok("Best-of-Best filter shows exactly the 23 items of THE LIST #2953", bobArticles === 23, "got " + bobArticles);
ok("filter hides other programs", !hBob.includes("GT-039 — fitted"));

/* ---------- scenario 5: fetch failure = loud error, zero items ---------- */
const hErr = ctx.errorHTML(new Error("HTTP 503"));
ok("error render is loud and carries zero items",
   hErr.includes("could not be read") && !(hErr.includes("<article")));

/* ---------- scenario 6: hostile text is escaped ---------- */
const evil = JSON.parse(JSON.stringify(data));
evil.items[0].title = '<script>alert(1)</script>';
const hEvil = ctx.buildHTML(evil, NOW, "All");
ok("item text is HTML-escaped", hEvil.includes("&lt;script&gt;alert(1)") && !hEvil.includes("<script>alert(1)</script>"));

console.log("\n" + pass + " passed, " + fail + " failed");
process.exit(fail ? 1 : 0);
