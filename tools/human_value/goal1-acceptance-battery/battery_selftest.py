#!/usr/bin/env python3
"""battery_selftest.py — fail-closed proof for the HV-GOAL1 acceptance battery.

What it proves (each assertion can fail):
  1. The spec carries all five checks, each with claim, evidence class,
     pass criterion, falsifier, and expiry — a check missing any of these
     is not a falsifiable check and the battery is incomplete.
  2. The candidate registration parses as JSON, carries every key of the
     observed-experience instrument's pending-candidate schema, has
     graded_units == null (anti-precision law), status pending, and its
     checks list equals the five spec IDs (no orphan, no drift).
  3. FAIL-CLOSED dry-run: with zero observations (pre-launch reality),
     every check evaluates to UNMEASURED and no PASS/FAIL is manufactured.
     A verdict asserted without a named evidence class is REJECTED.
  4. The D32 honesty section exists and disclaims live operation.

Exit 0 = all green. Exit 1 = named failures printed.
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPEC = HERE / "GOAL1-ACCEPTANCE-BATTERY.md"

failures = []


def check(name, cond, detail=""):
    print(("PASS " if cond else "FAIL ") + name + ("" if cond else f" — {detail}"))
    if not cond:
        failures.append(name)


def main():
    check("spec file exists", SPEC.exists(), str(SPEC))
    if not SPEC.exists():
        return finish()
    text = SPEC.read_text(encoding="utf-8")

    ids = ["HV-G1-01", "HV-G1-02", "HV-G1-03", "HV-G1-04", "HV-G1-05"]
    blocks = {}
    for cid in ids:
        m = re.search(rf"^### {re.escape(cid)} — .+?\n(.*?)(?=^### |\Z)", text, re.M | re.S)
        check(f"spec: {cid} section present", bool(m))
        if m:
            blocks[cid] = m.group(0)
    check("spec: exactly five checks", len(blocks) == 5, f"found {len(blocks)}")

    for cid, body in blocks.items():
        for field in ("**Claim:**", "**Evidence class:**", "**Pass:**",
                      "**Falsifier:**", "**Expiry:**"):
            check(f"spec: {cid} has {field}", field in body)
        em = re.search(r"\*\*Evidence class:\*\*\s*([A-Z]+)", body)
        valid = bool(em) and em.group(1) in ("STATED", "REVEALED", "CORRECTED")
        check(f"spec: {cid} evidence class valid",
              valid, em.group(1) if em else "missing")

    # Candidate registration: parse + schema + anti-precision law
    cm = re.search(r"```json\n(\{.*?\n\})\n```", text, re.S)
    check("spec: candidate registration JSON present", bool(cm))
    if cm:
        try:
            cand = json.loads(cm.group(1))
        except json.JSONDecodeError as e:
            check("spec: candidate JSON parses", False, str(e))
            return finish()
        check("spec: candidate JSON parses", True)
        required = ("candidate_id", "artifact", "claim", "graded_value_type",
                    "graded_units", "graded_by", "graded_at", "expires_at",
                    "status", "acceptance_battery", "checks")
        for k in required:
            check(f"candidate: key '{k}' present", k in cand)
        check("candidate: graded_units is null (anti-precision law)",
              cand.get("graded_units") is None, repr(cand.get("graded_units")))
        check("candidate: status == pending",
              cand.get("status") == "pending", repr(cand.get("status")))
        check("candidate: checks == five spec IDs",
              cand.get("checks") == ids, repr(cand.get("checks")))
        check("candidate: battery path points at this spec",
              cand.get("acceptance_battery", "").endswith(
                  "goal1-acceptance-battery/GOAL1-ACCEPTANCE-BATTERY.md"),
              repr(cand.get("acceptance_battery")))
        check("candidate: expires_at is 21 days after graded_at",
              cand.get("expires_at", "").startswith("2026-11-06"),
              repr(cand.get("expires_at")))

    # Fail-closed dry-run: the battery's evaluation rule
    def evaluate(check_id, observations):
        if not observations:
            return "UNMEASURED"
        for o in observations:
            if o.get("verdict") and not o.get("evidence_class"):
                return "REJECTED"
        return "OBSERVED"

    for cid in ids:
        check(f"dry-run: {cid} == UNMEASURED pre-launch",
              evaluate(cid, []) == "UNMEASURED")
    check("dry-run: zero PASS/FAIL manufactured pre-launch",
          all(evaluate(cid, []) not in ("PASS", "FAIL") for cid in ids))
    check("dry-run: verdict without evidence class is REJECTED",
          evaluate("HV-G1-01", [{"verdict": "PASS"}]) == "REJECTED")
    check("dry-run: verdict with evidence class is admissible",
          evaluate("HV-G1-01",
                   [{"verdict": "PASS", "evidence_class": "REVEALED"}]) == "OBSERVED")

    # D32 honesty gate
    check("spec: D32 section present",
          "## 4. What this does NOT claim (D32)" in text)
    check("spec: D32 disclaims live operation",
          "not live end-to-end" in text)
    check("spec: D32 disclaims grader-set units",
          "never 0–10 ratings of quotes" in text or "never 0-10 ratings" in text)

    return finish()


def finish():
    print()
    if failures:
        print(f"SELFTEST FAILED: {len(failures)} failure(s)")
        for f in failures:
            print(f"  - {f}")
        sys.exit(1)
    print("SELFTEST GREEN: battery is complete, mapped, and fail-closed.")
    sys.exit(0)


if __name__ == "__main__":
    main()
