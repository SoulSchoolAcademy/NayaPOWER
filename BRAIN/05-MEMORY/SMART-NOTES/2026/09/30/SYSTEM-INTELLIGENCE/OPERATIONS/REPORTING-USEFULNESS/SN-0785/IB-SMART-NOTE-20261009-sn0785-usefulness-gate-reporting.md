# The Usefulness Gate — a Report Must Not Contradict Its Own Evidence

**Intelligent Block:** IB-SMART-NOTE-20261009-sn0785-usefulness-gate-reporting
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-09
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6083037710 ([NAYA 5] REPORTING REBUILD: done, verified, pushed — `naya5/reporting-usefulness-rebuild @ 0f4747f7` — 2026-10-09T14:34Z). Source: SoulSchoolAcademy.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Naya 5 rebuilt the hourly report generator around the Usefulness Gate — Shawn's law: "if it's not useful it never ships." Four mechanical rules: (1) every item carries a timestamp; (2) unknown or out-of-window items are DROPPED, never recycled — stale scores can't move state; (3) every score labeled claim or authoritative (Learning 5.0 stays pinned authoritative); (4) the headline can never contradict the evidence.

Rule 4 is where the lesson lives, because it was earned the honest way: **during verification, Naya 5 caught her own first rebuild claiming "quiet" while the Evidence section listed 3 in-window PR updates.** The headline said nothing happened; the evidence said three things happened. She fixed it the structural way — in-window PR updates now count as movement — and added a test so the contradiction can never recur. A report whose headline contradicts its own evidence is worse than no report: it teaches the reader that the report lies, and after that no report is trusted.

Why this is brain-grade: stale recycling is a quiet bug class. Report generators run on schedules; every scheduled job faces empty windows; the tempting code path is "carry forward the last good stuff" so the report never looks empty. That path compounds: recycled numbers look current, readers act on them, and a cold successor inherits a system whose "truth" is increasingly composed of yesterday's truth. The note's mechanical fix is twofold and load-bearing: drop out-of-window content instead of recycling it (with an explicit one-line "Quiet hour — no window activity" for honest empty windows), and enforce headline↔evidence consistency as a tested invariant. Verification: 71/71 tests pass (freshness, no-boilerplate, quiet-hour, palette), a real end-to-end run on live data produced zero recycled content and zero boilerplate, and the PDF was screenshot-inspected.

Rule for a cold successor: **a report whose headline contradicts its own evidence is worse than silence — enforce headline↔evidence consistency as a tested invariant, drop out-of-window items instead of recycling them, and print an honest one-line quiet instead of fabricating activity.**

## 🩷 HUMAN NOTE

Shawn — the hourly report generator is rebuilt around your Usefulness Gate, per Naya 5's receipt this hour. Four rules now: every item timestamped, out-of-window items dropped instead of recycled, every score labeled claim or authoritative, and the headline can never contradict the evidence. The last rule was earned honestly: her first rebuild claimed "quiet" while the evidence listed three in-window PR updates — she fixed it so in-window PR updates count as movement and added a test so it can never recur. 71/71 tests pass, a real end-to-end run on live data showed zero recycled content, and the PDF was visually inspected. It goes live at the 15:00 UTC cron — the next report you see is the new format.

## 🟣 CHILD NOTE

Imagine a weather report that says "nothing happened today" but then lists three rainstorms underneath. You'd stop trusting the weather report — that's worse than no report at all. So the team made a new rule: the headline and the details can never disagree. If three things happened, the headline says three things happened. And if nothing happened, instead of copying yesterday's news to fill the space, the report just says one honest line: "quiet hour — nothing happened." The machine now checks this automatically every time.

## 👵 GRANDMA NOTE

The team rebuilt their regular status report so it can't mislead. The key fix: the headline and the details must always agree — the first version said "nothing happened" while its own details listed three updates, and the builder caught and fixed her own mistake. Old content is no longer carried forward to fill empty hours; quiet hours are simply labeled as quiet. An automatic check now verifies the headline matches the evidence every time the report runs.

## 🟠 NAYA NOTE

Apply the Usefulness Gate to every generator: (1) timestamp every item; (2) drop unknown/out-of-window items, never recycle — stale scores can't move state; (3) label every score claim or authoritative; (4) enforce headline↔evidence consistency as a tested invariant — in-window activity of any kind counts as movement. Empty windows print one honest line: "Quiet hour — no window activity." Verify with a real end-to-end run on live data: zero recycled content, zero boilerplate.

## ⚙️ MACHINE NOTE

{
  "schema": "smart-note-v1",
  "sn": "SN-0785",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-09",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE/OPERATIONS/REPORTING-USEFULNESS",
  "doctrine": "usefulness-gate-reporting",
  "rule": "A report whose headline contradicts its own evidence is worse than silence. Enforce headline↔evidence consistency as a tested invariant; drop out-of-window items instead of recycling them; print an honest one-line quiet.",
  "failure_mode": "report generators recycle stale content to fill empty windows; recycled numbers look current; readers act on them; headline contradicts evidence and trust in all reports dies",
  "mechanism": {
    "rules": [
      "every item timestamped",
      "unknown/out-of-window items dropped, never recycled",
      "every score labeled claim or authoritative (Learning 5.0 pinned authoritative)",
      "headline can never contradict evidence — in-window PR updates count as movement (test added after self-caught contradiction)"
    ],
    "verification": "71/71 tests pass (freshness, no-boilerplate, quiet-hour, palette); real end-to-end run on live data: zero recycled content, zero boilerplate; PDF screenshot-inspected; live at 15:00 UTC cron"
  },
  "related": ["SN-0692", "SN-0700", "SN-0783"],
  "provenance": ["#1354 comment 6083037710"]
}
