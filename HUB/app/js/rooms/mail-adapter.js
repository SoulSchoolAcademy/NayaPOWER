/* SMART MAIL ADAPTER — raw messages → conversation threads.
 *
 * There is no canonical mail store; seeded messages are DEMO content for
 * design review (director-authorized demo policy) and always carry
 * demo:true through this adapter. The Hub is a projection surface; the
 * adapter never invents messages — unparseable entries are skipped.
 *
 * Raw message:
 *   {id, threadId?, from, to, toKind:'person'|'space', subject, body,
 *    ts, unread, demo}
 * Thread:
 *   {id, subject, messages:[message...] (oldest first),
 *    ts (last activity), unread (any message unread),
 *    demo (every message demo), count}
 * Messages without a threadId each become a single-message thread.
 * Threads sort newest-activity-first.
 */
(function(){
  'use strict';

  function isStr(v){ return typeof v==='string' && v.length>0; }

  function parseOne(m){
    if(!m || typeof m!=='object') return null;
    if(!isStr(m.id) || !isStr(m.from) || !isStr(m.to) || !isStr(m.subject)) return null;
    var ts = m.ts;
    if(typeof ts!=='number' || !isFinite(ts)) ts = Date.now();
    return {
      id: m.id,
      threadId: isStr(m.threadId) ? m.threadId : null,
      from: m.from,
      to: m.to,
      toKind: m.toKind==='space' ? 'space' : 'person',
      subject: m.subject,
      snippet: String(m.body||'').split('\n')[0].slice(0,120),
      body: isStr(m.body) ? m.body : '',
      ts: ts,
      unread: m.unread===true,
      demo: m.demo!==false   /* seeded content is demo unless explicitly real */
    };
  }

  function parseThreads(raw){
    var msgs = [];
    (Array.isArray(raw) ? raw : []).forEach(function(m){
      try{ var e = parseOne(m); if(e) msgs.push(e); }catch(err){ /* skip */ }
    });
    msgs.sort(function(a,b){ return a.ts - b.ts; });

    var byTid = {}, order = [];
    msgs.forEach(function(m){
      var tid = m.threadId || ('t-'+m.id);
      if(!byTid[tid]){ byTid[tid] = []; order.push(tid); }
      byTid[tid].push(m);
    });

    var threads = order.map(function(tid){
      var ms = byTid[tid];
      var last = ms[ms.length-1];
      return {
        id: tid,
        subject: ms[0].subject,
        messages: ms,
        count: ms.length,
        ts: last.ts,
        unread: ms.some(function(m){ return m.unread; }),
        demo: ms.every(function(m){ return m.demo; })
      };
    });
    threads.sort(function(a,b){ return b.ts - a.ts; });
    return threads;
  }

  window.MailAdapter = { parseThreads: parseThreads };
})();
