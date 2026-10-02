# A Compelled Renumber Still Clears the Three-Layer Registry

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0169-compelled-renumber-clears-registry
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-02
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #554 comment 5945926396 (Naya 2 build-loop battery, 2026-10-02T05:04:41Z, SN-021→SN-031 renumber, commit cde9ead2); PR #1233 head cde9ead2 carrying IB-SMART-NOTE-20261001-sn031-ci-exit-2-triage.md; this lane's SN-031 (IB-SMART-NOTE-20260930-sn031-classify-before-code.md, staged 2026-10-01 ~06:15Z, commit c1fafcf0) live on PR #1229 head tree 372b64697a; SN-115 (three-layer registry); SN-033 (first-claim-stands).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Displacement by a director lock does not discharge the registry obligation. The lock-compelled SN-021→SN-031 renumber (Naya 2's PR #1233, commit cde9ead2, 2026-10-02 ~05:04Z) chose SN-031 as the replacement after being "verified free on main tree, commit graph, open PRs, #554 comments." But this lane's SN-031 — classify-before-code + scope-403-as-gate, staged 2026-10-01 ~06:15Z (commit c1fafcf0) — is live on the head tree of open draft PR #1229 (`naya4/smart-notes-2026-09-30`, head 372b64697a). The scan missed registry layer 2 (open Smart-Note PR heads/trees) — the registry-scan defect's 4th recurrence (SN-115 established the three layers: (1) #554 board, (2) open Smart-Note PR heads, (3) commit-graph search for SN-NNN; recurrences at the 17:15, 18:45, and 23:15 UTC ticks, then now). Per SN-033 first-claim-stands, this lane keeps SN-031; the colliding renumber is her lane's to renumber — flagged on #554, never unilaterally renumbered by another seat (SN-115: the winner does not dictate renumbering). The rule: the replacement number in a compelled renumber clears the same three-layer registry as a fresh claim. Urgency from a director lock does not shrink the registry — it is exactly when the registry matters most, because the displaced lane is choosing under time pressure and will reach for the nearest free-looking number.

## 🩷 HUMAN NOTE

Shawn — one correction to an otherwise correct resolution. Naya 2's lane did exactly the right thing when your SN-021 lock displaced her claim: she moved her own work to SN-031 and verified it carefully. But SN-031 was already taken — by an earlier note of mine, staged and live on the draft PR's branch tree. Her "verified free" check scanned the board, the main tree, and the commit graph, but missed the open draft-PR branches where the earlier claim lives. So the collision simply moved from one number to another. The lesson is almost comically human: the moment you're in a hurry (a lock forced your hand), you check less carefully — and that's exactly when the registry needs to be complete. The collision is flagged on the board for her lane to renumber; nothing was touched on her side by me. Nobody's work is blocked.

## 🟣 CHILD NOTE

Imagine the teacher takes back the name "Sailor" for her own boat, and one kid quickly renames his boat "Comet" — but he only checked the classroom wall, not the playground bulletin board where another kid had already claimed "Comet" an hour earlier. He checked three places but missed the fourth. Now two kids both think they own "Comet." The first kid keeps it (first-claim-stands), and the second kid needs to pick a new name — and this time, check ALL four boards. The lesson: when you have to rename in a hurry, that's when you need the FULL checklist, not a shorter one. Hurrying is exactly when mistakes sneak in.

## 🔵 GRANDMA NOTE

It's like being bumped from your parking spot by the mayor's reserved sign, so you pull into the nearest open spot — except someone had already parked there, behind a pillar where you couldn't see from the entrance. You checked the street, the lot map, and asked around, but you didn't walk the back row. Now two cars are assigned one spot, and the first one there keeps it. The lesson: the rulebook for finding a free spot has four checks, and the fourth exists precisely for hurried days — because the fastest decisions are the ones that skip steps. The displaced driver picks a new spot and this time walks the back row too.

## 🟠 NAYA NOTE

Apply this whenever you renumber under displacement (lock, collision, supersession): (1) the replacement number clears the FULL three-layer registry — (1) #554 board, (2) open Smart-Note PR heads/trees (including #1229's branch, which the last three recurrences missed), (3) commit-graph search for SN-NNN — no layer may be skipped because the move is urgent; (2) treat "verified free" as a claim with its own evidence burden — name which layers you checked and what each returned, so a miss is reviewable rather than invisible; (3) when a new collision is found, flag it on the board with both claims' timestamps and SHAs, cite SN-033, and never renumber the other seat's artifact — the colliding lane owns its renumber; (4) record the miss as a registry instance (this is the 4th recurrence of the scan defect) so the pattern, not just the instance, is what the next lane inherits.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "lock-compelled renumber chose a replacement number without clearing the full registry (new SN-031 double-claim; 4th registry-scan-defect recurrence)",
  "evidence": {
    "board": "#554 5945926396 (2026-10-02T05:04:41Z) — Naya 2 renumbered her lane's PR #1233 claim SN-021→SN-031 ('verified free on main tree, commit graph, open PRs, #554 comments'), commit cde9ead2; PR #1233 head now carries IB-SMART-NOTE-20261001-sn031-ci-exit-2-triage.md.",
    "first_claim": "this lane's SN-031 (IB-SMART-NOTE-20260930-sn031-classify-before-code.md, classify-before-code + scope-403-as-gate) staged 2026-10-01 ~06:15Z, commit c1fafcf0 on naya4/smart-notes-2026-09-30; live on open draft PR #1229 head tree 372b64697a (verified live this tick via git/trees recursive).",
    "registry": "SN-115 three-layer registry: (1) #554 board, (2) open Smart-Note PR heads/trees, (3) commit-graph search for SN-NNN. Layer 2 missed — 4th recurrence (17:15 / 18:45 / 23:15 UTC ticks, then this).",
    "disposition": "SN-033 first-claim-stands: this lane keeps SN-031; flagged on #554; renumber belongs to her lane (SN-115: winner does not dictate renumbering, never unilaterally renumber another seat's artifact)."
  },
  "rule": [
    "a compelled renumber clears the same three-layer registry as a fresh claim — displacement urgency never shrinks the registry",
    "'verified free' is an evidence-bearing claim: name the layers checked and what each returned",
    "flag new collisions on the board with both timestamps and SHAs; the colliding lane owns its renumber"
  ],
  "lesson_line": "Displacement never discharges the registry: the replacement number in a compelled renumber must clear all three registry layers, because hurried choosing is exactly when the full check matters most."
}
~~~
