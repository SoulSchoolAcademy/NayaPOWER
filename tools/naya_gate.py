#!/usr/bin/env python3
"""Naya unified delivery gate — code is law, machine-forced.

ONE gate at the delivery boundary, fusing three existing efforts
(no competing gates, no duplication):

  STAGE 1 — DESIGN (structural)
      Fused from Naya 5's tools/design_gate.py @ 728cab40
      (owner: Naya 5 / Smart Blocks lane; deep design rules stay hers).
      7 machine-provable structural laws.

  STAGE 2 — ACTIVATION (drink-first, trusted runner)
      Fused from:
      - Naya 4's NAYA-ACTIVATION/tools/drink_first_gate.py (PR #1979, 14/14 green)
        — fail-closed verdicts: unactivated / tip-moved / stale / citation / schema.
      - Naya 3's tools/qa/activation_receipt_consistency.mjs (PR #1974)
        — receipt consistency falsifier: schema, identity, repository binding,
          main_sha match, freshness, citation binding.
      - Naya 5's citation marker binding (sha256 of exact receipt bytes).

      TRUSTED RUNNER (SN-0787): a builder can forge both the receipt and the
      expected hashes, so expected values must come from a source the builder
      cannot write. In --enforce mode (default with --require-activation) the
      gate resolves the live tip ITSELF via `git ls-remote` on the canonical
      repo and compares the receipt against THAT. A caller-supplied --live-tip
      is honored ONLY with --trust-caller, and the verdict is then labeled
      ADVISORY — never enforcement. If the trusted fetch fails, the gate fails
      closed (FAIL-TRUSTED-FETCH): unverifiable is not shippable.

  STAGE 3 — WORKFLOW PROOF
      tools/test_naya_gate.py proves the required workflow actually runs the
      gate: adversarial fixtures (valid component passes; forbidden HTML fails;
      missing/stale/wrong-repo/forged-tip receipts fail) plus an end-to-end
      enforce-mode run against the REAL live tip.

Receipt schemas accepted: naya.activation.receipt.v1 (drink-first) and
naya.activation.receipt.v2 (activation protocol). The gate requires the union
of critical fields: status ACTIVATED, repository bound to the canonical repo,
40-hex main_sha, fresh activation timestamp, non-empty loaded set (v1) or
identity+job+gates (v2).

Usage:
    python3 tools/naya_gate.py --product page.html [--manifest m.json]
    python3 tools/naya_gate.py --product page.html --require-activation --receipt r.json
    python3 tools/naya_gate.py --product page.html --require-activation --receipt r.json --trust-caller --live-tip <sha>

Exit 0 = PASS. Exit 1 = FAIL (violations named). Exit 2 = tool error.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CANONICAL_REPO = "SoulSchoolAcademy/NayaPOWER"
CANONICAL_GIT_URL = "https://github.com/SoulSchoolAcademy/NayaPOWER.git"
RECEIPT_SCHEMAS = ("naya.activation.receipt.v1", "naya.activation.receipt.v2")
RECEIPT_TTL = timedelta(hours=4)
RECEIPT_MARKER_RE = re.compile(
    r"<!--\s*NAYA-ACTIVATION-RECEIPT-SHA256:([a-fA-F0-9]{64})\s*-->")
_NAYA_PREFIXES = ("naya-", "board", "orb-", "lv-", "torb", "gem-")


# =====================================================================
# STAGE 1 — DESIGN (fused from Naya 5 tools/design_gate.py @ 728cab40)
# =====================================================================

def read_page(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def inline_css(html: str) -> str:
    return "\n".join(re.findall(r"<style[^>]*>(.*?)</style>", html, re.S | re.I))


def _bg_of_rule(css: str, selector: str):
    for m in re.finditer(re.escape(selector) + r"\s*\{([^}]*)\}", css, re.I):
        bg = re.search(r"background(?:-color)?\s*:\s*([^;}]+);?", m.group(1), re.I)
        if bg:
            return bg.group(1).strip()
    return None


def _root_vars(css: str) -> dict:
    vars = {}
    for m in re.finditer(r":root\s*\{([^}]*)\}", css, re.I):
        for vm in re.finditer(r"--([a-zA-Z0-9_-]+)\s*:\s*([^;}]+);?", m.group(1)):
            vars[vm.group(1)] = vm.group(2).strip()
    return vars


def _resolve_vars(color: str, vars: dict, depth: int = 0) -> str:
    if depth > 5:
        return color
    m = re.search(r"var\(\s*--([a-zA-Z0-9_-]+)", color)
    if m and m.group(1) in vars:
        return _resolve_vars(vars[m.group(1)], vars, depth + 1)
    return color


def _is_dark(color: str, vars: dict | None = None) -> bool:
    color = _resolve_vars(color, vars or {})
    c = color.strip().lower()
    if c in ("transparent", "none", "initial", "inherit"):
        return True
    m = re.match(r"#([0-9a-f]{3,8})", c)
    if m:
        h = m.group(1)
        if len(h) == 3:
            h = "".join(ch * 2 for ch in h)
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        return (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255 < 0.35
    if "gradient" in c:
        first = c.split(",", 1)[1] if "," in c else c
        mm = re.search(r"#([0-9a-f]{3,8})", first)
        if mm:
            return _is_dark("#" + mm.group(1))
        return not re.search(r"\bwhite\b", first)
    if re.search(r"\bwhite\b", c):
        return False
    rgba = re.match(r"rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)", c)
    if rgba:
        r, g, b = map(int, rgba.groups())
        return (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255 < 0.35
    return True


def check_self_contained(html: str) -> list[str]:
    v = []
    for m in re.finditer(r'<link[^>]+rel=["\']stylesheet["\'][^>]*>', html, re.I):
        tag = m.group(0)
        href = re.search(r'href=["\']([^"\']+)', tag, re.I)
        ref = href.group(1) if href else tag
        if not ref.startswith("data:"):
            v.append(f"SELF-CONTAINED: external stylesheet reference: {ref}")
    for m in re.finditer(r'<script[^>]+src=["\']([^"\']+)["\']', html, re.I):
        if not m.group(1).startswith("data:"):
            v.append(f"SELF-CONTAINED: external script reference: {m.group(1)}")
    return v


def check_black_root(html: str, css: str) -> list[str]:
    v = []
    vars = _root_vars(css)
    for sel in ("html", "body"):
        bg = _bg_of_rule(css, sel)
        if bg is None and sel == "body":
            m = re.search(r"body\.[a-zA-Z0-9_-]+\s*\{([^}]*)\}", css, re.I)
            if m:
                b2 = re.search(r"background(?:-color)?\s*:\s*([^;}]+);?", m.group(1), re.I)
                bg = b2.group(1).strip() if b2 else None
        if bg is None:
            v.append(f"BLACK ROOT: no background declared for `{sel}` (browser default white leaks through)")
        elif not _is_dark(bg, vars):
            v.append(f"BLACK ROOT: `{sel}` background is not deep black: {bg}")
    return v


def check_no_light_surfaces(css: str) -> list[str]:
    v = []
    for m in re.finditer(r"([^{}]+)\{([^{}]*)\}", css):
        selector, body = m.group(1).strip(), m.group(2)
        if selector.startswith("@") or ":before" in selector or ":after" in selector:
            continue
        for bm in re.finditer(r"background(?:-color)?\s*:\s*([^;}]+);?", body, re.I):
            val = bm.group(1).strip()
            if re.match(r"^(white|#fff|#ffffff|#fafafa|#f5f5f5|#eee|#eeeeee)$", val.lower()):
                v.append(f"NO LIGHT SURFACES: `{selector}` has white background: {val}")
    return v


def check_dark_scheme(html: str, css: str) -> list[str]:
    if re.search(r'<meta[^>]+name=["\']color-scheme["\'][^>]*content=["\']dark["\']', html, re.I):
        return []
    if re.search(r"color-scheme\s*:\s*dark", css, re.I):
        return []
    return ["DARK COLOR-SCHEME: no dark color-scheme declared (native controls/chrome render light)"]


def _manifest_classes(manifest_path: Path) -> set[str]:
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    known: set[str] = set()
    manifest_dir = manifest_path.parent
    css_files = list(manifest_dir.glob("*.css")) + list(manifest_dir.glob("*/*.css"))
    for cssf in css_files:
        css = cssf.read_text(encoding="utf-8", errors="replace")
        for m in re.finditer(r"\.([a-zA-Z0-9_-]+)", css):
            if m.group(1).startswith(_NAYA_PREFIXES):
                known.add(m.group(1))
    for b in data.get("blocks", []):
        for c in b.get("css_classes", []):
            for part in re.split(r"[/,]", c):
                known.update(re.findall(r"\.([a-zA-Z0-9_-]+)", part))
    known.add("naya-page")
    return known


def check_no_freestyle(html: str, known: set[str]) -> list[str]:
    v = []
    used: set[str] = set()
    for m in re.finditer(r'class=["\']([^"\']+)["\']', html):
        used.update(m.group(1).split())
    for cls in sorted(used):
        if cls.startswith(_NAYA_PREFIXES) and cls not in known:
            base_name = cls.split("--")[0].split("__")[0]
            if base_name not in known:
                v.append(f"NO FREESTYLE: class `.{cls}` is not in the manifest — use a canonical block or file the gap")
    return v


def check_light_text(css: str) -> list[str]:
    bodies = re.findall(r"body(?:\.[a-zA-Z0-9_-]+)?\s*\{([^}]*)\}", css, re.I)
    if not bodies:
        return ["LIGHT TEXT: no body rule found"]
    col = None
    for b in bodies:
        m = re.search(r"(?<![a-z-])color\s*:\s*([^;}]+);?", b, re.I)
        if m:
            col = m.group(1).strip()
            break
    if not col:
        return ["LIGHT TEXT: body has no text color declared"]
    if _is_dark(col, _root_vars(css)):
        v = [f"LIGHT TEXT: body text color is dark: {col}"]
        return v
    return []


def check_viewport(html: str) -> list[str]:
    m = re.search(r'<meta[^>]+name=["\']viewport["\'][^>]*>', html, re.I)
    if not m:
        return ["MOBILE VIEWPORT: no viewport meta tag (mobile is the primary canvas)"]
    if "width=device-width" not in m.group(0).replace(" ", ""):
        return ["MOBILE VIEWPORT: viewport meta does not declare width=device-width"]
    return []


def run_design_stage(page: Path, manifest: Path) -> list[str]:
    html = read_page(page)
    css = inline_css(html)
    violations: list[str] = []
    violations += check_self_contained(html)
    violations += check_black_root(html, css)
    violations += check_no_light_surfaces(css)
    violations += check_dark_scheme(html, css)
    violations += check_viewport(html)
    if manifest.exists():
        violations += check_no_freestyle(html, _manifest_classes(manifest))
    else:
        violations.append(f"NO FREESTYLE: manifest not found at {manifest} — cannot verify components")
    violations += check_light_text(css)
    return violations


# =====================================================================
# STAGE 2 — ACTIVATION (fused: drink-first PR #1979 + Naya 3 PR #1974
#                       + Naya 5 citation binding @ 728cab40)
# =====================================================================

def resolve_live_tip_trusted() -> tuple[str | None, str | None]:
    """Resolve the live main tip from the canonical repo — the gate fetches
    it itself (SN-0787 trusted runner). Returns (tip, error)."""
    try:
        r = subprocess.run(
            ["git", "ls-remote", CANONICAL_GIT_URL, "HEAD"],
            capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.TimeoutExpired) as e:
        return None, f"trusted fetch failed: {e}"
    if r.returncode != 0:
        return None, f"trusted fetch failed: git ls-remote exit {r.returncode}"
    m = re.match(r"^([a-f0-9]{40})\s", r.stdout.strip())
    if not m:
        return None, f"trusted fetch returned unparseable output: {r.stdout[:80]!r}"
    return m.group(1), None


def _receipt_timestamp(receipt: dict):
    raw = receipt.get("activated_at") or receipt.get("timestamp")
    if not isinstance(raw, str) or not raw:
        return None
    try:
        dt = datetime.fromisoformat(raw.strip().replace("Z", "+00:00"))
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def run_activation_stage(html: str, receipt_path: Path | None,
                         enforce: bool, caller_tip: str | None,
                         trust_caller: bool) -> tuple[list[str], bool]:
    """Returns (violations, advisory). advisory=True means the verdict is
    NOT enforcement-grade (caller-supplied tip)."""
    v: list[str] = []
    advisory = False

    # 2.0 citation marker must exist in the deliverable
    m = RECEIPT_MARKER_RE.search(html)
    if not m:
        return (["ACTIVATION: no activation citation marker in deliverable "
                 "(<!-- NAYA-ACTIVATION-RECEIPT-SHA256:<64hex> -->). "
                 "Unactivated work doesn't ship."], advisory)
    marker_sha = m.group(1).lower()
    if receipt_path is None:
        return (["ACTIVATION: citation marker present but no --receipt given; "
                 "cannot verify freshness or integrity."], advisory)
    try:
        raw = receipt_path.read_bytes()
        receipt = json.loads(raw)
    except (OSError, ValueError) as e:
        return ([f"ACTIVATION: cannot read receipt {receipt_path}: {e}"], advisory)

    # 2.1 schema + status (drink-first FAIL-SCHEMA / FAIL-UNACTIVATED)
    if receipt.get("schema") not in RECEIPT_SCHEMAS:
        v.append(f"ACTIVATION: receipt schema {receipt.get('schema')!r} not in {RECEIPT_SCHEMAS}")
    if receipt.get("status") != "ACTIVATED":
        v.append("ACTIVATION: receipt status is not ACTIVATED (FAIL-UNACTIVATED)")

    # 2.2 repository binding (Naya 3: wrong-repo reject)
    repo = receipt.get("repository", "")
    if repo != CANONICAL_REPO:
        v.append(f"ACTIVATION: receipt repository {repo!r} != {CANONICAL_REPO} "
                 "(FAIL-WRONG-REPO — receipt is for another repository)")

    # 2.3 required fields (union of v1/v2 critical fields)
    for field in ("session_id", "main_sha"):
        if not receipt.get(field):
            v.append(f"ACTIVATION: receipt missing {field} (FAIL-SCHEMA)")
    # v2 identity fields when v2 schema claimed
    if receipt.get("schema") == "naya.activation.receipt.v2":
        for field in ("naya_identity", "human_authority", "job", "proof_plan"):
            if not receipt.get(field):
                v.append(f"ACTIVATION: v2 receipt missing {field}")
        if not receipt.get("gates"):
            v.append("ACTIVATION: v2 receipt names no governing gates")
    # v1 loaded set when v1 schema claimed
    if receipt.get("schema") == "naya.activation.receipt.v1":
        if not receipt.get("loaded"):
            v.append("ACTIVATION: v1 receipt names nothing loaded (what was drunk?)")
        if not receipt.get("activation_protocol"):
            v.append("ACTIVATION: v1 receipt missing activation_protocol")

    main_sha = str(receipt.get("main_sha", ""))
    if not re.fullmatch(r"[a-fA-F0-9]{40}", main_sha):
        v.append("ACTIVATION: receipt main_sha is not a 40-hex SHA")

    # 2.4 citation integrity: marker == sha256(exact receipt bytes) (Naya 5)
    digest = hashlib.sha256(raw).hexdigest()
    if digest != marker_sha:
        v.append("ACTIVATION: citation marker does not match receipt bytes "
                 "(FAIL-CITATION — stale or forged citation)")

    # 2.5 freshness: <4h, not future (drink-first FAIL-STALE)
    ts = _receipt_timestamp(receipt)
    now = datetime.now(timezone.utc)
    if ts is None:
        v.append("ACTIVATION: receipt has no parseable activation timestamp")
    else:
        if ts > now + timedelta(minutes=2):
            v.append("ACTIVATION: receipt timestamp is in the future")
        elif now - ts > RECEIPT_TTL:
            v.append("ACTIVATION: receipt expired (>4h old) — re-activate (FAIL-STALE)")

    # 2.6 tip match — TRUSTED RUNNER (SN-0787)
    if enforce:
        live_tip, err = resolve_live_tip_trusted()
        if err:
            v.append(f"ACTIVATION: {err} (FAIL-TRUSTED-FETCH — unverifiable is not shippable)")
        elif main_sha.lower() != live_tip.lower():
            v.append(f"ACTIVATION: receipt main_sha {main_sha[:8]} != live tip {live_tip[:8]} "
                     "(FAIL-TIP-MOVED — a decision expires when the tip moves; re-activate)")
    elif caller_tip and trust_caller:
        advisory = True
        if main_sha.lower() != caller_tip.lower():
            v.append("ACTIVATION: receipt main_sha != caller-supplied tip (advisory check)")
    elif caller_tip and not trust_caller:
        v.append("ACTIVATION: --live-tip without --trust-caller is rejected — "
                 "the gate will not compare against builder-supplied state as live (SN-0787). "
                 "Use --enforce (default) or pass --trust-caller for an advisory check.")
    # enforce=True and no caller tip: trusted fetch already handled above.
    return v, advisory


# =====================================================================
# main
# =====================================================================

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Naya unified delivery gate (design + activation).")
    ap.add_argument("product", nargs="?", help="deliverable HTML file")
    ap.add_argument("--manifest", default=None, help="smart-blocks manifest.json")
    ap.add_argument("--require-activation", action="store_true")
    ap.add_argument("--receipt", default=None)
    ap.add_argument("--enforce", action="store_true", default=True,
                    help="resolve the live tip via trusted fetch (default on with --require-activation)")
    ap.add_argument("--no-enforce", dest="enforce", action="store_false")
    ap.add_argument("--live-tip", default=None)
    ap.add_argument("--trust-caller", action="store_true",
                    help="accept caller-supplied --live-tip as ADVISORY only (never enforcement)")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv)

    if args.self_test:
        return self_test()

    if not args.product:
        ap.print_help()
        return 2
    page = Path(args.product)
    if not page.exists():
        print(f"naya_gate: no such file: {page}")
        return 2
    manifest = Path(args.manifest) if args.manifest else (REPO_ROOT / "smart-blocks" / "manifest.json")

    violations: list[str] = []
    advisory = False

    # STAGE 1 — DESIGN (always)
    violations += run_design_stage(page, manifest)

    # STAGE 2 — ACTIVATION (on --require-activation)
    if args.require_activation:
        html = read_page(page)
        receipt_path = Path(args.receipt) if args.receipt else None
        act_v, advisory = run_activation_stage(
            html, receipt_path,
            enforce=args.enforce, caller_tip=args.live_tip,
            trust_caller=args.trust_caller)
        violations += act_v

    if violations:
        print(f"NAYA GATE: FAIL — {len(violations)} violation(s) in {page}:")
        for viol in violations:
            print(f"  x {viol}")
        if advisory:
            print("  (advisory verdict — caller-supplied tip, NOT enforcement-grade)")
        return 1
    print(f"NAYA GATE: PASS — {page}" + (" (ADVISORY — not enforcement-grade)" if advisory else ""))
    return 0


def _good_html(marker: str = "") -> str:
    return f"""<!DOCTYPE html><html><head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="dark">
<style>html{{background:#050507}}body{{background:#050507;color:#f8f7fb}}
.naya-btn{{color:#fff}}</style></head>
<body class="naya-page"><button class="naya-btn">Go</button>{marker}</body></html>"""


def self_test() -> int:
    """Red-green adversarial controls. Exit 0 = gate behaves, 1 = broken."""
    import tempfile
    ok = True

    def check(name: str, violations: list[str], want_fail: bool):
        nonlocal ok
        failed = bool(violations)
        good = (failed == want_fail)
        print(f"  [{'OK' if good else 'BROKEN'}] {name}: "
              f"{'failed' if failed else 'passed'}"
              f"{' (' + str(len(violations)) + ' violations)' if failed else ''}")
        if not good:
            ok = False
            for viol in violations:
                print(f"       - {viol}")

    with tempfile.TemporaryDirectory() as d:
        td = Path(d)
        mf = td / "manifest.json"
        mf.write_text(json.dumps({"blocks": [{"css_classes": [".naya-btn"]}]}))

        # DESIGN adversarials (Naya 5's red-green, fused)
        bad = td / "bad.html"
        bad.write_text("""<!DOCTYPE html><html><head><link rel="stylesheet" href="x.css">
<style>body{background:#fff;color:#111}</style></head>
<body><div class="naya-frobnicate">hi</div></body></html>""")
        check("forbidden HTML (white root, external css, freestyle class)",
              run_design_stage(bad, mf), True)
        good = td / "good.html"
        good.write_text(_good_html())
        check("valid canonical component", run_design_stage(good, mf), False)

        # ACTIVATION adversarials — advisory mode (no network in unit test)
        now = datetime.now(timezone.utc)
        def receipt(**kw):
            r = {"schema": "naya.activation.receipt.v2", "status": "ACTIVATED",
                 "session_id": "t1", "naya_identity": "Naya QA",
                 "human_authority": "Shawn", "repository": CANONICAL_REPO,
                 "job": "test", "gates": ["law"], "proof_plan": "test",
                 "main_sha": "a" * 40, "activated_at": now.isoformat()}
            r.update(kw)
            return r

        # missing marker
        rp = td / "r.json"
        rp.write_bytes(json.dumps(receipt()).encode())
        vv, _ = run_activation_stage(_good_html(), rp, enforce=False,
                                     caller_tip="a" * 40, trust_caller=True)
        check("missing citation marker", vv, True)

        # valid (advisory)
        digest = hashlib.sha256(rp.read_bytes()).hexdigest()
        marked = _good_html(f"<!-- NAYA-ACTIVATION-RECEIPT-SHA256:{digest} -->")
        vv, adv = run_activation_stage(marked, rp, enforce=False,
                                        caller_tip="a" * 40, trust_caller=True)
        check("valid receipt+marker (advisory)", vv, False)
        if not adv:
            print("  [BROKEN] advisory flag not set on caller-supplied tip"); ok = False
        else:
            print("  [OK] advisory flag set on caller-supplied tip")

        # forged marker
        forged = _good_html("<!-- NAYA-ACTIVATION-RECEIPT-SHA256:" + "0" * 64 + " -->")
        vv, _ = run_activation_stage(forged, rp, enforce=False,
                                      caller_tip="a" * 40, trust_caller=True)
        check("forged citation marker", vv, True)

        # stale receipt
        old = receipt(activated_at=(now - timedelta(hours=5)).isoformat())
        rp_old = td / "ro.json"
        rp_old.write_bytes(json.dumps(old).encode())
        d_old = hashlib.sha256(rp_old.read_bytes()).hexdigest()
        marked_old = _good_html(f"<!-- NAYA-ACTIVATION-RECEIPT-SHA256:{d_old} -->")
        vv, _ = run_activation_stage(marked_old, rp_old, enforce=False,
                                      caller_tip="a" * 40, trust_caller=True)
        check("stale receipt (>4h)", vv, True)

        # wrong repository
        wr = receipt(repository="EvilCorp/OtherRepo")
        rp_wr = td / "rw.json"
        rp_wr.write_bytes(json.dumps(wr).encode())
        d_wr = hashlib.sha256(rp_wr.read_bytes()).hexdigest()
        marked_wr = _good_html(f"<!-- NAYA-ACTIVATION-RECEIPT-SHA256:{d_wr} -->")
        vv, _ = run_activation_stage(marked_wr, rp_wr, enforce=False,
                                      caller_tip="a" * 40, trust_caller=True)
        check("wrong-repository receipt", vv, True)

        # tip mismatch (advisory caller tip)
        vv, _ = run_activation_stage(marked, rp, enforce=False,
                                      caller_tip="b" * 40, trust_caller=True)
        check("tip mismatch (advisory)", vv, True)

        # untrusted caller tip rejected
        vv, _ = run_activation_stage(marked, rp, enforce=False,
                                      caller_tip="a" * 40, trust_caller=False)
        check("caller tip without --trust-caller rejected", vv, True)

        # unactivated status
        un = receipt(status="DRAFT")
        rp_un = td / "ru.json"
        rp_un.write_bytes(json.dumps(un).encode())
        d_un = hashlib.sha256(rp_un.read_bytes()).hexdigest()
        marked_un = _good_html(f"<!-- NAYA-ACTIVATION-RECEIPT-SHA256:{d_un} -->")
        vv, _ = run_activation_stage(marked_un, rp_un, enforce=False,
                                      caller_tip="a" * 40, trust_caller=True)
        check("unactivated status", vv, True)

        # v1 schema accepted
        r1 = {"schema": "naya.activation.receipt.v1", "status": "ACTIVATED",
              "session_id": "t1", "repository": CANONICAL_REPO,
              "main_sha": "a" * 40, "timestamp": now.isoformat(),
              "activation_protocol": "v2", "loaded": ["design-doctrine", "smart-blocks"]}
        rp1 = td / "r1.json"
        rp1.write_bytes(json.dumps(r1).encode())
        d1 = hashlib.sha256(rp1.read_bytes()).hexdigest()
        marked1 = _good_html(f"<!-- NAYA-ACTIVATION-RECEIPT-SHA256:{d1} -->")
        vv, _ = run_activation_stage(marked1, rp1, enforce=False,
                                      caller_tip="a" * 40, trust_caller=True)
        check("v1 receipt schema accepted", vv, False)

    print("SELF-TEST:", "ALL GREEN" if ok else "BROKEN")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
