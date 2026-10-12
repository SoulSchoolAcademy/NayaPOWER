#!/usr/bin/env python3
"""CT-4 strengthened cross-check battery (Lane 6 t0212).

Tests ct4_cross_check.run_ct4() against the CTA-PROTOCOL-v2 §4 CT-4 spec:

  1. REAL PHANTOM — branch `naya/phantom-cta-t0212` (never created): both
     independent remote reads must agree on absence -> PHANTOM_CAUGHT, with
     BOTH commands recorded verbatim and G2 elision-free.
  2. EXISTING BRANCH — `naya/six-sgf-daily-runner-t992` (the live runner
     branch): the targeted lookup finds it -> RECEIPT_CONFIRMED (not a
     phantom). The check must not mistake a real branch for a phantom.
  3. DISAGREEMENT PATH — simulated: targeted says absent while the full
     listing contains the branch -> UNABLE_TO_VERIFY, never a catch. (This is
     exactly why v1's single lookup was weak: a transient failure mimics a
     phantom. The test drives it by monkeypatching the transport.)
  4. ELIDED COMMANDS -> G2 failure -> the daily seat must rule UNPROVEN_CATCH
     (assert_rows_elision_free on successor-recorded rows; a catch on elided
     rows is a claim, not a catch, per v2 §6).

Live cases 1-2 use real `git ls-remote` (the instrument's actual mechanism).
Run:  python3 test_ct4_cross_check.py     (exit 0 = all green)
"""
import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SGF_DAILY = os.path.dirname(HERE)
REPO = os.path.expanduser("~/workspace/nayapower-rescue")

spec = importlib.util.spec_from_file_location(
    "ct4_cross_check", os.path.join(SGF_DAILY, "ct4_cross_check.py"))
ct4 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ct4)

PHANTOM = "naya/phantom-cta-t0212"
EXISTING = "naya/six-sgf-daily-runner-t992"


def main():
    failures = []

    # 1. Real phantom -> PHANTOM_CAUGHT with two verbatim rows.
    r1 = ct4.run_ct4(PHANTOM, REPO)
    if r1["verdict"] != "PHANTOM_CAUGHT":
        failures.append(f"phantom: expected PHANTOM_CAUGHT, got {r1['verdict']}: {r1['why']}")
    if len(r1["rows"]) != 2:
        failures.append(f"phantom: expected 2 cross-check rows, got {len(r1['rows'])}")
    cmds = [r["command"] for r in r1["rows"]]
    if not any("refs/heads/" + PHANTOM in c and "|" not in c for c in cmds):
        failures.append(f"phantom: missing verbatim targeted-lookup row: {cmds}")
    if not any("git ls-remote origin | grep" in c for c in cmds):
        failures.append(f"phantom: missing verbatim full-listing row: {cmds}")
    if not r1["g2_pass"]:
        failures.append("phantom: g2_pass must be True (no elided commands)")
    for r in r1["rows"]:
        for k in ("assertion", "command", "observed", "expected", "match"):
            if k not in r:
                failures.append(f"phantom row missing key {k}")

    # 2. Existing branch -> RECEIPT_CONFIRMED, never a phantom catch.
    r2 = ct4.run_ct4(EXISTING, REPO)
    if r2["verdict"] != "RECEIPT_CONFIRMED":
        failures.append(f"existing: expected RECEIPT_CONFIRMED, got {r2['verdict']}: {r2['why']}")
    if r2["verdict"] == "PHANTOM_CAUGHT":
        failures.append("existing: MUST NOT catch a real branch as phantom")

    # 3. Disagreement (targeted absent, full listing present) -> UNABLE_TO_VERIFY.
    real_ls = ct4._ls_remote
    ct4._ls_remote = lambda ref, repo: (0, "") if ref else (
        0, "deadbeefdeadbeefdeadbeefdeadbeefdeadbeef\trefs/heads/" + PHANTOM + "\n")
    r3 = ct4.run_ct4(PHANTOM, REPO)
    ct4._ls_remote = real_ls
    if r3["verdict"] != "UNABLE_TO_VERIFY":
        failures.append(f"disagreement: expected UNABLE_TO_VERIFY, got {r3['verdict']}: {r3['why']}")

    # 4. ELIDED ROW COMMANDS -> G2 failure -> seat must rule UNPROVEN_CATCH.
    #    The elision rule applies to SUCCESSOR-recorded rows: a PHANTOM_CAUGHT
    #    resting on an elided cross-check is a claim, not a catch (v2 §6).
    clean_rows = r1["rows"]
    if not ct4.assert_rows_elision_free(clean_rows)["g2_pass"]:
        failures.append("elision: the module's own verbatim rows must pass G2")
    elided = [dict(clean_rows[0]),
              dict(clean_rows[1], command=clean_rows[1]["command"] + " ... (elided)")]
    g2r = ct4.assert_rows_elision_free(elided)
    if g2r["g2_pass"]:
        failures.append("elision: a row command with an elision marker must fail G2")
    if g2r["offenders"] != [1]:
        failures.append(f"elision: offender must be row 1, got {g2r['offenders']}")
    for marker in ("...", "…", "[truncated]", "(elided)", "[snip]", "run it etc."):
        if ct4.elision_free(f"git ls-remote origin {marker}"):
            failures.append(f"elision: marker {marker!r} must be caught")

    print("=== CT-4 strengthened cross-check battery ===")
    print(f"1. real phantom        -> {r1['verdict']} (rows={len(r1['rows'])}, g2={r1['g2_pass']})")
    print(f"2. existing branch     -> {r2['verdict']}")
    print(f"3. read disagreement   -> {r3['verdict']} (transient-failure caught)")
    print(f"4. elision rule        -> G2 catches all markers; catch on elided rows = UNPROVEN_CATCH")
    if failures:
        print("\nFAILURES:")
        for f in failures:
            print(f"  - {f}")
        sys.exit(1)
    print("\nALL GREEN — double-negative cross-check catches the phantom, spares the real branch, "
          "refuses the disagreement, and rejects elided rows.")


if __name__ == "__main__":
    main()
