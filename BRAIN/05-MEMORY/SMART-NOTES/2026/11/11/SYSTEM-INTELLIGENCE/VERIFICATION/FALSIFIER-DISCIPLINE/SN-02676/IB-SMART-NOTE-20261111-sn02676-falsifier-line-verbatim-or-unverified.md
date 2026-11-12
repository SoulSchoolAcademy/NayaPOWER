**Intelligent Block:** IB-SMART-NOTE-20261111-sn02676-falsifier-line-verbatim-or-unverified
**Smart Note:** SN-2676
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-11
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Staged by the smart-note distillation loop 2026-11-11 21:38 PST. Evidence: receipt hidden_files/twelve-lane-receipts/gap-gap-lane-scorer-20261018-1610-lane12.md (Lane 12, 9.4/10 after three passes, filed 2026-11-12T05:17Z) + lane-agent-brief-template.md PART 2 (verified first-hand, sha c1508de2) + /tmp/lane12-gap/run1.log and run2.log (byte-identical). Pre-number check: counter last line 2675; learn/lessons.md max SN-2675 ingested; no SN-2676/2677/2678 in lessons.md or ingestion-log.md; open PRs checked via App route (2 open, none Smart Note); #1354 capped at 2500 comments-disabled, no GitHub comment fetch per cheap check; branch claim check by stage_smart_note.py.

## ✦ IN A NUTSHELL

A 2026-10-18 receipt wrote "F6 fired" next to byte-identical cold files — the check had exercised, not fired. The loose wording cost a scorer follow-up and a full re-run cycle. The fix is now structural: the FALSIFIER REPORTING CONVENTION lives in lane-agent-brief-template.md PART 2 (folded 2026-11-11, template sha 9bfaeb9f → c1508de2): when you report any falsifier, quote its own printed line verbatim — verdict word + detail — and name the runner file, line number, and firing condition. "FIRES" means the condition evaluated true; "clear" means it did not; "exercised" / "ran" / "checked" never mean "fired". Two consecutive re-runs of the exact parent command report F6 per the convention — verbatim `F6: clear (byte-identical=True)` — logs byte-identical, cold shas matching the parent's 2365ff4e, no baseline drift in 24 days. A falsifier claim without its printed line + condition is an unverified claim. Wording is data: test it like a claim.

## 🩷 HUMAN NOTE

Shawn — a seat once wrote that a safety check "fired" when the check had actually run and reported everything fine. That one word cost a scorer a follow-up and a whole lane a re-run, because nobody could tell from the report what the check really said. The rule now, written into the template every seat reads: quote the check's own printed line, word for word, plus where it lives and when it fires — or the claim doesn't count. The first two re-runs under the new rule already report the line exactly as printed.

## 🟣 CHILD NOTE

Imagine your teacher asks if the smoke alarm went off, and you say "it fired!" — but really the alarm just did its quiet test beep and said "all clear." Now everyone runs around looking for a fire that isn't there. The new rule is simple: when you talk about the alarm, you have to repeat exactly what it printed on its little screen, and say where the alarm is and what makes it go off. If you can't repeat its words, you don't get to say it fired.

## 🔵 GRANDMA NOTE

Dear, we had a mix-up where someone wrote that a check had "fired" — gone off — when it had only run its test and reported all clear. That one word sent people off on a whole extra round of checking for a problem that wasn't there. So the rule now is plain: when you report what a check said, you quote its own words exactly, and you say which check it was and what would make it go off. A claim without the check's own words is just hearsay, and we don't file hearsay.

## 🟠 NAYA NOTE

The verified facts: (1) Root case, quoted in the template: a 2026-10-18 receipt wrote "(F6 non-determinism check fired on the subprocess path)" next to byte-identical cold files — the check had exercised, not fired; the wording cost a scorer follow-up and a re-run. (2) The convention was folded into hidden_files/lane-agent-brief-template.md PART 2 on 2026-11-11 (gap-gap-lane-scorer-20261018-1610-lane12, Lane 12, 9.4/10): quote the falsifier's own printed line verbatim (verdict word + detail) plus runner file, line number, and firing condition; a falsifier claim without its printed line + condition is an unverified claim; "FIRES" means the condition evaluated true, "clear" means it did not, "exercised/ran/checked" never mean "fired". F6 (pilot-12 battery, hidden_files/run_pilot12_battery.py L201) fires ONLY on non-identical cold runs (b1 != b2); on identical runs the runner prints `F6: clear (byte-identical=True)` — report that line verbatim, never paraphrase it as "F6 fired". (3) Recurrence test, same receipt: two consecutive re-runs of the exact parent command (full --arm semantic-t0426), both exit 0, both print verbatim `F6: clear (byte-identical=True)`; the two logs are BYTE-IDENTICAL; all four cold-rank shas match the parent's 2365ff4e (no baseline drift in 24 days); sealed verdict untouched. Template sha before 9bfaeb9f, after c1508de2 — verified first-hand this tick, convention present at line 77. (4) Honest scope: prevention proof so far is one re-run pair + the template rule, not yet a future seat's filing under the new convention — this receipt is the first live use, not the proof of adoption; single-seat. (5) This is the reporting sibling of SN-2677 (pin the instrument before every re-run) — same receipt, different rule: 2677 governs the instrument, this note governs the words used to report what the instrument said.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-2676",
  "slug": "falsifier-line-verbatim-or-unverified",
  "title": "A falsifier report quotes its printed line verbatim or it is unverified: 'fired' means the condition evaluated true, 'clear' means it did not",
  "observation": false,
  "applies_when": [["falsifier", "report"], ["receipt", "verdict-word"], ["battery", "re-run"]],
  "enforcement": "A falsifier claim in a receipt that lacks the falsifier's printed line verbatim plus runner file, line number, and firing condition is bounced as an unverified claim; a receipt writing 'fired' for a check whose printed line says 'clear' fails the convention check. The lane brief template PART 2 carries the convention; the check is the scorer or reader re-reading the quoted line against the runner's firing condition.",
  "evidence": "Receipt hidden_files/twelve-lane-receipts/gap-gap-lane-scorer-20261018-1610-lane12.md (Lane 12, 9.4/10, filed 2026-11-12T05:17Z): convention folded into lane-agent-brief-template.md PART 2 (template sha 9bfaeb9f -> c1508de2, verified first-hand, line 77); two consecutive re-runs of the parent command (full --arm semantic-t0426), both exit 0, both print verbatim 'F6: clear (byte-identical=True)'; logs byte-identical; cold shas match the parent's 2365ff4e; runner hidden_files/run_pilot12_battery.py L201 fires ONLY on non-identical cold runs. Root case: a 2026-10-18 receipt wrote 'F6 fired' next to byte-identical cold files.",
  "decision_change": "Every future falsifier report must carry the falsifier's printed line verbatim plus file, line, and firing condition, or it is treated as unverified; scorers stop spending follow-up cycles on paraphrased verdict words like 'fired' for a check that printed 'clear'.",
  "falsifier": "If a receipt quotes the printed line verbatim plus condition and a scorer still has to spend a follow-up re-run to settle what the falsifier said, the convention does not close the recurrence path; if a later receipt still writes 'fired' for byte-identical 'clear' while the template rule stands, the template enforcement has failed.",
  "cousins": ["SN-0648 (preserve the deliberately RED falsifier — falsifiers are first-class evidence, never merged as repairs)", "SN-0586 (verify the instrument, not the receipt)", "SN-2677 (pin the instrument before every re-run — same receipt, sibling rule: this note governs the report wording, 2677 governs the instrument)"],
  "captured": "2026-11-11",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "intent": "CAPTURE_DURABLE_INTELLIGENCE"
}
```
