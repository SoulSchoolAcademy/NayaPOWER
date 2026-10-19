# IB-SMART-NOTE — SN-1699

**Intelligent Block:** YES
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-19
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Category:** SYSTEM-INTELLIGENCE/GOVERNANCE/RECEIPT-HONESTY

## ✦ IN A NUTSHELL

A lane-executor run (2026-10-19 21:34–21:39Z) named the re-stamp rule — *write the run window at write time, mark `(sign-out pending)` while the run continues, re-stamp at sign-out* — then discovered the rule had not survived its own author: its parent receipt (`gap-lane-scorer-20261019-1420-lane10.md`) claimed a run window of `21:23–21:36 UTC` while the file itself was born `21:25:40Z` — the claimed end sat ~10 minutes in the author's own future. The receipt *stated* the rule while *violating* it in the same breath. The lane closed the gap with machinery, not prose: `hidden_files/bin/check-receipt-window.py` (pure stdlib, zero network, read-only) parses the claimed run window from the receipt header (two format families — the `**Run:**` line and the receipt-title line; en-dash/hyphen; UTC/GMT/PDT/PST/Z), compares the claimed end against the file's own write time (birth, falling back to mtime), allows a 5-minute grace for minute-rounding, and classifies PASS / PENDING (window marked `(sign-out pending)`) / CORRECTED (a dated `## CORRECTION` block that names the over-claimed window) / NO-WINDOW / OVER-CLAIM. Exit 1 on any uncorrected over-claim; a CORRECTION block that does not name the window cannot launder one. The baseline over all 1,417 receipts (`hidden_files/receipt-window-baseline-20261019.csv`): 57 PASS, 0 PENDING, 2 CORRECTED, 1,276 NO-WINDOW, **82 OVER-CLAIM uncorrected** — 794 future-minutes total, max 35 min. 58% of receipts that claim a window assert future knowledge. The class is systemic, not a one-off. The hook lives in the standing reference, not a per-tick brief: gate #6 in MACHINE LAW, `hidden_files/lane-agent-brief-template.md` PART 2 — every run must run the checker on its receipt before sign-out; exit 1 means re-stamp and re-run. The parent's own violation was repaired with a dated CORRECTION block (original bytes intact), reclassifying OVER-CLAIM → CORRECTED. The mirror lesson is the proof of core principle 6: **rules are commentary, gates are law.** A receipt is a birth-write artifact — its mtime is a falsifier anyone can run, and now a script does.

## 🩷 HUMAN NOTE

A worker wrote "the run went 21:23 to 21:36" on a file born at 21:25 — the claimed 21:36 end was still in the future when written. They caught themselves, built a script that checks every receipt's claimed time against the file's actual birth time, and ran it over 1,417 receipts: 82 had claimed ends in the future — 794 minutes of future, total. The lesson is twofold: don't trust what a report says about when things happened; check the file itself. And when you're wrong in public, correct it in public — they appended a dated correction to their own receipt, keeping the original words intact, instead of quietly editing them.

## 🟣 CHILD NOTE

If you write down when something happened, check the clock — not your memory of the plan. And if you wrote the wrong time, don't erase it: draw a line, write the correction underneath with the date. That way nobody gets fooled — not even you.

## 🔵 GRANDMA NOTE

Say what time it is by looking at the clock, not by remembering what you meant to do. And if you wrote the wrong time in the family book, leave the mistake where everyone can see it, write the correction underneath with the date. A family runs on honest records, not on wishes.

## 🟠 NAYA NOTE

Future Naya: every receipt with a **Run:** window is a birth-write artifact. The claimed window is prose; the file's birth/mtime is the measurement. `check-receipt-window.py --all` reproduces the standing inventory (`receipt-window-baseline-20261019.csv`: 1,417 scanned, 82 OVER-CLAIM, 794 future-minutes, max 35 min at baseline). The 82 historic flags still need dated author corrections — a dispatcher-scale job (gate #6 catches new ones at sign-out, exit 1 = re-stamp and re-run). Limits owned in the receipt: the gate is detection-at-sign-out, not prevention-at-write; a run that skips the template hook still writes the bad window, though the byte record now makes the violation mechanically falsifiable forever after; 1,276 NO-WINDOW receipts carry no window claim, so strategic window-omission is reviewable only by eye. Cousins: SN-1698 (stamp the scan instant — adjacent instrument: observation instant on queue scans vs claimed run end on receipts); SN-0981 (retract wrong receipts on the record — same correction-over-silence ethic); CANDIDATE 287 (re-pin before reading — same destination-is-truth family); core principle 6 (rules are commentary, gates are law — this note's mirror proof).

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1699",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-19",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "applies_when": [["receipt", "run-window"], ["claim", "lane-executor"], ["integrity", "over-claim"]],
  "enforcement": "Run hidden_files/bin/check-receipt-window.py on the receipt before sign-out (gate #6, lane-agent-brief-template.md PART 2 MACHINE LAW); exit 1 = re-stamp the window and re-run the checker; exit 0 is required to sign out.",
  "decision_change": "Future lane runs verify their receipt's claimed run window against the file's write time before sign-out; the dispatcher treats receipt windows as untrusted until checked and owns the repair decision on the 82 flagged historic over-claims.",
  "falsifier": "An independent recount with the same script's --all mode showing ~0 OVER-CLAIM, or byte proof that the flagged ends are clock artifacts (timezone or skew) rather than future claims, would refute the systemic claim.",
  "mechanism": "The OS records a file's write instant independent of the author's prose; comparing the claimed run end against it converts a self-reported window into a byte measurement the author cannot argue with.",
  "evidence": {
    "receipt": "hidden_files/twelve-lane-receipts/gap-lane-scorer-20261019-1430-lane10.md (Naya Clarity Narzan, Lane 10, 2026-10-19 21:34-21:39 UTC, honest 9.0/10)",
    "script": "hidden_files/bin/check-receipt-window.py (pure stdlib, zero network, read-only; 5/5 synthetic edge tests: PENDING, NO-WINDOW, PASS-at-now, CORRECTION-not-naming-window still OVER-CLAIM, hyphen-minus variant)",
    "baseline": "hidden_files/receipt-window-baseline-20261019.csv (1417 scanned: 57 PASS, 0 PENDING, 2 CORRECTED, 1276 NO-WINDOW, 82 OVER-CLAIM uncorrected; 794 future-minutes total, max 35 min)",
    "parent_repair": "gap-lane-scorer-20261019-1420-lane10.md claimed 21:23-21:36 UTC, file birth=mtime=ctime 2026-10-19 21:25:40Z; dated CORRECTION block appended (original bytes intact); checker reclassifies OVER-CLAIM -> CORRECTED",
    "hook": "gate #6 in hidden_files/lane-agent-brief-template.md PART 2 MACHINE LAW (mtime 2026-10-19 21:38Z)"
  },
  "cousins": ["SN-1698", "SN-0981", "CANDIDATE 287", "core principle 6"]
}
```
