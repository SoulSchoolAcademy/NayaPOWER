#!/usr/bin/env python3
"""Grade Trial-04R (knowledge re-run) answer sheets.

Usage: grade_trial04r.py answers_raw_04r.json
answers.json: {"T5-A01": {"Q1": "...", ..., "Q13": "..."}, ...}
Arm mapping read from arm_assignment.txt in the same dir (kept separate from graders).
Writes results_trial04r.json + prints the verdict table.
"""
import json, math, os, random, re, sys

BASE = os.path.dirname(os.path.abspath(__file__))

BRIDGE = {"T4R-A01","T4R-A03","T4R-A05","T4R-A07","T4R-A08","T4R-A14","T4R-A15","T4R-A18","T4R-A19","T4R-A20"}
COLD   = {"T4R-A02","T4R-A04","T4R-A06","T4R-A09","T4R-A10","T4R-A11","T4R-A12","T4R-A13","T4R-A16","T4R-A17"}

# AMENDMENT T5-A1 (logged 2026-10-07, BEFORE grading, outcome-blind):
# Q1 VOIDED — defective premise. The question asserted SN-003 "names a six-step
# continuation loop," but the source is internally inconsistent: the note TITLE lists
# 6 steps (Reconstruct, Find Holes, Execute, Prove, Record, Reassess) while the note
# BODY line 38 lists 8 (RECONSTRUCT -> EVALUATE -> FIND HOLES -> PRIORITIZE ->
# EXECUTE -> PROVE -> RECORD -> REASSESS). Subject T5-A07 correctly flagged this.
# A question whose premise the source contradicts cannot fairly grade anyone.
# Scoring rescales to the 9 valid project questions (Q2-Q10); success threshold
# rescales proportionally from preregistered 7/10 (70%) to >=6/9 (nearest integer).
# The corpus defect itself is reported to the curation lane.
VOID = {"Q1"}
PROJ_QS = [f"Q{i}" for i in range(2, 11)]
SUCCESS_CUT = 6

def norm(s):
    s = (s or "").lower()
    s = re.sub(r"[^a-z0-9>\-\[\] ]", " ", s)
    return re.sub(r"\s+", " ", s).strip()

def has_all(s, parts):
    return all(p in s for p in parts)

def grade(q, ans):
    s = norm(ans)
    if q == "Q1":
        seq = ["reconstruct","find holes","execute","prove","record","reassess"]
        idx = [s.find(p) for p in seq]
        return all(i >= 0 for i in idx) and idx == sorted(idx)
    if q == "Q2":
        return has_all(s, ["what it is","what purpose it serves"]) and ("important" in s)
    if q == "Q3":
        return ("candidate" in s and "ratified" in s and "testing" in s
                and s.count("ratified") >= 2)
    if q == "Q4":
        return "17" in s or "seventeen" in s
    if q == "Q5":
        return "canary-drill" in s
    if q == "Q6":
        return has_all(s, ["thesis","manifesto","law","constitutional code",
                           "mission","mission contract","mechanism","systems contract"])
    if q == "Q7":
        seq = ["discern","distill","research","verify","decide","act","show proof",
               "learn","retire stale active noise","compound"]
        # order check on the distinctive steps
        idx = [s.find(p) for p in ["discern","distill","research","decide","act",
                                   "show proof","learn","retire stale active noise","compound"]]
        return all(i >= 0 for i in idx) and idx == sorted(idx) and "verify" in s
    if q == "Q8":
        return "documentation from proof" in s or "documentation" in s and "proof" in s
    if q == "Q9":
        return "restart loop" in s
    if q == "Q10":
        return (("baseline" in s or "before" in s) and ("evaluator" in s or "success" in s and "measur" in s))
    if q == "Q11":
        return "68" in s
    if q == "Q12":
        return "tokyo" in s
    if q == "Q13":
        return "366" in s
    return False

def fisher_exact_2sided(a, b, c, d):
    # table [[a,b],[c,d]]; two-sided via hypergeometric tail sum
    from math import comb
    n1, n2 = a+b, c+d
    m1 = a+c
    N = n1+n2
    def prob(x):
        return comb(n1,x)*comb(n2,m1-x)/comb(N,m1)
    p_obs = prob(a)
    lo, hi = max(0, m1-n2), min(n1, m1)
    return sum(prob(x) for x in range(lo, hi+1) if prob(x) <= p_obs + 1e-12)

def cohens_h(p1, p2):
    f = lambda p: 2*math.asin(math.sqrt(min(max(p,1e-9),1-1e-9)))
    return abs(f(p1)-f(p2))

def bayes_prob_greater(s1, f1, s2, f2, n=200000, seed=42):
    # P(p1 > p2), Beta(1+s,1+f) posteriors, Monte Carlo
    rng = random.Random(seed)
    import statistics
    wins = 0
    for _ in range(n):
        if rng.betavariate(1+s1, 1+f1) > rng.betavariate(1+s2, 1+f2):
            wins += 1
    return wins/n

def main():
    answers = json.load(open(sys.argv[1]))
    per_agent = {}
    for aid, qs in answers.items():
        proj = sum(1 for q in PROJ_QS if grade(q, qs.get(q,"")))
        gen  = sum(1 for i in range(11,14) if grade(f"Q{i}", qs.get(f"Q{i}","")))
        per_agent[aid] = {"proj": proj, "gen": gen,
                          "success": proj >= SUCCESS_CUT, "arm": "bridge" if aid in BRIDGE else "cold"}
    t = [a for a,d in per_agent.items() if d["arm"]=="bridge"]
    c = [a for a,d in per_agent.items() if d["arm"]=="cold"]
    ts = sum(1 for a in t if per_agent[a]["success"]); tf = len(t)-ts
    cs = sum(1 for a in c if per_agent[a]["success"]); cf = len(c)-cs
    p_fisher = fisher_exact_2sided(ts, tf, cs, cf)
    h = cohens_h(ts/len(t), cs/len(c))
    pb = bayes_prob_greater(ts, tf, cs, cf)
    t_mean = sum(per_agent[a]["proj"] for a in t)/len(t)
    c_mean = sum(per_agent[a]["proj"] for a in c)/len(c)
    t_gen = sum(per_agent[a]["gen"] for a in t)/len(t)
    c_gen = sum(per_agent[a]["gen"] for a in c)/len(c)
    verdict = {
        "n_treat": len(t), "n_ctrl": len(c),
        "treat_success": ts, "ctrl_success": cs,
        "fisher_two_sided_p": round(p_fisher, 6),
        "cohens_h": round(h, 4),
        "bayes_P_treat_gt_ctrl": round(pb, 4),
        "treat_mean_proj": round(t_mean,2), "ctrl_mean_proj": round(c_mean,2),
        "treat_mean_gen": round(t_gen,2), "ctrl_mean_gen": round(c_gen,2),
        "tierS_pass": bool(p_fisher < 0.05 and h >= 1.4),
        "ceiling_invalid": bool(c_mean >= 4.5),  # rescaled from prereg. 5.0/10 to 4.5/9 (Q1 voided)
        "negative_transfer_flag": bool(t_gen < c_gen - 1.0),
        "per_agent": per_agent,
    }
    json.dump(verdict, open(os.path.join(BASE,"results_trial04r.json"),"w"), indent=2)
    print(json.dumps({k:v for k,v in verdict.items() if k!="per_agent"}, indent=2))

if __name__ == "__main__":
    main()
