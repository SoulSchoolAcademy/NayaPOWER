#!/usr/bin/env python3
"""AGREEMENT FIX PASS (2026-11-15) — edit walk-beginning-fixed.html in place.

Fix 1: rebalance beats 58/59/60 to 4/4/4 sentences (was 6/3/3). No new
board, no renumbering: sentences move between boards, never rewritten,
dropped, or added. Words and order identical.
Fix 2a: rotate eye-note photos off /agmt-b02.jpg (was x11 notes) — every
note gets a distinct file except b09 (2 notes); b02 keeps exactly 1 note.
Fix 2b: faces onto §4 boards 37,40,43,46,49,52,55,58,61,64,67,70,73,76
(every third board), harvested pattern verbatim from beat 36 (face-left +
deal-beat-photo as first child of .ib-blocktop). Seven still-unused
face-library pictures used first (b00,b01,b03,b05,b10,b11,b12); b12
(Naya_Profile_Black.jpg) is the new KV key wbf-agmt-b12.jpg.
Every replacement asserted exactly-once before write. Temp-file write +
os.replace in the same directory, never truncate-first. Base copy kept as
walk-beginning-fixed-7553d76b-baseline.html.
"""
import hashlib, os, shutil, sys

D = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(D, "walk-beginning-fixed.html")
BASE_SHA = "7553d76bf2067d60838ec94894d4952acd2a1a8772802727f845f01a79d60af2"

raw = open(SRC, "rb").read()
assert hashlib.sha256(raw).hexdigest() == BASE_SHA, "base sha mismatch"
assert len(raw) == 3493483, "base bytes mismatch"
shutil.copyfile(SRC, os.path.join(D, "walk-beginning-fixed-7553d76b-baseline.html"))
h = raw.decode("utf-8")

def rep(old, new, tag):
    global h
    n = h.count(old)
    assert n == 1, f"{tag}: expected 1 occurrence, found {n}"
    h = h.replace(old, new)
    print(f"OK {tag}")

# ---------------- FIX 1: beats 58/59/60 -> 4/4/4 ----------------
# Beat 58 keeps only its first paragraph (4 sentences).
rep(
 '<div class="ib-nutshell"><p>I know what you might be thinking. &ldquo;What&rsquo;s the catch?&rdquo; &ldquo;Is this a scam?&rdquo; Those are fair questions.</p><p>So here&rsquo;s the logic: nobody buys their way in, nobody is promised income just for joining, and nobody is rewarded for fake accounts or moving money without delivering anything real.</p><p>A real person chooses something valuable.</p></div>',
 '<div class="ib-nutshell"><p>I know what you might be thinking. &ldquo;What&rsquo;s the catch?&rdquo; &ldquo;Is this a scam?&rdquo; Those are fair questions.</p></div>',
 "fix1 beat58 -> 4 sentences")
# Beat 59 takes the logic + real-person sentences, then its own two.
rep(
 '<article class="intel-board tone-purple letter-beat" data-beat="59" hidden><div class="ib-blocktop"><div class="ib-identity"><span class="ib-jewel" aria-hidden="true">&#9670;</span><div><span class="ib-kind">QUESTION 4 &middot; 24 OF 42</span><h2 class="ib-title">What&rsquo;s the agreement about?</h2></div></div></div><div class="ib-nutshell"><p>They make a real purchase.</p><p>The payment is verified.</p><p>And an eligible ambassador who helped bring them can receive a share.</p></div>',
 '<article class="intel-board tone-purple letter-beat" data-beat="59" hidden><div class="ib-blocktop"><div class="ib-identity"><span class="ib-jewel" aria-hidden="true">&#9670;</span><div><span class="ib-kind">QUESTION 4 &middot; 24 OF 42</span><h2 class="ib-title">What&rsquo;s the agreement about?</h2></div></div></div><div class="ib-nutshell"><p>So here&rsquo;s the logic: nobody buys their way in, nobody is promised income just for joining, and nobody is rewarded for fake accounts or moving money without delivering anything real.</p><p>A real person chooses something valuable.</p><p>They make a real purchase.</p><p>The payment is verified.</p></div>',
 "fix1 beat59 -> 4 sentences")
# Beat 60 takes the ambassador sentence, then its own three.
rep(
 '<article class="intel-board tone-purple letter-beat" data-beat="60" hidden><div class="ib-blocktop"><div class="ib-identity"><span class="ib-jewel" aria-hidden="true">&#9670;</span><div><span class="ib-kind">QUESTION 4 &middot; 25 OF 42</span><h2 class="ib-title">What&rsquo;s the agreement about?</h2></div></div></div><div class="ib-nutshell"><p>That&rsquo;s a referral-based business model.</p><p>It&rsquo;s not magic.</p><p>And it doesn&rsquo;t mean everybody is guaranteed to make money.</p></div>',
 '<article class="intel-board tone-purple letter-beat" data-beat="60" hidden><div class="ib-blocktop"><div class="ib-identity"><span class="ib-jewel" aria-hidden="true">&#9670;</span><div><span class="ib-kind">QUESTION 4 &middot; 25 OF 42</span><h2 class="ib-title">What&rsquo;s the agreement about?</h2></div></div></div><div class="ib-nutshell"><p>And an eligible ambassador who helped bring them can receive a share.</p><p>That&rsquo;s a referral-based business model.</p><p>It&rsquo;s not magic.</p><p>And it doesn&rsquo;t mean everybody is guaranteed to make money.</p></div>',
 "fix1 beat60 -> 4 sentences")

# ---------------- FIX 2a: eye-note photos off b02 ----------------
# (note id, old src, new src). collective + land keep theirs; hold keeps b02.
NOTES = [
    ("deal-note-business", "/agmt-b09.jpg", "/agmt-b11.jpg"),
    ("deal-note-deed",     "/agmt-b02.jpg", "/agmt-b00.jpg"),
    ("deal-note-cost",     "/agmt-b02.jpg", "/agmt-b01.jpg"),
    ("deal-note-joining",  "/agmt-b02.jpg", "/agmt-b03.jpg"),
    ("deal-note-privacy",  "/agmt-b02.jpg", "/agmt-b05.jpg"),
    ("deal-note-vault",    "/agmt-b02.jpg", "/agmt-b10.jpg"),
    ("deal-note-save",     "/agmt-b02.jpg", "/agmt-b12.jpg"),
    ("deal-note-job",      "/agmt-b02.jpg", "/agmt-b04.jpg"),
    ("deal-note-earn",     "/agmt-b02.jpg", "/agmt-b07.jpg"),
    ("deal-note-skeptic",  "/agmt-b02.jpg", "/agmt-b08.jpg"),
    ("deal-note-cap",      "/agmt-b02.jpg", "/agmt-b09.jpg"),
]
for nid, old, new in NOTES:
    rep(f'<div class="deal-eye-note" id="{nid}" hidden><img class="deal-quote-photo" src="{old}" alt="">',
        f'<div class="deal-eye-note" id="{nid}" hidden><img class="deal-quote-photo" src="{new}" alt="">',
        f"fix2a {nid} {old} -> {new}")

# ---------------- FIX 2b: faces onto §4 boards ----------------
# beat -> portrait file. All 7 still-unused pictures first (b00,b01,b03,
# b05,b10,b11,b12), then reuses; repeats only b10/b11, 36 boards apart.
FACES = {37: "b10", 40: "b11", 43: "b00", 46: "b01", 49: "b03", 52: "b05",
         55: "b12", 58: "b06", 61: "b04", 64: "b09", 67: "b08", 70: "b07",
         73: "b10", 76: "b11"}
for beat, f in FACES.items():
    ext = "png" if f == "b06" else "jpg"
    rep(f'<article class="intel-board tone-purple letter-beat" data-beat="{beat}" hidden><div class="ib-blocktop">',
        f'<article class="intel-board tone-purple letter-beat face-left" data-beat="{beat}" hidden><div class="ib-blocktop"><img class="deal-beat-photo" src="/agmt-{f}.{ext}" alt="Naya speaking">',
        f"fix2b beat{beat} -> /agmt-{f}.{ext}")

# ---------------- write (temp + replace, same dir) ----------------
out = h.encode("utf-8")
tmp = os.path.join(D, ".fixpass-tmp.html")
with open(tmp, "wb") as fh:
    fh.write(out)
assert hashlib.sha256(open(tmp, "rb").read()).hexdigest() == hashlib.sha256(out).hexdigest()
os.replace(tmp, SRC)
print("WROTE", len(out), "B sha256", hashlib.sha256(out).hexdigest())
