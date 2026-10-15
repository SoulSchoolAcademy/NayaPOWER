"""Self-test for tools/claim_reconcile.py — run: python3 tools/test_claim_reconcile.py

Acceptance (GRAND-TODO 0-series/0): a deliberately planted conflicting
claim is caught by the machine. These four cases prove it:
  conflict   -> the #2597 shape: "green CI" claimed, a gate red at the head
  cherrypick -> the #2552 shape: success+failure 3s apart, latest by
                started_at is the failure (started_at ordering, wave-179)
  stale      -> claim cites an older head SHA than the live head
  clean      -> all green; no false positive
w186 hardening cases prove the matcher is adversary-proof:
  named-exact            -> "Team gate green" binds the real "Team gate"
  named-homograph-green  -> "Te<cy>a</cy>m gate green" folds to the real check,
                            no false positive on a homograph name
  named-homograph-red    -> the same homograph claim is still bound to the
                            REAL red check: a misspelling cannot dodge a red
  named-ambiguous        -> "the old gate" vs "old gate"+"older gate":
                            substring-only matches fail closed
  vacuous-require        -> --require-claims: a claim-less intent is BLIND
  vacuous-plain          -> without the flag, no claims = RECONCILED
                            (the tool judges text; the gate judges intent)
w215 narrowing cases (Delta w213) prove the detector tells assertion
from citation:
  quoted-nofire          -> "green CI" in quotes, in a blockquote, in code,
                            and aspirational "keep CI green" do NOT fire —
                            RECONCILED even with a red check present
  bare-stillfires        -> the same narrative WITH a bare declarative
                            "CI is green" still fires — CONFLICT (fail closed)
"""
import json
import subprocess
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
FIX = TOOLS / "claim_reconcile_fixtures"

CASES = {
    # (want_exit, want_verdict, claim, pr, checks, extra_args)
    "conflict": (1, "CONFLICT", "claim-conflict.txt", "pr-conflict.json",
                 "checks-conflict.json", []),
    "cherrypick": (1, "CONFLICT", "claim-cherrypick.txt", "pr-cherrypick.json",
                   "checks-cherrypick.json", []),
    "stale": (2, "STALE", "claim-stale.txt", "pr-stale.json",
              "checks-stale.json", []),
    "clean": (0, "RECONCILED", "claim-clean.txt", "pr-clean.json",
              "checks-clean.json", []),
    # w186 hardening cases
    "named-exact": (0, "RECONCILED", "claim-named-exact.txt", "pr-named.json",
                    "checks-named.json", []),
    "named-homograph-green": (0, "RECONCILED", "claim-named-homograph.txt",
                              "pr-named.json", "checks-named.json", []),
    "named-homograph-red": (1, "CONFLICT", "claim-named-homograph.txt",
                            "pr-named.json", "checks-named-red.json", []),
    "named-ambiguous": (1, "CONFLICT", "claim-ambiguous.txt", "pr-named.json",
                        "checks-ambiguous.json", []),
    "vacuous-require": (3, "BLIND", "claim-vacuous.txt", "pr-clean.json",
                        "checks-clean.json", ["--require-claims"]),
    "vacuous-plain": (0, "RECONCILED", "claim-vacuous.txt", "pr-clean.json",
                      "checks-clean.json", []),
    # w215 narrowing cases (Delta w213): assertion vs citation
    "quoted-nofire": (0, "RECONCILED", "claim-quoted-nofire.txt", "pr-clean.json",
                      "checks-conflict.json", []),
    "bare-stillfires": (1, "CONFLICT", "claim-bare-stillfires.txt", "pr-clean.json",
                        "checks-conflict.json", []),
}


def main() -> int:
    failures = 0
    for name, (want_exit, want_verdict, claim_f, pr_f, checks_f, extra) in CASES.items():
        cmd = [sys.executable, str(TOOLS / "claim_reconcile.py"),
               "--pr", "2599",
               "--claim-file", str(FIX / claim_f),
               "--pr-json", str(FIX / pr_f),
               "--checks-json", str(FIX / checks_f)] + extra
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        try:
            verdict = json.loads(proc.stdout)["verdict"]
        except (json.JSONDecodeError, KeyError):
            verdict = f"<unparseable: {proc.stdout[:100]}>"
        ok = proc.returncode == want_exit and verdict == want_verdict
        print(f"{'PASS' if ok else 'FAIL'} {name}: exit={proc.returncode} "
              f"(want {want_exit}) verdict={verdict} (want {want_verdict})")
        failures += not ok
    print(f"{len(CASES) - failures}/{len(CASES)} pass" if not failures
          else f"{failures} FAILURES")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
