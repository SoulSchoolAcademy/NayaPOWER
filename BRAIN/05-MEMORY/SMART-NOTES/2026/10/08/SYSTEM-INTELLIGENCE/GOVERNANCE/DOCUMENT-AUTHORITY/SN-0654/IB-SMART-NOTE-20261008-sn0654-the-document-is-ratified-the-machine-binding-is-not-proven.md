# IB-SMART-NOTE-20261008-sn0654-the-document-is-ratified-the-machine-binding-is-not-proven.md

Intelligent Block: SN-0654
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-08
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

A ratified governance document that names its machine-enforcement paths makes TWO claims: (1) the doctrine is ratified, (2) the doctrine is bound to those enforcement paths. Claim 1 is proven by the ratification record. Claim 2 is proven ONLY by finding those exact paths on the pinned tip's real tree. Naya 1 checked the 8 paths the Operating Code v1.0 names as its machine law against main at tip `aca944b5` — all 8 were absent. The doctrine was ratified; the binding was not yet real. Verify the binding against the tree, never the document.

## HUMAN NOTE

Shawn ratified the Operating Code v1.0, and the Code says its machine law lives in `kernel/protocol/*.py` plus a CI workflow. That sentence feels like proof. It isn't. Naya 1 (2026-10-08 ~05:50 UTC) did the unglamorous check: list the named paths, look them up in the exact current `main` tree (`aca944b5`). Zero of the eight existed — main had `tools/protocol/` and a separate unreconciled `kernel/protocol/` branch instead. Her verdict: "The doctrine is ratified. The claimed machine binding is NOT YET PROVEN." That's the highest-value hole, because it violates the very law being locked: law-as-code that names enforcement paths it doesn't have.

The seam was healed later the same morning: a re-check at main tip `65269857` found all 8 paths present (`authority_gate.py`, `quality_gate.py`, `takeover.py`, `cold_start_gate.py`, `cold_successor_test.py`, `minimal_action.py`, `learning_capture.py`, `.github/workflows/protocol-gates.yml`). The lesson survives the heal — the method is the point, not the finding.

## CHILD NOTE

If someone says "the rules are enforced by the robot guards in rooms A through H," don't just believe them — go walk through rooms A through H and see if the guards are actually there. Believing the paper is not the same as checking the rooms.

## GRANDMA NOTE

A beautifully written rulebook is not the same as the rules being followed. When the rulebook says "these are the locks on the doors," someone still has to walk the building and jiggle every doorknob. Naya 1 walked the building. The locks weren't there yet — until they were. Check the building, not the brochure.

## NAYA NOTE

This is the evidence-law family applied to governance claims: SN-0388 (a deployed URL is not the deployed product — fingerprint the served bytes), SN-0429 (verify with the instrument CI uses), SN-0350 (a deploy stamp is not behavioral evidence). The new member: a document's self-described machine binding is a claim about the tree, and claims about the tree are checked against the tree.

Cold-successor procedure when any governance document names enforcement paths:
1. Pin the tip (`git rev-parse HEAD` or the refs API).
2. Enumerate the named paths; check each against `git ls-tree -r <tip>` (or the recursive tree API).
3. Report PRESENT/ABSENT per path. If any are absent: the doctrine is ratified, the binding is unproven — flag it as the top hole, don't assume a future merge will carry it.
4. Re-check after any merge that claims to heal it; the decision expires when the tip moves (SN-0493).

Never merge two implementations to "reconcile" before this check — Naya 1's directive stands: no new system, reconcile existing lanes into ONE canonical implementation, then bind the Code to what actually exists.

## MACHINE NOTE

{"sn": "SN-0654", "title": "The Document Is Ratified; the Machine Binding Is Not Proven", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-08", "source": "#1354 comment 6053311131 (Naya 1, 2026-10-08T05:50:52Z); re-verified by Naya 4 at main tip 65269857", "method": "enumerate named enforcement paths, check against pinned tip tree", "finding_at_aca944b5": "0/8 paths present", "finding_at_65269857": "8/8 paths present", "family": ["SN-0388", "SN-0429", "SN-0350", "SN-0629", "SN-0493"]}
