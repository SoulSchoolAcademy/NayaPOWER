#!/usr/bin/env python3
"""CI proof for the unified activation gate — ROUND 2 (Naya 1's bar).

Runs in the ACTUAL GitHub Actions workflow
(.github/workflows/unified-activation-gate.yml). The protected runner
resolves truth ITSELF (runner event payload + GITHUB_TOKEN, live GitHub
API) — no caller-supplied flags.

Round-2 rows (the independent attacker's four bypasses, now closed):
  R-T1 receipt transplant (same receipt, different deliverable) . REJECT
  R-T2 unbound receipt (no deliverable_sha256) .................. REJECT
  R-T3 job mismatch (receipt job != delivery job) ............... REJECT
  R-T4 GITHUB_REPOSITORY env override .......................... TOOL-ERROR (refused)
  R-T5 freestyle undocumented component (design-gate delegation)  REJECT
  R-T6 design-gate absent from protected ref ................... BLOCKED-DESIGN-GATE-ABSENT
  R-T7 local-mode labels: no "PASS" substring, exit != 0 ....... HOLD
  R-T8 workflow trigger structure: no avoidable paths filter ... HOLD

Plus the original 14 rows (lawful PASS + adversarial REJECTs).
The lawful fixture is a design-clean page so the full pipeline
(activation + structural delegation) is exercised.

Any assertion failure exits nonzero. If the live main tip moves between the
mint step and the gate step, the lawful case reports INFRA-FLAKE instead of
a gate failure.
"""

import base64
import hashlib
import json
import os
import subprocess
import sys
from datetime import timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
GATE = os.path.join(HERE, "activation_gate.py")
WORK = "/tmp/gate-proof"
JOB = "prove the unified activation gate in CI"
sys.path.insert(0, HERE)
from activation_gate import (  # noqa: E402 — same protected source
    resolve_truth, canonical_deliverable_bytes)

DG_DIR = "/tmp/design-gate-src"
DG_PATH = os.path.join(DG_DIR, "design_gate.py")
DG_MANIFEST = os.path.join(DG_DIR, "manifest.json")
DG_PINNED_COMMIT = "3bfa8f64cafa482a17ed89790f7be02c2e320628"  # reviewed; branch refs are mutable, SHAs are not


def run_gate(receipt_path, deliverable_path, extra=()):
    p = subprocess.run(
        [sys.executable, GATE, "--receipt", receipt_path,
         "--deliverable", deliverable_path, "--json", *extra],
        capture_output=True, text=True)
    try:
        out = json.loads(p.stdout.strip().splitlines()[-1])
    except (ValueError, IndexError):
        out = {"verdict": "TOOL-OUTPUT-UNPARSEABLE",
               "violations": [p.stdout[-500:], p.stderr[-500:]]}
    return p.returncode, out


CLEAN_TEMPLATE = """<html style="background:#050507"><head>""" \
    """<meta name="color-scheme" content="dark">""" \
    """<meta name="viewport" content="width=device-width, initial-scale=1">""" \
    """<style>html{background:#050507;color-scheme:dark}""" \
    """body{background:#050507;color:#f5f5f5}</style></head>""" \
    """<body>__BODY__</body></html>"""

FREESTYLE_TEMPLATE = """<html style="background:#050507"><head>""" \
    """<meta name="color-scheme" content="dark">""" \
    """<meta name="viewport" content="width=device-width, initial-scale=1">""" \
    """<style>html{background:#050507;color-scheme:dark}""" \
    """body{background:#050507;color:#f5f5f5}""" \
    """.naya-freestyle-mega-widget{background:hotpink}</style></head>""" \
    """<body><div class="naya-freestyle-mega-widget">evil</div>__BODY__</body></html>"""


def mint(body, truth, template=CLEAN_TEMPLATE, **over):
    """Two-phase mint: marker cites receipt bytes; receipt binds the
    canonical deliverable bytes. Returns (receipt_path, page_path)."""
    r = {
        "schema": "naya.activation.receipt.v2",
        "status": "ACTIVATED",
        "session_id": "ci-proof-%s" % os.environ.get("GITHUB_RUN_ID", "local"),
        "naya_identity": "unified-gate-ci-proof",
        "human_authority": "Shawn",
        "repository": truth["repository"],
        "job": JOB,
        "gates": ["Usefulness Gate", "Binary Gate"],
        "proof_plan": "this workflow run",
        "main_sha": truth["main_sha"],
        "activated_at": (truth["now"] - timedelta(hours=1)).isoformat(),
        "loaded": dict(truth["source_blobs"]),
    }
    r.update(over)
    rb1 = json.dumps(r, sort_keys=True).encode()
    d1 = template.replace("__BODY__", body).replace(
        "</body>", "<!-- NAYA-ACTIVATION-RECEIPT-SHA256:%s --></body>"
        % hashlib.sha256(rb1).hexdigest())
    r["deliverable_sha256"] = hashlib.sha256(
        canonical_deliverable_bytes(d1)).hexdigest()
    rb2 = json.dumps(r, sort_keys=True).encode()
    d2 = template.replace("__BODY__", body).replace(
        "</body>", "<!-- NAYA-ACTIVATION-RECEIPT-SHA256:%s --></body>"
        % hashlib.sha256(rb2).hexdigest())
    assert hashlib.sha256(canonical_deliverable_bytes(d2)).hexdigest() == \
        r["deliverable_sha256"], "binding dance broken"
    rp = os.path.join(WORK, "r-%s.json" % body.replace(" ", "-")[:20])
    dp = os.path.join(WORK, "p-%s.html" % body.replace(" ", "-")[:20])
    with open(rp, "wb") as f:
        f.write(rb2)
    with open(dp, "w", encoding="utf-8") as f:
        f.write(d2)
    return rp, dp


def fetch_design_gate(token, repo):
    """Fetch the design gate + manifest from the PINNED reviewed commit.
    A branch ref would be mutable (force-pushable); the commit SHA is the
    trust anchor. Returns True on success."""
    import urllib.request
    os.makedirs(DG_DIR, exist_ok=True)
    for src, dst in (("tools/design_gate.py", DG_PATH),
                     ("smart-blocks/manifest.json", DG_MANIFEST)):
        url = ("https://api.github.com/repos/%s/contents/%s?ref=%s"
               % (repo, src, DG_PINNED_COMMIT))
        req = urllib.request.Request(url, headers={
            "Authorization": "Bearer " + token,
            "Accept": "application/vnd.github.raw",
            "X-GitHub-Api-Version": "2022-11-28"})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                data = r.read()
        except Exception as e:
            print("DESIGN-GATE FETCH FAILED for %s: %s" % (src, e))
            return False
        with open(dst, "wb") as f:
            f.write(data)
    return True


def main():
    os.makedirs(WORK, exist_ok=True)
    results = []
    token = os.environ.get("GITHUB_TOKEN", "")

    truth = resolve_truth()
    print("protected truth: repo=%s main=%s" %
          (truth["repository"], truth["main_sha"][:12]))

    dg_ok = fetch_design_gate(token, truth["repository"])
    print("design-gate delegation source: %s (%s)"
          % ("fetched from pinned " + DG_PINNED_COMMIT[:12] if dg_ok else "UNAVAILABLE",
             DG_PATH if dg_ok else "n/a"))
    dg_extra = ("--design-gate", DG_PATH,
                "--design-manifest", DG_MANIFEST) if dg_ok else ()

    def gate(rp, dp, job=JOB, extra=()):
        return run_gate(rp, dp, extra=("--job", job, *dg_extra, *extra))

    # --- lawful: full pipeline (activation + structural delegation) ---
    rp, dp = mint("lawful", truth)
    code, out = gate(rp, dp)
    if not dg_ok:
        # Without the delegation source the honest verdict is BLOCKED.
        ok = (out.get("verdict") == "BLOCKED-DESIGN-GATE-ABSENT" and code == 1)
        results.append(("lawful page, design-gate source unavailable -> "
                        "BLOCKED-DESIGN-GATE-ABSENT (honest)", True, ok,
                        out.get("verdict")))
    else:
        ok = code == 0 and out.get("verdict") == "PASS"
        results.append(("lawful authentic fresh receipt + design-clean "
                        "page -> PASS", True, ok,
                        "%s %s" % (out.get("verdict"),
                                   out.get("violations")[:2] if out.get("verdict") != "PASS" else "")))

    # --- original adversarial matrix (each must be REJECTed, exit 1) ---
    attacks = [
        ("fabricated self-asserted receipt",
         {"main_sha": "f" * 40}, "TIP_MOVED"),
        ("stale activation (old main commit)",
         {"main_sha": "__STALE__"}, "TIP_MOVED"),
        ("wrong repository identity",
         {"repository": "evil-corp/stolen-repo"}, "WRONG_REPOSITORY"),
        ("abbreviated 7-char SHA",
         {"main_sha": truth["main_sha"][:7]}, "SHA_MALFORMED"),
        ("expired activation",
         {"activated_at": (truth["now"] - timedelta(hours=5)).isoformat()},
         "ACTIVATION_EXPIRED"),
        ("future activation",
         {"activated_at": (truth["now"] + timedelta(hours=1)).isoformat()},
         "FUTURE_ACTIVATION"),
        ("retired v1 schema",
         {"schema": "naya.activation.receipt.v1"}, "WRONG_SCHEMA"),
        ("status != ACTIVATED", {"status": "PENDING"}, "NOT_ACTIVATED"),
    ]
    loaded = dict(truth["source_blobs"]); loaded["secret_sauce"] = "c" * 40
    attacks.append(("unregistered source in loaded",
                    {"loaded": loaded}, "SOURCE_NOT_REGISTERED"))
    loaded2 = dict(truth["source_blobs"]); loaded2["design_contract"] = "d" * 40
    attacks.append(("source fingerprint mismatch",
                    {"loaded": loaded2}, "SOURCE_FINGERPRINT_MISMATCH"))

    for i, (name, over, want_viol) in enumerate(attacks):
        over = dict(over)
        if over.get("main_sha") == "__STALE__":
            import urllib.request
            req = urllib.request.Request(
                "https://api.github.com/repos/%s/commits/main" % truth["repository"],
                headers={"Authorization": "Bearer " + token,
                         "Accept": "application/vnd.github+json"})
            with urllib.request.urlopen(req, timeout=30) as r:
                parents = json.load(r).get("parents", [])
            over["main_sha"] = (parents[0]["sha"] if parents else "0" * 40)
        rp, dp = mint("attack%d" % i, truth, **over)
        code, out = gate(rp, dp)
        ok = (code == 1 and out.get("verdict") == "REJECT"
              and any(want_viol in v for v in out.get("violations", [])))
        results.append((name + " -> REJECT", True, ok,
                        "%s %s" % (out.get("verdict"),
                                   [v for v in out.get("violations", [])
                                    if want_viol in v][:1])))

    # tampered bytes
    rp, dp = mint("tamper", truth)
    with open(rp, "r+b") as f:
        data = bytearray(f.read()).replace(b"ACTIVATED", b"ACTIVATED ", 1)
        f.seek(0); f.write(data); f.truncate()
    code, out = gate(rp, dp)
    ok = (code == 1 and any("CITATION_DIGEST_MISMATCH" in v
                            for v in out.get("violations", [])))
    results.append(("tampered receipt bytes -> REJECT", True, ok, out.get("verdict")))

    # --- ROUND-2 ROWS ---
    # R-T1: transplant — same receipt bytes, different deliverable
    rp, dp = mint("lawful", truth)
    with open(dp, encoding="utf-8") as f:
        d = f.read()
    evil = d.replace("<body>lawful", "<body>PRODUCTION DEPLOY ARTIFACT")
    evil_p = os.path.join(WORK, "transplant.html")
    with open(evil_p, "w", encoding="utf-8") as f:
        f.write(evil)
    code, out = gate(rp, evil_p)
    ok = (code == 1 and any("DELIVERABLE_DIGEST_MISMATCH" in v
                            for v in out.get("violations", [])))
    results.append(("R-T1 receipt transplant -> REJECT", True, ok,
                    out.get("verdict")))

    # R-T2: unbound receipt
    r = {"schema": "naya.activation.receipt.v2", "status": "ACTIVATED",
         "session_id": "x", "naya_identity": "x", "human_authority": "Shawn",
         "repository": truth["repository"], "job": JOB,
         "gates": ["Usefulness Gate"], "proof_plan": "x",
         "main_sha": truth["main_sha"],
         "activated_at": (truth["now"] - timedelta(hours=1)).isoformat(),
         "loaded": dict(truth["source_blobs"])}
    rb = json.dumps(r, sort_keys=True).encode()
    up, upp = os.path.join(WORK, "unbound.json"), os.path.join(WORK, "unbound.html")
    with open(up, "wb") as f:
        f.write(rb)
    with open(upp, "w") as f:
        f.write("<html><!-- NAYA-ACTIVATION-RECEIPT-SHA256:%s --></html>"
                % hashlib.sha256(rb).hexdigest())
    code, out = gate(up, upp)
    ok = (code == 1 and any("RECEIPT_UNBOUND" in v
                            for v in out.get("violations", [])))
    results.append(("R-T2 unbound receipt -> REJECT", True, ok, out.get("verdict")))

    # R-T3: job mismatch
    rp, dp = mint("lawful", truth)
    code, out = gate(rp, dp, job="PRODUCTION DEPLOY ARTIFACT")
    ok = (code == 1 and any("RECEIPT_JOB_MISMATCH" in v
                            for v in out.get("violations", [])))
    results.append(("R-T3 receipt job != delivery job -> REJECT", True, ok,
                    out.get("verdict")))

    # R-T4: GITHUB_REPOSITORY env override must be refused
    t4 = subprocess.run(
        [sys.executable, "-c",
         "import os,sys; sys.path.insert(0, %r);"
         "from activation_gate import resolve_truth;"
         "resolve_truth(); print('BREACH')" % HERE],
        capture_output=True, text=True,
        env={**os.environ, "GITHUB_REPOSITORY": "evil-corp/stolen-repo"})
    refused = (t4.returncode != 0 and "BREACH" not in t4.stdout
               and ("identity conflict" in (t4.stdout + t4.stderr)
                    or "evil-corp" in (t4.stdout + t4.stderr)))
    results.append(("R-T4 GITHUB_REPOSITORY override -> refused (TOOL-ERROR)",
                    True, refused,
                    (t4.stdout.strip().splitlines() or ["?"])[0][:100]))

    # R-T5: freestyle undocumented component via design-gate delegation
    if dg_ok:
        rp, dp = mint("freestyle-victim", truth, template=FREESTYLE_TEMPLATE)
        code, out = gate(rp, dp)
        ok = (code == 1 and any(v.startswith("DESIGN_GATE:") and "FREESTYLE" in v
                                for v in out.get("violations", [])))
        results.append(("R-T5 undocumented component class -> REJECT "
                        "(design-gate delegation)", True, ok,
                        [v for v in out.get("violations", [])
                         if v.startswith("DESIGN_GATE:")][:1]))
    else:
        results.append(("R-T5 skipped: delegation source unavailable",
                        True, False, "INFRA"))

    # R-T6: design-gate absent from protected ref -> BLOCKED, never silent PASS
    rp, dp = mint("lawful", truth)
    code, out = run_gate(rp, dp, extra=(
        "--job", JOB, "--design-gate", "/nonexistent/dg.py",
        "--design-manifest", "/nonexistent/m.json"))
    ok = (code == 1 and out.get("verdict") == "BLOCKED-DESIGN-GATE-ABSENT")
    results.append(("R-T6 design-gate absent -> BLOCKED-DESIGN-GATE-ABSENT "
                    "(no silent pass-through)", True, ok, out.get("verdict")))

    # R-T7: local-mode label discipline
    fake_truth = {"repository": truth["repository"],
                  "main_sha": truth["main_sha"],
                  "source_blobs": dict(truth["source_blobs"])}
    with open(os.path.join(WORK, "fake-truth.json"), "w") as f:
        json.dump(fake_truth, f)
    rp, dp = mint("lawful", truth)
    code, out = run_gate(rp, dp, extra=(
        "--mode", "local", "--truth", os.path.join(WORK, "fake-truth.json"),
        "--design-gate", DG_PATH if dg_ok else "/nonexistent/dg.py",
        "--design-manifest", DG_MANIFEST if dg_ok else "/nonexistent/m.json"))
    verdict = out.get("verdict", "")
    ok = ("PASS" not in verdict and code != 0 and
          verdict in ("CANDIDATE-LOCAL-CLEAN", "CANDIDATE-LOCAL-REJECTED",
                      "BLOCKED-DESIGN-GATE-ABSENT"))
    results.append(("R-T7 local-mode labels carry no PASS substring and exit "
                    "nonzero", True, ok, "%s exit=%d" % (verdict, code)))

    # R-T8: workflow trigger structure — no avoidable paths filter
    wf = os.path.join(os.path.dirname(HERE), ".github", "workflows",
                      "unified-activation-gate.yml")
    try:
        with open(wf, encoding="utf-8") as f:
            y = f.read()
        on_section = y.split("jobs:")[0]
        has_pr_target = "pull_request_target" in on_section
        has_no_paths_filter = ("paths:" not in on_section
                               and "paths-ignore:" not in on_section)
        has_push_main = "push" in on_section and "main" in on_section
        ok = has_pr_target and has_no_paths_filter and has_push_main
        detail = "pull_request_target=%s no-paths-filter=%s push-main=%s" % (
            has_pr_target, has_no_paths_filter, has_push_main)
    except OSError as e:
        ok, detail = False, str(e)
    results.append(("R-T8 trigger not avoidable by path (pull_request_target, "
                    "no paths filter, push to main)", True, ok, detail))

    # --- report ---
    failed = 0
    print("\n==== UNIFIED ACTIVATION GATE — CI PROOF (ROUND 2) ====")
    for name, _, ok, detail in results:
        print("[%s] %s :: %s" % ("HOLD" if ok else "BREACH", name, detail))
        if not ok:
            failed += 1
    if failed:
        try:
            t2 = resolve_truth()
            if t2["main_sha"] != truth["main_sha"]:
                print("INFRA-FLAKE: live main moved %s -> %s during the proof; "
                      "rerun the workflow" % (truth["main_sha"][:12], t2["main_sha"][:12]))
                return 2
        except Exception:
            pass
    print("==== %d/%d rows hold ====" % (len(results) - failed, len(results)))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
