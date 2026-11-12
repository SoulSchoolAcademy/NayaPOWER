"""The node orchestrator: durable event → nine-node execution.

Naya 1's machine: "each completed stage emits a durable result, the next
stage consumes that result, and failures become explicit, recoverable states."

Execution semantics:
- Stages run in STAGE_ORDER. Completed stages are never re-executed (resume).
- A NOT_IMPLEMENTED stage is recorded loudly with its named reason and the
  run continues past it — the run can never be SUCCESS with gaps; its ceiling
  is INCOMPLETE with the missing stages named.
- A stage error → FAILED (named error), run halts, resume retries the stage.
- Governed halts: LAW BLOCKED → BLOCKED; VERIFY rejected → REJECTED.
- Interruption (crash while RUNNING): resume resets the stage to PENDING with
  an interruption note and retries it. Stage implementations MUST be
  idempotent for this to be safe — recorded as a contract requirement.
- No synthetic PASS anywhere. No silent fallback. No silent drop.
"""

from __future__ import annotations

from enum import Enum
from pathlib import Path
from typing import Any

from .event_store import EventStore
from .executors import NotImplementedStage, StageExecutor, StageOutput
from .run_state import RunRecord, RunStore
from .stages import STAGE_CONTRACTS, STAGE_ORDER, StageId


class RunStatus(str, Enum):
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    INCOMPLETE = "INCOMPLETE"
    FAILED = "FAILED"
    BLOCKED = "BLOCKED"
    REJECTED = "REJECTED"


class StageStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    NOT_IMPLEMENTED = "NOT_IMPLEMENTED"
    SKIPPED = "SKIPPED"


class NodeOrchestrator:
    """Durable nine-node pipeline executor."""

    def __init__(
        self,
        executor: StageExecutor,
        store_root: str | Path = ".naya/orchestrator",
    ):
        self.executor = executor
        self.store_root = Path(store_root)
        self.events = EventStore(self.store_root / "events.jsonl")
        self.runs = RunStore(self.store_root / "runs")

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def commit_capture(
        self,
        lesson_id: str,
        capture_fingerprint: str,
        note: str = "",
    ) -> str:
        """Create the durable processing obligation. Idempotent. Returns event_id."""
        event = self.events.commit(lesson_id, capture_fingerprint, note=note)
        self.events.set_status(event.event_id, "RUNNING", note="orchestrator run started")
        return event.event_id

    def run(
        self,
        event_id: str,
        capture: dict[str, Any],
        crash_after: str | None = None,
    ) -> RunRecord:
        """Execute (or resume) the pipeline for an event.

        crash_after: test hook — raise KeyboardInterrupt after the named stage
        completes, simulating a crash mid-run. The next run() call resumes.
        """
        event = self.events.get(event_id)
        if event is None:
            raise KeyError(f"unknown event: {event_id}")
        record = self.runs.create(event_id, event_id, event.correlation_id, event.lesson_id)
        if record.status in (RunStatus.SUCCESS.value,):
            return record  # Terminal success: nothing to do.

        record.status = RunStatus.RUNNING.value
        stage_results: dict[str, dict[str, Any]] = self._collect_results(record)

        for stage in STAGE_ORDER:
            rec = record.stages[stage.value]

            if rec.status == StageStatus.COMPLETED.value:
                continue  # Resume: never re-execute a completed stage.

            if rec.status == StageStatus.RUNNING.value:
                # Interrupted mid-stage: the stage never recorded completion,
                # so retry is safe only if the stage is idempotent (contract).
                # No attempt increment here — the execution below counts it.
                rec.error_name = "INTERRUPTED"
                rec.error_message = (
                    "previous run did not complete this stage; retrying. "
                    "Stage implementations must be idempotent."
                )

            contract = STAGE_CONTRACTS[stage]
            if not contract.implemented:
                # LOUD, never a silent PASS.
                rec.status = StageStatus.NOT_IMPLEMENTED.value
                rec.not_implemented_reason = contract.not_implemented_reason
                rec.completed_at = _utcnow()
                self.runs.save(record)
                continue

            stage_input = self._build_stage_input(stage, capture, event, stage_results, record)
            rec.status = StageStatus.RUNNING.value
            rec.attempts += 1
            rec.started_at = _utcnow()
            rec.input_ref = _summarize(stage_input)
            self.runs.save(record)

            try:
                output = self.executor.execute(stage, stage_input, event.correlation_id)
            except NotImplementedStage as exc:
                rec.status = StageStatus.NOT_IMPLEMENTED.value
                rec.not_implemented_reason = exc.reason
                rec.completed_at = _utcnow()
                self.runs.save(record)
                continue
            except KeyboardInterrupt:
                raise
            except Exception as exc:  # Explicit named failure, recoverable.
                rec.status = StageStatus.FAILED.value
                rec.error_name = type(exc).__name__
                rec.error_message = str(exc)[:1000]
                record.status = RunStatus.FAILED.value
                record.halt_reason = f"{stage.value} FAILED: {type(exc).__name__}: {str(exc)[:300]}"
                self.runs.save(record)
                self.events.set_status(event_id, "FAILED", note=record.halt_reason)
                return record

            if not output.ok:
                rec.status = StageStatus.FAILED.value
                rec.error_name = "STAGE_RETURNED_NOT_OK"
                rec.error_message = str(output.result.get("error", ""))[:1000]
                record.status = RunStatus.FAILED.value
                record.halt_reason = f"{stage.value} FAILED: {output.summary}"
                self.runs.save(record)
                self.events.set_status(event_id, "FAILED", note=record.halt_reason)
                return record

            rec.status = StageStatus.COMPLETED.value
            rec.completed_at = _utcnow()
            rec.output_summary = output.summary
            stage_results[stage.value] = output.result
            self.runs.save(record)

            # Governed halts: the pipeline stops here by rule, not by error.
            halt = self._governed_halt(stage, output)
            if halt is not None:
                status, reason = halt
                record.status = status
                record.halt_reason = reason
                self._mark_remaining_skipped(record, stage)
                self.runs.save(record)
                self.events.set_status(event_id, status, note=reason)
                return record

            if crash_after == stage.value:
                # Test hook: simulate a crash. The RUNNING/COMPLETED records
                # are already durable; resume continues from here.
                raise KeyboardInterrupt(f"simulated crash after {stage.value}")

        # All stages visited. SUCCESS requires every stage COMPLETED.
        missing = [s for s, r in record.stages.items() if r.status == StageStatus.NOT_IMPLEMENTED.value]
        if missing:
            record.status = RunStatus.INCOMPLETE.value
            record.halt_reason = (
                f"pipeline incomplete: stages not implemented: {', '.join(missing)}. "
                "No silent PASS was manufactured for any missing stage."
            )
        else:
            record.status = RunStatus.SUCCESS.value
            record.halt_reason = ""
        self.runs.save(record)
        self.events.set_status(event_id, record.status, note=record.halt_reason)
        return record

    def get_run(self, event_id: str) -> RunRecord | None:
        return self.runs.load(event_id)

    def query(self, status: str | None = None) -> list[RunRecord]:
        """Queryable state: what's pending, done, failed."""
        return self.runs.list_runs(status=status)

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    def _collect_results(self, record: RunRecord) -> dict[str, dict[str, Any]]:
        # Stage results are re-threaded from prior runs only via the executor
        # outputs recorded in this process. For resume across processes, the
        # output_summary carries the human-readable result; full outputs are
        # re-derived by re-running downstream stages from the capture + the
        # recorded summaries. (Full cross-process result replay is a known
        # limitation; stage inputs are rebuilt deterministically from capture.)
        return {}

    def _build_stage_input(
        self,
        stage: StageId,
        capture: dict[str, Any],
        event: Any,
        stage_results: dict[str, dict[str, Any]],
        record: RunRecord,
    ) -> dict[str, Any]:
        base: dict[str, Any] = {
            "lesson_id": event.lesson_id,
            "event_id": event.event_id,
            "correlation_id": event.correlation_id,
            "owner_id": capture.get("owner_id", "owner-1"),
            "naya_id": capture.get("naya_id", "naya-1"),
            "action": "learning.capture.process",
            "identity": capture.get("identity", {}),
            "mission": capture.get("mission", "prove the learning loop"),
            "objective": capture.get("objective", "execute the nine-node pipeline for one capture"),
            "capture": capture,
        }
        # Thread prior stage outputs forward (Naya 1's machine: each stage
        # consumes the previous stage's durable result).
        for prev_stage, result in stage_results.items():
            base[f"{prev_stage.lower()}_result"] = result
        return base

    def _governed_halt(self, stage: StageId, output: StageOutput) -> tuple[str, str] | None:
        if stage == StageId.LAW:
            status = output.result.get("decision", {}).get("status", "")
            if status == "BLOCKED":
                return (
                    RunStatus.BLOCKED.value,
                    f"LAW returned BLOCKED: {output.result.get('decision', {}).get('reason', '')[:300]}",
                )
            if status == "NEEDS_HUMAN_AUTHORIZATION":
                return (
                    RunStatus.BLOCKED.value,
                    "LAW returned NEEDS_HUMAN_AUTHORIZATION: awaiting human authorization (protected gate).",
                )
        if stage == StageId.VERIFY:
            if output.result.get("admitted") is False:
                codes = ",".join(output.result.get("reason_codes", []))
                return (
                    RunStatus.REJECTED.value,
                    f"VERIFY rejected the candidate: {codes}",
                )
        return None

    def _mark_remaining_skipped(self, record: RunRecord, after: StageId) -> None:
        seen_after = False
        for stage in STAGE_ORDER:
            if stage == after:
                seen_after = True
                continue
            if seen_after and record.stages[stage.value].status == StageStatus.PENDING.value:
                record.stages[stage.value].status = StageStatus.SKIPPED.value


def _utcnow() -> str:
    from datetime import datetime, timezone

    return datetime.now(timezone.utc).isoformat()


def _summarize(obj: dict[str, Any]) -> str:
    keys = sorted(obj.keys())
    shown = [k for k in keys if k not in ("capture",)]
    return f"keys={shown} (+capture)"
