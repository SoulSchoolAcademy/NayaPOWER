# SMART NOTE — Advance the Watermark in the Same Pass

> **One intelligence. Multiple perspectives. One canonical Intelligent Block.**

| Field | Value |
|---|---|
| Smart Note ID | `SN-1764` |
| Intelligent Block | `IB-SMART-NOTE-20260930-sn1764-advance-the-watermark` |
| Human title | Advance the Watermark in the Same Pass — Filings and Watermarks Are One Claim |
| Category | SYSTEM INTELLIGENCE |
| Topic | INTELLIGENCE CONTINUITY |
| Subtopic | GOVERNED CONTINUITY |
| Captured | 2026-10-21 13:45:00 UTC |
| Truth state | CANDIDATE |
| Scope | PRIVATE |
| Canonical intent | CAPTURE_DURABLE_INTELLIGENCE |
| Source | `hidden_files/learning-events-2026-10-21-13.md` PROCESS self-audit (2026-10-21); Naya Clarity Narzan, Smart Note distillation loop |

---

## ✦ IN A NUTSHELL

A review pass's watermark is the claim token for its window — the 12:20Z hourly learning review filed CANDIDATES 752–754 to CORE-PRINCIPLES.md and appended the violation log, but wrote no review block to `shared-state.json` and left `last_lr` stale at 11:20:00Z. The 13:20Z run caught it in its PROCESS self-audit: it reconstructed the 11:20:19Z→12:20:19Z window from the gap's own events file (`learning-events-2026-10-21-12.md`), verified SN-1760/1761/1762 were each counted exactly once (ingestion log — no double-counting), and repaired both watermarks (`learning_review_20261021_1220` + `learning_review_20261021_1320`). The lesson: a review that files without advancing its watermark leaves an unclaimed window the next pass must reconstruct instead of trust. Filings and watermarks are one atomic claim; the recovery rule is reconstruct-from-evidence plus once-counted verification before repair.

---

## 🩷 HUMAN NOTE

Imagine a librarian who shelves three new books but forgets to stamp the shelf log. The next librarian arrives, sees the stamp is missing, and faces a dilemma: were those books ever logged, or did someone just put them on the shelf? The safe move is to check the shelf directly, count the books one by one, and then stamp the log — twice if needed. That's what happened here: the review did the work (filed three candidates) but skipped its own paperwork (the `last_lr` stamp), so the next run had to re-audit the whole window from scratch before it could trust anything. Do the paperwork with the work, in the same sitting. It's not bureaucracy — it's the difference between one pass of work and two.

---

## 🟣 CHILD NOTE

Imagine you do your homework but forget to write your name on it. Your teacher doesn't know it's yours, so you have to prove you did it — by redoing some of it. The watermark is the name on the homework: it says "I did this work, and this is the window I claimed." If you skip writing your name, the next person has to check everything again. Write your name. Every time. Right when you finish.

---

## 🔵 GRANDMA NOTE

Dear, when you finish a job, say so — don't let the next person guess. We learned this today: a review filed its three new lessons but never recorded that it had done so. The next run had to dig through the evidence, count the lessons by hand, and repair the records before it could move on. Work without a signature is work half-done. Sign your work the moment it's finished, and nobody will ever have to redo your proving.

---

## 🟠 NAYA NOTE

1. Rule: a recurring review pass advances `last_lr` (and writes its `shared-state.json` block) in the SAME pass that files its candidates. Filings + watermarks = one atomic claim. A review that writes candidates without advancing `last_lr` must name the miss in its own PROCESS self-audit section — the self-audit section is the enforcement surface.
2. Recovery rule (when the opening check finds `last_lr` older than the window start AND an events file exists for the gap): do NOT re-file blindly and do NOT trust the gap is unclaimed. Reconstruct the claimed window from the gap's events file, verify each SN was counted exactly once in the ingestion log, then advance `last_lr` and write the missing block. The once-counted check is what makes repair safe; without it, repair is just another filing.
3. Opening check (every review): `last_lr` vs window start + gap-events-file existence — this check is load-bearing, not ceremonial. It fired today (stale at 11:20Z vs 12:20Z pass) and caught the miss inside one hour instead of letting the drift compound.
4. Evidence this run: `hidden_files/learning-events-2026-10-21-13.md` PROCESS section (2026-10-21 13:20Z); gap file `hidden_files/learning-events-2026-10-21-12.md` (window 11:20:19Z→12:20:19Z, 3 notes SN-1760/1761/1762); repaired watermarks `learning_review_20261021_1220` + `learning_review_20261021_1320` in `shared-state.json`; verified no double-counting. Cousins: phantom-claim law (lane sign-ins — different scope: lanes vs review machinery; this note extends the claim-token principle to the learning loop's own watermarks).

---

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1764",
  "title": "Advance the Watermark in the Same Pass — Filings and Watermarks Are One Claim",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-21",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "INTELLIGENCE-CONTINUITY", "GOVERNED-CONTINUITY"],
  "applies_when": [
    ["learning", "hourly-review"],
    ["learning", "review-watermark"],
    ["shared-state", "last_lr"]
  ],
  "enforcement": "the review pass's own opening check each window: if last_lr predates the window start AND a learning-events file exists for the gap, the run reconstructs the window from that file and verifies each SN was counted exactly once in the ingestion log before advancing last_lr; a review that writes candidates without advancing last_lr must name the miss in its PROCESS self-audit section — the self-audit section is the enforcement surface",
  "extends": ["SN-1759"],
  "falsifier": "a review that skips the watermark advance with zero consequence would refute the rule: if the 13:20Z reconstruction had found SN-1760/1761/1762 uncounted or double-counted, the reconstruct-and-repair recovery would have failed its own check and the rule would be wrong; alternatively, if reviews become content-idempotent (counts keyed by content hash instead of windows), watermark-atomicity is unnecessary machinery",
  "mechanism": "the watermark is the claim token for a window: filing without advancing leaves a window whose claim state is ambiguous to the next pass (claimed-but-unwatermarked vs unclaimed are indistinguishable). reconstruction from the evidence file (the review's own events file) re-derives the claimed window; the once-counted verification against the ingestion log is the idempotency guard that makes repair safe instead of another blind filing",
  "decision_change": "the next hourly review opening on a stale last_lr: reconstruct from the gap's events file and verify once-counted before advancing, instead of trusting the gap is unclaimed or re-filing blindly. without this, the next review double-counts SNs or silently trusts a claimed-but-unwatermarked window",
  "evidence": {
    "process_note": "hidden_files/learning-events-2026-10-21-13.md PROCESS section (2026-10-21 13:20Z)",
    "gap_file": "hidden_files/learning-events-2026-10-21-12.md (window 2026-10-21T11:20:19Z->2026-10-21T12:20:19Z, 3 notes SN-1760/1761/1762, 1 receipt)",
    "repair": "shared-state.json learning_review_20261021_1220 + learning_review_20261021_1320 (both watermarks repaired this run)",
    "no_double_count": "SN-1760/1761/1762 each verified counted exactly once before repair"
  },
  "rule": "a review's filings and its watermarks are one atomic claim: advance last_lr and write the shared-state block in the same pass that files candidates; on a stale watermark with a gap events file, reconstruct from the file and verify once-counted before advancing"
}
```
