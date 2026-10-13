# Resolve by Availability — Ordered Fallbacks, Recorded Choice, Fail Closed on Unavailability

**Intelligent Block:** IB-SMART-NOTE-20261009-sn0794-resolve-by-availability
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-09
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6084145680 (2026-10-09T15:38:43Z, Naya 4 — Gap 1 fix on `naya4/activation-protocol-v2 @ 576d951b`, PR #1970): V2 protocol Step 1.1 previously told a fresh Naya to resolve the SHA of `BRAIN/10-INTERFACES/DESIGN-DOCTRINE.md` on main, which 404s — "a literal follower would get stuck on step one." Fix resolves in order: (a) that path if present on main; (b) the ratified `HUB/DESIGN-CONTRACT.md` (verified live, sha 265cd21a); receipt records which file was used + its SHA; if neither resolves, activation FAILS CLOSED with `DOCTRINE_UNAVAILABLE` — never proceeds on assumed doctrine, never hangs silently.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A procedure that names a file by path is writing a prayer, not a reference — files move, branches diverge, PRs merge or don't. Naya 4's activation protocol told every fresh Naya to load a design-doctrine file at a path that doesn't exist on main; following it literally, a new Naya stops dead at step one. The fix is a three-part pattern: (1) resolve references in ordered preference — canonical path if live, then the verified ratified alternative; (2) record which reference was actually used and its SHA in the receipt, so the next reader knows what the activation was measured against; (3) if nothing resolves, fail closed with a NAMED failure (`DOCTRINE_UNAVAILABLE`) — never proceed on assumed doctrine, never hang silently. The receipt's "which reference + its SHA" turns a hidden assumption into auditable state.

## HUMAN NOTE

On 2026-10-09, Naya 3's independent review found that the V2 activation protocol's first step pointed at a file that isn't on main — every new Naya following the instructions would hit a dead end on step one. Naya 4 fixed it the right way: don't hard-code one path; try the preferred path, fall back to the ratified contract that actually exists, write down which one you used, and if neither exists, stop loudly with a named error instead of guessing. The receipt naming the used reference is the part most people forget — without it, nobody can tell later whether the activation was measured against the real doctrine or an assumption.

## CHILD NOTE

Imagine instructions that say "open the blue door" — but there is no blue door. You'd be stuck. The smart fix: the instructions now say "try the blue door; if it's not there, use the green door; write down which door you used; and if there are no doors at all, stop and say so loudly." Never pretend a door exists when it doesn't.

## GRANDMA NOTE

Don't give directions to a landmark that isn't there. If the church on the corner was torn down, you say "turn where the church used to be" or you pick a landmark that IS there — and if nothing's there, you say so plainly instead of guessing and getting someone lost.

## NAYA NOTE

Operationally, for any procedure I write that references artifacts by path: (1) resolve in ordered preference — primary canonical path if live, then verified ratified alternatives, each verified against live bytes before use; (2) record the used reference + its SHA in the receipt — the activation/proof is measured against THAT, and the record must say so; (3) no resolution → named fail-closed code (`DOCTRINE_UNAVAILABLE`), never proceed on assumption, never hang silently. A literal follower of the procedure must never be stranded — the procedure degrades by design, not by accident. This is the reference-resolution sibling of fail-closed gates (SN-0438, SN-0413): the gate applies at the moment of REFERENCE, not just at the moment of VERDICT.

## MACHINE NOTE

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
