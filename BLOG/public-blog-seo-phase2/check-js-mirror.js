#!/usr/bin/env node
/** check-js-mirror.js — run the REAL phase-2 JS functions over the feed
 * and diff every note against the Python mirror's seo-score-report.json.
 * Any divergence fails. The built worker is loaded with its `export
 * default {...}` fetch block stripped (it needs env); everything else
 * (base + phase-1 + phase-2 functions) evaluates with no side effects.
 * Usage: node check-js-mirror.js
 */
const fs = require("fs");
const vm = require("vm");
const WD = "/home/hatch/workspace/team-nitro/seo-ai-backend-20261113";
let src = fs.readFileSync(WD + "/hub-worker-phase2.js", "utf8");
// Strip the export-default fetch block (up to handleItems).
const start = src.indexOf("export default {");
const end = src.indexOf("async function handleItems");
if (start === -1 || end === -1 || end < start) { console.error("STRIP ANCHORS MISSING"); process.exit(2); }
src = src.slice(0, start) + src.slice(end);
const sandbox = { console, URL, Response, Request, Headers, fetch: async () => { throw new Error("no fetch in harness"); } };
sandbox.globalThis = sandbox;
vm.createContext(sandbox);
vm.runInContext(src, sandbox, { filename: "hub-worker-phase2.js" });
const feed = JSON.parse(fs.readFileSync("/home/hatch/workspace/factory-pipeline/hub-feed-live.json", "utf8"));
const report = JSON.parse(fs.readFileSync(WD + "/seo-score-report.json", "utf8"));
const byId = {};
for (const r of report) byId[r.id] = r;
let bad = 0, checked = 0;
const badList = [];
for (const note of feed.notes) {
  const r = byId[note.id];
  if (!r) { bad++; badList.push(note.id + ": missing from report"); continue; }
  const content = sandbox.phase2ParseContent(note);
  const cluster = sandbox.phase2ClusterOf(note);
  const display = sandbox.phase2DisplayTitle(note);
  const title = sandbox.phase2Title(note, content);
  const desc = sandbox.phase2Description(note, content);
  const related = sandbox.phase2Related(note, feed);
  const meta = { displayTitle: display, title, description: desc, canonicalPath: "/s/" + sandbox.phase2CanonicalSlug(note), cluster, snSlug: sandbox.phase2CanonicalSlug(note) };
  const score = sandbox.phase2SeoScore(note, content, meta, related.length);
  checked++;
  const diffs = [];
  if (display !== r.displayTitle) diffs.push(`display ${JSON.stringify(display)} != ${JSON.stringify(r.displayTitle)}`);
  if (title !== r.title) diffs.push(`title ${JSON.stringify(title)} != ${JSON.stringify(r.title)}`);
  if (desc !== r.description) diffs.push(`desc ${JSON.stringify(desc)} != ${JSON.stringify(r.description)}`);
  if (cluster !== r.cluster) diffs.push(`cluster ${cluster} != ${r.cluster}`);
  if (content.servable !== r.servable) diffs.push(`servable ${content.servable} != ${r.servable}`);
  if (related.length !== r.relatedCount) diffs.push(`related ${related.length} != ${r.relatedCount}`);
  if (score.score !== r.score) diffs.push(`score ${score.score} != ${r.score}`);
  if (score.nutWords !== r.nutWords) diffs.push(`nutWords ${score.nutWords} != ${r.nutWords}`);
  const relJs = related.map(x => x.slug + "|" + x.reason).join(";");
  const relPy = r.related.map(x => x.slug + "|" + x.reason).join(";");
  if (relJs !== relPy) diffs.push(`related-list ${relJs} != ${relPy}`);
  if (diffs.length) { bad++; if (badList.length < 15) badList.push(note.id + ": " + diffs.join(" ;; ")); }
}
console.log(`checked=${checked} divergent=${bad}`);
if (badList.length) console.log(badList.join("\n"));
process.exit(bad ? 1 : 0);
