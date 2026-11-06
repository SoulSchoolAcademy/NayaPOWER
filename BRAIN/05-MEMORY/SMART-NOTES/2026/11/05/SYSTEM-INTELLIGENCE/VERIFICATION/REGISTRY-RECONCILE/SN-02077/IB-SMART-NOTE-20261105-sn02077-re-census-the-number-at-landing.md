# INTELLIGENT BLOCK — SN-2077

**Intelligent Block:** IB-SMART-NOTE-20261105-sn02077-re-census-the-number-at-landing
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-05
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Branch staged SN-2075 "Claim the Content, Not Just the Number" (e5bc01c0, ~15:08 PST 2026-11-05) after a live census that found the number free on main (registry 1,132 entries, max SN 2074, SN-2075 absent at tip 5fccb1d5). Main took SN-2075 anyway by direct write 2256d92f at 23:49:47Z ("SN-2075: Value Is the Work — What the GrokBot Lesson Changes in How Naya Behaves"). Live main tip dcf30450 (merge PR #3220, 00:03:33Z) carries main's SN-2075 at BRAIN/05-MEMORY/SMART-NOTES/2026/11/05/SYSTEM/value-economics/SN-2075; live tree census this tick at dcf30450 (8,461 entries): main max SN 2075, SN-2076/2077 free. Sixteenth branch-vs-main number collision (main-seat alert). The staging script's claim check reads only the branch tree; the intelligence-door landing path has no number check at all.

## ✦ IN A NUTSHELL

A number verified free at staging time can be taken on main before the staged note lands — the branch staged SN-2075 at 15:08 after a clean live census, and main took SN-2075 by direct write 41 minutes later. A staging-time census measures main at staging time, and main moves under it: the intelligence door lets any seat write to main at any moment, the staging script's claim check reads only the branch tree, and the landing path checks no number at all. The durable rule: **re-census the number at landing** — a staged number is only a claim until the landing moment, so the number+title census must be re-run against the live main tip immediately before landing, and a taken number means renumber first. A staging-time clean verdict expires the moment main moves.

## 🩷 HUMAN NOTE

Shawn — the branch filed a note as SN-2075 at 3:08 this afternoon after checking the number was free, and 41 minutes later main took SN-2075 for a completely different note. Both checks were honest; the check just went stale. The number was free when we looked and taken by the time we landed, because notes can go straight onto main at any moment and nothing re-checks the number at landing. From here on, the landing step re-checks the number against live main right before it lands — if it's taken, we renumber first. A check from an hour ago is not a check.

## 🟣 CHILD NOTE

Imagine you pick seat number 75 in a classroom because you looked and it was empty — but while you walk over, another kid sits in it. You weren't wrong to look; you just looked too early. The fix isn't to look harder, it's to look again right when you sit down. Numbers on the wall are like that: free when you check, maybe taken when you land. So always check one more time, right at the landing, and if your seat is taken, pick the next free one.

## 🔵 GRANDMA NOTE

Dear, it's like reserving a library book by writing its number on a slip, then finding someone else checked the book out before you reached the desk. You did nothing wrong — you checked the shelf and it was there. The shelf just changed while you walked over. The fix is simple: check the shelf again at the desk, right before you take the book. If it's gone, take the next number. A check from an hour ago is a memory, not a guarantee.

## 🟠 NAYA NOTE

For every seat, the dock, and anyone landing a staged note: a staging-time census is a snapshot, not a reservation. Before any staged note lands, re-run the number+title census against the live main tip (registry max SN + title search) and record the landing-time census line (tip SHA + max SN + verdict) in the landing receipt — a landing without it is incomplete and must not proceed. If the staged number is taken on main, renumber and re-stage first; first claim stands, no exceptions. Do not rely on the staging script's claim check: it reads only the branch tree and cannot see main. The window between staging and landing is unguarded by every check we have, and it is exactly where collisions 1 through 16 were born.

## 🟢 MACHINE NOTE

```json
{
  "slug": "re-census-the-number-at-landing",
  "sn": "SN-2077",
  "title": "A Staging-Time Census Decays — Re-Census the Number at Landing",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-11-05",
  "intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "kind": "lesson",
  "applies_when": ["distillation", "numbering", "collision", "landing", "registry"],
  "enforcement": "Before landing any staged note, re-run the number+title census against the live main tip (registry max SN + title search); if the staged number is taken on main, renumber and re-stage before landing. The landing receipt must carry a landing-time census line (tip SHA + max SN + verdict); a landing without it is incomplete and must not proceed. The staging script's branch-only claim check does not satisfy this.",
  "falsifier": "A sustained run of landings that skip the landing-time census yet produce zero number collisions while direct writes to main continue would show the decay window is negligible in practice. A landing-time census that never finds a taken number across many landings would bound the lesson the same way. Either would show the staging-time census is sufficient after all.",
  "decision_changed": "Whether a staged note lands as numbered: the lander now re-runs the number+title census against the live main tip immediately before landing instead of trusting the staging-time verdict — a staged number taken in the interim is renumbered first, so the sixteenth branch-vs-main collision class cannot repeat through a stale census.",
  "mechanism": "The intelligence door lets any seat direct-write to main at any moment, so main's number space moves asynchronously under the branch. A staging-time census measures main at staging time only; the staging script's claim check reads only the branch tree; the landing path checks no number at all. The window between staging and landing is therefore unguarded, and any number verified in it can be taken before the landing commits — the branch claim is only a claim until the landing moment.",
  "provenance": "Branch staged SN-2075 'Claim the Content, Not Just the Number' (e5bc01c0, ~15:08 PST 2026-11-05) after a live census found the number free on main (registry 1,132 entries, max SN 2074, SN-2075 absent at tip 5fccb1d5). Main took SN-2075 by direct write 2256d92f at 23:49:47Z ('SN-2075: Value Is the Work — What the GrokBot Lesson Changes in How Naya Behaves'). Live main tip dcf30450 (merge PR #3220, 00:03:33Z) carries main's SN-2075 at BRAIN/05-MEMORY/SMART-NOTES/2026/11/05/SYSTEM/value-economics/SN-2075; live tree census this tick at dcf30450 (8,461 entries): main max SN 2075, SN-2076/2077 free. Sixteenth branch-vs-main number collision (main-seat alert). Cousins: SN-2075 (branch) 'Claim the Content, Not Just the Number' — the staging-time title census; this note is the landing-time leg, the same collision seen from the other end of the window. SN-2066 (a free verdict reads the registry and pages — single-number freedom) — this note adds the expiry of that verdict."
}
```
