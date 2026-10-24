**Intelligent Block:** IB-SMART-NOTE-20261024-sn1942-check-deploy-currency-before-grading-code
**Smart Note:** SN-1942
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-24
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** twelve-lane-receipts/t1530-lane12.md (Mirror: "the disagreement is evidence about deploy currency"); twelve-lane-receipts/t1531-lane12.md (Mirror: "pin the provenance path before grading the code"); twelve-lane-receipts/gap-t1530-lane12.md; learning-events-2026-10-24-10.md (LEARNING EVENT CANDIDATE 914)

## ✦ IN A NUTSHELL

Check deploy currency before grading code — a live-vs-repo mismatch is evidence about which bundle is live, not that either observation is wrong. t1530-lane12 found the 09:08–09:13Z audit's 15-label sidebar matches no room set in the 11-room main-tip rail and refused a DESIGNED/BROKEN verdict (UNKNOWN instead); t1531-lane12 pinned the live bundle (deployment d9d3d859, version ab6e0440 / number 222, created 2026-10-24T05:55:20Z) and proved the commit leg absent by construction — api-upload deploys carry no commit field — with the upload out-of-pipeline (workflow last run 2026-10-22, wrangler says workflow-only); gap-t1530-lane12 independently reproduced all three legs on a fresh clone plus a live workflow-runs check. The rule going forward: every future live-vs-repo mismatch verdict first establishes the live bundle's id, version, and provenance — and a commit-binding deploy path, not another lookup, is the cure for a commit-blind deploy.

## 🩷 HUMAN NOTE

Two people looked at the same app and disagreed: one saw a sidebar with 15 labels, the other saw a code repository with 11 rooms. Neither was lying — they were looking at different versions of the app. The live app had been uploaded by a path that leaves no record of which code commit it came from, so nobody could tie it back to the repository. The workers refused to call the app "broken" or "designed" until they had pinned down exactly which live bundle was running — its deployment id, its version, and how it got there. The lesson: when the live app and the code disagree, first ask "which version is actually live, and how did it get there?" A mismatch is a clue about currency, not proof that someone is wrong.

## 🟣 CHILD NOTE

Imagine two friends arguing about a picture: one says it has 15 stickers, the other says the original has 11! Neither is lying — they are looking at two different copies! The workers figured this out: the live app was uploaded in a way that left no note saying which original it came from. So they refused to say "broken!" until they found out exactly which copy was live — its name, its number, and how it arrived. The lesson: when two things disagree, first check which version is really live. A difference is a clue, not a fight!

## 🔵 GRANDMA NOTE

Dear, imagine two cooks arguing over a recipe: one tastes 15 spices, the other counts 11 in the book. Neither is wrong — they are tasting two different batches. That is what happened here: the live app and the code repository disagreed, and the workers refused to call either one broken until they pinned down which live bundle was actually served — its deployment, its version, and the path that put it there. The upload path, it turned out, leaves no record of its source commit at all. The lesson: when live and repo disagree, first establish which bundle is live and how it got there. The mismatch is evidence about currency, not a verdict about the code — and the real cure is a deploy path that binds every live bundle to its commit, so this question never has to be asked again.

## 🟠 NAYA NOTE

The instrument here is the bundle pin, and the verdict it gates is any live-vs-repo judgment. A live bundle deployed by api-upload carries no commit field by construction, so "live differs from repo tip" cannot be read as "the code is wrong" or "the live app is broken" — the two observations may simply describe different artifacts. t1530's refusal (UNKNOWN, not DESIGNED/BROKEN), t1531's pin (deployment d9d3d859, version ab6e0440 / number 222, 2026-10-24T05:55:20Z, out-of-pipeline), and gap-t1530's independent reproduction on a fresh clone form the complete pattern: pin first, grade second. Any future mismatch verdict that grades code before pinning provenance should be returned as unproven — and the structural cure is commit-binding deploys, not more lookups, because a lookup cannot recover a commit that was never recorded.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1942",
  "title": "Check deploy currency before grading code — a live-vs-repo mismatch is evidence about which bundle is live, not that either observation is wrong.",
  "applies_when": ["deployment", "verification", "live-vs-repo", "deploy-currency", "lane-executor"],
  "enforcement": "A live-vs-repo mismatch verdict must first cite the live bundle's deployment id, version, and provenance path; without a pinned bundle the verdict is UNKNOWN, never DESIGNED/BROKEN, and a commit-blind deploy path (api-upload, no commit field) is recorded as the provenance gap, cured only by a commit-binding deploy path.",
  "decision_change": "Future live-vs-repo mismatch verdicts establish the live bundle's id/version/provenance before grading code — the 15-label sidebar vs 11-room rail disagreement is read as a deploy-currency question (live bundle d9d3d859, version ab6e0440 / number 222) instead of a DESIGNED/BROKEN verdict on either side.",
  "falsifiability": "Falsified if every live bundle is proven commit-bound by construction (a single deploy path that always records its commit) — then a live-vs-repo mismatch must be a code difference, and provenance pinning adds nothing. Weakened if bundle pins repeatedly match the repo tip with no currency gaps found.",
  "mechanism": "Multiple deploy paths exist (api-upload vs workflow), and api-upload deploys carry no commit field, so a live bundle can be detached from any repo commit: grading that bundle against the repo tip compares two different artifacts. Pinning the bundle's id/version/provenance first separates the currency question (which bundle is live?) from the code question (is the code right?), preventing a currency gap from masquerading as a code defect.",
  "evidence": ["twelve-lane-receipts/t1530-lane12.md (Mirror: the disagreement is evidence about deploy currency)", "twelve-lane-receipts/t1531-lane12.md (Mirror: pin the provenance path before grading the code; deployment d9d3d859, version ab6e0440 / number 222, created 2026-10-24T05:55:20Z)", "twelve-lane-receipts/gap-t1530-lane12.md (independent reproduction on a fresh clone plus live workflow-runs check)", "learning-events-2026-10-24-10.md (LEARNING EVENT CANDIDATE 914)"]
}
```
