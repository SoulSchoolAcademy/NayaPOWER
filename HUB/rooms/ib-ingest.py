#!/usr/bin/env python3
"""IB → Hub feed pipeline (demo trigger).

Reads Intelligent Blocks from BRAIN/05-MEMORY/SMART-NOTES/** and emits
`.block` article HTML for injection into the Hub's `.blocks` container.

The Hub is the OUTPUT. This script is the TRIGGER: IB written -> event ->
feed block. Production trigger: GitHub Actions on push to SMART-NOTES/**.
"""
import os, re, html, glob

HERE = os.path.dirname(os.path.abspath(__file__))
# Canonical IB home: ratified protocol 0005-SMART-NODE-INTELLIGENT-BLOCK-PROTOCOL-V1
# specifies BRAIN/05-MEMORY/SMART-NOTES/YYYY/MM/DD/CATEGORY/TOPIC/SUBTOPIC/SN-###/IB-....md.
# Falls back to the branch-local demo tree when the canonical tree is absent.
IB_ROOT = os.path.join(HERE, 'BRAIN', '05-MEMORY', 'SMART-NOTES')
if not os.path.isdir(IB_ROOT):
    IB_ROOT = os.path.join(HERE, 'ib', 'SMART-NOTES')

LAYERS = [
    ("in a nutshell", None),  # special: .nutshell div
    ("human note", ("HUMAN NOTE", "HUMAN INPUT")),
    ("child note", ("CHILD", "SIMPLIFIED")),
    ("grandma note", ("GRANDMA NOTE", "WHY NOTICE?")),
    ("naya note", ("NAYA NOTE", "INTERPRETATION")),
    ("machine note", ("MACHINE NOTE", "MACHINE")),
    ("learning lesson", ("LEARNING LESSON", "LEARNING")),
    ("what it ultimately means", ("WHAT IT ULTIMATELY MEANS", "MEANING")),
    ("how to use it", ("HOW TO USE IT", "USE")),
    ("what's in it for you", ("WHAT'S IN IT FOR YOU", "VALUE")),
]

KIND_META = {
    "smart-note": "SMART NOTE",
    "activity": "ACTIVITY",
    "report": "REPORT",
}

def parse_ib(path):
    text = open(path).read()
    m = re.match(r'^---\n(.*?)\n---\n(.*)$', text, re.S)
    if not m:
        raise ValueError("no frontmatter: " + path)
    fm, body = m.group(1), m.group(2)
    meta = {}
    for line in fm.splitlines():
        if ':' in line:
            k, v = line.split(':', 1)
            meta[k.strip()] = v.strip().strip('"')
    sections = {}
    cur = None
    for line in body.splitlines():
        h = re.match(r'^##\s+(.*)', line)
        if h:
            cur = h.group(1).strip().lower()
            sections[cur] = []
        elif cur is not None:
            sections[cur].append(line)
    for k in sections:
        sections[k] = ' '.join(l.strip() for l in sections[k] if l.strip())
    return meta, sections

def esc(s):
    return html.escape(s or '', quote=True)

def block_html(meta, sections, idx):
    kind = meta.get('kind', 'smart-note')
    tone = meta.get('tone', '#9d75ff')
    glyph = meta.get('glyph', '🧠')
    title = meta.get('title', meta.get('ib', 'Untitled'))
    bid = 'ib-' + re.sub(r'[^a-z0-9]+', '-', meta.get('ib', 'x').lower()).strip('-')
    # Fan-out: personal (identified to owner) + collective (anonymized).
    # Demo renders the collective projection: provenance carries no identity.
    # kind=activity blocks default to the activity feed (her ACTIVITY mode).
    feed = meta.get('feed', 'activity' if kind == 'activity' else 'collective')
    provenance = meta.get('provenance', KIND_META.get(kind, 'SMART NOTE'))
    stream_label = KIND_META.get(kind, 'SMART NOTE')
    nutshell = sections.get('in a nutshell', '')
    layers = []
    for key, names in LAYERS:
        if names is None or key not in sections or not sections[key]:
            continue
        name, state = names
        layers.append(
            '<section class="layer" style="--layer:%s">'
            '<div class="layerHead"><i class="dot"></i><b>%s</b>'
            '<span class="state">%s</span></div>'
            '<div class="layerBody">%s</div></section>'
            % (tone, name, state, esc(sections[key])))
    actions = ''.join(
        '<button class="action%s" data-act="%s" data-id="%s">%s</button>' % (
            ' like' if a == 'like' else (' love' if a == 'love' else ''),
            a, bid, label)
        for a, label in [('favorite', '★ FAVORITE'), ('save', '🔖 SAVE'),
                         ('like', '👍 LIKE'), ('love', '♥ LOVE'),
                         ('rate', '★ RANK'), ('share', '＋ SHARE')])
    audience = 'ACTIVITY' if feed == 'activity' else 'COLLECTIVE'
    return (
        '<article class="block ib-block" id="%s" data-naya-direct-note="%d" '
        'data-real-smart-note="true" data-ib-id="%s" data-ib-kind="%s" '
        'data-naya-feed="%s" data-provenance="%s" style="--tone:%s">'
        '<div class="blockInner"><div class="blockTop"><div class="identity">'
        '<div class="glyph">%s</div><div><h3>%s</h3>'
        '<div class="meta"><span></span><span>·</span><span>%s · %s</span></div>'
        '</div></div><span class="truth">SOURCE SEPARATED</span></div>'
        '<div class="nutshell"><b>IN A NUTSHELL</b><p>%s</p></div>'
        '<div class="layers">%s</div>'
        '<div class="actions">%s</div>'
        '<div class="blockFoot"><span>ONE INTELLIGENCE · MANY VIEWS · ONE IDENTITY</span>'
        '<span>TRUST: SOURCE / INTERPRETATION SEPARATED</span></div>'
        '</div></article>'
        % (bid, 100 + idx, esc(meta.get('ib', '')), kind, feed,
           esc(provenance), tone,
           glyph, esc(title), stream_label, audience, esc(nutshell),
           ''.join(layers), actions))

def main():
    files = sorted(f for f in
                   glob.glob(os.path.join(IB_ROOT, '**', '*.md'), recursive=True)
                   if os.path.basename(f).lower() not in ('readme.md', 'index.md'))
    print('IB source files:', len(files))
    blocks = []
    for i, f in enumerate(files):
        meta, sections = parse_ib(f)
        blocks.append(block_html(meta, sections, i))
        print('  +', meta.get('ib'), meta.get('kind'), '-', meta.get('title', '')[:50])
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ib-blocks.html')
    open(out, 'w').write('\n'.join(blocks))
    print('wrote', out, sum(len(b) for b in blocks), 'bytes')

if __name__ == '__main__':
    main()
