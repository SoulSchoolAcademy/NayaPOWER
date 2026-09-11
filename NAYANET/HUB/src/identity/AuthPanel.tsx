import {FormEvent,useState} from 'react';
import {supabase,useIdentity} from './session';

export function AuthPanel(){
  const identity=useIdentity();
  const [email,setEmail]=useState('');
  const [password,setPassword]=useState('');
  const [message,setMessage]=useState('');
  const [busy,setBusy]=useState(false);
  if(identity.is_authenticated)return <section className="empty-route"><span className="eyebrow">AUTHENTICATED</span><h2>{identity.smart_name}</h2><p>Supabase session is active. The Hub is using the authenticated member boundary for persistent intelligence.</p><button className="hero-secondary" onClick={()=>supabase.auth.signOut()}>SIGN OUT</button></section>;
  const submit=async(e:FormEvent)=>{e.preventDefault();setBusy(true);setMessage('');const {error}=await supabase.auth.signInWithPassword({email:email.trim(),password});setBusy(false);setMessage(error?error.message:'Signed in.');};
  return <section className="empty-route" aria-label="NayaNET sign in"><span className="eyebrow">REAL SUPABASE AUTHENTICATION</span><h2>Enter the Hub</h2><p>This signs into the real Supabase session. No preview identity is promoted to live access.</p><form onSubmit={submit} style={{display:'grid',gap:12,maxWidth:440,marginTop:20}}><input value={email} onChange={e=>setEmail(e.target.value)} type="email" autoComplete="email" placeholder="Email" required style={{padding:14,borderRadius:10,border:'1px solid #333',background:'#111',color:'#fff'}}/><input value={password} onChange={e=>setPassword(e.target.value)} type="password" autoComplete="current-password" placeholder="Password" required style={{padding:14,borderRadius:10,border:'1px solid #333',background:'#111',color:'#fff'}}/><button className="hero-primary" disabled={busy}>{busy?'SIGNING IN…':'SIGN IN'}</button></form>{message&&<p role="status" style={{marginTop:14}}>{message}</p>}</section>;
}
