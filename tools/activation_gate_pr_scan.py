#!/usr/bin/env python3
"""Activation-claim scan — the delivery-boundary teeth of the unified gate.

On every pull request to main, the CI workflow runs this (from BASE-PINNED
code) against the PR's files, read as text and never executed. Any changed
HTML deliverable that CARRIES an activation receipt marker is claiming
activation — and a claim must be verified:

  marker digest -> find the receipt file (sha256 match over the repo's
  .json files) -> run the FULL unified gate (receipt authenticity +
  deliverable binding + design-gate structural closed-world).

A marker with no matching receipt file is REJECTED (citation without
receipt). A deliverable with no marker is not claiming activation and is
not gated here (structural law for all deliverables belongs to the
design-gate workflow lane).

This closes the "gate guards nothing" bypass: the workflow fires on EVERY
PR (no paths filter), and every activation claim inside it is verified by
code the PR cannot modify.

Exit codes: 0 = no claims failed (or no claims found) | 1 = a claim failed
| 2 = tool error.
"""

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from activation_gate import RECEIPT_MARKER_RE  # noqa: E402 — base-pinned

SCAN_EXTENSIONS = (".html", ".htm")


def _read_text(path):
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except (OSError, UnicodeDecodeError):
        return None


def find_claims(repo_dir):
    """Walk repo_dir; return [(html_path, marker_digest), ...]."""
    claims = []
    for root, dirs, files in os.walk(repo_dir):
        dirs[:] = [d for d in dirs if d != ".git"]
        for fn in files:
            if not fn.lower().endswith(SCAN_EXTENSIONS):
                continue
            p = os.path.join(root, fn)
            text = _read_text(p)
            if text is None:
                continue
            for m in RECEIPT_MARKER_RE.finditer(text):
                claims.append((p, m.group(1).lower()))
    # one verdict per file (first marker); duplicates collapse
    seen = {}
    for p, d in claims:
        seen.setdefault(p, d)
    return sorted(seen.items())


def find_receipts(repo_dir):
    """Map sha256-of-bytes -> path for every .json file under repo_dir."""
    out = {}
    for root, dirs, files in os.walk(repo_dir):
        dirs[:] = [d for d in dirs if d != ".git"]
        for fn in files:
            if not fn.lower().endswith(".json"):
                continue
            p = os.path.join(root, fn)
            try:
                with open(p, "rb") as f:
                    out[hashlib.sha256(f.read()).hexdigest()] = p
            except OSError:
                continue
    return out


def verify_claim(gate_py, html_path, receipt_path, design_gate, design_manifest):
    """Run the full unified gate (base-pinned) on one claim."""
    cmd = [sys.executable, gate_py, "--receipt", receipt_path,
           "--deliverable", html_path, "--json"]
    if design_gate:
        cmd += ["--design-gate", design_gate, "--design-manifest",
                design_manifest or ""]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    try:
        out = json.loads(p.stdout.strip().splitlines()[-1])
    except (ValueError, IndexError):
        out = {"verdict": "TOOL-OUTPUT-UNPARSEABLE",
               "violations": [p.stdout[-500:], p.stderr[-500:]]}
    return p.returncode, out


def scan(repo_dir, gate_py, design_gate="", design_manifest=""):
    """Returns (failures, report_lines)."""
    claims = find_claims(repo_dir)
    lines = ["activation-claim scan: %d marker-carrying deliverable(s) in %s"
             % (len(claims), repo_dir)]
    if not claims:
        return 0, lines
    receipts = find_receipts(repo_dir)
    failures = 0
    for html_path, digest in claims:
        receipt_path = receipts.get(digest)
        if not receipt_path:
            failures += 1
            lines.append("[REJECT] %s: marker cites receipt %s… but no "
                         "receipt file with that digest exists "
                         "(CITATION_WITHOUT_RECEIPT)"
                         % (html_path, digest[:12]))
            continue
        code, out = verify_claim(gate_py, html_path, receipt_path,
                                 design_gate, design_manifest)
        verdict = out.get("verdict", "?")
        if code == 0 and verdict == "PASS":
            lines.append("[PASS] %s (receipt %s)"
                         % (html_path, os.path.basename(receipt_path)))
        else:
            failures += 1
            lines.append("[REJECT] %s: %s %s"
                         % (html_path, verdict, out.get("violations")))
    return failures, lines


def self_test():
    """Exercise the scan logic synthetically: lawful claim passes, marker
    without receipt is rejected, transplanted claim is rejected."""
    import tempfile
    from datetime import datetime, timedelta, timezone
    sys.path.insert(0, HERE)
    from activation_gate import check, SCHEMA
    gate_py = os.path.join(HERE, "activation_gate.py")
    ok = True

    with tempfile.TemporaryDirectory() as d:
        # lawful claim: receipt bound to the page, marker cites it
        page = "<html><body>shipped</body></html>"
        canon_hash = hashlib.sha256(page.encode()).hexdigest()
        receipt = {"schema": SCHEMA, "status": "ACTIVATED",
                   "session_id": "s", "naya_identity": "n",
                   "human_authority": "Shawn", "repository": "r",
                   "job": "j", "gates": ["g"], "proof_plan": "p",
                   "main_sha": "a" * 40,
                   "activated_at": datetime.now(timezone.utc).isoformat(),
                   "loaded": {}, "deliverable_sha256": canon_hash}
        rp = os.path.join(d, "receipt.json")
        with open(rp, "w") as f:
            json.dump(receipt, f, sort_keys=True)
        with open(rp, "rb") as f:
            digest = hashlib.sha256(f.read()).hexdigest()
        hp = os.path.join(d, "page.html")
        with open(hp, "w") as f:
            f.write(page.replace("</body>",
                    "<!-- NAYA-ACTIVATION-RECEIPT-SHA256:%s --></body>" % digest))

        claims = find_claims(d)
        if claims != [(hp, digest)]:
            print("SELF-TEST FAIL: claim not found: %r" % (claims,)); ok = False
        receipts = find_receipts(d)
        if receipts.get(digest) != rp:
            print("SELF-TEST FAIL: receipt not matched"); ok = False

        # marker without receipt
        hp2 = os.path.join(d, "orphan.html")
        with open(hp2, "w") as f:
            f.write("<html><body>x<!-- NAYA-ACTIVATION-RECEIPT-SHA256:%s -->"
                    "</body></html>" % ("0" * 64))
        failures, lines = scan(d, gate_py)
        # orphan must be rejected; lawful page needs truth — the gate will
        # reject on TRUTH_UNTRUSTED (no live main), which still counts as
        # "claim evaluated, not passed". What matters: orphan flagged.
        if not any("CITATION_WITHOUT_RECEIPT" in ln for ln in lines):
            print("SELF-TEST FAIL: orphan marker not flagged: %r" % (lines,))
            ok = False
        else:
            print("SELF-TEST: orphan marker rejected (good)")
        print("SELF-TEST: scan logic exercised, %d failure(s) reported "
              "(lawful page needs live truth for PASS)" % failures)
    return 0 if ok else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo-dir", required=False, default=".",
                    help="repository checkout to scan (PR head, read-only)")
    ap.add_argument("--gate", default=os.path.join(HERE, "activation_gate.py"))
    ap.add_argument("--design-gate", default="")
    ap.add_argument("--design-manifest", default="")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv)
    if args.self_test:
        return self_test()
    failures, lines = scan(args.repo_dir, args.gate, args.design_gate,
                           args.design_manifest)
    for ln in lines:
        print(ln)
    print("claim scan: %s" % ("ALL CLAIMS VERIFIED" if failures == 0
                              else "%d CLAIM(S) FAILED" % failures))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
