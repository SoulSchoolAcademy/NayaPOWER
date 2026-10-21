#!/usr/bin/env python3
"""
Sync Smart Notes from GitHub to Supabase hub_smart_notes table.
Polls GitHub for notes in BRAIN/05-MEMORY/SMART-NOTES/, parses them,
and upserts to Supabase. This bridges the gap until the webhook is fixed.

====================================================================
VIRAL LAW — the headline standard for every note this pipeline touches
(Shawn, 2026-10-20 — standing law for ALL titles system-wide)
====================================================================
Humans read HEADLINES, not ID numbers. Every smart note carries:

  (a) HEADLINE — the note's real title, written like a showstopper:
      the one line a human stops scrolling for. Hook in the first
      breath; emotion over information; speaks to pain, desire, or
      identity; one powerful line over a thousand weak ones; clarity
      is king; passes "would I share this with a friend right now?"
      A label-style title ("The Naya Protocol — Ratified…") is a
      FAILING title. A truth-with-a-pulse line ("Words Without
      Action Have No Value") is the standard.
  (b) SUBHEADLINE — the second hook: the intelligent line that makes
      the headline land and makes the reader need the intelligence
      behind it. Drawn from the note's IN A NUTSHELL sharpest
      sentence. Boilerplate ("Live from Supabase") is PROHIBITED.
  (c) ID (IB-000047 / SN-0803) — metadata. Small print only.
      NEVER the display headline. A title equal to its own ID is a
      data defect and must be derived from the note's content.

Headline + hook are SCORECARD items: draft, score against the viral
principles, revise through the passes until honestly elite (9.5+).
This pipeline enforces the floor mechanically: titles come from the
note's Subject/headline (never the bare ID), and the Hub bake derives
the subtitle hook from the nutshell — never a boilerplate string.
====================================================================
FEED TRUTH (Shawn, 2026-10-20) — the feed must tell the truth about
every note it carries:
  (1) A card ALWAYS says what the note is ABOUT. A type ("Smart
      Note"), a kind ("Intelligent Block: SN-0305"), or a bare ID
      ("IB-000037") NEVER headlines. Generic titles are data defects:
      at ingest they are replaced by the note's own real title (its
      Subject / metadata title / Intelligent Block title line /
      heading), and if none exists, derived from its own nutshell.
  (2) Categorize by TOPIC — the note's own category (its Category
      field, else its folder taxonomy) — never by what the thing IS,
      never the junk bucket "Features".
  (3) ALL notes in the corpus ingest — no "newest N" window silently
      dropping notes. Change detection (tree blob SHA + parser
      version) keeps repeat runs cheap: unchanged notes are skipped,
      never re-fetched, never re-baked over.
  (4) Shawn's personal-superbrain notes are BOTH personal AND
      collective: notes filed in his personal philosophy corpus
      (top-level PHILOSOPHY / PHILOSOPHY-LIFE taxonomy — his thesis,
      his Codex, his Awesome Code; the thesis note's own metadata
      names him as author) bake with personal:true AND stay in the
      collective feed (the Personal lens filters, Collective shows
      all — personal is additive, never a silo).
====================================================================
"""
import os, sys, json, re, base64
import urllib.request
from datetime import datetime

sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
from dynamic_credentials import add_surrogate_to_request

SUPABASE_URL = 'https://dahisasgpfvziswqvmvm.supabase.co'
# Supabase auth injected at request time via add_surrogate_to_request (custom.supabase-anon)

# Change detection: a note is re-fetched/re-upserted only when its
# GitHub blob SHA changes OR the parser version bumps (a parser fix
# must reprocess the corpus once, then go quiet again).
PARSER_VERSION = 'feed-truth-2026-10-20-v4'
STATE_PATH = os.path.expanduser('~/workspace/factory-pipeline/.sync-state.json')


def load_state():
    try:
        s = json.load(open(STATE_PATH))
        if s.get('parser_version') != PARSER_VERSION:
            return {}
        return s.get('files', {})
    except Exception:
        return {}


def save_state(files):
    try:
        with open(STATE_PATH, 'w') as f:
            json.dump({'parser_version': PARSER_VERSION, 'files': files}, f)
    except Exception as e:
        print(f"  ⚠ state save failed: {str(e)[:80]}")


def gh_api(path):
    """Call GitHub API with App token."""
    # Get token via the helper
    import subprocess
    tok = subprocess.check_output(
        [os.path.expanduser("~/workspace/custom-connectors/custom.legacy-github/bin/gh-app-token")],
        text=True
    ).strip()

    req = urllib.request.Request(
        f"https://api.github.com/repos/SoulSchoolAcademy/NayaPOWER{path}",
        headers={"Authorization": f"Bearer {tok}", "Accept": "application/vnd.github.v3+json"}
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())

def sb_upsert(note):
    """Upsert a note to hub_smart_notes.

    Only non-None fields are sent: merge-duplicates would otherwise
    overwrite good columns (written by the canonical IB projection)
    with nulls for sections this parser could not extract.
    """
    note = {k: v for k, v in note.items() if v is not None}
    req = urllib.request.Request(
        f"{SUPABASE_URL}/rest/v1/hub_smart_notes?on_conflict=ib_id",
        data=json.dumps(note).encode(),
        method='POST',
        headers={
            'Content-Type': 'application/json',
            'Prefer': 'resolution=merge-duplicates,return=representation'
        }
    )
    add_surrogate_to_request(req, "custom.supabase-anon", allowed_hosts=["dahisasgpfvziswqvmvm.supabase.co"])
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())

def first_sentence(text, cap=200):
    """First sentence of a text block, whitespace-collapsed, capped."""
    if not text:
        return None
    flat = ' '.join(str(text).split())
    m = re.split(r'(?<=[.!?])\s+', flat)
    s = m[0] if m else flat
    return s[:cap] if s else None


def strip_id_prefix(t):
    """Remove a leading ID prefix from a title candidate:
    'IB-SMART-NOTE — SN-0568 — Highest Score Wins' -> 'Highest Score
    Wins'; 'SN-0412 — Field Stripping Is Deletion' -> 'Field
    Stripping Is Deletion'. Content mentions ('SN-0459 exists in
    git history…') are untouched — the pattern demands the dash."""
    if not t:
        return t
    s = str(t).strip()
    s = re.sub(r'^IB-SMART-NOTE\s*[—–-]\s*(?:SN|IB)-?[\w-]+\s*[—–-]\s*',
               '', s, flags=re.IGNORECASE)
    # Bare form: 'IB-SMART-NOTE — The Three Agreements of Connecting'
    # (spaced dash required — the hyphenated filename form is an ID,
    # handled as generic, never stripped into a fake title.)
    s = re.sub(r'^IB-SMART-NOTE\s+[—–]\s*', '', s, flags=re.IGNORECASE)
    s = re.sub(r'^(?:SN|IB)-?\d+\s*[—–:-]\s*', '', s)
    return s.strip()


def derive_headline(text, cap=90):
    """Derive a headline from a note's own words: its first sentence,
    cleaned of markdown furniture (leading '#'s, '**', a leading
    generic label like 'Smart Note —') and cut at a word boundary
    without leaving a dangling parenthesis."""
    s = first_sentence(text, 400)
    if not s:
        return None
    s = s.replace('**', '').strip()
    s = re.sub(r'^#+\s*', '', s)
    s = re.sub(r'^(smart note|intelligent block|intelligent note)\s*[—–:-]\s*',
               '', s, flags=re.IGNORECASE)
    s = strip_id_prefix(s)
    if len(s) > cap:
        cut = s[:cap]
        sp = cut.rfind(' ')
        if sp > cap * 0.5:
            cut = cut[:sp]
        if cut.count('(') > cut.count(')'):
            cut = cut[:cut.rfind('(')].rstrip()
        s = cut.rstrip(' —–-')
    return s or None


# --------------------------------------------------------------------
# FEED TRUTH helpers — one rule set shared by ingest and the Hub bake.
# --------------------------------------------------------------------

_GENERIC_EXACT = {
    '', 'smart note', 'smart notes', 'intelligent note',
    'intelligent block', 'intelligent blocks',
    'untitled', 'untitled intelligence',
}


def is_generic_title(t, ib_id='', filename=''):
    """True when a title carries no information about the note: a type
    label, a kind label, the bare ID, the filename, or label + ID."""
    if not t:
        return True
    s = ' '.join(str(t).split()).strip().strip('`"\' ')
    low = s.lower()
    if low in _GENERIC_EXACT:
        return True
    if ib_id and (s == ib_id or s == ib_id + '.md'):
        return True
    if filename and (s == filename or s == filename + '.md'):
        return True
    if low.startswith('ib-smart-note-'):
        return True  # filename-as-title
    if re.fullmatch(r'(IB|SN)-?\d+', s, re.IGNORECASE):
        return True  # bare ID
    if re.fullmatch(r'(intelligent block|smart note)\s*[:#—–-]?\s*((IB|SN)-?[\w-]*)?',
                    s, re.IGNORECASE):
        return True  # label + optional ID, nothing else
    return False


def _taxonomy(path):
    """Folder taxonomy below SMART-NOTES/YYYY/MM/DD/, minus the
    SN-#### / IB-#### leaf folder. Works for repo and local paths."""
    if not path or 'SMART-NOTES/' not in path:
        return []
    seg = path.split('SMART-NOTES/')[-1].split('/')
    tax = seg[3:-1] if len(seg) > 3 else []
    return [t for t in tax if not re.fullmatch(r'(SN|IB)-\d+', t or '')]


def _humanize_topic(seg):
    special = {'nayanet': 'NayaNET', 'nayapower': 'NayaPOWER',
               'ci': 'CI', 'ai': 'AI', 'api': 'API'}
    out = []
    for w in re.split(r'[-_]', seg or ''):
        if not w:
            continue
        lw = w.lower()
        if lw in special:
            out.append(special[lw])
        elif w.isdigit():
            out.append(w)
        else:
            out.append(lw.capitalize())
    return ' '.join(out) or 'System'


def topic_for_path(path):
    """The note's REAL category from its own filing: the taxonomy
    level directly under the collection root (Governance, CI Triage,
    Human Nexus, Viral Law…). The IB projections filed under the
    lowercase system/ root carry no subject folder — their category
    is System. Never 'Features', never the note's type."""
    tax = _taxonomy(path)
    if not tax:
        return 'System'
    if tax[0] == 'system':
        return 'System'
    if len(tax) >= 2:
        return _humanize_topic(tax[1])
    return _humanize_topic(tax[0])


def personal_for_path(path):
    """Shawn's personal-superbrain corpus: notes filed in his personal
    philosophy taxonomy (PHILOSOPHY / PHILOSOPHY-LIFE) — his thesis,
    his Human Nexus Codex, his Awesome Code — outside the system
    taxonomy. (Cross-check: the thesis note's own metadata table names
    'Shawn Vibert' as author; the Codex notes record 'Shawn shared…'
    at Scope PRIVATE.) Personal is additive: the record stays in the
    collective feed; the Personal lens additionally selects it."""
    tax = _taxonomy(path)
    return bool(tax) and tax[0] in ('PHILOSOPHY', 'PHILOSOPHY-LIFE')


def _norm_section_name(h):
    """'## ✦ IN A NUTSHELL' / '## Human view' -> 'IN A NUTSHELL' /
    'HUMAN VIEW' (emoji and punctuation stripped, case folded)."""
    h = re.sub(r'[^a-z0-9]+', ' ', (h or '').lower())
    return ' '.join(h.split()).upper()


def section_index(content):
    """Map normalized ## section name -> body. Handles both note
    dialects: the plain format (## IN A NUTSHELL, ## HUMAN NOTE) and
    the capture format (## ✦ IN A NUTSHELL, ## 🩷 HUMAN NOTE), plus
    the IB projection views (## In a nutshell, ## Human view…)."""
    idx = {}
    for chunk in re.split(r'^##\s+', content, flags=re.MULTILINE)[1:]:
        head, _, body = chunk.partition('\n')
        name = _norm_section_name(head)
        if name and name not in idx:
            idx[name] = body.strip()
    return idx


def _pick(idx, *names):
    for n in names:
        if idx.get(n):
            return idx[n]
    for n in names:  # combined headers: 'HOW TO APPLY HOW TO USE'
        for k, v in idx.items():
            if v and k.startswith(n):
                return v
    return None


def parse_smart_note(content, path):
    """Parse Smart Note markdown into structured fields.

    VIRAL LAW + FEED TRUTH (see module docstring): the title is the
    note's real HEADLINE, taken from the note's own words in order —
    ## Subject (IB projections) → the metadata-table | title | row →
    the **Intelligent Block:** SN-#### — <title> line → the first
    # heading — with generic labels rejected at every step. If no
    real title exists, the headline is derived from the note's own
    nutshell. Canonical ID: folder name for IB projection notes
    (.../IB-000047/smart-note.md), filename for SN-era notes.
    """
    filename = path.split('/')[-1].replace('.md', '')
    folder = path.split('/')[-2] if '/' in path else ''

    # Tombstone stubs (a superseded duplicate whose content was
    # intentionally replaced by a pointer to the canonical file) are
    # NOT notes — never ingest them as feed cards.
    head = content[:600]
    if ('<!-- TOMBSTONE' in head or '**Status:** SUPERSEDED' in head
            or re.search(r'^#\s+SUPERSEDED\b', content, re.MULTILINE)):
        return {'ib_id': None, 'tombstone': True, 'github_path': path}

    folder_ib = re.fullmatch(r'IB-\d+', folder or '')
    if folder_ib:
        ib_id = folder
    else:
        ib_id = filename[:100]  # Truncate to fit

    idx = section_index(content)
    nutshell = _pick(idx, 'IN A NUTSHELL')
    human = _pick(idx, 'HUMAN NOTE', 'HUMAN', 'HUMAN VIEW')
    what_it_means = _pick(idx, 'WHAT IT ALL MEANS', 'WHAT IT MEANS')
    if not nutshell:
        # A card must always carry its nutshell: fall back to the
        # note's own summary dialects ('## Essence', '## Executive
        # intelligence'), then its human/what-it-means text, then the
        # first substantial section — rather than skip the note.
        nutshell = (_pick(idx, 'ESSENCE', 'EXECUTIVE INTELLIGENCE')
                    or human or what_it_means)
    if not nutshell:
        for k, v in idx.items():
            if v and len(v) >= 40 and k != 'SUBJECT':
                nutshell = v
                break

    # --- Title chain: the note's own real title, never a label ---
    subject = _pick(idx, 'SUBJECT')
    if subject:
        subject = ' '.join(subject.splitlines()[0].split()).strip() or None
    table_title = None
    m = re.search(r'^\|\s*title\s*\|\s*(.+?)\s*\|', content,
                  re.MULTILINE | re.IGNORECASE)
    if m:
        table_title = m.group(1).strip()
    ib_title = None
    m = re.search(r'^\*\*Intelligent Block:\*\*\s*(.+)$', content, re.MULTILINE)
    if m:
        raw = m.group(1).strip()
        # Strip only a numeric ID prefix ('SN-0305 — ', 'IB-000047 — ');
        # a full IB-SMART-NOTE-… filename in this slot is the ID itself,
        # not a title (the greedy-strip bug once yielded titles like
        # '001' / 'method' / 'gate' from filename tails).
        m2 = re.match(r'^(?:SN|IB)-?\d+\s*[—–:-]\s*(.+)$', raw)
        ib_title = (m2.group(1) if m2 else raw).strip()
    heading = None
    m = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if m:
        heading = m.group(1).strip()

    title = None
    for cand in (subject, table_title, ib_title, heading):
        if cand:
            cand = strip_id_prefix(' '.join(cand.split()).strip())
        if cand and not is_generic_title(cand, ib_id, filename):
            title = cand.replace('**', '').strip()
            # Strip leading furniture (emoji etc.) off the headline.
            while title and not (title[0].isalnum() or title[0] in '"“\'('):
                title = title[1:].lstrip()
            break
    if not title:
        title = derive_headline(nutshell, 90) or derive_headline(human, 90) \
            or 'Smart Note'

    return {
        'ib_id': ib_id,
        'title': title,
        'nutshell': nutshell,
        'human_note': human,
        'child_note': _pick(idx, 'CHILD NOTE', 'CHILD', 'SIMPLE VIEW'),
        'grandma_note': _pick(idx, 'GRANDMA NOTE', 'GRANDMA', 'EVERYDAY VIEW'),
        'naya_note': _pick(idx, 'NAYA NOTE', 'NAYA', 'NAYA VIEW'),
        'what_it_means': what_it_means,
        'whats_in_it_for_you': _pick(idx, 'WHATS IN IT FOR YOU'),
        'how_it_applies': _pick(idx, 'HOW IT APPLIES', 'HOW TO USE IT',
                                'HOW TO APPLY'),
        'source': 'github-sync',
        'github_path': path,
    }


# ---------------------------------------------------------------------------
# Bake-on-publish (Shawn 2026-10-21): rendering a note's voice is part of
# posting it — nobody's click should ever start the rendering. When a
# note newly syncs, enqueue its FULL spoken content (every section the
# board play speaks, playSections order, nutshell first) with the voice
# service, chunked exactly as the page chunks. The worker keys each
# chunk by sha256(chunk)[:16] and dedupes by key, so re-posting an
# unchanged chunk is free. Fire-and-forget: a voice failure must never
# fail the sync.
VOICE_SYNTHESIZE_URL = 'https://naya-voice.nayapower.workers.dev/synthesize'


def _md_text(raw):
    """Approximate the textContent of the Hub board's md() rendering:
    inline markdown markers are consumed by the tags they become, each
    non-empty line becomes a block, and blocks concatenate with no
    separator — exactly what textContent returns for that HTML."""
    if not raw:
        return ''
    t = str(raw)
    t = re.sub(r'\*\*([^*]+)\*\*', r'\1', t)
    t = re.sub(r'(^|\W)\*([^*\n]+)\*', r'\1', t)
    t = re.sub(r'`([^`]+)`', r'\1', t)
    parts = []
    for line in t.split('\n'):
        m = re.match(r'^\s*[-•]\s+(.*)', line)
        if m:
            parts.append(m.group(1))
        elif line.strip():
            parts.append(line.strip())
    return ''.join(parts)


def _chunk_text_js(text, maxlen=600):
    """Byte-for-byte port of NayaVoice._chunkText (whitespace-normalized,
    ~600 chars on sentence bounds)."""
    clean = re.sub(r'\s+', ' ', str(text or '')).strip()
    if not clean:
        return []
    if len(clean) <= maxlen:
        return [clean]
    out = []
    rest = clean
    while len(rest) > maxlen:
        cut = rest.rfind('. ', 0, maxlen + 2)
        if cut < maxlen * 0.4:
            cut = rest.rfind(' ', 0, maxlen + 1)
        if cut <= 0:
            cut = maxlen
        out.append(rest[:cut + 1].strip())
        rest = rest[cut + 1:].strip()
    if rest:
        out.append(rest)
    return out


# (note field, layer name) in the exact order update_hub_and_deploy
# bakes the layers and the board renders — and speaks — them.
_SPOKEN_LAYERS = [
    ('human_note', 'Human Note'),
    ('child_note', 'Child Note'),
    ('grandma_note', 'Grandma Note'),
    ('naya_note', 'Naya Note'),
    ('machine_note', 'Machine Note'),
    ('what_it_means', 'What It Means'),
    ('whats_in_it_for_you', "What's In It For You"),
    ('how_it_applies', 'How It Applies'),
]


def spoken_sections(note):
    """The sections the board play speaks for this note, in order: the
    nutshell element first ('IN A NUTSHELL' label + the body's first
    600 chars as rendered), then each layer as 'Name. body'."""
    sections = []
    nutshell = note.get('nutshell')
    if nutshell:
        sections.append('IN A NUTSHELL' + _md_text(str(nutshell)[:600]))
    for field, name in _SPOKEN_LAYERS:
        body = note.get(field)
        if not body:
            continue
        if isinstance(body, dict):
            body = json.dumps(body, indent=2)
        sections.append(name + '. ' + _md_text(str(body)))
    return sections


def spoken_chunks(note):
    """All chunks the board play would request, in speak order —
    the nutshell chunks come first, so the most-played layer's voice
    lands first."""
    chunks = []
    for section in spoken_sections(note):
        chunks.extend(_chunk_text_js(section))
    return chunks


def enqueue_note_voice(note):
    """POST every spoken chunk of a newly-synced note to /synthesize.
    Returns the number of chunks posted. Never raises."""
    posted = 0
    for chunk in spoken_chunks(note):
        # One retry: the edge drops ~1 in 6 connections from this box,
        # and the worker dedupes by key, so a retry is always free.
        err = None
        for _attempt in range(2):
            try:
                req = urllib.request.Request(
                    VOICE_SYNTHESIZE_URL,
                    data=json.dumps({'text': chunk}).encode(),
                    method='POST',
                    headers={'Content-Type': 'application/json',
                             'User-Agent': 'naya-sync-bake-on-publish'})
                with urllib.request.urlopen(req, timeout=15) as resp:
                    resp.read()
                err = None
                break
            except Exception as e:
                err = e
        if err is None:
            posted += 1
        else:
            print(f"  ⚠ Voice enqueue chunk failed: {str(err)[:60]}")
    if posted:
        print(f"  ♪ Voice enqueue: {posted} chunk(s) for {note.get('ib_id')}")
    return posted


def generate_share_assets(note):
    """Generate share image and update manifest for a Smart Note.
    Called when a new note is synced. Makes the note shareable with a beautiful OG image.
    """
    import subprocess
    import tempfile

    # Extract sn ID from ib_id (e.g., IB-SMART-NOTE-20261019-sn0798-... -> sn0798)
    ib_id = note.get('ib_id', '')
    m = re.search(r'sn(\d+)', ib_id, re.IGNORECASE)
    if m:
        sn_id = f"sn{m.group(1)}"
    else:
        # Projection-era notes carry IB-##### ids with no sn#### component.
        # Their share key is ib + the zero-padded number (ib000051), matching
        # the keys already in the manifest for IB-000040..49. (Before this
        # fallback, IB-000050/51/52 silently got no share page — found and
        # fixed during the 2026-10-21 home cleanup.)
        m_ib = re.search(r'IB-(\d+)', ib_id, re.IGNORECASE)
        if not m_ib:
            print(f"  ⚠ No sn or IB ID in {ib_id}, skipping share assets")
            return False
        sn_id = f"ib{m_ib.group(1).zfill(6)}"
    title = note.get('title', 'NayaNET Intelligence')
    nutshell = note.get('nutshell', '') or note.get('human_note', '')[:200]
    # Clean nutshell for image (remove newlines, truncate)
    nutshell = ' '.join(nutshell.split())[:200]

    try:
        # 1. Generate the share image
        img_path = f"/tmp/{sn_id}-share.png"
        result = subprocess.run(
            ['python3', '/home/hatch/workspace/factory-pipeline/generate-share-card.py',
             title, nutshell, img_path],
            capture_output=True, text=True, timeout=60
        )
        if result.returncode != 0 or not os.path.exists(img_path):
            print(f"  ⚠ Share image generation failed for {sn_id}")
            return False

        # 2. Upload to R2
        upload = subprocess.run(
            ['curl', '-s', '-X', 'POST',
             f'https://naya-share.nayapower.workers.dev/upload/{sn_id}-share.png',
             '-H', 'x-upload-secret: naya-share-upload-2026',
             '-H', 'Content-Type: image/png',
             '--data-binary', f'@{img_path}'],
            capture_output=True, text=True, timeout=30
        )
        if '"ok":true' not in upload.stdout:
            print(f"  ⚠ Share image upload failed for {sn_id}")
            return False

        # 3. Update manifest.json in R2
        # Download current manifest
        dl = subprocess.run(
            ['curl', '-s', 'https://naya-share.nayapower.workers.dev/manifest.json'],
            capture_output=True, text=True, timeout=15
        )
        try:
            manifest = json.loads(dl.stdout) if dl.stdout.strip() else {}
        except:
            manifest = {}

        # Add/update this note
        manifest[sn_id] = {
            'title': title,
            'description': nutshell[:200],
        }

        # Upload updated manifest
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(manifest, f)
            manifest_path = f.name

        up = subprocess.run(
            ['curl', '-s', '-X', 'POST',
             'https://naya-share.nayapower.workers.dev/upload/manifest.json',
             '-H', 'x-upload-secret: naya-share-upload-2026',
             '-H', 'Content-Type: application/json',
             '--data-binary', f'@{manifest_path}'],
            capture_output=True, text=True, timeout=30
        )
        os.unlink(manifest_path)
        os.unlink(img_path)  # Clean up temp image

        if '"ok":true' in up.stdout:
            print(f"  ✓ Share assets ready for {sn_id}: nayanet.live/s/{sn_id}")
            return True
        else:
            print(f"  ⚠ Manifest update failed for {sn_id}")
            return False

    except Exception as e:
        print(f"  ⚠ Share assets error for {sn_id}: {str(e)[:60]}")
        return False


def update_hub_and_deploy():
    """Fetch live notes, inject into Hub HTML, and redeploy.

    Clean approach (no paren-balancing fragility):
      Original:  const NOTES = OFFICIAL_NOTES.concat([...]);
      Re-baked:  const NOTES_BASE = OFFICIAL_NOTES.concat([...]);
                 const NOTES = <LIVE_JSON>.concat(NOTES_BASE);
    Removal reverses both edits, so re-runs are idempotent.
    A node --check syntax gate runs before every deploy.

    FEED TRUTH: the bake covers the WHOLE table (no limit window),
    drops stale duplicate rows (same github_path, non-canonical ID —
    artifacts of older parsers), replaces generic titles with the
    note's own derived headline, and stamps each record with its
    REAL topic + personal flag derived from its own filing path.
    """
    import subprocess

    print("\n--- Updating Hub with live notes ---")

    # Step 1: Fetch ALL live notes from Supabase (no window)
    import urllib.request, json
    SUPABASE_URL = 'https://dahisasgpfvziswqvmvm.supabase.co'
    # Auth via surrogate (custom.supabase-anon)

    req = urllib.request.Request(
        f"{SUPABASE_URL}/rest/v1/hub_smart_notes?order=created_at.desc&limit=1000"
    )
    add_surrogate_to_request(req, "custom.supabase-anon", allowed_hosts=["dahisasgpfvziswqvmvm.supabase.co"])
    with urllib.request.urlopen(req, timeout=30) as resp:
        notes = json.loads(resp.read().decode())

    if not notes:
        print("No live notes to inject, skipping Hub update")
        return True

    # Step 2: Build safely-escaped notes (escape </script, strip control chars)
    def clean(text):
        if not text:
            return ""
        text = text.replace('</script', '<\\/script')
        text = ''.join(c for c in text if c == '\n' or c == '\t' or ord(c) >= 32)
        return text[:500]

    def canonical_id_for(path):
        if not path:
            return None
        fn = path.split('/')[-1].replace('.md', '')
        fo = path.split('/')[-2] if '/' in path else ''
        return fo if re.fullmatch(r'IB-\d+', fo or '') else fn[:100]

    live_notes = []
    seen_paths = set()
    dropped = 0
    for row in notes:
        # Stale-duplicate guard: one card per source file, under its
        # canonical ID. (The 'smart-note' and 'IB-SMART-NOTE-20261004-'
        # rows were old-parser duplicates of IB-000038 and the thesis.)
        rpath = row.get('github_path') or ''
        if rpath:
            if row.get('ib_id') != canonical_id_for(rpath) or rpath in seen_paths:
                dropped += 1
                continue
            seen_paths.add(rpath)

        layers = []
        if row.get('nutshell'):
            layers.append({"name": "In A Nutshell", "key": "IN A NUTSHELL", "color": "white", "tier": "primary", "body": row['nutshell']})
        if row.get('human_note'):
            layers.append({"name": "Human Note", "key": "HUMAN NOTE", "color": "magenta", "tier": "primary", "body": row['human_note']})
        if row.get('child_note'):
            layers.append({"name": "Child Note", "key": "CHILD NOTE", "color": "sapphire", "tier": "primary", "body": row['child_note']})
        if row.get('grandma_note'):
            layers.append({"name": "Grandma Note", "key": "GRANDMA NOTE", "color": "emerald", "tier": "primary", "body": row['grandma_note']})
        if row.get('naya_note'):
            layers.append({"name": "Naya Note", "key": "NAYA NOTE", "color": "purple", "tier": "primary", "body": row['naya_note']})
        if row.get('machine_note'):
            # machine_note is JSONB, convert to string
            machine = row['machine_note']
            if isinstance(machine, dict):
                import json as js
                machine = js.dumps(machine, indent=2)
            layers.append({"name": "Machine Note", "key": "MACHINE NOTE", "color": "indigo", "tier": "deeper", "body": str(machine)})
        if row.get('what_it_means'):
            layers.append({"name": "What It Means", "key": "WHAT IT MEANS", "color": "indigo", "tier": "deeper", "body": row['what_it_means']})
        if row.get('whats_in_it_for_you'):
            layers.append({"name": "What's In It For You", "key": "WHATS IN IT FOR YOU", "color": "gold", "tier": "deeper", "body": row['whats_in_it_for_you']})
        if row.get('how_it_applies'):
            layers.append({"name": "How It Applies", "key": "HOW IT APPLIES", "color": "teal", "tier": "deeper", "body": row['how_it_applies']})

        # VIRAL LAW + FEED TRUTH: headline = the note's real title.
        # A generic title (a type, a kind, the bare ID, the filename)
        # is a data defect — derive the headline from the note's own
        # nutshell. Subtitle = the hook line, the nutshell's sharpest
        # first sentence. Boilerplate ("Live from Supabase") is
        # prohibited. Topic + personal come from the note's own filing.
        row_id = clean(row.get('ib_id', 'unknown'))
        row_title = clean(row.get('title', '') or '')
        stem = rpath.split('/')[-1].replace('.md', '') if rpath else ''
        if is_generic_title(row_title, row_id, stem):
            row_title = clean(derive_headline(row.get('nutshell'), 90)
                              or derive_headline(row.get('human_note'), 90)
                              or 'Smart Note')
        hook = derive_headline(row.get('nutshell'), 160)
        if not hook or hook == row_title:
            hook = derive_headline(row.get('human_note'), 160)
        topic = topic_for_path(rpath)
        live_notes.append({
            "id": row_id,
            "title": row_title,
            "subtitle": clean(hook or ''),
            "topics": [topic],
            "topic": topic,
            "tone": "purple",
            "icon": "note",
            "kind": "official",
            "personal": personal_for_path(rpath),
            "layers": layers
        })
    if dropped:
        print(f"Dropped {dropped} stale duplicate row(s) at bake")

    live_json = json.dumps(live_notes, separators=(',', ':'), ensure_ascii=True)

    # Step 3: Edit Hub HTML (idempotent remove-then-inject)
    # (module-level `re` — a local import here once shadowed it and
    # broke canonical_id_for with an UnboundLocalError at bake time.)
    hub_path = '/home/hatch/workspace/user/files/index-2.html'
    with open(hub_path, 'r') as f:
        html = f.read()

    # 3a. Remove any previous live injection
    html = re.sub(
        r'const NOTES = \[.*?\]\.concat\(NOTES_BASE\);\n',
        '',
        html, flags=re.DOTALL, count=1,
    )
    html = html.replace(
        'const NOTES_BASE = OFFICIAL_NOTES.concat([',
        'const NOTES = OFFICIAL_NOTES.concat([',
        1,
    )

    # 3b. Inject fresh: rename base, then prepend live array
    if 'const NOTES_BASE = OFFICIAL_NOTES.concat([' in html:
        raise RuntimeError("Hub HTML still has NOTES_BASE after cleanup - aborting")
    if html.count('const NOTES = OFFICIAL_NOTES.concat([') != 1:
        raise RuntimeError("NOTES definition anchor not unique - aborting")
    html = html.replace(
        'const NOTES = OFFICIAL_NOTES.concat([',
        'const NOTES_BASE = OFFICIAL_NOTES.concat([',
        1,
    )
    anchor = 'window.NayaFeedIntelligence = { notes: NOTES'
    if anchor not in html:
        raise RuntimeError("NayaFeedIntelligence anchor not found - aborting")
    html = html.replace(
        anchor,
        'const NOTES = ' + live_json + '.concat(NOTES_BASE);\n  ' + anchor,
        1,
    )

    with open(hub_path, 'w') as f:
        f.write(html)

    print(f"Injected {len(live_notes)} live notes into Hub HTML")

    # Step 4: Syntax-check the edited script block before deploying
    idx = html.find('const NOTES_BASE = ')
    s_start = html.rfind('<script>', 0, idx)
    s_end = html.find('</script>', idx)
    with open('/tmp/hub_notes_check.js', 'w') as f:
        f.write(html[s_start + len('<script>'):s_end])
    chk = subprocess.run(['node', '--check', '/tmp/hub_notes_check.js'],
                         capture_output=True, text=True, timeout=30)
    if chk.returncode != 0:
        raise RuntimeError(f"Hub JS syntax check FAILED, aborting deploy: {chk.stderr[:300]}")
    print("Hub JS syntax check passed")

    # Step 5: Deploy the Hub
    print("Deploying Hub...")
    result = subprocess.run(
        ['python3', '/home/hatch/workspace/factory-pipeline/deploy.py',
         hub_path, 'hub'],
        capture_output=True, text=True, timeout=60
    )
    if result.returncode == 0:
        print("Hub deployed successfully")
        return True
    else:
        print(f"Deploy failed: {result.stderr[:200]}")
        return False


def sync_notes():
    """Main sync: find ALL Smart Notes on GitHub, upsert to Supabase.

    FEED TRUTH (3): the whole SMART-NOTES/2026/10 corpus ingests —
    the old newest-20 window silently dropped notes (Shawn's thesis
    among them). Blob-SHA change detection keeps the 5-minute cron
    cheap: unchanged notes are skipped without a fetch.
    """
    print("Syncing Smart Notes from GitHub to Supabase...")

    synced = 0
    skipped = 0
    tombstones = 0
    errors = 0

    try:
        tree = gh_api("/git/trees/main?recursive=1")

        blobs = {
            t['path']: t.get('sha') for t in tree.get('tree', [])
            if 'SMART-NOTES/2026/10' in t['path']
            and t['path'].endswith('.md')
            and t['type'] == 'blob'
        }

        print(f"Found {len(blobs)} Smart Note files on GitHub")

        # Newest-first: paths are zero-padded YYYY/MM/DD, so reverse
        # alphabetical order puts today's notes first (and makes
        # first-time backfill insert in feed order).
        state = load_state()
        for filepath in sorted(blobs, reverse=True):
            sha = blobs[filepath]
            if sha and state.get(filepath) == sha:
                skipped += 1
                continue
            try:
                # Get file content
                file_data = gh_api(f"/contents/{filepath}?ref=main")
                content = base64.b64decode(file_data['content']).decode('utf-8')

                # Parse and upsert
                note = parse_smart_note(content, filepath)
                if note.get('tombstone'):
                    tombstones += 1
                    if sha:
                        state[filepath] = sha
                    print(f"  ⊘ {filepath.split('/')[-1]}: tombstone stub, skipped")
                elif note['nutshell'] or note['human_note']:  # Only sync if it has content
                    sb_upsert(note)
                    synced += 1
                    if sha:
                        state[filepath] = sha
                    print(f"  ✓ {note['ib_id']}: {note['title'][:50]}")
                    # Generate share assets (beautiful OG image) for new notes
                    try:
                        generate_share_assets(note)
                    except Exception as e:
                        print(f"  ⚠ Share assets skipped: {str(e)[:60]}")
                    # Bake-on-publish: the voice renders as part of
                    # posting, so the first click is already instant.
                    try:
                        enqueue_note_voice(note)
                    except Exception as e:
                        print(f"  ⚠ Voice enqueue skipped: {str(e)[:60]}")
                else:
                    errors += 1
                    print(f"  ✗ {filepath}: no content sections parsed")
            except Exception as e:
                errors += 1
                print(f"  ✗ {filepath}: {str(e)[:80]}")

        save_state(state)

    except Exception as e:
        print(f"Sync failed: {str(e)[:200]}")
        return False

    print(f"\nSynced {synced} notes, skipped {skipped} unchanged, "
          f"{tombstones} tombstone(s), {errors} errors")

    # Update Hub with live notes and redeploy when new notes arrived
    if synced > 0:
        try:
            update_hub_and_deploy()
        except Exception as e:
            print(f"Hub re-bake failed (non-fatal): {str(e)[:200]}")

    return True

if __name__ == '__main__':
    success = sync_notes()
    sys.exit(0 if success else 1)
