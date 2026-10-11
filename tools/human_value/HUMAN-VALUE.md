# Human Value — the change-grade instrument (companion to the event ledger)

**Naya Mu · Human Value area · 2026-10-11**
**Status:** v1 — the change-grading companion of the human-value observatory.

## 0. Premise correction (read first)

This instrument is **not** the first human-value instrument. When I started,
the mission brief said "build the FIRST measurement instrument" — but the
live repo already holds a mature one: `tools/human_value/` on main
(`compute_hv.py`, `schema.py`, `real_outcome_loop.py`, 12 iterations,
92 real events, cold-recompute proofs).

Building a second, competing instrument would have been duplication —
exactly what the operating law forbids. So this is the **companion**:

| | Event-ledger instrument (existing, main) | Change-grade instrument (this file) |
|---|---|---|
| **Asks** | Did a human's life get measurably better, over time? | Was *this shipped change* valuable, with evidence? |
| **Unit** | A value event (outcome observed) | A change packet (diff shipped) |
| **Output** | HV/day, DAI/day, calibration vs predictions | A graded scorecard: 0–10 + verdict + why-not-10 |
| **When** | When outcomes are observed | At ship time (merge) |

**How they compose:** a scorecard graded REAL VALUE or higher can be exported
(`instrument.py to-event`) as a schema-valid ledger event — validated against
the existing `schema.py`, never hand-rolled. The change grader is an
*evidence supplier* to the event ledger, not a competitor. THIN and below
mint **no** event: the instrument refuses to manufacture value-credit.

## 1. What "human value" means (plain language)

**Human value is real help for real people — or a real improvement to something that helps real people — that you can point to and prove.**

It answers one question:

> **Did this actually help somebody — or did it just look busy?**

Three tests. A change has human value only if it passes all three:

1. **Someone can use it.** If nobody can use what you shipped, it isn't valuable — it's decoration. (Shawn's Usefulness Gate: *"If it's not useful, it can never be used. If you wouldn't give it to the world, don't give it to me."*)
2. **The number moved up.** Every action must leave things better than it found them. Activity is not value; value is the *difference* you made. (Shawn's 70% Commitment: every action must move the numbers UP. Busy work is not work.)
3. **You can prove it.** A claim without evidence is a story. Human value is *measured*, not asserted. Every judgment in this instrument must point at something checkable: a file and line, a test run, a SHA, a command with its output. (D32: no claim exceeds its evidence. A number without provenance is a lie with formatting.)

And one hard law, above everything else:

> **A human being is never the thing being measured.** This instrument measures the value of *actions*, never the worth of *people*. Human life and dignity are beyond price — they are not numbers here, not ever. (Human Invaluable Principle: human life and dignity are invaluable, never assigned numerical worth.)

**Child version:** *"Did it really help someone — or just look like work? And can you show me how?"*

**Grandma version:** *"It's only worth something if somebody can actually use it, things got genuinely better because of it, and you can show me the proof — not just tell me about it. And we never, ever put a price tag on a person."*

---

## 2. The rubric (v1)

A shipped change is graded on five dimensions. Each gets a score from 0 to 10.

| # | Dimension | The question it asks | Weight |
|---|-----------|----------------------|--------|
| 1 | **USE** | Can a real someone actually *use* what this shipped? Not "could, in theory" — who uses it, and for what? | 30% |
| 2 | **DELTA** | Did a real number move **up** because of this change? What was it before, what is it now? | 25% |
| 3 | **PROOF** | Is every claim backed by checkable evidence — file and line, test output, SHA, command? | 20% |
| 4 | **DURABLE** | Will this still be true tomorrow? Or does it rot, expire, or need constant re-doing? | 15% |
| 5 | **CLEAN** | Did it leave the place better than it found it — no new breakage, no rot, no hidden debt? | 10% |

**THE HARM GATE (checked first, binary).** Does the change harm anyone, break something that was working, or weaken a protection? If **yes** → the change is **DISQUALIFIED**. It gets no score. Harm is not a minus — harm means the change does not qualify for consideration at all. (Briefing law: *"Harm has zero value. Not negative. It's not in the decision matrix at all."*)

**The evidence rule (the instrument enforces this mechanically).**
- A dimension score **above 5** must cite at least one *verified* piece of evidence (a file that exists at the change's ref with the cited lines, a real SHA, a real test file). Otherwise the score is capped at 5 and flagged `UNCITED_CAP`.
- A dimension score **above 3** with *no evidence at all* is capped at 3 and flagged `NO_EVIDENCE_CAP`.
- Attested evidence (a command someone ran, a URL, another worker's report) counts as evidence — but is marked *attested, not verified*, so the reader knows whose word it rests on.

**Final score:** the weighted sum, one decimal place. Then the verdict:

| Score | Verdict | Meaning |
|-------|---------|---------|
| ≥ 9.0 | **HIGH VALUE** | Ship it to the world with pride. |
| 7.0 – 8.9 | **REAL VALUE** | Genuinely useful. Honest gaps noted. |
| 5.0 – 6.9 | **THIN** | Mostly activity. Ask: who is this for? |
| < 5.0 | **NO VALUE** | Busy work. Don't ship it — fix it or drop it. |
| — | **DISQUALIFIED** | Harm found. Never ships. |

Every scorecard also answers **"why not 10?"** — the two weakest dimensions and every flag, in plain words. The instrument grades the change; the "why not 10" tells the builder what to fix next.

---

## 2b. v2 hardening — what the full 28-change run taught us

Three fixes, each proven on real data before shipping:

**F1. Receipts as first-class evidence** (the attested loophole, closed one level up).
The full run confirmed the pilot's finding at scale: real deltas live in lane-feed prose, not in the repo. The new evidence kind `receipt` is a machine-readable JSON file committed WITH the change (`receipts/<change-id>.json`, template from `instrument.py receipt-template`). The instrument verifies it mechanically: exists at the ref, parses, holds before/after metrics. Receipts are verified-but-soft evidence: they carry a judgment up to 8 (flagged `RECEIPT_SOFT_CAP` above that). A committed claim is checkable; it is still the grader's own claim, not an independently re-runnable test. The 8.0 cap is asserted, not calibrated — say so when asked.

**F2. Second-seat grading** (`instrument.py compare --a A.json --b B.json`).
Two seats grade the same change; `compare` reports per-dimension gaps in agree / review / dispute bands and checks verdict agreement. Disagreement is made visible, not averaged away. Real-data proof: two seats independently graded #2376 (mission-state docs) at 5.3 and 5.5 — every dimension in the agree band, same verdict. Note the honest limit: both seats share this rubric, so correlated judgment is reduced, not eliminated.

**F3. The durability loop** (`instrument.py recheck --scorecard C.json --repo R --ref <later>`).
DURABLE was a prediction at grade time, never re-checked. Now every scorecard carries a `durable_check_due_utc` (7 days out); `recheck` re-verifies every cited piece of evidence at a later ref: HELD / ROTTED / MIXED per dimension, plus content-drift detection (the cited lines still exist but say something different — the exact way regenerated brain indexes "rot"). Real-data proof: pilot scorecard #2384 rechecked at the live tip → 5 held, 0 rotted, **2 content-drifted** (both the regenerated index files), reading "DURABLE prediction partly rotted". Honest limits, stated here: attested evidence (commands, URLs) is NOT_RECHECKABLE — the most important DELTA claims still can't be re-run by the machine; and recheck reports, it does not re-score — a rotted DURABLE doesn't auto-downgrade the grade, it asks a human to look.

**Mechanical fix:** pre-merge branch heads now diff against `merge-base(origin/main)` instead of `head^1` — the pilot run showed `^1` understating branch deltas (the sweep branch's 12-file substance hid behind a 3-file tip commit).

---

## 3. What this instrument is and is not

**It is:** a ruler for shipped changes. It turns "was this valuable?" from a feeling into a graded, evidenced judgment — the same shape every time, checkable by anyone.

**It is not:**
- A judge of people. It grades *changes*, never humans.
- A replacement for human judgment. It *structures* judgment and enforces the evidence rule; the scores themselves are a grader's honest call.
- A proof of real-world benefit. For infrastructure work, it measures *proximal* value (usable tooling, real tests, working gates) as a proxy. Whether Shawn's life actually got better is a question this v1 cannot answer — see the pilot report's honest weaknesses.
- Self-verifying. A grader can write a beautiful packet about a useless change. The instrument catches invented file citations (it checks they exist), but it cannot catch inflated claims about what a change *does*. Independent second-seat grading is still the gold standard.

**Machine note:** `tools/human_value/instrument.py` implements this rubric. Packet schema v1. `score` grades a packet; `pilot` builds a packet skeleton from a merge SHA; `to-event` exports a REAL VALUE+ scorecard as a schema-valid ledger event (validated by the existing `schema.py`); `compare` runs second-seat agreement; `recheck` runs the durability loop; `receipt-template` emits the receipt schema. Malformed input fails safe (exit 2, no score emitted — never a number without a valid packet).
