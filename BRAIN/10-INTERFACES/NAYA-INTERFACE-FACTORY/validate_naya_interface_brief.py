#!/usr/bin/env python3
"""Fail-closed semantic gate for Naya Interface Brief V1.

Uses only the Python standard library. This is a pre-build design-contract gate.
It does not replace the Smart Factory's existing build-contract or 13-feature
validators, and it does not certify runtime, privacy, accessibility, or visual
quality merely because a JSON brief passes.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


CONTRACT_ID = "NAYA-INTERFACE-BRIEF"
CONTRACT_VERSION = "1.0.0"
ALLOWED_TRUTH = {
    "live", "cached", "stale", "local", "demo", "predicted",
    "unavailable", "unknown",
}
ALLOWED_STATES = {
    "initial", "loading", "live", "cached", "stale", "empty", "error",
    "offline", "unavailable", "forbidden", "pending", "success",
    "rejected", "timeout",
}


def _text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _list(value: Any) -> bool:
    return isinstance(value, list)


def _need(mapping: Any, key: str, where: str, errors: list[str]) -> Any:
    if not isinstance(mapping, dict):
        errors.append(f"{where} must be an object")
        return None
    if key not in mapping:
        errors.append(f"{where}.{key} is required")
        return None
    return mapping[key]


def validate_brief(brief: Any, pieces: dict[str, Any] | None = None, stage: str = "prebuild") -> list[str]:
    """Return actionable semantic violations; an empty list means PASS."""
    errors: list[str] = []

    if not isinstance(brief, dict):
        return ["brief root must be a JSON object"]

    if brief.get("contract_id") != CONTRACT_ID:
        errors.append(f"contract_id must equal {CONTRACT_ID}")
    if brief.get("contract_version") != CONTRACT_VERSION:
        errors.append(f"contract_version must equal {CONTRACT_VERSION}")

    project = brief.get("project")
    for key in ("id", "name", "pi_ref", "source_of_truth"):
        if not isinstance(project, dict) or not _text(project.get(key)):
            errors.append(f"project.{key} is required and must be non-empty text")

    outcome = brief.get("outcome")
    for key in ("primary_user", "job", "success"):
        if not isinstance(outcome, dict) or not _text(outcome.get(key)):
            errors.append(f"outcome.{key} is required and must be non-empty text")

    authority = brief.get("design_authority")
    for key in ("design_contract_ref", "design_standard_ref"):
        if not isinstance(authority, dict) or not _text(authority.get(key)):
            errors.append(f"design_authority.{key} must reference the current authority")

    shell = brief.get("app_shell")
    for key in ("navigation_model", "global_context", "search_policy"):
        if not isinstance(shell, dict) or not _text(shell.get(key)):
            errors.append(f"app_shell.{key} must be explicitly defined")

    data_contracts = brief.get("data_contracts")
    if not _list(data_contracts) or not data_contracts:
        errors.append("data_contracts must contain at least one declared data source")
        data_contracts = []
    data_by_id: dict[str, dict[str, Any]] = {}
    for i, item in enumerate(data_contracts):
        where = f"data_contracts[{i}]"
        if not isinstance(item, dict):
            errors.append(f"{where} must be an object")
            continue
        ident = item.get("id")
        if not _text(ident):
            errors.append(f"{where}.id must be non-empty")
            continue
        if ident in data_by_id:
            errors.append(f"duplicate data contract id: {ident}")
        data_by_id[ident] = item
        for field in ("entity", "source_ref", "authority", "truth_state", "freshness", "empty_state", "error_state"):
            if not _text(item.get(field)):
                errors.append(f"{where}.{field} must be explicit and non-empty")
        if item.get("truth_state") not in ALLOWED_TRUTH:
            errors.append(f"{where}.truth_state is not a supported truth state")
        if item.get("truth_state") in {"unknown", "unavailable", "demo", "predicted"} and item.get("authority") == "canonical":
            errors.append(f"{where} cannot claim canonical authority while truth_state is {item.get('truth_state')}")

    components = brief.get("component_manifest")
    if not _list(components) or not components:
        errors.append("component_manifest must name at least one reusable part")
        components = []
    seen_parts: set[str] = set()
    for i, item in enumerate(components):
        where = f"component_manifest[{i}]"
        if not isinstance(item, dict):
            errors.append(f"{where} must be an object")
            continue
        piece_id = item.get("piece_id")
        if not _text(piece_id):
            errors.append(f"{where}.piece_id is required")
            continue
        if piece_id in seen_parts:
            errors.append(f"duplicate component manifest entry: {piece_id}")
        seen_parts.add(piece_id)
        for field in ("registry_path", "role", "use_when", "registry_status"):
            if not _text(item.get(field)):
                errors.append(f"{where}.{field} is required")
        if item.get("registry_status") in {"candidate", "unverified", "retired"}:
            errors.append(f"{where} uses {piece_id} with non-buildable registry_status {item.get('registry_status')}")
        if pieces is not None:
            registry_item = pieces.get(piece_id)
            if registry_item is None:
                errors.append(f"{where}: {piece_id} does not resolve in the supplied pieces registry")
            elif item.get("registry_status") == "reference" and registry_item.get("reference") is not True:
                errors.append(f"{where}: {piece_id} is declared reference but registry does not mark reference=true")

    viewports = brief.get("viewport_matrix")
    if not _list(viewports) or len(viewports) < 4:
        errors.append("viewport_matrix must cover at least four representative viewports")
        viewports = []
    widths: set[int] = set()
    for i, item in enumerate(viewports):
        where = f"viewport_matrix[{i}]"
        if not isinstance(item, dict):
            errors.append(f"{where} must be an object")
            continue
        width, height = item.get("width"), item.get("height")
        if not isinstance(width, int) or width < 320:
            errors.append(f"{where}.width must be an integer >= 320 CSS px")
        else:
            widths.add(width)
        if not isinstance(height, int) or height < 256:
            errors.append(f"{where}.height must be an integer >= 256 CSS px")
    if widths and min(widths) > 320:
        errors.append("viewport_matrix must include narrow 320 CSS px reflow coverage")
    if widths and max(widths) < 1440:
        errors.append("viewport_matrix must include a wide desktop viewport (>= 1440 CSS px)")

    screens = brief.get("screens")
    if not _list(screens) or not screens:
        errors.append("screens must contain at least one complete screen contract")
        screens = []
    seen_ids: set[str] = set()
    seen_routes: set[str] = set()
    for i, screen in enumerate(screens):
        where = f"screens[{i}]"
        if not isinstance(screen, dict):
            errors.append(f"{where} must be an object")
            continue
        sid, route = screen.get("id"), screen.get("route")
        if not _text(sid):
            errors.append(f"{where}.id is required")
        elif sid in seen_ids:
            errors.append(f"duplicate screen id: {sid}")
        else:
            seen_ids.add(sid)
        if not _text(route):
            errors.append(f"{where}.route is required")
        elif route in seen_routes:
            errors.append(f"duplicate screen route: {route}")
        else:
            seen_routes.add(route)
        if not _text(screen.get("job")) or len(str(screen.get("job", "")).strip()) < 8:
            errors.append(f"{where}.job must describe one specific user job")
        if not _text(screen.get("entry_context")):
            errors.append(f"{where}.entry_context must state how the screen is reached")

        first = screen.get("first_view")
        if not isinstance(first, dict):
            errors.append(f"{where}.first_view is required")
        else:
            for field in ("orientation", "focal_point"):
                if not _text(first.get(field)):
                    errors.append(f"{where}.first_view.{field} must be explicit")
            support = first.get("supporting_items", [])
            if not _list(support):
                errors.append(f"{where}.first_view.supporting_items must be an array")
            elif len(support) > 3:
                errors.append(f"{where}.first_view has more than three supporting items")
            secondary = first.get("secondary_actions", [])
            if not _list(secondary):
                errors.append(f"{where}.first_view.secondary_actions must be an array")
            elif len(secondary) > 1:
                errors.append(f"{where}.first_view has more than one visible secondary action")
            primary = first.get("primary_action")
            visible_actions = (1 if _text(primary) else 0) + (len(secondary) if _list(secondary) else 0)
            if visible_actions > 2:
                errors.append(f"{where}.first_view exposes more than two first-view actions")

        sections = screen.get("sections")
        if not _list(sections) or not sections:
            errors.append(f"{where}.sections must contain at least one purposeful section")
            sections = []
        focal_sections = 0
        for j, section in enumerate(sections):
            sw = f"{where}.sections[{j}]"
            if not isinstance(section, dict):
                errors.append(f"{sw} must be an object")
                continue
            if not _text(section.get("purpose")):
                errors.append(f"{sw}.purpose must explain why this section exists")
            if section.get("priority") == "focal":
                focal_sections += 1
        if focal_sections != 1:
            errors.append(f"{where} must have exactly one focal section; found {focal_sections}")

        dependencies = screen.get("data_dependencies")
        if not _list(dependencies):
            errors.append(f"{where}.data_dependencies must be an array")
        else:
            for dep in dependencies:
                if dep not in data_by_id:
                    errors.append(f"{where} references undeclared data contract: {dep}")

        states = screen.get("states")
        if not _list(states):
            errors.append(f"{where}.states must be an array")
            states = []
        state_names: set[str] = set()
        for j, state in enumerate(states):
            sw = f"{where}.states[{j}]"
            if not isinstance(state, dict):
                errors.append(f"{sw} must be an object")
                continue
            name = state.get("state")
            if name not in ALLOWED_STATES:
                errors.append(f"{sw}.state is unsupported: {name}")
            state_names.add(name)
            for field in ("presentation", "recovery"):
                if not _text(state.get(field)):
                    errors.append(f"{sw}.{field} must be explicit")
        for required_state in ("loading", "error"):
            if required_state not in state_names:
                errors.append(f"{where} must define a {required_state} state")
        if not ({"empty", "unavailable", "forbidden"} & state_names):
            errors.append(f"{where} must define an honest empty/unavailable/forbidden state")

        actions = screen.get("actions")
        if not _list(actions):
            errors.append(f"{where}.actions must be an array")
            actions = []
        action_ids: set[str] = set()
        for j, action in enumerate(actions):
            aw = f"{where}.actions[{j}]"
            if not isinstance(action, dict):
                errors.append(f"{aw} must be an object")
                continue
            aid = action.get("id")
            if not _text(aid) or aid in action_ids:
                errors.append(f"{aw}.id must be present and unique")
            action_ids.add(aid)
            for field in ("label", "intent", "actor", "scope", "authority", "effect", "success_signal", "failure_recovery"):
                if not _text(action.get(field)):
                    errors.append(f"{aw}.{field} must describe the real causal contract")
            if not isinstance(action.get("reversible"), bool):
                errors.append(f"{aw}.reversible must be a boolean")
            if not isinstance(action.get("requires_confirmation"), bool):
                errors.append(f"{aw}.requires_confirmation must be a boolean")

        responsive = screen.get("responsive")
        if not isinstance(responsive, dict):
            errors.append(f"{where}.responsive is required")
        else:
            for field in ("small", "medium", "large"):
                if not _text(responsive.get(field)):
                    errors.append(f"{where}.responsive.{field} must define the composition")
            if responsive.get("horizontal_overflow") not in {"none", "explicit-two-dimensional-region-only"}:
                errors.append(f"{where}.responsive.horizontal_overflow must be explicit and constrained")
            if responsive.get("no_clipping") is not True:
                errors.append(f"{where}.responsive.no_clipping must be true")
            if responsive.get("safe_area") is not True:
                errors.append(f"{where}.responsive.safe_area must be true")
            if responsive.get("keyboard_safe") is not True:
                errors.append(f"{where}.responsive.keyboard_safe must be true")

        accessibility = screen.get("accessibility")
        if not isinstance(accessibility, dict):
            errors.append(f"{where}.accessibility is required")
        else:
            if accessibility.get("target_standard") != "WCAG-2.2-AA":
                errors.append(f"{where}.accessibility.target_standard must be WCAG-2.2-AA")
            if not isinstance(accessibility.get("minimum_target_px"), int) or accessibility.get("minimum_target_px", 0) < 44:
                errors.append(f"{where}.accessibility.minimum_target_px must meet the 44px Naya house rule")
            for field in ("contrast_checked", "keyboard_complete", "focus_visible", "focus_not_obscured", "reduced_motion", "screen_reader_semantics", "zoom_reflow_checked"):
                if not isinstance(accessibility.get(field), bool):
                    errors.append(f"{where}.accessibility.{field} must be explicitly recorded as a boolean")
                elif stage == "release" and accessibility.get(field) is not True:
                    errors.append(f"{where}.accessibility.{field} must be true before release")

        acceptance = screen.get("acceptance")
        if not _list(acceptance) or not acceptance or any(not _text(x) for x in acceptance):
            errors.append(f"{where}.acceptance must contain concrete, testable criteria")

        # Unknown/demo/predicted inputs may not be presented as live on this screen.
        if isinstance(dependencies, list):
            referenced = [data_by_id.get(dep) for dep in dependencies]
            unproven = {
                d.get("id") for d in referenced
                if isinstance(d, dict) and d.get("truth_state") in {"unknown", "unavailable", "demo", "predicted"}
            }
            if unproven and "live" in state_names:
                errors.append(f"{where} declares live state while depending on unproven data: {sorted(unproven)}")

    gates = brief.get("quality_gates")
    if not isinstance(gates, dict):
        errors.append("quality_gates is required")
    else:
        score = gates.get("minimum_dimension_score")
        if not isinstance(score, (int, float)) or score < 9 or score > 10:
            errors.append("quality_gates.minimum_dimension_score must be between 9.0 and 10")
        if gates.get("independent_verification_required") is not True:
            errors.append("quality_gates.independent_verification_required must be true")
        hard = gates.get("hard_gates")
        if not _list(hard) or not hard:
            errors.append("quality_gates.hard_gates must contain at least one non-negotiable gate")

    return errors


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a Naya Interface Brief V1 before factory dispatch.")
    parser.add_argument("brief", type=Path, help="Path to the brief JSON file")
    parser.add_argument("--pieces", type=Path, help="Optional current Smart Factory pieces.json registry")
    parser.add_argument("--stage", choices=("prebuild", "release"), default="prebuild", help="prebuild validates completeness; release also requires completed accessibility checks")
    args = parser.parse_args()

    try:
        brief = load_json(args.brief)
        pieces = load_json(args.pieces) if args.pieces else None
        if pieces is not None and not isinstance(pieces, dict):
            raise ValueError("pieces registry must be a JSON object keyed by piece ID")
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        result = {"status": "BLOCKED", "errors": [f"Could not load required JSON input: {exc}"]}
        print(json.dumps(result, indent=2))
        return 2

    errors = validate_brief(brief, pieces, stage=args.stage)
    result = {
        "status": "PASS" if not errors else "BLOCKED",
        "contract_id": brief.get("contract_id"),
        "contract_version": brief.get("contract_version"),
        "project": brief.get("project", {}).get("name") if isinstance(brief.get("project"), dict) else None,
        "screens_checked": len(brief.get("screens", [])) if isinstance(brief.get("screens"), list) else 0,
        "components_checked": len(brief.get("component_manifest", [])) if isinstance(brief.get("component_manifest"), list) else 0,
        "registry_checked": str(args.pieces) if args.pieces else None,
        "stage": args.stage,
        "errors": errors,
        "note": "PASS means the brief meets this semantic pre-build contract only; it does not certify implementation, visual quality, security, accessibility conformance, deployment, or production behavior."
    }
    print(json.dumps(result, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
