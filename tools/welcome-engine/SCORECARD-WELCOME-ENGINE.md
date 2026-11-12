# The Welcome Engine — scorecard loops (Naya Power, SET B, 2026-10-24)
**Shawn's process, run as ordered: score -> why not 10 -> where's the bottleneck -> the 10x -> deliberate -> plan -> apply. Three times. All state tracked in Project Intelligence (item build-welcome-flow-engine); this file is the narrative, the item is the record.**

## Loop 1 — the spine: **6/10**
Built `welcome_engine.py`: answers -> slots (Questions V2 destination map) -> vector -> Trinity pages (verbatim, "not yet shared" never invented) -> coverage accounting -> ambassador link issuance -> first matches, as ONE deterministic `activate()` call. 7/7 tests.
**Why not 10 (found by running a realistic citizen through it):** a gardener citizen ("urban gardening, composting, teaching kids to grow food") matched her obvious space at only **20%** — the matcher's phrase-level math couldn't see her free vocabulary. Also: conversational lead-ins polluted phrases ("I love gardening"), coverage counted a one-word answer equal to a rich one, no findability gate inside the engine, and the matcher's SQL twin was still v1 math.

## Loop 2 — the 10x fixes: **8/10**
Deliberated: the bottleneck was vocabulary distance, not weights. Applied:
- **Matcher v1.3 — the word tier**: topics/goals raw score now blends phrase overlap with content-word overlap. Gardener -> her space **20% -> 35%** with clean reasons (composting, gardening, teaching); canonical corpus holds (P->NayaPOWER 55, N->Team Nitro 62).
- Lead-in stripping; **filled_thin** coverage state (thin answers count, and are named as follow-up candidates); **findability gate inside activate()** (unfindable corpus entries excluded + counted in the receipt); honest `match_note` when nothing surfaces; explicit business-branch handling. 11/11 engine tests, 9/9 matcher tests.

## Loop 3 — completion polish: **8.5/10**
- **SQL twin regenerated to v1.3 math** (`smart_match_v1_3.sql` — phrase/word/concept functions mirroring the Python; marked NOT deployed).
- **Demo receipts** for two synthetic citizens (full + sparse): the sparse citizen's coverage names every missing field — the accounting works hardest exactly where the answers are thinnest.
- Full suite green: 20/20 tests across both files.

## What still stands between here and 10 — named, not hidden
1. **The joining is not live**: the walk's completion event (interface lane) doesn't fire `activate()` yet; deployment of the SQL twin rides the same wiring. Engine-ready != citizen-live, and this scorecard doesn't pretend otherwise.
2. **Weights are still prototype-born (40/25/20/15)** — calibration needs real citizens' answers and outcomes; no honest shortcut exists.
3. **Extraction is heuristic** (phrase splits + governed taxonomy) — deliberate: deterministic-first economics. A semantic layer is a v-next candidate, admitted only with evidence it beats the deterministic floor.
4. **Nitro's independent scorecard of this engine is outstanding** — requested by mail; by our law, my 8.5 is a claim until her eyes land on it.

## Loop 4 — the golden set: **9.0**
Shawn's correction landed mid-loop: three was the minimum, not the target — the standard (already in the system) is **minimum 9, goal 10, love anything over 9.5; loop until you hit it.**
Built the **Golden Set** — 13 labeled expectations from the record + obvious-answer synthetic citizens — and it caught a real one: a wants-only chess citizen scored 17% but never surfaced ("chess partners" couldn't see "chess" — the cross scores had no word tier). Fixed: stemming (garden/gardens/gardening unify) + word tier in cross scores with a glue-word stoplist. Receipt completed to the full activation object: **SN-0852 settings bound per page + the citizen's own corpus entry emitted**. Golden set: **12/12** (one informational: Resolve->Mirror 20%, one signal — declaration depth, unchanged and owned).

## Loop 5 — calibration + hardening: **9.5** (the artifact)
- **Calibration harness** (`calibrate.py`): swept the weight grid over the golden set. The Lock Packet's 40/25/20/15 gets **every decision right**, tied with the best grid points; two neighbors show +3.3 margin by shrinking `wants` to 0.05 — thin evidence against a deliberate design weight, so **the weights stand** and the harness output is filed as the evidence packet. No silent retunes, ever.
- **Edge hardening**: emoji/punctuation, 30x-repeated long answers, stopword-only answers, empty corpus — 14/14 engine tests, 9/9 matcher tests, all green.
- **Scale measured**: ranking one citizen against a 1,000-citizen corpus = **54 ms**. Observed property, stated plainly: in a dense corpus the 2-signal bar surfaces many — ranking + a capped reveal is the mitigation, by design.
**Residuals (delivery, not artifact):** the live joining (walk-completion wiring + SQL v1.4 deployment) and Nitro's independent scorecard. By the network rule, the FLOW earns its own number when those land; the engine artifact stands at 9.5 on the evidence above.
