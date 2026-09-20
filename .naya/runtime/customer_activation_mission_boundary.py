"""Small composition boundary from canonical customer activation to human mission.

This module owns no persistence and no decision engine. It proves that mission
qualification can begin only after activation has produced canonical Note Event
provenance, while preserving the human's explicit intent for Priority.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from human_mission import HumanMission, qualify_mission


class ActivationMissionBindingError(ValueError):
    """Raised when activated customer knowledge cannot safely enter mission qualification."""


@dataclass(frozen=True)
class ActivationMissionBinding:
    """In-memory handoff; no second mission store is created."""

    activation_event_ids: tuple[str, ...]
    activation_identities: tuple[str, ...]
    mission: HumanMission

    def to_successor(self) -> dict[str, Any]:
        return {
            "schema": "naya-power-activation-mission-binding/v1",
            "activation": {
                "canonical_event_ids": list(self.activation_event_ids),
                "document_identities": list(self.activation_identities),
            },
            "mission": self.mission.to_successor(),
            "authority": {
                "activation": "canonical Note Events",
                "mission": "human-stated mission qualification",
                "priority": "existing Priority selector",
            },
        }


def _require_promoted_activation(
    activation: dict[str, Any],
) -> tuple[tuple[str, ...], tuple[str, ...]]:
    if not isinstance(activation, dict):
        raise ActivationMissionBindingError("activation result must be an object")

    # A promotion list alone is insufficient: a caller must present a
    # non-terminal activation state that the activation authority considers
    # ready for the mission handoff. This prevents a conflicted/failed/partial
    # package from smuggling one successful-looking promotion into Priority.
    status = str(activation.get("status", "")).upper()
    if status not in {"READY", "VERIFIED"}:
        raise ActivationMissionBindingError(
            "customer activation must be READY/VERIFIED before mission qualification"
        )

    outcomes = activation.get("promotion")
    if not isinstance(outcomes, list) or not outcomes:
        raise ActivationMissionBindingError(
            "customer knowledge must be canonically promoted before mission qualification"
        )

    event_ids: list[str] = []
    identities: list[str] = []
    for outcome in outcomes:
        if not isinstance(outcome, dict) or outcome.get("status") not in {"CREATED", "REPLAY"}:
            raise ActivationMissionBindingError(
                "activation promotion must resolve to canonical CREATED/REPLAY outcomes"
            )
        event_id = outcome.get("event_id")
        identity = outcome.get("document_identity")
        if not isinstance(event_id, str) or not event_id.strip():
            raise ActivationMissionBindingError("canonical activation event_id is required")
        if not isinstance(identity, str) or not identity.strip():
            raise ActivationMissionBindingError("canonical activation document_identity is required")
        event_ids.append(event_id.strip())
        identities.append(identity.strip())

    return tuple(event_ids), tuple(identities)


def bind_activation_to_human_mission(
    activation: dict[str, Any], mission_input: dict[str, Any]
) -> ActivationMissionBinding:
    """Bind canonical activation provenance to an explicitly stated human mission."""
    event_ids, identities = _require_promoted_activation(activation)
    mission = qualify_mission(mission_input)
    return ActivationMissionBinding(event_ids, identities, mission)
