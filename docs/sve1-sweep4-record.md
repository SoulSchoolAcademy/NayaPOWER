# PROVENANCE (added by Naya Mu, wave 33, 2026-10-13)

The record below is the EXACT sweep-4 record referenced by the PR body's
"evidence-of-use" claim, copied byte-for-byte from the collector's local file
(no edits below this line). Source on the collector's machine:

`hidden_files/areas/mu-value-sweep-4-20261013T0226.md`
(workspace: `~/workspace/goals/super-brain-engine-to-10-10/`)

---

# SVE-1 Fourth Sweep — the aging window (2026-10-12 21:43:00Z → 2026-10-13 02:27:12Z)

**Collector:** Naya Mu (Human Value lead), lane 2 / #1714 · night-shift wave 28
**Instrument:** `hidden_files/areas/mu-value-instrument-1-20261012T2145.md` (SVE-1 spec) + first working capability below
**Receipt:** this file · sign-in #1714 comment 6136864313
**Calibration banner:** formative — not yet independently calibrated.
**Briefing proof:** recorded 02:25Z (fp 7eb3485a…, file-based challenge, verify exit 0)

---

## 1. THE COUNT

| Window (UTC) | STATED (new) | Status |
|---|---|---|
| 2026-10-12 21:43:00 → 2026-10-13 02:27:12 | **0 units — clean NULL sweep, all three channels** | **SWEPT** — window closed |

**Standing record after this sweep:** 3 MEASURED + 1 CORRECTED confirmed + 1 correction-class observed + 1 dropped phantom + 6 PROVISIONAL + **2 NULL windows**. Ledgers never netted.

### Coverage proof (demonstrably complete, not my confidence)

- **C2 — daily logs (local, 0 API):** `~/memory/2026-10-12.md` lines **3841–4184** (344 lines, the tail past sweep-3's 3840 boundary) + `~/memory/2026-10-13.md` lines **1–134** (full file). Full attribution-pattern scan (`Shawn said/told/asked/directed/ordered/approved/gave/established/stated/pasted/affirmed/described/reported`, `Shawn: "`, straight + curly quote spans) → **0 hits**. Raw line dumps saved at `/tmp/mu-sweep4/c2-1012-tail.txt`, `c2-1013.txt`.
- **C1 — team feeds (API):** since-filtered comment pulls on all six feeds → **95 comments in-window** (#2154: 3, #1713: 26, #1714: 15, #1715: 16, #2471: 18, #2472: 17). Bodies fetched with the list responses — zero per-comment GETs. Pattern scan for Shawn attribution → **0 hits**; every Shawn mention is seat-referential ("needs from Shawn", "Shawn's word", "operator = Shawn") — never his own utterance. Independent corroboration: #2471 comment 6133970394 (a seat's own wave note) reads "19 comments, all worker sign-ins/sign-outs, 0 Shawn-authored" — same verdict, different count (earlier time).
- **C3 — repo main:** tip re-resolved via git protocol = `dd6f2d927d82` — the #2459 merge commit, **unmoved since 00:13:46Z**. One merge inside the window: **#2459 merged 00:13:46Z by the dock** (Naya 5 executed via git-database API after 5/5 live re-verification — see `~/memory/2026-10-13.md` director pass). Zero Shawn-merge agency: he clicked nothing. Conflict rule: dock-executed lawful merge, no human-attributed agency to adjudicate.

### Adjudication notes (why the tempting items are not units)

1. **The 00:15Z "Verified extraction" block** (daily log): four quote spans ("It's done. PR #2459 just merged…", "The B-51 fix is built…", "B-51's backfill is executed…", "I got one wrong…") — sources are `message:assistant-msg-*` (Naya 5's own nightly-report messages). Authorship = seat, not Shawn. The REPORTED SPEECH rule needs colon-attribution TO him; these carry none. → side ledger (uncertain), never counted.
2. **Delta's W8-001/002/003 status correction** (10-12 tail, L172: "MEASURED, not provisional"): seat-reported metadata about earlier-window events, not a new Shawn statement. Recorded; not an SVE candidate.
3. **Recounted pre-window quotes** (W8 spans, "word!", the six provisionals): appear as seat recounts in the tail — dedupe-by-content against sweep-3; no new utterances.

---

## 2. INSTRUMENT INCREMENT — sve1.py `extract` (works, tested, committed)

Branch `naya-mu/sve1-extract` @ `f565fb0fe` (worktree `~/workspace/goal-scratch/mu-sve1/`), implementing spec §7 step 1:

- **`tools/human_value/sve1.py` — `extract <logfile>`**: quote-span extraction + classification (verbatim / reported / paraphrase / uncertain) + sha256 content-hash dedupe. JSON and md output. Mechanical rule copied verbatim from the spec.
- **Honest boundary, named in the docstring:** the tool cannot distinguish "original bytes" from "recalled bytes," so ALL colon-attribution from seat-authored sources lands as `reported` (authorship=inferred). Extraction is mechanical; MEASURED/PROVISIONAL adjudication stays a seat judgment.
- **Dogfooded on this window:** ran on both C2 files → **0 candidates**, matching the manual sweep exactly.
- **`tests/test_sve1_extract.py` — 6/6 green** (colon→reported, clause→verbatim, paraphrase→side-ledger, unattributed→uncertain, dedupe across lines, empty window = clean exit 0).
- NOT built (named next): `count <window>`, `re-read <event-id>`, a C1 comment-JSON channel adapter, the v1 §5 known-answer battery, push + PR of this branch.

## 3. D32 — What this sweep does NOT claim

- That the window held no human value — the team's night was loud (hold drained, backfill executed, validator rehearsed). SVE-1 measures stated value, not effort; silence is NULL, not zero.
- That the 6 PROVISIONAL events are closer to resolution — still awaiting different-seat re-read of the chat bytes. Mu cannot satisfy this (P-005); the queue is named, not moved.
- That C1 covers everywhere Shawn could have written — six feeds only; a non-lane thread comment would be invisible (named limitation, unchanged).
- That sve1.py's classifications are adjudications — it emits candidates; the instrument's rules decide.

## 4. SELF-SCORE (triple validation)

- **Round 1 — 8.0:** API governor breached 18/10 (see §5); extract is files-only; branch unpushed.
- **Fix:** committed 6 tests (dogfooded, 6/6 green); flag-trap lesson broadcast to the hive (§5); next actions named precisely.
- **Round 2 — 9.0:** remaining gap — the provisionals' re-read is external to this seat; the sweep's honest ceiling.
- **Round 3 — 9.0:** the increment is real and verified (mechanical, tested, byte-matched against the manual sweep); the ceiling holds at the external dependency, not the work.

## 5. WIN-WHY (Every-Failure-Every-Win Law)

**Win:** the instrument's first capability exists and is proven against real data — sve1.py extract ran on this window's actual bytes and produced exactly the manual sweep's answer (0 candidates), and its 6 tests pass. **Why it worked (the mechanism):** extraction was specified as pure mechanics in the spec, so the builder had nothing to invent — the judgment stayed with the seat, the bytes stayed with the tool. Separation of extraction from adjudication is what made it testable.

**Failure (owned):** API governor breached — **18/10**. The gh-api wrapper silently ignores unknown flags: 11 calls (`--since`/`--per_page` on 11 GETs) returned the default oldest-30 page each; I only caught it because every feed returned exactly 30 and I checked timestamps instead of trusting the count. Fix-forward (mechanical): query params embedded in the PATH (`GET ".../comments?since=...&per_page=100"`) — verified working this wave. Broadcasting to the hive.

## 6. NEXT ACTION (exactly one)

Push branch `naya-mu/sve1-extract` and open the PR for different-seat validation (the One Gate path needs a scorer); on the same pass, hand the 6 PROVISIONAL events' byte-hunt to the next rotation seat with P-005 naming.
