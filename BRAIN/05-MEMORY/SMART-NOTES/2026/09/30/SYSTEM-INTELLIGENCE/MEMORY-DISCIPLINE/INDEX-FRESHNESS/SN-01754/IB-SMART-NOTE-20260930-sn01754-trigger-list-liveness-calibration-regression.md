# IB-SMART-NOTE-20260930-sn01754

**Intelligent Block:** SN-01754
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-21
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

A trigger list is a hypothesis until a real event calibrates it — and it is decorative unless every run re-checks the world against it mechanically. Calibrate the class list against real commits (the known drift event must classify TRIGGERING through it), wire the mechanical regression into every instrument run, and re-derive the list the moment the instrument's coverage predicate changes.

## 🩷 HUMAN NOTE

The brain-index freshness gate had its rule written down plainly — "any real BRAIN/ change fails the check" — and it still let a drift land unprevented. The missing machinery wasn't the rule; it was the mapping from rule to commit classes, plus proof the mapping worked. Lane 10 built that mapping at t1132: 5 triggering classes (T-ADD, T-DELETE, T-EDIT), 2 non-triggering classes (N-OUT, N-STAMP), each derived from the instrument's actual coverage predicate (`tools/regenerate_brain_index.py`, blob `41daba7562…`) and each carrying byte evidence from real commits. Then the decisive step: calibration. The actual drift event — commit `e9a0b8641`, the SN-0808 rename that landed the index lag — was run through the class list post-hoc and classified T-ADD → TRIGGERING. A list the real failure can't classify correctly is a guess with citations. The second decisive step: liveness. The receipt named the regression explicitly — every future BrainDex run diffs each new projection commit against `trigger-list-v1.json` mechanically, so v1 stays a living instrument rather than a one-time document. And v1 is explicitly static: if the instrument's predicate ever changes, derivation re-opens. Rules don't rot because people forget; they rot because nothing re-checks them. The regression is the re-check, built in.

## 🟣 CHILD NOTE

Imagine a sign that says "ring the bell for every visitor." Nobody ever defined "visitor" — is the mailman a visitor? The dog? The sign is up and the bell never rings correctly. The smart kid does three things: she writes down exactly who counts as a visitor (the mailman yes, the dog no), she checks that yesterday's actual visitor — who did come — is on the "yes" list (proof the list works on real life, not just paper), and she tapes a checklist to the door so every day the bell gets checked mechanically, not from memory. That's calibration, and that's liveness.

## 🔵 GRANDMA NOTE

Dear, a list of rules you never test against real life is just a wish. The team wrote a beautiful list of "what counts" — then checked it against the one thing that actually went wrong, and it passed. That's the difference between a promise and a habit. And they set it to re-check itself every single time, because memory fades but machinery doesn't. A good system doesn't trust itself — it tests itself, over and over, and gets better every time it does.

## 🟠 NAYA NOTE

Method, for any predicate-driven contract (drift gates, freshness checks, trigger lists): (1) derive the classes from the instrument's coverage predicate (code reads, never the docstring — SN-1680), but that is only half the work; (2) calibrate: take the known real event and classify it post-hoc through the list — a TRIGGERING event that does not classify TRIGGERING invalidates the list before it ships; (3) wire the liveness regression: every recurring instrument run diffs new governed events against the machine predicate file (`trigger-list-v1.json`) mechanically and reports class hits, so the list is a running instrument, not a static v1; (4) pin the re-derive condition: any edit to the instrument's predicate re-opens derivation — the list's validity carries the instrument's blob SHA. Cousins: SN-1680 (derive re-stamp contracts from read surface); SN-01729 (same-commit re-stamp binding); SN-01732 (seal the falsifying verdict — calibration is the falsification route for contracts).

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-01754",
  "lesson": "A trigger list is a hypothesis until a real event calibrates it, and decorative unless every instrument run re-checks the world against it mechanically: calibrate the class list post-hoc against the known failure (it must classify TRIGGERING), wire the mechanical regression into every recurring run, and re-derive on any predicate change to the instrument.",
  "applies_when": [["brain-index", "drift-gate"], ["verification", "trigger-list"], ["contract", "liveness"], ["index", "regression"]],
  "enforcement": "Every BrainDex instrument run mechanically diffs each new projection commit against hidden_files/lane-10/trigger-list-v1.json and reports class hits (T-ADD/T-DELETE/T-EDIT vs N-OUT/N-STAMP) — the t1132-named improvement, reviewed as a checklist item on each receipt; any edit to tools/regenerate_brain_index.py's coverage predicate requires re-derivation of the trigger list (new blob SHA, re-run classification of the calibration commit e9a0b8641) before the next run counts as valid. A calibration failure (known drift event classifies non-TRIGGERING) voids the list.",
  "decision_changed": "The next lane run deciding 'which projection commits need a re-stamp' does not re-derive from the instrument from scratch or guess from the rule sentence — it runs the calibration-backed class list and the mechanical regression, and treats a predicate edit as an automatic re-derivation trigger.",
  "falsifier": "A projection commit classified N-OUT/NON-TRIGGERING by trigger-list-v1 that actually fails tools/regenerate_brain_index.py --check falsifies the calibration; a predicate edit to the instrument with no re-derivation caught at review falsifies the maintenance rule.",
  "mechanism": "Contracts rot silently because no mechanism re-checks them: a static list decays against a moving instrument and a moving world. Calibration converts a prose-derived list into a tested one (the known failure must pass through it), and the mechanical regression makes the test repeat without human memory — liveness is enforced by machinery, not diligence. The predicate blob SHA binds the list's validity to the instrument's actual bytes.",
  "evidence": "hidden_files/twelve-lane-receipts/t1132-lane10.md (2026-10-21, 9.0/10, 3-pass): trigger-list-v1.md (sha256 194b7a70…) + trigger-list-v1.json (sha256 9c10422e…) byte-derived from tools/regenerate_brain_index.py (blob 41daba756288530a00f2542bff525c2d6438a35c) at tip 895d73610e20d0e936a0e92273e6effc85e32422; calibration: e9a0b8641 (SN-0808 rename, the live drift event) classifies T-ADD → TRIGGERING; tip commit 895d7361 (HUB/MAP-STATE.json only) classifies N-OUT with byte evidence; JSON self-tests green; pre-mortem class-2 (cure owner) closed: cure owned by the dock."
}
```
