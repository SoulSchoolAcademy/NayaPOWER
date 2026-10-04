#!/usr/bin/env python3
"""Render a Smart Note's human view FROM its canonical capture JSON.

THE PATH LAW IS ENCODED HERE: the output path is COMPUTED from the JSON's own
fields (capture date, projection slugs, smart_note_id). This script accepts NO
output-path argument — there is no parameter to improvise with. The brain path
is the only path; invented locations are unexpressible.

Usage: render_smart_note.py <capture-json>
  Prints the generated markdown to stdout.
  Prints the canonical brain path to stderr.

The pipeline (not this script) performs the authoritative write post-merge.
"""
import json
import sys


def brain_path(d):
    src = d.get("source", {})
    date = (src.get("captured_at") or "2026-10-04").replace("-", "/")
    proj = d.get("projection", {})
    cat = proj.get("category_slug", "SYSTEM-INTELLIGENCE")
    topic = proj.get("topic_slug", d.get("topic", "TOPIC").replace("-", "-"))
    sub = proj.get("subtopic_slug", d.get("subtopic", "SUB").replace("-", "-"))
    sid = d.get("smart_note_id", "SN-000")
    num = sid.replace("SN-", "").zfill(4)
    cap_id = d.get("capture_id", "capture").replace("sn" + sid.replace("SN-", ""), f"sn{num}")
    slug = d.get("title", "smart-note").lower()
    slug = "".join(c if (c.isalnum() or c == " ") else "" for c in slug)
    slug = "-".join(slug.split())[:60]
    ymd = date.replace("/", "")
    return (f"BRAIN/05-MEMORY/SMART-NOTES/{date}/{cat}/{topic}/{sub}/"
            f"SN-{num}/IB-SMART-NOTE-{ymd}-sn{num}-{slug}.md")


def render(d):
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
             "Truth state: CANDIDATE until the pipeline verifies and canonizes it.")
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


def main():
    if len(sys.argv) != 2:
        print("usage: render_smart_note.py <capture-json>", file=sys.stderr)
        sys.exit(2)
    with open(sys.argv[1], encoding="utf-8") as fh:
        d = json.load(fh)
    print(f"canonical-path: {brain_path(d)}", file=sys.stderr)
    print(render(d))


if __name__ == "__main__":
    main()
