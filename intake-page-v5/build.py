#!/usr/bin/env python3
"""Smart Factory intake v5 — the elevated library catalog.
Every piece: model number, 5 sizes + auto, Select -> cart, vision type/paste/dictate, Build app -> design contract.
Source pieces: the 15-set Naya Library (only what Shawn praised)."""
import os
SETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'vendor-css')
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'w453-zeta-copytext-regen.html')

def css(name):
    p = os.path.join(SETS, name)
    if not os.path.exists(p):
        raise FileNotFoundError("intake-page-v5 vendor-css missing: " + p)
    return open(p).read()

LIB_CSS = "\n".join(css(n) for n in [
    'primo.css','living-btn.css','cx-btn.css','naya-btn.css','minigem.css',
    'orb.css','jewel.css','truth.css','ecobar.css','hubboard.css','tog-chip.css','seg-tab.css'])

ELEV_CSS = '''
/* ============ ELEVATION LAW — nothing is flat ============ */
:root{
  --ease:cubic-bezier(.16,.84,.22,1);
}
/* OUTER: raised toward the user */
.elev-1{box-shadow:0 2px 8px rgba(0,0,0,.55),0 0 0 1px rgba(255,255,255,.07),inset 0 1px 0 rgba(255,255,255,.14) !important}
.elev-2{box-shadow:0 8px 22px rgba(0,0,0,.6),0 0 0 1px rgba(255,255,255,.09),inset 0 1px 0 rgba(255,255,255,.18) !important}
.elev-3{box-shadow:0 16px 40px rgba(0,0,0,.65),0 0 0 1px rgba(255,255,255,.11),inset 0 1px 0 rgba(255,255,255,.22) !important}
.elev-glow{box-shadow:0 10px 30px rgba(0,0,0,.6),0 0 26px -6px var(--ec,#a06bff),0 0 0 1px rgba(255,255,255,.1),inset 0 1px 0 rgba(255,255,255,.2) !important}
/* INNER: carved into the screen */
.carve-1{box-shadow:inset 0 3px 8px rgba(0,0,0,.65),inset 0 -1px 0 rgba(255,255,255,.07) !important}
.carve-2{box-shadow:inset 0 6px 16px rgba(0,0,0,.75),inset 0 -1px 0 rgba(255,255,255,.09) !important}
/* ============ JEWELS — verbatim N5 jewel library ============ */
.gem-bullet{--tone:#a06bff;width:14px;height:14px;flex:none;display:inline-block;transform:rotate(45deg);background:linear-gradient(140deg,#fff,var(--tone) 50%,#18101a);box-shadow:0 0 14px var(--tone)}
.mini-orb{--c:#3fb8ff;width:34px;height:34px;border-radius:50%;flex:none;background:radial-gradient(circle at 35% 27%,rgba(255,255,255,.6),var(--c) 37%,#08040c 78%);box-shadow:0 0 14px var(--c);border:1px solid rgba(255,255,255,.6)}
.orb--xs{width:30px;height:30px;animation:none}
.orb--xs::before{inset:-7px;padding:2px;animation-duration:8s}
.orb--xs::after{display:none}
.orb--black{background:radial-gradient(circle at 34% 26%,rgba(255,255,255,.55) 0%,transparent 26%),radial-gradient(circle at 50% 55%,#1b1b22 0%,#050507 72%);box-shadow:inset 0 0 0 2px rgba(var(--oc-rgb),.9),inset 0 -12px 24px rgba(0,0,0,.7),0 0 30px rgba(var(--oc-rgb),.5),0 0 70px -12px rgba(var(--oc-rgb),.4),0 24px 48px rgba(0,0,0,.65)}
.orb--hero{width:200px;height:200px}
.orb--hero::before{inset:-26px;padding:4px;animation-duration:9s}
.orb--hero::after{bottom:-46px;height:36px}
.orb--glyph{display:inline-grid;place-items:center;font-size:46px;color:#fff;text-shadow:0 2px 10px rgba(0,0,0,.75),0 0 22px rgba(var(--oc-rgb),.95)}
.orb--icon{width:64px;height:64px;font-size:26px}
.orb--icon::before{inset:-11px;padding:2px}
.orb--icon::after{bottom:-18px;height:14px}
.orb--twin::after{inset:-30px;left:auto;right:auto;top:auto;bottom:auto;height:auto;border-radius:50%;filter:none;z-index:auto;background:conic-gradient(from 90deg,transparent 0deg,transparent 310deg,rgba(var(--oc-rgb),.6) 345deg,transparent 360deg);-webkit-mask:linear-gradient(#fff 0 0) content-box,linear-gradient(#fff 0 0);-webkit-mask-composite:xor;mask-composite:exclude;padding:2px;animation:orb-spin-rev 11s linear infinite;opacity:.7}
button.orb--btn{cursor:pointer;font-family:inherit;border:none}
.orb--btn:active{transform:scale(.9);transition:transform .1s ease}
@keyframes orb-spin-rev{to{transform:rotate(-360deg)}}
/* ============ HUB ELEMENTS — verbatim from Shawn's 12 hub pages ============ */
:root{--line:rgba(255,255,255,.12);--line-soft:rgba(255,255,255,.08);--ink:#F8F7FB;--ink-dim:rgba(248,247,251,.72);--muted:rgba(248,247,251,.55);--text-muted:rgba(248,247,251,.55);--green:#2fe89e;--emerald:#2fe89e;--purple:#a06bff;--magenta:#e84fff;--purple-glow:rgba(160,107,255,.5);--edge:rgba(255,255,255,.1);--radius-md:13px;--radius-pill:999px;--depth-hi:0 18px 50px rgba(0,0,0,.55);--btn-accent:#a06bff}
/* B-1 ghost button */
.btn{display:inline-flex;align-items:center;gap:8px;padding:10px 14px;border-radius:10px;border:1px solid rgba(255,255,255,.25);background:rgba(0,0,0,.55);color:#fff;cursor:pointer;font-weight:800;font-size:13px;width:100%;justify-content:center}
.btn-ghost{background:transparent;border:1px solid var(--line);box-shadow:var(--depth-hi);color:var(--ink-dim)}
.btn-ghost:hover{border-color:rgba(160,107,255,.4);color:#fff}
/* B-2 toggle chip */
.tgl{display:inline-flex;align-items:center;gap:8px;padding:8px 12px;border-radius:10px;border:1px solid rgba(255,255,255,.22);background:rgba(0,0,0,.45);cursor:pointer;color:#fff;font-weight:800;font-size:13px}
.tgl.on{box-shadow:0 0 0 2px rgba(255,255,255,.3) inset,0 0 18px rgba(124,77,255,.25)}
/* B-3 smart-note buttons */
.sn-btn{padding:10px 20px;border-radius:10px;font-size:12px;font-weight:800;cursor:pointer;font-family:inherit;color:#fff;background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.25)}
.sn-btn.primary{background:linear-gradient(135deg,#6F3DFF,#9D7BFF);border-color:transparent}
/* B-4 nav buttons */
.nav-button{width:100%;min-height:42px;display:flex;align-items:center;justify-content:center;gap:9px;padding:10px 18px;border-radius:28px;text-decoration:none;color:#fff;font-size:.68rem;font-weight:950;letter-spacing:.13em;text-transform:uppercase;transition:transform .25s ease,box-shadow .3s ease}
.nav-button:hover{transform:translateY(-2px)}
.nav-button:active{transform:scale(.98)}
.nav-icon{font-size:.9rem;line-height:1}
.about-button{border:1px solid rgba(168,85,247,.9);background:linear-gradient(180deg,rgba(168,85,247,.25),rgba(50,20,75,.35));box-shadow:0 0 22px rgba(168,85,247,.24),inset 0 1px 0 rgba(255,255,255,.1)}
.whitepaper-button{border:1px solid rgba(255,255,255,.72);background:linear-gradient(180deg,rgba(255,255,255,.13),rgba(80,80,95,.14));box-shadow:0 0 18px rgba(255,255,255,.1),inset 0 1px 0 rgba(255,255,255,.1)}
.player{border:1px solid var(--green);background:linear-gradient(180deg,rgba(16,185,129,.22),rgba(6,78,59,.32));box-shadow:0 0 22px rgba(16,185,129,.28),inset 0 1px 0 rgba(255,255,255,.08)}
/* I-1 icon socket */
.ico{width:40px;height:40px;flex:0 0 40px;display:grid;place-items:center;border-radius:12px;color:var(--nav,var(--purple));background:rgba(160,107,255,.1);border:1px solid rgba(160,107,255,.25)}
.ico svg{width:24px;height:24px;stroke-width:1.8}
/* I-2 facet support */
.facet{fill:#fff;stroke:none;opacity:.48}.edge{fill:none;stroke:#fff;stroke-width:1.1;stroke-linecap:round;stroke-linejoin:round;opacity:.92}.shade{fill:#000;stroke:none;opacity:.28}.core{fill:currentColor;stroke:none;opacity:.98}
/* J-1 LED */
.led{width:8px;height:8px;border-radius:50%;background:var(--green);box-shadow:0 0 10px rgba(47,232,158,.8);display:inline-block}
/* J-2 corner jewel */
.corner-jewel{position:absolute;width:14px;height:14px;transform:rotate(45deg);background:linear-gradient(135deg,#fff 0%,var(--tone,var(--purple)) 45%,#000 100%);box-shadow:0 0 14px var(--tone-glow,var(--purple-glow));z-index:2}
/* D-1 metric stat */
.metric{background:linear-gradient(155deg,#121019,#09080d);padding:18px 16px;min-height:94px;border-radius:14px;border:1px solid var(--line)}
.metric b{display:block;font-size:28px;line-height:1;margin-bottom:8px;color:var(--ink)}
.metric span{font-size:13px;color:var(--muted)}
/* D-2 empty state */
.empty-instrument{padding:18px;border:1px dashed var(--line);border-radius:var(--radius-md)}
.empty-instrument strong{display:block;font-size:15px;margin-bottom:6px}
.empty-instrument p{font-size:14px;color:var(--muted);margin:0}
/* D-3 identity box */
.id-box{position:relative;overflow:hidden;border-radius:20px;padding:20px 22px;display:flex;align-items:center;gap:18px;background:linear-gradient(165deg,#0b0d13 0%,#040507 55%,#010203 100%);border:1px solid rgba(255,255,255,.07);border-top:2px solid var(--tone,var(--purple));box-shadow:inset 0 1px 0 rgba(255,255,255,.08),inset 0 -14px 26px rgba(0,0,0,.6),0 22px 44px rgba(0,0,0,.55)}
.id-box-label{font-size:.72rem;font-weight:900;letter-spacing:.28em;color:var(--text-muted);text-transform:uppercase;margin-bottom:8px}
.id-box-value{font-size:1.32rem;font-weight:800;color:#fff;text-shadow:0 0 24px var(--tone-glow,var(--purple-glow))}
/* R-1 meta row */
.meta-row{display:flex;gap:10px;flex-wrap:wrap;margin-top:11px;color:var(--muted);font-size:10.5px}
.meta-row span{padding:4px 8px;border:1px solid var(--line-soft);border-radius:var(--radius-pill)}
/* R-2 action row */
.action-row{display:flex;gap:8px;flex-wrap:wrap;margin-top:13px}
/* R-3 menu item */
.mi{padding:10px 12px;border-bottom:1px solid rgba(255,255,255,.08);cursor:pointer;color:#fff;font-weight:800;font-size:13px}
.mi:last-child{border-bottom:none}
/* R-4 import-method row */
.im-row{position:relative;display:flex;gap:12px;align-items:flex-start;background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.1);border-radius:14px;padding:10px 12px}
.im-jewel{flex:0 0 40px;width:40px;height:40px;border-radius:50%;display:flex;align-items:center;justify-content:center;background:rgba(160,107,255,.14);border:1px solid rgba(160,107,255,.35);color:var(--purple)}
.im-steps{margin:6px 0 0;padding-left:22px}
.im-steps li{margin:3px 0;color:rgba(255,255,255,.84);font-size:.84rem;line-height:1.5}
/* N-1 search bar */
.search-wrap{margin:0 auto;max-width:640px;width:100%}
.search-input{width:100%;min-height:48px;font-size:16px;color:var(--ink);background:rgba(255,255,255,.03);border:1px solid var(--line);border-radius:12px;padding:0 18px;font-family:inherit}
.search-input::placeholder{color:var(--muted)}
.search-input:focus{outline:none;border-color:#d86cff;box-shadow:0 0 0 3px rgba(216,108,255,.18)}
/* N-2 alias field */
.alias-input-box{width:100%;max-width:520px;margin:0 auto;text-align:left}
.alias-label{display:block;font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);margin-bottom:10px;font-weight:700}
.alias-field-wrapper{display:flex;align-items:center;background:#06070a;border:2px solid rgba(255,255,255,.85);border-radius:20px;padding:10px 18px;box-shadow:0 8px 22px rgba(0,0,0,.55),inset 0 1px 2px rgba(255,255,255,.15)}
.alias-field-wrapper:focus-within{border-color:var(--purple);box-shadow:0 0 32px var(--purple-glow),inset 0 1px 2px rgba(255,255,255,.25)}
.alias-field-input{flex:1;background:transparent;border:none;outline:none;color:#fff;font-size:1.25rem;font-weight:800;font-family:inherit}
/* H-1 eyebrow */
.eyebrow{font-size:11px;letter-spacing:.24em;font-weight:700;color:var(--room-accent,var(--green));margin-bottom:12px}
/* H-2 intelligence trio */
.intel-type{font-size:10px;font-weight:900;letter-spacing:.16em;color:var(--room-accent,var(--magenta));text-transform:uppercase;margin-bottom:7px}
.intel-title{font-size:16px;font-weight:850;line-height:1.25}
.intel-summary{color:var(--ink-dim);font-size:13px;line-height:1.55;margin-top:7px}
/* H-3 step number */
.num{display:inline-flex;align-items:center;gap:10px;margin-bottom:14px;font-size:12px;font-weight:700;letter-spacing:.2em;text-transform:uppercase;color:var(--c,var(--purple))}
.num .jewel{width:11px;height:11px;transform:rotate(45deg);flex-shrink:0;background:linear-gradient(135deg,#fff,var(--c,var(--purple)) 60%,#3a2a55);box-shadow:0 0 12px var(--c,var(--purple))}
/* K-1 status pill */
.pill{display:inline-flex;align-items:center;gap:7px;padding:5px 12px;border-radius:var(--radius-pill);font-size:11px;font-weight:800;letter-spacing:.14em;border:1px solid var(--line);background:rgba(255,255,255,.03);color:var(--muted);white-space:nowrap}
.pill .dot{width:7px;height:7px;border-radius:50%;background:currentColor}
.pill.live{color:var(--green);border-color:rgba(47,232,158,.4)}
/* K-2 done mark */
.done-mark{display:flex;margin-top:20px;align-items:center;gap:10px;font-size:14px;font-weight:600;color:var(--emerald)}
.done-mark .tick{width:22px;height:22px;border-radius:50%;background:var(--emerald);color:#04240f;display:flex;align-items:center;justify-content:center;font-size:14px;font-weight:800;box-shadow:0 0 14px rgba(85,227,154,.53)}
/* K-3 search highlight */
.hl{background:rgba(138,92,255,.5);color:#fff;border-radius:3px;padding:0 2px}
/* K-4 divider bar */
.bar{flex:1;height:2px;background:var(--edge);margin:0 6px;border-radius:2px;min-width:40px}
/* piece cards */
.pcard{background:linear-gradient(180deg,#101016,#0a0a0f);border:1px solid rgba(255,255,255,.1);border-radius:20px;padding:22px;display:flex;flex-direction:column;gap:14px;transition:transform .25s var(--ease),box-shadow .25s var(--ease),border-color .25s}
.pcard:hover{transform:translateY(-4px);border-color:rgba(255,255,255,.22)}
.pstage{min-height:120px;display:flex;align-items:center;justify-content:center;background:radial-gradient(circle at 50% 40%,#15151d,#08080c);border-radius:14px;padding:26px;overflow:hidden}
.pstage .zoom{transition:transform .25s var(--ease);display:flex;align-items:center;justify-content:center}
.pmodel{font-size:11px;letter-spacing:.18em;color:#a06bff;font-weight:700}
.pname{font-size:17px;font-weight:600}
.psizes{display:flex;gap:6px;flex-wrap:wrap}
.szpill{font-size:13px;padding:12px 18px;min-height:44px;display:inline-flex;align-items:center;border-radius:22px;border:1px solid rgba(255,255,255,.18);background:#0c0c12;color:#fff;cursor:pointer;letter-spacing:.06em}
.szpill.on{border-color:#a06bff;background:rgba(160,107,255,.16);box-shadow:0 0 12px -2px #a06bff}
.prow{display:flex;gap:10px}
.btn-select,.btn-notes{flex:1;padding:13px;border-radius:14px;font-size:13px;font-weight:700;letter-spacing:.08em;cursor:pointer;border:1.5px solid rgba(255,255,255,.6);background:linear-gradient(180deg,#1c1c26,#101015);color:#fff;box-shadow:inset 0 2px 2px rgba(255,255,255,.16),inset 0 -3px 6px rgba(0,0,0,.6),0 0 16px -4px rgba(255,255,255,.35),0 8px 20px rgba(0,0,0,.6);transition:all .25s var(--ease)}
.btn-select.picked{border-color:#2fe89e;background:rgba(47,232,158,.14);box-shadow:0 0 16px -4px #2fe89e}
/* toggle switch — elevated */
.tog{position:relative;width:60px;height:34px;border-radius:20px;background:#050507;cursor:pointer;flex:none;border:1.5px solid rgba(255,255,255,.35);box-shadow:inset 0 3px 8px rgba(0,0,0,.75),inset 0 1px 0 rgba(0,0,0,.6);transition:all .25s var(--ease)}
.tog .knob{position:absolute;top:2px;left:2px;width:26px;height:26px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#2e2e3a,#0e0e12);box-shadow:0 3px 8px rgba(0,0,0,.65);transition:all .25s var(--ease)}
.tog.on{border-color:#2fe89e;box-shadow:inset 0 3px 8px rgba(0,0,0,.75),0 0 18px -2px #2fe89e}
.tog.on .knob{left:28px;background:radial-gradient(circle at 35% 30%,#6ff2ab,#0d5a37);box-shadow:0 3px 8px rgba(0,0,0,.6),0 0 14px -2px #2fe89e}
/* cart */
#cartFab{position:fixed;bottom:24px;right:24px;z-index:90;width:68px;height:68px;border-radius:50%;background:linear-gradient(180deg,#2a2140,#14101f);border:1.5px solid #a06bff;color:#fff;font-size:24px;cursor:pointer;display:flex;align-items:center;justify-content:center;box-shadow:0 12px 32px rgba(0,0,0,.6),0 0 24px -6px #a06bff}
#cartCount{position:absolute;top:-4px;right:-4px;min-width:26px;height:26px;border-radius:14px;background:#e84fff;color:#000;font-size:13px;font-weight:800;display:flex;align-items:center;justify-content:center;padding:0 7px}
#cartDrawer{position:fixed;top:0;right:-420px;width:400px;max-width:92vw;height:100vh;z-index:95;background:#0b0b10;border-left:1px solid rgba(255,255,255,.12);transition:right .35s var(--ease);display:flex;flex-direction:column;box-shadow:-20px 0 60px rgba(0,0,0,.6)}
#cartDrawer.open{right:0}
.cartitem{display:flex;gap:12px;align-items:center;padding:12px;border:1px solid rgba(255,255,255,.1);border-radius:14px;margin:8px 16px;background:#101016}
.filterpill{padding:10px 18px;border-radius:24px;border:1px solid rgba(255,255,255,.16);background:#0e0e14;color:#fff;font-size:13px;cursor:pointer}
.filterpill.on{border-color:#3fb8ff;background:rgba(63,184,255,.14);box-shadow:0 0 14px -4px #3fb8ff}
.visioncard{background:linear-gradient(180deg,#14141c,#0c0c11);border:1px solid rgba(255,255,255,.1);border-radius:20px;padding:24px}
textarea.visionin{width:100%;min-height:110px;background:#060609;color:#fff;border:1px solid rgba(255,255,255,.12);border-radius:14px;padding:16px;font-size:15px;font-family:inherit;resize:vertical}
textarea.visionin:focus{outline:none;border-color:#a06bff;box-shadow:0 0 0 1px #a06bff,0 0 20px -6px #a06bff}
.contractbox{background:#060609;border:1px solid rgba(160,107,255,.35);border-radius:16px;padding:20px;font-family:ui-monospace,monospace;font-size:13px;line-height:1.7;white-space:pre-wrap;max-height:420px;overflow:auto}
.stepnum{display:inline-flex;width:34px;height:34px;border-radius:50%;align-items:center;justify-content:center;font-weight:800;font-size:15px;color:#000;margin-right:10px}
h2.stept{font-family:'Cormorant Garamond',Georgia,serif;font-size:34px;margin:6px 0 10px}
.kicker{font-size:11px;letter-spacing:.24em;opacity:.55;margin-bottom:4px}
.lede{font-size:16px;line-height:1.65;opacity:.85;max-width:640px}
.tmpl{border:1px solid rgba(255,255,255,.12);border-radius:18px;padding:20px;cursor:pointer;transition:all .25s var(--ease);background:linear-gradient(180deg,#121218,#0b0b0f)}
.tmpl.sel{border-color:var(--tc);box-shadow:0 0 24px -8px var(--tc)}
.tdot{width:14px;height:14px;border-radius:50%;background:var(--tc);box-shadow:0 0 10px var(--tc);display:inline-block;margin-right:8px}

.pcard{background:linear-gradient(180deg,#101016,#0a0a0f);border:1.5px solid rgba(255,255,255,.1);box-shadow:0 8px 22px rgba(0,0,0,.6),inset 0 1px 0 rgba(255,255,255,.14)}
.pcard:hover{transform:translateY(-4px);border-color:var(--sc);box-shadow:0 16px 40px rgba(0,0,0,.65),0 0 28px -8px var(--sc),inset 0 1px 0 rgba(255,255,255,.2)}
.pmodel{color:var(--sc)}
.btn-select:hover{border-color:#2fe89e;transform:translateY(-2px);box-shadow:inset 0 2px 2px rgba(255,255,255,.2),inset 0 -3px 6px rgba(0,0,0,.5),0 0 24px -4px #2fe89e,0 12px 26px rgba(0,0,0,.65)}.btn-notes:hover{border-color:#3fb8ff;transform:translateY(-2px);box-shadow:inset 0 2px 2px rgba(255,255,255,.2),inset 0 -3px 6px rgba(0,0,0,.5),0 0 24px -4px #3fb8ff,0 12px 26px rgba(0,0,0,.65)}.btn-select:active,.btn-notes:active{transform:translateY(1px) scale(.98)}
.btn-notes:hover{border-color:#3fb8ff;box-shadow:0 0 20px -4px #3fb8ff,inset 0 1px 0 rgba(255,255,255,.2);transform:translateY(-2px)}
.frow{display:flex;gap:14px;align-items:center;background:#0d0d13;border:1px solid rgba(255,255,255,.09);border-radius:16px;padding:14px 16px;margin:10px 0}
.frow b{display:block;font-size:15px;color:#fff}
.fsub{display:block;font-size:13px;color:#fff;opacity:.75;margin-top:2px}
.fic{width:48px;height:48px;flex:none;border-radius:14px;display:flex;align-items:center;justify-content:center;background:#0a0a0e;border:1.5px solid var(--fc);box-shadow:0 6px 16px rgba(0,0,0,.6),0 0 14px -4px var(--fc)}
.frow-head{font-size:11px;letter-spacing:.2em;color:#fff;opacity:.7;margin:14px 0 4px}
.xdrop{margin:14px 0;border:1px solid rgba(255,255,255,.12);border-radius:16px;background:#0d0d13;overflow:hidden}
.xdrop summary{padding:16px;cursor:pointer;font-size:13px;letter-spacing:.14em;color:#fff;list-style:none}
.xdrop summary::-webkit-details-marker{display:none}
.xdrop .frow{margin:10px 14px}
.tcard{border:1.5px solid var(--tc);border-radius:20px;padding:24px;background:linear-gradient(180deg,#121218,#0b0b0f);transition:all .3s var(--ease)}
.tcard:hover{box-shadow:0 16px 40px rgba(0,0,0,.6),0 0 30px -8px var(--tc);transform:translateY(-4px)}
.tcard.sel{box-shadow:0 0 0 2px var(--tc),0 0 34px -6px var(--tc)}
.tview{display:inline-block;margin-top:14px;padding:13px 34px;border-radius:30px;border:1.5px solid rgba(255,255,255,.35);background:#0a0a0e;color:#fff;font-size:13px;font-weight:800;letter-spacing:.1em;cursor:pointer;transition:all .25s var(--ease)}
.tview:hover{border-color:var(--tc);box-shadow:0 0 22px -4px var(--tc),inset 0 1px 0 rgba(255,255,255,.2);transform:translateY(-2px)}
.tdetail{display:none;margin-top:14px;font-size:14px;line-height:1.7;color:#fff}
.tcard.open .tdetail{display:block}
.lede{color:#F8F7FB;opacity:.92}

.mini-gem{--tone:#a06bff;width:60px;height:60px;flex:none;display:grid;place-items:center;border-radius:16px;background:radial-gradient(circle at 50% 30%,var(--tone),#070709 130%);border:1.5px solid var(--tone);box-shadow:0 8px 20px rgba(0,0,0,.55),0 0 18px -4px var(--tone),inset 0 -10px 16px rgba(0,0,0,.5)}
.mini-gem.circle{border-radius:50%}
.mini-gem.square{border-radius:12px}
.mini-gem.diamond{border-radius:10px;transform:rotate(45deg)}
.mini-gem.diamond svg{transform:rotate(-45deg)}
.tgrid{display:flex;flex-direction:column;gap:14px}
.tcard2{display:flex;align-items:center;gap:18px;border:1px solid rgba(255,255,255,.12);border-left:3px solid var(--tc);border-radius:18px;padding:18px 20px;background:linear-gradient(180deg,#0c0c12,#070709);box-shadow:0 10px 24px rgba(0,0,0,.5),inset 0 1px 0 rgba(255,255,255,.06);transition:all .3s var(--ease);cursor:pointer}
.tcard2:hover{transform:translateY(-2px);box-shadow:0 14px 30px rgba(0,0,0,.55),0 0 22px -6px var(--tc)}
.tcard2.sel{border:1px solid var(--tc);border-left:3px solid var(--tc);box-shadow:0 0 0 1.5px var(--tc),0 0 30px -6px var(--tc)}
.tcard2.open .tdetail{display:block}
.trow1{display:flex;gap:16px;align-items:center}
.tbrand{display:block;font-size:16px;color:#fff;line-height:1.3}
.tnut{display:block;font-size:13px;color:#fff;opacity:.7;margin-top:3px}

/* v8: template jewel layout discipline */
.trow1{align-items:flex-start}
.tcard2 .tview{margin-top:0;flex:none}
.tbrand{font-size:15px}
.tnut{font-size:12.5px}
/* v8: canonical 5-layer shadow physics on view buttons */
.tview{box-shadow:inset 0 2px 2px rgba(255,255,255,.22),inset 0 -3px 6px rgba(0,0,0,.6),0 0 22px -2px rgba(255,255,255,.18),0 12px 28px rgba(0,0,0,.65)}
.tview:hover{transform:translateY(-2px);box-shadow:inset 0 2px 2px rgba(255,255,255,.25),inset 0 -3px 6px rgba(0,0,0,.5),0 0 14px -4px var(--tc),0 16px 34px rgba(0,0,0,.68)}
.tview:active{transform:translateY(1px) scale(.98);box-shadow:inset 0 3px 8px rgba(0,0,0,.7),0 6px 13px rgba(0,0,0,.65)}
/* v8: make-it-official summary overlay */
#sumWrap{position:fixed;inset:0;z-index:60;display:none;align-items:flex-start;justify-content:center;background:rgba(2,2,4,.82);backdrop-filter:blur(8px);overflow-y:auto;padding:40px 16px}
#sumWrap.open{display:flex}
.sumpanel{width:min(760px,100%);background:linear-gradient(180deg,#121218,#0a0a0e);border:1.5px solid rgba(255,255,255,.14);border-radius:24px;padding:34px;box-shadow:0 30px 80px rgba(0,0,0,.7),inset 0 1px 0 rgba(255,255,255,.15)}
.sumpanel h2{font-family:var(--voice);font-size:30px;margin:0 0 6px;color:#fff}
.sumsec{border-top:1px solid rgba(255,255,255,.09);padding:18px 0}
.sumsec h4{font-size:11px;letter-spacing:.22em;color:#fff;opacity:.65;margin:0 0 12px}
.sumrow{display:flex;gap:12px;align-items:center;padding:10px 0;font-size:14px;color:#fff}
.sumrow .x{margin-left:auto;cursor:pointer;opacity:.6;font-size:18px}
.sumrow .x:hover{opacity:1;color:#ff5e6c}
.sumchg{font-size:12px;letter-spacing:.1em;opacity:.6;cursor:pointer}
.sumchg:hover{opacity:1;color:#fff}
.sumpiece{display:flex;gap:12px;align-items:center;background:#0d0d13;border:1px solid rgba(255,255,255,.08);border-radius:14px;padding:12px 14px;margin:8px 0;font-size:13.5px;color:#fff}
.sumpiece .pm{font-size:11px;letter-spacing:.08em;opacity:.6}
.sumbtn{display:block;width:100%;margin-top:20px;padding:18px;border-radius:999px;border:1.5px solid rgba(255,255,255,.78);background:linear-gradient(180deg,#15151a,#050506);color:#fff;font-size:15px;font-weight:800;letter-spacing:.08em;cursor:pointer;box-shadow:inset 0 2px 2px rgba(255,255,255,.22),inset 0 -3px 6px rgba(0,0,0,.6),0 12px 28px rgba(0,0,0,.65);transition:all .25s var(--ease)}
.sumbtn:hover{transform:translateY(-2px);border-color:#2fe89e;box-shadow:inset 0 2px 2px rgba(255,255,255,.25),0 0 18px -4px #2fe89e,0 16px 34px rgba(0,0,0,.68)}

#noteWrap{position:fixed;inset:0;background:rgba(0,0,0,.72);backdrop-filter:blur(6px);display:none;align-items:center;justify-content:center;z-index:300;padding:20px}
#noteWrap.open{display:flex}
.notebox{width:min(480px,100%);background:linear-gradient(180deg,#111118,#08080c);border:1px solid rgba(255,255,255,.16);border-radius:20px;padding:26px;box-shadow:0 30px 80px rgba(0,0,0,.75),0 0 30px -8px rgba(160,107,255,.35)}
.notebox h3{font-size:18px;margin-bottom:6px;color:#fff}
.notebox p{font-size:13px;opacity:.65;margin-bottom:12px}
#noteText{width:100%;min-height:110px}
.nextbox{margin-top:16px;padding:16px 18px;border-radius:14px;background:rgba(47,232,158,.06);border:1px solid rgba(47,232,158,.35);font-size:14px;line-height:1.65;color:#fff}
#draftToast{position:fixed;bottom:24px;left:50%;transform:translateX(-50%) translateY(80px);background:#0d2419;border:1px solid #2fe89e;color:#fff;padding:14px 24px;border-radius:30px;font-size:14px;z-index:400;transition:transform .4s var(--ease);box-shadow:0 10px 30px rgba(0,0,0,.6),0 0 20px -4px #2fe89e}
#draftToast.show{transform:translateX(-50%) translateY(0)}
'''
