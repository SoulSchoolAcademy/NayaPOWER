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
  self-minted truth (alternate route) ........... CANDIDATE-LOCAL-*, never PASS

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
from activation_gate import resolve_truth  # noqa: E402 — same protected source


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


def write_receipt(path, truth, **over):
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
    with open(path, "w", encoding="utf-8") as f:
        json.dump(r, f, sort_keys=True)
    return path


def write_page(path, receipt_path, marker=True):
    with open(receipt_path, "rb") as f:
        digest = hashlib.sha256(f.read()).hexdigest()
    body = "<html><body>lawful test page</body></html>"
    if marker:
        body = body.replace("</body>",
                            "<!-- NAYA-ACTIVATION-RECEIPT-SHA256:%s --></body>" % digest)
    with open(path, "w", encoding="utf-8") as f:
        f.write(body)
    return path


def main():
    os.makedirs(WORK, exist_ok=True)
    results = []

    truth = resolve_truth()
    print("protected truth: repo=%s main=%s" %
          (truth["repository"], truth["main_sha"][:12]))

    # --- lawful ---
    rp = write_receipt(f"{WORK}/lawful.json", truth)
    dp = write_page(f"{WORK}/lawful.html", rp)
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
        rp = write_receipt(f"{WORK}/attack{i}.json", truth, **over)
        dp = write_page(f"{WORK}/attack{i}.html", rp)
        code, out = run_gate(rp, dp)
        ok = (code == 1 and out.get("verdict") == "REJECT"
              and any(want_viol in v for v in out.get("violations", [])))
        results.append((name + " -> REJECT", True, ok,
                        "%s %s" % (out.get("verdict"), out.get("violations"))))

    # tampered bytes: marker computed over original, then flip a byte
    rp = write_receipt(f"{WORK}/tamper.json", truth)
    dp = write_page(f"{WORK}/tamper.html", rp)
    with open(rp, "r+b") as f:
        data = bytearray(f.read()).replace(b"ACTIVATED", b"ACTIVATED ", 1)
        f.seek(0); f.write(data); f.truncate()
    code, out = run_gate(rp, dp)
    ok = (code == 1 and any("CITATION_DIGEST_MISMATCH" in v
                            for v in out.get("violations", [])))
    results.append(("tampered receipt bytes -> REJECT", True, ok, out.get("verdict")))

    # missing citation marker
    rp = write_receipt(f"{WORK}/nocite.json", truth)
    dp = write_page(f"{WORK}/nocite.html", rp, marker=False)
    code, out = run_gate(rp, dp)
    ok = (code == 1 and any("CITATION_MISSING" in v
                            for v in out.get("violations", [])))
    results.append(("missing citation marker -> REJECT", True, ok, out.get("verdict")))

    # --- alternate route: self-minted truth can never yield PASS ---
    fake_truth = {"repository": truth["repository"],
                  "main_sha": truth["main_sha"],
                  "source_blobs": dict(truth["source_blobs"])}
    with open(f"{WORK}/fake-truth.json", "w") as f:
        json.dump(fake_truth, f)
    rp = write_receipt(f"{WORK}/selfmint.json", truth)
    dp = write_page(f"{WORK}/selfmint.html", rp)
    code, out = run_gate(rp, dp, extra=("--mode", "local", "--truth",
                                       f"{WORK}/fake-truth.json"))
    verdict = out.get("verdict", "")
    ok = verdict.startswith("CANDIDATE-LOCAL-") and verdict != "PASS"
    results.append(("self-minted truth alternate route -> CANDIDATE-LOCAL-*, never PASS",
                    True, ok, verdict))

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
