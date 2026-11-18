#!/usr/bin/env python3
"""Pricing Certificate Fix — deep inspection #3: print exact line ranges
of the reproduced tip (layout, keydown, claim, HTML). No writes, no staging.
"""
import hashlib
import importlib.util
import os
import sys

CUR = os.path.expanduser("~/workspace/team-nitro/pricing-certificate-current-20261117")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def sha(b):
    return hashlib.sha256(b if isinstance(b, bytes) else b.encode()).hexdigest()


cur = load("certcurrent", os.path.join(CUR, "build-certificate.py"))
walk_pf, entry_pf = cur.regen_pricing_fix_tip()
h = cur.harvest_identity()
t = cur.apply_certificate(entry_pf, h)
assert sha(t) == "1e1bb4894b3e4bffed026781ac08976e8353b0e2bb020652357f567a711b16a3"
ls = t.split("\n")


def show(a, b, label):
    print(f"\n===== {label} (lines {a}-{b}) =====")
    for j in range(a - 1, min(b, len(ls))):
        print(f"{j+1:5d}: {ls[j]}")


show(280, 330, "plaque + identity-face base")
show(420, 445, "short-viewport media")
show(1007, 1044, "640 media block 1")
show(1085, 1130, "641+ media block")
show(1190, 1230, "640/700 media + taken name")
show(1295, 1360, "certificate HTML")
show(1570, 1625, "keydown handler + name click")
show(1690, 1720, "setStatus")
show(1840, 1960, "activateAndRedirect + claimAlias")
