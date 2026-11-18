#!/usr/bin/env python3
"""Pricing Certificate Fix — inspect the current base entry (tip 1e1bb489)
in memory. Reproduces the tip through the filed build chain, asserts the
sha, then prints the regions the fix touches. No disk writes, no staging.
"""
import hashlib
import importlib.util
import os
import re
import sys

HERE = os.path.expanduser("~/workspace/team-nitro/pricing-certificate-fix-20261117")
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
new_entry = cur.apply_certificate(entry_pf, h)
print(f"reproduced entry: {len(new_entry.encode())} B sha256={sha(new_entry)}")
assert sha(new_entry) == "1e1bb4894b3e4bffed026781ac08976e8353b0e2bb020652357f567a711b16a3", \
    "tip NOT reproduced — STOP"


def show(pat, label, ctx=0, limit=12):
    ms = list(re.finditer(pat, new_entry))
    print(f"\n### {label}: {len(ms)} hit(s)")
    for m in ms[:limit]:
        s = max(0, m.start() - ctx)
        e = min(len(new_entry), m.end() + ctx)
        print("  ...", new_entry[s:e].replace("\n", " | ")[:600])


show(r"CERTIFICATE OF [A-Z ]+", "title strings")
show(r"This certifies that", "certifies line")
show(r"This Smart Name is yours", "welcome-back line")
show(r"By entering your name, you make it official", "official sentence")
show(r"cert-seal|logo-hero|five stones|cert-stone|gem", "seal / stones / gems")
show(r"class=\"cert-title\"|cert-title", "title element class")
show(r"\.cert-name \{[^}]*\}", "cert-name base rule")
show(r"\.cert-plaque\.is-certified \.cert-name \{[^}]*\}", "certified name rule")
show(r"\.cert-name::before \{[^}]*\}", "clone before body")
show(r"\.cert-name::before \{ z-index[^}]*\}", "clone before paint")
show(r"\.cert-name::after[^}]*\}", "clone after rules")
show(r"\.cert-agree \{[^}]*\}", "agree rule")
show(r"is-certified \.cert-agree[^}]*\}", "agree hidden certified")
show(r"@media \(max-width: 640px\) \{[^}]*\.cert-agree[^}]*\}", "agree 640 media")
show(r"keydown|key === 'Enter'|key==='Enter'|e\.key", "Enter key handling")
show(r"function activateAndRedirect", "claim function")
show(r"white-space:\s*nowrap", "nowrap rules")
show(r"\.face-foot \{[^}]*\}", "face-foot rule")
show(r"\.cert-plaque \{[^}]*\}", "plaque rule")
show(r"overflow[^;]*;", "overflow declarations (first 25)", limit=25)
show(r"data-state", "data-state refs")
show(r"alias-status", "alias-status refs")
print("\n### counts")
for pat in ["CERTIFICATE OF SMART IDENTITY", "CERTIFICATE OF AGREEMENT",
            "CERTIFICATE OF THE COLLECTIVE AGREEMENT", "This certifies that",
            "Collective Agreement", "color: transparent",
            "text-shadow: none", "background-clip: text", "-webkit-text-stroke",
            "paintHeroName(", "settleHeroName(", "is-certified"]:
    print(f"  {pat!r}: {new_entry.count(pat)}")
