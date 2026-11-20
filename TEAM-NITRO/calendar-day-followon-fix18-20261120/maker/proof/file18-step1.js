// FIX18 filing step 1: verify the fix-17 tip + file blob, create the fix-18 branch.
const { spawnSync } = require("child_process");
const GH = "/home/hatch/workspace/team-nitro/gh-direct.py";
const REPO = "SoulSchoolAcademy/NayaPOWER";
const PATH = "TEAM-NITRO/day-view-v18-fix-20261117/the-ultimate-calendar-v18-fix.staged.html";
const BASE_BRANCH = "calendar/day-followon-fix17-20261119";
const BASE_TIP = "a955d7fa2299a6667ba70215dd4347c1de80386e";
const BASE_BLOB = "f4c05109531f8b737891a43f6ea6bdcef84eddc9";
const NEW_BRANCH = "calendar/day-followon-fix18-20261120";
function gh(method, path, body) {
  const args = ["python3", GH, method, path];
  if (body !== undefined) args.push(body);
  const r = spawnSync("node", ["-e", `
const {spawnSync}=require("child_process");
const fs=require("fs");
const b = process.argv[1] === "-" ? null : null;
`].concat([]), { encoding: "utf8" });
  return r;
}
// Simpler: call gh-direct.py directly via spawnSync with JSON body piped through a temp-free approach:
// gh-direct.py accepts the body as a literal argv string or @file. For the small refs POST, pass JSON literally.
function ghCall(method, path, bodyArg) {
  const argv = ["python3", GH, method, path];
  if (bodyArg !== undefined) argv.push(bodyArg);
  const r = spawnSync(argv[0], argv.slice(1), { encoding: "utf8", timeout: 120000, maxBuffer: 16 * 1024 * 1024 });
  const nl = r.stdout.indexOf("\n");
  const status = r.stdout.slice(0, nl).trim();
  const body = r.stdout.slice(nl + 1);
  let json = null;
  try { json = JSON.parse(body); } catch (e) { /* keep raw */ }
  return { rc: r.status, status, json, raw: body.slice(0, 400) };
}
const br = ghCall("GET", `/repos/${REPO}/branches/${BASE_BRANCH}`);
console.log("base branch:", br.status, "tip:", br.json && br.json.commit && br.json.commit.sha);
console.log("  tip == brief:", br.json && br.json.commit && br.json.commit.sha === BASE_TIP);
const fc = ghCall("GET", `/repos/${REPO}/contents/${PATH}?ref=${BASE_BRANCH}`);
console.log("base file at tip:", fc.status, "sha:", fc.json && fc.json.sha);
console.log("  blob == brief:", fc.json && fc.json.sha === BASE_BLOB);
const nb = ghCall("GET", `/repos/${REPO}/branches/${NEW_BRANCH}`);
console.log("new branch pre-check:", nb.status, (nb.json && nb.json.message) || (nb.json && nb.json.name));
if (nb.status !== "HTTP 404" && !(nb.json && nb.json.message === "Branch not found")) {
  console.log("NEW BRANCH ALREADY EXISTS — stop, do not file twice");
  process.exit(1);
}
const created = ghCall("POST", `/repos/${REPO}/git/refs`, JSON.stringify({ ref: `refs/heads/${NEW_BRANCH}`, sha: BASE_TIP }));
console.log("create branch:", created.status, "ref:", created.json && created.json.ref, "sha:", created.json && created.json.object && created.json.object.sha);
if (!created.json || !created.json.ref) { console.log("CREATE FAILED raw:", created.raw); process.exit(1); }
console.log("BRANCH CREATED:", NEW_BRANCH, "from", BASE_TIP);
