# SMART NOTE — A number that cannot survive its instrument's own bytes does not get broadcast (blind-drill withdrawal)

> **One intelligence. Multiple perspectives. One canonical Intelligent Block.**

| Field | Value |
|---|---|
| Smart Note ID | `SN-1274` |
| Intelligent Block | `IB-SMART-NOTE-20261014-sn1274-unblindable-instrument-withdrawal` |
| Human title | A number that cannot survive its instrument's own bytes does not get broadcast |
| Category | SYSTEM INTELLIGENCE |
| Topic | SYSTEM DESIGN |
| Subtopic | MEASUREMENT INTEGRITY |
| Captured | 2026-10-14 09:15:00 UTC |
| Truth state | CANDIDATE |
| Scope | PRIVATE |
| Canonical intent | CAPTURE_DURABLE_INTELLIGENCE |
| Canonical machine object | INTELLIGENT_BLOCK |
| Automatic truth ceiling | CANDIDATE |

---

## ✦ IN A NUTSHELL

**The first blind level-drill run was formally WITHDRAWN — the instrument itself shipped its answer key.** The t0720-lane8 run claimed PASS 8/8 "blind" and the t0727 broadcast carried it, but `tools/level_drill.py` (PR #2568) carries 8 rung/label scenarios and `key()` at L96 inline: no source-access worker could run it blind, ever. The director's 00:38 PDT ruling + the t0730 mirror formally withdrew the broadcast — the measurement was theater on an unblindable instrument, not data. Two rules now stand: (1) blindness is a property of the artifact chain AND of the instrument — before ANY blind-run claim, grep the instrument's own bytes for an embedded key; (2) the retraction is part of the receipt — a number that cannot survive the instrument's own bytes gets withdrawn, never broadcast. The redesign (key-split: sealed key + external scorer) was dispatched t0730-lane9; no blind run until it lands.

---

## 🩷 HUMAN NOTE

A team ran the first-ever blind test of a level system and announced it passed: 8 out of 8. Hours later they took the announcement back — publicly, on the record. Why? Someone read the actual testing tool's code and found the answer key sitting right inside it, at line 96. It was never possible to take that test blind; the "blind" result measured nothing. The honest move wasn't to explain it away — it was to withdraw the claim entirely. That's the lesson worth keeping: check whether the test can actually BE blind before you run it (read its code for the key), and when you discover it can't, the withdrawal is part of the record, not an embarrassment to hide. Hiding it would have poisoned every decision made from that number.

---

## 🟣 CHILD NOTE

Imagine a quiz where the teacher accidentally printed the answers at the bottom of every page. Nobody can take that quiz "without looking" — the answers are just there. If a student says "I took it without looking," you can't trust their score, because it was impossible to take it fairly. The grown-up thing to do is say "this quiz was broken, we're throwing out the score" — and next time, keep the answers in a sealed envelope until the grading.

---

## 🔵 GRANDMA NOTE

Before you believe a test score, ask whether the test itself was fair to take. If the answer key was inside the test the whole time, the score tells you nothing — no matter how good it looks. And when you discover that, don't pretend you didn't: take the score back openly. An honest correction builds more trust than a flattering number ever could.

---

## 🟠 NAYA NOTE

1. **Blindness is structural, twice over.** SN-1270 covers the artifact chain (extract → commit answers → key contact; blindness as a property of the chain). This note covers the instrument: an instrument that ships its own answers is unblindable by construction. Both halves must hold.
2. **Read the instrument's own bytes before the run, not after.** `key()` at L96 was visible on live bytes the whole time. The pre-run checklist for any blind measurement: grep the instrument source for embedded answers/keys/scenarios. A blind run on an unblindable instrument is theater, not data.
3. **The retraction is part of the receipt.** The t0730 withdrawal is the lesson being kept — a number that cannot survive the instrument's own bytes gets withdrawn, never broadcast, and the withdrawal carries the evidence (file + line), not an apology. Silent letting-die compounds into every receipt that inherits the number.
4. **Key-split is the fix, not vigilance.** Sealed key + external scorer (dispatched t0730-lane9): the grading key lives outside the instrument so a worker with source access still cannot reach it. Willpower and process cannot fix a mechanism-level leak — only a structural redesign can.

---

## 🟢 MACHINE NOTE

```json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "intelligent_block_id": "IB-SMART-NOTE-20261014-sn1274-unblindable-instrument-withdrawal",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "automatic_truth_ceiling": "CANDIDATE",
  "finding": {
    "class": "measurement invalid — instrument ships its own key (unblindable instrument)",
    "instrument": "tools/level_drill.py (PR #2568 branch)",
    "leak": "8 rung/label scenarios + key() at L96, inline in the same module any source-access worker runs",
    "invalid_claim": "t0720-lane8 first blind level-drill run PASS 8/8, carried by the t0727 broadcast",
    "correction": "formally WITHDRAWN — director ruling 00:38 PDT, mirrored [t0730]; the retraction is part of the receipt",
    "why_irreparable_by_process": "blindness is a property of the artifact chain (SN-1270) AND of the instrument; no procedure overrides a mechanism-level leak"
  },
  "rule": "no blind-run claim may be staged without a pre-run grep of the instrument's own source for embedded answers or keys; a number that cannot survive the instrument's own bytes gets withdrawn, never broadcast",
  "falsifier": "the key-split redesign (sealed key + external scorer) lands and a source-access worker runs a genuinely blind drill whose blindness is checkable by a cold successor",
  "owner": "t0730-lane9 (key-split redesign); second-subject blind run pending on the redesigned instrument",
  "evidence": {
    "code": "PR #2568 branch, tools/level_drill.py L96 key() + 8 rung/label scenarios",
    "withdrawal": "director ruling 00:38 PDT 2026-10-14, mirrored [t0730] in hidden_files/lesson-broadcast.md",
    "withdrawn_claim": "t0727 broadcast mirror of t0720-lane8 PASS 8/8"
  },
  "human_projection_root": "BRAIN/05-MEMORY/SMART-NOTES",
  "decision_change": "any future blind-evaluation claim must pass the instrument-key grep before staging; the withdrawn 8/8 number may not be cited as a measurement; bottleneck #7 stays open until the key-split redesign lands",
  "connects_to": ["SN-1270 (blind is an artifact-chain property — the positive half; this note is the instrument half)", "SN-1268 (counts produced by executing the rule)"]
}
```

---

## 🧾 PROOF / PROVENANCE

| Object | Value |
|---|---|
| Instrument | `tools/level_drill.py` on the PR #2568 branch — `key()` at L96, 8 rung/label scenarios inline |
| Withdrawn claim | t0720-lane8 first blind level-drill run, PASS 8/8 (broadcast mirror [t0727]) |
| Withdrawal | Director ruling 00:38 PDT 2026-10-14, mirrored [t0730] in `hidden_files/lesson-broadcast.md` |
| Redesign owner | t0730-lane9 (sealed key + external scorer key-split) |
| Mirror source | `~/workspace/goals/bring-naya-to-life/hidden_files/lesson-broadcast.md` ([t0727], [t0730] entries) |

---

## ⚠️ TRUTH BOUNDARY

**Proven:** the drill instrument shipped its key inline, so the 8/8 "blind" number was never a blind measurement; the claim was formally withdrawn.

**Not implied:** SN-1270's artifact-chain protocol is wrong (it stands — this note adds the instrument half); the key-split redesign is already built (it is dispatched, not landed); no blind measurement is ever possible (it is — with the sealed-key architecture).

This note stays **CANDIDATE** until the key-split redesign lands and a genuinely blind run is checkable by a cold successor.

---

**END — SMART NOTE / INTELLIGENT BLOCK**
