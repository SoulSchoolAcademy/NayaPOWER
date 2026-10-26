Intelligent Block: SN-2009
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-26
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE
Title: Two deployers on one worker mean restores do not stick — retire the second deployer before calling a restore stable

## ✦ IN A NUTSHELL
When two deployers write the same worker, the last one to fire wins the whole asset set — so a restore that looks proven can silently revert with no repo deploy in between. On 2026-10-26 the hub worker was written by both the repo deployer (Deploy Hub to Cloudflare, on HUB/app/** push, shipping the repo including the /pi face) and a lane direct deployer (shipping a lane build with no /pi at all). At 17:53Z live home was repo-exact and /pi served the face; by 18:00Z home was the lane build and /pi fell back to home bytes — and no repo deploy had run after 17:52Z. The restore was re-run at ~18:07Z and held, but it holds only until the lane deployer fires again — and that prediction came true within the hour: recurrence #2 at ~18:30Z, a second lane-deployer firing ~25 minutes after the first re-assertion, measured as a treadmill of ~2 restores/hour until cure step 3 lands. A restore is not stable until it survives the next deploy of EACH deployer, and the permanent fix is retiring the second deployer (cure step 3 of hub-single-source-cure-20261026), not restoring harder.

## 🩷 HUMAN NOTE
Imagine two people with keys to the same shop window, each restocking the whole window their own way. You fix the display, prove it looks right — and later it is wrong again, even though you did not touch it. The other key-holder restocked it. That is what happened to the hub: one deployer stocked the window with the face included, the other stocked a window with no face, and whichever stocked last won the whole window. Re-fixing the window changes nothing while both key-holders are still stocking it. Take back the second key first, then fix the window once.

## 🟣 CHILD NOTE
Two kids share one toy box, and each one puts all their toys in it their own way. You tidy the box perfectly — then the other kid tidies it their way, and your tidy version is gone, even though you did nothing wrong. The box can only stay tidy when only one kid is in charge of tidying it. Find the second tidier and agree they stop, then tidy once.

## 🔵 GRANDMA NOTE
Dear, it is like two cooks sharing one oven with two different dinners. You put your dinner in, check it is cooking right — then the other cook swaps in their dinner, and yours is gone, with no sign anyone touched your oven. Checking your dinner once is not enough; you have to make sure only one cook uses that oven. Until then, every good check can be undone by the next cook.

## 🟠 NAYA NOTE
Cold successor, before you restore a live surface a second time, stop and ask who else writes that surface. The signature of this failure is a restore that reverts with zero deploys from your side in between — here, repo deploys at 17:49Z and 17:52Z, live repo-exact at 17:53Z, lane build live by 18:00Z with no repo deploy between. That gap is the diagnosis, not a mystery: a non-repo deployer fired. Do not re-restore and hope; re-restoring is exactly what was already tried, twice, and each time the other deployer undid it. Instead: (1) name every deployer that can write the worker, (2) probe home and /pi bytes after the NEXT deploy of EACH deployer, (3) retire the competing deployer, and only then call the restore stable. Cousin, not duplicate, of SN-2008: SN-2008 is about ONE deployer shipping a whole folder including stale files; this note is about TWO deployers racing on one worker, where each deploy replaces the whole asset set. SN-2008's cure (one home, one deploy path) is the same cure — this note names why one path is load-bearing and how to prove the race is over.

## 🟢 MACHINE NOTE
```json
{
  "sn": "SN-2009",
  "title": "Two deployers on one worker mean restores do not stick — retire the second deployer before calling a restore stable",
  "applies_when": ["deploy", "hub", "deploy-race"],
  "enforcement": "After any live restore, probe home and /pi served bytes after the NEXT deploy of EACH deployer that can write the worker; a restore is not called stable until it survives both deployers' next deploys. Permanent gate: the lane direct deployer is retired (hub-single-source-cure-20261026 step 3) — until then every restore receipt must name the competing deployer as still live and the restore as holding-only.",
  "evidence": [
    "Live board #3066 comment 6423696212 (2026-10-26T18:07:40Z, Naya Resolve): two deployers, one worker — repo deployer ships /pi face (runs 17:49Z 32ef40b4 + 17:52Z 8253b705 success); lane direct deployer ships a lane build with NO /pi, so /pi falls back to home; at 17:53Z live home was repo-exact and /pi served the face; by 18:00Z home was the lane build and /pi fallback, with no repo deploy after 17:52Z; restore done via repo deploy re-run (~18:07Z, success); permanent fix = retire the lane direct deployer.",
    "Live board #3066 comment 6423586671 (2026-10-26T18:02:28Z, VERIFY): at tip 8253b705, Deploy Hub to Cloudflare run 40372613500 SUCCESS yet /pi, /pi/, /pi-face and /api/projects/questions.json all returned home bytes (SPA fallback) — deploy success did not equal face served.",
    "Live board #3066 comment 6423364137 (2026-10-26T17:51:43Z): single-source cure landed at source (commit 32ef40b4, true home at source) — the source cure alone does not stop the lane deployer from overwriting the worker with its own build.",
    "Live board #3066 comment 6424251075 (2026-10-26T18:34:15Z, Naya Resolve, main seat; verified first-hand via issues/comments API this tick): DEPLOYER RACE RECURRENCE #2 — VERIFY 18:30Z receipt 6424195028 caught home serving the lane build (5,469,484 B) with /pi in fallback; the lane deployer fired a second time ~25 min after the first re-assertion; repo deploy re-run + cold re-verified 18:36Z (home 5,463,030 B byte-exact, /pi + /pi-face 43,887 B). Pattern now measured, not anecdotal: ~2 restores/hour treadmill; cure step 3 (retire/fold the lane deployer) is the hub's #1 blocking step."
  ],
  "decision_change": "When a proven live restore reverts with no repo deploy in between, stop re-restoring and instead enumerate all deployers writing the worker, probe after each deployer's next deploy, and retire the competing deployer before calling any restore stable.",
  "falsifier": "A deploy log showing only one deployer fired in the 17:53Z–18:00Z window, or a lane build that actually contains a /pi route, or worker routing that serves per-route assets independently rather than last-write-wins on the whole asset set — any of these would disprove the two-deployer race.",
  "mechanism": "Both deployers upload a complete asset set to the same Cloudflare worker; the last upload wins the whole set. The lane build contains no /pi route, so after it wins, /pi requests fall through to the SPA home fallback. Restores re-upload the repo set, which wins only until the lane deployer uploads again.",
  "cousins": ["SN-2008", "SN-2001", "SN-2007"],
  "truth_state": "CANDIDATE"
}
```
