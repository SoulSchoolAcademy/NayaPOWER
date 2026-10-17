#!/usr/bin/env python3
"""Grade Trial-06 (compounding with L5 isolation) answer sheets.

Usage: grade_trial06.py answers_raw_06.json
answers.json: {"T6-A01": {"Q1": "...", ..., "Q12": "..."}, ...}
Arm mapping read from arm_assignment.txt in the same dir.
Writes results_trial06.json + prints the verdict table.
"""
import json, math, os, random, re, sys

BASE = os.path.dirname(os.path.abspath(__file__))

TREAT, CTRL = set(), set()
for line in open(os.path.join(BASE, "arm_assignment.txt")):
    line = line.strip()
    if not line or line.startswith("#"):
        continue
    aid, arm = line.split()
    (TREAT if arm == "TREATMENT" else CTRL).add(aid)

PROJ_QS = [f"Q{i}" for i in range(1, 10)]
SUCCESS_CUT = 6

def norm(s):
    s = (s or "").lower()
    s = re.sub(r"[^a-z0-9>\-\[\]/. ]", " ", s)
    return re.sub(r"\s+", " ", s).strip()

def grade(q, ans):
    s = norm(ans)
    if q == "Q1":
        return "retriev" in s and "decision time" in s
    if q == "Q2":
        return ("t4r-a19" in s or "a19" in s) and "429" in s
    if q == "Q3":
        return "1.1e-05" in s or "1.1e-5" in s or "0.000011" in s
    if q == "Q4":
        return "ceiling" in s
    if q == "Q5":
        return "isolat" in s and "instruction" in s
    if q == "Q6":
        return "branch" in s and "tmp" in s
    if q == "Q7":
        return "fail" in s and "verif" in s
    if q == "Q8":
        return "fix" in s and "report" in s
    if q == "Q9":
        return "highest" in s and "win" in s
    if q == "Q10":
        return "68" in s
    if q == "Q11":
        return "tokyo" in s
    if q == "Q12":
        return "366" in s
    return False

def fisher_exact_2sided(a, b, c, d):
    from math import comb
    n1, n2 = a + b, c + d
    m1 = a + c
    N = n1 + n2
    def prob(x):
        return comb(n1, x) * comb(n2, m1 - x) / comb(N, m1)
    p_obs = prob(a)
    lo, hi = max(0, m1 - n2), min(n1, m1)
    return sum(prob(x) for x in range(lo, hi + 1) if prob(x) <= p_obs + 1e-12)

def cohens_h(p1, p2):
    f = lambda p: 2 * math.asin(math.sqrt(min(max(p, 1e-9), 1 - 1e-9)))
    return abs(f(p1) - f(p2))

def bayes_prob_greater(s1, f1, s2, f2, n=200000, seed=42):
    rng = random.Random(seed)
    wins = 0
    for _ in range(n):
        if rng.betavariate(1 + s1, 1 + f1) > rng.betavariate(1 + s2, 1 + f2):
            wins += 1
    return wins / n

def main():
    answers = json.load(open(sys.argv[1]))
    per_agent = {}
    per_q = {q: {"treat": [0, 0], "ctrl": [0, 0]} for q in PROJ_QS}
    for aid, qs in answers.items():
        arm = "treat" if aid in TREAT else "ctrl"
        proj = 0
        for q in PROJ_QS:
            ok = grade(q, qs.get(q, ""))
            per_q[q][arm][0] += 1 if ok else 0
            per_q[q][arm][1] += 1
            proj += 1 if ok else 0
        gen = sum(1 for i in range(10, 13) if grade(f"Q{i}", qs.get(f"Q{i}", "")))
        per_agent[aid] = {"proj": proj, "gen": gen,
                          "success": proj >= SUCCESS_CUT, "arm": arm}
    t = [a for a, d in per_agent.items() if d["arm"] == "treat"]
    c = [a for a, d in per_agent.items() if d["arm"] == "ctrl"]
    ts = sum(1 for a in t if per_agent[a]["success"]); tf = len(t) - ts
    cs = sum(1 for a in c if per_agent[a]["success"]); cf = len(c) - cs
    p_fisher = fisher_exact_2sided(ts, tf, cs, cf)
    h = cohens_h(ts / len(t), cs / len(c))
    pb = bayes_prob_greater(ts, tf, cs, cf)
    t_mean = sum(per_agent[a]["proj"] for a in t) / len(t)
    c_mean = sum(per_agent[a]["proj"] for a in c) / len(c)
    t_gen = sum(per_agent[a]["gen"] for a in t) / len(t)
    c_gen = sum(per_agent[a]["gen"] for a in c) / len(c)
    verdict = {
        "n_treat": len(t), "n_ctrl": len(c),
        "treat_success": ts, "ctrl_success": cs,
        "fisher_two_sided_p": round(p_fisher, 6),
        "cohens_h": round(h, 4),
        "bayes_P_treat_gt_ctrl": round(pb, 4),
        "treat_mean_proj": round(t_mean, 2), "ctrl_mean_proj": round(c_mean, 2),
        "treat_mean_gen": round(t_gen, 2), "ctrl_mean_gen": round(c_gen, 2),
        "tierS_pass": bool(p_fisher < 0.05 and h >= 1.4),
        "ceiling_invalid": bool(c_mean >= 4.5),
        "negative_transfer_flag": bool(t_gen < c_gen - 1.0),
        "per_question": {q: {"treat_rate": round(v["treat"][0] / max(v["treat"][1], 1), 3),
                             "ctrl_rate": round(v["ctrl"][0] / max(v["ctrl"][1], 1), 3)}
                         for q, v in per_q.items()},
        "per_agent": per_agent,
    }
    json.dump(verdict, open(os.path.join(BASE, "results_trial06.json"), "w"), indent=2)
    print(json.dumps({k: v for k, v in verdict.items() if k != "per_agent"}, indent=2))

if __name__ == "__main__":
    main()
