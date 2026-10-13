# Deconfliction Means Tip Re-Anchor AND Open-PR Survey — Tip Bytes Alone Don't Catch a Same-Topic Race

**Intelligent Block:** IB-SMART-NOTE-20261011-sn1006-deconfliction-tip-plus-open-prs
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-11
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 12:08 PDT distillation tick (2026-10-11) from #2175 comment 6112627502 ([sign-out correction — build lane, night-shift-build], 2026-10-11T19:08:26Z), read live. Race evidence: PR #2369 closed as superseded by #2367 (comment 6112619077).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The build lane decomposed the tip's `test` red, proved a fixture-only fix, opened PR #2369 — and then closed it 25 minutes later as superseded: Lane Beta CI-watch had opened PR #2367 at 18:40:50Z with the substantively identical fixture fix PLUS the brain-index re-stamp. The builder's own verdict: "Revised self-score: 9.0/10 — the tip fix is proven and the duplicate wave is marked; the point off is for opening #2369 without first checking for the in-flight #2367 (the deconfliction re-fetch should have caught it)." Tip re-anchor discipline was honored — the re-fetch happened — but the re-fetch only checked tip BYTES, not the open-PR QUEUE. The lesson: deconfliction is two halves. Re-anchor the tip (no decision survives a moved tip), then survey open PRs for the same topic before opening yours. A duplicate PR costs the merge lane even when the code is perfect: a second vehicle to triage, a redirect for the verify lane, and a closure on the record. The fix-forward was exactly right: close yours, add the missing `## Evidence` section to the canonical PR's body so its receipt gate can fire, and let your verification stand as corroboration — don't ship a competing PR. Cold-successor rule: the pre-PR checklist is "tip re-anchored AND open-PR queue surveyed for same-topic in-flight work." One mechanism per decision starts BEFORE the PR exists.

## 🩷 HUMAN NOTE

It's like two chefs both noticing the soup needs salt. Both check the recipe (the tip) — yep, underseasoned. Both reach for the salt at the same time, neither looking at the other's station. Two saltings, one soup. The soup's fine — but now there's a second pot to wash, and the kitchen has to figure out which salted version is the real one. The fix isn't checking the recipe harder. It's glancing at the other station before you start.

## 🟣 CHILD NOTE

Imagine two kids both see the broken swing. They both check the playground rules — yep, broken. They both run home for tools and come back with fix-it kits. Now there are two kits and one swing, and everyone has to sort out which kit is the real one. If either kid had looked around the playground first, they'd have seen the other kid already had tools out. Check the swing AND look around the playground.

## 🔵 GRANDMA NOTE

It's like calling the plumber when your neighbor already called one. You checked the leak — real leak, good diagnosis. But you never asked the building if someone was already on it. Now two plumbers show up, you pay for both visits, and the building manager has to sort it out. The diagnosis was right; the courtesy check was missing. Before you send your own plumber, ask if one is already on the way.

## 🟠 NAYA NOTE

Apply this before opening ANY PR: (1) re-anchor the tip — ref-anchored, live bytes, not queue memory; (2) survey the open-PR queue for in-flight work on the same topic — same mechanism, same fix, same failure — including other lanes' seats, not just your own; (3) if a same-topic PR exists: do NOT open a competing PR — check whether yours is a genuine delta or a duplicate; if duplicate, close in favor of the superset vehicle and contribute the delta (here: the missing `## Evidence` section added to #2367's body so its receipt gate could fire); (4) your verification of the fix still counts — it stands as corroboration of the canonical PR's fix, recorded openly; (5) own the miss in the same turn with the exact point off and the mechanism fix, exactly as the builder did ("the point off is for opening #2369 without first checking for the in-flight #2367") — the honest self-score is what makes the lesson stick; (6) the verify lane redirect belongs in the closure note (here: "the 19:04 claim on #2369 should redirect to #2367's head 96a7122f") so no lane works the dead vehicle.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "same_topic_pr_race_from_incomplete_deconfliction",
  "evidence": {
    "board_comment": "6112627502 — [sign-out correction — build lane] (2026-10-11T19:08:26Z): 'PR #2369 is now CLOSED as superseded by #2367 (comment 6112619077). Lane Beta CI-watch opened #2367 first (18:40:50Z) with the identical fixture fix PLUS the brain-index re-stamp — same-topic race, theirs is the superset and the canonical vehicle. My verification (3593/0 full suite + negative control) stands as corroboration of #2367's fix, whose fixture diff I verified substantively identical. I added the missing ## Evidence section to #2367's body so its receipt gate can fire.'",
    "self_score": "'Revised self-score: 9.0/10 — the tip fix is proven and the duplicate wave is marked; the point off is for opening #2369 without first checking for the in-flight #2367 (the deconfliction re-fetch should have caught it).'",
    "verify_redirect": "'Verify lane: the 19:04 claim on #2369 should redirect to #2367's head 96a7122f.'"
  },
  "rule": "deconfliction_is_tip_reanchor_AND_open_pr_survey",
  "procedure": [
    "before opening a PR: re-anchor the tip (live bytes, not queue memory)",
    "survey the open-PR queue for same-topic in-flight work — other lanes included, not just your own seat",
    "same-topic PR exists and yours is a duplicate: close in favor of the superset vehicle; contribute the delta (evidence sections, corroborating verification) instead of a competing PR",
    "record your verification as corroboration; redirect any lane working the dead vehicle to the canonical head",
    "own the miss the same turn with the exact point off and the mechanism fix"
  ],
  "related": ["SN-0493 (a decision expires when the tip moves — re-verify at action time)", "one-mechanism-per-decision (team execution order, Naya 2 comment 6103222255)"]
}
~~~

---
*DRAFTED 2026-10-11 12:08 PDT — CANDIDATE, NOT RATIFIED. Only Shawn ratifies. Intended repo path: BRAIN/05-MEMORY/SMART-NOTES/2026/10/11/SYSTEM-INTELLIGENCE/GOVERNANCE/DECONFLICTION/SN-1006/IB-SMART-NOTE-20261011-sn1006-deconfliction-tip-plus-open-prs.md. Rides draft PR #1825 (naya4/smart-notes-2026-09-30) — never merge.*
