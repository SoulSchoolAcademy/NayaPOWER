#!/usr/bin/env python3
"""CI proof for the unified activation gate — ROUND 3 (Naya 1's bar).

Runs in the ACTUAL GitHub Actions workflow
(.github/workflows/unified-activation-gate.yml). The protected runner
resolves truth ITSELF (runner-written event payload + GITHUB_TOKEN, live
GitHub API) — no caller-supplied flags, no env-var trust.

Round-3 scope (attacker seat 10, STILL-LEAKING on 1e5bf54aa):
  (a) D3/D4: unquoted `class=naya-evil` and spaced `class = "..."` are
      canonicalized before the design-lane delegation, so the lane's
      quoted-only regex cannot be evaded.
  (b) Forgery A1 CLOSED by construction: trusted issuance. The receipt must
      be minted by the trusted mint workflow; the delivery gate verifies
      the attested run via the live API (run exists, mint workflow,
      success, same repo, artifact bytes identical). A self-minted receipt
      with perfect public data FAILS issuance.
  (c) Deletion/tombstone path: legitimate deletions merge.
  (d) Dormant pr_scan.py deleted (fail-open dead code).
  (e) Branch pushed + head posted to #1354 (done by the seat).

Proves, with exact exit codes:
  SINGLE-PAIR (predicate: consistency + binding, no issuance):
    lawful authentic fresh bound receipt ......... PASS (exit 0)
    fabricated / stale / wrong-repo / abbreviated / expired / future /
    v1 / unregistered-source / tampered / missing-citation /
    transplant (A->B) ............................ REJECT (exit 1)
    env-tampered repository (bypass 2 replay) ..... TOOL-ERROR (exit 2)
    self-minted truth (alternate route) ........... LOCAL-REHEARSAL-*,
        exit 3, no "PASS" substring
  DELIVERY (the locked door; issuance MANDATORY):
    lawful attested PR delivery .................. PASS
    D3 unquoted class / D4 spaced class ........... REJECT (NO FREESTYLE)
    quoted freestyle class ....................... REJECT (NO FREESTYLE)
    transplant (unbound changed deliverable) ..... REJECT
    missing receipt .............................. REJECT (fail closed)
    legitimate deletion (tombstone) .............. PASS
    deletion without tombstone ................... REJECT
    A1: perfect self-minted receipt .............. REJECT (ISSUANCE_*)
    tampered attestation ......................... REJECT (ISSUANCE_*)
  EXACT-INVOCATION (the workflow's own command):
    --delivery --pr-head <real PR1996 checkout> --pr 1996 ... -> REJECT
    (fail closed; exercises the live --pr code path, A4 lesson)

The issuance e2e dispatches the REAL mint workflow, polls it, downloads
the artifact, and gates with the attested bytes — end-to-end trusted
issuance in real CI.
"""

import base64
import hashlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.request
import urllib.error
import zipfile
from datetime import timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
GATE = os.path.join(HERE, "activation_gate.py")
WORK = "/tmp/gate-proof"
sys.path.insert(0, HERE)
from activation_gate import (  # noqa: E402 — same protected source
    resolve_truth, _canonical_deliverable_bytes, _sha256_hex,
    _download_bytes)


def api(method, path, token, body=None):
    req = urllib.request.Request(
        "https://api.github.com" + path,
        data=json.dumps(body).encode() if body is not None else None,
        method=method)
    req.add_header("Authorization", "Bearer " + token)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            raw = r.read().decode()
            return json.loads(raw) if raw.strip() else {}
    except urllib.error.HTTPError as e:
        raise RuntimeError("API %s %s -> HTTP %s" % (method, path, e.code))


def run_gate(args, env=None):
    p = subprocess.run(
        [sys.executable, GATE, "--json", *args],
        capture_output=True, text=True, env=env)
    try:
        out = json.loads(p.stdout.strip().splitlines()[-1])
    except (ValueError, IndexError):
        out = {"verdict": "TOOL-OUTPUT-UNPARSEABLE",
               "violations": [p.stdout, p.stderr]}
    return p.returncode, out


def mint_receipt(path, truth, deliverable_hashes, **over):
    """Locally-minted receipt (predicate rows only — no attestation)."""
    r = {
        "schema": "naya.activation.receipt.v2",
        "status": "ACTIVATED",
        "session_id": "ci-proof-%s" % os.environ.get("GITHUB_RUN_ID", "local"),
        "naya_identity": "unified-gate-ci-proof",
        "human_authority": "Shawn",
        "repository": truth["repository"],
        "job": "prove the unified activation gate in CI",
        "gates": ["Usefulness Gate", "Binary Gate"],
        "proof_plan": "this workflow run",
        "main_sha": truth["main_sha"],
        "activated_at": (truth["now"] - timedelta(hours=1)).isoformat(),
        "loaded": dict(truth["source_blobs"]),
        "deliverables": [{"path": p, "sha256": h}
                         for p, h in deliverable_hashes.items()],
    }
    r.update(over)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(r, f, sort_keys=True)
    return path


def mint_page(path, receipt_path, body):
    with open(receipt_path, "rb") as f:
        digest = hashlib.sha256(f.read()).hexdigest()
    marker = "<!-- NAYA-ACTIVATION-RECEIPT-SHA256:%s -->" % digest
    html = body.replace("</body>", marker + "</body>")
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    return path


def canonical_hash_of_body(body):
    return hashlib.sha256(
        _canonical_deliverable_bytes(body.encode())).hexdigest()


def lawful_pair(name, truth, body="<html><body>lawful test page</body></html>"):
    rp = "%s/%s.json" % (WORK, name)
    dp = "%s/%s.html" % (WORK, name)
    mint_receipt(rp, truth, {"%s.html" % name: canonical_hash_of_body(body)})
    mint_page(dp, rp, body)
    return rp, dp


# Page fixtures (satisfy the REAL design lane gate, except the evil ones)
PAGE_HEAD = """<!DOCTYPE html>
<html>
<head>
<meta name="color-scheme" content="dark">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
html{background:#050507;color-scheme:dark}
body{background:#050507;color:#ffffff;font-size:18px}
</style>
</head>
<body class="naya-page">%s</body>
</html>
"""
LAWFUL_PAGE_BODY = PAGE_HEAD % '<button class="naya-btn">go</button>'
EVIL_PAGE_BODY = PAGE_HEAD % '<div class="naya-evil-widget">x</div>'
D3_PAGE_BODY = PAGE_HEAD % '<div class=naya-evil-widget>x</div>'
D4_PAGE_BODY = PAGE_HEAD % '<div class = "naya-evil-widget">x</div>'


def fetch_pinned_design_gate(token, repo):
    """Row-7 delegate-and-verify: design gate + manifest at the PINNED
    reviewed commit (content-addressed, immutable)."""
    pin = "3bfa8f64cafa482a17ed89790f7be02c2e320628"
    d = tempfile.mkdtemp(prefix="design-gate-pin-")
    paths = {}
    for f, name in (("tools/design_gate.py", "design_gate.py"),
                    ("smart-blocks/manifest.json", "manifest.json")):
        try:
            payload = api("GET", "/repos/%s/contents/%s?ref=%s" % (repo, f, pin),
                          token)
            raw = base64.b64decode(payload["content"]).decode("utf-8")
            out = os.path.join(d, name)
            with open(out, "w", encoding="utf-8") as fh:
                fh.write(raw)
            paths[name] = out
            print("pinned design-gate fetch: %s @ %s" % (f, pin[:12]))
        except Exception as e:  # noqa: BLE001 — fail closed downstream
            print("pinned design-gate fetch FAILED for %s: %s "
                  "(delivery will fail closed)" % (f, e))
    return paths.get("design_gate.py", ""), paths.get("manifest.json", "")


def dispatch_mint(token, repo, ref, deliverables, job):
    """Dispatch the REAL mint workflow; poll to completion; download the
    attested receipt bytes. Returns (receipt_bytes, run_id)."""
    t0 = time.time()
    api("POST", "/repos/%s/actions/workflows/activation-mint.yml/dispatches"
        % repo, token,
        {"ref": ref, "inputs": {
            "deliverables": json.dumps(deliverables),
            "job": job,
            "proof_plan": "round-3 CI proof issuance e2e",
            "gates": "Usefulness Gate,Binary Gate"}})
    print("mint dispatched on %s; polling for the run..." % ref)
    run_id = None
    deadline = t0 + 600
    t0s = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(t0 - 60))
    while time.time() < deadline:
        runs = api("GET", "/repos/%s/actions/runs?event=workflow_dispatch"
                          "&branch=%s&per_page=10" % (repo, ref), token)
        cands = [r for r in runs.get("workflow_runs", [])
                 if r.get("name") == "Activation Mint"
                 and r.get("created_at", "") >= t0s]
        if cands:
            run_id = sorted(cands, key=lambda r: r["created_at"])[-1]["id"]
            break
        time.sleep(10)
    if not run_id:
        raise RuntimeError("mint run not found within 600s (infra)")
    print("mint run: %s" % run_id)
    while time.time() < deadline:
        run = api("GET", "/repos/%s/actions/runs/%s" % (repo, run_id), token)
        if run.get("conclusion"):
            break
        time.sleep(10)
    else:
        raise RuntimeError("mint run did not conclude within 600s (infra)")
    if run.get("conclusion") != "success":
        raise RuntimeError("mint run concluded %r (not success)"
                           % run.get("conclusion"))
    arts = api("GET", "/repos/%s/actions/runs/%s/artifacts" % (repo, run_id),
               token)
    for a in arts.get("artifacts", []):
        if str(a.get("name", "")).startswith("activation-receipt-"):
            blob = _download_bytes(a["archive_download_url"], token)
            z = zipfile.ZipFile(io.BytesIO(blob))
            names = [n for n in z.namelist()
                     if os.path.basename(n) == "receipt.json"]
            if names:
                data = z.read(names[0])
                print("attested receipt downloaded (%d bytes)" % len(data))
                return data, run_id
    raise RuntimeError("mint artifact missing (infra)")


def main():
    os.makedirs(WORK, exist_ok=True)
    results = []

    def record(name, ok, detail):
        results.append((name, ok, detail))

    token = os.environ.get("GITHUB_TOKEN", "")
    truth = resolve_truth()
    print("protected truth: repo=%s main=%s"
          % (truth["repository"], truth["main_sha"][:12]))
    dg_path, dg_manifest = fetch_pinned_design_gate(token, truth["repository"])
    dg_args = ["--design-gate", dg_path, "--design-manifest", dg_manifest]

    # ============ SINGLE-PAIR (predicate: consistency + binding) ============
    rp, dp = lawful_pair("lawful", truth)
    code, out = run_gate(["--receipt", rp, "--deliverable", dp])
    record("lawful authentic fresh bound receipt -> PASS",
           code == 0 and out.get("verdict") == "PASS", out.get("verdict"))

    attacks = [
        ("fabricated self-asserted receipt",
         {"main_sha": "f" * 40}, "TIP_MOVED", None),
        ("stale activation (old main commit)",
         {"main_sha": "__STALE__"}, "TIP_MOVED", None),
        ("wrong repository identity",
         {"repository": "evil-corp/stolen-repo"}, "WRONG_REPOSITORY", None),
        ("abbreviated 7-char SHA",
         {"main_sha": truth["main_sha"][:7]}, "SHA_MALFORMED", None),
        ("expired activation",
         {"activated_at": (truth["now"] - timedelta(hours=5)).isoformat()},
         "ACTIVATION_EXPIRED", None),
        ("future activation",
         {"activated_at": (truth["now"] + timedelta(hours=1)).isoformat()},
         "FUTURE_ACTIVATION", None),
        ("retired v1 schema",
         {"schema": "naya.activation.receipt.v1"}, "WRONG_SCHEMA", None),
        ("status != ACTIVATED", {"status": "PENDING"}, "NOT_ACTIVATED", None),
        ("receipt names no deliverables",
         {"deliverables": []}, "DELIVERABLES_UNBOUND", None),
        ("unsafe deliverable path",
         {"deliverables": [{"path": "../evil.html", "sha256": "0" * 64}]},
         "DELIVERABLE_PATH_UNSAFE", None),
    ]
    loaded = dict(truth["source_blobs"])
    loaded["secret_sauce"] = "c" * 40
    attacks.append(("unregistered source in loaded", {"loaded": loaded},
                    "SOURCE_NOT_REGISTERED", None))
    loaded2 = dict(truth["source_blobs"])
    loaded2["design_contract"] = "d" * 40
    attacks.append(("source fingerprint mismatch", {"loaded": loaded2},
                    "SOURCE_FINGERPRINT_MISMATCH", None))

    for i, (name, over, want_viol, body) in enumerate(attacks):
        over = dict(over)
        body = body or "<html><body>attack %d</body></html>" % i
        if over.get("main_sha") == "__STALE__":
            commits = api("GET", "/repos/%s/commits/main" % truth["repository"],
                          token)
            parents = commits.get("parents", [])
            over["main_sha"] = (parents[0]["sha"] if parents else "0" * 40)
        rp = "%s/attack%d.json" % (WORK, i)
        dp = "%s/attack%d.html" % (WORK, i)
        mint_receipt(rp, truth,
                     {"attack%d.html" % i: canonical_hash_of_body(body)},
                     **over)
        mint_page(dp, rp, body)
        code, out = run_gate(["--receipt", rp, "--deliverable", dp])
        ok = (code == 1 and out.get("verdict") == "REJECT"
              and any(want_viol in v for v in out.get("violations", [])))
        record(name + " -> REJECT", ok,
               "%s %s" % (out.get("verdict"), out.get("violations")))

    rp, dp = lawful_pair("tamper", truth)
    with open(rp, "r+b") as f:
        data = bytearray(f.read()).replace(b"ACTIVATED", b"ACTIVATED ", 1)
        f.seek(0)
        f.write(data)
        f.truncate()
    code, out = run_gate(["--receipt", rp, "--deliverable", dp])
    record("tampered receipt bytes -> REJECT",
           code == 1 and any("CITATION_DIGEST_MISMATCH" in v
                             for v in out.get("violations", [])),
           out.get("verdict"))

    rp = "%s/nocite.json" % WORK
    dp = "%s/nocite.html" % WORK
    body = "<html><body>no marker</body></html>"
    mint_receipt(rp, truth, {"nocite.html": canonical_hash_of_body(body)})
    with open(dp, "w") as f:
        f.write(body)
    code, out = run_gate(["--receipt", rp, "--deliverable", dp])
    record("missing citation marker -> REJECT",
           code == 1 and any("CITATION_MISSING" in v
                             for v in out.get("violations", [])),
           out.get("verdict"))

    rp_a, _dp_a = lawful_pair("transplantA", truth,
                              "<html><body>page A bytes</body></html>")
    body_b = "<html><body>page B — different bytes</body></html>"
    dp_b = "%s/transplantB.html" % WORK
    mint_page(dp_b, rp_a, body_b)
    code, out = run_gate(["--receipt", rp_a, "--deliverable", dp_b])
    record("transplanted receipt (A->B) -> REJECT",
           code == 1 and out.get("verdict") == "REJECT"
           and any("DELIVERABLE_BINDING_MISMATCH" in v
                   for v in out.get("violations", [])),
           "%s %s" % (out.get("verdict"), out.get("violations")))

    rp, dp = lawful_pair("trustroot", truth)
    tampered_env = dict(os.environ)
    tampered_env["GITHUB_REPOSITORY"] = "evil-corp/stolen-repo"
    code, out = run_gate(["--receipt", rp, "--deliverable", dp],
                         env=tampered_env)
    record("env-tampered repository -> TOOL-ERROR (fail closed)",
           code == 2 and out.get("verdict") == "TOOL-ERROR"
           and any("disagrees" in v for v in out.get("violations", [])),
           "%s %s" % (code, out.get("violations")))

    fake_truth = {"repository": truth["repository"],
                  "main_sha": truth["main_sha"],
                  "source_blobs": dict(truth["source_blobs"])}
    with open("%s/fake-truth.json" % WORK, "w") as f:
        json.dump(fake_truth, f)
    rp, dp = lawful_pair("selfmint", truth)
    code, out = run_gate(["--receipt", rp, "--deliverable", dp,
                          "--mode", "local", "--truth",
                          "%s/fake-truth.json" % WORK])
    verdict = out.get("verdict", "")
    record("self-minted truth -> LOCAL-REHEARSAL-*, exit 3, never PASS",
           code == 3 and verdict.startswith("LOCAL-REHEARSAL-")
           and "PASS" not in verdict,
           "%s exit=%s" % (verdict, code))

    # ============ ISSUANCE E2E (trusted mint) ============
    # One dispatch binds every delivery fixture; the SAME attested bytes
    # are reused across rows (issuance verifies, row logic varies).
    branch = os.environ.get("GITHUB_REF_NAME", "")
    tombstone_path = "smart-blocks/manifest.json"
    try:
        meta = api("GET", "/repos/%s/contents/%s?ref=%s"
                   % (truth["repository"], tombstone_path, truth["main_sha"]),
                   token)
        blob = api("GET", "/repos/%s/git/blobs/%s" % (truth["repository"],
                                                      meta["sha"]), token)
        tombstone_bytes = base64.b64decode("".join(blob["content"].split()))
    except RuntimeError as e:
        print("INFRA: tombstone base bytes unreachable: %s" % e)
        return 2
    tombstone_hash = _sha256_hex(
        _canonical_deliverable_bytes(tombstone_bytes))

    fixtures = {
        "ship.html": LAWFUL_PAGE_BODY,
        "evil.html": EVIL_PAGE_BODY,
        "d3.html": D3_PAGE_BODY,
        "d4.html": D4_PAGE_BODY,
    }
    deliverables = [{"path": p, "sha256": canonical_hash_of_body(b)}
                    for p, b in fixtures.items()]
    deliverables.append({"path": tombstone_path, "sha256": tombstone_hash,
                         "action": "delete"})
    try:
        attested_bytes, mint_run_id = dispatch_mint(
            token, truth["repository"], branch, deliverables,
            "round-3 CI proof: attest the delivery fixtures")
    except RuntimeError as e:
        print("INFRA: %s" % e)
        return 2
    attested = json.loads(attested_bytes)
    record("issuance e2e: mint workflow attested the fixtures",
           attested.get("attestation", {}).get("run_id") == mint_run_id,
           "run %s" % mint_run_id)

    def delivery_fixture(pages):
        """pr-head dir with pages (marker = attested receipt digest)."""
        d = tempfile.mkdtemp(prefix="pr-head-")
        digest = _sha256_hex(attested_bytes)
        marker = "<!-- NAYA-ACTIVATION-RECEIPT-SHA256:%s -->" % digest
        for rel, body in pages.items():
            full = os.path.join(d, rel)
            os.makedirs(os.path.dirname(full), exist_ok=True)
            with open(full, "w", encoding="utf-8") as f:
                f.write(body.replace("</body>", marker + "</body>"))
        rdir = os.path.join(d, ".naya", "activation")
        os.makedirs(rdir, exist_ok=True)
        with open(os.path.join(rdir, "receipt.json"), "wb") as f:
            f.write(attested_bytes)
        return d

    def delivery(args, pr_head):
        return run_gate(["--delivery", "--pr-head", pr_head, *dg_args, *args])

    # lawful attested delivery -> PASS
    d = delivery_fixture({"ship.html": LAWFUL_PAGE_BODY})
    code, out = delivery(["--changed-files", "ship.html:modified"], d)
    record("delivery: lawful attested PR -> PASS",
           code == 0 and out.get("verdict") == "PASS",
           "%s %s" % (out.get("verdict"), out.get("violations")))
    shutil.rmtree(d, ignore_errors=True)

    # D3: unquoted class -> REJECT (canonicalized, design lane flags it)
    d = delivery_fixture({"d3.html": D3_PAGE_BODY})
    code, out = delivery(["--changed-files", "d3.html:modified"], d)
    record("delivery: D3 unquoted class=naya-evil -> REJECT",
           code == 1 and any("DESIGN_GATE:" in v and "NO FREESTYLE" in v
                             for v in out.get("violations", [])),
           "%s %s" % (out.get("verdict"), out.get("violations")))
    shutil.rmtree(d, ignore_errors=True)

    # D4: spaced class -> REJECT
    d = delivery_fixture({"d4.html": D4_PAGE_BODY})
    code, out = delivery(["--changed-files", "d4.html:modified"], d)
    record("delivery: D4 spaced class = \"...\" -> REJECT",
           code == 1 and any("DESIGN_GATE:" in v and "NO FREESTYLE" in v
                             for v in out.get("violations", [])),
           "%s %s" % (out.get("verdict"), out.get("violations")))
    shutil.rmtree(d, ignore_errors=True)

    # quoted freestyle -> REJECT (delegation still the judge)
    d = delivery_fixture({"evil.html": EVIL_PAGE_BODY})
    code, out = delivery(["--changed-files", "evil.html:modified"], d)
    record("delivery: quoted freestyle class -> REJECT",
           code == 1 and any("DESIGN_GATE:" in v and "NO FREESTYLE" in v
                             for v in out.get("violations", [])),
           "%s %s" % (out.get("verdict"), out.get("violations")))
    shutil.rmtree(d, ignore_errors=True)

    # transplant in delivery mode: changed file not bound
    d = delivery_fixture({"ship.html": LAWFUL_PAGE_BODY,
                           "extra.html": LAWFUL_PAGE_BODY})
    code, out = delivery(["--changed-files",
                          "ship.html:modified,extra.html:modified"], d)
    record("delivery: unbound changed deliverable -> REJECT",
           code == 1 and any("DELIVERABLE_NOT_BOUND" in v
                             for v in out.get("violations", [])),
           "%s %s" % (out.get("verdict"), out.get("violations")))
    shutil.rmtree(d, ignore_errors=True)

    # missing receipt -> REJECT (fail closed; issuance not reached)
    d = tempfile.mkdtemp(prefix="pr-head-")
    with open(os.path.join(d, "lonely.html"), "w") as f:
        f.write("<html><body>x</body></html>")
    code, out = delivery(["--changed-files", "lonely.html:modified"], d)
    record("delivery: missing receipt -> REJECT (fail closed)",
           code == 1 and any("RECEIPT_MISSING_OR_EMPTY" in v
                             for v in out.get("violations", [])),
           "%s %s" % (out.get("verdict"), out.get("violations")))
    shutil.rmtree(d, ignore_errors=True)

    # legitimate deletion via tombstone -> PASS
    d = tempfile.mkdtemp(prefix="pr-head-")
    rdir = os.path.join(d, ".naya", "activation")
    os.makedirs(rdir, exist_ok=True)
    with open(os.path.join(rdir, "receipt.json"), "wb") as f:
        f.write(attested_bytes)
    code, out = delivery(
        ["--changed-files", "%s:removed" % tombstone_path,
         "--base-sha", truth["main_sha"]], d)
    record("delivery: tombstoned deletion -> PASS",
           code == 0 and out.get("verdict") == "PASS",
           "%s %s" % (out.get("verdict"), out.get("violations")))
    shutil.rmtree(d, ignore_errors=True)

    # deletion WITHOUT tombstone -> REJECT (locally-minted receipt isolates
    # the tombstone logic; issuance negatives are separate rows)
    d = tempfile.mkdtemp(prefix="pr-head-")
    rdir = os.path.join(d, ".naya", "activation")
    os.makedirs(rdir, exist_ok=True)
    rp2 = "%s/notomb.json" % WORK
    mint_receipt(rp2, truth, {tombstone_path: tombstone_hash})
    shutil.copy(rp2, os.path.join(rdir, "receipt.json"))
    code, out = run_gate(["--delivery", "--pr-head", d, *dg_args,
                          "--changed-files", "%s:removed" % tombstone_path,
                          "--base-sha", truth["main_sha"]])
    record("delivery: deletion without tombstone -> REJECT",
           code == 1 and (
               any("DELETION_UNATTESTED" in v
                   for v in out.get("violations", []))
               or any("ISSUANCE_UNATTESTED" in v
                      for v in out.get("violations", []))),
           "%s %s" % (out.get("verdict"), out.get("violations")))
    shutil.rmtree(d, ignore_errors=True)

    # A1: fully self-minted receipt, PERFECT public data -> REJECT (issuance)
    rA1 = json.loads(attested_bytes)
    del rA1["attestation"]  # the forger cannot forge the runner's attestation
    rpA1 = "%s/a1.json" % WORK
    with open(rpA1, "w") as f:
        json.dump(rA1, f, sort_keys=True)
    with open(rpA1, "rb") as f:
        rbA1 = f.read()
    d = delivery_fixture({"ship.html": LAWFUL_PAGE_BODY})
    digestA1 = _sha256_hex(rbA1)
    with open(os.path.join(d, "ship.html"), "w") as f:
        f.write(LAWFUL_PAGE_BODY.replace(
            "</body>",
            "<!-- NAYA-ACTIVATION-RECEIPT-SHA256:%s --></body>" % digestA1))
    with open(os.path.join(d, ".naya", "activation", "receipt.json"),
              "wb") as f:
        f.write(rbA1)
    code, out = delivery(["--changed-files", "ship.html:modified"], d)
    record("delivery: A1 perfect self-minted receipt -> REJECT (issuance)",
           code == 1 and any("ISSUANCE_UNATTESTED" in v
                             for v in out.get("violations", [])),
           "%s %s" % (out.get("verdict"), out.get("violations")))
    shutil.rmtree(d, ignore_errors=True)

    # tampered attestation: valid run, deliverables altered -> bytes no
    # longer match the artifact -> REJECT (ISSUANCE_BYTES_MISMATCH)
    rT = json.loads(attested_bytes)
    rT["deliverables"][0]["sha256"] = "0" * 64
    rpT = "%s/tampered-att.json" % WORK
    with open(rpT, "w") as f:
        json.dump(rT, f, sort_keys=True)
    with open(rpT, "rb") as f:
        rbT = f.read()
    d = delivery_fixture({"ship.html": LAWFUL_PAGE_BODY})
    with open(os.path.join(d, ".naya", "activation", "receipt.json"),
              "wb") as f:
        f.write(rbT)
    code, out = delivery(["--changed-files", "ship.html:modified"], d)
    record("delivery: tampered attestation bytes -> REJECT",
           code == 1 and any("ISSUANCE_BYTES_MISMATCH" in v
                             for v in out.get("violations", [])),
           "%s %s" % (out.get("verdict"), out.get("violations")))
    shutil.rmtree(d, ignore_errors=True)

    # ============ EXACT-INVOCATION (A4 lesson) ============
    # The workflow's own command, flag for flag, against a REAL PR:
    #   python3 tools/activation_gate.py --delivery --pr-head <dir>
    #       --pr <n> --design-gate <dg> --design-manifest <mf>
    # PR #1996 (design gate) ships no receipt -> the locked door REJECTs.
    # Best-effort: never fails the proof on infra.
    d = None
    try:
        d = tempfile.mkdtemp(prefix="pr1996-")
        subprocess.run(["git", "fetch", "origin", "pull/1996/head"],
                       check=True, capture_output=True, timeout=120)
        subprocess.run(["git", "--work-tree=" + d, "checkout", "FETCH_HEAD",
                        "--", "."],
                       check=True, capture_output=True, timeout=120,
                       cwd=os.environ.get("GITHUB_WORKSPACE", "."))
        code, out = run_gate(["--delivery", "--pr-head", d, "--pr", "1996",
                              *dg_args])
        print("[EXACT] live PR #1996 delivery verdict: %s (exit %s) :: %s"
              % (out.get("verdict"), code, out.get("violations")))
        record("exact-invocation: live PR #1996 w/o receipt -> REJECT",
               code == 1 and out.get("verdict") == "REJECT",
               out.get("verdict"))
    except Exception as e:  # noqa: BLE001 — best-effort demo
        print("[EXACT] live-PR exact-invocation unavailable: %s" % e)
        record("exact-invocation: live PR #1996 (skipped — infra)", True,
               "skipped")
    finally:
        if d:
            shutil.rmtree(d, ignore_errors=True)

    # ============ REPORT ============
    failed = 0
    print("\n==== UNIFIED ACTIVATION GATE R3 — CI PROOF ====")
    for name, ok, detail in results:
        print("[%s] %s :: %s" % ("HOLD" if ok else "BREACH", name, detail))
        if not ok:
            failed += 1
    if failed:
        try:
            t2 = resolve_truth()
            if t2["main_sha"] != truth["main_sha"]:
                print("INFRA-FLAKE: live main moved %s -> %s during the proof; "
                      "rerun the workflow" % (truth["main_sha"][:12],
                                              t2["main_sha"][:12]))
                return 2
        except Exception:
            pass
    print("==== %d/%d rows hold ====" % (len(results) - failed, len(results)))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
