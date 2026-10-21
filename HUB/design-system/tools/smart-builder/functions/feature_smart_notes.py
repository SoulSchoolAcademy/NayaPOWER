#!/usr/bin/env python3
"""feature.smart_notes — "Smart Notes + Smart Links" (Smart Builder feature breaker).

Capability contract (functions/registry.json):
  id: feature.smart_notes, version 1.0.0, status tracked in the registry.
  activated_by: contract.features.smart_notes — the CONTRACT flips the breaker;
  the module never hand-wires itself into a page.
  Built on PR #2747's not_wired declaration: label "Smart Notes and Smart
  Links", default_enabled true, required true.

Activation input (from the contract):
  contract.features.smart_notes = {
      "enabled": True,
      "link_base": "https://nayanet.live",          # optional, http(s) only
      "page_address": "nayanet.live/morning-crumb",  # optional, feeds note ids
      "notes": [
          {"title": "Sourdough at 6am", "body": "The crumb ...", "voice": "naya"}
      ]
  }

Behavior:
  - Not declared (or enabled falsy) -> render nothing. The page refuses
    to render notes the contract did not declare.
  - Declared + registry says built -> note cards + a "smart note this"
    capture panel, each note carrying its minted smart link.
  - Declared + registry says anything else -> SmartNotesRefusal('feature_not_built').
    The contract never advertises a capability as operational unless the
    registry says it is built.
  - READY vs CONNECTED (Naya 3's consent-line refinement, 21:41Z): composing notes
    and minting links is READY (local, no grant needed); link resolution +
    network sharing is CONNECTED and needs the recorded grant
    'bridge.smart_links.resolve'. Without it the module shows the honest
    ready-not-connected state ("not connected — connect the NayaNET bridge
    to enable link resolution") — never a fabricated answer, never silent.
  - Note ids and smart links are MINTED deterministically at build time:
    note_id = sha256(page_address | index | title | body)[:12],
    link    = link_base + "/sn/" + note_id. The link is marked
    data-link-state="minted-unresolved" — the module mints, it never claims
    the link resolves (resolution rides the NayaNET bridge once wired;
    cf. lesson L-2026-10-17-002 — no dead link is claimed live).
  - Hostile content -> structured refusals, fail closed: unknown voice,
    non-http(s) link_base, empty note body, malformed declarations.
  - Declared but no notes -> graceful fallback: the capture panel alone
    (compose a note on the page; it saves locally and mints its link —
    labeled "saved on this page only", never claimed shared).
  - Interactive elements (copy buttons, capture form) bind only to DOM that
    exists: script sits directly after the markup, runs on DOMContentLoaded,
    and no-ops when its root section is absent (L-2026-10-17-004).

Stdlib only. Pure functions — same declaration -> same bytes, always.
"""
import hashlib
import html as htmlmod
from urllib.parse import urlparse

VERSION = "1.0.0"
FEATURE_ID = "feature.smart_notes"
# aliases the assembler imports
FEATURE_SMART_NOTES_ID = FEATURE_ID
FEATURE_SMART_NOTES_VERSION = VERSION

VOICES = ("human", "child", "grandma", "naya")
DEFAULT_LINK_BASE = "https://nayanet.live"

# The named grant for the connected half of the contract (READY vs CONNECTED,
# Naya 3's consent-line refinement 21:41Z): composing + minting is ready;
# resolution needs this recorded grant.
GRANT_RESOLVE = "bridge.smart_links.resolve"
CONNECTION_NAME = "NayaNET bridge"


class SmartNotesRefusal(Exception):
    """Structured refusal: the smart_notes breaker declined to activate.

    code: machine-readable failure class (never a transport error —
    this module performs no I/O, so every refusal is a content/contract
    failure, cf. lesson L-2026-10-16-004).
    detail: human-readable explanation for the receipt.
    """
    def __init__(self, code, detail=""):
        super().__init__("%s: %s" % (code, detail))
        self.code = code
        self.detail = detail


def esc(s):
    return htmlmod.escape(str(s), quote=True)


def sanitize_link_base(base, field="link_base"):
    """Allowlist the smart-link base. Returns the cleaned base URL,
    raises SmartNotesRefusal('unsafe_link_base') for anything hostile."""
    if base is None:
        return DEFAULT_LINK_BASE
    if not isinstance(base, str):
        raise SmartNotesRefusal("unsafe_link_base",
                                "%s: not a string (%s)" % (field, type(base).__name__))
    u = base.strip().rstrip("/")
    if not u:
        return DEFAULT_LINK_BASE
    if any(ord(c) < 0x20 for c in u):
        raise SmartNotesRefusal("unsafe_link_base",
                                "%s: control characters in URL" % field)
    p = urlparse(u)
    scheme = (p.scheme or "").lower()
    if scheme not in ("http", "https") or not p.hostname:
        raise SmartNotesRefusal("unsafe_link_base",
                                "%s: must be an absolute http(s) URL with a host" % field)
    if any(c.isspace() for c in p.hostname):
        raise SmartNotesRefusal("unsafe_link_base",
                                "%s: whitespace in host" % field)
    return u


def sanitize_note(note, i):
    """Validate one declared note. Returns (title, body, voice) or raises."""
    if not isinstance(note, dict):
        raise SmartNotesRefusal("bad_note",
                                "notes[%d]: must be an object, got %s" % (i, type(note).__name__))
    title = str(note.get("title") or "").strip() or "Untitled note"
    body = note.get("body")
    if not isinstance(body, str) or not body.strip():
        raise SmartNotesRefusal("bad_note",
                                "notes[%d]: body must be a non-empty string" % i)
    voice = str(note.get("voice") or "naya").strip().lower()
    if voice not in VOICES:
        raise SmartNotesRefusal("bad_note_voice",
                                "notes[%d]: voice %r not in %s" % (i, voice, "/".join(VOICES)))
    if len(title) > 200:
        raise SmartNotesRefusal("bad_note", "notes[%d]: title too long" % i)
    if len(body) > 20000:
        raise SmartNotesRefusal("bad_note", "notes[%d]: body too long" % i)
    return title, body.strip(), voice


def decl_for(contract):
    """Extract the smart_notes declaration from a contract, or None.

    Accepts the PLUMBING.md breaker convention (contract.features.smart_notes):
      - dict  -> the declaration (task shape: enabled/notes/link_base/…)
      - True  -> enabled with empty fields (capture panel fallback)
      - falsy / absent / features-not-a-dict -> None (not declared)
      - anything else truthy -> SmartNotesRefusal('bad_smart_notes_declaration')
    """
    feats = contract.get("features") if isinstance(contract, dict) else None
    if not isinstance(feats, dict):
        return None  # contract-page contracts carry features as a list
    if "smart_notes" not in feats:
        return None
    decl = feats["smart_notes"]
    if not decl:
        return None
    if decl is True:
        return {"enabled": True}
    if isinstance(decl, dict):
        return decl
    raise SmartNotesRefusal("bad_smart_notes_declaration",
                            "contract.features.smart_notes must be an object or true, "
                            "got %s" % type(decl).__name__)


def mint_note_id(page_address, index, title, body):
    """Deterministic note identity: same inputs -> same id, always."""
    raw = "%s|%d|%s|%s" % (page_address or "", index, title, body)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:12]


def mint_link(link_base, note_id):
    return "%s/sn/%s" % (link_base, note_id)


# The capture panel's script: binds ONLY to elements rendered above it
# (L-2026-10-17-004). Delegated copy buttons + a local-only composer.
# It never claims network publish — the caption says so in plain words.
CAPTURE_SCRIPT = """<script>
(function(){
  function ready(fn){if(document.readyState!=='loading'){fn();}else{document.addEventListener('DOMContentLoaded',fn);}}
  ready(function(){
    var root=document.querySelector('[data-feature="smart_notes"]');
    if(!root){return;}
    function djb2(s){var h=5381;for(var i=0;i<s.length;i++){h=((h<<5)+h+s.charCodeAt(i))>>>0;}return ('0000000'+h.toString(16)).slice(-8);}
    root.addEventListener('click',function(ev){
      var btn=ev.target.closest ? ev.target.closest('[data-copy-target]') : null;
      if(!btn||!root.contains(btn)){return;}
      var chip=document.getElementById(btn.getAttribute('data-copy-target'));
      if(!chip){return;}
      var done=function(){btn.textContent='Copied';setTimeout(function(){btn.textContent='Copy link';},1500);};
      var text=chip.textContent;
      if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(text).then(done,done);}
      else{var ta=document.createElement('textarea');ta.value=text;document.body.appendChild(ta);ta.select();try{document.execCommand('copy');}catch(e){}document.body.removeChild(ta);done();}
    });
    var form=document.getElementById('sn-capture');
    if(!form){return;}
    var text=document.getElementById('sn-text');
    var voice=document.getElementById('sn-voice');
    var out=document.getElementById('sn-result');
    if(!text||!voice||!out){return;}
    form.addEventListener('submit',function(ev){
      ev.preventDefault();
      var body=text.value.trim();
      if(!body){out.textContent='Write the note first — empty notes are not saved.';return;}
      var v=voice.value||'naya';
      var title=body.split('\\n')[0].slice(0,80)||'Untitled note';
      var id=djb2(v+'|'+title+'|'+body);
      var link='BASE_PLACEHOLDER/sn/'+id;
      out.innerHTML='';
      var chip=document.createElement('code');chip.className='sn-link';chip.id='snlink-local';chip.textContent=link;
      var btn=document.createElement('button');btn.type='button';btn.className='sn-copy';btn.setAttribute('data-copy-target','snlink-local');btn.textContent='Copy link';
      var cap=document.createElement('p');cap.className='sn-fine';cap.textContent='Saved on this page only — minted '+link+'. Not connected — connect the NayaNET bridge to enable sharing.';
      out.appendChild(chip);out.appendChild(btn);out.appendChild(cap);
      text.value='';
    });
  });
})();
</script>"""


def note_card(note_id, title, body, voice, link):
    chip_id = "snlink-%s" % note_id
    paras = "".join("<p>%s</p>" % esc(p) for p in body.split("\n") if p.strip())
    return (
        '<article class="sn-note" data-note-id="%s">'
        '<div class="sn-meta"><span class="sn-voice">%s voice</span></div>'
        '<h3 class="sn-title">%s</h3>'
        '<div class="sn-body">%s</div>'
        '<div class="sn-linkrow">'
        '<code class="sn-link" id="%s">%s</code>'
        '<button type="button" class="sn-copy" data-copy-target="%s">Copy link</button>'
        '</div>'
        '<p class="sn-fine">Smart link minted at build time · '
        '<span data-link-state="minted-unresolved" data-grant-needed="%s">'
        'not connected — connect the %s to enable link resolution</span>.</p>'
        '</article>'
        % (esc(note_id), esc(voice), esc(title), paras, chip_id, esc(link), chip_id,
           esc(GRANT_RESOLVE), esc(CONNECTION_NAME))
    )


def capture_panel(link_base):
    voices = "".join('<option value="%s"%s>%s</option>'
                     % (v, ' selected' if v == "naya" else "", v.capitalize())
                     for v in VOICES)
    return (
        '<form class="sn-capture" id="sn-capture">'
        '<h3 class="sn-title">Smart note this</h3>'
        '<p class="sn-fine">Write it here — it saves on this page and mints its smart link. '
        'Nothing leaves the page until the %s is connected.</p>'
        '<label class="sn-label" for="sn-text">Your note</label>'
        '<textarea class="sn-text" id="sn-text" rows="3"></textarea>'
        '<label class="sn-label" for="sn-voice">Voice</label>'
        '<select class="sn-voice-sel" id="sn-voice">%s</select>'
        '<button type="submit" class="sn-save" id="sn-save">Save note</button>'
        '<div class="sn-result" id="sn-result" aria-live="polite"></div>'
        '</form>' % (CONNECTION_NAME, voices)
    )


def render_smart_notes(decl, registry_status, page_address="", context=None):
    """Render the Smart Notes section. Returns (html, events).

    Raises SmartNotesRefusal unless the registry says 'built' — rendering
    is proof the registry says built; the section carries
    data-smart-notes-status="built" as the binding. Events name every
    note created and every link minted (the receipt's proof).

    context: resolved contract context (connections+privacy+identity).
    The connected half (link resolution) needs the recorded grant AND the
    wired bridge; the grant is necessary but not sufficient, so the module
    keeps the honest ready-not-connected state until the bridge exists —
    never claimed live (L-2026-10-17-002).
    """
    if decl is None or not decl.get("enabled"):
        return "", []  # not declared -> refuse to render notes
    if registry_status != "built":
        raise SmartNotesRefusal(
            "feature_not_built",
            "contract declares smart_notes but registry status is %r "
            "(contract never activates an unbuilt capability)" % (registry_status,))

    link_base = sanitize_link_base(decl.get("link_base"))
    raw_notes = decl.get("notes")
    if raw_notes is None:
        notes = []
    elif isinstance(raw_notes, list):
        notes = raw_notes
    else:
        raise SmartNotesRefusal("bad_smart_notes_declaration",
                                "notes must be a list, got %s" % type(raw_notes).__name__)

    cards, events = [], []
    for i, raw in enumerate(notes):
        title, body, voice = sanitize_note(raw, i)
        note_id = mint_note_id(page_address, i, title, body)
        link = mint_link(link_base, note_id)
        cards.append(note_card(note_id, title, body, voice, link))
        events.append({"event": "smart_note.created", "feature": FEATURE_ID,
                       "version": VERSION, "note_id": note_id, "voice": voice})
        events.append({"event": "smart_link.minted", "feature": FEATURE_ID,
                       "version": VERSION, "note_id": note_id, "link": link,
                       "link_state": "minted-unresolved",
                       "connection": CONNECTION_NAME,
                       "grant_needed": GRANT_RESOLVE})

    script = CAPTURE_SCRIPT.replace("BASE_PLACEHOLDER", link_base)
    html_out = (
        '<section class="sn" data-feature="smart_notes" data-smart-notes-status="built">'
        '<div class="sn-head"><h2>Smart Notes</h2>'
        '<p class="sn-fine">Notes from this page, each with its own smart link.</p></div>'
        '%s%s%s</section>'
        % ("".join(cards), capture_panel(link_base), script)
    )
    return html_out, events
