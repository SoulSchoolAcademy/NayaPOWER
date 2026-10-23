Intelligent Block
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-23
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

The distillation job's budget-law cheap check compares shared-state `issue_1354_comments` — a COUNT (2500, the GitHub hard cap) — against the board watermark, which holds comment IDs (~6201802368). A count and an identifier live in different unit spaces, so `2500 <= 6201802368` is a tautology that always reads "skip": the check costs a read and proves nothing, and it would keep reading "skip" forever even if #1354 were re-enabled and new comments poured in. The honest skip signal already exists in the same file: `issue_1354_comments_disabled: true`, with reason "GitHub hard cap: 2500 comments; commenting disabled by GitHub 2026-10-10 ~12:21 PDT (issue not locked)". The rule: cheap checks must compare within one unit space, and when a semantic flag answers the question ("can new comments exist?"), use the flag — never a cross-unit inequality. Correlated hygiene on the same evidence: the watermark file is an append-only log (2026 lines, 2 duplicate IDs — 6101230756 re-appended at line 2025 after appearing at line 1340; 6201802368 appearing twice), not a sorted unique set; only the last line is load-bearing, so no step may rely on ordering or uniqueness.

## 🩷 HUMAN NOTE

Shawn — a shortcut in the distillation loop looks like it's checking for new board comments, but it's actually comparing two things that can't be compared: a count (2,500, the GitHub ceiling) against a comment ID (in the billions). That comparison will always say "nothing new" — today by luck it gives the right answer, because GitHub disabled commenting on that board back on October 10th. But if commenting ever comes back, the loop would never notice new comments. The honest signal is already sitting in the same file: a flag that says commenting is disabled. The fix is to read the flag, not the fake comparison. Same family of lesson: the watermark file is an append-only log with a couple of duplicated lines in it — only the last line means anything, so nothing should treat it as a tidy unique list.

## 🟣 CHILD NOTE

Imagine deciding whether the mailbox has new mail by comparing the number of letters you've ever received (2,500) with the serial number on the last letter (6 billion). The serial number will ALWAYS be bigger, so the rule will ALWAYS say "no new mail" — even after the postman delivers a whole new batch. The right check is much simpler: is the mailbox locked? There's a tag on the box that says "locked by GitHub." Read the tag, not the numbers.

## 🔵 GRANDMA NOTE

It's like checking whether the store got new deliveries by comparing "we've sold 2,500 items total" with "the last receipt number was six billion." The receipt number will always be bigger, so you'd conclude "no new deliveries" forever — even after a truck unloads. The correct check is the sign on the door: "deliveries suspended." Read the sign.

## 🟠 NAYA NOTE

Identifiers and counts are incommensurable: an identifier is a name in an arbitrary monotonic namespace, a count is a bounded quantity of a resource. Any comparison across that boundary yields a constant, not a signal — and a constant masquerading as a check is worse than no check, because it suppresses the real decision path. The discipline is unit hygiene on loop guards: every cheap-check comparison must operate within one unit space, and wherever the system already maintains a semantic flag for the underlying question ("can new comments exist?" — `issue_1354_comments_disabled`), the flag IS the cheap check. Same file, same hygiene: the watermark is an append-only log with duplicate re-appends (2 duplicate IDs across 2026 lines, non-monotonic); only its last line is load-bearing. Treat append-logs as logs — last line is the marker, never assume ordering or uniqueness.

## 🟢 MACHINE NOTE

```json
{
  "slug": "sn-1870-cheap-check-unit-hygiene",
  "lesson": "The distillation job's budget-law cheap check (step 3) compares shared-state `issue_1354_comments` — a COUNT (2500, GitHub's hard comment cap for the issue) — against the board watermark file, which holds comment IDs (last 6201802368). A count and an identifier live in different unit spaces: `2500 <= 6201802368` is a tautology that always reads 'skip'. The check costs a read and proves nothing, and it would silently suppress the fetch path forever if #1354 were re-enabled with new comments landing. The honest skip signal already exists in the same file: `issue_1354_comments_disabled: true` with reason 'GitHub hard cap: 2500 comments; commenting disabled by GitHub 2026-10-10 ~12:21 PDT (issue not locked)'. Rule: cheap checks must compare within one unit space; when a semantic flag answers the underlying question ('can new comments exist?'), the flag IS the cheap check — never a cross-unit inequality. Correlated hygiene from the same evidence: smart-notes-board-watermark.md is an append-only log (2026 lines, 2 duplicate IDs: 6101230756 re-appended at line 2025 after first appearing at line 1340; 6201802368 appears twice), not a sorted unique set — only the last line is load-bearing, so no step may rely on ordering or uniqueness.",
  "applies_when": ["budget", "governor", "loop", "cheap-check", "watermark", "issue_1354", "failure:silent-skip", "unit-hygiene", "distillation"],
  "enforcement": "Retire the count-vs-ID comparison from the distillation job body: the fetch/no-fetch decision reads `issue_1354_comments_disabled` in shared-state.json as the flag, with `issue_1354_comments_disabled_reason` as the audit trail (currently: 'GitHub hard cap: 2500 comments; commenting disabled by GitHub 2026-10-10 ~12:21 PDT'). Any future cheap-check comparison added to a loop body must operate within one unit space — enforced by a review step that names both operands' units in the job body's own text. Acceptance test: with the flag true, no fetch (current behavior, now for the right reason); with the flag flipped false and a watermark below live IDs, the fetch path must trigger. Separately: no consumer of the watermark file may assume monotonicity or uniqueness — the last line is the only load-bearing value.",
  "evidence": [
    "shared-state.json (read this tick): issue_1354_comments=2500; issue_1354_comments_disabled=true; issue_1354_comments_disabled_reason='GitHub hard cap: 2500 comments; commenting disabled by GitHub 2026-10-10 ~12:21 PDT (issue not locked)'",
    "hidden_files/smart-notes-board-watermark.md: last line 6201802368; 2026 lines total, 2024 unique (duplicates: 6101230756 at lines 1340 and 2025; 6201802368 twice) — append-only log, non-monotonic, not a set",
    "Job body budget law step 3 as written: 'if shared-state issue_1354_comments <= your board watermark → SKIP' — compares a count against an ID namespace; with IDs in the billions the inequality is a constant 'true'",
    "GitHub /search/code: no existing Smart Note covers 'cheap check' semantics (only SN-033's collision-registry mention) — new ground"
  ]
}
```
