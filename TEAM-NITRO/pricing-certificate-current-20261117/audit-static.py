#!/usr/bin/env python3
"""Static audit of the STAGED /free bytes (fetched live, sha-verified),
plus a Node syntax check of every <script> block (vm.Script compile,
no disk writes — the EPERM flake blocks temp files).

Acceptance items that are static: sentence, reader, paint engine,
obsidian panels, token lift, clone, agree hide rules, taken shadow,
zero cut tokens, geometry kept, named non-harvests absent.
"""
import hashlib
import importlib.util
import os
import re
import subprocess
import sys

sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
sys.path.insert(0, os.path.expanduser("~/workspace/ninaya/integration"))

spec2 = importlib.util.spec_from_file_location(
    "btaken", "/home/hatch/workspace/team-nitro/pricing-taken-state-fix-20261117/build-taken-fix.py")
_bt = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(_bt)
_sim = _bt._sim

WANT = "1e1bb4894b3e4bffed026781ac08976e8353b0e2bb020652357f567a711b16a3"
st, _, got = _sim.http_get(
    "https://naya-pricing-free-staging.nayapower.workers.dev/free")
assert st == 200
new = got.decode("utf-8")
assert hashlib.sha256(new.encode()).hexdigest() == WANT, "staged /free moved"
print(f"staged /free: {len(new.encode())} B, sha MATCH")

SENTENCE = ("By entering your name, you make it official \u2014 you are signing "
            "the Collective Agreement, and you get the deed to your own world: "
            "high-level digital real estate \u2014 your personal page, your "
            "business, your space \u2014 free forever.")


def c(pat, label, want=None):
    n = len(re.findall(pat, new))
    flag = ""
    if want is not None:
        flag = "  <-- EXPECTED %s" % want if n != want else "  OK"
    print(f"{label}: {n}{flag}")
    return n


print("\n--- harvest present ---")
c(re.escape(SENTENCE), "official sentence (exact)", 1)
c(r'<p class="cert-info-para', "cert-info-para <p> elements", 9)
c(r"\.cert-info-para[^{]*\{", "cert-info-para CSS selectors", 2)
c(r"function paintHeroName", "paintHeroName", 1)
c(r"function paintValues", "paintValues", 1)
c(r"function settleHeroName", "settleHeroName", 1)
c(r"#101013", "obsidian panel gradient start", 3)
c(r"--silver: #ffffff", "--silver white", 1)
c(r"data-text", "data-text (clone) occurrences")
c(r"content: attr\(data-text\)", "clone content rule", 1)
c(r"#c9a5ff", "clone purple gradient start", 2)
c(r"\.cert-plaque\.is-certified \.cert-agree \{ display: none; \}", "agree hidden on certified", 1)
c(r"\.face-foot:has\(\.alias-status\[data-state=\"taken\"\]\) \.cert-agree \{ display: none; \}", "agree hidden on taken", 1)
c(r"text-shadow: none", "taken text-shadow none")
c(r"Marcellus", "Marcellus occurrences")
c(r"font-size: clamp\(2\.4rem, 6\.4vw, 4\.1rem\)", "name size clamp desktop (geometry kept)", 1)
c(r"font-size: clamp\(2\.55rem, 13\.5vw, 3\.4rem\)", "name size clamp phone (geometry kept)", 1)
c(r"\}\)\(\);", "IIFE closers })(); (reader + name-click)", 2)

print("\n--- cut tokens: must be ZERO ---")
c(r"#f2f2f6", "#f2f2f6 (silver token)", 0)
c(r"#a8dcff", "#a8dcff (blue label)", 0)
c(r"#ffd97a", "#ffd97a (gold label)", 0)
c(r"#163a56", "#163a56 (blue panel)", 0)
c(r"#3a2a09", "#3a2a09 (brown panel)", 0)
c(r"#a855f7", "#a855f7 (second purple)", 0)
c(r"245,241,232", "cream rgba (245,241,232)", 0)
c(r"Newsreader", "Newsreader", 0)
c(r"rgba\(242,242,246", "faint rgba(242,242,246)", 0)

print("\n--- named non-harvests (absent by decision) ---")
c(r"has signed the Collective Agreement", "membership sentence", 0)
c(r"taken-note", "H6 green taken message", 0)
c(r"cert-more", ".cert-more unfold", 0)

print("\n--- JS syntax (node vm.Script compile, per <script> block) ---")
blocks = re.findall(r"<script>(.*?)</script>", new, re.S)
print(f"script blocks: {len(blocks)}")
NODE_CHECK = ("const vm=require('vm');let s='';process.stdin.on('data',d=>s+=d)"
              ".on('end',()=>{try{new vm.Script(s,{filename:'entry-script.js'});"
              "console.log('SYNTAX OK '+s.length);}catch(e){console.log('SYNTAX FAIL: '+e.message);process.exit(1);}});")
ok = True
for i, b in enumerate(blocks):
    p = subprocess.run(["node", "-e", NODE_CHECK], input=b.encode(),
                       capture_output=True, timeout=60)
    out = p.stdout.decode().strip()
    print(f"  block {i}: {len(b)} chars -> {out or p.stderr.decode()[:200]}")
    ok = ok and p.returncode == 0
print("ALL SCRIPT BLOCKS COMPILE:", ok)
assert ok, "JS syntax failure — STOP"
print("\nSTATIC AUDIT DONE")
