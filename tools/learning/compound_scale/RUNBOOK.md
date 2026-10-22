# RUNBOOK — learn-compound scale proof

**What this is:** the scale proof that lessons compound — 11 distinct lessons
+ 3 adversarial probes through the full pipeline
(capture → distill → inject → verify → compound), each scored on the six
compounding gates (Truth, Understanding, Effect, Causality, Durability,
Transfer; verdict = minimum gate).

**Result (2026-10-11):** 11/11 lessons PROVEN (verdict ≥ 8), 3/3 adversarial
probes correctly REJECTED by the Truth gate, 14/14 pre-registration matches.
3 lessons additionally proven with REAL cold successors (stateless subagents
receiving only the stored lesson): L3, L4, L9 at verdict 9.

## Re-running the scale

```bash
cd <repo-root>
# 1. Seal the registry (pre-registration lock — the runner refuses to run
#    if the registry changed since sealing):
python3 tools/learning/compound_scale/run_scale.py seal

# 2. Run the full scale (writes to --out):
python3 tools/learning/compound_scale/run_scale.py run --out /tmp/scale-run \
    --real-transfer /path/to/real-transfer.json   # optional: cold-successor results

# 3. Read the scorecard:
python3 -c "import json; r=json.load(open('/tmp/scale-run/run_report.json')); print(r['summary'])"
```

## Harness unit tests (the prover's honesty checks)

```bash
python3 -m pytest tests/test_learn_compound_scale.py -q   # 51 tests
```

## Layout

- `lessons_registry.json` — the 11+3 pre-registered lessons (sealed before runs)
- `registry.seal.json` + `SEAL-HISTORY.md` — pre-registration integrity
- `fixtures.py` — 11 behavioral fixtures (naive vs lesson-prescribed procedure)
- `subjects.py` — the mechanical subject + four-arm runner
  (control / treatment / adversarial / successor)
- `gates.py` — the six compounding gates, 0–9 rubrics, verdict = min
- `pipeline.py` — capture / distill / inject / verify / compound
- `run_scale.py` — the pre-registered runner
- `capture_proof/` — the live error-signal-loop scan that captured L11
  (real P2 violation → real learning-event-candidate)
- `runs/2026-10-11-scale-v1/` — the definitive run's ledger + scorecard

## Design notes (read before extending)

- The mechanical subject is deliberately dumb and lesson-agnostic: it applies
  injected rules by task type after an integrity check (receipt present, not
  corrupt). The behavior contrast is real — different procedures, different
  artifacts, same verifier.
- The Truth gate verifies CITATION INTEGRITY (cited evidence exists verbatim
  in the cited source), not semantic entailment. The claim↔evidence binding is
  pre-registered and auditable by an independent seat (D32).
- Adversarial coverage is two-layer: (a) bad lessons are REJECTED by the Truth
  gate before inject (never enter the store as lessons); (b) tampered
  injections are REFUSED by the subject's integrity check (11/11 refused,
  behavior unchanged — see each entry's `integrity` field).
- Transfer 9 = cold real successor reproduced blind; 8 = stateless mechanical
  successor via the persisted-store inject path. The 8s are honest about what
  they are; the 9s are the genuine article.
- This harness is an EXPERIMENT artifact (the scale proof the LEARN charter
  demands), not a competing learning store. Canonical capture stays with the
  error-signal loop / Smart Note path; this harness consumes its schema.
