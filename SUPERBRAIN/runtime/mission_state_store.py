"""Persistent Mission State + Lead Mode host layer.

Keeps persistence and orchestration separate from the constitutional decision kernel.
The host supplies candidate actions and performs the selected action through its
existing authorized tools; this layer records the observed result and continues.
"""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any, Sequence

from naya_power_runtime import (
    ActionCandidate,
    ActionPlan,
    ExecutionReceipt,
    MissionState,
    activation_status,
    choose_next_action,
    cold_start,
    record_result,
)


class MissionStateStore:
    """Atomic JSON persistence for one active mission."""

    def __init__(self, path: str | Path):
        self.path = Path(path)

    def load(self) -> MissionState:
        if not self.path.exists():
            raise FileNotFoundError(f"Mission State not found: {self.path}")
        data = json.loads(self.path.read_text(encoding="utf-8"))
        state = MissionState.from_mapping(data)
        state.assert_valid()
        return state

    def save(self, state: MissionState) -> None:
        state.assert_valid()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        fd, temp_name = tempfile.mkstemp(
            prefix=f".{self.path.name}.", suffix=".tmp", dir=self.path.parent
        )
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                json.dump(state.to_dict(), handle, indent=2, ensure_ascii=False)
                handle.write("\n")
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temp_name, self.path)
        finally:
            if os.path.exists(temp_name):
                os.unlink(temp_name)


class LeadModeEngine:
    """RESTORE → LEAD → HANDOFF → VERIFY → UPDATE → CONTINUE."""

    def __init__(self, store: MissionStateStore):
        self.store = store

    def restore(self) -> dict[str, Any]:
        """Restore only verified/current operational context needed to lead."""
        return cold_start(self.store.load())

    def activate(self) -> dict[str, Any]:
        """Return an honest, machine-checkable activation result."""
        return activation_status(self.store.load())

    def choose(self, candidates: Sequence[ActionCandidate]) -> ActionPlan:
        """Choose the highest-value eligible action without executing it silently."""
        return choose_next_action(self.store.load(), candidates)

    def accept_execution(self, plan: ActionPlan, receipt: ExecutionReceipt) -> MissionState:
        """Record observed execution evidence and persist the next mission state."""
        state = self.store.load()
        updated = record_result(state, plan, receipt)
        self.store.save(updated)
        return updated
