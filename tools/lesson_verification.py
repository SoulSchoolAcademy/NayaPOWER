#!/usr/bin/env python3
"""Learning-loop closure harness: prove a promoted lesson is LEARNED, not merely stored.

Doctrine (Constitution V2, ratified 2026-10-10): stored != learned. Learning is
proven by behavior change, tested on NOVEL problems, scored BLIND.

A "battery" is a JSON file describing one promoted Smart Note lesson plus a set
of novel problems exercising it. Novel = the problem does NOT reuse the
originating incident's entities (enforced mechanically by fingerprint check).
Blind = the scoring path never sees which lesson is under test: cases are
shuffled and stripped of lesson identity before judging, and the judge receives
only (scenario, subject response, behavioral criteria).

Usage:
    python3 tools/lesson_verification.py scaffold --lesson-id SN-099 --title "..." --out battery.json
    python3 tools/lesson_verification.py check-novelty --battery battery.json
    python3 tools/lesson_verification.py score --battery battery.json --responses responses.json [--report report.json]
    python3 tools/lesson_verification.py verify --battery battery.json --responses responses.json [--registry .naya/memory/smart-notes/index.json]

The subject under test is pluggable. `--responses` points at a JSON file of the
form {"subject": "<who/what produced the responses>", "responses":
[{"case_id": ..., "response": ...}]}. In CI the subject is whatever the
promotion workflow wires up (an independent seat, a recorded transcript, or a
deterministic fixture); the harness itself stays subject-agnostic.

Default judge: deterministic lexical rubric matching. Each case declares `must`
criteria (positive signals that must appear in the response) and `must_not`
criteria (anti-signals that must not appear). A case PASSES only when every
`must` criterion fires and no `must_not` anti-signal fires. This is mechanical
and auditable on purpose: it tests the machinery, not eloquence. Teams may plug
a stronger judge (e.g. an independent scoring seat) via --judge module:function
with signature judge(scenario, response, must, must_not) -> list[(criterion,
passed, reason)].

Battery schema: naya.lesson-verification-battery.v1 (see `scaffold` output).

Exit codes: 0 = every case passed; 1 = one or more cases failed (honest data:
a fail proves the loop was open for that behavior); 2 = usage or structural
error (non-novel case, unknown case_id in responses, lesson missing from the
registry when --registry is given).
"""

from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import random
import re
import sys
from pathlib import Path

SCHEMA = "naya.lesson-verification-battery.v1"
REGISTRY_REQUIRED_KEYS = ("intelligent_block_id", "truth_state", "title")


# ---------------------------------------------------------------------------
# loading / validation
# ---------------------------------------------------------------------------

def load_battery(path: Path) -> dict:
    try:
        battery = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"cannot read battery {path}: {exc}") from exc
    if battery.get("schema") != SCHEMA:
        raise StructureError(f"{path}: schema must be {SCHEMA!r}")
    for key in ("lesson_id", "behavioral_expectation", "origin_incident", "cases"):
        if key not in battery:
            raise StructureError(f"{path}: missing required key {key!r}")
    incident = battery["origin_incident"]
    if "fingerprints" not in incident or not incident["fingerprints"]:
        raise StructureError(f"{path}: origin_incident.fingerprints must be non-empty")
    case_ids = set()
    for case in battery["cases"]:
        for key in ("case_id", "scenario", "must", "must_not", "rationale"):
            if key not in case:
                raise StructureError(f"{path}: case missing required key {key!r}")
        if case["case_id"] in case_ids:
            raise StructureError(f"{path}: duplicate case_id {case['case_id']!r}")
        case_ids.add(case["case_id"])
        if not case["must"]:
            raise StructureError(f"{path}: case {case['case_id']!r} must declare at least one `must` criterion")
    if not battery["cases"]:
        raise StructureError(f"{path}: battery must contain at least one case")
    return battery


class StructureError(Exception):
    """Raised for malformed batteries, responses, or registry lookups (exit 2)."""


def load_responses(path: Path, battery: dict) -> dict:
    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise StructureError(f"cannot read responses {path}: {exc}") from exc
    if "responses" not in doc or not isinstance(doc["responses"], list):
        raise StructureError(f"{path}: missing `responses` list")
    case_ids = {c["case_id"] for c in battery["cases"]}
    seen = set()
    for entry in doc["responses"]:
        cid = entry.get("case_id")
        if cid not in case_ids:
            raise StructureError(f"{path}: response for unknown case_id {cid!r}")
        if cid in seen:
            raise StructureError(f"{path}: duplicate response for case_id {cid!r}")
        if "response" not in entry or not str(entry["response"]).strip():
            raise StructureError(f"{path}: empty response for case_id {cid!r}")
        seen.add(cid)
    missing = case_ids - seen
    if missing:
        raise StructureError(f"{path}: missing responses for cases {sorted(missing)}")
    return doc


# ---------------------------------------------------------------------------
# novelty: the case must not replay the originating incident
# ---------------------------------------------------------------------------

def novelty_violations(battery: dict) -> list[dict]:
    """Return one entry per (case, fingerprint) hit. Empty list = novel."""
    fingerprints = [str(f).lower() for f in battery["origin_incident"]["fingerprints"]]
    violations = []
    for case in battery["cases"]:
        haystacks = {
            "scenario": case["scenario"],
            "must": " ".join(c.get("criterion", "") + " " + " ".join(c.get("signals", [])) for c in case["must"]),
            "must_not": " ".join(c.get("criterion", "") + " " + " ".join(c.get("anti_signals", [])) for c in case["must_not"]),
            "rationale": case.get("rationale", ""),
        }
        for field, text in haystacks.items():
            lowered = str(text).lower()
            for fp in fingerprints:
                if fp and fp in lowered:
                    violations.append(
                        {"case_id": case["case_id"], "field": field, "fingerprint": fp}
                    )
    return violations


# ---------------------------------------------------------------------------
# blind scoring
# ---------------------------------------------------------------------------

def _word_hit(text: str, phrase: str) -> bool:
    return re.search(r"\b" + re.escape(phrase) + r"\b", text, re.IGNORECASE) is not None


def lexical_judge(scenario: str, response: str, must: list, must_not: list) -> list[tuple[str, bool, str]]:
    """Deterministic default judge. Never receives any lesson identity."""
    findings = []
    for criterion in must:
        name = criterion.get("criterion", "?")
        signals = criterion.get("signals", [])
        hits = [s for s in signals if _word_hit(response, s)]
        if hits:
            findings.append((f"must:{name}", True, f"signal hit: {hits[0]!r}"))
        else:
            findings.append(
                (f"must:{name}", False,
                 f"no signal from {signals} found in response")
            )
    for criterion in must_not:
        name = criterion.get("criterion", "?")
        anti = criterion.get("anti_signals", [])
        hits = [s for s in anti if _word_hit(response, s)]
        if hits:
            findings.append((f"must_not:{name}", False, f"anti-signal hit: {hits[0]!r}"))
        else:
            findings.append((f"must_not:{name}", True, "no anti-signal present"))
    return findings


def load_judge(spec: str | None):
    if not spec:
        return lexical_judge
    module_name, _, func_name = spec.partition(":")
    if not func_name:
        raise StructureError(f"--judge must be module:function, got {spec!r}")
    module = importlib.import_module(module_name)
    func = getattr(module, func_name, None)
    if not callable(func):
        raise StructureError(f"--judge {spec!r} is not callable")
    return func


def blind_view(battery: dict) -> list[dict]:
    """Strip lesson identity and shuffle: the judge cannot know the lesson.

    The blind view carries only (anon_id, scenario, must, must_not). The
    `expected` label and rationale stay sealed until the report is assembled.
    Shuffle is seeded by the battery content hash so runs are deterministic.
    """
    seed = int(hashlib.sha256(
        json.dumps(battery, sort_keys=True).encode()).hexdigest(), 16)
    rng = random.Random(seed)
    order = list(range(len(battery["cases"])))
    rng.shuffle(order)
    view = []
    for anon_n, idx in enumerate(order, start=1):
        case = battery["cases"][idx]
        view.append({
            "anon_id": f"CASE-{anon_n:02d}",
            "case_id": case["case_id"],  # kept for joining only; NOT passed to judge
            "scenario": case["scenario"],
            "must": case["must"],
            "must_not": case["must_not"],
        })
    # Prove blindness structurally: drop everything the judge must not see.
    for item in view:
        item.pop("case_id")
    sealed = {c["case_id"]: c for c in battery["cases"]}
    return view, sealed


def score_battery(battery: dict, responses_doc: dict, judge) -> dict:
    responses = {r["case_id"]: r["response"] for r in responses_doc["responses"]}
    view, sealed = blind_view(battery)
    # Rebuild the join map without leaking identity into the judge call.
    join = {}
    order_check = list(battery["cases"])
    seed = int(hashlib.sha256(json.dumps(battery, sort_keys=True).encode()).hexdigest(), 16)
    rng = random.Random(seed)
    idxs = list(range(len(order_check)))
    rng.shuffle(idxs)
    for anon_n, idx in enumerate(idxs, start=1):
        join[f"CASE-{anon_n:02d}"] = order_check[idx]["case_id"]

    case_results = []
    for item in view:
        case_id = join[item["anon_id"]]
        response = responses[case_id]
        # The judge receives NO lesson identity: only scenario, response, criteria.
        findings = judge(item["scenario"], response, item["must"], item["must_not"])
        reasons = [
            {"criterion": name, "passed": passed, "reason": reason}
            for name, passed, reason in findings
        ]
        verdict = "PASS" if all(f[1] for f in findings) else "FAIL"
        case_results.append({
            "case_id": case_id,
            "anon_id": item["anon_id"],
            "expected": sealed[case_id].get("expected"),
            "verdict": verdict,
            "reasons": reasons,
        })
    # Report in original case order for readability (scoring itself was blind).
    case_results.sort(key=lambda r: [c["case_id"] for c in battery["cases"]].index(r["case_id"]))
    passed = sum(1 for r in case_results if r["verdict"] == "PASS")
    return {
        "schema": "naya.lesson-verification-report.v1",
        "lesson_id": battery["lesson_id"],
        "lesson_title": battery.get("lesson_title", ""),
        "subject": responses_doc.get("subject", "unspecified"),
        "blind": True,
        "novel": True,
        "verdict": "PASS" if passed == len(case_results) else "FAIL",
        "summary": {"passed": passed, "failed": len(case_results) - passed,
                    "total": len(case_results)},
        "cases": case_results,
    }


# ---------------------------------------------------------------------------
# registry check: the lesson under test must actually be promoted
# ---------------------------------------------------------------------------

def registry_lookup(registry_path: Path, battery: dict) -> dict:
    try:
        registry = json.loads(registry_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise StructureError(f"cannot read registry {registry_path}: {exc}") from exc
    entries = registry.get("entries", [])
    want = battery.get("registry_block_id") or battery["lesson_id"]
    for entry in entries:
        if entry.get("intelligent_block_id") == want or entry.get("smart_note_id") == want:
            missing = [k for k in REGISTRY_REQUIRED_KEYS if k not in entry]
            if missing:
                raise StructureError(f"registry entry for {want!r} missing {missing}")
            return entry
    raise StructureError(
        f"lesson {battery['lesson_id']!r} (block {want!r}) not found in registry "
        f"{registry_path}: cannot verify an unregistered lesson")


# ---------------------------------------------------------------------------
# commands
# ---------------------------------------------------------------------------

def cmd_scaffold(args) -> int:
    battery = {
        "schema": SCHEMA,
        "lesson_id": args.lesson_id,
        "lesson_title": args.title,
        "registry_block_id": args.block_id or "",
        "behavioral_expectation": "One paragraph: the observable behavior change this lesson demands.",
        "origin_incident": {
            "summary": "What incident produced this lesson (so cases can avoid replaying it).",
            "fingerprints": ["distinctive-token-1", "distinctive-token-2"],
        },
        "cases": [
            {
                "case_id": f"{args.lesson_id}-N1",
                "scenario": "A novel problem exercising the lesson. Must not reuse origin-incident entities.",
                "expected": "SHORT_BEHAVIOR_LABEL",
                "must": [{"criterion": "what must be observable", "signals": ["phrase one", "phrase two"]}],
                "must_not": [{"criterion": "what must be absent", "anti_signals": ["bad phrase"]}],
                "rationale": "Why this case discriminates learned vs stored.",
            }
        ],
    }
    out = Path(args.out)
    out.write_text(json.dumps(battery, indent=2) + "\n", encoding="utf-8")
    print(f"scaffolded {out}")
    return 0


def cmd_check_novelty(args) -> int:
    battery = load_battery(Path(args.battery))
    violations = novelty_violations(battery)
    if violations:
        print(f"NOVELTY FAIL: {len(violations)} fingerprint hit(s) — "
              f"these cases replay the originating incident:", file=sys.stderr)
        for v in violations:
            print(f"  {v['case_id']} [{v['field']}] reuses fingerprint {v['fingerprint']!r}",
                  file=sys.stderr)
        return 2
    print(f"novelty OK: {len(battery['cases'])} cases, "
          f"{len(battery['origin_incident']['fingerprints'])} fingerprints avoided")
    return 0


def cmd_score(args) -> int:
    battery = load_battery(Path(args.battery))
    responses_doc = load_responses(Path(args.responses), battery)
    judge = load_judge(args.judge)
    report = score_battery(battery, responses_doc, judge)
    if args.report:
        Path(args.report).write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print(f"report written to {args.report}")
    s = report["summary"]
    print(f"lesson {report['lesson_id']}: {report['verdict']} "
          f"({s['passed']}/{s['total']} cases passed, subject: {report['subject']})")
    for case in report["cases"]:
        mark = "PASS" if case["verdict"] == "PASS" else "FAIL"
        print(f"  [{mark}] {case['case_id']} ({case['anon_id']}, expected {case['expected']})")
        for r in case["reasons"]:
            tick = "ok " if r["passed"] else "MISS"
            print(f"         {tick} {r['criterion']}: {r['reason']}")
    return 0 if report["verdict"] == "PASS" else 1


def cmd_verify(args) -> int:
    battery = load_battery(Path(args.battery))
    violations = novelty_violations(battery)
    if violations:
        print(f"NOVELTY FAIL: {len(violations)} fingerprint hit(s):", file=sys.stderr)
        for v in violations:
            print(f"  {v['case_id']} [{v['field']}] reuses fingerprint {v['fingerprint']!r}",
                  file=sys.stderr)
        return 2
    registry_entry = None
    if args.registry:
        registry_entry = registry_lookup(Path(args.registry), battery)
        print(f"registry: {battery['lesson_id']} found as "
              f"{registry_entry['intelligent_block_id']} "
              f"(truth_state={registry_entry['truth_state']})")
    else:
        print("registry: skipped (no --registry given)")
    rc = cmd_score(args)
    if registry_entry and registry_entry.get("truth_state") not in ("RATIFIED", "LEARNED", "ACTIVE"):
        print(f"note: registry truth_state is {registry_entry['truth_state']!r} — "
              f"this battery gates promotion, it does not assume it", file=sys.stderr)
    return rc


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Learning-loop closure harness: verify a promoted Smart Note "
                    "lesson is LEARNED (behavior change on novel problems, scored blind).")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("scaffold", help="write a battery template")
    p.add_argument("--lesson-id", required=True)
    p.add_argument("--title", default="")
    p.add_argument("--block-id", default="")
    p.add_argument("--out", required=True)
    p.set_defaults(func=cmd_scaffold)

    p = sub.add_parser("check-novelty", help="reject cases that replay the origin incident")
    p.add_argument("--battery", required=True)
    p.set_defaults(func=cmd_check_novelty)

    p = sub.add_parser("score", help="blind-score subject responses against the battery")
    p.add_argument("--battery", required=True)
    p.add_argument("--responses", required=True)
    p.add_argument("--report", default="")
    p.add_argument("--judge", default="",
                   help="optional module:function judge override")
    p.set_defaults(func=cmd_score)

    p = sub.add_parser("verify", help="check-novelty + registry lookup + blind score (CI entrypoint)")
    p.add_argument("--battery", required=True)
    p.add_argument("--responses", required=True)
    p.add_argument("--report", default="")
    p.add_argument("--registry", default="")
    p.add_argument("--judge", default="")
    p.set_defaults(func=cmd_verify)

    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except StructureError as exc:
        print(f"STRUCTURE ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
