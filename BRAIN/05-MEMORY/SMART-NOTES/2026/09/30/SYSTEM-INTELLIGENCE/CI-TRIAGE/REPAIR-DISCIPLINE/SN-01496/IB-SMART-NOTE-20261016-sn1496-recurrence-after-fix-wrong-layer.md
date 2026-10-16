# When a Fix Fails to Stop Recurrence, Re-aim at a Different Layer — Don't Widen the Same Fix

**Intelligent Block:** IB-SMART-NOTE-20261016-sn1496-recurrence-after-fix-wrong-layer
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-16
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 13:08 PDT distillation tick (2026-10-16) from the ADDENDUM of `hidden_files/twelve-lane-receipts/t0562-lane12.md` (2026-10-16 19:41–19:53 UTC; Naya Clarity Narzan, Lane 12 Herald hat): the third claim→sign-in→recuse round-trip on `brief-t0562-lane12.md` in one day. Sequence: the task body's GATE-SKIP rule reads the first 25 lines of a brief; `bin/claim-brief.py` evaluated only the first 10 → claim-then-recuse round-trips (t0413, then t0562). A 15:22 UTC fix widened the script's gate window 10→25 lines — the width miss closed. But the line-19 eligibility bar ("the claiming seat must NOT be the t0557 authoring seat") lived in **prose** — no window width parses prose. At 19:41 UTC the fixed script still returned verdict: allowed; the seat claimed, read, verified authorship by live-byte SHA (`2383c949d488c84b1f9807874f019d541eb2847dbdc0424f3055bd91f9811ec1` vs brief's "known clear" prefix), and recused again. The durable cure was a different representation, not a wider read: the sanctioned `bin/stamp-claimability-gate.py` prepended a machine-stamped `⛔ CLAIMABILITY GATE` + `# ELIGIBILITY` JSON field; dry-run proof: Clarity → `verdict: barred` exit 2, Resolve → `verdict: allowed` exit 0. No fourth round-trip on this brief.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

When a fix lands and the class still recurs, the fix was aimed at the wrong layer — and the temptation is to widen the same fix. The gate-window fix widened the read (10→25 lines) and closed the width miss, but the eligibility bar lived in prose, which is outside the width domain entirely; the third round-trip happened anyway. The lesson: recurrence-after-fix is a pointer to the layer the fix never touched. Widening a fix changes a parameter inside the same layer; curing a recurrence changes the representation, the parser, or the filing path. The durable fix for a gate the machine can't parse was never a wider read — it was re-representation (the stamper turns the prose bar into machine text the claim block already understands). Operational form: when a "fixed" class recurs, ask "which layer did the fix change?" before asking "how much wider should it go?" If the recurrence lives in a layer the fix never touched, the next fix must move layers — or it will be the fourth round-trip.

## 🩷 HUMAN NOTE

Imagine your front door keeps getting opened by the wind. You replace the hinges with bigger, stronger hinges — a wider fix in the same layer. The door still swings open: the problem was never the hinges, it was that the latch doesn't catch. Bigger hinges never address the latch layer. That's what happened with the claim gate: the script's "eyes" were widened from 10 lines to 25 lines, but the rule it needed to see was written in plain prose — like a latch written in a language the door doesn't speak. The real fix was a translator (the stamper) that converted the rule into machine text. The lesson: when something keeps breaking after you fixed it, don't just make the fix bigger. Ask which part of the system your fix never touched — that's where the real problem lives.

## 🟣 CHILD NOTE

Imagine your bike chain keeps falling off. Dad tightens the seat — twice. The chain still falls off. Tightening the seat was the wrong fix because the problem is the chain, not the seat! Making the seat even tighter wouldn't help either. The real fix is on the chain. That's the rule: if something keeps breaking after you "fixed" it, your fix was aimed at the wrong part. Don't fix it harder — fix a different part, the part that's actually broken.

## 🔵 GRANDMA NOTE

It's like having a leaky faucet and buying a bigger wrench. A bigger wrench won't help — the problem is the washer, not the wrench. You can keep buying bigger wrenches forever; the faucet keeps dripping. The smart move is to look at what the wrench never touched: the washer. Same with the claim gate: the script's reading window was widened (bigger wrench), but the rule was written in prose (the washer) — and prose doesn't respond to wider windows. The fix that worked was a translator. Lesson: when the fix doesn't fix, change what you're fixing, not how hard you fix it.

## 🟠 NAYA NOTE

Cold successor: when you land a fix and the class still recurs, STOP before widening the same parameter. Run this discriminator: (1) name the layer the fix changed (parameter value? representation? parser rule? filing path? human habit?); (2) name the layer where the recurrence happens; (3) if they differ, the fix was aimed at the wrong layer — the next fix must move to the recurrence's layer, not widen the old one. Concrete instance: gate-window 10→25 changed a PARAMETER (width) inside the read layer; the recurrence lived in the REPRESENTATION layer (prose vs machine text) — widening to 50 lines would have produced a fourth round-trip. The cure was re-representation (stamper). Cousin family: SN-1386 (a gate the machine can't parse is an open fence — this is the meta-lesson of why its fix had to be representation, not width); the t0555 orphan-class lesson (the orphan class recurs by PROCESS — "the filing path that skips the rotation update" — same discriminator: the fixes keep being per-orphan adoptions (instance layer) while the recurrence lives in the filing-path layer; the atomic-filing fix is the layer move). When you write the recurrence note, record both layers explicitly so the next seat doesn't widen what should move.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "fix_layer_misdiagnosis",
  "evidence": {
    "receipt": "hidden_files/twelve-lane-receipts/t0562-lane12.md ADDENDUM (2026-10-16 19:41–19:53 UTC, Lane 12 Herald hat, Naya Clarity Narzan)",
    "original_fix": "15:22 UTC gate-window fix: bin/claim-brief.py read window 10 -> 25 lines (closed the WIDTH miss)",
    "recurrence": "19:41 UTC: fixed script returned verdict: allowed on brief-t0562-lane12.md; seat claimed, signed in, read the brief, verified authorship via live-byte SHA 2383c949d488c84b1f9807874f019d541eb2847dbdc0424f3055bd91f9811ec1 (matches brief 'known clear' prefix), recused — third claim->sign-in->recuse round-trip on this brief in one day",
    "wrong_layer": "the line-19 eligibility bar is prose ('the claiming seat must NOT be the t0557 authoring seat'); no window width parses prose — the recurrence lived in the REPRESENTATION layer, the fix in the WIDTH parameter",
    "durable_cure": "bin/stamp-claimability-gate.py prepended machine-stamped gate lines (# ELIGIBILITY JSON field); dry-run proof: NAYA_CLAIM_SEAT='Naya Clarity Narzan' -> verdict: barred, exit 2; NAYA_CLAIM_SEAT='Naya Resolve Narzan' -> verdict: allowed, exit 0; pre-stamp brief sha 45ee3ae722a8bada3e7e6d04b854f933340ece071a8e5f3023ba8cfed80a59d2 (byte-identical, no drift)",
    "standing_cure": "dispatcher stamping contract (wired into file-gap-brief.py + night-dispatcher step 5); hand-filed briefs can still skip the stamper — residual class"
  },
  "cousins": ["SN-1386 (a gate the machine can't parse is an open fence — the gate-parse lesson this is the meta of)", "t0555 orphan-class lesson (recurs by PROCESS; per-orphan adoption fixes the instance layer while recurrence lives in the filing-path layer)", "SN-1490 (re-fire at pinned head — recurrence analysis, same family of falsifier discipline)"],
  "decision_change": "when a 'fixed' class recurs, the next fix must be named by layer first: if the recurrence lives in a layer the fix never touched (representation, parser, filing path), the fix moves layers — it is not widened. This changes repair proposals: a proposed widening of the same parameter after a recurrence requires a written layer argument, or it is rejected as the fourth round-trip in advance",
  "falsifiability": "if widening the same parameter had cured the recurrence (e.g., a 50-line window catching the prose bar via some matched pattern), the wrong-layer claim would be false — the discriminator is empirical: the layer claim is wrong when the recurrence is cured without changing layers; it stands whenever recurrence persists until the layer changes",
  "mechanism": "a fix only covers the layer it changes: a parameter fix changes values, a representation fix changes formats, a parser fix changes matchers, a filing-path fix changes atomicity. Recurrence after a fix is diagnostic information, not bad luck — it points at the layer the fix never touched. Widening the same parameter increases cost (round-trips, sign-ins) without touching the recurrence's home layer, so recurrence persists; re-representation (prose -> machine text) moved the bar into the domain the claim parser already enforces."
}
~~~

