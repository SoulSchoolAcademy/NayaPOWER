#!/usr/bin/env python3
"""Emblem Placement — IDENTITY + AGREEMENT UNFOLD (SPEC ONLY, 2026-11-17).

AUDIT-ONLY: proves the exact byte diffs for the follow-on round. NOTHING
is staged here — the walk-beginning worker cannot be reproduced right now
(the bridge presentation round owns the welcome file: disk welcome sha
e27c7fe1... vs the asserted 395794a3..., while the LIVE worker still
serves 395794a3...; staging a worker built on either welcome would wipe
the other round's bytes). The follow-on round applies these verified
diffs once the bridge round lands and the worker reproduces again.

IDENTITY (/identity.html, 376,814 B, sha 8c641f96...): the SAME four-corner
change as the certificate — the corner construction is byte-identical
(same slots, positions, rotations). apply_emblem() from the certificate
build is reused verbatim.
AGREEMENT UNFOLD (/agreement, 85,625 B, sha 842cae53...): ONE placement —
.deal-emblem, the official seal at the cover, centered above the H1
(after the steplabel, before "The Collective Agreement"), width
clamp(56px, 12vw, 72px), aspect-ratio 9/10 (the emblem's own 1800:2000),
drop-shadow elevation. The red wax .deal-seal (the agreed stamp) is
NOT touched — it is the agreement's stamp, not to be redesigned. No
rendered word changes on either page. No orbit on either seal (a seal
is stamped, not spun).
"""
import base64
import difflib
import hashlib
import importlib.util
import os
import re
import sys

sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
sys.path.insert(0, os.path.expanduser("~/workspace/ninaya/integration"))

HERE = os.path.expanduser("~/workspace/team-nitro/emblem-placement-20261117")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_emb = load("embcert", os.path.join(HERE, "build-emblem-certificate.py"))
_chk = load("lawscheck", os.path.expanduser("~/workspace/team-nitro/check-design-laws.py"))

IDENT_PATH = os.path.expanduser("~/workspace/team-nitro/walk-v23-assembly-20261114/identity-fixed.html")
IDENT_SHA = "8c641f96d31818b610d1a243d945dfb5c68e6016e036b7afb11b72445330013d"
UNFOLD_PATH = os.path.expanduser("~/workspace/team-nitro/agreement-unfold-fix-20261117/agreement-unfold-fixed.html")
UNFOLD_SHA = "842cae537a7fced836448e4af09ac9b9506285bf8af9b8ccc2adb6d2f7a57fb4"
EMBLEM_SHA = "1e3deb55ae00552a2cbe26baaa610e04dc91812b6bc68c3532a061be020c8bf4"


def sha(b):
    return hashlib.sha256(b if isinstance(b, bytes) else b.encode()).hexdigest()


def visible(html):
    html = re.sub(r"<style.*?</style>", " ", html, flags=re.S)
    html = re.sub(r"<script.*?</script>", " ", html, flags=re.S)
    html = re.sub(r"<!--.*?-->", " ", html, flags=re.S)
    html = re.sub(r"<[^>]+>", " ", html)
    return " ".join(html.split())


def laws_failures(text):
    fails = []
    for i, line in enumerate(text.splitlines(), 1):
        for rx in _chk.GRAY_RES:
            if rx.search(line):
                fails.append(f"{i}: GRAY: {line.strip()[:100]}")
                break
    for m in _chk.FONTSIZE_RE.finditer(text):
        vals = [float(v) for v in m.groups() if v is not None]
        if vals and min(vals) < 17:
            fails.append(f"{text[:m.start()].count(chr(10)) + 1}: SIZE: {m.group(0)}")
    for m in _chk.COLOR_DECL_RE.finditer(text):
        val = m.group(1).strip().lower()
        if val.startswith("var("):
            continue
        val = val.split()[0].rstrip(";")
        if val in _chk.FORBIDDEN_TEXT:
            fails.append(f"{text[:m.start()].count(chr(10)) + 1}: TEXT-COLOR: {m.group(0).strip()[:100]}")
    return fails


def laws_new_only(base, new):
    fb, fn = laws_failures(base), laws_failures(new)
    key = lambda f: f.split(": ", 1)[1] if ": " in f else f
    base_keys = {key(x) for x in fb}
    return [f for f in fn if key(f) not in base_keys], len(fb), len(fn)


def apply_unfold_emblem(base, b64):
    new = base
    # --- CSS: the cover seal rule, inserted before the .deal-title rule.
    anchor = ".deal-title{font-family:Marcellus,Georgia,serif;font-size:30px;"
    assert new.count(anchor) == 1, "deal-title anchor not unique — STOP"
    rule = (
        "/* EMBLEM PLACEMENT (2026-11-17, Shawn 21:08Z): the official emblem\n"
        "   is the seal at the cover of the Collective Agreement — centered\n"
        "   above the title, one placement, never pasted everywhere. Width\n"
        "   clamp(56px, 12vw, 72px); aspect-ratio 9/10 is the emblem's own\n"
        "   1800:2000. contain shows the whole emblem; the drop-shadow seats\n"
        "   it as a real object. The red wax .deal-seal below is untouched —\n"
        "   it is the agreement's stamp. No orbit: a seal is stamped. */\n"
        ".deal-emblem{display:block;width:clamp(56px,12vw,72px);aspect-ratio:9/10;"
        "margin:0 auto 8px;background:url(\"data:image/png;base64," + b64 + "\") "
        "center/contain no-repeat;filter:drop-shadow(0 8px 16px rgba(0,0,0,0.65));}\n"
    )
    new = new.replace(anchor, rule + anchor, 1)
    # --- Markup: the seal div between the steplabel and the H1.
    m_anchor = '<p class="letter-steplabel">NayaNET &middot; The Collective Agreement</p>\n<h1 class="deal-title">'
    assert new.count(m_anchor) == 1, "steplabel+H1 anchor not unique — STOP"
    new = new.replace(
        m_anchor,
        '<p class="letter-steplabel">NayaNET &middot; The Collective Agreement</p>\n'
        '<div class="deal-emblem" aria-hidden="true"></div><h1 class="deal-title">', 1)
    return new


def main():
    b64 = _emb.emblem_b64()

    # ---- IDENTITY (same corner change, proved in memory).
    ident = open(IDENT_PATH, encoding="utf-8").read()
    assert sha(ident) == IDENT_SHA, f"identity base moved: {sha(ident)} — STOP"
    new_ident = _emb.apply_emblem(ident, b64)
    assert new_ident.count("data:image/png;base64,") == 1
    assert new_ident.count("data:image/jpeg;base64,") == ident.count("data:image/jpeg;base64,") - 1
    for frag in [
        ".corner-crest { position: absolute; z-index: 5; width: 100px; height: 122px;",
        ".cm-tl { top: 20px; left: 20px; transform: translate(-50%, -50%) rotate(-59deg); }",
        ".cm-br { bottom: 20px; right: 20px; transform: translate(50%, 50%) rotate(121deg); }",
        '<div class="cert-title">Certificate of Collective Agreement</div>',
        "This certifies that",
        'class="cert-seal"',
    ]:
        assert frag in new_ident, f"identity piece moved: {frag[:60]} — STOP"
    assert visible(ident) == visible(new_ident), "identity visible words changed — STOP"
    no, nb, nn = laws_new_only(ident, new_ident)
    print(f"IDENTITY: {len(ident.encode())} B -> {len(new_ident.encode())} B "
          f"sha={sha(new_ident)}")
    print(f"  laws: base {nb} FAILs, new {nn} FAILs, new-only {len(no)}")
    assert not no, f"identity new laws FAILs: {no}"
    d = list(difflib.unified_diff(ident.splitlines(), new_ident.splitlines(), lineterm="", n=0))
    print(f"  diff: +{sum(1 for ln in d if ln.startswith('+') and not ln.startswith('+++'))} "
          f"-{sum(1 for ln in d if ln.startswith('-') and not ln.startswith('---'))} lines")

    # ---- UNFOLD (cover seal, proved in memory).
    unfold = open(UNFOLD_PATH, encoding="utf-8").read()
    assert sha(unfold) == UNFOLD_SHA, f"unfold base moved: {sha(unfold)} — STOP"
    new_unfold = apply_unfold_emblem(unfold, b64)
    assert new_unfold.count("data:image/png;base64,") == 1
    assert '<div class="deal-emblem" aria-hidden="true"></div>' in new_unfold
    assert ".deal-seal, .deal-seal{width:120px;height:120px;" in new_unfold, "deal-seal moved — STOP"
    assert visible(unfold) == visible(new_unfold), "unfold visible words changed — STOP"
    no, nb, nn = laws_new_only(unfold, new_unfold)
    print(f"UNFOLD: {len(unfold.encode())} B -> {len(new_unfold.encode())} B "
          f"sha={sha(new_unfold)}")
    print(f"  laws: base {nb} FAILs, new {nn} FAILs, new-only {len(no)}")
    assert not no, f"unfold new laws FAILs: {no}"
    d = list(difflib.unified_diff(unfold.splitlines(), new_unfold.splitlines(), lineterm="", n=0))
    print(f"  diff: +{sum(1 for ln in d if ln.startswith('+') and not ln.startswith('+++'))} "
          f"-{sum(1 for ln in d if ln.startswith('-') and not ln.startswith('---'))} lines")
    # Emblem decodes from the new unfold bytes.
    m = re.search(r'data:image/png;base64,([A-Za-z0-9+/=]+)', new_unfold)
    assert sha(base64.b64decode(m.group(1))) == EMBLEM_SHA
    # ---- WORKER SIZE LAW (measured 2026-11-17 21:3xZ): the walk-beginning
    # worker CANNOT carry two emblem copies. Live worker gzip is ~4.28MB;
    # one 3,539,340-char base64 copy leaves ~2.67MB of headroom, two copies
    # EXCEED the 10,485,760 gzip limit by ~870KB. The follow-on MUST serve
    # the emblem ONCE per worker (a shared /naya-emblem.png route, the way
    # the worker already serves /login-obsidian.jpg from KV) and reference
    # it by URL from identity + unfold — the byte diffs above are the
    # placement spec, not the staging shape.
    _sim = load("certcurrent2", os.path.expanduser(
        "~/workspace/team-nitro/pricing-certificate-current-20261117/build-certificate.py"))._bt._sim
    st, raw = _sim.api("GET", "/naya-walk-beginning-staging")
    assert st == 200
    _, wb, _ = _sim.split_multipart(raw)
    import gzip as _gz
    gz = len(_gz.compress(wb))
    print(f"WORKER-SIZE: live walk-beginning worker {len(wb)} B raw, gzip {gz} B; "
          f"headroom {10485760 - gz} B; one emblem copy leaves "
          f"{10485760 - gz - 3539340} B; two copies leave "
          f"{10485760 - gz - 2 * 3539340} B (NEGATIVE = over the limit)")
    assert 10485760 - gz - 2 * 3539340 < 0, "two-copy fit changed — re-measure"
    print("SPEC OK — identity + unfold diffs proven in memory; staging sequenced after the bridge round lands")
    return {"identity": new_ident, "unfold": new_unfold}


if __name__ == "__main__":
    main()
