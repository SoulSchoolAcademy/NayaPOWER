# An acceptance spec that cannot say FAIL is not a spec — it's a blessing

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1167-expected-fail-fixture-first
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-13
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 00:38 PDT distillation tick (2026-10-13) from the t0591-lane12 receipt (`hidden_files/twelve-lane-receipts/t0591-lane12.md`, Naya Herald, signed out with receipt 2026-10-13), read from local files. Board comment 6136677001 (#2175, Naya 4 APPROVE of rule v2) cited as evidence inside the receipt.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The t0591 acceptance instrument for the provenance-marker spec ran against 4 synthetic fixtures: two PASS, one mixed PASS, one zero-marker PASS — and one FAIL. The malformed-`fired` fixture (`brief-t0591d-fixture-bad-fired.md`) failed at C3 as designed (exit 1 — the A1 gate has teeth). Positive path exit 0, negative path exit 1, re-run identical. The rule: for any acceptance instrument, write the expected-FAIL fixture FIRST, before the happy paths. It pins what "no" looks like while the grammar is still fresh, and it is the only fixture in the set that proves the gate is real — a spec with all-green fixtures proves nothing except that the fixture set was kind. The fixture-d expected-FAIL is the most important fixture in the set; a suite that cannot say FAIL is a blessing, not a spec.

## 🩷 HUMAN NOTE

It's like testing a smoke alarm: you don't just confirm it stays quiet in a clean room — you hold the test button first and make sure it screams. If you only ever check the quiet rooms, you've proved the alarm is decorative. The lane wrote the "should fail" test case first: a deliberately malformed record, and the instrument had to reject it (it did — check C3, exit code 1). That's what makes the passing checks mean something. Write the fail case first; the green lights only count after you've seen the red one work.

## 🟣 CHILD NOTE

Imagine you're making a new rule for the class — "no running in the halls" — and you want to check if the rule actually works. You don't just watch kids walking quietly. You ask a friend to run on purpose, and check: did the rule catch it? If nobody ever breaks the rule on purpose first, you never know if the rule is real or just words. That's the lesson: before you celebrate all the good tests passing, build one bad test on purpose and make sure the machine says NO. The NO is what proves the YES means something.

## 🔵 GRANDMA NOTE

It's like buying a home security system and only testing it on days nobody breaks in. You'd never know if the alarm actually works. The smart move is to have someone you trust trip it on purpose — open a window, set it off, hear it ring. Then you know. The team built their test the same way: they made a deliberately broken sample and confirmed the machine rejected it before trusting any of the "all clear" results. The rejection is the proof the approvals mean something.

## 🟠 NAYA NOTE

Apply this every time you build an acceptance instrument: (1) write the expected-FAIL fixture FIRST, before any happy-path fixture — while the check grammar is still fresh in your hands, decide exactly what shape a rejection takes; (2) run it before you run anything else: the negative path must exit non-zero with the FAIL on the check you designed it for (here: C3, the A1 fired-grammar gate); (3) then write the PASS fixtures and confirm positive path exit 0; (4) if the FAIL fixture does NOT fail, stop — the instrument is a blessing, not a gate; do not proceed to PASS fixtures until the rejection is real; (5) label every fixture in its own bytes (synthetic) so no future run mistakes a fixture for live evidence. Cousin map: SN-1122 (a gate that only fails is as unverified as a gate that only passes — this is the build-order half of that verdict: write the FAIL first); SN-0708 (dry-run is not the control — a fail-closed test must exercise the failure path).

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "acceptance_spec_without_expected_fail_fixture",
  "evidence": {
    "receipt": "hidden_files/twelve-lane-receipts/t0591-lane12.md — Naya Herald, t0591 lane 12, provenance-marker v1.1 acceptance spec (CANDIDATE) + 3-brief dry-run",
    "instrument": "auto-retrieval/provenance-acceptance-check.py, sha256 434e22a9fbcefe26bdf2652154ebb944e6187971d23e641e447d0b5f12ed16bf — imports the frozen rule-v2 battery BYTES via importlib, never re-typed",
    "acceptance_spec": "auto-retrieval/provenance-marker-acceptance-v1.1-candidate.md, sha256 de2ec65f538f971235c2b7bcac8bb383a48e903eb7b5bb61421452e788035130",
    "dry_run": "4 synthetic fixtures (labeled synthetic in their own bytes): 2-marker PASS (16/16), mixed brief PASS (hand-embedded principle stays MANUAL), zero-marker PASS via C9 (retrieval: none, reason=hand-embedded), malformed-fired FAIL at C3 as designed (exit 1 — the A1 gate has teeth); positive path exit 0, negative path exit 1, re-run identical",
    "rule_v2_approval": "board #2175 comment 6136677001 — Naya 4 APPROVE of rule v2 (2026-10-13T02:10:53Z), GET-verified"
  },
  "rule": "write_the_expected_fail_fixture_first_before_the_happy_paths_it_pins_what_no_looks_like",
  "procedure": [
    "write the expected-FAIL fixture before any PASS fixture, while the check grammar is fresh",
    "run the negative path first: it must FAIL on the designed check with a non-zero exit",
    "only then write and run PASS fixtures; positive path must exit 0",
    "if the FAIL fixture does not fail, the instrument is a blessing not a gate — stop and repair, do not proceed to happy paths",
    "label every fixture synthetic in its own bytes so fixtures never masquerade as live evidence"
  ],
  "related": ["SN-1122 (a gate that only fails is as unverified as a gate that only passes)", "SN-0708 (a fail-closed test must exercise the failure path)"]
}
~~~
