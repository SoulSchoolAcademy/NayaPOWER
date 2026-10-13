# A Test That Doesn't Probe a Hole Can't Certify It Closed

**Intelligent Block:** IB-SMART-NOTE-20261009-sn0810-threat-class-coverage
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-09
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Filed by:** distillation loop, #1354 comment 6087114851 (2026-10-09).
**Provenance:** #1354 6087114851 (STEWARD UPDATE — gate-R2: STILL-LEAKING, 2026-10-09T18:44:26Z) correcting the earlier CLOSED verdict 6087022581 (9.0/10). Related: SN-0531 (a proof gate must prove it can fire), SN-0719 (falsification-check your gates), SN-079 (withheld certification is the gate working).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The activation gate's permission repair earned an independent CLOSED verdict at 9.0/10 — and then a second independent re-attacker, built with a *different* battery, found a real leak the first battery never tested: quote-smuggling via `&#34;`/`&#x22;`/`&quot;`/`&#39;`. The root cause: `canonicalize_class_attributes()` runs `html.unescape` on class values and re-wraps them in double quotes without re-escaping, so a disguised quote terminates the rewritten attribute early — the freestyle class falls outside the inspector's regex while the browser applies it live. Proven 7/7 on the real pinned lane: `<div class="&#34; naya-evil">` scored DESIGN GATE: PASS against a FAIL for the plain version.

The lesson is not about quotes. It is about certification itself: the first CLOSED battery had **zero quote-smuggling rows** — it could not possibly have caught this hole, and it certified anyway. SN-0531 says a gate must prove it can fire; this says a battery must prove it probes. A battery's verdict is only as complete as its threat-class coverage. Falsification checks (SN-0719) prove the battery works on *known* breaks; threat-class coverage proves it looked where breaks can hide. Both are required before "CLOSED" means anything.

## 🩷 HUMAN NOTE

Shawn — the guard got a clean bill of health, and then we sent a second burglar with a different set of tools. The first inspector tested the lock against every trick he knew — but he didn't know the disguised-quotation-mark trick, so his perfect score was measuring the wrong thing. The lesson for the whole team: when someone says "tested and closed," ask "what did you test *against*?" A test that never tried the hole can't tell you the hole is closed. We now require every certification battery to name its threat classes and prove it has rows for each one — no coverage, no certification.

## 👶 CHILD NOTE

Imagine a teacher gives a spelling test with only words from chapter 1, and gives the whole class an A. Then a new kid shows up with words from chapter 2 — and everyone misspells them. The test wasn't wrong, but it only tested chapter 1, so the A was about chapter 1, not about spelling. Before you celebrate an A, check which chapters were on the test. A grade without the test list is just a rumor.

## 👵 GRANDMA NOTE

Sweetie, it's like the health inspector who checked the kitchen's stove, sink, and counters — a thorough job — and gave the restaurant a perfect score. But he never opened the walk-in freezer, because his checklist didn't have one. The next week the freezer went warm. Nobody lied. The checklist was just missing a door. Always ask the inspector which doors he opened, not just what grade he gave. A checklist is only as good as the doors it knows about.

## 🤖 NAYA NOTE

Before accepting or issuing any certification verdict (CLOSED / VERIFIED / 9.0+):

1. **Enumerate the threat classes for the fix's claimed scope.** For an HTML gate: entity-encoding variants, attribute forms (quoted/unquoted/none), raw-text elements, case tricks, comment/string disguises, inline styles, srcdoc/documents, data-URIs.
2. **Demand battery rows per class, not per example.** The first battery had letter-encoding rows (8 variants, genuinely CLOSED) and zero quote rows. One example per class is the minimum; zero rows in a class = that class is untested.
3. **Treat a coverage gap as a verdict gap.** The earlier CLOSED verdict was corrected, not deleted — its evidence held for what it probed. Certification claims must be scoped to what the battery actually probed: "CLOSED against classes X, Y; class Z untested."
4. **Pair independent re-attackers with independent batteries.** The second re-attacker mattered because he built his own tools, not because he re-ran the first one's. Re-running the same battery can only confirm; it can never discover.

## 🧠 MACHINE NOTE

```json
{
  "sn": "SN-0810",
  "class": "ENGINEERING-PROOF",
  "subcategory": "VERIFY-COVERAGE",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-09",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "rule": "A certification verdict is only as complete as its battery's threat-class coverage: a battery with zero rows for an entire attack class cannot certify that class closed. Every CLOSED/VERIFIED claim must enumerate the threat classes it probed and the classes it did not; independent re-attackers must build independent batteries, not re-run the first one's.",
  "worked_example": {
    "first_verdict": "#1354 6087022581 — CLOSED 9.0/10, battery had zero quote-smuggling rows",
    "correction": "#1354 6087114851 — second re-attacker found 7/7 quote-smuggling leaks live (canonicalize_class_attributes decode-without-re-escape on design_gate.py @ 3bfa8f64); lane re-opened for round 5",
    "root_cause": "html.unescape then re-wrap in quotes WITHOUT re-escaping: <div class=\"&#34; naya-evil\"> -> class=\"\" naya-evil\" invisible to pinned-lane regex, applied live by the browser"
  },
  "related": ["SN-0531", "SN-0719", "SN-079"]
}
```
