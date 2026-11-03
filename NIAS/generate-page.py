#!/usr/bin/env python3
"""
NAYA PAGE GENERATOR — The machine that builds pages.
Input: PI data (JSON) → Output: finished HTML page (DNA-locked).

Usage: python3 generate-page.py <pi-data.json> <output.html>
"""

import json
import sys
from pathlib import Path

BASE = Path(__file__).parent

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

    # Replace placeholders
    html = template
    html = html.replace("{{name}}", pi["name"])
    html = html.replace("{{type}}", page_type)
    html = html.replace("{{vision}}", pi["vision"])
    html = html.replace("{{mission}}", pi["mission"])
    html = html.replace("{{goal}}", pi["goal"])

    # Custom sections (if any)
    if "sections" in pi and pi["sections"]:
        custom_html = ""
        for s in pi["sections"]:
            color = s.get("color", "purple")
            custom_html += f'''
  <div class="naya-section" style="--section-color: var(--naya-{color});">
    <h2>{s["title"]}</h2>
    <p style="font-size: var(--naya-nutshell);">{s["content"]}</p>
  </div>
'''
        # Insert before closing main
        html = html.replace("</main>", custom_html + "\n</main>")

    # Write output
    Path(output_path).write_text(html)
    print(f"✓ Generated {output_path} — type: {page_type}, DNA-locked, 10-star ready")
    return output_path

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 generate-page.py <pi-data.json> <output.html>")
        sys.exit(1)
    generate(sys.argv[1], sys.argv[2])
