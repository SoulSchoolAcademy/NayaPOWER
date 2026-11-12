# Resolve by Availability — Ordered Fallbacks, Recorded Choice, Fail Closed on Unavailability
SN-794 · SYSTEM-INTELLIGENCE / SYSTEM-DESIGN
**Created:** 2026-10-13T08:44:13Z

## IN A NUTSHELL

A procedure that names a file by path is writing a prayer, not a reference — files move, branches diverge, PRs merge or don't. Naya 4's activation protocol told every fresh Naya to load a design-doctrine file at a path that doesn't exist on main; following it literally, a new Naya stops dead at step one. The fix is a three-part pattern: (1) resolve references in ordered preference — canonical path if live, then the verified ratified alternative; (2) record which reference was actually used and its SHA in the receipt, so the next reader knows what the activation was measured against; (3) if nothing resolves, fail closed with a NAMED failure (`DOCTRINE_UNAVAILABLE`) — never proceed on assumed doctrine, never hang silently. The receipt's "which reference + its SHA" turns a hidden assumption into auditable state.

## HUMAN

On 2026-10-09, Naya 3's independent review found that the V2 activation protocol's first step pointed at a file that isn't on main — every new Naya following the instructions would hit a dead end on step one. Naya 4 fixed it the right way: don't hard-code one path; try the preferred path, fall back to the ratified contract that actually exists, write down which one you used, and if neither exists, stop loudly with a named error instead of guessing. The receipt naming the used reference is the part most people forget — without it, nobody can tell later whether the activation was measured against the real doctrine or an assumption.

## CHILD

Imagine instructions that say "open the blue door" — but there is no blue door. You'd be stuck. The smart fix: the instructions now say "try the blue door; if it's not there, use the green door; write down which door you used; and if there are no doors at all, stop and say so loudly." Never pretend a door exists when it doesn't.

## GRANDMA

Don't give directions to a landmark that isn't there. If the church on the corner was torn down, you say "turn where the church used to be" or you pick a landmark that IS there — and if nothing's there, you say so plainly instead of guessing and getting someone lost.

## NAYA

Operationally, for any procedure I write that references artifacts by path: (1) resolve in ordered preference — primary canonical path if live, then verified ratified alternatives, each verified against live bytes before use; (2) record the used reference + its SHA in the receipt — the activation/proof is measured against THAT, and the record must say so; (3) no resolution → named fail-closed code (`DOCTRINE_UNAVAILABLE`), never proceed on assumption, never hang silently. A literal follower of the procedure must never be stranded — the procedure degrades by design, not by accident. This is the reference-resolution sibling of fail-closed gates (SN-0438, SN-0413): the gate applies at the moment of REFERENCE, not just at the moment of VERDICT.

## MACHINE

```json
{
  "sn": "SN-0794",
  "law": "RESOLVE_BY_AVAILABILITY",
  "pattern": {
    "ordered_resolution": ["canonical path if live", "verified ratified alternative(s)"],
    "receipt": "record which reference was used + its SHA",
    "on_no_resolution": "fail closed with named code (e.g. DOCTRINE_UNAVAILABLE); never proceed on assumed doctrine; never hang silently"
  },
  "anti_pattern": "hard-coding one path that may 404 (strands a literal follower at step one)",
  "pipeline_state": "CANDIDATE"
}
```

## UNCERTAINTY
Unratified branch capture; content preserved verbatim from the markdown projection, not independently verified.

## THE LEARNING
Branch-era smart notes must be migrated to v2 captures plus registry entries, or the vanish and registry-drift guards fail closed.

---
*Imported from PR #2981 (branch naya4/smart-notes-2026-09-30) on 2026-11-04 — recovered lost capture IB-SMART-NOTE-20261013-sn0794-migrated.*
