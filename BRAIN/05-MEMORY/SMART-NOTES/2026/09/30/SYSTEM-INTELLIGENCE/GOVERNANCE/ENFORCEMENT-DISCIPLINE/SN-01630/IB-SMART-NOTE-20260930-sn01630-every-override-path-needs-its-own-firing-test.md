# Every Override Path Needs Its Own Firing Test — Lexicographic Tick Order Is Not Time

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01630-every-override-path-needs-its-own-firing-test
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-18
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Lexicographic order is not time. `file-gap-brief.py`'s `is_lifted` compared claim ticks as strings, so `"lane-executor-20261018-0538"` sorted *before* `"lane-scorer-20261016-2120"` — a sanctioned no-refile lift that was genuinely later was silently voided as "not later," and the lane recorded a lift that never fired. Repaired within the tick: cross-shape ticks now compare by embedded `YYYYMMDD-HHMM` wall clock, `_same_shape` tightened to same mechanism prefix, 2 regression cases added, `--self-test` 12/12 green. The standing doctrine: an override path is the most dangerous code in the machinery — it must prove itself with its own firing test *before* the hour it is needed, because the hour it is needed is the worst hour to discover it never fired.

## 🩷 HUMAN NOTE

Some buttons are more dangerous than others. The "override" button — the one that lets a lane-executor bypass a "don't re-file" verdict — is the most dangerous button in the whole machine, because it exists precisely for the moment when the normal rules don't fit. Ours was silently broken: the code that decides "is this override newer than the verdict?" compared the two ticket labels alphabetically instead of by time. "Lane-executor October 18" alphabetically comes before "lane-scorer October 16," so the machine said "not newer" and threw the override away without telling anyone. A seat thought it had exercised a sanctioned override; the machine had quietly voided it. The fix took one tick: compare the dates buried inside the labels, not the labels. The durable rule is bigger than the bug: every override path — every "break glass" mechanism — must carry its own firing test, and that test must be green before the path is ever needed. The one time an override fires is the one time you cannot afford to discover it is decorative.

## 🟣 CHILD NOTE

The "break glass" button must be tested before there is a fire. Ours looked fine but compared words instead of dates, so it silently didn't work when someone pressed it. Now it has a test that presses it on purpose, every time, and the button only counts if the test is green.

## 🔵 GRANDMA NOTE

Every emergency procedure gets a fire drill, and the drill happens before the emergency — not during. Our override button had no drill, and when it mattered, the button compared names alphabetically instead of checking the clock. Now the drill runs twelve checks and all twelve must pass, or the button doesn't get used.

## 🟠 NAYA NOTE

Machinery-repair class (2026-10-18): `file-gap-brief.py is_lifted` compared cross-shape claim ticks lexicographically — `"lane-executor-20261018-0538"` ordered before `"lane-scorer-20261016-2120"` because `'e' < 's'` — so a genuinely-later sanctioned no-refile lift was silently voided ("not later"). Same run: `_same_shape` tightened to same mechanism prefix (cross-shape comparison is a category error, not an ordering problem); 2 regression cases added; `--self-test` 12/12 green. The executor also repaired venue pointers in the same tick (`coldstart-packet-template.md`, `dispatcher-stale-check-procedure.md`: retired boards `#2175`/`#2641` → live board `#2721`). Lesson filed by the repairing seat in its own receipt: every override path needs its own firing test before it is needed. This pairs with the gate-design family: a gate that fails open on its own bar (cf. the claim-brief.py compound-token matcher, t0834) and an override that fails closed on its own purpose are the same bug in two clothes — both are machinery whose contract was never exercised.

## 🟢 MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "sn": "SN-01630",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-18",
  "applies_when": [
    ["claim", "file-gap-brief"],
    ["machinery", "override-path"],
    ["compare", "cross-shape-ticks"],
    ["mechanism", "sanctioned-lift"]
  ],
  "enforcement": "file-gap-brief.py --self-test is the standing enforcement: it runs 12/12 green — including the 2 is_lifted cross-shape regression cases (genuinely-later lift across shapes must return TRUE; same-mechanism-prefix gating must hold) — after ANY edit to claim/lift/verify machinery, before that machinery is used in a live tick. A failing is_lifted case voids the run: no dispatch, no claim, no lift until the test is green. The independent witness is the filed second-seat followup (brief-gap-lane-scorer-20261018-0550-lane9.md): the _same_shape fail-surface change gets a different-seat eyeball.",
  "decision_change": "The sanction decision 'is this lift genuinely later than the verdict?' changes from string-compare to embedded-wall-clock-compare: cross-shape ticks order by the YYYYMMDD-HHMM embedded in the label, never by the label. The machinery-maintenance decision changes from 'the override path is there if we need it' to 'the override path proved it fires this tick' — no override path ships or survives without its firing test green.",
  "falsifiability": "Run --self-test: if is_lifted misorders a genuinely-later cross-shape lift as 'not later', the fix is incomplete and the lesson's mechanism claim is wrong. Falsified at a deeper level if a future tick format carries no parseable embedded wall clock and ordering must move to an explicit timestamp field — then 'embedded-YYYYMMDD-HHMM' is superseded as the canonical source, but the firing-test doctrine survives it.",
  "mechanism": "String ordering of heterogeneous-shape labels does not track time: prefix letters ('lane-executor' vs 'lane-scorer') dominate the comparison and the embedded date never gets consulted. The embedded YYYYMMDD-HHMM is the only order-faithful component, so it must be extracted and compared directly. Override paths fail silently because they run rarely — no firing test means no exercise, and no exercise means the first live use is also the first test, at the worst possible moment."
}
~~~

## 🧾 PROOF / PROVENANCE

~~~json
{
  "event": "2026-10-18 05:38-05:56 PDT (12:38-12:56 UTC), lane-executor brief-gap-lane-scorer-20261017-1630-lane9",
  "receipt": "hidden_files/twelve-lane-receipts/gap-lane-scorer-20261017-1630-lane9.md (9.3/10)",
  "board_record": "https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2721#issuecomment-6250071871",
  "bug": "is_lifted compared 'lane-executor-20261018-0538' < 'lane-scorer-20261016-2120' lexicographically -> 'not later' -> sanctioned lift silently voided",
  "repair": "cross-shape ticks compare by embedded YYYYMMDD-HHMM; _same_shape tightened to same mechanism prefix; 2 regression cases added",
  "self_test": "12/12 green post-repair",
  "same_tick": "venue pointers repaired: coldstart-packet-template.md + dispatcher-stale-check-procedure.md, #2175/#2641 -> live board #2721",
  "witness": "brief-gap-lane-scorer-20261018-0550-lane9.md (second-seat eyeball of the fail-surface change, lane-scorer 05:50 PDT)",
  "seat_lesson": "every override path needs its own firing test before it is needed (repairing seat's own words)"
}
~~~

## 🟨 HOW TO APPLY / HOW TO USE

1. Touching claim/lift/verify machinery: write the firing test FIRST (a case that exercises the override end-to-end), then the fix, then run `--self-test` green before any live use.
2. Comparing ticks across shapes: extract the embedded `YYYYMMDD-HHMM` and compare wall clocks; never compare the labels as strings.
3. `_same_shape` (or any shape gate): tighten to same mechanism prefix — comparing across shapes is a category error, not an ordering decision.
4. Auditing any "break glass" path you did not write: demand its firing test; no test, no trust.
5. When a repair touches machinery AND pointers in one tick, record both; venue rot is the quiet twin of logic rot.

## ⚠️ TRUTH BOUNDARY / UNCERTAINTY

The repair is proven by `--self-test` 12/12 and the live lift that fired after it; the second-seat eyeball (brief-gap-lane-scorer-20261018-0550-lane9.md) is filed but still owed — the fail-surface change has not yet had its independent witness. The doctrine (firing test before need) is standing; the embedded-YYYYMMDD-HHMM convention is current-canonical and falsifiable per above.
