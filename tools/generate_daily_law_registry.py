#!/usr/bin/env python3
"""DAILY-LAW REGISTRY generator + validator (GT-010, activation build steps 4+5).

WHY: the law a Naya actually governs by, moment to moment, is the distilled
L-entry corpus in ~/AGENTS.md — hundreds of entries that existed only as
prose on one seat's VM, with no machine form and no repo home (activation
analysis 2026-10-21 §1.4: the single largest activation gap). A seat on
any other box did not receive them at all. This generator compiles that
corpus into one versioned machine file in the repo:

  BRAIN/01-GOVERNANCE/DAILY-LAW-REGISTRY.machine.json  (+ a human index)

Two sources, one compilation:
  * the DAILY LAW — the L / WP / SN entry bullets of ~/AGENTS.md, parsed
    into structured records (id, kind, family, title, rule, falsifier,
    owner, declared behavior change, confidence, markers, provenance).
    Fields a source entry does not carry are null — never invented. An
    id cited in prose without its own entry bullet is counted as absent,
    never fabricated into a record.
  * the NUMBERED GOVERNANCE SETS — folded in via the existing
    tools/generate_laws_delta.py build (imported, never re-derived):
    this registry EXTENDS the delta, it does not duplicate it.

ONE COMPILATION STORY: BRAIN/01-GOVERNANCE/OPERATING-LAW.json (the
2026-10-10 compilation under the separate LAW-X scheme) is RETIRED by the
PR that lands this generator. After it, exactly two generated artifacts
carry compiled law — LAWS-DELTA.machine.json (governance sets) and this
registry (daily law + the delta folded in) — both freshness-checked.
OPERATING-LAW.md remains as a historical human document; its "single
canonical load" claim is superseded by the canon above and is flagged in
that PR for the LAW lane (a status change to a ratified-claiming doc is a
governance act, not a machinery edit).

DETERMINISM: no wall-clock anywhere in the output; re-running over
unchanged sources produces byte-identical files, which is what makes
--check a real freshness test. --check fails (exit 1, cure lines) when
prose and registry diverge — e.g. a law edited in AGENTS.md without
regenerating — and when the committed LAWS-DELTA's fingerprint differs
from the one this registry embeds.

Usage:
  python3 tools/generate_daily_law_registry.py [--agents-md ~/AGENTS.md] [--gov DIR]
  python3 tools/generate_daily_law_registry.py --check [--agents-md ...] [--gov DIR]

Every failure prints the self-explaining form:
  MISSING: <what> — CURE: <the single curing action> (owner: <lane>)
"""
import argparse
import hashlib
import importlib.util
import json
import re
import sys
from pathlib import Path

SCHEMA = "naya/daily-law-registry/v1"

ID_RE = re.compile(r"\b(WP-\d{1,4}|L-?\d{1,4}|SN-\d{3,4})\b")
BULLET_RE = re.compile(r"^\s*- \*\*(.+?)\*\*\s*:?\s*(.*)$")
HEADING_RE = re.compile(r"^#{1,3}\s+(.*)$")
FAMILY_RE = re.compile(r"\[?F(\d{1,2})\b")
LABEL_RE = re.compile(
    r"(Rule|Falsifier|Confidence|Guardrail owner|Mechanism|Declared behavior change(?:\s*\([^)]*\))?):\s*"
)
MARKER_WORDS = (
    "NEW FILING", "PROMOTED", "WIN-PATTERN", "STANDING", "CORE", "NEW",
    "SUPERSEDED", "REPEAT",
)


def normalize_id(raw: str) -> str:
    return raw.replace("L-", "L")


def kind_of(law_id: str) -> str:
    if law_id.startswith("WP"):
        return "win-pattern"
    if law_id.startswith("SN"):
        return "smart-note-law"
    return "lesson"


def split_fields(body: str) -> dict:
    """Split an entry body on its field labels. Unlabeled lead text is the
    statement segment; it becomes `rule` when no explicit Rule: exists."""
    parts = LABEL_RE.split(body)
    # parts: [lead, label1, seg1, label2, seg2, ...]
    fields = {"lead": parts[0].strip()}
    for i in range(1, len(parts) - 1, 2):
        label = parts[i].split("(")[0].strip().lower()
        key = {
            "rule": "rule",
            "falsifier": "falsifier",
            "confidence": "confidence",
            "guardrail owner": "owner",
            "mechanism": "mechanism",
            "declared behavior change": "behavior_change",
        }[label]
        seg = parts[i + 1].strip()
        if key not in fields or not fields[key]:
            fields[key] = seg
    return fields


def clean(text):
    if text is None:
        return None
    text = re.sub(r"\s+", " ", text).strip()
    return text or None


def title_of(head: str, idm) -> str | None:
    """The entry's human title. Two source shapes exist: id-first heads
    ('L489 [F7] — reported ≠ verified: …'), whose descriptor follows the id
    once bracket/paren tags and marker words are stripped, and titled heads
    ('The Fix-It Law (L249 — …)'), whose title precedes the parenthetical."""
    raw = idm.group(1)
    if head.startswith(raw):
        rest = head[idm.end():]
        rest = re.sub(r"\[[^\]]*\]", "", rest)
        rest = re.sub(r"\([^)]*\)", "", rest)
        rest = re.sub(r"\b(NEW FILING|PROMOTED|WIN-PATTERN|STANDING|CORE|NEW)\b", "", rest)
        return clean(rest.strip(" —-·:"))
    idx = head.find("(")
    if idx > 0 and ID_RE.search(head[idx:]):
        return clean(head[:idx])
    return clean(head)


def parse_agents_md(text: str):
    """Return (records_by_id, stats). One record per id; a later mention
    wins per-field over an earlier one; provenance accumulates."""
    lines = text.split("\n")
    records: dict[str, dict] = {}
    rule_explicit: dict[str, bool] = {}
    section = None
    bullets = 0
    for lineno, line in enumerate(lines, start=1):
        h = HEADING_RE.match(line)
        if h:
            section = h.group(1).strip()
            continue
        m = BULLET_RE.match(line)
        if not m:
            continue
        head, body = m.group(1), m.group(2)
        idm = ID_RE.search(head)
        if not idm:
            continue
        bullets += 1
        law_id = normalize_id(idm.group(1))
        fam = FAMILY_RE.search(head) or FAMILY_RE.search(body[:200])
        fields = split_fields(body)
        explicit_rule = clean(fields.get("rule"))
        lead_rule = clean(fields.get("lead"))
        title = title_of(head, idm)
        markers = [w for w in MARKER_WORDS if w in head.upper()]
        rec = records.setdefault(law_id, {
            "id": law_id,
            "kind": kind_of(law_id),
            "family": None,
            "title": None,
            "rule": None,
            "falsifier": None,
            "owner": None,
            "behavior_change": None,
            "mechanism": None,
                "confidence": None,
            "markers": [],
            "sections": [],
            "mentions": 0,
            "first_line": lineno,
        })
        rec["mentions"] += 1
        if section and section not in rec["sections"]:
            rec["sections"].append(section)
        # Rule provenance: an explicit "Rule:" label always wins; an
        # unlabeled lead only fills a rule the record does not have yet —
        # a later restatement's lead must not displace a labeled rule.
        if explicit_rule:
            rec["rule"] = explicit_rule
            rule_explicit[law_id] = True
        elif lead_rule and not rule_explicit.get(law_id) and not rec["rule"]:
            rec["rule"] = lead_rule
        for key, val in (
            ("family", f"F{fam.group(1)}" if fam else None),
            ("title", title),
            ("falsifier", clean(fields.get("falsifier"))),
            ("owner", clean(fields.get("owner"))),
            ("behavior_change", clean(fields.get("behavior_change"))),
            ("mechanism", clean(fields.get("mechanism"))),
            ("confidence", clean(fields.get("confidence"))),
        ):
            if val:
                rec[key] = val
        for mk in markers:
            if mk not in rec["markers"]:
                rec["markers"].append(mk)
    ordered = sorted(
        records.values(),
        key=lambda r: ({"lesson": 0, "win-pattern": 1, "smart-note-law": 2}[r["kind"]],
                       int(re.sub(r"\D", "", r["id"]))),
    )
    lesson_nums = {int(r["id"][1:]) for r in ordered if r["kind"] == "lesson"}
    absent = []
    if lesson_nums:
        absent = [f"L{n}" for n in range(min(lesson_nums), max(lesson_nums) + 1)
                  if n not in lesson_nums]
    stats = {"entry_bullets": bullets, "absent_lesson_numbers": absent}
    return ordered, stats


def load_delta_module():
    path = Path(__file__).resolve().parent / "generate_laws_delta.py"
    spec = importlib.util.spec_from_file_location("generate_laws_delta", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def build_registry(agents_text: str, gov: Path):
    delta_mod = load_delta_module()
    delta, problems = delta_mod.build_delta(gov)
    daily, stats = parse_agents_md(agents_text)
    raw = agents_text.encode()
    counts = {
        "daily_law_records": len(daily),
        "lessons": sum(1 for r in daily if r["kind"] == "lesson"),
        "win_patterns": sum(1 for r in daily if r["kind"] == "win-pattern"),
        "smart_note_laws": sum(1 for r in daily if r["kind"] == "smart-note-law"),
        "entry_bullets_parsed": stats["entry_bullets"],
        "with_family": sum(1 for r in daily if r["family"]),
        "with_falsifier": sum(1 for r in daily if r["falsifier"]),
        "with_owner": sum(1 for r in daily if r["owner"]),
        "with_behavior_change": sum(1 for r in daily if r["behavior_change"]),
        "with_mechanism": sum(1 for r in daily if r["mechanism"]),
        "absent_lesson_numbers": len(stats["absent_lesson_numbers"]),
        "governance_sets": delta["law_count"],
        "governance_sets_with_falsifier": sum(1 for l in delta["laws"] if l["falsifier"]),
    }
    registry = {
        "schema": SCHEMA,
        "scope": (
            "The daily operating law of Team Naya in machine form. Daily-law records are parsed "
            "from the entry bullets of ~/AGENTS.md (the seat-VM prose source); fields a source "
            "entry does not carry are null, never invented, and an L-number cited in prose "
            "without its own entry bullet is counted absent, never fabricated. Numbered "
            "governance sets are folded in verbatim from tools/generate_laws_delta.py's build "
            "(extension, not re-derivation). OPERATING-LAW.json (2026-10-10, LAW-X scheme) is "
            "retired by the landing PR — this registry plus LAWS-DELTA are the only compilations."
        ),
        "generated_from": {
            "generator": "tools/generate_daily_law_registry.py",
            "daily_law_source": {
                "path_label": "~/AGENTS.md",
                "sha256": hashlib.sha256(raw).hexdigest(),
                "bytes": len(raw),
                "lines": agents_text.count("\n") + 1,
            },
            "governance_delta": {
                "generator": "tools/generate_laws_delta.py",
                "law_count": delta["law_count"],
                "source_fingerprint_sha256":
                    delta["generated_from"]["source_fingerprint_sha256"],
            },
        },
        "counts": counts,
        "absent_lesson_numbers": stats["absent_lesson_numbers"],
        "daily_laws": daily,
        "governance_sets": delta["laws"],
    }
    return registry, problems


def render_json(registry) -> bytes:
    return (json.dumps(registry, indent=1, sort_keys=True) + "\n").encode()


def render_human(registry) -> bytes:
    c = registry["counts"]
    src = registry["generated_from"]["daily_law_source"]
    lines = [
        "# DAILY-LAW REGISTRY — human index",
        "",
        "The daily operating law of Team Naya, compiled to data. This index is",
        "GENERATED by `tools/generate_daily_law_registry.py` from ~/AGENTS.md plus",
        "the numbered governance sets (via `tools/generate_laws_delta.py`). Do not",
        "edit it by hand — regenerate. Freshness is mechanical:",
        "`python3 tools/generate_daily_law_registry.py --check` fails when the prose",
        "and this registry diverge.",
        "",
        f"- Daily-law records: **{c['daily_law_records']}** "
        f"({c['lessons']} lessons · {c['win_patterns']} win-patterns · "
        f"{c['smart_note_laws']} smart-note laws) from {c['entry_bullets_parsed']} entry bullets",
        f"- With falsifier: {c['with_falsifier']} · with owner: {c['with_owner']} · "
        f"with declared behavior change: {c['with_behavior_change']} · "
        f"with named mechanism: {c['with_mechanism']}",
        f"- L-numbers cited but carrying no entry of their own (counted, never "
        f"fabricated): {c['absent_lesson_numbers']}",
        f"- Governance sets folded in: {c['governance_sets']} "
        f"({c['governance_sets_with_falsifier']} with falsifiers)",
        f"- Source: ~/AGENTS.md sha256 `{src['sha256'][:16]}…` ({src['bytes']} bytes)",
        "",
        "OPERATING-LAW.json (the 2026-10-10 LAW-X compilation) is retired: this",
        "registry and LAWS-DELTA.machine.json are the only law compilations now.",
        "",
        "## Daily laws",
        "",
        "| id | family | rule (first 140 chars) |",
        "|---|---|---|",
    ]
    for r in registry["daily_laws"]:
        rule = (r["rule"] or r["title"] or "").replace("|", "/")
        if len(rule) > 140:
            rule = rule[:137] + "…"
        lines.append(f"| {r['id']} | {r['family'] or '—'} | {rule} |")
    lines += ["", "## Governance sets (via LAWS-DELTA)", "",
              "| id | title |", "|---|---|"]
    for g in registry["governance_sets"]:
        lines.append(f"| {g['id']} | {(g['title'] or '').replace('|', '/')} |")
    lines.append("")
    return ("\n".join(lines)).encode()


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--agents-md", default=str(Path.home() / "AGENTS.md"))
    ap.add_argument("--gov", default="BRAIN/01-GOVERNANCE")
    ap.add_argument("--out", default=None,
                    help="default: <gov>/DAILY-LAW-REGISTRY.machine.json")
    ap.add_argument("--human-out", default=None,
                    help="default: <gov>/DAILY-LAW-REGISTRY.human.md")
    ap.add_argument("--check", action="store_true",
                    help="validate + freshness check, write nothing")
    args = ap.parse_args(argv)
    gov = Path(args.gov)
    out = Path(args.out) if args.out else gov / "DAILY-LAW-REGISTRY.machine.json"
    human_out = Path(args.human_out) if args.human_out else gov / "DAILY-LAW-REGISTRY.human.md"
    agents_path = Path(args.agents_md).expanduser()
    if not agents_path.exists():
        print(f"MISSING: daily-law source {agents_path} — CURE: pass --agents-md pointing at "
              f"the seat's AGENTS.md (owner: calling lane)")
        return 1
    if not gov.is_dir():
        print(f"MISSING: governance directory {gov} — CURE: run from the repo root (owner: calling lane)")
        return 1
    registry, problems = build_registry(agents_path.read_text(encoding="utf-8", errors="replace"), gov)
    for p in problems:
        print(p)
    if problems:
        return 1
    json_bytes = render_json(registry)
    human_bytes = render_human(registry)
    if args.check:
        failed = False
        for path, fresh, label in ((out, json_bytes, "daily-law registry"),
                                   (human_out, human_bytes, "human index")):
            if not path.exists():
                print(f"MISSING: {label} at {path} — CURE: run tools/generate_daily_law_registry.py "
                      f"and commit the result (owner: LAW lane)")
                failed = True
            elif path.read_bytes() != fresh:
                print(f"MISSING: a current {label} at {path} (committed bytes differ from a fresh "
                      f"generation — the prose moved without regenerating) — CURE: run "
                      f"tools/generate_daily_law_registry.py and commit the result (owner: LAW lane)")
                failed = True
        delta_path = gov / "LAWS-DELTA.machine.json"
        if delta_path.exists():
            committed_fp = None
            try:
                committed_fp = json.loads(delta_path.read_bytes())["generated_from"][
                    "source_fingerprint_sha256"]
            except Exception:  # noqa: BLE001
                committed_fp = None
            embedded_fp = registry["generated_from"]["governance_delta"][
                "source_fingerprint_sha256"]
            if committed_fp != embedded_fp:
                print(f"MISSING: a current laws delta at {delta_path} (its fingerprint differs from "
                      f"the one this registry embeds) — CURE: run tools/generate_laws_delta.py and "
                      f"commit the result (owner: main seat)")
                failed = True
        if failed:
            return 1
        print(f"OK: registry fresh — {registry['counts']['daily_law_records']} daily-law records, "
              f"{registry['counts']['governance_sets']} governance sets, source "
              f"sha256 {registry['generated_from']['daily_law_source']['sha256'][:12]}…")
        return 0
    out.write_bytes(json_bytes)
    human_out.write_bytes(human_bytes)
    print(f"wrote {out} — {registry['counts']['daily_law_records']} daily-law records "
          f"({registry['counts']['lessons']} lessons, {registry['counts']['win_patterns']} win-patterns)")
    print(f"wrote {human_out} — human index")
    return 0


if __name__ == "__main__":
    sys.exit(main())
