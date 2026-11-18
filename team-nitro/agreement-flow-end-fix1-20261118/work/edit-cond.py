#!/usr/bin/env python3
"""CONDITIONS edit driver (2026-11-18) — agreement flow-end FIX1 conditions.

Closes the checker's two conditions from CHECKER-REPORT.md §14, nothing else.
Base: walk-end/agreement-flow-end-fix1-20261118 @ 43c8ba1e (unfold blob
ef780d10, 104,259 B, sha c295061a — verified from the git blob API).

Condition 1 — unfold visual slot cover -> contain. The rule
`.letter-beat.fp-smart-visual .lb-showcase img` still says
object-fit:cover (byte-identical to the flow-end base). The images it
shows are 4:3 (1448x1086), so /agreement's visual phase crops ~16% top
and bottom. Change that ONE rule to contain. No other object-fit rule
moves: the welcome stage slots are already contain; the remaining cover
hits are circular photos (beat photo, sign photo).

Condition 2 — unfold no-voice tip. The unfold player's 2.5s watchdog
returns to idle silently on no-start. Give it the same "Voice not
available on this device — read below" message the intro player shows
(same wording, same place — the player's tip element). Watchdog
mechanics untouched: warm-up, pick, assignment, clear on
start/end/error all stay as they are.

NOTE ON THE TIP ELEMENT: the unfold player has NO tip element — the
intro player's `.p3-play-tip` span does not exist in the unfold file
(grep: 0 hits), and the unfold's `.play-note` class (17px white,
centred, line 257) is defined but never used in the markup (grep: 1
hit, the CSS rule only). So the tip element is ADDED, reusing that
existing unused `.play-note` style — no new CSS: a <p
class="play-note" id="playTip"> directly under the play button, with
the intro's own default text ("Naya will talk you through this
page"). The watchdog writes the no-voice message into it; setState
restores the default text when play starts again, so a stale message
can never sit under a working voice (mirrors the intro, whose tip
updates with state).

DO NOT TOUCH: the divider (.ib-foot-logo / deck-logo.jpg — recorded,
unchanged), the hold, the letter caps, the play toggle, the snap, the
intro row, fix-4, the tones, the portrait. F2 stays UNVERIFIED.
#playStop is a CIRCLE (border-radius:50%), not a square.

Every replacement is asserted (exact occurrence counts). Nothing is
written unless every assertion passes. A unified diff is printed and
scope-guarded: every changed line must carry one of the expected
markers. Writes are resilient (chunked, size+sha verified, retried)
for the EPERM flake. Run: python3 edit-cond.py
"""
import difflib, hashlib, json, os, re, subprocess, sys, time

HOME = os.path.expanduser('~')
RECORDS = os.path.join(HOME, 'workspace/team-nitro/agreement-flow-end-fix1-20261118')
WORK = os.path.join(RECORDS, 'work')
BASE = os.path.join(WORK, 'unfold-cond-base.html')
OUT = os.path.join(WORK, 'unfold-cond.html')

BASE_UNFOLD_SHA = 'c295061acf18b8458098d951f7a80d2b3056ff0afe77c48f4920c64cb757436c'
BASE_UNFOLD_BYTES = 104259

def sha(b): return hashlib.sha256(b).hexdigest()

def read_bytes(p):
    with open(p, 'rb') as f: return f.read()

def write_resilient(path, data):
    tmp = path + '.tmp-cond'
    last = None
    for attempt in range(40):
        try:
            wrote = False
            try:
                with open(tmp, 'wb') as f:
                    for i in range(0, len(data), 8192):
                        f.write(data[i:i+8192])
                    f.flush(); os.fsync(f.fileno())
                got = read_bytes(tmp)
                if len(got) == len(data) and sha(got) == sha(data):
                    wrote = True
            except Exception as e:
                last = e
            if not wrote:
                r = subprocess.run(['/bin/bash', '-c', 'cat > "$1"', 'bash', tmp],
                                   input=data, capture_output=True, timeout=120)
                if r.returncode != 0:
                    raise IOError('shell write failed rc=%d' % r.returncode)
                got = read_bytes(tmp)
                if len(got) != len(data) or sha(got) != sha(data):
                    raise IOError('shell verify failed: tmp %d bytes sha %s' % (len(got), sha(got)[:12]))
            os.replace(tmp, path)
            got2 = read_bytes(path)
            if len(got2) != len(data) or sha(got2) != sha(data):
                raise IOError('verify failed after replace')
            print('wrote %s %d B sha %s (attempt %d)' % (path, len(data), sha(data)[:12], attempt+1), flush=True)
            return
        except Exception as e:
            last = e
            print('write attempt %d failed: %s' % (attempt+1, e), flush=True)
            time.sleep(2 + attempt)
    raise IOError('write_resilient gave up on %s: %s' % (path, last))

def rep(text, old, new, count, label):
    n = text.count(old)
    if n != count:
        raise AssertionError('%s: expected %d occurrence(s) of %r, found %d' % (label, count, old[:100], n))
    return text.replace(old, new)

# ---------------------------------------------------------------- base input
base_b = read_bytes(BASE)
assert len(base_b) == BASE_UNFOLD_BYTES, 'base bytes mismatch: %d' % len(base_b)
assert sha(base_b) == BASE_UNFOLD_SHA, 'base sha mismatch: %s' % sha(base_b)
print('base OK: unfold %d B %s' % (len(base_b), BASE_UNFOLD_SHA[:8]))
u = base_b.decode('utf-8')
base_counts = {
    'cover': u.count('object-fit:cover'),
    'contain': u.count('object-fit:contain'),
    'no-voice': u.count('Voice not available'),
    'playTip': u.count('playTip'),
    'foot-logo': u.count('ib-foot-logo'),
    'play-note': u.count('play-note'),
    'script-end': u.count('Your world begins here.'),
}
print('base counts: %s' % json.dumps(base_counts))
assert base_counts['cover'] == 3, 'expected 3 cover hits (2 circular photos + 1 visual slot)'
assert base_counts['no-voice'] == 0, 'unfold already has a no-voice message?'
assert base_counts['playTip'] == 0, 'playTip already exists?'
assert base_counts['play-note'] == 1, 'expected .play-note CSS only (unused in markup)'

# ================================================================ CONDITION 1
OLD_SLOT = ".letter-beat.fp-smart-visual .lb-showcase img{width:100%;height:100%;object-fit:cover;aspect-ratio:auto}"
NEW_SLOT = ".letter-beat.fp-smart-visual .lb-showcase img{width:100%;height:100%;object-fit:contain;aspect-ratio:auto}"
u = rep(u, OLD_SLOT, NEW_SLOT, 1, 'C1 visual slot cover->contain')

# ================================================================ CONDITION 2
# --- C2a. the tip element (reuses the existing unused .play-note style) ---
OLD_PLAYWRAP_TAIL = """<button class="play-stop" id="playStop" type="button" hidden aria-label="Stop — stop reading the agreement">&#9632;</button>
</div>"""
NEW_PLAYWRAP_TAIL = """<button class="play-stop" id="playStop" type="button" hidden aria-label="Stop — stop reading the agreement">&#9632;</button>
</div>
<p class="play-note" id="playTip">Naya will talk you through this page</p>"""
u = rep(u, OLD_PLAYWRAP_TAIL, NEW_PLAYWRAP_TAIL, 1, 'C2a tip element')

# --- C2b. wirePlay: tip lookup + watchdog writes the message ---------------
OLD_TRI = "    var tri = btn ? btn.querySelector('.play-tri') : null;"
NEW_TRI = """    var tri = btn ? btn.querySelector('.play-tri') : null;
    var tip = document.getElementById('playTip');"""
u = rep(u, OLD_TRI, NEW_TRI, 1, 'C2b tip lookup')
OLD_STOPHIDDEN = "if (stopBtn) stopBtn.hidden = (st === 'idle');"
NEW_STOPHIDDEN = "if (stopBtn) stopBtn.hidden = (st === 'idle'); if (tip && st === 'playing') tip.textContent = 'Naya will talk you through this page';"
u = rep(u, OLD_STOPHIDDEN, NEW_STOPHIDDEN, 1, 'C2b setState restores default tip')
OLD_WD = "      var wd = setTimeout(function(){ if (state === 'playing' && idx === i) setState('idle'); }, 2500);"
NEW_WD = """      /* CONDITIONS (2026-11-18) — the no-voice tip, same wording as the
         intro player: on no-start the citizen is told the voice is not
         available instead of the player returning to idle silently.
         Watchdog mechanics unchanged: 2500ms, clears on start/end/error. */
      var wd = setTimeout(function(){ if (state === 'playing' && idx === i) { setState('idle'); if (tip) tip.textContent = 'Voice not available on this device \\u2014 read below'; } }, 2500);"""
u = rep(u, OLD_WD, NEW_WD, 1, 'C2b watchdog tip')

# ---------------------------------------------------------------- verify scope
new_counts = {
    'cover': u.count('object-fit:cover'),
    'contain': u.count('object-fit:contain'),
    'no-voice': u.count('Voice not available'),
    'playTip': u.count('playTip'),
    'foot-logo': u.count('ib-foot-logo'),
    'play-note': u.count('play-note'),
    'script-end': u.count('Your world begins here.'),
}
print('new counts: %s' % json.dumps(new_counts))
assert new_counts['cover'] == 2, 'cover must drop 3 -> 2 (visual slot only)'
assert new_counts['contain'] == 3, 'contain must rise 2 -> 3 (comment + generic rule + visual slot)'
assert new_counts['no-voice'] == 1, 'exactly one no-voice message'
assert new_counts['playTip'] == 2, 'playTip: id + getElementById only'
assert new_counts['foot-logo'] == base_counts['foot-logo'], 'divider moved!'
assert new_counts['script-end'] == base_counts['script-end'], 'distilled script moved!'
# the two surviving cover hits must be the circular photos only
for line in u.splitlines():
    if 'object-fit:cover' in line:
        assert ('deal-beat-photo' in line or 'deal-sign-photo' in line), 'unexpected cover survivor: %s' % line[:120]
# watchdog mechanics still present, exactly as before
for needle in ("window.speechSynthesis.getVoices()", "voiceschanged",
               "var v = pickVoice(); if (v) ut.voice = v;",
               "ut.onstart = function(){ clearTimeout(wd); };",
               "ut.onend = function(){ clearTimeout(wd);",
               "ut.onerror = function(){ clearTimeout(wd);"):
    assert needle in u, 'watchdog mechanic lost: %s' % needle
# unified diff, scope-guarded: every changed line must carry an expected marker
diff = list(difflib.unified_diff(base_b.decode('utf-8').splitlines(),
                                 u.splitlines(), lineterm=''))
changed = [ln[1:] for ln in diff if (ln.startswith('+') or ln.startswith('-')) and not ln.startswith(('+++', '---'))]
print('diff changed lines: %d' % len(changed))
for ln in changed:
    print('  %s' % ln[:160])
MARKERS = ('object-fit:contain', 'object-fit:cover', 'playTip', 'tip.textContent',
           'Voice not available', 'Naya will talk you through this page',
           'CONDITIONS (2026-11-18)', 'intro player:', 'available instead of',
           'Watchdog mechanics unchanged', 'setState(st)', 'stopBtn.hidden',
           'var wd = setTimeout')
for ln in changed:
    assert any(m in ln for m in MARKERS), 'SCOPE BREACH — changed line without expected marker: %r' % ln[:160]
print('diff scope guard OK: %d changed lines, all inside the two conditions' % len(changed))

# ---------------------------------------------------------------- write
write_resilient(OUT, u.encode('utf-8'))
print('EDIT-RESULT ' + json.dumps({
    'unfold_bytes': len(u.encode('utf-8')), 'unfold_sha': sha(u.encode('utf-8')),
    'base_bytes': len(base_b), 'base_sha': BASE_UNFOLD_SHA,
    'counts': new_counts, 'diff_lines': len(changed),
}, indent=1))

# node --check every script block
def node_check_file(path, label):
    txt = read_bytes(path).decode('utf-8')
    blocks = re.findall(r'<script>(.*?)</script>', txt, re.S)
    print('%s: %d script blocks' % (label, len(blocks)))
    for n, b in enumerate(blocks):
        tmp = os.path.join(WORK, 'nodecheck-cond-%s-%d.js' % (label, n))
        write_resilient(tmp, b.encode('utf-8'))
        r = subprocess.run(['node', '--check', tmp], capture_output=True, text=True)
        assert r.returncode == 0, 'node --check failed %s block %d: %s' % (label, n, r.stderr[:400])
        print('  node --check OK block %d (%d chars)' % (n, len(b)))
        os.remove(tmp)

node_check_file(OUT, 'unfold')
print('EDIT DONE')
