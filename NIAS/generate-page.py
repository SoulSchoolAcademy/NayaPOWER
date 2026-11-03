#!/usr/bin/env python3
"""
NAYA PAGE GENERATOR v2 — The machine that builds pages.
Input: PI data (JSON) → Output: finished HTML page (DNA-locked, elite).

Usage: python3 generate-page.py <pi-data.json> <output.html>

Placeholders: {{name}} {{type}} {{vision}} {{mission}} {{goal}}
              {{alias}} {{hero_color}} {{cover_div}} {{custom_sections}}
"""

import json
import sys
from pathlib import Path

BASE = Path(__file__).parent

# Spectrum colors by page type (for hero glow)
TYPE_COLORS = {
    "personal": "rgba(160,107,255,.15)",   # purple
    "business": "rgba(255,191,61,.15)",    # gold
    "space": "rgba(127,212,255,.15)",      # sky
    "membership": "rgba(232,79,255,.15)",  # magenta
}

def load_template():
    return (BASE / "universal-template.html").read_text()

def load_configs():
    return json.loads((BASE / "page-type-configs.json").read_text())

def generate(pi_data_path, output_path):
    # Load inputs
    pi = json.loads(Path(pi_data_path).read_text())
    template = load_template()
    configs = load_configs()

    # Validate
    for field in ["name", "type", "vision", "mission", "goal"]:
        if field not in pi:
            raise ValueError(f"Missing required field: {field}")

    page_type = pi["type"]
    if page_type not in configs:
        raise ValueError(f"Unknown type: {page_type}. Must be one of: {list(configs.keys())}")

    config = configs[page_type]
    alias = pi.get("alias", pi["name"].lower().replace(" ", "-").replace("[^a-z0-9-]", ""))

    # Cover div (if cover URL provided)
    cover_url = pi.get("cover", "")
    cover_div = ""
    if cover_url:
        cover_div = f'<div class="cover" style="background-image: url(\'{cover_url}\');" data-naya-bind="hero-cover"></div>'

    # Custom sections
    custom_html = ""
    if "sections" in pi and pi["sections"]:
        for s in pi["sections"]:
            color = s.get("color", "purple")
            icon = s.get("icon", "")
            icon_html = f'<span class="sec-icon">{icon}</span> ' if icon else ""
            custom_html += f'''
<section class="naya-section" style="--section-color: var(--naya-{color});" data-naya-bind="custom-section">
  <h2>{icon_html}{s["title"]}</h2>
  <p>{s["content"]}</p>
</section>
'''

    # Replace placeholders
    html = template
    html = html.replace("{{name}}", pi["name"])
    html = html.replace("{{type}}", page_type)
    html = html.replace("{{vision}}", pi["vision"])
    html = html.replace("{{mission}}", pi["mission"])
    html = html.replace("{{goal}}", pi["goal"])
    html = html.replace("{{alias}}", alias)
    html = html.replace("{{hero_color}}", pi.get("hero_color", TYPE_COLORS.get(page_type, TYPE_COLORS["personal"])))
    html = html.replace("{{cover_div}}", cover_div)
    html = html.replace("{{custom_sections}}", custom_html)

    # Write output
    Path(output_path).write_text(html)
    print(f"✓ Generated {output_path} — type: {page_type}, DNA-locked, elite")
    return output_path

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 generate-page.py <pi-data.json> <output.html>")
        sys.exit(1)
    generate(sys.argv[1], sys.argv[2])
