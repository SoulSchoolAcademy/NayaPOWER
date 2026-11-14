# A Caveat That Lives Only in Prose Is a Caveat Waiting to Be Dropped — Put the Caveat in the Instrument That Emits the Number

**Intelligent Block:** IB-SMART-NOTE-20260930-sn02797-caveat-lives-in-the-emitter
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-14
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** gap-lane-scorer-20261114-0120-lane11.md (9.5/10, 01:30–01:35 PST); CANDIDATE 1052 in CORE-PRINCIPLES.md; LEARNING event in learning-events-2026-11-14-02.md (hourly review 02:20 PST).

## ✦ IN A NUTSHELL

`hv_measure.py` line 413 printed `HV1 tasks completed WITHOUT rework: 0/10 = 0.0%` with no "ceiling" anywhere in the file — while every prose quote of HV1 0/10 already carried the ceiling caveat: all 10 Lane-11 receipts, STATS.md, the instrument doc, the journal — 10/10 discipline, and still the one place that actually emits the number dropped it. The caveat lived only in quoters' prose, so it was one careless quote away from vanishing everywhere. The fix landed at the source (the definition and the print now carry CEILING), proven computation-neutral by a pre/post diff-walk (exactly one difference, the definition string; M2/M3/M4 reproduce 8/2/3 on both windows). The rule: when a number needs a caveat every time it is quoted, the caveat goes into the instrument that emits the number — never into quoters' discipline. Prose discipline depends on every quoter remembering, every time; the emitter depends on nobody remembering anything.

## 🩷 HUMAN NOTE

Shawn — the machine that prints our headline number had a warning attached to it ("this 0/10 is a ceiling, not a failure"), and every person who quoted the number remembered to say the warning — ten out of ten times, perfectly. But the machine itself didn't say it: it just printed the bare number. Sooner or later someone copies the machine's output instead of a person's quote, and the warning is gone. The fix was simple: teach the machine to print the warning with the number, every time, so no human has to remember. Whenever a number always needs a warning, put the warning where the number is born — not in the people repeating it.

## 🟣 CHILD NOTE

Imagine a scoreboard that shows "0 points" but the real story is "the game only let you score 0 points at most." Every kid who tells the score remembers to add "but that's the most anyone could get!" — all ten kids, every time. But the scoreboard itself just says "0 points." One day a new kid reads only the scoreboard and thinks the team failed. The fix: write the little note right on the scoreboard, next to the number, so nobody has to remember to say it. If something always needs explaining, write the explanation where the number lives.

## 🔵 GRANDMA NOTE

Dear, it's like a medicine bottle whose label says the dose, but the warning — "take with food" — is only in the letter the doctor wrote, not on the bottle. Every nurse who hands it over remembers to say it, ten out of ten. But the bottle itself stays silent, and one day someone reads only the bottle. The lesson, love: the warning belongs on the bottle, not in the letters about the bottle. Anything that must be said every time a number is said must be printed where the number is printed.

## 🟠 NAYA NOTE

Source: gap-lane-scorer-20261114-0120-lane11.md (9.5/10), 2026-11-14 01:30–01:35 PST; CANDIDATE 1052 in CORE-PRINCIPLES.md; LEARNING event in learning-events-2026-11-14-02.md. The HV1 ceiling caveat was carried in prose with 10/10 discipline across all 10 Lane-11 receipts, STATS.md, the instrument doc, and the journal — yet `hv_measure.py` line 413 printed the bare `HV1 tasks completed WITHOUT rework: 0/10 = 0.0%` with no "ceiling" anywhere in the file. The same run's F5 is the same lesson in miniature at edit time: a multi-line safe-edit broke on shell quoting, was caught on read-back, restored byte-identical, and re-applied via file payloads — the safe path is the one the tool enforces, not the one the seat remembers (edit-discipline family, SN-2692). What this note does NOT re-teach: naming an instrument's blindness (SN-1894 — what the instrument cannot see) or the check-name-is-not-a-suite rule (SN-2795 — what a check label does not prove). Those name what is missing from a measurement; this one names WHERE a known caveat must live — in the emitter, not in the quoters. Cousin: SN-1894.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "rule": "caveat_lives_in_the_emitter",
  "mechanism": "a caveat carried only in quoters' prose depends on every quoter remembering it on every quote; the emitter is the single source every quote descends from, so a caveat embedded in the emitting instrument's definition and print strings is inherited by every consumer automatically and can never be dropped by a careless quote",
  "evidence": "gap-lane-scorer-20261114-0120-lane11.md (9.5/10, 2026-11-14 01:30-01:35 PST): hv_measure.py line 413 printed 'HV1 tasks completed WITHOUT rework: 0/10 = 0.0%' with no 'ceiling' anywhere in the file, while all 10 Lane-11 receipts, STATS.md, the instrument doc, and the journal carried the ceiling caveat (10/10 prose discipline); fix landed at the source (definition + print now carry CEILING), proven computation-neutral by pre/post diff-walk (exactly one difference, the definition string; M2/M3/M4 reproduce 8/2/3 on both windows); all 10 t1162 audit rows CONFIRMED by a second seat",
  "falsifiability": "if a caveat embedded in the emitter is still dropped in quotes (consumers strip or paraphrase it away), the mechanism fails and the lesson weakens; if quoters carry a prose-only caveat reliably across many quotes with zero drops, the emitter rule is unnecessary",
  "decision_change": "a future seat adding a caveat to a metric puts it in the emitting instrument's definition and print strings first; prose quotes inherit it, and no seat relies on quoter discipline to carry it",
  "applies_when": ["instrument", "metric-emission", "caveat"],
  "enforcement": "the lane-scorer receipt audit: when a receipt quotes a metric, the scorer greps the emitting instrument's definition and print strings for the caveat text; a metric whose emitter does not carry its caveat fails the receipt's evidence check, and the fix lands in the emitter, not in the prose",
  "related": ["SN-1894 name the instrument's blindness", "SN-2795 a check name is not a suite"]
}
~~~
