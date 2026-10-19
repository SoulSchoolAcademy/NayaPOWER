#!/usr/bin/env python3
"""Template Customizer — contract JSON in, customized working app out.

Takes a PROVEN template (9/10 hand-built) + contract data
(name, tagline, colors, content) → outputs customized HTML.

This is the "assembler" — not generating from scratch,
customizing proven templates. That's how we lock in quality.
"""

import json
import sys
import os

def customize(template_path, contract_path, output_path):
    # Load template
    with open(template_path, 'r') as f:
        html = f.read()
    
    # Load contract
    with open(contract_path, 'r') as f:
        contract = json.load(f)
    
    # Apply customizations
    # 1. Name
    if 'name' in contract:
        # Replace default name placeholders
        html = html.replace('>Your Name<', f'>{contract["name"]}<')
        html = html.replace('id="pname" title="Click to edit">Your Name', 
                           f'id="pname" title="Click to edit">{contract["name"]}')
    
    # 2. Tagline/motto
    if 'tagline' in contract:
        html = html.replace('>My personal hub<', f'>{contract["tagline"]}<')
    
    # 3. About text
    if 'about' in contract:
        html = html.replace('Creator, thinker, builder. I turn ideas into reality.',
                           contract['about'])
    
    # 4. Soul color (primary theme)
    if 'soul_color' in contract:
        # This would replace the primary accent
        # For now, log it
        print(f"Soul color: {contract['soul_color']} (manual theming needed)")
    
    # 5. Template-specific content
    if 'sections' in contract:
        print(f"Sections: {list(contract['sections'].keys())}")
    
    # Write output
    with open(output_path, 'w') as f:
        f.write(html)
    
    print(f"✓ Customized: {template_path} → {output_path}")
    print(f"  Contract: {contract_path}")
    return True

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: customize.py <template.html> <contract.json> <output.html>")
        sys.exit(1)
    customize(sys.argv[1], sys.argv[2], sys.argv[3])
