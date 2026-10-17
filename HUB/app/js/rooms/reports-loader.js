/* REPORTS LOADER — GitHub/Brain → adapter → room.
 *
 * The Hub shell calls this to populate `ctx.reports` before mounting the room:
 *
 *   const {reports, errors} = await ReportsLoader.loadDaily({from:'2026-09-27', to:'2026-10-02'});
 *   mount(window.NayaRooms.reports(el, {reports}));
 *
 * Sources are the canonical daily records:
 *   BRAIN/05-MEMORY/INTELLIGENCE-REPORTS/DAILY/YYYY/MM/DD/IB-DIR-NAYAPOWER-YYYYMMDD-001.md
 *
 * `base` defaults to a relative path (Hub served from the repo). Pass an
 * absolute base (e.g. a GitHub raw URL) when the Hub runs elsewhere.
 * Missing days are skipped and recorded in `errors` — never fatal.
 */
(function(){
  'use strict';

  function pad(n){ return String(n).padStart(2,'0'); }

  function dayPaths(dateKey){
    const [y,m,d]=dateKey.split('-').map(Number);
    const dir='BRAIN/05-MEMORY/INTELLIGENCE-REPORTS/DAILY/'+y+'/'+pad(m)+'/'+pad(d);
    const stem='IB-DIR-NAYAPOWER-'+y+pad(m)+pad(d)+'-001.md';
    return {dir:dir, file:dir+'/'+stem};
  }

  function eachDay(from,to){
    const out=[]; const a=new Date(from+'T00:00:00'); const b=new Date(to+'T00:00:00');
    for(let t=a; t<=b; t=new Date(t.getTime()+86400000)){
      out.push(t.getFullYear()+'-'+pad(t.getMonth()+1)+'-'+pad(t.getDate()));
    }
    return out;
  }

  async function fetchText(url){
    const res=await fetch(url,{headers:{'Accept':'text/plain'}});
    if(!res.ok) throw new Error('HTTP '+res.status+' for '+url);
    return await res.text();
  }

  async function loadDaily(opts){
    opts=opts||{};
    const base=(opts.base||'').replace(/\/+$/,'');
    const days=eachDay(opts.from||'2026-09-27', opts.to||new Date().toISOString().slice(0,10));
    const reports=[], errors=[];
    for(const dk of days){
      const p=dayPaths(dk);
      const url=(base?base+'/':'')+p.file;
      try{
        const md=await fetchText(url);
        const parsed=window.ReportsAdapter.parse(md);
        if(parsed && parsed.id && parsed.id!=='UNKNOWN') reports.push(parsed);
        else errors.push({day:dk, reason:'unparseable'});
      }catch(e){
        errors.push({day:dk, reason:String(e&&e.message||e)});
      }
    }
    /* newest first, mechanical */
    reports.sort((a,b)=>String(b.dateKey||'').localeCompare(String(a.dateKey||'')));
    return {reports:reports, errors:errors};
  }

  window.ReportsLoader={loadDaily:loadDaily, dayPaths:dayPaths};
})();
