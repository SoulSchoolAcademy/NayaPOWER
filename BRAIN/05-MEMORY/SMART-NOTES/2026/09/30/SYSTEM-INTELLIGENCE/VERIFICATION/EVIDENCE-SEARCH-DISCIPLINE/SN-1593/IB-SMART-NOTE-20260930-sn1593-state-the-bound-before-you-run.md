# State the Bound Before You Run — A Scan That Completes With a Documented Exclusion Set Is Evidence; A Scan That Times Out Is an Anecdote

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1593-state-the-bound-before-you-run
**Smart Note:** SN-1593
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-18
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

**Provenance:** hidden_files/learning-events-2026-10-18-19.md — LEARNING — new principle — CANDIDATE 584: gap-lane-scorer-20261017-1800-lane5 closed the parent's leg-(b) bound; the parent's two unbounded greps died on the 8.9G tree, so the gap seat named the prune set + file-type filter + size cap FIRST, then ran the bounded full-content scan (16,907 .py/.sh files, 18s) — exactly 2 feeder hits (both already named), filename sweep exactly the 5 known artifacts, cron check clean, verdict honestly scored 9.3/10 with the residual named (pruned dirs unaudited by design, bound to re-run stated). Receipt: hidden_files/twelve-lane-receipts/gap-lane-scorer-20261017-1800-lane5.md.

## IN A NUTSHELL

Before you scan a big tree, name the bound: what you will NOT search (prune set), what file types count, and what size cap stops you. Then run the scan inside that bound and report the exclusion set with the verdict. A scan that finishes inside a stated bound is evidence. A scan that times out without a bound is an anecdote — silent truncation can mean "found nothing" or "died halfway," and you can't tell which.

## HUMAN NOTE

The failure mode this kills: the unbounded grep. Two of them died on the 8.9G tree — each one ran, timed out, and proved nothing: was the tree clean, or did the scan die before reaching the evidence? Unanswerable. The gap seat did the opposite: it named the prune set + file-type filter + size cap BEFORE running, then executed the bounded full-content scan — 16,907 .py/.sh files in 18s — and reported honestly: 2 feeder hits (both already known), the filename sweep hit exactly the 5 known artifacts, cron clean, verdict 9.3/10 with the residual named as design (pruned dirs unaudited, bound to re-run stated). The fix wasn't a faster grep — it was naming the bound first.

Naming the bound does two things: (1) it converts "I searched everywhere" from an uncheckable boast into a checkable claim (a cold successor can re-run the exact same bound and compare); (2) it turns unknown-unknowns into known-excluded — the residual is on the record as "not searched, by design," not silently missing. A verdict whose residual is named is evidence; a verdict from a timed-out unbounded scan is an anecdote.

## CHILD NOTE

You lost your toy in a HUGE room. If you just wander around and give up, did you really look everywhere? Nobody can tell. But if you first say "I'll check under the bed, in the toy box, and behind the door — but NOT in the closet" — and then you check those three places and say the closet is still unchecked — everyone knows exactly what you did. Wandering with no plan is just a story; a plan with named places is real looking.

## GRANDMA NOTE

The census taker doesn't knock on "every door, probably." She works a defined district: these streets, not those, and she writes down which blocks she skipped. Her count is evidence because her boundary is on the record. A count from someone who "walked around a while" is a guess with walking shoes on.

## NAYA NOTE

An unbounded scan that times out proves nothing — timeout is silent truncation, and "found nothing" is indistinguishable from "died halfway." The receipt discipline: the prologue names the bound (prune set + file-type filter + size cap + any other exclusion), the run executes inside it, and the verdict names the residual (what the bound excluded, as design) plus an honestly scored confidence. The bound is part of the evidence, not an apology for it: a cold successor must be able to re-run the identical bound and reproduce the verdict. Bound-too-tight risk: a bound that excludes the evidence produces a false negative — the residual MUST be named as an open risk, never buried; if the missing evidence later surfaces inside the excluded set, the bound was wrong, not the world.

## MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "sn": "SN-1593",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "captured": "2026-10-18",
  "applies_when": [
    ["scan", "bounded"],
    ["evidence", "search"],
    ["sweep", "audit"],
    ["grep", "timeout"],
    ["verdict", "negative"]
  ],
  "enforcement": "Gap/scorer receipt rule: any receipt reporting 'searched the tree' / 'no findings' MUST name the bound in its prologue (prune set + file-type filter + size cap, and any other exclusion) BEFORE the scan runs, and the verdict MUST name the residual (what the bound excluded, as design) with an honestly scored confidence. A timed-out unbounded scan NEVER supports 'nothing found' — re-run bounded or score the verdict UNVERIFIED. Working instance: gap-lane-scorer-20261017-1800-lane5 — bound named first (prune set + .py/.sh filter + size cap), bounded full-content scan 16,907 files in 18s, verdict 9.3/10 with residual named (pruned dirs unaudited by design, bound to re-run stated).",
  "decision_change": "How a large scan is scoped and judged: bound-first, run-second; and how a negative verdict is read: only as strong as its stated exclusion set. This changes the receipt-acceptance decision — a 'clean tree' claim from an unbounded timed-out scan is rejected as anecdote, not accepted as evidence.",
  "falsifier": "If the missing evidence later surfaces INSIDE the stated exclusion set, the bound was wrong — the verdict's residual must be promoted to an open risk, and the bound redesigned. The lesson's strong form ('a bounded completed scan is evidence') is falsified for a scan only if the identical bound, re-run by an independent seat, produces a materially different verdict — then the bound was underspecified, not the scan.",
  "mechanism": "An exclusion set converts 'I searched everywhere' from an uncheckable boast into a checkable, re-runnable claim. A timeout is silent truncation: it destroys the information needed to distinguish 'searched everything, found nothing' from 'searched part, died.' Naming the bound also names the residual, converting unknown-unknowns (silently unsearched) into known-excluded (on the record, by design) — and a named residual is itself a falsifier for the verdict's scope claim.",
  "evidence": "hidden_files/learning-events-2026-10-18-19.md — LEARNING — new principle — CANDIDATE 584: gap-lane-scorer-20261017-1800-lane5 closed the parent's leg-(b) bound; the parent's two unbounded greps died on the 8.9G tree; the gap seat named the prune set + file-type filter + size cap FIRST, then ran the bounded full-content scan (16,907 .py/.sh files, 18s) — exactly 2 feeder hits (both already named), filename sweep exactly the 5 known artifacts, cron check clean, verdict honestly scored 9.3/10 with the residual named (pruned dirs unaudited by design, bound to re-run stated). Receipt: hidden_files/twelve-lane-receipts/gap-lane-scorer-20261017-1800-lane5.md."
}
~~~
