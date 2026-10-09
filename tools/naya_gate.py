#!/usr/bin/env python3
"""Naya unified delivery gate — code is law, machine-forced.

ONE gate at the delivery boundary, fusing existing efforts
(no competing gates, no duplication):

  STAGE 1 — DESIGN (structural)
      7 machine-provable structural laws, implemented in this file, plus the
      CLOSED-WORLD component rule (Naya 1, 2026-10-09): every class used in a
      deliverable must be registered in the manifest (or be a BEM
      modifier/element of a registered block) — undocumented classes fail
      whether or not they carry a naya- prefix.
      ATTRIBUTION (corrected 2026-10-09): previously cited as "Naya 5's
      tools/design_gate.py @ 728cab40" — that citation is WITHDRAWN.
      Commit 728cab40 changed only AGENTS.md (+20/-0), and no
      tools/design_gate.py exists on main or any indexed branch (verified
      2026-10-09 via contents API + code search). The 7 checks below are
      the gate-fusion doer's implementation of the reported 7-law
      specification from the design-gate lane. If the source file
      surfaces, Stage 1 converges to it.

  STAGE 2 — ACTIVATION (drink-first, trusted runner)
      Fused from:
      - Naya 4's NAYA-ACTIVATION/tools/drink_first_gate.py (PR #1979, open draft)
        — fail-closed verdicts: unactivated / tip-moved / stale / citation / schema.
      - Naya 3's tools/qa/activation_receipt_consistency.mjs (PR #1974, open)
        — receipt consistency falsifier: schema, identity, repository binding,
          main_sha match, freshness, citation binding.

      TRUSTED RUNNER (SN-0787): a builder can forge both the receipt and the
      expected hashes, so expected values must come from a source the builder
      cannot write. In --enforce mode (default with --require-activation) the
      gate resolves the live tip ITSELF via `git ls-remote` on the canonical
      repo and compares the receipt against THAT. A caller-supplied --live-tip
      is honored ONLY with --trust-caller, and the verdict is then labeled
      ADVISORY — never enforcement. If the trusted fetch fails, the gate fails
      closed (FAIL-TRUSTED-FETCH): unverifiable is not shippable.

      COMPONENTS_LIVE (TRUSTED-RUNNER-DESIGN.md check 6): receipts that record
      component SHAs (doctrine file / manifest blob SHAs) have them verified
      against the live tree — the gate fetches the tip's tree objects itself
      (partial clone, blob:none) and reads blob SHAs from the tree, bound to
      the exact trusted tip. Forged or stale component SHAs fail
      (FAIL-COMPONENT-MISMATCH). Receipts recording no components emit an
      explicit COMPONENTS_LIVE NOT_BOUND note (documented limit, not a fail).

      HONEST LIMITS (full text in tools/NAYA-GATE-FUSION-README.md):
      the gate proves a receipt is CURRENT and INTERNALLY CONSISTENT. A forger
      who copies ALL true current public values (live tip, current timestamp,
      live component blob SHAs — all publicly readable) and computes a valid
      citation produces a receipt this gate cannot distinguish from a genuine
      activation. COMPONENTS_LIVE raises forgery from "copy any plausible
      values" to "resolve all true current values" — the same work as genuine
      activation; the residual gap (did the builder actually read and follow
      the doctrine) is behavioral, closed by the cold-Naya proof, not by this
      gate. Naya 2's independent assessment (#1354 comment 6084472606):
      "Fix requires architectural change (signed receipts or
      challenge-response)" — recorded as the follow-up that would close the
      forgery hole fundamentally; explicitly out of scope for this PR.

  STAGE 3 — WORKFLOW PROOF
      tools/test_naya_gate.py proves the gate's own behavior: adversarial
      fixtures (valid component passes; forbidden HTML fails;
      missing/stale/wrong-repo/forged-tip receipts fail) plus end-to-end
      enforce-mode runs against the REAL live tip.
      .github/workflows/naya-gate-delivery.yml proves the gate guards a REAL
      deliverable: it builds a fresh receipt from live state at CI time,
      gates tools/naya-gate-sample/product.html in --enforce mode, and runs
      negative controls (tampered / stale / component-mismatched receipts
      must fail).

Receipt schemas accepted: naya.activation.receipt.v1 (drink-first) and
naya.activation.receipt.v2 (activation protocol). The gate requires the union
of critical fields: status ACTIVATED, repository bound to the canonical repo,
40-hex main_sha, fresh activation timestamp, non-empty loaded set (v1) or
identity+job+gates (v2).

Recorded deviations from NAYA-ACTIVATION/TRUSTED-RUNNER-DESIGN.md (CANDIDATE):
- Citation format: this gate uses <!-- NAYA-ACTIVATION-RECEIPT-SHA256:<64hex> -->
  (sha256 of the EXACT receipt bytes). The design specifies activation:<16-hex>
  (first 16 hex of sha256 over canonical JSON: keys sorted, separators
  (',', ':')). Rationale: 256-bit binding is strictly stronger than 64-bit;
  exact-bytes covers formatting tampering. Canonical-JSON normalization is
  deferred to a future alignment pass.
- Schema scope: the design specifies v2-only. This gate accepts v1+v2, to fuse
  the drink-first receipts already in flight (PR #1979). v1 gets the full
  battery except COMPONENTS_LIVE (v1 records no component SHAs — the NOT_BOUND
  note is emitted). v2-only enforcement is a one-line change when ratified.
- Check location: the design specifies a GitHub Actions workflow runner. The
  checks live in this tool (trusted fetch via git, same semantics); CI
  workflows invoke the tool. The trust property is identical — expected
  values come from the canonical repo, never the builder — and holds in any
  environment the builder does not control (CI). A builder running the gate
  on their own machine gets self-attestation, not enforcement.

Usage:
    python3 tools/naya_gate.py --product page.html [--manifest m.json]
    python3 tools/naya_gate.py --product page.html --require-activation --receipt r.json
    python3 tools/naya_gate.py --product page.html --require-activation --receipt r.json --trust-caller --live-tip <sha>

Exit 0 = PASS. Exit 1 = FAIL (violations named). Exit 2 = tool error.
Notes prefixed ACTIVATION-NOTE: are informational (documented limits);
they are printed but do not fail the gate.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
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
# STAGE 1 — DESIGN (Naya 5 7-law spec, implemented here; @728cab40 withdrawn, see ATTRIBUTION)
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
    """CLOSED-WORLD component rule (Naya 1, 2026-10-09): only explicitly
    documented and permitted classes are accepted. Every class used in the
    deliverable must be registered in the manifest (or be a BEM
    modifier/element of a registered block). An unregistered class fails —
    whether or not it carries a naya- prefix. A component being
    undocumented must not mean it escapes the rules."""
    v = []
    used: set[str] = set()
    for m in re.finditer(r'class=["\']([^"\']+)["\']', html):
        used.update(m.group(1).split())
    for cls in sorted(used):
        if cls in known:
            continue
        base_name = cls.split("--")[0].split("__")[0]
        if base_name in known:
            continue
        v.append(f"NO FREESTYLE: class `.{cls}` is not registered in the manifest — "
                 f"register it (and satisfy its contract) or remove it. "
                 f"Undocumented components do not escape the rules.")
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
#                       + Naya 5 citation binding (spec; @728cab40 withdrawn))
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


def validate_components_shape(components) -> list[str]:
    """Pure shape validation for receipt `components` (no network).
    Each component must be {"path": <repo-relative path>, "sha": <40-hex blob SHA>}."""
    if components is None:
        return []
    if not isinstance(components, list):
        return ["ACTIVATION: receipt components is not a list (FAIL-SCHEMA)"]
    v = []
    for i, c in enumerate(components):
        if not isinstance(c, dict):
            v.append(f"ACTIVATION: components[{i}] is not an object (FAIL-SCHEMA)")
            continue
        if not isinstance(c.get("path"), str) or not c["path"]:
            v.append(f"ACTIVATION: components[{i}] missing path (FAIL-SCHEMA)")
        if not re.fullmatch(r"[a-fA-F0-9]{40}", str(c.get("sha", ""))):
            v.append(f"ACTIVATION: components[{i}] sha is not a 40-hex blob SHA (FAIL-SCHEMA)")
    return v


def fetch_live_tree_blob_shas(paths: list[str]) -> tuple[dict[str, str] | None, str | None]:
    """Resolve blob SHAs for repo-relative paths at the trusted live tip.

    The gate fetches the tip's TREE objects itself (partial clone,
    --filter=blob:none: trees only, no blob contents) from the canonical repo
    and reads blob SHAs from the tree — bound to the exact tip returned by
    resolve_live_tip_trusted(). The builder cannot write these. No API token,
    no auth, no rate-limit dependency.
    Returns ({path: blob_sha}, None) or (None, error_message). Any error is
    fail-closed by the caller: unverifiable is not shippable.
    """
    tip, err = resolve_live_tip_trusted()
    if err:
        return None, err
    tmp = tempfile.mkdtemp(prefix="naya-gate-tree-")
    try:
        def git(*args):
            return subprocess.run(["git", "-C", tmp, *args],
                                  capture_output=True, text=True, timeout=90)
        r = git("init", "-q")
        if r.returncode != 0:
            return None, f"trusted tree fetch failed: git init exit {r.returncode}"
        r = git("fetch", "-q", "--depth", "1", "--filter=blob:none",
                CANONICAL_GIT_URL, "HEAD")
        if r.returncode != 0:
            return None, ("trusted tree fetch failed: git fetch exit "
                          f"{r.returncode}: {r.stderr.strip()[:160]}")
        r = git("rev-parse", "FETCH_HEAD")
        fetched = r.stdout.strip()
        if r.returncode != 0 or fetched.lower() != tip.lower():
            return None, ("trusted tree fetch failed: fetched tip "
                          f"{fetched[:8]} != trusted tip {tip[:8]} — refusing "
                          f"to verify against unbound state")
        out: dict[str, str] = {}
        for p in paths:
            r = git("ls-tree", "FETCH_HEAD", "--", p)
            if r.returncode != 0:
                return None, (f"trusted tree fetch failed: ls-tree exit "
                              f"{r.returncode} for {p!r}")
            m = re.match(r"^\d+ blob ([a-f0-9]{40})\t", r.stdout)
            if not m:
                return None, (f"component not found at live tip: {p!r} "
                              f"(no blob in tip tree)")
            out[p] = m.group(1)
        return out, None
    except (OSError, subprocess.TimeoutExpired) as e:
        return None, f"trusted tree fetch failed: {e}"
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


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

    # 2.7a component shape — pure validation, runs in every mode (no network)
    components = receipt.get("components")
    shape_v = validate_components_shape(components)
    v.extend(shape_v)

    # 2.7b COMPONENTS_LIVE (TRUSTED-RUNNER-DESIGN.md check 6) — enforce only.
    # Each RECORDED component SHA is verified against the live tree, fetched
    # by the gate itself and bound to the exact trusted tip. Forged or stale
    # component SHAs fail. A receipt recording no components emits an explicit
    # NOT_BOUND note (documented limit — v1 receipts record no components);
    # it does not fail the gate, and it does not pass silently.
    if enforce and not shape_v:
        if components:
            live, err = fetch_live_tree_blob_shas([c["path"] for c in components])
            if err:
                v.append(f"ACTIVATION: {err} (FAIL-TRUSTED-FETCH — unverifiable is not shippable)")
            else:
                for c in components:
                    want = str(c["sha"]).lower()
                    got = live.get(c["path"])
                    if got is None or got.lower() != want:
                        v.append(
                            f"ACTIVATION: component {c['path']!r} SHA {want[:8]} != "
                            f"live blob {(got[:8] if got else 'MISSING')} "
                            "(FAIL-COMPONENT-MISMATCH — forged or stale doctrine/blocks)")
        else:
            v.append("ACTIVATION-NOTE: receipt records no component SHAs — "
                     "COMPONENTS_LIVE NOT_BOUND (documented limit: without recorded "
                     "component SHAs the gate cannot prove current doctrine/blocks; "
                     "v1 receipts never record them)")
    # enforce=True and no caller tip: trusted fetch already handled above.
    return v, advisory

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
        notes = [x for x in violations if x.startswith("ACTIVATION-NOTE:")]
        fails = [x for x in violations if not x.startswith("ACTIVATION-NOTE:")]
        if fails:
            print(f"NAYA GATE: FAIL — {len(fails)} violation(s) in {page}:")
            for viol in fails:
                print(f"  x {viol}")
            for note in notes:
                print(f"  ! {note}")
            if advisory:
                print("  (advisory verdict — caller-supplied tip, NOT enforcement-grade)")
            return 1
        # Notes only: the gate passes, but the documented limits are visible.
        print(f"NAYA GATE: PASS — {page}" + (" (ADVISORY — not enforcement-grade)" if advisory else ""))
        for note in notes:
            print(f"  ! {note}")
        return 0
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

        # COMPONENTS shape — pure validation, no network (Naya 1 case 5)
        bad_comp = receipt(components=[{"path": "HUB/DESIGN-CONTRACT.md"}])
        rp_bc = td / "rbc.json"
        rp_bc.write_bytes(json.dumps(bad_comp).encode())
        d_bc = hashlib.sha256(rp_bc.read_bytes()).hexdigest()
        marked_bc = _good_html(f"<!-- NAYA-ACTIVATION-RECEIPT-SHA256:{d_bc} -->")
        vv, _ = run_activation_stage(marked_bc, rp_bc, enforce=False,
                                      caller_tip="a" * 40, trust_caller=True)
        check("malformed components (missing sha) rejected", vv, True)

        bad_comp2 = receipt(components="not-a-list")
        rp_bc2 = td / "rbc2.json"
        rp_bc2.write_bytes(json.dumps(bad_comp2).encode())
        d_bc2 = hashlib.sha256(rp_bc2.read_bytes()).hexdigest()
        marked_bc2 = _good_html(f"<!-- NAYA-ACTIVATION-RECEIPT-SHA256:{d_bc2} -->")
        vv, _ = run_activation_stage(marked_bc2, rp_bc2, enforce=False,
                                      caller_tip="a" * 40, trust_caller=True)
        check("malformed components (not a list) rejected", vv, True)

        # CLOSED-WORLD component rule (Naya 1 case 7): an undocumented class
        # fails even WITHOUT a naya- prefix — undocumented != escapes the rules.
        sneaky = td / "sneaky.html"
        sneaky.write_text("""<!DOCTYPE html><html><head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="dark">
<style>html{background:#050507}body{background:#050507;color:#f8f7fb}
.naya-btn{color:#fff}.widget{color:#fff}</style></head>
<body class="naya-page"><div class="widget">hi</div><button class="naya-btn">Go</button></body></html>""")
        check("undocumented non-prefixed class rejected (closed-world)",
              run_design_stage(sneaky, mf), True)

        # BEM modifier/element of a REGISTERED block stays permitted.
        bem = td / "bem.html"
        bem.write_text(_good_html().replace(
            'class="naya-btn"', 'class="naya-btn naya-btn--large"'))
        check("BEM modifier of registered block permitted",
              run_design_stage(bem, mf), False)

    print("SELF-TEST:", "ALL GREEN" if ok else "BROKEN")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
