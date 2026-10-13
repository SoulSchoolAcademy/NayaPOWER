# Seal the Mechanism's Field Contract, Not Just Its Scoreboard — Fixture-Green Can Be Dead Code on Live Bytes

**Intelligent Block:** IB-SMART-NOTE-20261012-sn1140-seal-the-mechanisms-field-contract
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-12
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** [LANE LEARN · LANE 5 · M3 STAMPING DECISION PACKET] #2175 comment 6135811139 (2026-10-13 ~01:03Z, t0555): the retrieval-auth gate candidate (naya/five-retrieval-auth-gate-t942 @ e654f16e8a49e9a26309fd852695a0bef202673d, re-verified live) reads entry["superseded_by"] — but the registry writer stores superseded_by_capture_id: the supersession arm was DEAD CODE on live bytes while its 25/25 tests were GREEN on fixture field names. Worse: 0/52 retrieval_authorized writers exist on live bytes → wiring as-is = total retrieval blackout; the module's publication vocabulary excludes PUBLIC_DERIVED_VIEW_BY_HUMAN_DIRECTOR_REQUEST (16 of Shawn's own published entries). Option A (recommended): wire the scope rule mirroring render() — fields the capture path already writes today, zero migration. Lane 5 falsified the field contract against live bytes BEFORE certifying — candidate 38's family applied to authority code. Related: SN-1132 (seal the mechanism's heartbeat — pre-registered firing predicates), SN-1133 (liveness instrument is a write, not a read).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The M3 stamping gate candidate was verified logic — 25/25 tests green, re-verified live, a clean decision packet ready for Shawn's gate. And it would have been a disaster to wire as-is: it reads a field the registry never writes (`superseded_by` vs the live `superseded_by_capture_id`), so its supersession arm was dead code on real bytes — green only because the fixtures used the candidate's own field names. And zero of 52 live entries carry `retrieval_authorized`, so wiring it would have excluded the entire corpus — a total retrieval blackout wearing a passing test suite. The durable rule: **seal the mechanism's field contract, not just its scoreboard — the tests must exercise the live registry's actual field names, vocabularies, and writer coverage, or green means nothing.** Lane 5 caught it by doing exactly that: falsifying the candidate against live bytes before certifying, mirroring what the capture path already writes today (Option A: zero migration). Fixture-scope tests prove the mechanism works in the fixture's world; only a live-bytes field-contract check proves it works in ours.

## 🩷 HUMAN NOTE

Shawn — Lane 5 saved us from a nasty one tonight. The M3 stamping gate looked ready: 25/25 tests green, logic verified, decision packet polished. But when Lane 5 checked it against the REAL registry bytes before certifying, it fell apart: the gate reads a field the registry never writes, and not a single one of the 52 live entries carries the stamp the gate requires — wiring it would have blacked out the entire retrieval corpus. The tests were green because they tested the gate's own imaginary field names, not the live ones. The rule on the wall now: no mechanism is certified until its tests run against the live field contract — real field names, real vocabularies, real writer coverage. Green on fixtures is a hypothesis; green on live bytes is evidence.

## 🟣 CHILD NOTE

Imagine you build a key and test it on a lock you made yourself — it turns perfectly, 25 times out of 25! But the real door's lock has a different shape inside, and your key was never going to fit. Even worse: your key needs a stamp that NO real door in the building has — so if you installed it, every door would stay locked forever. The tests were perfect… against the wrong lock. The rule: always test your key on the REAL door. If the real door uses different-shaped locks, your perfect test score means nothing.

## 👵 GRANDMA NOTE

It's like a pharmacist who checks every prescription against a sample medicine cabinet — 25 checks, all perfect — but the real pharmacy stocks bottles with different labels, and none of the real bottles have the seal the new rule requires. The first day the rule goes live, every prescription gets rejected. The sample cabinet was the pharmacist's own fantasy; the real shelves were never consulted. The lesson: before you certify any rule, you walk the real shelves — check the real labels, count the real seals. A test that only touches your own samples is a rehearsal, not an inspection.

## 🤖 NAYA NOTE

Fixture-scope blindness is the mechanism-term-zero problem in new clothes: a test suite that exercises the candidate's own vocabulary instead of the live registry's. The M3 candidate had everything — verified logic, re-verified live head, a blast-radius table — and both defects were invisible to it: (1) field-name mismatch (`superseded_by` vs `superseded_by_capture_id`) — the arm never fires on live bytes, a silent no-op; (2) writer-coverage zero (0/52 `retrieval_authorized`) — the gate excludes everything, a loud blackout nobody tested for because fixtures carried the field. The discipline Lane 5 demonstrated: falsify the field contract against live bytes BEFORE certifying — enumerate the fields the mechanism reads, grep the live writer paths, count real coverage, mirror what the capture path already writes (Option A: zero migration, explicit-False still excluded, closes the t902 hole). The general rule for every gate, seal, and instrument: the test battery includes a live-contract arm — real field names, real vocabularies, real writer coverage — or the scoreboard is theater. Cousins: SN-1132 (heartbeat pre-registration — prove the arm FIRES), SN-1133 (write-check — prove the instrument touches reality). This is the third leg: prove it reads reality's actual fields.

## ⚙️ MACHINE NOTE

```json
{
  "sn": "SN-1140",
  "lesson": "seal-the-mechanisms-field-contract-not-just-the-scoreboard",
  "rule": "No mechanism is certified until its tests exercise the live registry's actual field names, vocabularies, and writer coverage; fixture-scope green is a hypothesis, live-bytes field-contract green is evidence.",
  "failure_class": "fixture-scope blindness / live-field-contract mismatch",
  "evidence": {
    "packet": "#2175 comment 6135811139 (2026-10-13 ~01:03Z): M3 stamping decision packet (Lane 5, t0555), candidate naya/five-retrieval-auth-gate-t942 @ e654f16e8a49e9a26309fd852695a0bef202673d",
    "field_mismatch": "module reads entry[\"superseded_by\"]; registry writer stores superseded_by_capture_id → supersession arm dead code on live bytes; 25/25 tests GREEN on fixture field names",
    "blackout": "0/52 retrieval_authorized writers on live bytes → wiring as-is = total retrieval blackout; module vocabulary excludes PUBLIC_DERIVED_VIEW_BY_HUMAN_DIRECTOR_REQUEST (16 of Shawn's published entries)",
    "repair": "Lane 5 falsified against live bytes before certifying; Option A (recommended): wire the scope rule mirroring render() — zero migration, explicit-False excluded (closes t902 hole)"
  },
  "repair_doctrine": "Every mechanism's test battery includes a live-contract arm: enumerate read fields, grep live writer paths, count real coverage — before certification, never after",
  "related": ["SN-1132", "SN-1133"]
}
```
