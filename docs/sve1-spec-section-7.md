# PROVENANCE (added by Naya Mu, wave 33, 2026-10-13)

The section below is the EXACT text of SVE-1 spec §7, referenced by the PR body
("spec: `hidden_files/areas/mu-value-instrument-1-20261012T2145.md` §7 step 1"),
copied byte-for-byte from the spec's local file (no edits below this line).
Source on the collector's machine:

`hidden_files/areas/mu-value-instrument-1-20261012T2145.md` §7
(workspace: `~/workspace/goals/super-brain-engine-to-10-10/`)

---

## 7. First implementation steps (builder-sized, not today)

1. `tools/human_value/sve1.py` — `extract <logfile>` (quote-span extraction + verbatim/paraphrase/uncertain classification), `count <window>` (SVE report with the §5 shape), `re-read <event-id>` (different-seat verification workflow). The mechanical extraction rule (so the builder doesn't reinvent it):
   - Scan each source line for **quote spans**: (a) `Shawn:` + quoted text (colon-attribution); (b) quoted text with an attribution clause in the same line ("he said", "Shawn said", "he called Naya… said"); (c) bold-quoted or marker-matched tokens (authorship-marker hits).
   - **Classification per span:** quote marks present in the source bytes → `verbatim`; seat-authored restatement without quote marks → `paraphrase` (side ledger, never counted); colon-attributed quotes recalled from chat-turn memory → `reported` (counts, authorship `inferred`, stays provisional until chat bytes are pinned).
   - **Dedupe:** sha256 of normalized quote text across lines and channels — the same sentence appearing in C1, C2, and MEMORY.md is 1 unit.
   - ~150 lines.
2. Wire wave-9 sweep to include the 15:13Z–now ABSENT window (four named candidates in §4 are its opening material).
3. Run v1 §5's known-answer battery over the 2026-10-11→12 window with the answer key pre-registered before the run — no peeking.
4. Lift the calibration banner only when: exact keyed match, inter-collector agreement ≥ 0.8, Coda 1 adversarial probes all blocked.
