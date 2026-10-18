# PRE-REGISTRATION — t0842 long-text regime probe (filed BEFORE authoring/run)

**Regime parameter:** LENGTH_FLOOR = 80 words per doc. (Killed regime: docs median
7 words, max 17 — the probe regime is 4.7x the max, a stated, falsifiable floor.)

**Control held constant:** the delta=2 band ov(g,q) < ov(d,q) <= ov(g,q)+2 per
(query, distractor) — the discrimination mechanism, NOT the variable under test.
The brief forbids re-dialing delta; the band is frozen as the control and length
is the independent variable. Query texts reused verbatim (the instrument).

**Design:** 4 queries (pq01 calib/hosting, pq03 accept/fourteen, pq07 calib/feeder,
pq09 accept/merge) x (gold + 5 distractors). Each long doc is an ELABORATION of
the killed pilot's short doc (same core claim, same stem profile) — paired at the
doc level. SHORT baseline = the same 5 distractors' margins from the killed pilot,
recomputed with the battery's own _embed/_cos (paired comparison, no confound).

**Hypothesis H:** longer texts give the t0426 bi-encoder's paraphrase geometry room
to overcome the 1-2 stem deficit -> LONG margins rise vs SHORT margins; queries
cross zero.

**Falsification (weakest reading, filed before the run):**
- F-A: median(LONG margins) <= -0.15 (killed pilot acceptance median was -0.2225;
  -0.15 is the no-material-move line) -> REGIME FALSIFIED.
- F-B: zero of 4 LONG margins > 0 -> no query crosses zero -> REGIME FALSIFIED.
- F-C: median(LONG - SHORT paired delta) <= +0.05 -> length does not move the arm
  -> REGIME FALSIFIED (strongest: the paired test).

**What CONFIRMS (partial):** median paired delta > +0.10 with >=1 margin crossing
zero -> the regime moves the arm; a full 12-query battery brief is justified.

**Blinding:** no semantic-arm scores viewed during authoring. The band check is
mechanical (v3_toks/overlap_lex), never semantic. Margins computed ONCE, after
all 24 docs are frozen.

**Why a probe, not the full 12-query battery (filed in the receipt):**
(1) Rate math: 114 long docs x 80+ words is unauthorable in a 40-min slice
(verified, not assumed). (2) The brief's "different arm" option is incoherent
through run_pilot12_battery.py: margins and the section-3.1 gate are computed by
the battery's own _embed (all-MiniLM-L6-v2, replicated verbatim from arm.py) —
a swapped arm changes P1 but cannot move the margins or flip the pin verdict.
The probe tests the only coherent variable (length) with a paired design.
