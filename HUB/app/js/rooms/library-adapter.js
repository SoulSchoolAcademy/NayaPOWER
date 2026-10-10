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
    {id:'SN-016', kind:'notes', area:'governance', stream:'BRAIN · SMART NOTES',
     title:'Prime Judgment Rule — Judgment Before Blind Obedience',
     excerpt:'Obedience without judgment is abdication. An instruction is an input to judgment, not proof the instructed action is right.',
     truth:'RATIFIED', demo:false,
     provenance:{source:'Shawn, 2026-09-30 — ratified as Prime Operating Law 1',
                 evidence:'~/workspace/your_files/the-judgment-rule-2026-09-30.md',
                 status:'RATIFIED — constitutional-adjacent law', supersededBy:null}},
    {id:'SN-017', kind:'notes', area:'build', stream:'BRAIN · SMART NOTES',
     title:'Asserted Is Not Verified',
     excerpt:'A builder claiming "done" is not evidence. UNKNOWN, BLOCKED and IMPLEMENTED never count as VERIFIED or PASS.',
     truth:'CANDIDATE', demo:false,
     provenance:{source:'Naya 4 auto-capture, 2026-09-30 — draft PR #1229',
                 evidence:'BRAIN/04-INTELLIGENCE/SMART-NOTES/2026/09/30/',
                 status:'CANDIDATE — awaiting Shawn ratification', supersededBy:null}},
    {id:'SN-217', kind:'notes', area:'build', stream:'BRAIN · SMART NOTES',
     title:'Compare Semantic Identity, Not Raw Bytes',
     excerpt:'Independently regenerated index artifacts may differ only by generated timestamps; verify with the tool\u2019s semantic normalizers, not raw blob equality.',
     truth:'CANDIDATE', demo:false,
     provenance:{source:'Night-shift distillation, 2026-10-02 — staged on naya4/smart-notes-2026-09-30 @ 0c395f1c',
                 evidence:'Draft PR #1229', status:'CANDIDATE — awaiting Shawn ratification', supersededBy:null}},
    {id:'IB-006', kind:'discoveries', area:'build', stream:'BRAIN · INTELLIGENT BLOCKS',
     title:'Freeze-and-Extend Protocol',
     excerpt:'The working answer to the AI app-interface build problem: freeze the proven foundation, extend behind the seam — never rebuild the foundation per attempt.',
     truth:'CANDIDATE', demo:false,
     provenance:{source:'North-Star deep dive, 2026-10-01 — Shawn: "this is the most valuable thing I could possibly do"',
                 evidence:'BRAIN/04-INTELLIGENCE/INTELLIGENT-BLOCKS/', status:'CANDIDATE working answer', supersededBy:null}},
    {id:'DEC-6TO10', kind:'decisions', area:'governance', stream:'TEAM NAYA · DIRECTIVES',
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
      area: isStr(o.area) ? o.area : null,
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

  var STOP = {what:1,how:1,why:1,when:1,where:1,who:1,which:1,whom:1,whose:1,
    the:1,a:1,an:1,is:1,are:1,was:1,were:1,be:1,been:1,do:1,does:1,did:1,
    can:1,could:1,should:1,would:1,will:1,of:1,to:1,in:1,on:1,for:1,with:1,
    and:1,or:1,my:1,your:1,it:1,its:1,this:1,that:1,there:1,here:1,by:1,
    from:1,about:1,into:1,over:1,me:1,i:1,all:1,any:1};

  function terms(query){
    return String(query || '').toLowerCase().replace(/[^a-z0-9\s-]/g, ' ')
      .split(/[\s-]+/).filter(function(t){ return t.length > 1 && !STOP[t]; });
  }

  function isQuestion(query){
    var q = String(query || '').trim().toLowerCase();
    if(/\?$/.test(q)) return true;
    return /^(who|what|where|when|why|how|which|can|does|do|is|are|should|tell me)\b/.test(q);
  }

  /* Relevance-ranked search for the Q&A job: ID match first, then title,
     excerpt, stream/area term overlap. Returns [{obj, score}] sorted desc. */
  function rank(objects, query){
    var ts = terms(query);
    var out = [];
    objects.forEach(function(o){
      var score = 0;
      var idU = String(o.id).toUpperCase();
      var qU = String(query || '').trim().toUpperCase();
      if(qU && idU === qU) score += 100;
      else if(qU && idU.indexOf(qU) !== -1 && qU.length > 2) score += 50;
      var title = o.title.toLowerCase(), ex = o.excerpt.toLowerCase();
      var hay = (o.stream + ' ' + (o.area || '')).toLowerCase();
      ts.forEach(function(t){
        if(title.indexOf(t) !== -1) score += 10;
        else if(ex.indexOf(t) !== -1) score += 5;
        if(hay.indexOf(t) !== -1) score += 3;
      });
      if(score > 0) out.push({obj:o, score:score});
    });
    out.sort(function(a,b){ return b.score - a.score; });
    return out;
  }

  function search(objects, query){
    var q = String(query || '').trim().toLowerCase();
    if(!q) return objects.slice();
    return rank(objects, query).map(function(r){ return r.obj; });
  }

  /* Major areas of NayaPOWER — the browse strip. Every object carries one. */
  var AREAS = [
    {id:'nodes',      name:'Nine nodes'},
    {id:'rooms',      name:'Hub rooms'},
    {id:'nayanet',    name:'NayaNET'},
    {id:'governance', name:'Governance'},
    {id:'organism',   name:'One organism'},
    {id:'build',      name:'Build practice'}
  ];

  /* Proposed Q&A corpus (DEMO-labeled seeds). The real corpus gets written
     as Brain Smart Notes / Intelligent Blocks through the smart-note
     pipeline (CANDIDATE, Shawn ratifies) — these seeds show the shape. */
  var QA_SEEDS = [
    {id:'QA-NODES-01', kind:'notes', area:'nodes', stream:'Q&A · NINE NODES',
     title:'What are the nine nodes?',
     excerpt:'SELF, LAW, ACT, KNOW, PROVE, CONNECT, VERIFY, LEARN, EVOLVE — the nine-node kernel is the living mind: identity, law, action, knowledge, proof, connection, verification, learning, and evolution, invoked in sequence with per-node receipts.',
     truth:'DEMO', demo:true,
     provenance:{source:'Proposed Q&A seed — from the nine-node kernel spec (CANDIDATE)',
                 evidence:'BRAIN/00-SPEC/0001-INTELLIGENT-GRAPH-AND-TREE-SPEC-V1.md',
                 status:'Proposed — needs a real Brain note', supersededBy:null}},
    {id:'QA-ORGANISM-01', kind:'notes', area:'organism', stream:'Q&A · ONE ORGANISM',
     title:'How do Smart Mail, Connections, Spaces and Lists fit together?',
     excerpt:'They are parts of each other — one graph, four views. Connections is the people spine, Mail is the voice, Spaces are the gatherings, Lists are the memory. A mail to a space IS a post in that space: same object, two views.',
     truth:'DEMO', demo:true,
     provenance:{source:'Proposed Q&A seed — from Shawn\u2019s 2026-10-02 organism ruling',
                 evidence:'MEMORY.md — Hub room integration vision', status:'Proposed — needs a real Brain note', supersededBy:null}},
    {id:'QA-SPACES-01', kind:'notes', area:'rooms', stream:'Q&A · HUB ROOMS',
     title:'What is a Smart Space?',
     excerpt:'A social connection group organized around intelligence. Any two or more people gather around any subject, an Intelligent Block, a Smart Note, or a feed topic — instant chat, post to the group, mail the whole space, add people.',
     truth:'DEMO', demo:true,
     provenance:{source:'Proposed Q&A seed — from Shawn\u2019s 2026-10-02 product definition',
                 evidence:'Smart Spaces v4 room', status:'Proposed — needs a real Brain note', supersededBy:null}},
    {id:'QA-NAYANET-01', kind:'notes', area:'nayanet', stream:'Q&A · NAYANET',
     title:'What is NayaNET?',
     excerpt:'The governed intelligence network NayaPOWER connects to — one brain, many doors. The Hub is the human cockpit; NayaNET is the network it bridges into.',
     truth:'DEMO', demo:true,
     provenance:{source:'Proposed Q&A seed', evidence:'HUB/NAYANET-SMART-APP-ROOMS-V1.json',
                 status:'Proposed — needs a real Brain note', supersededBy:null}},
    {id:'QA-HUB-01', kind:'notes', area:'rooms', stream:'Q&A · HUB ROOMS',
     title:'What is the Hub?',
     excerpt:'The human cockpit for NayaPOWER — not the source of truth, the projection surface. Eleven rooms: Feed, Today, Reports, Library, Connect, Ledger, Connections, Lists, Mail, Spaces, Settings.',
     truth:'DEMO', demo:true,
     provenance:{source:'Proposed Q&A seed', evidence:'HUB/NAYANET-SMART-APP-ROOM-SPEC-V1.md',
                 status:'Proposed — needs a real Brain note', supersededBy:null}},
    {id:'QA-PRIVACY-01', kind:'notes', area:'governance', stream:'Q&A · GOVERNANCE',
     title:'How is my privacy protected?',
     excerpt:'Private by default. Shared by choice. Collective by consent. Public by decision. Capability never creates authority — the human director is the final authority on what leaves the vault.',
     truth:'DEMO', demo:true,
     provenance:{source:'Proposed Q&A seed — from the activation constitution',
                 evidence:'NAYA-ACTIVATION/CONSTITUTION/', status:'Proposed — needs a real Brain note', supersededBy:null}},
    {id:'QA-BUILD-01', kind:'notes', area:'build', stream:'Q&A · BUILD PRACTICE',
     title:'What does "asserted is not verified" mean in practice?',
     excerpt:'A green-looking document, commit, or test is not proof of the larger claim. UNKNOWN, BLOCKED and IMPLEMENTED never count as VERIFIED or PASS — and VERIFIED is not PRODUCTION-PROVEN.',
     truth:'DEMO', demo:true,
     provenance:{source:'Proposed Q&A seed — see the real SN-017', evidence:'Draft PR #1229',
                 status:'Proposed — the real note is SN-017', supersededBy:null}}
  ];

  function byArea(objects, areaId){
    return objects.filter(function(o){ return o.area === areaId; });
  }

  window.LibraryAdapter = {
    KINDS: KINDS,
    AREAS: AREAS,
    REAL: REAL,
    DEMO: DEMO,
    QA_SEEDS: QA_SEEDS,
    parseOne: parseOne,
    parseMany: parseMany,
    resolveId: resolveId,
    search: search,
    rank: rank,
    terms: terms,
    isQuestion: isQuestion,
    byArea: byArea
  };
})();
