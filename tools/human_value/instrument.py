#!/usr/bin/env python3
"""Human Value change-grade instrument v1 — companion to the event ledger.

Grades a shipped change against the Human Value rubric (see HUMAN-VALUE.md):
USE 30 / DELTA 25 / PROOF 20 / DURABLE 15 / CLEAN 10, with a binary HARM gate
checked first. Every judgment must cite evidence; the instrument verifies each
citation mechanically and caps scores that rest on nothing checkable.

This is the change-grading companion to the existing event-ledger instrument
(tools/human_value/compute_hv.py + schema.py): it grades individual shipped
changes at merge time; `to-event` exports REAL VALUE+ scorecards as
schema-valid ledger events, so the two instruments compose instead of compete.

Commands:
  score     --packet PACKET.json --repo REPO --ref SHA [--out OUT.json]
  pilot     --merge SHA --repo REPO --out PACKET.json [--pr N] [--title T]
  to-event  --scorecard CARD.json --out EVENT.json [--date YYYY-MM-DD]
            [--event-id ID] [--receipt-ref REF] [--pr-url URL]
  compare   --a CARD_A.json --b CARD_B.json [--out REPORT.json]
            (second-seat grading: agreement bands, not averaged)
  recheck   --scorecard CARD.json --repo REPO --ref LATER_SHA [--out REPORT.json]
            (durability loop: re-verify evidence at a later ref)
  receipt-template [--change-id ID] [--out RECEIPT.json]
            (in-repo machine-readable delta receipt schema)

`to-event` mints a ledger event ONLY for verdicts HIGH VALUE / REAL VALUE.
THIN, NO VALUE, and DISQUALIFIED mint nothing — the instrument refuses to
manufacture value-credit. Every minted event is validated against the
existing schema.py before it is written.

Exit codes: 0 = scored (or skeleton built). 2 = fail-safe: the input was
malformed or unverifiable, so NO score is emitted. A number without a valid
packet is a lie with formatting — the instrument refuses to produce one.

Only the standard library is used. Evidence verification shells out to git.
"""

import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone

PACKET_VERSION = 1

DIMENSIONS = ("USE", "DELTA", "PROOF", "DURABLE", "CLEAN")
WEIGHTS = {"USE": 0.30, "DELTA": 0.25, "PROOF": 0.20, "DURABLE": 0.15, "CLEAN": 0.10}

EVIDENCE_KINDS = ("file", "sha", "test", "command", "url", "receipt")

# Receipt schema v1 — a machine-readable, in-repo record of a change's delta.
# Lane workers commit receipts/<change-id>.json WITH the change; the instrument
# then verifies them mechanically (they exist at the ref, they parse, they
# hold before/after numbers) instead of capping off-repo delta claims at 5.
# Receipts are verified-but-soft evidence: they carry DELTA up to 8, flagged
# RECEIPT_SOFT_CAP above that — a committed claim is checkable, but it is
# still the grader's own claim, not an independent re-run.
RECEIPT_VERSION = 1
RECEIPT_SOFT_CAP = 8.0

VERDICTS = (
    (9.0, "HIGH VALUE"),
    (7.0, "REAL VALUE"),
    (5.0, "THIN"),
    (0.0, "NO VALUE"),
)


class InstrumentError(Exception):
    """Fail-safe: malformed or unverifiable input. Never emits a score."""


# ---------------------------------------------------------------- git helpers

def _git(repo, *args):
    p = subprocess.run(
        ["git", "-C", repo, *args],
        capture_output=True, text=True, timeout=60,
    )
    return p


def _git_ok(repo, *args):
    return _git(repo, *args).returncode == 0


def _file_line_count(repo, ref, path):
    """Line count of path at ref, or None if the path is not there."""
    p = _git(repo, "show", f"{ref}:{path}")
    if p.returncode != 0:
        return None
    return len(p.stdout.splitlines())


def _parse_lines(spec, max_lines):
    """'12-34' or '12' -> (start, end); raises InstrumentError on garbage."""
    m = re.fullmatch(r"\s*(\d+)\s*(?:-\s*(\d+)\s*)?", str(spec))
    if not m:
        raise InstrumentError(f"bad lines spec: {spec!r} (want 'N' or 'N-M')")
    start, end = int(m.group(1)), int(m.group(2) or m.group(1))
    if start < 1 or end < start or end > max_lines:
        raise InstrumentError(
            f"lines {spec!r} out of range for file with {max_lines} lines"
        )
    return start, end


# ---------------------------------------------------------------- validation

def _need(packet, key, what="packet"):
    if key not in packet:
        raise InstrumentError(f"{what} missing required field: {key!r}")
    return packet[key]


def _check_score(value, where):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise InstrumentError(f"{where}: score must be a number 0-10, got {value!r}")
    if not (0 <= value <= 10):
        raise InstrumentError(f"{where}: score {value} out of range 0-10")
    return float(value)


def _validate_evidence(item, i, dim):
    where = f"judgment {dim} evidence[{i}]"
    if not isinstance(item, dict):
        raise InstrumentError(f"{where}: must be an object")
    kind = _need(item, "kind", where)
    if kind not in EVIDENCE_KINDS:
        raise InstrumentError(f"{where}: unknown kind {kind!r} (want one of {EVIDENCE_KINDS})")
    if kind in ("file", "test", "receipt"):
        path = _need(item, "path", where)
        if not isinstance(path, str) or not path.strip() or path.startswith("/"):
            raise InstrumentError(f"{where}: bad path {path!r}")
    if kind == "sha":
        sha = _need(item, "sha", where)
        if not isinstance(sha, str) or not re.fullmatch(r"[0-9a-f]{7,40}", sha):
            raise InstrumentError(f"{where}: bad sha {sha!r}")
    if "lines" in item and not isinstance(item["lines"], str):
        raise InstrumentError(f"{where}: lines must be a string like '12-34'")
    return item


def validate_packet(packet):
    """Strict schema check. Raises InstrumentError on anything malformed."""
    if not isinstance(packet, dict):
        raise InstrumentError("packet must be a JSON object")
    if packet.get("packet_version") != PACKET_VERSION:
        raise InstrumentError(
            f"packet_version must be {PACKET_VERSION}, got {packet.get('packet_version')!r}"
        )
    for key in ("change_id", "title", "merge_sha", "grader"):
        v = _need(packet, key)
        if not isinstance(v, str) or not v.strip():
            raise InstrumentError(f"field {key!r} must be a non-empty string")
    if not re.fullmatch(r"[0-9a-f]{7,40}", packet["merge_sha"]):
        raise InstrumentError(f"bad merge_sha {packet['merge_sha']!r}")

    harm = _need(packet, "harm_check")
    if not isinstance(harm, dict) or not isinstance(harm.get("found"), bool):
        raise InstrumentError("harm_check must be an object with boolean 'found'")

    judgments = _need(packet, "judgments")
    if not isinstance(judgments, list):
        raise InstrumentError("judgments must be a list")
    seen = set()
    for j in judgments:
        if not isinstance(j, dict):
            raise InstrumentError("each judgment must be an object")
        dim = _need(j, "dimension", "judgment")
        if dim not in DIMENSIONS:
            raise InstrumentError(f"unknown dimension {dim!r} (want one of {DIMENSIONS})")
        if dim in seen:
            raise InstrumentError(f"duplicate judgment for dimension {dim!r}")
        seen.add(dim)
        if j.get("score") is None:
            raise InstrumentError(f"judgment {dim}: score is required (packet incomplete)")
        j["score"] = _check_score(j["score"], f"judgment {dim}")
        ev = j.get("evidence", [])
        if not isinstance(ev, list):
            raise InstrumentError(f"judgment {dim}: evidence must be a list")
        j["evidence"] = [_validate_evidence(e, i, dim) for i, e in enumerate(ev)]
    missing = set(DIMENSIONS) - seen
    if missing:
        raise InstrumentError(f"packet missing judgments for: {sorted(missing)}")
    return packet


# ---------------------------------------------------------------- verification

def _cited_hash(repo, ref, path, lines):
    """sha256 of the cited line range of path at ref, or None."""
    n = _file_line_count(repo, ref, path)
    if n is None:
        return None
    try:
        if lines:
            s, e = _parse_lines(lines, n)
        else:
            s, e = 1, n
    except InstrumentError:
        return None
    p = _git(repo, "show", f"{ref}:{path}")
    if p.returncode != 0:
        return None
    text = "\n".join(p.stdout.splitlines()[s - 1:e])
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def verify_receipt(item, repo, ref):
    """Verify a committed receipt: exists at ref, parses, holds before/after
    metrics. Returns (status, detail)."""
    path = item["path"]
    p = _git(repo, "show", f"{ref}:{path}")
    if p.returncode != 0:
        return "UNVERIFIABLE", f"receipt {path} not present at {ref[:12]}"
    try:
        rec = json.loads(p.stdout)
    except json.JSONDecodeError as ex:
        return "UNVERIFIABLE", f"receipt {path} does not parse as JSON: {ex}"
    if not isinstance(rec, dict) or rec.get("receipt_version") != RECEIPT_VERSION:
        return "UNVERIFIABLE", f"receipt {path}: receipt_version must be {RECEIPT_VERSION}"
    metrics = rec.get("metrics")
    if not isinstance(metrics, list) or not metrics:
        return "UNVERIFIABLE", f"receipt {path}: 'metrics' must be a non-empty list"
    good = 0
    for m in metrics:
        if (isinstance(m, dict) and isinstance(m.get("name"), str) and m["name"].strip()
                and "before" in m and "after" in m):
            good += 1
    if good == 0:
        return "UNVERIFIABLE", f"receipt {path}: no metric has before+after values"
    return "VERIFIED", f"receipt {path} holds {good} before/after metric(s) at {ref[:12]}"


def verify_evidence(item, repo, ref):
    """Returns (status, detail). status: VERIFIED | ATTESTED | UNVERIFIABLE."""
    kind = item["kind"]
    if kind in ("command", "url"):
        return "ATTESTED", f"{kind} evidence rests on the grader's word"
    if kind == "sha":
        if _git_ok(repo, "cat-file", "-e", item["sha"]):
            return "VERIFIED", f"object {item['sha']} exists"
        return "UNVERIFIABLE", f"object {item['sha']} not found in repo"
    if kind == "receipt":
        return verify_receipt(item, repo, ref)
    # file / test
    path = item["path"]
    n = _file_line_count(repo, ref, path)
    if n is None:
        return "UNVERIFIABLE", f"{path} not present at {ref[:12]}"
    if kind == "test":
        base = path.split("/")[-1].lower()
        if not (path.startswith("tests/") or "test" in base):
            return "UNVERIFIABLE", f"{path} does not look like a test file"
    if "lines" in item:
        try:
            s, e = _parse_lines(item["lines"], n)
        except InstrumentError as ex:
            return "UNVERIFIABLE", str(ex)
        return "VERIFIED", f"{path}:{s}-{e} of {n} lines at {ref[:12]}"
    return "VERIFIED", f"{path} present at {ref[:12]} ({n} lines)"


# ---------------------------------------------------------------- scoring

def grade_packet(packet, repo, ref):
    """Validate, verify evidence, apply caps, compute the scorecard.

    Returns the scorecard dict. Raises InstrumentError (fail safe) on bad input.
    """
    packet = validate_packet(packet)
    if not _git_ok(repo, "cat-file", "-e", ref):
        raise InstrumentError(f"ref {ref!r} not found in repo {repo}")

    harm = packet["harm_check"]
    if harm["found"]:
        return {
            "packet_version": PACKET_VERSION,
            "change_id": packet["change_id"],
            "title": packet["title"],
            "merge_sha": packet["merge_sha"],
            "grader": packet["grader"],
            "graded_at_utc": datetime.now(timezone.utc).isoformat(),
            "disqualified": True,
            "score": None,
            "verdict": "DISQUALIFIED",
            "harm_note": harm.get("note", ""),
            "judgments": [],
            "mechanical": mechanical_signals(repo, packet["merge_sha"]),
            "why_not_10": "Harm found. A harmful change does not qualify for a score.",
        }

    scored, ledger = [], []
    for j in packet["judgments"]:
        dim = j["dimension"]
        verified = attested = 0
        receipt_only = True  # verified evidence that is ONLY receipts
        for i, item in enumerate(j["evidence"]):
            status, detail = verify_evidence(item, repo, ref)
            ledger.append({
                "dimension": dim, "index": i, "kind": item["kind"],
                "status": status, "detail": detail,
                "citation": item.get("path") or item.get("sha") or item.get("kind"),
                "lines": item.get("lines"),  # for recheck content-drift
            })
            if status == "VERIFIED":
                verified += 1
                if item["kind"] != "receipt":
                    receipt_only = False
            elif status == "ATTESTED":
                attested += 1
        claimed, flags = j["score"], []
        applied = claimed
        if not j["evidence"] and claimed > 3:
            applied, flags = 3.0, ["NO_EVIDENCE_CAP"]
        elif verified == 0 and claimed > 5:
            applied, flags = 5.0, ["UNCITED_CAP"]
        elif receipt_only and verified > 0 and claimed > RECEIPT_SOFT_CAP:
            # In-repo receipts are verified-but-soft: a committed claim is
            # checkable, not independently re-runnable. It carries DELTA up to
            # 8; above that needs harder evidence (tests, runnable checks).
            applied, flags = RECEIPT_SOFT_CAP, ["RECEIPT_SOFT_CAP"]
        scored.append({
            "dimension": dim,
            "claimed": claimed,
            "applied": round(applied, 1),
            "weight": WEIGHTS[dim],
            "verified_evidence": verified,
            "attested_evidence": attested,
            "flags": flags,
            "rationale": j.get("rationale", ""),
        })

    total = round(sum(s["applied"] * s["weight"] for s in scored), 1)
    verdict = next(v for bound, v in VERDICTS if total >= bound)

    weakest = sorted(scored, key=lambda s: s["applied"])[:2]
    why = "; ".join(
        f"{w['dimension']}={w['applied']}"
        + (f" [{','.join(w['flags'])}]" if w["flags"] else "")
        + (f" — {w['rationale']}" if w["rationale"] else "")
        for w in weakest
    )
    flagged = [s for s in scored if s["flags"]]
    if flagged:
        why += " | flags: " + ", ".join(
            f"{s['dimension']}:{','.join(s['flags'])}" for s in flagged
        )

    return {
        "packet_version": PACKET_VERSION,
        "change_id": packet["change_id"],
        "title": packet["title"],
        "merge_sha": packet["merge_sha"],
        "grader": packet["grader"],
        "graded_at_utc": datetime.now(timezone.utc).isoformat(),
        # The durability loop (recheck command): DURABLE is a prediction at
        # grade time; this is when the instrument asks for it to be re-tested.
        "durable_check_due_utc": (
            datetime.now(timezone.utc) + timedelta(days=7)
        ).isoformat(),
        "disqualified": False,
        "score": total,
        "verdict": verdict,
        "judgments": scored,
        "evidence_ledger": ledger,
        "mechanical": mechanical_signals(repo, packet["merge_sha"]),
        "why_not_10": why,
    }


def mechanical_signals(repo, merge_sha):
    """Numbers straight from git — the machine's view of the change.

    Informational only: the score never depends on these. If the diff base
    does not exist (e.g. a root commit), the section reports UNAVAILABLE
    instead of failing the grade — a grader's evidenced judgment still counts.

    For pre-merge branch heads (single-parent, not a merge commit), the true
    change is merge-base(origin/main)..head, not head^1..head — the pilot's
    full run showed ^1 understating branch deltas, so the base is resolved
    that way when origin/main is available.
    """
    base = f"{merge_sha}^1"
    mb = _git(repo, "merge-base", "origin/main", merge_sha)
    if mb.returncode == 0:
        mb_sha = mb.stdout.strip()
        first_parent = _git(repo, "rev-parse", f"{merge_sha}^1").stdout.strip()
        if mb_sha and mb_sha != first_parent:
            base = mb_sha
    stat = _git(repo, "diff", "--numstat", base, merge_sha)
    names = _git(repo, "diff", "--name-status", base, merge_sha)
    if stat.returncode != 0 or names.returncode != 0:
        return {"unavailable": f"cannot diff {base}..{merge_sha}"}
    files, ins, dels, test_files, doc_files = [], 0, 0, 0, 0
    for line in stat.stdout.splitlines():
        a, d, path = line.split("\t")
        files.append(path)
        ins += int(a) if a != "-" else 0
        dels += int(d) if d != "-" else 0
        low = path.lower()
        if path.startswith("tests/") or "/tests/" in path or "test" in low.split("/")[-1]:
            test_files += 1
        if low.endswith((".md", ".rst", ".txt")):
            doc_files += 1
    subj = _git(repo, "log", "-1", "--format=%s", merge_sha).stdout.strip()
    return {
        "merge_subject": subj,
        "files_changed": len(files),
        "files": files,
        "insertions": ins,
        "deletions": dels,
        "test_files": test_files,
        "doc_files": doc_files,
    }


# ---------------------------------------------------------------- pilot

def build_skeleton(repo, merge_sha, pr=None, title=None):
    if not _git_ok(repo, "cat-file", "-e", merge_sha):
        raise InstrumentError(f"merge {merge_sha!r} not found in repo {repo}")
    mech = mechanical_signals(repo, merge_sha)
    if pr is None:
        m = re.search(r"#(\d+)", mech["merge_subject"])
        pr = m.group(1) if m else "?"
    judgments = []
    for dim in DIMENSIONS:
        judgments.append({
            "dimension": dim,
            "score": None,
            "rationale": "",
            "evidence": [],
            "_hint": (
                f"weight {WEIGHTS[dim]:.0%}. Scores above 5 need VERIFIED evidence "
                "(file/sha/test citing real paths at this merge); above 3 needs "
                "some evidence. Fill rationale in plain words."
            ),
        })
    return {
        "packet_version": PACKET_VERSION,
        "change_id": f"PR-{pr}",
        "title": title or mech["merge_subject"],
        "merge_sha": merge_sha,
        "grader": "",
        "harm_check": {"found": False, "note": ""},
        "judgments": judgments,
        "_mechanical_preview": mech,
    }


# ---------------------------------------------------------------- compare

AGREE_BANDS = (
    (1.0, "agree"),          # graders say the same thing
    (2.5, "review"),         # worth a second look
    (float("inf"), "dispute"),  # graders disagree; do not trust either alone
)


def compare_scorecards(a, b):
    """Second-seat comparison of two scorecards for the same change.

    Returns a report dict. Per-dimension |applied_a - applied_b| falls into
    agree / review / dispute bands; verdict agreement is checked separately.
    Disagreement is made visible, not averaged away.
    """
    for key in ("change_id", "score", "verdict", "judgments"):
        if key not in a or key not in b:
            raise InstrumentError(f"compare needs scorecards with {key!r}")
    da = {j["dimension"]: j["applied"] for j in a["judgments"]}
    db = {j["dimension"]: j["applied"] for j in b["judgments"]}
    if set(da) != set(db):
        raise InstrumentError("scorecards cover different dimensions")
    dims = []
    for dim in DIMENSIONS:
        gap = round(abs(da[dim] - db[dim]), 1)
        band = next(band for bound, band in AGREE_BANDS if gap <= bound)
        dims.append({
            "dimension": dim, "seat_a": da[dim], "seat_b": db[dim],
            "gap": gap, "band": band,
        })
    disputes = [d for d in dims if d["band"] == "dispute"]
    reviews = [d for d in dims if d["band"] == "review"]
    verdict_match = a["verdict"] == b["verdict"]
    score_gap = round(abs(a["score"] - b["score"]), 1)
    standing = "TRUST" if not disputes and verdict_match else (
        "REVIEW" if not disputes else "DISPUTE")
    return {
        "change_id": a["change_id"],
        "seat_a": a.get("grader", "?"), "seat_b": b.get("grader", "?"),
        "score_a": a["score"], "score_b": b["score"], "score_gap": score_gap,
        "verdict_a": a["verdict"], "verdict_b": b["verdict"],
        "verdict_match": verdict_match,
        "dimensions": dims,
        "n_agree": sum(1 for d in dims if d["band"] == "agree"),
        "n_review": len(reviews), "n_dispute": len(disputes),
        "standing": standing,
        "note": ("Both seats agree." if standing == "TRUST"
                 else "Disagreement visible — re-grade with a third seat or "
                      "reconcile evidence before trusting this grade."),
    }


# ---------------------------------------------------------------- recheck (durability loop)

def recheck_scorecard(scorecard, repo, ref):
    """Re-run the evidence verification of a scorecard at a LATER ref.

    Turns DURABLE from a prediction into a track record: every cited
    file/test/sha/receipt is checked again. HELD = still verified at the
    later ref; ROTTED = no longer verifiable (moved, deleted, changed beyond
    recognition); NOT_RECHECKABLE = attested evidence (a command someone ran,
    a URL) that no machine can re-run.
    """
    for key in ("change_id", "judgments", "evidence_ledger", "verdict"):
        if key not in scorecard:
            raise InstrumentError(f"recheck needs a scorecard with {key!r}")
    if not _git_ok(repo, "cat-file", "-e", ref):
        raise InstrumentError(f"ref {ref!r} not found in repo {repo}")
    results = []
    for item in scorecard["evidence_ledger"]:
        kind = item["kind"]
        if kind in ("command", "url"):
            results.append({**item, "recheck": "NOT_RECHECKABLE",
                            "recheck_detail": "attested evidence cannot be re-run"})
            continue
        citation = ({"kind": kind, "path": item["citation"]}
                    if kind in ("file", "test", "receipt")
                    else {"kind": kind, "sha": item["citation"]})
        status, detail = verify_evidence(citation, repo, ref)
        state = "HELD" if status == "VERIFIED" else "ROTTED"
        # Content drift: does the cited content still SAY the same thing?
        # Compare the cited line range's hash at grade time vs the later ref.
        # (Regenerated files like brain indexes "rot" exactly this way: the
        # file still exists, but its content is a different stamping.)
        drift = ""
        if state == "HELD" and kind in ("file", "test", "receipt"):
            orig = scorecard.get("merge_sha")
            lines = citation.get("lines")
            if orig:
                h1 = _cited_hash(repo, orig, citation["path"], lines)
                h2 = _cited_hash(repo, ref, citation["path"], lines)
                if h1 and h2:
                    drift = "UNCHANGED" if h1 == h2 else "CHANGED"
        results.append({**item, "recheck": state,
                        "recheck_detail": detail,
                        "content_drift": drift or None})
    per_dim = {}
    for dim in DIMENSIONS:
        items = [r for r in results if r["dimension"] == dim
                 and r["recheck"] != "NOT_RECHECKABLE"]
        if not items:
            per_dim[dim] = "NOT_RECHECKABLE"
        elif all(r["recheck"] == "HELD" for r in items):
            per_dim[dim] = "HELD"
        elif all(r["recheck"] == "ROTTED" for r in items):
            per_dim[dim] = "ROTTED"
        else:
            per_dim[dim] = "MIXED"
    rotted = sum(1 for r in results if r["recheck"] == "ROTTED")
    held = sum(1 for r in results if r["recheck"] == "HELD")
    drifted = sum(1 for r in results if r.get("content_drift") == "CHANGED")
    original_durable = next(
        (j["applied"] for j in scorecard["judgments"] if j["dimension"] == "DURABLE"),
        None)
    return {
        "change_id": scorecard["change_id"],
        "graded_at_utc": scorecard.get("graded_at_utc"),
        "original_verdict": scorecard["verdict"],
        "original_durable": original_durable,
        "rechecked_at_ref": ref,
        "rechecked_utc": datetime.now(timezone.utc).isoformat(),
        "per_dimension": per_dim,
        "held": held, "rotted": rotted, "content_drifted": drifted,
        "items": results,
        "durability_reading": (
            "DURABLE prediction HELD" if per_dim.get("DURABLE") == "HELD"
            and not drifted
            else "DURABLE prediction ROTTED" if per_dim.get("DURABLE") == "ROTTED"
            else "DURABLE prediction partly rotted"),
    }


def receipt_template(change_id):
    return {
        "receipt_version": RECEIPT_VERSION,
        "change_id": change_id,
        "recorded_at": "YYYY-MM-DD",
        "metrics": [
            {"name": "what got better", "before": 0, "after": 1, "unit": "count",
             "how_measured": "command run / file inspected (say exactly)"},
        ],
        "notes": "plain words: what changed, for whom",
    }


# ---------------------------------------------------------------- to-event

MINTABLE_VERDICTS = ("HIGH VALUE", "REAL VALUE")


def _repo_root():
    here = os.path.abspath(__file__)          # .../tools/human_value/instrument.py
    return os.path.dirname(os.path.dirname(os.path.dirname(here)))


def _load_ledger_schema():
    """Import the existing event-ledger schema. Fail safe if unavailable."""
    root = _repo_root()
    if root not in sys.path:
        sys.path.insert(0, root)
    try:
        from tools.human_value import schema
    except ImportError as ex:
        raise InstrumentError(
            f"to-event needs tools/human_value/schema.py from a repo checkout: {ex}"
        )
    return schema


def to_ledger_event(scorecard, recorded_at=None, event_id=None,
                    receipt_ref=None, pr_url=None):
    """Export a REAL VALUE+ scorecard as a schema-valid ledger event.

    Raises InstrumentError (mints NOTHING) when the verdict is THIN, NO VALUE,
    or DISQUALIFIED — the instrument does not manufacture value-credit.
    The minted event is validated against the existing schema.py before return.
    """
    if not isinstance(scorecard, dict):
        raise InstrumentError("scorecard must be a JSON object")
    if scorecard.get("disqualified"):
        raise InstrumentError("DISQUALIFIED scorecard mints no event")
    verdict = scorecard.get("verdict")
    if verdict not in MINTABLE_VERDICTS:
        raise InstrumentError(
            f"verdict {verdict!r} mints no event "
            f"(only {list(MINTABLE_VERDICTS)} do)"
        )
    for key in ("change_id", "score", "why_not_10"):
        if key not in scorecard:
            raise InstrumentError(f"scorecard missing {key!r}")
    try:
        score = _check_score(scorecard["score"], "scorecard score")
    except InstrumentError as ex:
        raise InstrumentError(f"scorecard has unusable score: {ex}")

    schema = _load_ledger_schema()
    day = recorded_at or datetime.now(timezone.utc).date().isoformat()
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", day):
        raise InstrumentError(f"bad date {day!r} (want YYYY-MM-DD)")
    change_id = scorecard["change_id"]
    eid = event_id or f"HV-{day.replace('-', '')}-{change_id.replace('#', '')}"

    evidence = []
    if receipt_ref:
        evidence.append({"kind": "receipt", "ref": receipt_ref})
    if pr_url:
        evidence.append({"kind": "url", "ref": pr_url})
    if not evidence:
        raise InstrumentError("to-event needs at least one evidence pointer "
                              "(--receipt-ref and/or --pr-url)")

    event = {
        "schema_version": "1",
        "event_id": eid,
        "recorded_at": day,
        "value_type": "useful_outcome",
        "value_units": 1,
        "unit_description": (
            f"shipped change graded {verdict} ({score}/10) "
            f"on the human-value rubric"
        ),
        "evidence": evidence,
        "beneficiary": "team",
        # Linear map of the 0-10 rubric score onto the calculus [-10, 10] scale.
        "delta_v_actual": round((score - 5.0) * 2.0, 1),
        "note": (
            f"{scorecard.get('title', '')} | why not 10: "
            f"{scorecard['why_not_10']} | proximal (team-level) value: "
            f"this records an evidenced valuable change, not a directly "
            f"measured human-life improvement."
        ),
    }
    return schema.validate_event(event)


# ---------------------------------------------------------------- CLI

def _print_card(card):
    if card["disqualified"]:
        print(f"{card['change_id']} — DISQUALIFIED (harm found)")
        print(f"  note: {card['harm_note']}")
        return
    print(f"{card['change_id']} — {card['title']}")
    print(f"  score: {card['score']}/10  verdict: {card['verdict']}")
    for j in card["judgments"]:
        flag = f" [{','.join(j['flags'])}]" if j["flags"] else ""
        print(
            f"  {j['dimension']:7s} claimed {j['claimed']:>4} -> applied {j['applied']:>4}"
            f"  (w {j['weight']:.0%}, verified {j['verified_evidence']},"
            f" attested {j['attested_evidence']}){flag}"
        )
    m = card["mechanical"]
    if "unavailable" in m:
        print(f"  mechanical: UNAVAILABLE ({m['unavailable']})")
    else:
        print(
            f"  mechanical: {m['files_changed']} files, +{m['insertions']}/-{m['deletions']},"
            f" {m['test_files']} test files, {m['doc_files']} doc files"
        )
    print(f"  why not 10: {card['why_not_10']}")


def main(argv):
    if len(argv) < 2 or argv[1] not in (
        "score", "pilot", "to-event", "compare", "recheck", "receipt-template"
    ):
        print("usage: instrument.py {score|pilot|to-event|compare|recheck|receipt-template} ...",
              file=sys.stderr)
        return 2
    cmd = argv[1]
    args = dict(zip(argv[2::2], argv[3::2]))
    try:
        if cmd == "score":
            for k in ("--packet", "--repo", "--ref"):
                if k not in args:
                    raise InstrumentError(f"score needs {k}")
            with open(args["--packet"], encoding="utf-8") as f:
                packet = json.load(f)
            card = grade_packet(packet, args["--repo"], args["--ref"])
            _print_card(card)
            if "--out" in args:
                with open(args["--out"], "w", encoding="utf-8") as f:
                    json.dump(card, f, indent=2)
        elif cmd == "pilot":
            for k in ("--merge", "--repo", "--out"):
                if k not in args:
                    raise InstrumentError(f"pilot needs {k}")
            skel = build_skeleton(
                args["--repo"], args["--merge"],
                pr=args.get("--pr"), title=args.get("--title"),
            )
            with open(args["--out"], "w", encoding="utf-8") as f:
                json.dump(skel, f, indent=2)
            print(f"skeleton written to {args['--out']} for {skel['change_id']}")
        elif cmd == "to-event":
            for k in ("--scorecard", "--out"):
                if k not in args:
                    raise InstrumentError(f"to-event needs {k}")
            with open(args["--scorecard"], encoding="utf-8") as f:
                card = json.load(f)
            event = to_ledger_event(
                card,
                recorded_at=args.get("--date"),
                event_id=args.get("--event-id"),
                receipt_ref=args.get("--receipt-ref"),
                pr_url=args.get("--pr-url"),
            )
            with open(args["--out"], "w", encoding="utf-8") as f:
                json.dump(event, f, indent=2)
            print(f"minted {event['event_id']} ({event['value_type']}, "
                  f"delta_v_actual={event['delta_v_actual']}) -> {args['--out']}")
        elif cmd == "compare":
            for k in ("--a", "--b"):
                if k not in args:
                    raise InstrumentError(f"compare needs {k}")
            with open(args["--a"], encoding="utf-8") as f:
                a = json.load(f)
            with open(args["--b"], encoding="utf-8") as f:
                b = json.load(f)
            report = compare_scorecards(a, b)
            print(f"{report['change_id']}: seat {report['seat_a']} "
                  f"({report['score_a']}) vs seat {report['seat_b']} "
                  f"({report['score_b']}), gap {report['score_gap']}")
            print(f"  verdicts: {report['verdict_a']} vs {report['verdict_b']} "
                  f"({'match' if report['verdict_match'] else 'MISMATCH'})")
            for d in report["dimensions"]:
                print(f"  {d['dimension']:7s} {d['seat_a']:>4} vs {d['seat_b']:>4} "
                      f"gap {d['gap']:<4} [{d['band'].upper()}]")
            print(f"  standing: {report['standing']} — {report['note']}")
            if "--out" in args:
                with open(args["--out"], "w", encoding="utf-8") as f:
                    json.dump(report, f, indent=2)
        elif cmd == "recheck":
            for k in ("--scorecard", "--repo", "--ref"):
                if k not in args:
                    raise InstrumentError(f"recheck needs {k}")
            with open(args["--scorecard"], encoding="utf-8") as f:
                card = json.load(f)
            report = recheck_scorecard(card, args["--repo"], args["--ref"])
            print(f"{report['change_id']}: rechecked at {args['--ref'][:12]} "
                  f"(graded {report['graded_at_utc'][:10]})")
            for dim in ("USE", "DELTA", "PROOF", "DURABLE", "CLEAN"):
                print(f"  {dim:7s} {report['per_dimension'][dim]}")
            print(f"  evidence: {report['held']} held / {report['rotted']} rotted / "
                  f"{report['content_drifted']} content-drifted")
            print(f"  reading: {report['durability_reading']}")
            if "--out" in args:
                with open(args["--out"], "w", encoding="utf-8") as f:
                    json.dump(report, f, indent=2)
        elif cmd == "receipt-template":
            cid = args.get("--change-id", "PR-0000")
            tpl = receipt_template(cid)
            print(json.dumps(tpl, indent=2))
            if "--out" in args:
                with open(args["--out"], "w", encoding="utf-8") as f:
                    json.dump(tpl, f, indent=2)
        return 0
    except InstrumentError as ex:
        print(json.dumps({"ok": False, "error": str(ex)}), file=sys.stderr)
        return 2
    except (json.JSONDecodeError, OSError) as ex:
        print(json.dumps({"ok": False, "error": f"input unreadable: {ex}"}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
