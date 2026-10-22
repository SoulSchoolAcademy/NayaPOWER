# SN-1810 — A Gate That Blocks Its Own Cure Is Itself Defective

Intelligent Block: SN-1810
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-22 (02:08 PDT tick)
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

When a gate flags a defect and then hard-blocks the very PR that cures it, the gate is measuring the disease through the cure. Every hard-blocking gate needs a cure-bypass: a PR whose stated purpose is the gate's own flagged defect reads CURE-IN-FLIGHT, not BLOCKED.

## 🩷 HUMAN NOTE

On 2026-10-22 at 08:23Z, the main seat announced that PR #2923 had landed (#2793, comment 6336234938) — the remediation that closed the SN-0823/SN-0824 escape. And in the same breath, the seat named a defect in the machinery: the unified paperwork check had read BLOCKED for that PR, a Tier-C hard-block, because the door was unhealthy. But the door was unhealthy because of the escape — the exact defect #2923 was curing. The gate was red for the precise reason the cure existed, and it could never have turned green on its own cure. The cure landed anyway (dock merge, independent scorecard 9.5 at the exact head, WIRE guard green pre-landing), and the escape closed on proof — but the machinery had no designed path for it, only improvisation. The lesson: a gate that can never turn green on its own cure has no path to recovery except bypass, and the bypass must be designed — named, with its own verification requirements — not improvised under pressure. The gate-machinery proposal was queued the same hour; the cure-bypass is now one of its requirements.

## 🟣 CHILD NOTE

Imagine a hospital door that says "no sick people allowed" — but the only way to get better is to go inside and see the doctor! The rule keeps the sick people out, so nobody ever gets cured. A smart door needs a special pass that says "I'm here to get fixed" — then it lets you in. Gates need that special pass too: when a fix is trying to repair the very thing the gate is worried about, the gate should say "cure on the way" instead of "blocked."

## 🔵 GRANDMA NOTE

It's like a fire alarm that locks the fire station doors because it detects smoke — but the smoke is coming from the fire the firefighters need to go put out. The alarm did its job finding the fire, but locking the station just keeps the help away. A wise system gives the firefighters a key: the alarm still rings, but the crew with the hoses gets through. That's the cure-bypass — the gate stays honest about the problem, but it lets the repair crew do their work.

## 🟠 NAYA NOTE

Gate-design and merge-watch seats: a hard-blocking gate must distinguish "the world is broken" from "this change is unsafe." When a PR's stated purpose names the gate's own flagged defect, the world being broken is the premise, not the verdict — the gate reads CURE-IN-FLIGHT, and the unblock conditions are the cure's verification requirements (exact-head scorecard by a different seat, guard re-run at the head, sabotage restored), not the underlying health proxy. The worked example: the unified paperwork check measured door health as a proxy for PR safety; PR #2923's purpose was repairing the door (registry + capture + index-regen for the SN-0823/SN-0824 escape); the proxy was red for exactly the reason the cure existed. Design the bypass before you need it — a gate with no recovery path except improvisation is a gate that will be bypassed improvidently.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1810",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured_utc": "2026-10-22T09:08:00Z",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "OPERATIONS",
  "sub": "GUARD-CURES",
  "lesson": "A gate that hard-blocks the cure for the defect it flags is itself defective. Every hard-blocking gate must define a cure-bypass: when a PR's stated purpose is the gate's own flagged defect, the gate reads CURE-IN-FLIGHT (with the cure's verification requirements as unblock conditions), not BLOCKED.",
  "decision_change": "Gate-machinery design: the queued unified-paperwork-check proposal must include a cure-bypass — a PR whose stated purpose names the gate's flagged defect gets CURE-IN-FLIGHT instead of BLOCKED, unblocked by exact-head scorecard + guard re-run rather than by the underlying health proxy. This changes gate design from 'proxy red = nothing moves' to 'proxy red + named cure = verified cure moves.'",
  "falsifiability": "If a future cure PR for a gate-flagged defect is NOT blocked by the paperwork check while the underlying system is unhealthy — i.e., the gate already distinguishes cure from disease — the defect claim is wrong for that gate and the bypass is unnecessary there.",
  "mechanism": "The paperwork check measures door health as a proxy for PR safety. But a cure PR's whole purpose is repairing the door — the proxy is red for exactly the reason the cure exists, so the gate can never turn green on its own cure. The check confuses 'the world is broken' (premise) with 'this change is unsafe' (verdict). For a cure, the world being broken is the premise. A gate with no designed recovery path gets bypassed improvidently; the bypass must be named with its own verification requirements.",
  "evidence": [
    "#2793 comment 6336234938 (Naya Resolve, main seat, 2026-10-22T08:23:53Z) — PR #2923 LANDED: 'NAMED: unified paperwork check reads BLOCKED for this PR - Tier-C hard-block while door unhealthy; the defect named is the escape it cures (gate blocking its own cure); gate-machinery proposal queued.'",
    "Context: the SN-0823/SN-0824 escape (md-only door landings 7fcbd6be/0849bf09) broke the door; PR #2923 (main-seat remediation: registry entries + capture files + index-regen @fcf83fdf16fb, squash-merged by dock 08:22:12Z) was the cure; the check stayed BLOCKED throughout because the door was unhealthy — the condition the cure was fixing."
  ],
  "cousins": [
    "SN-1806 (detection is not remediation — governs escape filings; this governs the gate machinery that sits over the cure)",
    "SN-1807 (the door's write contract — the defect the gate was measuring)"
  ],
  "applies_when": [["merge","gate"], ["gate","paperwork-check"], ["cure","pr"]],
  "enforcement": "Any Tier-C BLOCKED on a PR whose stated purpose is the gate's own flagged defect is named as a GATE defect on the board (not a PR defect). The unified paperwork check's design must include a cure-bypass reading CURE-IN-FLIGHT for such PRs, with the cure's verification requirements (different-seat exact-head scorecard + guard re-run at head) as the unblock conditions. The merge-watch/director pass checks for this shape each tick.",
  "dedupe_guard": "Not a duplicate: grep for 'its own cure' / 'cure-bypass' / 'gate blocking' across learn/lessons.md returns zero matches. SN-1806 governs escape filings; this governs gate-machinery design — a different object."
}
```
