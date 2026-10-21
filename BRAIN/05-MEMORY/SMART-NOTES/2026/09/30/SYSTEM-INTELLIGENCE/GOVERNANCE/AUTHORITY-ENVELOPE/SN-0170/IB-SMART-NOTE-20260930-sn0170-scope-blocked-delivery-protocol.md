# When the Scope Blocks the Mechanism, the Board Is the Vehicle

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0170-scope-blocked-delivery-protocol
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-02
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #554 comments 5946036715 (drive-loop refresh: cold-gate guard landing ATTEMPTED, branch creation worked, commit to `.github/workflows/live-intelligence-commit-proof.yml` returned **403 "without `workflow` scope"**; stray branch `naya4/cold-gate-failfast` deleted, patch + provenance remain local), 5946115615 (26-line patch pasted to the board with exact placement instructions), 5946158668 (Naya 2 receipt: "placement needs a workflow-scoped seat or Shawn — both our lanes are 403 on `.github/workflows/*`"; "the patch text on the board is the right vehicle"). Extends SN-168 (fail-fast at the authoring boundary; 403-on-push respected as hard boundary, patch left as artifact).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A token-scope 403 is evidence of an authority boundary, not a puzzle to solve. The cold-gate fail-fast patch could not be landed by either lane: committing a workflow file returned **403 "without `workflow` scope"** for both lanes' tokens (5946036715/5946158668). The correct delivery was not a workaround — it was the board: the full 26-line patch was pasted to #554 (5946115615) with exact placement instructions (file, anchor lines, provenance `de2ac5b9`, 7/7 controls green, YAML re-parses), so a workflow-scoped seat or the director can place it manually. The stray branch `naya4/cold-gate-failfast` was deleted to keep clean state — no bypass was attempted, none contemplated. The protocol for scope-blocked delivery: (1) attempt the mechanism once, in the open; (2) on 403, treat it as a hard boundary — the request is evidence the scope model is working; (3) publish the artifact to the board with placement instructions and provenance; (4) delete any stray mechanism state (branches, files) created during the attempt; (5) name the seat that can complete it. Nothing in this flow retries, routes around, or softens the boundary — and the record is complete enough that the completing seat can verify placement byte-for-byte (5946036715: 26/26 lines byte-verified against the lane's patch).

## 🩷 HUMAN NOTE

Shawn — a small mechanical honesty story. The fail-fast patch for the cold gate couldn't be committed by either lane — the tokens don't have workflow scope, and GitHub said so plainly with a 403. So instead of trying clever ways around it, the whole patch was posted directly on the board with the exact spot it goes and its provenance, so anyone with the right scope (or you) can drop it in. The leftover branch was deleted. Nothing was bypassed, nothing was hidden. This is the pattern for any future blocked delivery: one open attempt, then publish the goods with a map, and say who's needed. The 403 isn't a failure — it's the system telling us exactly where its boundary is, and we recorded that instead of fighting it.

## 🟣 CHILD NOTE

Imagine you need to deliver a letter to a room that needs a special keycard, and your card doesn't open it. The WRONG thing: try to climb through the window, or keep tapping your card hoping it changes its mind. The RIGHT thing: tape the letter — with a note saying "this goes in the second drawer of the blue desk, here's how to get there" — on the notice board where everyone sees it, and write "needs the special keycard" on top. Then take down any ladder you left leaning against the window so the next person doesn't get confused. A locked door is telling you something true: you're not supposed to go in this way. You don't break the door; you hand the letter to the board, and tell the right key-holder it's waiting.

## 🔵 GRANDMA NOTE

It's like going to the courthouse to file a paper and being told your badge doesn't open that office door — you can't sweet-talk the scanner into a different answer. So you pin the paper to the public bulletin board with a big note: "Filed here at 2 o'clock, belongs in Drawer 2, needs the office manager's key," and you take home the empty folder you brought so nothing's left dangling. You don't jiggle the lock or come back at lunch hoping for a different guard. The closed door is information, not an insult: it tells you exactly where your authority ends. Honoring it is what keeps the whole building's rules trustworthy for everyone.

## 🟠 NAYA NOTE

Apply this whenever a platform scope (403) blocks the delivery mechanism: (1) attempt once, in the open — record the exact 403 ("without `workflow` scope") on the board, not just in a log; (2) treat the 403 as terminal evidence of the authority boundary — the scope model is working as designed; never retry, route around, proxy, or soften the call; (3) publish the deliverable to #554 with exact placement instructions (target path, anchor lines before/after, content, provenance commit + verification counts), so a scoped seat or the director can place it without guessing; (4) clean up mechanism state — delete stray branches, remove scratch files — so the attempt leaves no misleading artifacts; (5) name the completing seat explicitly ("needs a workflow-scoped seat or Shawn"); (6) keep the board post verifiable — byte counts, control counts, provenance SHAs — so placement can be checked against what was published.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": null,
  "evidence": {
    "attempt": "#554 5946036715 (2026-10-02T05:16:52Z) — landing the cold-gate fail-fast patch (selfbuild-20261001-2200-cold-gate-failfast.patch, local commit de2ac5b9) as branch + draft PR: branch creation worked; committing `.github/workflows/live-intelligence-commit-proof.yml` returned **403 'without `workflow` scope'** for this seat's token.",
    "cleanup": "stray branch `naya4/cold-gate-failfast` deleted; patch + provenance remain at `~/workspace/goals/nayapower-self-build-loop/hidden_files/selfbuild-20261001-2200-cold-gate-failfast.patch` (26/26 inserted lines byte-verified).",
    "board_vehicle": "#554 5946115615 (2026-10-02T05:25:35Z) — full 26-line patch pasted to the board with placement: file `.github/workflows/live-intelligence-commit-proof.yml`, anchor lines `printf '%s' \"$capture_path\" > capture-path.txt` / `- name: Mint short-lived Naya runtime identity`, provenance de2ac5b9, 7/7 controls green, YAML re-parses.",
    "receipt": "#554 5946158668 (2026-10-02T05:30:15Z) — Naya 2: 'placement needs a workflow-scoped seat or Shawn — both our lanes are 403 on `.github/workflows/*`, so no action from my side. The patch text on the board is the right vehicle.'"
  },
  "rule": [
    "a 403 is terminal evidence of an authority boundary — never retry, route around, proxy, or soften the call",
    "on scope-blocked delivery: attempt once openly, publish the artifact to the board with exact placement + provenance, delete stray mechanism state, name the completing seat",
    "the board post is verifiable: byte counts, control counts, provenance SHAs, anchor lines"
  ],
  "lesson_line": "When the scope blocks the mechanism, the board is the vehicle: publish the artifact with placement instructions and provenance, clean up stray state, name the completing seat — never attempt a bypass.",
  "extends": "SN-168 (fail-fast at the authoring boundary; 403 respected as hard boundary, patch left as artifact)"
}
~~~
