#!/usr/bin/env python3
"""Build the PHASE-2 shell from the bars-fixed shell (frozen base).
Base: hub-shell-bars-20261113/index-intel-today.html
  (5,559,180 B, sha a687f16a...02ac — re-verified here; stop on any move).
Output: index-intel-today-phase2.html (this work dir) — the base file is
never overwritten; the edited copy is what deploys as staging index.html.

Two insertions only (the brief's highlight-chain shell work):
E1 — the Hub card title link becomes the canonical /s/<slug> href.
    Today it is '#/smart-notes/sn<digits>' (a hash link). A browser
    that follows /s/<slug> is 302'd by the worker back into the Hub at
    the same note, so the destination is unchanged and the link is now
    the canonical article URL, in the static shell's own card template.
E2 — the <noscript> block gains a static Intel Today highlights strip:
    real <a href="/s/<slug>"> links (SN-2696 + one rep per cluster, from
    highlights.json) + the six cluster links (/?cluster=<slug>). Static
    markup in the shell bytes — the no-JS fallback crawlers read — not
    runtime-built JS. The cluster tabs themselves are NOT rebuilt: the
    Hub's existing auto-organizer already renders All + the six clusters
    + per-topic tabs with ?cluster= arrivals (verified first-hand).
"""
import hashlib, json, sys

WD = "/home/hatch/workspace/team-nitro/seo-ai-backend-20261113"
BASE = "/home/hatch/workspace/team-nitro/hub-shell-bars-20261113/index-intel-today.html"
OUT = WD + "/index-intel-today-phase2.html"
SHELL_SHA = "a687f16a666f27875dcc2cdb6dbe5fca113cf7eed610d76ff5b39ee8fc8d02ac"

def sha(b): return hashlib.sha256(b).hexdigest()

raw = open(BASE, "rb").read()
assert sha(raw) == SHELL_SHA, f"SHELL MOVED: {sha(raw)}"
shell = raw.decode("utf-8")
print(f"OK base shell: {len(raw)} B sha {SHELL_SHA[:12]}")

# ---- E1: canonical card title links ----
old_e1 = """    const titleLink = el('a', 'ib-title-link');
    titleLink.href = snMatch
      ? '#/smart-notes/sn' + snMatch[1]
      : '#/smart-notes/' + String(note.id || ('note-' + idx)).toLowerCase();"""
assert shell.count(old_e1) == 1, f"E1 anchor: {shell.count(old_e1)}"
new_e1 = """    /* PHASE 2 (2026-11-13): the card title links the CANONICAL article
       URL /s/<slug> (the Phase 1 step-8 gap, closed). A browser that
       follows it is 302'd by the worker back into the Hub at the same
       note, so the destination is unchanged; the link itself is now the
       article URL crawlers and sharers read. The SN number comes from
       the note's title where it carries one, else from the id (both
       parseInt-normalized, so sn0423 links /s/sn423 — the worker's
       canonical form, never the zero-padded id form); otherwise the id
       slug, as the P2 fix2 rule already did. */
    const titleLink = el('a', 'ib-title-link');
    const snTitle = String(note.title || '').match(/SN-(\\d+)/);
    titleLink.href = snTitle
      ? '/s/sn' + parseInt(snTitle[1], 10)
      : snMatch
      ? '/s/sn' + parseInt(snMatch[1], 10)
      : '/s/' + String(note.id || ('note-' + idx)).toLowerCase();"""
shell = shell.replace(old_e1, new_e1)
print("OK E1 card title links -> canonical /s/<slug>")

# ---- E2: static highlights strip in <noscript> ----
highlights = json.load(open(WD + "/highlights.json"))
clusters = json.load(open(WD + "/cluster-topics.json"))["mapping"]
assert len(highlights) >= 6, f"highlights too few: {len(highlights)}"
links = " \u00b7 ".join(
    f'<a href="/s/{h["slug"]}" style="color:#ffbf3d">{h["displayTitle"]}</a>'
    for h in highlights)
cluster_links = " \u00b7 ".join(
    f'<a href="/?cluster={slug}" style="color:#fff">{info["label"]}</a>'
    for slug, info in clusters.items())
strip = (
    '\n    <nav aria-label="Intel Today highlights" style="max-width:640px;margin:28px auto 0;text-align:left">'
    '<h2 style="font-size:18px;letter-spacing:.06em;margin:0 0 10px">Intel Today \u2014 highlights</h2>'
    f'<p style="font-size:15px;line-height:1.9;margin:0 0 12px">{links}</p>'
    f'<p style="font-size:14px;line-height:1.9;margin:0;opacity:.85">Clusters: {cluster_links}</p>'
    '</nav>')
old_ns = "please enable JavaScript to step through.</p></div>"
assert shell.count(old_ns) == 1, f"noscript anchor: {shell.count(old_ns)}"
shell = shell.replace(old_ns, "please enable JavaScript to step through.</p>" + strip + "</div>")
print(f"OK E2 noscript highlights strip: {len(highlights)} note links + {len(clusters)} cluster links")

out = shell.encode("utf-8")
open(OUT, "wb").write(out)
print(f"wrote {OUT}: {len(out)} B sha={sha(out)[:12]}")
print(f"   href=\"/s/ occurrences in edited shell bytes: {shell.count('href=\"/s/')}")
print(f"   href=\"/?cluster= occurrences: {shell.count('href=\"/?cluster=')}")
print(f"   '#/smart-notes/sn' title-link occurrences left: {shell.count(chr(39) + '#/smart-notes/sn')}")
