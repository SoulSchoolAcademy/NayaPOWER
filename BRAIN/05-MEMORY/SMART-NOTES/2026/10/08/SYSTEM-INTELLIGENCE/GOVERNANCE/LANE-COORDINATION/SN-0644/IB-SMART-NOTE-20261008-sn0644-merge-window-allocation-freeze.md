# Merge-Window Allocation Freeze — Proactive Captures Route to Lane Branches, Never the Shared Staging Branch

**Intelligent Block:** IB-SMART-NOTE-20261008-sn0644-merge-window-allocation-freeze
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-08
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6050500807 (Naya 4 freeze request, 2026-10-08T01:48:27Z — SN-0522→0626→0627→0630 four-hop renumber chain; registry, capture, sequence_policy (631) updated at branch `naya4/smart-notes-2026-09-30` commit 5761a94c; "pause new SN-ID allocations (proactive captures) to the #1229 branch until it merges"), comment 6050593121 (Naya 2 relay acknowledgment, 2026-10-08T01:57:09Z — allocations run exclusively through the relay's own `brain-build/smart-note-sn<NNN>-<slug>` branches; "the lane stays clear of #1229 until your merge lands"). — SoulSchoolAcademy.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A new collision failure mode appeared on the shared Smart Notes staging branch: not a bad claim at push time (SN-0367's TOCTOU gap) but a **mid-renumber claim race**. Naya 4 renumbered the branch's voice note SN-0522 → SN-0626, and while the renumber was still in flight, proactive captures kept allocating the "next free ID" — forcing SN-0626 → SN-0627 → SN-0630, three renumbers in one night. The shared branch's ID space is a shared mutable resource with no lock, and scan-before-claim cannot see a renumber that hasn't landed yet. The repair was a **merge-window allocation freeze**: the owning lane posted a bounded request (scope: SN-ID allocations to the #1229 branch only; end: the merge lands), and the other lane acknowledged through the relay, routing its allocations to its own `brain-build/` branches. Two honest boundaries of the primitive: the freeze is an allocation moratorium, not a work stoppage — lanes keep capturing on their own branches (SN-0204's bounding discipline: a freeze without scope and end condition is a veto); and the freeze lifts on merge, at which point the registry + sequence_policy on the branch are the single source of the next free ID again. This is SN-0204's freeze primitive applied to a new domain — the registry ID space rather than branch scope — and the complement to SN-0367's pre-push re-scan, which guards claims but not allocations during a pending renumber.

## 🩷 HUMAN NOTE

Shawn — a process fix worth keeping: one shared Smart Note branch got renumbered three times in a night (SN-0522 → 0626 → 0627 → 0630) because new notes kept grabbing the "next free number" while the renumber was still landing. The fix is simple and it's already working: while a shared branch is in its final merge run, nobody allocates new numbers onto it — other lanes capture on their own branches instead, and say so out loud so everyone can see the freeze is honored. Bounded (numbers only, ends at merge), not a veto. That's the standing rule now.

## 👶 CHILD NOTE

Imagine a line of kids waiting to pick cubby numbers, and one kid is in the middle of switching cubbies. If the next kid grabs a number while the switch is happening, everything gets mixed up — and it happened three times in one night! The fix: while someone is switching, everybody else waits and picks their numbers from their own classroom instead. Once the switch is done, the line moves again. Waiting your turn only works if everyone can see the "wait" sign — so you say it out loud.

## 👵 GRANDMA NOTE

Dear, this is about taking turns with shared things. A shared notebook's page numbers belong to everyone, so when one person is renumbering pages, the others must not grab numbers mid-way — three renumbers in one night proved that. The polite fix is a proper "hold, please": you announce exactly what is on hold (just the numbers, not the work) and exactly when the hold ends (when the merge lands), and the others confirm they've heard. A hold with no end is just bossiness; a hold with a scope and an end is good manners. And you never rearrange someone else's pages — you ask, and they do it themselves.

## 🧠 NAYA NOTE

Cold successor: when you own a shared staging branch entering its final merge run and its ID space is being renumbered: (1) post the freeze request on the authoritative feed before the renumber lands — name the branch, the commit, the scope (SN-ID allocations to this branch only), and the end condition (merge lands); (2) update registry + capture + sequence_policy in the same commit as the renumber so the next free ID is unambiguous; (3) expect the race — proactive capture loops allocate against "next free" and cannot see your unlanded renumber, so the freeze is the mechanism, not the scan; (4) collect explicit acknowledgment (the relay pattern: owning lane requests, other lanes confirm and route to their own branches); (5) lift on merge and say so. If you are a non-owning lane: on seeing a freeze request, route all allocations to your own branch namespace immediately and acknowledge — staying clear of the shared branch until the merge receipt posts is the coordination half of the primitive. Never allocate into a branch someone else is renumbering; never renumber into a branch someone else owns.

## 🤖 MACHINE NOTE

```json
{
  "sn": "SN-0644",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-08",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE/GOVERNANCE/LANE-COORDINATION",
  "doctrine": "Merge-window allocation freeze: while a shared staging branch is renumbering toward merge, its owner posts a bounded freeze (scope: SN-ID allocations to that branch; end: merge lands); other lanes route allocations to their own branches and acknowledge. Guards the mid-renumber claim race that scan-before-claim cannot see.",
  "family": "LANE-COORDINATION (SN-0204 takeover-sign-in freeze primitive, SN-0367 collision-protocol re-scan, SN-0117 converge-by-scored-selection)",
  "evidence": [
    "#1354 comment 6050500807 (Naya 4: SN-0522→0626→0627→0630 renumber chain from mid-renumber allocations; registry+capture+sequence_policy(631) updated at 5761a94c; freeze requested on #1229 until merge)",
    "#1354 comment 6050593121 (Naya 2 relay: allocations exclusively via relay's own brain-build branches; lane stays clear of #1229 until merge lands)"
  ],
  "falsifiers": [
    "Allocating a new SN-ID onto a shared staging branch during its posted merge window",
    "Posting a freeze with no scope or no end condition (veto, not coordination — SN-0204)",
    "Treating a pre-push claim re-scan as sufficient protection during a pending renumber"
  ],
  "applies_to": "shared staging branches undergoing ID renumbering toward merge; proactive capture allocation loops; relay coordination"
}
```
