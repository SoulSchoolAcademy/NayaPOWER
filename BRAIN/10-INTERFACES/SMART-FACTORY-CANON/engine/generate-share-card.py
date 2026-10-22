#!/usr/bin/env python3
"""
Standard NayaNET Share Card Generator
Dynamic template: takes title + nutshell, outputs 1200x630 share image
Uses real factory ICO001 diamonds (5 colors) as signature
"""
from PIL import Image, ImageDraw, ImageFont
import textwrap

def get_font(size, bold=True):
    name = 'DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf'
    return ImageFont.truetype(f'/usr/share/fonts/truetype/dejavu/{name}', size)

def hx(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

# Paths
BG_PATH = '/home/hatch/workspace/factory-pipeline/media-generation-black-diamond-bg-0-4fda8a56-3397-4e30-9b41-1c52c4c3ba94.webp'
LOGO_PATH = '/home/hatch/workspace/user/media_library/image/08/08b753d3e79ff334598e97ac500a888d9d15dd57412cc7afc37ec30c9bc15f92.jpg'
DIAMOND_DIR = '/home/hatch/workspace/factory-pipeline/assets'

def generate_share_card(title, nutshell, output_path):
    # Background
    bg = Image.open(BG_PATH).convert('RGB')
    bg = bg.resize((1200, 630), Image.LANCZOS)
    overlay = Image.new('RGB', (1200, 630), (0, 0, 0))
    bg = Image.blend(bg, overlay, 0.78)
    draw = ImageDraw.Draw(bg)
    
    # Logo 140px
    logo = Image.open(LOGO_PATH).convert('RGB')
    logo_size = 140
    logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
    mask = Image.new('L', (logo_size, logo_size), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, logo_size, logo_size], fill=255)
    bg.paste(logo, ((1200-logo_size)//2, 25), mask)
    
    # Brand 24px
    bf = get_font(24, True)
    brand = "NAYANET.LIVE"
    bw = draw.textbbox((0,0), brand, font=bf)[2]
    draw.text(((1200-bw)//2, 175), brand, font=bf, fill=(255,255,255))
    
    # Title 48px, up to 2 lines
    tf = get_font(48, True)
    # Split title into lines if too long
    title_lines = []
    for line in title.split('\n'):
        if draw.textbbox((0,0), line, font=tf)[2] > 1000:
            # Wrap long lines
            words = line.split()
            curr = ""
            for w in words:
                test = curr + " " + w if curr else w
                if draw.textbbox((0,0), test, font=tf)[2] > 1000:
                    title_lines.append(curr)
                    curr = w
                else:
                    curr = test
            title_lines.append(curr)
        else:
            title_lines.append(line)
    # Limit to 2 lines
    title_lines = title_lines[:2]
    
    ty = 225
    for line in title_lines:
        tw = draw.textbbox((0,0), line, font=tf)[2]
        draw.text(((1200-tw)//2, ty), line, font=tf, fill=(255,255,255))
        ty += 58
    
    # Nutshell 21px (slightly bigger per Shawn), 2-3 lines
    nf = get_font(21, False)
    words = nutshell.split()
    lines = []
    curr = ""
    for w in words:
        test = curr + " " + w if curr else w
        if draw.textbbox((0,0), test, font=nf)[2] > 880:
            lines.append(curr)
            curr = w
        else:
            curr = test
    lines.append(curr)
    # Limit to 3 lines
    lines = lines[:3]
    
    # Center the text block vertically in available space
    # Available: from ty (after title) to 440 (before diamonds)
    text_block_height = len(lines) * 30
    available_top = ty + 10
    available_bottom = 440
    available_height = available_bottom - available_top
    # Center text block in available space
    ny = available_top + (available_height - text_block_height) // 2
    
    for line in lines:
        nw = draw.textbbox((0,0), line, font=nf)[2]
        draw.text(((1200-nw)//2, ny), line, font=nf, fill=(255,255,255))
        ny += 30
    
    # Diamonds at bottom
    names = ["magenta", "purple", "blue", "green", "gold"]
    diamonds = [Image.open(f'{DIAMOND_DIR}/diamond3-{n}.png').convert('RGBA') for n in names]
    target_size = 75
    scaled = [d.resize((target_size, target_size), Image.LANCZOS) for d in diamonds]
    gap = 20
    total_w = sum(s.size[0] for s in scaled) + gap * 4
    row = Image.new('RGBA', (total_w, target_size), (0,0,0,0))
    x = 0
    for s in scaled:
        row.paste(s, (x, 0), s)
        x += s.size[0] + gap
    
    bg_rgba = bg.convert('RGBA')
    bx = (1200 - total_w) // 2
    by = 445
    bg_rgba.paste(row, (bx, by), row)
    
    bg_rgba.convert('RGB').save(output_path, 'PNG')
    print(f"Generated: {output_path}")
    return output_path

if __name__ == '__main__':
    import sys
    if len(sys.argv) >= 4:
        generate_share_card(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        print("Usage: generate-share-card.py '<title>' '<nutshell>' <output.png>")
