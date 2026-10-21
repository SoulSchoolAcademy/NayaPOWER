#!/usr/bin/env python3
"""Standalone Hub deploy pipeline — Balanced Machine step 4 (DESIGN.ai.md §5.1).

WHY THIS EXISTS
---------------
Until now the Hub (nayanet.live) was only ever re-shipped as a side effect of
Smart Note landings: the sync lane's combined path baked notes into the page
and uploaded it, so a canonical Hub-source fix merged to main stayed invisible
until a note happened to land. On 2026-10-21 the sync watcher also died
silently on a VM replacement and the live wall sat at 1 card for hours.

This tool makes deploy its own act, invocable at any time, independently of
note landings:

    syntax gate  ->  deploy  ->  smoke check  ->  receipt
    smoke failure => automatic rollback to the previously deployed commit
                     + a defect receipt naming the failure.

DEPLOY TRANSPORT
--------------
There is no in-repo deploy transport for the Hub app (no wrangler config, no
deploy workflow — the upload was lane machinery outside the repo). The deploy
step is therefore an adapter:

* ``--target DIR``   : CopyAdapter — publishes the Hub source set into DIR
                       (a static-host directory / staging dir / dry-run).
* ``HUB_DEPLOY_CMD`` : CommandAdapter — a shell command run with
                       $HUB_DEPLOY_SOURCE (dir holding the source set) and
                       $HUB_DEPLOY_COMMIT set. This is where the real upload
                       command plugs in when the lane wires it.
* neither            : the pipeline FAILS CLOSED with status NOT_CONFIGURED.
                       It never pretends to have deployed.

STATE
-----
Every successful deploy records ``HUB/.hub-deploy-state.json``:
``{deployed_commit, previous_commit, deployed_at, adapter}``. Rollback
re-publishes the Hub source of ``previous_commit`` (extracted from git) through
the same adapter and swaps the state back.

USAGE
-----
    python3 tools/hub_deploy.py deploy --ref <commit> [--target DIR]
    python3 tools/hub_deploy.py deploy --ref <commit> --dry-run --target DIR
    python3 tools/hub_deploy.py rollback [--target DIR]
    python3 tools/hub_deploy.py gate [--files f1 f2 ...]

Exit codes: 0 ok · 2 syntax gate failed · 3 smoke failed (rollback done) ·
4 smoke failed AND rollback failed · 5 not configured · 6 usage/state error.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
HUB_SOURCE_DIR = REPO_ROOT / "HUB" / "app"
STATE_PATH = REPO_ROOT / "HUB" / ".hub-deploy-state.json"
DEFAULT_SMOKE_URL = "https://nayanet.live/"

EXIT_OK = 0
EXIT_GATE = 2
EXIT_SMOKE = 3
EXIT_SMOKE_ROLLBACK_FAILED = 4
EXIT_NOT_CONFIGURED = 5
EXIT_USAGE = 6


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# --------------------------------------------------------------------------
# Syntax gate
# --------------------------------------------------------------------------

_INLINE_SCRIPT_RE = re.compile(
    r"<script(?![^>]*\bsrc\s*=)[^>]*>(.*?)</script>", re.DOTALL | re.IGNORECASE
)


def extract_inline_scripts(html: str) -> list[str]:
    return [m.group(1) for m in _INLINE_SCRIPT_RE.finditer(html) if m.group(1).strip()]


def _node_check(script_path: Path) -> tuple[bool, str]:
    node = shutil.which("node")
    if node is None:
        return False, "node not found on PATH — syntax gate cannot run (fail closed)"
    proc = subprocess.run(
        [node, "--check", str(script_path)],
        capture_output=True, text=True, timeout=60,
    )
    if proc.returncode == 0:
        return True, ""
    return False, (proc.stderr or proc.stdout).strip().splitlines()[0:3].__str__()


def syntax_gate(files: list[Path], scratch: Path) -> list[str]:
    """Return a list of failure strings; empty list == gate passed."""
    failures: list[str] = []
    scratch.mkdir(parents=True, exist_ok=True)
    for f in files:
        if f.suffix == ".js":
            ok, detail = _node_check(f)
            if not ok:
                failures.append(f"{f}: JS parse failed: {detail}")
        elif f.suffix in (".html", ".htm"):
            html = f.read_text(encoding="utf-8", errors="replace")
            for i, script in enumerate(extract_inline_scripts(html)):
                tmp = scratch / f"inline-{f.stem}-{i}.js"
                tmp.write_text(script, encoding="utf-8")
                ok, detail = _node_check(tmp)
                if not ok:
                    failures.append(f"{f} inline script #{i}: JS parse failed: {detail}")
    return failures


def collect_hub_files(source_dir: Path) -> list[Path]:
    if not source_dir.is_dir():
        return []
    return sorted(p for p in source_dir.rglob("*") if p.is_file())


# --------------------------------------------------------------------------
# Deploy adapters
# --------------------------------------------------------------------------

class CopyAdapter:
    """Publish the source set into a target directory (dry-run / static host)."""

    name = "copy"

    def __init__(self, target: Path):
        self.target = target

    def publish(self, source_dir: Path, commit: str) -> None:
        self.target.mkdir(parents=True, exist_ok=True)
        staging = Path(tempfile.mkdtemp(dir=self.target.parent, prefix=".hub-publish-"))
        try:
            for f in collect_hub_files(source_dir):
                dest = staging / f.relative_to(source_dir)
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(f, dest)
            # Swap: clear target contents, move staged files in.
            for child in self.target.iterdir():
                if child.is_dir():
                    shutil.rmtree(child)
                else:
                    child.unlink()
            for child in staging.iterdir():
                shutil.move(str(child), str(self.target / child.name))
        finally:
            shutil.rmtree(staging, ignore_errors=True)


class CommandAdapter:
    """Run the lane's real upload command ($HUB_DEPLOY_CMD)."""

    name = "command"

    def __init__(self, cmd: str):
        self.cmd = cmd

    def publish(self, source_dir: Path, commit: str) -> None:
        env = dict(os.environ)
        env["HUB_DEPLOY_SOURCE"] = str(source_dir)
        env["HUB_DEPLOY_COMMIT"] = commit
        proc = subprocess.run(self.cmd, shell=True, env=env,
                              capture_output=True, text=True, timeout=600)
        if proc.returncode != 0:
            raise RuntimeError(
                f"deploy command failed (exit {proc.returncode}): "
                f"{(proc.stderr or proc.stdout).strip()[:400]}"
            )


def make_adapter(target: str | None) -> CopyAdapter | CommandAdapter | None:
    if target:
        return CopyAdapter(Path(target))
    cmd = os.environ.get("HUB_DEPLOY_CMD", "").strip()
    if cmd:
        return CommandAdapter(cmd)
    return None


# --------------------------------------------------------------------------
# Smoke check
# --------------------------------------------------------------------------

def _feed_array_parses(body: str) -> tuple[bool, str]:
    """The served page must carry its feed array; if the array is a JSON
    literal it must parse. (The built page bakes `const NOTES = [...]`.)"""
    if "NayaFeedIntelligence" not in body and "const NOTES" not in body:
        return False, "no feed array marker (const NOTES / NayaFeedIntelligence) in served page"
    idx = body.find("const NOTES")
    if idx >= 0:
        eq = body.find("=", idx)
        start = body.find("[", eq) if eq >= 0 else -1
        # Only treat it as a JSON literal if '[' directly opens the value
        # (modulo whitespace) — `OFFICIAL_NOTES.concat(...)` is the unbuilt
        # source form and is not a baked array.
        between = body[eq + 1:start].strip() if start > eq >= 0 else ""
        if start >= 0 and between == "":
            try:
                json.JSONDecoder().raw_decode(body[start:])
            except json.JSONDecodeError as exc:
                return False, f"feed array does not parse: {exc}"
    return True, "feed array present and parses"


def smoke_check(url: str, timeout: int = 20) -> tuple[bool, str]:
    """GET the deployed page (http(s) URL or a local file/dir path)."""
    if url.startswith(("http://", "https://")):
        req = urllib.request.Request(url, headers={"User-Agent": "hub-deploy-smoke/1.0"})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                status = resp.status
                body = resp.read().decode("utf-8", errors="replace")
        except Exception as exc:  # connection, TLS, HTTP error status
            return False, f"GET {url} failed: {exc}"
        if status != 200:
            return False, f"GET {url} returned HTTP {status}"
    else:
        path = Path(url)
        page = path / "index.html" if path.is_dir() else path
        if not page.is_file():
            return False, f"smoke target page not found: {page}"
        body = page.read_text(encoding="utf-8", errors="replace")
    return _feed_array_parses(body)


# --------------------------------------------------------------------------
# State + rollback
# --------------------------------------------------------------------------

def read_state(state_path: Path = STATE_PATH) -> dict:
    if state_path.is_file():
        try:
            return json.loads(state_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}
    return {}


def write_state(state: dict, state_path: Path = STATE_PATH) -> None:
    state_path.parent.mkdir(parents=True, exist_ok=True)
    tmp = state_path.with_suffix(".tmp")
    tmp.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    tmp.replace(state_path)


def extract_hub_source_at_ref(ref: str, dest: Path, repo: Path = REPO_ROOT) -> Path:
    """Materialise HUB/app at a git ref into dest/hub-src (via git archive)."""
    dest.mkdir(parents=True, exist_ok=True)
    proc = subprocess.run(
        ["git", "archive", ref, "HUB/app"],
        cwd=repo, capture_output=True, timeout=120,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"git archive {ref} failed: {proc.stderr.decode()[:300]}")
    import io, tarfile
    with tarfile.open(fileobj=io.BytesIO(proc.stdout)) as tar:
        tar.extractall(dest)
    src = dest / "HUB" / "app"
    if not src.is_dir():
        raise RuntimeError(f"HUB/app not present at ref {ref}")
    return src


# --------------------------------------------------------------------------
# Pipeline
# --------------------------------------------------------------------------

def run_deploy(ref: str, target: str | None, smoke_url: str,
               state_path: Path = STATE_PATH, repo: Path = REPO_ROOT,
               receipt_path: Path | None = None) -> int:
    adapter = make_adapter(target)
    if adapter is None:
        print("NOT_CONFIGURED: no deploy transport — set --target DIR for a "
              "copy publish or $HUB_DEPLOY_CMD for the real upload. "
              "Failing closed; nothing was deployed.")
        return EXIT_NOT_CONFIGURED

    scratch = Path(tempfile.mkdtemp(prefix="hub-deploy-"))
    receipt: dict = {"ref": ref, "started_at": now_iso(), "adapter": adapter.name}
    try:
        source = extract_hub_source_at_ref(ref, scratch / "src", repo=repo)

        failures = syntax_gate(collect_hub_files(source), scratch / "gate")
        if failures:
            receipt.update({"result": "GATE_FAILED", "failures": failures})
            print("SYNTAX GATE FAILED — deploy refused:")
            for f in failures:
                print(f"  - {f}")
            return EXIT_GATE
        receipt["gate"] = "passed"

        state = read_state(state_path)
        previous = state.get("deployed_commit")
        try:
            adapter.publish(source, ref)
        except Exception as exc:
            receipt.update({"result": "DEPLOY_FAILED", "error": str(exc)})
            print(f"DEPLOY FAILED: {exc}")
            return EXIT_SMOKE_ROLLBACK_FAILED
        receipt["deployed_at"] = now_iso()

        ok, detail = smoke_check(smoke_url)
        receipt["smoke"] = {"ok": ok, "detail": detail, "url": smoke_url}
        if not ok:
            print(f"SMOKE FAILED: {detail}")
            receipt["result"] = "SMOKE_FAILED"
            if previous:
                print(f"Rolling back to previously deployed commit {previous} ...")
                try:
                    prev_src = extract_hub_source_at_ref(previous, scratch / "prev", repo=repo)
                    adapter.publish(prev_src, previous)
                    write_state({"deployed_commit": previous,
                                 "previous_commit": ref,
                                 "deployed_at": now_iso(),
                                 "adapter": adapter.name,
                                 "note": f"auto-rollback after smoke failure at {ref}"},
                                state_path)
                    receipt["rollback"] = "done"
                    print("Rollback complete.")
                    return EXIT_SMOKE
                except Exception as exc:
                    receipt["rollback"] = f"FAILED: {exc}"
                    print(f"ROLLBACK FAILED: {exc}")
                    return EXIT_SMOKE_ROLLBACK_FAILED
            receipt["rollback"] = "skipped — no previous deploy recorded"
            return EXIT_SMOKE

        write_state({"deployed_commit": ref,
                     "previous_commit": previous,
                     "deployed_at": receipt["deployed_at"],
                     "adapter": adapter.name}, state_path)
        receipt["result"] = "DEPLOYED"
        print(f"DEPLOYED {ref} via {adapter.name}; smoke OK ({detail}).")
        return EXIT_OK
    finally:
        if receipt_path is not None:
            receipt["finished_at"] = now_iso()
            receipt_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
        shutil.rmtree(scratch, ignore_errors=True)


def run_rollback(target: str | None, state_path: Path = STATE_PATH,
                 repo: Path = REPO_ROOT) -> int:
    adapter = make_adapter(target)
    if adapter is None:
        print("NOT_CONFIGURED: no deploy transport (see deploy --help).")
        return EXIT_NOT_CONFIGURED
    state = read_state(state_path)
    previous = state.get("previous_commit")
    if not previous:
        print("No previous_commit recorded in deploy state — nothing to roll back to.")
        return EXIT_USAGE
    scratch = Path(tempfile.mkdtemp(prefix="hub-rollback-"))
    try:
        src = extract_hub_source_at_ref(previous, scratch / "src", repo=repo)
        failures = syntax_gate(collect_hub_files(src), scratch / "gate")
        if failures:
            print("SYNTAX GATE FAILED on rollback source — refusing:")
            for f in failures:
                print(f"  - {f}")
            return EXIT_GATE
        adapter.publish(src, previous)
        write_state({"deployed_commit": previous,
                     "previous_commit": state.get("deployed_commit"),
                     "deployed_at": now_iso(),
                     "adapter": adapter.name,
                     "note": "manual rollback"}, state_path)
        print(f"ROLLED BACK to {previous}.")
        return EXIT_OK
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_gate = sub.add_parser("gate", help="run the syntax gate on Hub sources")
    p_gate.add_argument("--files", nargs="*", default=None)

    p_deploy = sub.add_parser("deploy", help="gate -> deploy -> smoke -> rollback-on-fail")
    p_deploy.add_argument("--ref", required=True, help="commit whose HUB/app to deploy")
    p_deploy.add_argument("--target", default=None, help="CopyAdapter target dir")
    p_deploy.add_argument("--dry-run", action="store_true",
                          help="dry run: requires --target; smoke checks the target copy")
    p_deploy.add_argument("--smoke-url", default=None,
                          help="default: the --target copy (dry-run) or https://nayanet.live/")
    p_deploy.add_argument("--receipt", default=None, help="write a JSON receipt to this path")

    p_rb = sub.add_parser("rollback", help="re-publish the previously deployed commit")
    p_rb.add_argument("--target", default=None)

    args = parser.parse_args(argv)

    if args.cmd == "gate":
        files = [Path(f) for f in args.files] if args.files else collect_hub_files(HUB_SOURCE_DIR)
        scratch = Path(tempfile.mkdtemp(prefix="hub-gate-"))
        try:
            failures = syntax_gate(files, scratch)
        finally:
            shutil.rmtree(scratch, ignore_errors=True)
        if failures:
            print("SYNTAX GATE FAILED:")
            for f in failures:
                print(f"  - {f}")
            return EXIT_GATE
        print(f"Syntax gate passed over {len(files)} Hub source files.")
        return EXIT_OK

    if args.cmd == "deploy":
        if args.dry_run and not args.target:
            print("--dry-run requires --target DIR.")
            return EXIT_USAGE
        smoke_url = args.smoke_url or (args.target if args.dry_run else DEFAULT_SMOKE_URL)
        return run_deploy(args.ref, args.target, smoke_url,
                          receipt_path=Path(args.receipt) if args.receipt else None)

    if args.cmd == "rollback":
        return run_rollback(args.target)

    return EXIT_USAGE


if __name__ == "__main__":
    sys.exit(main())
