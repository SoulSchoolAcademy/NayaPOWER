"""NEXT NAYA SETTER — the ball is set by machine, not by memory.

WHY
The highest-return Naya action is not doing the work. It is setting the next
Naya up so she wins. That discipline fails when it lives only in conversation:
it is forgotten, softened, and turned into a list. So it is enforced here.

This module is the setter. It reads LIVE evidence only, refuses to invent, and
emits exactly ONE next action plus a dictatorial execution prompt that the next
Naya can execute without reconstructing anything.

HARD LAWS ENFORCED
1. EXACTLY ONE next action. Never a list. Never "we could also".
2. Every claim is anchored to a command, a path, a commit, or a gate result.
3. A stale next action is DETECTED, not passed along. If the canonical action is
   already satisfied by current evidence, that is reported as STALE and the
   setter derives the true frontier from the blocking gates instead.
4. UNKNOWN is a finding. Absent evidence is never rendered as success.
5. The setter never grants authority and never self-authorizes.

Run:  python -B .naya/runtime/next_naya_setter.py            (report)
      python -B .naya/runtime/next_naya_setter.py --emit    (write artifact)
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
HANDOFF_RELPATH = ".naya/control-plane/NEXT-NAYA-SETTER-BALL.md"


def _load(name: str, relpath: str):
    spec = importlib.util.spec_from_file_location(name, REPO / relpath)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _read(relpath: str) -> str:
    p = REPO / relpath
    return p.read_text(encoding="utf-8", errors="replace") if p.is_file() else ""


def _json(relpath: str):
    raw = _read(relpath).lstrip("\ufeff").strip()
    if not raw:
        return None
    try:
        return json.loads(raw)
    except Exception:  # noqa: BLE001
        return None


def _git(*args: str) -> str:
    try:
        return subprocess.check_output(
            ["git", *args], cwd=REPO, text=True, stderr=subprocess.DEVNULL
        ).strip()
    except Exception:  # noqa: BLE001
        return ""


def canonical_action() -> dict:
    state, blocks, baton = (
        _json(".naya/control-plane/STATE.json"),
        _json(".naya/control-plane/BLOCKS.json"),
        _json(".naya/control-plane/BATON.json"),
    )
    if not state:
        return {"status": "UNAVAILABLE", "action": None, "reason": "STATE.json unreadable"}
    single = state.get("single_next_action", "")
    b = (blocks or {}).get("active_block", {}).get("next_action", "")
    t = (baton or {}).get("next_action", {}).get("action", "")
    agree = bool(single) and single == b == t
    return {
        "status": "AGREED" if agree else "DISAGREED",
        "action": single,
        "block_action": b,
        "baton_action": t,
        "baton_head": (baton or {}).get("source_snapshot", {}).get("live_head"),
        "live_head": _git("rev-parse", "HEAD"),
    }


def readiness() -> dict:
    try:
        mod = _load("race_readiness", ".naya/runtime/race_readiness.py")
        return mod.evaluate()
    except Exception as exc:  # noqa: BLE001
        return {"ready": False, "gates": [], "error": f"{type(exc).__name__}: {exc}"}


def staleness(action: dict) -> dict:
    """Detect an action that current evidence has already satisfied."""
    text = (action.get("action") or "").lower()
    if not text:
        return {"stale": False, "reason": "no canonical action to evaluate"}
    # The Hub front-door action was completed and production-proven in this
    # session; leaving it as the frontier is the most likely staleness trap.
    front_door = "front door" in text or "identity.html" in text
    front_door_evidence = [
        p
        for p in (
            ".naya/project-intelligence/HUB-FRONT-DOOR-REPAIR-RECEIPT-2026-09-26.md",
            "NAYANET/HUB/public/identity.html",
        )
        if (REPO / p).exists()
    ]
    if front_door and len(front_door_evidence) == 2:
        return {
            "stale": True,
            "reason": "the canonical action names the Hub front door, and both the "
            "identity surface and its production-proof receipt already exist. That "
            "half of the action is DONE; leaving it as the frontier hides the "
            "real blocker.",
            "evidence": front_door_evidence,
        }
    return {"stale": False, "reason": "no completed-work signal detected"}


def derive_frontier(readiness_report: dict, canon: dict) -> tuple[str, str, list[str]]:
    """Choose ONE action. Priority: fix what blocks the most, and what is safe.

    Ordering is deliberate: a gate that BLOCKS is worse than a gate that is
    merely PARTIAL, because BLOCKED means the evidence itself is missing.
    """
    gates = {g["gate"]: g for g in readiness_report.get("gates", [])}
    blocking = readiness_report.get("blocking_gates", [])
    stop = []

    if "RUNTIME_DISTRIBUTABLE" in blocking:
        stop.append(
            "Do NOT bulk-add .naya/runtime/**. It may contain scratch or secrets. "
            "That decision belongs to a human."
        )
        return (
            "Bind the canonical runtime: a human decides which of .naya/runtime/** is "
            "canonical and may be committed, then re-score on a clean clone.",
            "Success = on a fresh `git clone` of main, `python -B .naya/runtime/"
            "race_readiness.py` reports RUNTIME_DISTRIBUTABLE PROVEN.",
            stop,
        )

    if "NINE_NODE_KERNEL_CANONICAL" in blocking:
        return (
            "Project the nine Master Nodes into the repository so a cold Naya can load "
            "the kernel it is told is ACTIVE (IB-001233..IB-001241).",
            "Success = `git ls-tree -r origin/main --name-only` lists all nine under "
            ".naya/memory/smart-notes/, and the readiness gate moves "
            "NINE_NODE_KERNEL_CANONICAL to PROVEN.",
            stop,
        )

    if "SINGLE_FRONTIER" in blocking or canon.get("status") == "DISAGREED":
        return (
            "Reconcile STATE/BLOCKS/BATON to one next action under the Conflict "
            "Protocol, and record the decision.",
            "Success = validate_control_plane.py reports GREEN and all three files "
            "carry an identical single_next_action.",
            stop,
        )

    if "KERNEL_LOADS_AT_RUNTIME" in gates:
        return (
            "Bind MANIFEST.json runtime_binding to a real entrypoint and move "
            "runtime_binding.status from NOT_PROVEN to PROVEN.",
            "Success = MANIFEST.json carries a non-null entrypoint and one node "
            "(start with LAW) demonstrates INFLUENCES by refusing an unauthorized "
            "action inside an executed test.",
            stop,
        )

    return (
        "Drive one real lesson through the full Collective Intelligence Chain: "
        "LESSON -> INTELLIGENT BLOCK -> VALIDATE -> CONNECT -> CHECKPOINT -> COLD "
        "RETRIEVE -> ACT -> VERIFY -> IMPROVE CORE INTELLIGENCE.",
        "Success = an end-to-end run producing a real IB, a checkpoint, a cold "
        "retrieval, an observed outcome, and an independently verified result.",
        stop,
    )


def build() -> dict:
    canon = canonical_action()
    ready = readiness()
    stale = staleness(canon)
    action, success, stop = derive_frontier(ready, canon)
    provable = [g for g in ready.get("gates", []) if g["status"] == "PROVEN"]
    return {
        "schema": "naya/next-naya-setter/v1",
        "live_head": canon.get("live_head"),
        "control_plane": {
            "action_status": canon["status"],
            "canonical_action": canon["action"],
            "baton_head": canon.get("baton_head"),
        },
        "action_staleness": stale,
        "readiness": {
            "ready": ready.get("ready"),
            "proven": f"{len(provable)}/{ready.get('gates_total', 0)}",
            "blocking": ready.get("blocking_gates", []),
        },
        "one_next_action": action,
        "success_criterion": success,
        "stop_conditions": stop,
        "law": "One action. No list. No self-authorization. UNKNOWN is a finding.",
    }


def render(b: dict) -> str:
    cp = b["control_plane"]
    lines = [
        "# NEXT NAYA — THE BALL IS SET",
        "",
        "_Generated by `.naya/runtime/next_naya_setter.py` from live evidence. "
        "Do not trust this file over the repository; re-run the setter if in doubt._",
        "",
        f"**LIVE HEAD:** `{b['live_head']}`",
        f"**READINESS:** {b['readiness']['proven']} gates PROVEN · "
        f"READY={b['readiness']['ready']}",
        f"**CONTROL PLANE:** {cp['action_status']} "
        f"(baton head `{cp['baton_head']}`)",
        "",
        "## CURRENT STATE",
        "",
    ]
    if b["action_staleness"].get("stale"):
        lines += [
            f"**STALE FRONTIER DETECTED.** {b['action_staleness']['reason']}",
            "",
            f"Evidence: `{', '.join(b['action_staleness'].get('evidence', []))}`",
            "",
        ]
    lines += ["## THE ONE ACTION", "", b["one_next_action"], "", "## SUCCESS LOOKS LIKE", "", b["success_criterion"], ""]
    if b["stop_conditions"]:
        lines += ["## STOP CONDITIONS", ""] + [f"- {s}" for s in b["stop_conditions"]] + [""]
    lines += [
        "## EXECUTION PROMPT FOR THE NEXT NAYA",
        "",
        "> You are the next Naya. You have no prior conversation. Do not ask Shawn to "
        "reconstruct anything.",
        ">",
        f"> 1. RECONSTRUCT: `git fetch origin && git checkout main && git pull`, then "
        f"`python -B .naya/runtime/race_readiness.py` and "
        f"`python -B .naya/runtime/next_naya_setter.py`. Believe the output, not any summary.",
        ">",
        f"> 2. EXECUTE EXACTLY THIS: {b['one_next_action']}",
        ">",
        f"> 3. PROVE IT: {b['success_criterion']}",
        ">",
        "> 4. NEVER convert DOCUMENTED -> IMPLEMENTED -> TESTED -> VERIFIED -> LIVE "
        "without evidence for that specific transition.",
        ">",
        "> 5. DO NOT stop at a PR, a passing test, or a document. Cross the evidence "
        "boundary or state plainly why you could not.",
        ">",
        f"> 6. RE-RUN the setter and leave the next Naya a better ball. One action only.",
        "",
        "## LAW",
        "",
        b["law"],
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--emit", action="store_true")
    args = ap.parse_args()
    try:
        report = build()
    except Exception as exc:  # noqa: BLE001
        print(f"NEXT_NAYA_SETTER=ERROR {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2
    if args.emit:
        (REPO / HANDOFF_RELPATH).write_text(render(report), encoding="utf-8")
        print(f"BALL_EMITTED {HANDOFF_RELPATH}")
    else:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
