#!/usr/bin/env python3
"""NayaNET design gate — code is law, machine-forced.

Usage:
    python3 tools/design_gate.py <page.html> [--manifest smart-blocks/manifest.json]
    python3 tools/design_gate.py <page.html> --require-activation --receipt=<receipt.json>

Enforces the STRUCTURAL design laws from DESIGN-LAWS.md as a hard gate.
Exit 0 = pass. Exit 1 = fail, with each violation named specifically.
Eye-enforced laws (craft, copy, motion meaning) remain Shawn's verdict —
this gate catches what a machine can prove.

With --require-activation, the gate also rejects deliverables with no, stale,
or mismatched activation citation (Naya 3's Gap 2, PR #1974). The citation
marker <!-- NAYA-ACTIVATION-RECEIPT-SHA256:<64hex> --> must match the sha256
of the exact receipt bytes, and the receipt must be fresh (<4h). Deep
verification against live GitHub state is Naya 3's checker in CI.

Structural checks:
  1. SELF-CONTAINED — no external stylesheet/script references (all inlined).
  2. BLACK ROOT — html/body background is deep black.
  3. NO LIGHT SURFACES — no white/light background declarations.
  4. DARK COLOR-SCHEME — meta or CSS declares dark.
  5. NO FREESTYLE COMPONENTS — every Naya-prefixed class exists in the manifest.
  6. LIGHT TEXT — body text color is light.
  7. MOBILE VIEWPORT — the viewport meta declares width=device-width
     (mobile is the primary canvas).
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def read_page(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def inline_css(html: str) -> str:
    """All <style> block contents concatenated."""
    return "\n".join(re.findall(r"<style[^>]*>(.*?)</style>", html, re.S | re.I))


def check_self_contained(html: str) -> list[str]:
    v = []
    for m in re.finditer(
        r'<link[^>]+rel=["\']stylesheet["\'][^>]*>', html, re.I
    ):
        tag = m.group(0)
        href = re.search(r'href=["\']([^"\']+)', tag, re.I)
        ref = href.group(1) if href else tag
        if not ref.startswith("data:"):
            v.append(f"SELF-CONTAINED: external stylesheet reference: {ref}")
    for m in re.finditer(r'<script[^>]+src=["\']([^"\']+)["\']', html, re.I):
        src = m.group(1)
        if not src.startswith("data:"):
            v.append(f"SELF-CONTAINED: external script reference: {src}")
    return v


def _bg_of_rule(css: str, selector: str) -> str | None:
    for m in re.finditer(
        re.escape(selector) + r"\s*\{([^}]*)\}", css, re.I
    ):
        body = m.group(1)
        bg = re.search(r"background(?:-color)?\s*:\s*([^;}]+);?", body, re.I)
        if bg:
            return bg.group(1).strip()
    return None


def _root_vars(css: str) -> dict[str, str]:
    """Parse :root { --name: value } custom properties."""
    vars: dict[str, str] = {}
    for m in re.finditer(r":root\s*\{([^}]*)\}", css, re.I):
        for vm in re.finditer(r"--([a-zA-Z0-9_-]+)\s*:\s*([^;}]+);?", m.group(1)):
            vars[vm.group(1)] = vm.group(2).strip()
    return vars


def _resolve_vars(color: str, vars: dict[str, str], depth: int = 0) -> str:
    if depth > 5:
        return color
    m = re.search(r"var\(\s*--([a-zA-Z0-9_-]+)", color)
    if m and m.group(1) in vars:
        return _resolve_vars(vars[m.group(1)], vars, depth + 1)
    return color


def _is_dark(color: str, vars: dict[str, str] | None = None) -> bool:
    color = _resolve_vars(color, vars or {})
    c = color.strip().lower()
    if c in ("transparent", "none", "initial", "inherit"):
        return True  # not a light surface
    # hex
    m = re.match(r"#([0-9a-f]{3,8})", c)
    if m:
        h = m.group(1)
        if len(h) == 3:
            h = "".join(ch * 2 for ch in h)
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        lum = (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255
        return lum < 0.35
    if "gradient" in c:
        # gradients: fail only if they START with a light stop
        first = c.split(",", 1)[1] if "," in c else c
        mm = re.search(r"#([0-9a-f]{3,8})", first)
        if mm:
            return _is_dark("#" + mm.group(1))
        if re.search(r"\bwhite\b", first):
            return False
        return True
    if re.search(r"\bwhite\b", c):
        return False
    rgba = re.match(
        r"rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)", c
    )
    if rgba:
        r, g, b = map(int, rgba.groups())
        lum = (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255
        return lum < 0.35
    return True


def check_black_root(html: str, css: str) -> list[str]:
    v = []
    vars = _root_vars(css)
    for sel in ("html", "body"):
        bg = _bg_of_rule(css, sel)
        # also accept body class selectors like body.naya-page
        if bg is None and sel == "body":
            m = re.search(
                r"body\.[a-zA-Z0-9_-]+\s*\{([^}]*)\}", css, re.I
            )
            if m:
                b2 = re.search(
                    r"background(?:-color)?\s*:\s*([^;}]+);?", m.group(1), re.I
                )
                bg = b2.group(1).strip() if b2 else None
        if bg is None:
            v.append(f"BLACK ROOT: no background declared for `{sel}` "
                     f"(browser default white leaks through)")
        elif not _is_dark(bg, vars):
            v.append(f"BLACK ROOT: `{sel}` background is not deep black: {bg}")
    return v


def check_no_light_surfaces(css: str) -> list[str]:
    v = []
    for m in re.finditer(
        r"([^{}]+)\{([^{}]*)\}", css
    ):
        selector, body = m.group(1).strip(), m.group(2)
        if selector.startswith("@"):
            continue
        # pseudo-element detail craft (specular dots, facet highlights)
        # are not surfaces — skip them
        if ":before" in selector or ":after" in selector:
            continue
        for bm in re.finditer(
            r"background(?:-color)?\s*:\s*([^;}]+);?", body, re.I
        ):
            val = bm.group(1).strip()
            # exact white / light page surfaces only — gradient highlights
            # and tiny jewel facets are craft, not surfaces
            if re.match(
                r"^(white|#fff|#ffffff|#fafafa|#f5f5f5|#eee|#eeeeee)$",
                val.lower(),
            ):
                v.append(f"NO LIGHT SURFACES: `{selector}` has white "
                         f"background: {val}")
    return v


def check_dark_scheme(html: str, css: str) -> list[str]:
    if re.search(
        r'<meta[^>]+name=["\']color-scheme["\'][^>]*content=["\']dark["\']',
        html, re.I,
    ):
        return []
    if re.search(r"color-scheme\s*:\s*dark", css, re.I):
        return []
    return ["DARK COLOR-SCHEME: no dark color-scheme declared "
            "(native controls/chrome render light)"]


def _manifest_classes(manifest_path: Path) -> set[str]:
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    known: set[str] = set()
    manifest_dir = manifest_path.parent
    # Closed-world law: every class selector in canonical CSS is documented.
    css_files = list(manifest_dir.glob("*.css"))
    css_files += list(manifest_dir.glob("*/*.css"))
    for cssf in css_files:
        css = cssf.read_text(encoding="utf-8", errors="replace")
        for m in re.finditer(r"\.([a-zA-Z0-9_-]+)", css):
            known.add(m.group(1))
    for b in data.get("blocks", []):
        for c in b.get("css_classes", []):
            for part in re.split(r"[/,]", c):
                # all class names in the selector, not just the first
                # (handles `table.naya-table[x]` -> naya-table)
                known.update(re.findall(r"\.([a-zA-Z0-9_-]+)", part))
        # every class used inside the block's own snippet is canonical too
        html_file = b.get("html_file", "")
        if html_file:
            cat = b.get("category_id", "")
            snippet = manifest_dir / cat / Path(html_file).name
            if snippet.exists():
                shtml = snippet.read_text(encoding="utf-8", errors="replace")
                for m in re.finditer(r'class=["\']([^"\']+)["\']', shtml):
                    known.update(m.group(1).split())
    # structural page root — not a component
    known.add("naya-page")
    return known


_NAYA_PREFIXES = ("naya-", "board", "orb-", "lv-", "torb", "gem-")


def check_no_freestyle(html: str, known: set[str]) -> list[str]:
    """Reject every undocumented class, regardless of its spelling/prefix."""
    used: set[str] = set()
    for m in re.finditer(r'class=["\']([^"\']+)["\']', html):
        used.update(m.group(1).split())
    return [
        f"NO FREESTYLE: class .{cls} is not in canonical CSS, manifest, or snippets"
        for cls in sorted(used - known)
    ]


def check_light_text(css: str) -> list[str]:
    v = []
    # body rule or body.<class> rules (page root carries the text color)
    bodies = re.findall(
        r"body(?:\.[a-zA-Z0-9_-]+)?\s*\{([^}]*)\}", css, re.I
    )
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
    # light text = NOT dark
    if _is_dark(col, _root_vars(css)):
        v.append(f"LIGHT TEXT: body text color is dark: {col}")
    return v


def check_viewport(html: str) -> list[str]:
    m = re.search(
        r'<meta[^>]+name=["\']viewport["\'][^>]*>', html, re.I
    )
    if not m:
        return ["MOBILE VIEWPORT: no viewport meta tag "
                "(mobile is the primary canvas)"]
    if "width=device-width" not in m.group(0).replace(" ", ""):
        return ["MOBILE VIEWPORT: viewport meta does not declare "
                "width=device-width"]
    return []


RECEIPT_MARKER_RE = re.compile(
    r"<!--\s*NAYA-ACTIVATION-RECEIPT-SHA256:([a-fA-F0-9]{64})\s*-->")
RECEIPT_TTL = timedelta(hours=4)


def _normalize_repo(ref: str) -> str:
    """Normalize a repository reference to owner/repo for comparison."""
    s = str(ref or "").strip().lower()
    s = re.sub(r"^(https?://github\.com/|git@github\.com:)", "", s)
    s = re.sub(r"\.git$", "", s).rstrip("/")
    return s


def _detect_repo() -> str:
    """Best-effort expected repository from git remote.origin.url."""
    try:
        out = subprocess.run(
            ["git", "config", "--get", "remote.origin.url"],
            capture_output=True, text=True, timeout=10,
            cwd=REPO_ROOT).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        out = ""
    return _normalize_repo(out)


def check_activation(html: str, receipt_path: Path | None,
                     expected_repo: str | None = None,
                     expected_repo_id: str | None = None,
                     expected_main_sha: str | None = None) -> list[str]:
    """Activation citation check (Naya 3's Gap 2 — PR #1974 integration).

    With --require-activation, a deliverable FAILS unless it carries a
    current activation citation. This is the gate layer: structural
    presence/format/freshness. Deep verification of the receipt against
    live GitHub state is Naya 3's checker (tools/qa/) running in CI —
    the gate cannot fetch live state, and must not trust builder-supplied
    state as live.
    """
    v = []
    m = RECEIPT_MARKER_RE.search(html)
    if not m:
        return ["ACTIVATION: no activation citation marker in deliverable "
                "(<!-- NAYA-ACTIVATION-RECEIPT-SHA256:<64hex> -->). "
                "Unactivated work doesn't ship."]
    marker_sha = m.group(1).lower()
    if receipt_path is None:
        return ["ACTIVATION: citation marker present but no --receipt given; "
                "cannot verify freshness or integrity."]
    try:
        raw = receipt_path.read_bytes()
        receipt = json.loads(raw)
    except (OSError, ValueError) as e:
        return [f"ACTIVATION: cannot read receipt {receipt_path}: {e}"]
    if receipt.get("schema") != "naya.activation.receipt.v2":
        v.append("ACTIVATION: receipt schema is not naya.activation.receipt.v2")
    if receipt.get("status") != "ACTIVATED":
        v.append("ACTIVATION: receipt status is not ACTIVATED")
    for field in ("session_id", "naya_identity", "human_authority",
                  "repository", "job", "proof_plan", "repository_id",
                  "activation_run_id", "activation_run_attempt",
                  "activation_workflow"):
        if not receipt.get(field):
            v.append(f"ACTIVATION: receipt missing {field}")
    if not receipt.get("gates"):
        v.append("ACTIVATION: receipt names no governing gates")
    main_sha = receipt.get("main_sha", "")
    if not re.fullmatch(r"[a-fA-F0-9]{40}", str(main_sha)):
        v.append("ACTIVATION: receipt main_sha is not a 40-hex SHA")
    # Trusted CI identity is mandatory. Never fall back to a mutable git remote.
    # Bind both canonical repository name and immutable numeric ID.
    want = _normalize_repo(expected_repo) if expected_repo else ""
    got = _normalize_repo(receipt.get("repository", ""))
    if not want:
        v.append("ACTIVATION: cannot determine the gated repository "
                 "(no --expected-repo and no git remote) - refusing to bind")
    elif got != want:
        v.append(f"ACTIVATION: receipt is for repository '{got}', not the "
                 f"gated repository '{want}' (wrong-repository activation)")
    if not expected_repo_id or not str(expected_repo_id).isdigit():
        v.append("ACTIVATION: trusted --expected-repo-id is required; refusing repository identity fallback")
    elif str(receipt.get("repository_id", "")) != str(expected_repo_id):
        v.append("ACTIVATION: receipt repository_id does not match trusted GitHub repository ID")
    if not expected_main_sha or not re.fullmatch(r"[a-fA-F0-9]{40}", expected_main_sha):
        v.append("ACTIVATION: trusted --expected-main-sha (full 40-hex) is required")
    elif str(main_sha).lower() != expected_main_sha.lower():
        v.append("ACTIVATION: receipt main_sha does not equal trusted live main tip")
    # Integrity: the marker must be the sha256 of the exact receipt bytes.
    digest = hashlib.sha256(raw).hexdigest()
    if digest != marker_sha:
        v.append("ACTIVATION: citation marker does not match receipt bytes "
                 "(stale or forged citation)")
    # Freshness: 4h TTL, no future activations.
    try:
        activated = datetime.fromisoformat(
            str(receipt.get("activated_at", "")).replace("Z", "+00:00"))
        now = datetime.now(timezone.utc)
        if activated > now + timedelta(minutes=2):
            v.append("ACTIVATION: receipt activated_at is in the future")
        elif now - activated > RECEIPT_TTL:
            v.append("ACTIVATION: receipt expired (>4h old) — re-activate")
    except ValueError:
        v.append("ACTIVATION: receipt activated_at is not a valid timestamp")
    return v


def run_gate(page: Path, manifest: Path,
             require_activation: bool = False,
             receipt_path: Path | None = None,
             expected_repo: str | None = None,
             expected_repo_id: str | None = None,
             expected_main_sha: str | None = None) -> list[str]:
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
        violations.append(f"NO FREESTYLE: manifest not found at {manifest} "
                          f"— cannot verify components")
    violations += check_light_text(css)
    if require_activation:
        violations += check_activation(html, receipt_path, expected_repo,
                                       expected_repo_id, expected_main_sha)
    return violations


def self_test() -> int:
    """Red-green: a violating page must fail, a lawful page must pass."""
    bad = """<!DOCTYPE html><html><head><link rel="stylesheet" href="x.css">
<style>body{background:#fff;color:#111}</style></head>
<body><div class="naya-frobnicate">hi</div></body></html>"""
    good = """<!DOCTYPE html><html><head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="dark">
<style>html{background:#050507}body{background:#050507;color:#f8f7fb}
.naya-btn{color:#fff}</style></head>
<body><button class="naya-btn">Go</button></body></html>"""
    import tempfile
    mf = REPO_ROOT / "smart-blocks" / "manifest.json"
    with tempfile.TemporaryDirectory() as d:
        pb, pg = Path(d) / "bad.html", Path(d) / "good.html"
        pb.write_text(bad)
        pg.write_text(good)
        bad_v = run_gate(pb, mf)
        good_v = run_gate(pg, mf)
        # --- activation scenarios (Naya 3 Gap 2) ---
        now = datetime.now(timezone.utc)
        receipt = {
            "schema": "naya.activation.receipt.v2",
            "status": "ACTIVATED",
            "session_id": "selftest-1",
            "naya_identity": "Naya 5",
            "human_authority": "Shawn",
            "repository": "SoulSchoolAcademy/NayaPOWER",
            "repository_id": "1337349667",
            "activation_run_id": "1",
            "activation_run_attempt": "1",
            "activation_workflow": ".github/workflows/design-gate-activation.yml",
            "job": "self-test",
            "gates": ["Usefulness Gate"],
            "proof_plan": "self-test",
            "main_sha": "a" * 40,
            "activated_at": now.isoformat(),
        }
        rp = Path(d) / "receipt.json"
        rp.write_bytes(json.dumps(receipt).encode())
        digest = hashlib.sha256(rp.read_bytes()).hexdigest()
        marked = good.replace("</body>",
                              f"<!-- NAYA-ACTIVATION-RECEIPT-SHA256:{digest} --></body>")
        pm = Path(d) / "marked.html"
        pm.write_text(marked)
        noact_v = run_gate(pg, mf, require_activation=True,
                           receipt_path=rp, expected_repo="SoulSchoolAcademy/NayaPOWER",
                           expected_repo_id="1337349667", expected_main_sha="a" * 40)          # no marker -> fail
        okact_v = run_gate(pm, mf, require_activation=True,
                           receipt_path=rp, expected_repo="SoulSchoolAcademy/NayaPOWER",
                           expected_repo_id="1337349667", expected_main_sha="a" * 40)          # valid -> pass
        forged = marked.replace(digest, "0" * 64)
        pf = Path(d) / "forged.html"
        pf.write_text(forged)
        forged_v = run_gate(pf, mf, require_activation=True,
                            receipt_path=rp, expected_repo="SoulSchoolAcademy/NayaPOWER",
                           expected_repo_id="1337349667", expected_main_sha="a" * 40)         # mismatch -> fail
        old = dict(receipt,
                   activated_at=(now - timedelta(hours=5)).isoformat())
        rp_old = Path(d) / "receipt_old.json"
        rp_old.write_bytes(json.dumps(old).encode())
        d_old = hashlib.sha256(rp_old.read_bytes()).hexdigest()
        pm_old = Path(d) / "marked_old.html"
        pm_old.write_text(good.replace(
            "</body>",
            f"<!-- NAYA-ACTIVATION-RECEIPT-SHA256:{d_old} --></body>"))
        expired_v = run_gate(pm_old, mf, require_activation=True,
                             receipt_path=rp_old, expected_repo="SoulSchoolAcademy/NayaPOWER",
                             expected_repo_id="1337349667", expected_main_sha="a" * 40)    # expired -> fail
        # wrong-repository receipt -> fail (Naya 1's adversarial case)
        wrong = dict(receipt, repository="SomeoneElse/OtherRepo")
        rp_wrong = Path(d) / "receipt_wrong.json"
        rp_wrong.write_bytes(json.dumps(wrong).encode())
        d_wrong = hashlib.sha256(rp_wrong.read_bytes()).hexdigest()
        pm_wrong = Path(d) / "marked_wrong.html"
        pm_wrong.write_text(good.replace(
            "</body>",
            f"<!-- NAYA-ACTIVATION-RECEIPT-SHA256:{d_wrong} --></body>"))
        wrongrepo_v = run_gate(
            pm_wrong, mf, require_activation=True, receipt_path=rp_wrong,
            expected_repo="SoulSchoolAcademy/NayaPOWER", expected_repo_id="1337349667",
            expected_main_sha="a" * 40)  # wrong repo -> fail
        wrongid = dict(receipt, repository_id="999999")
        rp_wrongid = Path(d) / "receipt_wrongid.json"
        rp_wrongid.write_bytes(json.dumps(wrongid).encode())
        wrongid_digest = hashlib.sha256(rp_wrongid.read_bytes()).hexdigest()
        pm_wrongid = Path(d) / "marked_wrongid.html"
        pm_wrongid.write_text(good.replace(
            "</body>", f"<!-- NAYA-ACTIVATION-RECEIPT-SHA256:{wrongid_digest} --></body>"))
        wrongid_v = run_gate(
            pm_wrongid, mf, require_activation=True, receipt_path=rp_wrongid,
            expected_repo="SoulSchoolAcademy/NayaPOWER", expected_repo_id="1337349667",
            expected_main_sha="a" * 40)
        stale_v = run_gate(
            pm, mf, require_activation=True, receipt_path=rp,
            expected_repo="SoulSchoolAcademy/NayaPOWER", expected_repo_id="1337349667",
            expected_main_sha="b" * 40)
        undocumented = good.replace('class="naya-btn"', 'class="undocumented-widget"')
        pu = Path(d) / "undocumented.html"
        pu.write_text(undocumented)
        unknown_class_v = run_gate(pu, mf)
    ok = True
    if not bad_v:
        print("SELF-TEST FAIL: violating page passed the gate")
        ok = False
    else:
        print(f"SELF-TEST: violating page failed with {len(bad_v)} violations (good)")
        for viol in bad_v:
            print("   -", viol)
    if good_v:
        print("SELF-TEST FAIL: lawful page failed the gate:")
        for viol in good_v:
            print("   -", viol)
        ok = False
    else:
        print("SELF-TEST: lawful page passed (good)")
    for name, vv, want_fail in [
            ("no-marker+required", noact_v, True),
            ("valid receipt", okact_v, False),
            ("forged marker", forged_v, True),
            ("expired receipt", expired_v, True),
            ("wrong-repository receipt", wrongrepo_v, True),
            ("wrong repository ID", wrongid_v, True),
            ("stale main SHA", stale_v, True),
            ("undocumented unprefixed class", unknown_class_v, True)]:
        has_act = any(x.startswith("ACTIVATION") for x in vv)
        if want_fail and not has_act:
            print(f"SELF-TEST FAIL: activation case '{name}' did not fail")
            ok = False
        elif not want_fail and vv:
            print(f"SELF-TEST FAIL: activation case '{name}' failed: {vv}")
            ok = False
        else:
            print(f"SELF-TEST: activation case '{name}' "
                  f"{'failed as required' if want_fail else 'passed'} (good)")
    return 0 if ok else 1


def main(argv: list[str]) -> int:
    if "--self-test" in argv:
        return self_test()
    args = [a for a in argv if not a.startswith("--")]
    flags = {a for a in argv if a.startswith("--")}
    if not args:
        print(__doc__)
        return 2
    page = Path(args[0])
    manifest = Path(args[1]) if len(args) > 1 else (
        REPO_ROOT / "smart-blocks" / "manifest.json"
    )
    require_activation = "--require-activation" in flags
    receipt_path = None
    expected_repo = None
    expected_repo_id = None
    expected_main_sha = None
    for a in argv:
        if a.startswith("--receipt="):
            receipt_path = Path(a.split("=", 1)[1])
        elif a.startswith("--expected-repo="):
            expected_repo = a.split("=", 1)[1]
        elif a.startswith("--expected-repo-id="):
            expected_repo_id = a.split("=", 1)[1]
        elif a.startswith("--expected-main-sha="):
            expected_main_sha = a.split("=", 1)[1]
    if not page.exists():
        print(f"design_gate: no such file: {page}")
        return 2
    violations = run_gate(page, manifest,
                          require_activation=require_activation,
                          receipt_path=receipt_path,
                          expected_repo=expected_repo,
                          expected_repo_id=expected_repo_id,
                          expected_main_sha=expected_main_sha)
    if violations:
        print(f"DESIGN GATE: FAIL — {len(violations)} violation(s) in {page}:")
        for viol in violations:
            print(f"  ✕ {viol}")
        return 1
    print(f"DESIGN GATE: PASS — {page}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
