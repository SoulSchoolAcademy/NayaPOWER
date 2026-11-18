#!/usr/bin/env python3
"""WALKTHROUGH-CHAIN edit driver (2026-11-18).

Job 1 — BRIDGE FIRST (welcome): after agreeing inside the stage, the
hold/fallback releases go to the bridge (goBridgeAfterAgree), then the
bridge's own buttons go to name-entry. Pre-agree routes untouched.
Job 2 — IDENTITY TRUST (identity): a name match alone NEVER grants
ownership. On "taken" the row is read back WITH this browser's device
key; only d.own grants. Without the key the citizen gets the key panel:
paste the device key, press "Use my key", the key is verified against
the registry row, and only then does the cert stamp + Enter proceed.
The key is also SHOWN on the certified certificate (#certKey) so the
citizen can carry it to another device.

Bases (verified by sha256 before editing):
  welcome  = fix1/cond welcome, 1,851,969 B, sha d367efe1...
  identity = walkthrough-frontend tip 8eaaecb1, 380,286 B, sha 9c9cc86c...
Inputs:  work/welcome-chain-base.html, work/identity-chain-base.html
Outputs: work/welcome-chain.html, work/identity-chain.html
Every replacement is asserted (exact count); node --check runs on every
inline script block of both files. Writes are verified by size + sha.
"""
import hashlib, os, re, subprocess, sys

HOME = os.path.expanduser("~")
WORK = os.path.join(HOME, "workspace/team-nitro/walkthrough-chain-20261118/work")

def sha(b): return hashlib.sha256(b).hexdigest()

def read(p):
    with open(p, "rb") as f: return f.read()

def write_verified(path, data):
    tmp = path + ".tmp-chain"
    with open(tmp, "wb") as f:
        for i in range(0, len(data), 8192): f.write(data[i:i+8192])
        f.flush(); os.fsync(f.fileno())
    got = read(tmp)
    assert len(got) == len(data) and sha(got) == sha(data), "tmp verify failed: " + path
    os.replace(tmp, path)
    got2 = read(path)
    assert len(got2) == len(data) and sha(got2) == sha(data), "final verify failed: " + path
    print("wrote %s %d B sha %s" % (path, len(data), sha(data)[:12]), flush=True)

def rep(data, old, new, count, label):
    n = data.count(old)
    assert n == count, "%s: expected %d, found %d" % (label, count, n)
    return data.replace(old, new)

def node_check(data, label):
    blocks = re.findall(rb"<script>(.*?)</script>", data, re.S)
    print("%s: %d inline script blocks" % (label, len(blocks)), flush=True)
    assert blocks, label + ": no script blocks found"
    for i, b in enumerate(blocks):
        tmp = os.path.join(WORK, "nodecheck-%s-%d.js" % (label, i))
        with open(tmp, "wb") as f: f.write(b)
        r = subprocess.run(["node", "--check", tmp], capture_output=True, text=True)
        assert r.returncode == 0, "%s block %d node --check failed: %s" % (label, i, r.stderr[:500])
        print("%s block %d: node --check OK (%d B)" % (label, i, len(b)), flush=True)

# ---------------------------------------------------------------- welcome
w = read(os.path.join(WORK, "welcome-chain-base.html"))
assert len(w) == 1851969 and sha(w).startswith("d367efe1"), "welcome base mismatch"
w = w.decode("utf-8")

# W1 — agreed line at the top of the bridge (hidden until post-agree).
w = rep(w,
    'id="fpBridge"> <div class="fp-bridge-group" id="fpBridgeG1">',
    'id="fpBridge"> <p class="letter-steplabel" id="fpBridgeAgreed" hidden>Agreed &#9670; Welcome home.</p> <div class="fp-bridge-group" id="fpBridgeG1">',
    1, "W1 agreed line")

# W2 — onward button in the bridge final (hidden until post-agree).
w = rep(w,
    '</div><button class="fp-intro-choice fp-bridge-exit" id="fpBridgeExit"',
    '</div><button class="fp-intro-choice" id="fpBridgeToName" type="button" style="--tone:#07925f;margin-top:12px" hidden>Continue &#8212; enter your name <span class="fp-btn-jewel" aria-hidden="true"></span></button><button class="fp-intro-choice fp-bridge-exit" id="fpBridgeExit"',
    1, "W2 onward button")

# W3 — scoped hidden rule: .fp-intro-choice{display:block} beats [hidden].
w = rep(w,
    "#fpNextBtn[hidden]{display:none}\nbody.fp-stage-on.fp-bridge #fpStageBarB{display:none}",
    "#fpNextBtn[hidden]{display:none}\n/* WALKTHROUGH-CHAIN (2026-11-18) — the onward button is a .fp-intro-choice\n   (display:block beats UA [hidden], same root cause as the More pills):\n   this scoped rule hides it until the citizen has agreed. */\n#fpBridgeToName[hidden]{display:none}\nbody.fp-stage-on.fp-bridge #fpStageBarB{display:none}",
    1, "W3 hidden rule")

# W7 first (before W4 inserts a similar reset line): enterStage resets the
# agreed line + onward button, so re-entering the stage shows the bridge
# in its pre-agree presentation.
w = rep(w,
    "if(bm1)bm1.hidden=false;if(bm2)bm2.hidden=true;if(bm3)bm3.hidden=true;if(bm4)bm4.hidden=true;}",
    "if(bm1)bm1.hidden=false;if(bm2)bm2.hidden=true;if(bm3)bm3.hidden=true;if(bm4)bm4.hidden=true;var _ag2=q('#fpBridgeAgreed');if(_ag2)_ag2.hidden=true;var _on2=q('#fpBridgeToName');if(_on2)_on2.hidden=true;}",
    1, "W7 enterStage reset")

# W4 — goBridgeAfterAgree(), right before exitStage().
w = rep(w,
    "  function exitStage(){",
    """  /* WALKTHROUGH-CHAIN (2026-11-18, Shawn ~21:54Z) — BRIDGE FIRST:
     after agreeing inside the stage, the citizen goes to the bridge
     next, then from the bridge to name-entry. The bridge is the welcome
     between agreeing and naming — context before they claim anything.
     The hold's release calls this, never exitStage() directly: the
     stage stays up, S.view='bridge', the unfold resets to group 1,
     and the agreed line + the onward button show. The bridge's own
     "Back to the login" (#fpBridgeExit) and the new "Continue — enter
     your name" (#fpBridgeToName) both call exitStage() — that is the
     bridge-to-name-entry step. Pre-agree routes are untouched:
     ?stage=bridge, the Back buttons, and /agreement agree → bridge
     still land here with the agreed line and the onward button hidden. */
  function goBridgeAfterAgree(){
    window.__fpAgreed=true;
    cancelAgreeExit();
    S.view='bridge';S.all=null;
    var bg2=q('#fpBridgeG2'),bg3=q('#fpBridgeG3'),bg4=q('#fpBridgeG4'),bf=q('#fpBridgeFinal'),bm1=q('#fpBridgeMore1'),bm2=q('#fpBridgeMore2'),bm3=q('#fpBridgeMore3'),bm4=q('#fpBridgeMore4');
    if(bg2)bg2.hidden=true;if(bg3)bg3.hidden=true;if(bg4)bg4.hidden=true;if(bf)bf.hidden=true;if(bm1)bm1.hidden=false;if(bm2)bm2.hidden=true;if(bm3)bm3.hidden=true;if(bm4)bm4.hidden=true;
    var ag=q('#fpBridgeAgreed');if(ag)ag.hidden=false;
    var on=q('#fpBridgeToName');if(on)on.hidden=false;
    render();
    var br=q('#fpBridge');if(br)br.scrollTop=0;
  }
  function exitStage(){""",
    1, "W4 goBridgeAfterAgree")

# W5a — deck-end Enter (nextBtn) + beat-9 anchor: hold releases to bridge.
w = rep(w, "showNHold(function(){exitStage();});",
        "showNHold(function(){goBridgeAfterAgree();});", 2, "W5a deckJoin holds")
# W5b — I agree: hold releases to bridge.
w = rep(w, "showNHold(function(){cancelAgreeExit();exitStage();});",
        "showNHold(function(){goBridgeAfterAgree();});", 1, "W5b agree hold")
# W5c — the 10s agree fallback: also bridge, never straight to login.
w = rep(w, "stopAgreeCount();exitStage();},10000);",
        "stopAgreeCount();goBridgeAfterAgree();},10000);", 1, "W5c agree fallback")

# W6 — the plain-page agree handler's 2000ms scroll must not yank the
# viewport under the bridge (DOM-read guard, same shape as the FIX1 hold
# guard: it works across the two script blocks).
w = rep(w,
    """      var _nh=document.getElementById('fpNHold');
      if(_nh&&!_nh.hidden)return;""",
    """      var _nh=document.getElementById('fpNHold');
      if(_nh&&!_nh.hidden)return;
      /* WALKTHROUGH-CHAIN — never scroll the login into view UNDER the
         bridge: after agreeing, the citizen is on the bridge, and this
         2000ms scroll would yank the viewport beneath it. */
      var _ag=document.getElementById('fpAgreement');
      if(_ag&&_ag.classList.contains('fp-view-bridge'))return;""",
    1, "W6 scroll guard")

# W8 — wire the onward button beside the bridge exit.
w = rep(w,
    "if(bExit){bExit.addEventListener('click',function(){cancelAgreeExit();exitStage();});}",
    "if(bExit){bExit.addEventListener('click',function(){cancelAgreeExit();exitStage();});}\n  var bToName=q('#fpBridgeToName');if(bToName){bToName.addEventListener('click',function(){cancelAgreeExit();exitStage();});}",
    1, "W8 onward wiring")

# W9 — the hold comment still says "release to the name-entry login".
w = rep(w,
    "Stamp .55s + hold 3000ms from first paint, then release to the\n     name-entry login. Tap anywhere to continue at once — the 3s never\n     traps. */",
    "Stamp .55s + hold 3000ms from first paint, then release to the\n     bridge — CHAIN (2026-11-18): bridge first, then name-entry from\n     the bridge. Tap anywhere to continue at once — the 3s never\n     traps. */",
    1, "W9 hold comment")

wb = w.encode("utf-8")
node_check(wb, "welcome")
write_verified(os.path.join(WORK, "welcome-chain.html"), wb)
print("welcome chain sha %s" % sha(wb))

# ---------------------------------------------------------------- identity
d = read(os.path.join(WORK, "identity-chain-base.html"))
assert len(d) == 380286 and sha(d).startswith("9c9cc86c"), "identity base mismatch"
d = d.decode("utf-8")

# I1 — the key panel, right after the hubNote line.
d = rep(d,
    """        <p class="hub-note" id="hubNote" hidden>One step left: set <code>HUB_APP_URL</code> in this page to your Intelligent Hub address, then this button takes you straight in.</p>""",
    """        <p class="hub-note" id="hubNote" hidden>One step left: set <code>HUB_APP_URL</code> in this page to your Intelligent Hub address, then this button takes you straight in.</p>
        <div class="key-panel" id="keyPanel" hidden>
          <p class="key-panel-line">This name is yours? Use your device key.</p>
          <p class="key-panel-help">Your key lives on the device where you claimed this name — it is shown on your certificate there. Paste it here, then press the button.</p>
          <div class="alias-field-wrapper key-input-wrap"><input type="text" id="keyInput" class="alias-field-input" placeholder="Paste your device key" autocomplete="off" /></div>
          <button type="button" class="activate-btn key-use-btn" id="keyUseBtn"><span class="ab-face" aria-hidden="true"></span><span class="ab-content"><span class="ab-title">Use my key</span></span></button>
          <p class="key-note" id="keyNote" hidden></p>
        </div>""",
    1, "I1 key panel")

# I2 — the key shown on the certified certificate, after the regalia.
d = rep(d,
    """        </div>
        <p class="cert-agree-cert">This is your certificate of agreement.</p>""",
    """        </div>
        <div class="cert-key" id="certKey" hidden>
          <span class="id-box-label">Your device key</span>
          <span class="id-box-value key-value" id="keyValue"></span>
          <button type="button" class="cert-more key-copy" id="keyCopyBtn">Copy key</button>
        </div>
        <p class="cert-agree-cert">This is your certificate of agreement.</p>""",
    1, "I2 key display")

# I3 — key CSS, after the taken-note rule (the last hub-note rule).
d = rep(d,
    """      box-shadow: inset 0 1px 0 rgba(255,255,255,0.12), 0 8px 24px rgba(0,0,0,0.6), 0 0 22px -4px rgba(47,232,158,0.45); }""",
    """      box-shadow: inset 0 1px 0 rgba(255,255,255,0.12), 0 8px 24px rgba(0,0,0,0.6), 0 0 22px -4px rgba(47,232,158,0.45); }
    /* WALKTHROUGH-CHAIN (2026-11-18) — THE DEVICE KEY, PRESENTED.
       The key is a real object, royal, obvious: the panel is an
       obsidian board with a royal-purple rim (the certificate's own
       purple), the well is the harvested alias well verbatim, the
       button is the harvested ENTER plate verbatim, the shown key
       sits in its own lit box. White text only, 17px floor.
       Nothing here is invented — every piece is harvested from this
       page. The panel shows ONLY on "taken" without the key; the
       key line shows ONLY on the certified certificate. */
    .key-panel{margin-top:14px;max-width:460px;margin-left:auto;margin-right:auto;text-align:center;
      background:linear-gradient(165deg,#120a1e 0%,#050505 100%);
      border:1px solid rgba(160,107,255,0.55);border-radius:12px;padding:14px;
      box-shadow:inset 0 1px 0 rgba(255,255,255,0.12),0 8px 24px rgba(0,0,0,0.6),0 0 22px -4px rgba(160,107,255,0.45);}
    .key-panel-line{font-size:17px;font-weight:700;line-height:1.5;color:#ffffff;margin:0 0 8px;}
    .key-panel-help{font-size:17px;font-weight:500;line-height:1.55;color:#ffffff;margin:0 0 12px;}
    .key-input-wrap{margin-top:4px;}
    .key-input-wrap .alias-field-input{font-size:17px;}
    .key-input-wrap .alias-field-input::placeholder{font-size:17px;}
    .key-use-btn{margin-top:12px;}
    .key-note{margin-top:10px;font-size:17px;font-weight:600;line-height:1.5;color:#ffffff;text-align:center;}
    .cert-key{margin-top:8px;max-width:460px;margin-left:auto;margin-right:auto;text-align:center;}
    .cert-key .key-value{display:block;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:17px;color:#ffffff;
      background:rgba(255,255,255,0.08);padding:8px 10px;border-radius:8px;word-break:break-all;margin:8px 0;}""",
    1, "I3 key CSS")

# I4 — show the key: one helper, called from both certified painters.
d = rep(d,
    "    window.stampCertificate = function(createdAt, certNo) {",
    """    /* WALKTHROUGH-CHAIN — show this device's key on the certified
       certificate, so the citizen can carry it to another device.
       The key is THIS browser's nayanet_vault_key, minted once and
       reused; it is shown only once the certificate is certified —
       never while composing. The Copy button wires once. */
    window.__chainShowKey = function(){
      try {
        var kv = document.getElementById('keyValue');
        var kk = document.getElementById('certKey');
        if (kv) { try { kv.textContent = localStorage.getItem('nayanet_vault_key') || ''; } catch(e){} }
        if (kk) kk.hidden = false;
        var kcb = document.getElementById('keyCopyBtn');
        if (kcb && !kcb.dataset.chainWired) {
          kcb.dataset.chainWired = '1';
          kcb.addEventListener('click', function(){
            var v = document.getElementById('keyValue');
            var txt = v ? v.textContent : '';
            var done = function(){ kcb.textContent = 'Copied \\u25C6'; setTimeout(function(){ kcb.textContent = 'Copy key'; }, 2000); };
            if (navigator.clipboard && navigator.clipboard.writeText) { navigator.clipboard.writeText(txt).then(done, done); }
            else { done(); }
          });
        }
      } catch(e){}
    };
    window.stampCertificate = function(createdAt, certNo) {""",
    1, "I4 show-key helper")

# I5 — stampCertificate paints the key too.
d = rep(d,
    """        paintNo(certNo);
        if (wrap) wrap.hidden = false;""",
    """        paintNo(certNo);
        if (wrap) wrap.hidden = false;
        try { if (window.__chainShowKey) window.__chainShowKey(); } catch(e){}""",
    1, "I5 stamp paints key")

# I6 — the 'own' restore paints the key too.
d = rep(d,
    """          if (cd) cd.textContent = 'Certified · ' + formatCertStamp(certRegalia.createdAt);
          if (wrap) wrap.hidden = false;""",
    """          if (cd) cd.textContent = 'Certified · ' + formatCertStamp(certRegalia.createdAt);
          if (wrap) wrap.hidden = false;
          try { if (window.__chainShowKey) window.__chainShowKey(); } catch(e){}""",
    1, "I6 restore paints key")

# I7 — remember the stored profile before this Enter overwrites it, so a
# "taken" stop can put it back instead of leaving someone else's name.
d = rep(d,
    """      var deviceKey = null;
      try { deviceKey = localStorage.getItem('nayanet_vault_key'); } catch(e){}""",
    """      var prevAlias = null, prevName = null;
      try { prevAlias = localStorage.getItem('nayanet_smart_alias'); prevName = localStorage.getItem('nayanet_smart_name'); } catch(e){}
      var deviceKey = null;
      try { deviceKey = localStorage.getItem('nayanet_vault_key'); } catch(e){}""",
    1, "I7 remember previous profile")

# I8 — stampCertificate's certNo read-back sends the device key too.
d = rep(d,
    """            fetch('/api/claim?alias=' + encodeURIComponent(savedAlias), { cache: 'no-store' })""",
    """            var _sk = null; try { _sk = localStorage.getItem('nayanet_vault_key'); } catch(e){}
            fetch('/api/claim?alias=' + encodeURIComponent(savedAlias) + (_sk ? '&device_key=' + encodeURIComponent(_sk) : ''), { cache: 'no-store' })""",
    1, "I8 read-back sends key")

# I9 — THE TRUST FIX: the taken branch. Read the row back WITH this
# browser's device key; ONLY d.own grants. A name match alone never
# opens it. Without the key: the taken note + the key panel, and the
# stored profile is put back the way it was.
old_taken = """          var showTaken = function() {
            setAliasState('taken', finalAlias);
            note.textContent = 'That alias is already claimed on another device. Pick a different alias to continue.';
            note.classList.add('taken-note'); /* ROUND 5 H6: green + unmissable. */
            note.hidden = false;"""
new_taken = """          var showTaken = function() {
            /* WALKTHROUGH-CHAIN — this Enter did not own the name, so
               the stored profile goes back the way it was: the claim
               above stored this alias + name before it knew the name
               was taken, and leaving someone else's name stored would
               poison the next load's restore. */
            try { if (prevAlias) localStorage.setItem('nayanet_smart_alias', prevAlias); else localStorage.removeItem('nayanet_smart_alias'); if (prevName) localStorage.setItem('nayanet_smart_name', prevName); else localStorage.removeItem('nayanet_smart_name'); } catch(e){}
            setAliasState('taken', finalAlias);
            note.textContent = 'That alias is already claimed. If it is yours, use your device key below — a name alone never opens it.';
            note.classList.add('taken-note'); /* ROUND 5 H6: green + unmissable. */
            note.hidden = false;
            var kp0 = document.getElementById('keyPanel'); if (kp0) kp0.hidden = false;"""
d = rep(d, old_taken, new_taken, 1, "I9a showTaken")

old_fetch = """          fetch('/api/claim?alias=' + encodeURIComponent(finalAlias), { cache: 'no-store' })
            .then(function(r){ return r.ok ? r.json() : null; })
            .then(function(d){
              var rowName = (d && d.name) ? String(d.name).trim().toLowerCase() : '';
              var myName = String(finalName || '').trim().toLowerCase();
              if (d && d.exists && rowName && myName && rowName === myName) {"""
new_fetch = """          /* WALKTHROUGH-CHAIN (2026-11-18, Shawn ~21:54Z) — IDENTITY IS
             NAME *PLUS* THE DEVICE KEY. The old code granted ownership
             on a NAME match alone: anyone who knew a citizen's name
             could walk in as them. That check is gone — deleted, not
             softened. The read-back now carries THIS browser's device
             key, and only the registry's own answer (d.own — the row's
             key matches this browser's key) grants. A matching name
             with no key does NOT grant: the citizen gets the key panel
             instead, and the key is verified the same way below. */
          var verifyKey = function(pastedKey){
            var kn = document.getElementById('keyNote');
            if (!pastedKey) { if (kn) { kn.textContent = 'Paste your device key first.'; kn.hidden = false; } return; }
            fetch('/api/claim?alias=' + encodeURIComponent(finalAlias) + '&device_key=' + encodeURIComponent(pastedKey), { cache: 'no-store' })
              .then(function(r){ return r.ok ? r.json() : null; })
              .then(function(dd){
                if (dd && dd.exists && dd.own) {
                  try { localStorage.setItem('nayanet_vault_key', pastedKey); } catch(e){}
                  try { localStorage.setItem('nayanet_smart_alias', finalAlias); localStorage.setItem('nayanet_smart_name', finalName); } catch(e){}
                  certRegalia = { createdAt: dd.created_at || null, certNo: (dd.cert_no != null ? dd.cert_no : null), alias: dd.alias || finalAlias, name: dd.name || null };
                  try { if (window.rememberIdentity) window.rememberIdentity(finalAlias, finalName); } catch(e){}
                  var kp2 = document.getElementById('keyPanel'); if (kp2) kp2.hidden = true;
                  setAliasState('own', finalAlias);
                  try { if (window.stampCertificate) window.stampCertificate(certRegalia.createdAt, certRegalia.certNo); } catch(e){}
                  setTimeout(function(){ window.location.href = walkthroughEntryUrl(finalName, finalAlias); }, 800);
                } else { if (kn) { kn.textContent = 'That key does not match this name. Check the key on the device where you claimed it.'; kn.hidden = false; } }
              })
              .catch(function(){ if (kn) { kn.textContent = 'The key could not be checked — try Enter again.'; kn.hidden = false; } });
          };
          var kub = document.getElementById('keyUseBtn');
          if (kub && !kub.dataset.chainWired) { kub.dataset.chainWired = '1'; kub.addEventListener('click', function(){ var ki = document.getElementById('keyInput'); verifyKey(ki ? ki.value.trim() : ''); }); }
          fetch('/api/claim?alias=' + encodeURIComponent(finalAlias) + '&device_key=' + encodeURIComponent(deviceKey), { cache: 'no-store' })
            .then(function(r){ return r.ok ? r.json() : null; })
            .then(function(d){
              if (d && d.exists && d.own) {"""
d = rep(d, old_fetch, new_fetch, 1, "I9b key-checked read-back")

# I9c — the old name-match grant body stays, but it now runs ONLY on d.own.
# The stale comment above it must go: it describes the deleted check.
old_comment = """          /* WALKTHROUGH-FRONTEND 2026-11-18 — "already claimed" is not
             always a stranger: the row may carry THIS citizen's own
             name (claimed once, on a device whose key this browser
             never held — Shawn's own cert Nº 1, "shawn"/"Shawn",
             Oct 20). The claim POST only says taken; the GET read-back
             carries the row's name. When that name matches the name
             this citizen arrived with, the citizen IS the owner: the
             certificate stamps from registry truth (real Nº + stamp)
             and Enter goes on to the walkthrough, the same as a fresh
             claim. A name that does NOT match still stops here, exactly
             as before. No credential is read, written, or bypassed —
             the check is the registry row's own name against the name
             the citizen arrived with, the same name the Hub handoff
             already trusts (?name=&alias=, no key). */"""
new_comment = """          /* WALKTHROUGH-CHAIN — the grant below runs ONLY when the
             registry says this browser holds the row's device key
             (d.own). The frontend round's name-match grant is deleted:
             a name alone never proves ownership. */"""
d = rep(d, old_comment, new_comment, 1, "I9c stale comment")

db = d.encode("utf-8")
node_check(db, "identity")
write_verified(os.path.join(WORK, "identity-chain.html"), db)
print("identity chain sha %s" % sha(db))
print("CHAIN EDIT DONE")
