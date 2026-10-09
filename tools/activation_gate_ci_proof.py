#!/usr/bin/env python3
"""CI proof for the unified activation gate — ROUND 2 (Naya 1's bar).

Runs in the ACTUAL GitHub Actions workflow
(.github/workflows/unified-activation-gate.yml). The protected runner
resolves truth ITSELF (runner-written event payload + GITHUB_TOKEN, live
GitHub API) — no caller-supplied flags, no env-var trust.

Proves, with exact exit codes:
  lawful authentic fresh bound receipt ................. PASS (exit 0)
  fabricated / self-asserted receipt ................. REJECT (exit 1)
  stale activation (genuinely old main commit) ....... REJECT
  wrong repository identity ......................... REJECT
  env-tampered repository (attacker's bypass 2) ..... TOOL-ERROR (exit 2)
  abbreviated SHA ................................... REJECT
  tampered receipt bytes ............................ REJECT
  missing citation marker ........................... REJECT
  transplanted receipt (minted for page A, ships B) . REJECT
  unregistered source (closed-world) ................ REJECT
  unregistered component class (interim row 7) ...... REJECT
  expired / future activation ....................... REJECT
  v1 schema ......................................... REJECT
  self-minted truth (alternate route) ............... LOCAL-REHEARSAL-*,
      exit 3, no "PASS" substring — never a pass
  delivery mode: lawful PR delivery ................. PASS
  delivery mode: transplant / missing receipt ....... REJECT (fail closed)

Any assertion failure exits nonzero. If the live main tip moves between the
mint step and the gate step, the lawful case reports INFRA-FLAKE (the gate
correctly rejected a moved tip) instead of a gate failure.
"""

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
GATE = os.path.join(HERE, "activation_gate.py")
WORK = "/tmp/gate-proof"
sys.path.insert(0, HERE)
from activation_gate import (  # noqa: E402 — same protected source
    resolve_truth, _canonical_deliverable_bytes, RECEIPT_MARKER_RE)


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
    """Mint order: page -> canonical hash -> receipt -> marker (one pass)."""
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


def fetch_pinned_design_gate():
    """Row-7 delegate-and-verify: fetch the design lane's gate + manifest at
    the PINNED reviewed commit (content-addressed, immutable). Returns
    (gate_path, manifest_path) or ("", "") when the fetch fails — the gate
    then fails closed (DESIGN_GATE_UNAVAILABLE)."""
    import base64
    import urllib.request
    pin = "3bfa8f64cafa482a17ed89790f7be02c2e320628"
    repo = os.environ.get("GITHUB_REPOSITORY", "SoulSchoolAcademy/NayaPOWER")
    token = os.environ.get("GITHUB_TOKEN", "")
    d = tempfile.mkdtemp(prefix="design-gate-pin-")
    paths = {}
    for f, name in (("tools/design_gate.py", "design_gate.py"),
                    ("smart-blocks/manifest.json", "manifest.json")):
        try:
            req = urllib.request.Request(
                "https://api.github.com/repos/%s/contents/%s?ref=%s"
                % (repo, f, pin),
                headers={"Authorization": "Bearer " + token,
                         "Accept": "application/vnd.github+json"})
            with urllib.request.urlopen(req, timeout=30) as r:
                payload = json.load(r)
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


LAWFUL_PAGE_BODY = """<!DOCTYPE html>
<html>
<head>
<meta name="color-scheme" content="dark">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
html{background:#050507;color-scheme:dark}
body{background:#050507;color:#ffffff;font-size:18px}
</style>
</head>
<body class="naya-page"><button class="naya-btn">go</button></body>
</html>
"""

EVIL_PAGE_BODY = """<!DOCTYPE html>
<html>
<head>
<meta name="color-scheme" content="dark">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
html{background:#050507;color-scheme:dark}
body{background:#050507;color:#ffffff;font-size:18px}
</style>
</head>
<body class="naya-page"><div class="naya-evil-widget">x</div></body>
</html>
"""


def lawful_pair(name, truth, body="<html><body>lawful test page</body></html>"):
    rp = "%s/%s.json" % (WORK, name)
    dp = "%s/%s.html" % (WORK, name)
    mint_receipt(rp, truth, {"%s.html" % name: canonical_hash_of_body(body)})
    mint_page(dp, rp, body)
    return rp, dp


def main():
    os.makedirs(WORK, exist_ok=True)
    results = []

    def record(name, ok, detail):
        results.append((name, ok, detail))

    truth = resolve_truth()
    print("protected truth: repo=%s main=%s"
          % (truth["repository"], truth["main_sha"][:12]))

    # --- lawful ---
    rp, dp = lawful_pair("lawful", truth)
    code, out = run_gate(["--receipt", rp, "--deliverable", dp])
    record("lawful authentic fresh bound receipt -> PASS",
           code == 0 and out.get("verdict") == "PASS", out.get("verdict"))

    # --- adversarial matrix (each must be REJECTed, exit 1) ---
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
    # unregistered source (closed-world)
    loaded = dict(truth["source_blobs"])
    loaded["secret_sauce"] = "c" * 40
    attacks.append(("unregistered source in loaded", {"loaded": loaded},
                    "SOURCE_NOT_REGISTERED", None))
    # fingerprint mismatch
    loaded2 = dict(truth["source_blobs"])
    loaded2["design_contract"] = "d" * 40
    attacks.append(("source fingerprint mismatch", {"loaded": loaded2},
                    "SOURCE_FINGERPRINT_MISMATCH", None))

    for i, (name, over, want_viol, body) in enumerate(attacks):
        over = dict(over)
        body = body or "<html><body>attack %d</body></html>" % i
        if over.get("main_sha") == "__STALE__":
            import urllib.request
            req = urllib.request.Request(
                "https://api.github.com/repos/%s/commits/main" % truth["repository"],
                headers={"Authorization": "Bearer " + os.environ["GITHUB_TOKEN"],
                         "Accept": "application/vnd.github+json"})
            with urllib.request.urlopen(req, timeout=30) as r:
                parents = json.load(r).get("parents", [])
            over["main_sha"] = (parents[0]["sha"] if parents else "0" * 40)
        rp = "%s/attack%d.json" % (WORK, i)
        dp = "%s/attack%d.html" % (WORK, i)
        mint_receipt(rp, truth, {"attack%d.html" % i: canonical_hash_of_body(body)},
                     **over)
        mint_page(dp, rp, body)
        code, out = run_gate(["--receipt", rp, "--deliverable", dp])
        ok = (code == 1 and out.get("verdict") == "REJECT"
              and any(want_viol in v for v in out.get("violations", [])))
        record(name + " -> REJECT", ok,
               "%s %s" % (out.get("verdict"), out.get("violations")))

    # tampered bytes: marker computed over original, then flip a byte
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

    # missing citation marker
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

    # TRANSPLANT (bypass 4): receipt minted for page A ships page B.
    # Page B cites receipt A's marker, so the citation check passes — the
    # deliverable binding must still reject.
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

    # BYPASS-2 REPLAY: attacker's proven move was setting
    # GITHUB_REPOSITORY=evil-corp/stolen-repo. The runner event payload wins;
    # disagreement must fail closed (exit 2), never query the attacker's repo.
    rp, dp = lawful_pair("trustroot", truth)
    tampered_env = dict(os.environ)
    tampered_env["GITHUB_REPOSITORY"] = "evil-corp/stolen-repo"
    code, out = run_gate(["--receipt", rp, "--deliverable", dp], env=tampered_env)
    record("env-tampered repository -> TOOL-ERROR (fail closed)",
           code == 2 and out.get("verdict") == "TOOL-ERROR"
           and any("disagrees" in v for v in out.get("violations", [])),
           "%s %s" % (code, out.get("violations")))

    # --- alternate route: self-minted truth can never yield PASS ---
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

    # --- delivery mode (fail-closed PR gating) ---
    dg_path, dg_manifest = fetch_pinned_design_gate()
    dg_args = ["--design-gate", dg_path, "--design-manifest", dg_manifest]

    def make_pr_head(pages):
        d = tempfile.mkdtemp(prefix="pr-head-")
        hashes = {}
        for rel, body in pages.items():
            hashes[rel] = canonical_hash_of_body(body)
        rp = os.path.join(d, "receipt.json")
        mint_receipt(rp, truth, hashes)
        for rel, body in pages.items():
            full = os.path.join(d, rel)
            os.makedirs(os.path.dirname(full), exist_ok=True)
            mint_page(full, rp, body)
        rdir = os.path.join(d, ".naya", "activation")
        os.makedirs(rdir, exist_ok=True)
        shutil.copy(rp, os.path.join(rdir, "receipt.json"))
        return d

    # lawful delivery (page passes the REAL design lane gate too)
    d = make_pr_head({"ship.html": LAWFUL_PAGE_BODY})
    code, out = run_gate(["--delivery", "--pr-head", d,
                          "--changed-files", "ship.html", *dg_args])
    record("delivery: lawful bound PR -> PASS",
           code == 0 and out.get("verdict") == "PASS",
           "%s %s" % (out.get("verdict"), out.get("violations")))
    shutil.rmtree(d, ignore_errors=True)

    # delivery transplant: receipt binds ship.html, PR also changes evil.html
    d = make_pr_head({"ship.html": LAWFUL_PAGE_BODY})
    open(os.path.join(d, "evil.html"), "w").write("<html><body>unbound</body></html>")
    code, out = run_gate(["--delivery", "--pr-head", d,
                          "--changed-files", "ship.html,evil.html", *dg_args])
    record("delivery: unbound changed deliverable -> REJECT",
           code == 1 and any("DELIVERABLE_NOT_BOUND" in v
                             for v in out.get("violations", [])),
           "%s %s" % (out.get("verdict"), out.get("violations")))
    shutil.rmtree(d, ignore_errors=True)

    # delivery: no receipt at all -> REJECT (fail closed)
    d = tempfile.mkdtemp(prefix="pr-head-")
    open(os.path.join(d, "lonely.html"), "w").write("<html><body>x</body></html>")
    code, out = run_gate(["--delivery", "--pr-head", d,
                          "--changed-files", "lonely.html", *dg_args])
    record("delivery: missing receipt -> REJECT (fail closed)",
           code == 1 and any("RECEIPT_MISSING_OR_EMPTY" in v
                             for v in out.get("violations", [])),
           "%s %s" % (out.get("verdict"), out.get("violations")))
    shutil.rmtree(d, ignore_errors=True)

    # ROW 7 (attacker's bypass 3): undocumented component class + freestyle
    # CSS ships with a VALID receipt — the design lane's gate (pinned
    # reviewed commit, delegate-and-verify) must reject it.
    d = make_pr_head({"freestyle.html": EVIL_PAGE_BODY})
    code, out = run_gate(["--delivery", "--pr-head", d,
                          "--changed-files", "freestyle.html", *dg_args])
    record("delivery: unregistered component class -> REJECT (row 7, "
           "design lane)",
           code == 1 and any("DESIGN_GATE:" in v and "NO FREESTYLE" in v
                             for v in out.get("violations", [])),
           "%s %s" % (out.get("verdict"), out.get("violations")))
    shutil.rmtree(d, ignore_errors=True)

    # --- live-PR demonstration (best-effort): the delivery gate against a
    # real open PR (#1996, design gate — touches smart-blocks/manifest.json,
    # a deliverable path). It ships no activation receipt, so the locked door
    # must REJECT. Never fails the proof job: this is evidence, not a gate.
    d = None
    try:
        d = tempfile.mkdtemp(prefix="pr-demo-")
        code, out = run_gate(["--delivery", "--pr-head", d, "--pr", "1996",
                              "--changed-files",
                              "smart-blocks/manifest.json,tools/design_gate.py"])
        print("[DEMO] live PR #1996 delivery verdict: %s (exit %s) :: %s"
              % (out.get("verdict"), code, out.get("violations")))
        record("demo: live PR #1996 without receipt -> REJECT (fail closed)",
               code == 1 and out.get("verdict") == "REJECT", out.get("verdict"))
    except Exception as e:  # noqa: BLE001 — best-effort demo
        print("[DEMO] live-PR demonstration unavailable: %s" % e)
        record("demo: live PR #1996 (skipped — infra)", True, "skipped")
    finally:
        if d:
            shutil.rmtree(d, ignore_errors=True)

    # --- report ---
    failed = 0
    print("\n==== UNIFIED ACTIVATION GATE R2 — CI PROOF ====")
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
