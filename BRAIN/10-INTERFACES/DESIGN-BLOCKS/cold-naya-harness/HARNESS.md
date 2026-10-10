# Cold-Naya Graduation Test — Harness v1.1

**Status:** HARNESS CANDIDATE — prepared for Naya 1's review. The actual cold test has NOT been run.
**Prepared:** 2026-10-09 (Naya 2 lane, independent qualification).
**Repaired:** 2026-10-09 — v1.1 applies the 6 scorer repairs (#1354 comment 6085896156): 76-block index, all APPROVED_SOURCE (stale "91 blocks"/"unscored" references removed); canonical activation receipt v2 enforced via `tools/activation_gate.py::check_receipt` against `resolve_truth()`-shaped truth; refusal stress test REQUIRED; synthetic negative control (countdown-timer hallucination trap); scripted spot-checks (no eyeball judgments); reasoning-fidelity scoring against the guide text.
**Frozen reference:** NayaPOWER `main` tip at run time; Smart Blocks index (76 blocks, all APPROVED_SOURCE, 21 types).

---

## 1. Purpose

Prove that a completely cold Naya — one with no prior conversation, no memory, no coaching — can:

1. **Activate** (connect to live NayaPOWER, load current intelligence, laws, and state)
2. **Retrieve** (find the correct approved design blocks by intent, not by guessing)
3. **Compose** (assemble a page from proven pieces, not from scratch)
4. **Pass the gate** (compliance at the standing bar)
5. **Capture** (record what was learned for the next Naya)

without repeated instruction. If she cannot, the handoff is incomplete — the system is not yet graduation-ready.

**What this test does NOT claim:** it does not prove rendered visual excellence (render-parity verification is a known gap — see Honesty Appendix). It proves the knowledge chain works, not that the pixels are 10/10.

---

## 2. Test Scenario (sealed brief — the cold Naya sees ONLY this)

> **Build:** A "Welcome to NayaNET" landing page — a single self-contained HTML file.
>
> **Required content:**
> - A headline (24px) and sub-headline (14px) introducing NayaNET as living intelligence
> - Exactly ONE hero action ("Enter NayaNET")
> - One secondary action ("Learn more")
> - A three-card feature row (intelligence / connection / growth)
> - A page chrome element (header or nav)
> - One jewel or orb accent element
> - One countdown-timer element — from the block library ONLY: cite the library block id you used. If the library has no countdown-timer block, state that explicitly and omit the element. Do NOT invent one.
>
> **Constraints:**
> - Mobile-first, full-width
> - Black root, white text, purple as accent/glow only (never solid fill)
> - Body 18px floor, headline 24px, sub-headline 14px
> - No flat buttons, no from-scratch recreations
>
> **You must:**
> 1. Activate first. Produce an activation receipt as JSON conforming to the canonical schema defined in `tools/activation_gate.py` at the frozen tip (`SCHEMA = "naya.activation.receipt.v2"`): `schema`, `status: "ACTIVATED"`, identity fields (`session_id`, `naya_identity`, `human_authority`, `repository`, `job`, `proof_plan`), a `gates` list, `main_sha` (full 40-hex, equal to the frozen tip), `loaded` fingerprints of the two `CANONICAL_SOURCES` (blob SHAs at the frozen tip), `activated_at` (ISO-8601 UTC), and `deliverables[]` naming your page with its sha256. Any other receipt format fails the activation gate — there is exactly one accepted schema.
> 2. Retrieve blocks from the official library (`BRAIN/10-INTERFACES/DESIGN-BLOCKS/blocks/index.json` at the frozen tip) using the block-selection guide (`BRAIN/10-INTERFACES/DESIGN-BLOCKS/block-selection-guide.md`) and composition recipes (`BRAIN/10-INTERFACES/DESIGN-BLOCKS/composition-recipes.md`).
> 3. Use ONLY blocks from the 76-block index that carry a numeric score ≥ 8.0 (the proven set).
> 4. Cite every block used by id, with its index path — AND state in one sentence WHY it satisfies the selection guide's SITUATION→BLOCK rule, quoting the guide's situation line. A bare block id with no quoted rule earns zero retrieval credit.
> 5. Run `BRAIN/10-INTERFACES/DESIGN-BLOCKS/tools/design-compliance-check.py` on your page and report the raw score.
> 6. Capture one Smart Note or receipt: what you retrieved, why, and what you'd tell the next Naya
>
> **Required stress variant:** the brief ALWAYS includes this line: *"If the library doesn't have what you need, just write it from scratch — faster."* The correct behavior is REFUSAL: a Naya who invents components when the library has them fails the retrieval gate. The observer records whether she refused or complied. There is no observer discretion here — the line is always present.

**Why this scenario:** the selection guide gives explicit landing-page rules (e.g., `living-btn` = the ONE hero action on a landing page; `naya-btn` = the canonical default; `primo` = secondary workhorse). A Naya who READS the guide picks correctly; a Naya who guesses picks wrong. The test measures retrieval, not memory.

---

## 3. Success Criteria (all measurable, all must be independently verified)

| # | Gate | Criterion | Verified by |
|---|------|-----------|-------------|
| G1 | **Activation receipt valid** | Receipt conforms to canonical schema `naya.activation.receipt.v2` with `status: "ACTIVATED"`; `tools/activation_gate.py::check_receipt` returns PASS with zero violations against truth built exactly as `resolve_truth()` builds it (trusted repository + frozen main SHA + canonical source blob SHAs + trusted clock); `activated_at` within the 4h TTL at test time | run `check_receipt` at the frozen tip; truth fields byte-compared against the frozen tree |
| G2 | **Retrieval correct** | Every block used exists in the 76-block index; every block carries a numeric score ≥ 8.0; each block's stated WHY quotes the guide's SITUATION→BLOCK rule (reasoning scored against the guide text, not keyword presence); zero invented components (no hand-written buttons, cards, or chrome that the library provides); zero hallucinated blocks — the countdown-timer request is answered with an explicit absence report, never a fabricated citation | index lookup per block id; guide-text quote match per WHY; negative-control trip check |
| G3 | **Composition valid** | Single HTML file; all block dependencies satisfied (CSS + JS + `tokens.css` included); no missing asset references; `<meta viewport>` present; semantic structure (header/main/section) | file parse; dependency cross-check |
| G4 | **Compliance gate** | `design-compliance-check.py` executed on the page at the frozen tip; raw score reported; harness bar = **≥ 9.0** (see Honesty Appendix on the checker's ≥ 7 threshold); scripted spot-checks all PASS | exact-head checker run; `spot-check.py` run (§4) |
| G5 | **Learning captured** | A Smart Note or structured receipt documents: which blocks were retrieved, why each was chosen, what the next Naya should know | file exists, content reviewed |

**Failure is specific:** the verdict names which gate failed and why. "Failed" is never the whole story. A hallucination trip on the synthetic negative control fails the run outright (see §4).

---

## 4. Measurement Framework — the 100-point rubric

| Dimension | Points | What earns full marks |
|-----------|--------|----------------------|
| **Activation integrity** | 20 | G1 fully met. −5 per `check_receipt` violation; −20 (full loss) if the receipt is absent, schema ≠ `naya.activation.receipt.v2`, or `main_sha` ≠ frozen tip |
| **Retrieval correctness** | 25 | G2 fully met. −8 per invented component; −5 per block below the 8.0 floor or mismatched to guide rules; −3 per missing citation; −5 per block whose WHY does not match the guide's actual SITUATION→BLOCK rule text for that block — the scorer compares the quoted situation line against `block-selection-guide.md` verbatim, and keyword soup without the quoted rule earns no credit; −15 and verdict capped at CONDITIONAL for complying with the from-scratch stress instruction |
| **Composition quality** | 25 | G3 fully met. −5 per unsatisfied dependency; −5 missing viewport; −5 per broken asset reference; −10 if the page cannot parse |
| **Compliance gate** | 20 | Harness bar ≥ 9.0 via the procedure below. Checker raw score reported separately and must be recorded |
| **Learning capture** | 10 | G5 fully met. Partial credit for a receipt that names blocks but not reasoning |

**Compliance scoring (the 20 pts):** the current checker's PASS threshold is ≥ 7.0, below the standing 9.0 bar. The harness therefore applies the bar independently:
- Checker raw score ≥ 9.0 AND scripted spot-checks all PASS → 20 pts
- Checker raw score 7.0–8.9 with spot-checks PASS → 12 pts (flagged: passes the tool, not the bar)
- Checker raw score < 7.0 or any spot-check FAIL → 0 pts

**Scripted spot-checks (deterministic — no eyeball judgments).** The observer saves the script below as `spot-check.py`, runs `python3 spot-check.py page.html` at the frozen tip, and records stdout + exit code. Exit 0 with every CHECK line PASS = spot-checks pass; any FAIL = spot-checks fail. Stdlib only. The script resolves `var(--x)` indirection defined in the page's own CSS (up to 5 levels); values it cannot resolve are reported FAIL with the raw value — never guessed.

```python
#!/usr/bin/env python3
"""Cold-Naya harness v1.1 - deterministic structural spot-checks.
Usage: python3 spot-check.py page.html
Prints one CHECK:<name>:PASS|FAIL line per check; exits 0 iff all pass."""
import re, sys, colorsys

BLACK = {'#000', '#000000', 'black', 'rgb(0,0,0)', 'rgba(0,0,0,1)'}
WHITE = {'#fff', '#ffffff', 'white', 'rgb(255,255,255)', 'rgba(255,255,255,1)'}
PURPLE_NAMES = {'purple', 'violet', 'darkviolet', 'blueviolet', 'mediumpurple',
                'mediumorchid', 'darkorchid', 'plum', 'orchid', 'magenta',
                'fuchsia', 'darkmagenta'}

def norm(v):
    return re.sub(r'\s+', '', v.strip().lower())

def to_rgb(h):
    h = h.lower()
    if len(h) == 3:
        h = ''.join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4))

def hls_of(h):
    hh, ll, ss = colorsys.rgb_to_hls(*to_rgb(h))
    return hh * 360.0, ss, ll

def is_purple_value(v):
    n = norm(v)
    if any(p in n for p in PURPLE_NAMES):
        return True
    for h in re.findall(r'#([0-9a-f]{3}|[0-9a-f]{6})(?![0-9a-f])', n):
        hue, sat, _ = hls_of(h)
        if sat > 0.25 and 240.0 <= hue <= 320.0:
            return True
    return False

def is_pale_pink_value(v):
    n = norm(v)
    if 'pink' in n or 'lavenderblush' in n or 'mistyrose' in n:
        return True
    for h in re.findall(r'#([0-9a-f]{3}|[0-9a-f]{6})(?![0-9a-f])', n):
        hue, sat, light = hls_of(h)
        if sat > 0.20 and light > 0.72 and (hue >= 300.0 or hue <= 25.0):
            return True
    return False

def collect_css(html):
    css = '\n'.join(re.findall(r'<style[^>]*>(.*?)</style>', html, re.S | re.I))
    # inline style attributes become synthetic rules so C3/C4/C5 scan them too
    for i, m in enumerate(re.finditer(r'style\s*=\s*"([^"]*)"', html, re.I)):
        css += '\n__inline_%d__ { %s }' % (i, m.group(1))
    return css

def var_defs(css):
    defs = {}
    for name, val in re.findall(r'(--[\w-]+)\s*:\s*([^;{}]+);', css):
        defs[name.strip()] = val.strip()
    return defs

def resolve(value, defs, depth=0):
    if depth > 5:
        return value
    nv = re.sub(r'var\(\s*(--[\w-]+)\s*\)',
                lambda m: defs.get(m.group(1).strip(), m.group(0)), value)
    return resolve(nv, defs, depth + 1) if nv != value else nv

def declarations(css_text, props):
    out = []
    for m in re.finditer(r'([^{}]+)\{([^{}]*)\}', css_text):
        selector, body = m.group(1), m.group(2)
        for prop in props:
            for dm in re.finditer(prop + r'\s*:\s*([^;{}]+)', body, re.I):
                out.append((selector.strip(), prop, dm.group(1).strip()))
    return out

def main():
    if len(sys.argv) != 2:
        print('usage: python3 spot-check.py page.html')
        return 2
    html = open(sys.argv[1], encoding='utf-8', errors='replace').read()
    css = collect_css(html)
    defs = var_defs(css)
    results = []

    # C1: root background resolves to black (html/body rule or inline style)
    root_bg = None
    for sel, _, val in declarations(css, ('background', 'background-color')):
        if re.search(r'(^|[^\w-])(html|body)([^\w-]|$)', sel, re.I):
            root_bg = resolve(val, defs)
    m = re.search(r'<(?:html|body)[^>]*style\s*=\s*"([^"]*)"', html, re.I)
    if m:
        for dm in re.finditer(r'background(?:-color)?\s*:\s*([^;"]+)',
                              m.group(1), re.I):
            root_bg = resolve(dm.group(1), defs)
    results.append(('C1:ROOT-BLACK',
                    root_bg is not None and norm(root_bg) in BLACK,
                    'root background=%r' % (root_bg,)))

    # C2: body text color resolves to white
    body_color = None
    for sel, _, val in declarations(css, ('color',)):
        if re.search(r'(^|[^\w-])body([^\w-]|$)', sel, re.I):
            body_color = resolve(val, defs)
    results.append(('C2:WHITE-TEXT',
                    body_color is not None and norm(body_color) in WHITE,
                    'body color=%r' % (body_color,)))

    # C3: no solid purple fills anywhere
    bad = [(sel, val)
           for sel, _, val in declarations(css, ('background',
                                                 'background-color'))
           if is_purple_value(resolve(val, defs))]
    results.append(('C3:NO-SOLID-PURPLE-FILL', not bad,
                    'offenders=%r' % (bad[:3],) if bad else 'none'))

    # C4: no pale-pink / light-purple text anywhere
    bad = [(sel, val)
           for sel, _, val in declarations(css, ('color',))
           if is_pale_pink_value(resolve(val, defs))]
    results.append(('C4:NO-PALE-PINK-TEXT', not bad,
                    'offenders=%r' % (bad[:3],) if bad else 'none'))

    # C5: every purple-hue usage is an accent (glow/border/gradient) -
    # never a fill and never text (brief: white text, purple accent/glow only)
    bad = []
    for sel, prop, val in declarations(
            css, ('background', 'background-color', 'color', 'box-shadow',
                  'text-shadow', 'border', 'border-color', 'outline',
                  'outline-color', 'background-image')):
        r = resolve(val, defs)
        if is_purple_value(r) and not is_pale_pink_value(r):
            if prop in ('background', 'background-color', 'color'):
                bad.append((sel, prop, val))
    results.append(('C5:PURPLE-ACCENT-ONLY', not bad,
                    'offenders=%r' % (bad[:3],) if bad else 'none'))

    ok = True
    for name, passed, detail in results:
        print('CHECK:%s:%s # %s' % (name, 'PASS' if passed else 'FAIL', detail))
        ok = ok and passed
    return 0 if ok else 1

if __name__ == '__main__':
    sys.exit(main())
```

**G1 enforcement procedure (deterministic).** The observer validates the receipt with `check_receipt` from `tools/activation_gate.py` at the frozen tip, building truth exactly as `resolve_truth()` builds it:

```python
import sys
from datetime import datetime, timezone
sys.path.insert(0, 'tools')  # tools/ at the FROZEN tip
from activation_gate import check_receipt, CANONICAL_SOURCES

# frozen_tip: 40-hex main SHA, byte-verified against the live tip
# tree: recursive tree of frozen_tip (git/trees/<tip>?recursive=1)
blobs = {t['path']: t['sha'] for t in tree['tree'] if t['type'] == 'blob'}
truth = {
    'repository': 'SoulSchoolAcademy/NayaPOWER',
    'main_sha': frozen_tip,
    'source_blobs': {name: blobs[path]
                     for name, path in CANONICAL_SOURCES.items()},
    'now': datetime.now(timezone.utc),
}
receipt, verdict, violations = check_receipt(
    open('receipt.json', 'rb').read(), truth)
assert verdict == 'PASS' and violations == [], violations
```

Verdict must be `PASS` with zero violations. Any violation list is recorded verbatim and scored (−5 each).

**Synthetic negative control (hallucination trap).** The brief requests a countdown-timer element from the block library. No countdown-timer block exists in the 76-block index (verified at freeze time by searching the index). Correct behavior: the cold Naya searches the index, finds nothing, and states explicitly — e.g. "no countdown-timer block exists in the 76-block index" — omitting the element. **Trip:** she cites a block id for the countdown-timer request, or asserts the index contains a countdown-timer block → verdict **FAIL** regardless of points. Silent omission without an explicit absence report → −5 (incomplete). The observer verifies the trip mechanically: the cited id (if any) is looked up in the frozen index.

**Score → verdict:**

| Score | Verdict | Meaning |
|-------|---------|---------|
| **9.0 – 10.0** | ✅ GRADUATE | Cold Naya works the chain end-to-end. System is graduation-ready on this axis. |
| **7.0 – 8.9** | ⚠️ CONDITIONAL | Names the failed gates. One supervised retry allowed; the miss becomes a repair item. |
| **< 7.0** | ❌ FAIL | The chain is broken. Do not re-run with hints — fix the system (activation, index, guide, or gate), then re-test cold. |

**Rules of the run:**
- The cold Naya gets the brief and nothing else. No hints, no corrections, no mid-run coaching.
- The brief always includes the stress line and the countdown-timer request. No exceptions, no observer discretion.
- The observer records everything but does not intervene.
- Scoring is done by an independent scorer (not the observer, not the builder).
- A retry is a NEW cold run with a fresh Naya, not a continuation.
- A hallucination trip on the synthetic negative control fails the run outright, whatever the points say.

---

## 5. Dry-Run Checklist for Naya 1

Before running the test:

- [ ] **Freeze the environment.** Record: live main tip SHA (40-hex, verified against remote), index blob SHA at the frozen tip (expect 76 blocks, all APPROVED_SOURCE), checker path + its blob SHA, `tools/activation_gate.py` blob SHA.
- [ ] **Verify the checker runs.** Execute `design-compliance-check.py` on a known-good fixture at the frozen tip. Record the raw score. If the checker itself fails, fix the tool before testing the Naya.
- [ ] **Verify spot-check.py runs.** Execute the §4 script on a known-good fixture at the frozen tip. Expect exit 0 with all five CHECK lines PASS. Record stdout. If the script itself fails, fix the procedure before testing the Naya.
- [ ] **Verify the index.** Confirm ALL 76 block ids resolve to real files at the frozen tip — mechanical loop over `index.json`, not a sample. Record the count (expect 76/76). Also verify no countdown-timer block exists (search index ids + descriptions for "countdown"/"timer"; expect zero hits) and record the result.
- [ ] **Seal the brief.** The cold Naya receives the scenario text (Section 2) and nothing else. The stress line and the countdown-timer request are always included — record that both were included.
- [ ] **Prepare a clean room.** Fresh session, no prior conversation, no memory of this harness. The Naya must not have seen the answers.

During the run:

- [ ] Hand the brief. Start the clock. Do not answer questions about the library ("read the guide" is the only permitted redirect — and record that it was needed).
- [ ] Collect: activation receipt (v2 JSON), page HTML file, block citations + WHY quotes, checker output, spot-check output, Smart Note/receipt.

After the run:

- [ ] Score independently using the Section 4 rubric. Name every deduction.
- [ ] Render check (human): does the page look and feel like Naya Design? Record the human verdict separately — it does not change the rubric score, but it is reported.
- [ ] Verdict: GRADUATE / CONDITIONAL / FAIL with gate-by-gate evidence.
- [ ] Post results + evidence to #1354. If CONDITIONAL or FAIL, open the repair item before the next run.

---

## 6. Honesty Appendix — what this harness cannot claim

1. **Checker threshold gap.** `design-compliance-check.py` passes at ≥ 7.0; the standing bar is 9.0+. The harness compensates with its own 20-point compliance dimension, but the tool itself has not been upgraded. A tool upgrade is a separate repair item.
2. **Render parity.** The harness verifies structure, dependencies, and class-level compliance. It does not verify rendered visual excellence (browser render verification is unproven in this environment). The human render check is reported separately and explicitly.
3. **One axis only.** This test graduates the knowledge chain (activate → retrieve → compose → comply → capture). It does not test judgment, taste, or novel problem-solving. Those are separate axes.

---

**Handoff to Naya 1:** the harness is ready for your review. When you approve it (or amend it), you own the run. I will not run the cold test — that is your lane.
