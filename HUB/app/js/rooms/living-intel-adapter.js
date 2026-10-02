/* LIVING INTEL ADAPTER — every living source -> one heartbeat stream.
 *
 * Sources: canonical intelligence reports, smart notes, the smart ledger,
 * and the smart-door registry. Projection only — never invention. Demo
 * ledger entries arrive labeled demo:true and keep that label here.
 *
 * THE FLOW: the stream flows through the natural color spectrum —
 * purple -> indigo -> cyan -> forest -> lime -> yellow -> gold ->
 * orange -> red -> magenta -> back to purple, continuously. The room
 * assigns flow colors by visible position; sources keep their identity
 * colors in the legend.
 *
 *   const items = LivingIntelAdapter.build({reports, notes, doors, ledger});
 *   // -> [{source, color, jewel, ts, title, nutshell, meta, demo,
 *   //      stats:[[label,value]], graph:{kind,...}|null, explain}]
 *   sorted newest-first.
 */
(function(){
  'use strict';

  /* the natural flow, director-stated 2026-10-02 */
  var FLOW = ['#a855f7','#6366f1','#22d3ee','#16a34a','#a3e635',
              '#facc15','#d4a017','#fb923c','#ef4444','#ec4899'];

  var COLORS = {
    report:  '#38bdf8',
    note:    '#c084fc',
    ledger:  '#d4a017',
    connect: '#6366f1'
  };
  var JEWELS = { report:'\u25C8', note:'\u2726', ledger:'\u25C6', connect:'\u25C9' };

  var EXPLAIN = {
    report: 'A canonical daily intelligence record \u2014 the durable memory of that day, written to the Brain. The report is the memory artifact; the Hub event is the signal that something new became available.',
    note: 'A Smart Note \u2014 distilled intelligence captured for cold successors. It lands as a CANDIDATE; only Shawn ratifies it into canonical truth.',
    ledger: 'A ledger receipt \u2014 proof that an action happened: what the decision math said, what authority allowed it, and what was actually observed.',
    connect: 'A smart door \u2014 a capability boundary. Capability does not create authority: LAW decides every use, ACT invokes it, VERIFY checks the result.'
  };

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
        meta: 'BRAIN/05-MEMORY/INTELLIGENCE-REPORTS', demo:false,
        stats: [['Sections', r.sections||'\u2014'], ['Words', r.words||'\u2014']],
        graph: (r.sections && r.words)
          ? {kind:'bars', bars:[['Sections', r.sections, 12], ['Words \u00F7 100', Math.round(r.words/100), 60]]}
          : null,
        explain: EXPLAIN.report
      });
    });

    (packs.notes||[]).forEach(function(n){
      items.push({
        source:'note', color:COLORS.note, jewel:JEWELS.note,
        ts: tsOf(n.date, '10:00:00'),
        title: n.title,
        nutshell: n.nutshell || '',
        meta: (n.truth||'CANDIDATE') + ' \u00B7 SMART-NOTE',
        demo:false,
        stats: [['Truth', n.truth||'CANDIDATE'], ['Words', n.words||'\u2014']],
        graph: null,
        explain: EXPLAIN.note
      });
    });

    (packs.doors||[]).forEach(function(d){
      var live = /LIVE|BOUNDED/.test(String(d.status).toUpperCase());
      var caps = (d.capabilities||[]).slice(0,6).join(', ');
      items.push({
        source:'connect', color:d.color||COLORS.connect, jewel:d.jewel||JEWELS.connect,
        ts: Date.now() - (live ? 1000*60*14 : 1000*60*60*5),
        title: d.name + (live ? ' \u2014 live' : ' \u2014 in design'),
        nutshell: live
          ? 'Bounded live connection. Capability is live; LAW still decides every use.'
          : 'Registered contract. The door exists on paper; the wire comes later.',
        meta: String(d.status||'').replace(/_/g,' '),
        demo:false,
        stats: [['Status', String(d.status||'').replace(/_/g,' ')],
                ['Capabilities', (d.capabilities||[]).length]],
        graph: null,
        explain: EXPLAIN.connect + (caps ? ' This door\u2019s capabilities: ' + caps + '.' : '')
      });
    });

    (packs.ledger||[]).forEach(function(e){
      var dv = e.scores && e.scores.deltaV;
      var q = e.scores && e.scores.q;
      var cf = e.scores && e.scores.confidence;
      var vP = e.scores && e.scores.vPred;
      var vA = e.scores && e.scores.vActual;
      var stats = [['Outcome', e.outcome]];
      if(q!=null) stats.push(['Q', q.toFixed(1)]);
      if(dv!=null) stats.push(['\u0394V', (dv>0?'+':'')+dv]);
      if(cf!=null) stats.push(['Confidence', cf.toFixed(2)]);
      stats.push(['Proof', e.proofState]);
      var graph = null;
      if(vP!=null && vA!=null){
        graph = {kind:'spark', points:[vP, vA], labels:['predicted','observed']};
      } else if(q!=null){
        graph = {kind:'bars', bars:[['Q', q, 10], ['Confidence', cf*10, 10]]};
      }
      items.push({
        source:'ledger', color:COLORS.ledger, jewel:'\u25C6',
        ts: new Date(e.issuedAt).getTime() || Date.now(),
        title: e.glyph + ' ' + e.smartName + ' \u00B7 ' + e.outcome,
        nutshell: e.effectsObserved
          || (dv!=null ? ('\u0394V ' + (dv>0?'+':'') + dv) : '')
          || String(e.kind||'').toUpperCase(),
        meta: 'smart id \u00B7 ' + String(e.hash||'').slice(0,10) + '\u2026',
        demo: !!e.demo,
        stats: stats, graph: graph, explain: EXPLAIN.ledger
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

  window.LivingIntelAdapter = { build:build, COLORS:COLORS, FLOW:FLOW };
})();
