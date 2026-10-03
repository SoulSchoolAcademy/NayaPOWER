/* INTELLIGENT LIBRARY — adapter: parse + seed canonical references.
   The Library shelves REFERENCES, never copies. Every object below is a
   reference to a canonical Brain object (real ones) or a clearly-labeled
   DEMO illustration. "N REFERENCES · 0 COPIES" is computed, not written.
   Load before library.js. */
(function(){
  'use strict';

  var KINDS = [
    {id:'notes',      name:'Smart Notes'},
    {id:'discoveries',name:'Discoveries'},
    {id:'learning',   name:'Learning'},
    {id:'decisions',  name:'Decisions'},
    {id:'reports',    name:'Reports'},
    {id:'activity',   name:'Activity'}
  ];

  /* Real canonical objects (Brain). demo:false = genuine reference. */
  var REAL = [
    {id:'SN-016', kind:'notes', stream:'BRAIN · SMART NOTES',
     title:'Prime Judgment Rule — Judgment Before Blind Obedience',
     excerpt:'Obedience without judgment is abdication. An instruction is an input to judgment, not proof the instructed action is right.',
     truth:'RATIFIED', demo:false,
     provenance:{source:'Shawn, 2026-09-30 — ratified as Prime Operating Law 1',
                 evidence:'~/workspace/your_files/the-judgment-rule-2026-09-30.md',
                 status:'RATIFIED — constitutional-adjacent law', supersededBy:null}},
    {id:'SN-017', kind:'notes', stream:'BRAIN · SMART NOTES',
     title:'Asserted Is Not Verified',
     excerpt:'A builder claiming "done" is not evidence. UNKNOWN, BLOCKED and IMPLEMENTED never count as VERIFIED or PASS.',
     truth:'CANDIDATE', demo:false,
     provenance:{source:'Naya 4 auto-capture, 2026-09-30 — draft PR #1229',
                 evidence:'BRAIN/04-INTELLIGENCE/SMART-NOTES/2026/09/30/',
                 status:'CANDIDATE — awaiting Shawn ratification', supersededBy:null}},
    {id:'SN-217', kind:'notes', stream:'BRAIN · SMART NOTES',
     title:'Compare Semantic Identity, Not Raw Bytes',
     excerpt:'Independently regenerated index artifacts may differ only by generated timestamps; verify with the tool\u2019s semantic normalizers, not raw blob equality.',
     truth:'CANDIDATE', demo:false,
     provenance:{source:'Night-shift distillation, 2026-10-02 — staged on naya4/smart-notes-2026-09-30 @ 0c395f1c',
                 evidence:'Draft PR #1229', status:'CANDIDATE — awaiting Shawn ratification', supersededBy:null}},
    {id:'IB-006', kind:'discoveries', stream:'BRAIN · INTELLIGENT BLOCKS',
     title:'Freeze-and-Extend Protocol',
     excerpt:'The working answer to the AI app-interface build problem: freeze the proven foundation, extend behind the seam — never rebuild the foundation per attempt.',
     truth:'CANDIDATE', demo:false,
     provenance:{source:'North-Star deep dive, 2026-10-01 — Shawn: "this is the most valuable thing I could possibly do"',
                 evidence:'BRAIN/04-INTELLIGENCE/INTELLIGENT-BLOCKS/', status:'CANDIDATE working answer', supersededBy:null}},
    {id:'DEC-6TO10', kind:'decisions', stream:'TEAM NAYA · DIRECTIVES',
     title:'The 6→10 Doctrine',
     excerpt:'Before acting: will it wreck anything? Is it reversible? Risk vs reward? Clear 6→10 with no plausible path to 3 — act. Plausible 6→3 or uncertain — ask.',
     truth:'DIRECTOR-STATED', demo:false,
     provenance:{source:'Shawn, 2026-09-30 — director-stated decision procedure',
                 evidence:'~/workspace/your_files/smart-note-6-to-10-doctrine-2026-09-30.md (IB-OP-001)',
                 status:'Standing operating doctrine', supersededBy:null}}
  ];

  /* DEMO illustrations so every shelf has a shape to show. Plainly labeled. */
  var DEMO = [
    {id:'DEMO-LN-01', kind:'learning', stream:'DEMO · LEARNING',
     title:'Board congruence: carry the full flow, not the summary color',
     excerpt:'The unsupervised batch broke congruence once on Smart List — mostly-green boards where the full flow belonged. Drilled laws now travel with every build.',
     truth:'DEMO', demo:true,
     provenance:{source:'Demo illustration', evidence:'—', status:'Illustrative only', supersededBy:null}},
    {id:'DEMO-RP-01', kind:'reports', stream:'DEMO · REPORTS',
     title:'Nightly build verification — six rooms green',
     excerpt:'Illustrative report shape: what was built, exact branch/commit/PR/test counts, candidate vs verified vs merged vs deployed.',
     truth:'DEMO', demo:true,
     provenance:{source:'Demo illustration', evidence:'—', status:'Illustrative only', supersededBy:null}},
    {id:'DEMO-AC-01', kind:'activity', stream:'DEMO · ACTIVITY',
     title:'Hub shell integration proof captured',
     excerpt:'CDP-verified: rail renders 11 tabs; Spaces and Mail mount full-bleed through the shell adapter.',
     truth:'DEMO', demo:true,
     provenance:{source:'Demo illustration', evidence:'—', status:'Illustrative only', supersededBy:null}}
  ];

  function isStr(x){ return typeof x === 'string'; }

  function parseOne(o){
    if(!o || typeof o !== 'object') return null;
    if(!isStr(o.id) || !isStr(o.title)) return null;
    var kindOk = KINDS.some(function(k){ return k.id === o.kind; });
    return {
      id: o.id,
      kind: kindOk ? o.kind : 'notes',
      stream: isStr(o.stream) ? o.stream : '',
      title: o.title,
      excerpt: isStr(o.excerpt) ? o.excerpt : '',
      truth: isStr(o.truth) ? o.truth : 'CANDIDATE',
      demo: !!o.demo,
      provenance: o.provenance && typeof o.provenance === 'object' ? {
        source: isStr(o.provenance.source) ? o.provenance.source : '—',
        evidence: isStr(o.provenance.evidence) ? o.provenance.evidence : '—',
        status: isStr(o.provenance.status) ? o.provenance.status : '—',
        supersededBy: isStr(o.provenance.supersededBy) ? o.provenance.supersededBy : null
      } : {source:'—', evidence:'—', status:'—', supersededBy:null}
    };
  }

  function parseMany(raw){
    var out = [];
    (Array.isArray(raw) ? raw : []).forEach(function(o){
      try{ var p = parseOne(o); if(p) out.push(p); }catch(e){/* skip */}
    });
    return out;
  }

  /* Exact canonical-ID resolution: the primary path. Returns the object or null. */
  function resolveId(objects, query){
    var q = String(query || '').trim().toUpperCase();
    if(!q) return null;
    for(var i = 0; i < objects.length; i++){
      if(String(objects[i].id).toUpperCase() === q) return objects[i];
    }
    /* tolerant: allow "SN217" or "sn-217" prefix forms */
    var compact = q.replace(/[^A-Z0-9]/g, '');
    for(var j = 0; j < objects.length; j++){
      if(String(objects[j].id).toUpperCase().replace(/[^A-Z0-9]/g, '') === compact) return objects[j];
    }
    return null;
  }

  function search(objects, query){
    var q = String(query || '').trim().toLowerCase();
    if(!q) return objects.slice();
    return objects.filter(function(o){
      return o.title.toLowerCase().indexOf(q) !== -1 ||
             o.excerpt.toLowerCase().indexOf(q) !== -1 ||
             String(o.id).toLowerCase().indexOf(q) !== -1;
    });
  }

  window.LibraryAdapter = {
    KINDS: KINDS,
    REAL: REAL,
    DEMO: DEMO,
    parseOne: parseOne,
    parseMany: parseMany,
    resolveId: resolveId,
    search: search
  };
})();
