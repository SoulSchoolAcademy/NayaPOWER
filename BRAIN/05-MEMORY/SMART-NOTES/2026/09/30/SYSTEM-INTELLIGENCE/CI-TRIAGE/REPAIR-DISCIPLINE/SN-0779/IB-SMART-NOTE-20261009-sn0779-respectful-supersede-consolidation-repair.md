# A Respectful Supersede Consolidates the Repair Without Duplicating the Class

**Intelligent Block:** IB-SMART-NOTE-20261009-sn0779-respectful-supersede-consolidation-repair
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-09
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6080991626 (SCORECARD RECEIPT — merge decision for PR #1961, 2026-10-09T12:34:46Z, SoulSchoolAcademy); PR #1961 body byte-verification evidence; superseded PR #1838 registry-heal portion

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The brain-build battery found a registry-drift RED on the exact main tip `de6e247b`: `test_live_repository_drift_never_grows_per_class` showed `published_pages_without_registry_entry` 1 → 8. The same-class repair, Naya 4's PR #1838, was open but conflicted — its registry-heal portion stale against the moved tip. The two naive options both fail: open a second repair (violates SN-0236, one RED class, one declared owner) or stand down for a claim that can no longer merge (violates SN-0716's lesson that a stale claim blocking a live RED is an invisible blocker).

The lane took the third path: a **consolidation repair**, PR #1961. Registry-heal content from #1838 was re-anchored onto the current tip `de6e247b` and **verified byte-equivalent** before use. The Scorecard Law receipt was posted on #1354 *before* the merge (9.1, all gates passing: one-commit revert; additive-only — 8 index entries appended, 8 capture files added, the existing 620 entries byte-untouched by diff of entry sets; positive forward effect — main goes 10 → 9 failures on the tip battery, 8 Smart Notes become hash-retrievable). Claim scan: CLEAR. And critically, a **respectful note was posted on #1838 itself**, naming exactly what was superseded (the registry-heal portion) and explicitly leaving Naya 4's workflow edit and other contents untouched — their property to salvage.

Why this is brain-grade: SN-0236 (one repair per class) and SN-0716 (verify currency before standing down) together cover "don't duplicate" and "don't blindly defer" — but neither tells you what to do when the claim is live-stale and the RED is real. The respectful supersede closes that gap. It is not a takeover of authorship; it is a merge of evidence. The superseding lane must prove its replacement equals the claimed content (byte-equivalence, re-anchored to the current tip) and must say so on the superseded PR's own page, in writing, before the merge. That written note is what keeps consolidation from becoming clobber: the original owner sees exactly what moved and what stayed theirs.

Rule for a cold successor: **when the same-class claim is conflicted, unmergeable, or stale and the RED is live, you may supersede — but only the portion you can prove equivalent, and only in the open.** (1) Verify your replacement content is byte-equivalent to the claim and re-anchored to the current tip; (2) post a respectful note on the superseded PR naming what you took and what stays theirs; (3) confirm the claim scan is CLEAR of any other live claim; (4) post the Scorecard Law receipt before the merge. Anything less is duplication or theft wearing a merge message.

## 🩷 HUMAN NOTE

Shawn — a lane-coordination lesson from this morning's build loop. The loop found 8 Smart Notes missing from the brain's registry (a real red on the live tip). Naya 4's PR #1838 already claimed that fix, but it had gone stale — conflicted, couldn't merge. So the loop didn't build a duplicate repair, and it didn't just stand down waiting on a fix that would never land. It rebuilt the same fix onto the current tip, proved it was byte-for-byte equivalent to hers, and — this is the part that matters — posted a note on her PR saying exactly which part was being taken over and that everything else in her PR stays hers. The standing rule: you can supersede a stalled repair, but only if you can prove your version equals theirs, and only if you say so publicly on their PR before you merge. Transparency is what separates a consolidation from a takeover.

## 🟣 CHILD NOTE

Imagine your friend is fixing a broken toy but her tools don't fit anymore, and the toy is still broken. You could grab the toy and "fix it your way" — but that's not fair, and you might break what she already did. The fair move: figure out exactly which part she was fixing, fix that same part with tools that work, then go back to her and say "I redid your wheel part because your tools didn't fit — the rest of the toy is still yours to finish." You prove your part matches hers, you say it out loud on her drawing board, and only then do you put the wheel on. That's a respectful supersede.

## 👵 GRANDMA NOTE

Two workers were responsible for the same repair. The first worker's fix had gone stale — it no longer fit the current machine. The second worker didn't build a competing fix (that wastes effort) and didn't just wait (the machine stayed broken). She rebuilt the identical fix for the current machine, verified it matched the first worker's work piece for piece, and left a written note on the first worker's job card: "I carried forward your register entries; the rest of your card is still yours to finish." The lesson: when someone else's stalled work is blocking a real problem, you may carry their piece forward — but you must prove it's the same piece, and you must tell them in writing, on their own record, before you act.

## 🟣 NAYA NOTE

The no-duplicate law and the currency law are both boundary laws — they say what I must NOT do. This note is the action law for the gap between them. When the claim scan finds a same-class claim that is conflicted/unmergeable/stale and the RED reproduces live, I run the supersede checklist: (1) re-anchor the claimed portion onto the exact current tip and verify byte-equivalence; (2) confirm no other lane holds a live claim (claim scan CLEAR); (3) write the five-step scorecard receipt on the board; (4) post the respectful note on the superseded PR before the merge, naming taken vs. remaining. I never supersede silently, never supersede more than I proved equivalent, and never touch the original PR's other contents. Consolidation is a public act with receipts — the moment it goes private, it's clobber.

## ⚙️ MACHINE NOTE

{
  "schema": "smart-note-v1",
  "sn": "SN-0779",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-09",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE/CI-TRIAGE/REPAIR-DISCIPLINE",
  "doctrine": "respectful-supersede-consolidation-repair",
  "rule": "A live RED with a conflicted/unmergeable/stale same-class claim may be superseded by a consolidation repair only if: (1) the superseded portion is verified byte-equivalent and re-anchored to the current tip; (2) the claim scan is CLEAR of other live claims; (3) the Scorecard Law receipt is posted before the merge; (4) a respectful note is posted on the superseded PR naming what was taken and what remains the owner's. Never supersede silently, never beyond proven equivalence.",
  "failure_mode": "silent or over-broad supersede = clobber of another lane's work; standing down for a stale claim = invisible blocker on a live RED; opening a second repair = class duplication",
  "receipt": [
    "#1354 comment 6080991626 (scorecard receipt for PR #1961, 2026-10-09T12:34:46Z)",
    "PR #1961: registry-heal of SN-0632..SN-0639 re-anchored onto tip de6e247b, blob sha 59fa5c89…, remote-bytes == local sha256 51451d9f2bbaced4, 12/12 drift module green on worktree of pushed head 827b345e",
    "gates: one-commit revert; additive-only (620 existing entries byte-untouched per entry-set diff); tip battery 10 → 9 failures",
    "respectful note posted on #1838 naming the superseded registry portion; #1838 workflow edit + other contents untouched"
  ],
  "see_also": ["SN-0236", "SN-0508", "SN-0716", "SN-0753", "SN-0340"]
}
