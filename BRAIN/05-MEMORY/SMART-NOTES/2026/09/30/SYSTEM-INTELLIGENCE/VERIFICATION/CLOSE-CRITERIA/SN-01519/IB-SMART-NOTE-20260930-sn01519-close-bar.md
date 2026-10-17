# SN-1519 — "Closed" Means Two Clean Tick Cycles, Not One Revert Plus One Green — The #2601 Premature-Closure Correction

Intelligent Block: SN-1519
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-16 (18:08 PDT distillation tick)
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

The "fight over" claim about #2601's master-directive overwrite war was premature and was publicly corrected the same day. The standing bar set with Shawn: "closed" = **two full tick cycles with no overwrite**. One revert plus one clean read is a quiet interval, not closure — after the x57 revert at 23:56Z and the main-seat adjudication, the ticker fired once more (x57). The bar that closed it held this time: the fix (two re.sub blocks removed from the flip script) survived, the detector re-armed, and the re-armed detector correctly flagged a *legitimate* flip-script update as its first post-fix event — proof the close bar is live, not ornamental.

## HUMAN NOTE

What happened: the seat reported "the fight is over" after reverting the 53rd foreign overwrite. It was wrong — the ticker fired again (x57). What the correction established: never say "closed with proof" off a single passing observation. The new rule, set with Shawn himself: two full tick cycles with zero overwrites before the word "closed" is used. Reverts don't count as cycles; only un-triggered detection does. The bar works: the same ticker that caught x57 later caught the legitimate 00:58:56Z flip-script update (single-writer line intact, fix holding) — a detector that stayed silent on purpose but still fires on everything is exactly what "closed" needs to mean.

## CHILD NOTE

Imagine you cleaned up a mess on the kitchen floor and declared the kitchen "clean forever." But your brother walked through with muddy shoes one more time. You didn't get to say "clean forever" — you got to say "clean right now, watching." The new rule: you only get to say "clean forever" after two full days where nobody walks through with muddy shoes. And the mop-and-bucket alarm still works, because it went off when your brother came in with CLEAN shoes too.

## GRANDMA NOTE

You can't call a fight over just because it's quiet for a minute. You call it over after you've watched it stay quiet for a proper while — and after you've made sure your own alarm still rings. Then you trust the quiet.

## NAYA NOTE

This note is the twin of SN-1512 (falsification citation discipline) and the adjudication sibling of SN-1520 ("the intruder was us"): closure claims are falsification events, not mood statements. A closure claim without a stated falsification window is a reservation about the future dressed as a fact about the past. Two cycles is cheap; a second premature claim costs the trust the first one bought. Note the honest asymmetry: the window must be *detector-verified* silence — not "I didn't see anything," but "the detector that caught x57 ran and reported nothing." The 00:58:56Z legitimate-update flag is the falsifier-in-practice: the detector fires on everything, so its silence on the protected line is evidence, not absence.

## MACHINE NOTE

```json
{
  "sn": "SN-1519",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured_utc": "2026-10-17T01:08:00Z",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "VERIFICATION",
  "sub": "CLOSE-CRITERIA",
  "lesson": "Never say 'closed with proof' off a single passing observation. The standing bar (set with Shawn): 'closed' = two full tick cycles with zero overwrites on the detector that was catching the incident. One revert plus one clean read is a quiet interval, not closure. Reverts don't count as cycles; only detector-verified silence does.",
  "decision_change": "Future closure claims carry an explicit falsification window: name the detector, the window length, and what counts as a cycle. Reviewers ask 'how many clean cycles?' before honoring the word 'closed.' A premature closure claim is corrected on the record the same day, publicly, with the new bar named.",
  "falsifiability": "An overwrite landing inside the two-cycle window falsifies the claim — that is the window working as designed (it did exactly this at x57). If the detector stays silent for two cycles and an overwrite appears in cycle 3, the bar is refuted as too short and lengthens. The detector firing on a *legitimate* update (00:58:56Z flip-script update, single-writer line intact) proves the detector is live during the window, so silence is evidence, not a dead detector.",
  "mechanism": "A single clean observation cannot separate 'resolved' from 'quiet interval' — both look identical at the moment. The separation comes from sustained non-triggering of the same mechanism that caught the incident: the ticker-as-detector over two cycles converts silence from an absence of data into a measurement of the line it protects. Reverts are interventions, not observations, so they can't be cycles — counting them would let the fixer grade their own homework.",
  "evidence": [
    "main-seat adjudication comment 6226954814 (2026-10-16 23:56Z) — x57 overwrite; the seat's 'closed with proof' claim retracted in the director-pass correction 2026-10-16 ~18:00 PDT; new bar: 'closed' = two full tick cycles with no overwrite",
    "director-pass master-directive-pushed.json re-baseline (38h stale -> verified-canonical 10878cff…); master_directive.py drift-detection surgery re-armed; 00:58:56Z legitimate flip-script update correctly flagged (single-writer line intact, fix holding) — detector live post-fix"
  ],
  "cousins": ["SN-1512 / CANDIDATE 510 (a falsification credit must cite a falsification — closure claims are falsification events)", "SN-1520 (the intruder was us — the same incident's root-cause twin)", "SN-1500 (a falsifier quoted in a receipt is unholdable — quote the falsifier, not the mood)"],
  "dedupe_guard": "Not a duplicate: SN-1512 covers falsification citation discipline (what counts as a falsification); SN-1500 covers shipping re-runnable falsifiers in receipts; SN-1517 covers experimental pre-registration. This note covers closure-bar design for incident adjudication (two-cycle detector-verified silence) — none of the cousins address when the word 'closed' may be used.",
  "applies_when": ["closure", "detector", "claim", "incident"],
  "enforcement": "The word 'closed' requires two full tick cycles with zero detections by the mechanism that was catching the incident; reverts never count as cycles. A closure claim lacking the detector name + window length + cycle definition is bounced as an unclosed claim."
}
```
