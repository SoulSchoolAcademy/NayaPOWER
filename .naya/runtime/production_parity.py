"""PRODUCTION PARITY GATE — does production run what the repository says?

WHY THIS EXISTS
A reset commit removed a production-proven artifact from `main` while the live
Worker kept serving it. Nothing failed. Production looked healthy while source
and runtime had silently diverged, and the NEXT legitimate release would have
deleted working human sign-in in production.

A manual probe found that. A gate prevents it recurring. This one is read-only,
needs no credential, and is safe to run anywhere.

LAW: VERIFIED != PRODUCTION-PROVEN, and SOURCE == RUNTIME is a claim that must be
re-measured, never assumed.

Run:  python -B .naya/runtime/production_parity.py [--json]
Exit: 0 = no new drift, 1 = new drift, 2 = could not run
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
HUB = "https://sparkling-shape-7ae5.smartnetpodcast.workers.dev"
UA = {"User-Agent": "Mozilla/5.0 (compatible; naya-production-parity-gate/1)"}

# Artifacts that MUST be byte-identical between source and production.
# Each is a live path paired with its canonical repository source.
PAIRED: tuple[tuple[str, str], ...] = (
    ("/identity.html", "NAYANET/HUB/public/identity.html"),
    ("/", "NAYANET/HUB/index.html"),
    ("/assistant-runtime.js", "NAYANET/HUB/public/assistant-runtime.js"),
    (
        "/NAYANET/name-first-auth-adapter.js",
        "NAYANET/HUB/public/NAYANET/name-first-auth-adapter.js",
    ),
    ("/hub-completeness.js", "NAYANET/HUB/public/hub-completeness.js"),
)

# Artifacts production MUST serve, with the source path that must produce them.
# A reset that deletes the source is a latent production outage.
MUST_EXIST_IN_SOURCE: tuple[tuple[str, str], ...] = (
    ("identity page is live and functional", "NAYANET/HUB/public/identity.html"),
)

BASELINE = ".naya/production-parity-baseline.json"
REPORT = ".naya/production-parity-report.json"


def _finding(code: str, subject: str, detail: str) -> dict:
    fp = hashlib.sha256("|".join((code, subject)).encode()).hexdigest()[:16]
    return {"code": code, "subject": subject, "detail": detail, "fingerprint": fp}


def _git_blob(relpath: str, ref: str = "origin/main") -> bytes | None:
    try:
        out = subprocess.check_output(
            ["git", "cat-file", "blob", f"{ref}:{relpath}"], cwd=REPO, stderr=subprocess.DEVNULL
        )
        return out
    except Exception:  # noqa: BLE001
        return None


def _fetch(path: str) -> tuple[int, bytes]:
    req = urllib.request.Request(HUB + path, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, b""
    except Exception:  # noqa: BLE001
        return 0, b""


def audit() -> dict:
    findings: list[dict] = []
    pairs: list[dict] = []

    for live_path, src_path in PAIRED:
        status, live = _fetch(live_path)
        src = _git_blob(src_path)
        record = {
            "live_path": live_path,
            "source_path": src_path,
            "live_status": status,
            "live_sha256": hashlib.sha256(live).hexdigest() if live else None,
            "source_present": src is not None,
            "source_sha256": hashlib.sha256(src).hexdigest() if src is not None else None,
        }
        record["identical"] = bool(live) and src is not None and record["live_sha256"] == record["source_sha256"]
        pairs.append(record)

        if src is None:
            findings.append(
                _finding(
                    "SOURCE_ABSENT_PRODUCTION_SERVES",
                    live_path,
                    f"production serves {live_path} (HTTP {status}) but `{src_path}` is not "
                    f"in origin/main. Source/runtime parity is BROKEN: a reset removed the "
                    f"source while production kept serving it, and the next legitimate release "
                    f"will delete it in production.",
                )
            )
        elif not record["identical"]:
            findings.append(
                _finding(
                    "PARITY_MISMATCH",
                    live_path,
                    f"production sha256 {record['live_sha256']} != source sha256 "
                    f"{record['source_sha256']}. Production is running an artifact that does "
                    f"not match the repository.",
                )
            )

    for label, src_path in MUST_EXIST_IN_SOURCE:
        if _git_blob(src_path) is None:
            findings.append(
                _finding(
                    "LATENT_PRODUCTION_OUTAGE",
                    label,
                    f"`{src_path}` is required for a working production surface but is absent "
                    f"from origin/main. The next release will remove it in production.",
                )
            )

    return {
        "schema": "naya/production-parity/v1",
        "hub": HUB,
        "source_ref": "origin/main",
        "pairs_checked": len(pairs),
        "identical": sum(1 for p in pairs if p["identical"]),
        "parity_ok": not findings,
        "pairs": pairs,
        "findings": findings,
    }


def classify(report: dict, baseline: set[str]) -> dict:
    new = [f for f in report["findings"] if f["fingerprint"] not in baseline]
    return {"new_drift": len(new), "known_debt": len(report["findings"]) - len(new), "new": new}


def load_baseline() -> set[str]:
    p = REPO / BASELINE
    if not p.is_file():
        return set()
    return {f["fingerprint"] for f in json.loads(p.read_text(encoding="utf-8")).get("findings", [])}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--write-baseline", action="store_true")
    args = ap.parse_args()
    try:
        report = audit()
    except Exception as exc:  # noqa: BLE001
        print(f"PRODUCTION_PARITY=AUDIT_ERROR {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2

    if args.write_baseline:
        (REPO / BASELINE).write_text(
            json.dumps(
                {
                    "schema": "naya/production-parity-baseline/v1",
                    "note": "Known source/runtime drift. New drift fails the gate.",
                    "findings": report["findings"],
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        print(f"BASELINE_WRITTEN findings={len(report['findings'])}")
        return 0

    result = classify(report, load_baseline())
    if args.json:
        print(json.dumps({**report, **result}, indent=2))
    else:
        print("NAYA_PRODUCTION_PARITY")
        print(f"HUB={report['hub']}  SOURCE_REF={report['source_ref']}")
        for p in report["pairs"]:
            flag = "IDENTICAL" if p["identical"] else ("SOURCE_ABSENT" if not p["source_present"] else "MISMATCH")
            print(f"  [{flag:>12}] {p['live_path']}")
        for f in report["findings"]:
            print(f"  FINDING {f['code']}: {f['subject']}")
        print(f"KNOWN_DEBT={result['known_debt']}  NEW_DRIFT={result['new_drift']}")
        print(f"PARITY_OK={report['parity_ok']}")
        for f in result["new"]:
            print(f"  NEW: {f['code']} {f['subject']}")

    (REPO / REPORT).write_text(json.dumps({**report, **result}, indent=2) + "\n", encoding="utf-8")
    return 1 if result["new_drift"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
