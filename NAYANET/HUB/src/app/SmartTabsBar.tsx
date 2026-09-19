import { useEffect, useState } from 'react';
import { supabase } from '../identity/session';
import { routes } from './routes';

type Tab = { id:string; label:string; target_type:string; target:string; favorite:boolean; position:number };

function resolve(targetType:string,target:string){
  if(targetType==='url') { window.location.assign(target); return; }
  if(targetType==='query' || targetType==='topic' || targetType==='category'){
    window.history.pushState({},'',routes.feed);
    window.dispatchEvent(new CustomEvent('popstate'));
    window.dispatchEvent(new CustomEvent('nayanet:search',{detail:{query:target}}));
    return;
  }
  const path=target.startsWith('/')?target:'/'+target.replace(/^\//,'');
  window.history.pushState({},'',path);
  window.dispatchEvent(new PopStateEvent('popstate'));
}

export function SmartTabsBar(){
  const [tabs,setTabs]=useState<Tab[]>([]);
  const [status,setStatus]=useState('');
  const [open,setOpen]=useState(false);
  const [label,setLabel]=useState('');
  const [target,setTarget]=useState('');
  const [busy,setBusy]=useState(false);

  const load=async()=>{
    const {data:{session}}=await supabase.auth.getSession();
    if(!session){setTabs([]);return;}
    const {data,error}=await supabase.from('nayanet_smart_tabs')
      .select('id,label,target_type,target,favorite,position').order('position').order('created_at');
    if(error){setStatus('SMART TABS BLOCKED · '+error.message);return;}
    setTabs((data||[]) as Tab[]);
  };
  useEffect(()=>{void load();const h=()=>void load();window.addEventListener('naya-auth-state',h);return()=>window.removeEventListener('naya-auth-state',h)},[]);

  const add=async()=>{
    if(!label.trim()||!target.trim()||busy)return;
    setBusy(true);setStatus('PERSISTING TAB…');
    const {data:{session}}=await supabase.auth.getSession();
    if(!session){setStatus('AUTHENTICATION REQUIRED');setBusy(false);return;}
    const target_type=/^https?:\/\//i.test(target)?'url':target.startsWith('/')?'route':'query';
    const {error}=await supabase.from('nayanet_smart_tabs').insert({owner_id:session.user.id,label:label.trim(),target,target_type,scope:'private',position:tabs.length});
    setBusy(false);
    if(error){setStatus('TAB CREATE BLOCKED · '+error.message);return;}
    setLabel('');setTarget('');setOpen(false);setStatus('TAB PERSISTED');await load();
  };

  const remove=async(id:string)=>{
    const {error}=await supabase.from('nayanet_smart_tabs').delete().eq('id',id);
    setStatus(error?'TAB DELETE BLOCKED · '+error.message:'TAB DELETED');await load();
  };

  return <section className="smart-tabs-bar" aria-label="Smart Tabs">
    <div className="smart-tabs-head"><span>SMART TABS</span><small>PRIVATE NAVIGATION · {tabs.length}</small><button onClick={()=>setOpen(v=>!v)} aria-expanded={open}>＋ ADD</button></div>
    <div className="smart-tabs-list">
      {tabs.map(tab=><div className="smart-tab" key={tab.id}><button onClick={()=>resolve(tab.target_type,tab.target)} title={tab.target}>{tab.favorite?'★ ':''}{tab.label}</button><button className="smart-tab-delete" onClick={()=>void remove(tab.id)} aria-label={'Delete '+tab.label}>×</button></div>)}
      {!tabs.length&&<span className="smart-tabs-empty">Save the destinations and intelligence you use most.</span>}
    </div>
    {open&&<div className="smart-tabs-editor"><input value={label} onChange={e=>setLabel(e.target.value)} placeholder="Label" aria-label="Smart Tab label"/><input value={target} onChange={e=>setTarget(e.target.value)} placeholder="/feed, /today, or a search topic" aria-label="Smart Tab target"/><button disabled={busy||!label.trim()||!target.trim()} onClick={()=>void add()}>SAVE TAB</button></div>}
    {status&&<div className="smart-tabs-status" role="status">{status}</div>}
  </section>;
}
