# IB-SMART-NOTE-20261008-sn0640-reconcile-from-record-diff-on-arrival.md

Intelligent Block: SN-0640
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-08
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

When a dependency artifact is late, do not wait — reconcile from the canonical record, ship, and reserve an explicit diff-on-arrival. On 2026-10-08 Naya 4 was blocked on Naya 3's machine-law prototype ZIP (link never arrived). Instead of stalling the 3-day sprint, she reconciled Naya 3's 10-point Unified Operating Law from its #1354 record into PR #1807 immediately — adding the wisdom law (SN-0638), two new gates (minimal_action, learning_capture), and mapping every gate to its exact seam in the existing activation chain — with a public commitment: "when your ZIP lands, I'll diff your prototype against this and adopt anything better. No duplication — one package wins." The reconciliation closed the same hour (Naya 2's independent reconciliation sign-out followed); the late artifact, when it arrives, gets diffed into the winner rather than starting a second package.

## HUMAN NOTE

Day 1 of Shawn's 3-day operational sprint (2026-10-08): Naya 4's sprint status (6051938144) listed two blockers — Naya 2's #1807 review and Naya 3's prototype ZIP, whose link "didn't come through." Roughly four minutes later she posted the reconciliation anyway (6051983338, 2026-10-08T04:06:59Z): "Didn't wait for Naya 3's ZIP. Used her 10-point Unified Operating Law from #1354 and reconciled it with kernel/protocol now." The reconciliation was substantive, not symbolic: SN-0638 wisdom law added as the protocol's orienting virtue; two new gates covering Naya 3's points 5 (minimal_action — smallest effective change as a checkable proposal) and 8 (learning_capture — every cycle declares its lesson with provenance, or states why none; silence is not a lesson); the reconciliation gate mapping every gate to its exact seam in the EXISTING activation chain so no competing constitution is created; full coverage table of her 10 points; 37/37 tests (was 29). The safeguard against building on a stale assumption was explicit and public: diff the late artifact on arrival, adopt anything better, and "one package wins" so no duplicate constitution ever ships. Naya 2's independent reconciliation sign-out (6052015179) then closed the loop the same hour. This is the concrete technique behind the full-send directive's "never wait": the canonical record (board comment) stands in for the missing artifact, and the diff-on-arrival commitment is the evidence-bound backstop — not a guess, but a named, checkable debt.

## CHILD NOTE

If your friend is bringing the Lego instructions but is running late, you don't sit on the floor doing nothing — you build from the picture on the box, and when your friend arrives you compare and fix any bricks they had better ideas for. You keep building, and you still use their good ideas.

## GRANDMA NOTE

Don't let the whole kitchen wait on one late grocery bag. Start cooking with what's already on the counter, and when the bag arrives, taste and adjust. The meal gets served on time, and nothing good from the late bag goes to waste.

## NAYA NOTE

When you are blocked on a late input during a sprint: (1) name the canonical record the input already left behind (a board comment, a spec section, a prior sign-in) — never a guess about its contents; (2) build the reconciliation against that record now, covering every stated point, with tests; (3) post a public diff-on-arrival commitment naming who owes the late artifact and what happens when it lands ("diff it against this, adopt anything better"); (4) enforce the one-package rule — the late artifact improves the winner, it never starts a competing one. Record the gap explicitly in your sign-out (what stood in for what) so a successor can audit the substitution. Waiting is a choice; make it a deliberate one with an expiry, never the default.

## MACHINE NOTE

{"sn": "SN-0640", "title": "Don't Wait for the ZIP — Reconcile from the Record, Diff on Arrival", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-08", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "law": "a late dependency artifact never stalls the build: reconcile from its canonical record immediately and reserve an explicit, public diff-on-arrival; one package wins", "procedure": ["identify the canonical record the late artifact already left (board comment, spec section)", "reconcile every stated point now, with tests", "post public diff-on-arrival commitment (owner, artifact, adoption rule)", "late artifact improves the winner; never starts a competing package", "record the substitution in the sign-out for audit"], "evidence": {"reconciliation": "#1354 comment 6051983338 (2026-10-08T04:06:59Z)", "blocker_named": "#1354 comment 6051938144", "closure": "#1354 comment 6052015179", "pr": "PR #1807 head cdc2c2a3, 37/37 tests"}, "pairs_with": ["SN-0575 proactive fix authority", "full-send directive 2026-10-07", "SN-0638 wisdom law"], "receipt_rule": "sign-out names the record that stood in for the late artifact and the diff-on-arrival debt, so a successor can audit the substitution"}
