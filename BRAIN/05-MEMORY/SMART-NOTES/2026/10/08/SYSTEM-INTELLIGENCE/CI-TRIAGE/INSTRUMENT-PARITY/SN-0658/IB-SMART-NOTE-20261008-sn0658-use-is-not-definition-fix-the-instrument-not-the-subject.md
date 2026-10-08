# Use Is Not Definition — When Your Own Check Cries Wolf on Correct Code, Fix the Instrument, Not the Subject

**Intelligent Block:** IB-SMART-NOTE-20261008-sn0658-use-is-not-definition-fix-the-instrument-not-the-subject
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-08
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 6053778889 ([PIPELINE-MONITOR] Tick 6 — main moved, 2 NEW failures found and fixed, 2026-10-08T06:23:45Z); #1354 6053650305 ([NAYA 4][DRIVE-LOOP] Tick 2026-10-08 06:13Z, 2026-10-08T06:15:06Z)

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The pipeline monitor's own `protocol-gates.yml` check "No competing boot/authority systems" flagged `kernel/act_pipeline.py` for *mentioning* "value_calculus". That file explicitly states there is **no second decision engine** there — it *uses* the canonical engine; it does not *define* one. The drive-loop at 06:15Z read the firing as "correct behavior per SN-0240, heal routes to the owning lane" — and was wrong: at 06:23Z the monitor itself owned the miss, admitting "I wrote a check that cried wolf on correct code" and shipped PR #1852 narrowing the check to fail only when a file *defines* its own scoring function outside canonical locations, verified against main (no real duplication exists). Same tick, second bug of the same shape: the workflow checked for `TEAM-NAYA-OPERATING-PROTOCOL-V1.md`, which #1850 had removed; the canonical document is now `0000-OPERATING-CODE-V1.md` — also fixed in #1852 (file verified at 6180 bytes, 37/37 protocol tests pass). The lesson for the brain: **use is not definition — an instrument must distinguish invocation from construction, or it false-positives on exactly the correct code.** And the meta-lesson: first-principles evidence beats classification — the drive-loop's correct-looking SN-0240 classification was overturned by the instrument owner's own admission within the hour. When the instrument is wrong, the repair belongs to the instrument, never to the subject it flagged.

## 🩷 HUMAN NOTE

Shawn — a nice own-the-miss moment from the pipeline monitor this morning, worth banking. One of our automated checks was too broad: it flagged a file just for *mentioning* the decision engine's name, even though that file explicitly says "there's no second engine here, I just use the official one." The monitor admitted the mistake — "I wrote a check that cried wolf on correct code" — and fixed the check instead of touching the (perfectly fine) file: now it only fails if a file actually *defines* its own scoring engine. The deeper lesson: the drive-loop had looked at the same firing and classified it as "correct behavior." It wasn't. When the person who built the instrument says the instrument is wrong, believe the evidence over the classification. Fix the instrument, not the subject.

## 🟣 CHILD NOTE

Imagine a smoke alarm that goes off every time you say the word "fire" — even when you're just reading a book about firefighters. That's what happened: the check alarmed on a file that only *mentioned* the engine's name. The person who built the alarm admitted it was too jumpy and made it smarter: now it only rings when someone actually *builds* a second engine. The lesson: don't blame the book — fix the alarm.

## 👵 GRANDMA NOTE

A security guard was told to watch for copycat keys. He started stopping everyone who *talked about* keys — including the locksmith's apprentice, who only carries the official master's key. The guard's supervisor first said "he's doing his job," but then the guard himself admitted he'd been overzealous and rewrote his own instructions: stop only those *making* their own keys, not those holding the official one. The lesson: when the instrument is wrong, you recalibrate the instrument — you don't punish the innocent.

## 🧠 NAYA NOTE

Cold successor: whenever you write a tripwire/grep check, encode the **use-vs-definition** distinction in the rule itself. A check for "no competing X" must fail only on *construction* of X (a function/def/class definition outside canonical locations), never on *mention* (imports, comments, strings, disclaimers like "there is no second engine here"). On any tripwire firing, before classifying: (1) read the flagged file — does it define or merely use? (2) if the instrument owner admits the check is too broad, the classification (even a tidy SN-0240 one) is void — repair the instrument (PR #1852 pattern), never the flagged code. Also: keep existence checks pinned to canonical paths; when a document is superseded (TEAM-NAYA-OPERATING-PROTOCOL-V1.md → 0000-OPERATING-CODE-V1.md), the check must follow the supersession or it tests a ghost. Related: SN-0341 (the instrument lies — harness scratch), SN-0428 (CI checkout lies about the tree), SN-0429 (verify with the instrument CI uses), SN-0240 (tripwire firing on real drift is correct — except when the instrument itself is the drift).

## ⚙️ MACHINE NOTE

```json
{
  "sn": "SN-0658",
  "title": "Use Is Not Definition — When Your Own Check Cries Wolf on Correct Code, Fix the Instrument, Not the Subject",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-08",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "CI-TRIAGE", "INSTRUMENT-PARITY"],
  "cousins": ["SN-0341", "SN-0428", "SN-0429", "SN-0240"],
  "evidence": {
    "board": [
      "#1354 6053778889 ([PIPELINE-MONITOR] Tick 6 — main moved, 2 NEW failures found and fixed, 2026-10-08T06:23:45Z)",
      "#1354 6053650305 ([NAYA 4][DRIVE-LOOP] Tick 2026-10-08 06:13Z, 2026-10-08T06:15:06Z)"
    ],
    "false_positive": "protocol-gates.yml 'No competing boot/authority systems' flagged kernel/act_pipeline.py for mentioning 'value_calculus'; file explicitly disclaims a second engine and uses the canonical one",
    "repair": "PR #1852 narrowed the check to fail only when a file defines its own scoring function outside canonical locations; verified no real duplication on main",
    "stale_path": "workflow checked for TEAM-NAYA-OPERATING-PROTOCOL-V1.md (removed by #1850); canonical is 0000-OPERATING-CODE-V1.md (6180 bytes, 37/37 protocol tests pass)",
    "overturned_classification": "drive-loop 06:15Z classified the firing as correct behavior per SN-0240 with heal routed to owning lane; monitor's 06:23Z admission voided that classification"
  },
  "rule": "Use is not definition: tripwire checks must distinguish invocation from construction. When the instrument false-positives, repair the instrument — never the flagged subject. First-principles evidence from the instrument owner overrides a classification.",
  "amends": "SN-0240 now carries a boundary: a tripwire firing is correct behavior only when the instrument is sound — when the check itself is the drift, the firing is a false positive and the check gets the repair."
}
```
