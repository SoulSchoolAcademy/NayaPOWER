# The Registry Scans Every Branch That Carries Live Claims

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0171-registry-scans-all-claim-branches
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-02
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #554 comment 5946158668 (Naya 2 relay, 2026-10-02T05:30:15Z — her lane's SN-031→SN-131 replacement number verified free across six sources: main tree (max SN-021), #1229 head tree (25/28/29/31–52/54–60/140–169), `naya4/hub-rooms-v1` tree (SN-0134–0139/0143–0144/0148–0158/0162/0166 — "non-SN-PR branches hold claims too, new check added"), `naya4/nine-node-kernel-v1` tree (SN-002–016), all open Smart-Note PR numbers, commit-graph search for sn131/sn-131 (0 hits); commit 56f46ae0 on `brain-build/smart-note-sn018-ci-triage`, old SN-031 paths gone, content byte-identical except the number, PR #1233 retitled to SN-131). Extends SN-115 (three-layer registry: board / open Smart-Note PR heads / commit-graph search) and SN-169 (4th registry-scan-defect recurrence: layer 2 missed).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Smart Note numbers can be claimed from branches that were never Smart-Note PRs — so the registry's layer 2 must scan them too. Resolving the SN-031 double-claim (SN-169), Naya 2 renumbered her lane's note SN-031→SN-131 and verified the replacement number free across **six** sources: main tree, #1229 head tree, all open Smart-Note PR numbers, commit-graph search — and two trees nobody had scanned before as claim registries: the `naya4/hub-rooms-v1` branch tree (which carries live claims SN-0134–0139/0143–0144/0148–0158/0162/0166 — "non-SN-PR branches hold claims too, new check added") and the `naya4/nine-node-kernel-v1` branch tree (SN-002–016). The old SN-031 paths were confirmed gone and the new SN-131 dir + file tree-verified at the new head, content byte-identical except the number, PR #1233 retitled. The durable rule: layer 2 of the registry is not "open Smart-Note PR heads" — it is **every branch tree that carries live claims**, including hub-lane and kernel-lane branches. Any lane that holds live claims on a branch adds that branch to the registry's scan list; claims retire from the scan list only when the branch is merged, closed, or its claims are renumbered. The renumber commit itself (56f46ae0) proves the six-source scan works — this is the first replacement number verified against the widened registry, and the collision family closes with it.

## 🩷 HUMAN NOTE

Shawn — closing a loop properly this time. When Naya 2's lane had to renumber her note (SN-031 was mine first), she didn't just check the usual places — she checked six sources, including two branch trees that nobody had treated as claim-registries before: the Hub rooms branch and the kernel branch, which both quietly hold live Smart Note numbers. Everything came back clean, the old paths are gone, the new number is in, byte-identical content. The lesson she added to the registry is the kind that compounds: from now on, *every* branch that carries live claims gets scanned — not just the obvious Smart-Note PRs. The SN-031 double-claim family ends here: the replacement was chosen against the full widened registry, and the board record shows the whole six-source scan.

## 🟣 CHILD NOTE

Imagine there are lots of bulletin boards in the school — the classroom board, the hallway board, the gym board. Before, the rule was: when you want a new name, check the classroom board, the hallway board, and ask the teacher. But then someone realized: the art room has been quietly putting name tags up too, and the science lab has some on its wall — boards nobody checked before. So now the rule is better: check EVERY board in the whole school that has name tags on it, not just the famous ones. The first time anyone used the new rule, they checked six boards and found a clean name. Now the rulebook says: if your room puts up name tags, your board gets added to the checklist. No more hidden boards.

## 🔵 GRANDMA NOTE

It's like the town rule that before you take a new parking spot, you check the street signs, the lot map, and ask at the office. Then someone discovers the church lot and the library lot also have assigned spots — places the checklist never mentioned. So the rule gets fixed: you check every lot that has assigned spots, not just the well-known ones. The first person to follow the fixed rule checked six lots and found a free spot cleanly. And the rulebook adds: any lot that starts assigning spots gets itself added to the checklist. The registry only works if the map of places to check grows with the town.

## 🟠 NAYA NOTE

Apply this whenever you claim or replace an SN number: (1) registry layer 2 is "every branch tree that carries live claims" — currently main tree, `naya4/smart-notes-2026-09-30` (PR #1229 head), `brain-build/smart-note-sn018-ci-triage` (PR #1233 head), `naya4/hub-rooms-v1` (hub-lane live claims SN-0134–0139/0143–0144/0148–0158/0162/0166), `naya4/nine-node-kernel-v1` (SN-002–016) — not merely "open Smart-Note PR heads"; (2) when your lane's branch starts carrying live claims, add that branch to the scan list yourself and announce it on the board; claims retire from the scan list only when the branch is merged/closed or the claims are renumbered; (3) a replacement number is verified by tree scan, not by reading the branch name — confirm old paths are gone and new paths exist at the new head (git/trees recursive), and record which sources returned what, so a miss is reviewable; (4) content-preservation check on renumber: byte-identical except the number, old paths removed; (5) record each widening of the registry as a note (this is SN-115's registry growing) so the next lane inherits the map, not just the instinct.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": null,
  "evidence": {
    "resolution": "#554 5946158668 (2026-10-02T05:30:15Z) — Naya 2 renumbered her lane's note SN-031→SN-131 on PR #1233: commit 56f46ae0 on `brain-build/smart-note-sn018-ci-triage`; tree-verified at the new head (old SN-031 paths gone, new SN-131 dir + file present, content byte-identical except the number); PR retitled to SN-131.",
    "six_source_scan": "replacement verified free across: (1) main tree (max SN-021), (2) #1229 head tree (her lane holds 25/28/29/31–52/54–60/140–169), (3) `naya4/hub-rooms-v1` tree (SN-0134–0139/0143–0144/0148–0158/0162/0166), (4) `naya4/nine-node-kernel-v1` tree (SN-002–016), (5) all open Smart-Note PR numbers, (6) commit-graph search for sn131/sn-131 (0 hits).",
    "widening": "'non-SN-PR branches hold claims too, new check added' — sources (3) and (4) are non-Smart-Note PR branches carrying live claims.",
    "prior_defect": "SN-115 three-layer registry (board / open Smart-Note PR heads / commit-graph); SN-169 4th recurrence — her lane's SN-021→SN-031 renumber missed layer 2, colliding with this lane's SN-031 (kept per SN-033 first-claim-stands)."
  },
  "rule": [
    "registry layer 2 = every branch tree that carries live claims, not merely 'open Smart-Note PR heads'",
    "a lane that starts holding live claims on a branch adds that branch to the scan list and announces it on the board",
    "verify replacement numbers by recursive tree scan at the new head (old paths gone, new paths present); content byte-identical except the number",
    "record each registry widening as a note so the map, not just the instinct, is inherited"
  ],
  "lesson_line": "The registry scans every branch that carries live claims — including non-Smart-Note PR branches — because claim registries only work when the map of checked places grows with the lanes.",
  "extends": "SN-115 (three-layer collision registry), SN-169 (4th scan-defect recurrence, SN-031 double-claim)"
}
~~~
