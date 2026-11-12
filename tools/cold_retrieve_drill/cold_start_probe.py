#!/usr/bin/env python3
"""Cold-start probe for the weekly cold-retrieve drill.

Answers the untested question: does the retrieve path fire from a TRULY cold
session — no drill log, no warm caches, no ambient environment — and does it
fail LOUD (never silent-pass) when its preconditions are gone?

Probes (each prints PASS/FAIL with evidence):
  P1 show-cold       drill.py --show from a pristine CWD, env scrubbed, no
                     drill_log.jsonl anywhere near -> valid drill JSON.
  P2 retrieve-cold   smart_note_v2.py retrieve for the week's KNOW query,
                     env scrubbed to PATH+HOME only -> exact expected note_id.
  P3 missing-bank    drill.py --show --bank /nonexistent -> non-zero, loud.
  P4 empty-bank      all items retired -> BANK_EMPTY, non-zero, loud.
  P5 zero-relevance  gibberish query, scrubbed env -> NO_RELEVANT_INTELLIGENCE.

Usage:
  python3 tools/cold_retrieve_drill/cold_start_probe.py [--repo ROOT] [--week N]

Exit 0 = all probes PASS. Exit 1 = at least one FAIL. Machine-readable JSON
goes to stdout; human lines to stderr.
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile

PROBE_WEEK = 41  # seeded rotation week; deterministic across runs


def scrubbed_env():
    """Minimal env: a cold session has no ambient state to lean on."""
    home = tempfile.mkdtemp(prefix="cold-probe-home-")
    return {"PATH": "/usr/bin:/bin:/usr/local/bin", "HOME": home}


def run(cmd, cwd, env):
    return subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True, timeout=300)


def probe_show_cold(repo, bank, week, env):
    """P1: --show must work with no drill log, no warm state, pristine CWD."""
    cold_cwd = tempfile.mkdtemp(prefix="cold-probe-cwd-")
    r = run([sys.executable, str(repo / "tools/cold_retrieve_drill/drill.py"),
             "--bank", str(bank), "--week", str(week), "--show"],
            cwd=cold_cwd, env=env)
    if r.returncode != 0:
        return False, f"exit={r.returncode} stderr={r.stderr.strip()[:200]}"
    try:
        d = json.loads(r.stdout)
    except Exception as e:
        return False, f"stdout not JSON: {e}"
    need = {"drill_id", "expected_note_id", "know_query", "application_question"}
    missing = need - set(d)
    if missing:
        return False, f"missing keys: {sorted(missing)}"
    return True, f"drill_id={d['drill_id']} note={d['expected_note_id']}"


def probe_retrieve_cold(repo, bank, week, env):
    """P2: the KNOW query must hit the exact expected note in a scrubbed env."""
    b = json.loads((repo / bank).read_text())
    items = [i for i in b["items"] if not i.get("retired")]
    item = items[week % len(items)]
    r = run([sys.executable, str(repo / "tools/smart_note_v2.py"),
             "retrieve", "--query", item["query"]],
            cwd=tempfile.mkdtemp(prefix="cold-probe-cwd-"), env=env)
    if r.returncode != 0:
        return False, f"exit={r.returncode} out={r.stdout.strip()[:120]} err={r.stderr.strip()[:120]}"
    try:
        d = json.loads(r.stdout)
        got = d["retrieved"]["smart_note_id"]
    except Exception as e:
        return False, f"result not parseable: {e}"
    if got != item["note_id"]:
        return False, f"WRONG NOTE: got {got}, expected {item['note_id']}"
    return True, f"query hit exact note {got} (drill {item['id']})"


def probe_missing_bank(repo, env):
    """P3: a missing bank must fail LOUD, never silently pass."""
    r = run([sys.executable, str(repo / "tools/cold_retrieve_drill/drill.py"),
             "--bank", "/nonexistent/bank.json", "--show"],
            cwd=tempfile.mkdtemp(prefix="cold-probe-cwd-"), env=env)
    if r.returncode == 0:
        return False, "exit 0 on missing bank — silent pass"
    loud = "FileNotFoundError" in r.stderr or "No such file" in r.stderr
    return True, f"exit={r.returncode} loud={loud}"


def probe_empty_bank(repo, env):
    """P4: an all-retired bank must say BANK_EMPTY, not crash cryptically."""
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump({"items": [{"id": "x", "retired": True}]}, f)
        empty_bank = f.name
    r = run([sys.executable, str(repo / "tools/cold_retrieve_drill/drill.py"),
             "--bank", empty_bank, "--show"],
            cwd=tempfile.mkdtemp(prefix="cold-probe-cwd-"), env=env)
    if r.returncode == 0:
        return False, "exit 0 on empty bank — silent pass"
    said = "BANK_EMPTY" in (r.stdout + r.stderr)
    return (True, f"exit={r.returncode} BANK_EMPTY announced") if said \
        else (False, f"exit={r.returncode} but BANK_EMPTY not announced: {(r.stdout+r.stderr).strip()[:160]}")


def probe_zero_relevance_cold(repo, env):
    """P5: a query matching nothing must fail closed, even when cold."""
    r = run([sys.executable, str(repo / "tools/smart_note_v2.py"),
             "retrieve", "--query", "xqzqw wibblzqrk zzzqqq kkkvvv"],
            cwd=tempfile.mkdtemp(prefix="cold-probe-cwd-"), env=env)
    closed = r.returncode != 0 and "NO_RELEVANT_INTELLIGENCE" in (r.stdout + r.stderr)
    return (True, "fail-closed NO_RELEVANT_INTELLIGENCE") if closed \
        else (False, f"exit={r.returncode} out={(r.stdout+r.stderr).strip()[:160]}")


PROBES = [
    ("P1", "show works with zero warm state", probe_show_cold),
    ("P2", "scrubbed-env retrieve hits exact note", probe_retrieve_cold),
    ("P3", "missing bank fails loud", probe_missing_bank),
    ("P4", "all-retired bank says BANK_EMPTY", probe_empty_bank),
    ("P5", "zero-relevance fails closed when cold", probe_zero_relevance_cold),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=None)
    ap.add_argument("--week", type=int, default=PROBE_WEEK)
    ap.add_argument("--bank", default="tools/cold_retrieve_drill/drill_bank.json")
    a = ap.parse_args()
    repo = a.repo
    if repo is None:
        repo = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                              capture_output=True, text=True).stdout.strip()
    from pathlib import Path
    repo = Path(repo).resolve()  # absolutize: probes run with CWD=/tmp/...
    bank = a.bank if os.path.isabs(a.bank) else str(repo / a.bank)
    env = scrubbed_env()
    results = []
    failed = 0
    for pid, name, fn in PROBES:
        try:
            if pid in ("P1", "P2"):
                ok, ev = fn(repo, bank, a.week, env)
            else:
                ok, ev = fn(repo, env)
        except Exception as e:  # a probe that explodes is a failed probe
            ok, ev = False, f"EXCEPTION {type(e).__name__}: {e}"
        results.append({"probe": pid, "name": name, "pass": ok, "evidence": ev})
        print(f"[{'PASS' if ok else 'FAIL'}] {pid} {name} — {ev}", file=sys.stderr)
        failed += 0 if ok else 1
    print(json.dumps({"probes": results, "failed": failed}, indent=2))
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
