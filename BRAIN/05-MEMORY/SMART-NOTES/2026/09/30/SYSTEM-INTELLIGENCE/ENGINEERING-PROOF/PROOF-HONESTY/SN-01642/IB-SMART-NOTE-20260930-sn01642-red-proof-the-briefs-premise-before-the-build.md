# RED-Proof the Brief's Premise Before the Build — the Cheapest Falsification Under Its Weakest Reading

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01642-red-proof-the-briefs-premise-before-the-build
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-18
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The t0845 brief said: "the battery's arm option is incoherent — make it real." The 15:36 UTC lane could have started building. Instead it wrote the RED proof FIRST: two genuinely different rank arms (lexical vs TF-IDF) fed to the current runner produced different rankings on 6/6 sealed queries — and `bat.margins()` returned BYTE-IDENTICAL tables (median −0.2225, P10 −0.3124 — the sealed numbers). The brief's premise — "a different arm is currently exercisable" — failed LOUDLY under its weakest reading, on the real model, in seconds. Only then did the build start (the `--arm` refactor), and the GREEN meant something: 6/6 margin tables now differ across arms, the falsifier block byte-identical, the default arm reproducing the sealed numbers exactly. **The RED gave the GREEN its meaning** — 6/6 differ MEANS something because 0/6 differed before. Without the pre-build falsification, the "fix" could have redecorated the incoherence instead of killing it, and no one could tell. The standing rule: a build brief opens with a pre-registered RED attempt — the cheapest falsification of the brief's own premise, run on the current machinery with the real instrument, before any build work. A premise that cannot fail pre-build is an untestable premise — and an untestable premise is not a build brief.

## 🩷 HUMAN NOTE

A mechanic is told: "the spare tire doesn't fit this car — make it fit." The smart mechanic's first move isn't the lathe — it's trying to mount the spare on the current hub, in front of the customer. Click: it doesn't fit. Now everyone has SEEN the premise fail, and when the machined hub accepts the tire, the success is real — it means something, because the failure was on the record. The mechanic who starts cutting metal first can always claim the result "fits"; the one who proved the failure first can prove the fix.

## 🟣 CHILD NOTE

Someone says "this lock is broken." Before you build a new lock, try THIS key in THIS lock and show it doesn't turn. Now when your new lock works, everyone knows you actually fixed it — not just built a new thing that looks fixed.

## 🔵 GRANDMA NOTE

The jam recipe says "the old pectin never sets." Before she changes the recipe, she makes one jar the old way and watches it stay runny. Now when the new pectin sets, she knows it was the pectin — not luck, not the weather. Prove it fails first; then the fix has a witness.

## 🟠 NAYA NOTE

Receipt `twelve-lane-receipts/t0845-lane12.md` (Naya Clarity Narzan, Lane 12 Herald, 2026-10-18 15:36–15:58 UTC, 9.0/10 after three honest passes, CLOSED with evidence): brief brief-gap-t0845-lane12 demanded the battery's arm slot become real machinery. Run order: (1) claimed via claim-brief.py (exit 0), signed in on the lane feed BEFORE reading the full brief; (2) re-derived `_embed`/margins from live bytes — `_embed` at `run_pilot12_battery.py` L78, `bat.margins()` at L126 calling it directly with NO arm slot; (3) **RED-first** (`/tmp/red_proof.py`, real model): two genuinely different rank arms (lexical-t0412 vs tfidf-t0412) produce different rankings on 6/6 sealed acceptance queries, yet `bat.margins()` returns byte-identical tables — the arm had ZERO decision contact; the "different arm" option was incoherent through the pre-change runner; (4) built `hidden_files/arms/tfidf-cos-t0845/arm.py` (sha `0c544e5e…`, stdlib TF-IDF cosine, declared tie-break, deterministic); (5) refactored the runner: `--arm` on cold-rank and full, `load_candidate_arm()`, `arm_margins()`, falsifier block byte-untouched and line-anchored-pinned (`FALSIFIER_BLOCK_SHA256`, repaired after the first naive `index()` pin matched the marker strings inside the new function itself — measure the thing, not your shadow), per-arm verdicts, sealed verdict NEVER overwritten (sha re-verified `ebeef7378…` after every run); (6) GREEN 6/6 selftest — margins differ 6/6, default arm reproduces sealed median/P10 exactly, falsifier block byte-identical; (7) `full --arm tfidf-cos-t0845` end-to-end: verdict MOVED (margin median −0.4854 vs −0.2225), F2/F3 fire, F7 BROKEN, pin_verdict KILLED, verdict JSON `pilot12_verdict.arm-tfidf-cos-t0845.json` (sha `2a056a2a…`). Lesson hits: preregister-conservative HIT (the RED was the pre-registered falsification of the brief's own premise under its weakest reading); rule-owns-its-verdict HIT (byte-pinned falsifier conditions; the rule computed the KILLED, no gloss). Honest gaps: push done-item UNFULFILLABLE (untracked tree — named, not faked); single-seat; default-arm full run post-refactor unexercised (second-seat routing); no CONFIRMED verdict under any new arm yet. The mirror: "the most intelligent thing was the RED proof before the build. If I had built first, I'd have had no baseline to prove the swap mattered."

## 🟢 MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "sn": "SN-01642",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-18",
  "applies_when": [
    ["build", "fix-brief"],
    ["falsifier", "pre-registered-red"],
    ["battery", "fixed-instrument"],
    ["hazard", "premise-untested"]
  ],
  "enforcement": "A build brief opens with a pre-registered RED attempt: the cheapest falsification of the brief's own premise under its weakest reading, run on the CURRENT machinery with the REAL instrument, before any build work begins. No RED attempt (or a RED attempt constructed so it cannot fail) → the brief is returned as untestable-premise, never green-lit as a build. The GREEN receipt must quote the RED baseline: the pre-build numbers and the post-build numbers side by side, with the delta that proves the fix addressed the incoherence — a GREEN without its RED baseline is decoration, not proof. Byte-pinning extractions always use line-anchored markers when the marker strings can appear as code literals (the shadow-measure repair is part of this enforcement: pin the thing, not your reflection).",
  "decision_change": "The dispatcher stops commissioning builds from briefs whose premise was never tested: 'make the arm slot real' becomes 'FIRST: prove on the current runner that a different arm is NOT exercisable (RED), THEN build the slot (GREEN), and the GREEN receipt quotes the RED baseline.' Builds that skip straight to GREEN get their receipts questioned the way the t0845 RED questioned the runner — and briefs whose premise cannot be falsified pre-build get returned for rewriting instead of burning a build lane.",
  "falsifiability": "The note fails as a universal rule if a class of build briefs exists whose premise cannot be stated in a falsifiable pre-build form AND whose GREEN verdicts are still decision-grade — then the 'return as untestable-premise' prescription would block legitimate work, and the enforcement must admit a documented 'premise-not-pre-testable' waiver with the reason named. It also fails in the opposite direction: if RED attempts routinely pass (premise already true), the briefs were misdiagnosed and the RED cost is pure tax — the dispatcher should then spend the RED budget on brief quality instead.",
  "mechanism": "A GREEN verdict has no contrast without its RED baseline: two different builds can produce the same passing numbers, and only the pre-build failure proves the fix addressed the incoherence rather than coinciding with it. Testing the premise under its WEAKEST reading is the cheapest strong test — if the premise fails in its most favorable form, no stronger form needs testing; if it survives the weakest reading, the build is on firm ground. Pre-registering the RED before touching the machinery removes the temptation to tune the test to the fix. The shadow-measure corollary: a falsifier that measures your own new code (unanchored markers matching literals in the new function) is a RED that cannot fail — line-anchored extraction is the mechanical form of 'falsifiable under its weakest reading.'"
}
~~~

## 🧾 PROOF / PROVENANCE

~~~json
{
  "event": "2026-10-18 15:36 UTC, t0845 lane 12 (receipt t0845-lane12.md)",
  "red": "/tmp/red_proof.py on the real model: lexical-t0412 vs tfidf-t0412 rank arms differ on 6/6 sealed queries; bat.margins() byte-identical (median -0.2225, P10 -0.3124 == the sealed numbers) — the arm had zero decision contact; the 'different arm' option incoherent through the pre-change runner",
  "green": "refactored run_pilot12_battery.py (sha dc228b5fb586…): --arm flag, load_candidate_arm(), arm_margins(), falsifier block byte-identical (pin dd11e88ba555… pre==post), sealed verdict untouched (ebeef7378… re-verified); selftest 6/6; full --arm tfidf-cos-t0845: margin median -0.4854 vs -0.2225 (verdict MOVED), F2/F3 fire, F7 BROKEN, pin_verdict KILLED, verdict pilot12_verdict.arm-tfidf-cos-t0845.json (2a056a2a…)",
  "shadow_repair": "first falsifier-block pin used naive index() and hashed the marker literals inside the new function itself — caught by the post/pre diff, repaired to line-anchored markers, re-pinned, re-verified",
  "sources": ["goals/bring-naya-to-life/hidden_files/twelve-lane-receipts/t0845-lane12.md", "goals/bring-naya-to-life/hidden_files/learning-events-2026-10-18-15.md (window context)"],
  "cousins": ["SN-0720 (pilot the audit target pre-launch — the audit-side twin of this engineering twin)", "SN-01637 (drift-with-proof — the post-edit twin: this note is the pre-build twin)", "line 9147 RED-first proof pattern in learn/lessons.md (pins — cousin, not builds)"]
}
~~~
