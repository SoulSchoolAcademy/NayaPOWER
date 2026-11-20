// MAKER fix-18: filing re-derivation via git blob API (gh-direct.py only)
// + staged-link verification. Writes fetched bytes for the record.
const { spawnSync } = require("child_process");
const crypto = require("crypto");
const fs = require("fs");
const https = require("https");
const REPO = "SoulSchoolAcademy/NayaPOWER";
const PATH = "TEAM-NITRO/day-view-v18-fix-20261117/the-ultimate-calendar-v18-fix.staged.html";
const BRANCH = "calendar/day-followon-fix18-20261120";
const EXPECT_PARENT = "a955d7fa2299a6667ba70215dd4347c1de80386e";
const EXPECT_BLOB = "f7b14ce75d590738a9efb87a4fa056ee98f3561d";
const EXPECT_SIZE = 413386;
const EXPECT_SHA = "52ff950fb4dfeb942415c96ee2af393b815e06e9019c77a9758121a9f40770cc";
const BASE_BLOB = "f4c05109531f8b737891a43f6ea6bdcef84eddc9";
const BASE_SIZE = 410236;
const BASE_SHA = "1f798b65dfa557a4e4e20472e3d56e2bda29fd69912481338b3bb6b2bc602887";
const STAGED = "https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO/day-view-v18-fix-20261117/the-ultimate-calendar-v18-fix.staged.html&ref=calendar/day-followon-fix18-20261120&cb=f7b14ce75d590738a9efb87a4fa056ee98f3561d";
const GH = "/home/hatch/workspace/team-nitro/gh-direct.py";
const OUT = "/home/hatch/workspace/team-nitro/calendar-day-followon-fix18-20261120/maker/proof/";
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
console.log("branch:", br.status, "name:", br.json.name, "tip:", br.json.commit && br.json.commit.sha);
const tip = br.json.commit && br.json.commit.sha;
const cm = ghGet(`/repos/${REPO}/commits/${tip}`);
const parents = (cm.json.parents || []).map((p) => p.sha);
console.log("commit:", cm.status, "sha:", cm.json.sha, "parents:", parents);
console.log("  parent == fix-17 tip:", JSON.stringify(parents) === JSON.stringify([EXPECT_PARENT]));
console.log("  commit message:", (cm.json.commit && cm.json.commit.message || "").split("\n")[0]);
const bl = ghGet(`/repos/${REPO}/git/blobs/${EXPECT_BLOB}`);
const filed = Buffer.from(bl.json.content.replace(/\s/g, ""), "base64");
console.log("filed blob:", bl.status, "encoding:", bl.json.encoding, "size:", filed.length, "sha256:", sha(filed));
console.log("  size == claimed:", filed.length === EXPECT_SIZE, " sha == claimed:", sha(filed) === EXPECT_SHA);
fs.writeFileSync(OUT + "fetched-fixed.html", filed);
const bl2 = ghGet(`/repos/${REPO}/git/blobs/${BASE_BLOB}`);
const base = Buffer.from(bl2.json.content.replace(/\s/g, ""), "base64");
console.log("base blob:", bl2.status, "size:", base.length, "sha256:", sha(base));
console.log("  size == claimed:", base.length === BASE_SIZE, " sha == claimed:", sha(base) === BASE_SHA);
fs.writeFileSync(OUT + "fetched-base.html", base);
// Rebuild: base - Hz segment + fix18 block before </style> == filed
const HZ_OLD = Buffer.from(' + " \\u00b7 <span style=\\"white-space:nowrap\\">" + dayDigitsHTML(DAY_FREQ[d.getDay()], dc) + " Hz</span></span>"', "utf8");
const HZ_NEW = Buffer.from(" + '</span>'", "utf8");
const noHz = Buffer.concat([base.subarray(0, base.indexOf(HZ_OLD)), HZ_NEW, base.subarray(base.indexOf(HZ_OLD) + HZ_OLD.length)]);
const block = fs.readFileSync(OUT + "fix18-block.css");
const rebuilt = Buffer.concat([noHz.subarray(0, noHz.lastIndexOf(Buffer.from("</style>"))), block, Buffer.from("\n"), noHz.subarray(noHz.lastIndexOf(Buffer.from("</style>")))]);
console.log("rebuilt size:", rebuilt.length, "sha256:", sha(rebuilt));
console.log("rebuilt == filed blob:", rebuilt.equals(filed));
console.log("filed == local fixed-fix18.html:", filed.equals(fs.readFileSync(OUT + "fixed-fix18.html")));
https.get(STAGED, { headers: { "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36" } }, (res) => {
  const chunks = [];
  res.on("data", (c) => chunks.push(c));
  res.on("end", () => {
    const staged = Buffer.concat(chunks);
    console.log("staged GET:", res.statusCode, "size:", staged.length, "sha256:", sha(staged));
    console.log("  staged == filed blob:", staged.equals(filed));
    fs.writeFileSync(OUT + "fetched-staged.html", staged);
  });
}).on("error", (e) => console.log("staged fetch ERROR:", e.message));
