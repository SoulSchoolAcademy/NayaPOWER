import {FormEvent,useEffect,useState} from 'react';
import {supabase,useIdentity} from './session';

type NameFirstAuth={
  establish:(input:{name:string;alias:string})=>Promise<{authenticated:boolean;userId:string;smartName:string;smartAlias:string}>;
};

declare global { interface Window { NayaNETNameFirstAuth?:NameFirstAuth } }

export function AuthPanel(){
  const identity=useIdentity();
  const [name,setName]=useState('');
  const [alias,setAlias]=useState('');
  const [message,setMessage]=useState('');
  const [busy,setBusy]=useState(false);
  useEffect(()=>{
    if(identity.is_authenticated){
      setName(identity.smart_name||'');
      return;
    }
    const saved=localStorage.getItem('nayanet_smart_name')||'';
    const savedAlias=localStorage.getItem('nayanet_smart_alias')||'';
    setName(saved);setAlias(savedAlias);
  },[identity.is_authenticated,identity.smart_name]);

  if(identity.is_authenticated){
    return <section className="empty-route">
      <span className="eyebrow">AUTHENTICATED</span>
      <h2>{identity.smart_name}</h2>
      <p>Supabase session is active. The Hub is using the authenticated member boundary for persistent intelligence.</p>
      <button className="hero-secondary" onClick={()=>supabase.auth.signOut()}>SIGN OUT</button>
    </section>;
  }

  const suggest=(value:string)=>value.toLowerCase().replace(/[^a-z0-9]/g,'').slice(0,48);
  const submit=async(e:FormEvent)=>{
    e.preventDefault();setBusy(true);setMessage('');
    try{
      const smartName=name.trim();const smartAlias=suggest(alias||smartName);
      if(!smartName||!smartAlias) throw new Error('NAME_AND_ALIAS_REQUIRED');
      if(!window.NayaNETNameFirstAuth) throw new Error('IDENTITY_ADAPTER_NOT_LOADED');
      const result=await window.NayaNETNameFirstAuth.establish({name:smartName,alias:smartAlias});
      if(!result.authenticated||!result.userId) throw new Error('AUTH_SESSION_NOT_ESTABLISHED');
      localStorage.setItem('nayanet_smart_name',result.smartName);localStorage.setItem('nayanet_smart_alias',result.smartAlias);
      setMessage('Identity established. Loading your Intelligent Hub…');
    }catch(error){setMessage(error instanceof Error?error.message:'Unable to establish your NayaNET identity.');}
    finally{setBusy(false);}
  };
  return <section className="empty-route" aria-label="NayaNET name-first identity"><span className="eyebrow">NAYANET IDENTITY</span><h2>Enter the Hub</h2><p>Use your name and NayaNET address. Your address is an application namespace — not an email address.</p><form onSubmit={submit} style={{display:'grid',gap:12,maxWidth:440,marginTop:20}}><input value={name} onChange={e=>{setName(e.target.value);if(!alias)setAlias(suggest(e.target.value));}} autoComplete="name" placeholder="What's your name?" required maxLength={120} style={{padding:14,borderRadius:10,border:'1px solid #333',background:'#111',color:'#fff'}}/><input value={alias} onChange={e=>setAlias(e.target.value)} autoComplete="username" placeholder="Choose your NayaNET address" required maxLength={48} style={{padding:14,borderRadius:10,border:'1px solid #333',background:'#111',color:'#fff'}}/><button className="hero-primary" disabled={busy}>{busy?'ESTABLISHING…':'ENTER NAYANET'}</button></form>{message&&<p role="status" style={{marginTop:14}}>{message}</p>}</section>;
}
