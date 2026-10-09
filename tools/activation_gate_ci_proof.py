#!/usr/bin/env python3
"""CI proof for the unified activation gate (Naya 1's bar).

Runs in the ACTUAL GitHub Actions workflow
(.github/workflows/unified-activation-gate.yml). The protected runner
resolves truth ITSELF (GITHUB_REPOSITORY + GITHUB_TOKEN from the runner
context, live GitHub API) — no caller-supplied flags.

Proves, with exact exit codes:
  lawful authentic fresh receipt ................. PASS (exit 0)
  fabricated / self-asserted receipt ............. REJECT (exit 1)
  stale activation (genuinely old main commit) ... REJECT
  wrong repository identity ..................... REJECT
  abbreviated SHA ............................... REJECT
  tampered receipt bytes ........................ REJECT
  missing citation marker ....................... REJECT
  unregistered source (closed-world) ............ REJECT
  expired / future activation ................... REJECT
  v1 schema ..................................... REJECT
  receipt transplant (marker replayed on another deliverable) . REJECT
  unbound receipt (no deliverables[]) ........... REJECT
  self-minted truth (alternate route) ........... LOCAL-REHEARSAL-*, never PASS (exit 3)

Any assertion failure exits nonzero. If the live main tip moves between the
mint step and the gate step, the lawful case reports INFRA-FLAKE (the gate
correctly rejected a moved tip) instead of a gate failure.
"""

import hashlib
import json
import os
import subprocess
import sys
from datetime import timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
GATE = os.path.join(HERE, "activation_gate.py")
WORK = "/tmp/gate-proof"
sys.path.insert(0, HERE)
from activation_gate import (  # noqa: E402 — same protected source
    resolve_truth, canonical_deliverable_bytes)


def run_gate(receipt_path, deliverable_path, extra=()):
    p = subprocess.run(
        [sys.executable, GATE, "--receipt", receipt_path,
         "--deliverable", deliverable_path, "--json", *extra],
        capture_output=True, text=True)
    try:
        out = json.loads(p.stdout.strip().splitlines()[-1])
    except (ValueError, IndexError):
        out = {"verdict": "TOOL-OUTPUT-UNPARSEABLE", "violations": [p.stdout, p.stderr]}
    return p.returncode, out


def mint(name, truth, body, **over):
    """Two-phase mint: the marker cites the receipt bytes; the receipt binds
    the canonical (marker-stripped) deliverable bytes. Returns
    (receipt_path, deliverable_path)."""
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
    }
    r.update(over)
    rb1 = json.dumps(r, sort_keys=True).encode()
    d1 = body.replace("</body>",
                      "<!-- NAYA-ACTIVATION-RECEIPT-SHA256:%s --></body>"
                      % hashlib.sha256(rb1).hexdigest())
    r["deliverables"] = [
        {"path": "%s.html" % name,
         "sha256": hashlib.sha256(canonical_deliverable_bytes(d1)).hexdigest()}]
    rb2 = json.dumps(r, sort_keys=True).encode()
    d2 = body.replace("</body>",
                      "<!-- NAYA-ACTIVATION-RECEIPT-SHA256:%s --></body>"
                      % hashlib.sha256(rb2).hexdigest())
    assert hashlib.sha256(canonical_deliverable_bytes(d2)).hexdigest() == \
        r["deliverables"][0]["sha256"], "binding dance broken"
    rp = os.path.join(WORK, "r-%s.json" % name)
    dp = os.path.join(WORK, "p-%s.html" % name)
    with open(rp, "wb") as f:
        f.write(rb2)
    with open(dp, "w", encoding="utf-8") as f:
        f.write(d2)
    return rp, dp


BODY = "<html><body>lawful test page</body></html>"


def main():
    os.makedirs(WORK, exist_ok=True)
    results = []

    truth = resolve_truth()
    print("protected truth: repo=%s main=%s" %
          (truth["repository"], truth["main_sha"][:12]))

    # --- lawful ---
    rp, dp = mint("lawful", truth, BODY)
    code, out = run_gate(rp, dp)
    lawful_ok = code == 0 and out.get("verdict") == "PASS"
    results.append(("lawful authentic fresh receipt -> PASS", True, lawful_ok,
                    out.get("verdict")))

    # --- adversarial matrix (each must be REJECTed, exit 1) ---
    attacks = []
    # 1. fabricated: plausible-looking but not live main
    attacks.append(("fabricated self-asserted receipt",
                    {"main_sha": "f" * 40}, "TIP_MOVED"))
    # 2. stale: genuinely old main commit (first parent of live main)
    attacks.append(("stale activation (old main commit)",
                    {"main_sha": "__STALE__"}, "TIP_MOVED"))
    # 3. wrong repository
    attacks.append(("wrong repository identity",
                    {"repository": "evil-corp/stolen-repo"}, "WRONG_REPOSITORY"))
    # 4. abbreviated SHA
    attacks.append(("abbreviated 7-char SHA",
                    {"main_sha": truth["main_sha"][:7]}, "SHA_MALFORMED"))
    # 5. expired
    attacks.append(("expired activation",
                    {"activated_at": (truth["now"] - timedelta(hours=5)).isoformat()},
                    "ACTIVATION_EXPIRED"))
    # 6. future
    attacks.append(("future activation",
                    {"activated_at": (truth["now"] + timedelta(hours=1)).isoformat()},
                    "FUTURE_ACTIVATION"))
    # 7. v1 schema
    attacks.append(("retired v1 schema",
                    {"schema": "naya.activation.receipt.v1"}, "WRONG_SCHEMA"))
    # 8. unregistered source (closed-world)
    loaded = dict(truth["source_blobs"]); loaded["secret_sauce"] = "c" * 40
    attacks.append(("unregistered source in loaded",
                    {"loaded": loaded}, "SOURCE_NOT_REGISTERED"))
    # 9. fingerprint mismatch
    loaded2 = dict(truth["source_blobs"]); loaded2["design_contract"] = "d" * 40
    attacks.append(("source fingerprint mismatch",
                    {"loaded": loaded2}, "SOURCE_FINGERPRINT_MISMATCH"))
    # 10. not activated
    attacks.append(("status != ACTIVATED", {"status": "PENDING"}, "NOT_ACTIVATED"))

    for i, (name, over, want_viol) in enumerate(attacks):
        over = dict(over)
        if over.get("main_sha") == "__STALE__":
            # resolve the genuinely previous main commit
            import urllib.request
            req = urllib.request.Request(
                "https://api.github.com/repos/%s/commits/main" % truth["repository"],
                headers={"Authorization": "Bearer " + os.environ["GITHUB_TOKEN"],
                         "Accept": "application/vnd.github+json"})
            with urllib.request.urlopen(req, timeout=30) as r:
                parents = json.load(r).get("parents", [])
            over["main_sha"] = (parents[0]["sha"] if parents else "0" * 40)
        rp, dp = mint("attack%d" % i, truth, BODY, **over)
        code, out = run_gate(rp, dp)
        ok = (code == 1 and out.get("verdict") == "REJECT"
              and any(want_viol in v for v in out.get("violations", [])))
        results.append((name + " -> REJECT", True, ok,
                        "%s %s" % (out.get("verdict"), out.get("violations"))))

    # tampered bytes: marker computed over original, then flip a byte
    rp, dp = mint("tamper", truth, BODY)
    with open(rp, "r+b") as f:
        data = bytearray(f.read()).replace(b"ACTIVATED", b"ACTIVATED ", 1)
        f.seek(0); f.write(data); f.truncate()
    code, out = run_gate(rp, dp)
    ok = (code == 1 and any("CITATION_DIGEST_MISMATCH" in v
                            for v in out.get("violations", [])))
    results.append(("tampered receipt bytes -> REJECT", True, ok, out.get("verdict")))

    # missing citation marker
    rp, dp = mint("nocite", truth, BODY)
    with open(dp, "w", encoding="utf-8") as f:
        f.write(BODY)  # deliverable without the marker
    code, out = run_gate(rp, dp)
    ok = (code == 1 and any("CITATION_MISSING" in v
                            for v in out.get("violations", [])))
    results.append(("missing citation marker -> REJECT", True, ok, out.get("verdict")))

    # HOTFIX ROW 1: transplant — the lawful receipt's marker replayed onto
    # different deliverable bytes. Citation passes; the binding must fail.
    rp, dp = mint("transplant", truth, BODY)
    with open(dp, encoding="utf-8") as f:
        page = f.read()
    marker_start = page.index("<!--")
    other = ("<html><body>PRODUCTION DEPLOY ARTIFACT</body>"
             + page[marker_start:])
    op = os.path.join(WORK, "p-transplant-other.html")
    with open(op, "w", encoding="utf-8") as f:
        f.write(other)
    code, out = run_gate(rp, op)
    ok = (code == 1 and out.get("verdict") == "REJECT"
          and any("DELIVERABLE_BINDING_MISMATCH" in v
                  for v in out.get("violations", [])))
    results.append(("receipt transplant onto other deliverable -> REJECT", True,
                    ok, "%s %s" % (out.get("verdict"), out.get("violations"))))

    # HOTFIX ROW 2: unbound receipt — strip the binding, the receipt must
    # fail closed.
    rp, dp = mint("unbound", truth, BODY)
    with open(rp, "rb") as f:
        receipt = json.loads(f.read())
    del receipt["deliverables"]
    rb_raw = json.dumps(receipt, sort_keys=True).encode()
    with open(rp, "wb") as f:
        f.write(rb_raw)
    with open(dp, "w", encoding="utf-8") as f:
        f.write(BODY.replace(
            "</body>",
            "<!-- NAYA-ACTIVATION-RECEIPT-SHA256:%s --></body>"
            % hashlib.sha256(rb_raw).hexdigest()))
    code, out = run_gate(rp, dp)
    ok = (code == 1 and out.get("verdict") == "REJECT"
          and any("DELIVERABLES_UNBOUND" in v
                  for v in out.get("violations", [])))
    results.append(("unbound receipt (no deliverables[]) -> REJECT", True,
                    ok, "%s %s" % (out.get("verdict"), out.get("violations"))))

    # --- alternate route: self-minted truth can never yield PASS ---
    fake_truth = {"repository": truth["repository"],
                  "main_sha": truth["main_sha"],
                  "source_blobs": dict(truth["source_blobs"])}
    with open(f"{WORK}/fake-truth.json", "w") as f:
        json.dump(fake_truth, f)
    rp, dp = mint("selfmint", truth, BODY)
    code, out = run_gate(rp, dp, extra=("--mode", "local", "--truth",
                                       f"{WORK}/fake-truth.json"))
    verdict = out.get("verdict", "")
    # HOTFIX: no "PASS" substring anywhere in the local verdict, and the
    # local code path (exit 3) is unambiguous — it can never be read as a
    # protected pass (exit 0).
    ok = (code == 3 and verdict.startswith("LOCAL-REHEARSAL-")
          and "PASS" not in verdict)
    results.append(("self-minted truth alternate route -> LOCAL-REHEARSAL-*, never PASS, exit 3",
                    True, ok, "%s (exit %d)" % (verdict, code)))

    # --- report ---
    failed = 0
    print("\n==== UNIFIED ACTIVATION GATE — CI PROOF ====")
    for name, _, ok, detail in results:
        print("[%s] %s :: %s" % ("HOLD" if ok else "BREACH", name, detail))
        if not ok:
            failed += 1
    # infra-flake check: did the tip move mid-proof?
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
