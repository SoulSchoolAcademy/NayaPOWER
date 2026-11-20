#!/usr/bin/env python3
"""Captain's eye fix-5: fresh git blob-API reads via gh-direct.py (never contents API).
Verifies all six filed files on the fix-5 branch tip, plus the fix-4 welcome blob
for the laws base comparison. Writes eye-blob-verify.json."""
import base64, hashlib, json, subprocess, sys

GH = "/home/hatch/workspace/team-nitro/gh-direct.py"
REPO = "SoulSchoolAcademy/NayaPOWER"
BRANCH = "walkthrough/agreement-distill-fix5-20261119"
EXPECT_TIP = "f38e63402823ef884e439a9ed6e4550a7f2e296a"
PARENT_TIP = "d5003b2fd5c59e352b84169294b2773263876e01"
FIX4_BRANCH = "walkthrough/agreement-distill-fix4-20261119"
EYE = "/home/hatch/workspace/team-nitro/walkthrough-agreement-distill-fix5-20261119/eye"
EXPECT = {
  "team-nitro/agreement-unfold-fix-20261117/agreement-unfold-fixed.html": {"bytes":142532, "sha256":"a3b3907f2f80d09a14c1e7e8bfb7a00c63332a7b26ac2707912c39436e177b98", "blob":"1f0b04747e3315be6f1b619c1411e5e14fbdc1bb"},
  "team-nitro/walk-v23-assembly-20261114/welcome-staged.html": {"bytes":1930947, "sha256":"57ebe2d295b494ebe8d0e8d3c23de0a89d0025089991a7422ffa514cc4a636d6", "blob":"00082c3d65801997f1dcb035bea6ee51bf600737"},
  "team-nitro/walk-v23-assembly-20261114/walk-beginning-fixed.html": {"bytes":4363683, "sha256":"856d392c439ebb5cb97aac27f34abc3b97b52b8b6bdc55b50abac9768e198b4d", "blob":"2f7a5e3ef599e00cb39c1e577bcb42563cd7ed81"},
  "team-nitro/walk-v23-assembly-20261114/identity-fixed.html": {"bytes":404147, "sha256":"fef65d2cdbf2f1e8c096548df9adcdb465ac38a628f299c8e7cee2fb57703f52", "blob":"b3e5af088ef1d516079d96eeaa61d811d7889b8e"},
  "team-nitro/walk-v23-assembly-20261114/walk-beginning-staging-worker.js": {"bytes":8463055, "sha256":"c9bc8fedcbad3299654c85bd17832aa5a0b205e238dedf53aa98ac1f03b33586", "blob":"0413500982bc14dfbe5534cbe82cd9c75a68696a"},
  "team-nitro/walk-v23-assembly-20261114/build-v23-staging-worker.py": {"bytes":96371, "sha256":"7ce1a895051cd6e48f9c30cfde0a1b3f7392e16e9c7e5cb604d9beefb90aea77", "blob":"2299b99155e442257ca46eeb2c777ad4816ff6b0"},
}

def gh(path):
    out = subprocess.run(["python3", GH, "GET", path], capture_output=True, text=True, timeout=180)
    body = out.stdout
    i = body.find("{")
    if i < 0:
        raise RuntimeError(f"gh {path}: no JSON in output: {body[:200]} | stderr {out.stderr[:200]}")
    return json.loads(body[i:])

def get_blob(sha):
    j = gh(f"/repos/{REPO}/git/blobs/{sha}")
    if not j.get("content"):
        raise RuntimeError(f"empty blob content for {sha}")
    return base64.b64decode(j["content"].replace("\n", ""))

result = {"branch": BRANCH, "expectedTip": EXPECT_TIP, "files": {}, "errors": []}
try:
    ref = gh(f"/repos/{REPO}/git/ref/heads/{BRANCH}")
    result["refSha"] = ref["object"]["sha"]
    result["tipMatch"] = result["refSha"] == EXPECT_TIP
    commit = gh(f"/repos/{REPO}/git/commits/{result['refSha']}")
    result["parents"] = [p["sha"] for p in commit.get("parents", [])]
    result["parentMatch"] = PARENT_TIP in result["parents"]
    tree = gh(f"/repos/{REPO}/git/trees/{commit['tree']['sha']}?recursive=1")
    by_path = {e["path"]: e for e in tree.get("tree", [])}
    for p, exp in EXPECT.items():
        ent = by_path.get(p)
        rec = {"treeBlob": ent["sha"] if ent else None, "treeSize": ent.get("size") if ent else None,
               "expectedBlob": exp["blob"], "blobMatch": ent["sha"] == exp["blob"] if ent else None}
        try:
            buf = get_blob(exp["blob"])
            rec["bytes"] = len(buf)
            rec["sha256"] = hashlib.sha256(buf).hexdigest()
            rec["bytesMatch"] = len(buf) == exp["bytes"]
            rec["shaMatch"] = rec["sha256"] == exp["sha256"]
            gh1 = hashlib.sha1(b"blob %d\0" % len(buf) + buf).hexdigest()
            rec["gitHashMatch"] = gh1 == exp["blob"]
            with open(f"{EYE}/work/eye-fix5-" + p.split("/")[-1], "wb") as f:
                f.write(buf)
        except Exception as e:
            rec["error"] = str(e)[:300]
            result["errors"].append(p + ": " + str(e)[:200])
        result["files"][p] = rec
except Exception as e:
    result["errors"].append("top: " + str(e)[:300])

# fix-4 welcome blob for the laws base comparison
try:
    ref4 = gh(f"/repos/{REPO}/git/ref/heads/{FIX4_BRANCH}")
    result["fix4Tip"] = ref4["object"]["sha"]
    result["fix4TipMatch"] = result["fix4Tip"] == PARENT_TIP
    c4 = gh(f"/repos/{REPO}/git/commits/{result['fix4Tip']}")
    t4 = gh(f"/repos/{REPO}/git/trees/{c4['tree']['sha']}?recursive=1")
    by4 = {e["path"]: e for e in t4.get("tree", [])}
    wp = "team-nitro/walk-v23-assembly-20261114/welcome-staged.html"
    ent4 = by4.get(wp)
    result["fix4WelcomeBlob"] = ent4["sha"] if ent4 else None
    result["fix4WelcomeSize"] = ent4.get("size") if ent4 else None
    buf4 = get_blob(ent4["sha"])
    result["fix4WelcomeBytes"] = len(buf4)
    result["fix4WelcomeSha256"] = hashlib.sha256(buf4).hexdigest()
    with open(f"{EYE}/work/eye-fix4-welcome-staged.html", "wb") as f:
        f.write(buf4)
except Exception as e:
    result["errors"].append("fix4: " + str(e)[:300])

with open(f"{EYE}/work/eye-blob-verify.json", "w") as f:
    json.dump(result, f, indent=1)
print(json.dumps(result, indent=1)[:6000])
print("WROTE eye-blob-verify.json")
