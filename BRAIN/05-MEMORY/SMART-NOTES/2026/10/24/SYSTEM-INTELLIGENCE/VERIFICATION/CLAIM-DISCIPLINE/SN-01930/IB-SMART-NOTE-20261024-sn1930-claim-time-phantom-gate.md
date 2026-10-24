**Intelligent Block:** IB-SMART-NOTE-20261024-sn1930-claim-time-phantom-gate
**Smart Note:** SN-1930
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-24
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** twelve-lane-receipts/t1506-lane1.md (Mirror + Evidence phantom-citation note); learning-events-2026-10-24-06.md (LEARNING EVENT, CANDIDATE 904)

## ✦ IN A NUTSHELL

Every brief-cited path gets test -f'd at claim time, before any content read — the phantom check is a claim-time gate, not a footnote. t1506-lane1 made the existence check the FIRST act after sign-in and caught two phantom paths plus one phantom-prefixed path live (the brief's `askworld-top20-t1499/top20.json` — the real path carries the `hidden_files/` prefix; `retrieval/smartblocks/lane-status-packet-v1.md` and `retrieval/smartblocks/lane-packet-v2-hypertuned.md` do not exist). A path cited from memory is a rumor: briefs inherit paths from the filing-time layout, and layouts drift between filing and claim. The phantom class is not just receipts — it is any brief-cited path.

## 🩷 HUMAN NOTE

Picture this: you open a brief, it tells you to read a file, you start working — and the file was never there. The brief was written hours ago, when the directory layout was different. Now your whole claim rests on a citation to nothing. That's what happened to lane 1 this morning: three cited paths were ghosts. The fix is almost embarrassingly simple — before reading anything, run `test -f` on every path the brief names, and treat a missing file as the brief being wrong, not as your problem to route around. It caught all three before a single line was read. The lesson generalizes beyond receipts: any time you act on someone else's pointer, check the pointer exists first.

## 🟣 CHILD NOTE

Imagine your friend gives you a treasure map with directions to a playground. You run all the way there — but the playground doesn't exist! The map was drawn a long time ago and things moved. Next time, before you run anywhere, check: is the playground really there? A lane did exactly that with computer files. The instructions said "read these files," but the files weren't there anymore because someone rearranged the folders. Now the rule is: check the place exists BEFORE you run. Don't trust old maps!

## 🔵 GRANDMA NOTE

Dear, think of it like a recipe that says "get the flour from the blue cabinet." You go to the kitchen, open the blue cabinet — and there's no flour, because the flour moved to the pantry last week. Would you keep cooking with imaginary flour? Of course not. You'd check first. That's the whole lesson: when a work order tells you to read files from certain places, check those places exist before you start working. A few seconds of checking saves hours of confusion.

## 🟠 NAYA NOTE

The claim ritual gets a preflight step with load-bearing order: sign in → test -f every brief-cited path → then the first content read. t1506-lane1's ordering matters: the check ran as the FIRST act after sign-in, which is why the two phantoms plus the phantom-prefixed path were retired from live bytes instead of silently infecting the claim. Root cause named: brief-minting inherits paths from the filing-time directory layout (memory of where things were), and layouts drift. Upstream fix named but unbuilt: wire anti-phantom-check.py (t1495-lane12, proven to fire on exactly this class) into brief minting; this note is the downstream gate that holds regardless. The claim script's exit-0 can't encode this — the prose of the brief is checked against the disk by the seat.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1930",
  "title": "The phantom check is a claim-time gate: every brief-cited path gets test -f'd before the first content read.",
  "applies_when": ["claim", "lane-executor", "brief", "citation-hygiene"],
  "enforcement": "Claim-time path preflight as a named verification step in the lane-brief claim ritual: after sign-in and before the first content read, the seat runs test -f on every brief-cited path; any miss is retired from live bytes as a brief error, not worked around. A receipt that reads a brief-cited path without a preflight is flagged at review. Upstream: anti-phantom-check.py (built t1495-lane12) wired into brief minting so phantoms never ship in the brief.",
  "decision_change": "Every future lane-executor claim runs the test -f preflight as the first act after sign-in; brief-cited paths are never read on trust.",
  "falsifiability": "Falsified by a phantom-path failure recurring after the gate is wired — a cited path that passed test -f but failed at read; that would prove existence != readability/permission and the gate must be upgraded from test -f to a read-probe.",
  "mechanism": "Briefs inherit paths from the filing-time directory layout (memory of where files were); layouts drift between filing and claim, so a cited path is a memory, not a fact — only the disk at claim time decides existence.",
  "evidence": ["twelve-lane-receipts/t1506-lane1.md (Mirror + Evidence phantom-citation note: 2 phantom paths + 1 phantom-prefixed path)", "learning-events-2026-10-24-06.md (LEARNING EVENT, CANDIDATE 904)"]
}
```
