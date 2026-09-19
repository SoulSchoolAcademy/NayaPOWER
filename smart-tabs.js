(()=>{'use strict';
const esc=v=>String(v??'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const css=()=>{if(document.getElementById('naya-smart-tabs-style'))return;const s=document.createElement('style');s.id='naya-smart-tabs-style';s.textContent=`
#naya-smart-tabs{margin:0 22px 18px;padding:14px;border:1px solid #ffffff16;border-radius:18px;background:#08080c;box-shadow:inset 0 1px #fff3,0 18px 40px #0009}
#naya-smart-tabs .st-head{display:flex;justify-content:space-between;align-items:center;gap:12px;margin-bottom:10px}
#naya-smart-tabs .st-head b{font-size:8px;letter-spacing:.16em}
#naya-smart-tabs .st-head span{font-size:7px;color:#8f8798}
#naya-smart-tabs .st-list{display:flex;gap:7px;flex-wrap:wrap}
#naya-smart-tabs button{min-height:36px;padding:0 12px;border:1px solid #8b63ff55;border-radius:11px;background:linear-gradient(145deg,#15111d,#08080c);color:#eeeaf2;font-size:8px;font-weight:1000;letter-spacing:.06em;box-shadow:inset 0 1px #fff3,0 8px 18px #0008}
#naya-smart-tabs button:hover{transform:translateY(-1px);border-color:#d86cff}
#naya-smart-tabs .fav{border-color:#e8c76688}
#naya-smart-tabs .st-empty{color:#8f8798;font-size:8px;padding:7px 0}
#naya-smart-tabs .st-add{border-color:#55e39a77}
#naya-smart-tabs .st-state{margin-top:8px;color:#9f98a7;font-size:7px;min-height:12px}
@media(max-width:700px){#naya-smart-tabs{margin:0 14px 14px}.st-list{overflow:auto;flex-wrap:nowrap!important;padding-bottom:3px}}
`;document.head.append(s)};
async function load(){css();if(!window.NayaAssistantRuntime)return;const snap=await window.NayaAssistantRuntime.init();let root=document.getElementById('naya-smart-tabs');if(!root){root=document.createElement('section');root.id='naya-smart-tabs';const anchor=document.querySelector('.feedNav')||document.querySelector('.hero');(anchor?.parentElement||document.body).insertBefore(root,anchor?.nextSibling||null)}root.innerHTML='<div class="st-head"><b>SMART TABS · YOUR NAVIGATION</b><span id="st-auth">CHECKING AUTHORITY…</span></div><div class="st-list" id="st-list"></div><div class="st-state" id="st-state"></div>';if(!snap.authenticated){root.querySelector('#st-auth').textContent='AUTHENTICATION REQUIRED';root.querySelector('#st-state').textContent='Private navigation is not exposed without an authenticated session.';return}root.querySelector('#st-auth').textContent='AUTHENTICATED · PRIVATE';await render(root)}
async function render(root){const state=root.querySelector('#st-state'),list=root.querySelector('#st-list');try{const r=await window.NayaAssistantRuntime.listSmartTabs();const tabs=r.tabs||[];list.innerHTML='';if(!tabs.length){list.innerHTML='<span class="st-empty">No Smart Tabs yet. Create one from the navigation controls.</span>'}for(const t of tabs){const b=document.createElement('button');b.className=t.favorite?'fav':'';b.textContent=(t.favorite?'★ ':'')+t.label;b.title=t.target;b.onclick=()=>resolve(t);list.append(b)}const add=document.createElement('button');add.className='st-add';add.textContent='＋ ADD TAB';add.onclick=async()=>{const label=prompt('Tab label');if(!label)return;const target=prompt('Target route or URL', '/feed');if(!target)return;const targetType=/^https?:\\/\\//i.test(target)?'url':'route';state.textContent='Persisting…';try{await window.NayaAssistantRuntime.createSmartTab({label,target,target_type:targetType,position:tabs.length});state.textContent='TAB CREATED · PERSISTED';await render(root)}catch(e){state.textContent='CREATE FAILED · '+(e?.message||e)}};list.append(add);state.textContent=tabs.length?tabs.length+' PRIVATE TAB'+(tabs.length===1?'':'S')+' · OWNER-SCOPED':'Ready · no tabs'}catch(e){state.textContent='SMART TABS FAILED · '+(e?.message||e)}}
function resolve(t){if(t.target_type==='url')location.assign(t.target);else if(t.target.startsWith('/'))location.assign(t.target);else if(t.target.startsWith('#'))location.hash=t.target.slice(1);else location.assign('/'+t.target.replace(/^\\//,''))}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',()=>load().catch(()=>{}),{once:true});else load().catch(()=>{});
window.addEventListener('naya-auth-ready',()=>load().catch(()=>{}));
})();