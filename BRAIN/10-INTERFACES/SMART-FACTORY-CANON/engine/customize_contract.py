#!/usr/bin/env python3
"""Cured Template Customizer — factory-r1 (R1 proposal, NOT the live file).

Contract in → (customized HTML, application ledger) out.

THE CURE, in one rule: every field present in the contract ends the build
with a ledger entry — APPLIED (with the replacement count as evidence) or
NOT-APPLIED (with the reason). Silent drops are the defect being cured;
this module makes them structurally impossible: apply_contract() iterates
a fixed field plan and every branch appends to the ledger.

Display fields apply to the template base's real spots:
  name      → <title>, the #pname visible name spot, and every occurrence
              of the base's baked demo identity (registry base_identity +
              the known demo strings of the personal-v5 lineage)
  tagline   → the base's baked tagline string(s)
  about     → the base's baked about string(s)
  soul_color→ the template's exposed accent knobs (--soul / --tone hex)
  photo     → an <img> inside the #avv avatar well — the exact element the
              page's own upload logic inserts (.ph-av img CSS anticipates it)

Intent fields (idea, vision, do, behave, rules) and structured asks
(functions, pieces) have NO slots in any current template base — the bases
are one page body (personal-v5) with demo identities, pending the R4
template-model program. They are logged NOT-APPLIED with reasons, and the
receipt carries them so nothing is lost. Pieces are at least resolved
against the Step-0 library (pieces.json) so the receipt states whether
the piece exists.
"""

import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
PIECES_PATH = "/home/hatch/workspace/personal-app/pieces.json"

# Demo strings baked into the personal-v5 lineage (from the live
# customize.py's dual-coverage replacements — the strings that exist in
# the bases, verified by grep 2026-10-21).
KNOWN_DEMO = {
    "name": ["Alex Morgan", "Your Name"],
    "tagline": ["Building the future, one smart note at a time", "My personal hub"],
    "about": [
        "Founder and creator. I build intelligent systems that help people "
        "achieve their maximum. Passionate about AI, design, and human potential.",
        "Creator, thinker, builder. I turn ideas into reality.",
    ],
}

INTENT_FIELDS = ["idea", "vision", "do", "behave", "rules"]


def _replace_counted(html, old, new):
    """Replace all occurrences; return (html, count). No-op on empty old."""
    if not old or old == new:
        return html, 0
    n = html.count(old)
    if n:
        html = html.replace(old, new)
    return html, n


def _apply_display_field(html, field, value, base_identity, ledger):
    """Apply name/tagline/about to the base's real spots, with counts."""
    candidates = []
    baked = (base_identity or {}).get(field)
    if baked:
        candidates.append(baked)
    for s in KNOWN_DEMO.get(field, []):
        if s not in candidates:
            candidates.append(s)

    total = 0
    matched = []
    for cand in candidates:
        html, n = _replace_counted(html, cand, value)
        if n:
            total += n
            matched.append(cand)

    if field == "name":
        # The <title> spot: every current base titles itself 'My World'
        # regardless of its baked identity — set it to the app name.
        m = re.search(r"<title>[^<]*</title>", html)
        if m:
            html = html.replace(m.group(0), f"<title>{value}</title>", 1)
            total += 1
            matched.append("<title>")

    if total:
        ledger.append({
            "field": field, "status": "APPLIED",
            "detail": f"{total} replacement(s) across spot(s): "
                      + ", ".join(repr(s[:40]) for s in matched),
        })
    else:
        ledger.append({
            "field": field, "status": "NOT-APPLIED",
            "reason": "no matching name/tagline/about spot found in template base",
        })
    return html


def _apply_soul_color(html, color, ledger):
    """Recolor the template's exposed accent knobs (--soul / --tone)."""
    total = 0
    for knob in ("--soul:", "--tone:"):
        pat = knob + "#a06bff"
        html, n = _replace_counted(html, pat, knob + color)
        total += n
    if total:
        ledger.append({
            "field": "soul_color", "status": "APPLIED",
            "detail": f"{total} accent knob(s) (--soul/--tone) set to {color}; "
                      "wider spectrum glows unchanged by design (knob scope)",
        })
    else:
        ledger.append({
            "field": "soul_color", "status": "NOT-APPLIED",
            "reason": "template base exposes no --soul/--tone accent knob",
        })
    return html


def _apply_photo(html, url, ledger):
    """Insert the contract photo as the avatar <img> inside #avv — the
    element the page's own upload handler inserts (.ph-av img is styled)."""
    m = re.search(r'(<div class="ph-av" id="avv">)', html)
    if m:
        img = f'<img src="{url}" alt="" style="width:100%;height:100%;object-fit:cover;border-radius:50%;">'
        html = html.replace(m.group(1), m.group(1) + img, 1)
        ledger.append({
            "field": "photo", "status": "APPLIED",
            "detail": f"avatar <img> inserted into #avv with contract photo URL {url}",
        })
    else:
        ledger.append({
            "field": "photo", "status": "NOT-APPLIED",
            "reason": "template base has no #avv avatar well",
        })
    return html


def apply_contract(html, contract, base_identity):
    """Apply a contract-v1 contract to a template base.
    Returns (html, ledger). Ledger covers every field PRESENT in the
    contract (plus structural entries added by the caller)."""
    ledger = []

    # --- display fields -------------------------------------------------
    # ORDER MATTERS (proven by the R1 test build): the base's baked about
    # text contains the demo name ("Acme Corp delivers excellence…"), so
    # replacing name first destroys the about candidate before its turn.
    # Longest/most-specific strings first: about -> tagline -> name.
    for field in ("about", "tagline", "name"):
        if contract.get(field):
            html = _apply_display_field(html, field, str(contract[field]),
                                        base_identity, ledger)

    if contract.get("soul_color"):
        html = _apply_soul_color(html, str(contract["soul_color"]), ledger)

    if contract.get("photo"):
        html = _apply_photo(html, str(contract["photo"]), ledger)

    # --- intent fields: no display slot in any current base -------------
    for field in INTENT_FIELDS:
        if contract.get(field):
            ledger.append({
                "field": field, "status": "NOT-APPLIED",
                "reason": "prose intent field — no slot in current template "
                          "bases (one shared page body; slots arrive with "
                          "the R4 template-model program). Carried in the "
                          "receipt so the intent is never lost.",
            })

    # --- functions: bases have a baked feature set, no slots -----------
    funcs = contract.get("functions") or {}
    for fname, on in funcs.items():
        if on:
            ledger.append({
                "field": f"functions.{fname}", "status": "NOT-APPLIED",
                "reason": "template base has a baked feature set and no "
                          "per-function slots; function wiring arrives "
                          "with the R4 template-model program.",
            })

    # --- pieces: resolve against the library, no slots in bases ---------
    pieces = contract.get("pieces") or []
    if pieces:
        try:
            with open(PIECES_PATH) as f:
                library = json.load(f)
        except Exception:
            library = {}
        for piece in pieces:
            model = piece.get("model", "?")
            resolved = model in library
            ledger.append({
                "field": f"pieces.{model}", "status": "NOT-APPLIED",
                "reason": ("resolved in the Step-0 library (pieces.json) but "
                           "the template base defines no piece slots; slot "
                           "standard arrives with R4."
                           if resolved else
                           "piece model not found in the Step-0 library "
                           "(pieces.json), and the template base defines no "
                           "piece slots."),
            })

    # --- identity plumbing (not contract content, but receipted) -------
    if contract.get("handle"):
        ledger.append({
            "field": "handle", "status": "APPLIED",
            "detail": "used as the worker-name slug (see receipt.worker)",
        })

    return html, ledger
