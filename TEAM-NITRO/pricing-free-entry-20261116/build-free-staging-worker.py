#!/usr/bin/env python3
"""Build the pricing free-entry route staging worker (F4, 2026-11-17).
Harvests, never rebuilds:
  - walk-beginning-fixed.html (sha df17ac67…) -> WALK_FREE, with 4 free
    patches: Hub door first (+recommended), Dashboard un-recommended,
    free line on the end slide, free-entry localStorage flag at boot.
  - identity-fixed.html (sha 84c2b29a…) -> FREE_ENTRY, with 3 free patches:
    WALKTHROUGH_URL /welcome -> /free/walk, free line + info-eye under
    ENTER (eye SVG harvested verbatim from the pricing page's .plan-eye),
    eye toggles the Naya Free explainer.
  - the fetch handler of walk-beginning-staging-worker.js (the proven
    walk staging worker) -> routes renamed to the free path; /api/* logic
    verbatim (claim, welcome/me, welcome/complete); alias redirects kept
    (the walk's reveal pages are relative /<alias> links).
  - the Supabase anon key is read programmatically from the live-extracted
    identity file and embedded ONLY in this staging worker (the key is the
    public anon key already shipped in the live page; never printed).
Worker: naya-pricing-free-staging. Serves:
  /            -> the free-route index (staging status page)
  /free        -> free entry (name + alias claim, no payment, no card)
  /free/walk   -> the walk, free mode, ends Hub-first
  /free/hub    -> 302 to the Hub (https://nayanet.app/)
  /api/claim, /api/welcome/me, /api/welcome/complete -> harvested verbatim
  /<alias>[/business|space|dashboard] -> 302 to the live nayanet.app pages
KV binding: WELCOME_ASSETS (the live nayanet KV namespace) — completions
are stored as complete_<alias> keys, test aliases only.
Writes: free-entry.html, walk-free.html, free-index.html,
free-staging-worker.js (+ worker-meta.json) into the round dir.
All writes go through the retrying writer (EPERM flake).
"""
import hashlib
import importlib.util
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
sys.path.insert(0, os.path.expanduser("~/workspace/ninaya/integration"))
_spec = importlib.util.spec_from_file_location(
    "bv78", os.path.join(HERE, "build-v78.py"))
_bv78 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_bv78)
shell_write = _bv78.shell_write
_dn_spec = importlib.util.spec_from_file_location(
    "deploy_ninaya", os.path.expanduser("~/workspace/ninaya/integration/deploy-ninaya.py"))
_dn = importlib.util.module_from_spec(_dn_spec)
_dn_spec.loader.exec_module(_dn)
js_encode = _dn.js_encode

WALK_SRC = os.path.expanduser(
    "~/workspace/team-nitro/walk-beginning-fix-20261111/walk-beginning-fixed.html")
WALK_SHA = "df17ac67"
IDENT_SRC = os.path.expanduser(
    "~/workspace/team-nitro/walk-beginning-fix-20261111/identity-fixed.html")
IDENT_SHA = "84c2b29a"
LIVE_IDENT = os.path.expanduser(
    "~/workspace/team-nitro/walk-fix-20261111/identity-live-extracted.html")
WALK_WORKER_SRC = os.path.expanduser(
    "~/workspace/team-nitro/walk-beginning-fix-20261111/walk-beginning-staging-worker.js")

FREE_WORKER = "naya-pricing-free-staging"
FREE_HOST = "https://naya-pricing-free-staging.nayapower.workers.dev"

EYE_SVG = ('<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M2.6 12C5.1 6.9 8.7 4.6 12 4.6S18.9 6.9 21.4 12c-2.5 5.1-6.1 7.4-9.4 7.4S5.1 17.1 2.6 12Z" fill="rgba(255,255,255,.20)" stroke="#fff" stroke-width="1.6" stroke-linejoin="round"/><circle cx="12" cy="12" r="3.9" fill="#fff"/><circle cx="12" cy="12" r="2" fill="#1a1030"/><circle cx="13.3" cy="10.5" r="1" fill="#fff"/></svg>')


def replace_once(page, old, new, name):
    n = page.count(old)
    assert n == 1, f"{name}: anchor count {n}, expected 1 — STOP"
    return page.replace(old, new)


def build_walk_free():
    raw = open(WALK_SRC, "rb").read()
    assert hashlib.sha256(raw).hexdigest().startswith(WALK_SHA), \
        "walk sha is not the quote-fix sha — STOP"
    w = raw.decode("utf-8")
    # P1: the recommendation paragraph recommends the Hub first now.
    reco_old = ("Recommended first &mdash; start here, get your Smart Link. "
                "It&rsquo;s your identity, your smart name, your ambassador link, "
                "and your tracking, so you can get paid every Wednesday.")
    reco_new = ("Recommended first &mdash; start in your Hub. Everything, in one place "
                "&mdash; then get your Smart Link on your Dashboard.")
    w = replace_once(w, reco_old, reco_new, "walk reco")
    # P2: doors — Hub first and recommended; Dashboard un-recommended.
    doors = re.findall(r'<button class="p3-door[^>]*>.*?</button>', w)
    assert len(doors) == 5, f"door count {len(doors)} — STOP"
    order = [re.search(r'data-door="([^"]+)"', d).group(1) for d in doors]
    assert order == ["Dashboard", "Personal", "Business", "Space", "Hub"], \
        f"door order {order} — STOP"
    hub = doors[4].replace('class="p3-door"',
                           'class="p3-door p3-door-rec"', 1)
    hub = hub.replace("Everything, in one place</span>",
                      "Everything, in one place &mdash; start here</span>", 1)
    dash = doors[0].replace('class="p3-door p3-door-rec"',
                            'class="p3-door"', 1)
    dash = dash.replace("Get your Smart Link &mdash; recommended first</span>",
                        "Get your Smart Link</span>", 1)
    assert 'p3-door-rec' in hub and 'recommended first' not in dash
    new_doors = "\n".join([hub, dash, doors[1], doors[2], doors[3]])
    w = replace_once(w, "\n".join(doors), new_doors, "walk doors")
    # P3: free line on the end slide, after the welcome paragraph.
    w = replace_once(
        w, "Invite the world.</p>",
        "Invite the world.</p> <p class=\"p3-welcome\">You&rsquo;re in on Naya Free "
        "&mdash; zero cost, zero risk. Step up any time in Settings.</p>",
        "walk free line")
    # P4: free-entry flag at boot.
    w = replace_once(
        w, "/* --- boot --- */\n(function boot(){",
        "/* FREE-ENTRY (F4): this copy runs the free walk — no payment, no card; "
        "the citizen entered free from pricing. */\n  "
        "try{localStorage.setItem('nayanet_free_entry','1');}catch(e){}\n  "
        "/* --- boot --- */\n(function boot(){",
        "walk free flag")
    assert "nayanet_free_entry" in w
    assert w.count("data-door=\"Hub\"") == 1
    return w


def build_free_entry():
    raw = open(IDENT_SRC, "rb").read()
    assert hashlib.sha256(raw).hexdigest().startswith(IDENT_SHA), \
        "identity sha is not the entry-identity-fix sha — STOP"
    d = raw.decode("utf-8")
    # P1: the walkthrough lives at /free/walk on this worker.
    d = replace_once(d, "WALKTHROUGH_URL = '/welcome'",
                     "WALKTHROUGH_URL = '/free/walk'", "entry walk url")
    # P2: free line + info-eye under ENTER, before the claim line.
    claim_anchor = ('<p class="cert-claim">Claim your Smart Name — yours alone: '
                    'one person, one route, forever.</p>')
    free_block = (
        '<p class="cert-claim free-line"><button class="free-eye" id="freeEye" '
        'type="button" aria-expanded="false" aria-controls="freeWhat" '
        'aria-label="What is Naya Free?">' + EYE_SVG + '</button>'
        '<span>Enter free &mdash; no payment, no card.</span></p>\n        '
        '<p class="cert-privacy" id="freeWhat" hidden>Naya Free is the free way in: '
        'your Smart Name, your pages, your Hub &mdash; zero cost, zero risk. '
        'Step up any time in Settings.</p>\n        '
        '<script>(function(){var b=document.getElementById(\'freeEye\'),'
        'n=document.getElementById(\'freeWhat\');if(!b||!n)return;'
        'b.addEventListener(\'click\',function(){var s=n.hidden;'
        'n.hidden=!s;b.setAttribute(\'aria-expanded\',String(s));});})();</script>\n        ')
    d = replace_once(d, claim_anchor, free_block + claim_anchor, "entry free line")
    # P3: CSS for the free line + eye, before the first </style>.
    css = (
        "/* FREE ENTRY (F4): the free line + info-eye on the free entry page. "
        "Eye SVG harvested verbatim from the pricing page's .plan-eye. */\n    "
        ".free-line{display:flex;gap:10px;align-items:center;justify-content:center}\n    "
        ".free-eye{flex:none;width:34px;height:34px;border-radius:10px;display:grid;"
        "place-items:center;cursor:pointer;background:#0a0a10;"
        "border:1.5px solid rgba(255,255,255,.9);"
        "box-shadow:inset 0 1px 0 rgba(255,255,255,.35),0 4px 12px rgba(0,0,0,.55)}\n    "
        ".free-eye svg{width:20px;height:20px}\n    "
        ".free-eye:hover{border-color:#2fe89e;"
        "box-shadow:inset 0 1px 0 rgba(255,255,255,.35),"
        "0 0 16px rgba(47,232,158,.65),0 4px 12px rgba(0,0,0,.55)}\n    "
        ".free-eye:active{transform:scale(.97)}\n    ")
    assert d.count("</style>") >= 1
    d = d.replace("</style>", css + "</style>", 1)
    assert "WALKTHROUGH_URL = '/free/walk'" in d
    assert d.count('id="freeEye"') == 1
    assert d.count('id="freeWhat"') == 1
    return d


FREE_INDEX = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>NayaNET — Free entry route (staging)</title>
<style>body{margin:0;background:#060609;color:#fff;font-family:system-ui,-apple-system,sans-serif;display:flex;min-height:100vh;align-items:center;justify-content:center;padding:24px;box-sizing:border-box}.card{max-width:640px;width:100%;text-align:center;background:linear-gradient(135deg,#1e1e26 0%,#0a0a0f 50%,#1e1e26 100%);border:1.5px solid rgba(47,232,158,.85);border-radius:22px;padding:32px 24px;box-shadow:inset 0 1px 0 rgba(255,255,255,.15),0 8px 24px rgba(0,0,0,.5)}h1{font-size:28px;margin:0 0 12px}p{font-size:16px;line-height:1.6;color:#fff;margin:0 0 12px}.sub{font-size:14px;color:#d5f5e6}.pill{display:inline-block;margin:8px 6px 0;padding:14px 26px;border-radius:999px;border:1.5px solid rgba(47,232,158,.9);background:linear-gradient(180deg,#1a1a22 0%,#0a0a0f 45%,#050507 100%);color:#fff;text-decoration:none;font-weight:800;font-size:15px;box-shadow:inset 0 1px 0 rgba(255,255,255,.35),0 0 24px rgba(47,232,158,.35),0 12px 32px rgba(0,0,0,.65)}.pill:hover{transform:translateY(-2px);box-shadow:inset 0 1px 0 rgba(255,255,255,.35),0 0 36px rgba(47,232,158,.8),0 14px 36px rgba(0,0,0,.65)}.note{margin-top:20px;font-size:13px;color:#cfc9e8}</style></head>
<body><main class="card">
<h1>Enter free — the route, staged</h1>
<p>This staging worker serves the pricing free-entry route (F4): enter free, no payment, no card — walk the walk — end in the Hub.</p>
<a class="pill" href="/free">Enter free ◆</a>
<a class="pill" href="/free/walk">Walk free ◆</a>
<a class="pill" href="/free/hub">Hub ◆</a>
<p class="sub">STAGING — not live. Live deploy is Shawn&rsquo;s tap.</p>
<p class="note">Pricing (staged): <a style="color:#fff" href="__PRICING_STAGED__">v78 with the free button on top</a></p>
</main></body></html>
"""


def build_worker(walk_free, free_entry):
    src = open(WALK_WORKER_SRC, encoding="utf-8").read()
    i = src.find("export default {")
    assert i > 0, "walk worker handler not found — STOP"
    handler = src[i:]
    # The harvested handler's page branches, renamed to the free path.
    old_root = ('    if (p === "/") {\n      return new Response(WELCOME, '
                '{ headers: { "content-type": "text/html;charset=utf-8", '
                '"cache-control": "no-store" } });\n    }')
    new_root = ('    if (p === "/") {\n      return new Response(FREE_INDEX, '
                '{ headers: { "content-type": "text/html;charset=utf-8", '
                '"cache-control": "no-store" } });\n    }')
    handler = replace_once(handler, old_root, new_root, "worker /")
    old_ident = ('    if (p === "/identity.html") {\n      return new Response(IDENTITY, '
                 '{ headers: { "content-type": "text/html;charset=utf-8", '
                 '"cache-control": "no-store" } });\n    }')
    assert handler.count(old_ident) == 1
    handler = handler.replace(old_ident + "\n", "", 1)
    old_walk = ('    if (p === "/welcome" || p === "/welcome/") {\n      return new Response(WALK, '
                '{ headers: { "content-type": "text/html;charset=utf-8", '
                '"cache-control": "no-store" } });\n    }')
    new_walk = ('    if (p === "/free") {\n      return new Response(FREE_ENTRY, '
                '{ headers: { "content-type": "text/html;charset=utf-8", '
                '"cache-control": "no-store" } });\n    }\n'
                '    if (p === "/free/walk" || p === "/free/walk/") {\n'
                '      return new Response(WALK_FREE, '
                '{ headers: { "content-type": "text/html;charset=utf-8", '
                '"cache-control": "no-store" } });\n    }\n'
                '    if (p === "/free/hub") {\n'
                '      return Response.redirect("https://nayanet.app/", 302);\n    }')
    handler = replace_once(handler, old_walk, new_walk, "worker /free")
    # Welcome-page assets are not used by the free pages (no external refs).
    a_start = handler.find('// ---- welcome-page assets')
    a_end = handler.find('if (p.startsWith("/api/"))')
    assert a_start > 0 and a_end > a_start
    handler = handler[:a_start] + handler[a_end:]
    # Reserved aliases: /free must not be treated as a citizen alias.
    handler = replace_once(
        handler, 'const reserved = ["welcome", "dashboard", "identity.html", "hub", "enter",',
        'const reserved = ["welcome", "dashboard", "identity.html", "hub", "enter", "free",',
        "worker reserved")
    # Unknown paths: a plain 404 naming the route (the walk worker falls
    # back to the walk; the free worker's front door is /free).
    old_fb = ('    return new Response(WALK, { headers: { "content-type": '
              '"text/html;charset=utf-8", "cache-control": "no-store" } });')
    assert handler.count(old_fb) == 1
    handler = handler.replace(
        old_fb,
        'return new Response("Not found — start free at /free", { status: 404, '
        'headers: { "content-type": "text/plain;charset=utf-8" } });')
    assert "Response(IDENTITY" not in handler and "const IDENTITY" not in handler \
        and "WELCOME," not in handler and '"/welcome"' not in handler, \
        "harvested handler still references the old pages — STOP"
    assert "/free/walk" in handler and "/free/hub" in handler
    assert "/api/welcome/complete" in handler and "/api/claim" in handler

    live = open(LIVE_IDENT, encoding="utf-8").read()
    m = re.search(r"var SB_ANON_KEY = '([^']+)';", live)
    assert m, "registry key not found in live-extracted identity"
    sb_key = m.group(1)
    assert sb_key.startswith("eyJ"), "key shape unexpected"
    print("registry key read programmatically (value not printed)")

    head = ('const FREE_ENTRY = "' + js_encode(free_entry) + '";\n'
            'const WALK_FREE = "' + js_encode(walk_free) + '";\n'
            'const FREE_INDEX = "' + js_encode(
                FREE_INDEX.replace("__PRICING_STAGED__",
                                   "https://naya-pricing-f4-staging.nayapower.workers.dev/")) + '";\n'
            'const SB_URL = "https://dahisasgpfvziswqvmvm.supabase.co/rest/v1/nayanet_identities";\n'
            'const SB_KEY = ' + json.dumps(sb_key) + ';\n\n'
            'const JSONH = { "content-type": "application/json" };\n'
            'function j(obj, status) {\n'
            '  return new Response(JSON.stringify(obj), { status: status || 200, headers: JSONH });\n}\n'
            'function sbHeaders() {\n'
            '  return { "apikey": SB_KEY, "Authorization": "Bearer " + SB_KEY, "Content-Type": "application/json" };\n}\n'
            'async function sbGetRow(alias) {\n'
            '  const r = await fetch(SB_URL + "?alias=eq." + encodeURIComponent(alias)\n'
            '    + "&select=alias,name,device_key,cert_no,created_at", { headers: sbHeaders() });\n'
            '  if (!r.ok) return null;\n'
            '  const rows = await r.json().catch(() => null);\n'
            '  return (rows && rows.length) ? rows[0] : null;\n}\n'
            'function cleanAlias(a) {\n'
            '  return String(a || "").trim().toLowerCase().replace(/[^a-z0-9]/g, "").slice(0, 32);\n}\n'
            'function slug(s, fb) {\n'
            '  return String(s || "").trim().toLowerCase().replace(/[^a-z0-9\\s-]/g, "")\n'
            '    .replace(/[\\s_]+/g, "-").replace(/-+/g, "-").replace(/^-|-$/g, "") || fb;\n}\n\n')
    return head + handler


def main():
    walk_free = build_walk_free()
    free_entry = build_free_entry()
    worker = build_worker(walk_free, free_entry)
    shell_write(os.path.join(HERE, "walk-free.html"), walk_free)
    shell_write(os.path.join(HERE, "free-entry.html"), free_entry)
    shell_write(os.path.join(HERE, "free-index.html"),
                FREE_INDEX.replace("__PRICING_STAGED__",
                                   "https://naya-pricing-f4-staging.nayapower.workers.dev/"))
    shell_write(os.path.join(HERE, "free-staging-worker.js"), worker)
    meta = {"main_module": "worker.js",
            "bindings": [{"type": "kv_namespace", "name": "WELCOME_ASSETS",
                          "namespace_id": "1cf80db6183245d19dd5296645a12bd0"}]}
    shell_write(os.path.join(HERE, "worker-meta.json"),
                json.dumps(meta, indent=2) + "\n")
    for name, data in [("walk-free.html", walk_free),
                       ("free-entry.html", free_entry),
                       ("free-staging-worker.js", worker)]:
        p = os.path.join(HERE, name)
        got = open(p, "rb").read()
        print(f"{name}: {len(got)} B sha256={hashlib.sha256(got).hexdigest()}")
    import gzip
    gz = gzip.compress(worker.encode("utf-8"))
    print(f"worker gzip: {len(gz)} B (limit 10,485,760)")
    assert len(gz) < 10485760, "worker gzip over the 10 MB limit — STOP"
    print("FREE WORKER BUILD OK")


if __name__ == "__main__":
    main()
