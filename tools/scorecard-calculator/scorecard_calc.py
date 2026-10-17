#!/usr/bin/env python3
"""NayaPOWER scorecard calculator v1 — the mechanical judge.

Takes a work artifact (a commit SHA and/or a branch name) plus the BUILDER's
claim set (a packet v1 JSON: per-dimension claimed scores with cited evidence
and rationales) and produces an HONEST scorecard JSON that conforms to
.naya/specifications/NAYA-SCORECARD-RECEIPT-AUTHORITY-V1.schema.json.

What the machine does (everything below is mechanical, no judgment invented):
  1. Resolves the artifact to a SHA and verifies it exists locally (git).
  2. Runs a mechanical harm scan over the change's diff. A hit ->
     DISQUALIFIED (harm is binary; a harmful change gets no score).
  3. Verifies EVERY cited evidence item at the ref:
       file/test/receipt -> the path must exist at the ref (VERIFIED),
       sha               -> the object must exist in the repo (VERIFIED),
       command/url       -> rests on the grader's word (ATTESTED),
       anything missing  -> UNVERIFIABLE (not invented, not scored).
  4. Applies the Human-Value evidence-rule caps mechanically (HUMAN-VALUE.md):
       NO_EVIDENCE_CAP  (>3 with no evidence at all -> 3.0)
       UNCITED_CAP      (>5 with zero verified evidence -> 5.0)
       RECEIPT_SOFT_CAP (>8 resting only on in-repo receipts -> 8.0)
     Each cap is a named deduction tied to the evidence-ledger entries.
  5. Computes the honest 0-10 score (weighted sum, one decimal) and verdict.
  6. Maps the verified five-dimension judgment into the receipt-law frame:
       step1: options "ship" / "do-not-ship"
       step2: four receipt dimensions derived from verified HV judgments:
         value                    = mean(USE, DELTA)  applied
         consequences             = mean(CLEAN, DURABLE) applied
         mission_vision_alignment = USE applied
         situational_awareness    = PROOF applied
       step3: hard gates from mechanical signals (reversible, no_major_damage,
              positive_forward_effect) — no score overrides a failed gate.
       step4: winner = argmax mean; falsifier stated concretely.
       step5: receipt_posted_comment_id must be supplied by the caller —
              a private scorecard is not a gate (fail-closed, exit 2).
  7. Mechanically validates the emitted JSON against the receipt schema
     (hand-rolled, stdlib-only) before writing it. Invalid output is never
     emitted — a number without a valid receipt is a lie with formatting.

What the machine REFUSES to do (unmeasurable = stated, never scored):
  - It never upgrades a score beyond what verified evidence supports.
  - It never attests to things it cannot check (CI green, live production
    effects, human experience). Those go in the `unmeasurable` list.
  - It never invents evidence, citations, or line ranges.
  - The "do-not-ship" null option uses a stated convention (flagged
    NULL_BASELINE): a non-action delivers nothing (value 0), breaks nothing
    (consequences 10), and carries no evidence of mission alignment or
    situational awareness (0 each). Cost of inaction is UNMEASURED and listed.

Usage:
  python3 tools/scorecard-calculator/scorecard_calc.py \
      --repo REPO --sha SHA --packet PACKET.json \
      --receipt-posted-comment-id N [--branch BR] [--out OUT.json] [--judge NAME]

Exit codes: 0 = scorecard emitted (including DISQUALIFIED — a verdict was
reached). 2 = fail-safe: malformed input, unresolvable ref, missing receipt
posting, or invalid output — no scorecard emitted.

Only the standard library is used. Evidence verification shells out to git.
No network. No GitHub API.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone

CALCULATOR = "scorecard-calculator"
CALCULATOR_VERSION = "1.0"

DIMENSIONS = ("USE", "DELTA", "PROOF", "DURABLE", "CLEAN")
WEIGHTS = {"USE": 0.30, "DELTA": 0.25, "PROOF": 0.20, "DURABLE": 0.15, "CLEAN": 0.10}
EVIDENCE_KINDS = ("file", "sha", "test", "command", "url", "receipt")
RECEIPT_VERSION = 1
RECEIPT_SOFT_CAP = 8.0

VERDICTS = (
    (9.0, "HIGH VALUE"),
    (7.0, "REAL VALUE"),
    (5.0, "THIN"),
    (0.0, "NO VALUE"),
)

SHA_RE = re.compile(r"^[0-9a-f]{7,40}$")

# Mechanical harm patterns scanned in the change's diff. A hit disqualifies:
# harm is binary — a harmful change gets no score. The scan is a floor, not a
# ceiling: absence of hits is NOT proof of safety (stated in the output).
HARM_PATTERNS = [
    (re.compile(r"^-(?:diff --git a/)?\.github/workflows/.*", re.M), "DELETED_WORKFLOW",
     "deletes a CI workflow file"),
    (re.compile(r"^-(?:diff --git a/)?kernel/protocol/.*", re.M), "DELETED_GATE",
     "deletes a protocol gate file"),
    (re.compile(r"AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----", re.M),
     "SECRET_MATERIAL", "adds secret-like material to the diff"),
    (re.compile(r"(?im)^\+.*\b(password|api_key|secret|token)\s*[:=]\s*['\"][^'\"]{4,}", re.M),
     "HARDCODED_CREDENTIAL", "adds a hard-coded credential-like assignment"),
]


class CalcError(Exception):
    """Fail-safe: malformed or unverifiable input. Never emits a score."""


# ---------------------------------------------------------------- git helpers

def _git(repo, *args):
    p = subprocess.run(
        ["git", "-C", repo, *args],
        capture_output=True, text=True, timeout=120,
    )
    return p


def _git_ok(repo, *args):
    return _git(repo, *args).returncode == 0


def _file_line_count(repo, ref, path):
    p = _git(repo, "show", f"{ref}:{path}")
    if p.returncode != 0:
        return None
    return len(p.stdout.splitlines())


def _parse_lines(spec, max_lines):
    m = re.fullmatch(r"\s*(\d+)\s*(?:-\s*(\d+)\s*)?", str(spec))
    if not m:
        raise CalcError(f"bad lines spec: {spec!r} (want 'N' or 'N-M')")
    start, end = int(m.group(1)), int(m.group(2) or m.group(1))
    if start < 1 or end < start or end > max_lines:
        raise CalcError(f"lines {spec!r} out of range for file with {max_lines} lines")
    return start, end


# ---------------------------------------------------------------- packet input

def _need(packet, key, what="packet"):
    if key not in packet:
        raise CalcError(f"{what} missing required field: {key!r}")
    return packet[key]


def _check_score(value, where):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise CalcError(f"{where}: score must be a number 0-10, got {value!r}")
    if not (0 <= value <= 10):
        raise CalcError(f"{where}: score {value} out of range 0-10")
    return float(value)


def _normalize_evidence(item, i, dim):
    """Accept the instrument packet shape (path/sha) and the observatory
    scorecard shape (citation). Normalizes to path/sha internally."""
    where = f"judgment {dim} evidence[{i}]"
    if not isinstance(item, dict):
        raise CalcError(f"{where}: must be an object")
    item = dict(item)  # copy; do not mutate caller data
    kind = _need(item, "kind", where)
    if kind not in EVIDENCE_KINDS:
        raise CalcError(f"{where}: unknown kind {kind!r}")
    if kind in ("file", "test", "receipt") and "path" not in item:
        item["path"] = item.get("citation")
    if kind == "sha" and "sha" not in item:
        item["sha"] = item.get("citation")
    if kind in ("file", "test", "receipt"):
        path = item.get("path")
        if not isinstance(path, str) or not path.strip() or path.startswith("/"):
            raise CalcError(f"{where}: bad path {path!r}")
    if kind == "sha":
        sha = item.get("sha")
        if not isinstance(sha, str) or not SHA_RE.match(sha):
            raise CalcError(f"{where}: bad sha {sha!r}")
    if "lines" in item and not isinstance(item["lines"], str):
        raise CalcError(f"{where}: lines must be a string like '12-34'")
    return item


def validate_packet(packet):
    """Strict input validation. Raises CalcError on anything malformed."""
    if not isinstance(packet, dict):
        raise CalcError("packet must be a JSON object")
    if packet.get("packet_version") not in (1,):
        raise CalcError("packet_version must be 1")
    for key in ("change_id", "title", "merge_sha", "grader"):
        v = _need(packet, key)
        if not isinstance(v, str) or not v.strip():
            raise CalcError(f"field {key!r} must be a non-empty string")
    if not SHA_RE.match(packet["merge_sha"]):
        raise CalcError(f"bad merge_sha {packet['merge_sha']!r}")

    harm = packet.get("harm_check")
    if harm is None and "disqualified" in packet:
        harm = {"found": bool(packet["disqualified"]),
                "note": packet.get("harm_note", "")}
    if not isinstance(harm, dict) or not isinstance(harm.get("found"), bool):
        raise CalcError("harm_check must be an object with boolean 'found'")

    judgments = _need(packet, "judgments")
    if not isinstance(judgments, list):
        raise CalcError("judgments must be a list")
    seen = set()
    for j in judgments:
        if not isinstance(j, dict):
            raise CalcError("each judgment must be an object")
        dim = _need(j, "dimension", "judgment")
        if dim not in DIMENSIONS:
            raise CalcError(f"unknown dimension {dim!r}")
        if dim in seen:
            raise CalcError(f"duplicate judgment for dimension {dim!r}")
        seen.add(dim)
        score = j.get("score", j.get("claimed"))
        if score is None:
            raise CalcError(f"judgment {dim}: score/claimed is required")
        j["score"] = _check_score(score, f"judgment {dim}")
        ev = j.get("evidence", [])
        if not isinstance(ev, list):
            raise CalcError(f"judgment {dim}: evidence must be a list")
        j["evidence"] = [_normalize_evidence(e, i, dim) for i, e in enumerate(ev)]
    missing = set(DIMENSIONS) - seen
    if missing:
        raise CalcError(f"packet missing judgments for: {sorted(missing)}")
    packet["harm_check"] = harm
    return packet


# ---------------------------------------------------------------- evidence verification

def verify_receipt(item, repo, ref):
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
    good = sum(1 for m in metrics
               if isinstance(m, dict) and isinstance(m.get("name"), str)
               and m["name"].strip() and "before" in m and "after" in m)
    if good == 0:
        return "UNVERIFIABLE", f"receipt {path}: no metric has before+after values"
    return "VERIFIED", f"receipt {path} holds {good} before/after metric(s) at {ref[:12]}"


def verify_evidence(item, repo, ref):
    """Returns (status, detail). VERIFIED | ATTESTED | UNVERIFIABLE.

    Attested evidence (command, url) rests on the grader's word — the machine
    does not upgrade it to verified. It counts as evidence for the <=5 band
    but never carries a score above 5 by itself (UNCITED_CAP).
    """
    kind = item["kind"]
    if kind in ("command", "url"):
        return "ATTESTED", f"{kind} evidence rests on the grader's word"
    if kind == "sha":
        if _git_ok(repo, "cat-file", "-e", item["sha"]):
            return "VERIFIED", f"object {item['sha']} exists"
        return "UNVERIFIABLE", f"object {item['sha']} not found in repo"
    if kind == "receipt":
        return verify_receipt(item, repo, ref)
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
        except CalcError as ex:
            return "UNVERIFIABLE", str(ex)
        return "VERIFIED", f"{path}:{s}-{e} of {n} lines at {ref[:12]}"
    return "VERIFIED", f"{path} present at {ref[:12]} ({n} lines)"


def _evidence_citation(item):
    if item["kind"] in ("file", "test", "receipt"):
        return item["path"]
    if item["kind"] == "sha":
        return item["sha"]
    return item["kind"]  # command / url — the grader's word, no address


# ---------------------------------------------------------------- harm scan + diff signals

def _diff_base(repo, sha):
    """Same base rules as the HV instrument's mechanical_signals:
    merge commits diff first-parent..merge; single-parent heads diff
    merge-base(origin/main)..head, guarded against the main-push collapse."""
    first = _git(repo, "rev-parse", f"{sha}^1")
    if first.returncode != 0:
        raise CalcError(f"no first parent for {sha[:12]} (shallow checkout or root)")
    first_sha = first.stdout.strip()
    base = f"{sha}^1"
    if _git_ok(repo, "rev-parse", "--verify", f"{sha}^2"):
        return base, first_sha
    mb = _git(repo, "merge-base", "origin/main", sha)
    if mb.returncode == 0:
        mb_sha = mb.stdout.strip()
        if mb_sha and mb_sha != sha and mb_sha != first_sha:
            return mb_sha, first_sha
    return base, first_sha


def mechanical_signals(repo, sha):
    base, _ = _diff_base(repo, sha)
    stat = _git(repo, "diff", "--numstat", base, sha)
    names = _git(repo, "diff", "--name-status", base, sha)
    if stat.returncode != 0 or names.returncode != 0:
        raise CalcError(f"cannot diff {base}..{sha}")
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
    subj = _git(repo, "log", "-1", "--format=%s", sha).stdout.strip()
    diff_text = _git(repo, "diff", base, sha, "--", ".").stdout
    return {
        "merge_subject": subj,
        "diff_base": base,
        "files_changed": len(files),
        "files": files,
        "insertions": ins,
        "deletions": dels,
        "test_files": test_files,
        "doc_files": doc_files,
        "diff_text": diff_text,
    }


def harm_scan(mech):
    """Binary harm gate over the diff. Returns (found, hits).

    Hits are named evidence (pattern id + description). Absence of hits is a
    floor, not a ceiling — the output states the method's limits.
    """
    hits = []
    for pattern, pid, desc in HARM_PATTERNS:
        m = pattern.search(mech["diff_text"])
        if m:
            hits.append({
                "pattern": pid,
                "description": desc,
                "matched": m.group(0)[:120],
            })
    return (len(hits) > 0), hits


# ---------------------------------------------------------------- scoring

def _band(score):
    return next(v for bound, v in VERDICTS if score >= bound)


def grade(packet, repo, ref):
    """Verify evidence, apply caps, compute honest scorecard (not the receipt
    frame — that comes later). Returns (judgments, ledger, score, verdict)."""
    scored, ledger = [], []
    for j in packet["judgments"]:
        dim = j["dimension"]
        verified = attested = 0
        receipt_only = True
        ver_items, att_items, unv_items = [], [], []
        for i, item in enumerate(j["evidence"]):
            status, detail = verify_evidence(item, repo, ref)
            citation = _evidence_citation(item)
            ledger.append({
                "dimension": dim, "index": i, "kind": item["kind"],
                "status": status, "detail": detail, "citation": citation,
                "lines": item.get("lines"),
            })
            if status == "VERIFIED":
                verified += 1
                ver_items.append(citation)
                if item["kind"] != "receipt":
                    receipt_only = False
            elif status == "ATTESTED":
                attested += 1
                att_items.append(citation)
            else:
                unv_items.append(citation)
        claimed = j["score"]
        applied, flags, deductions = claimed, [], []
        if not j["evidence"] and claimed > 3:
            applied, flags = 3.0, ["NO_EVIDENCE_CAP"]
            deductions.append({
                "amount": round(claimed - 3.0, 1),
                "rule": "NO_EVIDENCE_CAP",
                "reason": f"{dim}: score above 3 with no evidence at all — "
                          f"nothing cited, nothing checkable.",
                "evidence": [],
            })
        elif verified == 0 and claimed > 5:
            applied, flags = 5.0, ["UNCITED_CAP"]
            deductions.append({
                "amount": round(claimed - 5.0, 1),
                "rule": "UNCITED_CAP",
                "reason": (f"{dim}: score above 5 with zero verified evidence "
                           f"({attested} attested, {len(unv_items)} unverifiable) — "
                           f"a score above 5 must cite something the machine "
                           f"can check at the ref."),
                "evidence": att_items + unv_items,
            })
        elif receipt_only and verified > 0 and claimed > RECEIPT_SOFT_CAP:
            applied, flags = RECEIPT_SOFT_CAP, ["RECEIPT_SOFT_CAP"]
            deductions.append({
                "amount": round(claimed - RECEIPT_SOFT_CAP, 1),
                "rule": "RECEIPT_SOFT_CAP",
                "reason": (f"{dim}: verified evidence is receipts only — a committed "
                           f"claim is checkable, not independently re-runnable. "
                           f"Carries the judgment to 8.0, no higher."),
                "evidence": ver_items,
            })
        if unv_items and not flags:
            # Evidence was cited but does not check out — the cap rules already
            # bound the score; name the dead citations as a deduction of 0 so
            # the builder sees exactly what failed, without double-penalizing.
            deductions.append({
                "amount": 0.0,
                "rule": "DEAD_CITATION",
                "reason": (f"{dim}: cited evidence does not verify at the ref — "
                           f"named so the builder can fix the citation; the "
                           f"evidence-rule caps above already bound the score."),
                "evidence": unv_items,
            })
        scored.append({
            "dimension": dim,
            "claimed": claimed,
            "applied": round(applied, 1),
            "weight": WEIGHTS[dim],
            "verified_evidence": verified,
            "attested_evidence": attested,
            "flags": flags,
            "deductions": deductions,
            "rationale": j.get("rationale", ""),
        })
    total = round(sum(s["applied"] * s["weight"] for s in scored), 1)
    return scored, ledger, total, _band(total)


# ---------------------------------------------------------------- receipt frame

def _receipt_scores(scored):
    """Map verified HV judgments onto the receipt law's four dimensions.

    Mapping (documented, uniform, no per-change judgment):
      value                    = mean(USE, DELTA)   applied — what it delivered
      consequences             = mean(CLEAN, DURABLE) applied — how it landed
      mission_vision_alignment = USE applied — real use is mission alignment
      situational_awareness    = PROOF applied — checkable claims know their limits
    """
    a = {s["dimension"]: s["applied"] for s in scored}
    ship = {
        "value": round((a["USE"] + a["DELTA"]) / 2, 1),
        "consequences": round((a["CLEAN"] + a["DURABLE"]) / 2, 1),
        "mission_vision_alignment": round(a["USE"], 1),
        "situational_awareness": round(a["PROOF"], 1),
    }
    # The null option: stated convention, flagged NULL_BASELINE. A non-action
    # delivers nothing (0), breaks nothing (10), and carries no evidence of
    # mission alignment or situational awareness (0). Cost of inaction is
    # UNMEASURED — listed, never scored.
    null = {
        "value": 0.0,
        "consequences": 10.0,
        "mission_vision_alignment": 0.0,
        "situational_awareness": 0.0,
    }
    return ship, null


def build_scorecard(packet, repo, ref, receipt_posted_comment_id, judge_name):
    """Full pipeline: verify, score, frame as a receipt-law scorecard."""
    if not isinstance(receipt_posted_comment_id, int) or isinstance(
            receipt_posted_comment_id, bool):
        raise CalcError(
            "receipt_posted_comment_id must be an integer board-comment id — "
            "a private scorecard is not a gate (fail-closed)")
    if not _git_ok(repo, "cat-file", "-e", ref):
        raise CalcError(f"ref {ref!r} not found in repo {repo}")

    mech_full = mechanical_signals(repo, ref)
    mech = {k: v for k, v in mech_full.items() if k != "diff_text"}

    graded_at = datetime.now(timezone.utc).isoformat()
    decided_by = f"{CALCULATOR}/{CALCULATOR_VERSION} (mechanical judge" + \
        (f"; {judge_name}" if judge_name else "") + \
        f"; input packet by {packet['grader']})"

    harm_hits = []
    if packet["harm_check"]["found"]:
        harm_hits.append({
            "pattern": "BUILDER_ATTESTED",
            "description": "the builder's own packet declares harm",
            "matched": packet["harm_check"].get("note", "")[:120],
        })
    scan_found, scan_hits = harm_scan(mech_full)
    harm_hits.extend(scan_hits)

    unmeasurable = [
        "CI/test-run outcome: the machine did not run the change's tests and "
        "did not query CI — a test file's presence is verified, its passing is not.",
        "Live production effect: DELTA claims about live gates or real users "
        "rest on attested evidence (the grader's word), never machine-verified.",
        "Human experience: whether a real someone actually benefited is not "
        "machine-measurable in v1 — the HV instrument states this limit too.",
        "Cost of inaction: the null option's score does not account for what "
        "not shipping costs — stated, not scored.",
        "Harm completeness: the diff scan is a floor, not a ceiling — absence "
        "of pattern hits is not proof of safety.",
    ]

    if harm_hits:
        scored, ledger, total, verdict = [], [], None, "DISQUALIFIED"
    else:
        scored, ledger, total, verdict = grade(packet, repo, ref)

    weakest = sorted(scored, key=lambda s: s["applied"])[:2] if scored else []
    why = "; ".join(
        f"{w['dimension']}={w['applied']}"
        + (f" [{','.join(w['flags'])}]" if w["flags"] else "")
        + (f" — {w['rationale']}" if w["rationale"] else "")
        for w in weakest
    )
    flagged = [s for s in scored if s["flags"]]
    if flagged:
        why += " | flags: " + ", ".join(
            f"{s['dimension']}:{','.join(s['flags'])}" for s in flagged)

    if verdict == "DISQUALIFIED":
        why = ("Harm found. A harmful change does not qualify for a score. Hits: "
               + "; ".join(f"{h['pattern']}: {h['description']}" for h in harm_hits))
        card = {
            "packet_version": 1,
            "change_id": packet["change_id"],
            "title": packet["title"],
            "merge_sha": ref,
            "calculator": f"{CALCULATOR}/{CALCULATOR_VERSION}",
            "graded_at_utc": graded_at,
            "disqualified": True,
            "score": None,
            "verdict": "DISQUALIFIED",
            "harm": {"method": "builder attestation + mechanical diff scan "
                               f"({len(HARM_PATTERNS)} patterns)",
                     "hits": harm_hits},
            "judgments": [],
            "evidence_ledger": ledger,
            "mechanical": mech,
            "unmeasurable": unmeasurable,
            "why_not_10": why,
        }
        return card

    ship, null = _receipt_scores(scored)
    ship_mean = round(sum(ship.values()) / 4, 2)
    null_mean = round(sum(null.values()) / 4, 2)
    winner = "ship" if ship_mean >= null_mean else "do-not-ship"

    weakest_dim = weakest[0]["dimension"] if weakest else "USE"
    falsifier = (
        f"For {packet['change_id']}: a re-verification at the merge ref showing "
        f"the cited {weakest_dim} evidence does not exist or does not say what "
        f"is claimed, or CI evidence the change broke a previously green gate."
    )
    strongest_alt_summary = (
        "Do not ship: keep main exactly as-is and avoid unknown regressions. "
        f"Costs the delivered value the calculator scored at {ship['value']}."
        if winner == "ship" else
        f"Ship {packet['change_id']}: accept the scored value "
        f"({ship['value']}) against the regression risk the evidence shows."
    )

    # Hard gates — mechanical proxies, stated as such:
    reversible = not any(
        re.search(pat, mech_full["diff_text"], re.M)
        for pat in (r"(?im)^\+.*drop\s+table", r"(?im)^\+.*delete\s+from\s+\w+\s+where\s+1\s*=\s*1",
                    r"(?im)^\+.*rm\s+-rf\s+/", r"(?im)^\+.*DROP\s+DATABASE")
    )
    no_major_damage = True  # harm scan already cleared; CLEAN<5 would have been disqualified-adjacent
    positive_forward_effect = total >= 5.0  # THIN or better = the rubric's "numbers moved up"

    per_area = {}
    for s in scored:
        per_area[s["dimension"]] = {
            "claimed": s["claimed"],
            "applied": s["applied"],
            "weight": s["weight"],
            "verified_evidence": s["verified_evidence"],
            "attested_evidence": s["attested_evidence"],
            "flags": s["flags"],
            "deductions": s["deductions"],
            "rationale": s["rationale"],
        }

    card = {
        # --- receipt-law frame (NAYA-SCORECARD-RECEIPT-AUTHORITY-V1) ---
        "scope_target": packet["change_id"],
        "scope_action": "learning_lock_in",
        "decided_at": graded_at,
        "decided_by": decided_by,
        "promotion_option_id": winner,
        "step1_enumerate": {"options": [{"id": "ship"}, {"id": "do-not-ship"}]},
        "step2_score": {
            "scores": {
                "ship": dict(ship),
                "do-not-ship": dict(null),
            },
            "null_baseline_convention": (
                "do-not-ship scores are a stated convention, flagged "
                "NULL_BASELINE: a non-action delivers nothing (value 0), "
                "breaks nothing (consequences 10), and carries no evidence of "
                "mission alignment or situational awareness (0). Cost of "
                "inaction is UNMEASURED — listed, never scored."
            ),
            "dimension_mapping": (
                "value=mean(USE,DELTA); consequences=mean(CLEAN,DURABLE); "
                "mission_vision_alignment=USE; situational_awareness=PROOF — "
                "all from mechanically verified applied scores."
            ),
            "ship_mean": ship_mean,
            "do_not_ship_mean": null_mean,
        },
        "step3_gate": {
            "reversible": reversible,
            "no_major_damage": no_major_damage,
            "positive_forward_effect": positive_forward_effect,
            "gate_method": ("mechanical proxies: reversible=diff shows no destructive "
                            "DDL/rm patterns; no_major_damage=harm scan clear; "
                            "positive_forward_effect=honest score >= 5.0. "
                            "A failed gate overrides any score."),
        },
        "step4_decide": {
            "winner": winner,
            "strongest_alternative": {"summary": strongest_alt_summary},
            "falsifier": falsifier,
        },
        "step5_receipt": {"receipt_posted_comment_id": receipt_posted_comment_id},
        # --- honest-score sidecar (additionalProperties: true) ---
        "packet_version": 1,
        "change_id": packet["change_id"],
        "title": packet["title"],
        "merge_sha": ref,
        "calculator": f"{CALCULATOR}/{CALCULATOR_VERSION}",
        "graded_at_utc": graded_at,
        "durable_check_due_utc": (
            datetime.now(timezone.utc).isoformat()
        ),
        "disqualified": False,
        "score": total,
        "verdict": verdict,
        "harm": {"method": ("builder attestation + mechanical diff scan "
                            f"({len(HARM_PATTERNS)} patterns)"),
                 "hits": harm_hits},
        "judgments": scored,
        "per_area": per_area,
        "evidence_ledger": ledger,
        "mechanical": mech,
        "unmeasurable": unmeasurable,
        "why_not_10": why,
    }
    return card


# ---------------------------------------------------------------- schema validation (hand-rolled, stdlib-only)

def _is_num(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def validate_receipt(card):
    """Mechanical check of the receipt-law frame. Returns a list of errors
    (empty = valid). Mirrors NAYA-SCORECARD-RECEIPT-AUTHORITY-V1."""
    errs = []
    if not isinstance(card, dict):
        return ["card must be a JSON object"]
    if card.get("disqualified") is True:
        return []  # disqualified cards carry no receipt authority by design

    def req(key, types, check=None):
        v = card.get(key)
        if v is None:
            errs.append(f"missing required field {key!r}")
            return None
        if not isinstance(v, types):
            errs.append(f"{key!r} must be {types}, got {type(v).__name__}")
            return None
        if check:
            errs.extend(check(key, v))
        return v

    def nonempty_str(key, v):
        return [] if (isinstance(v, str) and v.strip()) else [f"{key!r} must be a non-empty string"]

    req("scope_target", str, lambda k, v: nonempty_str(k, v))
    act = req("scope_action", str)
    if act is not None and act != "learning_lock_in":
        errs.append("scope_action must be 'learning_lock_in'")
    ts = req("decided_at", str)
    if ts is not None:
        try:
            datetime.fromisoformat(ts)
        except ValueError:
            errs.append("decided_at must be ISO-8601 date-time")
    req("decided_by", str, lambda k, v: nonempty_str(k, v))
    req("promotion_option_id", str, lambda k, v: nonempty_str(k, v))

    s1 = req("step1_enumerate", dict)
    opt_ids = []
    if s1 is not None:
        opts = s1.get("options")
        if not isinstance(opts, list) or len(opts) < 2:
            errs.append("step1_enumerate.options must be a list of >= 2")
        else:
            for o in opts:
                if not isinstance(o, dict) or not o.get("id") or not str(o["id"]).strip():
                    errs.append("step1_enumerate.options[*] must have non-empty id")
                else:
                    opt_ids.append(str(o["id"]))

    s2 = req("step2_score", dict)
    receipt_dims = ("value", "consequences", "mission_vision_alignment",
                    "situational_awareness")
    means = {}
    if s2 is not None:
        scores = s2.get("scores")
        if not isinstance(scores, dict):
            errs.append("step2_score.scores must be an object keyed by option id")
        else:
            for oid in opt_ids:
                sc = scores.get(oid)
                if not isinstance(sc, dict):
                    errs.append(f"step2_score.scores[{oid!r}] missing")
                    continue
                for d in receipt_dims:
                    v = sc.get(d)
                    if not _is_num(v) or not (0 <= v <= 10):
                        errs.append(f"step2_score.scores[{oid}][{d}] must be 0-10 number")
                if all(_is_num(sc.get(d)) for d in receipt_dims):
                    means[oid] = sum(sc[d] for d in receipt_dims) / 4

    s3 = req("step3_gate", dict)
    if s3 is not None:
        for g in ("reversible", "no_major_damage", "positive_forward_effect"):
            if s3.get(g) is not True:
                errs.append(f"step3_gate.{g} must be true (hard stop — no score overrides it)")

    s4 = req("step4_decide", dict)
    if s4 is not None:
        winner = s4.get("winner")
        if not winner or not str(winner).strip():
            errs.append("step4_decide.winner must be a non-empty string")
        elif opt_ids and winner not in opt_ids:
            errs.append(f"step4_decide.winner {winner!r} not among enumerated options")
        sa = s4.get("strongest_alternative")
        if not isinstance(sa, dict) or not str(sa.get("summary", "")).strip():
            errs.append("step4_decide.strongest_alternative.summary required")
        fal = s4.get("falsifier", "")
        if not isinstance(fal, str) or len(fal) < 20:
            errs.append("step4_decide.falsifier must be >= 20 chars")
        poi = card.get("promotion_option_id")
        if winner and poi and winner != poi:
            errs.append("promotion_option_id must equal step4_decide.winner")

    s5 = req("step5_receipt", dict)
    if s5 is not None:
        cid = s5.get("receipt_posted_comment_id")
        if not isinstance(cid, int) or isinstance(cid, bool):
            errs.append("step5_receipt.receipt_posted_comment_id must be an integer")

    if means and card.get("promotion_option_id"):
        best = max(means, key=lambda k: means[k])
        if card["promotion_option_id"] != best:
            errs.append(f"promotion_option_id {card['promotion_option_id']!r} is not "
                        f"the highest-mean option ({best!r} at {means[best]:.2f})")
    return errs


# ---------------------------------------------------------------- CLI

def main(argv):
    ap = argparse.ArgumentParser(description="NayaPOWER scorecard calculator v1 — the mechanical judge")
    ap.add_argument("--repo", required=True, help="Repo path (local git)")
    ap.add_argument("--sha", help="Work artifact commit SHA (40 hex ok, 7+ accepted)")
    ap.add_argument("--branch", help="Work artifact branch name (alternative to --sha)")
    ap.add_argument("--packet", required=True, help="Builder claim-set packet JSON (path)")
    ap.add_argument("--receipt-posted-comment-id", required=True, type=int,
                    help="Board comment id where the scorecard receipt was posted")
    ap.add_argument("--out", help="Write scorecard JSON here (default: stdout)")
    ap.add_argument("--judge", default="", help="Seat/agent name invoking the calculator")
    args = ap.parse_args(argv)

    try:
        if not args.sha and not args.branch:
            raise CalcError("one of --sha or --branch is required")
        with open(args.packet, "r", encoding="utf-8") as fh:
            packet = json.load(fh)
        packet = validate_packet(packet)

        if args.sha:
            if not SHA_RE.match(args.sha):
                raise CalcError(f"bad --sha {args.sha!r}")
            ref = _git(args.repo, "rev-parse", "--verify", args.sha).stdout.strip()
        else:
            ref = _git(args.repo, "rev-parse", "--verify", args.branch).stdout.strip()
        if not ref:
            raise CalcError("could not resolve artifact to a SHA")

        card = build_scorecard(packet, args.repo, ref,
                               args.receipt_posted_comment_id, args.judge)
        errs = validate_receipt(card)
        if errs:
            raise CalcError("emitted card failed receipt-schema validation: "
                            + "; ".join(errs))
    except CalcError as ex:
        print(json.dumps({"verdict": "INPUT_ERROR", "reason": str(ex)}))
        return 2
    except (OSError, json.JSONDecodeError) as ex:
        print(json.dumps({"verdict": "INPUT_ERROR", "reason": f"input read failed: {ex}"}))
        return 2

    out = json.dumps(card, indent=2)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(out + "\n")
    else:
        print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
