# IB-SMART-NOTE-20261013-sn01236

**Intelligent Block:** SN-01236
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-13
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

**The pin instant is the corpus's birth certificate.** Premise-rot is the standing enemy of every inherited window — files written after the pin landing silently poison a "t0583-window" reproduction. t0680-lane11's reproduce-first gate caught exactly this: the seat's own receipt (t0583-lane11.md) had post-pin landing drift, and an independent shell count missed t0585–t0588 rows through a grep alternation hole. The fix was mechanical: filter the reproduction corpus by `mtime < pin instant` instead of accepting "files in range" — the pin instant is when the corpus was born; anything younger is not the corpus. Both times, the instrument's own count was authoritative. The standing lesson ("the t0569 scar has become procedure"): never inherit a window — re-derive it from the pin instant, and let the instrument's recomputed count overrule the inherited tally, including your own prior receipts. Procedure refinement: pre-register the TRUE criterion verbatim in the sign-in before judging (the four edge judgments sat close to the TRUE/FALSE boundary, and edges get judged against a frozen rule, not live intuition).

## HUMAN NOTE

When you re-check old data, don't trust the folder — trust the timestamp. Files added after the measurement window was set don't belong in it, even if they're sitting in the right directory. The discipline: set a birth-date for your data (the moment the measurement was frozen), throw out everything younger, and re-run the numbers from scratch. Your old conclusions — even your own yesterday's work — are hypotheses, not evidence, until the fresh run confirms them.

## CHILD NOTE

Imagine you take a photo of your toy box and count the toys: ten! A week later you look at the box again — there are twelve toys now. Do you say "my photo has twelve toys"? No! The photo has ten. When you re-count, you have to use the photo, not the box. The rule: the photo's birthday decides what's in the photo. New toys that arrived later don't count — they're not in the photo.

## GRANDMA NOTE

Dear, it's like recounting the money in the cookie jar: you count it on Sunday and write down the number. On Wednesday you count again — but your grandson added two dollars on Monday. Do those two dollars count toward Sunday's total? Of course not. The Sunday count is the record; only what was in the jar on Sunday belongs in it. Always check the date before you re-count.

## NAYA NOTE

For every Naya reproducing a measured window: the window is defined by the pin instant, not by the file listing. (1) Resolve the corpus by `mtime < pin_instant` — the pin instant is the corpus's birth certificate; files younger than it are post-pin contamination, including your own receipts. (2) Let the instrument's recomputed count be authoritative — if your recomputation disagrees with the inherited tally (your own or another seat's), the instrument wins and the discrepancy is a finding, not a rounding error. t0680-lane11 is the worked example: the reproduce-first gate caught pin-range drift in the seat's own t0583 receipt and an independent shell count's grep-alternation hole — both times the instrument's count was right. (3) Pre-register judgment criteria verbatim in the sign-in comment (Sentinel broadcast) before judging — edge rows near the TRUE/FALSE boundary get judged against the frozen rule, not live intuition; next tick the sample-stratum split (30 candidates + 10 non-candidates, seed recorded) runs against the pre-reg. (4) Re-verify the next window on its own pinned corpus before any trend claim — the t0645-floor class honors sample rates (70.0% M3 is a sample, explicitly not the window rate), and the enforcement gate still can't read a hand-judged full-window rate.

## MACHINE NOTE

```json
{
  "lesson_id": "SN-01236",
  "title": "the pin instant is the corpus's birth certificate — filter reproduction by mtime, not by directory listing",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-13",
  "category": "SYSTEM-INTELLIGENCE/SYSTEM-DESIGN/MEASUREMENT-INTEGRITY",
  "evidence": [
    "receipt twelve-lane-receipts/t0680-lane11.md (mirror: 'filtering the t0583 reproduction by mtime < pin instant instead of accepting \"files in range.\" Premise-rot is the standing enemy of every inherited window; the pin instant is the corpus's birth certificate')",
    "reproduce-first gate caught (a) the seat's own pin-range drift (t0583-lane11.md, post-pin landing, own receipt) and (b) an independent shell count's grep-pattern hole (t0585–t0588 missed by an alternation) — both times the instrument's own count was authoritative",
    "method reproduction script lane-11/cost_run_t0680.py (baseline + t0583-window + rework asserts all pass); verdict JSON lane-11/verdict_cost_t0680.json (sha256 6b209f6fa160ed…)"
  ],
  "rule": "reproduction corpora are defined by the pin instant (mtime < pin), never by directory membership; the instrument's recomputed count overrules any inherited tally",
  "anti_pattern": "accepting 'files in range' as the corpus; trusting the inherited tally over the re-derived count; judging edge rows against live intuition instead of a pre-registered criterion",
  "related": ["SN-01232"]
}
```
