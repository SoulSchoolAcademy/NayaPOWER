#!/usr/bin/env python3
"""CARD-LABELS-FIX grep audit v2 (maker, 2026-11-13).
For every inventoried render site, asserts the MARKED form exists in the
built file (data-mw-tr + pinned data-mw-en, data-mw-ph, data-mw-aria, or
an mwTr() routing through the shared btn()). The bare English string
legitimately survives in three places — the MW_I18N dict key itself, the
data-mw-en pin, and the mwTr() fallback — so "string present" is not the
test; the marked form is. Sites routed through the shared BoardActions
btn() are proven once (btn marks + translates) and their defs are checked
against the dictionary instead.
"""
import json, re

WORK = '/home/hatch/workspace/team-nitro/auto-translate-20261113/'
BASE = WORK + 'captain-fix-staged-check.html'
FIX = '/tmp/cardfix-built.html'
DICT = WORK + 'dict-final.json'

# (site, marked-pattern regex, expected count in FIX)
MARKED = [
    ('IN A NUTSHELL intelBoard <b>',
     r'<b data-mw-tr="set" data-mw-en="IN A NUTSHELL">', 1),
    ('IN A NUTSHELL ibFeedCard label x2',
     r'<span class="ib-nutshell-label" data-mw-tr="set" data-mw-en="IN A NUTSHELL">', 2),
    ('IN A NUTSHELL noteCard <p>',
     r'<p class="ph-nutshell" data-mw-tr="set" data-mw-en="IN A NUTSHELL">', 1),
    ('IN A NUTSHELL sa lesson x3',
     r'<span class="ph-nl" data-mw-tr="set" data-mw-en="IN A NUTSHELL">', 3),
    ('ONE INTELLIGENCE microcopy',
     r'data-mw-en="ONE INTELLIGENCE · MANY VIEWS · ONE IDENTITY"', 1),
    ('TRUST microcopy',
     r'data-mw-en="TRUST: SOURCE / INTERPRETATION SEPARATED"', 1),
    ('ADD TO THE INTELLIGENCE heading',
     r"dataset\.mwEn = 'ADD TO THE INTELLIGENCE'", 1),
    ('Be the first to add intel... empty',
     r"dataset\.mwEn = 'Be the first to add intel\.\.\.'", 1),
    ('Add an observation... placeholder',
     r"dataset\.mwEn = 'Add an observation, question, correction, or contribution\.\.\.'", 1),
    ('Add to the intelligence aria',
     r"setAttribute\('data-mw-aria', 'Add to the intelligence'\)", 1),
    ('Rate this intelligence... aria',
     r"setAttribute\('data-mw-aria', 'Rate this intelligence from one to five stars'\)", 1),
    ('FILE UNDER A CATEGORY head',
     r"dataset\.mwEn = 'FILE UNDER A CATEGORY'", 1),
    ('Presented by Naya chip x2',
     r'data-mw-en="Presented by Naya"', 2),
    ('Smart Note foot',
     r'data-mw-en="Smart Note"', 1),
    ('Official NayaNET Guide foot',
     r'data-mw-en="Official NayaNET Guide"', 1),
    ('from your Smart Feed foot',
     r'data-mw-en="from your Smart Feed"', 1),
    ('from the Intelligent Library foot',
     r'data-mw-en="from the Intelligent Library"', 1),
    ('Note <id> meta',
     r'data-mw-en="Note"', 1),
    ('YOUR WORDS, WORD FOR WORD summary',
     r'data-mw-en="YOUR WORDS, WORD FOR WORD"', 1),
    ('DISTILLED... microcopy',
     r'data-mw-en="DISTILLED FROM THE AUTHOR', 1),
    ('YOUR WORDS — FORMATTED... fidelity',
     r'data-mw-en="YOUR WORDS — FORMATTED BEAUTIFULLY BY NAYA"', 1),
    ('Save to list (ibFeedCard)',
     r'data-mw-en="Save to list"', 1),
    ('Pin/Unpin (ibFeedCard)',
     r"data-mw-en=\"'\+ \(post\.pinned\?'Unpin':'Pin'\) \+'\"", 0),  # see note below
    ('Space from this (ibFeedCard)',
     r'data-mw-en="Space from this"', 1),
    ('Business from this (ibFeedCard)',
     r'data-mw-en="Business from this"', 1),
    ('Add a comment… placeholder (ibFeedCard)',
     r'data-mw-en="Add a comment…"', 1),
    ('Send (ibFeedCard)',
     r'data-mw-en="Send"', 1),
    ('Comment fallback (ibFeedCard)',
     r'data-mw-en="Comment"', 1),
    ('Share (ibFeedCard)',
     r'data-mw-en="Share"', 1),
    ('OWNER badge (ibFeedCard)',
     r'data-mw-en="OWNER"', 1),
    ('PINNED badge (ibFeedCard)',
     r'data-mw-en="PINNED"', 1),
    ('kind spans x2 (ibFeedCard kind div + microcopy)',
     r"data-mw-en=\"'\+kind\+'\"", 2),
    ('Layer heads (intelBoard)',
     r"data-mw-en=\"' \+ esc\(L\.name\) \+ '\"", 1),
    ('Layer heads (ibFeedCard)',
     r"data-mw-en=\"'\+esc\(L\.head\|\|'Detail'\)\+'\"", 1),
    ('Save/Saved (noteCard) [literal]',
     'LITERAL::data-mw-en="\'+(isSaved?\'Saved \u2713\':\'Save\')+\'"', 1),
    ('List (noteCard)',
     r'data-mw-en="List"', 1),
    ('In: prefix (noteCard slInLine)',
     r'data-mw-en="In:"', 1),
    ('IN: (ibFeedCard microcopy)',
     r'data-mw-en="IN:"', 1),
    ('All notes (ibCatBarHTML)',
     r'data-mw-en="All notes"', 1),
    ('+ List (ibCatBarHTML)',
     r'data-mw-en="\+ List"', 1),
    ('btn() marks label span (shared)',
     r"lab\.setAttribute\('data-mw-tr', 'set'\)", 1),
    ('btn() marks aria (shared)',
     r"b\.setAttribute\('data-mw-aria', ariaLabel \|\| label\)", 1),
    ('mwApplyLang [data-mw-aria] pass',
     r"querySelectorAll\('\[data-mw-aria\]'\)", 1),
]

# btn()-routed labels: defs stay as data, btn() translates at creation.
# Assert each def label exists in the dictionary (all three languages).
BTN_LABELS = ['\uff0b CREATE SPACE', '\u2605 FAVORITE', 'SAVE',
              '\u2764\ufe0f LOVE', '\U0001f44d LIKE', '\uff0b SHARE INTEL',
              'ADD INTEL', 'ADD TO THE INTELLIGENCE']
BTN_ARIA = ['Create a smart space from this intelligence', 'Mark as favorite',
            'Save this intelligence', 'Share this intelligence',
            'Add your contribution']

fix = open(FIX, encoding='utf-8', errors='replace').read()
base = open(BASE, encoding='utf-8', errors='replace').read()
d = json.load(open(DICT, encoding='utf-8'))
bad = 0
print('%-48s %6s %6s' % ('marked form (FIX)', 'want', 'got'))
for label, pat, want in MARKED:
    if want == 0:
        continue
    if pat.startswith('LITERAL::'):
        got = fix.count(pat[len('LITERAL::'):])
    else:
        got = len(re.findall(pat, fix))
    ok = got == want
    if not ok:
        bad += 1
    print('%-48s %6d %6d %s' % (label, want, got, '' if ok else '<-- MISMATCH'))
print('--- btn()-routed defs: dict coverage ---')
for k in BTN_LABELS + BTN_ARIA:
    have = all(k in d[lang] for lang in ('es', 'fr', 'de'))
    if not have:
        bad += 1
    print('%-48s %s' % (k, 'OK' if have else '<-- MISSING FROM DICT'))
print('--- Pin/Unpin dynamic pin (checked by hand) ---')
print('pin/unpin marked span present:', 'data-mw-en="\'+(post.pinned' in fix)
print('--- bare-label sweep: unmarked render forms left in FIX ---')
# unmarked forms that must be gone (exact source fragments, no marking)
GONE = [
    ("<b>IN A NUTSHELL</b>' + md(", 'intelBoard nutshell'),
    ("<span class=\"ib-nutshell-label\">IN A NUTSHELL</span>'", 'ibFeedCard nutshell'),
    ("<p class=\"ph-nutshell\">IN A NUTSHELL</p>", 'noteCard nutshell'),
    ("<span class=\"ph-nl\">IN A NUTSHELL</span>", 'sa nutshell'),
    ("<span class=\"left\">ONE INTELLIGENCE", 'microcopy left'),
    ("<span class=\"right\">TRUST: SOURCE", 'microcopy right'),
    ("<span>Smart Note ' + esc(note.id", 'foot personal'),
    ("<span>Official NayaNET Guide", 'foot official'),
    ("<span>Note ' + esc(idStr)", 'Note meta'),
    ("<summary>YOUR WORDS, WORD FOR WORD</summary>", 'rawdetails summary'),
    ("<span>DISTILLED FROM THE AUTHOR", 'distilled microcopy'),
    ("<span class=\"ib-naya-fidelity\">YOUR WORDS", 'fidelity span'),
    (">💾 Save to list</button>", 'Save to list'),
    (">➕ Space from this</button>", 'Space from this'),
    (">🏢 Business from this</button>", 'Business from this'),
    ("placeholder=\"Add a comment…\"", 'comment placeholder (unmarked)'),
    ("data-ib-cmt-send=\"'+esc(post.id||'')+'\" style=\"--ac:#3fb8ff;\">Send</button>", 'Send button (ibFeedCard)'),
    ("· OWNER</span>", 'OWNER badge'),
    ("📌 PINNED</span>", 'PINNED badge'),
    ("<div class=\"ib-kind\">'+kind+'", 'kind div'),
    ("'<b>' + esc(L.name) + '</b>'", 'intelBoard layer head'),
    ("<span>'+esc(L.head||'Detail')+'</span>'", 'ibFeedCard layer head'),
    ("data-ib-cat=\"\">All notes</button>", 'All notes'),
    ("data-ib-cat-add>+ List</button>", '+ List'),
    ("b.textContent = label; b.setAttribute('aria-label', ariaLabel || label);",
     'old btn()'),
]
for frag, name in GONE:
    c = fix.count(frag)
    if c:
        bad += 1
    print('%-48s left=%d %s' % (name, c, '' if not c else '<-- STILL THERE'))
print('data-mw-tr: base %d -> fix %d | data-mw-ph: base %d -> fix %d | data-mw-aria: base %d -> fix %d' % (
    base.count('data-mw-tr'), fix.count('data-mw-tr'),
    base.count('data-mw-ph'), fix.count('data-mw-ph'),
    base.count('data-mw-aria'), fix.count('data-mw-aria')))
print('MISMATCHES:', bad)
json.dump({'mismatches': bad}, open(WORK + 'grep-card-labels.json', 'w'), indent=1)
