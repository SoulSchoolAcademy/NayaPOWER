"""Stage executors: how each pipeline stage is actually executed.

Two executors implement the StageExecutor protocol:

LocalExecutor — executes the REAL implementations in this repository:
  SELF   → kernel/self_node.py::SelfNode.cold_boot (in-process Python)
  LAW    → nayanet-law-runtime/law.ts::evaluateLaw (node bridge)
  ACT    → nayanet-act-runtime/act.ts::buildActPlan (node bridge)
  KNOW   → nayanet-know-runtime/know.ts::selectKnowContext (node bridge)
  PROVE  → nayanet-prove-runtime/prove.ts::assessKnowProof (node bridge)
  VERIFY → tools/learning_admission_gate.py::admit_candidate (in-process Python;
           the pinned behavioral twin of the WO3 TypeScript gate — 38/38
           fixtures verdict-identical. Production binds the TS gate endpoint
           once merged and deployed. This module is NOT reimplemented here.)
  EVOLVE → tools/learning_evolve.py::evolve_lesson (in-process Python;
           the EVOLVE node: improvement measurement, preservation verdict,
           and correction records with the supersession lifecycle. This
           module is NOT reimplemented here.)
  CONNECT / LEARN → NotImplementedStage (loud, named, never PASS)

HttpExecutor — production bindings: POSTs each stage to its edge-function
endpoint. Defined here so the production wiring is explicit and reviewable.
Live invocation is NOT proven by this module's tests (needs deployed
functions + credentials); the tests prove the LocalExecutor path.

No executor may manufacture a PASS. Every result comes from the invoked
implementation or is an explicit failure / not-implemented state.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol

_REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO_ROOT / "kernel"))
sys.path.insert(0, str(_REPO_ROOT / "tools"))

from .stages import StageId, STAGE_CONTRACTS  # noqa: E402
from .ts_bridge import TsBridgeError, call_ts  # noqa: E402


class NotImplementedStage(RuntimeError):
    """Raised when a stage has no implementation. Loud by design."""

    def __init__(self, stage: StageId):
        contract = STAGE_CONTRACTS[stage]
        super().__init__(contract.not_implemented_reason)
        self.stage = stage
        self.reason = contract.not_implemented_reason


@dataclass
class StageOutput:
    ok: bool
    result: dict[str, Any]
    summary: str


class StageExecutor(Protocol):
    def execute(self, stage: StageId, input: dict[str, Any], correlation_id: str) -> StageOutput:
        ...


# --------------------------------------------------------------------------
# LocalExecutor — the real implementations, executed locally for proof.
# --------------------------------------------------------------------------

class LocalExecutor:
    """Executes each implemented stage via its real implementation."""

    def __init__(self, continuity_dir: str | Path = ".naya/orchestrator/continuity"):
        self.continuity_dir = Path(continuity_dir)
        self.continuity_dir.mkdir(parents=True, exist_ok=True)
        # Count executions per stage: the kill-and-resume proof asserts
        # completed stages are never re-executed.
        self.execution_counts: dict[str, int] = {}

    def _count(self, stage: StageId) -> None:
        self.execution_counts[stage.value] = self.execution_counts.get(stage.value, 0) + 1

    def execute(self, stage: StageId, input: dict[str, Any], correlation_id: str) -> StageOutput:
        contract = STAGE_CONTRACTS[stage]
        if not contract.implemented:
            raise NotImplementedStage(stage)
        self._count(stage)
        handler = {
            StageId.SELF: self._run_self,
            StageId.LAW: self._run_law,
            StageId.ACT: self._run_act,
            StageId.KNOW: self._run_know,
            StageId.PROVE: self._run_prove,
            StageId.VERIFY: self._run_verify,
            StageId.EVOLVE: self._run_evolve,
        }[stage]
        return handler(input, correlation_id)

    # -- SELF ----------------------------------------------------------
    def _run_self(self, input: dict[str, Any], correlation_id: str) -> StageOutput:
        from self_node import JsonContinuityStore, RuntimeIdentity, SelfNode

        identity_in = input.get("identity", {})
        store = JsonContinuityStore(self.continuity_dir / "self_state.json")
        node = SelfNode(store)
        receipt = node.cold_boot(
            runtime_identity=RuntimeIdentity(
                actor_id=identity_in.get("actor_id", "unknown-actor"),
                system_id=identity_in.get("system_id", "naya-power"),
                role=identity_in.get("role", "learner"),
            ),
            mission=input.get("mission", "prove the learning loop"),
            objective=input.get("objective", "execute the nine-node pipeline for one capture"),
            scope=input.get("scope", "orchestrator-proof"),
        )
        return StageOutput(
            ok=True,
            result={"identity_receipt": receipt, "correlation_id": correlation_id},
            summary=f"SELF identity established: {receipt.get('actor_id', '?')} "
                    f"(state={receipt.get('state', '?')}, checkpoint={receipt.get('checkpoint_id', '?')[:12]})",
        )

    # -- LAW -----------------------------------------------------------
    def _run_law(self, input: dict[str, Any], correlation_id: str) -> StageOutput:
        identity = input.get("self_result", {}).get("identity_receipt", {})
        # The orchestrator processes captures originating from the human
        # director's capture directive ("smart note this" — the Verification
        # Law: the ask IS the verification). The LAW request carries the
        # standing same-lifecycle authority fields, and the real evaluateLaw
        # decides.
        req = {
            "owner_id": input.get("owner_id", "owner-1"),
            "naya_id": identity.get("actor_id", "naya-1"),
            "action": "smart_note_lifecycle_complete",
            "target": input.get("lesson_id", "unknown-lesson"),
            "same_smart_note_lifecycle": True,
            "explicit_human_smart_note_directive": bool(
                input.get("capture", {}).get("human_directive", True)
            ),
        }
        try:
            decision = call_ts("LAW", [req, input.get("grants", [])])
        except TsBridgeError as exc:
            return StageOutput(ok=False, result={"error": str(exc)}, summary=f"LAW bridge failed: {exc}")
        status = decision.get("status", "UNKNOWN")
        return StageOutput(
            ok=True,
            result={"decision": decision, "correlation_id": correlation_id},
            summary=f"LAW decision: {status}",
        )

    # -- ACT -----------------------------------------------------------
    def _run_act(self, input: dict[str, Any], correlation_id: str) -> StageOutput:
        law_result = input.get("law_result", {}).get("decision", {})
        req = {
            "owner_id": input.get("owner_id", "owner-1"),
            "naya_id": input.get("naya_id", "naya-1"),
            "action": input.get("action", "learning.capture.process"),
            "target": input.get("lesson_id", "unknown-lesson"),
            "door_id": "orchestrator",
            "operation": "process",
        }
        try:
            plan = call_ts("ACT", [req, law_result or None, None, None, None, None, None])
        except TsBridgeError as exc:
            return StageOutput(ok=False, result={"error": str(exc)}, summary=f"ACT bridge failed: {exc}")
        return StageOutput(
            ok=True,
            result={"plan": plan, "correlation_id": correlation_id},
            summary=f"ACT plan built: {str(plan)[:80]}",
        )

    # -- KNOW ----------------------------------------------------------
    def _run_know(self, input: dict[str, Any], correlation_id: str) -> StageOutput:
        req = {
            "owner_id": input.get("owner_id", "owner-1"),
            "naya_id": input.get("naya_id", "naya-1"),
            "task_id": input.get("lesson_id", "unknown-lesson"),
            "task_class": "learning-capture",
            "required_capability": input.get("required_capability", "lesson-interpretation"),
        }
        try:
            result = call_ts("KNOW", [req, input.get("blocks", [])])
        except TsBridgeError as exc:
            return StageOutput(ok=False, result={"error": str(exc)}, summary=f"KNOW bridge failed: {exc}")
        return StageOutput(
            ok=True,
            result={"know_result": result, "correlation_id": correlation_id},
            summary=f"KNOW: {result.get('status', '?')} (selected={result.get('selected_block_id')})",
        )

    # -- PROVE ---------------------------------------------------------
    def _run_prove(self, input: dict[str, Any], correlation_id: str) -> StageOutput:
        know_result = input.get("know_result", {}).get("know_result")
        # Thread the KNOW output through as the proof receipt: the next stage
        # consumes the previous stage's result, per Naya 1's machine.
        receipt = None
        if isinstance(know_result, dict):
            receipt = {
                "id": f"know-receipt-{input.get('lesson_id', 'x')}",
                "user_id": input.get("owner_id", "owner-1"),
                "project_id": "NayaPOWER",
                "action": "know.select",
                "status": know_result.get("status", "UNKNOWN"),
                "observed_result": know_result.get("status"),
                "evidence": {"know_result": know_result},
            }
        try:
            assessment = call_ts(
                "PROVE",
                [
                    input.get("owner_id", "owner-1"),
                    input.get("naya_id", "naya-1"),
                    receipt,
                    None,  # block
                    None,  # grant
                    [],    # relationships
                ],
            )
        except TsBridgeError as exc:
            return StageOutput(ok=False, result={"error": str(exc)}, summary=f"PROVE bridge failed: {exc}")
        verdict = assessment.get("verdict", assessment.get("status", "?"))
        return StageOutput(
            ok=True,
            result={"assessment": assessment, "correlation_id": correlation_id},
            summary=f"PROVE assessment: {verdict}",
        )

    # -- VERIFY --------------------------------------------------------
    def _run_verify(self, input: dict[str, Any], correlation_id: str) -> StageOutput:
        # The pinned behavioral twin of the WO3 TypeScript gate (38/38
        # fixtures verdict-identical). NOT a reimplementation — this module
        # imports the canonical reference. Production binds the TS gate
        # endpoint once merged and deployed.
        from learning_admission_gate import admit_candidate

        candidate = input.get("candidate")
        if not isinstance(candidate, dict):
            candidate = input.get("capture", {}).get("candidate")
        if not isinstance(candidate, dict):
            return StageOutput(
                ok=False,
                result={"error": "VERIFY requires an admission candidate object"},
                summary="VERIFY failed: no candidate supplied",
            )
        result = admit_candidate(candidate)
        codes = list(result.reasons) if not result.admitted else []
        verdict = "ADMITTED" if result.admitted else f"REJECTED:{','.join(codes)}"
        return StageOutput(
            ok=True,
            result={
                "admitted": result.admitted,
                "admitted_as": result.admitted_as,
                "reason_codes": codes,
                "correlation_id": correlation_id,
            },
            summary=f"VERIFY verdict: {verdict}",
        )

    # -- EVOLVE --------------------------------------------------------
    def _run_evolve(self, input: dict[str, Any], correlation_id: str) -> StageOutput:
        # The EVOLVE node: tools/learning_evolve.py::evolve_lesson (in-process
        # Python — NOT a reimplementation; this module imports the canonical
        # reference). It measures the lesson against its recorded application
        # history, emits the preservation verdict, and — for verified
        # failures — correction records with the supersession lifecycle.
        # Production binds a future evolve edge function once deployed.
        from learning_evolve import evolve_lesson

        lesson = input.get("lesson")
        if not isinstance(lesson, dict):
            lesson = input.get("capture", {}).get("lesson")
        applications = input.get("applications")
        if applications is None:
            applications = input.get("capture", {}).get("applications")
        if not isinstance(lesson, dict):
            return StageOutput(
                ok=False,
                result={"error": "EVOLVE requires a lesson object (input['lesson'])"},
                summary="EVOLVE failed: no lesson supplied",
            )
        if not isinstance(applications, list):
            return StageOutput(
                ok=False,
                result={"error": "EVOLVE requires an applications list (input['applications'])"},
                summary="EVOLVE failed: no application history supplied",
            )
        try:
            result = evolve_lesson(
                lesson,
                applications,
                baseline_success_rate=input.get("baseline_success_rate"),
            )
        except ValueError as exc:
            return StageOutput(
                ok=False,
                result={"error": str(exc)},
                summary=f"EVOLVE failed: {exc}",
            )
        measurement = result.measurement
        delta = measurement.get("delta_vs_baseline")
        delta_text = f"{delta:+.3f}" if delta is not None else "UNKNOWN"
        return StageOutput(
            ok=True,
            result={
                "lesson_id": result.lesson_id,
                "verdict": result.verdict,
                "verdict_reason": result.verdict_reason,
                "measurement": measurement,
                "correction_records": list(result.correction_records),
                "correlation_id": correlation_id,
            },
            summary=(
                f"EVOLVE verdict: {result.verdict} "
                f"(verified={measurement['verified_applications']}, "
                f"delta_vs_baseline={delta_text}, "
                f"corrections={len(result.correction_records)})"
            ),
        )


# --------------------------------------------------------------------------
# HttpExecutor — production bindings (explicit, not live-proven here).
# --------------------------------------------------------------------------

# Production stage endpoints. Invoking these requires deployed functions +
# credentials; the wiring manifest records deployed versions as GAP/STALE.
# This executor exists so the production wiring is reviewable in one place.
PRODUCTION_ENDPOINTS: dict[str, str] = {
    "SELF": "(in-process: kernel/self_node.py — no HTTP binding)",
    "LAW": "nayanet-law-runtime",
    "ACT": "nayanet-act-runtime",
    "KNOW": "nayanet-know-runtime",
    "PROVE": "nayanet-prove-runtime",
    "CONNECT": "(no implementation — no endpoint)",
    "VERIFY": "nayanet-learning-verify (WO3 gate at mode==='candidate' write site, post-merge)",
    "LEARN": "(no implementation — no endpoint)",
    "EVOLVE": "(no edge function deployed — local binding only: tools/learning_evolve.py; production binding TBD)",
}


class HttpExecutor:
    """Production HTTP bindings. Not live-proven by this package's tests."""

    def __init__(self, base_url: str, auth_token: str):
        self.base_url = base_url.rstrip("/")
        self.auth_token = auth_token

    def execute(self, stage: StageId, input: dict[str, Any], correlation_id: str) -> StageOutput:
        import urllib.request

        contract = STAGE_CONTRACTS[stage]
        if not contract.implemented:
            raise NotImplementedStage(stage)
        endpoint = PRODUCTION_ENDPOINTS.get(stage.value, "")
        if endpoint.startswith("("):
            return StageOutput(
                ok=False,
                result={"error": f"no HTTP binding for {stage.value}: {endpoint}"},
                summary=f"{stage.value} has no HTTP endpoint",
            )
        body = json_dumps({"input": input, "correlation_id": correlation_id})
        req = urllib.request.Request(
            f"{self.base_url}/{endpoint}",
            data=body.encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.auth_token}",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                payload = json_loads(resp.read().decode("utf-8"))
        except Exception as exc:  # Failures are explicit, never silent.
            return StageOutput(
                ok=False,
                result={"error": f"{type(exc).__name__}: {exc}"},
                summary=f"{stage.value} HTTP invocation failed",
            )
        return StageOutput(ok=True, result=payload, summary=f"{stage.value} executed via {endpoint}")


def json_dumps(obj: dict) -> str:
    import json as _json

    return _json.dumps(obj)


def json_loads(text: str) -> dict:
    import json as _json

    return _json.loads(text)
