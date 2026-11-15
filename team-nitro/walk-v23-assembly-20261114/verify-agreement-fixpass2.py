#!/usr/bin/env python3
"""Fix-pass-2 self-verification (pass 1 of 3).
Baseline: the fix-pass file (ae1bd0ba). Edited file must differ ONLY by
the 13 intended replacements: 6 board portraits, 1 note photo, 1 sign
src, 3 plainLetterText lines, 1 CSS block.
- Sentence counts per <p> (Vera's method) identical to the fix-pass list;
  sentence multiset + ordered list identical baseline->edited (words
  only moved: none moved this pass, so identical by construction).
- Official word-multiset check (same scope as the fix-pass verifier).
- Portrait audit, fix-pass-2 rules: openers unique as boards; b09 <= 2
  total; no file > 3 src occurrences; no file on > 2 boards; §4 faced
  every 3-board window; no adjacent boards share a portrait; no note
  photo equals its own board's portrait or an adjacent board's portrait;
  b10 on zero boards; sign is /agmt-sign2.png, old sign src gone.
- Fix 2: plainParaText helper present; both board branches use it.
- Fix 3: scoped 57/63 rule present at 17px.
- No-regression greps (same set as the fix-pass verifier).
Exits 1 on any violation.
"""
import html as H
import re
import sys
from collections import Counter
from html.parser import HTMLParser  # noqa: F401  (parity import)

D = "walk-beginning-fixed.html"
BASE = "walk-beginning-fixed-ae1bd0ba-baseline.html"
OFF = "COLLECTIVE-AGREEMENT-OFFICIAL-20261115.md"
h = open(D, encoding="utf-8").read()
base = open(BASE, encoding="utf-8").read()
off = open(OFF, encoding="utf-8").read()
fails = []
VERA = [3, 3, 2, 4, 3, 2, 3, 3, 3, 1, 4, 4, 3, 3, 2, 3, 4, 4, 4, 4, 1, 4, 3, 3, 1, 4, 1, 3, 3, 3, 2, 3, 4, 3, 3, 3, 4, 2, 4, 4, 3, 3, 1, 4, 3, 3, 2, 2, 3, 2, 4, 3, 2, 3, 3, 2, 3, 1, 4, 4, 4, 2, 4, 2, 3, 1, 3, 3, 2, 2, 4, 3, 3, 1, 2, 3, 3, 1, 2, 3, 3, 3, 2]


def nutshells(doc):
    arts = re.findall(r'<article class="[^"]*letter-beat[^"]*"[^>]*data-beat="(\d+)"[^>]*>(.*?)</article>', doc, re.S)
    out = {}
    for n, body in arts:
        nuts = re.search(r'<div class="ib-nutshell">(.*?)</div>\s*<div class="ib-foot">', body, re.S)
        assert nuts, f"beat {n}: no nutshell"
        out[int(n)] = nuts.group(1)
    return out


def sentences_per_p(nuts_html):
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


# ---------- 1. sentence counts (unchanged this pass) ----------
new_n = nutshells(h)
old_n = nutshells(base)
assert len(new_n) == 83 and len(old_n) == 83
counts = [sentences_per_p(new_n[i]) for i in range(83)]
base_counts = [sentences_per_p(old_n[i]) for i in range(83)]
print("COUNTS max:", max(counts), "min:", min(counts), "total:", sum(counts))
print("counts == Vera list:", counts == VERA, "| baseline == Vera:", base_counts == VERA)
if counts != VERA:
    fails.append(f"counts != Vera: {[(i, counts[i], VERA[i]) for i in range(83) if counts[i] != VERA[i]]}")
if counts != base_counts:
    fails.append("counts changed vs baseline (no board text should move)")

# ---------- 2. sentence multiset + order identical ----------
def all_sents(nuts_map):
    c = Counter()
    for i in sorted(nuts_map):
        for s in sentence_texts(nuts_map[i]):
            c[s] += 1
    return c
sn, so = all_sents(new_n), all_sents(old_n)
print("sentence multiset identical baseline->edited:", sn == so)
if sn != so:
    fails.append("sentence multiset changed")
def ordered_sents(nuts_map):
    out = []
    for i in sorted(nuts_map):
        out += sentence_texts(nuts_map[i])
    return out
print("ordered board sentences identical:", ordered_sents(new_n) == ordered_sents(old_n))
if ordered_sents(new_n) != ordered_sents(old_n):
    fails.append("ordered sentence list differs")

# ---------- 3. Official word multiset ----------
WORD = re.compile(r"[A-Za-z0-9']+")
def norm_words(t):
    t = H.unescape(t).replace('\u2019', "'").replace('\u201c', '"').replace('\u201d', '"')
    return [w.lower() for w in WORD.findall(t)]
body = off.split("Hi, I'm Naya.", 1)[1].split("## THE END", 1)[0]
body = re.sub(r'^#{1,3} .*$', ' ', body, flags=re.M)
body = re.sub(r'\*\*', ' ', body)
off_words = Counter(norm_words("Hi, I'm Naya. " + body + " nayanet.app — enter."))
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
print("Official words missing:", missing)
if outside:
    fails.append(f"outside: {outside}")
if missing:
    fails.append(f"missing: {missing}")

# ---------- 4. portrait audit, fix-pass-2 rules ----------
src_counts = Counter(re.findall(r'src="(/agmt-(?:b\d+|top|sign2?|logo)\.(?:jpg|png))"', h))
print("src counts:", dict(sorted(src_counts.items())))
b_counts = {k: v for k, v in src_counts.items() if re.match(r'/agmt-b\d+\.', k)}
print("b-file totals:", dict(sorted(b_counts.items())), "max:", max(b_counts.values()))
if max(b_counts.values()) > 3:
    fails.append("a b-file totals > 3")
if b_counts.get('/agmt-b09.jpg', 0) > 2:
    fails.append("b09 totals > 2")
print("b09 total:", b_counts.get('/agmt-b09.jpg', 0), "(want <= 2)")
board_photos = {}
for m in re.finditer(r'<article class="[^"]*letter-beat[^"]*"[^>]*data-beat="(\d+)"[^>]*>(.*?)</article>', h, re.S):
    f = re.findall(r'<img class="deal-beat-photo" src="([^"]+)"', m.group(2))
    if f:
        board_photos[int(m.group(1))] = f[0]
print("board portraits (19):", {b: board_photos[b] for b in sorted(board_photos)})
if len(board_photos) != 19:
    fails.append(f"board portrait count {len(board_photos)} != 19")
board_file_counts = Counter(board_photos.values())
print("per-file board counts:", dict(board_file_counts), "max:", max(board_file_counts.values()))
if max(board_file_counts.values()) > 2:
    fails.append("a file appears on > 2 boards")
OPENERS = {11: '/agmt-b06.png', 18: '/agmt-b04.jpg', 25: '/agmt-b09.jpg', 78: '/agmt-b08.jpg'}
for beat, src in OPENERS.items():
    if board_photos.get(beat) != src:
        fails.append(f"opener beat {beat} is not {src}")
    others = [b for b, f in board_photos.items() if f == src and b != beat]
    if others:
        fails.append(f"opener file {src} also on board(s) {others}")
print("openers unique as boards: OK" if not fails else "opener check FAILED")
if '/agmt-b10.jpg' in board_photos.values():
    fails.append("b10 still on a board")
if '/agmt-b09.jpg' in [f for b, f in board_photos.items() if b != 25]:
    fails.append("b09 on a board other than the opener")
print("b10 on boards:", [b for b, f in board_photos.items() if f == '/agmt-b10.jpg'], "(want [])")
s4 = {b: f for b, f in board_photos.items() if 36 <= b <= 77}
print("§4 faced:", sorted(s4), "count:", len(s4))
if len(s4) != 15:
    fails.append(f"§4 faced {len(s4)} != 15")
for w in range(36, 76):
    if not any(b in s4 for b in (w, w + 1, w + 2)):
        fails.append(f"§4 window {w}-{w+2} faceless")
for b in sorted(board_photos):
    if b + 1 in board_photos and board_photos[b] == board_photos[b + 1]:
        fails.append(f"adjacent {b}/{b+1} share portrait")
# notes: parent board from the article containing the note div
notes = []
for m in re.finditer(r'<article class="[^"]*letter-beat[^"]*"[^>]*data-beat="(\d+)"[^>]*>(.*?)</article>', h, re.S):
    for nid, src in re.findall(r'<div class="deal-eye-note" id="([^"]+)" hidden><img class="deal-quote-photo" src="([^"]+)"', m.group(2)):
        notes.append((int(m.group(1)), nid, src))
print("notes (14):", notes)
if len(notes) != 14:
    fails.append(f"note count {len(notes)} != 14")
nc = Counter(src for _, _, src in notes)
print("note photo counts:", dict(nc), "max:", max(nc.values()))
if max(nc.values()) > 2:
    fails.append("a file illustrates > 2 notes")
for b, nid, src in notes:
    if board_photos.get(b) == src:
        fails.append(f"note {nid} == own board {b} portrait")
    for adj in (b - 1, b + 1):
        if board_photos.get(adj) == src:
            fails.append(f"note {nid} == adjacent board {adj} portrait")
# summary board portrait (the 34th b-occurrence, named not counted)
summ_photos = re.findall(r'id="dealAgreementSummary"[^>]*>.*?<img class="deal-beat-photo" src="([^"]+)"', h, re.S)
print("summary board portrait:", summ_photos, "(the extra b-occurrence)")
if summ_photos != ['/agmt-b07.jpg']:
    fails.append("summary board portrait changed")
# sign
print("sign src occurrences: /agmt-sign2.png =", h.count('/agmt-sign2.png'), "| /agmt-sign.jpg =", h.count('/agmt-sign.jpg'))
if h.count('/agmt-sign2.png') != 1 or h.count('/agmt-sign.jpg') != 0:
    fails.append("sign swap wrong")
if 0 in board_photos:
    fails.append("beat 0 has portrait")

# ---------- 5. fix 2: plain-text builder strips buttons ----------
print("plainParaText present:", "function plainParaText(el)" in h)
print("board branch uses plainParaText:", "lines.push(plainParaText(ps[a]))" in h)
print("fallback branch uses plainParaText:", "lines.push(plainParaText(ap[c]))" in h)
print("raw textContent reads left in board branches:", h.count("ps[a].textContent"), h.count("ap[c].textContent"))
if "function plainParaText(el)" not in h or "lines.push(plainParaText(ps[a]))" not in h or "lines.push(plainParaText(ap[c]))" not in h:
    fails.append("plainParaText fix missing")
if "ps[a].textContent" in h or "ap[c].textContent" in h:
    fails.append("board branch still reads textContent directly")

# ---------- 6. fix 3: scoped 57/63 rule ----------
m3 = re.search(r'\[data-beat="57"\] \.ib-nutshell b, \[data-beat="63"\] \.ib-nutshell b \{\s*font-size: 17px;', h)
print("scoped 57/63 rule at 17px:", bool(m3))
if not m3:
    fails.append("fix-3 scoped rule missing")
BASE_B = ".ib-nutshell b {\n  display: block; color: #f4f2f7; font-size: 12px;\n  letter-spacing: .16em; margin-bottom: 8px; font-weight: 800;\n}"
print("base .ib-nutshell b block intact x1:", h.count(BASE_B) == 1)
if h.count(BASE_B) != 1:
    fails.append("base .ib-nutshell b rule changed/duplicated")

# ---------- 7. no-regression greps ----------
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
    (grep("double points") == 1, "dbl"),
]
for ok, name in checks:
    if not ok:
        fails.append(f"grep check failed: {name}")

# ---------- 8. diff scope: only the 13 intended changes ----------
import difflib
base_lines = base.split('\n')
new_lines = h.split('\n')
diff = [l for l in difflib.unified_diff(base_lines, new_lines, lineterm='')]
changed = [l for l in diff if l.startswith(('+', '-')) and not l.startswith(('+++', '---'))]
print("diff +/- lines:", len(changed))
for l in changed:
    print("  ", l[:220])
if len(changed) > 40:
    fails.append(f"diff too wide: {len(changed)} +/- lines")

print("FAILS:", fails if fails else "NONE")
sys.exit(1 if fails else 0)
