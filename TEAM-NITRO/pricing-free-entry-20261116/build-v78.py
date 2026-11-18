#!/usr/bin/env python3
"""Build pricing v78 (F4 free-entry route) from the v77 live source.
v78 = v77 + exactly 3 change groups, nothing else:
  G1 CSS: .free-entry rules (button, star, copy, orbit) appended after the
     v77 .plan-free rule (same place v77 appended its CSS).
  G2 HTML: the free-entry section (link pill + orbit) directly under the
     trial banner, in the visible hero, above the chart.
  G3 JS: FREE_ENTRY_URL const + orbit-path IIFE; #finaleFree and
     #chooserFree now open the route (they only wrote a note before).
The live source file is NEVER edited in place: v77 is read, v78 is written
to ~/workspace/team-nitro/pricing/v78/pricing-v78.html. A diff vs v77 is
written to v78/diff-v78.txt. All anchors asserted unique before editing.
"""
import hashlib
import os
import shlex
import subprocess


def shell_write(path, data):
    """Write with retries across the EPERM flake (TOOLS.md: the flake is
    time-varying and per-path; small writes land between windows, large
    writes fail inside them). Proven 2026-11-17 00:17Z: Node's
    fs.writeFileSync lands while python open()/shell `cat`/cp all EPERM —
    so Node is tried FIRST, then python, then shell `cat >`, then a
    scratch path + `mv` (rename writes no content). Retries up to ~10 min.
    Verifies the byte count after every attempt — a 0-byte file is flake
    damage, never a success."""
    import time
    raw = data.encode("utf-8")
    scratch = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           ".tmp-" + os.path.basename(path))
    node_js = ("require('fs').writeFileSync(process.argv[1], "
               "require('fs').readFileSync(0));")
    deadline = time.time() + 600
    attempt = 0
    while True:
        attempt += 1
        for mode in ("node", "py", "sh", "mv"):
            try:
                if mode == "node":
                    r = subprocess.run(
                        ["node", "-e", node_js, path], input=raw)
                    if r.returncode != 0:
                        continue
                elif mode == "py":
                    with open(path, "wb") as f:
                        f.write(raw)
                elif mode == "sh":
                    r = subprocess.run("cat > " + shlex.quote(path), shell=True,
                                       input=raw)
                    if r.returncode != 0:
                        continue
                else:
                    r = subprocess.run(
                        ["node", "-e", node_js, scratch], input=raw)
                    if r.returncode != 0:
                        continue
                    subprocess.run(["mv", scratch, path], check=True)
                if os.path.getsize(path) == len(raw):
                    print(f"write {path}: {len(raw)} B via {mode} (attempt {attempt})")
                    return
            except Exception as e:
                print(f"write {path} via {mode} failed (attempt {attempt}): {e}")
        if time.time() > deadline:
            raise SystemExit(f"write failed for {path} after {attempt} attempts — STOP")
        time.sleep(15)

V77 = os.path.expanduser("~/workspace/team-nitro/pricing/v77/pricing-v77.html")
V77_SHA = "b043167b2fa9a863a18216cdd2d282a20dcf5ff4159ac93e0da28ddea1635577"
V78 = os.path.expanduser("~/workspace/team-nitro/pricing/v78/pricing-v78.html")
DIFF = os.path.expanduser("~/workspace/team-nitro/pricing/v78/diff-v78.txt")

FREE_URL = "https://naya-pricing-free-staging.nayapower.workers.dev/free"

CSS_ANCHOR = ".plan-free{font-size:13px;font-weight:800;color:#fff;letter-spacing:.02em}"
CSS_ADD = """ /* FREE ENTRY (v78, F4 2026-11-17) — the free button on top, in the language. Harvested from .primo (Hub lines 689-698, NAYA-BTN-005) + .finale-btn/.finale-star/.finale-copy (the page's own big free pill) + the orbit (THE-NAYA-CODE.md §8: circles have flow — two glint orbs circle the button's outline opposite ways, the vortex: CW 60s, CCW 90s, slow per the Playbook). Obsidian pill, white word, green rim (#2fe89e, free/positive), alive on hover (lifts, rim + halo ignite green — .primo:hover). The button is a plain link, so it works with JS off; no dead button. It sits directly under the trial banner, in the visible hero, above the chart: the banner keeps its proven place (fully in viewport at scroll 0, 1440 and 390), and the button is the first action under the trial promise. */
 .free-entry{display:table;margin:16px auto 0;position:relative}
 .free-entry-btn{--glow:#2fe89e;position:relative;z-index:1;display:inline-flex;align-items:center;justify-content:center;gap:18px;text-align:left;width:min(680px,100%);padding:20px 30px;border-radius:999px;border:1.5px solid rgba(47,232,158,.85);text-decoration:none}
 .free-entry-btn:hover{border-color:#2fe89e}
 .free-entry-star{width:54px;height:54px;flex:none;border-radius:50%;display:grid;place-items:center;font-size:26px;line-height:1;color:#fff;text-shadow:0 0 10px rgba(255,255,255,.9),0 1px 3px rgba(30,5,80,.6);background:radial-gradient(circle at 34% 26%,#ffffff 0%,rgba(255,255,255,.85) 9%,rgba(255,255,255,.25) 24%,transparent 40%),radial-gradient(circle at 50% 58%,rgba(47,232,158,.55) 0%,transparent 55%),radial-gradient(circle at 50% 50%,#7dffc4 0%,#2fe89e 34%,#0d7a4d 72%,#063d27 100%);border:1.5px solid rgba(237,255,247,.8);box-shadow:inset 0 0 0 2px rgba(255,255,255,.35),inset 0 6px 12px rgba(255,255,255,.30),inset 0 -8px 14px rgba(0,0,0,.5),0 0 26px rgba(47,232,158,.95),0 0 54px -6px rgba(47,232,158,.8),0 10px 22px rgba(0,0,0,.6)}
 .free-entry-copy{display:flex;flex-direction:column;align-items:flex-start;gap:3px;min-width:0}
 .free-entry-title{font-size:clamp(24px,3.2vw,34px);font-weight:900;letter-spacing:.02em;line-height:1.12;color:#fff;white-space:nowrap}
 .free-entry-sub{font-size:clamp(14px,1.7vw,17px);font-weight:600;color:#d5f5e6;line-height:1.3}
 .free-orbit{position:absolute;inset:-12px;border-radius:999px;border:1px solid rgba(47,232,158,.35);pointer-events:none}
 .free-orbit::after{content:"";position:absolute;inset:-10px;border-radius:999px;border:1px solid rgba(47,232,158,.18);pointer-events:none}
 .free-orbit-dot{position:absolute;top:0;left:0;width:9px;height:9px;margin:-4px 0 0 -4px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#fff 0%,#c8ffe6 35%,#2fe89e 70%,#0d7a4d 100%);box-shadow:0 0 10px rgba(47,232,158,.95),0 0 22px rgba(47,232,158,.6);pointer-events:none;animation:free-orbit-a 60s linear infinite}
 .free-orbit-dot--b{animation:free-orbit-b 90s linear infinite reverse}
 @keyframes free-orbit-a{from{offset-distance:0%}to{offset-distance:100%}}
 @keyframes free-orbit-b{from{offset-distance:0%}to{offset-distance:100%}}
 @media(max-width:640px){.free-entry{margin-top:12px}.free-entry-btn{padding:16px 20px;gap:14px}.free-entry-star{width:44px;height:44px;font-size:21px}.free-entry-title{white-space:normal}}
 @media(prefers-reduced-motion:reduce){.free-orbit-dot{animation:none}}"""

HTML_ANCHOR = '<div class="letter-sign" id="letterSign" hidden>'
HTML_ADD = """    <!-- FREE ENTRY (v78, F4 2026-11-17) — the free button, on top: the first action under the trial promise, in the visible hero, above the chart. It opens the real free-entry route (enter free, no payment, no card → the walk → the Hub). STAGED URL in the href: the live deploy swaps this one href for the live walk entry. The two older free controls (#finaleFree, #chooserFree) open the same route now — they only wrote a note before, a dead end. -->
    <div class="free-entry">
      <span class="free-orbit" aria-hidden="true"><span class="free-orbit-dot"></span><span class="free-orbit-dot free-orbit-dot--b"></span></span>
      <a class="primo free-entry-btn" id="freeEntry" href="__FREE_URL__" style="--glow:#2fe89e" aria-label="Enter free — no card, no payment. Start the walk free and end in your Hub."><span class="free-entry-star" aria-hidden="true">★</span><span class="free-entry-copy"><span class="free-entry-title">Enter free</span><span class="free-entry-sub">Zero cost, zero risk</span></span></a>
    </div>
""".replace("__FREE_URL__", FREE_URL)

JS_ANCHOR = "var massiveNote=document.getElementById('massiveNote');"
JS_ADD = """
   var FREE_ENTRY_URL='__FREE_URL__'; /* F4 STAGED free-entry route (enter free → walk → Hub). The live deploy swaps this one string for the live walk entry. */
   /* FREE ENTRY orbit (F4): two glint orbs circle the button's outline — a measured rounded-rect path, CW 60s + CCW 90s (the vortex, THE-NAYA-CODE.md §8). If JS is off the orbs sit still at the ring's corner and the button still works — it is a plain link. */
   (function(){var o=document.querySelector('.free-orbit');if(!o)return;var dots=o.querySelectorAll('.free-orbit-dot');function path(){var r=o.getBoundingClientRect();var w=r.width,h=r.height,rad=h/2;return 'M '+rad+',0 H '+(w-rad)+' A '+rad+','+rad+' 0 0 1 '+w+','+rad+' V '+(h-rad)+' A '+rad+','+rad+' 0 0 1 '+(w-rad)+','+h+' H '+rad+' A '+rad+','+rad+' 0 0 1 0,'+(h-rad)+' V '+rad+' A '+rad+','+rad+' 0 0 1 '+rad+',0 Z';}function set(){var p='path("'+path()+'")';for(var i=0;i<dots.length;i++)dots[i].style.offsetPath=p;}set();window.addEventListener('resize',set);})();""".replace("__FREE_URL__", FREE_URL)

NOTE = r"Welcome in — you\u2019re starting on Naya Free. Zero cost, zero risk — and you can step up any time in Settings."
FINALE_OLD = (
    "document.getElementById('finaleFree').addEventListener('click',function(){\n"
    "    /* The Free note lives at the foot of the start section (massiveNote, under the\n"
    "       five-jewel Start door). Write it there and bring the note itself fully into\n"
    "       view once it has rendered. */\n"
    "    massiveNote.textContent='" + NOTE + "';\n"
    "    massiveNote.classList.add('show');\n"
    "    var bringNote=function(){massiveNote.scrollIntoView({behavior:window.matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth',block:'end',inline:'nearest'});};\n"
    "    if(window.requestAnimationFrame)window.requestAnimationFrame(bringNote);else bringNote();\n"
    "  });"
)
FINALE_NEW = (
    "document.getElementById('finaleFree').addEventListener('click',function(){\n"
    "    /* F4: the free route is real now — this door opens it (enter free, no payment, no card → the walk → the Hub). It used to only write a note; a note is a dead end. */\n"
    "    window.location.href=FREE_ENTRY_URL;\n"
    "  });"
)
CHOOSER_OLD = (
    "document.getElementById('chooserFree').addEventListener('click',function(){\n"
    "    closeChooser();\n"
    "    massiveNote.textContent='" + NOTE + "';\n"
    "    massiveNote.classList.add('show');\n"
    "    massiveNote.scrollIntoView({behavior:'smooth',block:'center'});\n"
    "  });"
)
CHOOSER_NEW = (
    "document.getElementById('chooserFree').addEventListener('click',function(){\n"
    "    /* F4: the same route as the free button on top — close the chooser, then enter free. */\n"
    "    closeChooser();\n"
    "    window.location.href=FREE_ENTRY_URL;\n"
    "  });"
)


def replace_once(page, old, new, name):
    n = page.count(old)
    assert n == 1, f"{name}: anchor count {n}, expected 1 — STOP"
    return page.replace(old, new)


def main():
    src = open(V77, encoding="utf-8").read()
    assert hashlib.sha256(src.encode()).hexdigest() == V77_SHA, "v77 sha mismatch — STOP"
    page = src
    page = replace_once(page, CSS_ANCHOR, CSS_ANCHOR + CSS_ADD, "G1 css")
    page = replace_once(page, HTML_ANCHOR, HTML_ADD + "      " + HTML_ANCHOR, "G2 html")
    page = replace_once(page, JS_ANCHOR, JS_ANCHOR + JS_ADD, "G3 const+orbit")
    page = replace_once(page, FINALE_OLD, FINALE_NEW, "G3 finaleFree")
    page = replace_once(page, CHOOSER_OLD, CHOOSER_NEW, "G3 chooserFree")
    # v77 carried markers must survive untouched
    for m in ["Nine days free on every plan — nothing is charged for 9 days. Day 10, you&rsquo;re charged for the level you&rsquo;re on.",
              '<span class="plan-free">Nine days free</span>',
              "The first thousand founders get half price", "Plug in your AI",
              "WANT THE FULL PICTURE", "If PayPal holds a payment",
              "or continue with Naya Free"]:
        assert m in page, f"carried marker missing: {m[:40]}"
    for m in ["bonus", "bottomStart", "blockchain"]:
        assert m not in page, f"forbidden marker present: {m}"
    # v78 new markers
    assert page.count('id="freeEntry"') == 1
    assert page.count(FREE_URL) == 2, f"FREE_URL count {page.count(FREE_URL)} (expect 2: href + const)"
    assert page.count('<span class="plan-free">Nine days free</span>') == 9
    assert page.count("nayanet.app/power-monthly") == 1
    assert page.count("nayanet.app/max-yearly") == 1
    assert "openChooser" in page
    assert page.count("free-entry") >= 10
    shell_write(V78, page)
    sha = hashlib.sha256(page.encode()).hexdigest()
    print(f"v78 written: {V78}")
    print(f"v78 bytes: {len(page.encode())} sha256={sha}")
    r = subprocess.run(["diff", V77, V78], capture_output=True, text=True)
    shell_write(DIFF, r.stdout)
    print(f"diff lines: {len(r.stdout.splitlines())} -> {DIFF}")
    print("BUILD OK")


if __name__ == "__main__":
    main()
