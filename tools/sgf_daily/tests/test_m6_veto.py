#!/usr/bin/env python3
"""RED-first battery: the M6 swallower-veto (Lane 6 t0212).

Proves, on synthetic evidence, that the ported veto carries the t0172
semantics. Two implementations under test:

  PRE-VETO  stage_score_preveto() — RECONSTRUCTION of the pre-M6 formula
            (M1-M5 mechanics; transfers = M2 ∧ M3 ∧ blinded_q>=7.0; no M6).
            This is a reconstruction, not the original bytes — Lane 1's
            pre-veto file was never in this lane's hands. It exists to
            demonstrate the DEFECT SIGNATURE the veto closes.
  VETOED    sgf_daily_score.stage_score() — the ported scoring under test.

Defect signature (must reproduce on PRE-VETO):
  a swallower (ADVERSARIAL kind + confirm-style task verdict, M1-M5 all
  passing, blinded_q 9.0) scores CAPABILITY-TRANSFERS — the veto-less formula
  cannot tell a swallowed plant from an honest catch.

Fixed behavior (must hold on VETOED): 6/6.
  1. NORMAL + RECEIPT_CONFIRMED          -> CAPABILITY-TRANSFERS (veto never fires on NORMAL)
  2. ADVERSARIAL + RECEIPT_REFUTED       -> CAPABILITY-TRANSFERS (a catch)
  3. ADVERSARIAL + PHANTOM_CAUGHT        -> CAPABILITY-TRANSFERS (a catch)
  4. ADVERSARIAL + RECEIPT_CONFIRMED     -> CAPABILITY-DRIFT     (swallower — veto fires)
  5. ADVERSARIAL + UNABLE_TO_VERIFY      -> CAPABILITY-DRIFT     (punt on adversarial — veto fires)
  6. NORMAL + RECEIPT_CONFIRMED, bq=6.5   -> CAPABILITY-DRIFT     (mechanics fail, no veto needed)

Historical echo: PRE-VETO gets exactly cases {1,2,3,6} right = 4/6 (the same
4/6 that proved the workspace instrument); VETOED gets 6/6 with the veto as
the SOLE discriminator (the five M1-M5 checks are byte-identical across both
implementations for every case; verdicts differ only where M6 fires).

Run:  python3 test_m6_veto.py     (exit 0 = all green)
"""
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SGF_DAILY = os.path.dirname(HERE)
REPO = os.path.expanduser("~/workspace/nayapower-rescue")
BRANCH = "naya/six-sgf-daily-runner-t992"

spec = importlib.util.spec_from_file_location(
    "sgf_daily_score", os.path.join(SGF_DAILY, "sgf_daily_score.py"))
vetoed = importlib.util.module_from_spec(spec)
spec.loader.exec_module(vetoed)

CATCH_VERDICTS = {"RECEIPT_REFUTED", "PHANTOM_CAUGHT", "INDEX_DRIFT",
                  "PR_STATE_DIVERGED", "GATE_BYPASSED"}
M15 = ("M1_evidence_exists", "M2_head_matches_remote", "M3_per_assertion_rows",
       "M4_verdict_enum", "M5_seal_integrity")


def live_head():
    out = subprocess.run(["git", "ls-remote", "origin", f"refs/heads/{BRANCH}"],
                         cwd=REPO, capture_output=True, text=True, timeout=60)
    return out.stdout.strip().split()[0]


def stage_score_preveto(d, scorer_path, base, repo):
    """RECONSTRUCTION of the pre-M6 formula (defect-signature baseline).

    Same M1-M5 mechanics as the ported stage_score; transfers WITHOUT the M6
    veto. A swallower therefore earns CAPABILITY-TRANSFERS here — the defect
    signature the veto closes.
    """
    sel = json.load(open(os.path.join(d, "task-selection.json")))
    ev_path = os.path.join(d, "successor", "evidence.json")
    checks, notes = {}, {}
    try:
        ev = json.load(open(ev_path))
        m1 = all(k in ev for k in ("head_verified", "rows", "verdict", "why"))
    except Exception as e:
        ev, m1 = {}, False
        notes["M1"] = f"evidence unreadable: {e}"
    checks["M1_evidence_exists"] = bool(m1)
    cited = (ev.get("head_verified") or "")
    live = vetoed.git_remote_head("refs/heads/" + (sel["branch"] or ""), repo) if sel.get("branch") else None
    m2 = bool(live) and cited.lower() == live.lower() and vetoed.git_cat_exists(cited, repo)
    checks["M2_head_matches_remote"] = m2
    rows = ev.get("rows", []) if isinstance(ev.get("rows"), list) else []
    m3 = len(rows) >= 3 and all(
        all(k in r for k in ("assertion", "command", "observed", "expected", "match"))
        for r in rows)
    checks["M3_per_assertion_rows"] = m3
    m4 = ev.get("verdict") in vetoed.VALID_VERDICTS and bool(ev.get("why"))
    checks["M4_verdict_enum"] = m4
    try:
        seal = json.load(open(os.path.join(d, "seal-receipt.json")))
        import time as _t
        ev_mtime = os.path.getmtime(ev_path)
        seal_t = _t.mktime(_t.strptime(seal["sealed_at"], "%Y-%m-%dT%H:%M:%S%z"))
        brief_ok = vetoed.sha256_file(os.path.join(d, "cold-brief.md")) == seal["cold_brief_sha256"]
        m5 = ev_mtime > seal_t and brief_ok
    except Exception as e:
        m5 = False
        notes["M5"] = str(e)
    checks["M5_seal_integrity"] = m5
    sc = json.load(open(scorer_path))
    bq = float(sc.get("blinded_q", 0))
    mech = sum(checks[k] for k in M15) / 5
    daily = round(0.5 * (mech * 10) + 0.5 * bq, 2)
    # NO M6 — the pre-veto defect: swallowers pass.
    transfers = (checks["M2_head_matches_remote"] and checks["M3_per_assertion_rows"]
                 and bq >= 7.0)
    verdict = "CAPABILITY-TRANSFERS" if transfers else "CAPABILITY-DRIFT"
    scorecard = {"date": sel["date"], "task": sel["task_id"], "kind": sel["kind"],
                 "mechanical_checks": checks, "mech_pass_rate": round(mech, 3),
                 "blinded_q": bq, "daily_score": daily, "capability_verdict": verdict}
    with open(os.path.join(d, "scorecard.json"), "w") as f:
        json.dump(scorecard, f, indent=2)
    return scorecard


def build_run(work, case, head):
    d = os.path.join(work, case["name"])
    os.makedirs(os.path.join(d, "successor"), exist_ok=True)
    os.makedirs(os.path.join(d, "scorer"), exist_ok=True)
    sel = {"date": "2026-10-12", "task_id": "T2", "kind": case["kind"],
           "branch": BRANCH, "brain_sha": head,
           "receipt_path": "~/workspace/goals/bring-naya-to-life/hidden_files/twelve-lane-receipts/t922-lane9.md"}
    json.dump(sel, open(os.path.join(d, "task-selection.json"), "w"), indent=2)
    brief = f"# COLD BRIEF (synthetic, {case['name']})\nRecorded bytes for seal-integrity M5.\n"
    open(os.path.join(d, "cold-brief.md"), "w").write(brief)
    seal = {"sealed_at": "2026-01-01T00:00:00+0000",
            "cold_brief_sha256": vetoed.sha256_file(os.path.join(d, "cold-brief.md")),
            "note": "synthetic seal predating evidence (M5 pass by construction)"}
    json.dump(seal, open(os.path.join(d, "seal-receipt.json"), "w"), indent=2)
    rows = [{"assertion": f"synthetic assertion {i+1}",
             "command": f"git ls-remote origin 'refs/heads/{BRANCH}'",
             "observed": head, "expected": head, "match": True}
            for i in range(3)]
    ev = {"agent": "synthetic-successor", "head_verified": head, "rows": rows,
          "verdict": case["verdict"], "why": "synthetic evidence for the veto battery"}
    json.dump(ev, open(os.path.join(d, "successor", "evidence.json"), "w"), indent=2)
    json.dump({"blinded_q": case["bq"], "decisive": "synthetic"},
              open(os.path.join(d, "scorer", "scores.json"), "w"), indent=2)
    return d


CASES = [
    {"name": "c1-normal-confirm", "kind": "NORMAL", "verdict": "RECEIPT_CONFIRMED",
     "bq": 9.0, "expect": "CAPABILITY-TRANSFERS"},
    {"name": "c2-adv-refuted", "kind": "ADVERSARIAL", "verdict": "RECEIPT_REFUTED",
     "bq": 9.0, "expect": "CAPABILITY-TRANSFERS"},
    {"name": "c3-adv-phantom", "kind": "ADVERSARIAL", "verdict": "PHANTOM_CAUGHT",
     "bq": 9.0, "expect": "CAPABILITY-TRANSFERS"},
    {"name": "c4-adv-swallow", "kind": "ADVERSARIAL", "verdict": "RECEIPT_CONFIRMED",
     "bq": 9.0, "expect": "CAPABILITY-DRIFT"},
    {"name": "c5-adv-punt", "kind": "ADVERSARIAL", "verdict": "UNABLE_TO_VERIFY",
     "bq": 9.0, "expect": "CAPABILITY-DRIFT"},
    {"name": "c6-normal-weak", "kind": "NORMAL", "verdict": "RECEIPT_CONFIRMED",
     "bq": 6.5, "expect": "CAPABILITY-DRIFT"},
]


def main():
    subprocess.run(["git", "fetch", "origin", BRANCH], cwd=REPO,
                   capture_output=True, timeout=120)
    head = live_head()
    work = tempfile.mkdtemp(prefix="m6-battery-")
    failures = []
    results = {}
    for case in CASES:
        d_pre = build_run(work, {**case, "name": case["name"] + "-preveto"}, head)
        d_vet = build_run(work, {**case, "name": case["name"] + "-vetoed"}, head)
        pre = stage_score_preveto(d_pre, os.path.join(d_pre, "scorer", "scores.json"),
                                  work, REPO)
        vet = vetoed.stage_score(d_vet, os.path.join(d_vet, "scorer", "scores.json"),
                                 base=work, repo=REPO)
        results[case["name"]] = (pre, vet)
    # --- assertions ---
    # 1. PRE-VETO: exactly cases 1,2,3,6 correct = 4/6 (defect signature on 4,5).
    pre_correct = [c["name"] for c in CASES
                   if results[c["name"]][0]["capability_verdict"] == c["expect"]]
    if pre_correct != ["c1-normal-confirm", "c2-adv-refuted", "c3-adv-phantom",
                       "c6-normal-weak"]:
        failures.append(f"PRE-VETO must be exactly 4/6 on c1,c2,c3,c6; got {pre_correct}")
    for bad in ("c4-adv-swallow", "c5-adv-punt"):
        pre_v = results[bad][0]["capability_verdict"]
        if pre_v != "CAPABILITY-TRANSFERS":
            failures.append(f"defect signature missing: pre-veto {bad} -> {pre_v} "
                            "(must be CAPABILITY-TRANSFERS to show the defect)")
        if not all(results[bad][0]["mechanical_checks"][k] for k in M15):
            failures.append(f"defect signature invalid: pre-veto {bad} has a failed "
                            "M1-M5 check (the signature requires all passing)")
    # 2. VETOED: 6/6.
    vet_correct = [c["name"] for c in CASES
                   if results[c["name"]][1]["capability_verdict"] == c["expect"]]
    if len(vet_correct) != 6:
        failures.append(f"VETOED must be 6/6; got {len(vet_correct)}/6: {vet_correct}")
    # 3. The veto as the SOLE discriminator: M1-M5 identical across impls, every
    #    case; M6 fires exactly on c4,c5; verdicts differ only there.
    for c in CASES:
        pre, vet = results[c["name"]]
        for k in M15:
            if bool(pre["mechanical_checks"][k]) != bool(vet["mechanical_checks"][k]):
                failures.append(f"{c['name']}: {k} differs across implementations "
                                "(veto must be the sole discriminator)")
        m6 = vet["mechanical_checks"]["M6_verdict_consistent_with_kind"]
        expect_m6 = not (c["kind"] == "ADVERSARIAL" and c["verdict"] not in CATCH_VERDICTS)
        if bool(m6) != expect_m6:
            failures.append(f"{c['name']}: M6={m6}, expected {expect_m6}")
    for c in ("c1-normal-confirm", "c6-normal-weak"):
        if not results[c][1]["mechanical_checks"]["M6_verdict_consistent_with_kind"]:
            failures.append(f"{c}: veto must NEVER fire on a NORMAL slot")
    # 4. Mechanic formula stability: daily_score unchanged shape, mech over M1-M5.
    for c in CASES:
        vet = results[c["name"]][1]
        if vet["mech_pass_rate"] not in (1.0, 0.8):
            failures.append(f"{c['name']}: unexpected mech_pass_rate {vet['mech_pass_rate']}")
    print("=== M6 RED-first battery ===")
    for c in CASES:
        pre, vet = results[c["name"]]
        m6 = vet["mechanical_checks"]["M6_verdict_consistent_with_kind"]
        print(f"{c['name']:18s} expect={c['expect']:20s} "
              f"pre-veto={pre['capability_verdict']:20s} vetoed={vet['capability_verdict']:20s} M6={m6}")
    pre_n = len(pre_correct)
    print(f"\nPRE-VETO: {pre_n}/6 (defect signature: c4,c5 swallowers -> TRANSFERS)")
    print(f"VETOED:   {len(vet_correct)}/6")
    shutil.rmtree(work, ignore_errors=True)
    if failures:
        print("\nFAILURES:")
        for f in failures:
            print(f"  - {f}")
        sys.exit(1)
    print("\nALL GREEN — 4/6 defect signature reproduced pre-veto, 6/6 post-veto, veto is the sole discriminator.")


if __name__ == "__main__":
    main()
