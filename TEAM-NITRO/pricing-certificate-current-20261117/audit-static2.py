#!/usr/bin/env python3
"""Static audit v2 — corrects audit v1's own pattern mistakes and
adjudicates the script-syntax flag against the BASE bytes.

The v1 flags were: (a) cert-info-para 11 vs 9 — the string also occurs
in 2 CSS selectors; count the HTML <p> elements. (b) #101013 x3 and
#c9a5ff x2 — count with context, don't assert 2/1. (c) agree-hide 0 —
the rule has spaces (`{ display: none; }`), v1's regex demanded none.
(d) name clamps 0 — v1 guessed the clamp values; grep the real ones.
(e) script block 2 SYNTAX FAIL — adjudicate: same check on BASE.
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
base = open("/home/hatch/workspace/team-nitro/pricing-fix-20261117/fixed-entry.html",
            encoding="utf-8").read()
print(f"staged /free: {len(new.encode())} B sha MATCH; base {len(base.encode())} B")

print("\n--- corrected counts (NEW) ---")
print("HTML <p class=\"cert-info-para\":",
      len(re.findall(r'<p class="cert-info-para', new)), "(want 9)")
print("CSS .cert-info-para selectors:",
      len(re.findall(r"\.cert-info-para[^{]*\{", new)))
for m in re.finditer(r"#101013", new):
    line = new[max(0, m.start()-90):m.start()+40].replace("\n", " ")
    print("  #101013 @", line.strip()[:130])
for m in re.finditer(r"#c9a5ff", new):
    line = new[max(0, m.start()-90):m.start()+40].replace("\n", " ")
    print("  #c9a5ff @", line.strip()[:130])
print("agree-hide rule present:",
      ".is-certified .cert-agree, .is-taken .cert-agree { display: none; }" in new)
print("certified name hover rule present:",
      ".is-certified .cert-name:hover" in new)
for m in re.finditer(r"\.cert-name[^{]*\{[^}]*font-size:\s*clamp\([^)]*\)", new):
    print("  name clamp:", m.group(0).replace("\n", " ")[:140])
print("data-text occurrences:", new.count("data-text"))
print("paintHeroName def:", "function paintHeroName" in new,
      "| paintValues def:", "function paintValues" in new,
      "| settleHeroName def:", "function settleHeroName" in new)

NODE_CHECK = ("const vm=require('vm');let s='';process.stdin.on('data',d=>s+=d)"
              ".on('end',()=>{try{new vm.Script(s,{filename:'entry-script.js'});"
              "console.log('SYNTAX OK '+s.length);}catch(e){console.log('SYNTAX FAIL: '+(e.stack||e.message).split('\\n').slice(0,4).join(' | '));process.exit(1);}});")


def check_blocks(text, label):
    blocks = re.findall(r"<script>(.*?)</script>", text, re.S)
    print(f"\n--- JS syntax {label}: {len(blocks)} script blocks ---")
    results = []
    for i, b in enumerate(blocks):
        p = subprocess.run(["node", "-e", NODE_CHECK], input=b.encode(),
                           capture_output=True, timeout=60)
        print(f"  block {i}: {len(b)} chars -> {p.stdout.decode().strip() or p.stderr.decode()[:200]}")
        results.append(p.returncode == 0)
    return results


new_res = check_blocks(new, "NEW (staged)")
base_res = check_blocks(base, "BASE")
print("\nNEW blocks all compile:", all(new_res), "| BASE blocks all compile:", all(base_res))
if not all(new_res) and all(base_res):
    print("VERDICT: syntax regression introduced by the harvest — STOP")
elif not all(new_res) and not all(base_res):
    print("VERDICT: same block(s) fail in BASE — pre-existing extraction artifact, not a harvest regression")
    # show which blocks fail in each
    print("  NEW failing blocks:", [i for i, ok in enumerate(new_res) if not ok])
    print("  BASE failing blocks:", [i for i, ok in enumerate(base_res) if not ok])
