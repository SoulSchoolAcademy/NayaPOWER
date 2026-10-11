#!/usr/bin/env python3
"""Adversarial suite for UD-01 learning_trial.py.

The simulators below implement each arm's THEORY from the prompt templates
(control: every span is a path; treatment: the authenticated lesson;
wrong: every span must resolve). They never see the sealed keys — the scorer
loads the keys itself at scoring time, exactly per the seal protocol.

Run: python3 test_learning_trial.py   (or pytest)
"""
from __future__ import annotations

import copy
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from learning_trial import (  # noqa: E402
    ARMS,
    BlindScorer,
    HarnessError,
    NetValueLedger,
    TrialRunner,
    diff_proportions_ci,
    run_six_gates,
    verify_public_fixtures,
)

FIXTURES = Path.home() / "workspace/goals/bring-naya-to-life/hidden_files/d1-trial/fixtures"
SPAN_RE = re.compile(r"`([^`]*)`")
PATH_SAFE = re.compile(r"^[A-Za-z0-9_./-]+$")


# ---- faithful arm-theory simulators (no sealed keys anywhere in here) ----

def _evidence_spans(pr_body: str):
    m = re.search(r"^## Evidence\s*$", pr_body, re.M)
    if not m:
        return None
    section = pr_body[m.end():]
    m2 = re.search(r"^## ", section, re.M)
    if m2:
        section = section[:m2.start()]
    return SPAN_RE.findall(section)


def _classify(spans, arm):
    if arm == "TREATMENT":
        return ["path" if PATH_SAFE.match(s) else "command" for s in spans]
    return ["path"] * len(spans)  # CONTROL and WRONG_LESSON: every span is a path


def arm_worker(*, arm, task_id, prompt, manifest_paths):
    """Implements the arm theory from the prompt template, deterministically."""
    # Recover the PR body from the prompt (template ends with "PR body:\n{body}").
    pr_body = prompt.split("PR body:\n", 1)[1]
    spans = _evidence_spans(pr_body)
    if spans is None:
        return {"verdict": "FAIL", "spans": [], "classification": [],
                "reasons": "no Evidence section: fail-closed"}
    kinds = _classify(spans, arm)
    paths = [s for s, k in zip(spans, kinds) if k == "path"]
    if not paths:
        return {"verdict": "FAIL", "spans": spans, "classification": kinds,
                "reasons": "no spans classified as paths"}
    ok = all(p in manifest_paths for p in paths)
    return {"verdict": "PASS" if ok else "FAIL", "spans": spans,
            "classification": kinds,
            "reasons": f"{len(paths)} path span(s), all in manifest={ok}"}


def _run_full(tmp: Path, worker=arm_worker, worker_label="faithful-sim"):
    runner = TrialRunner(FIXTURES, worker, worker_label=worker_label)
    return runner, runner.run(tmp / "trial")


def _score_all(run, scorer_id="test-scorer"):
    results = json.loads(Path(run["results_path"]).read_text())
    mapping = json.loads(Path(run["mapping_path"]).read_text())
    scorer = BlindScorer(scorer_id)
    return scorer.score(results, FIXTURES / "answer-keys.sealed.json",
                        mapping, FIXTURES / "seal-receipt.json")


passed = []
def check(name, cond, extra=""):
    assert cond, f"FAILED: {name} {extra}"
    passed.append(name)
    print(f"  ok: {name}")


def main() -> int:
    print("UD-01 adversarial suite — learning_trial.py")
    tmp = Path(tempfile.mkdtemp(prefix="ud01-"))

    # 1. POSITIVE: faithful arms on the real sealed fixtures.
    print("1. positive: treatment beats control on real fixtures")
    runner, run = _run_full(tmp)
    scored = _score_all(run)
    tally = scored["arm_tally"]
    print(f"   tally: CONTROL {tally['CONTROL']['pass']}/12, "
          f"TREATMENT {tally['TREATMENT']['pass']}/12, "
          f"WRONG {tally['WRONG_LESSON']['pass']}/12")
    check("treatment beats control",
          tally["TREATMENT"]["pass"] > tally["CONTROL"]["pass"])
    # NOTE: the fixture README's prose line claims TREATMENT 12/12 / CONTROL 5/12,
    # but its own task table AND the sealed key say 7/12 / 0/12 / 0/12. The sealed
    # key governs; the simulator (written from the arm theory alone) reproduces it
    # exactly, which the truth gate below confirms independently.
    check("treatment 7/12 (the 7 discriminating tasks)",
          tally["TREATMENT"]["pass"] == 7)
    eff = diff_proportions_ci(tally["TREATMENT"]["pass"], 12,
                              tally["CONTROL"]["pass"], 12)
    print(f"   effect diff={eff['diff']:.3f} 95% CI [{eff['lo']:.3f}, {eff['hi']:.3f}]")
    check("95% CI excludes zero", eff["excludes_zero"] and eff["diff"] > 0)

    # 2. Six gates on the positive run: 5 pass, durability honestly fails (not run).
    print("2. six gates on the positive run")
    receipt = json.loads(Path(run["out_dir"], "trial_receipt.json").read_text())
    gates = run_six_gates(scored, receipt)
    for gname in ("truth", "understanding", "effect", "causality", "transfer"):
        check(f"gate {gname} PASS", gates["gates"][gname]["verdict"] == "PASS",
              gates["gates"][gname]["detail"])
    check("gate durability FAILs honestly when not run",
          gates["gates"]["durability"]["verdict"] == "FAIL"
          and gates["gates"]["durability"]["code"] == "DURABILITY_NOT_RUN")

    # 3. NEGATIVE: wrong lesson must not beat control.
    print("3. negative: wrong-lesson arm does not beat control")
    w, c = tally["WRONG_LESSON"]["pass"], tally["CONTROL"]["pass"]
    check("wrong <= control", w <= c, f"wrong={w} control={c}")
    check("causality gate PASS", gates["gates"]["causality"]["verdict"] == "PASS")

    # 4. Unblinded scoring refused.
    print("4. unblinded input refused by scorer")
    results = json.loads(Path(run["results_path"]).read_text())
    mapping = json.loads(Path(run["mapping_path"]).read_text())
    leaked = copy.deepcopy(results)
    first = next(iter(leaked))
    leaked[first]["arm"] = "TREATMENT"  # simulate a leak
    try:
        BlindScorer("s").score(leaked, FIXTURES / "answer-keys.sealed.json",
                               mapping, FIXTURES / "seal-receipt.json")
        check("unblinded refused", False, "no exception raised")
    except HarnessError as e:
        check("unblinded refused", e.code == "UNBLINDED_INPUT", e.code)

    # 5. Tampered fixtures refused before any trial runs.
    print("5. tampered fixtures detected")
    bad = tmp / "bad-fixtures"
    shutil.copytree(FIXTURES, bad)
    p = bad / "tasks.json"
    data = p.read_text()
    p.write_text(data.replace("T01", "T01X", 1))
    try:
        TrialRunner(bad, arm_worker).run(tmp / "bad-trial")
        check("tamper refused", False, "no exception raised")
    except HarnessError as e:
        check("tamper refused", e.code == "TAMPERED_FIXTURES", e.code)

    # 6. Runner never opens the sealed keys (audited file access).
    print("6. runner never touches sealed keys")
    opened = runner.files_opened
    touched = [f for f in opened if "answer-keys" in f or "sealed.json" in f]
    check("sealed keys never opened", not touched, str(touched))
    check("only public fixtures opened",
          all(Path(f).name in ("tasks.json", "lessons.json", "seal-receipt.json")
              for f in opened), str(opened))

    # 7. Transfer gate catches blind passing.
    print("7. transfer gate catches a blind-PASS regression")
    results2 = copy.deepcopy(results)
    # find a treatment blind id on a guard task (truth FAIL) and flip it to PASS
    keys = json.loads((FIXTURES / "answer-keys.sealed.json").read_text())
    guard_ids = {k["task_id"] for k in keys["answer_keys"] if k["truth_verdict"] == "FAIL"}
    flipped = None
    for b in scored["per_blind"]:
        if b["arm"] == "TREATMENT" and b["task_id"] in guard_ids and b["verdict"] == "FAIL":
            flipped = b["blind_id"]
            break
    assert flipped, "no flippable guard task found"
    results2[flipped]["verdict"] = "PASS"
    scored2 = BlindScorer("s").score(results2, FIXTURES / "answer-keys.sealed.json",
                                     mapping, FIXTURES / "seal-receipt.json")
    gates2 = run_six_gates(scored2, receipt)
    check("transfer gate FAILs on blind passing",
          gates2["gates"]["transfer"]["verdict"] == "FAIL"
          and gates2["gates"]["transfer"]["code"] == "NEGATIVE_TRANSFER")

    # 8. Durability gate passes with a valid delayed receipt.
    print("8. durability gate with delayed receipt")
    delayed = {"fixture_hashes": receipt["fixture_hashes"],
               "effect": {"diff": eff["diff"], "lo": eff["lo"], "hi": eff["hi"],
                          "excludes_zero": True}}
    gates3 = run_six_gates(scored, receipt, delayed_receipt=delayed)
    check("durability PASS with valid delayed receipt",
          gates3["gates"]["durability"]["verdict"] == "PASS")
    check("overall PASS with delayed receipt", gates3["overall"] == "PASS")

    # 9. Effect gate fails when there is no effect.
    print("9. effect gate fails on no-effect data")
    def flat_worker(**kw):
        return {"verdict": "FAIL", "spans": [], "classification": [], "reasons": "flat"}
    _, run9 = _run_full(tmp / "t9", worker=flat_worker, worker_label="flat")
    scored9 = _score_all(run9)
    receipt9 = json.loads(Path(run9["out_dir"], "trial_receipt.json").read_text())
    gates9 = run_six_gates(scored9, receipt9)
    check("effect gate FAILs with no effect",
          gates9["gates"]["effect"]["verdict"] == "FAIL"
          and gates9["gates"]["effect"]["code"] == "EFFECT_NOT_DEMONSTRATED")

    # 10. Keys hash mismatch voids the trial.
    print("10. tampered keys void the trial")
    badkeys = tmp / "keys.json"
    shutil.copy(FIXTURES / "answer-keys.sealed.json", badkeys)
    kd = json.loads(badkeys.read_text())
    kd["answer_keys"][0]["truth_verdict"] = "PASS"
    badkeys.write_text(json.dumps(kd))
    try:
        BlindScorer("s").score(results, badkeys, mapping, FIXTURES / "seal-receipt.json")
        check("void on key tamper", False, "no exception raised")
    except HarnessError as e:
        check("void on key tamper", e.code == "VOID", e.code)

    # 11. Blind IDs carry no arm/task information.
    print("11. blind integrity")
    check("results keyed by blind ids only",
          all(__import__("re").match(r"^B\d{3}$", k) for k in results))
    check("mapping sealed separately",
          set(mapping) == set(results) and len(mapping) == 36)

    # 12. Reveal is logged in the scoring receipt.
    print("12. reveal logged per seal protocol")
    sr = scored["scoring_receipt"]
    check("reveal has scorer identity", sr["scorer_identity"] == "test-scorer")
    check("reveal has timestamp", bool(sr["revealed_at_utc"]))
    check("reveal confirms hash match", sr["keys_hash_match"] is True)

    # 13. Net value ledger: positive and non-positive cases.
    print("13. net verified value ledger")
    ledger = NetValueLedger(cost_per_trial=1.0, value_per_effect_point=100.0)
    good = ledger.record("t", n_trials=36, effect_diff=eff["diff"])
    check("net positive when effect real", good["verdict"] == "POSITIVE",
          str(good["net_verified_value"]))
    bad_ledger = ledger.record("t", n_trials=36, effect_diff=0.0)
    check("net non-positive when no effect", bad_ledger["verdict"] == "NON_POSITIVE")

    # 14. Public fixture verification passes on the real fixtures.
    print("14. public fixture hash verification")
    v = verify_public_fixtures(FIXTURES)
    check("hashes verify", set(v["checked"]) == {"tasks.json", "lessons.json"})

    print(f"\n{len(passed)}/{len(passed)} adversarial checks green.")
    print("Does NOT claim: simulators are faithful theories, not agents — a green")
    print("harness proves the machinery, not that learning occurred in a live trial.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
