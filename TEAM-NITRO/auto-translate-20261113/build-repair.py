#!/usr/bin/env python3
"""Auto-translate REPAIR fix — build the edited page IN MEMORY.

Closes the checker's F1-F10 on the third-surface tip bytes. Reads the base
from argv[1]: a local file path, or the literal "TIP" to fetch the
third-surface tip blob (ce42cec8...) from GitHub in memory (the local
worktree file may be 0 bytes from EPERM flake damage; the blob is the
source of truth either way — sha verified before any edit).

Grows the dictionary in memory (791 -> 807 keys/language, apply-repair-
dict.py), regenerates the embedded MW_I18N JSON in place, then applies
every render-site edit with exact-count assertions. Prints the edited HTML
to STDOUT and a verification report to STDERR. Writes NO files.
"""
import sys, re, json, hashlib, base64, subprocess

BASE_ARG = sys.argv[1]
DICTSCRIPT = "/home/hatch/workspace/team-nitro/auto-translate-20261113/apply-repair-dict.py"
GH = "/home/hatch/workspace/team-nitro/gh-direct.py"
REPO = "SoulSchoolAcademy/NayaPOWER"
TIP_BLOB = "ce42cec8d4c18f6b89eccab8ff20d7b9a6221ee2"
TIP_SHA256 = "f9f58cc77807aa01a85be6c89c8b2b7078a52fd04cd74da172add029e5de0c24"

failures = []

def rep(html, old, new, expect=1, tag=""):
    global failures
    n = html.count(old)
    if n != expect:
        failures.append(f"REP {tag}: expected {expect}, found {n}: {old[:110]!r}")
        return html
    return html.replace(old, new)

def tr(k):
    """mwTr guard for a JS string literal (keys never contain an ASCII quote)."""
    assert "'" not in k and "\\" not in k, f"key not safe for JS single quotes: {k!r}"
    return "(window.mwTr?window.mwTr('" + k + "'):'" + k + "')"

# ---------- base bytes ----------
if BASE_ARG == "TIP":
    out = subprocess.run(["python3", GH, "GET", f"/repos/{REPO}/git/blobs/{TIP_BLOB}"],
                         capture_output=True, text=True, timeout=120)
    lines = out.stdout.splitlines()
    body = "\n".join(lines[1:]) if lines and lines[0].startswith("HTTP ") else out.stdout
    raw = base64.b64decode(json.loads(body)["content"])
    print("base: tip blob from GitHub", file=sys.stderr)
else:
    raw = open(BASE_ARG, "rb").read()
    print(f"base: local file {BASE_ARG}", file=sys.stderr)
sha = hashlib.sha256(raw).hexdigest()
assert sha == TIP_SHA256, f"base sha mismatch: {sha} != {TIP_SHA256}"
assert len(raw) == 1814328, f"base size mismatch: {len(raw)}"
html0 = raw.decode("utf-8")
print(f"base verified: sha256={sha} bytes={len(raw)}", file=sys.stderr)

# ---------- grown dictionary (in memory) ----------
src = open(DICTSCRIPT, encoding="utf-8").read()
head = src.split("def main():")[0]
g = {}
exec(head, g)
NEW = g["NEW"]
# parse embedded MW_I18N robustly (JSONDecoder, not a regex span)
m0 = re.search(r"var MW_I18N\s*=\s*", html0)
assert m0, "MW_I18N not found in base"
brace = html0.index("{", m0.end())
dec = json.JSONDecoder()
d, end = dec.raw_decode(html0, brace)
assert {k: len(v) for k, v in d.items()} == {"es": 791, "fr": 791, "de": 791}, "base dict not 791"
d = g["grow"](d)
assert {k: len(v) for k, v in d.items()} == {"es": 807, "fr": 807, "de": 807}
DICT_JSON = json.dumps(d, ensure_ascii=False, indent=1, sort_keys=True)
html = html0[:brace] + DICT_JSON + html0[end:]
print(f"DICT grown: 791 -> 807 keys/language ({len(NEW)} new)", file=sys.stderr)

# ---------- F1: Dashboard static h3 'Plugged into this world' ----------
html = rep(html,
  '<h3><span class="os-jewel os-jewel-h" style="--jc:#a06bff">🔌</span> Plugged into this world</h3>',
  '<h3><span class="os-jewel os-jewel-h" style="--jc:#a06bff">🔌</span> <span data-mw-tr="dash">Plugged into this world</span></h3>',
  tag="F1-plugged-h3")

# ---------- F2: TnTacho setCap captions ----------
html = rep(html,
  "setCap('<b>Birth score</b> — every post, note and share moves the needle.');",
  "setCap(" + tr("<b>Birth score</b> — every post, note and share moves the needle.") + ");",
  tag="F2-cap-birth")
html = rep(html,
  "setCap('Quiet — the first post, note or invite lights the needle.');",
  "setCap(" + tr("Quiet — the first post, note or invite lights the needle.") + ");",
  tag="F2-cap-quiet")
html = rep(html,
  "setCap('Reading your actions…');",
  "setCap(" + tr("Reading your actions…") + ");",
  tag="F2-cap-reading")

# ---------- F3: renderLinks no-clicks empty state ----------
html = rep(html,
  '\'<p class=""os-note">No clicks yet — share a link and the first click lands here.</p>\'',
  '\'<p class=""os-note">\'+' + tr("No clicks yet — share a link and the first click lands here.") + '+\'</p>\'',
  tag="F3-noclicks")

# ---------- F4: renderBars / renderWeek Busiest: / quiet-stretch sites ----------
html = rep(html,
  "if (note) note.textContent=buckets[bi].n?('Busiest: '+buckets[bi].note+' Posts, messages and invites together.'):'A quiet stretch — the next post, message or invite lights the first bar.';",
  "if (note) note.textContent=buckets[bi].n?(" + tr("Busiest: ") + "+buckets[bi].note+' '+" + tr("Posts, messages and invites together.") + "):" + tr("A quiet stretch — the next post, message or invite lights the first bar.") + ";",
  tag="F4-bars-buckets")
html = rep(html,
  "if (note) note.textContent=(days[bi].n?('Busiest: '+days[bi].note+' Posts, messages and invites together.'):'A quiet stretch — the next post, message or invite lights the first circle.')+(repPeriod===0?' The circles show the story week by week; the totals cover the whole story.':(repPeriod!==7?' The circles show the last 7 days; the totals cover the full period.':''));",
  "if (note) note.textContent=(days[bi].n?(" + tr("Busiest: ") + "+days[bi].note+' '+" + tr("Posts, messages and invites together.") + "):" + tr("A quiet stretch — the next post, message or invite lights the first circle.") + ")+(repPeriod===0?' '+" + tr("The circles show the story week by week; the totals cover the whole story.") + ":(repPeriod!==7?' '+" + tr("The circles show the last 7 days; the totals cover the full period.") + ":''));",
  tag="F4-week-days")
html = rep(html,
  "if (note) note.textContent=buckets[bi].n?('Busiest: '+buckets[bi].note+' '+(subject||'Posts, notes, messages and invites together.')):('A quiet stretch so far — the chart is waiting. '+(quiet||'The next post, note, message or invite lights the first bar.'));",
  "if (note) note.textContent=buckets[bi].n?(" + tr("Busiest: ") + "+buckets[bi].note+' '+(subject||" + tr("Posts, notes, messages and invites together.") + ")):(" + tr("A quiet stretch so far — the chart is waiting.") + "+' '+(quiet||" + tr("The next post, note, message or invite lights the first bar.") + "));",
  tag="F4-bars-generic")

# ---------- F5: renderFunnel (the bare copy) — conv + stage + truths ----------
html = rep(html,
  "+conv(joined, total, 'of recorded invites joined', '#3fb8ff')",
  "+conv(joined, total, " + tr("of recorded invites joined") + ", '#3fb8ff')",
  tag="F5-conv")
html = rep(html,
  "+stage('Joined', joined, '#3fb8ff', 1)",
  "+stage(" + tr("Joined") + ", joined, '#3fb8ff', 1)",
  tag="F5-stage-joined")
html = rep(html,
  "if (!total) truth='No invites yet — record the first one above.';",
  "if (!total) truth=" + tr("No invites yet — record the first one above.") + ";",
  tag="F5-truth-none")
html = rep(html,
  "else if (allDry) truth='Record-only mode: saved, never sent — Joined honestly reads 0 until a friend connects.';",
  "else if (allDry) truth=" + tr("Record-only mode: saved, never sent — Joined honestly reads 0 until a friend connects.") + ";",
  tag="F5-truth-dry")
html = rep(html,
  "else if (!joined) truth='Invites are recorded — the first join is the milestone ahead.';",
  "else if (!joined) truth=" + tr("Invites are recorded — the first join is the milestone ahead.") + ";",
  tag="F5-truth-first")
html = rep(html,
  "else truth=joined+(joined===1?' person has':' people have')+' walked the whole invite journey.';",
  "else truth=joined+(joined===1?" + tr(" person has") + ":" + tr(" people have") + ")+" + tr(" walked the whole invite journey.") + ";",
  tag="F5-truth-walked")

# ---------- F6: the old + menu (#plusmenu) — the live one (#plusbtn opens it) ----------
html = rep(html,
  '<div class="fc-plusmenu" id="fcPlusMenu" hidden role="menu" aria-label="Add">',
  '<div class="fc-plusmenu" id="fcPlusMenu" hidden role="menu" data-mw-aria="Add" aria-label="Add">',
  tag="F6g-fcmenu-aria")
html = rep(html,
  '<button class="ph-plus" id="plusbtn" type="button" aria-label="Add something" title="Add">＋</button>',
  '<button class="ph-plus" id="plusbtn" type="button" data-mw-aria="Add something" aria-label="Add something" data-mw-title="Add" title="Add">＋</button>',
  tag="F6-plusbtn")
html = rep(html,
  '<span class="ph-plus-label">Add</span>',
  '<span class="ph-plus-label" data-mw-tr="pm">Add</span>',
  tag="F6-plus-label")
html = rep(html,
  '<div class="ph-plusitem" data-os-go="home">✎ Make a post</div>',
  '<div class="ph-plusitem" data-os-go="home">✎ <span data-mw-tr="pm">Make a post</span></div>',
  tag="F6-item-post")
html = rep(html,
  '<div class="ph-plusitem" data-os-go="message">✉️ Send a message</div>',
  '<div class="ph-plusitem" data-os-go="message">✉️ <span data-mw-tr="pm">Send a message</span></div>',
  tag="F6-item-message")
html = rep(html,
  '<div class="ph-plusitem" data-os-go="growth">🔗 Add a Smart Link</div>',
  '<div class="ph-plusitem" data-os-go="growth">🔗 <span data-mw-tr="pm">Add a Smart Link</span></div>',
  tag="F6-item-link")
html = rep(html,
  '<div class="ph-plusitem" data-os-go="lists">☰ Add to a list</div>',
  '<div class="ph-plusitem" data-os-go="lists">☰ <span data-mw-tr="pm">Add to a list</span></div>',
  tag="F6-item-list")
# F6-adjacent, same standalone 'Add' label: the Lists view Add button.
html = rep(html,
  '<button class="ph-connect" id="os-list-add" type="button" style="padding:12px 22px;">Add</button>',
  '<button class="ph-connect" id="os-list-add" type="button" style="padding:12px 22px;"><span data-mw-tr="lists">Add</span></button>',
  tag="F6h-list-add")

# ---------- F7: avatar camera button (#avedit) ----------
html = rep(html,
  '<button class="ph-av-edit" id="avedit" type="button" aria-label="Change picture" title="Edit photo">📷</button>',
  '<button class="ph-av-edit" id="avedit" type="button" data-mw-aria="Change picture" aria-label="Change picture" data-mw-title="Edit photo" title="Edit photo">📷</button>',
  tag="F7-avedit")

# ---------- F8: Video/Voice note save-path bake — store empty, let the guarded display fallback translate ----------
html = rep(html,
  "var title = (($('os-nn-title') && $('os-nn-title').value) || '').trim() || (r.kind === 'video' ? 'Video note' : 'Voice note');",
  "var title = (($('os-nn-title') && $('os-nn-title').value) || '').trim();",
  tag="F8-save-title")

# ---------- F9: Notes wall 'Untitled note' — renderNotes map + bestSave ----------
html = rep(html,
  "return {id:'r'+x.row.id, t:x.c.t||'Untitled note', b:x.c.b||'', c:'#a06bff', at:x.row.created_at, sample:false, i:i, cat:fl?fl.category_name:null};",
  "return {id:'r'+x.row.id, t:x.c.t||" + tr("Untitled note") + ", b:x.c.b||'', c:'#a06bff', at:x.row.created_at, sample:false, i:i, cat:fl?fl.category_name:null};",
  tag="F9-wall-map")
html = rep(html,
  "bestSave={title:r.j.t||'Untitled note', n:n}",
  "bestSave={title:r.j.t||" + tr("Untitled note") + ", n:n}",
  tag="F9-bestSave")

# ---------- F10: 'Hide breakdown' toggle (+ its T() re-sync on switch) ----------
html = rep(html,
  "b.textContent=open?'Hide breakdown':'Breakdown';",
  "b.textContent=open?" + tr("Hide breakdown") + ":" + tr("Breakdown") + ";",
  tag="F10-toggle")
html = rep(html,
  "document.querySelectorAll('[data-sl-dim]').forEach(function(b){ b.textContent=T('Breakdown'); });",
  "document.querySelectorAll('[data-sl-dim]').forEach(function(b){ var _r=b.closest?b.closest('.os-link-row'):null; var _p=_r?_r.nextElementSibling:null; var _o=_p&&_p.classList.contains('os-link-dim')&&!_p.hasAttribute('hidden'); b.textContent=T(_o?'Hide breakdown':'Breakdown'); });",
  tag="F10-resync")

# ---------- report ----------
out = html.encode("utf-8")
print(f"data-mw-tr: {html.count('data-mw-tr')} (was 364)", file=sys.stderr)
print(f"data-mw-ph: {html.count('data-mw-ph')} (was 12)", file=sys.stderr)
print(f"data-mw-aria: {html.count('data-mw-aria')} (was 16)", file=sys.stderr)
print(f"data-mw-title: {html.count('data-mw-title')} (was 8)", file=sys.stderr)
print(f"mwTr guard uses: {html.count('window.mwTr?')} (was 603)", file=sys.stderr)
print(f"built bytes={len(out)} lines={html.count(chr(10))+1}", file=sys.stderr)
if failures:
    for f in failures:
        print("FAIL:", f, file=sys.stderr)
    sys.exit(1)
print(f"OK sha256={hashlib.sha256(out).hexdigest()}", file=sys.stderr)
sys.stdout.buffer.write(out)
sys.stdout.buffer.flush()
