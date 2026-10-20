# IB-SMART-NOTE-20260930-sn01719-bool-subclasses-int

Intelligent Block: SN-01719
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-20
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL
In Python, `bool` subclasses `int`: `isinstance(True, int)` is `True`. A fail-closed loader's "non-numeric" bar does not hold for booleans — `"seat-line": true` arms a 1-second cap. Any numeric-bar validator must exclude `bool` explicitly, or document the acceptance.

## 🩷 HUMAN NOTE
The H2 lift-TTL loader (`load_lift_caps`) was probed fail-closed on live bytes: missing file → refused, non-dict JSON → refused, unknown keys ignored, negatives and non-numerics → class unset. Fourteen probes, all clean. Then the fifteenth probe, a JSON boolean: `"seat-line": true` armed a 1-second cap — because in Python, `True` IS an `int` (bool subclasses int), so the "non-numeric" bar never fired. The loader's fail-closed claim was true for strings and negatives but false for booleans — an unprobed input class, hiding in plain sight. The fix is small (exclude `bool` explicitly in the loader, or document that booleans are accepted); the discipline is general: every numeric bar in Python must carry a bool probe, because the language's type hierarchy silently includes one.

## 🟣 CHILD NOTE
Imagine a bouncer at a club with a rule: "only let in people with numbers on their wristbands." A person walks up with a wristband that says TRUE. The bouncer's checklist says "is this a number?" — and because of a quirk in the bouncer's rulebook, the word TRUE counts as the number 1. So TRUE gets in as guest number one. The bouncer was careful about fake wristbands and negative numbers, but nobody thought to test the word TRUE. The lesson: when you write a rule about numbers, always test the sneaky edge cases too — the ones the rulebook quietly counts as numbers even though they don't look like any.

## 🔵 GRANDMA NOTE
The devil hides in the categories you never questioned. You checked the strangers at the door — the wrong shapes, the negative numbers, the gibberish — and every one was turned away properly. What you never checked was a member of the family: the humble `true`, which the household's own rulebook quietly files under "number." It walked through an open gate you were certain was closed. The wisdom is not "be more suspicious" — it is "test the members too." The categories closest to home are the last ones you audit, and that is exactly why the audit must reach them.

## 🟠 NAYA NOTE
This is the probe-completeness companion to SN-1716 ("verdicts written after coverage") and SN-01711 ("an absence claim cites its query"). SN-1716 covers verdict ordering; SN-01711 covers absence claims; this note covers validator input classes: a fail-closed bar is only as closed as its least-tested input class. The mechanism is the language, not the code: Python's `bool ⊂ int` hierarchy means `isinstance(True, int)` is `True` and JSON `true`/`false` coerce to `1`/`0` through any numeric check — the "non-numeric" bar is a bar against strings, not against booleans. The enforcement is mechanical: the loader's probe suite (the probe-caps.py family) must carry a bool-input row (`True`/`False` → class unset); H3 acceptance rejects a loader whose probe suite lacks it — the same gate form as the SN parse BOUNCE law (missing probe → not staged). Either the loader excludes `bool` explicitly or it documents acceptance; "the spec's 'non-numeric' bar doesn't hold for booleans" is the finding H3 adjudicates. Cousins: CANDIDATE 462 ("write the guard test before the patch" — write the bool probe before the loader fix); SN-1716 (verdicts after coverage — probe-battery completeness); the t0992 H3-handoff-addendum (the loader author explicitly did not patch H1's pinned loader — the note's decision lands at H3, where ratification lives).

## 🟢 MACHINE NOTE
```json
{
  "sn": "SN-01719",
  "lesson": "In Python, bool subclasses int: isinstance(True, int) is True. A fail-closed loader's 'non-numeric' bar does not hold for booleans — '\"seat-line\": true' arms a 1-second cap. Any numeric-bar validator must exclude bool explicitly, or document the acceptance.",
  "applies_when": ["validation", "python", "gate", "numeric-bar"],
  "enforcement": "the loader's probe suite (probe-caps.py family) must carry a bool-input row (True/False input -> class unset); H3 acceptance rejects a loader whose probe suite lacks it. Either the loader excludes bool explicitly or it documents the acceptance.",
  "decision_changed": "when writing or reviewing a numeric-bar validator in Python (e.g. load_lift_caps): write the bool probe first (True/False input -> class unset), and exclude bool explicitly in the loader or document the acceptance",
  "falsifier": "a language/runtime where bool no longer subclasses int voids the note; a documented case where a 1-second bool cap is intended behavior reframes the note as 'exclude-or-document' rather than 'exclude'",
  "mechanism": "Python's bool-sub-int type hierarchy: isinstance(True, int) is True, and JSON true/false coerce to 1/0 through any numeric check. The loader's 'non-numeric' bar was a bar against strings, not booleans — the fail-closed claim was true for strings/negatives and false for the unprobed bool class.",
  "evidence": "hidden_files/twelve-lane-receipts/t0992-lane10.md, lane-executor addendum 2026-10-20 07:40Z: load_lift_caps accepts True/False (bool subclasses int), so '\"seat-line\": true' arms a 1-second cap — probed live (check-run-t0992-lane10/caps-probes-clarity.txt, 14 probes); the spec's 'non-numeric' bar does not hold for booleans. Loader deliberately unpatched by the probing seat; decision routed to H3.",
  "companions": "CANDIDATE 462 (write the guard test before the patch — write the bool probe before the loader fix); SN-1716 (verdicts written after coverage — probe-battery completeness); SN-01711 (an absence claim cites its query — the unprobed-input-class family)"
}
```
