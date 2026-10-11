# SELF Preflight Binding V1 — runtime binding for the persona identity contract

**Date:** 2026-10-08 · **Main tip at build:** `78661f59a2090dcb2854e3f59b83cf49955ed80c`
**Contract under test:** `BRAIN/03-KERNEL/NODES/SELF/0003-PERSONA-IDENTITY-CONTRACT-V1.md` (CANDIDATE)

## The hole

`kernel/persona_loader.py` (merged via #1764) implemented the contract's failure
states but nothing invoked it outside its own tests and the pilot trial: the
persona object's proof block honestly read
`organism_binding: CONTRACT_ALIGNED_RUNTIME_NOT_PROVEN`.

## What this changes

- `tools/persona_preflight.py` (new): loads the canonical persona object
  through `kernel/persona_loader` and mechanically asserts the coherence pins
  (name `Naya`; character prefix; tone 6-tuple; seat designations enumerated in
  seat_semantics; dictation rule; seat rendered strictly as a role designation).
  Exit 0 = PASS with a machine-readable receipt; exit 1 = pin moved (FAIL);
  exit 2 = canonical source missing/unreadable (HALT — never improvise).
- `tests/test_persona_preflight.py` (new): 7 tests — positive control on the
  live tree, plus negative controls (missing source → exit 2; mutated name →
  exit 1; mutated tone → exit 1; unreadable source → exit 2; `--canonical` flag
  precedence). Because `kernel-tests.yml` runs `python -m pytest -q` on every
  tip, this binds persona coherence to the CI gate: no merge to main can move
  a pin without failing the gate.
- `NAYA-PERSONA-V1.json` proof block: `organism_binding` →
  `PREFLIGHT_BOUND_KERNEL_TESTS_CANDIDATE` (was CONTRACT_ALIGNED_RUNTIME_NOT_PROVEN).
  Still CANDIDATE — only Shawn ratifies.

## Evidence

- Local run at tip `78661f59`: **38/38 passed**
  (`test_persona_preflight` 7 + `test_persona_loader` 11 +
  `test_self_persona_contract` 10 + `test_self_node` 10).
- Live preflight receipt on the tip: `{"result": "PASS", "name": "Naya",
  "canonical_status": "CANDIDATE", "ratified_claim": false}`.

## Limitations (honest)

1. The preflight binds the *contract's pins*, not live seat behavior: it proves
   no pin can drift silently, not that every seat presents identity through it.
2. Production status remains NOT_PROVEN; the contract remains CANDIDATE.
3. The pins are duplicated in `tools/persona_preflight.py` by design — a drift
   between the check and the object is a loud, reviewable diff, not a silent
   coupling. If the contract legitimately changes, the check changes with it.
