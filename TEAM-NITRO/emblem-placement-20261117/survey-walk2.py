#!/usr/bin/env python3
"""Survey walk steps + identity page structure for official-area placements."""
import hashlib, importlib.util, os, re, sys
sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
sys.path.insert(0, os.path.expanduser("~/workspace/ninaya/integration"))
spec = importlib.util.spec_from_file_location("certcurrent",
    os.path.expanduser("~/workspace/team-nitro/pricing-certificate-current-20261117/build-certificate.py"))
_cur = importlib.util.module_from_spec(spec); spec.loader.exec_module(_cur)
_sim = _cur._bt._sim
def sha(b): return hashlib.sha256(b if isinstance(b, bytes) else b.encode()).hexdigest()
w = open("base-walk.html", encoding="utf-8", errors="ignore").read()
# step headings: find h1/h2 inside each step section
for m in re.finditer(r'id="step-([^"]+)"', w):
    seg = w[m.start():m.start()+3000]
    heads = re.findall(r"<h[12][^>]*>(.*?)</h[12]>", seg, re.S)
    heads = [" ".join(re.sub(r"<[^>]+>"," ",h).split())[:90] for h in heads][:3]
    print(f"STEP {m.group(1)}: {heads}")
print("=== door/end ===")
for m in re.finditer(r'id="step-(door|end|building)"', w):
    seg = w[m.start():m.start()+2500]
    txt = " ".join(re.sub(r"<[^>]+>"," ", seg).split())[:400]
    print(m.group(1).upper(), ":", txt[:400])
print("=== congrats ===")
i = w.find("p3-congrats")
print(w[max(0,i-500):i+1500].replace("\n"," ")[:2000] if i>=0 else "no p3-congrats")
print("=== identity page ===")
st, _, ident = _sim.http_get("https://naya-walk-beginning-staging.nayapower.workers.dev/identity.html")
print("identity GET:", st, len(ident), "B sha:", sha(ident))
open("base-identity.html","wb").write(ident)
iw = ident.decode("utf-8", errors="ignore")
for pat in ["corner","crest","medal","frame-light","<img","data:image","seal","emblem","title","h1"]:
    print(f"identity {pat}: {len(re.findall(re.escape(pat), iw))}")
