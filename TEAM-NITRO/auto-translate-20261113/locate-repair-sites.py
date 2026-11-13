#!/usr/bin/env python3
"""In-memory site locator for the repair round: reads the staged page bytes
from stdin, verifies sha, strips the embedded MW_I18N dict, and prints every
occurrence of each F1-F10 label in the remaining bytes with surrounding context
and a guarded/unguarded classification per the checker's rules."""
import hashlib, json, re, sys

raw = sys.stdin.buffer.read()
print("BYTES", len(raw), "SHA", hashlib.sha256(raw).hexdigest(), file=sys.stderr)
text = raw.decode("utf-8")

# Strip the embedded dictionary span: var MW_I18N = {...};
m = re.search(r"var MW_I18N\s*=\s*(\{.*?\});", text, re.S)
assert m, "MW_I18N span not found"
d = json.loads(m.group(1))
print("DICT keys:", {k: len(v) for k, v in d.items()}, file=sys.stderr)
stripped = text[:m.start()] + "/*DICT-STRIPPED*/" + text[m.end():]

LABELS = {
 "F1": ["Plugged into this world"],
 "F2": ["<b>Birth score</b> — every post, note and share moves the needle.",
        "Quiet — the first post, note or invite lights the needle.",
        "Reading your actions…"],
 "F3": ["No clicks yet — share a link and the first click lands here."],
 "F4": ["Posts, messages and invites together.",
        "Posts, notes, messages and invites together.",
        "A quiet stretch — the next post, message or invite lights the first bar.",
        "A quiet stretch — the next post, message or invite lights the first circle.",
        "A quiet stretch so far — the chart is waiting.",
        "The next post, note, message or invite lights the first bar.",
        "The next post, note, message or invite lights the first circle.",
        "The circles show the story week by week; the totals cover the whole story.",
        "The circles show the last 7 days; the totals cover the full period.",
        "Busiest: "],
 "F5": ["of recorded invites joined",
        "No invites yet — record the first one above.",
        "Record-only mode: saved, never sent — Joined honestly reads 0 until a friend connects.",
        "Invites are recorded — the first join is the milestone ahead.",
        " person has", " people have", " walked the whole invite journey.",
        "Joined"],
 "F6": ["Make a post", "Send a message", "Add a Smart Link", "Add to a list",
        "Add something", "Add"],
 "F7": ["Change picture", "Edit photo"],
 "F8": ["Video note", "Voice note"],
 "F9": ["Untitled note"],
 "F10": ["Hide breakdown", "Breakdown"],
}

def guarded(s, i, label):
    """Classify occurrence at index i in stripped text s.
    Mirrors the checker's rules, including the mwTr ternary fallback branch:
    an occurrence is guarded if it is the KEY argument of mwTr()/T(), the
    English FALLBACK branch of the same ternary (preceded by
    mwTr('SAME-LABEL'):'), a dict['...'] lookup, the (code==='en') ternary,
    a data-mw-tr/ph/aria/title element (or its paired native attribute), or
    a comment."""
    pre = s[max(0, i-260):i]
    # inside a T(...) call (incl. T(cond?'A':'B') branches): T has no fallback
    # literal, the call itself is the guard.
    if re.search(r"\bT\([^)]*$", pre):
        return "GUARDED(T-call)"
    # the [data-sl-dim] button's static 'Breakdown' text: mwApplyLang's T()
    # re-sync rewrites it on load and on switch (checker §3 exoneration).
    if label == "Breakdown" and re.search(r"data-sl-dim[^>]*>$", pre):
        return "GUARDED(T-resync)"
    # fallback branch of a mwTr ternary: mwTr('LABEL'):'
    if pre.endswith("window.mwTr?window.mwTr('" + label + "'):'") or \
       pre.endswith("mwTr('" + label + "'):'"):
        return "GUARDED(mwTr-fallback)"
    # key argument of a mwTr call
    if re.search(r"(window\.mwTr\?window\.mwTr\(|mwTr\(|[^a-zA-Z]T\()(['\"])$", pre):
        return "GUARDED(mwTr-call)"
    if re.search(r"dict\[['\"]$", pre):
        return "GUARDED(dict-lookup)"
    if re.search(r"\(code==='en'\)\?'$", pre):
        return "GUARDED(en-ternary)"
    # inside a data-mw-* attribute value, or the text of a data-mw-tr element
    if re.search(r"data-mw-(tr|ph|aria|title)=['\"][^'\"]*$", pre):
        return "GUARDED(data-mw-attr)"
    if re.search(r"<[^>]*data-mw-tr=['\"][^'\"]*['\"]>$", pre):
        return "GUARDED(data-mw-tr-elem)"
    if "<!--" in pre[-80:] and "-->" not in pre[-80:]:
        return "GUARDED(comment)"
    if "/*" in pre[-120:] and "*/" not in pre[pre.rfind("/*"):]:
        return "GUARDED(comment)"
    # paired native attribute: aria-label/title/placeholder whose value is the label
    # and the element carries data-mw-aria/title/ph
    if re.search(r'(aria-label|title|placeholder)=["\']$', pre):
        tagstart = s.rfind("<", 0, i)
        tag = s[tagstart:i+len(label)+2]
        if "data-mw-" in tag:
            return "GUARDED(paired-native-attr)"
        return "UNGUARDED(native-attr-no-data-mw)"
    return "UNGUARDED"

for f, labels in LABELS.items():
    for label in labels:
        idxs = [m2.start() for m2 in re.finditer(re.escape(label), stripped)]
        print(f"\n### {f}: {label!r} — {len(idxs)} occurrence(s) in stripped bytes")
        for i in idxs:
            line = stripped.count("\n", 0, i) + 1
            ctx = stripped[max(0, i-160):i+len(label)+160].replace("\n", "\\n")
            print(f"  line {line} [{guarded(stripped, i, label)}] ...{ctx}...")
