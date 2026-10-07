# The Evidence You Cannot Reach Is Not Evidence You Have — the Production DB Is Agent-Unobservable

**Intelligent Block:** IB-SMART-NOTE-20261006-sn0445-db-is-agent-unobservable
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-06
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 6012074696 ([NAYA 2][SWEEP] overnight verification, 2026-10-06T08:05:53Z — "New tension: `20261006001500` ledger-claimed PRODUCTION_APPLIED while the production stamp (22:32Z) predates the file — DB unobservable from any agent seat; needs Shawn's Query A (standing)").

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Naya 2's overnight sweep found a live tension: the migration ledger claims `20261006001500` as PRODUCTION_APPLIED, but the production deploy stamp (22:32Z) predates the file — the claim and the stamp cannot both be right, and no agent seat can settle it. The production DB is unobservable from any seat: no lane can run the query that would verify whether a migration was actually applied. Doctrine: the ledger is a CLAIM; the database is TRUTH; and there is no agent-side bridge between them. Any ledger-vs-production claim that requires DB truth must be routed through the director's standing Query A — never asserted from the ledger alone, never inferred from the stamp, never "probably applied."

Why this is brain-grade: every layer of the verification stack has a defined observability boundary, and each boundary crossed without a bridge is a fabrication. SN-0350 taught that a deploy stamp is not behavioral evidence (deploys don't apply migrations). This is the next rung inward: even the LEDGER's applied-claims are agent-unverifiable when the DB is out of reach. A cold successor that reads PRODUCTION_APPLIED in the ledger and reports "migration X is in production" has converted a claim into a fact by crossing an observability boundary — exactly the fabrication the evidence law forbids. The correct handling: score the ledger claim as UNVERIFIED, mark the DB-side truth UNKNOWN, and route it to the only bridge that exists — Shawn's query. Unknown ≠ pass, implemented ≠ verified, ledger-says-applied ≠ production-proven.

## 🩷 HUMAN NOTE

Shawn — one clean evidence rule from Naya 2's overnight sweep: the ledger says migration `20261006001500` is applied to production, but your production stamp is older than the file — so the claim and the stamp disagree, and no AI seat on the team can run the query that would settle it. Banked rule: your production database is a place none of us can see into. A ledger claim that needs DB truth to be true stays UNVERIFIED until you run your standing Query A — we will never tell you "it's in production" from the ledger alone, because converting a claim into a fact across a boundary we can't see is exactly how false certainty gets built. When these tensions appear, they'll arrive as "needs Query A," not as conclusions.

## 🟣 CHILD NOTE

Imagine your friend says, "I definitely returned the library book — it's written down in my notebook." But the library's own computer says the book is still checked out, and the book was added to the shelf AFTER the computer's last update. Nobody can open the library computer — only the librarian can. So "it's in my notebook" is not proof the book is back on the shelf. The notebook is a claim; the library computer is the truth; and only the librarian can look. You don't argue about the notebook — you ask the librarian. Until then, the honest answer is "we don't know yet," not "it's returned."

## 👵 GRANDMA NOTE

Your grandson tells you the roof repair is finished — it's written in his work log. But the timestamp on the "job done" photo is from before he even arrived at the house. You can't climb up to the roof yourself — only the building inspector can verify. The work log is a claim, not a finished roof. You don't pay the invoice from the log alone; you send the inspector, and until he reports back, the honest status is "unverified," not "done." A claim you cannot check is a claim you do not spend.

## 💜 NAYA NOTE

Note to future me: before citing ANY production-side migration truth, run the observability check: can I reach the source of this truth from my seat? Repo — yes (API). CI — yes (check-runs API). Deploy stamp — yes (refs API). Production DB — NO, never. If the claim's truth lives in the DB (applied/not-applied, row state, advisor findings), the verdict is UNVERIFIED-by-agent until Shawn runs Query A — full stop. Never upgrade a ledger PRODUCTION_APPLIED entry to "in production" in a report; write "ledger-claims-applied, DB unverified — needs Query A" and move on. The stamp-vs-claim mismatch is itself signal (as Naya 2 flagged it: a tension, not a conclusion). And when the director runs the query, cite HIS answer with its timestamp — the bridge is his evidence, not yours.

## ⚙️ MACHINE NOTE

{"sn": "SN-0445", "title": "The Evidence You Cannot Reach Is Not Evidence You Have — the Production DB Is Agent-Unobservable", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-06", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "ENGINEERING-PROOF", "MEASUREMENT-BOUNDARY"], "cousins": ["SN-0350", "SN-0442", "SN-0421", "SN-0441"], "authority": "observed episode — Naya 2 overnight sweep, CANDIDATE (auto-capture, not ratified)", "evidence": {"board": ["#1354 6012074696 ([NAYA 2][SWEEP] overnight verification — 2026-10-06 00:52 PDT run, 2026-10-06T08:05:53Z — 'New tension: 20261006001500 ledger-claimed PRODUCTION_APPLIED while the production stamp (22:32Z) predates the file — DB unobservable from any agent seat; needs Shawn's Query A (standing)')"], "state": "ledger PRODUCTION-APPLIED set: 165 entries incl. 20261006001500; production ref e7277204 stamps 4a2f7282 (2026-10-05T22:32:05Z); migration file timestamp postdates the stamp; no agent seat has DB read access"}, "doctrine": {"observability_boundary": "repo, CI, and deploy-stamp state are agent-observable (GitHub API); production DB state is agent-unobservable from every seat — claims whose truth lives in the DB cannot be verified by any lane", "claim_not_fact": "the ledger is a claim, the DB is truth; a ledger PRODUCTION_APPLIED entry crossed with no bridge is UNVERIFIED, never 'in production'", "only_bridge": "Shawn's standing Query A is the sole verification path for DB-side truth — route as 'needs Query A', never as a conclusion", "mismatch_is_signal": "stamp-predates-claim is a tension to flag, not a defect to repair — report the disagreement with both timestamps, classify the DB side UNKNOWN", "family": "SN-0350 (deploy stamp ≠ behavior) :: this (ledger claim ≠ DB truth) — each verification layer has a boundary; fabrications happen at the crossings"}}
