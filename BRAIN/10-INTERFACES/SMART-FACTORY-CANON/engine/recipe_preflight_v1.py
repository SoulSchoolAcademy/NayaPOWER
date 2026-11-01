#!/usr/bin/env python3
"""PROPOSED read-only Naya RECIPE preflight. NOT a production release gate.

Uses current factory index and working store, never a new parts registry.
Exit 0 structural pass; exit 1 fail; exit 2 unavailable/unknown source.
Actual action auth, responsive UI and independent verdict require separate proof.
"""
import argparse
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
CANON = BASE / "CANONICAL-PIECE-INDEX.json"
STORE = BASE / "pieces.json"
SMALL = {(320, 700), (390, 844), (768, 1024), (1440, 900)}
UNKNOWN = {"", "UNKNOWN", "UNVERIFIED", "UNASSIGNED", "UNWIRED"}
STATES = {"loading", "ready", "empty", "error", "denied", "offline", "success"}

def inspect(recipe, index, store, mode="draft"):
    errors, warnings = [], []
    def err(where, msg): errors.append(where + ": " + msg)
    def warn(where, msg): warnings.append(where + ": " + msg)
    def field(obj, name, where, release=False):
        val = obj.get(name) if isinstance(obj, dict) else None
        if not isinstance(val, str) or not val.strip():
            err(where + "." + name, "nonempty text required")
        elif val.strip() in UNKNOWN:
            if mode == "release_candidate" and release:
                err(where + "." + name, "unresolved placeholder")
            else: warn(where + "." + name, "unresolved placeholder")
        return val
    if not isinstance(recipe, dict): return ["root: object required"], []
    if recipe.get("contract") != "NAYA_APP_RECIPE_V1": err("contract", "unsupported")
    if recipe.get("version") != 1: err("version", "requires integer 1")
    if recipe.get("build_status") not in ("draft", "release_candidate"):
        err("build_status", "unknown")
    pi = recipe.get("project_intelligence")
    if not isinstance(pi, dict): err("project_intelligence", "object required"); pi = {}
    for k in ("project_id", "owner", "source_sha", "mission_ref", "human_outcome"):
        field(pi, k, "project_intelligence", k != "human_outcome")
    if mode == "release_candidate" and pi.get("authority_status") != "verified":
        err("project_intelligence.authority_status", "verified authority required")
    r = recipe.get("recipe")
    if not isinstance(r, dict): err("recipe", "object required"); r = {}
    for k in ("app_id", "audience", "purpose"): field(r, k, "recipe")
    scenes = r.get("scenes")
    if not isinstance(scenes, list) or not scenes:
        err("recipe.scenes", "nonempty list required"); scenes = []
    known_scenes, needed_parts, needed_actions, needed_data = set(), set(), set(), set()
    for i, scene in enumerate(scenes):
        w = f"recipe.scenes[{i}]"
        if not isinstance(scene, dict): err(w, "object required"); continue
        for k in ("id", "human_job", "hero", "ambient", "primary_action_id"):
            field(scene, k, w)
        sid = scene.get("id")
        if isinstance(sid, str):
            if sid in known_scenes: err(w + ".id", "duplicate")
            known_scenes.add(sid)
        context = scene.get("context")
        if not isinstance(context, list) or len(context) > 3 or any(not isinstance(x, str) or not x.strip() for x in context):
            err(w + ".context", "0–3 meaningful facts")
        ids = scene.get("part_ids")
        if not isinstance(ids, list) or not ids: err(w + ".part_ids", "nonempty list required")
        else: needed_parts.update(x for x in ids if isinstance(x, str))
        ids = scene.get("data_refs")
        if not isinstance(ids, list): err(w + ".data_refs", "list required")
        else: needed_data.update(x for x in ids if isinstance(x, str))
        states = scene.get("states")
        if not isinstance(states, list) or not {"ready", "error"}.issubset(states) or set(states) - STATES:
            err(w + ".states", "ready/error and known state names required")
        for k in ("primary_action_id", "secondary_action_id"):
            val = scene.get(k)
            if isinstance(val, str) and val: needed_actions.add(val)
    for i, scene in enumerate(scenes):
        if isinstance(scene, dict) and scene.get("next_screen") and scene["next_screen"] not in known_scenes:
            err(f"recipe.scenes[{i}].next_screen", "unknown next scene")
    parts = recipe.get("parts")
    if not isinstance(parts, list) or not parts: err("parts", "nonempty list required"); parts = []
    seen = set()
    for i, part in enumerate(parts):
        w = f"parts[{i}]"
        if not isinstance(part, dict): err(w, "object required"); continue
        pid = part.get("id")
        if not isinstance(pid, str) or not pid: err(w + ".id", "text required"); continue
        if pid in seen: err(w + ".id", "duplicate declaration")
        seen.add(pid)
        if (index.get("pieces", {}).get(pid) or {}).get("status") != "canonical":
            err(w + ".id", "not canonical; refuse new-build selection")
        if pid not in store: err(w + ".id", "missing from current working store")
        field(part, "slot", w)
    for missing in sorted(needed_parts - seen): err("recipe.scenes.part_ids", missing + " undeclared")
    shell = recipe.get("shell")
    if not isinstance(shell, dict): err("shell", "object required"); shell = {}
    for k in ("shell_ref", "navigation_ref", "scroll_policy"): field(shell, k, "shell")
    viewports = shell.get("responsive_viewports")
    if not isinstance(viewports, list) or any(not isinstance(v, list) or len(v) != 2 for v in viewports):
        err("shell.responsive_viewports", "width/height pairs required")
    elif not SMALL.issubset({tuple(v) for v in viewports}):
        err("shell.responsive_viewports", "missing canonical device coverage")
    data = recipe.get("data")
    if not isinstance(data, dict): err("data", "object required"); data = {}
    datasets = data.get("datasets")
    if not isinstance(datasets, list): err("data.datasets", "list required"); datasets = []
    known_data = set()
    for i, item in enumerate(datasets):
        if not isinstance(item, dict): err(f"data.datasets[{i}]", "object required"); continue
        known_data.add(field(item, "id", f"data.datasets[{i}]"))
        for k in ("source_ref", "scope", "permission_ref"): field(item, k, f"data.datasets[{i}]", True)
    for missing in sorted(needed_data - known_data): err("recipe.scenes.data_refs", missing + " undeclared")
    actions = data.get("actions")
    if not isinstance(actions, list): err("data.actions", "list required"); actions = []
    known_actions = set()
    for i, action in enumerate(actions):
        w = f"data.actions[{i}]"
        if not isinstance(action, dict): err(w, "object required"); continue
        known_actions.add(field(action, "id", w))
        for k in ("label", "service_ref", "permission_ref", "outcome_receipt_ref"):
            field(action, k, w, k != "label")
        if action.get("binding_status") not in ("wired", "unwired"):
            err(w + ".binding_status", "must be wired or unwired")
        elif action.get("binding_status") != "wired":
            (err if mode == "release_candidate" else warn)(w, "action is unwired")
    for missing in sorted(needed_actions - known_actions): err("recipe.scenes.action_ids", missing + " undeclared")
    gate = recipe.get("gate")
    if not isinstance(gate, dict): err("gate", "object required"); gate = {}
    if mode == "release_candidate":
        if recipe.get("build_status") != "release_candidate": err("build_status", "must match release_candidate mode")
        if gate.get("independent") is not True: err("gate.independent", "separate verifier required")
        if gate.get("status") != "independently_verified": err("gate.status", "independent evidence required")
        if not gate.get("proof_refs"): err("gate.proof_refs", "nonempty proof references required")
        for k in ("source_sha", "deployed_sha", "privacy_deny_proof", "accessible_render_proof"):
            field(gate, k, "gate", True)
        if gate.get("source_sha") != gate.get("deployed_sha"): err("gate.versions", "tested and deployed SHA differ")
    return errors, warnings

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("recipe", type=Path)
    ap.add_argument("--mode", choices=("draft", "release_candidate"), default="draft")
    a = ap.parse_args()
    try:
        recipe = json.loads(a.recipe.read_text(encoding="utf-8"))
        index = json.loads(CANON.read_text(encoding="utf-8"))
        store = json.loads(STORE.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print(json.dumps({"status": "UNKNOWN", "reason": str(exc)})); return 2
    errors, warnings = inspect(recipe, index, store, a.mode)
    print(json.dumps({"status": "DENY" if errors else "STRUCTURAL_PASS_NOT_RELEASE_PROOF",
        "errors": errors, "warnings": warnings,
        "note": "Only a read-only contract preflight. Actual security, visual, and deployment proof owed."}, indent=2))
    return 1 if errors else 0

if __name__ == "__main__":
    raise SystemExit(main())
