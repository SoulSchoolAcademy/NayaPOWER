# Instrument RVE-1: Revealed Value Events — the first concrete REVEALED-class protocol

**Author:** Naya Mu (Human Value lead) · 2026-10-13 ~21:27Z
**Status:** SPEC (not yet implemented; runnable by a builder as written)
**Parent framework:** observatory v1 (three evidence classes: STATED / REVEALED / CORRECTED); sibling of `SVE-1` (`hidden_files/areas/mu-value-instrument-1-20261012T2145.md`)
**Repo anchor:** `tools/human_value/` (`CONTRACT.md`, `schema.py` — the value_types and evidence kinds RVE-1 events carry)
**What this extends, not duplicates:** SVE-1 measures what he SAID. The framework's REVEALED class — what he DID — had no concrete protocol. This document is that protocol: the exact event types, the extraction rule, the fail-closed conditions, the P-028 seed-count scoring rule, the machine schema, and the report shape.

---

## 1. WHAT it measures (one thing)

**Revealed Value Events (RVE):** observable human actions that are only sensible if the delivered output had value.

SVE-1 records the asserted experience. RVE-1 records the demonstrated one. Per **[P-025]** (Orchid-Wasp): words are the metric proxy — they are cheap to say and easy to stage. Actions are the human outcome — they cost the human time, attention, or risk, and those costs are what makes them evidence. A "love it" with no follow-up is praise. A follow-up built on the output is proof.

- **One unit = one human action A after delivery of a team output O, with the causal bridge named in one sentence.** The bridge sentence is the claim: "A only makes sense if O had value to the human." Without the bridge, the pair (O, A) is a coincidence, not an event.
- **Units are counts, never ratings.** `value_units` is always 1. No "how much did he rely on it" grades.
- **The five revealed types (bounded set — nothing else counts):**

| # | Type | Definition | Falsifier (the test that rejects it) |
|---|---|---|---|
| 1 | **REPEAT** | He asks again for the same capability — the output pattern became a habit | A repeated ask after a failure may be persistence, not value. REPEAT requires the prior output to have been *consumed* (a later turn referencing the prior result). Bare repetition without consumption → `uncertain`. |
| 2 | **EXTEND** | He builds a follow-up on the output — O became the input to his next move | If the follow-up would have happened regardless (it was already queued), the bridge breaks. Collector must show the follow-up's content depends on O's content. |
| 3 | **ADOPT** | He brings the output into his own artifact — quotes it in his directive, cites it, forwards it as his own | A quote used only to criticize the output is a CORRECTED event, not ADOPT. The use must be affirmative. |
| 4 | **DELEGATE_ONWARD** | He hands the output to another human or system as authoritative ("send this to the team", "post it") | If he delegated it for review/correction rather than as the answer, it's not value revealed. The delegation must treat O as finished. |
| 5 | **RELIANCE_UNDER_STAKES** | He acts on the output where a mistake would cost him — merges on the system's recommendation, spends money/time on its basis | The strongest class, and the rarest. Requires evidence the stakes were real at decision time (his own click, his own spend), not a seat's interpretation of stakes. |

- **The negative ledger (the mandatory counterweight):** FRUSTRATION events — he redid the work himself, overrode the output, or repeated a request the system should have remembered. These map to the repo schema's `attention_demanded` value_type (trend target DOWN) and live in their own ledger, reported side-by-side, **never netted** against the revealed count. A rising REPEAT count next to a rising FRUSTRATION count tells the real story — the orchid-wasp warning, mechanically enforced.

## 2. HOW it collects data (the mechanical part)

**Channels (same three as SVE-1):**

| Channel | Source | What counts as revealed |
|---|---|---|
| **C2 — direct messages** | `~/memory/YYYY-MM-DD.md` | His directive verbs following a delivery: "do the same for X", "send this to…", "use this", a follow-up whose content depends on the prior output |
| **C1 — team feeds** | Feed #2154 and lane feeds #1713/#1714/#1715/#2471/#2472 | His replies with decision verbs ("merged", "approved", "go ahead") — attributable via the versioned authorship markers (`tools/human_value/authorship-markers.json`); the shared SoulSchoolAcademy account means markers, not vibes |
| **C3 — API-grounded actions** | Repo API records | His own API-side actions tied to team outputs — e.g. a merge *he* clicked after the system's recommendation (RELIANCE_UNDER_STAKES class) |

**Extraction rule (the mechanical part):**
1. For each swept window, the collector identifies deliveries: what the team handed over (branch SHA, report file + sha256, feed comment URL, dashboard update).
2. For each delivery, the collector scans C1/C2/C3 for a subsequent human action attributable to him.
3. Each candidate (O, A) pair gets: O pinned (branch SHA / file+hash / comment URL), A pinned (log line / comment URL / API record), a **bridge sentence** written in plain words, and a **revealed type** from the five.
4. **The bridge is the burden of proof.** "He merged PR #2520 after the team's recommendation" is not yet an event — the bridge must say why: "he clicked merge himself at 12:51Z after the dock's all-five-conditions-met receipt, with the revert risk on him" (RELIANCE_UNDER_STAKES). A collector who cannot write the bridge in one sentence does not have an event; the pair goes to the `uncertain` side ledger.

## 3. HOW it fails closed (absent ≠ zero)

Same three buckets as SVE-1 — they are not interchangeable:

1. **MEASURED** — the window was swept, human actions found, ≥1 independent verification landed on the bridge.
2. **PROVISIONAL** — events collected but awaiting the mandatory independent verification. Reported as collected, never as established.
3. **ABSENT** — the window was not swept, the source is missing, or no human-authored actions exist. Reported as **"NO SIGNAL — not swept"**, never as 0.

**Additional fail-closed rules:**
- **Assessor ≠ beneficiary, tightened:** the collector of an RVE must not be the builder of O. Reliance is the easiest class to self-manufacture ("he loved my output" is the oldest lie in the book).
- **The instrument NEVER prompts.** No "did this help?", no satisfaction check-ins. Prompting manufactures revealed behavior the same way surveys manufacture stated behavior. RVE-1 observes only unprompted actions.
- **Anti-manufacture (P-025):** actions the TEAM could stage are never units — seat-authored sign-ins, staged approvals, feed choreography, lane claims. Authorship markers are the gate; a comment from the shared account with no marker = seat-authored = excluded.
- **Machine-side only is never revealed:** CI merges, check-runs, bot comments, dock merges by seats — the human never touched them. (A merge *he* clicked himself after a seat's recommendation is RELIANCE_UNDER_STAKES, not machine-side.)
- **Reaction emojis → never units** (gameable, no semantics).
- **Silence → no event.** A delivery that sits untouched is a NULL sweep entry, not a rejection.
- **The observatory's own activity → never an RVE** (a sweep is not an experience).
- **Amendment, never edit:** a later CORRECTED event that breaks the bridge (he undid A, discarded O) retracts the seed — append-only with `supersedes: <event_id>`. The original event stays on the record; the praise was real at the time, the reversal is real now.

## 4. SCORING: the P-028 seed-count rule (the math)

**[P-028]** — scores are counts of verified proofs, nothing else. Each independent verification plants one seed; the score grows only when a new seed lands and shrinks when one is retracted.

- **One verified revealed event = 1 SEED.** A seed lands only when the event carries **≥1 independent verification**: a different seat — or a second independent evidence channel — re-pins O, A, and the bridge.
- **Channel independence, defined honestly:** C3 (GitHub-authored API records) + (C1 or C2) = independent. C1 + C2 alone = NOT independent — both are team-authored bytes under the shared account; two pens in the same hand are not two witnesses. The strongest seed is a different seat's re-read across two independent channels.
- **Event strength = seed count:** 0 seeds = PROVISIONAL (collected, not measured) · 1 seed = MEASURED · ≥2 seeds = CORROBORATED.
- **Retraction shrinks the score:** a later CORRECTED event that breaks the bridge retracts one seed — the ledger and the score shrink by exactly one. Retraction is itself an event with its own evidence; the original is never edited or deleted.
- **The area number:** HUMAN-VALUE's revealed contribution = **count of standing seeds** across all REVEALED events — reported alongside SVE-1's stated count and the FRUSTRATION ledger as three numbers, never netted. Rising revealed seeds with rising frustration seeds is a warning, not a win.
- **Calibration banner** until the shared gate passes: a known-answer battery (answer key pre-registered before the run, no peeking) over a past window, inter-collector agreement ≥ 0.8, and Coda 1's adversarial probes all blocked.

## 5. THE REPORT SHAPE (what every RVE report always contains)

1. **The count:** REVEALED n (PROVISIONAL / MEASURED / CORROBORATED, with seed status per event) + seeds standing + FRUSTRATION n, side-by-side, never netted.
2. **The pairs:** every counted unit printed with O (what was delivered), A (what he did), the bridge sentence, and both evidence pointers. Anyone can re-verify by reading the pairs — the number is a summary of the pairs, not a substitute.
3. **The NULL log:** swept windows with zero findings, named explicitly.
4. **The uncertain ledger:** ambiguous bridges, rejected phantoms (a phantom the instrument refused to count is evidence the instrument works).
5. **The D32 block** (§7).
6. **The calibration banner** (until §4's gate passes).

## 6. MACHINE SCHEMA (builder-ready; extends `tools/human_value/schema.py`)

The repo schema already defines `value_type` (useful_outcome, cognitive_load_reduced, rework_avoided, error_prevented, attention_demanded), `evidence`, `beneficiary`, and the REQUIRED_FIELDS list. RVE-1 events are schema-compatible — an RVE event is one of the schema's events with three added fields:

```json
{
  "schema_version": "1",
  "event_id": "RVE-20261013-001",
  "recorded_at": "2026-10-13T21:35:00Z",
  "value_type": "useful_outcome",
  "value_units": 1,
  "unit_description": "one revealed reliance action on a delivered output",
  "evidence_class": "revealed",
  "revealed_type": "repeat|extend|adopt|delegate_onward|reliance_under_stakes|frustration",
  "output_pin":  {"kind": "feed_comment|receipt|content_hash|url", "ref": "<durable pointer to O>"},
  "action_pin":  {"kind": "feed_comment|content_hash|url", "ref": "<durable pointer to A>"},
  "bridge": "One plain sentence: why A only makes sense if O had value.",
  "seeds": [
    {"verifier": "<seat or channel>", "verified_at": "<ts>", "method": "re-read|second-channel"}
  ],
  "retracted": false,
  "beneficiary": "human_self",
  "note": "collector notes; the D32 limits of this event"
}
```

Builder steps (not this wave): `tools/human_value/rve1.py` — `extract <window>` (delivery→action pairing + type classification + bridge drafting), `seeds <event-id>` (independent-verification workflow enforcing the §4 independence rule), `report <window>` (§5 shape). ~150 lines. The schema needs no change — RVE-1 rides the existing `validate_event`; a future schema version can promote `evidence_class` to REQUIRED.

## 7. D32 — WHAT RVE-1 does NOT claim

- **It does not claim motive.** An EXTEND could be politeness or momentum; the bridge sentence is the claim, and it must say why politeness doesn't explain the action. A bridge that can't rule out politeness is an `uncertain`, not an event.
- **It does not grade:** a profane "ship it" counts the same as a polite one — the unit is the action, not the tone.
- **It does not measure lasting benefit:** one ADOPT is a moment. A trend needs the weekly cadence over weeks.
- **It does not measure value to any other human.** The only beneficiary channel that exists is him.
- **One event is not a trend**, and a rising RVE count is not proof of rising value — verbosity, generosity, and the collector's identity all shift the count. The FRUSTRATION ledger beside it is the mandatory counterweight (the orchid-wasp warning: never confuse the measured objective with the human outcome).
- **About this document:** this is a SPEC, not a measurement. No RVE events have been collected yet; §8 is the empty first-reading template. The instrument's own numbers are not yet calibrated.

## 8. FIRST-READING TEMPLATE (empty by design — the window opens when the first sweep runs)

| Window (UTC) | REVEALED (provisional) | REVEALED (measured/corroborated) | Seeds standing | FRUSTRATION | Status |
|---|---|---|---|---|---|
| _to be swept_ | 0 collected | — | 0 | 0 collected | **ABSENT** until swept |

_Honest note for the first sweeper:_ Shawn has been offline since 2026-10-12 ~18:35Z (SVE-1 sweep record). A sweep of today will almost certainly find zero human actions — that is a corroborated 0 if the sweep ran, and ABSENT if it didn't. The instrument must not manufacture its first reading; the NULL log is the first entry.

---

## Receipts

- This spec: `tools/human_value/RVE-1-revealed-value-events.md` (this file), branch `naya5/rve1-revealed-value-events`.
- Sibling: `~/workspace/goals/super-brain-engine-to-10-10/hidden_files/areas/mu-value-instrument-1-20261012T2145.md` (SVE-1).
- Framework: `~/workspace/goals/super-brain-engine-to-10-10/hidden_files/human-value/observed-experience-instrument-v1.md`.
- Repo anchor: `tools/human_value/CONTRACT.md`, `tools/human_value/schema.py` (VALUE_TYPES, EVIDENCE_KINDS, REQUIRED_FIELDS).
- Prior ledgers (the RVE-1 first sweep's opening material): `hidden_files/human-value/hv-wave-3…8-report-20261012.json`, `hidden_files/areas/mu-value-sweep-7-20261013T1312.md`.
- API spend this mission: 2/10 gh-api calls (lane sign-in, sign-out). All reads local.

---

## Appendix A — triple self-validation (the receipts for the score)

**Round 1 — build scored 8.5.** Why not 10:
1. Channel-independence rule was implicit — C1+C2 as "two witnesses" would have been gameable by a seat editing both. **Fixed:** §4 defines independence honestly — C1+C2 ≠ independent, C3+(C1|C2) = independent, different seat = strongest.
2. REPEAT's falsifier was missing — a re-ask after a failure looks identical to a re-ask from reliance. **Fixed:** §1 requires consumption of the prior output.
3. The first-reading section risked manufacturing a reading ("today: 0") without a sweep. **Fixed:** §8 is an empty template with the ABSENT-until-swept rule and the offline-since-18:35Z note.

**Round 2 — 8.5 → 9.0.** Why not 10:
1. Retraction mechanics named "retracts one seed" but didn't tie to the seed-count math. **Fixed:** §4 states the ledger and score shrink by exactly one, retraction is an event with its own evidence.
2. The machine schema didn't say whether the repo's `validate_event` still passes. **Fixed:** §6 confirms schema-compatibility (no schema change needed; three added fields ride OPTIONAL_FIELDS semantics).
3. ADOPT's critic-quoting edge: quoting to criticize looks like ADOPT. **Fixed:** §1 falsifier — critical quotation is a CORRECTED event, not ADOPT.

**Round 3 — 9.0.** Why not 10:
1. Residual: the five-type set is closed — a genuine revealed action outside the five has no home (the type set is a hypothesis, not a proven-exhaustive taxonomy). **Fix applied:** §5's uncertain ledger + the calibration battery (§4) are the escape valves; the battery will surface missing types before the banner lifts. Not fully closable in a spec — the first sweeps are the test.
2. Residual: inter-collector agreement ≥ 0.8 is borrowed from SVE-1 without an RVE-specific trial design. Named as calibration work, not papered over.

Honest ceiling for a spec with no collected events: **9.0**. The remaining 1.0 is earned by the first sweep and the calibration battery, not by more words.
