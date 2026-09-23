const REPORT_REPO='SoulSchoolAcademy/NayaPOWER';
const SUPABASE_URL='https://dahisasgpfvziswqvmvm.supabase.co';
const SUPABASE_KEY='sb_publishable_oQFKOYFuJ9bT-E9QkJUb4g_lAUyInue';
const REPORT_ROOT='NAYA/REPORTS/DAILY/2026/09';
const REPORT_PATH=(date)=>REPORT_ROOT+'/'+date+'.md';
const REPORT_API=(date)=>'https://api.github.com/repos/'+REPORT_REPO+'/contents/'+REPORT_PATH(date)+'?ref=main';

async function sha256Hex(value){
  const bytes=new TextEncoder().encode(value);
  const digest=await crypto.subtle.digest('SHA-256',bytes);
  return [...new Uint8Array(digest)].map(b=>b.toString(16).padStart(2,'0')).join('');
}

async function dailyReport(request,url){
  const auth=request.headers.get('Authorization')||'';
  if(!/^Bearer\s+\S+$/i.test(auth))return new Response(JSON.stringify({ok:false,error:'AUTH_REQUIRED'}),{status:401,headers:{'content-type':'application/json','cache-control':'no-store'}});
  const authCheck=await fetch(SUPABASE_URL+'/auth/v1/user',{headers:{'apikey':SUPABASE_KEY,'Authorization':auth}});
  if(!authCheck.ok)return new Response(JSON.stringify({ok:false,error:'AUTH_INVALID'}),{status:401,headers:{'content-type':'application/json','cache-control':'no-store'}});
  const actor=await authCheck.json();
  const match=url.pathname.match(/^\/api\/reports\/daily\/(\d{4}-\d{2}-\d{2})$/);
  if(!match)return new Response(JSON.stringify({ok:false,error:'INVALID_REPORT_PATH'}),{status:400,headers:{'content-type':'application/json','cache-control':'no-store'}});
  const date=match[1],path=REPORT_PATH(date);
  const gh=await fetch(REPORT_API(date),{headers:{'Accept':'application/vnd.github+json','User-Agent':'NayaNET-Intelligence-Hub-Report-Gateway'}});
  if(!gh.ok)return new Response(JSON.stringify({ok:false,error:'CANONICAL_REPORT_UNAVAILABLE',date,path,source_ref:'main',github_status:gh.status}),{status:gh.status===404?404:502,headers:{'content-type':'application/json','cache-control':'no-store'}});
  const meta=await gh.json();
  if(meta.type!=='file'||typeof meta.content!=='string')return new Response(JSON.stringify({ok:false,error:'CANONICAL_REPORT_INVALID',date,path}),{status:502,headers:{'content-type':'application/json','cache-control':'no-store'}});
  const content=atob(meta.content.replace(/\s/g,''));
  const hash=await sha256Hex(content);
  const payload={ok:true,schema:'NAYANET_DAILY_REPORT_RETRIEVAL_V1',report_id:'DIR-'+date,report_type:'DAILY',report_date:date,source:{repository:REPORT_REPO,path,ref:'main',blob_sha:meta.sha||null,source_url:meta.html_url||null},provenance:{retrieved_by:'nayanet-canonical-report-gateway',actor_user_id:actor?.id||null,retrieved_at:new Date().toISOString(),content_sha256:hash,authority:'CANONICAL_MAIN'},content};
  return new Response(JSON.stringify(payload),{status:200,headers:{'content-type':'application/json; charset=utf-8','cache-control':'no-store, no-cache, must-revalidate, max-age=0','x-naya-report-authority':'CANONICAL_MAIN','x-naya-report-path':path,'x-naya-report-sha256':hash}});
}

export default {
  async fetch(request, env) {
    const url=new URL(request.url);
    if(url.pathname.startsWith('/api/reports/daily/'))return dailyReport(request,url);
    return env.ASSETS.fetch(request);
  },
};
