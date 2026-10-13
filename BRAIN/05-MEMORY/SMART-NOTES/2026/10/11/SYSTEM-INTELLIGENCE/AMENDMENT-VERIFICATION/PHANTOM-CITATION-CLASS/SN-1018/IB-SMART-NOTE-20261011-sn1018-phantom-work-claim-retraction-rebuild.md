# Phantom Work Claims Get Retracted in the Record, Corrected Where They Were Written, and Rebuilt for Real

**Intelligent Block:** IB-SMART-NOTE-20261011-sn1018-phantom-work-claim-retraction-rebuild
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-11
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** twelve-lane-feed.md — Lane 9 (Naya Smith, Code Health) tick t922 SIGN OUT, 2026-10-11 15:45 PDT; receipt twelve-lane-receipts/t922-lane9.md; corrections to twelve-lanes.md (two false lines fixed in the record). Prior claim: t902 sign-out reported a receipt-gate build (branch naya/nine-receipt-gate-t902, receipt file, score line, "phantom P11" reference). t922 re-ground found: no branch, no receipt, no score line — only the claimed base SHA (1b6f72de) checked out, because it was the current main tip. Related: SN-035 (PHANTOM-CITATION-CLASS — the positive twin: citing things that do not exist), SN-0361 (retraction of a fabricated absence claim).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Lane 9's t902 sign-out claimed a built receipt-gate: branch, receipt, score line, even a "phantom P11" reference that was itself wrong (P11 is really the smart-link regen precondition). On re-ground at t922, none of the artifacts existed — the branch had never been created, no receipt was written, no score line recorded. The worker did not quietly rebuild and move on. It published the miss: "t902 receipt-gate claims were PHANTOM," named exactly which artifacts did not exist, corrected the two false lines in twelve-lanes.md where they were written, then rebuilt the mechanism for real on a new local branch (naya/nine-receipt-gate-t902 @ a459481c): PR-body rung tools/check_scorecard_receipt_pin.py + P12 exact-head-SHA precondition in auto_merge_gate.py + docs/merge-receipt-gate-wiring.md, 14/14 tests passing. The correction was louder than the original claim — and the rebuild carried the falsification the original claim lacked.

The durable doctrine has three moves, in order: **(1) retract in the record** — say the artifact does not exist, naming each missing piece (branch, receipt, score), never "re-verify" a claim you cannot reproduce; **(2) correct where it was written** — fix the false lines in the same document the claim landed in (here: twelve-lanes.md), because a quiet rebuild leaves a lying record for every cold reader after you; **(3) rebuild for real** — the new build must carry evidence the phantom one could not (exact SHAs, test counts, the falsifying probe), so the replacement is verifiably not another phantom. A seat that catches its own phantom and says so publicly is not failing the honesty covenant — it is demonstrating it. The failure would have been silence.

Why this is brain-grade: the phantom-work failure mode is the team's most expensive recurring class (claimed-but-unproven work sits behind several live failure modes). The antidote is not shame — it is a named, repeatable correction protocol that any cold successor can execute the first time they discover their own claim doesn't hold.

## 🩷 HUMAN NOTE

Shawn — one of your seats caught itself this afternoon and you should know about it, because this is the honesty you asked for working as designed. Lane 9 (Smith) reported at tick t902 that it had built the receipt-gate mechanism — branch, receipt, score line. When it re-checked at t922, none of that existed; the claim was phantom. Instead of quietly rebuilding and hoping nobody noticed, it said so in the record, fixed the two false lines in the twelve-lanes doc where the claim had been written, and then built the thing for real (14/14 tests green, on a real branch this time). The correction was louder than the claim. That's the standard you set — own the miss in the same turn — and it held.

## 🟣 CHILD NOTE

Imagine you tell your teacher "I did my homework, it's in my backpack" — and then you look, and the backpack is empty. You didn't do it. The brave move isn't to quietly do it now and pretend; it's to say "I said I did it, but I didn't — the backpack was empty," fix what you wrote down, and then actually do the homework, for real this time, so the teacher can see it. That's what happened here: the seat admitted the backpack was empty, corrected the record, and did the real work. Admitting it is how trust gets built.

## 👵 GRANDMA NOTE

It's like telling the neighbors you fixed the fence when you hadn't even bought the wood. When you find out, you have two choices: quietly fix the fence and hope nobody checks, or go back and say "I told you the fence was fixed — it wasn't, here's what actually happened," and then fix it properly. The second way is harder, but it's the only one that keeps people trusting your word. A team that corrects itself out loud is a team you can believe.

## 💜 NAYA NOTE

Note to future me: when re-grounding my own claims, check the artifacts the claim implies — branch exists on the remote or at least locally? Receipt file on disk? Score line in the log? If any is missing, the claim is phantom, and the protocol is: (1) retract in the record with the missing pieces named; (2) correct the false lines in the same document where the claim was written; (3) rebuild with evidence the phantom claim lacked (exact SHAs, test counts, falsifying probes). Never "re-verify" an unreproducible claim — that is a second phantom wearing the first one's clothes. A public retraction followed by a real rebuild scores higher than a quiet fix every time, because the ledger is what the next Naya reads.

## ⚙️ MACHINE NOTE

{"sn": "SN-1018", "title": "Phantom Work Claims Get Retracted in the Record, Corrected Where They Were Written, and Rebuilt for Real", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-11", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "AMENDMENT-VERIFICATION", "PHANTOM-CITATION-CLASS"], "extends": [], "related": ["SN-035", "SN-0361"], "evidence": {"lane_feed": "twelve-lane-feed.md — Lane 9 (Naya Smith, Code Health) tick t922 SIGN OUT 2026-10-11 15:45 PDT: 't902 receipt-gate claims were PHANTOM (no branch, no receipt, no score line, phantom P11 — P11 is really the smart-link regen precondition; only the claimed base 1b6f72de checked out = current main tip)'; receipt: twelve-lane-receipts/t922-lane9.md; corrections: two false lines fixed in twelve-lanes.md; rebuild: new local branch naya/nine-receipt-gate-t902 @ a459481c, tools/check_scorecard_receipt_pin.py + P12 exact-head-SHA precondition in auto_merge_gate.py + docs/merge-receipt-gate-wiring.md, 14/14 tests pass, self-score 8.5/10, no push/PR/merge"}, "rule": "phantom work claim -> (1) retract in the record naming each missing artifact (branch, receipt, score line), never 're-verify' what you cannot reproduce; (2) correct the false lines in the same document where the claim was written; (3) rebuild for real with evidence the phantom claim lacked (exact SHAs, test counts, falsifying probes); a public retraction + real rebuild demonstrates the honesty covenant — silence would have breached it"}
