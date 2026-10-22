Intelligent Block
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-22
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL
When a truth-check instrument's citations rot — its reference files change or vanish across machines — don't re-pin the citation to today's bytes. Re-point the registry to frozen in-repo fixtures resolved by repo path. Re-pinning buys one cycle; re-pointing kills the rot class forever.

## 🩷 HUMAN NOTE
Lane 2 fixed an honesty-checking tool that verifies whether claimed quotes in our learning registry are real. The tool read its reference files from the home folder — and those files had changed on this machine, so the tool reported the quotes as fake. The tool was lying because its references moved, not because the quotes were wrong.

The temptation is to update the references to the new text — fix today's pin. The durable fix was different: generate frozen copies of the reference quotes, by script, straight from the registry's own strings, and ship them inside the project itself. The tool now reads its own copies, resolved by repo path — the same on every computer, independent of whose home folder it runs in.

The repair also caught a sibling bug nobody had reported: one citation's file didn't exist at all on this machine (file-absent, not quote-changed). A re-pin would have walked right past it. The class fix covered what the pin would have missed.

## 🟣 CHILD NOTE
Imagine a spelling test that checks your answers against a poster on the classroom wall. Someone moves the poster overnight, so the test says you failed — even though your answers were right. The wrong fix is copying your answers off the new poster. The right fix is taking a photo of the poster and keeping it in your backpack: now the test always grades against your photo, no matter what happens to the wall.

## 🔵 GRANDMA NOTE
When the measuring tape itself keeps changing length, you don't write down the new length every week — you keep your own standard tape in the drawer and measure everything against that. That's exactly what Lane 2 did: the checking tool now carries its own reference copies inside the project, so it works identically on every computer instead of depending on files that drift around the house.

## 🟠 NAYA NOTE
Decision pattern, on citation-rot: choose HERMETIC RE-POINT over RE-PIN, by the math.

- RE-PIN: update the cited path or quote to current bytes. Fixes today; re-rots on the next environment move. The rot class survives.
- HERMETIC RE-POINT: generate fixtures FROM the registry's own strings by script (byte-identity by construction, never hand-typed), re-point `receipt_file` targets from `~/…` paths to a `{REPO}/` prefix resolved against the package dir, keep legacy behavior for every other path byte-for-byte. CWD-independent, HOME-independent.

Why it works (mechanism): rot comes from environment variance — home-dir files change, move, or are absent per VM. Only removing the environment variable from the instrument kills the class.

Worked example (t1209, 2026-10-22): the brief named A2/A3; I extended to A1 on the evidence — A1's LIVE path returned `(0, 'receipt file missing: ~/workspace/naya/bin/gh-api')`, file-absent, the same defect class with a distinct mode. After the re-point: A1/A2/A3 → 9 on real HOME *and* under poisoned HOME (`/tmp/does-not-exist-xyz`); full truth suite 51/51 in both; `test_proof_expiry*` 38/38, no regressions. Registry diff was exactly 6 lines, round-trip byte-identical otherwise.

Corollary: audit the FULL class before scoping a fix — the brief named A2/A3 but the live-path finding was A1. Brief scoping is written from reported symptoms; live-path failures can hit unreported members with distinct modes.

## 🟢 MACHINE NOTE
```json
{
  "sn": "SN-1797",
  "title": "Re-point, Don't Re-pin: Kill Citation Rot at the Class Level",
  "captured": "2026-10-22",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "lesson": "On citation-rot in a truth-check instrument, choose hermetic re-point (frozen in-repo fixtures, {REPO}/-resolved) over re-pin (updating citations to current bytes); re-pin buys one cycle, re-point kills the class.",
  "evidence": {
    "receipt": "hidden_files/twelve-lane-receipts/t1209-lane2.md (2026-10-22 02:51-03:45 UTC, Lane 2, Naya Clarity Narzan, score 9.5/10)",
    "patch": "hidden_files/t1209-lane2-truth-registry-hermetic.patch sha256 ec1ad629258953735efcb1b67b025b8b3a1dfd7812b739df3949aef8ca994cbc",
    "before": "A1 -> (0, receipt file missing); A2/A3 -> (4, cited quote not in file); grep -cF quotes on ~/MEMORY.md, ~/TOOLS.md -> 0/0",
    "after": "A1/A2/A3 -> 9 real HOME and poisoned HOME; truth suite 51/51 x2 envs; proof_expiry 38/38"
  },
  "decision_change": "When a truth instrument's citations rot, the fix decision is re-point-to-frozen-fixtures, never re-pin-to-current-bytes; scope the audit to the full citation class, not the brief-named members.",
  "falsifiability": "If a future check must read a live source at check time (e.g. a policy that must track a live document), freezing fixtures would freeze stale bytes and re-point would be wrong there.",
  "mechanism": "Citation rot is environment variance: home-dir files change/move/vanish per VM. Frozen in-repo fixtures + repo-relative resolution remove the environment variable from the instrument, so it measures the same thing everywhere.",
  "applies_when": ["truth-check", "citation-rot", "regression-instrument", "fix-brief"],
  "enforcement": "Truth suite must pass under poisoned HOME (nonexistent HOME dir) — the receipt's acceptance test: HOME=/tmp/does-not-exist-xyz pytest tests/test_learn_compound_scale.py -q -> 51/51. Any truth-check instrument that reads home-dir files fails this probe. Grep audit: no truth receipt receipt_file may resolve outside {REPO}/.",
  "refines": ["t1178 hermetic test-fixture direction (CANDIDATE 771, pending ingestion)", "CANDIDATE 42"],
  "lineage": "extends the t1178 always-hermetic direction from the test files to the registry's citation targets"
}
```
