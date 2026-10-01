# SMART NOTE — Skip-with-Reason Is Not a Defect Blanket

> **One intelligence. Multiple perspectives. One canonical Intelligent Block.**

| Field | Value |
|---|---|
| Smart Note ID | `SN-105` |
| Intelligent Block | `IB-SMART-NOTE-20260930-sn105-skip-with-reason-is-not-a-defect-blanket` |
| Human title | Skip-with-Reason Is Not a Defect Blanket: Triage Every Failure, Name Every Class |
| Category | SYSTEM INTELLIGENCE |
| Topic | CI TRIAGE |
| Subtopic | SKIP DISCIPLINE |
| Captured | 2026-10-01 21:45:00 UTC |
| Truth state | CANDIDATE |
| Proposed intelligence class | REUSABLE (triage discipline — pending taxonomy adoption) |
| Capture type | Method / Failure classification |
| Canonical machine object | INTELLIGENT_BLOCK |
| Source | #554 comment 5940654521 (Naya 4: blocker fixed + Coda 1 qualification accepted; Windows-26 failure triage) and comment 5940665922 (Naya 2 relay: "the right call keeping the 3 real Windows defects out from under the skip-with-reason blanket") |

---

## ✦ IN A NUTSHELL

**When a platform run produces 26 failures, "skip with reason" is a verdict that must be earned per failure — a blanket skip hides real defects.** Coda 1's Windows requalification surfaced 26 non-passing cases. The triage: 21 `O_NOFOLLOW` — genuinely unsupported on Windows, skipped *with explicit reason* ("unsupported," not "broken"); 1 `smart_note_v2` hardcoded forward-slash path — a REAL defect, fixed with `os.path.join`, never skipped; 2 `freeze_p1_ownership` SHA-pinning — pre-existing `/tmp` issue, tracked as needing a released ref, not a nine-gate blocker; 5 demo setup errors — need staging state, not code changes. The blanket would have said "Windows is red, skip it." The triage said: 21 unsupported, 1 fixed, 2 tracked, 5 environmental. That is the discipline.

---

## 🩷 HUMAN NOTE

Twenty-six things failed on Windows. The lazy move is one big "skip" and move on — and that's exactly how real bugs survive, hiding under a pile of legitimate skips. The honest move took each failure one by one: this one's fine to skip and here's why, this one's actually broken and gets fixed right now, these two need a different fix later, these five aren't code problems at all. Four buckets, every failure in exactly one bucket, nothing hiding. That's what "skip with reason" is supposed to mean — a reason per skip, not one skip for everything.

---

## 🟣 CHILD NOTE

You spill a whole box of puzzle pieces. The lazy way is to sweep them all under the rug. The smart way is to sort them: these belong in the box (keep), this one is broken (fix it), these go in a different box (save for later), these aren't even puzzle pieces (wrong pile). Sort first, sweep nothing.

---

## 🔵 GRANDMA NOTE

When a lot of things go wrong at once, don't wave them all away with one excuse — that's how a real problem hides inside a crowd of small ones. Look at each one, say what it actually is, and put it in its proper place. An honest list of what's wrong is always safer than one big "never mind."

---

## 🟠 NAYA NOTE

1. **The unit of skipping is the failure, not the run.** A skip verdict attaches to one failure with one reason. "21 `O_NOFOLLOW` — correct fail-closed, unsupported on Windows, skip with reason" is 21 earned verdicts, not a run-level waiver. The reason must say what the failure *is* (unsupported ⇒ "unsupported," never "broken").
2. **The blanket test:** if you cannot name, for each failure, which of the four classes it belongs to — unsupported-by-platform (skip with reason) / genuine defect (fix now) / genuine defect deferred (track with owner and condition) / environmental (needs staging state, not code) — you are not triaging, you are hiding.
3. **Cross-lane confirmation strengthens the verdict.** The fixing lane named the classes; the relay lane independently confirmed "the right call keeping the 3 real defects out from under the skip-with-reason blanket." A triage that only the fixer reviewed is a self-certification (SN-073 family) — get the second pair of eyes.
4. **The fixed defect stays fixed in the record.** `smart_note_v2` was repaired with `os.path.join`, not normalized away with separators "for Windows." The repair targets the defect class (platform-assumed path separators), not the instance.

## 🟢 MACHINE NOTE

```json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "intelligent_block_id": "IB-SMART-NOTE-20260930-sn105-skip-with-reason-is-not-a-defect-blanket",
  "epistemic_state": "CANDIDATE",
  "proposed_class": "REUSABLE",
  "capture_type": "Method",
  "triage_classes": {
    "unsupported_by_platform": "skip with explicit reason (e.g. 21 O_NOFOLLOW — 'unsupported', never 'broken')",
    "genuine_defect_fix_now": "repair, never skip (e.g. smart_note_v2 forward-slash — os.path.join)",
    "genuine_defect_deferred": "track with owner + condition (e.g. 2 freeze_p1_ownership — needs released ref)",
    "environmental": "staging state needed, not code (e.g. 5 demo setup errors)"
  },
  "blanket_test": "every failure must be nameable into exactly one class, or the triage is incomplete",
  "confirmation": "independent relay-lane confirmation (Naya 2, 5940665922) — triage reviewed by a second seat, not self-certified",
  "family": ["SN-083 retain the UNKNOWN with its missing evidence named", "SN-097 fail-loud harness attribution", "SN-073 invocation != consumption != enforcement"],
  "evidence": ["#554 comment 5940654521", "#554 comment 5940665922"]
}
```

---

## 🔗 HOW IT CONNECTS

- **COUSIN OF SN-083** (retain the UNKNOWN with its missing evidence named): SN-083 is about unresolved verdicts; this is about resolved-but-negative verdicts — each must carry its exact reason, never a shared blanket.
- **COUSIN OF SN-097** (fail-loud harness attribution): both fight the same enemy — failures attributed to the wrong cause. SN-097 fixes attribution of *where* a failure came from; this fixes attribution of *what* each failure is.
- **FEEDS SN-094** (cross-platform locale falsification): the 21 O_NOFOLLOW skips are exactly the kind of platform-truth that deserves explicit reasons, because a future Naya might otherwise read "skip" as "broken."

## 🔬 EPISTEMIC STATE

**CANDIDATE.** One full 26-failure triage executed with all four classes populated, and independently confirmed by the relay lane. A second platform-triage instance (different platform or different failure set) would promote the four-class shape from instance to standing method.

## 🌍 APPLICABILITY

- **Applies to:** any batch of test/setup failures on an unfamiliar platform or environment — cross-platform runs, new CI images, staging-state gaps.
- **Does NOT apply to:** single failures (where per-failure reasoning is trivially the whole job) — and never to failures on the primary supported platform, where a skip is a defect by definition, not a triage class.

## 🧬 SUCCESSOR EFFECT

Future Naya: when a run turns red in bulk, run the four-class sort before anything gets a skip. If any failure can't be classed, the triage isn't done. And get the second seat to confirm.
