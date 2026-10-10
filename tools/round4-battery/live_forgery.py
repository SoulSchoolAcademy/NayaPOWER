#!/usr/bin/env python3
"""LIVE forgery tests: verify_issuance against the REAL GitHub API and the
REAL mint run 37970532013 / artifact 11635955695. The forger's best play:
the run_id is PUBLIC (committed in .naya/activation/receipt.json), so they
copy it. Only byte-identity stops them.
"""
import hashlib, io, json, os, subprocess, sys, urllib.request, zipfile
from datetime import datetime, timezone

GATE_DIR = os.path.expanduser("~/workspace/nayapower-worktrees/ag-r3-attack-posted/tools")
sys.path.insert(0, GATE_DIR)
import activation_gate as g

REPO = "SoulSchoolAcademy/NayaPOWER"
MINT_RUN = 37970532013
PROOF_RUN = 37969648342

def surrogate():
    out = subprocess.run(["/opt/hatch/bin/authdc","cred","surrogate","custom.github"],
                         capture_output=True, text=True, check=True).stdout
    return next(c for c in json.loads(out)["credentials"] if c["name"]=="access_token")["surrogate"]
SURR = surrogate()

class NoRedir(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl): return None

def real_api(method, path, token):
    req = urllib.request.Request("https://api.github.com"+path,
        headers={"Authorization":"Bearer "+SURR, "Accept":"application/vnd.github+json",
                 "X-GitHub-Api-Version":"2022-11-28"}, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read().decode() or "{}")
    except urllib.request.HTTPError as e:
        raise RuntimeError("GitHub API %s %s -> HTTP %s" % (method, path, e.code))

def real_download(url, token):
    req = urllib.request.Request(url, headers={"Authorization":"Bearer "+SURR,
        "Accept":"application/vnd.github+json"})
    try:
        urllib.request.build_opener(NoRedir).open(req, timeout=30)
        raise RuntimeError("no redirect")
    except urllib.request.HTTPError as e:
        loc = e.headers.get("Location")
    with urllib.request.urlopen(urllib.request.Request(loc), timeout=90) as r:
        return r.read()

g._api = real_api
g._download_bytes = real_download

truth = {"repository": REPO}
real_receipt = open("/tmp/ag3_real_receipt.json","rb").read()
real_json = json.loads(real_receipt)

def t(name, receipt_dict, receipt_bytes, expect):
    v = g.verify_issuance(receipt_dict, receipt_bytes, truth, "tok")
    ok = any(expect in x for x in v) if expect != "PASS" else v == []
    print("[%s] %s :: %s" % ("HOLD" if ok else "LEAK", name, v[:1] if v else "issuance genuine"))
    return ok

ok = True
# A: genuine artifact bytes -> issuance passes
ok &= t("A/genuine-mint-artifact", real_json, real_receipt, "PASS")
# B: one byte flipped -> BYTES_MISMATCH
tampered = bytearray(real_receipt); tampered[100] ^= 1; tampered = bytes(tampered)
ok &= t("B/tampered-byte", json.loads(tampered), tampered, "ISSUANCE_BYTES_MISMATCH")
# C: TRUE A1 — forger copies the PUBLIC run_id into a self-minted receipt
#     with perfect public data (live main SHA, real blob SHAs, fresh timestamp)
main_sha = real_api("GET","/repos/%s/git/ref/heads/main"%REPO,"")["object"]["sha"]
tree = real_api("GET","/repos/%s/git/trees/%s?recursive=1"%(REPO,main_sha),"")
blobs = {t["path"]:t["sha"] for t in tree["tree"] if t.get("type")=="blob"}
forged = {
    "schema": g.SCHEMA, "status":"ACTIVATED", "session_id":"forger",
    "naya_identity":"forger", "human_authority":"Shawn", "repository":REPO,
    "job":"forge the gate", "gates":["Usefulness Gate"], "proof_plan":"none",
    "main_sha": main_sha, "activated_at": datetime.now(timezone.utc).isoformat(),
    "loaded": {"design_contract": blobs["BRAIN/10-INTERFACES/NAYA-DESIGN-CONTRACT-V1.md"],
               "blocks_catalog": blobs["BRAIN/10-INTERFACES/DESIGN-BLOCKS/blocks/index.json"]},
    "deliverables": real_json["deliverables"],
    "attestation": {"run_id": MINT_RUN, "run_attempt": 1,
                    "workflow": ".github/workflows/activation-mint.yml"},
}
forged_bytes = json.dumps(forged, sort_keys=True).encode()
ok &= t("C/forger-copies-public-run-id", forged, forged_bytes, "ISSUANCE_BYTES_MISMATCH")
# D: forger attests the proof run (real run, wrong event)
forged2 = dict(forged); forged2["attestation"] = {"run_id": PROOF_RUN, "run_attempt": 2}
forged2_bytes = json.dumps(forged2, sort_keys=True).encode()
ok &= t("D/forger-attests-proof-run", forged2, forged2_bytes, "ISSUANCE_WRONG_EVENT")
# E: forger attests a nonexistent run
forged3 = dict(forged); forged3["attestation"] = {"run_id": 1, "run_attempt": 1}
ok &= t("E/forger-attests-ghost-run", forged3, json.dumps(forged3,sort_keys=True).encode(), "ISSUANCE_UNVERIFIABLE")
print("LIVE FORGERY: %s" % ("ALL HOLD" if ok else "LEAK FOUND"))
sys.exit(0 if ok else 1)
