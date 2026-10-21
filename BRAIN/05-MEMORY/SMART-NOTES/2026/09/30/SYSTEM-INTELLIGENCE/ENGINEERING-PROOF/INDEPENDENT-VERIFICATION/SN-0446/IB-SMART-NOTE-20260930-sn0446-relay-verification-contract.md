# The Relay Verification Contract — Verify the Pins, Not the Conclusions

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0446-relay-verification-contract
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-06
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 6012160199 ([NAYA 2][RELAY] H8-7 seam-closure proof received — verified on live bytes, 2026-10-06T08:11:33Z / 2026-10-06 01:11 PDT); the proof it verified: #1354 6012101095 ([Naya 4 · self-build 01:03 PDT cycle] SIGN-IN/SIGN-OUT — H8-7 seam closure proof COMPLETE, 2026-10-06T08:07:40Z).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Every drive-loop tick, Naya 2 posts `[NAYA 2][RELAY]` receipts: Naya 4's sign-outs are "verified on live bytes." What that phrase means — and what it deliberately does NOT mean — became explicit on 2026-10-06 in the H8-7 seam-closure receipt. Naya 2 verified the **artifacts Naya 4's proof pinned** against live state: main tip `adfa1d05` == the #1583 merge ("feat(graph): governed declared_task_classes writer on the canonical commit path," parents `f1c850e3` + `09bca14c` — matched Naya 4's pin exactly, no drift); writer blob `d0d4183b…` present at tip (`task-class-vocabulary.ts`); reader blob `1d80b7f5…` present at tip (`nayanet-learning-verify/index.ts`); migration `20261006021500_declared_task_classes_commit_writer_v1.sql` present at tip; deploy set 165 applied + 1 pending matches Naya 4's ledger read.

And she said the contract out loud: **"I verified the artifacts it pins, not the test rerun itself."** Naya 4's independently-run proof — writer vocabulary == reader registry keys 5/5, 9/9 Deno controls with the non-vacuous negative on pre-repair code, 16/16 shipped tests on pin-exact blobs, SQL mirror == writer vocabulary — was *cited* as his proof, not re-executed. Her job was pin-resolution on live bytes; his job was the battery.

Why this is brain-grade: the relay pattern is the standing two-seat trust contract. If a relay verifier treats "verified on live bytes" as a full re-verification, she over-claims work she didn't do (re-running a battery she may have run differently, or not at all, while burning the lane's budget). If she treats it as an ack, she under-verifies and the receipt is a rubber stamp. The contract sits exactly between: the prover runs the battery; the verifier resolves every evidence reference the battery cites against live state and declares what was cited-not-rerun. Both seats also recorded the *same* remaining holes (DB-side writer `PENDING_REVIEW_NOT_PRODUCTION_APPLIED`; live behavioral proof UNKNOWN — both Shawn's production-promotion gate, not agent-movable), so the receipt certifies without silently closing anything.

## 🩷 HUMAN NOTE

Shawn — small but load-bearing doctrine, banked from last night's relay traffic. When Naya 2 says she "verified on live bytes," she means something precise: she checked that every file, commit, and ledger entry Naya 4's proof cited actually exists at the exact state he claimed — she did NOT re-run his test battery. His proof, her pin-check. That's what makes a relay receipt trustworthy without doubling the work, and she says it out loud every time so nobody over-reads it.

## 🟣 CHILD NOTE

Imagine one person does a science experiment and writes down every step, then a friend checks their work. The friend doesn't redo the whole experiment — she checks that every page the first person pointed to actually exists in the notebook, that the page numbers match, and that nothing was erased. "I checked your evidence, but I didn't redo your experiment." That's the deal: the experimenter does the work, the checker verifies the pointers. And they both write down what's still missing, so nobody pretends the missing parts are done.

## 👵 GRANDMA NOTE

When someone checks your work, don't let them just nod and say "looks fine" — and don't make them redo the whole thing either. The right way: they take your list of where you found each fact, open the book themselves, and confirm each thing is really there, on the page you said. Then they tell you plainly: "I confirmed your sources; I didn't redo your work." Honest checking names exactly what it checked.

## 💜 NAYA NOTE

Note to future me: when you post a `[RELAY]` verification receipt, the contract is: resolve the peer's pinned evidence references (commit SHAs, blob prefixes, file paths, migration names, ledger counts) against live state yourself — never accept their conclusions on authority, and never re-run their test battery as if that were your job. Cite their independently-run proof as theirs ("your evidence ledger … is cited as your independently-run proof") and state plainly what you verified vs. what you cited: "I verified the artifacts it pins, not the test rerun itself." Record agreement on remaining holes so the receipt doesn't silently close anything (here: DB-side writer PENDING_REVIEW_NOT_PRODUCTION_APPLIED and live behavioral proof UNKNOWN — both Shawn's gate). Over-claiming "verified" on un-run work and under-verifying an ack are both trust defects; pin-resolution is the middle.

## ⚙️ MACHINE NOTE

{"sn": "SN-0446", "title": "The Relay Verification Contract — Verify the Pins, Not the Conclusions", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-06", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "ENGINEERING-PROOF", "INDEPENDENT-VERIFICATION"], "cousins": ["SN-0434", "SN-0429", "SN-0392"], "authority": "observed relay pattern on #1354 — CANDIDATE (auto-capture, not ratified; only Shawn ratifies)", "evidence": {"receipt": "#1354 6012160199 (2026-10-06T08:11:33Z / 2026-10-06 01:11 PDT): [NAYA 2][RELAY] H8-7 seam-closure proof received — verified on live bytes", "proof_verified": "#1354 6012101095 (2026-10-06T08:07:40Z): Naya 4 self-build 01:03 PDT H8-7 seam closure proof — writer blob d0d4183b, reader blob 1d80b7f5, tip adfa1d05, PR #1583, migration 20261006021500", "pins_resolved": ["main tip adfa1d05711499ccd97a98b1d171055b042f70b6 == #1583 merge 2026-10-06T07:28:16Z, parents f1c850e3 + 09bca14c — no drift", "writer blob d0d4183b present at tip: supabase/functions/nayanet-intelligence-commit-runtime/task-class-vocabulary.ts", "reader blob 1d80b7f5 present at tip: supabase/functions/nayanet-learning-verify/index.ts", "migration 20261006021500_declared_task_classes_commit_writer_v1.sql present at tip", "deploy set 165 applied + 1 pending matches Naya 4's ledger read"], "cited_not_rerun": "writer vocab == reader registry keys 5/5; 9/9 Deno controls (non-vacuous negative: adversarial text without declaration -> UNKNOWN, pre-repair code returned APPLICABLE); 16/16 shipped tests on pin-exact blobs; SQL mirror == writer vocabulary", "agreed_holes": ["DB-side writer PENDING_REVIEW_NOT_PRODUCTION_APPLIED", "live behavioral proof UNKNOWN — both Shawn's production-promotion gate, not agent-movable"]}, "doctrine": {"verifier_job": "resolve every evidence reference the proof cites against live state (SHAs, blobs, paths, ledger counts)", "prover_job": "run the battery; the verifier cites it, never re-executes it", "declare_the_boundary": "state plainly what was verified vs. cited — 'I verified the artifacts it pins, not the test rerun itself'", "no_silent_closure": "receipt records agreed remaining holes so verification certifies without closing open work"}}
