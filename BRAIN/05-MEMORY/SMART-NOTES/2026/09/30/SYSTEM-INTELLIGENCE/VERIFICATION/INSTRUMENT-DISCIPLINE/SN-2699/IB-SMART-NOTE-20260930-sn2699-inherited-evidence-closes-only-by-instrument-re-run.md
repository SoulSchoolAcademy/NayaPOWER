# Inherited Evidence Closes Only by Re-Running the Instrument — and a Re-Run Needs the Bytes, Not Just the Sha

**Intelligent Block:** IB-SMART-NOTE-20260930-sn2699-inherited-evidence-closes-only-by-instrument-re-run
**Smart Note:** SN-2699
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-12
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

A gap that names "inherited evidence" closes only when a different seat re-runs the instrument with its own hands: re-reading the receipt is not re-verification. And a sha pin must carry the bytes — snapshot the log bytes alongside the sha, or the next seat cannot re-run the tally on the exact historical bytes.

## 🩷 HUMAN NOTE

When one seat's verdict rests on evidence it inherited from another seat, the only thing that closes the gap is a second seat doing the work again — fresh clone, same instrument, quoted exit codes. Reading the first seat's receipt again just re-reads the same words; it cannot catch the first seat's mistake, because the mistake would be in the words being re-read. The t0548 gap is the worked example: the second seat re-ran the first-parent walk and the `--check` instrument at three commits (bf16b098 exit 0 CLEAN; 715bce27 exit 1 DRIFT; 6a5aaed46 exit 1 inherits) and flipped the attribution — introducer PR #2446, PR #2448 inheritor plus merge-discard — while holding the heal. The corollary bites just as hard: the 36-line log snapshot no longer exists on disk, so the t0539 tally could not be re-run on the exact historical bytes. The sha chain across the two receipts held, but the tally re-run was one verification short. A pin that names a sha without preserving the bytes proves identity of a record, not reproducibility of the tally.

## 🟣 CHILD NOTE

If your friend tells you they checked something, you don't just read their note again to be sure — you go and check it yourself, with your own hands. And if you want someone else to check your work later, you have to save the actual thing you checked, not just its name.

## 🔵 GRANDMA NOTE

Trust, but verify by doing it yourself. If someone says "I already checked," the next person still has to run the check themselves — otherwise the same mistake just gets passed along in nicer handwriting. And always keep the paper you measured from, not just the number you wrote down, or nobody can ever measure it again.

## 🟠 NAYA NOTE

Gap-closure acceptance rule, distinct from P1 (prove it on live bytes, the general rule): this is what counts as closing inherited evidence. A scorer or dispatcher judging a gap closure demands the instrument re-run with quoted exit codes from a different seat, never a re-read. Future slice-(c) briefs snapshot the log bytes alongside the sha. Honest scope: no independent scorer for the t0548 receipt yet; the t0550-class stale-detector misfire and the slice-(c) conditional re-tally remain routed, not implemented; the 10-vs-13 merge-count variance is named, not smoothed. Cousins: SN-1144 (seal the unrunnable), CANDIDATE 700 (an absence claim cites its query — re-fire, don't inherit), P1, P3 (count seats out loud).

## 🟢 MACHINE NOTE

```json
{
  "smart_note": "SN-2699",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-11-12",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "applies_when": ["gap-closure", "inherited-evidence", "second-seat", "verification", "receipt"],
  "enforcement": "A scorer or dispatcher judging a gap closure that names inherited evidence must demand the instrument re-run with quoted exit codes from a different seat before accepting the closure; a closure citing only a re-read is refused. Slice-(c) briefs snapshot the log bytes alongside the sha (brief-template check).",
  "decision_change": "A scorer or dispatcher judging a gap closure now demands an instrument re-run with quoted exit codes from a different seat, not a re-read of the parent receipt.",
  "falsifier": "A gap closed by re-read alone whose verdict later survives a second seat's instrument re-run unchanged — that would mean the re-run added nothing and the acceptance rule is over-strict.",
  "mechanism": "Re-reading propagates the original seat's errors and assumptions; only re-running the instrument on live bytes can falsify the inherited verdict. A sha without the bytes cannot be re-run, so the pin proves identity of a record, not reproducibility of the tally.",
  "evidence": [
    "twelve-lane-receipts/gap-t0548-lane3.md (2026-11-12): second-seat re-verification — fresh clone, first-parent walk d998cac4..501bf82a in t1292's exact order, index blobs at 6a5aaed46 == 1st parent 916b9271b and != 2nd parent d5015eb7c, --check instrument re-run at three commits (bf16b098 exit 0 CLEAN; 715bce27 exit 1 DRIFT; 6a5aaed46 exit 1 inherits). D1 HOLD sharpened AGREE; D2 FLIP on attribution (introducer PR #2446, PR #2448 inheritor + merge-discard), HOLD on the heal.",
    "CORE-PRINCIPLES.md CANDIDATE 1028 (2026-11-12): 'Inherited evidence closes only by re-running the instrument — and a re-run needs the bytes, not just the sha.'",
    "learning-events-2026-11-12-04.md: gap-t0548 closure learning event; the 36-line log snapshot is gone, so the t0539 tally could not be re-run on exact historical bytes."
  ],
  "cousins": ["SN-1144", "CANDIDATE 700", "P1", "P3"],
  "provenance": "gap-t0548-lane3.md receipt (Naya Clarity Narzan, Lane 3 Judge hat, 2026-11-12 ~04:13-04:35 PST); filed as LEARNING event in learning-events-2026-11-12-04.md"
}
```
