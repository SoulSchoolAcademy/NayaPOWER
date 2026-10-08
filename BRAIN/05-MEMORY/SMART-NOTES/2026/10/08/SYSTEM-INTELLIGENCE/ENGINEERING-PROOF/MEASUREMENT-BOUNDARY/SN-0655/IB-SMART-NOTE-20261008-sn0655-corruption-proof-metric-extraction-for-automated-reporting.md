# IB-SMART-NOTE-20261008-sn0655-corruption-proof-metric-extraction-for-automated-reporting.md

Intelligent Block: SN-0655
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-08
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

When a machine extracts scores and metrics from human/agent-written text for automated reports, bake anti-corruption rules into the extractor — caught live during the build, not theorized: (1) area and score must share one sentence or the claim is dropped; (2) sentences covering multiple areas are skipped, not split; (3) movement beats prefix — "re-score: 8.5 → 8.8" means 8.8; (4) an authoritative status is never downgraded by a heuristic claim; (5) degraded sources render as UNAVAILABLE, never silently dropped.

## HUMAN NOTE

Naya 5 built the automated reporting system (morning/hourly/nightly reports from live data: worker logs, memory, GitHub read-only, Supabase SELECT-only). While wiring the score extractor, she caught four live corruption patterns that naive regex parsing would have shipped:

1. **Detached score attribution** — a score floating in a sentence without its area name attached. Rule: area + score must share a sentence, else the claim is dropped. No cross-sentence guessing.
2. **Multi-area sentence smearing** — one sentence mentions two areas and one number. Rule: skip the sentence entirely. Splitting a shared number across areas manufactures data.
3. **Prefix blindness** — "re-score: 8.5 → 8.8" naively parses as 8.5. Rule: movement beats prefix; the arrow's target (8.8) is the score.
4. **Heuristic status downgrade** — a heuristic labeled an authoritative score as a mere claim. Rule: authoritative status is never downgraded by heuristic claims; provenance outranks pattern-matching.

Plus the source-discipline rule: every item carries its source; a degraded source renders as "unavailable," never silently disappears. A report that quietly drops what it couldn't read is lying by omission.

## CHILD NOTE

When a robot reads people's words to count their scores, it has to be very careful not to mix things up: only count a score if the name of the thing being scored is in the same sentence, skip sentences that talk about two things at once, read the arrow's end not the beginning, and never guess something important is less important than it really is. And if it can't read something, it must say "I couldn't read this" — never pretend it wasn't there.

## GRANDMA NOTE

Shawn's team now gets automatic reports written by a machine that reads everything the team writes and pulls out the numbers. The danger: the machine misreading a sentence and reporting a wrong score as fact. So the rules are strict — the machine only trusts a number when the label sits right next to it, skips confusing sentences, reads updates as the new number, respects officially-stated numbers over its own guesses, and openly admits when something couldn't be read instead of quietly leaving it out.

## NAYA NOTE

This is measurement-boundary discipline (engineering-proof family) for the specific hazard of LLM/agent-text metric extraction — a recurring cold-successor trap, because the extractor looks "done" the moment it returns numbers. The extractor shipped with 29/29 pytest green on `tools/reporting/`; the tests encode the anti-corruption rules, so the rules are machine-checked, not documented-wishes.

Design checklist for any future score/metric extractor in this system:
- Co-location rule (area+score same sentence) as a hard filter, not a heuristic weight.
- Skip > split for ambiguous sentences.
- Temporal/latest-wins parsing for movement notation.
- Provenance hierarchy: authoritative status pins are immutable to the extractor.
- Degraded-source rendering: every metric carries `src:`; unreadable sources appear as "unavailable" with the reason (e.g., "Supabase 401 — credentials gate, not reporting's to fix").

Relevance: the morning/hourly/nightly reports (06:00 / 08:00–22:00 / 23:00 UTC) are Shawn's standing consumption surface — a corrupted number there propagates into his decisions. Extractor integrity is a trust-contract surface (SN on the Autonomous Operating Model: if a claimed 9.0 doesn't feel like a 9.0, trust breaks).

## MACHINE NOTE

{"sn": "SN-0655", "title": "Corruption-Proof Metric Extraction for Automated Reporting", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-08", "source": "#1354 comment 6053109026 (Naya 5, 2026-10-08T05:35:12Z); branch naya5/automated-reporting; 29/29 pytest green", "rules": ["colocation_area_score", "skip_multi_area", "movement_beats_prefix", "authoritative_status_immutable", "degraded_source_renders_unavailable"], "report_surface": ["06:00 UTC morning", "08:00-22:00 UTC hourly", "23:00 UTC nightly"]}
