#!/usr/bin/env python3
"""Render a Smart Note's THREE projections FROM its canonical capture JSON.

THE PATH LAW IS ENCODED HERE: every output path is COMPUTED from the JSON's
own fields (capture date, projection slugs, smart_note_id). This script accepts
NO output-path argument — there is no parameter to improvise with. The brain
paths are the only paths; invented locations are unexpressible.

The three projections (Shawn's three-angle law — every perspective covered):
  1. HUMAN  — IB-SMART-NOTE-....md          — plain-words view for the human.
  2. AI     — IB-SMART-NOTE-....ai.md       — Naya-language brief: instructions,
     evaluation, operating loop, anti-patterns. No interpretation needed.
  3. MACHINE— IB-SMART-NOTE-....machine.json — canonized machine projection:
     identity envelope + machine_view + the three views, post-capture.

One ingestion door (.naya/capture/). Three generated projections in the brain.
All views generated, never hand-written.

Usage: render_smart_note.py <capture-json>
  Prints the HUMAN markdown to stdout.
  Prints all three canonical paths to stderr.
  (The pipeline performs the authoritative three-file write post-merge.)
"""
import json
import sys


def _slug(title):
    s = "".join(c if (c.isalnum() or c == " ") else "" for c in (title or "smart-note").lower())
    return "-".join(s.split())[:60]


def brain_paths(d):
    src = d.get("source", {})
    date = (src.get("captured_at") or "2026-10-04").replace("-", "/")
    ymd = date.replace("/", "")
    proj = d.get("projection", {})
    cat = proj.get("category_slug", "SYSTEM-INTELLIGENCE")
    topic = proj.get("topic_slug", "TOPIC")
    sub = proj.get("subtopic_slug", "SUB")
    sid = d.get("smart_note_id", "SN-000")
    num = sid.replace("SN-", "").zfill(4)
    slug = _slug(d.get("title"))
    base = (f"BRAIN/05-MEMORY/SMART-NOTES/{date}/{cat}/{topic}/{sub}/"
            f"SN-{num}/IB-SMART-NOTE-{ymd}-sn{num}-{slug}")
    return {
        "human": base + ".md",
        "ai": base + ".ai.md",
        "machine": base + ".machine.json",
    }


def render_human(d):
    intel = d.get("intelligence", {})
    hv = intel.get("human_view", {})
    sv = intel.get("simple_view", {})
    av = intel.get("ai_view", {})
    nv = intel.get("naya_view", {})
    mv = intel.get("machine_view", {})
    src = d.get("source", {})

    L = []
    L.append(f"# {d.get('title', '')}")
    L.append("")
    L.append(f"**Smart Note {d.get('smart_note_id', '')}** · "
             f"{d.get('canonical_intent', '')} · Truth state: CANDIDATE")
    L.append("")
    L.append(f"*Source: {src.get('source_reference', '')}*")
    L.append("")
    L.append("> GENERATED HUMAN VIEW — rendered mechanically from the canonical "
             "capture JSON in `.naya/capture/`. This file is never hand-written. "
             "Truth state: CANDIDATE until the pipeline verifies and canonizes it. "
             "Sibling projections: `.ai.md` (Naya-language brief), "
             "`.machine.json` (canonized machine truth).")
    L.append("")
    sections = [
        ("IN A NUTSHELL", intel.get("essence", "")),
        ("HUMAN NOTE", hv.get("meaning", "")),
        ("CHILD NOTE", sv.get("child", "")),
        ("GRANDMA NOTE", sv.get("grandma", "")),
        ("NAYA NOTE",
         "\n\n".join(x for x in [nv.get("purpose", ""), nv.get("event_flow", ""),
                                 f"Operating loop: `{nv.get('operating_loop', '')}`"] if x)),
        ("MACHINE NOTE", "```json\n" + json.dumps(mv, indent=2, ensure_ascii=False) + "\n```"),
        ("LEARNING LESSON", intel.get("learning_lesson", "")),
        ("WHAT IT MEANS",
         "\n".join(f"- {x}" for x in intel.get("decisions", []))),
        ("WHAT'S IN IT FOR YOU", hv.get("goal", "")),
        ("HOW TO USE IT",
         "\n\n".join(x for x in [hv.get("simple_rule", ""),
                                 av.get("primary_evaluation", "")] if x)),
    ]
    for title, body in sections:
        L.append(f"## {title}")
        L.append("")
        L.append(body)
        L.append("")
    L.append("---")
    L.append(f"*Applicability: {intel.get('applicability', '')}*")
    L.append("")
    L.append(f"*Uncertainty: {intel.get('uncertainty', '')}*")
    L.append("")
    return "\n".join(L)


def render_ai(d):
    """The Naya-language brief: instructions an AI can execute without interpretation."""
    intel = d.get("intelligence", {})
    av = intel.get("ai_view", {})
    nv = intel.get("naya_view", {})
    sid = d.get("smart_note_id", "")

    L = []
    L.append(f"# NAYA BRIEF — {d.get('title', '')} ({sid})")
    L.append("")
    L.append("> GENERATED AI PROJECTION — rendered mechanically from the canonical "
             "capture JSON. Never hand-written. This is the instruction set, not the story.")
    L.append("")
    L.append("## INSTRUCTION")
    L.append("")
    L.append(av.get("instruction", ""))
    L.append("")
    L.append("## PRIMARY EVALUATION")
    L.append("")
    L.append(av.get("primary_evaluation", ""))
    L.append("")
    L.append("## OPERATING LOOP")
    L.append("")
    L.append(f"`{nv.get('operating_loop', '')}`")
    L.append("")
    if nv.get("anti_pattern"):
        L.append("## ANTI-PATTERN — DO NOT")
        L.append("")
        L.append(nv.get("anti_pattern", ""))
        L.append("")
    if intel.get("decisions"):
        L.append("## STANDING DECISIONS")
        L.append("")
        for x in intel["decisions"]:
            L.append(f"- {x}")
        L.append("")
    if intel.get("successor_effect"):
        L.append("## SUCCESSOR EFFECT")
        L.append("")
        L.append(intel["successor_effect"])
        L.append("")
    L.append("---")
    L.append(f"*Truth state: CANDIDATE. Siblings: human `.md`, machine `.machine.json`.*")
    L.append("")
    return "\n".join(L)


def render_machine(d):
    """Canonized machine projection: identity envelope + the three views."""
    intel = d.get("intelligence", {})
    return json.dumps({
        "projection": "machine",
        "schema": d.get("schema"),
        "smart_note_id": d.get("smart_note_id"),
        "capture_id": d.get("capture_id"),
        "canonical_intent": d.get("canonical_intent"),
        "truth_ceiling": (intel.get("machine_view", {})
                          .get("automatic_truth_ceiling", "CANDIDATE")),
        "category": d.get("category"),
        "topic": d.get("topic"),
        "subtopic": d.get("subtopic"),
        "title": d.get("title"),
        "source": d.get("source"),
        "projection_slugs": d.get("projection"),
        "human_view": intel.get("human_view"),
        "ai_view": intel.get("ai_view"),
        "machine_view": intel.get("machine_view"),
        "essence": intel.get("essence"),
        "decisions": intel.get("decisions"),
        "connections": intel.get("connections"),
        "applicability": intel.get("applicability"),
        "successor_effect": intel.get("successor_effect"),
        "uncertainty": intel.get("uncertainty"),
    }, indent=2, ensure_ascii=False)


def main():
    if len(sys.argv) != 2:
        print("usage: render_smart_note.py <capture-json>", file=sys.stderr)
        sys.exit(2)
    with open(sys.argv[1], encoding="utf-8") as fh:
        d = json.load(fh)
    paths = brain_paths(d)
    for kind, p in paths.items():
        print(f"canonical-path[{kind}]: {p}", file=sys.stderr)
    print(render_human(d))


if __name__ == "__main__":
    main()
