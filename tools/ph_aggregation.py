#!/usr/bin/env python3
"""ph_aggregation.py — pinned p/h aggregation for the trial grade-acceptance instrument.

Closes gr-w310-zeta-gapclose: the p/h aggregation step (Fisher's exact two-sided
+ Cohen's h + T3 print-precision tolerance) previously ran ad hoc per executor.
This script pins every choice so the next cold execution has ZERO executor-chosen
degrees of freedom in the aggregation.

Formulas (documented in the instrument's own graders, e.g.
BRAIN/05-MEMORY/LEARNING-TRIALS/2026/10/07/GRADER-REPAIR-2026-10-07/grade_trial11.py):
  - Fisher's exact test (two-sided) on 2x2 contingency:
      [[treat_correct, treat_wrong], [ctrl_correct, ctrl_wrong]]
    Two-sided = sum of hypergeometric probabilities of all margin-consistent
    tables whose probability is <= the observed table's probability.
    Reference: scipy.stats.fisher_exact (two-sided); the script re-implements it
    in stdlib so the cold env needs no scipy. Exactness: table ordering uses
    Fraction (exact rationals), so the two-sided set is deterministic.
  - Cohen's h = 2*arcsin(sqrt(p_treat)) - 2*arcsin(sqrt(p_ctrl)),
    p_treat / p_ctrl = per-question success proportions.

T3 COMPARE (design doc hidden_files/alpha-w292-trial-instrument-design.md, T3;
Adopted from gr-w307-alpha-precision-rule, Alpha w305 LEARN; landed Zeta w307):
  Integer scores match EXACTLY. For p and h: the claim arrives as a PRINTED
  value with n significant figures — PASS iff |recomputed - claim| <= tol,
  where tol = 0.5 * 10^(floor(log10(|claim|)) - n + 1) — half a unit in the
  claim's last printed place. n is counted from the PRINTED STRING
  ("1.95e-13" -> n=3 -> tol=5e-16; "1.70" -> n=3 -> tol=0.005).
  claim == 0 -> HELD (log10 undefined; parse gap, never FAIL).
  Unparseable claimed shape -> HELD, not FAIL.

Inputs come from T1's claim-bound copy (design doc T1 claim-bound copy rule) —
the script pins the computation; T1 pins the inputs. Provenance-unknown rows
(T11/T13 claimed p's match no tested formula): a FAIL licenses ONLY
"recomputed != printed claim", never "wrong test".

Usage:
  ph_aggregation.py --treat-correct 90 --treat-wrong 0 --ctrl-correct 39 \\
      --ctrl-wrong 51 --claimed-p "1.95e-13" --claimed-h "1.70"
  ph_aggregation.py --self-test   # the four known rows; asserts pinned legs
"""
import argparse, json, math, sys
from fractions import Fraction
from math import comb

def parse_claim(s):
    """Parse a PRINTED claim string -> (value, n_sigfigs, tol).

    tol = 0.5 * 10^(floor(log10(|value|)) - n + 1). value == 0 -> tol None (HELD).
    Unparseable -> raises ValueError (caller converts to HELD).
    """
    t = s.strip()
    v = float(t)  # raises ValueError if unparseable
    # count significant digits from the mantissa of the printed string
    mant = t.lstrip('+-').split('e')[0].split('E')[0].replace('.', '')
    mant = mant.lstrip('0') or '0'
    n = len(mant)
    if v == 0.0:
        return v, n, None
    tol = 0.5 * 10 ** (math.floor(math.log10(abs(v))) - n + 1)
    return v, n, tol

def fisher_two_sided(a, b, c, d):
    """Fisher's exact two-sided p for [[a,b],[c,d]] (stdlib, deterministic).

    Enumerates every table consistent with the margins; sums the exact
    hypergeometric probabilities of tables with P <= P(observed), comparing
    with exact Fraction arithmetic. Matches scipy.stats.fisher_exact
    two-sided (verified in --self-test against Theta's scipy-cited rows).
    """
    n1 = a + b          # treatment total
    n2 = c + d          # control total
    k = a + c           # column-1 (correct) total
    n = n1 + n2
    lo = max(0, k - n2)
    hi = min(n1, k)
    denom = comb(n, k)
    def p_of(x):
        # P(treat_correct == x | margins) = C(n1,x)*C(n2,k-x)/C(n,k)
        return Fraction(comb(n1, x) * comb(n2, k - x), denom)
    p_obs = p_of(a)
    total = Fraction(0, 1)
    for x in range(lo, hi + 1):
        if p_of(x) <= p_obs:
            total += p_of(x)
    return float(total)

def cohens_h(p_treat, p_ctrl):
    """Cohen's h = 2*arcsin(sqrt(p_t)) - 2*arcsin(sqrt(p_c))."""
    return 2 * math.asin(math.sqrt(p_treat)) - 2 * math.asin(math.sqrt(p_ctrl))

def compare_leg(claimed_str, recomputed):
    """Apply the T3 rule to one leg. Returns dict with verdict PASS/FAIL/HELD."""
    try:
        claim, n, tol = parse_claim(claimed_str)
    except ValueError:
        return {"verdict": "HELD", "reason": "unparseable claimed shape",
                "claimed": claimed_str, "recomputed": recomputed}
    if tol is None:
        return {"verdict": "HELD", "reason": "claim == 0 (log10 undefined)",
                "claimed": claim, "sigfigs": n, "recomputed": recomputed}
    diff = abs(recomputed - claim)
    return {"verdict": "PASS" if diff <= tol else "FAIL",
            "claimed": claim, "sigfigs": n, "tol": tol,
            "recomputed": recomputed, "diff": diff}

def aggregate(tc, tw, cc, cw, claimed_p, claimed_h):
    p = fisher_two_sided(tc, tw, cc, cw)
    h = cohens_h(tc / (tc + tw), cc / (cc + cw))
    return {
        "inputs": {"treat_correct": tc, "treat_wrong": tw,
                   "ctrl_correct": cc, "ctrl_wrong": cw,
                   "claimed_p": claimed_p, "claimed_h": claimed_h},
        "recomputed": {"p": p, "h": h},
        "p_leg": compare_leg(claimed_p, p),
        "h_leg": compare_leg(claimed_h, h),
    }

# The four known rows: (treat 2x2, ctrl 2x2, claimed p, claimed h, expected legs).
# Ground truth: T12/T14 claimed p's match scipy Fisher two-sided (Theta,
# gr-w303-theta-pformula); T11 claimed p is provenance-unknown (20+ methods
# tested, none match) -> p-leg FAIL is the pinned expectation, licensing ONLY
# "recomputed != printed claim". T13 claimed p likewise provenance-unknown.
SELF_TEST_ROWS = [
    # T11: 90/90 vs 39/90 — p FAIL (provenance-unknown claim), h PASS
    dict(tc=90, tw=0, cc=39, cw=51, cp="1.95e-13", ch="1.70",
         exp_p="FAIL", exp_h="PASS", name="T11"),
    # T12: 90/90 vs 61/90 — p PASS (scipy-cited), h PASS
    dict(tc=90, tw=0, cc=61, cw=29, cp="2.51e-10", ch="1.21",
         exp_p="PASS", exp_h="PASS", name="T12"),
    # T13: 90/90 vs 40/90 — p FAIL (provenance-unknown claim), h PASS
    dict(tc=90, tw=0, cc=40, cw=50, cp="5.31e-13", ch="1.68",
         exp_p="FAIL", exp_h="PASS", name="T13"),
    # T14: 40/40 vs 28/40 — p PASS (scipy-cited), h PASS
    dict(tc=40, tw=0, cc=28, cw=12, cp="1.85e-04", ch="1.16",
         exp_p="PASS", exp_h="PASS", name="T14"),
]

def self_test():
    ok = True
    for r in SELF_TEST_ROWS:
        out = aggregate(r["tc"], r["tw"], r["cc"], r["cw"], r["cp"], r["ch"])
        pv, hv = out["p_leg"]["verdict"], out["h_leg"]["verdict"]
        good = (pv == r["exp_p"] and hv == r["exp_h"])
        ok = ok and good
        print(f"{r['name']}: p={out['recomputed']['p']:.6e} "
              f"(claim {r['cp']}, tol {out['p_leg'].get('tol')}, leg {pv}, exp {r['exp_p']}) | "
              f"h={out['recomputed']['h']:.6f} "
              f"(claim {r['ch']}, tol {out['h_leg'].get('tol')}, leg {hv}, exp {r['exp_h']}) "
              f"-> {'OK' if good else 'MISMATCH'}")
    return ok

def main():
    ap = argparse.ArgumentParser(description="Pinned p/h aggregation (Fisher two-sided + Cohen's h + T3 tolerance).")
    ap.add_argument("--treat-correct", type=int)
    ap.add_argument("--treat-wrong", type=int)
    ap.add_argument("--ctrl-correct", type=int)
    ap.add_argument("--ctrl-wrong", type=int)
    ap.add_argument("--claimed-p")
    ap.add_argument("--claimed-h")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        sys.exit(0 if self_test() else 1)
    for req in ("treat_correct", "treat_wrong", "ctrl_correct", "ctrl_wrong",
                "claimed_p", "claimed_h"):
        if getattr(args, req) is None:
            ap.error(f"--{req.replace('_','-')} is required (or use --self-test)")
    out = aggregate(args.treat_correct, args.treat_wrong,
                    args.ctrl_correct, args.ctrl_wrong,
                    args.claimed_p, args.claimed_h)
    print(json.dumps(out, indent=2))
    sys.exit(0)

if __name__ == "__main__":
    main()
