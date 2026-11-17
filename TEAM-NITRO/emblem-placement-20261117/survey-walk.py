#!/usr/bin/env python3
"""Survey the walk (live staged /free/walk) for official-area placements:
agreement unfold + identity. Also measure current worker gzip headroom."""
import gzip, hashlib, importlib.util, os, re, sys
sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
sys.path.insert(0, os.path.expanduser("~/workspace/ninaya/integration"))
spec = importlib.util.spec_from_file_location("certcurrent",
    os.path.expanduser("~/workspace/team-nitro/pricing-certificate-current-20261117/build-certificate.py"))
_cur = importlib.util.module_from_spec(spec); spec.loader.exec_module(_cur)
_sim = _cur._bt._sim
def sha(b): return hashlib.sha256(b if isinstance(b, bytes) else b.encode()).hexdigest()
st, _, walk = _sim.http_get("https://naya-pricing-free-staging.nayapower.workers.dev/free/walk")
print("walk GET:", st, len(walk), "B sha:", sha(walk))
w = walk.decode("utf-8")
open("base-walk.html","wb").write(walk)
print("walk sha expected 46bc52e5:", sha(walk)=="46bc52e54ac02e87cdad0ae2924ce35555671333ce3c7cd96676f17d86253fa1")
for pat in ["agreement","Agreement","collective agreement","Collective Agreement","identity","Identity","certificate","Certificate","step","showStep","data:image","<img","seal","emblem","corner"]:
    print(f"{pat}: {len(re.findall(re.escape(pat), w))}")
# step markers
print("showStep calls:", sorted(set(re.findall(r"showStep\((\d+)\)", w))))
print("step ids:", re.findall(r'id="(?:step|panel|screen)[^"]*"', w)[:30])
# agreement-ish headings
for m in re.finditer(r"(?i)(agreement|identity|certificate)[^<]{0,80}", w):
    s = m.group(0).replace("\n"," ")[:120]
    if len(s) > 12: print("  CTX:", s)
    if m.start() > 2000000: break
