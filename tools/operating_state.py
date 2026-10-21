#!/usr/bin/env python3
"""Operating state as data — emitter, validator, and cold-activation proof.

WHY: every Naya seat used to reconstruct the operating picture by parsing
prose (LIVE-PLAN.md, board comments, drain-order markdown). This tool emits
two machine-readable artifacts any seat can load at activation and execute
against:

  OPERATING-STATE.json  — tip, queue shape (tier x action), the tip's own
                          failing checks, the balance gauge's four numbers,
                          the laws pointer, and the HOLD-HUMAN set.
  QUEUE-CONTRACT.json   — the live drain as data: per open PR its tier,
                          its one action, the cure text, and the owner.

ONE PUBLISHER RULE: this emitter is run by the existing hub-refresh owner
(the hourly job that already publishes HUB-STATE.md / MISSION-STATE.md to
live/mission-state) and its outputs ride that same publish. It is not a
second publisher; see tools/OPERATING-STATE.md for the wiring.

Sources (all live, all derived — nothing hand-written):
  - tip:            GET /git/refs/heads/main (the ref is the anchor, never
                    the commits list endpoint, which can serve stale data)
  - queue:          GET /pulls?state=open (fully paginated) + per-PR files
                    and check-runs at the exact head
  - tiers:          tools/pr_flow_tier.py classify_tier (Balanced Machine
                    step 1, on main) — imported, never re-implemented
  - actions:        the drain-order rules (gate-redesign/DRAIN-ORDER +
                    Balanced Machine design §2/§7), encoded in derive_action
  - gauge numbers:  the newest GAUGE-READ-*.md in the Balanced Machine
                    files dir, parsed, with the source file + its read
                    anchor carried in the output (gauge PR #2863's
                    tools/balance_gauge.py supersedes this reader the day
                    it merges — the field records which source produced
                    the numbers)

Modes:
  emit       build both artifacts from live data, validate them against
             the shipped schemas, refuse to publish a state whose tip does
             not match the live ref at publish time, write the JSONs.
  validate   validate existing JSON files against the schemas; every
             failure prints `MISSING: ... — CURE: ... (owner: ...)`.
  cold       the cold-activation proof: load ONLY the two artifacts (+ the
             laws pointer inside the state) and answer the five questions
             a cold seat needs, printed as the activation receipt.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = "SoulSchoolAcademy/NayaPOWER"
TOOLS_DIR = Path(__file__).resolve().parent

# The drain-order rules, encoded (Balanced Machine, ratified 2026-10-21).
HOLD_HUMAN = {
    1130: "Shawn's decision only: ratification of Governance Contract V1.",
    2838: "Shawn's decision: GH013 / Hub Feeds Emit — ruleset-bypass/deploy-key authority (governor territory).",
    2385: "Shawn's decision: workflow-class — adding a Required gate is a ruleset/governor act.",
    2680: "Shawn's decision: workflow-class per the standing record.",
    2747: "Shawn's decision: workflow-class per the standing record.",
}
CLOSE_CANDIDATE = {
    2848: "Survivor: SN-1771's door landing — close citing the landing once VERIFIED_LIVE.",
    2851: "Survivor: SN-1772's door landing — close citing the landing once VERIFIED_LIVE.",
    2836: "Survivor: mechanical index regeneration on the landed tree — indexes are never hand-merged.",
}
PAPERWORK_CHECKS = {
    "Team review + scorecard receipt",
    "Receipt gate (evidence or it didn't happen)",
    "Receipt pin — exact head SHA",
    "Unified paperwork gate",
    "Unified PR paperwork gate",
    "Unified paperwork — tier + cross-seat scorecard + live evidence",
}
TIER_FLOOR = {"A": 9.5, "B": 8.0}


# --------------------------------------------------------------------------
# API access (pluggable: NAYA_GH_API env, else the workspace wrapper, else gh)
# --------------------------------------------------------------------------

def gh_api(method: str, path: str):
    override = os.environ.get("NAYA_GH_API")
    candidates = []
    if override:
        candidates.append(override.split())
    wrapper = Path.home() / "workspace" / "naya" / "bin" / "gh-api"
    if wrapper.exists():
        candidates.append([str(wrapper)])
    candidates.append(["gh", "api"])
    last_err = None
    for cmd in candidates:
        try:
            if cmd[0].endswith("gh-api"):
                full = cmd + [method, f"/repos/{REPO}{path}"]
            else:
                full = cmd + ["-X", method, f"repos/{REPO}{path}"]
            out = subprocess.run(full, capture_output=True, text=True, timeout=120)
            if out.returncode == 0 and out.stdout.strip():
                return json.loads(out.stdout)
            last_err = out.stderr.strip() or out.stdout.strip()
        except Exception as exc:  # noqa: BLE001
            last_err = str(exc)
    raise RuntimeError(f"gh-api {method} {path} failed: {last_err}")


def live_tip() -> str:
    return gh_api("GET", "/git/refs/heads/main")["object"]["sha"]


def paginated(path: str, per_page: int = 100) -> list:
    items, page = [], 1
    while True:
        sep = "&" if "?" in path else "?"
        batch = gh_api("GET", f"{path}{sep}per_page={per_page}&page={page}")
        if not batch:
            break
        items.extend(batch)
        if len(batch) < per_page:
            break
        page += 1
    return items


def all_check_runs(sha: str) -> list[dict]:
    runs, page = [], 1
    while True:
        resp = gh_api("GET", f"/commits/{sha}/check-runs?per_page=100&page={page}")
        batch = resp.get("check_runs", []) if isinstance(resp, dict) else []
        runs.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    return runs


def latest_failing_checks(sha: str) -> list[str]:
    runs = all_check_runs(sha)
    latest: dict[str, dict] = {}
    for run in runs:
        name = run.get("name", "")
        prev = latest.get(name)
        if prev is None or (run.get("started_at") or "") >= (prev.get("started_at") or ""):
            latest[name] = run
    failing = []
    for name, run in latest.items():
        if run.get("status") == "completed" and run.get("conclusion") in {
            "failure", "timed_out", "cancelled", "action_required", "startup_failure",
        }:
            failing.append(name)
    return sorted(failing)


# --------------------------------------------------------------------------
# Tier + action derivation (pure — unit-tested without the API)
# --------------------------------------------------------------------------

def classify(title: str, paths: list[str]) -> tuple[str, str]:
    sys.path.insert(0, str(TOOLS_DIR))
    try:
        from pr_flow_tier import classify_tier  # Balanced Machine step 1, on main
        result = classify_tier(title, paths)
        return result["tier"], result.get("reason", "")
    except Exception:  # noqa: BLE001 — classifier absent: fail safe to A
        return "A", "classifier unavailable — fail-safe to Tier A"


def derive_action(number: int, tier: str, mergeable_state: str,
                  failing_at_head: list[str], failing_at_base: list[str]) -> dict:
    """Attribution is by merge-base (the balance gauge's method): a red at
    the head counts against the PR only if it was not already red at the
    PR's merge-base with main. Reds inherited from the base are cured by a
    branch update, never charged to the author as content defects."""
    if number in HOLD_HUMAN:
        return {"action": "HOLD-HUMAN", "cure": HOLD_HUMAN[number], "owner": "Shawn"}
    if number in CLOSE_CANDIDATE:
        return {"action": "CLOSE-CANDIDATE", "cure": CLOSE_CANDIDATE[number], "owner": "dock"}
    if mergeable_state == "dirty":
        return {"action": "CURE",
                "cure": "Author updates/rebases the branch onto current main (merge conflicts), then fresh checks re-derive.",
                "owner": "author lane"}
    own_failing = [c for c in failing_at_head if c not in failing_at_base]
    inherited = [c for c in failing_at_head if c in failing_at_base]
    content_reds = [c for c in own_failing if c not in PAPERWORK_CHECKS]
    paperwork_reds = [c for c in own_failing if c in PAPERWORK_CHECKS]
    if not own_failing and inherited:
        return {"action": "CURE",
                "cure": f"Author updates the branch onto current main — its only red(s) ({', '.join(inherited)}) are inherited from its merge-base, not caused by its diff; fresh checks re-derive at the new head.",
                "owner": "author lane"}
    if content_reds:
        return {"action": "CURE",
                "cure": f"Author cures the PR-caused red check(s): {', '.join(content_reds)}; then re-derive at the new head.",
                "owner": "author lane"}
    if paperwork_reds:
        if tier == "C":
            return {"action": "MERGE-NOW",
                    "cure": "Tier C bar is machine validation only; the paperwork reds are the retired form toll. Dock merges + faithfulness proof.",
                    "owner": "dock"}
        floor = TIER_FLOOR.get(tier, 9.5)
        return {"action": "CURE",
                "cure": f"One different-seat gate-format scorecard >= {floor}/10 at the exact head (self-tested against the consensus matcher), then the paperwork checks pass.",
                "owner": "any seat != author (scorecard drive)"}
    return {"action": "MERGE-NOW",
            "cure": "Satisfies its tier's bar at the current head. Dock merges + faithfulness proof.",
            "owner": "dock"}


# --------------------------------------------------------------------------
# Gauge numbers (latest GAUGE-READ file; superseded by balance_gauge.py
# functions once PR #2863 merges — the source is recorded either way)
# --------------------------------------------------------------------------

def read_gauge(gauge_dir: Path | None) -> dict:
    out = {"source": None, "read_anchor": None,
           "paperwork_block_rate_pct": None, "time_to_merge_median_hours": {},
           "escape_rate_proxy_pct": None, "feed_freshness": None}
    if gauge_dir is None:
        return out
    reads = sorted(gauge_dir.glob("GAUGE-READ-*.md"))
    if not reads:
        return out
    text = reads[-1].read_text(encoding="utf-8")
    out["source"] = f"files/balanced-machine/{reads[-1].name}"
    m = re.search(r"Read anchor: \*\*([^*]+)\*\*", text)
    if m:
        out["read_anchor"] = m.group(1)
    m = re.search(r"Paperwork-block rate\*\* \| \*\*([\d.]+)%", text)
    if m:
        out["paperwork_block_rate_pct"] = float(m.group(1))
    m = re.search(r"Tier A \*\*([\d.]+) h\*\*.*?Tier B \*\*([\d.]+) h\*\*.*?Tier C \*\*([\d.]+) h\*\*", text, re.S)
    if m:
        out["time_to_merge_median_hours"] = {"A": float(m.group(1)), "B": float(m.group(2)), "C": float(m.group(3))}
    m = re.search(r"escape rate \(proxy\)\*\* \| \*\*([\d.]+)%", text)
    if m:
        out["escape_rate_proxy_pct"] = float(m.group(1))
    if re.search(r"wall holds exactly \*?\*?1 entry", text):
        out["feed_freshness"] = "outside band — wall held exactly 1 entry at read; see source read"
    return out


def laws_pointer(laws_file: Path | None) -> dict:
    pointer = {"source": "~/AGENTS.md (distilled standing laws, tail carries the current iteration)",
               "iteration": None, "latest_laws": []}
    if laws_file and laws_file.exists():
        tail = laws_file.read_text(encoding="utf-8", errors="replace")[-20000:]
        iters = re.findall(r"iteration (\d+)", tail)
        if iters:
            pointer["iteration"] = int(iters[-1])
        pointer["latest_laws"] = sorted(set(re.findall(r"\bL6\d\d\b", tail)))[-6:]
    return pointer


# --------------------------------------------------------------------------
# Build (pure assembly from fetched data — unit-tested)
# --------------------------------------------------------------------------

def build_state(tip: str, generated_at: str, queue: list[dict],
                tip_failing: list[str], gauge: dict, laws: dict) -> dict:
    by_tier_action: dict[str, dict[str, int]] = {}
    for row in queue:
        by_tier_action.setdefault(row["tier"], {}).setdefault(row["action"], 0)
        by_tier_action[row["tier"]][row["action"]] += 1
    return {
        "schema": "naya.operating-state/1",
        "generated_at": generated_at,
        "tip": tip,
        "open_pr_count": len(queue),
        "queue_by_tier_action": by_tier_action,
        "tip_failing_checks": tip_failing,
        "gauge": gauge,
        "laws": laws,
        "hold_human": sorted(n for n in (r["number"] for r in queue) if n in HOLD_HUMAN),
    }


def build_queue_contract(tip: str, generated_at: str, queue: list[dict]) -> dict:
    return {"schema": "naya.queue-contract/1", "generated_at": generated_at,
            "tip": tip, "prs": queue}


# --------------------------------------------------------------------------
# Mini JSON-Schema validator for the shipped schemas (stdlib only).
# Supports: type (object/array/string/integer/number), required, properties,
# items, enum, additionalProperties=false. Every failure is a cure line.
# --------------------------------------------------------------------------

def validate(instance, schema, path: str = "$", errors: list[str] | None = None) -> list[str]:
    errors = errors if errors is not None else []
    t = schema.get("type")
    if isinstance(t, list):
        for member in t:
            sub_errors: list[str] = []
            validate(instance, {**schema, "type": member}, path, sub_errors)
            if not sub_errors:
                return errors
        errors.append(f"MISSING: {path} matches none of types {t} — CURE: emit a value of one of those types (owner: emitter)")
        return errors
    if t == "null":
        if instance is not None:
            errors.append(f"MISSING: {path} must be null — CURE: emit null at {path} (owner: emitter)")
        return errors
    if t == "object":
        if not isinstance(instance, dict):
            errors.append(f"MISSING: {path} must be an object — CURE: emit an object at {path} (owner: emitter)")
            return errors
        for key in schema.get("required", []):
            if key not in instance:
                errors.append(f"MISSING: {path}.{key} is required — CURE: the emitter must populate {key} (owner: emitter)")
        props = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            for key in instance:
                if key not in props:
                    errors.append(f"MISSING: {path}.{key} is not in the schema — CURE: remove it or extend the schema by PR (owner: emitter)")
        for key, sub in props.items():
            if key in instance:
                validate(instance[key], sub, f"{path}.{key}", errors)
    elif t == "array":
        if not isinstance(instance, list):
            errors.append(f"MISSING: {path} must be an array — CURE: emit an array at {path} (owner: emitter)")
        elif "items" in schema:
            for i, item in enumerate(instance):
                validate(item, schema["items"], f"{path}[{i}]", errors)
    elif t == "string":
        if not isinstance(instance, str):
            errors.append(f"MISSING: {path} must be a string — CURE: emit a string at {path} (owner: emitter)")
    elif t == "integer":
        if not isinstance(instance, int) or isinstance(instance, bool):
            errors.append(f"MISSING: {path} must be an integer — CURE: emit an integer at {path} (owner: emitter)")
    elif t == "number":
        if not isinstance(instance, (int, float)) or isinstance(instance, bool):
            errors.append(f"MISSING: {path} must be a number — CURE: emit a number at {path} (owner: emitter)")
    if "enum" in schema and instance not in schema["enum"]:
        errors.append(f"MISSING: {path} must be one of {schema['enum']} — CURE: use a schema enum value (owner: emitter)")
    return errors


def publish(state: dict, queue_contract: dict, out_dir: Path, tip_now: str,
            state_schema: dict, queue_schema: dict) -> list[Path]:
    """Write both artifacts. Refuses a stale tip and an invalid artifact."""
    if state["tip"] != tip_now:
        raise SystemExit(
            f"MISSING: state tip {state['tip']} does not match the live ref {tip_now} "
            "— CURE: re-run the emitter against the live ref before publishing (owner: hub-refresh owner)")
    for artifact, schema in ((state, state_schema), (queue_contract, queue_schema)):
        errs = validate(artifact, schema)
        if errs:
            raise SystemExit("State failed schema validation:\n" + "\n".join(errs))
    out_dir.mkdir(parents=True, exist_ok=True)
    paths = []
    for name, artifact in (("OPERATING-STATE.json", state), ("QUEUE-CONTRACT.json", queue_contract)):
        p = out_dir / name
        p.write_text(json.dumps(artifact, indent=2) + "\n", encoding="utf-8")
        paths.append(p)
    return paths


# --------------------------------------------------------------------------
# Fetch + emit
# --------------------------------------------------------------------------

def fetch_queue(tip_failing: list[str]) -> list[dict]:
    pulls = paginated("/pulls?state=open")
    queue = []
    base_failing_cache: dict[str, list[str]] = {}
    for pr in sorted(pulls, key=lambda p: p["number"]):
        files = paginated(f"/pulls/{pr['number']}/files")
        paths = [f["filename"] for f in files]
        tier, _reason = classify(pr["title"], paths)
        failing = latest_failing_checks(pr["head"]["sha"])
        compare = gh_api("GET", f"/compare/main...{pr['head']['sha']}")
        base_sha = (compare.get("merge_base_commit") or {}).get("sha")
        if base_sha and base_sha not in base_failing_cache:
            base_failing_cache[base_sha] = latest_failing_checks(base_sha)
        failing_at_base = base_failing_cache.get(base_sha, [])
        derived = derive_action(pr["number"], tier, pr.get("mergeable_state") or "unknown",
                                failing, failing_at_base)
        queue.append({
            "number": pr["number"],
            "title": pr["title"],
            "tier": tier,
            "action": derived["action"],
            "cure": derived["cure"],
            "owner": derived["owner"],
            "head": pr["head"]["sha"],
        })
    return queue


def cmd_emit(args) -> int:
    state_schema = json.loads((TOOLS_DIR / "operating_state.schema.json").read_text())
    queue_schema = json.loads((TOOLS_DIR / "queue_contract.schema.json").read_text())
    # The tip can move mid-fetch on an active night. Rebuild once against
    # the new ref; if it moves again, publish() refuses — a stale state
    # never rides, and the refusal is the receipt.
    for attempt in (1, 2):
        tip = live_tip()
        tip_failing = latest_failing_checks(tip)
        queue = fetch_queue(tip_failing)
        generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        gauge = read_gauge(Path(args.gauge_dir) if args.gauge_dir else None)
        laws = laws_pointer(Path(args.laws_file) if args.laws_file else None)
        state = build_state(tip, generated_at, queue, tip_failing, gauge, laws)
        contract = build_queue_contract(tip, generated_at, queue)
        if live_tip() == tip:
            paths = publish(state, contract, Path(args.out), tip, state_schema, queue_schema)
            for p in paths:
                print(f"wrote {p}")
            print(f"tip={tip} open_prs={len(queue)} tip_failing={tip_failing}")
            return 0
        print(f"tip moved mid-fetch (attempt {attempt}, was {tip}) — rebuilding against the new ref")
    publish(state, contract, Path(args.out), live_tip(), state_schema, queue_schema)
    return 0  # unreachable: publish raises on the stale tip


def cmd_validate(args) -> int:
    ok = True
    for file_arg, schema_file in ((args.state, "operating_state.schema.json"),
                                  (args.queue, "queue_contract.schema.json")):
        schema = json.loads((TOOLS_DIR / schema_file).read_text())
        instance = json.loads(Path(file_arg).read_text())
        errs = validate(instance, schema)
        if errs:
            ok = False
            print(f"{file_arg}: INVALID")
            for e in errs:
                print("  " + e)
        else:
            print(f"{file_arg}: valid against {schema_file}")
    return 0 if ok else 1


def cmd_cold(args) -> int:
    """Cold-activation proof: ONLY the two artifacts (+ the laws pointer
    inside the state) are loaded. Five answers a cold seat needs."""
    state = json.loads(Path(args.state).read_text())
    contract = json.loads(Path(args.queue).read_text())
    mergeable = [r["number"] for r in contract["prs"] if r["action"] == "MERGE-NOW"]
    g = state["gauge"]
    ttm = g.get("time_to_merge_median_hours") or {}
    print("COLD ACTIVATION — answers from OPERATING-STATE.json + QUEUE-CONTRACT.json only")
    print(f"1. Tip: {state['tip']} (state generated {state['generated_at']})")
    print(f"2. Mergeable now (MERGE-NOW): {mergeable if mergeable else 'none'} "
          f"of {state['open_pr_count']} open PRs")
    print(f"3. Held for the human (HOLD-HUMAN): {state['hold_human'] if state['hold_human'] else 'none'}")
    print(f"4. Tip's own failing checks: {state['tip_failing_checks'] if state['tip_failing_checks'] else 'none — tip is green'}")
    print(f"5. Gauge: paperwork-block {g.get('paperwork_block_rate_pct')}% · "
          f"time-to-merge medians A/B/C = {ttm.get('A')}/{ttm.get('B')}/{ttm.get('C')} h · "
          f"escape proxy {g.get('escape_rate_proxy_pct')}% · feed: {g.get('feed_freshness')} "
          f"(source: {g.get('source')}, read anchor {g.get('read_anchor')})")
    print(f"Laws pointer: {state['laws']['source']} — iteration {state['laws'].get('iteration')}, "
          f"latest {state['laws'].get('latest_laws')}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="mode", required=True)
    p_emit = sub.add_parser("emit")
    p_emit.add_argument("--out", required=True)
    p_emit.add_argument("--gauge-dir", default=None,
                        help="dir holding GAUGE-READ-*.md (the Balanced Machine files dir)")
    p_emit.add_argument("--laws-file", default=None, help="path to AGENTS.md for the laws pointer")
    p_emit.set_defaults(fn=cmd_emit)
    p_val = sub.add_parser("validate")
    p_val.add_argument("--state", required=True)
    p_val.add_argument("--queue", required=True)
    p_val.set_defaults(fn=cmd_validate)
    p_cold = sub.add_parser("cold")
    p_cold.add_argument("--state", required=True)
    p_cold.add_argument("--queue", required=True)
    p_cold.set_defaults(fn=cmd_cold)
    args = parser.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
