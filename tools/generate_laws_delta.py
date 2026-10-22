#!/usr/bin/env python3
"""LAWS-DELTA generator + validator.

Emits the distilled, numbered governance law sets of BRAIN/01-GOVERNANCE/
as one versioned machine file (LAWS-DELTA.machine.json): per set — id,
title, statement, falsifier, owner, tongues, and the git blob SHA of the
machine tongue it was distilled from. The output is deterministic (no
wall-clock anywhere): re-running it over unchanged sources produces a
byte-identical file, which is what makes the freshness check meaningful.

SCOPE (honest): numbered governance sets only — the sets that carry a
`NNNN-*.machine.json` tongue. Two neighbouring artifacts are deliberately
NOT folded in:
  * AGENTS.md's L-numbered lesson entries live outside this repo (seat VM)
    and are prose without a stable per-entry schema; parsing them here
    would be brittle and would manufacture fields the source doesn't carry.
  * BRAIN/01-GOVERNANCE/OPERATING-LAW.json (compiled 2026-10-10, LAW-X01
    scheme) was RETIRED 2026-10-22 by the daily-law-registry landing
    (GT-010): superseded for governance sets by this delta and for the
    daily law by BRAIN/01-GOVERNANCE/DAILY-LAW-REGISTRY.machine.json.
    Exactly two generated compilations of law survive; this is one.
Fields a source set does not carry (older sets predate the falsifier/owner
convention) are emitted as null — never invented.

Usage:
  python3 tools/generate_laws_delta.py [--gov DIR] [--out FILE]
  python3 tools/generate_laws_delta.py --check [--gov DIR] [--out FILE]

--check validates every numbered machine tongue (JSON parses; the delta's
required fields are derivable) and that the committed delta is fresh
(regeneration == committed bytes). Every failure prints the self-explaining
form:  MISSING: <what> — CURE: <the single curing action> (owner: <lane>)
"""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

SCHEMA = "naya/laws-delta/v1"
MACHINE_RE = re.compile(r"^(\d{4})-.+\.machine\.json$")


def blob_sha(data: bytes) -> str:
    """git blob SHA-1 of raw bytes (pure python — no repo needed)."""
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def pick(d, *keys):
    for k in keys:
        v = d.get(k)
        if isinstance(v, str) and v.strip():
            return v
    return None


def statement_of(d):
    v = pick(d, "statement", "one_line_form", "the_one_line_form")
    if v:
        return v
    vl = d.get("value_law")
    if isinstance(vl, dict):
        v = pick(vl, "statement")
        if v:
            return v
    return pick(d, "vow", "law", "title", "protocol")


def title_of(d, stem):
    return pick(d, "title", "protocol") or stem


def collect(gov: Path):
    """Return (laws, sources, problems). problems = list of cure lines."""
    laws, sources, problems = [], {}, []
    for f in sorted(gov.glob("*.machine.json")):
        m = MACHINE_RE.match(f.name)
        if not m:
            continue
        num = m.group(1)
        raw = f.read_bytes()
        sources[f.name] = blob_sha(raw)
        try:
            d = json.loads(raw)
        except json.JSONDecodeError as e:
            problems.append(
                f"MISSING: valid JSON in BRAIN/01-GOVERNANCE/{f.name} "
                f"(line {e.lineno} col {e.colno}: {e.msg}) — "
                f"CURE: fix the JSON syntax at the reported position and re-run "
                f"tools/generate_laws_delta.py --check (owner: the set's author lane)"
            )
            continue
        if not isinstance(d, dict):
            problems.append(
                f"MISSING: a JSON object at the root of BRAIN/01-GOVERNANCE/{f.name} — "
                f"CURE: rewrite the machine tongue as a single JSON object (owner: the set's author lane)"
            )
            continue
        human = sorted(gov.glob(f"{num}-*.human.md"))
        ai = sorted(gov.glob(f"{num}-*.ai.md"))
        laws.append({
            "id": f"GOV-{num}",
            "number": num,
            "title": title_of(d, f.name),
            "statement": statement_of(d),
            "falsifier": d.get("falsifier") if isinstance(d.get("falsifier"), str) else None,
            "owner": d.get("owner") if isinstance(d.get("owner"), str) else None,
            "status": d.get("status") if isinstance(d.get("status"), str) else None,
            "tongues": {
                "human": f"BRAIN/01-GOVERNANCE/{human[0].name}" if human else None,
                "ai": f"BRAIN/01-GOVERNANCE/{ai[0].name}" if ai else None,
                "machine": f"BRAIN/01-GOVERNANCE/{f.name}",
            },
            "source_blob_sha": sources[f.name],
        })
    laws.sort(key=lambda x: x["number"])
    return laws, sources, problems


def build_delta(gov: Path):
    laws, sources, problems = collect(gov)
    fingerprint = hashlib.sha256(
        "".join(f"{name}\0{sha}\n" for name, sha in sorted(sources.items())).encode()
    ).hexdigest()
    delta = {
        "schema": SCHEMA,
        "scope": (
            "Numbered governance sets of BRAIN/01-GOVERNANCE/ that carry a machine tongue. "
            "Excludes AGENTS.md L-entries (compiled separately by tools/generate_daily_law_registry.py "
            "into DAILY-LAW-REGISTRY.machine.json, which folds this delta in) "
            "and OPERATING-LAW.json (2026-10-10 LAW-X01 compilation, retired 2026-10-22 by GT-010). "
            "Fields a source set does not carry are null, never invented."
        ),
        "generated_from": {
            "governance_dir": "BRAIN/01-GOVERNANCE",
            "generator": "tools/generate_laws_delta.py",
            "machine_tongue_blob_shas": sources,
            "source_fingerprint_sha256": fingerprint,
        },
        "law_count": len(laws),
        "laws": laws,
    }
    return delta, problems


def render(delta) -> bytes:
    return (json.dumps(delta, indent=1, sort_keys=True) + "\n").encode()


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--gov", default="BRAIN/01-GOVERNANCE")
    ap.add_argument("--out", default=None, help="default: <gov>/LAWS-DELTA.machine.json")
    ap.add_argument("--check", action="store_true", help="validate + freshness check, write nothing")
    args = ap.parse_args(argv)
    gov = Path(args.gov)
    out = Path(args.out) if args.out else gov / "LAWS-DELTA.machine.json"
    if not gov.is_dir():
        print(f"MISSING: governance directory {gov} — CURE: run from the repo root (owner: calling lane)")
        return 1
    delta, problems = build_delta(gov)
    for p in problems:
        print(p)
    if problems:
        return 1
    data = render(delta)
    if args.check:
        if not out.exists():
            print(f"MISSING: laws delta at {out} — CURE: run tools/generate_laws_delta.py (owner: main seat)")
            return 1
        if out.read_bytes() != data:
            print(f"MISSING: a current laws delta at {out} (committed bytes differ from a fresh generation) — "
                  f"CURE: run tools/generate_laws_delta.py and commit the result (owner: main seat)")
            return 1
        print(f"OK: {delta['law_count']} law sets valid; delta fresh (fingerprint {delta['generated_from']['source_fingerprint_sha256'][:12]}…)")
        return 0
    out.write_bytes(data)
    print(f"wrote {out} — {delta['law_count']} law sets, fingerprint {delta['generated_from']['source_fingerprint_sha256'][:12]}…")
    return 0


if __name__ == "__main__":
    sys.exit(main())
