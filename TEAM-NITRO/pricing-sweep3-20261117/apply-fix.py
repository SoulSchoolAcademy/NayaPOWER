#!/usr/bin/env python3
"""Sweep #3 fix round for Free Entry (/free) — REPORT-13.

Reads the verified base (fixed-entry.html, sha 06b08242...) in this
directory, applies the 14 fix items in place (never a rebuild), and
writes the fixed page + PWA icons + manifest back here.

Every replacement asserts its exact match count: a count of 0 or >1
STOPS the script instead of silently editing the wrong bytes.
Run: python3 apply-fix.py
"""
import base64
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "fixed-entry.html")

BASE_SHA = "06b08242c72e9d0b8f28037df3b93e74c5955e6702f358d0a07fff799edf58fd"


def sha(b):
    return hashlib.sha256(b).hexdigest()


def rep(text, old, new, count=1):
    n = text.count(old)
    assert n == count, f"REPLACE FAIL (want {count}, got {n}): {old[:110]!r}"
    return text.replace(old, new)


def main():
    raw = open(SRC, "rb").read()
    assert sha(raw) == BASE_SHA, f"base sha mismatch: {sha(raw)}"
    t = raw.decode("utf-8")
    orig_len = len(t)

    # ================================================================
    # Fix 8 — headings + zoom.
    # ================================================================
    t = rep(t, '<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">',
            '<meta name="viewport" content="width=device-width, initial-scale=1.0">')
    t = rep(t, '<div class="cert-title">Certificate of Smart Identity</div>',
            '<h1 class="cert-title">Certificate of Smart Identity</h1>')

    # ================================================================
    # Fix 12 — clock placeholder: paint nothing until ticked.
    # (Zero rule: a missing number never wears a bare dash.)
    # ================================================================
    t = rep(t, '<span id="sysClock">—</span>', '<span id="sysClock"></span>')

    # ================================================================
    # Fix 13 — hub-note latent leak: plain human words, no variable name.
    # ================================================================
    t = rep(t, '<p class="hub-note" id="hubNote" hidden>One step left: set <code>HUB_APP_URL</code> in this page to your Intelligent Hub address, then this button takes you straight in.</p>',
            '<p class="hub-note" id="hubNote" hidden>One step left: the Hub address isn\'t set yet, so this button can\'t take you straight in.</p>')

    # ================================================================
    # Fix 1 — type scale 25 / 19 / 17 (root is the 16px default; the
    # fix is in the rules, not the root). 1.5625rem=25, 1.1875rem=19,
    # 1.0625rem=17. Headline: cert-title. Sub-headline: brand wordmark,
    # status line, install sub, phone title. Everything else: 17.
    # ================================================================
    t = rep(t, "    .brand-logo-title { font-family: var(--serif); font-size: 0.90rem; font-weight: 600;",
            "    .brand-logo-title { font-family: var(--serif); font-size: 1.1875rem; font-weight: 600;")
    t = rep(t, "      font-size: 0.66rem; font-weight: 600; letter-spacing: 0.18em; text-transform: uppercase;",
            "      font-size: 1.0625rem; font-weight: 600; letter-spacing: 0.18em; text-transform: uppercase;")
    t = rep(t, "      color: var(--ink); font-size: 0.76rem; font-weight: 700; letter-spacing: 0.18em;",
            "      color: var(--ink); font-size: 1.0625rem; font-weight: 700; letter-spacing: 0.18em;")
    t = rep(t, "    .cert-title { margin-top: 10px; font-size: 0.95rem; font-weight: 700;",
            "    .cert-title { margin-top: 10px; font-size: 1.5625rem; font-weight: 700;")
    t = rep(t, "    .id-box-label { font-size: 0.66rem; font-weight: 700; letter-spacing: 0.36em;",
            "    .id-box-label { font-size: 1.0625rem; font-weight: 700; letter-spacing: 0.36em;")
    t = rep(t, "    .cert-date { font-size: 0.74rem; font-weight: 600; letter-spacing: 0.26em;",
            "    .cert-date { font-size: 1.0625rem; font-weight: 600; letter-spacing: 0.26em;")
    t = rep(t, "    .cert-benefit { position: relative; margin-top: 7px; font-size: 0.88rem; font-weight: 500;",
            "    .cert-benefit { position: relative; margin-top: 7px; font-size: 1.0625rem; font-weight: 500;")
    t = rep(t, "    .cert-privacy { position: relative; margin-top: 9px; font-size: 0.78rem; font-weight: 500;",
            "    .cert-privacy { position: relative; margin-top: 9px; font-size: 1.0625rem; font-weight: 500;")
    t = rep(t, "    .cert-no { font-size: 0.72rem; font-weight: 700; letter-spacing: 0.30em;",
            "    .cert-no { font-size: 1.0625rem; font-weight: 700; letter-spacing: 0.30em;")
    t = rep(t, "      font-size: 0.88rem; font-weight: 600; color: #f2f2f6;",
            "      font-size: 1.1875rem; font-weight: 600; color: #f2f2f6;")
    t = rep(t, "    .hub-note { margin-top: 14px; font-size: 0.85rem; font-weight: 500; color: #f2f2f6;",
            "    .hub-note { margin-top: 14px; font-size: 1.0625rem; font-weight: 500; color: #f2f2f6;")
    t = rep(t, "      font-size: 0.84rem; font-weight: 700; letter-spacing: 0.20em;",
            "      font-size: 1.0625rem; font-weight: 700; letter-spacing: 0.20em;")
    t = rep(t, "      font-size: 0.95rem; cursor: pointer;",
            "      font-size: 1.0625rem; cursor: pointer;")
    t = rep(t, "    .install-sub { color: var(--silver); font-size: 0.95rem; line-height: 1.55; margin: 0 0 22px; }",
            "    .install-sub { color: var(--silver); font-size: 1.1875rem; line-height: 1.55; margin: 0 0 22px; }")
    t = rep(t, "    .install-manual { font-size: 0.85rem; color: var(--silver); line-height: 1.6;",
            "    .install-manual { font-size: 1.0625rem; color: var(--silver); line-height: 1.6;")
    t = rep(t, "    .im-title { margin: 0 0 10px; font-size: 0.74rem; font-weight: 700;",
            "    .im-title { margin: 0 0 10px; font-size: 1.0625rem; font-weight: 700;")
    t = rep(t, "    .im-row strong { display: block; color: var(--ink); font-size: 0.86rem;",
            "    .im-row strong { display: block; color: var(--ink); font-size: 1.0625rem;")
    t = rep(t, "      font-size: 0.60rem; font-weight: 800; letter-spacing: 0.18em;",
            "      font-size: 1.0625rem; font-weight: 800; letter-spacing: 0.18em;")
    t = rep(t, "    .im-steps li { margin: 3px 0; color: var(--silver); font-size: 0.84rem; line-height: 1.5; }",
            "    .im-steps li { margin: 3px 0; color: var(--silver); font-size: 1.0625rem; line-height: 1.5; }")
    t = rep(t, "    .im-alt { margin: 8px 0 0; font-size: 0.76rem; color: var(--muted); line-height: 1.5; }",
            "    .im-alt { margin: 8px 0 0; font-size: 1.0625rem; color: var(--muted); line-height: 1.5; }")
    t = rep(t, "    .im-foot { margin: 10px 0 0; font-size: 0.80rem; color: var(--muted); line-height: 1.5; }",
            "    .im-foot { margin: 10px 0 0; font-size: 1.0625rem; color: var(--muted); line-height: 1.5; }")
    t = rep(t, "      font-size: 0.80rem; letter-spacing: 0.14em; text-transform: uppercase;",
            "      font-size: 1.0625rem; letter-spacing: 0.14em; text-transform: uppercase;")
    t = rep(t, "      .brand-logo-title { font-size: 0.72rem; letter-spacing: 0.14em; }",
            "      .brand-logo-title { font-size: 1.0625rem; letter-spacing: 0.14em; }")
    t = rep(t, "      .install-corner { padding: 8px 13px; min-height: 38px; font-size: 0.64rem; letter-spacing: 0.12em; margin-left: 8px; }",
            "      .install-corner { padding: 8px 13px; min-height: 38px; font-size: 1.0625rem; letter-spacing: 0.12em; margin-left: 8px; }")
    t = rep(t, "      .cert-no { font-size: 0.68rem; letter-spacing: 0.20em; text-indent: 0.20em; }",
            "      .cert-no { font-size: 1.0625rem; letter-spacing: 0.20em; text-indent: 0.20em; }")
    t = rep(t, "      .cert-title { margin-top: 14px; font-size: 0.78rem; letter-spacing: 0.36em; text-indent: 0.36em; }",
            "      .cert-title { margin-top: 14px; font-size: 1.1875rem; letter-spacing: 0.36em; text-indent: 0.36em; }")
    t = rep(t, "      .bottom-system-bar { font-size: 0.64rem; letter-spacing: 0.06em; padding: 0 10px; }",
            "      .bottom-system-bar { font-size: 1.0625rem; letter-spacing: 0.06em; padding: 0 10px; }")
    t = rep(t, "      font-size:clamp(.84rem,3.6vw,1rem);",
            "      font-size:clamp(1.0625rem,3.6vw,1.1875rem);")
    t = rep(t, "        font-size:.76rem;",
            "        font-size:1.0625rem;")
    t = rep(t, "font-size:.8rem;font-weight:700",
            "font-size:1.0625rem;font-weight:700")
    # The 480px step-down retires with the floor: the caption stays
    # 1.0625rem at every width (it wraps to three lines at 390px).
    t = rep(t, "    @media (max-width: 480px) {\n      .cert-benefit { font-size: 0.82rem; }\n    }",
            "    /* SWEEP #3 (2026-11-17): the 480px step-down to 0.82rem is retired — the type scale (§2.3) floors at 17px, so the caption stays 1.0625rem at every width and wraps to three lines at 390px. The comment above records the old fit reason. */")

    # ================================================================
    # Fix 2 + Fix 9 — deep palette (§3.1) + Spectrum Flow re-flow.
    # Re-flow: focus BLUE (sapphire) -> Link GREEN (emerald) -> Mail
    # GOLD (deep gold) -> ENTER PURPLE (royal). The v2.7 assignment
    # (Link blue, Mail gold, ENTER purple) predates the Flow law.
    # ================================================================
    # :root first.
    t = rep(t, "      --green: #2fe89e;\n      --gold: #ffbf3d;",
            "      --green: #07925f;\n      --gold: #d4a017;\n      --blue: #0f52ba;")
    t = rep(t, "      --royal: #a06bff;",
            "      --royal: #8e24aa;")
    t = rep(t, "      --purple: #a855f7; /* harvested with the entrance .enter button — its border color */",
            "      --purple: #8e24aa; /* SWEEP #3 (2026-11-17): deep palette — the entrance .enter button's border, re-valued to the §3.1 table; the bright value it was harvested with is superseded */")
    t = rep(t, "      --royal-soft: rgba(160, 107, 255, 0.55);",
            "      --royal-soft: rgba(142, 36, 170, 0.55);")
    t = rep(t, "      --royal-faint: rgba(160, 107, 255, 0.26);",
            "      --royal-faint: rgba(142, 36, 170, 0.26);")
    t = rep(t, "      --label: #a06bff;",
            "      --label: #8e24aa;")
    # Focus ring + travel go BLUE (sapphire) — do these BEFORE the
    # global bright-green swap, which must only catch the eye hover.
    t = rep(t, "        rgba(47,232,158,0) 292deg, rgba(196,255,228,0.95) 326deg,\n        rgba(47,232,158,0) 352deg, transparent 360deg);",
            "        rgba(15,82,186,0) 292deg, rgba(190,214,255,0.95) 326deg,\n        rgba(15,82,186,0) 352deg, transparent 360deg);")
    t = rep(t, "        0 0 0 1.5px rgba(47,232,158,0.90),\n        0 0 34px rgba(47,232,158,0.55); }",
            "        0 0 0 1.5px rgba(15,82,186,0.90),\n        0 0 34px rgba(15,82,186,0.55); }")
    t = rep(t, "    .alias-field-wrapper:focus-within { border-color: var(--green);",
            "    .alias-field-wrapper:focus-within { border-color: var(--blue);")
    # Global bright -> deep swaps (counts verified against the base).
    t = rep(t, "#2fe89e", "#07925f", count=1)          # eye hover (the --green var was replaced in the :root block above)
    t = rep(t, "47,232,158", "7,146,95", count=1)      # eye hover glow only now
    t = rep(t, "63,184,255", "7,146,95", count=9)      # Link box -> emerald
    t = rep(t, "255,191,61", "212,160,23", count=9)    # Mail box -> deep gold
    t = rep(t, "160,107,255", "142,36,170", count=22)  # royal purple family
    t = rep(t, "168,85,247", "142,36,170", count=3)    # harvested .enter glow
    # Link / Mail box faces: dark tints of the deep hues + 135 deg.
    t = rep(t, "      background: linear-gradient(180deg, #163a56 0%, #0a1c2e 46%, #030609 100%);",
            "      background: linear-gradient(135deg, #0b3d2c 0%, #062015 46%, #030604 100%);")
    t = rep(t, "    .mail-line { background: linear-gradient(180deg, #3a2a09 0%, #1c1204 46%, #060402 100%);",
            "    .mail-line { background: linear-gradient(135deg, #33260a 0%, #1a1305 46%, #060402 100%);")
    # Box labels: light tints of their (new) families.
    t = rep(t, "    .link-line .id-box-label { color: #a8dcff; }",
            "    .link-line .id-box-label { color: #a9e5cd; }")
    t = rep(t, "    .mail-line .id-box-label { color: #ffd97a; }",
            "    .mail-line .id-box-label { color: #ecd27e; }")
    # breathe-blue becomes breathe-green (Link is green now).
    t = rep(t, "breathe-blue", "breathe-green", count=2)
    # Seal star + frame light: light tints of the deep families.
    t = rep(t, "rgba(255,236,190,0.85)", "rgba(246,220,143,0.85)")
    t = rep(t, "rgba(255,205,120,0.34)", "rgba(233,198,92,0.34)")
    t = rep(t, "rgba(255,190,110,0.10)", "rgba(212,160,23,0.10)")
    t = rep(t, "rgba(230,216,255,0.85)", "rgba(216,190,255,0.85)")

    # ================================================================
    # Fix 10 — light direction: linear gradients to 135 deg; radial
    # lights to top-left. Conic rings (frame travel, well travel) and
    # the centred seal-star radial have no linear angle; recorded.
    # ================================================================
    t = rep(t, "      background: radial-gradient(ellipse 130% 90% at 50% 34%, #060607 0%, #020203 55%, #000000 100%);",
            "      background: radial-gradient(ellipse 130% 90% at 0% 0%, #060607 0%, #020203 55%, #000000 100%);")
    t = rep(t, "      background: linear-gradient(168deg, #050506 0%, #010102 55%, #030304 100%);",
            "      background: linear-gradient(135deg, #050506 0%, #010102 55%, #030304 100%);")
    t = rep(t, "      background: linear-gradient(105deg, transparent 42%, rgba(245,241,232,0.13) 50%, transparent 58%);",
            "      background: linear-gradient(135deg, transparent 42%, rgba(245,241,232,0.13) 50%, transparent 58%);")
    t = rep(t, "      background: linear-gradient(105deg, transparent 42%, rgba(255,255,255,0.08) 50%, transparent 58%);",
            "      background: linear-gradient(135deg, transparent 42%, rgba(255,255,255,0.08) 50%, transparent 58%);")
    t = rep(t, "      background: linear-gradient(115deg, transparent 32%, rgba(255,255,255,0.55) 50%, transparent 68%);",
            "      background: linear-gradient(135deg, transparent 32%, rgba(255,255,255,0.55) 50%, transparent 68%);")
    t = rep(t, "      background: linear-gradient(155deg, #e9edf5 0%, #78818f 52%, #c9d1de 100%);",
            "      background: linear-gradient(135deg, #e9edf5 0%, #78818f 52%, #c9d1de 100%);")
    t = rep(t, "      background: linear-gradient(165deg, #101013 0%, #070708 100%);",
            "      background: linear-gradient(135deg, #101013 0%, #070708 100%);")
    t = rep(t, "      background: linear-gradient(180deg, #17171c 0%, #050505 55%, #0a0a0e 100%);",
            "      background: linear-gradient(135deg, #17171c 0%, #050505 55%, #0a0a0e 100%);")
    t = rep(t, "        circle at 50% 0%,\n        #302054,",
            "        circle at 0% 0%,\n        #2e0a38,")

    # ================================================================
    # Fix 11 — clock dot: a jewel, not a flat dot.
    # ================================================================
    t = rep(t, "    .clock-dot { width: 6px; height: 6px; border-radius: 50%; background: var(--royal); }",
            "    .clock-dot { width: 8px; height: 8px; border-radius: 50%;\n      background: radial-gradient(circle at 30% 28%, #ffffff 0%, #e3c8f5 24%, #8e24aa 58%, #3d0a52 100%);\n      box-shadow: 0 0 6px rgba(142,36,170,0.65), inset 0 0 1px rgba(255,255,255,0.65); }")

    # Header fit guard (Fix 1 consequence): at the 17px floor the
    # header (wordmark + clock + Install) needs ~970px; below 1024px
    # the clock would clip the Install button. The clock is chrome —
    # the certificate is the ceremony — so it hides at tablet widths
    # too (phones already hid it). Verified by measurement, §5.
    t = rep(t, "    @media (max-width: 640px) { .sys-clock { display: none; } }",
            "    /* SWEEP #3 (2026-11-17): the clock hides at tablet widths too — measured in Chromium: the header with the clock needs 956px, so below 960px the clock would push Install off-screen. Desktop keeps it. */\n    @media (max-width: 960px) { .sys-clock { display: none; } }")

    # ================================================================
    # Assignment comments, corrected to the re-flow (history kept,
    # the new assignment named with its date and law).
    # ================================================================
    t = rep(t, "       colors Shawn assigned: Smart Link burns BLUE (#3fb8ff),\n       Secure Smart Mail ID burns GOLD (#ffbf3d), ENTER breathes\n       PURPLE; the box values are pure bright white lit by their",
            "       colors Shawn assigned (v2.7): Smart Link BLUE, Secure Smart\n       Mail ID GOLD, ENTER PURPLE — SWEEP #3 (2026-11-17): the\n       Spectrum Flow (his 18:00Z law) re-flows the ignition to BLUE\n       → GREEN → GOLD, so the input's focus is sapphire #0f52ba, the\n       Smart Link box is emerald #07925f, the Mail box stays gold\n       #d4a017 and ENTER stays royal #8e24aa (all re-valued to the\n       deep palette, §3.1); the box values are pure bright white\n       lit by their")
    t = rep(t, "       Each box now BURNS in the color Shawn assigned it: Smart\n       Link BLUE (#3fb8ff), Secure Smart Mail ID GOLD (#ffbf3d);",
            "       Each box now BURNS in its Spectrum Flow color (SWEEP #3,\n       2026-11-17 — v2.7's Link BLUE / Mail GOLD assignment predates\n       the Flow law): Smart Link EMERALD #07925f, Secure Smart Mail\n       ID GOLD #d4a017; the input's focus carries the BLUE #0f52ba;")
    t = rep(t, "       the certificate's center, inside the frame. The input glows\n       GREEN; ENTER carries the PURPLE glow (below). Both keep the",
            "       the certificate's center, inside the frame. The input glows\n       BLUE on focus; ENTER carries the PURPLE glow (below). SWEEP #3:\n       Spectrum Flow — blue precedes green; the Link box is green now.\n       Both keep the")
    t = rep(t, "       v211/DEPTH-RECIPE.md). Its focus color is the certificate's\n       green. Depth = edge contrast + crisp shade + luminance",
            "       v211/DEPTH-RECIPE.md). Its focus color is sapphire blue\n       (SWEEP #3: Spectrum Flow). Depth = edge contrast + crisp shade\n       + luminance")
    t = rep(t, "    /* v2.9 — FOCUS TRAVEL (Shawn's motion law, 02:04Z): while the\n       well holds focus, its green light TRAVELS the border ring —",
            "    /* v2.9 — FOCUS TRAVEL (Shawn's motion law, 02:04Z): while the\n       well holds focus, its blue light TRAVELS the border ring —")
    t = rep(t, "    /* Focus: the green ignites — and the well DEEPENS (v2.9: the",
            "    /* Focus: the blue ignites — and the well DEEPENS (v2.9: the")
    t = rep(t, "    /* Available speaks GREEN — the input's own glow family (v2.4);",
            "    /* Available speaks GREEN — live and good (v2.4; SWEEP #3: the Link box's family now — the input's focus is blue);")

    # ================================================================
    # Fit compensations for the 17px floor (the foot's own rhythm,
    # v2.11.1's own method) + the face scrolls when the document is
    # taller than the frame (the page's own tall-state pattern).
    # ================================================================
    # Benefit / privacy measure: 460 -> 500px keeps the benefit on two
    # lines at desktop at 17px (it would spill to three at 460).
    t = rep(t, "      max-width: 460px; padding: 0 6px; }", "      max-width: 500px; padding: 0 6px; }", count=3)
    # Desktop panels-shown compression.
    t = rep(t, "      .cert-plaque:not(.is-certified):has(.cert-lines:not([hidden])):not(:has(.alias-status[data-state=\"taken\"])) .alias-status { margin-top: 4px; }",
            "      .cert-plaque:not(.is-certified):has(.cert-lines:not([hidden])):not(:has(.alias-status[data-state=\"taken\"])) .alias-status { margin-top: 2px; }")
    t = rep(t, "      .cert-plaque:not(.is-certified):has(.cert-lines:not([hidden])):not(:has(.alias-status[data-state=\"taken\"])) .cert-lines { margin-top: 6px; gap: 6px; }",
            "      .cert-plaque:not(.is-certified):has(.cert-lines:not([hidden])):not(:has(.alias-status[data-state=\"taken\"])) .cert-lines { margin-top: 4px; gap: 4px; }")
    t = rep(t, "      .cert-plaque:not(.is-certified):has(.cert-lines:not([hidden])):not(:has(.alias-status[data-state=\"taken\"])) .cert-line { padding: 7px 18px 8px; gap: 3px; }",
            "      .cert-plaque:not(.is-certified):has(.cert-lines:not([hidden])):not(:has(.alias-status[data-state=\"taken\"])) .cert-line { padding: 5px 18px 6px; gap: 2px; }")
    t = rep(t, "      .cert-plaque:not(.is-certified):has(.cert-lines:not([hidden])):not(:has(.alias-status[data-state=\"taken\"])) .activate-btn { margin-top: 6px; }",
            "      .cert-plaque:not(.is-certified):has(.cert-lines:not([hidden])):not(:has(.alias-status[data-state=\"taken\"])) .activate-btn { margin-top: 4px; }")
    t = rep(t, "      .cert-plaque:not(.is-certified):has(.cert-lines:not([hidden])):not(:has(.alias-status[data-state=\"taken\"])) .cert-claim { margin-top: 8px; line-height: 1.24; }",
            "      .cert-plaque:not(.is-certified):has(.cert-lines:not([hidden])):not(:has(.alias-status[data-state=\"taken\"])) .cert-claim { margin-top: 6px; line-height: 1.24; }")
    t = rep(t, "      .cert-plaque:not(.is-certified):has(.cert-lines:not([hidden])):not(:has(.alias-status[data-state=\"taken\"])) .cert-benefit { margin-top: 3px; line-height: 1.45; }",
            "      .cert-plaque:not(.is-certified):has(.cert-lines:not([hidden])):not(:has(.alias-status[data-state=\"taken\"])) .cert-benefit { margin-top: 2px; line-height: 1.45; }")
    t = rep(t, "      .cert-plaque:not(.is-certified):has(.cert-lines:not([hidden])):not(:has(.alias-status[data-state=\"taken\"])) .cert-privacy { margin-top: 4px; line-height: 1.42; }",
            "      .cert-plaque:not(.is-certified):has(.cert-lines:not([hidden])):not(:has(.alias-status[data-state=\"taken\"])) .cert-privacy { margin-top: 2px; line-height: 1.42; }\n      /* SWEEP #3 (2026-11-17): panels-shown trims — the well slims and the face starts higher, so the 17px foot scrolls less. */\n      .cert-plaque:not(.is-certified):has(.cert-lines:not([hidden])):not(:has(.alias-status[data-state=\"taken\"])) .alias-field-wrapper { padding: 10px 18px; }\n      .cert-plaque:not(.is-certified):has(.cert-lines:not([hidden])):not(:has(.alias-status[data-state=\"taken\"])) .identity-face { padding-top: 16px; }")
    # Phone panels-shown compression.
    t = rep(t, "      .cert-line { padding: 5px 18px 7px; gap: 3px; }",
            "      .cert-line { padding: 4px 18px 6px; gap: 3px; }")
    t = rep(t, "      .cert-claim { margin-top: 6px; font-size: 1.20rem; line-height: 1.24; }",
            "      .cert-claim { margin-top: 4px; font-size: 1.20rem; line-height: 1.24; }")
    # The face scrolls when the panels-shown document is taller than
    # the frame — reachable tail, never a clipped line. At scroll 0
    # the input sits exactly where it sat (measured, §5).
    t = rep(t, "    /* ---------- v2.11 — mobile: quiet corner, lifted composition ----------",
            "    /* SWEEP #3 (2026-11-17) — THE TAIL IS REACHABLE, NEVER CLIPPED.\n       The 17px floor makes the panels-shown foot taller than its track\n       (and the baseline already clipped the privacy line 33px at desktop,\n       52px at phone, measured live — v2.11.1's “≈836” does not reproduce).\n       The face scrolls inside the frame when the document is taller than\n       it — the page's own tall-state pattern (taken / certified already\n       scroll) — so the privacy line is a short scroll away, never cut off;\n       at scroll 0 the input sits exactly where it sat. */\n    .cert-plaque:not(.is-certified):has(.cert-lines:not([hidden])) .identity-face { overflow-y: auto; }\n\n    /* ---------- v2.11 — mobile: quiet corner, lifted composition ----------")
    # Phone panels-shown trims, appended to the phone block's fit rules.
    t = rep(t, "      .cert-privacy { margin-top: 2px; line-height: 1.42; }",
            "      .cert-privacy { margin-top: 2px; line-height: 1.42; }\n      /* SWEEP #3 (2026-11-17): panels-shown phone trims — the well slims and the face starts higher, so the 17px foot scrolls less. */\n      .cert-plaque:not(.is-certified):has(.cert-lines:not([hidden])) .alias-field-wrapper { padding: 10px 18px; }\n      .cert-plaque:not(.is-certified):has(.cert-lines:not([hidden])) .identity-face { padding-top: 12px; }")

    # ================================================================
    # Fix 5 — veil truth: the veil INTERCEPTS. First click dismisses
    # only and never reaches the control beneath (the pointer-
    # transparent veil let ENTER claim under it on the first click
    # wherever the card did not cover it; the F4 probe only saw the
    # covered geometry at 635px).
    # ================================================================
    t = rep(t, "    .install-veil{pointer-events:none;}",
            "    /* SWEEP #3 (2026-11-17): the veil INTERCEPTS — first click dismisses only, never claims under it (see the veil handler note below). */\n    .install-veil{pointer-events:auto;}")
    veil_old = None
    for line in t.split("\n"):
        if line.strip().startswith("/* PRICING FIX (2026-11-17, item 4): the veil must never block"):
            veil_old = line
            break
    assert veil_old, "veil comment not found"
    veil_new = ("      /* SWEEP #3 (2026-11-17) CORRECTS the F4 shape: the veil INTERCEPTS (CSS pointer-events:auto) — the FIRST pointerdown "
                "anywhere dismisses only and never reaches the control beneath, so ENTER cannot claim under the visible veil. The F4 shape was "
                "pointer-transparent with buttons exempt: the 635px probe only proved the covered geometry (the card sat over ENTER's center, so the "
                "click died on the common ancestor), while an uncovered ENTER fired — and claimed — on the first click. Only the card's BUTTONS are "
                "exempt now, so Install App / Not now / the X still work. The click that dismisses does not also fire the control beneath it; the "
                "next click acts. */")
    t = rep(t, veil_old, veil_new)

    # ================================================================
    # Fix 3 — keyboard Enter submits. Veil rule: Enter while the veil
    # is up dismisses the veil first and does NOT submit (one gesture,
    # one outcome). The veil's own keydown handler skips Enter from
    # this field so this handler decides.
    # ================================================================
    t = rep(t, "    aliasInput.value = '';\n",
            "    aliasInput.value = '';\n\n    /* SWEEP #3 (2026-11-17) — KEYBOARD ENTER SUBMITS: the most natural\n       gesture on an entry page did nothing (no handler, no <form>).\n       Enter now fires the same door as the ENTER button. VEIL RULE: while\n       the install veil is up, Enter dismisses the veil first and does NOT\n       submit — one gesture, one outcome (the veil's own keydown handler\n       skips Enter from this field so this handler decides). */\n    aliasInput.addEventListener('keydown', function (e) {\n      if (e.key !== 'Enter') return;\n      var veil = document.getElementById('installVeil');\n      if (veil && !veil.hidden) { if (window.__nayaCloseInstallVeil) window.__nayaCloseInstallVeil(); return; }\n      e.preventDefault();\n      if (window.activateAndRedirect) window.activateAndRedirect();\n    });\n")
    t = rep(t, "      document.addEventListener('keydown', function (e) { if (veil.hidden) return; if (e.target && e.target.closest && e.target.closest('button')) return; if (e.key !== 'Escape') dismiss(); }, true);",
            "      document.addEventListener('keydown', function (e) { if (veil.hidden) return; if (e.target && e.target.closest && e.target.closest('button')) return; if (e.key === 'Enter' && e.target && e.target.id === 'aliasInput') return; /* SWEEP #3: Enter from the alias field is the field's own handler's call (dismiss-first, never submit-under-veil) */ if (e.key !== 'Escape') dismiss(); }, true);")

    # ================================================================
    # Fix 6 — taken-name spelling: the spaced name, not the stripped
    # echo. Only the spelling changes; fitTakenName keeps the
    # one-line rule. (The claim-time stored name is untouched — Fix 7
    # forbids redesigning the claim flow; the walk still corrects it
    # on restore, as before.)
    # ================================================================
    t = rep(t, "    const prettyName = s => s ? s.charAt(0).toUpperCase() + s.slice(1) : '';\n",
            "    const prettyName = s => s ? s.charAt(0).toUpperCase() + s.slice(1) : '';\n    /* SWEEP #3 (2026-11-17) — THE TAKEN NAME IS SPELLED, NOT STRIPPED:\n       the echo painted prettyName(alias) — “Rowanhale” — while the fresh\n       certificate paints the spaced name (“Rowan Hale”). The spaced name\n       comes from the typed words themselves (or the passed/saved name\n       when it matches this alias); an alias typed without spaces paints\n       exactly as before. Only the spelling changes. */\n    function spacedName(alias) {\n      var raw = '';\n      try { raw = aliasInput.value || ''; } catch (e) {}\n      if (rawName && rawName.toLowerCase().replace(/[^a-z0-9]/g, '') === alias) return rawName;\n      var words = String(raw).split(/[^A-Za-z0-9]+/).filter(function (w) { return !!w; });\n      if (!words.length) return prettyName(alias);\n      return words.map(function (w) { return w.charAt(0).toUpperCase() + w.slice(1); }).join(' ');\n    }\n")
    t = rep(t, "      if (nameEl) { nameEl.textContent = prettyName(currentAlias); nameEl.hidden = false; }",
            "      if (nameEl) { nameEl.textContent = spacedName(currentAlias); nameEl.hidden = false; }")

    # ================================================================
    # Fix 4 (page part) — install card logo fallback: the seal art is
    # the source (the inspector's “no .logo-hero” is wrong — the seal
    # img exists at line 1205 and the copy works); the shipped icon is
    # the fallback so the card never renders an empty logo box.
    # ================================================================
    t = rep(t, "        if (logo && hero && hero.src) logo.src = hero.src;",
            "        if (logo && hero && hero.src) logo.src = hero.src;\n        else if (logo) logo.src = 'icons/apple-touch-icon.png'; /* SWEEP #3: the card never renders an empty logo box — the seal art is the source; the shipped icon is the fallback. */")

    # ================================================================
    # Final guards: nothing the brief forbids, everything it orders.
    # ================================================================
    assert "maximum-scale" not in t, "viewport still locks zoom"
    assert "<h1 class=\"cert-title\">" in t, "h1 missing"
    assert '<span id="sysClock"></span>' in t, "clock placeholder not empty"
    assert "HUB_APP_URL</code>" not in t, "hub-note still names the variable"
    assert "pointer-events:none" not in t or t.count("pointer-events:none") == 0, "veil still pointer-transparent"
    assert "breathe-blue" not in t, "breathe-blue rename incomplete"
    for bad in ["#2fe89e", "#ffbf3d", "#a06bff", "#a855f7", "#3fb8ff", "#a8dcff", "#ffd97a",
                "47,232,158", "63,184,255", "255,191,61", "160,107,255", "168,85,247",
                "#163a56", "#3a2a09", "#302054"]:
        assert bad not in t, f"bright value remains: {bad}"
    ids = re.findall(r'id="([^"]+)"', t)
    assert len(ids) == 24 and len(set(ids)) == 24, f"id count changed: {len(ids)} ids, {len(set(ids))} unique"
    # No font-size rule below 17px remains (root 16px; rem -> px).
    for m in re.finditer(r"font-size:\s*(?:clamp\()?([0-9.]+)(rem|px)", t):
        v, u = float(m.group(1)), m.group(2)
        px = v * 16 if u == "rem" else v
        assert px >= 17 - 1e-9, f"sub-17px font-size remains: {m.group(0)}"
    # No linear-gradient left off 135 deg (conic/radial excepted).
    for m in re.finditer(r"linear-gradient\((\d+)deg", t):
        assert m.group(1) == "135", f"gradient off 135deg: {m.group(0)}"

    new_raw = t.encode("utf-8")
    open(SRC, "wb").write(new_raw)
    print(f"fixed-entry.html: {orig_len} chars -> {len(t)} chars, {len(new_raw)} B")
    print(f"sha256: {sha(new_raw)}")
    return t


def build_icons_and_manifest(text):
    """Fix 4 (assets): the crystal N, harvested from the page's own
    embedded 512x512 JPEG (the seal's .logo-hero / header brand-mark,
    sha f9c2290e...), rendered as the three PWA icons; the manifest
    re-valued to the deep palette (theme_color only — everything
    else byte-identical to the live manifest)."""
    from PIL import Image
    import io

    jpegs = re.findall(r"data:image/jpeg;base64,([A-Za-z0-9+/=]+)", text)
    assert len(jpegs) == 3, f"expected 3 embedded JPEGs, got {len(jpegs)}"
    raws = [base64.b64decode(j) for j in jpegs]
    assert sha(raws[1]) == sha(raws[2]), "seal/brand JPEGs differ"
    assert sha(raws[1]).startswith("f9c2290e"), "crystal N sha mismatch"
    src = Image.open(io.BytesIO(raws[1])).convert("RGB")
    assert src.size == (512, 512), f"crystal N size {src.size}"
    icons_dir = os.path.join(HERE, "icons")
    os.makedirs(icons_dir, exist_ok=True)
    for name, size in [("icon-512.png", 512), ("icon-192.png", 192),
                       ("apple-touch-icon.png", 180)]:
        img = src if size == 512 else src.resize((size, size), Image.LANCZOS)
        p = os.path.join(icons_dir, name)
        img.save(p, format="PNG")
        print(f"icons/{name}: {size}x{size}, {os.path.getsize(p)} B, sha256 {sha(open(p,'rb').read())[:16]}...")

    manifest = {
        "name": "NayaNET — Intelligent Sovereign Network",
        "short_name": "NayaNET",
        "description": "Humans and AI, becoming more intelligent together.",
        "start_url": "/index.html",
        "display": "standalone",
        "background_color": "#010103",
        "theme_color": "#8e24aa",
        "orientation": "portrait-primary",
        "icons": [
            {"src": "icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any maskable"},
            {"src": "icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any maskable"},
        ],
    }
    mp = os.path.join(HERE, "manifest.webmanifest")
    with open(mp, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
        f.write("\n")
    print(f"manifest.webmanifest: {os.path.getsize(mp)} B, theme_color #8e24aa")


if __name__ == "__main__":
    text = main()
    build_icons_and_manifest(text)
    print("APPLY-FIX DONE")
