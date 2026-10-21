# Intelligent Block
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-03 ~01:15 PDT (Smart Note distillation tick)
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**SN number:** SN-0219
**Category:** ENGINEERING-PROOF
**Subcategory:** INDEPENDENT-VERIFICATION

## IN A NUTSHELL
What's built is not what's shipped. When the director reports a gap on the live system, walk the LIVE deployment — not the repo, not the branch, not the PR. Naya 4's rich Hub rooms existed on her branch for weeks while the live site still served old "Quiet here — honestly" placeholders: the beautiful versions never shipped. And the "tabs go nowhere" feeling turned out to be a collapsible drawer that needs opening at desktop viewport — a UX affordance invisible in dev, never a dead route. The chain has four links, verify at the right one: branch-green ≠ merged-true (SN-061), merged ≠ deployed, built ≠ shipped.

## HUMAN NOTE
Shawn's report (~01:10 PDT, 2026-10-03): the deployed Hub felt degraded — rooms that should be rich were placeholders, tabs unreliable. Naya 4 walked the actual live site at app.nayanet.technology/hub (board comment 5967016268), verified in Chromium:

1. All 11 sidebar tabs navigate — nothing dead at desktop viewport. The room nav is a collapsible drawer; tabs "go nowhere" only if you never open the drawer. That explains SN-218's unreproducible "dead tabs" — the symptom was a UX affordance in the user's viewport, never a broken route, and it could not be reproduced in a dev viewport where the drawer state differed. Lesson inside the lesson: when you can't reproduce the user's complaint, reproduce the user's environment first.
2. 7 rooms are rich (Feed, Today, Reports, Connect, Ledger, Lists, Settings). **4 are old placeholders** — Mail, Spaces, Connections, Library, all her lane's rooms. The beautiful versions never shipped. The gap Shawn felt was real and exactly located: live hash-route renderers serving stale placeholders while path-route static files existed on-branch, ready to drop in.
3. CDP click-test of every button/overlay in all four rooms: all working, zero JS errors. The rooms were never the problem. Deployment was.

She staged 4 drop-in static pages (mail/spaces/connections/library.html, self-contained, back-to-hub button, DEMO-labeled where simulated) and asked the deploy-seam question instead of guessing: path routes replacing the hash-route placeholders, or swapping the shell's `NayaRooms.*` renderers? She did not touch the shell — the deploy path is another lane's jurisdiction (SN-019 shell-barrier discipline, SN-104 propose-first). The open question sits on the board (5967016268) where the lane that owns the deploy owns the answer.

## CHILD NOTE
Imagine you bake a beautiful cake and put it on the kitchen counter, then wonder why the party guests say there's no cake — because the cake never made it to the party table. The party table is the only place the guests can see. Always check the party table (the live site), not the kitchen counter (your branch). And if a guest says "the door won't open," check whether the door is actually a drawer first — in THEIR hallway, not yours.

## GRANDMA NOTE
A director's complaint about the live system is a report about the live system — verify it at the live system. Beautiful code on a branch changes nothing for the person looking at the site. When you can't reproduce what the user feels, reproduce their environment: the symptom may be an affordance you never saw, not a bug. And when the fix is deploying through someone else's path, ask which path — don't choose for them.

## NAYA NOTE
For me, months from now: the verification chain is branch → merged → deployed → live-rendered, and each link fails silently in its own way. Branch-green ≠ merged-true (SN-061), merged ≠ deployed, built ≠ shipped. When Shawn reports a live-site gap, the FIRST move is a live walkthrough of the deployed URL at his viewport (collapsible drawers, sidebar states, responsive breakpoints), never a repo re-read. SN-218's held "dead tabs" question is resolved by this note: it was the drawer. The deploy-seam question pattern — "do my pages ship as path routes or as renderer swaps?" — is the standing ask-first-on-another-lane's-path discipline (SN-019, SN-104); keep asking it, never infer it. Related: SN-216 (verify at the target tree), SN-061 (post-merge verification at the pin), SN-059 (attribute the failure before blaming the change), SN-083 (retain the UNKNOWN with the missing evidence named).

## MACHINE NOTE
```json
{
  "sn": "SN-0219",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "ENGINEERING-PROOF",
  "subcategory": "INDEPENDENT-VERIFICATION",
  "captured": "2026-10-03",
  "evidence": ["#554 comment 5967016268 (Naya 4 deployed Hub findings + 4 rich rooms ready for deploy, 2026-10-03 ~01:10 PDT)", "#554 comment 5966761970 (Naya 2 relay receipt, live-verified state)"],
  "family": ["SN-061 post-merge verification at the pin", "SN-216 verify at the target tree", "SN-218 mount contract (resolves its held dead-tabs question)", "SN-019 shell-barrier", "SN-104 propose-first", "SN-059 attribute the failure", "SN-083 retain the UNKNOWN"],
  "lesson": "Verify a live-site complaint at the live site: branch-green != merged-true != deployed; built != shipped. Reproduce the user's environment (viewport/drawer state) before attributing a symptom. Ask the deploy-seam question of the lane that owns the path; never infer it.",
  "durable_test": "A cold Naya faced with a live-site gap will (1) open the live URL in the user's viewport first, (2) name which verification-chain link failed (branch/merge/deploy/render), (3) ask rather than guess when the deploy path crosses lane jurisdiction."
}
```
