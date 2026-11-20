// CHECKER fix-18: independent filing re-derivation via git blob API (gh-direct.py only) + staged-link check.
// Writes fetched bytes under checker/proof/ for the record.
const { spawnSync } = require("child_process");
const crypto = require("crypto");
const fs = require("fs");
const https = require("https");
const REPO = "SoulSchoolAcademy/NayaPOWER";
const PATH = "TEAM-NITRO/day-view-v18-fix-20261117/the-ultimate-calendar-v18-fix.staged.html";
const BRANCH = "calendar/day-followon-fix18-20261120";
const EXPECT_COMMIT = "ffd220c7d7d54fbbfc08c82ceed793ce1b0968a3";
const EXPECT_PARENT = "a955d7fa2299a6667ba70215dd4347c1de80386e";
const EXPECT_BLOB = "f7b14ce75d590738a9efb87a4fa056ee98f3561d";
const EXPECT_SIZE = 413386;
const EXPECT_SHA = "52ff950fb4dfeb942415c96ee2af393b815e06e9019c77a9758121a9f40770cc";
const BASE_BLOB = "f4c05109531f8b737891a43f6ea6bdcef84eddc9";
const BASE_SIZE = 410236;
const BASE_SHA = "1f798b65dfa557a4e4e20472e3d56e2bda29fd69912481338b3bb6b2bc602887";
const STAGED = "https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO/day-view-v18-fix-20261117/the-ultimate-calendar-v18-fix.staged.html&ref=calendar/day-followon-fix18-20261120&cb=f7b14ce75d590738a9efb87a4fa056ee98f3561d";
const GH = "/home/hatch/workspace/team-nitro/gh-direct.py";
const OUT = "/home/hatch/workspace/team-nitro/calendar-day-followon-fix18-20261120/checker/proof/";
const sha = (b) => crypto.createHash("sha256").update(b).digest("hex");
function ghGet(path) {
  const r = spawnSync("python3", [GH, "GET", path], { encoding: "utf8", timeout: 120000, maxBuffer: 64 * 1024 * 1024 });
  const nl = r.stdout.indexOf("\n");
  const status = r.stdout.slice(0, nl).trim();
  const body = r.stdout.slice(nl + 1);
  if (r.status !== 0) console.log("  !! gh-direct rc=" + r.status + " stderr=" + (r.stderr || "").slice(0, 300));
  return { status, json: JSON.parse(body) };
}
const br = ghGet(`/repos/${REPO}/branches/${BRANCH}`);
console.log("branch:", br.status, "tip:", br.json.commit && br.json.commit.sha, "tip==claimed:", (br.json.commit||{}).sha === EXPECT_COMMIT);
const tip = br.json.commit && br.json.commit.sha;
const cm = ghGet(`/repos/${REPO}/commits/${tip}`);
const parents = (cm.json.parents || []).map((p) => p.sha);
console.log("commit:", cm.status, "sha:", cm.json.sha, "parents:", parents, "parent==fix17tip:", JSON.stringify(parents) === JSON.stringify([EXPECT_PARENT]));
console.log("  message:", (cm.json.commit && cm.json.commit.message || "").split("\n")[0]);
const bl = ghGet(`/repos/${REPO}/git/blobs/${EXPECT_BLOB}`);
const filed = Buffer.from(bl.json.content.replace(/\s/g, ""), "base64");
console.log("filed blob:", bl.status, "size:", filed.length, "sha256:", sha(filed), "size==claimed:", filed.length === EXPECT_SIZE, "sha==claimed:", sha(filed) === EXPECT_SHA);
fs.writeFileSync(OUT + "fetched-fixed.html", filed);
console.log("  wrote fetched-fixed.html bytes:", fs.statSync(OUT + "fetched-fixed.html").size);
const bl2 = ghGet(`/repos/${REPO}/git/blobs/${BASE_BLOB}`);
const base = Buffer.from(bl2.json.content.replace(/\s/g, ""), "base64");
console.log("base blob:", bl2.status, "size:", base.length, "sha256:", sha(base), "size==claimed:", base.length === BASE_SIZE, "sha==claimed:", sha(base) === BASE_SHA);
fs.writeFileSync(OUT + "fetched-base.html", base);
// Scope: rebuild base - Hz + fix18 block == filed, using maker's block file as the claimed block (read, not trusted for content — rebuild equality is the check)
const HZ_OLD = Buffer.from(' + " \\u00b7 <span style=\\"white-space:nowrap\\">" + dayDigitsHTML(DAY_FREQ[d.getDay()], dc) + " Hz</span></span>"', "utf8");
console.log("HZ_OLD occurrences in base:", base.toString("utf8").split(HZ_OLD.toString("utf8")).length - 1, "in filed:", filed.toString("utf8").split(HZ_OLD.toString("utf8")).length - 1);
const HZ_NEW = Buffer.from(" + '</span>'", "utf8");
const idx = base.indexOf(HZ_OLD);
const noHz = Buffer.concat([base.subarray(0, idx), HZ_NEW, base.subarray(idx + HZ_OLD.length)]);
const block = fs.readFileSync("/home/hatch/workspace/team-nitro/calendar-day-followon-fix18-20261120/maker/proof/fix18-block.css");
const sty = Buffer.from("</style>");
const rebuilt = Buffer.concat([noHz.subarray(0, noHz.lastIndexOf(sty)), block, Buffer.from("\n"), noHz.subarray(noHz.lastIndexOf(sty))]);
console.log("rebuilt size:", rebuilt.length, "sha256:", sha(rebuilt), "rebuilt==filed:", rebuilt.equals(filed));
// fixed-minus-block + Hz-reinsert == base
const fidx = filed.indexOf(block);
const minusBlock = Buffer.concat([filed.subarray(0, fidx), filed.subarray(fidx + block.length + 1)]);
const hidx = minusBlock.indexOf(HZ_NEW);
const reinsert = Buffer.concat([minusBlock.subarray(0, hidx), HZ_OLD, minusBlock.subarray(hidx + HZ_NEW.length)]);
console.log("fixed-minus-block+HzReinsert == base:", reinsert.equals(base));
https.get(STAGED, { headers: { "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36" } }, (res) => {
  const chunks = [];
  res.on("data", (c) => chunks.push(c));
  res.on("end", () => {
    const staged = Buffer.concat(chunks);
    console.log("staged GET:", res.statusCode, "size:", staged.length, "sha256:", sha(staged), "staged==filed:", staged.equals(filed));
    fs.writeFileSync(OUT + "fetched-staged.html", staged);
  });
}).on("error", (e) => console.log("staged fetch ERROR:", e.message));
