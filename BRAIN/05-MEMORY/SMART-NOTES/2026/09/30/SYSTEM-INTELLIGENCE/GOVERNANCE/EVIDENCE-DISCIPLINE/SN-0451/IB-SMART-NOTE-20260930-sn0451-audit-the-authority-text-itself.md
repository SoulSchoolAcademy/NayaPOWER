# Intelligent Block: SN-0451
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-06
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL
Audit the ratified authority text itself — never trust memory's path claim for where it lives.

## HUMAN NOTE
Memory told me the ratified NAYA Design Contract v1.1 was on main at BRAIN/10-INTERFACES/NAYA-DESIGN-CONTRACT-V1.md (PR #1346). The live tree at tip 0a1353bc proved it absent — it exists only on PR #1346's unmerged branch. I almost audited the shipped Hub against the wrong document. The lesson: every cited artifact gets re-anchored on the live tip before it is trusted; memory's path claims are leads, not evidence.

## CHILD NOTE
When someone says "the rules are in the big book on the shelf," go look at the shelf yourself. The book might still be in someone's backpack.

## GRANDMA NOTE
Trust, but check with your own eyes. Even good memories can remember the wrong shelf.

## NAYA NOTE
This is the evidence law applied to provenance. Before any conformance audit, the audit's own authority document must be located on the exact SHA being audited. A conformance finding against the wrong contract version is a fabricated result.

## MACHINE NOTE
{"sn":"SN-0451","category":"GOVERNANCE","sub":"EVIDENCE-DISCIPLINE","evidence":["tip 0a1353bcade21f0c712d8ac793648facc09fbf6e","PR #1346 unmerged, head 6fc6cc04","recursive tree API shows no NAYA-DESIGN-CONTRACT-V1.md on tip"],"related":["SN-0350","SN-0388"],"admission":{"durable":true,"new":true,"signal":true,"evidence_backed":true}}
