/* SMART MAIL ADAPTER — raw thread payloads → mail thread view-models.
 *
 * There is no canonical mail store; seeded threads are DEMO content for
 * design review (director-authorized demo policy) and always carry
 * demo:true through this adapter. The Hub is a projection surface; the
 * adapter never invents threads — unparseable entries are skipped.
 *
 *   const threads = MailAdapter.parseThreads(raw);
 *   // -> [{id, from, to, toKind:'person'|'space', subject, snippet, body,
 *   //      ts, unread, demo}], newest first.
 */
(function(){
  'use strict';

  function isStr(v){ return typeof v==='string' && v.length>0; }

  function parseOne(t){
    if(!t || typeof t!=='object') return null;
    if(!isStr(t.id) || !isStr(t.from) || !isStr(t.to) || !isStr(t.subject)) return null;
    var ts = t.ts;
    if(typeof ts!=='number' || !isFinite(ts)) ts = Date.now();
    return {
      id: t.id,
      from: t.from,
      to: t.to,
      toKind: t.toKind==='space' ? 'space' : 'person',
      subject: t.subject,
      snippet: isStr(t.snippet) ? t.snippet : String(t.body||'').slice(0,120),
      body: isStr(t.body) ? t.body : '',
      ts: ts,
      unread: t.unread===true,
      demo: t.demo!==false   /* seeded content is demo unless explicitly real */
    };
  }

  function parseThreads(raw){
    var list = Array.isArray(raw) ? raw : [];
    var out = [];
    list.forEach(function(t){
      try{ var e=parseOne(t); if(e) out.push(e); }catch(err){ /* skip */ }
    });
    out.sort(function(a,b){ return b.ts - a.ts; });
    return out;
  }

  window.MailAdapter = { parseThreads: parseThreads };
})();
