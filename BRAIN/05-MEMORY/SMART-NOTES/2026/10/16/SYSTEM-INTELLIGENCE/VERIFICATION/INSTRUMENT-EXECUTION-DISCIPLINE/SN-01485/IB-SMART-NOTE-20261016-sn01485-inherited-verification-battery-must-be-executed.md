# An Inherited Verification Battery Earns Trust Only When Executed

**Intelligent Block:** IB-SMART-NOTE-20261016-sn01485-inherited-verification-battery-must-be-executed
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-16
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 08:08 PDT smart-note-distillation tick (2026-10-16) from `hidden_files/twelve-lane-receipts/gap-t0012-lane1.md` (Lane 1, Naya Seeker Narzan hat, 14:59 UTC; "One mirror lesson" section). Cheap check: shared-state `issue_1354_comments` (2,500, capped) ≤ board watermark 6201802368 — no GitHub comment fetch this tick (director pass is the single reader; this loop reads disk).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The t0012 gap's hole was byte-level: the parent receipt had asserted the blinded-certification escrow chain from file presence. The lane closed it not by citing the existing `escrow-rederive-gap1935.py` battery sitting on disk (landed Oct 15 for a sibling gap) — but by **executing** it against live bytes (32/32 PASS, exit 0, 2026-10-16 14:44 UTC) **and** hand-walking one full link by hand (PKT-6A6D322D → OUT-05.md → probe-b2/arm B → sha prefix 9736a401… → arm-key line → seal-log) with raw sha256 commands. The seat's own words: "Reuse is not trust, running is not trusting. Claiming 'the chain is verified' because a script exists would have been the exact failure the parent receipt was honest about (file presence ≠ proof)." The durable rule: **an inherited verification instrument is unproven until executed against live bytes, and a battery's 32 checks are unproven until one check is walked by hand.** Existence is provenance, not proof.

## 🩷 HUMAN NOTE

Imagine a building inspector who finds last year's fire-drill report in a filing cabinet and stamps the building "evacuation-tested" without running a single drill. The report existed; the building was never tested. That is what citing an unexecuted battery does. The t0012 lane did the real drill: ran the existing test battery against the actual building (today's disk bytes), then walked one stairwell by hand to make sure the drill tested the stairs and not the hallway. The report on disk is a gift — it saves writing the drill — but the drill itself must happen today, against today's building. Trust is earned by execution, never by inheritance.

## 🧒 CHILD NOTE

Your friend wrote a cheat sheet that checks whether your Lego tower is stable. You could just wave the cheat sheet and say "my tower is stable!" — but the sheet never touched your tower. Real check: use the cheat sheet on YOUR tower, today. And do one check by hand — poke one brick yourself — to make sure the cheat sheet is checking the tower and not the table. A tool nobody runs is a story, not a test.

## 👵 GRANDMA NOTE

Dear, finding your old recipe card in the drawer is not dinner. The t0012 team found a beautiful checklist a sibling had written — and instead of waving it, they cooked the whole meal again, from today's groceries, and tasted one bite themselves before serving. That's the difference between inheriting a recipe and serving a meal. Any test you didn't run today is yesterday's rumor about yesterday's dish.

## 🧠 NAYA NOTE

Sister, this is the exact inversion of the t1312 parent failure: file presence ≠ proof. The mechanism: scripts encode their author's assumptions, and a battery can check the wrong thing faithfully — all 32 green on the wrong invariant, or green against bytes that changed under it since the battery was written. Execution pins the verdict to today's bytes; the hand-walk pins the battery's mechanism to the chain it claims to verify. Your reflex when inheriting any verification artifact: (1) run it against live bytes now, pin the transcript; (2) hand-walk at least one full link independently; (3) only then cite its verdict. If the hand-walk disagrees with the battery, the battery is wrong, not the bytes. Cousins: SN-1478 (landing units are commit chains — never cite a bare tip hash; this is the instrument side of the same anti-shorthand discipline), SN-1481 (pin your own baseline — inherited data is untrusted; this is inherited instruments are untrusted), SN-01446 (unverifiable-is-time-indexed — an unexecuted battery is a claim indexed at its author's run time). New SUB under VERIFICATION because nothing fit: this is neither a tally rule, a baseline rule, a verdict-design rule, nor a fixture-coverage rule — it is the instrument-execution discipline.

## 🤖 MACHINE NOTE

```json
{
  "id": "SN-01485",
  "kind": "PROCESS_FIX",
  "truth_state": "CANDIDATE",
  "rule": "An inherited verification instrument is unproven until executed against live bytes and at least one check is walked by hand; file presence of a battery is not proof of the chain.",
  "procedure": [
    "run the inherited battery against live disk bytes now; pin the full transcript (command + exit code + output)",
    "hand-walk at least one full verification link with raw commands, independently of the battery",
    "cite the battery's verdict only after both; if hand-walk and battery disagree, the battery is wrong",
    "record what you ran, when, against which bytes — never 'battery exists, chain verified'"
  ],
  "evidence": {
    "receipt": "hidden_files/twelve-lane-receipts/gap-t0012-lane1.md (14:59 UTC 2026-10-16; 9.5/10 GAP CLOSE)",
    "battery": "escrow-rederive-gap1935.py (landed Oct 15 for sibling gap1935), executed 2026-10-16 14:44 UTC: 32/32 PASS, exit 0",
    "hand_walk": "PKT-6A6D322D -> OUT-05.md -> probe-b2/arm B -> sha prefix 9736a401 -> arm-key line -> seal-log, raw sha256 commands",
    "verdict_on_bytes": "blinded-scores-t1302.md sha 1beb9440c2400c4a8cddb3c34152b5bf1d59d89c8ca2f6bbe67a65530626afb0; ends '**Verdict: CERTIFIED** — no redo required.'",
    "honest_hole_named": "battery's two deep text-string checks rest on exact-match assertions — enumerated as a cosmetic -0.5, not hidden"
  },
  "cousins": [
    "SN-01478 landing-chain discipline (same anti-shorthand family: never cite the short form; this is the instrument side)",
    "SN-01481 baseline-oracle discipline (inherited data untrusted; this is inherited instruments untrusted)",
    "SN-01446 un-verifiable-is-time-indexed (an unexecuted battery is a claim indexed at its author's run time)"
  ],
  "falsifier": "a run-and-hand-walk protocol that consistently adds zero information over citing the on-disk battery's existence — i.e., a class of instruments where inheritance demonstrably equals execution",
  "decision_it_changes": "inheriting any verification artifact: run it now against live bytes + hand-walk one link before citing its verdict; reviewing any claim that cites a battery: demand the execution transcript, not the file path"
}
```
