#!/usr/bin/env python3
"""Generate NAYA-DESIGN-CONTRACT.machine.json FROM NAYA-DESIGN-CONTRACT-V1.md.

The human contract (BRAIN/10-INTERFACES/NAYA-DESIGN-CONTRACT-V1.md, v1.2+)
is the single source of truth. This script DERIVES its machine twin into the
canon folder (BRAIN/10-INTERFACES/SMART-FACTORY-CANON/, per the canonical-set
declaration in MANIFEST.md). The twin is never hand-written: if the .md
changes, re-run this script; validate-machine-contract.py (check 9) fails
until the committed twin is byte-identical to a fresh generation.

Extraction is anchored and fail-loud: every structured field is pulled from a
named anchor in the .md (the canonical walk line, the Tokens list, the SS3
reaction list, the SmartNote board mapping, ...). If an anchor is missing or
a count is off, the generator exits 2 naming what it could not extract --
nothing is silently dropped or invented. Prose that has no clean structured
shape is carried verbatim (emphasis stripped, whitespace normalized) in the
owning field or in `sections`, so the twin loses no wording.

Usage:
  generate-contract-twin.py [--md PATH] [--out PATH]   # regenerate the twin
  generate-contract-twin.py --check [--md PATH] [--out PATH]
      # exit 0 iff the twin at --out is byte-identical to a fresh generation

Defaults resolve from this file's location (canon/engine/), so the script
works from any checkout. Output is deterministic: no timestamps, fixed key
order -- same .md in, same bytes out.
"""
import argparse, hashlib, json, pathlib, re, sys

ENGINE = pathlib.Path(__file__).resolve().parent
CANON = ENGINE.parent
INTERFACES = CANON.parent
DEFAULT_MD = INTERFACES / "NAYA-DESIGN-CONTRACT-V1.md"
DEFAULT_OUT = CANON / "NAYA-DESIGN-CONTRACT.machine.json"
MD_REPO_PATH = "BRAIN/10-INTERFACES/NAYA-DESIGN-CONTRACT-V1.md"
GEN_REPO_PATH = "BRAIN/10-INTERFACES/SMART-FACTORY-CANON/engine/generate-contract-twin.py"

HEX = r"#[0-9a-f]{6}"
PAIR = re.compile(r"(\w+) `(" + HEX + r")`")


class ExtractError(Exception):
    pass


def need(cond, what):
    if not cond:
        raise ExtractError(what)


def norm(s):
    """Verbatim text, machine-carried: emphasis stripped, whitespace collapsed."""
    s = s.replace("**", "")
    return re.sub(r"\s+", " ", s).strip()


def section(md, heading):
    """Body of the `## <heading>` section, up to the next `## ` heading."""
    m = re.search(r"^## " + re.escape(heading) + r"\s*$", md, flags=re.M)
    need(m, f"section '## {heading}' not found")
    rest = md[m.end():]
    nxt = re.search(r"^## ", rest, flags=re.M)
    return rest[:nxt.start()] if nxt else rest


def subsection(body, heading):
    """Body of the `### <heading>` subsection inside a section body."""
    m = re.search(r"^### " + re.escape(heading) + r".*$", body, flags=re.M)
    need(m, f"subsection '### {heading}' not found")
    rest = body[m.end():]
    nxt = re.search(r"^### ", rest, flags=re.M)
    return rest[:nxt.start()] if nxt else rest


def line_starting(body, prefix, where):
    for line in body.splitlines():
        if line.strip().startswith(prefix):
            return line.strip()
    raise ExtractError(f"no line starting '{prefix}' in {where}")


def pairs(text):
    """All `name `#hex`` pairs, in order, as {'name': lower, 'hex': ...}."""
    return [{"name": n.lower(), "hex": h} for n, h in PAIR.findall(text)]


def named_principles(body, where):
    """Bullets of the form `- **Name.** statement` or `- **Name** -- statement`.

    The name is the bold lead with its trailing period and surrounding quotes
    stripped (typography, not identity); the statement is carried verbatim.
    """
    out = []
    for line in body.splitlines():
        m = re.match(r"^- \*\*(.+?)\*\*\s*(.*)$", line.strip())
        if not m:
            continue
        name = m.group(1).strip().strip('"').rstrip(".").strip()
        stmt = re.sub(r"^[\s.\u2014-]+", "", m.group(2))
        out.append({"name": name, "statement": norm(stmt)})
    need(out, f"no named-principle bullets found in {where}")
    return out


def build_twin(md_bytes):
    md = md_bytes.decode("utf-8")

    # -- meta -----------------------------------------------------------------
    first = md.splitlines()[0]
    m = re.match(r"^# (.+?) v(\d+\.\d+)\s*$", first)
    need(m, f"title line not in '# NAME vX.Y' form: {first!r}")
    contract_name, version = m.group(1), m.group(2)
    status = norm(line_starting(md, "**Status:**", "header").split("**Status:**", 1)[1])
    mrat = re.search(r"\*\*Ratified:\*\* (\d{4}-\d{2}-\d{2}) by (.+)$", md, flags=re.M)
    need(mrat, "Ratified line not found")
    purpose = norm(line_starting(md, "**Purpose:**", "header").split("**Purpose:**", 1)[1])

    sec1 = section(md, "1. COLOR LANGUAGE")

    # -- dominant colors --------------------------------------------------------
    dom_block = subsection(sec1, "Dominant (always present)")
    dominant = []
    for line in dom_block.splitlines():
        mm = re.match(r"^- \*\*(\w+)\*\* \(`(" + HEX + r")`\) \u2014 (.+)$", line.strip())
        if mm:
            dominant.append({"name": mm.group(1).lower(), "hex": mm.group(2),
                             "role": norm(mm.group(3))})
    need(len(dominant) == 3, f"dominant colors: expected 3, parsed {len(dominant)}")

    # -- the canonical spectrum walk --------------------------------------------
    walk_line = line_starting(sec1, "**The walk (canonical, stated once):", "SS1")
    walk = pairs(walk_line)
    need(len(walk) == 7, f"spectrum walk: expected 7 colors, parsed {len(walk)}")
    mw = re.search(r"back to (\w+)", walk_line)
    need(mw and mw.group(1) == walk[0]["name"],
         "walk must wrap back to its first color")
    walk_hex = [c["hex"] for c in walk]
    rule = norm(line_starting(sec1, "**The rule:**", "SS1").split("**The rule:**", 1)[1])

    # -- the three color jobs -----------------------------------------------------
    jobs = subsection(sec1, "Spectrum (accents, never dominant)")

    jewels_anchor = jobs.find("**1. Accent jewels**")
    need(jewels_anchor >= 0, "accent jewels job not found in SS1")
    jewel_line = next((l for l in jobs[jewels_anchor:].splitlines()[1:]
                       if "`#" in l), "")
    jewels = pairs(jewel_line)
    need(len(jewels) == 5, f"accent jewels: expected 5, parsed {len(jewels)}")

    flow_line = next((l for l in jobs.splitlines() if "(repeats)" in l), "")
    need(flow_line, "endless flow line ('(repeats)') not found in SS1")
    flow = pairs(flow_line)
    need([c["hex"] for c in flow] == walk_hex,
         "endless flow sequence differs from the canonical walk")

    board_anchor = jobs.find("**3. SmartNote board sections**")
    need(board_anchor >= 0, "SmartNote board mapping not found in SS1")
    board_entries = []
    for line in jobs[board_anchor:].splitlines():
        mm = re.match(r"^- (.+?) \u2192 (.+)$", line.strip())
        if not mm:
            continue
        found = PAIR.findall(mm.group(2))
        need(found, f"board mapping bullet carries no color: {line.strip()!r}")
        entry = {
            "section": mm.group(1),
            "color_name": found[0][0].lower(),
            "hex": found[0][1],
            "walk_member": found[0][1] in walk_hex,
            "board_mapping_only": "board-mapping-only" in line,
        }
        if len(found) > 1:
            entry["alternatives"] = [{"color_name": n.lower(), "hex": h}
                                      for n, h in found[1:]]
        board_entries.append(entry)
    need(len(board_entries) == 9,
         f"SmartNote board mapping: expected 9 entries, parsed {len(board_entries)}")

    # -- tokens -------------------------------------------------------------------
    tok_block = subsection(sec1, "Tokens")
    tokens = []
    for line in tok_block.splitlines():
        mm = re.match(r"^- (\w+) `(" + HEX + r")`$", line.strip())
        if mm:
            tokens.append({"name": mm.group(1).lower(), "hex": mm.group(2)})
    need(len(tokens) == 7 and [t["hex"] for t in tokens] == walk_hex,
         "Tokens list must be the 7 walk colors in walk order")

    color_law = norm(line_starting(sec1, "**Law:**", "SS1").split("**Law:**", 1)[1])
    active_intel = norm(line_starting(sec1, "**Active intelligence:**", "SS1")
                        .split("**Active intelligence:**", 1)[1])

    # -- SS2 lighting ----------------------------------------------------------
    sec2 = section(md, "2. THE LIGHTING STANDARD")
    states, keymap = [], {"idle": "idle", "hover": "hover", "active": "active_selected"}
    for line in sec2.splitlines():
        mm = re.match(r"^- \*\*([A-Za-z/ ]+?)(?: \([^)]*\))?:\*\* (.+)$", line.strip())
        if mm:
            key = keymap.get(mm.group(1).split("/")[0].strip().lower())
            need(key, f"lighting state not recognized: {mm.group(1)!r}")
            states.append({"state": key, "label": mm.group(1), "rule": norm(mm.group(2))})
    need([s["state"] for s in states] == ["idle", "hover", "active_selected"],
         f"lighting states: expected idle/hover/active_selected, parsed {[s['state'] for s in states]}")
    applies_to = norm(line_starting(sec2, "**Applies to:**", "SS2")
                      .split("**Applies to:**", 1)[1])

    # -- SS3 buttons -------------------------------------------------------------
    sec3 = section(md, "3. BUTTON LANGUAGE")
    prim = subsection(sec3, "Primary toggle buttons (sidebar openers, menu triggers)")
    mg = re.search(r"radial-gradient\([^)]*\)", prim)
    need(mg, "primary toggle gradient not found in SS3")
    prim_rules = [norm(l.strip()[2:]) for l in prim.splitlines()
                  if l.strip().startswith("- ")]
    act = subsection(sec3, "Action buttons (Love, Like, Save, etc.)")
    reactions, act_rules = [], []
    for line in act.splitlines():
        mr = re.match(r"^\s+- ([A-Z][A-Z ]*[A-Z]): (\w+) `(" + HEX + r")`(.*)$", line)
        if mr:
            reactions.append({"action": mr.group(1), "color_name": mr.group(2).lower(),
                              "hex": mr.group(3),
                              "walk_value": "walk value" in mr.group(4)})
        elif line.startswith("- "):
            act_rules.append(norm(line.strip()[2:]))
    need(len(reactions) == 6,
         f"SS3 reactions: expected 6, parsed {len(reactions)}")
    need(all(r["hex"] in walk_hex for r in reactions),
         "every SS3 reaction hex must be a walk value (the .md annotates them canonical)")
    eco = subsection(sec3, "Ecosystem buttons (bottom bar)")
    eco_rules = [norm(l.strip()[2:]) for l in eco.splitlines()
                 if l.strip().startswith("- ")]

    # -- SS4 icons -----------------------------------------------------------------
    sec4 = section(md, "4. ICON LANGUAGE")
    icon_rules = named_principles(sec4, "SS4")
    mi = re.search(r"(\d+) unique icons \(([^)]+)\)", sec4)
    need(mi, "ecosystem icon list not found in SS4")
    eco_icons = [s.strip() for s in mi.group(2).split(",")]
    need(int(mi.group(1)) == len(eco_icons) == 12,
         f"ecosystem icons: stated {mi.group(1)}, listed {len(eco_icons)}")
    icon_law = norm(line_starting(sec4, "**Law:**", "SS4").split("**Law:**", 1)[1])

    # -- SS5 typography -------------------------------------------------------------
    sec5 = section(md, "5. TYPOGRAPHY & READABILITY")
    law_zero = norm(line_starting(sec5, "- **LAW ZERO (supreme):**", "SS5")
                    .split(":**", 1)[1])
    mb = re.search(r"Body: (\d+)-(\d+)px target, (\d+)px floor", sec5)
    need(mb, "body type sizes not found in SS5")
    typo_rules = [norm(l.strip()[2:]) for l in sec5.splitlines()
                  if l.strip().startswith("- ")
                  and "LAW ZERO" not in l and not l.strip().startswith("- Body:")]

    # -- SS6/SS7/SS8 named principles ----------------------------------------------
    layout = named_principles(section(md, "6. LAYOUT PRINCIPLES"), "SS6")
    honesty = named_principles(section(md, "7. HONESTY"), "SS7")
    philosophy = named_principles(section(md, "8. THE NAYA PHILOSOPHY (logic & thinking)"), "SS8")
    need(len(layout) == 5, f"layout principles: expected 5, parsed {len(layout)}")
    need(len(honesty) == 4, f"honesty principles: expected 4, parsed {len(honesty)}")
    need(len(philosophy) == 6, f"philosophy principles: expected 6, parsed {len(philosophy)}")

    # -- SS9 relevance algorithm -------------------------------------------------------
    sec9 = section(md, "9. RELEVANCE ALGORITHM (locked 2026-10-03)")
    rel_purpose = norm(line_starting(sec9, "**Purpose:**", "SS9").split("**Purpose:**", 1)[1])
    components = []
    for line in sec9.split("**Components:**", 1)[1].split("**Phases:**", 1)[0].splitlines():
        mm = re.match(r"^- (.+?) \((\d+)%\) \u2014 (.+)$", line.strip())
        if mm:
            components.append({"name": mm.group(1), "weight_pct": int(mm.group(2)),
                               "note": norm(mm.group(3))})
    need(len(components) == 4 and sum(c["weight_pct"] for c in components) == 100,
         f"relevance components: parsed {len(components)}, weights sum "
         f"{sum(c['weight_pct'] for c in components)} (must be 4 components, 100%)")
    phases = []
    for line in sec9.split("**Phases:**", 1)[1].split("**Principle:**", 1)[0].splitlines():
        mm = re.match(r"^- ([^:]+): (.+)$", line.strip())
        if mm:
            phases.append({"name": mm.group(1), "statement": norm(mm.group(2))})
    need(len(phases) == 3, f"relevance phases: expected 3, parsed {len(phases)}")
    rel_principle = norm(line_starting(sec9, "**Principle:**", "SS9")
                         .split("**Principle:**", 1)[1])

    # -- amendment process + version history -------------------------------------------
    amend = section(md, "AMENDMENT PROCESS")
    process_text = norm(amend.split("**Version history:**", 1)[0])
    history = []
    for line in amend.splitlines():
        mm = re.match(r"^- v(\d+\.\d+) \((\d{4}-\d{2}-\d{2})\): (.+)$", line.strip())
        if mm:
            history.append({"version": mm.group(1), "date": mm.group(2),
                            "summary": norm(mm.group(3))})
    need(history and history[-1]["version"] == version,
         f"version history must end at the title version {version}")

    # -- full section texts (nothing lost) ----------------------------------------------
    sections = []
    for chunk in re.split(r"^## ", md, flags=re.M)[1:]:
        head, _, body = chunk.partition("\n")
        mh = re.match(r"^(\d+)\.\s+(.*)$", head.strip())
        clean = "\n".join(l for l in body.splitlines() if l.strip() != "---")
        sections.append({
            "number": int(mh.group(1)) if mh else None,
            "title": (mh.group(2) if mh else head.strip()),
            "text": norm(clean),
        })
    need(len(sections) == 10, f"sections: expected 10, parsed {len(sections)}")

    twin = {
        "contract": contract_name.replace(" ", "-"),
        "kind": "machine",
        "version": version,
        "status": "canonical",
        "authority": ("This machine version is made FROM the human contract "
                      "(NAYA-DESIGN-CONTRACT-V1.md), never instead of it. The human "
                      "contract is the source of truth; if this file and the human "
                      "contract disagree, the human contract governs until this file "
                      "is regenerated with engine/generate-contract-twin.py."),
        "source": {
            "human_file": MD_REPO_PATH,
            "human_file_sha256": hashlib.sha256(md_bytes).hexdigest(),
            "human_file_bytes": len(md_bytes),
            "generator": GEN_REPO_PATH,
            "drift_detection": ("Recompute sha256 of the human file; if it differs from "
                                "human_file_sha256, this machine version is stale. "
                                "validate-machine-contract.py check 9 also regenerates "
                                "the twin and fails on any byte difference."),
        },
        "status_line": status,
        "ratified": {"date": mrat.group(1), "by": norm(mrat.group(2))},
        "purpose": purpose,
        "spectrum_walk": {
            "order": walk_hex,
            "names": [c["name"] for c in walk],
            "sequence": walk,
            "wraps_to_first": True,
            "wraps_to": walk[0]["name"],
            "adjacency_rule": ("Each section takes the NEXT color in the walk; "
                               "never the same color twice in a row."),
            "rest_and_ignition": ("Elements sit white at rest, and ignite in their "
                                  "OWN color on hover/touch."),
            "rule": rule,
        },
        "tokens": tokens,
        "dominant_colors": dominant,
        "accent_jewels": jewels,
        "endless_flow": {
            "order": [c["hex"] for c in flow],
            "names": [c["name"] for c in flow],
            "repeats": True,
        },
        "smartnote_board_mapping": {
            "name": "smartnote_board_sections",
            "kind": "fixed semantic mapping",
            "distinct_from_walk": True,
            "rule": ("A fixed semantic mapping, distinct from the spectrum walk. It "
                     "may name non-walk hues; those non-walk hues are forbidden "
                     "everywhere else."),
            "entries": board_entries,
        },
        "color_law": color_law,
        "active_intelligence": active_intel,
        "lighting_standard": {"states": states, "applies_to": applies_to},
        "button_language": {
            "primary_toggle": {"fill": mg.group(0), "rules": prim_rules},
            "action_buttons": {"rules": act_rules, "reactions": reactions},
            "ecosystem_buttons": {"rules": eco_rules},
        },
        "icon_language": {
            "rules": icon_rules,
            "ecosystem_icons": eco_icons,
            "ecosystem_icon_count": len(eco_icons),
            "law": icon_law,
        },
        "typography": {
            "law_zero": law_zero,
            "body_px": {"target_min": int(mb.group(1)), "target_max": int(mb.group(2)),
                        "floor": int(mb.group(3))},
            "rules": typo_rules,
        },
        "layout_principles": layout,
        "honesty": honesty,
        "philosophy": philosophy,
        "relevance_algorithm": {
            "purpose": rel_purpose,
            "components": components,
            "phases": phases,
            "principle": rel_principle,
        },
        "amendment_process": process_text,
        "version_history": history,
        "sections": sections,
    }
    return twin


def render(twin):
    return (json.dumps(twin, indent=2, ensure_ascii=False) + "\n").encode("utf-8")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--md", type=pathlib.Path, default=DEFAULT_MD,
                    help=f"human contract (default: {DEFAULT_MD})")
    ap.add_argument("--out", type=pathlib.Path, default=DEFAULT_OUT,
                    help=f"twin output (default: {DEFAULT_OUT})")
    ap.add_argument("--check", action="store_true",
                    help="exit 0 iff --out is byte-identical to a fresh generation")
    args = ap.parse_args(argv)

    try:
        md_bytes = args.md.read_bytes()
    except OSError as e:
        print(f"generate-contract-twin: cannot read {args.md}: {e}", file=sys.stderr)
        return 2
    try:
        data = render(build_twin(md_bytes))
    except ExtractError as e:
        print(f"generate-contract-twin: EXTRACTION FAILED: {e}", file=sys.stderr)
        return 2

    if args.check:
        if not args.out.exists():
            print(f"CHECK FAIL: twin missing at {args.out}")
            return 1
        if args.out.read_bytes() == data:
            print(f"CHECK PASS: {args.out.name} is byte-identical to a fresh "
                  f"generation from {args.md.name}")
            return 0
        print(f"CHECK FAIL: {args.out.name} differs from a fresh generation "
              f"from {args.md.name} -- regenerate it, never hand-edit it")
        return 1

    args.out.write_bytes(data)
    sha = hashlib.sha256(md_bytes).hexdigest()
    print(f"generate-contract-twin: wrote {args.out} ({len(data)} bytes) "
          f"from {args.md.name} sha256 {sha[:12]}\u2026")
    return 0


if __name__ == "__main__":
    sys.exit(main())
