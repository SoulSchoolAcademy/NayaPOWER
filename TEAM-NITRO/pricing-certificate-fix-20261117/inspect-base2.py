#!/usr/bin/env python3
"""Pricing Certificate Fix — deep inspection #2 of the reproduced tip.
Prints full regions (CSS rules + JS handlers + HTML lines) the fix edits.
No disk writes, no staging.
"""
import hashlib
import importlib.util
import os
import re
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


def rule(start_marker, what):
    print(f"\n===== {what} =====")
    print(cur.extract_rule(t, start_marker, what))


def lines_with(pat, what, before=0, after=0):
    print(f"\n===== {what} (/{pat}/) =====")
    ls = t.split("\n")
    for i, ln in enumerate(ls):
        if re.search(pat, ln):
            for j in range(max(0, i - before), min(len(ls), i + after + 1)):
                print(f"{j+1:5d}: {ls[j]}")


rule("    .cert-name { position: absolute; left: 50%; transform: translateX(-50%);",
     "cert-name base (trophy)")
lines_with(r"class=\"cert-title\"", "title HTML")
lines_with(r"This certifies that", "certifies occurrences", 1, 1)
lines_with(r"This Smart Name is yours", "welcome-back HTML", 3, 3)
lines_with(r"cert-agree", "agree lines", 0, 0)
lines_with(r"white-space:\s*nowrap", "nowrap contexts", 1, 1)
lines_with(r"keydown", "keydown lines", 0, 0)
lines_with(r"activateAndRedirect|activate\(\)|claimAlias|doClaim|submitAlias",
          "claim function refs", 0, 0)
lines_with(r"addEventListener\('click', function", "click listeners", 0, 0)
lines_with(r"@media", "media queries", 0, 0)
lines_with(r"identity-face", "identity-face rules", 0, 0)
