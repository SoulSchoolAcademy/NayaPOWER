// MAKER fix-18: laws check on base-fix17 + fixed-fix18 (real check-design-laws.py).
const { spawnSync } = require("child_process");
const fs = require("fs");
const OUT = "/home/hatch/workspace/team-nitro/calendar-day-followon-fix18-20261120/maker/proof/";
function run(file) {
  const r = spawnSync("python3", ["/home/hatch/workspace/team-nitro/check-design-laws.py", file], { encoding: "utf8" });
  return { code: r.status, out: r.stdout };
}
const b = run(OUT + "base-fix17.html");
const f = run(OUT + "fixed-fix18.html");
fs.writeFileSync(OUT + "laws-base18.txt", b.out);
fs.writeFileSync(OUT + "laws-fixed18.txt", f.out);
console.log("base exit:", b.code, "| fixed exit:", f.code);
const stripFile = (s, fn) => s.split("\n").filter((l) => l.startsWith("WARN")).map((l) => l.replace(new RegExp("^WARN .*?/" + fn + ":\\d+: "), ""));
const bw = stripFile(b.out, "base-fix17.html");
const fw = stripFile(f.out, "fixed-fix18.html");
console.log("WARN count base/fixed:", bw.length, fw.length);
console.log("WARN texts identical:", JSON.stringify(bw) === JSON.stringify(fw));
const blines = b.out.split("\n").filter((l) => l.startsWith("WARN")).map((l) => +l.match(/:(\d+):/)[1]);
const flines = f.out.split("\n").filter((l) => l.startsWith("WARN")).map((l) => +l.match(/:(\d+):/)[1]);
console.log("line shifts (fixed-base):", JSON.stringify(flines.map((x, i) => x - blines[i])));
console.log("FAIL count base/fixed:", (b.out.match(/^FAIL/gm) || []).length, (f.out.match(/^FAIL/gm) || []).length);
console.log("PASS lines:", b.out.split("\n").filter((l) => l.startsWith("PASS")).join(" | "), "||", f.out.split("\n").filter((l) => l.startsWith("PASS")).join(" | "));
