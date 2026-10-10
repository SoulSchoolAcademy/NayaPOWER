#!/usr/bin/env python3
"""TRIAL-16 grading: unblind sealed mapping, score VALID-DESIGN, run Tier-S stats."""
import json, math, re, sys
from pathlib import Path

D = Path(__file__).parent

def parse_gradesheet(text):
    grades = {}
    for line in text.splitlines():
        m = re.match(r'(DESIGN-\d+):\s*R1=(\d)\s*R2=(\d)\s*R3=(\d)\s*R4=(\d)\s*COMPLETENESS=(\d)', line)
        if m:
            g = [int(x) for x in m.groups()[1:]]
            grades[m.group(1)] = {'R': g[:4], 'C': g[4]}
    return grades

def fisher_exact_2x2(a, b, c, d):
    # a=treat valid, b=treat invalid, c=ctrl valid, d=ctrl invalid; two-sided via enumeration
    from math import comb
    n1, n2 = a + b, c + d
    K = a + c
    N = n1 + n2
    def prob(x):
        return comb(n1, x) * comb(n2, K - x) / comb(N, K)
    p_obs = prob(a)
    p = sum(prob(x) for x in range(max(0, K - n2), min(K, n1) + 1) if prob(x) <= p_obs + 1e-12)
    return min(p, 1.0)

def cohens_h(p1, p2):
    return 2 * math.asin(math.sqrt(p1)) - 2 * math.asin(math.sqrt(p2))

def bayes_p_treat_gt_ctrl(a, b, c, d, sims=200000):
    import random
    random.seed(16)
    wins = 0
    for _ in range(sims):
        pt = random.betavariate(a + 1, b + 1)
        pc = random.betavariate(c + 1, d + 1)
        if pt > pc:
            wins += 1
    return wins / sims

def main():
    grades = parse_gradesheet((D / 'grade_sheet.txt').read_text())
    mapping = json.loads((D / 'sealed_mapping.json').read_text())  # DESIGN-NN -> subject ID
    arms = {}
    for line in (D / 'arm_assignment.txt').read_text().splitlines():
        if line.startswith('TREATMENT:'):
            for s in line.split(':', 1)[1].split(','):
                arms[s.strip()] = 'treat'
        elif line.startswith('CONTROL:'):
            for s in line.split(':', 1)[1].split(','):
                arms[s.strip()] = 'ctrl'
    rows = []
    for design, g in sorted(grades.items()):
        subj = mapping.get(design)
        if not subj or subj not in arms:
            print(f'WARN: {design} unmapped, skipped', file=sys.stderr)
            continue
        valid = sum(g['R']) >= 3
        rows.append({'design': design, 'subject': subj, 'arm': arms[subj],
                     'R': g['R'], 'C': g['C'], 'valid': valid})
    treat = [r for r in rows if r['arm'] == 'treat']
    ctrl = [r for r in rows if r['arm'] == 'ctrl']
    a = sum(r['valid'] for r in treat); b = len(treat) - a
    c = sum(r['valid'] for r in ctrl); d = len(ctrl) - c
    p1, p0 = (a / len(treat)) if treat else 0, (c / len(ctrl)) if ctrl else 0
    p = fisher_exact_2x2(a, b, c, d)
    h = cohens_h(p1, p0)
    bayes = bayes_p_treat_gt_ctrl(a, b, c, d)
    ct = sum(r['C'] for r in treat) / len(treat) if treat else 0
    cc = sum(r['C'] for r in ctrl) / len(ctrl) if ctrl else 0
    tier_s = (p < 0.05) and (abs(h) >= 1.4) and (p1 > p0)
    ceiling_invalid = p0 >= 0.50
    neg_transfer = ct < cc - 0.5
    verdict = ('INVALID_BY_CEILING' if ceiling_invalid
               else 'TIER_S_MET' if tier_s
               else 'FAIL_CLOSED_NEGTRANSFER' if neg_transfer else 'NOT_TIER_S')
    results = {
        'trial': 'T16-20261008-compounding-reuse',
        'n_treat': len(treat), 'n_ctrl': len(ctrl),
        'treat_valid': a, 'ctrl_valid': c,
        'treat_valid_rate': round(p1, 4), 'ctrl_valid_rate': round(p0, 4),
        'fisher_two_sided_p': round(p, 6), 'cohens_h': round(h, 4),
        'bayes_P_treat_gt_ctrl': round(bayes, 4),
        'treat_completeness_mean': round(ct, 3), 'ctrl_completeness_mean': round(cc, 3),
        'ceiling_invalid': ceiling_invalid, 'negative_transfer': neg_transfer,
        'tier_s': tier_s, 'verdict': verdict,
        'rows': rows,
    }
    (D / 'results_trial16.json').write_text(json.dumps(results, indent=2))
    print(json.dumps({k: v for k, v in results.items() if k != 'rows'}, indent=2))

if __name__ == '__main__':
    main()
