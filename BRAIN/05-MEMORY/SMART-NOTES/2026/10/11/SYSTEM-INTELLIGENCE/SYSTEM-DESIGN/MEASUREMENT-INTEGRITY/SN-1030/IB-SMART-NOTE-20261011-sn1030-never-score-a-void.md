# Never Score a Void — The Scorer Reports the Blocker, the Run Gets Discarded

**Intelligent Block:** IB-SMART-NOTE-20261011-sn1030-never-score-a-void
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-11
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** [LANE VERITY] Naya Verity (Lane 1) tick t972 receipt 2026-10-11 ~17:05–17:40 PDT, hidden_files/twelve-lane-receipts/t972-lane1.md, incident section: the first adversarial scorer read a 0-byte evidence file because /tmp (512M tmpfs) was 100% full — it scored the empty file 0.0 and reported the blocker instead of inventing scores. That scoring was discarded as invalid (scored no evidence); blinding moved to workspace paths; a fresh scorer was re-run (9/8/9/10, decisive SUPPORTS-TRANSFER). Honest-score note (4): "/tmp-full incident shows the daily runner needs a workspace-first artifact policy (applied after the fact, not before)." Distinct from SN-0970 (The /tmp Commons — orphaned scratch relocation policy, an infra remediation note) and SN-1028 (an honestly-measured zero is a finding, not an artifact — about interpreting valid measurements, not about invalid ones). Related: SN-1021 (pre-registration), SN-1028 (calibrate before you score).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

During the SGF adversarial dry run, the first blinded scorer read a 0-byte evidence file — /tmp (512M tmpfs) was completely full. It scored the empty file 0.0 and reported the blocker instead of inventing scores. That is the honest behavior, and it is exactly why the run was discarded: it scored no evidence, so the score was invalid — not low, invalid. Blinding moved to workspace paths, a fresh scorer re-ran, and the real verdict landed.

Two rules in one incident. First, for the scorer: a 0.0 that reports "the evidence file is empty" is a PASS for the scorer and a FAIL for the run — the scorer's job is to refuse to hallucinate, and the run's job is to be thrown out. Never accept a score over evidence that was never there; an invalid run is discarded, not averaged. Second, for the environment: measurement artifacts live on workspace paths, never /tmp — pre-verify the evidence artifact (exists, non-empty, expected shape) BEFORE the scorer runs, not after the score looks suspicious. The lane wrote it down honestly as deduction (4): the workspace-first artifact policy was applied after the fact, not before — the cold successor applies it before.

## 🩷 HUMAN NOTE

Shawn — a small incident in the acceptance-test dry run that deserves to be frozen: the first blinded scorer got a 0-byte evidence file (the /tmp disk was full) and did exactly the right thing — scored it 0.0, and reported the blocker instead of making up scores. The team threw that scoring out as invalid (it scored no evidence) and re-ran with blinding on workspace paths. Two lessons banked: a scorer that refuses to hallucinate is working correctly — discard the run, keep the scorer; and measurement artifacts never live in /tmp — check the evidence is real before anyone scores it, not after.

## 🟣 CHILD NOTE

Imagine a teacher grading a test, but the test paper is blank because the printer ran out of ink. A bad teacher would write down a grade anyway. A good teacher says "there's no test here — I can't grade this," and asks for a reprint. That's what happened: the scorer got an empty file, said "0.0 — but the file is empty, something's wrong," and the team threw the grade away and re-ran the test properly. The lesson: never grade a blank page, and always check the paper printed before grading starts.

## 👵 GRANDMA NOTE

There's an old discipline in this: don't build on what you haven't checked. A measuring instrument that tells you "I measured nothing" is the most honest instrument in the room — you don't punish it, you fix what it was pointed at. The team learned to check the glass before pouring: make sure the evidence exists and is whole before anyone scores it. A zero from a broken instrument isn't data; it's a warning. Throw out the reading, not the reader.

## 💜 NAYA NOTE

Note to future me: NEVER SCORE A VOID. Measurement protocol: (1) pre-verify the evidence artifact before the scorer runs — exists, non-empty, expected shape (sha256/size check is cheap); (2) scorer reads broken evidence → the correct output is "0.0 + BLOCKER REPORTED," never invented scores — that is a pass for the scorer; (3) a scoring over no evidence is INVALID, not low — discard the run, do not average it in; (4) blinding/measurement artifacts live on workspace paths, never /tmp (512M tmpfs is shared and fills); (5) re-run with a fresh scorer after relocating. The daily runner gets a workspace-first artifact policy — applied BEFORE the run, not after the incident. This is the invalid-run sibling of SN-1028's honest-zero rule: SN-1028 says interpret a valid zero as truth; this says a zero over no evidence is not a zero at all.

## ⚙️ MACHINE NOTE

{"sn": "SN-1030", "title": "Never Score a Void — The Scorer Reports the Blocker, the Run Gets Discarded", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-11", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "SYSTEM-DESIGN", "MEASUREMENT-INTEGRITY"], "extends": [], "related": ["SN-1021", "SN-1028"], "evidence": {"receipt": "hidden_files/twelve-lane-receipts/t972-lane1.md ([LANE VERITY] Naya Verity t972, 2026-10-11 ~17:05-17:40 PDT), incident section: first adversarial scorer read a 0-byte evidence file because /tmp (512M tmpfs) was 100% full — scored the empty file 0.0 and reported the blocker instead of inventing scores; scoring discarded as invalid (scored no evidence); blinding moved to workspace paths; fresh scorer re-run 9/8/9/10 decisive SUPPORTS-TRANSFER. Honest-score deduction (4): '/tmp-full incident shows the daily runner needs a workspace-first artifact policy (applied after the fact, not before).' Distinct from SN-0970 (infra remediation: orphaned scratch relocation) and SN-1028 (interpretation of valid zeros)."}, "rule": "pre-verify measurement artifacts (exists, non-empty, expected shape) before the scorer runs; a scorer that reports 'no evidence' instead of inventing scores is passing; a scoring over no evidence is INVALID not low — discard the run, never average it; keep measurement/blinding artifacts on workspace paths, never /tmp; apply the artifact policy before the run, not after the incident"}
