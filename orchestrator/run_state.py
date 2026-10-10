"""Per-run stage tracking: queryable state for every orchestrated run.

One run per event (run_id == event_id). Each stage record carries the shared
correlation_id so the whole chain is traceable. Writes are atomic
(write-temp-then-rename) so a crash can never leave a half-written record.

Stage statuses:
  PENDING         — not yet attempted
  RUNNING         — currently executing (a crash here means "interrupted")
  COMPLETED       — executed, result recorded
  FAILED          — raised an error; named, recoverable; resume retries it
  NOT_IMPLEMENTED — no implementation exists; named reason; never a silent PASS
  SKIPPED         — not attempted because the run halted before reaching it

Run statuses:
  RUNNING | INCOMPLETE | FAILED | BLOCKED | REJECTED | SUCCESS
SUCCESS requires every stage COMPLETED. With missing stages the ceiling is
INCOMPLETE — explicit, with the missing stages named.
"""

from __future__ import annotations

import json
import os
import tempfile
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from .stages import STAGE_ORDER, StageId


def _utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class StageRecord:
    stage: str
    status: str = "PENDING"
    correlation_id: str = ""
    attempts: int = 0
    started_at: str | None = None
    completed_at: str | None = None
    input_ref: str = ""
    output_summary: str = ""
    error_name: str = ""
    error_message: str = ""
    not_implemented_reason: str = ""


@dataclass
class RunRecord:
    run_id: str
    event_id: str
    correlation_id: str
    lesson_id: str
    status: str = "RUNNING"
    created_at: str = field(default_factory=_utcnow)
    updated_at: str = field(default_factory=_utcnow)
    stages: dict[str, StageRecord] = field(default_factory=dict)
    halt_reason: str = ""

    def to_dict(self) -> dict:
        d = asdict(self)
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "RunRecord":
        stages = {k: StageRecord(**v) for k, v in d.get("stages", {}).items()}
        return cls(
            run_id=d["run_id"],
            event_id=d["event_id"],
            correlation_id=d["correlation_id"],
            lesson_id=d["lesson_id"],
            status=d.get("status", "RUNNING"),
            created_at=d.get("created_at", ""),
            updated_at=d.get("updated_at", ""),
            stages=stages,
            halt_reason=d.get("halt_reason", ""),
        )


class RunStore:
    """Atomic JSON run records, one file per run. Queryable state."""

    def __init__(self, directory: str | Path):
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)

    def _path(self, run_id: str) -> Path:
        # run_id is evt_<32 hex> — safe as a filename.
        safe = "".join(c for c in run_id if c.isalnum() or c in ("_", "-"))
        return self.directory / f"{safe}.json"

    def create(self, run_id: str, event_id: str, correlation_id: str, lesson_id: str) -> RunRecord:
        existing = self.load(run_id)
        if existing is not None:
            return existing  # Resume path: never create twice.
        record = RunRecord(
            run_id=run_id,
            event_id=event_id,
            correlation_id=correlation_id,
            lesson_id=lesson_id,
            stages={s.value: StageRecord(stage=s.value, correlation_id=correlation_id) for s in STAGE_ORDER},
        )
        self.save(record)
        return record

    def load(self, run_id: str) -> RunRecord | None:
        path = self._path(run_id)
        if not path.exists():
            return None
        return RunRecord.from_dict(json.loads(path.read_text(encoding="utf-8")))

    def save(self, record: RunRecord) -> None:
        record.updated_at = _utcnow()
        path = self._path(record.run_id)
        fd, tmp = tempfile.mkstemp(dir=str(self.directory), suffix=".tmp")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(record.to_dict(), f, indent=2, sort_keys=True)
                f.write("\n")
            os.replace(tmp, path)  # Atomic: crash-safe.
        except BaseException:
            try:
                os.unlink(tmp)
            except OSError:
                pass
            raise

    def list_runs(self, status: str | None = None) -> list[RunRecord]:
        runs = []
        for path in sorted(self.directory.glob("*.json")):
            try:
                record = RunRecord.from_dict(json.loads(path.read_text(encoding="utf-8")))
            except (json.JSONDecodeError, KeyError):
                continue
            if status is None or record.status == status:
                runs.append(record)
        return runs

    # ---- queryable state -------------------------------------------------

    def pending_stages(self, run_id: str) -> list[str]:
        record = self.load(run_id)
        if record is None:
            return []
        return [s for s, r in record.stages.items() if r.status in ("PENDING", "RUNNING", "FAILED")]

    def completed_stages(self, run_id: str) -> list[str]:
        record = self.load(run_id)
        if record is None:
            return []
        return [s for s, r in record.stages.items() if r.status == "COMPLETED"]

    def missing_stages(self, run_id: str) -> list[str]:
        record = self.load(run_id)
        if record is None:
            return []
        return [s for s, r in record.stages.items() if r.status == "NOT_IMPLEMENTED"]

    def failed_stages(self, run_id: str) -> list[str]:
        record = self.load(run_id)
        if record is None:
            return []
        return [s for s, r in record.stages.items() if r.status == "FAILED"]
