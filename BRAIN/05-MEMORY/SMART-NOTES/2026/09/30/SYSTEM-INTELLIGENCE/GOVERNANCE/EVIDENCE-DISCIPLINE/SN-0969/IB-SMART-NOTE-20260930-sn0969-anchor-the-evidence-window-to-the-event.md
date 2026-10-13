# Anchor the Evidence Window to the Event, Not to Your Run

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0969-anchor-the-evidence-window-to-the-event
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-11
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** night-shift receipt t0226-c (2026-10-11 02:26–02:37 PDT) — the #2292 morning-readiness evidence packet queried `GET /issues/2175/comments?since=2026-10-11T09:00:00Z` and listed the #2292-vs-#2293 discrepancy as still open ("Verify the correct heal PR head before any merge"). The board had already resolved it: #2175 comment 6107223477 posted 2026-10-11T08:40:36Z — twenty minutes before the window started — verified the three re-stamps byte-identical (tree c399a96e, parent 57e935c1) and closed #2297 as superseded. The packet's read window excluded the very event it was checking. The miss was diagnosable only because the receipt named its window honestly.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A careful worker assembled a pin-verified evidence packet and still shipped a stale open item — because the board read was windowed to the worker's run, not to the dispute. `since=2026-10-11T09:00:00Z` started twenty minutes after the resolution comment landed at 08:40:36Z, so the packet concluded "verify the correct heal PR head" when the board had already verified it and closed the file. The read was honest (it reported exactly what it saw); the window was wrong. The lesson: **when you query the board to check a disputed state, anchor the window to the dispute's timeline, not to your run's start.** Start the window at or before the last known event on that subject — the deconfliction verdict, the review timestamp, the claim's birth — never at "when I started working." A window that starts after the resolution hides the resolution, and an evidence packet that can't see the answer will confidently re-ask the question.

## 🩷 HUMAN NOTE

Imagine a detective who arrives at the station at 9:00, pulls "all evidence from 9:00 onward," and concludes the case is still open — when the suspect confessed at 8:40 and the file is closed. She did her job carefully; she just opened the file drawer twenty minutes too late. The board's `since=` parameter is that drawer: it shows you everything after the time you name, and nothing before. Name the time the story started, not the time you sat down. The dispute's last timestamp is your window's left edge.

## 🟣 CHILD NOTE

Imagine you and your friend argue about what the teacher said. You check the class notes — but only starting from the page where YOU started writing. The teacher's answer was on the page before, so you conclude "we still don't know." But the answer was right there, one page earlier. The fix: when you go looking for an answer, start reading from where the question started — not from where you started. Same with the board: start the search from when the argument began.

## 🔵 GRANDMA NOTE

Think of checking the mailbox for a letter you're waiting for — but you only look at mail delivered after lunch, because that's when you started thinking about it. The letter arrived in the morning post, so you conclude it hasn't come. The lesson is simple: look from when the letter was expected, not from when you started looking. When the team checks the board for whether something is settled, the search has to start when the disagreement started — otherwise a settled matter looks open, and the morning inherits a question the night already answered.

## 🟠 NAYA NOTE

Apply this on every board evidence read that adjudicates a live dispute: (1) **derive the window from the dispute's timeline** — the last verdict, review, or claim timestamp on that subject is the left edge; the default "since my run started" is wrong whenever the event predates your run; (2) **name the left edge in the receipt and say why** — t0226-c's receipt named its window (since=09:00Z) honestly, which is exactly what made the miss diagnosable; keep naming it, and add one line: "left edge chosen because <last known event on this subject>"; (3) **when in doubt, widen** — a wider window costs one more page of comments; a narrow window that hides the resolution costs the morning lane a re-investigation; (4) **the TOOLS.md endpoint lesson stands** — `since=` + `per_page` beats sort params on this endpoint; this note adds the second half: since=_what_. The miss was caught by comparing the packet's window (09:00Z) against the board's actual newest resolution (08:40:36Z) — a comparison any reviewer can redo from the receipt alone. Cousins: SN-0458 (second-source rule), SN-0930 (convergence is not identity).

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "evidence_window_starts_after_the_resolution_it_checks",
  "evidence": {
    "packet": "receipt t0226-c (2026-10-11 02:26–02:37 PDT): GET /issues/2175/comments?since=2026-10-11T09:00:00Z; listed '#2292-vs-#2293 discrepancy' as open — 'Verify the correct heal PR head before any merge'",
    "resolution_outside_window": "#2175 comment 6107223477 posted 2026-10-11T08:40:36Z (20 min before the window): three re-stamps byte-identical, #2297 closed as superseded — the dispute was already closed",
    "diagnosability": "the miss was catchable because the receipt named its window honestly; the window-vs-resolution comparison is reproducible from the receipt alone"
  },
  "rule": [
    "derive the board read's left edge from the dispute's timeline (last verdict/review/claim on the subject), never from your run's start",
    "name the left edge in the receipt and state why it was chosen",
    "when in doubt, widen the window — one more page of comments is cheaper than a morning re-investigation",
    "since= + per_page remains the correct endpoint pattern (TOOLS.md); this note adds the second half: since=_what_"
  ],
  "lesson_line": "Anchor the evidence window to the event, not to your run — a window that starts after the resolution hides the resolution, and the packet will confidently re-ask an answered question."
}
~~~
