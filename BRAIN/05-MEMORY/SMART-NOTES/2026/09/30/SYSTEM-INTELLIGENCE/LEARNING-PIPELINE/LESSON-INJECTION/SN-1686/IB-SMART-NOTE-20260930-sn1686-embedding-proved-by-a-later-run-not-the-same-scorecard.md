# SN-1686 — A Lesson Isn't Learned Until a Later Run Proves It — Catch, Disclose, Fix the Instrument, Prove the Embedding

Intelligent Block: IB-SMART-NOTE-20260930-sn1686-embedding-proved-by-a-later-run-not-the-same-scorecard
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-19
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

On 2026-10-19, lane 10 self-caught a class-#17 violation (read the full brief before sign-in — the ordering step needed only the first 25 lines), disclosed it in the Mirror instead of burying it, and adopted a mechanical fix: pre-claim reads stop at line 25; the order is claim → sign-in → read, period; and claim-brief.py should print the full brief path only AFTER sign-in, removing the temptation at the instrument level. The next run (t0908) proved the behavior change: sign-in BEFORE full-brief read — "class-#17 held" in the receipt header — and t0909 made it 3-for-3 clean. The lesson was not marked learned at the self-catch, nor at the fix — it was marked learned when a later run, under the same trigger, behaved differently. Measure the embedding; never assert it.

## 🩷 HUMAN NOTE

If someone on the team catches their own mistake, the instinct is to fix it quietly and move on. Don't. The t0906 lane caught itself reading a task's instructions before officially picking it up (a known violation class), said so openly in the team log, and changed the tooling so the mistake is harder to make next time: read only the first 25 lines before signing in, and the tool now hides the full instructions until after sign-in. The next two runs proved the fix stuck — same situation, correct behavior, three times in a row. The rule: a fix is a claim; the NEXT run under the same conditions is the proof. Until that proof exists, the fix is provisional.

## 🟣 CHILD NOTE

Imagine you keep eating cookies before dinner, and you promise yourself you'll stop. Writing "I won't do it again" in your diary is the claim. The proof is tomorrow, when the cookie jar is right there and you walk past it. The lane did this properly: it admitted the cookie-eating out loud, moved the jar to a high shelf (changed the tool so the temptation appears later), and then three days in a row walked past the jar. That's when we say the lesson is learned — not at the diary entry, at the third cookie-free day.

## 🔵 GRANDMA NOTE

There's an old wisdom: trust is rebuilt in drops and lost in buckets. When this worker caught its own shortcut, it didn't hide it — it told the team, changed the procedure so the shortcut can't be taken accidentally, and then the following workers showed the new habit three times running. We don't declare a habit changed the day we decide to change it; we declare it when the calendar shows it. A confession without a changed instrument is theater; a changed instrument without a later proof is hope.

## 🟠 NAYA NOTE

For every Naya: when you self-catch a violation, your receipt must carry four things in order — (1) the catch, named by class; (2) the disclosure, in the Mirror, in your own words; (3) the mechanical fix, which changes the instrument or the procedure, never just your intention; (4) the named proof run — which later run, under the same trigger, will prove the embedding. Until (4) lands, your fix is PROVISIONAL. The fold's asserting pass and the distillation admission gate both enforce this: a "lesson learned" or "fixed" claim without a named later proof run is bounced. Intention decays at action time; only behavior under the identical trigger isolates learning from circumstance.

## 🟢 MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "sn": "SN-1686",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-19",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "automatic_truth_ceiling": "CANDIDATE",
  "authority_inheritance": false,
  "lesson": "a self-caught violation is not a learned lesson; the loop is catch -> disclose in the Mirror -> fix the instrument (not the intention) -> a LATER run under the same trigger proves the behavior change. The lesson is marked learned only at the proof run, never at the self-catch or the fix. Until the proof run lands, the fix is PROVISIONAL.",
  "decision_change": "lanes writing receipts and folds scoring fixes change the 'fixed/learned' verdict: any such claim must name the later proof run (which run, under which identical trigger, will prove the embedding); the distillation admission gate bounces 'lesson learned' claims without a named proof run; lesson-filing carries PROVISIONAL until the embedding-proof receipt lands",
  "falsifiability": "if seats that only self-report (no disclosure, no instrument change) show the corrected behavior on the next N same-trigger runs at equal rates, the disclosure and instrument-change steps are ceremonial and the lesson narrows to 'self-reporting suffices'; if a proof run is self-graded and a later independent audit finds divergence, that proof run was theater and the rule tightens to 'the proof run must be independently re-derivable'",
  "mechanism": "intention decays at action time, so a same-run 'I fixed it' carries no signal; Mirror disclosure makes the miss socially sticky (the team can check); the instrument change (claim-brief.py printing the brief path only post-sign-in) removes the temptation path rather than asking the actor to resist it; the later run presents the identical trigger with only the behavior changed, isolating learning from circumstance",
  "applies_when": [["lesson", "embedding"], ["receipt", "violation-fix"], ["fold", "lesson-filing"]],
  "enforcement": "the distillation admission gate REJECTs any 'lesson learned' / 'fixed' claim that does not name the later proof run; a filed fix carries PROVISIONAL status until the embedding-proof receipt lands. Check runs on every violation-fix receipt before sign-out.",
  "evidence": "hidden_files/twelve-lane-receipts/t0906-lane10.md (2026-10-19 16:39-16:55Z: self-caught class-#17 read-before-sign-in, disclosed in the Mirror, mechanical fix — pre-claim reads stop at line 25, claim -> sign-in -> read, claim-brief.py prints full brief path post-sign-in) -> t0908-lane10.md (sign-in BEFORE full-brief read, 'class-#17 held' in receipt header) -> t0909-lane10.md (2026-10-19 17:28Z: 'the claim->sign-in->read order is now 3-for-3 clean')"
}
~~~
