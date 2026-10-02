/* LIVING INTEL ADAPTER — every living source -> one heartbeat stream.
 *
 * Sources: canonical intelligence reports, smart notes, the smart ledger,
 * and the smart-door registry. Projection only — never invention. Demo
 * ledger entries arrive labeled demo:true and keep that label here.
 *
 *   const items = LivingIntelAdapter.build({reports, notes, doors, ledger});
 *   // -> [{source, color, jewel, ts, title, nutshell, meta, demo}]
 *   sorted newest-first.
 */
(function(){
  'use strict';

  var COLORS = {
    report:  '#38bdf8',
    note:    '#c084fc',
    ledger:  '#d4a017',
    connect: '#6366f1'
  };
  var JEWELS = { report:'\u25C8', note:'\u2726', ledger:'\u25C6', connect:'\u25C9' };
  var LABELS = { report:'INTEL REPORT', note:'SMART NOTE', ledger:'LEDGER', connect:'CONNECT' };

  function tsOf(dateStr, hour){
    var d = new Date(dateStr + 'T' + (hour||'12:00:00'));
    return isNaN(d) ? Date.now() : d.getTime();
  }

  function build(packs){
    packs = packs || {};
    var items = [];

    (packs.reports||[]).forEach(function(r){
      items.push({
        source:'report', color:COLORS.report, jewel:JEWELS.report,
        ts: tsOf(r.date, '08:00:00'),
        title: 'Daily Intelligence \u2014 ' + prettyDate(r.date),
        nutshell: r.nutshell || 'The day\u2019s canonical intelligence record.',
        meta: 'BRAIN/05-MEMORY/INTELLIGENCE-REPORTS', demo:false
      });
    });

    (packs.notes||[]).forEach(function(n){
      items.push({
        source:'note', color:COLORS.note, jewel:JEWELS.note,
        ts: tsOf(n.date, '10:00:00'),
        title: n.title,
        nutshell: n.nutshell || '',
        meta: (n.truth||'CANDIDATE') + ' \u00B7 SMART-NOTE',
        demo:false
      });
    });

    (packs.doors||[]).forEach(function(d){
      var live = /LIVE|BOUNDED/.test(String(d.status).toUpperCase());
      items.push({
        source:'connect', color:d.color||COLORS.connect, jewel:d.jewel||JEWELS.connect,
        ts: Date.now() - (live ? 1000*60*14 : 1000*60*60*5),
        title: d.name + (live ? ' \u2014 live' : ' \u2014 in design'),
        nutshell: live
          ? 'Bounded live connection. Capability is live; LAW still decides every use.'
          : 'Registered contract. The door exists on paper; the wire comes later.',
        meta: String(d.status||'').replace(/_/g,' '),
        demo:false
      });
    });

    (packs.ledger||[]).forEach(function(e){
      var dv = e.scores && e.scores.deltaV;
      items.push({
        source:'ledger', color:COLORS.ledger, jewel:'\u25C6',
        ts: new Date(e.issuedAt).getTime() || Date.now(),
        title: e.glyph + ' ' + e.smartName + ' \u00B7 ' + e.outcome,
        nutshell: e.effectsObserved
          || (dv!=null ? ('\u0394V ' + (dv>0?'+':'') + dv) : '')
          || String(e.kind||'').toUpperCase(),
        meta: 'smart id \u00B7 ' + String(e.hash||'').slice(0,10) + '\u2026',
        demo: !!e.demo
      });
    });

    items.sort(function(a,b){ return b.ts - a.ts; });
    return items;
  }

  function prettyDate(iso){
    var d = new Date(iso + 'T12:00:00');
    if(isNaN(d)) return iso;
    return d.toLocaleDateString('en-US',{month:'long',day:'numeric'});
  }

  window.LivingIntelAdapter = { build:build, COLORS:COLORS, LABELS:LABELS };
})();
