#!/usr/bin/env python3
"""Compile PROTOCOL.md into the machine spec (protocol_spec.json).

The protocol is law in prose (PROTOCOL.md, ratified by Shawn Vibert).
This generator compiles that prose into a machine-readable spec so code
can check the surfaces agree — it parses, never hand-duplicates. Any
hand-edited or stale spec fails protocol_version_sync because that check
re-runs build_spec() and deep-compares.

Parsed, never duplicated:
  title (first '# ' line), ratified date + ratified_by, one_sentence
  (first non-empty line after '## THE ONE-SENTENCE PROTOCOL'), the three
  moments (bold leads in THE THREE MOMENTS), phases (name with trailing
  parenthetical stripped; steps assigned by document position), steps
  (n / phase / title / sha256 of the step's raw text slice from its
  header line start to the next step header or the next '## ' header),
  standing_laws (bold segments in STANDING LAWS, trailing ':' and '.'
  stripped), declaration canonical refs (from Step 0's Canonical
  parenthetical, in order of appearance), the scorecard loop markers
  in Step 15, and the value-verdict markers in FINAL ACCEPTANCE.

Fail closed: build_spec raises ValueError (main exits 2) if steps != 18
or phases != 5 or standing laws < 10 or any required marker is missing.

No timestamps anywhere — regeneration must be byte-identical.

Usage:
    python3 kernel/protocol/compile_protocol_spec.py [--root <repo>] \
        [--out <path>]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

STEP_RE = re.compile(r"^\*\*(\d+)\.\s+(.+?)\.\*\*", re.M)
PHASE_RE = re.compile(r"^## PHASE (\d+) \u2014 (.+?)\s*$", re.M)
H2_RE = re.compile(r"^## ", re.M)
RATIFIED_RE = re.compile(r"Ratified and amended by (.+?), (\d{4}-\d{2}-\d{2})")
REF_RE = re.compile(r"(SN-\d{4}|IB-\d{6})")
MOMENT_RE = re.compile(r"\*\*Moment \d+ \u2014 (.+?)\*\*")
BOLD_RE = re.compile(r"\*\*(.+?)\*\*", re.S)


def _fail(message: str) -> ValueError:
    return ValueError(message)


def _section(text: str, header: str) -> str:
    """Return the slice from a '## <header>' line to the next '## ' header."""
    start = text.find(f"## {header}")
    if start == -1:
        raise _fail(f"missing section: ## {header}")
    nxt = text.find("\n## ", start + 1)
    return text[start:] if nxt == -1 else text[start:nxt]


def build_spec(root) -> dict:
    root = Path(root).resolve()
    protocol_path = root / "PROTOCOL.md"
    if not protocol_path.is_file():
        raise _fail(f"PROTOCOL.md not found under root {root}")
    raw = protocol_path.read_bytes()
    text = raw.decode("utf-8")
    sha = hashlib.sha256(raw).hexdigest()

    # Title: first '# ' line.
    title = None
    for line in text.splitlines():
        if line.startswith("# "):
            title = line[2:].strip()
            break
    if not title:
        raise _fail("missing title: no '# ' line in PROTOCOL.md")

    # Ratified date / ratified_by.
    m = RATIFIED_RE.search(text)
    if not m:
        raise _fail("missing ratified marker: "
                    "'Ratified and amended by Shawn Vibert, (date)' not found")
    ratified_by = m.group(1).strip()
    version = m.group(2).strip()

    # One-sentence protocol: first non-empty line after the section header.
    one_section = _section(text, "THE ONE-SENTENCE PROTOCOL")
    one_sentence = None
    for line in one_section.splitlines()[1:]:
        if line.strip():
            one_sentence = line.strip()
            break
    if not one_sentence:
        raise _fail("missing one-sentence protocol text")

    # Moments: bold leads in THE THREE MOMENTS.
    moments_section = _section(text, "THE THREE MOMENTS")
    moments = [x.strip() for x in MOMENT_RE.findall(moments_section)]
    if moments != ["Activation", "Shift start", "Every consequential action"]:
        raise _fail(f"THE THREE MOMENTS markers missing or unexpected: {moments!r}")

    # Phases.
    phase_matches = list(PHASE_RE.finditer(text))
    phases = []
    phase_positions = []  # (pos, name)
    for pm in phase_matches:
        raw_name = pm.group(2).strip()
        name = re.sub(r"\s*\(.*\)\s*$", "", raw_name).strip()
        phases.append({"n": int(pm.group(1)), "name": name})
        phase_positions.append((pm.start(), name))
    if len(phases) != 5:
        raise _fail(f"phases != 5 (found {len(phases)})")

    # Steps.
    step_matches = list(STEP_RE.finditer(text))
    if len(step_matches) != 18:
        raise _fail(f"steps != 18 (found {len(step_matches)})")
    h2_positions = [hm.start() for hm in H2_RE.finditer(text)]
    steps = []
    step_texts: dict[int, str] = {}
    for i, sm in enumerate(step_matches):
        n = int(sm.group(1))
        start = sm.start()
        candidates = []
        if i + 1 < len(step_matches):
            candidates.append(step_matches[i + 1].start())
        later_h2 = [p for p in h2_positions if p > start]
        if later_h2:
            candidates.append(min(later_h2))
        end = min(candidates) if candidates else len(text)
        raw_slice = text[start:end]
        step_texts[n] = raw_slice
        phase_name = None
        for pos, pname in phase_positions:
            if pos < start:
                phase_name = pname
            else:
                break
        if phase_name is None:
            raise _fail(f"step {n} appears before any phase header")
        steps.append({
            "n": n,
            "phase": phase_name,
            "title": sm.group(2).strip(),
            "sha256": hashlib.sha256(raw_slice.encode("utf-8")).hexdigest(),
        })
    steps.sort(key=lambda s: s["n"])

    # Standing laws: bold segments in the STANDING LAWS section.
    laws_section = _section(text, "STANDING LAWS")
    standing_laws = []
    for bold in BOLD_RE.findall(laws_section):
        cleaned = bold.strip().rstrip(":").rstrip(".").strip()
        # rstrip above removes a trailing ':' or '.' but not both in
        # sequence; normalise by repeated stripping of those chars.
        cleaned = bold.strip().rstrip(":.").strip()
        if cleaned:
            standing_laws.append(cleaned)
    if len(standing_laws) < 10:
        raise _fail(f"standing laws < 10 (found {len(standing_laws)})")

    # Declaration: canonical refs from Step 0.
    step0 = step_texts.get(0, "")
    if not step0:
        raise _fail("Step 0 text missing")
    canonical_match = re.search(r"\(Canonical:\s*(.+?)\)", step0, re.S)
    canonical_source = canonical_match.group(1) if canonical_match else step0
    canonical_refs = REF_RE.findall(canonical_source)
    if not canonical_refs:
        raise _fail("Step 0 canonical refs missing (no SN-/IB- refs found)")
    declaration = {"step": 0, "canonical_refs": canonical_refs}

    # Scorecard loop: markers extracted from Step 15 (fail if absent).
    step15 = step_texts.get(15, "")
    if not step15:
        raise _fail("Step 15 text missing")
    if "Three rounds" not in step15:
        raise _fail("Step 15 marker missing: 'Three rounds'")
    rounds = 3  # extracted marker is the literal 'Three rounds'
    bar_m = re.search(r"The bar is (\d+(?:\.\d+)?)\+", step15)
    if not bar_m:
        raise _fail("Step 15 marker missing: 'The bar is 9+'")
    bar = float(bar_m.group(1))
    fixes_m = re.search(r"(\d+) most valuable fixes", step15)
    if not fixes_m:
        raise _fail("Step 15 marker missing: '10 most valuable fixes'")
    fixes_max = int(fixes_m.group(1))
    if "does not ship" not in step15:
        raise _fail("Step 15 marker missing: 'does not ship'")
    if "**compressed**" not in step15 or "**in full**" not in step15:
        raise _fail("Step 15 marker missing: weights 'compressed' / 'in full'")
    scorecard_loop = {
        "step": 15,
        "rounds": rounds,
        "bar": bar,
        "fixes_list_max": fixes_max,
        "weights": ["compressed", "full"],
        "below_bar_after_rounds": "does_not_ship",
    }

    # Value verdict: markers in FINAL ACCEPTANCE (fail if absent).
    final_section = _section(text, "FINAL ACCEPTANCE")
    if "The Value Verdict, first" not in final_section:
        raise _fail("FINAL ACCEPTANCE marker missing: 'The Value Verdict, first'")
    if "Name who benefits" not in final_section:
        raise _fail("FINAL ACCEPTANCE marker missing: 'Name who benefits'")
    value_verdict = {
        "required": True,
        "position": "first",
        "must_name_beneficiary": True,
    }

    return {
        "schema": "naya.protocol.spec.v1",
        "document": title,
        "source": {"path": "PROTOCOL.md", "sha256": sha, "bytes": len(raw)},
        "version": version,
        "ratified_by": ratified_by,
        "one_sentence": one_sentence,
        "moments": moments,
        "phases": phases,
        "steps": steps,
        "standing_laws": standing_laws,
        "declaration": declaration,
        "scorecard_loop": scorecard_loop,
        "value_verdict": value_verdict,
        "generator": "kernel/protocol/compile_protocol_spec.py",
    }


def main() -> int:
    default_root = Path(__file__).resolve().parents[2]
    parser = argparse.ArgumentParser(
        description="Compile PROTOCOL.md into protocol_spec.json")
    parser.add_argument("--root", default=str(default_root),
                        help="Repo root (default: repo root, parents[2] of "
                             "this file / parents[1] of kernel/protocol/)")
    parser.add_argument("--out", default=None,
                        help="Output path (default: "
                             "<root>/kernel/protocol/protocol_spec.json)")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    out = Path(args.out).resolve() if args.out else (
        root / "kernel" / "protocol" / "protocol_spec.json")
    try:
        spec = build_spec(root)
    except Exception as exc:
        print(f"FAIL CLOSED: {exc}", file=sys.stderr)
        return 2
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        json.dumps(spec, sort_keys=True, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8")
    print(f"wrote {out} (version {spec['version']}, "
          f"sha256 {spec['source']['sha256']})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
