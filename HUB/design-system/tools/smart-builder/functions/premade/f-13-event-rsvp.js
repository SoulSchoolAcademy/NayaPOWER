/* NayaFunction: f-13-event-rsvp v1.0.0
   What: event invite — details, RSVP yes/no with party size, live attendee
     count that updates when people respond
   Activation: <div data-fn="f-13-event-rsvp" data-fn-config='{...}'></div>
   Config: {
     title: string,               // * event name
     date_label: string,          // e.g. "Sat, Oct 24"
     time_label: string,          // e.g. "7:00 PM"
     venue: string,               // where
     description: string,        // what it is
     base_attendees: number,      // already-confirmed count from elsewhere (default 0)
     storage_key: string         // localStorage key (default "naya_fn_f13_rsvp")
   }
   Ready behavior: full RSVP flow client-side — name + yes/no + party size,
     attendee total = base + saved yes-responses, persisted to localStorage,
     re-submitting under the same name updates that response. No backend needed.
   Connected behavior: none (reserved key `connected`).
   Backend twin: none.
*/
(function(){
'use strict';
var NF = window.NayaFunctions = window.NayaFunctions || {};
NF._r = NF._r || {};
NF.register = NF.register || function(id, def){ if (!NF._r[id]) NF._r[id] = def; };

var CSS = [
'.nf-f13{--nf-accent:#40d3bb;--obs:#0b0d14;--raise:#121623;--white:#ffffff;--silver:#c9c9d4;--slate:#8a8a99;--line:rgba(255,255,255,.12);',
'font-family:Inter,ui-sans-serif,system-ui,sans-serif;color:var(--silver);font-size:15px;line-height:1.5}',
'.nf-f13 *{box-sizing:border-box}',
'.nf-f13 .nf-board{background:linear-gradient(180deg,var(--raise),var(--obs));border:1px solid var(--line);border-radius:20px;',
'padding:26px 22px;box-shadow:0 18px 44px rgba(0,0,0,.5),inset 0 1px 0 rgba(255,255,255,.06);position:relative;overflow:hidden}',
'.nf-f13 .nf-rail{position:absolute;left:0;top:0;bottom:0;width:5px;background:var(--nf-accent);box-shadow:0 0 14px var(--nf-accent)}',
'.nf-f13 .nf-kicker{font-size:11px;letter-spacing:.22em;text-transform:uppercase;font-weight:700;color:#ffffff;margin-bottom:10px}',
'.nf-f13 h3{color:#ffffff;font-size:22px;margin:0 0 10px;font-weight:600}',
'.nf-f13 .nf-when{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:12px}',
'.nf-f13 .nf-pill{background:#0a0a0f;border:1.5px solid rgba(255,255,255,.35);border-radius:999px;color:#ffffff;',
'font-size:13px;font-weight:600;padding:7px 14px}',
'.nf-f13 .nf-desc{color:var(--silver);font-size:14px;margin:0 0 16px}',
'.nf-f13 .nf-countrow{display:flex;align-items:center;gap:10px;margin:0 0 18px;padding:12px 14px;border-radius:14px;',
'background:#0a0a0f;border:1px solid var(--line)}',
'.nf-f13 .nf-led{width:12px;height:12px;border-radius:50%;background:#2fe89e;box-shadow:0 0 12px #2fe89e;flex:none}',
'.nf-f13 .nf-countrow span{color:#ffffff;font-size:15px;font-weight:600}',
'.nf-f13 .nf-countrow span b{font-size:20px}',
'.nf-f13 .nf-field{margin-bottom:14px}',
'.nf-f13 .nf-field label{display:block;font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:var(--silver);margin-bottom:8px;font-weight:600}',
'.nf-f13 .nf-field input{width:100%;background:#0a0a0f;border:1.5px solid rgba(255,255,255,.35);border-radius:12px;',
'color:#ffffff;font-size:16px;padding:12px 14px;outline:none;transition:border-color .18s,box-shadow .18s}',
'.nf-f13 .nf-field input:focus{border-color:var(--nf-accent);box-shadow:0 0 0 1px var(--nf-accent),0 0 14px rgba(64,211,187,.35)}',
'.nf-f13 .nf-yn{display:flex;gap:10px;margin-bottom:16px}',
'.nf-f13 .nf-yesno{flex:1;background:#0a0a0f;border:1.5px solid rgba(255,255,255,.55);color:#ffffff;border-radius:14px;',
'padding:13px 8px;font-size:15px;font-weight:700;cursor:pointer;transition:border-color .18s,box-shadow .18s;box-shadow:0 6px 16px rgba(0,0,0,.4)}',
'.nf-f13 .nf-yesno:hover{border-color:#ffffff}',
'.nf-f13 .nf-yesno.is-yes{border-color:#2fe89e;box-shadow:0 0 0 1px #2fe89e,0 0 18px rgba(47,232,158,.45)}',
'.nf-f13 .nf-yesno.is-no{border-color:#ff5e6c;box-shadow:0 0 0 1px #ff5e6c,0 0 18px rgba(255,94,108,.45)}',
'.nf-f13 .nf-partyrow{display:flex;align-items:center;justify-content:space-between;margin-bottom:16px}',
'.nf-f13 .nf-partyrow .lbl{font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:var(--silver);font-weight:600}',
'.nf-f13 .nf-stepper{display:flex;align-items:center;gap:10px}',
'.nf-f13 .nf-stbtn{width:38px;height:38px;border-radius:50%;background:#0a0a0f;border:1.5px solid rgba(255,255,255,.55);',
'color:#ffffff;font-size:20px;font-weight:700;cursor:pointer;line-height:1;transition:border-color .18s,box-shadow .18s;box-shadow:0 6px 14px rgba(0,0,0,.4)}',
'.nf-f13 .nf-stbtn:hover{border-color:var(--nf-accent);box-shadow:0 0 12px rgba(64,211,187,.45)}',
'.nf-f13 .nf-qty{color:#ffffff;font-size:18px;font-weight:700;min-width:28px;text-align:center}',
'.nf-f13 .nf-btn{display:block;width:100%;background:#0a0a0f;border:2px solid #ffffff;color:#ffffff;',
'border-radius:999px;padding:14px 18px;font-size:16px;font-weight:700;cursor:pointer;letter-spacing:.04em;',
'transition:border-color .18s,box-shadow .18s,transform .12s;box-shadow:0 8px 22px rgba(0,0,0,.45),inset 0 1px 0 rgba(255,255,255,.08)}',
'.nf-f13 .nf-btn:hover{border-color:var(--nf-accent);box-shadow:0 0 22px rgba(64,211,187,.5),inset 0 1px 0 rgba(255,255,255,.08);transform:translateY(-1px)}',
'.nf-f13 .nf-btn:active{transform:translateY(1px)}',
'.nf-f13 .nf-err{display:none;margin-top:10px;padding:10px 14px;border-radius:12px;background:rgba(255,94,108,.08);',
'border-left:4px solid #ff5e6c;color:#ffffff;font-size:14px}',
'.nf-f13 .nf-err.show{display:block}',
'.nf-f13 .nf-me{margin-top:14px;padding:12px 14px;border-radius:14px;border:1px solid var(--line);color:#ffffff;font-size:14px}',
'.nf-f13 .nf-me b{font-weight:700}',
'.nf-f13 .nf-chg{background:transparent;border:none;color:var(--slate);cursor:pointer;font-size:13px;text-decoration:underline;padding:0 0 0 8px}',
'.nf-f13 .nf-chg:hover{color:#ffffff}',
'.nf-f13 .nf-failsoft{padding:18px;border-radius:14px;border:1px dashed rgba(255,255,255,.3);color:#ffffff;font-size:14px}'
].join('');

function escapeHtml(s){
  return String(s == null ? '' : s).replace(/[&<>"']/g, function(c){
    return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
  });
}
function load(key){ try { var v = localStorage.getItem(key); return v ? JSON.parse(v) : {}; } catch (e) { return {}; } }
function save(key, v){ try { localStorage.setItem(key, JSON.stringify(v)); } catch (e) {} }

NF.register('event-rsvp', {
  version: '1.0.0',
  activate: function(root, config){
    config = config || {};
    root.classList.add('nf-f13');
    var st = document.createElement('style');
    st.textContent = CSS;
    root.appendChild(st);

    var title = typeof config.title === 'string' ? config.title : '';
    var key = config.storage_key || 'naya_fn_f13_rsvp';
    var base = (typeof config.base_attendees === 'number' && isFinite(config.base_attendees) && config.base_attendees >= 0)
      ? Math.floor(config.base_attendees) : 0;
    var listeners = [];
    function on(el, ev, fn){ el.addEventListener(ev, fn); listeners.push([el, ev, fn]); }

    // Fail soft: an invite without a title is a blank page — say so honestly.
    if (!title) {
      root.insertAdjacentHTML('beforeend',
        '<div class="nf-board"><div class="nf-rail"></div><div class="nf-failsoft">This invite is missing its event title — the page owner still needs to set it up.</div></div>');
      return { destroy: function(){} };
    }

    var rsvps = load(key); // nameKey -> {name, yes, party}
    function attending(){
      var n = base;
      for (var k in rsvps) if (rsvps.hasOwnProperty(k) && rsvps[k].yes) n += (rsvps[k].party || 1);
      return n;
    }

    var sel = { yes: null }; // true | false | null
    var party = 1;
    var me = null; // currently-displayed respondent key (for "change")

    function render(){
      root.innerHTML = '';
      root.appendChild(st);
      var b = document.createElement('div');
      b.className = 'nf-board';
      var pills = [];
      if (config.date_label) pills.push('<span class="nf-pill">' + escapeHtml(config.date_label) + '</span>');
      if (config.time_label) pills.push('<span class="nf-pill">' + escapeHtml(config.time_label) + '</span>');
      if (config.venue) pills.push('<span class="nf-pill">' + escapeHtml(config.venue) + '</span>');
      b.innerHTML =
        '<div class="nf-rail"></div>' +
        '<div class="nf-kicker">You are invited</div>' +
        '<h3>' + escapeHtml(title) + '</h3>' +
        (pills.length ? '<div class="nf-when">' + pills.join('') + '</div>' : '') +
        (config.description ? '<p class="nf-desc">' + escapeHtml(config.description) + '</p>' : '') +
        '<div class="nf-countrow"><span class="nf-led"></span><span><b data-r="count">' + attending() + '</b> attending</span></div>' +
        '<div class="nf-field"><label for="nf13-name">Your name</label>' +
        '<input id="nf13-name" type="text" data-in="name" placeholder="e.g. Shawn Vibert" maxlength="80" autocomplete="name"></div>' +
        '<div class="nf-yn">' +
          '<button class="nf-yesno" data-act="yes">Yes, I\'m in</button>' +
          '<button class="nf-yesno" data-act="no">Can\'t make it</button>' +
        '</div>' +
        '<div class="nf-partyrow"><span class="lbl">Party size</span>' +
          '<div class="nf-stepper">' +
            '<button class="nf-stbtn" data-act="pdec" aria-label="Decrease party size">−</button>' +
            '<span class="nf-qty" data-r="party">1</span>' +
            '<button class="nf-stbtn" data-act="pinc" aria-label="Increase party size">+</button>' +
          '</div></div>' +
        '<button class="nf-btn" data-act="send">Send RSVP</button>' +
        '<div class="nf-err" data-e="err"></div>' +
        '<div data-r="me"></div>';
      root.appendChild(b);

      var countEl = b.querySelector('[data-r="count"]');
      var partyEl = b.querySelector('[data-r="party"]');
      var yesBtn = b.querySelector('[data-act="yes"]');
      var noBtn = b.querySelector('[data-act="no"]');
      var nameIn = b.querySelector('[data-in="name"]');
      var meBox = b.querySelector('[data-r="me"]');
      var errBox = b.querySelector('[data-e="err"]');

      function markYN(){
        yesBtn.classList.toggle('is-yes', sel.yes === true);
        noBtn.classList.toggle('is-no', sel.yes === false);
      }
      function fail(msg){ errBox.style.borderLeftColor = '#ff5e6c'; errBox.textContent = msg; errBox.classList.add('show'); }
      function paintMe(){
        if (!me || !rsvps[me]) { meBox.innerHTML = ''; return; }
        var r = rsvps[me];
        meBox.innerHTML = '<div class="nf-me">You (' + escapeHtml(r.name) + '): <b>' +
          (r.yes ? 'Yes' : 'No') + '</b>' + (r.yes ? ' · party of ' + r.party : '') +
          '<button class="nf-chg" data-act="chg">change</button></div>';
        on(meBox.querySelector('[data-act="chg"]'), 'click', function(){
          me = null;
          nameIn.value = '';
          sel.yes = null; party = 1; markYN(); partyEl.textContent = '1'; paintMe();
        });
      }
      paintMe();

      var acts = b.querySelectorAll('[data-act]');
      for (var i = 0; i < acts.length; i++) on(acts[i], 'click', function(ev){
        var act = ev.currentTarget.getAttribute('data-act');
        if (act === 'yes') { sel.yes = true; markYN(); }
        else if (act === 'no') { sel.yes = false; markYN(); }
        else if (act === 'pinc') { party = Math.min(20, party + 1); partyEl.textContent = party; }
        else if (act === 'pdec') { party = Math.max(1, party - 1); partyEl.textContent = party; }
        else if (act === 'send') { send(); }
      });

      function send(){
        var nm = (nameIn.value || '').trim();
        if (!nm) { fail('Give us your name so the host knows who is who.'); return; }
        if (sel.yes === null) { fail('Tap Yes or No so we know where you stand.'); return; }
        var k = nm.toLowerCase();
        var isUpdate = !!rsvps[k];
        rsvps[k] = { name: nm, yes: sel.yes, party: party, at: Date.now() };
        save(key, rsvps);
        me = k;
        countEl.textContent = attending();
        paintMe();
        nameIn.value = '';
        sel.yes = null; party = 1; markYN(); partyEl.textContent = '1';
        errBox.classList.remove('show');
        fail(isUpdate ? 'Updated — your RSVP was changed.' : 'RSVP received — see you there!');
        errBox.classList.add('show');
        errBox.style.borderLeftColor = '#2fe89e';
      }
    }

    render();
    return { destroy: function(){
      for (var i = 0; i < listeners.length; i++) {
        try { listeners[i][0].removeEventListener(listeners[i][1], listeners[i][2]); } catch (e) {}
      }
      listeners = [];
      try { root.classList.remove('nf-f13'); } catch (e) {}
    } };
  }
});
})();
