#!/usr/bin/env python3
"""Ritual Bounce Mechanism — tool-assisted reviewer checklist for Operating Code V2 rituals.

STATUS: This is a REVIEWER AID, not a hard gate. Rituals require human judgment;
this tool makes ritual compliance easy to verify and hard to skip by checking
the MECHANICAL parts of each ritual (presence of a self-score, presence of two
update sections, presence of the Law of One test string, ...) and reporting
FOUND / MISSING / N/A with evidence snippets. A human reviewer makes the call.
Exit code is ALWAYS 0 — the tool never auto-rejects.

Usage:
    python3 tools/ritual_checklist.py --file report.md [--json]
    python3 tools/ritual_checklist.py --text "..."   [--json]
    python3 tools/ritual_checklist.py --pr 2091      [--json]   # fetches PR body via gh-api

The seven rituals (from the Operating Code V2 audit — ritual provisions are
27% of the law; "reviewer rejects work missing ritual proof. Make it a norm,
then a tool."):

  1. DECISION      — agent names each score dimension; states "I ran the
                     calculator" with scoring shown.
  2. COMMUNICATION— two-part update present (technical + plain English);
                     first paragraph has zero PR/issue numbers.
  3. EXECUTION     — work product states self-score, lists holes found,
                     describes fills; describes what was SEEN rendered.
  4. LEARNING      — learning claims include behavioral proof (novel problem,
                     blind scored) — not just "I saved it."
  5. AUTHORITY     — agent states misalignment plainly before fixing
                     Shawn's mistakes.
  6. CONSTITUTION  — mandatory Law of One test stated before significant
                     actions; human value named ("what human is better off?");
                     close calls name which option serves the human.
  7. DESIGN        — designer states how work serves "one living
                     intelligence"; every visual effect justified; what
                     improved vs preserved.

Checkable (mechanical) vs judgment-only — per ritual:
  - DECISION: mechanical = dimensions named + scores shown + calculator
    stated. Judgment = are the dimensions the RIGHT ones; is the scoring honest.
  - COMMUNICATION: mechanical = two sections present + first paragraph has no
    #NNN refs. Judgment = is the plain-English part actually plain English.
  - EXECUTION: mechanical = self-score / holes / fills / seen-rendered strings
    present. Judgment = are the holes real; was the render truly verified.
  - LEARNING: mechanical = behavioral-proof markers (novel problem, blind,
    scored) present alongside the claim. Judgment = was the problem truly
    novel; was the scoring truly blind.
  - AUTHORITY: mechanical = plain misalignment statement present where a
    Shawn mistake was corrected. Judgment = tone, accuracy of the claim.
  - CONSTITUTION: mechanical = Law-of-One test string + named human value +
    close-call naming present. Judgment = is the stated value real; was the
    test genuinely applied.
  - DESIGN: mechanical = "one living intelligence" + effect justifications +
    improved-vs-preserved present. Judgment = craft, taste, coherence.

A check that does not apply to the product (no learning claims, no Shawn
correction, no design work, not an update) reports N/A — not FOUND, not
MISSING — so the checklist never invents obligations.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
GH_API = Path.home() / "workspace" / "naya" / "bin" / "gh-api"
REPO_SLUG = "SoulSchoolAcademy/NayaPOWER"

SNIPPET_MAX = 140


# ---------------------------------------------------------------- helpers

def _first_match_line(text: str, pattern: re.Pattern) -> str | None:
    """First matching region of text, expanded to its enclosing lines.

    Matches may span a line break (e.g. "serves the\\nhuman"); the snippet
    shows the full enclosing line(s) so the evidence stays readable.
    """
    m = pattern.search(text)
    if not m:
        return None
    start = text.rfind("\n", 0, m.start()) + 1
    end = text.find("\n", m.end())
    if end == -1:
        end = len(text)
    snippet = " ".join(text[start:end].split())
    if len(snippet) > SNIPPET_MAX:
        snippet = snippet[: SNIPPET_MAX - 3].rstrip() + "..."
    return snippet


def _snip(line: str | None) -> str:
    return line if line else "(no match)"


@dataclass
class Check:
    """One mechanical check inside a ritual."""
    check_id: str
    ritual: str          # ritual key, e.g. "DECISION"
    description: str     # what the ritual requires
    status: str          # FOUND | MISSING | N/A
    evidence: str        # snippet or reason
    applicable_note: str = ""


@dataclass
class RitualResult:
    key: str
    name: str
    checks: list[Check] = field(default_factory=list)

    def verdict(self) -> str:
        """Ritual-level rollup: N/A if no check applied, else FOUND/MISSING counts."""
        statuses = [c.status for c in self.checks]
        if all(s == "N/A" for s in statuses):
            return "N/A"
        if any(s == "MISSING" for s in statuses):
            return "FLAG"
        return "PASS"


# ---------------------------------------------------------------- rituals

def check_decision(text: str) -> RitualResult:
    r = RitualResult("DECISION", "1. Decision — scorecard ritual")
    dim_pat = re.compile(r"\bdimensions?\b|\bcriteria\b|\bcriterion\b", re.I)
    score_pat = re.compile(r"\b\d{1,2}(?:\.\d)?\s*/\s*10\b|\bscore[d]?\s*[:=]?\s*\d", re.I)
    dims = _first_match_line(text, dim_pat)
    scores = _first_match_line(text, score_pat)
    found = bool(dims and scores)
    r.checks.append(Check(
        "decision.dimensions", "DECISION",
        "Agent names each score dimension, with scoring shown.",
        "FOUND" if found else "MISSING",
        f"dimension: {_snip(dims)} | score: {_snip(scores)}",
    ))
    calc_pat = re.compile(r"\bran the calculator\b", re.I)
    calc = _first_match_line(text, calc_pat)
    if calc is None:
        # looser fallback: "calculator" with scoring nearby (same paragraph-ish window)
        m = re.search(r"\bcalculator\b(.{0,120}?)\bscor", text, re.I | re.S)
        if m:
            calc = _snip((m.group(0).splitlines() or [None])[0]) or "calculator + scoring nearby"
    r.checks.append(Check(
        "decision.calculator", "DECISION",
        'Agent states "I ran the calculator" (scorecard math run).',
        "FOUND" if calc else "MISSING",
        _snip(calc),
    ))
    return r


def check_communication(text: str) -> RitualResult:
    r = RitualResult("COMMUNICATION", "2. Communication — two-part update")
    tech_pat = re.compile(r"^\s*#{1,4}\s*(?:THE\s+)?TECHNICAL\b|\*\*\s*THE TECHNICAL\s*\*\*", re.I | re.M)
    # The plain-English part must be a section, not an inline aside: the
    # canonical "## LITERALLY WHAT I'M SAYING" header or a plain-English
    # heading at line start. Inline mentions ("explained in plain English")
    # do not count — the reviewer judges whether the section is real.
    plain_pat = re.compile(
        r"^\s*(?:#{1,4}\s*)?(?:\*\*)?(?:LITERALLY WHAT I['\u2019]?M SAYING"
        r"|(?:WHAT THIS MEANS )?(?:IN )?PLAIN[- ]ENGLISH)\b",
        re.I | re.M,
    )
    tech = _first_match_line(text, tech_pat)
    # avoid false-positive "plain english" in boilerplate like "in plain English:"? That IS the section header — keep it FOUND.
    plain = _first_match_line(text, plain_pat)
    if not tech and not plain:
        r.checks.append(Check(
            "communication.two_part", "COMMUNICATION",
            "Two-part update present (technical + plain English).",
            "N/A",
            "No update sections detected — not a Shawn-facing update; reviewer decides if the ritual applies.",
        ))
        r.checks.append(Check(
            "communication.first_paragraph_clean", "COMMUNICATION",
            "First paragraph has zero PR/issue numbers.",
            "N/A",
            "No update sections detected.",
        ))
        return r
    two_part = bool(tech and plain)
    r.checks.append(Check(
        "communication.two_part", "COMMUNICATION",
        "Two-part update present (technical + plain English).",
        "FOUND" if two_part else "MISSING",
        f"technical: {_snip(tech)} | plain-English: {_snip(plain)}",
    ))
    # first paragraph = first non-empty, non-heading block
    first_para = ""
    for para in re.split(r"\n\s*\n", text):
        stripped = para.strip()
        if not stripped:
            continue
        if re.match(r"^\s*#{1,6}\s", stripped):
            continue
        first_para = stripped
        break
    num_pat = re.compile(r"#\d+|\bPR\s*#?\s*\d+|\bissue\s*#?\s*\d+", re.I)
    hit = num_pat.search(first_para)
    r.checks.append(Check(
        "communication.first_paragraph_clean", "COMMUNICATION",
        "First paragraph has zero PR/issue numbers (numbers belong below the fold).",
        "FOUND" if not hit else "MISSING",
        ("clean — first paragraph: " + _snip(first_para.splitlines()[0] if first_para else None))
        if not hit
        else f"number found in first paragraph: '{hit.group(0)}' — paragraph: {_snip(first_para.splitlines()[0] if first_para else None)}",
    ))
    return r


def check_execution(text: str) -> RitualResult:
    r = RitualResult("EXECUTION", "3. Execution — work-product ritual")
    self_pat = re.compile(r"\bself[- ]score\b", re.I)
    score_val_pat = re.compile(r"\b\d{1,2}(?:\.\d)?\s*/\s*10\b")
    self_line = _first_match_line(text, self_pat)
    score_line = _first_match_line(text, score_val_pat)
    found_self = bool(self_line and score_line)
    r.checks.append(Check(
        "execution.self_score", "EXECUTION",
        "Work product states a self-score (with the number).",
        "FOUND" if found_self else "MISSING",
        f"self-score: {_snip(self_line)} | score value: {_snip(score_line)}",
    ))
    hole_pat = re.compile(r"\bholes?\b|\bgaps?\s+(?:found|identified|listed)|\bmiss(?:es)?\s+(?:found|named|listed)", re.I)
    hole = _first_match_line(text, hole_pat)
    r.checks.append(Check(
        "execution.holes", "EXECUTION",
        "Lists holes found (gaps/misses named).",
        "FOUND" if hole else "MISSING",
        _snip(hole),
    ))
    fill_pat = re.compile(r"\bfills?\b|\bfixed\b|\baddressed\b|\bcorrective action", re.I)
    fill = _first_match_line(text, fill_pat)
    r.checks.append(Check(
        "execution.fills", "EXECUTION",
        "Describes fills for the holes (fixed/addressed).",
        "FOUND" if fill else "MISSING",
        _snip(fill),
    ))
    seen_pat = re.compile(
        r"\bI saw\b|\bscreenshot\b|\brender(ed|ing|s)?\b|\bvisually\b"
        r"|\bwith my own eyes\b|\bwatched it render\b",
        re.I,
    )
    seen = _first_match_line(text, seen_pat)
    r.checks.append(Check(
        "execution.seen_rendered", "EXECUTION",
        "Describes what was SEEN rendered (not just coded).",
        "FOUND" if seen else "MISSING",
        _snip(seen),
    ))
    return r


_LEARN_CLAIM_PAT = re.compile(
    r"\blearning claim\b|\bwhat I learned\b|\bI learned\b|\bsmart note\b"
    r"|\blearned (?:a |the )?(?:lesson|pattern|way)\b",
    re.I,
)


def check_learning(text: str) -> RitualResult:
    r = RitualResult("LEARNING", "4. Learning — behavioral-proof ritual")
    claim = _first_match_line(text, _LEARN_CLAIM_PAT)
    if not claim:
        r.checks.append(Check(
            "learning.behavioral_proof", "LEARNING",
            'Learning claims include behavioral proof (novel problem, blind scored) — not just "I saved it."',
            "N/A",
            "No learning claims detected — reviewer decides if the ritual applies.",
        ))
        return r
    novel = _first_match_line(text, re.compile(r"\bnovel problem\b", re.I))
    blind = _first_match_line(text, re.compile(r"\bblind\b", re.I))
    scored = _first_match_line(text, re.compile(r"\bscor(?:ed|ing|ecard)\b", re.I))
    found = bool(novel and blind and scored)
    r.checks.append(Check(
        "learning.behavioral_proof", "LEARNING",
        'Learning claims include behavioral proof (novel problem, blind scored) — not just "I saved it."',
        "FOUND" if found else "MISSING",
        f"claim: {_snip(claim)} | novel problem: {_snip(novel)} | blind: {_snip(blind)} | scored: {_snip(scored)}",
    ))
    return r


_AUTHORITY_TRIGGER_PAT = re.compile(
    r"shawn['\u2019]?s\b.{0,60}?\b(?:mistake|error|bug)\b|you did this"
    r"|his\b.{0,40}?\b(?:mistake|error|bug)\b"
    r"|not aligned with (?:our |the )?protocol|\bmisalign",
    re.I | re.S,
)


def check_authority(text: str) -> RitualResult:
    r = RitualResult("AUTHORITY", "5. Authority — fix-Shawn's-mistakes ritual")
    trigger = _first_match_line(text, _AUTHORITY_TRIGGER_PAT)
    if not trigger:
        r.checks.append(Check(
            "authority.misalignment_stated", "AUTHORITY",
            "Agent states the misalignment plainly before fixing Shawn's mistake.",
            "N/A",
            "No Shawn correction detected — reviewer decides if the ritual applies.",
        ))
        return r
    plain_pat = re.compile(
        r"\bmisalign(?:ed|ment)?\b|\bnot (?:right|aligned)\b|\bmistake\b|\byou did this\b",
        re.I,
    )
    plain = _first_match_line(text, plain_pat)
    r.checks.append(Check(
        "authority.misalignment_stated", "AUTHORITY",
        "Agent states the misalignment plainly before fixing Shawn's mistake.",
        "FOUND" if plain else "MISSING",
        f"trigger: {_snip(trigger)} | plain statement: {_snip(plain)}",
    ))
    return r


def check_constitution(text: str) -> RitualResult:
    r = RitualResult("CONSTITUTION", "6. Constitution — Law of One ritual")
    law_pat = re.compile(r"\blaw of one\b|\bmost intelligent thing\b", re.I)
    law = _first_match_line(text, law_pat)
    r.checks.append(Check(
        "constitution.law_of_one", "CONSTITUTION",
        'Mandatory Law of One test stated ("Law of One" / "most intelligent thing") before significant actions.',
        "FOUND" if law else "MISSING",
        _snip(law),
    ))
    hv_pat = re.compile(r"\bbetter off\b|\bhuman value\b|\bwhat human\b", re.I)
    hv = _first_match_line(text, hv_pat)
    r.checks.append(Check(
        "constitution.human_value", "CONSTITUTION",
        'Human value named ("what human is better off?").',
        "FOUND" if hv else "MISSING",
        _snip(hv),
    ))
    close_pat = re.compile(
        r"\bserves?\s+the\s+human\b|\bserving\s+the\s+human\b"
        r"|\bwhich\s+option\b.{0,60}?\bhuman\b",
        re.I | re.S,
    )
    close = _first_match_line(text, close_pat)
    r.checks.append(Check(
        "constitution.close_call", "CONSTITUTION",
        "Close calls name which option serves the human.",
        "FOUND" if close else "MISSING",
        _snip(close),
    ))
    return r


_DESIGN_TRIGGER_PAT = re.compile(
    r"\bdesign\b|\bvisual\b|\bglow\b|\blayout\b|\bcolor scheme\b|\brender(ed)?\b",
    re.I,
)


def check_design(text: str) -> RitualResult:
    r = RitualResult("DESIGN", "7. Design — craft ritual")
    trigger = _first_match_line(text, _DESIGN_TRIGGER_PAT)
    if not trigger:
        for cid, desc in (
            ("design.one_living_intelligence", 'Designer states how work serves "one living intelligence".'),
            ("design.effect_justified", "Every visual effect justified."),
            ("design.improved_vs_preserved", "States what improved vs what was preserved."),
        ):
            r.checks.append(Check(
                cid, "DESIGN", desc, "N/A",
                "No design work detected — reviewer decides if the ritual applies.",
            ))
        return r
    oli = _first_match_line(text, re.compile(r"\bone living intelligence\b", re.I))
    r.checks.append(Check(
        "design.one_living_intelligence", "DESIGN",
        'Designer states how work serves "one living intelligence".',
        "FOUND" if oli else "MISSING",
        _snip(oli),
    ))
    effect_pat = re.compile(
        r"\b(?:glow|animation|shadow|gradient|blur|border|color|effect)\b.{0,150}?"
        r"\b(?:because|justif\w*|serves to|in order to|to signal|to communicate|to guide)\b"
        r"|\bjustif\w*\b.{0,150}?\b(?:glow|animation|shadow|gradient|blur|border|color|effect)\b",
        re.I | re.S,
    )
    justified = _first_match_line(text, effect_pat)
    if justified is None:
        # allow "justification:" heading + effect words in the same product
        if re.search(r"\bjustif\w*\b", text, re.I) and re.search(
            r"\b(?:glow|animation|shadow|gradient|blur|border|color|effect)\b", text, re.I
        ):
            justified = "(justification marker + effect terms present in product)"
    r.checks.append(Check(
        "design.effect_justified", "DESIGN",
        "Every visual effect justified (why it exists, what it serves).",
        "FOUND" if justified else "MISSING",
        _snip(justified),
    ))
    improved = _first_match_line(text, re.compile(r"\bimprov\w*\b", re.I))
    preserved = _first_match_line(text, re.compile(r"\bpreserv\w*\b|\bkept\b", re.I))
    both = bool(improved and preserved)
    r.checks.append(Check(
        "design.improved_vs_preserved", "DESIGN",
        "States what improved vs what was preserved.",
        "FOUND" if both else "MISSING",
        f"improved: {_snip(improved)} | preserved: {_snip(preserved)}",
    ))
    return r


RITUAL_ORDER = [
    check_decision,
    check_communication,
    check_execution,
    check_learning,
    check_authority,
    check_constitution,
    check_design,
]


# ---------------------------------------------------------------- driver

def run_all(text: str) -> list[RitualResult]:
    return [fn(text) for fn in RITUAL_ORDER]


def format_report(results: list[RitualResult], source: str) -> str:
    lines = [
        "RITUAL CHECKLIST — reviewer aid (NOT a gate; exit 0 always; human decides)",
        f"source: {source}",
        "",
    ]
    n_found = n_missing = n_na = 0
    for rr in results:
        lines.append(f"{rr.name}  →  {rr.verdict()}")
        for c in rr.checks:
            mark = {"FOUND": "[+]", "MISSING": "[-]", "N/A": "[ ]"}[c.status]
            lines.append(f"  {mark} {c.description}")
            lines.append(f"      evidence: {c.evidence}")
            n_found += c.status == "FOUND"
            n_missing += c.status == "MISSING"
            n_na += c.status == "N/A"
        lines.append("")
    lines.append(
        f"summary: {n_found} FOUND / {n_missing} MISSING / {n_na} N/A — "
        "MISSING flags are for the reviewer to bounce or accept, not auto-rejections."
    )
    return "\n".join(lines)


def report_json(results: list[RitualResult], source: str) -> dict:
    return {
        "tool": "ritual_checklist",
        "source": source,
        "auto_reject": False,
        "rituals": [
            {
                "key": rr.key,
                "name": rr.name,
                "verdict": rr.verdict(),
                "checks": [
                    {
                        "id": c.check_id,
                        "description": c.description,
                        "status": c.status,
                        "evidence": c.evidence,
                    }
                    for c in rr.checks
                ],
            }
            for rr in results
        ],
    }


def fetch_pr_body(pr_number: str) -> tuple[str, str]:
    """Fetch PR title+body via the gh-api wrapper. Returns (source_label, text)."""
    if not GH_API.exists():
        raise SystemExit(f"gh-api not found at {GH_API}; use --file or --text instead.")
    out = subprocess.run(
        [str(GH_API), "GET", f"/repos/{REPO_SLUG}/pulls/{pr_number}"],
        capture_output=True, text=True, timeout=60,
    )
    if out.returncode != 0:
        raise SystemExit(f"gh-api failed for PR {pr_number}: {out.stderr.strip()[:200]}")
    try:
        pr = json.loads(out.stdout)
    except json.JSONDecodeError:
        raise SystemExit(f"gh-api returned non-JSON for PR {pr_number}.")
    title = pr.get("title", "")
    body = pr.get("body") or ""
    return f"PR #{pr_number} ({pr.get('head', {}).get('sha', 'sha?')[:8]})", f"{title}\n\n{body}"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Ritual checklist: mechanical verification aid for the seven Operating Code V2 rituals."
    )
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--file", help="path to the work product (report text, PR body, spec)")
    src.add_argument("--text", help="work product text inline")
    src.add_argument("--pr", help="GitHub PR number; fetches title+body via gh-api")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    args = ap.parse_args(argv)

    if args.file:
        p = Path(args.file)
        if not p.exists():
            raise SystemExit(f"file not found: {p}")
        text = p.read_text(encoding="utf-8", errors="replace")
        source = f"file {p}"
    elif args.text:
        text = args.text
        source = "inline --text"
    else:
        source, text = fetch_pr_body(args.pr)

    results = run_all(text)
    if args.json:
        print(json.dumps(report_json(results, source), indent=2))
    else:
        print(format_report(results, source))
    return 0  # never auto-rejects


if __name__ == "__main__":
    sys.exit(main())
