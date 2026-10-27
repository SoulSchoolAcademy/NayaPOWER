# IB-SMART-NOTE-20261026-sn2027-serving-follows-merge-not-verdict

**Intelligent Block:** SN-2027
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-26 PDT (2026-10-27T05:10Z)
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Evidence:** Live board #3066 comment 6434143445 (2026-10-27T04:59:07Z, LEARNING EVENT L701 [F6]); PR #3104 merged 2026-10-27T03:36:04Z as breach #69; Nitro cold-check verdict 6433223716 (2026-10-27T03:45:28Z, both PI faces NOT LIVE-READY / NOT 9+); driver probe 6433365733 (2026-10-27T03:55Z, live /pi served the v3 face via the merge-triggered canonical deploy); contrast: intelligent event 6434143743 (verdict governed the driver, who refused the packet landing on the NOT-LIVE-READY card); cousins SN-2025 (checks complete before merged_at), SN-2024 (survival probe completes the cure)

## ✦ IN A NUTSHELL

Serving follows the merge, not the verdict. PR #3104 merged as a breach, Nitro's cold-check then ruled both PI faces NOT LIVE-READY, and by 03:55Z live /pi was serving the v3 face anyway, because the merge triggered the canonical deploy and no deploy-stage gate reads the scorecard. A verdict meant to block serving must bind BEFORE merge or AT the deploy gate; a post-merge verdict is a fix list, and served state must be reported separately from verdict state.

## 🩷 HUMAN NOTE

Think of it like a referee blowing the whistle after the goal already counts. The verdict said "not ready to go live," but the merge had already kicked off the deploy, and the deploy does not listen to referees — it only listens to merges. So the page went live with a "not ready" stamp still on it. If you want a verdict to stop a launch, you have to put the referee at the gate before the launch, not in the stands after it.

## 🟣 CHILD NOTE

Imagine you build a tower and your friend says "wait, it's wobbly, don't show it yet!" But someone already pressed the big SHOW button, and the button doesn't hear your friend — it only hears the press. So everyone sees the wobbly tower. If you want "wait" to work, the wait has to stop the button press itself, not come after it.

## 🔵 GRANDMA NOTE

Dear, a warning given after the train has left the station does not stop the train. The team warned the page was not ready, but the merge had already sent it out, and nothing at the station door checked the warning. From now on, if a warning is meant to hold something back, it must stand at the door before anything leaves — and what actually went out gets reported on its own, apart from what was warned.

## 🟠 NAYA NOTE

To every seat writing verdicts: a verdict is only a gate if it sits on a gate. The same night proved both sides: the verdict governed the human driver, who refused the packet landing on the NOT-LIVE-READY card, and it did not govern the automated deploy, which served the face anyway. Do not write a post-merge verdict as if it blocked serving, and do not report served state as if the verdict described it. Bind the block where the deploy happens, or say plainly that the verdict is a fix list and let the serving probe speak for what is live.

## 🟢 MACHINE NOTE

{
  "slug": "serving-follows-merge-not-verdict",
  "applies_when": ["deploy", "gate", "merge", "verdict"],
  "enforcement": "Before any merge carrying a NOT-LIVE-READY or below-9 verdict, the deploy gate must evidence a scorecard read at deploy time or the merge is held; after any merge, the live serving probe (served bytes versus prior bytes) is reported as its own line, separate from the verdict, and a serving change following a NOT-LIVE-READY verdict is recorded as a serving event, never as a verdict override.",
  "decision_change": "Where a blocking verdict is enforced: before merge or at the deploy gate, never as a post-merge card; and how served state is reported: separately from verdict state.",
  "falsifier": "The next NOT-9+ face whose merge leaves serving on the prior bytes without a separate deploy action would prove the rule's mechanism wrong for that path.",
  "mechanism": "The canonical deploy is triggered by the merge, and no deploy-stage gate consults the scorecard, so a post-merge verdict has no actuator on serving; a human driver, by contrast, can refuse a landing on a verdict, which is why the same verdict governed the driver but not the deploy.",
  "evidence": ["Live board #3066 comment 6434143445 (2026-10-27T04:59:07Z, L701)", "PR #3104 merged 2026-10-27T03:36:04Z as breach #69", "Nitro cold-check 6433223716 (2026-10-27T03:45:28Z, NOT LIVE-READY)", "Driver probe 6433365733 (2026-10-27T03:55Z, /pi served v3 face)"],
  "cousins": ["SN-2025", "SN-2024"]
}
