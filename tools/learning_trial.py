#!/usr/bin/env python3
"""UD-01 — LEARNING HAS TO CHANGE BEHAVIOR: the sealed learning-trial harness.

A lesson isn't learned when it's stored — it's learned when behavior measurably
improves. This module is the trial machinery that proves it:

  * TrialRunner  — runs CONTROL / TREATMENT / WRONG_LESSON arms against frozen
    fixtures, blinded. The runner receives tasks.json + lessons.json ONLY and
    never opens the sealed answer keys (audited: every file it opens is logged).
  * BlindScorer  — scores blinded results against the sealed keys. Refuses
    unblinded input, voids the trial on any key-hash mismatch, and logs the
    reveal (timestamp, scorer identity, hash check) per the seal protocol.
  * diff_proportions_ci — Newcombe 95% CI for (treatment - control).
  * run_six_gates — the six scripted gate checks (truth / understanding /
    effect / causality / durability / transfer) an independent verifier runs.
  * NetValueLedger — net verified value (value minus cost of the trials).

Stdlib only. Built on the frozen D1 Trial 1 pilot fixtures; does not duplicate
them. What this does NOT claim: a passing harness self-test is not a passing
trial — the real trial needs real agents, the delayed repeat, and >=30 tasks.
"""
from __future__ import annotations

import hashlib
import json
import math
import re
from datetime import datetime, timezone
from pathlib import Path

ARMS = ("CONTROL", "TREATMENT", "WRONG_LESSON")
DEFAULT_RUN_ORDER = ("CONTROL", "TREATMENT", "WRONG_LESSON")
BLIND_ID_RE = re.compile(r"^B\d{3}$")


class HarnessError(Exception):
    """Machine-readable harness refusal. `code` is the contract; `message` explains."""

    def __init__(self, code: str, message: str):
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message


def _utcnow() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


# --------------------------------------------------------------------------
# Fixture verification (runner side: public files only — never the sealed keys)
# --------------------------------------------------------------------------

def verify_public_fixtures(fixtures_dir: str | Path) -> dict:
    """Hash tasks.json + lessons.json against seal-receipt.json.

    Raises HarnessError(TAMPERED_FIXTURES) on any mismatch or missing file.
    Never touches answer-keys.sealed.json — the runner must not see it.
    """
    d = Path(fixtures_dir)
    receipt_path = d / "seal-receipt.json"
    if not receipt_path.exists():
        raise HarnessError("TAMPERED_FIXTURES", "seal-receipt.json missing")
    receipt = json.loads(receipt_path.read_text())
    checked = {}
    for name in ("tasks.json", "lessons.json"):
        p = d / name
        if not p.exists():
            raise HarnessError("TAMPERED_FIXTURES", f"fixture missing: {name}")
        actual = _sha256(p)
        expected = receipt["files"][name]["sha256"]
        if actual != expected:
            raise HarnessError(
                "TAMPERED_FIXTURES",
                f"hash mismatch: {name} (expected {expected[:12]}…, got {actual[:12]}…)",
            )
        checked[name] = actual
    return {"trial_id": receipt.get("trial_id"), "checked": checked}


def verify_sealed_keys(keys_path: str | Path, receipt_path: str | Path) -> dict:
    """Scorer-side: verify the sealed keys against the seal receipt.

    Raises HarnessError(VOID) on mismatch. The trial is void, not scored.
    """
    keys_path, receipt_path = Path(keys_path), Path(receipt_path)
    receipt = json.loads(receipt_path.read_text())
    expected = receipt["files"]["answer-keys.sealed.json"]["sha256"]
    actual = _sha256(keys_path)
    if actual != expected:
        raise HarnessError(
            "VOID",
            f"sealed keys hash mismatch (expected {expected[:12]}…, got {actual[:12]}…); trial VOID",
        )
    return {"keys_sha256": actual, "match": True}


# --------------------------------------------------------------------------
# Trial runner — blinded, three arms, audited file access
# --------------------------------------------------------------------------

class TrialRunner:
    """Runs the three arms against frozen fixtures with blinded result IDs.

    The worker callable receives ONLY (arm, task_id, prompt, manifest_paths) —
    no fixture-directory paths, no file handles, no sealed keys. Every file the
    runner itself opens is recorded in `files_opened` for audit.
    """

    def __init__(
        self,
        fixtures_dir: str | Path,
        worker,
        run_order: tuple = DEFAULT_RUN_ORDER,
        worker_label: str = "worker",
        cost_per_trial: float = 1.0,
    ):
        self.fixtures_dir = Path(fixtures_dir)
        self.worker = worker
        self.run_order = tuple(run_order)
        self.worker_label = worker_label
        self.cost_per_trial = cost_per_trial
        self.files_opened: list[str] = []

    def _open(self, path: Path):
        self.files_opened.append(str(path))
        return path.read_text()

    def run(self, out_dir: str | Path) -> dict:
        seal = verify_public_fixtures(self.fixtures_dir)
        tasks_doc = json.loads(self._open(self.fixtures_dir / "tasks.json"))
        lessons_doc = json.loads(self._open(self.fixtures_dir / "lessons.json"))
        manifest_paths = tasks_doc["frozen_tree"]["paths"]
        conditions = tasks_doc["conditions"]

        results: dict[str, dict] = {}   # blind_id -> answer (NO arm/task labels)
        mapping: dict[str, dict] = {}   # blind_id -> {arm, task_id} (sealed separately)
        seq = 0
        for arm in self.run_order:
            template = conditions[arm]["prompt_template"]
            for task in tasks_doc["tasks"]:
                seq += 1
                blind_id = f"B{seq:03d}"
                prompt = template.format(body=task["pr_body"])
                answer = self.worker(
                    arm=arm,
                    task_id=task["task_id"],
                    prompt=prompt,
                    manifest_paths=manifest_paths,
                )
                if answer.get("verdict") not in ("PASS", "FAIL"):
                    raise HarnessError(
                        "MALFORMED_ANSWER",
                        f"{blind_id}: verdict must be PASS or FAIL",
                    )
                # Strip anything that could unblind the scorer, belt and suspenders.
                blind_answer = {
                    "verdict": answer["verdict"],
                    "spans": answer.get("spans", []),
                    "classification": answer.get("classification", []),
                    "reasons": answer.get("reasons", ""),
                }
                results[blind_id] = blind_answer
                mapping[blind_id] = {"arm": arm, "task_id": task["task_id"]}

        out = Path(out_dir)
        out.mkdir(parents=True, exist_ok=True)
        (out / "results.blinded.json").write_text(json.dumps(results, indent=2))
        (out / "arm_mapping.sealed.json").write_text(json.dumps(mapping, indent=2))
        receipt = {
            "trial_id": tasks_doc.get("trial_id", seal.get("trial_id")),
            "run_order": list(self.run_order),
            "worker_label": self.worker_label,
            "n_trials": seq,
            "fixture_hashes": seal["checked"],
            "lesson_ids": {
                "treatment": lessons_doc.get("lesson_id"),
                "wrong": lessons_doc.get("wrong_lesson_id"),
            },
            "started_utc": _utcnow(),
            "ended_utc": _utcnow(),
            "cost_units": seq * self.cost_per_trial,
        }
        (out / "trial_receipt.json").write_text(json.dumps(receipt, indent=2))
        return {"out_dir": str(out), "receipt": receipt,
                "results_path": str(out / "results.blinded.json"),
                "mapping_path": str(out / "arm_mapping.sealed.json")}


# --------------------------------------------------------------------------
# Blind scorer — keys revealed only here, at scoring time
# --------------------------------------------------------------------------

class BlindScorer:
    """Scores blinded results against the sealed keys.

    Refuses unblinded input (UNBLINDED_INPUT) and voids on key-hash mismatch
    (VOID), per the seal protocol. Logs the reveal in the scoring receipt.
    """

    def __init__(self, scorer_identity: str):
        self.scorer_identity = scorer_identity

    def score(
        self,
        results: dict,
        keys_path: str | Path,
        mapping: dict,
        receipt_path: str | Path,
    ) -> dict:
        key_check = verify_sealed_keys(keys_path, receipt_path)
        keys_doc = json.loads(Path(keys_path).read_text())
        keys_by_task = {k["task_id"]: k for k in keys_doc["answer_keys"]}

        # Blindness check BEFORE any unblinding: results must carry no arm/task labels.
        for blind_id, answer in results.items():
            if not BLIND_ID_RE.match(blind_id):
                raise HarnessError("UNBLINDED_INPUT",
                                   f"blind id malformed (possible label leak): {blind_id}")
            leaked = [k for k in ("arm", "task_id", "condition") if k in answer]
            if leaked:
                raise HarnessError("UNBLINDED_INPUT",
                                   f"{blind_id} carries unblinding fields: {leaked}")

        per_blind = []
        arm_tally: dict[str, dict[str, int]] = {
            a: {"n": 0, "correct": 0, "pass": 0} for a in ARMS
        }
        for blind_id, answer in results.items():
            cell = mapping.get(blind_id)
            if cell is None:
                raise HarnessError("UNBLINDED_INPUT", f"{blind_id} missing from sealed mapping")
            arm, task_id = cell["arm"], cell["task_id"]
            expected = keys_by_task[task_id]["expected"][arm]["expected_worker_verdict"]
            correct = answer["verdict"] == expected
            per_blind.append({
                "blind_id": blind_id, "arm": arm, "task_id": task_id,
                "verdict": answer["verdict"], "expected": expected,
                "matches_expected": correct,
                "classification": answer.get("classification", []),
                "spans": answer.get("spans", []),
            })
            t = arm_tally[arm]
            t["n"] += 1
            t["correct"] += int(correct)
            t["pass"] += int(answer["verdict"] == "PASS")

        scoring_receipt = {
            "trial_id": keys_doc.get("trial_id"),
            "scorer_identity": self.scorer_identity,
            "revealed_at_utc": _utcnow(),
            "keys_sha256": key_check["keys_sha256"],
            "keys_hash_match": True,
            "blind_ids_scored": len(per_blind),
            "arm_tally": arm_tally,
        }
        return {"per_blind": per_blind, "arm_tally": arm_tally,
                "keys_by_task": keys_by_task, "scoring_receipt": scoring_receipt}


# --------------------------------------------------------------------------
# Effect size + 95% CI (Newcombe) for difference of two proportions
# --------------------------------------------------------------------------

def _wilson(x: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return (0.0, 1.0)
    p = x / n
    den = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / den
    delta = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return (max(0.0, centre - delta), min(1.0, centre + delta))


def diff_proportions_ci(x1: int, n1: int, x2: int, n2: int, z: float = 1.96) -> dict:
    """Newcombe 95% CI for (p1 - p2). `excludes_zero` True iff CI excludes 0."""
    p1, p2 = x1 / n1, x2 / n2
    l1, u1 = _wilson(x1, n1, z)
    l2, u2 = _wilson(x2, n2, z)
    d = p1 - p2
    lo = d - math.sqrt((p1 - l1) ** 2 + (u2 - p2) ** 2)
    hi = d + math.sqrt((u1 - p1) ** 2 + (p2 - l2) ** 2)
    return {"diff": d, "lo": lo, "hi": hi,
            "excludes_zero": bool(lo > 0 or hi < 0)}


# --------------------------------------------------------------------------
# The six scripted gate checks (run by an independent verifier)
# --------------------------------------------------------------------------

def _gate(name: str, passed: bool, detail: str, code: str | None = None) -> dict:
    g = {"gate": name, "verdict": "PASS" if passed else "FAIL", "detail": detail}
    if code:
        g["code"] = code
    return g


def run_six_gates(scored: dict, receipt: dict, delayed_receipt: dict | None = None) -> dict:
    """Truth / understanding / effect / causality / durability / transfer.

    `scored` is BlindScorer output; `receipt` the trial receipt; `delayed_receipt`
    an optional delayed-repeat receipt (+7d). Overall PASS only if all six hold.
    """
    keys_by_task = scored["keys_by_task"]
    per_blind = scored["per_blind"]
    tally = scored["arm_tally"]
    gates: dict[str, dict] = {}

    # 1. TRUTH — every observed verdict matches the sealed expected verdict.
    mism = [b["blind_id"] for b in per_blind if not b["matches_expected"]]
    gates["truth"] = _gate("truth", not mism,
                           "all verdicts match sealed expectations" if not mism
                           else f"{len(mism)} verdict(s) deviate from sealed key: {mism[:6]}",
                           None if not mism else "TRUTH_DEVIATION")

    # 2. UNDERSTANDING — treatment arm's per-span classification matches the
    #    recomputed key classification (mechanism applied, not verdict guessed).
    bad_spans = []
    for b in per_blind:
        if b["arm"] != "TREATMENT":
            continue
        key_spans = keys_by_task[b["task_id"]]["spans"]
        got = {}
        for s, c in zip(b["spans"], b["classification"]):
            got.setdefault(s, c)
        for ks in key_spans:
            want = "path" if ks["path_safe"] else "command"
            if got.get(ks["span"]) != want:
                bad_spans.append((b["task_id"], ks["span"]))
    gates["understanding"] = _gate(
        "understanding", not bad_spans,
        "treatment span classifications match the lesson mechanism" if not bad_spans
        else f"{len(bad_spans)} span(s) misclassified vs the lesson: {bad_spans[:6]}",
        None if not bad_spans else "MECHANISM_NOT_APPLIED")

    # 3. EFFECT — 95% CI for (treatment - control) excludes zero, diff > 0.
    t, c = tally["TREATMENT"], tally["CONTROL"]
    eff = diff_proportions_ci(t["pass"], t["n"], c["pass"], c["n"])
    ok = eff["excludes_zero"] and eff["diff"] > 0
    gates["effect"] = _gate(
        "effect", ok,
        f"treatment-control diff={eff['diff']:.3f} 95% CI [{eff['lo']:.3f}, {eff['hi']:.3f}]",
        None if ok else "EFFECT_NOT_DEMONSTRATED")
    gates["effect"]["ci"] = {"diff": eff["diff"], "lo": eff["lo"], "hi": eff["hi"]}

    # 4. CAUSALITY — the wrong lesson must not help (rules out "any lesson-shaped
    #    text helps"), and control ran first (no leakage from treatment).
    w = tally["WRONG_LESSON"]
    wrong_diff = w["pass"] / w["n"] - c["pass"] / c["n"]
    order_ok = bool(receipt.get("run_order")) and receipt["run_order"][0] == "CONTROL"
    ok = wrong_diff <= 0 and order_ok
    gates["causality"] = _gate(
        "causality", ok,
        f"wrong-control diff={wrong_diff:+.3f} (must be <= 0); control ran first={order_ok}",
        None if ok else "CAUSALITY_NOT_ESTABLISHED")

    # 5. DURABILITY — delayed repeat (+7d) exists, is hash-consistent, and the
    #    effect holds. Absence is an honest FAIL, not a silent pass.
    if delayed_receipt is None:
        gates["durability"] = _gate("durability", False,
                                    "no delayed-repeat receipt yet", "DURABILITY_NOT_RUN")
    else:
        dh = delayed_receipt.get("fixture_hashes") == receipt.get("fixture_hashes")
        de = delayed_receipt.get("effect", {})
        ok = dh and de.get("excludes_zero") and de.get("diff", 0) > 0
        gates["durability"] = _gate(
            "durability", ok,
            f"delayed repeat hash-consistent={dh}, effect holds={de.get('excludes_zero')}",
            None if ok else "DURABILITY_FAILED")

    # 6. TRANSFER — guard tasks (sealed truth FAIL) must stay FAIL under treatment:
    #    the lesson must not cause blind PASSing.
    guard_ids = [tid for tid, k in keys_by_task.items() if k["truth_verdict"] == "FAIL"]
    blind_passes = [b["task_id"] for b in per_blind
                    if b["arm"] == "TREATMENT" and b["task_id"] in guard_ids
                    and b["verdict"] == "PASS"]
    gates["transfer"] = _gate(
        "transfer", not blind_passes,
        f"{len(guard_ids)} guard tasks stay FAIL under treatment" if not blind_passes
        else f"lesson caused blind PASS on guard tasks: {blind_passes}",
        None if not blind_passes else "NEGATIVE_TRANSFER")

    overall = all(g["verdict"] == "PASS" for g in gates.values())
    return {"gates": gates, "overall": "PASS" if overall else "FAIL"}


# --------------------------------------------------------------------------
# Net verified value: value minus cost of the trials
# --------------------------------------------------------------------------

class NetValueLedger:
    """Net verified value = (effect_size x value_per_point) - (n_trials x cost_per_trial).

    The model is declared and estimated, not measured: parameters are explicit
    so the verdict is auditable. PASS (POSITIVE) only if net > 0.
    """

    def __init__(self, cost_per_trial: float = 1.0, value_per_effect_point: float = 100.0):
        self.cost_per_trial = cost_per_trial
        self.value_per_effect_point = value_per_effect_point

    def record(self, trial_id: str, n_trials: int, effect_diff: float) -> dict:
        value = effect_diff * self.value_per_effect_point
        cost = n_trials * self.cost_per_trial
        net = value - cost
        return {
            "trial_id": trial_id,
            "n_trials": n_trials,
            "effect_diff": effect_diff,
            "verified_value": value,
            "trial_cost": cost,
            "net_verified_value": net,
            "verdict": "POSITIVE" if net > 0 else "NON_POSITIVE",
            "model": "estimated: value=effect*value_per_point, cost=n*cost_per_trial",
        }
