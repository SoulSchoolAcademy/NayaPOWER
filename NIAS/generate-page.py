#!/usr/bin/env python3
"""
NAYA PAGE GENERATOR v3 — Active Intelligence.
Input: PI data (JSON) → Output: finished HTML page (Real Object Law, v3.0).

Usage: python3 generate-page.py <pi-data.json> <output.html>

Placeholders: {{name}} {{alias}} {{type}} {{vision}} {{mission}} {{goal}}
              {{cover}} {{sections}} {{spectrum_color}}
"""

import json
import sys
import re
from pathlib import Path

BASE = Path(__file__).parent

# Soul spectrum colors by page type (hex — one soul color per page)
TYPE_COLORS = {
    "personal": "#a06bff",    # purple — the vibe
    "business": "#ffbf3d",    # gold — value
    "space": "#3fb8ff",       # sky — community
    "membership": "#e84fff",  # magenta — exclusive
}

# Section accent colors cycle (spectrum flow, never doubled)
SECTION_COLORS = ["purple", "blue", "green", "gold", "orange", "red", "magenta"]


def load_template():
    return (BASE / "universal-template.html").read_text()


def load_configs():
    return json.loads((BASE / "page-type-configs.json").read_text())


def build_cover(pi):
    """{{cover}} — cover div or empty string."""
    cover_url = pi.get("cover", "")
    if not cover_url:
        return ""
    # Escape single quotes in URL
    safe = cover_url.replace("'", "%27")
    return f'<div class="cover" style="background-image: url(\'{safe}\');" data-naya-bind="hero-cover"></div>'


def build_sections(pi):
    """{{sections}} — custom boards with spectrum inlay, gem bullets."""
    sections = pi.get("sections", [])
    if not sections:
        return ""
    html_parts = []
    for i, s in enumerate(sections):
        color = s.get("color", SECTION_COLORS[i % len(SECTION_COLORS)])
        icon = s.get("icon", "◆")
        title = s.get("title", "")
        content = s.get("content", "")
        # Basic HTML escape for title/content to avoid breaking markup
        html_parts.append(f'''
  <section class="ai-board" style="--bc:var(--naya-{color});" data-naya-bind="board-custom-{i}">
    <h2 class="board-title"><span class="gem" style="--gc:var(--naya-{color});">{icon}</span>{title}</h2>
    <p class="board-text">{content}</p>
  </section>''')
    return "\n".join(html_parts)


def generate(pi_data_path, output_path):
    pi = json.loads(Path(pi_data_path).read_text())
    template = load_template()
    configs = load_configs()

    # Validate required fields
    for field in ["name", "type", "vision", "mission", "goal"]:
        if field not in pi:
            raise ValueError(f"Missing required field: {field}")

    page_type = pi["type"]
    if page_type not in configs:
        raise ValueError(f"Unknown type: {page_type}. Must be one of: {list(configs.keys())}")

    raw_alias = pi.get("alias", pi["name"])
    alias = re.sub(r"[^a-z0-9-]", "", raw_alias.lower().replace(" ", "-"))

    html = template
    html = html.replace("{{name}}", pi["name"])
    html = html.replace("{{alias}}", alias)
    html = html.replace("{{type}}", page_type)
    html = html.replace("{{vision}}", pi["vision"])
    html = html.replace("{{mission}}", pi["mission"])
    html = html.replace("{{goal}}", pi["goal"])
    html = html.replace("{{cover}}", build_cover(pi))
    html = html.replace("{{sections}}", build_sections(pi))
    html = html.replace("{{spectrum_color}}", pi.get("spectrum_color", TYPE_COLORS.get(page_type, TYPE_COLORS["personal"])))

    # Safety: no unfilled placeholders may ship
    leftover = re.findall(r"\{\{[a-z_]+\}\}", html)
    if leftover:
        raise ValueError(f"Unfilled placeholders: {set(leftover)}")

    Path(output_path).write_text(html)
    print(f"✓ Generated {output_path} — type: {page_type}, v3.0 Active Intelligence")
    return output_path


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 generate-page.py <pi-data.json> <output.html>")
        sys.exit(1)
    generate(sys.argv[1], sys.argv[2])
