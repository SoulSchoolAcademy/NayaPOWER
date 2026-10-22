#!/usr/bin/env python3
"""Mechanical activation checklist runner (GT-015 family).

Executes BRAIN/00-ACTIVATION/activation-checklist.json (schema
naya.activation.checklist.v1) as checks-with-receipts against published
state + canon, and emits a receipt (schema naya.activation-receipt/1).

The receipt's FIRST line is always the boot gate's LIVE verdict, read by
running kernel/protocol/protocol_integrity_gate.py as a subprocess at run
time — reported, never hidden. While the PROTOCOL.md pin stands drifted
(GT-001; re-pin ratified 2026-10-22, executed by the protocol owner) that
line is RED and the runner exits nonzero. This tool never touches the pin.

Check classes:
  PASS   — machine-verified against live/published/canonical bytes
  ATTEST — an attestation supplied on the command line, recorded verbatim
           (the checklist's own verify text demands a human/agent statement)
  FAIL   — a required check did not pass; every FAIL carries a cure line
  NA     — an applies_when check whose condition is not in force

Attestations: --outcome, --laws (">=2 specific laws"), --proof,
--memory-note, --brief, --lane-note, --tools-note, --design-note,
--project-id / --no-project-intelligence. A missing attestation is a FAIL
with a cure naming the flag — activation never passes on silence.

Published-state probes (beyond the checklist's 12): the venue pointer in
STATE-CORE on live/mission-state resolves to the live board (2793), and
OPERATING-STATE + QUEUE-CONTRACT are present, tip-matched, and fresh
(<= 90 min — the hourly publisher's cadence plus slack).

Usage:
  python3 tools/activation_checklist_runner.py --agent-id <seat> \
      [--repo-root .] [--agents-md ~/AGENTS.md] [--design] \
      --outcome "..." --laws "LAW A, LAW B" --proof "..." \
      --memory-note "..." --brief "..." --lane-note "..." \
      --tools-note "..." [--receipt-out receipt.json]

Exit 0 only when the boot gate is green and no required check FAILs.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

REPO = "SoulSchoolAcademy/NayaPOWER"
GH_API = Path.home() / "workspace" / "naya" / "bin" / "gh-api"
STATE_BRANCH = "live/mission-state"
LIVE_VENUE = 2793
STATE_MAX_AGE_S = 90 * 60


# --------------------------------------------------------------------------
# live providers (injectable for tests)
# --------------------------------------------------------------------------

def gh_api(method, path):
    r = subprocess.run([str(GH_API), method, f"/repos/{REPO}{path}"],
                       capture_output=True, text=True, timeout=120)
    if r.returncode != 0:
        raise RuntimeError(f"gh-api {method} {path}: {r.stderr.strip()[:200]}")
    return json.loads(r.stdout) if r.stdout.strip() else {}


def fetch_tip():
    return gh_api("GET", "/git/refs/heads/main")["object"]["sha"]


def fetch_state_file(name):
    try:
        d = gh_api("GET", f"/contents/{name}?ref={STATE_BRANCH}")
    except RuntimeError:
        return None
    if d.get("encoding") == "base64":
        return json.loads(base64.b64decode(d["content"]))
    return None


def fetch_open_prs():
    prs = gh_api("GET", "/pulls?state=open&per_page=100")
    return [{"number": p["number"], "title": p["title"]} for p in prs]


def run_gate(repo_root: Path, agent_id: str) -> dict:
    r = subprocess.run(
        [sys.executable, "kernel/protocol/protocol_integrity_gate.py",
         "--agent-id", agent_id, "--json"],
        cwd=repo_root, capture_output=True, text=True, timeout=300)
    out = r.stdout.strip()
    if not out:
        return {"pass": False, "checks": [], "failures": [{
            "name": "gate_unreadable", "pass": False,
            "detail": f"gate produced no JSON (exit {r.returncode}): {r.stderr.strip()[:200]}"}]}
    return json.loads(out)


def fetch_ancestry(state_tip, live_tip):
    """True when state_tip is the live tip or an ancestor of it (the state
    was published from main's own history, possibly before later landings)."""
    if state_tip == live_tip:
        return True
    try:
        d = gh_api("GET", f"/compare/{state_tip}...{live_tip}")
    except RuntimeError:
        return False
    return d.get("status") in ("identical", "ahead")  # live tip at or ahead of state tip


def run_delta_check(repo_root: Path):
    r = subprocess.run([sys.executable, "tools/generate_laws_delta.py", "--check"],
                       cwd=repo_root, capture_output=True, text=True, timeout=120)
    return r.returncode == 0, (r.stdout + r.stderr).strip().split("\n")[0][:200]


# --------------------------------------------------------------------------
# the runner
# --------------------------------------------------------------------------

def load_json(path: Path):
    try:
        return json.loads(path.read_text())
    except Exception:
        return None


def parse_ts(s):
    try:
        return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc).timestamp()
    except Exception:
        return None


class Runner:
    def __init__(self, repo_root: Path, args, providers=None, now=None):
        self.root = repo_root
        self.args = args
        p = providers or {}
        self.p_tip = p.get("tip", fetch_tip)
        self.p_state = p.get("state", fetch_state_file)
        self.p_prs = p.get("prs", fetch_open_prs)
        self.p_gate = p.get("gate", run_gate)
        self.p_delta = p.get("delta", run_delta_check)
        self.p_ancestry = p.get("ancestry", fetch_ancestry)
        self.now = now if now is not None else time.time()
        self.checks: list[dict] = []
        self.tip = None

    def add(self, step, check, status, evidence, cure=None):
        row = {"step": step, "check": check, "status": status, "evidence": evidence}
        if cure:
            row["cure"] = cure
        self.checks.append(row)
        return row

    # -- checklist step implementations ------------------------------------

    def s_tune_in_laws(self):
        a = self.args
        agents = Path(a.agents_md).expanduser()
        registry = load_json(self.root / "BRAIN/01-GOVERNANCE/DAILY-LAW-REGISTRY.machine.json")
        if not agents.exists():
            self.add("tune-in-laws", "AGENTS.md read at current main tip", "FAIL",
                     f"AGENTS.md not found at {agents}",
                     "run from a seat with the law corpus present (owner: activating seat)")
        else:
            sha = hashlib.sha256(agents.read_bytes()).hexdigest()
            if registry is None:
                self.add("tune-in-laws", "AGENTS.md read at current main tip", "FAIL",
                         f"AGENTS.md sha256 {sha[:16]}… recorded, but DAILY-LAW-REGISTRY is "
                         "absent at this tip — the law read cannot be proven to be the law compiled",
                         "land the daily-law registry (GT-010) so the fingerprint can be checked")
            else:
                want = (registry.get("generated_from") or {}).get("agents_md_sha256")
                if want == sha:
                    self.add("tune-in-laws", "AGENTS.md read at current main tip", "PASS",
                             f"AGENTS.md sha256 {sha[:16]}… == registry source fingerprint")
                else:
                    self.add("tune-in-laws", "AGENTS.md read at current main tip", "FAIL",
                             f"AGENTS.md sha256 {sha[:16]}… != registry fingerprint "
                             f"{str(want)[:16]}… — the prose moved or the registry is stale",
                             "regenerate the registry (tools/generate_daily_law_registry.py) or "
                             "re-read the current AGENTS.md (owner: LAW lane)")
        if a.memory_note:
            self.add("tune-in-laws", "MEMORY.md key sections read", "ATTEST", a.memory_note)
        else:
            self.add("tune-in-laws", "MEMORY.md key sections read", "FAIL",
                     "no attestation supplied",
                     "pass --memory-note naming one preference and one commitment for this task")
        if a.brief:
            self.add("tune-in-laws", "task brief read in full", "ATTEST", a.brief)
        else:
            self.add("tune-in-laws", "task brief read in full", "FAIL",
                     "no attestation supplied",
                     "pass --brief with the task restated in one sentence")

    def s_tune_in_state(self):
        a = self.args
        try:
            self.tip = self.p_tip()
            self.add("tune-in-state", "current main tip SHA recorded", "PASS",
                     f"{self.tip} (live ref, fetched this run)")
        except Exception as e:  # noqa: BLE001
            self.add("tune-in-state", "current main tip SHA recorded", "FAIL",
                     f"live tip fetch failed: {e}", "restore API access and re-run")
        try:
            prs = self.p_prs()
            pr_ev = f"open PRs at run time: {[p['number'] for p in prs]}"
        except Exception as e:  # noqa: BLE001
            pr_ev = f"open-PR scan unavailable: {e}"
        if a.lane_note:
            self.add("tune-in-state", "no conflicting active lane on this work", "ATTEST",
                     f"{a.lane_note} | {pr_ev}")
        else:
            self.add("tune-in-state", "no conflicting active lane on this work", "FAIL",
                     f"no attestation supplied | {pr_ev}",
                     "pass --lane-note with the board claim scan result")
        manifest_path = self.root / ".naya/project-intelligence/MANIFEST.json"
        manifest = load_json(manifest_path)
        if manifest is not None:
            ids = [p.get("project_id") for p in manifest.get("projects", [])]
            ev = f"manifest read at tip; projects: {ids}"
            if a.project_id:
                ev += f"; this task's project: {a.project_id}"
            self.add("tune-in-state", "project intelligence manifest read", "PASS", ev)
        elif a.no_project_intelligence:
            self.add("tune-in-state", "project intelligence manifest read", "ATTEST",
                     "no project intelligence applies (attested); MANIFEST.json absent at this tip")
        else:
            self.add("tune-in-state", "project intelligence manifest read", "FAIL",
                     "MANIFEST.json absent at this tip and no attestation supplied",
                     "create .naya/project-intelligence/MANIFEST.json (project-intelligence lane) "
                     "or pass --no-project-intelligence")

    def s_name_the_job(self):
        if self.args.outcome:
            self.add("name-the-job", "outcome sentence written", "ATTEST", self.args.outcome)
        else:
            self.add("name-the-job", "outcome sentence written", "FAIL",
                     "no outcome sentence supplied",
                     "pass --outcome with the human-experienced result in one sentence")

    def s_name_the_gates(self):
        a = self.args
        laws = [x.strip() for x in (a.laws or "").split(",") if x.strip()]
        if len(laws) >= 2:
            self.add("name-the-gates", "governing laws named", "ATTEST",
                     f"{len(laws)} laws named: {'; '.join(laws)}")
        elif laws:
            self.add("name-the-gates", "governing laws named", "FAIL",
                     f"only {len(laws)} law named; the checklist requires at least 2 specific laws",
                     "pass --laws with at least 2 specific laws/rules by name or number")
        else:
            self.add("name-the-gates", "governing laws named", "FAIL",
                     "no governing laws supplied",
                     "pass --laws with at least 2 specific laws/rules by name or number")
        if not a.design:
            self.add("name-the-gates", "design work: design laws loaded", "NA",
                     "applies_when 'task involves visual output' not in force (no --design)")
        else:
            doc = self.root / "BRAIN/00-ACTIVATION/DESIGN-ACTIVATION.md"
            if not doc.exists():
                self.add("name-the-gates", "design work: design laws loaded", "FAIL",
                         "DESIGN-ACTIVATION.md absent at this tip",
                         "restore BRAIN/00-ACTIVATION/DESIGN-ACTIVATION.md (owner: design lane)")
            elif a.design_note:
                self.add("name-the-gates", "design work: design laws loaded", "ATTEST",
                         f"DESIGN-ACTIVATION.md present; {a.design_note}")
            else:
                self.add("name-the-gates", "design work: design laws loaded", "FAIL",
                         "design laws present but completion not attested",
                         "complete DESIGN-ACTIVATION.md steps and pass --design-note")

    def s_name_the_proof(self):
        if self.args.proof:
            self.add("name-the-proof", "verification method named", "ATTEST", self.args.proof)
        else:
            self.add("name-the-proof", "verification method named", "FAIL",
                     "no verification method supplied",
                     "pass --proof describing verification through the director's eyes")

    def s_pick_up_tools(self):
        a = self.args
        if not a.design:
            self.add("pick-up-tools", "block catalog consulted for design work", "NA",
                     "applies_when 'task involves visual output' not in force (no --design)")
        else:
            blocks = load_json(self.root / "BRAIN/10-INTERFACES/DESIGN-BLOCKS/blocks/index.json")
            if blocks is None:
                self.add("pick-up-tools", "block catalog consulted for design work", "FAIL",
                         "blocks/index.json absent or unreadable at this tip",
                         "restore the block catalog (owner: design lane)")
            else:
                n = len(blocks) if isinstance(blocks, list) else len(blocks.get("blocks", []))
                self.add("pick-up-tools", "block catalog consulted for design work", "PASS",
                         f"blocks/index.json read; {n} blocks catalogued")
        mech = load_json(self.root / "tools/mechanism-registry.json")
        if mech is None:
            self.add("pick-up-tools", "no reinventing", "FAIL",
                     "tools/mechanism-registry.json absent or unreadable — the canonical "
                     "mechanism census cannot be consulted",
                     "restore the mechanism registry (owner: kernel lane)")
        elif a.tools_note:
            n = len(mech) if isinstance(mech, list) else len(mech.get("mechanisms", []))
            self.add("pick-up-tools", "no reinventing", "ATTEST",
                     f"mechanism registry loads ({n} entries); {a.tools_note}")
        else:
            self.add("pick-up-tools", "no reinventing", "FAIL",
                     "mechanism registry loads but no tooling attestation supplied",
                     "pass --tools-note naming the existing mechanism/spec used, or the "
                     "written justification for a custom build")

    # -- published-state probes ---------------------------------------------

    def s_published_state(self):
        core = self.p_state("STATE-CORE.json")
        if core is None:
            self.add("published-state", "venue pointer resolves (STATE-CORE)", "FAIL",
                     f"STATE-CORE.json unreadable on {STATE_BRANCH}",
                     "restore the STATE-CORE publisher (owner: state lane)")
        else:
            venue = ((core.get("venue") or {}).get("live"))
            if venue == LIVE_VENUE:
                self.add("published-state", "venue pointer resolves (STATE-CORE)", "PASS",
                         f"venue.live == {LIVE_VENUE} (live board)")
            else:
                self.add("published-state", "venue pointer resolves (STATE-CORE)", "FAIL",
                         f"venue.live == {venue}, expected {LIVE_VENUE}",
                         "fix the venue pointer at source (STATE-CORE builder) — GT-068 decided 2793")
        state = self.p_state("OPERATING-STATE.json")
        if state is None:
            self.add("published-state", "operating state published + fresh", "FAIL",
                     f"OPERATING-STATE.json absent on {STATE_BRANCH}",
                     "the hourly publisher emits it (GT-006) — check hub-state-builder --publish")
        else:
            gen = parse_ts(state.get("generated_at", ""))
            age = None if gen is None else int(self.now - gen)
            # The publisher runs hourly; landings after a publish move main
            # without making the state wrong. What fails: a state whose tip
            # is NOT in main's history (published from a stray line), or age.
            tip_ok = (self.tip is not None and state.get("tip")
                      and self.p_ancestry(state["tip"], self.tip))
            if tip_ok and age is not None and age <= STATE_MAX_AGE_S:
                rel = "tip == live tip" if state.get("tip") == self.tip else \
                    "state tip is an ancestor of the live tip (in-history; hourly cadence)"
                self.add("published-state", "operating state published + fresh", "PASS",
                         f"generated_at {state.get('generated_at')} (age {age}s); {rel}")
            else:
                why = []
                if not tip_ok:
                    why.append(f"state tip {str(state.get('tip'))[:12]}… is not the live tip "
                               "or an ancestor of it")
                if age is None:
                    why.append("generated_at unparseable")
                elif age > STATE_MAX_AGE_S:
                    why.append(f"age {age}s > {STATE_MAX_AGE_S}s")
                self.add("published-state", "operating state published + fresh", "FAIL",
                         "; ".join(why),
                         "wait for / repair the hourly publish (GT-006 wiring, owner: hub lane)")
        contract = self.p_state("QUEUE-CONTRACT.json")
        if contract is None:
            self.add("published-state", "queue contract present", "FAIL",
                     f"QUEUE-CONTRACT.json absent on {STATE_BRANCH}",
                     "the hourly publisher emits it beside OPERATING-STATE (GT-006)")
        else:
            gen = parse_ts(contract.get("generated_at", ""))
            age = None if gen is None else int(self.now - gen)
            prs = contract.get("prs") or contract.get("queue") or []
            if age is not None and age <= STATE_MAX_AGE_S:
                self.add("published-state", "queue contract present", "PASS",
                         f"present; generated_at {contract.get('generated_at')} "
                         f"(age {age}s); {len(prs)} PR rows")
            else:
                self.add("published-state", "queue contract present", "FAIL",
                         f"present but stale/unparseable (age {age})",
                         "wait for / repair the hourly publish (GT-006 wiring, owner: hub lane)")
        ok, detail = self.p_delta(self.root)
        if ok:
            self.add("published-state", "law loads as data (LAWS-DELTA --check)", "PASS", detail)
        else:
            self.add("published-state", "law loads as data (LAWS-DELTA --check)", "FAIL",
                     detail, "regenerate the delta (tools/generate_laws_delta.py) (owner: LAW lane)")

    # -- driver ---------------------------------------------------------------

    def run(self) -> dict:
        checklist = load_json(self.root / "BRAIN/00-ACTIVATION/activation-checklist.json")
        gate = self.p_gate(self.root, self.args.agent_id)
        gate_failures = [f for f in gate.get("failures", []) if not f.get("pass", False)]
        if gate.get("pass") and not gate_failures:
            n = len(gate.get("checks", []))
            first = f"BOOT GATE: GREEN — {n}/{n} checks pass"
        else:
            names = ", ".join(f.get("name", "?") for f in gate_failures) or "unknown"
            detail = gate_failures[0].get("detail", "") if gate_failures else ""
            first = (f"BOOT GATE: RED — {names}: {detail} — reported, not hidden; "
                     "activation proceeds no further than this receipt until cured")
        self.s_tune_in_laws()
        self.s_tune_in_state()
        self.s_name_the_job()
        self.s_name_the_gates()
        self.s_name_the_proof()
        self.s_pick_up_tools()
        self.s_published_state()
        counts = {}
        for c in self.checks:
            counts[c["status"]] = counts.get(c["status"], 0) + 1
        verdict = "PASS" if (not gate_failures and gate.get("pass")
                             and counts.get("FAIL", 0) == 0) else "FAIL"
        return {
            "schema": "naya.activation-receipt/1",
            "agent_id": self.args.agent_id,
            "generated_at": datetime.fromtimestamp(self.now, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "checklist_schema": (checklist or {}).get("schema"),
            "boot_gate": {"pass": bool(gate.get("pass")) and not gate_failures,
                          "failures": [f.get("name") for f in gate_failures],
                          "first_line": first},
            "checks": self.checks,
            "counts": counts,
            "verdict": verdict,
        }


def render_text(receipt: dict) -> str:
    lines = [receipt["boot_gate"]["first_line"]]
    for c in receipt["checks"]:
        lines.append(f"[{c['status']}] {c['step']}/{c['check']} — {c['evidence']}")
        if c.get("cure"):
            lines.append(f"    CURE: {c['cure']}")
    k = receipt["counts"]
    lines.append(f"ACTIVATION: {receipt['verdict']} "
                 f"({k.get('PASS', 0)} PASS · {k.get('ATTEST', 0)} ATTEST · "
                 f"{k.get('FAIL', 0)} FAIL · {k.get('NA', 0)} NA)")
    return "\n".join(lines)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Mechanical activation checklist runner (GT-015)")
    ap.add_argument("--agent-id", default="activation-runner")
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--agents-md", default="~/AGENTS.md")
    ap.add_argument("--design", action="store_true")
    ap.add_argument("--outcome")
    ap.add_argument("--laws")
    ap.add_argument("--proof")
    ap.add_argument("--memory-note")
    ap.add_argument("--brief")
    ap.add_argument("--lane-note")
    ap.add_argument("--tools-note")
    ap.add_argument("--design-note")
    ap.add_argument("--project-id")
    ap.add_argument("--no-project-intelligence", action="store_true")
    ap.add_argument("--receipt-out")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    receipt = Runner(Path(args.repo_root), args).run()
    if args.receipt_out:
        Path(args.receipt_out).write_text(json.dumps(receipt, indent=1) + "\n")
    print(json.dumps(receipt, indent=1) if args.json else render_text(receipt))
    return 0 if receipt["verdict"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
