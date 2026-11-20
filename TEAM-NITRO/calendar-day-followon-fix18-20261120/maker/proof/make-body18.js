// MAKER fix-18: emit the Contents-API PUT body (JSON) to stdout.
// The 413KB file becomes ~551KB of base64; piped via process substitution
// and never staged to disk (EPERM flake).
const fs = require("fs");
const raw = fs.readFileSync("/home/hatch/workspace/team-nitro/calendar-day-followon-fix18-20261120/maker/proof/fixed-fix18.html");
process.stdout.write(JSON.stringify({
  message: "Calendar day-view fix-18: November 2026 centered title line (24px gap), 396 Hz off the header, Change cover only where a cover shows (wisdom + worlds)",
  content: raw.toString("base64"),
  branch: "calendar/day-followon-fix18-20261120",
  sha: "f4c05109531f8b737891a43f6ea6bdcef84eddc9",
}));
