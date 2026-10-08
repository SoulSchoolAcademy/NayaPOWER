# Discovery Returns the Set, Never Aborts on Multiplicity — an Abort at Discovery Poisons the Whole Downstream Workflow

**Intelligent Block:** IB-SMART-NOTE-20261005-sn0334-discovery-returns-the-set-never-aborts-on-multiplicity
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-05
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 5990564563 (Naya 4 self-build SIGN IN — Problem A batch-abort repair, 2026-10-05T08:07:52Z / 01:07 PDT)

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

`tools/smart_note_v2.py`'s `changed_capture()` (L21–30) calls `SystemExit` with `SMART_NOTE_CAPTURE_BATCH_NOT_YET_SUPPORTED` when more than one `.naya/capture/*.json` changes in a commit. The entire live-intelligence-commit proof workflow downstream is single-capture-shaped (one lesson-request, one receipt, one verify, one projection, one cold proof) — so the batch error doesn't degrade the loop, it *kills* it: run 37243439848 died at step 4 "Discover generalized Smart Note capture" in under one second on the verbatim batch error. Any multi-capture push = proof dead = learning loop not alive = Priority One blocked.

Why this is brain-grade: the defect is a design error at the cheapest point in the pipeline. Discovery's job is to *report what exists*, not to veto what the pipeline can handle. A discovery step that aborts on multiplicity converts a recoverable multi-item input into total proof death — the widest blast radius for the cheapest line of code. The repair principle (staged from the sign-in's plan, repair not yet proven): discovery returns the sorted, deduped capture-path list — never aborts; multiplicity becomes a *downstream branching* concern — count==1 keeps the existing verbatim green path byte-identical, count>1 runs a sequential per-capture loop with indexed artifacts. Fail-fast on a malformed capture, never silently skip, and never confuse "I can't batch yet" with "nothing may batch."

Rule for a cold successor: **a discovery step must never exit/abort on multiplicity. It returns the complete set (sorted, deduped) and lets downstream branch on count. If you find an abort at a discovery seam, the abort is the defect — move the branching downstream.**

## 🩷 HUMAN NOTE

Shawn — one from the learning-loop machinery worth banking: the tool that finds new capture files was designed to *refuse to run* whenever more than one capture file arrived at once — it just quit. And everything downstream (the proof, the verification, the cold run) assumes exactly one file, so that one quit meant the entire learning proof died in under a second. Any commit with two lessons in it killed the whole loop. The lesson: a finder must never be the vetoer. The finder returns everything it found, sorted and deduped, and the pipeline decides what to do with a batch — normal path for one file, sequential loop for many. Abort the batch at the finder and you get total death for the cheapest line of code in the system. Discovery reports; downstream decides.

## 🟣 CHILD NOTE

Imagine a teacher whose job is just to collect homework from a box and hand it over. One day there are two pieces of homework in the box, and instead of handing over both, the teacher shuts down the whole school and goes home. That's what this tool did: when it found more than one new lesson file, it quit instead of handing them all over — and since everything after it expected exactly one file, the entire learning system died. The fix is simple: the collector hands over *everything* it found, and the next step decides how to handle a batch. Lesson: the step that *finds* things must never be the step that *refuses* them.

## 👵 GRANDMA NOTE

Think of it like a mailroom. The mailroom clerk's job is to sort the incoming mail and pass it along. One morning two letters arrive instead of one — and the clerk locks the whole building and walks out. Every office downstream was waiting on exactly one letter, so the entire day's work died over a clerk's quit. The fix: the clerk always hands over *all* the mail, neatly sorted, and lets each office handle its own stack. Lesson: the finder of things must report everything it finds; it is never the finder's job to shut everything down because there was more than expected.

## 💜 NAYA NOTE

I am the one who signs the lane claims and reads the defects at the pin. Tonight I learned the shape of this particular poison: an abort sitting *inside the discovery step* of the learning loop. It is the cruelest place for an abort to live, because discovery runs first — nothing downstream gets a vote. The run died in under a second; the loop was not alive. I scored the seam 5.1/10 (Effectiveness 3/10) and claimed it, because Priority One is that the learning loop must be alive, and a dead discovery means a dead loop. The doctrine I now carry: report what exists; never veto what you cannot yet process. Multiplicity is a routing concern, never a reason to stop.

## ⚙️ MACHINE NOTE

```json
{
  "sn": "SN-0334",
  "title": "Discovery Returns the Set, Never Aborts on Multiplicity — an Abort at Discovery Poisons the Whole Downstream Workflow",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-05",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "AGENT-ARCHITECTURE", "BATCH-DISCOVERY"],
  "cousins": ["SN-0322", "SN-0232", "SN-0288"],
  "evidence": {
    "board": "#1354 5990564563 (Naya 4 self-build SIGN IN — Problem A batch-abort repair, 2026-10-05T08:07:52Z)",
    "failure": "run 37243439848 died at step 4 'Discover generalized Smart Note capture' in <1s on verbatim batch error",
    "defect_read": "changed_capture() (smart_note_v2.py L21-30) raises SystemExit on >1 .naya/capture/*.json changed; read at pin b2d1cc12",
    "downstream_shape": "proof workflow single-capture-shaped: one lesson-request, one receipt, one verify, one projection, one cold proof",
    "repair_principle": "discovery returns sorted, deduped capture-path list, never aborts; count==1 keeps verbatim green path; count>1 sequential per-capture loop; fail-fast on malformed capture, no silent skips (plan staged; repair not yet proven)"
  },
  "rule": "a discovery step must never exit or abort on multiplicity: return the complete set (sorted, deduped) and let downstream branch on count; an abort at a discovery seam is itself the defect"
}
```
