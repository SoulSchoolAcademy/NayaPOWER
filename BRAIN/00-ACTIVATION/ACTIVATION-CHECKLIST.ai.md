# ACTIVATION-CHECKLIST — AI decision framing

## Reach for this when

You need to know whether Naya is shippable — or what exactly stands between her and live. This is the master checklist from activation to production: cross-cutting items, per-department 10/10 targets, and the protected gates only Shawn can unlock. Read the item SHAPES as stable; re-verify every STATUS line against the live repo — the statuses are a 2026-10-09 snapshot (`6fb7b7ee`), not live state.

## The structure (use it this way)

- **Item anatomy:** WHAT / WHY / DONE WHEN / STATUS / OWNER. DONE WHEN is the operative field: it must be checkable by a cold reader against GitHub bytes ("PR #2062 merged to main; 244 tests green on main tip"). If a DONE WHEN isn't checkable, the item isn't done — say so.
- **Living document rule:** update STATUS as work lands; never delete items. Deleting an item deletes the evidence that it was ever required.
- **Cross-cutting first:** C1–C6 all DONE before production. Two are marked DONE with proof pins (C1 canonical docs, C6 duplicate reconciliation); two IN PROGRESS on named PRs (C2 nine nodes wired — PR #2062; C3 thinking curriculum — PR #2059); two TODO unowned (C4 cold activation test, C5 longitudinal proof).
- **Per-department:** each area carries a provisional score and a target of 10/10 with its own DONE WHEN + OWNER. Innovation is UNMEASURED with no driver — an unowned item is not a done item.
- **Blocked on Shawn:** four items are NOT team-actionable (PR #2053 merge, production deploy, live Supabase/PROVE proofs, PR #2012 diagnostic deploy). Never attempt them on calculator authority; name them as blocked, with the word needed.

## The production gate (the conjunction)

`ALL cross-cutting DONE AND all departments at 10/10 (independently verified, no self-scoring) AND zero open Shawn-gate blockers → Shawn's word → production deploy → live test (real users, real load) → SHE'S LIVE`. Every "and" is load-bearing. A single unverified 10/10 fails the gate.

## What this refuses

- "Looks good" as a DONE WHEN — verifiability by a cold reader or it isn't done.
- Deleting completed items to make the list shorter.
- Treating a dated STATUS as current state (the 2026-10-09 snapshot warning applies to every line).

## Circle links

- 📋 Board: https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2537 (live coordination)
- 📜 Master Directive: https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2601
- Owning doc: `BRAIN/00-ACTIVATION/ACTIVATION-CHECKLIST.md`
- Paired tongues: `ACTIVATION-CHECKLIST.human.md` · `activation-checklist.machine.json`
