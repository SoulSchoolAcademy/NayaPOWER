"""Machine-enforced VERIFIED verdict gate for learning (Pair C scorer's 5-point bar).

Problem (2026-10-09, pair-c-scorer-verdict-20261009.md): the learning loop
drained 36 candidates with ZERO honest VERIFIED verdicts because the method
was a compliance ritual, not a causal experiment. The independent scorer
ratified a 5-point bar for an honest VERIFIED verdict:

  1. Falsifiable claim: a specific observable outcome could disprove it.
  2. Same named task in both arms, with a PRE-REGISTERED success criterion
     independent of the lesson (machine-parseable artifact property -- not
     "agent says it preserved provenance").
  3. Outcome measured by something other than the experimenter's self-report:
     a machine check, a different seat's inspection, or a deterministic
     artifact. Any VERIFIED resting on self-reported behavior strings FAILS.
  4. Doer != scorer: verifier re-runs blind, or the outcome is mechanically
     checkable.
  5. Null results recorded as NOT VERIFIED, never as support. Replication
     on >=3 distinct tasks; one task is a demonstration, not proof.

Nothing in the tree enforced this bar -- verdicts were judgments, not
computations. This module is the bar as code: a pure (no DB, no network)
gate that takes a pre-registered experiment plan plus raw arm artifacts and
returns a tamper-evident verdict receipt. A verdict that fails any rule is
NOT_VERIFIED, and the receipt says exactly which rule failed and why.

Fail-closed rules (never repaired, never rounded up):
  - a rule that cannot be evaluated (missing machine check, malformed arm)
    fails CLOSED: NOT_VERIFIED, never an exception, never VERIFIED.
  - a machine check that cannot discriminate control from treatment is a
    self-report ritual, not a measurement: NOT_VERIFIED.
  - null arms are recorded per-task in the receipt, never counted as support.
  - tasks seen before (seen_tasks) cannot earn the cold rung: NOT_VERIFIED
    (anti-memorization; recall is not learning).

Receipt schema: NAYANET_VERIFIED_VERDICT_RECEIPT_V1.

The live experiment still needs Shawn's word (DB writes for the verdict
row, a different seat as scorer) -- this gate is the machinery the
authorized run will invoke, testable today without any gate.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List

SCHEMA = "NAYANET_VERIFIED_VERDICT_RECEIPT_V1"
MIN_REPLICATION_TASKS = 3

RULE_IDS = ("R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8")

RULE_TEXT = {
    "R1": "pre-registered contract complete: non-empty claim, falsifiable "
          "observation, named task family, machine-parseable success "
          "criterion, preregistration timestamp",
    "R2": "machine check present and callable -- no self-report-only verdicts",
    "R3": "machine check runs cleanly on every arm artifact (unmeasured "
          "arms cannot verify)",
    "R4": "doer != scorer -- scorer is independent of every arm's doer",
    "R5": "treatment parses AND control does not, on every task "
          "(delta or it did not happen)",
    "R6": "tasks are distinct and unseen (anti-memorization; recall is not "
          "learning)",
    "R7": "replication on >= %d distinct tasks (one task is a demonstration, "
          "not proof)" % MIN_REPLICATION_TASKS,
    "R8": "null results recorded as NOT VERIFIED, never as support "
          "(per-task rows in the receipt)",
}


# ---------------------------------------------------------------------------
# Canonical machine check (reference, not the only one)
# ---------------------------------------------------------------------------

PROVENANCE_REQUIRED_KEYS = ("source", "timestamp", "authority")


def provenance_block_check(artifact: Any) -> bool:
    """Reference machine check: artifact contains a machine-parseable
    provenance block. Parses the artifact; does not trust agent prose.

    Returns True only if the artifact is a JSON object with a 'provenance'
    block carrying source, timestamp, and authority. Any unparsable or
    incomplete artifact is False -- never an exception.
    """
    try:
        if isinstance(artifact, bytes):
            artifact = artifact.decode("utf-8")
        if not isinstance(artifact, str):
            return False
        obj = json.loads(artifact)
        if not isinstance(obj, dict):
            return False
        block = obj.get("provenance")
        if not isinstance(block, dict):
            return False
        return all(
            isinstance(block.get(k), str) and block.get(k).strip()
            for k in PROVENANCE_REQUIRED_KEYS
        )
    except Exception:
        return False


# ---------------------------------------------------------------------------
# Request shape
# ---------------------------------------------------------------------------

@dataclass
class Arm:
    task_name: str          # distinct task within the named family
    lesson_provided: bool   # True = treatment, False = control
    artifact: Any           # raw artifact bytes/str; measured by machine_check
    doer_id: str


@dataclass
class VerdictRequest:
    claim: str
    falsifiable: str        # the observable that would disprove the claim
    task_family: str         # named family both arms share
    success_criterion: str  # pre-registered, machine-parseable artifact property
    machine_check: Callable[[Any], bool] | None
    arms: List[Arm] = field(default_factory=list)
    scorer_id: str = ""
    blind: bool = True       # scorer unaware of arm assignment
    preregistered_at: str = ""  # ISO timestamp; empty = not pre-registered
    seen_tasks: frozenset = frozenset()


# ---------------------------------------------------------------------------
# The gate
# ---------------------------------------------------------------------------

def _fail(rule: str, detail: str) -> Dict[str, Any]:
    return {"rule": rule, "passed": False, "detail": detail}


def _pass(rule: str, detail: str) -> Dict[str, Any]:
    return {"rule": rule, "passed": True, "detail": detail}


def _receipt_core(verdict: str, trace: List[Dict[str, Any]], tasks: List[Dict[str, Any]],
                  request: VerdictRequest) -> Dict[str, Any]:
    return {
        "schema": SCHEMA,
        "verdict": verdict,
        "claim": request.claim,
        "task_family": request.task_family,
        "success_criterion": request.success_criterion,
        "scorer_id": request.scorer_id,
        "doer_ids": sorted({a.doer_id for a in (request.arms or []) if a.doer_id}),
        "blind": bool(request.blind),
        "rule_trace": trace,
        "task_rows": tasks,
    }


def _digest(core: Dict[str, Any]) -> str:
    canonical = json.dumps(core, sort_keys=True, separators=(",", ":"),
                           ensure_ascii=True)
    return "vvd-%s" % hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:32]


def verdict(request: VerdictRequest | None) -> Dict[str, Any]:
    """Compute the VERIFIED / NOT_VERIFIED verdict. Pure. Never raises:
    malformed input is unproven (NOT_VERIFIED with the failed rule named),
    never an exception."""
    trace: List[Dict[str, Any]] = []
    task_rows: List[Dict[str, Any]] = []

    def done(verdict_value: str) -> Dict[str, Any]:
        core = _receipt_core(verdict_value, trace, task_rows,
                             request if request else VerdictRequest(
                                 claim="", falsifiable="", task_family="",
                                 success_criterion="", machine_check=None))
        receipt = dict(core)
        receipt["digest"] = _digest(core)
        return receipt

    # ---- R1: pre-registered contract complete ---------------------------
    if request is None:
        trace.append(_fail("R1", "no verdict request supplied"))
        return done("NOT_VERIFIED")
    r1_gaps = [name for name, val in (
        ("claim", request.claim),
        ("falsifiable", request.falsifiable),
        ("task_family", request.task_family),
        ("success_criterion", request.success_criterion),
        ("preregistered_at", request.preregistered_at),
    ) if not (isinstance(val, str) and val.strip())]
    if r1_gaps:
        trace.append(_fail("R1", "contract incomplete: missing %s" % ", ".join(r1_gaps)))
        # R1 is structural: the rest is meaningless without the contract.
        for rid in RULE_IDS[1:]:
            trace.append({"rule": rid, "passed": False,
                          "detail": "unevaluated: R1 failed"})
        return done("NOT_VERIFIED")
    trace.append(_pass("R1", "contract complete and pre-registered at %s"
                       % request.preregistered_at))

    # ---- R2: machine check present and callable --------------------------
    if not callable(request.machine_check):
        trace.append(_fail("R2", "machine check missing or not callable -- "
                                 "self-report-only verdicts cannot VERIFY"))
        for rid in ("R3", "R4", "R5", "R6", "R7"):
            trace.append({"rule": rid, "passed": False,
                          "detail": "unevaluated: R2 failed"})
        trace.append(_pass("R8", "no support claimed"))
        return done("NOT_VERIFIED")
    trace.append(_pass("R2", "machine check is callable: %s"
                       % getattr(request.machine_check, "__name__", "check")))

    # ---- arm shape --------------------------------------------------------
    arms = request.arms or []
    malformed = [i for i, a in enumerate(arms)
                 if not isinstance(a, Arm)
                 or not (isinstance(a.task_name, str) and a.task_name.strip())
                 or not isinstance(a.lesson_provided, bool)
                 or not (isinstance(a.doer_id, str) and a.doer_id.strip())]
    if malformed:
        trace.append(_fail("R3", "malformed arms at index %s -- unmeasurable, "
                                 "excluded from verification" % malformed))
        for rid in ("R4", "R5", "R6", "R7"):
            trace.append({"rule": rid, "passed": False,
                          "detail": "unevaluated: arms malformed"})
        trace.append(_pass("R8", "no support claimed"))
        return done("NOT_VERIFIED")

    # ---- R3: machine check runs cleanly on every artifact -----------------
    measured: List[Dict[str, Any]] = []
    for a in arms:
        try:
            parses = bool(request.machine_check(a.artifact))
        except Exception as exc:  # noqa: BLE001 -- a check that blows up
            trace.append(_fail(  # measured nothing
                "R3", "machine check failed on task '%s' (%s): unmeasured "
                      "arms cannot verify" % (a.task_name, type(exc).__name__)))
            for rid in ("R4", "R5", "R6", "R7"):
                trace.append({"rule": rid, "passed": False,
                              "detail": "unevaluated: R3 failed"})
            trace.append(_pass("R8", "no support claimed"))
            return done("NOT_VERIFIED")
        measured.append({"arm": a, "parses": parses})
    trace.append(_pass("R3", "machine check measured all %d arms" % len(arms)))

    # ---- R4: doer != scorer ------------------------------------------------
    doer_ids = {a.doer_id for a in arms}
    if not request.scorer_id or not request.scorer_id.strip():
        trace.append(_fail("R4", "no scorer named"))
    elif request.scorer_id in doer_ids:
        trace.append(_fail("R4", "scorer '%s' is also a doer -- verifier "
                                 "must be independent" % request.scorer_id))
    else:
        trace.append(_pass("R4", "scorer '%s' independent of doers %s "
                                 "(blind=%s)" % (request.scorer_id,
                                                 sorted(doer_ids),
                                                 request.blind)))
    if not trace[-1]["passed"]:
        for rid in ("R5", "R6", "R7"):
            trace.append({"rule": rid, "passed": False,
                          "detail": "unevaluated: R4 failed"})
        trace.append(_pass("R8", "no support claimed"))
        return done("NOT_VERIFIED")

    # ---- R6 (structural, before R5/R7): distinct + unseen tasks -----------
    # Pair into control/treatment per task.
    by_task: Dict[str, List[Dict[str, Any]]] = {}
    for m in measured:
        by_task.setdefault(m["arm"].task_name, []).append(m)
    pair_problems = [t for t, ms in by_task.items()
                     if sorted(x["arm"].lesson_provided for x in ms) != [False, True]]
    if len(by_task) != len(set(by_task)):
        # unreachable (dict keys), kept as the explicit distinctness guard
        pass
    if len(arms) != sum(len(v) for v in by_task.values()):
        pass
    dup_arms = [t for t, ms in by_task.items() if len(ms) != 2]
    if dup_arms or pair_problems:
        bad = sorted(set(dup_arms) | set(pair_problems))
        trace.append(_fail("R6", "tasks must be distinct with exactly one "
                                 "control and one treatment arm each; "
                                 "violations: %s" % bad))
        for rid in ("R5", "R7"):
            trace.append({"rule": rid, "passed": False,
                          "detail": "unevaluated: task pairing invalid"})
        trace.append(_pass("R8", "no support claimed"))
        return done("NOT_VERIFIED")
    seen_hit = [t for t in by_task if t in (request.seen_tasks or frozenset())]
    if seen_hit:
        trace.append(_fail("R6", "tasks already seen (anti-memorization): %s "
                                 "-- recall is not learning" % sorted(seen_hit)))
        for rid in ("R5", "R7"):
            trace.append({"rule": rid, "passed": False,
                          "detail": "unevaluated: R6 failed"})
        trace.append(_pass("R8", "no support claimed"))
        return done("NOT_VERIFIED")
    trace.append(_pass("R6", "%d distinct unseen tasks, each paired "
                             "control/treatment" % len(by_task)))

    # ---- R7: replication >= 3 ---------------------------------------------
    if len(by_task) < MIN_REPLICATION_TASKS:
        trace.append(_fail("R7", "only %d distinct task(s); need >= %d -- "
                                 "one task is a demonstration, not proof"
                                 % (len(by_task), MIN_REPLICATION_TASKS)))
        trace.append({"rule": "R5", "passed": False,
                      "detail": "unevaluated: R7 failed"})
        trace.append(_pass("R8", "no support claimed"))
        return done("NOT_VERIFIED")
    trace.append(_pass("R7", "replicated on %d distinct tasks"
                       % len(by_task)))

    # ---- R5: the delta, per task ------------------------------------------
    all_delta = True
    for task in sorted(by_task):
        ms = by_task[task]
        control = next(m for m in ms if not m["arm"].lesson_provided)
        treatment = next(m for m in ms if m["arm"].lesson_provided)
        row = {
            "task": task,
            "control_parses": control["parses"],
            "treatment_parses": treatment["parses"],
            "delta": (not control["parses"]) and treatment["parses"],
        }
        task_rows.append(row)
        if not row["delta"]:
            all_delta = False
    if all_delta:
        trace.append(_pass("R5", "treatment parses AND control does not on "
                                 "all %d tasks" % len(by_task)))
    else:
        nulls = [r["task"] for r in task_rows if not r["delta"]]
        trace.append(_fail("R5", "no causal delta on task(s) %s -- null "
                                 "recorded as NOT VERIFIED, never as support"
                                 % nulls))

    # ---- R8: nulls are rows, never support ---------------------------------
    if all_delta:
        trace.append(_pass("R8", "no nulls; nothing to misrecord"))
    else:
        trace.append(_pass("R8", "null task rows recorded above as "
                                 "NOT VERIFIED evidence, not support"))

    return done("VERIFIED" if all_delta else "NOT_VERIFIED")


def verify_receipt(receipt: Dict[str, Any] | None) -> bool:
    """Recompute a verdict receipt's digest. Tampered receipts fail."""
    if not isinstance(receipt, dict):
        return False
    digest = receipt.get("digest")
    core = {k: v for k, v in receipt.items() if k != "digest"}
    return isinstance(digest, str) and _digest(core) == digest
