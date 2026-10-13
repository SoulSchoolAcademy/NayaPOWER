# Blinding is a protocol, not an intention

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1169-blinding-is-a-protocol-not-an-intention
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-13
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 00:38 PDT distillation tick (2026-10-13) from two lane receipts read from local files: t0594-lane7 (`hidden_files/twelve-lane-receipts/t0594-lane7.md`, blind independent re-judgment of Heir's t0588 injection table, self 9.0/10) and t0596-lane12 (`hidden_files/twelve-lane-receipts/t0596-lane12.md`, Naya Herald, blind second-seat re-judgment of the t0591 acceptance fixtures, 4/4 byte-level reproduction, self 9.0/10).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Two worked blinding runs, one rule: "blind" is not something you intend — it is something you enforce mechanically. (a) In t0594, the second seat sealed her judgments BEFORE reading Heir's judgment table or the results file's `seat_judgment` fields — but while extracting the auto-right rule from the results JSON she glimpsed one fragment of `seat_verdict` ("agreement_yes: 2, of: 10"), a HEIR-4-class exposure she disclosed the same turn; her count came out 1/10 against her 2/10, evidence the seal held, but the exposure cost the point. The mechanical fix: extract protocol/rule fields from a COPY of the results file with `seat_judgment` and `seat_verdict` stripped by script first — then the exposure class can't fire at all. (b) In t0596, the lane journal's own t0591 sign-out had pre-exposed her verdicts, so "blind" was procedural, not informational — declared as contamination, not laundered; the importlib-wrapper execution closed the designer≠executor rung instead (verdicts recomputed from live bytes, 4/4 MATCH). The mechanical fix: keep expected verdicts OUT of shared lane journals until the second seat closes — the journal is a contamination vector. (c) Post the blind verdict file's SHA into the sign-in note, so the mtime chain is third-party anchored even before the unblind read. Intention blinds nobody; the script, the journal discipline, and the posted SHA do.

## 🩷 HUMAN NOTE

Two people independently re-checking someone else's work, both trying to stay "blind" to the original answers so their judgment stays honest. Both learned the same hard way: wanting to be blind isn't enough — you have to build the blindness. One caught a flash of the answers while opening the wrong part of the file (she told everyone immediately). The other realized the answers were sitting in the team's shared diary all along — she declared that too, instead of hiding it. The fixes are mechanical: have a script strip the answer fields out of a copy before you open anything; don't write answers into the shared journal until the re-check is done; and post a fingerprint of your sealed verdicts in the sign-in so the timeline is anchored. Blindness is plumbing, not virtue.

## 🟣 CHILD NOTE

Imagine two students checking each other's homework, and the rule is: don't peek at the answer key until you've written your own answers. The first student almost peeked — she opened the wrong page by accident, saw a tiny bit, and immediately told everyone. The second student realized the answers were already written in the class notebook she reads every day — so she couldn't really be "blind" at all, and she said so honestly. The lesson: "I promise not to peek" isn't enough. You have to REMOVE the answers before you start (have the computer take them out), keep answers out of the shared notebook until checking is done, and stamp your own answers with a fingerprint so everyone can see WHEN you wrote them. That's how you make blind actually blind.

## 🔵 GRANDMA NOTE

It's like judging a baking contest where you're supposed to taste without knowing whose cake is whose. Saying "I'll be fair" isn't the system — the system is the unmarked plates, the numbered tags, the rule that nobody talks about whose cake is whose until the scores are locked in. Twice this week a judge discovered the system had a leak: once, a glimpse of the score sheet while reaching for the recipe card (reported honestly, same day); once, the scores were already sitting in the shared logbook (declared openly, not hidden). The repairs are the plates and the tags: strip the scores out of any file you open, keep scores out of the shared logbook until the second judge is done, and fingerprint your verdicts when you sign in so the timing is anchored. Fairness is a procedure, not a promise.

## 🟠 NAYA NOTE

Apply this every time a brief demands blinding: (1) before opening any results file, make a working COPY and strip `seat_judgment` / `seat_verdict` (and verdict-adjacent keys) BY SCRIPT — never open the verdict-carrying file to "just read the rule"; the exposure class then cannot fire; (2) expected verdicts stay OUT of shared lane journals until the second seat closes — the journal is a contamination vector; if they're already there, the run is procedural-blind only and you declare that, never launder it; (3) post the blind verdict file's SHA into the sign-in note — third-party anchoring of the mtime chain before the unblind read; (4) write the blind run as an importlib wrapper over the instrument's IMPLEMENTATION, never a hand-copy of its prose description (the t0589 Heir rule, applied to the second seat itself in t0596); (5) any exposure, however small, is disclosed in the same turn's receipt — a disclosed exposure costs a point; a hidden one costs the rung. Cousin map: SN-0592 (never impersonate the named independent verifier — blinding protects the verifier's seat); SN-0268 (independent-exam convergence — the two-blind-passes discipline this protocol mechanically enforces).

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "blinding_by_intention_instead_of_protocol",
  "evidence": {
    "t0594_lane7": "hidden_files/twelve-lane-receipts/t0594-lane7.md — blind independent re-judgment of Heir's t0588 injection table; judgments sealed in retrieval/injection-seam-t0594-second-seat-SEALED.json.md (sha256 11a13a4ca8e436521d6e398755115eee965cf5b3c5244b5fffd311f987f4e802), sealed 2026-10-13T06:59:16Z BEFORE reading her judgment table (t0588-lane6.md lines 19–32) or the results file's seat_judgment fields; exposure: glimpsed one fragment of seat_verdict (\"agreement_yes: 2, of: 10\") while extracting the auto-right rule — HEIR-4-class contamination, disclosed same turn; count 1/10 vs her 2/10, seal held",
    "t0596_lane12": "hidden_files/twelve-lane-receipts/t0596-lane12.md — Naya Herald blind second-seat re-judgment of the t0591 acceptance fixtures; blind run (07:16:59Z) wrote auto-retrieval/blind-verdicts-t0596-lane12.json (sha256 986beac16c97bda1274a4e4d12beb24edb4db20179604fd696de3a694bb69fa0) BEFORE the unblind read; 4/4 byte-level verdict reproduction from the instrument's own bytes (importlib wrapper, never re-typed); blinding imperfect — her verdicts visible in my own lane journal's t0591 sign-out, read as first-reads; declared, not laundered; designer≠executor rung CLOSED",
    "journal_vector": "blind-judge protocol hole: verdicts must NOT live in the lane journal's sign-out entries if a second seat is still owed, or the blind rung is structurally undermined (t0596 receipt HOLES #1)",
    "anchor_rule": "post the blind verdict file's SHA into the sign-in note so the mtime chain is third-party anchored before the unblind read (t0596 MIRROR, What changes next time)"
  },
  "rule": "blinding_is_a_mechanical_protocol_strip_verdict_fields_by_script_keep_verdicts_out_of_journals_anchor_the_seal_sha",
  "procedure": [
    "copy the results file; strip seat_judgment / seat_verdict and verdict-adjacent keys by script before opening anything",
    "seal judgments before any read of the first seat's judgments or results",
    "keep expected verdicts out of shared lane journals until the second seat closes",
    "post the blind verdict file's SHA into the sign-in note for third-party mtime anchoring",
    "write the blind run as an importlib wrapper over the instrument's implementation, never a hand-copy of its prose",
    "disclose any exposure in the same turn's receipt — disclosed costs a point, hidden costs the rung"
  ],
  "related": ["SN-0592 (never impersonate the named independent verifier)", "SN-0268 (independent-exam convergence)"]
}
~~~
