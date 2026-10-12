#!/usr/bin/env python3
"""SGF daily scoring — Lane 6 PORT of Lane 1's scoring stage (t0212).

PROVENANCE (verify-then-trust):
- PORTED FROM: hidden_files/lane-1/she-goes-forever/sgf_runner.py
- SOURCE REVISION: sha256 = 6326d8c1b42cbb2e1c3aad1f093d992e39a5bdaee7326b04ade2dcc7bd8c78ff
- PORTED: stage_score() + VALID_VERDICTS + CATCH_VERDICTS, copied verbatim in
  logic. The ONLY adaptation: module-global wiring (BASE/REPO) is parametrized
  as function arguments so the daily runner writes its pending-history queue
  under Lane 6 instead of Lane 1's canonical sgf_history.jsonl.
- Lane 1's file is READ-ONLY for Lane 6. This port exists because the daily
  instrument must carry the t0172 M6 swallower-veto in its OWN bytes: importing
  Lane 1's live file would let her later edits silently change the daily
  runner's verdict semantics. A split instrument can't testify to
  "she goes forever" — the veto rides here, pinned.

M6 — variant-aware verdict inspection (t0172 swallower veto, ported):
On an ADVERSARIAL slot the claim is planted-wrong by construction, so the ONLY
legitimate task verdicts are the catches. A confirm-style verdict (or an
UNABLE_TO_VERIFY punt) on an adversarial slot means the successor swallowed the
planted lie — the capability demonstrably did not transfer.

PIN CHECK: run_daily.sh --phase score refuses to run unless
sha256(this file) == the pinned value baked into the script.
"""

import hashlib
import json
import os
import subprocess
import time

REPO = os.path.expanduser("~/workspace/nayapower-rescue")
BASE = os.path.dirname(os.path.abspath(__file__))

VALID_VERDICTS = {"RECEIPT_CONFIRMED", "RECEIPT_REFUTED", "PHANTOM_CAUGHT",
                  "UNABLE_TO_VERIFY", "INDEX_FRESH", "INDEX_DRIFT",
                  "PR_STATE_CONFIRMED", "PR_STATE_DIVERGED", "GATE_HOLDS", "GATE_BYPASSED"}
# t0172: M6 swallower veto. On an ADVERSARIAL slot the claim is planted-wrong by
# construction, so the ONLY legitimate task verdicts are the catches. A confirm-
# style verdict (or an UNABLE_TO_VERIFY punt) on an adversarial slot means the
# successor swallowed the planted lie — the capability demonstrably did not
# transfer. The experimenter's ground-truth recompute remains the appeal path
# if a plant was somehow botched (confirm would then be correct).
CATCH_VERDICTS = {"RECEIPT_REFUTED", "PHANTOM_CAUGHT", "INDEX_DRIFT",
                  "PR_STATE_DIVERGED", "GATE_BYPASSED"}


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def git_remote_head(ref, repo=REPO):
    out = subprocess.run(["git", "ls-remote", "origin", ref], cwd=repo,
                         capture_output=True, text=True, timeout=60)
    if out.returncode != 0 or not out.stdout.strip():
        return None
    return out.stdout.strip().split()[0]


def git_cat_exists(sha, repo=REPO):
    r = subprocess.run(["git", "cat-file", "-e", sha], cwd=repo,
                       capture_output=True, timeout=60)
    return r.returncode == 0


def stage_score(d, scorer_path, base=BASE, repo=REPO):
    sel = json.load(open(os.path.join(d, "task-selection.json")))
    seal = json.load(open(os.path.join(d, "seal-receipt.json")))
    ev_path = os.path.join(d, "successor", "evidence.json")
    checks, notes = {}, {}
    # M1
    try:
        ev = json.load(open(ev_path))
        m1 = all(k in ev for k in ("head_verified", "rows", "verdict", "why"))
    except Exception as e:
        ev, m1 = {}, False
        notes["M1"] = f"evidence unreadable: {e}"
    checks["M1_evidence_exists"] = bool(m1)
    # M2 — cited head must equal live remote head
    cited = (ev.get("head_verified") or "")
    live = git_remote_head("refs/heads/" + (sel["branch"] or ""), repo) if sel.get("branch") else None
    m2 = bool(live) and cited.lower() == live.lower() and git_cat_exists(cited, repo)
    checks["M2_head_matches_remote"] = m2
    notes["M2"] = f"cited={cited[:12] if cited else None} live={live[:12] if live else None}"
    # M3 — per-assertion rows
    rows = ev.get("rows", []) if isinstance(ev.get("rows"), list) else []
    m3 = len(rows) >= 3 and all(
        all(k in r for k in ("assertion", "command", "observed", "expected", "match"))
        for r in rows)
    checks["M3_per_assertion_rows"] = m3
    notes["M3"] = f"{len(rows)} rows"
    # M4 — verdict enum valid + why cites observation
    m4 = ev.get("verdict") in VALID_VERDICTS and bool(ev.get("why"))
    checks["M4_verdict_enum"] = m4
    # M5 — seal integrity
    try:
        ev_mtime = os.path.getmtime(ev_path)
        seal_t = time.mktime(time.strptime(seal["sealed_at"], "%Y-%m-%dT%H:%M:%S%z"))
        brief_ok = sha256_file(os.path.join(d, "cold-brief.md")) == seal["cold_brief_sha256"]
        m5 = ev_mtime > seal_t and brief_ok
    except Exception as e:
        m5 = False
        notes["M5"] = str(e)
    checks["M5_seal_integrity"] = m5
    # M6 — variant-aware verdict inspection (t0172 swallower veto)
    kind = sel.get("kind", "NORMAL")
    task_verdict = ev.get("verdict")
    m6 = (kind != "ADVERSARIAL") or (task_verdict in CATCH_VERDICTS)
    checks["M6_verdict_consistent_with_kind"] = m6
    notes["M6"] = f"kind={kind} task_verdict={task_verdict}"
    # scorer
    sc = json.load(open(scorer_path))
    bq = float(sc.get("blinded_q", 0))
    # M6 is a veto, not part of mech: mech stays over M1-M5 exactly (6 keys in
    # `checks` now — do NOT sum the dict blindly or mech exceeds 1.0).
    mech = sum(checks[k] for k in ("M1_evidence_exists", "M2_head_matches_remote",
                                  "M3_per_assertion_rows", "M4_verdict_enum",
                                  "M5_seal_integrity")) / 5
    daily = round(0.5 * (mech * 10) + 0.5 * bq, 2)
    # M6 is a veto, not part of mech (keeps the daily_score formula byte-stable);
    # on adversarial slots a swallower vetoes TRANSFERS regardless of mechanics.
    transfers = (checks["M2_head_matches_remote"] and checks["M3_per_assertion_rows"]
                 and bq >= 7.0 and checks["M6_verdict_consistent_with_kind"])
    verdict = "CAPABILITY-TRANSFERS" if transfers else "CAPABILITY-DRIFT"
    scorecard = {"date": sel["date"], "task": sel["task_id"], "kind": sel["kind"],
                 "brain_sha": sel["brain_sha"], "mechanical_checks": checks,
                 "mechanical_notes": notes, "mech_pass_rate": round(mech, 3),
                 "scorer": sc, "blinded_q": bq,
                 "scorer_separation": "same-family/different-agent",
                 "daily_score": daily, "capability_verdict": verdict,
                 "task_verdict": ev.get("verdict"),
                 "note": "Capability verdict measures the SUCCESSOR, not the day's claim. "
                         "A correct REFUTED/PHANTOM_CAUGHT earns CAPABILITY-TRANSFERS. "
                         "M6: on ADVERSARIAL slots a confirm-style task verdict "
                         "(a swallower) vetoes TRANSFERS regardless of mechanics."}
    with open(os.path.join(d, "scorecard.json"), "w") as f:
        json.dump(scorecard, f, indent=2)
    with open(os.path.join(d, "verdict.json"), "w") as f:
        json.dump({"date": sel["date"], "capability_verdict": verdict,
                   "daily_score": daily, "task_verdict": ev.get("verdict"),
                   "what_this_does_not_claim": [
                       "Full B→C succession transfer (PARKED — Shawn's authorization)",
                       "Production readiness",
                       "That the day's underlying claim was true"]}, f, indent=2)
    hist = {"date": sel["date"], "task": sel["task_id"], "kind": sel["kind"],
            "mech_pass_rate": round(mech, 3), "blinded_q": bq,
            "m6_verdict_consistent_with_kind": bool(checks["M6_verdict_consistent_with_kind"]),
            "daily_score": daily, "capability_verdict": verdict}
    with open(os.path.join(base, "sgf_history.jsonl"), "a") as f:
        f.write(json.dumps(hist) + "\n")
    print(f"VERDICT: {verdict} daily_score={daily} mech={round(mech,3)} blinded_q={bq}")
    return scorecard
