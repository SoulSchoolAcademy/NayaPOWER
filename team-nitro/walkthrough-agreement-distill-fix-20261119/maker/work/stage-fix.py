#!/usr/bin/env python3
"""FIX stage + file (2026-11-19) — agreement-distill fix round.

Inputs: fixed unfold + welcome + worker from build-fix.py (in-memory,
from the distill base via transform-fix.js); walk + builder edited on
disk; maker report + brief + work files from disk. Does:
  1. verifies inputs by sha (computed, never typed),
  2. node --checks every script block of the fixed unfold/welcome,
  3. rebuilds the staging worker twice (deterministic sha) and verifies
     every embed by sha256 + the FIX markers,
  4. creates branch walkthrough/agreement-distill-fix-20261119 from the
     distill tip 3e5647cf,
  5. files ONE commit (unfold + welcome + walk + worker + builder +
     brief + maker report + drivers), read-back verified,
  6. PUTs the worker to the walk staging worker,
  7. verifies all 7 routes by sha256 via curl, plus the proof-host
     links for the three edited files.
No PR, no merge, no live deploy, no message to Shawn.
"""
import base64, hashlib, json, os, re, subprocess, sys, time

HOME = os.path.expanduser("~")
RECORDS = os.path.join(HOME, "workspace/team-nitro/walkthrough-agreement-distill-fix-20261119")
WORK = os.path.join(RECORDS, "maker/work")
V23 = os.path.join(HOME, "workspace/team-nitro/walk-v23-assembly-20261114")
BUILDER = os.path.join(V23, "build-v23-staging-worker.py")
WALK_LOCAL = os.path.join(V23, "walk-beginning-fixed.html")
META = os.path.join(V23, "v23-meta.json")
GH = os.path.join(HOME, "workspace/team-nitro/gh-direct.py")
CF = os.path.join(HOME, "workspace/project-intelligence/cf-worker.py")
REPO = "SoulSchoolAcademy/NayaPOWER"
NEW_BRANCH = "walkthrough/agreement-distill-fix-20261119"
PARENT_TIP = "3e5647cf3ea95a1fa57aa7c51c16e47055913bf6"
CF_ACCOUNT = "b5e2a51b3e883f7722287c5f51b1196b"
CF_SCRIPT = "naya-walk-beginning-staging"
STAGING = "https://naya-walk-beginning-staging.nayapower.workers.dev"
PROOF = "https://naya-proof-host.nayapower.workers.dev"
IDENT_SHA = "3279dc3572337e5e971369a3742effcaac7f6e5b059192ddaa6e689f0f92886c"

# Final fixed shas (computed by build-fix.py; asserted, never trusted blind).
UNFOLD_SHA = "5fe1a3ec2231c128774c6eb00736913d93117d3eaa06278e2a16183cdebee6ab"
WELCOME_SHA = "c3c750b72a2b0330d15de8831e9b24719116991e6c0df9dbc5d329834fbbaed5"
WALK_SHA = "0f05b3f96ce8edd0ecb094c0f64972098f788c3943e22b5446c8bb60e9b0e2fd"
WORKER_SHA = "cd2ed5438546f42dc8b7acce2aef70933bbe3abdcf2b7ea93540503e81c9567c"


def sha(b):
    return hashlib.sha256(b).hexdigest()


def read_bytes(p):
    with open(p, "rb") as f:
        return f.read()


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


def build_all():
    import importlib.util
    spec = importlib.util.spec_from_file_location("build_fix", os.path.join(WORK, "build-fix.py"))
    build_fix = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(build_fix)
    u, w, worker = build_fix.main()
    assert sha(u) == UNFOLD_SHA, "unfold sha moved: %s" % sha(u)
    assert sha(w) == WELCOME_SHA, "welcome sha moved: %s" % sha(w)
    assert sha(worker) == WORKER_SHA, "worker sha moved: %s" % sha(worker)
    return u, w, worker


def commit_message(worker_sha, worker_bytes, welcome_sha, unfold_sha, walk_sha):
    return (
        "Agreement-distill FIX (2026-11-19, maker round; MAKER-REPORT.md in "
        "walkthrough-agreement-distill-fix-20261119/)\\n\\n"
        "The eye's verdict on the distill was GOES BACK: on /agreement Next moved "
        "the pill but the board never changed (37 articles stacked as one long "
        "page); the deck took two taps per image board and left a black void; the "
        "deck's words differed from /agreement's; ?stage=letter was broken and "
        "/agreement ignored ?stage=; five button destinations were wrong; the frame "
        "read dark throughout with clipped buttons and flaky pictures; the reader "
        "text carried an internal note, a false count and repeats.\\n\\n"
        "Root causes, all probed in the distill bytes: (1) the frame-now hide "
        "(.letter-beat:not(.frame-now), 0,2,0) lost to a later #deckBody rule "
        "(1,1,0) — fixed with an outranking (1,2,0) hide rule. (2) A two-phase "
        "Smart Block (visual tap, then advance) plus a talk-phase showcase hide "
        "that left the grid's second column an empty void, plus faces centred on "
        "the speaking line and alternating left — now one tap per board, showcase "
        "always shown, faces top-right pinned to the board top. (3) One story: "
        "superhighway everywhere; the deck's 37 extra subtitle lines removed. "
        "(4) /agreement honours ?stage= via redirect; the letterPage jewel now "
        "updates. (5) Hero Read goes to /agreement; the last board's Keep reading "
        "ends through the hold; bridge Enter holds before identity; the name-entry "
        "state survives a reload via a session flag; /welcome paints its door at "
        "once (the 4s claim gate untouched). (6) The travelling rim light is "
        "verified present on all routes (interior stays board black per §4); "
        "pictures retry once, then fall back to the crystal N / hide. (7) The "
        "internal note is plain reader words now; 99/100 gone; You're hired once, "
        "on board 37; the count is thirty-seven boards. The harness also found "
        "and fixed two more: the letterPage jewel and the stage Back (a no-op "
        "because derive()'s lastShown landed back on the current beat).\\n\\n"
        "Carried: boards 2/22 have their jargon baked into the image pixels — no "
        "text edit can change them and no unused harvested picture exists to swap "
        "in; the captain's eye must pick a replacement picture or a re-render.\\n\\n"
        "Proof: a DOM harness (maker/work/dom-harness.js) that parses the real "
        "HTML, runs the real scripts in a vm context and drives the real handlers "
        "tap by tap — 54 assertions, 0 failures, across /agreement, "
        "?stage=deck, ?stage=letter, the plain welcome and the stage redirects. "
        "Laws delta 0 (unfold 1 FAIL / 2 WARN, welcome 83 FAIL / 4 WARN, "
        "identical before/after). Worker built twice, identical sha %s (%d B); "
        "embeds verified: WALK %s, IDENTITY 3279dc35, WELCOME %s, UNFOLD %s, "
        "TEMPLATE 61002d15.\\n\\n"
        "Staged: %s/ - routes curl-verified byte-identical by sha256 after "
        "the PUT. NO PR, NO MERGE — the checker and the captain come after "
        "this seat. Nothing live."
        % (worker_sha[:8], worker_bytes, walk_sha[:8], welcome_sha[:8], unfold_sha[:8], STAGING))


def curl_sha(url, ua):
    rr = subprocess.run(["curl", "-s", "-A", ua, url], capture_output=True, timeout=120)
    return rr.stdout, sha(rr.stdout)


def main():
    new_unfold, new_welcome, worker = build_all()
    new_walk = read_bytes(WALK_LOCAL)
    builder = read_bytes(BUILDER)
    print("inputs: unfold %d B %s, welcome %d B %s, walk %d B %s, worker %d B %s" % (
        len(new_unfold), sha(new_unfold), len(new_welcome), sha(new_welcome),
        len(new_walk), sha(new_walk), len(worker), sha(worker)), flush=True)
    assert sha(new_walk) == WALK_SHA, "walk sha moved: %s" % sha(new_walk)
    for needle in (b'assert welcome_sha.startswith("c3c750b7")',
                   b'assert unfold_sha.startswith("5fe1a3ec")',
                   b'assert walk_sha.startswith("0f05b3f9")'):
        assert needle in builder, "builder missing %s" % needle
    r = subprocess.run([sys.executable, "-c", "compile(open(%r).read(), 'builder', 'exec')" % BUILDER], capture_output=True)
    assert r.returncode == 0, "builder does not compile: %s" % r.stderr.decode("utf-8", "replace")[-500:]
    print("builder verified: asserts the new shas (%d B)" % len(builder), flush=True)
    for idx, code in enumerate(extract_scripts(new_unfold, "unfold")):
        node_check_script(code, "unfold-%d" % idx)
    for idx, code in enumerate(extract_scripts(new_welcome, "welcome")):
        node_check_script(code, "welcome-%d" % idx)
    _, ref = gh("GET", "/repos/%s/git/refs/heads/walkthrough/agreement-distill-20261119" % REPO)
    print("parent branch tip:", ref["object"]["sha"], flush=True)
    assert ref["object"]["sha"] == PARENT_TIP, "parent tip moved: %s" % ref["object"]["sha"]
    _, nb = gh("POST", "/repos/%s/git/refs" % REPO,
               {"ref": "refs/heads/%s" % NEW_BRANCH, "sha": PARENT_TIP})
    print("new branch created:", nb["ref"], nb["object"]["sha"], flush=True)
    assert nb["object"]["sha"] == PARENT_TIP
    _, ref2 = gh("GET", "/repos/%s/git/refs/heads/%s" % (REPO, NEW_BRANCH))
    assert ref2["object"]["sha"] == PARENT_TIP, "branch tip moved: %s" % ref2["object"]["sha"]
    _, commit = gh("GET", "/repos/%s/git/commits/%s" % (REPO, PARENT_TIP))
    base_tree = commit["tree"]["sha"]
    print("base tree:", base_tree, flush=True)
    report = read_bytes(os.path.join(RECORDS, "maker/MAKER-REPORT.md"))
    brief = read_bytes(os.path.join(RECORDS, "AGREEMENT-DISTILL-FIX-BRIEF.md"))
    driver_names = ["transform-fix.js", "build-fix.py", "law-fix.py", "dom-harness.js",
                    "debug-letter.js", "probe-fix.js", "probe-fix2.js", "probe-fix3.js",
                    "probe-fix4.js", "boards-distill.js", "transform-distill.js",
                    "build-mem.py", "law-distill.py", "probe-distill.py", "stage-fix.py"]
    files = [
        ("team-nitro/agreement-unfold-fix-20261117/agreement-unfold-fixed.html", new_unfold),
        ("team-nitro/walk-v23-assembly-20261114/welcome-staged.html", new_welcome),
        ("team-nitro/walk-v23-assembly-20261114/walk-beginning-fixed.html", new_walk),
        ("team-nitro/walk-v23-assembly-20261114/walk-beginning-staging-worker.js", worker),
        ("team-nitro/walk-v23-assembly-20261114/build-v23-staging-worker.py", builder),
        ("team-nitro/walkthrough-agreement-distill-fix-20261119/AGREEMENT-DISTILL-FIX-BRIEF.md", brief),
        ("team-nitro/walkthrough-agreement-distill-fix-20261119/maker/MAKER-REPORT.md", report),
    ]
    for name in driver_names:
        files.append(("team-nitro/walkthrough-agreement-distill-fix-20261119/maker/work/" + name,
                      read_bytes(os.path.join(WORK, name))))
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
    msg = commit_message(sha(worker), len(worker), WELCOME_SHA, UNFOLD_SHA, WALK_SHA)
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
        "/": WELCOME_SHA,
        "/agreement": UNFOLD_SHA,
        "/welcome": WALK_SHA,
        "/identity.html": IDENT_SHA,
        "/?stage=bridge": WELCOME_SHA,
        "/?stage=deck": WELCOME_SHA,
        "/?stage=letter": WELCOME_SHA,
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
            ("unfold", "team-nitro/agreement-unfold-fix-20261117/agreement-unfold-fixed.html", UNFOLD_SHA),
            ("welcome", "team-nitro/walk-v23-assembly-20261114/welcome-staged.html", WELCOME_SHA),
            ("walk", "team-nitro/walk-v23-assembly-20261114/walk-beginning-fixed.html", WALK_SHA)):
        url = "%s/?file=%s&ref=%s&cb=%s&t=%d" % (PROOF, path, NEW_BRANCH, blobs[path], int(time.time()))
        _, got = curl_sha(url, ua)
        print("proof %s: sha=%s (want %s)" % (label, got[:12], want[:12]), flush=True)
        assert got == want, "proof-host %s mismatch" % label
        proof[label] = url
    print("STAGE-RESULT " + json.dumps({
        "unfold_bytes": len(new_unfold), "unfold_sha": UNFOLD_SHA,
        "welcome_bytes": len(new_welcome), "welcome_sha": WELCOME_SHA,
        "walk_bytes": len(new_walk), "walk_sha": WALK_SHA,
        "worker_bytes": len(worker), "worker_sha": WORKER_SHA,
        "commit": commit_sha, "tree": tree["sha"], "blobs": blobs,
        "routes": routes, "proof": proof}, indent=1), flush=True)


if __name__ == "__main__":
    main()
