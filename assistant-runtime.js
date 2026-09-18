/* NayaNET Assistant Runtime — governed authenticated session + durable cognition boundary. */
(()=>{'use strict';
const URL='https://dahisasgpfvziswqvmvm.supabase.co',KEY='sb_publishable_oQFKOYFuJ9bT-E9QkJUb4g_lAUyInue',PROJECT='NayaNET';
let client=null,session=null,modal=null;
const state={authenticated:false,user_id:null,session_id:null,persistence:'unknown'};
function load(){return new Promise((resolve,reject)=>{if(window.supabase?.createClient)return resolve(window.supabase);const s=document.createElement('script');s.src='https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2';s.onload=()=>resolve(window.supabase);s.onerror=reject;document.head.append(s)})}
async function init(){const lib=await load();client=lib.createClient(URL,KEY,{auth:{persistSession:true,autoRefreshToken:true,detectSessionInUrl:true}});const got=await client.auth.getSession();session=got.data.session||null;apply(session);client.auth.onAuthStateChange((_e,s)=>{session=s;apply(s)});if(session)await initialize();return snapshot()}
function apply(s){state.authenticated=!!s;state.user_id=s?.user?.id||null;state.session_id=s?.access_token?String(s.access_token).slice(0,12):null;state.persistence=s?'supabase:session':'unauthenticated';document.documentElement.dataset.nayaAuth=s?'authenticated':'anonymous'}
function snapshot(){return {...state}}
async function initialize(){if(!session)return false;const r=await client.rpc('nayanet_initialize_cognition',{p_project_id:PROJECT,p_state:{runtime:'assistant-cloudflare',initialized_at:new Date().toISOString()}});if(r.error)throw r.error;state.persistence='supabase:connected';return true}
async function signIn(email,password){if(!client)await init();const r=await client.auth.signInWithPassword({email:String(email).trim(),password});if(r.error)throw r.error;session=r.data.session;apply(session);await initialize();return snapshot()}
async function signOut(){if(client)await client.auth.signOut();session=null;apply(null);return snapshot()}
async function record(input){if(!client)await init();if(!session)throw new Error('AUTH_REQUIRED');const event={...input,event_id:input.event_id||('assistant_'+Date.now().toString(36)),project:PROJECT,source:input.source||'nayanet-assistant-cloudflare',actor:'human',created_at:new Date().toISOString(),schema_version:'2.0.0'};const r=await client.rpc('nayanet_record_cognition_event',{p_project_id:PROJECT,p_event:event,p_action:'record_intelligence',p_expected_result:'event persisted with receipt',p_observed_result:'event persisted',p_learning:[{status:'captured',at:new Date().toISOString()}]});if(r.error)throw r.error;return r.data}
async function retrieve(eventId){if(!client)await init();if(!session)throw new Error('AUTH_REQUIRED');let q=client.from('nayanet_cognition_events').select('*').eq('project_id',PROJECT);if(eventId)q=q.eq('event_id',eventId);const r=await q.order('created_at',{ascending:false}).limit(100);if(r.error)throw r.error;return r.data||[]}
window.NayaAssistantRuntime={init,signIn,signOut,record,retrieve,snapshot};
function ui(){if(document.getElementById('naya-assistant-auth'))return;const style=document.createElement('style');style.textContent='#naya-assistant-auth{position:fixed;inset:0;z-index:1000;display:none;place-items:center;background:#000d;backdrop-filter:blur(18px);padding:18px}#naya-assistant-auth.open{display:grid}#naya-assistant-auth .box{width:min(460px,100%);padding:24px;border:2px solid #9d75ff88;border-radius:22px;background:linear-gradient(145deg,#17111f,#08080d);box-shadow:0 35px 90px #000f}#naya-assistant-auth h2{margin:0 0 6px;font-size:25px}#naya-assistant-auth p{color:#aaa4b1;font-size:10px;line-height:1.6}#naya-assistant-auth input{width:100%;margin:6px 0;padding:13px;border:2px solid #ffffff22;border-radius:11px;background:#07070a;color:#fff}#naya-assistant-auth button{min-height:40px;margin:8px 6px 0 0;padding:0 14px;border:2px solid #8b63ff66;border-radius:11px;background:#0b0a10;color:#fff;font-weight:900}#naya-assistant-auth .state{margin-top:10px;color:#9ff2bb;font-size:9px}';document.head.append(style);const m=document.createElement('div');m.id='naya-assistant-auth';m.innerHTML='<div class="box"><h2>NayaNET Member Access</h2><p>Real Supabase authentication. Authenticated sessions unlock the governed persistent intelligence boundary. No preview identity is promoted.</p><input id="naya-auth-email" type="email" autocomplete="email" placeholder="Email"><input id="naya-auth-password" type="password" autocomplete="current-password" placeholder="Password"><button id="naya-auth-signin">SIGN IN</button><button id="naya-auth-close">CLOSE</button><div class="state" id="naya-auth-state"></div></div>';document.body.append(m);modal=m;
}
const close=()=>modal?.classList.remove('open');document.getElementById('naya-auth-close').onclick=close;document.getElementById('naya-auth-signin').onclick=async()=>{const st=document.getElementById('naya-auth-state');st.textContent='Signing in…';try{await signIn(document.getElementById('naya-auth-email').value,document.getElementById('naya-auth-password').value);st.textContent='AUTHENTICATED · SUPABASE SESSION ACTIVE';close();sync()}catch(e){st.textContent='SIGN IN FAILED · '+(e?.message||'AUTH_ERROR')}};window.NayaAssistantRuntime.openAuth=()=>modal?.classList.add('open');
function sync(){document.querySelectorAll('a[href="https://hmclibrary.groovemember.net/login"]').forEach(a=>{a.href='#';a.target='';a.onclick=e=>{e.preventDefault();window.NayaAssistantRuntime.openAuth()};a.textContent='MEMBER LOGIN'});const n=document.querySelector('.naya509-corner');if(n){const led=n.querySelector('.naya509-led');if(led)led.style.background=state.authenticated?'#55e39a':'#e8c766';}}
window.addEventListener('load',async()=>{try{await init()}catch(e){state.persistence='error';document.documentElement.dataset.nayaAuthError='1'}ui();sync()});
if(document.readyState!=='loading'){ui();sync()}
})();
/* NAYA HUB APPLICATION BRIDGE V1
   Preserves the canonical Hub presentation and connects its existing Personal feed
   to the authenticated cognition boundary. No replacement UI is created. */
(()=>{
  'use strict';
  const esc=(v)=>String(v??'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
  const textOf=(e)=>String(e?.summary||e?.content||e?.meaning||e?.title||'').trim();
  const liveId=(e)=>'naya-live-'+String(e?.event_id||e?.id||'event').replace(/[^a-zA-Z0-9_-]/g,'-');

  function liveCard(e){
    const title=String(e?.title||e?.event?.title||'Preserved Intelligence').trim();
    const summary=textOf(e).slice(0,1800);
    const id=liveId(e);
    return `<article class="block naya509-board naya-runtime-live" id="${id}" data-naya-runtime-event="${esc(e?.event_id||e?.id||'')}" style="--tone:#55e39a">
      <div class="blockInner">
        <div class="blockTop">
          <div class="identity">
            <div class="glyph" aria-hidden="true">◈</div>
            <div>
              <h3>${esc(title)}</h3>
              <div class="meta"><span>PERSONAL INTELLIGENCE</span><span>RUNTIME RETRIEVED</span><span>${esc(e?.created_at||'')}</span></div>
            </div>
          </div>
          <div class="truth">AUTHENTICATED · PERSISTED</div>
        </div>
        <div class="nutshell"><b>IN A NUTSHELL</b><p>${esc(summary||'Preserved intelligence retrieved from the authenticated cognition store.')}</p></div>
        <div class="layers">
          <section class="layer" style="--layer:#55e39a"><div class="layerHead"><i class="dot"></i><b>NAYA NOTE</b><span class="state">PERSISTED</span></div><div class="layerBody">${esc(summary||'No interpretation stored.')}</div></section>
          <section class="layer" style="--layer:#55b9ee"><div class="layerHead"><i class="dot"></i><b>MACHINE NOTE</b><span class="state">PROVENANCE</span></div><div class="layerBody">Event ID: <strong>${esc(e?.event_id||e?.id||'unknown')}</strong></div></section>
        </div>
        <div class="blockFoot"><span>NAYA POWER RUNTIME</span><span>LIVE RETRIEVAL · SOURCE PRESERVED</span></div>
      </div>
    </article>`;
  }

  async function loadPersonal(){
    try{
      if(!window.NayaAssistantRuntime?.snapshot || !window.NayaAssistantRuntime?.retrieve) return;
      const snap=window.NayaAssistantRuntime.snapshot();
      if(!snap.authenticated) return;
      const events=await window.NayaAssistantRuntime.retrieve();
      const blocks=document.getElementById('blocks');
      if(!blocks) return;
      blocks.querySelectorAll('.naya-runtime-live').forEach(x=>x.remove());
      const relevant=(events||[]).filter(e=>String(e?.project_id||e?.project||'NayaNET')==='NayaNET').slice(0,20);
      if(relevant.length) blocks.insertAdjacentHTML('afterbegin',relevant.map(liveCard).join(''));
      const count=document.getElementById('feedCount');
      if(count) count.textContent=(relevant.length||0)+' LIVE + CANONICAL INTELLIGENCE';
      const title=document.getElementById('feedTitle');
      if(title) title.textContent='Personal Intelligence';
      const desc=document.getElementById('feedDesc');
      if(desc) desc.textContent='Authenticated intelligence retrieved from the governed NayaNET cognition boundary.';
    }catch(err){
      document.documentElement.dataset.nayaRuntimeFeedError='1';
    }
  }

  function wire(){
    document.addEventListener('click',(event)=>{
      const feed=event.target.closest('[data-feed="personal"]');
      if(feed) setTimeout(loadPersonal,0);
    },true);
    window.NayaAssistantRuntime && (window.NayaAssistantRuntime.loadPersonalIntelligence=loadPersonal);
    if(document.documentElement.dataset.nayaAuth==='authenticated') setTimeout(loadPersonal,50);
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',wire,{once:true});
  else wire();
})();
