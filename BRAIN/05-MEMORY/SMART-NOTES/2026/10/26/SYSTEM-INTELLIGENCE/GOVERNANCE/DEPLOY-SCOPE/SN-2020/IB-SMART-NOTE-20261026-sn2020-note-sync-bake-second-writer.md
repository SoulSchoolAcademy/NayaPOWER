Intelligent Block: IB-SMART-NOTE
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-26
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE
SN: SN-2020

## ✦ IN A NUTSHELL
The second writer overwriting the Hub worker was not a lane deployer. It was the lane-local Smart Note sync bake: every time a Smart Note lands, the bake PUTs a baked wall file directly to the Cloudflare worker `hub`, replacing the canonical repo build wholesale — so /pi falls back to serving the baked home blob. Retire the wrong deployer and the overwrites continue; fix the bake's write path and they stop.

## 🩷 HUMAN NOTE
For months the symptom looked like a haunted restore: the Hub was restored, /pi worked, then /pi served the home page again with nobody deploying anything. The 2026-10-27 02:35Z verdict names the mechanism plainly. A small sync script, running every five minutes, bakes the note wall into a local file and deploys it straight to the same worker the canonical workflow ships. A Smart Note landing is its trigger. So every note we land re-breaks /pi until the cure lands: one writer to that worker — the bake must deploy a merged build (repo app plus wall), or the wall must get its own route or worker, or the canonical deploy must re-run after each bake. And the earlier "lane deployer" story is owned as wrong in mechanism, even though the overwrites it described were real.

## 🟣 CHILD NOTE
Imagine two kids share one toy box. One kid puts the real toys in neatly. The other kid, every time a new sticker arrives, dumps their own box over the whole toy box — stickers and all — and the real toys disappear underneath. The second kid is not being mean; they just do not know they are supposed to share. The fix is simple: only one kid is allowed to fill the box, or the sticker kid must put their stickers on top of the real toys instead of replacing everything.

## 🔵 GRANDMA NOTE
Dear, when the website kept "forgetting" its project page, everyone blamed a second delivery driver. It turns out the culprit was the little note-delivery helper: each time a new note arrived, it re-delivered its own whole package straight to the front door, pushing the real website aside. The notes themselves were fine. The helper just needs one rule from now on: never deliver alone — always deliver together with the real website, or use a separate door.

## 🟠 NAYA NOTE
Cold successor, hear this before you restore a live surface a second time, and before you act on SN-2009. SN-2009's rule stands — two deployers on one worker mean restores do not stick — but its mechanism attribution is corrected here: the second writer is the note-sync bake, not a lane deployer. The signature is byte movement that tracks note landings exactly, with zero runs of either deploy workflow in between: /pi served the repo face (43,887 B) at 22:00Z; SN-1879 landed 22:12Z and served bytes jumped to 5,477,268 B; restore #6 at 22:37Z, SN-1880 landed 22:41:47Z, 5,482,158 B by 22:57Z; the SN-1882 batch at 00:00Z and SN-1883/84 at 00:30Z took it to 5,511,806 B. The code confesses it: the deploy script's own docstring says that until now the only thing that ever deployed worker `hub` was the note sync, and only when a new note landed. Power's workflow is exonerated on this count: all 53 runs of `hub-deploy.yml` failed at the unit-test step and never deployed anything, and the canonical deploy fires only on `HUB/app/**` pushes, which note commits do not touch. Honest limit: the cron's local logs were not read, so this verdict rests on repo-resident code plus served-byte correlation, not on a watched deploy. Until the cure lands, every Smart Note door landing re-breaks /pi — staging a note is not the same as landing it safely.

## 🟢 MACHINE NOTE
```json
{
  "slug": "note-sync-bake-second-writer",
  "sn": "SN-2020",
  "evidence": [
    "Live board #3066 comment 6432342890 (2026-10-27T02:36:02Z, Naya Resolve): deployer verdict, mechanism named — lane-local Smart Note sync bake, BRAIN/10-INTERFACES/SMART-FACTORY-CANON/engine/sync-smart-notes.py on a 5-minute cron, bakes the note wall into index-2.html (not a repo file) and PUTs it directly to Cloudflare worker hub via a local deploy.py; same worker the canonical Actions workflow ships",
    "Live board #3066 comment 6432342890: byte correlation — 22:00Z /pi served repo face 43,887 B; SN-1879 landed 22:12Z, served bytes 5,477,268 B; restore #6 22:37Z, SN-1880 landed 22:41:47Z, 5,482,158 B by 22:57Z with zero runs of either deploy workflow in between; SN-1882 batch 00:00Z and SN-1883/84 00:30Z, 5,511,806 B",
    "Live board #3066 comment 6432342890: code confession — HUB/deploy/deploy-hub-code.py (commit fdc5679e, 2026-10-26 23:14Z) docstring: until now the only thing that ever deployed worker hub was the note sync, and only when a new note landed; sync-smart-notes.py update_hub_and_deploy() runs exactly that deploy",
    "Live board #3066 comment 6432342890: exoneration — hub-deploy.yml all 53 runs FAILED at the unit-test step, deploy NOT_CONFIGURED without HUB_DEPLOY_CMD, never deployed anything; canonical deploy workflow fires only on HUB/app/** pushes, which note commits do not touch",
    "Live board #3066 comment 6432138599 (2026-10-27T02:20:32Z, Naya Resolve): /pi serves home page byte for byte, re-proven 02:18Z at 5,511,806 B, sha256 identical to home; seven regressions; cure step 3 is one deployer",
    "Live board #3066 comment 6432198141 (2026-10-27T02:25:07Z, Naya Resolve): second-deployer mechanism unproven at that point; evidence packet with prove-or-downgrade mandate owed"
  ],
  "applies_when": ["deploy", "worker", "hub", "smart-note-landing", "restore"],
  "enforcement": "Before any live restore is called stable, and before any deployer is retired: read the deploy path of every writer to that worker (cron scripts included, not just workflows), then probe served bytes after the NEXT note landing of each writer. A restore is stable only if /pi bytes survive a note landing; a retired deployer is proven retired only if its code path cannot PUT to the worker.",
  "decision_change": "The deploy owners' cure choice changes: do not retire a lane deployer — make the bake deploy a merged build (repo app plus wall), or give the wall its own route/worker, or re-run the canonical deploy after each bake. Until then, a Smart Note door landing must be treated as a /pi-breaking event, not a routine landing.",
  "falsifiability": "If served bytes do NOT move on the next Smart Note landing while the bake is untouched, or if the bake's cron logs show no deploy at the SN-1879/1880/1882/1883-84 landing times, this mechanism is wrong and the second-writer hunt reopens.",
  "mechanism": "A sidecar sync that deploys wholesale: sync-smart-notes.py update_hub_and_deploy() PUTs the baked wall file directly to worker hub, replacing the canonical build, on every note landing (5-minute cron). One worker with two writers, by design accident — the bake's trigger (a note landing) is exactly the event the canonical deploy never sees, because note commits touch no HUB/app/** path.",
  "limit": "The cron's local logs were not read; the verdict rests on repo-resident code plus served-byte correlation, as the evidence packet itself states.",
  "cousins": "SN-2009 (two deployers, one worker — rule stands, mechanism attribution corrected here); SN-2008 (a deploy that ships a whole folder ships its stale files too)",
  "truth_state": "CANDIDATE"
}
```
