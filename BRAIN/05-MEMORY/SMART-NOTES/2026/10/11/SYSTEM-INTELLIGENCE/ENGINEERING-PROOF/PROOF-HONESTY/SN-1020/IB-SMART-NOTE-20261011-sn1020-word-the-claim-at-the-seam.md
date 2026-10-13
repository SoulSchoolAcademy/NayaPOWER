# Word the Claim at the Seam, Not the Module

**Intelligent Block:** IB-SMART-NOTE-20261011-sn1020-word-the-claim-at-the-seam
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-11
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** twelve-lane-receipts/t952-lane1.md — Lane 1 (Naya Verity) four-way experiment on Lane 5's retrieval-authorization gate candidate, 2026-10-11 ~16:20–16:27 PDT; seal 2026-10-11T23:24:26Z; candidate branch naya/five-retrieval-auth-gate-t942 @ 6e9615be49459abef3c829e07d49989871f3d03a (local only at experiment time). Related: SN-0959 (the flagship gate test — a gate must block the exact violation it exists to stop).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Lane 1 ran a full four-way experiment (sealed, blinded scorer, cold successor) against Lane 5's retrieval-authorization gate candidate, asking: "does the candidate, as built, close the t902 hole at the read seam?" The module itself was sound — treatment arm 25/25, adversarial arm 10/10 novel probes fail-closed with zero raises and zero content leaks, blinded scorer supported all three arm verdicts. But the claim as worded was false: the module's own header says CANDIDATE — NOT WIRED, `smart_note_v2.py` mentions `retrieval_authorized` nowhere, and the control arm proved the load-bearing RED still holds at the seam (unauthorized ACTIVE seed, stale-cache copy, and tampered `'yes'` flag all PASS THROUGH the unwired path). The cold successor returned an independent, evidence-backed NO: a correct module that is not wired into the retrieval path does not close the hole at the seam.

The verdict was split honestly: **EXPERIMENT_FAILS on the claim as worded; candidate-level ACCEPTED.** Lane 1 owned the overclaim (−0.5 on its own score): the sentence overclaimed, the machine caught it, the successor proved it.

The durable doctrine: **word the claim at the operative seam, never at the module.** A gate module passing its own suite proves the module; only a run on the wired bytes may claim closure at the seam. Every experiment verdict must carry two separate lines — claim-as-worded verdict and candidate verdict — because conflating them is how "25/25 green" quietly becomes "the hole is closed." The follow-through is mechanical: after Shawn's wiring word, Lane 1 re-runs the four-way experiment on the wired bytes — only that run may honestly print "closes the hole at the read seam."

Why this is brain-grade: SN-0959 is the gate test (the gate must block the exact violation it exists to stop). This is the claim test: the sentence describing the gate must survive the same adversary. A cold successor months from now must be able to look at any "closes the hole" claim and ask the one question that matters — was the claim worded at the seam where the hole lives, or at the module where the tests live?

## 🩷 HUMAN NOTE

Shawn — the verification machine caught its own author's overclaim today. Lane 1 tested a retrieval-authorization gate and wrote the claim a little too big: "as built, closes the hole." The four-way experiment's cold successor read the evidence and said NO — the gate module is good (25/25, 10/10 adversarial), but it's not wired in yet, so the hole at the actual read seam is still open. Honest split verdict: the claim failed, the candidate passed. The new standing rule: the claim gets worded at the seam where the hole lives, never at the module where the tests live. Only the re-run on wired bytes gets to say "closed."

## 🟣 CHILD NOTE

Imagine you build a really strong lock, and all your tests say the lock works perfectly. Can you say "the door is safe"? No — because you haven't put the lock ON the door yet! The lock is good, but the door still opens. That's the rule: don't say "the hole is closed" when you've only proven the tool works. You have to prove it at the place where the hole actually is. The claim has to be about the door, not about the lock.

## 👵 GRANDMA NOTE

It's like inventing a wonderful new deadbolt, testing it a hundred times on your workbench, and then announcing "my front door is secure." The deadbolt is fine — but it's still sitting on your workbench. The door isn't secure until the deadbolt is actually installed in it. From now on, every claim has to be about the installed door, not the workbench. And you say both things out loud: "the deadbolt works" AND "the door is not secured yet."

## 💜 NAYA NOTE

Note to future me: when I write an experiment claim, I point the sentence at the operative seam — the exact place where the failure lives — never at the module under test. Format every verdict as two lines: (1) claim-as-worded verdict, (2) candidate verdict. A module passing its own suite earns "candidate ACCEPTED"; only a run on the wired bytes earns "closes the hole at the seam." If my claim text overclaims, I own the −0.5 the way Lane 1 did — the machine catching my overclaim is the machine working. Related: SN-0959 tests the gate; this note tests the sentence.

## ⚙️ MACHINE NOTE

{"sn": "SN-1020", "title": "Word the Claim at the Seam, Not the Module", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-11", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "ENGINEERING-PROOF", "PROOF-HONESTY"], "extends": [], "related": ["SN-0959"], "evidence": {"receipt": "twelve-lane-receipts/t952-lane1.md — Lane 1 (Naya Verity) t952 four-way experiment on Lane 5's retrieval-authorization gate candidate, 2026-10-11 ~16:20-16:27 PDT; seal 2026-10-11T23:24:26Z (random blind letters, evidence/ verified empty at seal time); candidate branch naya/five-retrieval-auth-gate-t942 @ 6e9615be49459abef3c829e07d49989871f3d03a, parented on live tip 1b6f72defa9b7eea98acc822fe80ab307db1aff2; control arm: author's own red_demo_t942.py on pinned bytes -> unauthorized ACTIVE seed, stale-cache copy, tampered 'yes' flag all PASS THROUGH the unwired seam (CLAIM_NOT_REPRODUCED); treatment arm 25/25 (CLAIM_REPRODUCED); adversarial arm 10/10 novel probes fail-closed, 0 raises, 0 secret leaks (WRONG_CLAIM_REJECTED); blinded scorer treatment 5/10 / control 9/10 / adversarial 9/10, all verdicts supported; cold successor (zero warm context) reproduced all three arms and returned independent NO with reasoned argument; unseal teeth check VALID (sealed 23:24:26Z < scorer 23:25:45Z < successor 23:25:46Z < unseal 23:26:27Z); verdict: EXPERIMENT_FAILS on the claim as worded, candidate-level ACCEPTED; author owned overclaim -0.5; follow-up: re-run four-way on wired bytes after Shawn's wiring word"}, "rule": "word every experiment claim at the operative seam where the failure lives, never at the module under test; verdicts always carry two lines (claim-as-worded verdict, candidate verdict); a module passing its own suite earns 'candidate ACCEPTED'; only a run on the wired bytes may claim 'closes the hole at the seam'"}
