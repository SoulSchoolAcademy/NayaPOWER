# Mark Self-Seams With Stable Markers; Never Regex Your Own Code

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1583-mark-self-seams-never-regex-own-code
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-17
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** hidden_files/twelve-lane-receipts/t0798-lane9.md (Naya Clarity Narzan, Lane 9 Smith, self 9.5/10 — "MIRROR" lesson L59, AGENT FEEDBACK L68, fixes L37) — the baked-variant regex for the Smart Note feed page broke twice on the seat's own code shape; fix: `/* LIVE-FETCH-START/END */` markers in the page + marker-split in hidden_files/bin/verify_feed_page.py (L124–129). Also logged as learning-event candidate 576, 2026-10-17 17:20 PDT.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Regex over code you control is a rumor about your own file. The t0798-lane9 seat built a Smart Note feed page and its honesty gate (`verify_feed_page.py`); the gate's baked-snapshot falsifier located the fetch code with a regex — and the regex broke twice as the seat's own code shape evolved. The pattern was matching prose, not the seam. Fix: the page carries stable `/* LIVE-FETCH-START */` / `/* LIVE-FETCH-END */` markers, and the gate splits on the markers instead of regexing code shape; the baked variant then fires on the robust path. Rule: mark your own seams with stable markers at the first commit; a gate never infers structure from code it owns. The near-miss (the two broken regexes) was kept as evidence instead of tuning the gate toward the answer.

Why this is brain-grade: any page or instrument that fetches a file needs a way to find its own fetch block again. Regex couples the finder to accidental code shape, so every refactor of your own page silently re-breaks the gate — a failure class that is invisible until the falsifier stops firing. Markers are an explicit writer↔reader contract: the writer promises where the seam is, the reader reads where promised. Refactors preserve the markers, so the gate stays green for free.

## 🩷 HUMAN NOTE

Shawn — a small build discipline from the Smart Note feed page work. When I built the feed page, I also built its honesty gate — a script that proves the page renders live data instead of a baked snapshot. The gate had to find the page's fetch code, and my first version used a text pattern (regex) to find it. It broke twice — not because the page was wrong, but because my own page's code shape changed underneath the pattern. I was reading my own prose like a stranger.

The fix: the page now carries two stable markers (`LIVE-FETCH-START` / `LIVE-FETCH-END`) around the fetch block, and the gate splits on those markers — no pattern-matching my own code ever again. The standing rule going forward: the moment a page or instrument fetches a file, the markers go in at the first commit, and the gate reads the markers. Your own code is never a guessing game — mark the seam, split on the mark.

## 🟣 CHILD NOTE

Imagine you hide a key in your room and then forget where — so you have to turn the whole room upside down every time you want it. That's what regex does: it searches your own code like a stranger's room. A marker is like putting a little flag where you hid the key: the flag stays, so finding it is instant, forever. Always plant the flag the first time you hide something.

## 👵 GRANDMA NOTE

When you put the sugar away, you put a label on the jar — you don't sniff every jar in the kitchen each morning hoping to find it. Labels are promises you keep to yourself. The feed page's markers are labels on the jar: the gate opens the labeled jar every time, no sniffing. Put the label on at the start, and morning never breaks.

## 🧠 NAYA NOTE

This is the self-directed form of structural matching (cf. SN-1576): where SN-1576 anchors the reader to structure it does not own, this note marks structure you DO own at write time. The pair covers both directions of the same principle — never let prose be the interface. Writers emit seams; readers split on them. The t0798 seat kept the first failed regex as evidence (did not tune the gate toward the answer), which is why this lesson is falsifiable rather than anecdotal: the marker-split path demonstrably fires the baked falsifier while the regex path broke twice on the same bytes.

## ⚙️ MACHINE NOTE

```json
{
  "sn": "SN-1583",
  "applies_when": ["page", "honesty-gate", "verify", "fetch", "gate", "regex", "self-seam"],
  "enforcement": "hidden_files/bin/verify_feed_page.py marker-split step (L124-129): the gate reads the page's /* LIVE-FETCH-START */ / /* LIVE-FETCH-END */ markers and raises RuntimeError('LIVE-FETCH markers missing from the page') when absent; the baked-variant falsifier must fire on the marker-split path. Any new fetching page gets markers at its first commit; CI/verify gates that locate self-code must split on declared markers, never regex code shape.",
  "falsifier": "A code-shape change that preserves the LIVE-FETCH markers yet breaks the marker-split gate would falsify the lesson.",
  "mechanism": "Markers are an explicit writer-reader contract; regex infers structure from prose and is brittle to code-shape change.",
  "decision_change": "Any page/instrument that fetches a file carries stable seam markers from the first commit; honesty gates split on markers.",
  "related": ["SN-1576"],
  "provenance": "hidden_files/twelve-lane-receipts/t0798-lane9.md (L37, L59, L68); hidden_files/bin/verify_feed_page.py L124-129"
}
```
