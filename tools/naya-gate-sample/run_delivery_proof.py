#!/usr/bin/env python3
"""Delivery proof for the Naya unified gate (blocker 2: the gate must guard a
REAL deliverable, not just itself).

What it does, end to end:
  1. Builds a FRESH activation receipt from live repository state at run time
     (live tip via the gate's trusted fetch, current timestamp, live component
     blob SHAs via the gate's trusted tree fetch). Nothing is committed; the
     receipt is time-bound and cannot be pre-baked.
  2. Embeds the citation marker in a copy of tools/naya-gate-sample/product.html.
  3. POSITIVE: runs tools/naya_gate.py --require-activation --receipt in
     --enforce mode against the real deliverable. Must PASS (exit 0),
     enforcement-grade (no ADVISORY).
  4. NEGATIVES (each must FAIL with the named verdict):
     - tampered receipt bytes (marker no longer matches) -> FAIL-CITATION
     - backdated 5h receipt (fresh marker)               -> FAIL-STALE
     - forged component SHA (fresh marker)               -> FAIL-COMPONENT-MISMATCH

Exit 0 = the gate demonstrably guards a real deliverable, lawful and
adversarial. Exit 1 = the proof failed (details printed).

Run: python3 tools/naya-gate-sample/run_delivery_proof.py [--out-dir DIR]
CI:  .github/workflows/naya-gate-delivery.yml runs this on every relevant push/PR.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE.parent))
import naya_gate as G  # noqa: E402

SAMPLE_COMPONENTS = ["HUB/DESIGN-CONTRACT.md", "AGENTS.md"]
CANON = "SoulSchoolAcademy/NayaPOWER"


def build_receipt(out_dir: Path) -> tuple[Path, Path]:
    """Build a fresh receipt from live state; return (receipt_path, marked_html)."""
    tip, err = G.resolve_live_tip_trusted()
    if err:
        raise RuntimeError(f"trusted tip fetch failed: {err}")
    live, err = G.fetch_live_tree_blob_shas(SAMPLE_COMPONENTS)
    if err:
        raise RuntimeError(f"trusted component fetch failed: {err}")
    now = datetime.now(timezone.utc)
    receipt = {
        "schema": "naya.activation.receipt.v2",
        "status": "ACTIVATED",
        "session_id": f"gate-delivery-proof-{uuid.uuid4().hex[:12]}",
        "naya_identity": "naya-gate-delivery (CI proof)",
        "human_authority": "Shawn",
        "repository": CANON,
        "job": "gate delivery proof: guard a real deliverable",
        "gates": ["SN-0787", "delivery-gate", "closed-world-components"],
        "proof_plan": ".github/workflows/naya-gate-delivery.yml",
        "main_sha": tip,
        "activated_at": now.isoformat(),
        "components": [{"path": p, "sha": live[p]} for p in sorted(live)],
    }
    rp = out_dir / "receipt.json"
    rp.write_bytes(json.dumps(receipt, indent=2).encode())
    digest = hashlib.sha256(rp.read_bytes()).hexdigest()
    html = (HERE / "product.html").read_text(encoding="utf-8")
    marker = f"<!-- NAYA-ACTIVATION-RECEIPT-SHA256:{digest} -->"
    marked = html.replace("</body>", f"{marker}</body>")
    hp = out_dir / "product.html"
    hp.write_text(marked, encoding="utf-8")
    return rp, hp


def run_gate(html: Path, receipt: Path, manifest: Path) -> tuple[int, str]:
    r = subprocess.run(
        [sys.executable, str(HERE.parent / "naya_gate.py"), str(html),
         "--manifest", str(manifest),
         "--require-activation", "--receipt", str(receipt)],
        capture_output=True, text=True, timeout=300)
    return r.returncode, r.stdout + r.stderr


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-dir", default=None)
    args = ap.parse_args()
    out = Path(args.out_dir) if args.out_dir else Path(tempfile.mkdtemp(prefix="gate-proof-"))
    out.mkdir(parents=True, exist_ok=True)
    manifest = HERE / "manifest.json"
    results: list[tuple[str, bool, str]] = []

    def record(name: str, ok: bool, detail: str = ""):
        results.append((name, ok, detail))
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail and not ok else ""))

    # ---- build fresh lawful artifacts ----
    try:
        rp, hp = build_receipt(out)
    except RuntimeError as e:
        print(f"DELIVERY PROOF: ABORT — {e}")
        return 1
    print(f"receipt: {rp}\ndeliverable: {hp}")

    # ---- POSITIVE: lawful fresh receipt passes, enforcement-grade ----
    code, out_text = run_gate(hp, rp, manifest)
    record("lawful fresh receipt passes in --enforce mode",
           code == 0 and "NAYA GATE: PASS" in out_text and "ADVISORY" not in out_text,
           out_text[-400:])

    # ---- NEGATIVE 1: tampered receipt bytes -> FAIL-CITATION ----
    tampered = out / "receipt-tampered.json"
    raw = bytearray(rp.read_bytes())
    raw[len(raw) // 2] ^= 0x01  # flip one byte mid-file (JSON stays parseable)
    tampered.write_bytes(bytes(raw))
    code, out_text = run_gate(hp, tampered, manifest)
    record("tampered receipt bytes rejected",
           code == 1 and "FAIL-CITATION" in out_text, out_text[-400:])

    # ---- NEGATIVE 2: stale receipt (5h old, fresh marker) -> FAIL-STALE ----
    stale = out / "receipt-stale.json"
    r = json.loads(rp.read_bytes())
    from datetime import timedelta
    r["activated_at"] = (datetime.now(timezone.utc) - timedelta(hours=5)).isoformat()
    stale.write_bytes(json.dumps(r).encode())
    d = hashlib.sha256(stale.read_bytes()).hexdigest()
    hp_stale = out / "product-stale.html"
    hp_stale.write_text((HERE / "product.html").read_text(encoding="utf-8").replace(
        "</body>", f"<!-- NAYA-ACTIVATION-RECEIPT-SHA256:{d} --></body>"), encoding="utf-8")
    code, out_text = run_gate(hp_stale, stale, manifest)
    record("stale receipt rejected",
           code == 1 and "FAIL-STALE" in out_text, out_text[-400:])

    # ---- NEGATIVE 3: forged component SHA (fresh marker) -> FAIL-COMPONENT-MISMATCH ----
    forged = out / "receipt-forged-component.json"
    r = json.loads(rp.read_bytes())
    r["components"][0]["sha"] = "0" * 40
    forged.write_bytes(json.dumps(r).encode())
    d = hashlib.sha256(forged.read_bytes()).hexdigest()
    hp_forged = out / "product-forged.html"
    hp_forged.write_text((HERE / "product.html").read_text(encoding="utf-8").replace(
        "</body>", f"<!-- NAYA-ACTIVATION-RECEIPT-SHA256:{d} --></body>"), encoding="utf-8")
    code, out_text = run_gate(hp_forged, forged, manifest)
    record("forged component SHA rejected",
           code == 1 and "FAIL-COMPONENT-MISMATCH" in out_text, out_text[-400:])

    # ---- NEGATIVE 4: undocumented component class -> NO FREESTYLE ----
    hp_sneaky = out / "product-sneaky.html"
    sneaky = (HERE / "product.html").read_text(encoding="utf-8").replace(
        'class="naya-proof-badge"', 'class="naya-proof-badge mystery-widget"')
    rp2, _ = build_receipt(out)  # fresh lawful receipt for the sneaky page
    d2 = hashlib.sha256(rp2.read_bytes()).hexdigest()
    hp_sneaky.write_text(sneaky.replace(
        "</body>", f"<!-- NAYA-ACTIVATION-RECEIPT-SHA256:{d2} --></body>"), encoding="utf-8")
    code, out_text = run_gate(hp_sneaky, rp2, manifest)
    record("undocumented component class rejected (closed-world)",
           code == 1 and "NO FREESTYLE" in out_text and "mystery-widget" in out_text,
           out_text[-400:])

    ok = all(r[1] for r in results)
    print(f"DELIVERY PROOF: {'ALL GREEN' if ok else 'BROKEN'} "
          f"({sum(r[1] for r in results)}/{len(results)} controls behaved)")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
