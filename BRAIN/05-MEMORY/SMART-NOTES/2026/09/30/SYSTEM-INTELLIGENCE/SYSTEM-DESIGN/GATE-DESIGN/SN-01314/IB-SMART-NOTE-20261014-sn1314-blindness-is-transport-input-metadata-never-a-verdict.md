# IB-SMART-NOTE-20261014-sn1314

**Intelligent Block:** SN-1314
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-14
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

Blindness is transport-input metadata, never a verdict. The gate packet-3 build gave "we can't see" its own channel: exit contract 0 = pass, 1 = judged-fail, 2 = blind — and the word FAIL never appears on a blind line, nor GATE_BLIND on a judged line. Blind still fails closed (non-zero, blocking), but a builder seat maps exit 2 to "re-run advised," never to pass. The rule: give every non-verdict signal its own marker and its own exit code, and never let verdict vocabulary touch it. A blind run wearing FAIL's clothes masquerades as verdict instability; a blind run in its own uniform reads as what it is: transport-blind, try again.

## HUMAN NOTE

Imagine a referee who blows the whistle three different ways: one for "goal," one for "foul," and one for "I couldn't see what happened." The third whistle means "replay the play," not "penalty." Now imagine the referee only had two whistles — so "I couldn't see" came out sounding exactly like "foul." Every missed view would look like a bad call, and the whole game would argue about phantom penalties. That's the design lesson from the gate work: when a system can't get its answer (rate-limited, permission denied, network down), it must say "I couldn't see" in its own distinct voice — never borrow the language of failure. Keep failing closed (still block, still non-zero), but keep the vocabulary honest: "transport-blind, re-run advised."

## CHILD NOTE

Imagine three traffic lights: green means go, red means stop, and a special flashing yellow means "my camera is broken, so I don't know — be careful." Now imagine someone painted the "camera broken" light red too. Drivers would think there was danger on the road when really the camera was just broken — and the road crew would get called out for nothing. The lesson: give "I don't know" its own light. It still means "be careful" (fail closed), but it must never look like "there's danger." A blind signal wearing a verdict's clothes confuses everyone.

## GRANDMA NOTE

Dear, this one's about honest signals. The young ones built a gate that checks their work — and they found the gate needed a third answer besides yes and no: "I couldn't see." The network was down, the permission was missing, the rate was limited — none of that means the work is wrong; it means the check couldn't run. So they gave "I couldn't see" its own name and its own code, and they made a rule: that word never appears on a failure line, and failure words never appear on it. It still blocks (caution stays), but nobody mistakes a blind spot for a bad verdict. Plain dealing, even in machinery.

## NAYA NOTE

For every seat designing a gate or judged pipeline: reserve a dedicated blind channel — distinct marker, distinct exit code — and never let verdict vocabulary touch it. Evidence: [t0778] dispatcher mirror of t0762-lane8 INFRA packet-3 GATE_BLIND (2026-10-14, 9.0/10, branch naya/gate-blind-marker-t0762, unmerged, reviewable): exit contract 0=pass / 1=judged-fail / 2=blind; the words FAIL/REJECT/FAILED never appear on a blind line; GATE_BLIND never appears on a judged line; fail-closed preserved (blind is non-zero, blocking); a builder seat may map exit 2 -> "re-run advised," NEVER -> pass. Source quoted verbatim from #2537 comment 6167590868 (Lane 6 design): "Give GATE_BLIND its own marker (not FAILURE) so a blinded run reads as 'transport-blind, re-run advised' and never masquerades as verdict instability." Operational shape: three tools wired (ci_claim_evidence_gate.py, activation_gate.py, check_merge_consensus.py) — blind paths emit GATE_BLIND + exit 2 with a transport classification (rate-limited|permission-denied|io-error|missing-env); judged-fail paths keep exit 1 and exact texts; 11-test falsifier battery offline-proves the separation. Cousins: SN-1302 (blindness is what you DON'T run — blind-signal family); SN-1244 (adjudicate a gate verdict from its own predicate — gate-verdict discipline).

## MACHINE NOTE

{"sn": 1314, "category": "SYSTEM-DESIGN/GATE-DESIGN", "evidence": "hidden_files/twelve-lane-receipts/t0762-lane8.md + lesson-broadcast.md [t0778] (2026-10-14): packet-3 built on branch naya/gate-blind-marker-t0762; exit 0=pass/1=judged-fail/2=blind; FAIL vocabulary never on blind lines; blind still non-zero blocking; 11-test falsifier battery", "decision_change": "future gate/builder designs give non-verdict signals (transport-blind, can't-verify) their own marker + exit code, never reusing verdict vocabulary; builders map blind -> 're-run advised', never -> pass", "falsifier": "blind lines wearing FAIL vocabulary across sustained runs produce no verdict-instability confusion and no wasted human triage — the separation buys nothing", "mechanism": "verdict vocabulary triggers human-side reactions (holds, merges, investigations); a blind signal wearing FAIL's clothes masquerades as verdict instability, so every blind spot spawns a phantom verdict dispute; a distinct channel keeps 'we can't see' from ever reading as 'it's wrong'", "cousins": ["SN-1302", "SN-1244"], "admission_gates": {"durable": true, "new": true, "signal": true, "evidence_backed": true}}
