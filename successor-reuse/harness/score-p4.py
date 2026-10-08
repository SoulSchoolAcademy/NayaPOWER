#!/usr/bin/env python3
"""SR-P4 scorer: one-sided Fisher exact (B > A) on related-task PASS rates.
No scipy dependency; uses math.comb for the hypergeometric tail.
Usage: score-p4.py <a_pass> <a_n> <b_pass> <b_n>
Prints rates, delta, one-sided p, and Cohen's h."""
import sys, math

def main():
    a_pass, a_n, b_pass, b_n = map(int, sys.argv[1:5])
    a_rate, b_rate = a_pass / a_n, b_pass / b_n
    delta = b_rate - a_rate
    # Hypergeometric: N = a_n + b_n, K = total passes, n = b_n draws; X = B passes.
    N, K, n = a_n + b_n, a_pass + b_pass, b_n
    def hg(k):
        return math.comb(K, k) * math.comb(N - K, n - k) / math.comb(N, n)
    p = sum(hg(k) for k in range(b_pass, min(K, n) + 1))
    # Cohen's h
    h = 2 * math.asin(math.sqrt(b_rate)) - 2 * math.asin(math.sqrt(a_rate))
    print(f"A: {a_pass}/{a_n} = {a_rate:.3f}")
    print(f"B: {b_pass}/{b_n} = {b_rate:.3f}")
    print(f"delta (B-A): {delta:+.3f}")
    print(f"one-sided Fisher exact p (B>A): {p:.6g}")
    print(f"Cohen's h: {h:.3f}")
    print(f"practical (delta>=0.20): {'YES' if delta >= 0.20 else 'NO'}")
    print(f"statistical (p<0.05): {'YES' if p < 0.05 else 'NO'}")

main()
