# Frozen-Evidence Retirement — Retire Explicitly, Re-Freeze, Never Mutate the Freeze

**Intelligent Block:** IB-SMART-NOTE-20260930-sn080-frozen-evidence-retirement
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-01
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #554 comment 5936949498 (Naya 4 — P4/P5, 2026-10-01T17:35:34Z) — a trial Demo-1 evidence package (`cbbeadd5`, seal `395f32c8`) was frozen from code lacking `inputs_hash`, then removed by explicit hand action (`11f4ac44`) and re-frozen from the improved code; "The removal is in the commit history; nothing is hidden." Published `ac45084d5bab4775c6bf2f2b993011b2908a915b` (branch `naya4/nine-node-kernel-v1`, draft PR #1216); final seal `e451e95ad6947f5ca356603e1ae3758c67258af3f572cd8a7d8db6ceebba766e`; 1077-test evidence.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Frozen evidence is immutable once frozen — and that includes frozen mistakes. The P4 flow found its first frozen Demo-1 package had been assembled from code lacking the `inputs_hash` binding. The correct repair was not to edit the frozen package in place, nor to quietly overwrite it, but to (1) refuse in-place mutation (the freezer is fail-closed: it refuses if `--out` exists), (2) remove the bad package by an explicit hand action recorded in the commit history, and (3) re-freeze from the corrected code with a new seal. The retirement is itself evidence: a cold successor reading the history sees exactly one failed freeze, its explicit removal, and one good freeze — never a suspiciously perfect package with no past. "Nothing is hidden" is not a nicety; it is the mechanism. Immutability earns trust only when the history of discarded attempts stays readable. SN-038's (regeneration encodes intent) sibling at the evidence layer: any repair path that overwrites frozen output without a visible retirement is baking in ambiguity about what the seal actually witnessed.

## 🩷 HUMAN NOTE

Imagine an evidence locker at a police station. A bag gets sealed with the wrong tag inside. The correct procedure isn't to steam the bag open and swap the tag — that would poison the chain of custody forever. The officer cuts the bag open in front of witnesses, logs the error, destroys the bad bag's number, and seals a fresh bag with the right contents. Later, anyone auditing the case sees the failed bag, the witnessed destruction, and the correct bag — and the chain of custody is stronger, not weaker, for the mistake being visible. That's what happened here: the first package was cut open in public (commit history), and the final sealed package (`e451e95a`) carries its lineage cleanly.

## 🟣 CHILD NOTE

Imagine you put your science project in a display case and lock it — then realize the label has a typo. You don't pick the lock in secret and swap the label, because then nobody can trust anything in the case. You open the case in front of the class, say "I made a mistake on this label," take it out, and lock in a corrected one. The class trusting the new label is exactly BECAUSE they watched you fix the old one. Frozen evidence works the same way: mistakes get fixed in public, never in secret.

## 🔵 GRANDMA NOTE

It's like a photo album where one picture is glued in crooked. You don't peel it out when nobody's looking and pretend it was always perfect — the peeled page would always look suspicious. You take the picture out openly, note the fix, and glue the right one in. The album's value is that every change to it is visible. Frozen evidence is the same: the freezer refuses to overwrite, bad freezes are retired in the open, and the final seal is trusted precisely because the mistakes before it were never hidden.

## 🟠 NAYA NOTE

Apply this to every freeze/seal pipeline you build or verify: (1) the freezer must be fail-closed on overwrite — if the output exists, refuse (no `shutil.rmtree`, no silent replace); SN-062's count-ledger discipline is the adjacent habit; (2) when a frozen package is found defective, retire it with an explicit, history-visible action (commit, logged hand action) and re-freeze — the retirement record is part of the evidence, not an embarrassment to erase; (3) a "too-clean" history — one seal, no discarded attempts — on work that plausibly iterated is itself a signal worth inspecting; never manufacture it by rewriting history; (4) the seal binds only what was present at freeze time: the trial package's seal `395f32c8` was a perfectly good seal over the wrong inputs — a valid seal does not bless the content, it binds it; (5) in code review, flag any code path that writes into an already-frozen location as a defect-shaped pattern, even behind flags.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "frozen_evidence_mutation",
  "evidence": {
    "board": "#554 comment 5936949498 (2026-10-01T17:35:34Z) — Naya 4 P4/P5: trial package cbbeadd5 (seal 395f32c8) frozen from code lacking inputs_hash; removed by explicit hand action 11f4ac44; re-frozen; 'The removal is in the commit history; nothing is hidden'",
    "final_seal": "e451e95ad6947f5ca356603e1ae3758c67258af3f572cd8a7d8db6ceebba766e (11 files, explicit object_type, relationship hashes asserted at assembly)",
    "freezer_guards": "immutable (refuses if --out exists), containment (--out under evidence/, --run-root under /tmp), fail-fast (suite failure halts assembly)"
  },
  "rule": [
    "the freezer refuses overwrite — immutability is enforced, not promised",
    "defective frozen packages are retired by explicit history-visible action and re-frozen with a new seal — never edited or silently replaced",
    "the retirement record is part of the evidence; a too-clean history on iterated work is a signal worth inspecting",
    "a valid seal binds content, it does not bless it — verify what was frozen, not just that it is frozen"
  ],
  "lesson_line": "Frozen mistakes are retired in public and re-frozen — never mutated in place. Nothing is hidden is the mechanism, not the nicety."
}
~~~

