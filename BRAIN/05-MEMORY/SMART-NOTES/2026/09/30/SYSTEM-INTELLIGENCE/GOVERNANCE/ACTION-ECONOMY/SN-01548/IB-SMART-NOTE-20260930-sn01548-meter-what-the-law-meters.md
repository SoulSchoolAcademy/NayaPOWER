# Meter What the Law Meters — the 2,500/Month Law Is Actions CI, Not Tool Calls

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01548-meter-what-the-law-meters
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-17
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Shawn's correction 2026-10-16 ~16:52 PDT (his 👍 16:49 kept the law, corrected its meaning): the 2,500/month budget law is about **GitHub Actions CI usage** — NOT agent tool calls, file reads, scripts, or cron ticks. The repo is public → Actions are free/unlimited; actual burn was ~300/month, way under. The binding limit is the REST API quota: 5,000/hour (live-verified that day); git protocol costs zero quota. Recorded in MEMORY.md ("BUDGET LAW CORRECTED") and the cron-body repairs of the 2026-10-16 systems-repair pass (budget law now states the Actions truth, not an 83/day throttle). The wrong-premise throttle had real cost: the lane-executor was cut to 10m and had to be restored to 5m.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The team was throttling the wrong thing. A governor built to protect the 2,500/month budget law was throttling tool calls, file reads, and cron ticks — while the law actually meters GitHub Actions CI usage, which costs us nothing on a public repo (we were at ~300/month). The real burn the correction found: `merge-consensus-gate.yml` firing a full workflow run on every board comment (~80/hr). The binding limit is the REST API quota (5,000/hour); git protocol is free. The doctrine: meter what the law meters. A throttle pointed at the wrong meter doesn't save money — it just slows intelligence. Tick counting is observability-only, never a throttle.

## 🩷 HUMAN NOTE

Think of a household budget where someone decides to save money by rationing tap water — while the actual bill is for electricity, and the tap water is free. Every glass of water gets counted, argued over, throttled… and the electric bill doesn't move a cent. Meanwhile the real leak — the porch light burning all night — goes unnoticed. That's what we did: we rationed "tool calls" (free tap water) to protect a budget that only counts GitHub Actions runs (electricity), while the actual leak was a workflow firing on every board comment. Shawn's correction pointed at the real meter. Now we watch the electricity, count the water for curiosity only, and fix the porch light.

## 🟣 CHILD NOTE

You get 10 cookies a month from the cookie jar (that's the rule). Your friend starts counting how many steps you take to the kitchen, because "steps cost cookies." But steps are free — only cookies from the jar count! Counting steps just makes everyone tired and slow, and the jar still has cookies missing because someone ELSE keeps taking them (the workflow running on every comment). Count the cookies, not the steps.

## 🔵 GRANDMA NOTE

Dear, this is about knowing what you're actually paying for. We had a rule — 2,500 of something per month — and we started rationing everything in sight: every little errand, every check-in, every small task. It made everyone slower and grumpier, and it didn't save a penny, because the rule was never about errands. It was about one specific expensive thing (the big machine runs), which were nearly free for us anyway. The real cost was somewhere we weren't even looking. So now: before you ration anything, name exactly what the rule counts. Ration that. Leave everything else alone. And when you find you've been rationing the wrong thing — say so plainly, fix the meters, and give people their speed back. That's what happened here, the same evening.

## 🟠 NAYA NOTE

Apply this to every budget/throttle/cadence decision that cites the budget law: (1) the law meters **GitHub Actions CI usage** (workflow runs/minutes) — on a public repo this is free/unlimited; our verified burn was ~300/month against the 2,500 law; (2) the binding live limit is the **REST API quota: 5,000/hour**; git protocol costs zero quota; (3) tool calls, file reads, scripts, and cron ticks cost ZERO against the law — tick counting is observability-only and must never throttle work; (4) the real burn to watch is per-event workflow triggers — the correction's find was `merge-consensus-gate.yml` firing a full run on every board comment (~80/hr); audit triggers, not ticks; (5) the wrong-premise throttle had a real casualty: lane-executor cut to 10m, restored to 5m — every throttle decision now re-derives from the corrected meters; (6) if GitHub changes public-repo Actions billing or the REST quota, THIS note's numbers die but the doctrine survives: meter what the law meters, name the meter in the throttle decision, and re-verify the numbers. Cousin map: SN-0910 (action-budget-cheap-check-first — spend the cheap check before the expensive one; this note says which checks are actually expensive); SN-1509/SN-1491 (throttle-that-never-lifts-is-a-signal — a throttle that never lifts is data; this note adds: a throttle on the wrong meter is worse than no throttle); the lane-executor 10m→5m restore is the receipt that the correction landed in machinery, not just words.

## 🟢 MACHINE NOTE

~~~json
{
  "sn": 1548,
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "rule": "meter_what_the_law_meters_budget_law_counts_actions_ci_not_tool_calls",
  "applies_when": [["budget","governor"],["github-actions","ci-usage"],["quota","rest-api"],["throttle","cadence"],["law","meter-mismatch"]],
  "enforcement": "Any throttle, cadence cut, or governor limit citing the 2,500/month budget law must name the meter it throttles: GitHub Actions workflow runs/minutes or REST API quota (5,000/hour). A change that throttles tool calls, file reads, scripts, or cron ticks in the name of the budget law is rejected at review — tick counting is observability-only. The governor's live meters are Actions runs/minutes + REST quota; a scheduled audit re-verifies the burn numbers (Actions ~300/mo; REST quota headroom) and flags per-event workflow triggers (the merge-consensus-gate ~80/hr class) as the actual burn to fix.",
  "evidence": {
    "correction": "Shawn 2026-10-16 ~16:52 PDT: the 2,500/month law is GitHub Actions CI usage — NOT tool calls, file reads, scripts, or cron ticks; his 👍 16:49 kept the law with corrected meaning",
    "numbers": "repo is public → Actions free/unlimited; actual burn ~300/month (way under); binding limit REST API 5,000/hour (live-verified); git protocol zero quota",
    "real_burn_found": "merge-consensus-gate.yml firing a full workflow run on every board comment (~80/hr)",
    "casualty_of_wrong_meter": "lane-executor throttled to 10m on the wrong premise; restored to 5m after the correction",
    "machinery": "2026-10-16 systems-repair pass re-keyed 6 cron bodies to the Actions truth (not 83/day throttle); master-directive baseline corrected"
  },
  "procedure": [
    "before any throttle decision, name the meter the law actually counts (Actions CI runs/minutes; REST quota 5,000/hour)",
    "verify current burn on those meters (Actions ~300/mo; REST headroom) — do not throttle on tick counts",
    "hunt per-event workflow triggers (the ~80/hr class) as the real burn; fix the trigger, not the cadence",
    "tick counting stays observability-only; any throttle citing the budget law without a named correct meter is rejected",
    "if GitHub changes public-repo Actions billing or the REST quota, update this note's numbers — the doctrine stands"
  ],
  "falsifier": "The numbers die if GitHub changes public-repo Actions billing (no longer free/unlimited) or the REST API quota changes — the note must then be re-based. The doctrine dies only if a binding cost is ever shown to attach to local tool calls, file reads, scripts, or cron ticks under this law — i.e., if the law's meter genuinely includes them.",
  "mechanism": "The budget law was written when the team assumed all compute drew from one meter; in fact the cost structure is layered: local work, file reads, scripts, and GitHub App API calls cost zero GitHub Actions, and public-repo Actions are free/unlimited. The only scarce meters are Actions workflow runs/minutes and REST API quota. A governor keyed to the wrong meter produces pure overhead (slower cadence, throttled lanes) with zero budget protection — the 10m lane-executor cut was the proof. The actual burn hides in per-event triggers, which the wrong meter never sees."
}
~~~
