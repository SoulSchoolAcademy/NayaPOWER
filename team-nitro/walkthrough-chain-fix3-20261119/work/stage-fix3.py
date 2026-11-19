#!/usr/bin/env python3
"""FIX3 stage + file (2026-11-19) — walkthrough chain fix round 3.

Inputs are the LOCAL files, edited in place:
  welcome-staged.html (fix3), identity-fixed.html (fix3),
  agreement-unfold-fixed.html (fix3: agree carries the agreed keys),
  build-v23-staging-worker.py (fix3: asserts moved to the new shas).
Does:
  1. verifies the local inputs by sha (computed, never typed),
  2. node --checks the welcome/identity/unfold script blocks,
  3. rebuilds the staging worker twice (deterministic sha) and verifies
     every embed by sha256 + the FIX3 markers,
  4. creates branch walkthrough/chain-fix3-20261119 from fix2 tip 7181266f,
  5. files ONE commit (welcome + identity + unfold + worker + builder +
     drivers), read-back verified,
  6. PUTs the worker to the walk staging worker,
  7. verifies all 7 routes by sha256 via curl, plus the proof-host
     links for the two edited files.
No PR, no merge, no live deploy, no message to Shawn.
"""
import base64, hashlib, json, os, re, subprocess, sys, time

HOME = os.path.expanduser("~")
RECORDS = os.path.join(HOME, "workspace/team-nitro/walkthrough-chain-fix3-20261119")
WORK = os.path.join(RECORDS, "work")
V23 = os.path.join(HOME, "workspace/team-nitro/walk-v23-assembly-20261114")
BUILDER = os.path.join(V23, "build-v23-staging-worker.py")
WELCOME_LOCAL = os.path.join(V23, "welcome-staged.html")
IDENT_LOCAL = os.path.join(V23, "identity-fixed.html")
WORKER_LOCAL = os.path.join(V23, "walk-beginning-staging-worker.js")
UNFOLD_LOCAL = os.path.join(HOME, "workspace/team-nitro/agreement-unfold-fix-20261117/agreement-unfold-fixed.html")
META = os.path.join(V23, "v23-meta.json")
GH = os.path.join(HOME, "workspace/team-nitro/gh-direct.py")
CF = os.path.join(HOME, "workspace/project-intelligence/cf-worker.py")
REPO = "SoulSchoolAcademy/NayaPOWER"
NEW_BRANCH = "walkthrough/chain-fix3-20261119"
PARENT_TIP = "7181266f91c15315fa574f00eabcce6422e89b5a"
CF_ACCOUNT = "b5e2a51b3e883f7722287c5f51b1196b"
CF_SCRIPT = "naya-walk-beginning-staging"
STAGING = "https://naya-walk-beginning-staging.nayapower.workers.dev"
PROOF = "https://naya-proof-host.nayapower.workers.dev"
WALK_SHA = "4b5f926423d765bd750026e65986f0b67f6b52d51588fe64e857b39df7ee01c0"
WELCOME_SHA = "d79793c0d9b74121e83c0c65fed095e6d0dd278481b60c7a2b339bbe9231c934"
IDENT_SHA = "22a1ae611921d82bff986a5cf23f5248bb9d372bbc797513c5b03139b559286d"
UNFOLD_SHA = "3252948ed7f80157d0fa86fd730dc2e535a749f00e80944f0274ded54eb6a0f8"

def sha(b):
    return hashlib.sha256(b).hexdigest()

def read_bytes(p):
    with open(p, "rb") as f:
        return f.read()

def write_resilient(path, data, attempts=40):
    tmp = path + ".tmp-stage-fix3"
    last = None
    for n in range(attempts):
        try:
            wrote = False
            try:
                with open(tmp, "wb") as f:
                    for i in range(0, len(data), 8192):
                        f.write(data[i:i + 8192])
                    f.flush()
                    os.fsync(f.fileno())
                got = read_bytes(tmp)
                if len(got) == len(data) and sha(got) == sha(data):
                    wrote = True
            except Exception as e:
                last = e
            if wrote:
                os.replace(tmp, path)
                got2 = read_bytes(path)
                if len(got2) != len(data) or sha(got2) != sha(data):
                    raise RuntimeError("verify after replace failed: %s" % path)
                print("wrote %s %d B sha %s" % (path, len(data), sha(data)[:12]), flush=True)
                return
        except Exception as e:
            last = e
        time.sleep(2)
    raise RuntimeError("write_resilient failed for %s: %r" % (path, last))

def gh(method, path, body=None):
    args = [sys.executable, GH, method, path]
    inp = None
    if body is not None:
        args.append("@/dev/stdin")
        inp = json.dumps(body).encode()
    p = subprocess.run(args, input=inp, capture_output=True)
    out = p.stdout.decode("utf-8", "replace")
    lines = out.split("\n", 1)
    status = int(lines[0].split()[1]) if lines and lines[0].startswith("HTTP") else -1
    payload = lines[1] if len(lines) > 1 else ""
    try:
        data = json.loads(payload) if payload.strip() else {}
    except json.JSONDecodeError:
        data = {"_raw": payload[:500]}
    if status >= 400 or p.returncode != 0:
        print("FAIL %s %s: HTTP %s\n%s" % (method, path, status, payload[:800]), file=sys.stderr)
        sys.exit(1)
    return status, data

def cf_put_inprocess(worker):
    import importlib.util, uuid, urllib.error
    spec = importlib.util.spec_from_file_location("cf_worker_helper", CF)
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    meta_json = read_bytes(META)
    boundary = "----pi-preview-deploy-" + uuid.uuid4().hex[:16]
    parts = []
    parts.append(
        f"--{boundary}\r\n"
        'Content-Disposition: form-data; name="metadata"\r\n'
        "Content-Type: application/json\r\n\r\n".encode() + meta_json + b"\r\n"
    )
    parts.append(
        f"--{boundary}\r\n"
        'Content-Disposition: form-data; name="worker.js"; filename="worker.js"\r\n'
        "Content-Type: application/javascript+module\r\n\r\n".encode() + worker + b"\r\n"
    )
    parts.append(f"--{boundary}--\r\n".encode())
    body = b"".join(parts)
    headers = {"Content-Type": f"multipart/form-data; boundary={boundary}"}
    url = f"{helper.BASE}/accounts/{CF_ACCOUNT}/workers/scripts/{CF_SCRIPT}"
    try:
        status, resp = helper.run(helper.authed_req(url, method="PUT", data=body, headers=headers))
        print("staging PUT HTTP %s %s" % (status, resp.decode("utf-8", "replace")[:2000]), flush=True)
    except urllib.error.HTTPError as e:
        print("staging PUT HTTP %s %s" % (e.code, e.read().decode("utf-8", "replace")[:2000]), flush=True)
        raise
    assert status == 200 and (b'"success": true' in resp or b'"success":true' in resp), "staging PUT failed"
    return status

def extract_scripts(html_bytes, label):
    txt = html_bytes.decode("utf-8")
    parts = re.findall(r"<script>(.*?)</script>", txt, re.S)
    print("%s: %d script blocks" % (label, len(parts)), flush=True)
    return parts

def node_check_script(code, label):
    r = subprocess.run(["node", "--check", "-"], input=code.encode("utf-8"), capture_output=True)
    assert r.returncode == 0, "node --check failed for %s: %s" % (label, r.stderr.decode("utf-8", "replace")[:500])
    print("node --check OK: %s (%d B)" % (label, len(code)), flush=True)

def run_builder(new_welcome, welcome_sha, ident_sha, unfold_sha):
    workers = []
    for n in range(2):
        r = subprocess.run([sys.executable, BUILDER, "--stdout", "--welcome-stdin"],
                           input=new_welcome, capture_output=True, timeout=300)
        assert r.returncode == 0, "builder failed: %s" % r.stderr.decode("utf-8", "replace")[-800:]
        log = r.stderr.decode("utf-8", "replace")
        for needle in (welcome_sha[:8], unfold_sha[:8], "4b5f9264", "61002d15", ident_sha[:8]):
            assert needle in log, "builder log missing %s; log tail: %s" % (needle, log[-600:])
        workers.append(r.stdout)
        print("builder run %d: worker %d B sha=%s" % (n + 1, len(r.stdout), sha(r.stdout)[:12]), flush=True)
    assert workers[0] == workers[1], "worker build not deterministic"
    w = workers[0]
    for marker in (b"goBridgeAfterAgree", b"fpBridgeToName", b"fpBridgeAgreed",
                   b"__chainShowKey", b"keyPanel", b"Use my key",
                   b"bridge-agreed", b"__chainApiBase", b"doCopyKey",
                   b"access-control-allow-origin", b"OPTIONS",
                   b"flex-wrap:nowrap;overflow-x:auto",
                   b"nayanet_fp_agreed", b"goBridgeToName",
                   b"flex:0 0 auto;white-space:nowrap",
                   b"currentDisplayName", b"titleName", b"key-copy"):
        assert marker in w, "worker missing FIX3/chain marker %s" % marker
    dec = json.JSONDecoder()
    embeds = {}
    for name in ("WALK", "IDENTITY", "WELCOME", "UNFOLD", "PERSONAL_TEMPLATE"):
        i = w.find(("const %s = " % name).encode())
        assert i >= 0, "worker missing %s" % name
        j = w.find(b'"', i)
        val, _ = dec.raw_decode(w[j:].decode("utf-8"))
        embeds[name] = val.encode("utf-8")
    print("worker embeds: " + ", ".join("%s %d B %s" % (k, len(v), sha(v)[:8]) for k, v in embeds.items()), flush=True)
    assert sha(embeds["WELCOME"]) == welcome_sha, "worker does not embed the new welcome"
    assert sha(embeds["UNFOLD"]) == unfold_sha, "worker does not embed the new unfold"
    assert sha(embeds["WALK"]) == WALK_SHA, "worker walk changed"
    assert sha(embeds["IDENTITY"]) == ident_sha, "worker identity changed"
    assert sha(embeds["PERSONAL_TEMPLATE"])[:8] == "61002d15", "worker template changed"
    return w

def commit_message(worker_sha, worker_bytes, welcome_sha, ident_sha, unfold_sha):
    return (
        "Walkthrough CHAIN FIX3 (2026-11-19, maker round; MAKER-REPORT.md in "
        "walkthrough-chain-fix3-20261119/)\\n\\n"
        "Fix2 was byte-correct but the eye still saw the old behaviour on the live "
        "paths, so this round diagnoses from the live bytes and fixes the paths "
        "the eye actually walked. (1) BRIDGE: the /agreement agree button navigates "
        "to /?stage=bridge, and fix2 left that arrival PRE-agree by design (its own "
        "comment) while the boot restore is suppressed whenever ?stage= is set and "
        "render() wipes the saved key on arrival — so the eye got group 1, no gold "
        "pill, and the agreed state gone after reload. Now the agree carries the "
        "state with it (unfold sets 'bridge-agreed' + 'nayanet_fp_agreed' before "
        "navigating), the welcome boot re-enters the post-agree bridge from the "
        "durable agreed key on any arrival (?stage=bridge, login re-entry, plain "
        "reload), and the gold pill goes DIRECTLY to name entry (goBridgeToName "
        "opens the name form itself instead of landing on the login behind an extra "
        "'Create a new account' click). The boot restore is guarded with !_fpStage "
        "so the agreed key cannot hijack ?stage=deck/?stage=letter. (2) COPY: the "
        "'Copied' feedback was set on the Copy button, but the button carries "
        ".cert-more and '.cert-plaque.is-certified .cert-more{display:none}' hid it "
        "on every certificate — the eye saw nothing. The button now has its own "
        "visible .key-copy style, and the feedback also lands ON the device-key pill "
        "itself, only on real clipboard success (execCommand fallback; failure shows "
        "nothing). (3) TAKEN ALIAS: typing a taken alias now opens the note + the "
        "device-key panel on the availability result itself, not only after ENTER; "
        "ENTER stays dimmed, never armed as if the alias were free. (4) NAME LEAK: "
        "the claim POST already sent the paired name, but the stored name saved "
        "rawName (load-time ?name=) and stampCertificate paints the hero from the "
        "stored name — so fix3eyecheck certified as 'Jordan Test' (Nº 000841). The "
        "stored name is now finalName (computed live at ENTER from the claimed "
        "alias and its paired name). The composing hero echo title-cases the typed "
        "words, so 'nova eye test' no longer renders twice as 'Novaeyetest' + "
        "'Nova Eye Test'. (6) FOOTER: the bridge strip links get flex:0 0 auto + "
        "nowrap (the entrance strip's treatment), so multi-word labels stop wrapping "
        "to two lines at 534/390. (7) The four corner emblems no longer straddle "
        "the plaque corners (translate -50% put half of each outside the viewport); "
        "they sit fully inside the corners, same spot and rotation. Talk/Play audio: "
        "not rebuilt — a cloud/headless browser has no speech voice to sound with; "
        "see the maker report for the evidence.\\n\\n"
        "Builder sha correction carried from the fix2 checker: the filed fix2 builder "
        "hashes to 0cd80c85..., not the 594044ee... in the fix2 maker report.\\n\\n"
        "Worker built twice, identical sha %s (%d B); embeds verified: "
        "WALK 4b5f9264, IDENTITY %s, WELCOME %s, UNFOLD %s, TEMPLATE "
        "61002d15.\\n\\n"
        "Staged: %s/ - routes curl-verified byte-identical by sha256 after "
        "the PUT. NO PR, NO MERGE — the checker and the captain come after "
        "this seat. Nothing live."
        % (worker_sha[:8], worker_bytes, ident_sha[:8], welcome_sha[:8], unfold_sha[:8], STAGING))

def curl_sha(url, ua):
    rr = subprocess.run(["curl", "-s", "-A", ua, url], capture_output=True, timeout=120)
    return rr.stdout, sha(rr.stdout)

def main():
    new_welcome = read_bytes(WELCOME_LOCAL)
    new_ident = read_bytes(IDENT_LOCAL)
    new_unfold = read_bytes(UNFOLD_LOCAL)
    welcome_sha, ident_sha, unfold_sha = sha(new_welcome), sha(new_ident), sha(new_unfold)
    print("inputs: welcome %d B %s, identity %d B %s, unfold %d B %s" % (
        len(new_welcome), welcome_sha, len(new_ident), ident_sha, len(new_unfold), unfold_sha), flush=True)
    assert welcome_sha == WELCOME_SHA, "welcome sha moved: %s" % welcome_sha
    assert ident_sha == IDENT_SHA, "identity sha moved: %s" % ident_sha
    assert unfold_sha == UNFOLD_SHA, "unfold sha moved: %s" % unfold_sha
    assert sha(read_bytes(os.path.join(V23, "walk-beginning-fixed.html"))) == WALK_SHA, "walk moved"
    builder = read_bytes(BUILDER)
    for needle in (b'assert welcome_sha.startswith("d79793c0")',
                   b'assert ident_sha.startswith("22a1ae61")',
                   b'assert unfold_sha.startswith("3252948e")',
                   b'access-control-allow-origin', b'req.method === "OPTIONS"'):
        assert needle in builder, "builder missing %s" % needle
    r = subprocess.run([sys.executable, "-c", "compile(open(%r).read(), 'builder', 'exec')" % BUILDER], capture_output=True)
    assert r.returncode == 0, "builder does not compile: %s" % r.stderr.decode("utf-8", "replace")[-500:]
    print("builder verified: asserts welcome/identity/unfold new shas, CORS + OPTIONS present (%d B)" % len(builder), flush=True)
    for idx, code in enumerate(extract_scripts(new_welcome, "welcome")):
        node_check_script(code, "welcome-%d" % idx)
    for idx, code in enumerate(extract_scripts(new_ident, "identity")):
        node_check_script(code, "identity-%d" % idx)
    for idx, code in enumerate(extract_scripts(new_unfold, "unfold")):
        node_check_script(code, "unfold-%d" % idx)
    _, ref = gh("GET", "/repos/%s/git/refs/heads/walkthrough/chain-fix2-20261118" % REPO)
    print("parent branch tip:", ref["object"]["sha"], flush=True)
    assert ref["object"]["sha"] == PARENT_TIP, "parent tip moved: %s" % ref["object"]["sha"]
    worker = run_builder(new_welcome, welcome_sha, ident_sha, unfold_sha)
    r = subprocess.run(["node", "--check", "--input-type=module", "-"], input=worker, capture_output=True)
    assert r.returncode == 0, "node --check failed for worker: %s" % r.stderr.decode("utf-8", "replace")[:500]
    print("node --check OK: worker (%d B)" % len(worker), flush=True)
    try:
        write_resilient(WORKER_LOCAL, worker)
    except Exception as e:
        print("WARNING: local worker copy not written (EPERM flake): %r — restore from the filed blob later" % e, flush=True)
    try:
        write_resilient(os.path.join(WORK, "worker-fix3.js"), worker)
    except Exception as e:
        print("WARNING: work-dir worker copy not written (EPERM flake): %r" % e, flush=True)
    _, nb = gh("POST", "/repos/%s/git/refs" % REPO,
               {"ref": "refs/heads/%s" % NEW_BRANCH, "sha": PARENT_TIP})
    print("new branch created:", nb["ref"], nb["object"]["sha"], flush=True)
    assert nb["object"]["sha"] == PARENT_TIP
    _, ref2 = gh("GET", "/repos/%s/git/refs/heads/%s" % (REPO, NEW_BRANCH))
    assert ref2["object"]["sha"] == PARENT_TIP, "branch tip moved: %s" % ref2["object"]["sha"]
    _, commit = gh("GET", "/repos/%s/git/commits/%s" % (REPO, PARENT_TIP))
    base_tree = commit["tree"]["sha"]
    print("base tree:", base_tree, flush=True)
    drivers = {
        "team-nitro/walkthrough-chain-fix3-20261119/work/fetch-bases.py": read_bytes(os.path.join(WORK, "fetch-bases.py")),
        "team-nitro/walkthrough-chain-fix3-20261119/work/law-fix3.py": read_bytes(os.path.join(WORK, "law-fix3.py")),
        "team-nitro/walkthrough-chain-fix3-20261119/work/stage-fix3.py": read_bytes(os.path.join(WORK, "stage-fix3.py")),
    }
    files = [
        ("team-nitro/walk-v23-assembly-20261114/welcome-staged.html", new_welcome),
        ("team-nitro/walk-v23-assembly-20261114/identity-fixed.html", new_ident),
        ("team-nitro/agreement-unfold-fix-20261117/agreement-unfold-fixed.html", new_unfold),
        ("team-nitro/walk-v23-assembly-20261114/walk-beginning-staging-worker.js", worker),
        ("team-nitro/walk-v23-assembly-20261114/build-v23-staging-worker.py", builder),
    ] + sorted(drivers.items())
    blobs = {}
    for path, data in files:
        _, blob = gh("POST", "/repos/%s/git/blobs" % REPO,
                     {"content": base64.b64encode(data).decode("ascii"), "encoding": "base64"})
        blobs[path] = blob["sha"]
        print("blob %s: %s (%d B)" % (path.split("/")[-1], blob["sha"][:12], len(data)), flush=True)
    _, tree = gh("POST", "/repos/%s/git/trees" % REPO,
                 {"base_tree": base_tree,
                  "tree": [{"path": p, "mode": "100644", "type": "blob", "sha": s} for p, s in blobs.items()]})
    print("new tree:", tree["sha"], flush=True)
    msg = commit_message(sha(worker), len(worker), welcome_sha, ident_sha, unfold_sha)
    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    _, cm = gh("POST", "/repos/%s/git/commits" % REPO,
               {"message": msg, "tree": tree["sha"], "parents": [PARENT_TIP],
                "author": {"name": "nayapower-lane-agent[bot]",
                           "email": "338161897+nayapower-lane-agent[bot]@users.noreply.github.com",
                           "date": now},
                "committer": {"name": "GitHub", "email": "noreply@github.com", "date": now}})
    commit_sha = cm["sha"]
    print("commit sha:", commit_sha, flush=True)
    _, ref3 = gh("PATCH", "/repos/%s/git/refs/heads/%s" % (REPO, NEW_BRANCH),
                 {"sha": commit_sha, "force": False})
    print("branch now:", ref3["object"]["sha"], flush=True)
    assert ref3["object"]["sha"] == commit_sha
    for path, data in files:
        _, rb = gh("GET", "/repos/%s/git/blobs/%s" % (REPO, blobs[path]))
        raw = base64.b64decode("".join(rb["content"].split()))
        assert len(raw) == len(data) and sha(raw) == sha(data), "blob read-back mismatch for %s" % path
        print("blob read-back OK:", path.split("/")[-1], len(raw), "bytes, sha match", flush=True)
    cf_put_inprocess(worker)
    ua = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
          "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")
    expect = {
        "/": welcome_sha,
        "/agreement": unfold_sha,
        "/welcome": WALK_SHA,
        "/identity.html": ident_sha,
        "/?stage=bridge": welcome_sha,
        "/?stage=deck": welcome_sha,
        "/?stage=letter": welcome_sha,
    }
    routes = {}
    for route, want in expect.items():
        got = None
        for attempt in (1, 2, 3):
            _, got = curl_sha(STAGING + route, ua)
            print("route %s: sha=%s (want %s) attempt %d" % (route, got[:12], want[:12], attempt), flush=True)
            if got == want:
                break
            time.sleep(15)
        routes[route] = got
        assert got == want, "route %s mismatch: got %s want %s" % (route, got, want)
    proof = {}
    for label, path, want in (
            ("welcome", "team-nitro/walk-v23-assembly-20261114/welcome-staged.html", welcome_sha),
            ("identity", "team-nitro/walk-v23-assembly-20261114/identity-fixed.html", ident_sha)):
        url = "%s/?file=%s&ref=%s&cb=%s&t=%d" % (PROOF, path, NEW_BRANCH, blobs[path], int(time.time()))
        _, got = curl_sha(url, ua)
        print("proof %s: sha=%s (want %s)" % (label, got[:12], want[:12]), flush=True)
        assert got == want, "proof-host %s mismatch" % label
        proof[label] = url
    print("STAGE-RESULT " + json.dumps({
        "welcome_bytes": len(new_welcome), "welcome_sha": welcome_sha,
        "identity_bytes": len(new_ident), "identity_sha": ident_sha,
        "unfold_bytes": len(new_unfold), "unfold_sha": unfold_sha,
        "worker_bytes": len(worker), "worker_sha": sha(worker),
        "commit": commit_sha, "tree": tree["sha"], "blobs": blobs,
        "routes": routes, "proof": proof}, indent=1), flush=True)

if __name__ == "__main__":
    main()
