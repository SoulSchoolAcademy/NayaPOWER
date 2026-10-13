# Falsifier Suites Must Probe the Time Dimension, Not Just Shape

**Intelligent Block:** IB-SMART-NOTE-20261009-sn0820-falsifier-time-dimension
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-09
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Filed by:** distillation loop, #1354 comment 6088748791 (2026-10-09).
**Provenance:** #1354 6088748791 ([NAYA 5 — REPAIR: delegated-merge receipt gate], 2026-10-09T20:30:37Z — LESSON section: "A gate that checks only parseability of a timestamp has a time hole. The 20-test suite never varied time — that's the pattern to watch"); #1354 6088678545 (original validator finding); related: SN-0518 (law operative only if machine can falsify), SN-0531 (falsifiability battery), SN-0603 (falsifier must fire).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The delegated-merge receipt gate's C4 condition ("team consensus, no seat objects") read `consensus.window_closed_at` and checked it only for *parseability*: a receipt with the objection window closing in 2099 returned ALLOW. An authority gate that authorizes a merge while the objection window is still open in the future contradicts its own condition 4 — objections cannot exist yet if the window hasn't closed, so "no objections" is unprovable. The gate shipped with a 20-test falsifier suite, all green — and the suite never once varied time. The fix required `window_closed_at <= now(UTC)` (a future timestamp denies as "objection window still open"), and the new test probes the time dimension twice: the validator's far-future literal `2099-12-31T23:59:59Z` AND a `now()+1h` window — proving it is a real time check, not a 2099 special case; `now()-1s` allows, boundary at `<=`. The durable addition to the falsifier family (SN-0518/SN-0531/SN-0603, which covered shape, firing, and pre-declared falsifiers): **a falsifier suite must vary every dimension the gate reasons over.** Timestamps demand time-probes (far future, near future, boundary ±1s, naive-vs-tz, malformed, epoch-int, missing); a suite that only probes shapes (bools, blanks, unicode, case) leaves a time hole shaped exactly like its own blind spot. The same lesson generalizes: for any condition with a threshold, the battery must straddle the threshold, not just poke the field's edges. The re-validator's 14 time probes (boundary both sides, offsets ±14:00/−05:00, naive future assumed UTC denies, malformed/empty/epoch-int/None/missing all deny fail-closed) are the template. Every green suite is evidence only over the dimensions it varied — a 20/20 green that never touched time proved nothing about time.

## 🩷 HUMAN NOTE

Shawn — today's permission-lock repair surfaced a testing lesson worth banking: the lock's 20-test test suite was all green, but it never tested *time*. It checked that a deadline was written in a valid date format — not whether the deadline had passed. So a deadline in the year 2099 (meaning "team members can still object") was read as "deadline reached, everyone's had their say" and the lock opened. The fix was tiny: the lock now compares the deadline to the actual current time. The lesson: every test suite only proves what it actually tested — if your test never changes the clock, it proves nothing about dates. For any check involving time, test the past, the future, and the exact boundary.

## 👶 CHILD NOTE

Imagine a rule that says "you can't have dessert until dinner time is over." Now imagine the rule-checker only looks to see if "dinner time" is written down somewhere — it doesn't check what time it actually is! If someone writes "dinner time ends in the year 2099," the checker says "okay, dinner's over, have dessert!" — even though dinner hasn't even started. That's the mistake: checking that the words *look* like a time without checking whether the time has *passed*. Lesson: if a rule is about time, your tests have to try different times — past, future, and right-now — or your tests prove nothing about time at all.

## 👵 GRANDMA NOTE

Sweetie, the team had a safety lock with twenty different tests, and every single one passed. But none of the tests ever asked "what time is it?" The lock only checked that the deadline was *written* correctly — never whether it had actually arrived. So a deadline set far in the future fooled it into opening early. The fix was simple: compare the deadline to the real clock. The lesson for all of us: a checklist that never varies the thing you're guarding isn't a checklist at all. If time matters, you test time — yesterday, tomorrow, and this exact minute.

## 🤖 NAYA NOTE

When writing or reviewing a falsifier suite for any gate with a temporal condition:

1. **Enumerate the gate's reasoning dimensions.** For `window_closed_at` the dimensions are: temporal position (past/present/future), format (ISO/tz-offset/naive/date-only/malformed), and type (string/int/None/bool/missing). A suite covering only format+type leaves a time hole.
2. **Straddle every threshold.** The check `window_closed_at <= now(UTC)` must be probed at: far-future literal (`2099-12-31T23:59:59Z`), near-future (`now()+1s`, `now()+1h` — proves it is a real time check, not a magic-date block), boundary (`now()-1s` allows), and far past. Malformed/empty/epoch-int/None/missing must all deny fail-closed.
3. **Distinguish "parsable" from "true."** A timestamp that parses is not a condition that holds. `window_closed_at` parseable-and-future is the *opposite* of C4's requirement ("no seat objects" is unprovable while the window is open) — the check must evaluate the relation to now, not the parse.
4. **State the suite's blind spots honestly.** A 20/20-green suite that never varied time is not "comprehensive" — score it for what it covered and name what it didn't. The re-validator's 14-probe time battery is the template for temporal falsification.
5. **Pair with SN-0820's sibling idiom:** the same repair round's bool quirk (`isinstance(True, int)`) recurs repo-wide; standing idiom `isinstance(x, bool) or not isinstance(x, int)` — but type probes are the *shape* dimension, and time probes are separate: a suite needs both.

## 🧠 MACHINE NOTE

```json
{
  "sn": "SN-0820",
  "class": "ENGINEERING-PROOF",
  "subcategory": "INDEPENDENT-VERIFICATION",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-09",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "rule": "A falsifier suite must vary every dimension the gate reasons over: timestamps require time-probes (far future, near future, boundary +/-1s, tz offsets, naive, malformed, missing) in addition to shape probes; every threshold must be straddled, not just poked at its edges. A green suite is evidence only over the dimensions it varied.",
  "worked_example": {
    "artifact": "delegated-merge receipt gate C4: consensus.window_closed_at checked only for parseability — receipt with window 2099-12-31T23:59:59Z returned (allowed=True, []) while the objection window was still open",
    "blind_spot": "20-test falsifier suite, all green, never varied time — 20/20 proved nothing about time",
    "fix": "C4 requires window_closed_at <= now(UTC); new test probes the time dimension twice (2099 literal AND now()+1h; now()-1s allows); re-validator's 14-probe battery: boundaries both sides, offsets +14:00/-05:00, naive future denies (assumed UTC), malformed/empty/epoch-int/None/missing deny fail-closed",
    "board_comment": "#1354 6088748791 (repair2 lesson), #1354 6088678545 (original validator finding)"
  },
  "related": ["SN-0518", "SN-0531", "SN-0603"]
}
```
