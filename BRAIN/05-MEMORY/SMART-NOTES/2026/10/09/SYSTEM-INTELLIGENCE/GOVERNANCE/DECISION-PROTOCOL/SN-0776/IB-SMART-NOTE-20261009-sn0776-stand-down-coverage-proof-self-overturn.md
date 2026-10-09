# Assumed Coverage Is Not Proven Coverage — Verify the Wave's Registered Scope, Then Own the Overturn

**Intelligent Block:** IB-SMART-NOTE-20261009-sn0776-stand-down-coverage-proof-self-overturn
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-09
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6080067135 ([NAYA 2 — BRAIN-BUILD LOOP] Repair PR #1959 — registry heal for SN-0742/0743/0744 (SCORECARD RECEIPT), 2026-10-09T11:36:04Z, SoulSchoolAcademy); commit 8ae49c54 (published SN-0742/0743/0744 without capture/index step); #1838 head `65d167d2`; PRs #1844, #1854, #1959

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A lane's 04:19Z disposition stood down on registry-heal instances SN-0742/0743/0744, assuming the "#1838/#1844/#1854 registry wave" covered them. That was an unverified assumption, not a finding. When the lane re-opened the case, it ran the coverage proof on exact bytes instead of trusting the assumption:

- **#1838's head `65d167d2` index.json registers ONLY SN-0632..0639** — 8 ids in the patch, no more.
- **#1844's and #1854's patches contain ZERO mentions of SN-0742/0743/0744.**

The wave does not cover these instances. The stand-down premise was falsified, and the lane overturned its own disposition publicly: "the stand-down premise was an unverified assumption, and the assumption is now falsified. Correction is mine to make in my own lane." The repair (PR #1959) was verified scope-disjoint from #1838 (zero overlapping paths) before it was built, and all 11 pre-existing failures+error on its head were classified to classes owned by other open repairs.

Why this is brain-grade: stand-downs are issued *against claims*, and SN-0716 already teaches that a colliding open claim must prove currency before it earns the stand-down. This note closes the other half: **coverage itself must be proven.** "The wave covers it" is a claim about registered scope, and it is checked the same way — read the registry (which ids are actually registered), grep the patches (are the instances mentioned). An assumed scope is exactly as dangerous as a stale claim: it converts the no-duplicate rule into silent neglect of a live defect. The second half is the protocol: **when the proof falsifies your own disposition, overturn it publicly, in your own lane, with the evidence that killed it.** No lane change, no blame — just the byte-level receipt of the overturn.

Rule for a cold successor: **before you stand down because "a wave/another lane covers it," prove coverage mechanically** — (1) list the registered scope of the covering repair (index.json ids, patch file lists); (2) grep the covering patches for your instances; (3) if the instances are absent, the coverage claim is false and the stand-down is void. Then repair your instances, scope-disjoint from the wave (zero overlapping paths), and post the overturn receipt naming the falsified premise.

## 🩷 HUMAN NOTE

Shawn — a lane-coordination lesson from this morning's brain-build loop. A lane had earlier stood down on three registry defects (SN-0742/0743/0744) believing the registry-heal wave covered them. When she re-checked, she didn't trust the belief — she read the wave's actual registered IDs and grepped its patches for the three notes. Zero mentions. The wave never covered them. So she publicly overturned her own earlier call, built the repair herself, and verified it touches none of the wave's files. The standing rule: "someone's covering it" is a claim about scope, and scope gets proven from the bytes — the registered ID list, the patch contents — not from the assumption. And when the proof kills your own earlier call, you overturn it openly in your own lane with the evidence that killed it.

## 🟣 CHILD NOTE

Imagine a repair crew says "we'll fix all the broken fences." Your fence is broken too, so you walk away. But later you check their work list — your fence isn't on it. They never said they'd fix yours; you just assumed. The smart move: check the list *before* you walk away, and if your fence isn't there, go back and fix it yourself — and tell everyone "I checked the list, my fence wasn't on it, so I'm fixing it." That's what happened here: the lane checked the wave's list, found her three items missing, and fixed them herself.

## 👵 GRANDMA NOTE

One worker stepped aside from fixing three defects, assuming another team's repair wave covered them. She later checked the wave's actual list of repaired items — her three weren't on it. So she reversed her own earlier decision publicly, fixed the three defects herself, and proved her fix didn't overlap the other team's work. The lesson: never assume someone else's repair covers your problem — read their actual list first. And if the check proves you were wrong, say so plainly and make the correction yourself.

## 🟣 NAYA NOTE

Stand-downs are issued against claims, and claims carry scope. When I stand down because a wave covers my instances, I prove coverage the same way I prove currency: I read the registered scope (index.json ids, patch file lists) and grep the covering patches for my instances. Assumed scope is a silent blocker for a live defect — the no-duplicate rule only binds when the class is actually claimed. And when the proof falsifies my own disposition, I overturn it myself, publicly, with the evidence that killed it: "the stand-down premise was an unverified assumption, and the assumption is now falsified." Scope-disjoint repair (zero overlapping paths), failures classified to their real owners, receipt posted.

## ⚙️ MACHINE NOTE

{
  "schema": "smart-note-v1",
  "sn": "SN-0776",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-09",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE/GOVERNANCE/DECISION-PROTOCOL",
  "doctrine": "stand-down-coverage-proof-self-overturn",
  "rule": "Before standing down on assumed coverage, prove coverage mechanically: list the covering repair's registered scope and grep its patches for your instances; absent instances void the stand-down. When the proof falsifies your own disposition, overturn it publicly in your own lane with the killing evidence.",
  "failure_mode": "assumed wave coverage converts the no-duplicate-repair rule into silent neglect of live defects",
  "receipt": [
    "#1838 head 65d167d2 index.json registers ONLY SN-0632..0639 (8 ids in patch)",
    "#1844 and #1854 patches contain ZERO mentions of SN-0742/0743/0744",
    "commit 8ae49c54 published SN-0742/0743/0744 (Shawn-directed vision notes) with no capture/index step -> 3 vanish + 3 drift instances on live tip 925e4c34",
    "PR #1959 repair scope-disjoint from #1838 (0632..0639, zero overlapping paths); 1473 passed, 10 failures + 1 error identical to tip baseline, all owned by other open repairs"
  ],
  "kin": ["SN-0236", "SN-0508", "SN-0716"],
  "related_agents": ["naya2"]
}
