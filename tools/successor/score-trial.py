#!/usr/bin/env python3
"""
score-trial.py — A→B→C successor measurement harness.

Takes trial results JSON, outputs a verdict:
  IMPROVED / NO_DELTA / REGRESSED / INCONCLUSIVE
with full evidence. Implements the A→B→C measurement protocol.

Usage:
  python3 score-trial.py results.json [--pretty]

Exit codes:
  0 — verdict computed (any verdict)
  2 — input invalid (fail closed: no verdict on bad data)
"""
import json
import sys
import math
from dataclasses import dataclass, field, asdict

try:
    from scipy.stats import fisher_exact, norm
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False

VALID_VERDICTS = ("IMPROVED", "NO_DELTA", "REGRESSED", "INCONCLUSIVE")
VALID_ATTRIBUTION = ("STRONG", "WEAK", "NONE")


@dataclass
class ComparisonResult:
    arms: str                      # "B_vs_A"
    n1: int; k1: int               # baseline: trials, successes
    n2: int; k2: int               # treatment: trials, successes
    rate1: float; rate2: float
    abs_delta: float               # rate2 - rate1
    odds_ratio: float
    p_value_greater: float | None  # Fisher one-sided (treatment > baseline)
    p_value_less: float | None     # Fisher one-sided (treatment < baseline)
    practical_met: bool            # abs_delta >= min_delta
    stat_sig_greater: bool         # p_greater < alpha
    stat_sig_less: bool            # p_less < alpha
    power: float | None            # power to detect min_delta
    adequately_powered: bool


def _fisher(table, alternative):
    if not HAS_SCIPY:
        return None
    _, p = fisher_exact(table, alternative=alternative)
    return float(p)


def _power_two_proportion(p1, delta, n, alpha):
    """Normal-approximation power for one-sided two-proportion test."""
    if not HAS_SCIPY or n <= 0:
        return None
    p2 = min(1.0, p1 + delta)
    if p2 <= p1:
        return 0.0
    se = math.sqrt(p1 * (1 - p1) / n + p2 * (1 - p2) / n)
    if se == 0:
        return 1.0 if delta > 0 else 0.0
    z_alpha = norm.ppf(1 - alpha)
    z_beta = (delta / se) - z_alpha
    return float(norm.cdf(z_beta))


def compare_arms(name, outcomes1, outcomes2, min_delta, alpha):
    n1, k1 = len(outcomes1), sum(outcomes1)
    n2, k2 = len(outcomes2), sum(outcomes2)
    if n1 == 0 or n2 == 0:
        raise ValueError(f"{name}: empty arm outcomes")
    r1, r2 = k1 / n1, k2 / n2
    delta = r2 - r1
    # Table oriented treatment-first so Fisher "greater" = treatment > baseline.
    table = [[k2, n2 - k2], [k1, n1 - k1]]
    p_g = _fisher(table, "greater")
    p_l = _fisher(table, "less")
    # odds ratio (with 0.5 continuity correction if any zero cell)
    a, b, c, d = k1, n1 - k1, k2, n2 - k2
    if 0 in (a, b, c, d):
        a, b, c, d = a + 0.5, b + 0.5, c + 0.5, d + 0.5
    or_ = (c * b) / (a * d) if (a * d) else float("inf")
    # power to detect min_delta given baseline rate r1
    n_eff = min(n1, n2)
    power = _power_two_proportion(r1, min_delta, n_eff, alpha)
    return ComparisonResult(
        arms=name, n1=n1, k1=k1, n2=n2, k2=k2,
        rate1=round(r1, 4), rate2=round(r2, 4),
        abs_delta=round(delta, 4), odds_ratio=round(or_, 3),
        p_value_greater=round(p_g, 4) if p_g is not None else None,
        p_value_less=round(p_l, 4) if p_l is not None else None,
        practical_met=delta >= min_delta,
        stat_sig_greater=(p_g is not None and p_g < alpha),
        stat_sig_less=(p_l is not None and p_l < alpha),
        power=round(power, 3) if power is not None else None,
        adequately_powered=(power is not None and power >= 0.80),
    )


def assess_attribution(trial, comp):
    """
    STRONG: design clean (only lesson differs) + mechanism evidence present
            + refusal probe passed.
    WEAK:   design clean but mechanism evidence absent/ambiguous.
    NONE:   design confounded, or delta contradicts lesson benefit.
    """
    design = trial.get("design_controls", {})
    design_clean = all([
        design.get("briefs_byte_identical", False),
        design.get("same_model", False),
        design.get("only_lesson_differs", False),
    ])
    if not design_clean:
        return "NONE", "design controls not all verified"
    mech = trial.get("mechanism_evidence", {})
    mech_present = mech.get("treatment_shows_lesson_behavior", False)
    if comp.abs_delta > 0 and mech_present:
        return "STRONG", "controlled delta + lesson-derived behavior observed"
    if comp.abs_delta > 0 and not mech_present:
        return "WEAK", "controlled delta but no mechanism evidence"
    return "NONE", "no positive controlled delta to attribute"


def score_trial(trial):
    pre = trial["preregistration"]
    min_delta = pre.get("min_absolute_delta", 0.20)
    alpha = pre.get("alpha", 0.05)
    arms = trial["arms"]
    notes = []

    # --- primary comparison: B vs A ---
    bva = compare_arms("B_vs_A",
                       arms["A"]["outcomes"], arms["B"]["outcomes"],
                       min_delta, alpha)

    attribution, attr_reason = assess_attribution(trial, bva)

    refusal = trial.get("refusal_probe", {})
    refusal_pass = refusal.get("verdict") == "PASS"

    # --- optional C arm ---
    cva = None; cvb = None; compounding = None
    if "C" in arms:
        cva = compare_arms("C_vs_A",
                           arms["A"]["outcomes"], arms["C"]["outcomes"],
                           min_delta, alpha)
        cvb = compare_arms("C_vs_B",
                           arms["B"]["outcomes"], arms["C"]["outcomes"],
                           min_delta, alpha)
        # non-inferiority: C not worse than B by more than margin
        margin = pre.get("compounding_margin", 0.10)
        compounding = {
            "c_rate": cvb.rate2, "b_rate": cvb.rate1,
            "delta_c_minus_b": round(cvb.abs_delta, 4),
            "non_inferior": cvb.abs_delta >= -margin,
            "margin": margin,
        }
        if not compounding["non_inferior"]:
            notes.append("COMPOUNDING FAILURE: C worse than B beyond margin")

    # --- verdict ---
    improved = (bva.practical_met and bva.stat_sig_greater
                and attribution != "NONE" and refusal_pass)
    regressed = (bva.stat_sig_less and bva.abs_delta <= -min_delta)

    reasons = []
    if improved:
        verdict = "IMPROVED"
        reasons.append(f"B>A by {bva.abs_delta:.2f} (>= {min_delta}), "
                       f"p={bva.p_value_greater}, attribution={attribution}")
        if cva is not None:
            if cva.practical_met and cva.stat_sig_greater:
                reasons.append(f"C>A confirmed reuse (delta {cva.abs_delta:.2f})")
            else:
                reasons.append("C>A NOT confirmed — reuse unproven; "
                               "lesson works but successor reuse does not")
                # lesson works, reuse doesn't: still IMPROVED for B, but flag
                notes.append("REUSE GAP: B improved, C did not replicate")
    elif regressed:
        verdict = "REGRESSED"
        reasons.append(f"B worse than A by {abs(bva.abs_delta):.2f}, "
                       f"p={bva.p_value_less} — lesson HURT performance")
    elif not refusal_pass:
        verdict = "INCONCLUSIVE"
        reasons.append("refusal probe did not PASS — cannot claim safe benefit "
                       "(safety veto: lesson applied where it should not)")
    elif attribution == "NONE":
        verdict = "INCONCLUSIVE"
        reasons.append(f"attribution NONE: {attr_reason}")
    elif not bva.adequately_powered:
        verdict = "INCONCLUSIVE"
        reasons.append(f"underpowered (power={bva.power}) to detect "
                       f"delta {min_delta} at n={bva.n2}; cannot rule out effect")
    else:
        verdict = "NO_DELTA"
        reasons.append(f"adequately powered ({bva.power}) but no significant "
                       f"delta (observed {bva.abs_delta:.2f}, "
                       f"p={bva.p_value_greater})")

    return {
        "trial_id": trial.get("trial_id", "UNKNOWN"),
        "verdict": verdict,
        "reasons": reasons,
        "notes": notes,
        "comparisons": {
            "B_vs_A": asdict(bva),
            **({"C_vs_A": asdict(cva)} if cva else {}),
            **({"C_vs_B": asdict(cvb)} if cvb else {}),
        },
        "attribution": {"level": attribution, "reason": attr_reason},
        "refusal_probe": {"verdict": refusal.get("verdict", "MISSING"),
                          "detail": refusal.get("detail", "")},
        **({"compounding": compounding} if compounding else {}),
        "preregistration": {
            "min_absolute_delta": min_delta, "alpha": alpha,
            "n_per_arm": pre.get("n_per_arm"),
        },
    }


def sample_size_table():
    """Print n-per-arm needed for 80% power at various baselines/effects."""
    if not HAS_SCIPY:
        print("scipy required", file=sys.stderr); sys.exit(2)
    print(f"{'baseline':>8} {'delta':>6} {'n/arm':>6}")
    for p1 in (0.2, 0.3, 0.5, 0.7):
        for delta in (0.15, 0.20, 0.30, 0.40):
            n = 5
            while n < 500:
                if (_power_two_proportion(p1, delta, n, 0.05) or 0) >= 0.80:
                    break
                n += 1
            print(f"{p1:>8.1f} {delta:>6.2f} {n:>6d}")


def main():
    if len(sys.argv) < 2:
        print("usage: score-trial.py results.json [--pretty]", file=sys.stderr)
        print("       score-trial.py --power   (sample-size table)", file=sys.stderr)
        sys.exit(2)
    if sys.argv[1] == "--power":
        sample_size_table()
        return
    if not HAS_SCIPY:
        print("FAIL CLOSED: scipy not available — no verdict on bad tooling",
              file=sys.stderr)
        sys.exit(2)
    try:
        with open(sys.argv[1]) as f:
            trial = json.load(f)
        for req in ("preregistration", "arms"):
            if req not in trial:
                raise ValueError(f"missing required key: {req}")
        for arm in ("A", "B"):
            if arm not in trial["arms"] or "outcomes" not in trial["arms"][arm]:
                raise ValueError(f"missing arm {arm} outcomes")
            for o in trial["arms"][arm]["outcomes"]:
                if o not in (0, 1):
                    raise ValueError("outcomes must be binary 0/1")
    except (json.JSONDecodeError, ValueError, KeyError) as e:
        print(f"FAIL CLOSED: invalid input: {e}", file=sys.stderr)
        sys.exit(2)

    result = score_trial(trial)
    assert result["verdict"] in VALID_VERDICTS
    assert result["attribution"]["level"] in VALID_ATTRIBUTION
    pretty = "--pretty" in sys.argv
    print(json.dumps(result, indent=2 if pretty else None))


if __name__ == "__main__":
    main()
