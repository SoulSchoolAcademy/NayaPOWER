#!/usr/bin/env python3
"""Fix-pass self-verification v2 (pass 1 of 3, corrected methods).
- Sentence counts per <p> (Vera's method), diffed per-board vs Vera's
  baseline list from the checker record.
- Baseline-vs-edited sentence multiset equality (words only moved).
- Official word-multiset check, proper scope + apostrophe normalisation.
- #letterBody visible-text equality (scoped parse, no script/style inside).
- Portrait audit + no-regression greps.
Exits 1 on any violation.
"""
import html as H
import re
import sys
from collections import Counter
from html.parser import HTMLParser

D = "walk-beginning-fixed.html"
BASE = "walk-beginning-fixed-7553d76b-baseline.html"
OFF = "COLLECTIVE-AGREEMENT-OFFICIAL-20261115.md"
h = open(D, encoding="utf-8").read()
base = open(BASE, encoding="utf-8").read()
off = open(OFF, encoding="utf-8").read()
fails = []
VERA = [3, 3, 2, 4, 3, 2, 3, 3, 3, 1, 4, 4, 3, 3, 2, 3, 4, 4, 4, 4, 1, 4, 3, 3, 1, 4, 1, 3, 3, 3, 2, 3, 4, 3, 3, 3, 4, 2, 4, 4, 3, 3, 1, 4, 3, 3, 2, 2, 3, 2, 4, 3, 2, 3, 3, 2, 3, 1, 6, 3, 3, 2, 4, 2, 3, 1, 3, 3, 2, 2, 4, 3, 3, 1, 2, 3, 3, 1, 2, 3, 3, 3, 2]


def nutshells(doc):
    arts = re.findall(r'<article class="[^"]*letter-beat[^"]*"[^>]*data-beat="(\d+)"[^>]*>(.*?)</article>', doc, re.S)
    out = {}
    for n, body in arts:
        nuts = re.search(r'<div class="ib-nutshell">(.*?)</div>\s*<div class="ib-foot">', body, re.S)
        assert nuts, f"beat {n}: no nutshell"
        out[int(n)] = nuts.group(1)
    return out


def sentences_per_p(nuts_html):
    """Vera's method: per <p>, split on [. ! ? ...], eye button + note divs
    removed; each non-empty <p> counts >= 1."""
    txt = re.sub(r'<div class="deal-eye-note"[^>]*>.*?</div>', '', nuts_html, flags=re.S)
    paras = re.findall(r'<p[^>]*>(.*?)</p>', txt, flags=re.S)
    total = 0
    for p in paras:
        p = re.sub(r'<button[^>]*>.*?</button>', '', p, flags=re.S)
        p = re.sub(r'<[^>]+>', '', p)
        p = H.unescape(p)
        p = re.sub(r'\$\d+\.\d+', 'PRICE', p)
        frags = [s for s in re.split(r'[.!?\u2026]+', p) if s.strip()]
        total += max(1, len(frags)) if p.strip() else 0
    return total


def sentence_texts(nuts_html):
    """Normalised sentence strings per <p>, for multiset comparison."""
    txt = re.sub(r'<div class="deal-eye-note"[^>]*>.*?</div>', '', nuts_html, flags=re.S)
    paras = re.findall(r'<p[^>]*>(.*?)</p>', txt, flags=re.S)
    out = []
    for p in paras:
        p = re.sub(r'<button[^>]*>.*?</button>', '', p, flags=re.S)
        p = re.sub(r'<[^>]+>', '', p)
        p = H.unescape(p).replace('\u2019', "'").replace('\u201c', '"').replace('\u201d', '"')
        p = re.sub(r'\s+', ' ', p).strip()
        if p:
            out.append(p)
    return out


# ---------- 1. sentence counts ----------
new_n = nutshells(h)
old_n = nutshells(base)
assert len(new_n) == 83 and len(old_n) == 83
counts = [sentences_per_p(new_n[i]) for i in range(83)]
base_counts = [sentences_per_p(old_n[i]) for i in range(83)]
print("COUNTS:", counts)
print("max:", max(counts), "min:", min(counts), "total:", sum(counts))
print("BASELINE counts match Vera:", base_counts == VERA)
if base_counts != VERA:
    print("  diff vs Vera:", [(i, base_counts[i], VERA[i]) for i in range(83) if base_counts[i] != VERA[i]])
    fails.append("baseline counts != Vera's list (method mismatch)")
if max(counts) > 4 or min(counts) < 1:
    fails.append(f"count out of 1-4: {counts}")
print("beats 58/59/60:", counts[58], counts[59], counts[60])
changed = [(i, base_counts[i], counts[i]) for i in range(83) if base_counts[i] != counts[i]]
print("changed boards:", changed)
if changed != [(58, 6, 4), (59, 3, 4), (60, 3, 4)]:
    fails.append(f"unexpected changed boards: {changed}")

# ---------- 2. sentence multiset: baseline vs edited ----------
def all_sents(nuts_map):
    c = Counter()
    for i in sorted(nuts_map):
        for s in sentence_texts(nuts_map[i]):
            c[s] += 1
    return c
sn, so = all_sents(new_n), all_sents(old_n)
print("sentence multiset identical baseline->edited:", sn == so)
if sn != so:
    print("  only-new:", list((sn - so).items())[:5])
    print("  only-old:", list((so - sn).items())[:5])
    fails.append("sentence multiset changed")

# ---------- 3. Official word multiset ----------
WORD = re.compile(r"[A-Za-z0-9']+")
def norm_words(t):
    t = H.unescape(t).replace('\u2019', "'").replace('\u201c', '"').replace('\u201d', '"')
    return [w.lower() for w in WORD.findall(t)]
# Official scope: body from "Hi, I'm Naya." through the end of "The Agreement"
# section (before "## THE END") PLUS the final line "nayanet.app — enter."
# (it sits after the SEPARATE section in the file); drop markdown headers.
body = off.split("Hi, I'm Naya.", 1)[1].split("## THE END", 1)[0]
body = re.sub(r'^#{1,3} .*$', ' ', body, flags=re.M)
body = re.sub(r'\*\*', ' ', body)
off_words = Counter(norm_words("Hi, I'm Naya. " + body + " nayanet.app — enter."))
# Board scope: 83 nutshells + 2 summary nutshells + 5 section subtitles.
board_text = []
for i in range(83):
    board_text += sentence_texts(new_n[i])
summ = re.findall(r'id="dealAgreementSummary2?" hidden>(.*?)</article>', h, re.S)
for s in summ:
    nuts = re.search(r'<div class="ib-nutshell">(.*?)</div>\s*<div class="ib-foot">', s, re.S)
    board_text += sentence_texts(nuts.group(1))
subs = [H.unescape(re.sub(r'<[^>]+>', ' ', s)) for s in re.findall(r'<p class="ib-subtitle">(.*?)</p>', h)]
board_words = Counter(norm_words(" ".join(board_text + subs)))
FOUNDERS = "The first 1,000 founders get half price, and double points once a thousand founders join."
for w in norm_words(FOUNDERS):
    board_words[w] -= 1
    if board_words[w] <= 0:
        del board_words[w]
outside = {w: c for w, c in board_words.items() if off_words.get(w, 0) < c}
missing = {w: c for w, c in off_words.items() if board_words.get(w, 0) < c}
print("board words outside Official:", outside)
print("Official words missing from boards+subtitles:", missing)
if outside:
    fails.append(f"outside: {outside}")
if missing:
    fails.append(f"missing: {missing}")

# ---------- 4. ordered sentence list identical (order preserved) ----------
# Moving sentences between boards must not change their global order: the
# ordered list of board sentences must be byte-identical baseline->edited.
def ordered_sents(nuts_map):
    out = []
    for i in sorted(nuts_map):
        out += sentence_texts(nuts_map[i])
    return out
on, oo = ordered_sents(new_n), ordered_sents(old_n)
print("ordered board sentences identical:", on == oo, "| n:", len(on), len(oo))
if on != oo:
    fails.append("ordered sentence list differs")

# ---------- 5. portrait audit ----------
notes = re.findall(r'<div class="deal-eye-note" id="([^"]+)" hidden><img class="deal-quote-photo" src="([^"]+)"', h)
nc = Counter(src for _, src in notes)
print("NOTES:", len(notes), "photo counts:", dict(nc), "max:", max(nc.values()))
if len(notes) != 14 or max(nc.values()) > 2:
    fails.append("note audit fail")
board_photos = {}
for m in re.finditer(r'<article class="[^"]*letter-beat[^"]*"[^>]*data-beat="(\d+)"[^>]*>(.*?)</article>', h, re.S):
    f = re.findall(r'<img class="deal-beat-photo" src="([^"]+)"', m.group(2))
    if f:
        board_photos[int(m.group(1))] = f[0]
s4 = {b: f for b, f in board_photos.items() if 36 <= b <= 77}
print("§4 faced:", sorted(s4))
for w in range(36, 76):
    if not any(b in s4 for b in (w, w + 1, w + 2)):
        fails.append(f"§4 window {w}-{w+2} faceless")
for b in sorted(board_photos):
    if b + 1 in board_photos and board_photos[b] == board_photos[b + 1]:
        fails.append(f"adjacent {b}/{b+1} share portrait")
bnote = {}
for n, body in new_n.items():
    for m in re.finditer(r'data-note="(deal-note-[a-z]+)"', body):
        bnote[m.group(1)] = n
for nid, src in notes:
    b = bnote[nid]
    if b in board_photos and board_photos[b] == src:
        fails.append(f"note {nid} == board {b} portrait")
if 0 in board_photos:
    fails.append("beat 0 has portrait")
print("b02 occurrences:", h.count("/agmt-b02.jpg"), "(want 2)")

# ---------- 6. greps ----------
def grep(pat):
    c = h.count(pat); print(f"grep {pat!r}: {c}"); return c
checks = [
    (grep("bonus") == 0, "bonus"), (grep("blockchain") == 0, "blockchain"),
    (grep("Our planned privacy standard") == 0, "hedge1"),
    (grep("until the full retention system is implemented and independently verified") == 0, "hedge2"),
    (grep("THE ROYAL MANUSCRIPT") == 0, "royal"), (grep("Ready to sign") == 0, "ready"),
    (grep("letterPreview") == 0, "preview"),
    (grep("The first 1,000 founders get half price, and double points once a thousand founders join.") == 1, "founders"),
    (grep("governed by the applicable published agreements") == 1, "off-hedge1"),
    (grep("the intended default is seven days") == 1, "off-hedge2"),
    (grep("I&rsquo;m not an LLM") == 1, "not-llm"), (grep("$25") == 2, "$25"),
    (grep("$20") == 0, "$20"), (grep("nayanet.app &mdash; enter.") == 1, "final"),
    (grep("double points") == 1, "dbl"), (grep("/agmt-b02.jpg") == 2, "b02x2"),
    (grep("agmt-b00.jpg") == 2, "b00x2"), (grep("/agmt-b12.jpg") == 2, "b12x2"),
]
for ok, name in checks:
    if not ok:
        fails.append(f"grep check failed: {name}")

print("FAILS:", fails if fails else "NONE")
sys.exit(1 if fails else 0)
