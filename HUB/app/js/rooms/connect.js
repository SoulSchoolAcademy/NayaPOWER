/* SMART CONNECT — Room: understand and configure connection doors.
 * Registry: HUB app rooms registry id "connect", route "/connect", theme emerald.
 * Contract: window.NayaRooms.connect(el, ctx)
 *   ctx.doors     — door view-models from ConnectAdapter.parse (canonical registry)
 *   ctx.onConnect — optional fn(doorId); called when a CONNECT/MANAGE button fires.
 *                   Without it, the room shows the door's honest state inline.
 * Law: a door never grants authority. LAW decides permitted use, every operation.
 * Every button has a real consequence: live doors call onConnect; doors in
 * design open an honest inline panel — never a fake connection.
 */
(function(){
  'use strict';

  /* plain-words copy, keyed by canonical door id. Presentation lives here;
     the facts underneath come from the registry via the adapter. */
  var DOOR_COPY = {
    'DOOR-GITHUB': {
      tagline: 'Your code\u2019s front door.',
      plain: 'Plug GitHub in and Naya can read your repos, open issues and pull requests, and run workflows. Reads are quiet; writes and deploys always need your explicit word first.',
      authority: 'Reads are quiet. Every write or deploy needs your word, each time.'
    },
    'DOOR-MCP': {
      tagline: 'Any provider\u2019s tools, one door.',
      plain: 'Connect tools from any MCP provider. What each tool may do is decided per use \u2014 the door discovers the tools, LAW decides the permissions.',
      authority: 'LAW plus the tool\u2019s own scope, decided per use.'
    },
    'DOOR-AI': {
      tagline: 'Agent to agent.',
      plain: 'One AI talking to another through the A2A protocol \u2014 context can move between minds so intelligence compounds. Authority never transfers.',
      authority: 'LAW governs scope and privacy; authority never crosses the door.'
    },
    'DOOR-DATA': {
      tagline: 'Your database, connected.',
      plain: 'Naya reads and writes your Supabase data through this door. Every consequential operation is decided by LAW before it runs.',
      authority: 'LAW decides each consequential operation, with your scope and grant.'
    },
    'DOOR-EMAIL': {
      tagline: 'Your inbox as a door.',
      plain: 'Naya can read and triage your email. Reading is quiet; sending anything always needs your word.',
      authority: 'Sending is consequential \u2014 LAW decides, you confirm.'
    },
    'DOOR-CALENDAR': {
      tagline: 'Your time, visible.',
      plain: 'Naya sees your calendar and understands your day. Changing anything on it needs your word.',
      authority: 'Changes are consequential \u2014 LAW decides, you confirm.'
    },
    'DOOR-VOICE': {
      tagline: 'Talk to Naya.',
      plain: 'Your voice as an interface \u2014 speak and be heard, hands-free. Your words stay yours.',
      authority: 'Privacy and scope govern every use.'
    },
    'DOOR-WEB': {
      tagline: 'The web, through Naya.',
      plain: 'Naya\u2019s browser as a door: reading pages is quiet; anything consequential needs your word first.',
      authority: 'LAW decides every consequential use.'
    },
    'DOOR-NAYA': {
      tagline: 'Naya to Naya.',
      plain: 'One Naya talking to another \u2014 context can move between minds so intelligence compounds. Authority never transfers.',
      authority: 'LAW governs scope and privacy; authority never crosses the door.'
    }
  };

  function copyFor(id){
    return DOOR_COPY[id] || { tagline:'A connection door.', plain:'A registered way for Naya to reach an outside service.', authority:'LAW decides permitted use.' };
  }

  /* color language: each door owns a stable color (keyed by door id, never by
     list index). Director palette 2026-10-02. Live doors burn in their color;
     doors in design rest white and ignite on hover. */
  var DOOR_COLORS = {
    'DOOR-GITHUB':   '#a371f7',  /* purple */
    'DOOR-MCP':      '#6366f1',  /* indigo blue */
    'DOOR-AI':       '#2f7bff',  /* sapphire blue — A2A */
    'DOOR-DATA':     '#22d3ee',  /* cyan (director correction 2026-10-02: cyan, not beige) */
    'DOOR-EMAIL':    '#a3e635',  /* lime green */
    'DOOR-CALENDAR': '#facc15',  /* yellow */
    'DOOR-VOICE':    '#d4a017',  /* gold */
    'DOOR-WEB':      '#fb923c',  /* orange */
    'DOOR-NAYA':     '#ef4444'   /* red */
  };

  /* each door's own jewel glyph */
  var DOOR_GLYPHS = {
    'DOOR-GITHUB':   '\u25C6',
    'DOOR-MCP':      '\u2B22',
    'DOOR-AI':       '\u2726',
    'DOOR-DATA':     '\u25C8',
    'DOOR-EMAIL':    '\u2709',
    'DOOR-CALENDAR': '\u25B2',
    'DOOR-VOICE':    '\u25CF',
    'DOOR-WEB':      '\u25A0',
    'DOOR-NAYA':     '\u2727'
  };

  /* display-name overrides. DOOR-AI presents as A2A per director 2026-10-02
     ("agent-to-agent — there's actually a real thing"); the canonical
     registry still records "AI Connect" until his A2A material lands. */
  var DOOR_NAMES = { 'DOOR-AI': 'A2A Connect' };

  function capLabel(c){
    return String(c||'').replace(/_/g,' ').toUpperCase();
  }

  function ConnectRoom(el, ctx){
    ctx = ctx || {};
    var doors = Array.isArray(ctx.doors) ? ctx.doors : [];
    var onConnect = (typeof ctx.onConnect==='function') ? ctx.onConnect : null;

    var stage = el('div','connect-stage');

    /* header */
    var head = el('header','cn-head');
    head.appendChild(el('p','cn-kicker','SMART CONNECT'));
    var h1 = el('h1','cn-title',''); h1.textContent = 'Doors into your NayaPOWER';
    head.appendChild(h1);
    var sub = el('p','cn-sub','');
    sub.textContent = 'A door is how Naya reaches the outside world \u2014 GitHub, your email, your data. Connecting a door never gives Naya authority: LAW decides what each door may do, every single time. Doors don\u2019t own your truth, memory, or identity.';
    head.appendChild(sub);
    stage.appendChild(head);

    /* honest status strip */
    var live = doors.filter(function(d){return d.statusKind==='live';}).length;
    var design = doors.length - live;
    var strip = el('div','cn-strip');
    var s1 = el('span','cn-count',''); s1.textContent = live + ' LIVE';
    var s2 = el('span','cn-count dim',''); s2.textContent = design + ' IN DESIGN';
    strip.appendChild(s1); strip.appendChild(s2);
    var note = el('span','cn-strip-note',''); note.textContent = 'Live doors connect today. Doors in design show their honest state \u2014 no fake buttons.';
    strip.appendChild(note);
    stage.appendChild(strip);

    /* door boards, registry order */
    var list = el('div','cn-list');
    doors.forEach(function(d){
      list.appendChild(doorBoard(el, d, onConnect));
    });
    stage.appendChild(list);

    /* footer law */
    var foot = el('footer','cn-foot','');
    foot.textContent = 'Door capability does not create authority. \u00B7 Canonical registry: BRAIN/10-INTERFACES/0002-SMART-DOOR-REGISTRY-V1.json';
    stage.appendChild(foot);

    return stage;
  }

  function doorBoard(el, d, onConnect){
    var copy = copyFor(d.id);
    var board = el('article','cn-door '+d.statusKind);
    var dispName = DOOR_NAMES[d.id] || d.name;
    /* the door's own stable color; design doors rest white and ignite on hover */
    board.style.setProperty('--door', DOOR_COLORS[d.id] || '#34d399');

    var top = el('div','cn-door-top');
    var gem = el('span','cn-gem','');
    var glyph = el('span','cn-gem-glyph',''); glyph.textContent = DOOR_GLYPHS[d.id] || '\u25C6';
    gem.appendChild(glyph);
    top.appendChild(gem);
    var nameWrap = el('div','cn-namewrap');
    var nm = el('h2','cn-name',''); nm.textContent = DOOR_NAMES[d.id] || d.name;
    nameWrap.appendChild(nm);
    var tag = el('p','cn-tagline',''); tag.textContent = copy.tagline;
    nameWrap.appendChild(tag);
    top.appendChild(nameWrap);
    var pill = el('span','cn-pill '+d.statusKind,''); pill.textContent = d.statusLabel;
    top.appendChild(pill);
    board.appendChild(top);

    var plain = el('p','cn-plain',''); plain.textContent = copy.plain;
    board.appendChild(plain);

    if(d.capabilities && d.capabilities.length){
      var caps = el('div','cn-caps');
      caps.appendChild(el('span','cn-caps-label','UNLOCKS'));
      d.capabilities.forEach(function(c){
        var ch = el('span','cn-cap',''); ch.textContent = capLabel(c); caps.appendChild(ch);
      });
      board.appendChild(caps);
    }

    var auth = el('p','cn-auth','');
    var ak = el('strong','',''); ak.textContent = 'Authority: ';
    auth.appendChild(ak);
    auth.appendChild(el('span','','')); auth.lastChild.textContent = copy.authority;
    board.appendChild(auth);

    var row = el('div','cn-actions');
    var btn = el('button','cn-connect'+(d.statusKind==='live'?' live':''), d.statusKind==='live' ? 'MANAGE CONNECTION' : 'CONNECT');
    btn.type = 'button';
    btn.setAttribute('aria-label', (d.statusKind==='live' ? 'Manage connection: ' : 'Connect: ') + dispName);
    btn.addEventListener('click', function(){
      /* dismiss any open notice on this board first */
      var old = board.querySelector('.cn-notice'); if(old) old.remove();
      if(onConnect){ onConnect(d.id); return; }
      /* honest inline state — never a fake connection */
      var n = el('div','cn-notice');
      var t = el('p','cn-notice-title',''); t.textContent = d.statusKind==='live' ? 'Connection manager' : 'Not yet wired';
      n.appendChild(t);
      var p = el('p','cn-notice-text','');
      p.textContent = d.statusKind==='live'
        ? 'This door is live in the registry. The Hub\u2019s connection manager will open here when the shell wires it \u2014 nothing was changed.'
        : 'The ' + dispName + ' door is registered in the Brain\u2019s door registry, but its connection flow is still being built. This button will start the real connection when the Hub wires it \u2014 nothing was changed.';
      n.appendChild(p);
      var x = el('button','cn-notice-close','GOT IT'); x.type='button';
      x.addEventListener('click', function(){ n.remove(); btn.focus(); });
      n.appendChild(x);
      row.appendChild(n);
      x.focus();
    });
    row.appendChild(btn);
    board.appendChild(row);

    return board;
  }

  window.NayaRooms = window.NayaRooms || {};
  window.NayaRooms.connect = ConnectRoom;
})();
