import {FormEvent,useState} from 'react';
import {supabase,useIdentity} from './session';

const GITHUB_REPO='SoulSchoolAcademy/NayaPOWER';
const DISPATCH_FUNCTION='nayanet-github-dispatch';

export function AuthPanel(){
  const identity=useIdentity();
  const [email,setEmail]=useState('');
  const [password,setPassword]=useState('');
  const [message,setMessage]=useState('');
  const [busy,setBusy]=useState(false);
  const [dispatchBusy,setDispatchBusy]=useState(false);
  const [dispatchResult,setDispatchResult]=useState('');

  if(identity.is_authenticated){
    const dispatchCanonical=async()=>{
      setDispatchBusy(true);
      setDispatchResult('');
      try{
        const {data:{session},error:sessionError}=await supabase.auth.getSession();
        if(sessionError)throw new Error(`AUTH_SESSION_LOOKUP_FAILED: ${sessionError.message}`);
        if(!session?.access_token)throw new Error('AUTHENTICATED_NAYA_POWER_SESSION_REQUIRED');

        const branchResponse=await fetch(`https://api.github.com/repos/${GITHUB_REPO}/branches/main`,{
          headers:{Accept:'application/vnd.github+json'}
        });
        if(!branchResponse.ok)throw new Error(`GITHUB_MAIN_LOOKUP_FAILED: HTTP ${branchResponse.status}`);
        const branch=await branchResponse.json() as {commit?:{sha?:string}};
        const commit_sha=branch.commit?.sha;
        if(!commit_sha||!/^[0-9a-f]{40}$/i.test(commit_sha))throw new Error('GITHUB_MAIN_SHA_INVALID');

        const idempotency_key=`nayanet-canonical-deploy-${commit_sha}-${Date.now()}`;
        const {data,error}=await supabase.functions.invoke(DISPATCH_FUNCTION,{
          body:{
            commit_sha,
            approval:'EXPLICIT_APPROVAL_GRANTED',
            reason:'Canonical NayaNET Hub deployment verification',
            idempotency_key
          },
          headers:{Authorization:`Bearer ${session.access_token}`}
        });
        if(error)throw new Error(`DISPATCH_FAILED: ${error.message}`);
        setDispatchResult(JSON.stringify(data,null,2));
      }catch(error){
        setDispatchResult(error instanceof Error?error.message:'CANONICAL_DISPATCH_FAILED');
      }finally{
        setDispatchBusy(false);
      }
    };

    return <section className="empty-route">
      <span className="eyebrow">AUTHENTICATED</span>
      <h2>{identity.smart_name}</h2>
      <p>Supabase session is active. The Hub is using the authenticated member boundary for persistent intelligence.</p>
      <div style={{display:'grid',gap:12,maxWidth:720,marginTop:20}}>
        <button className="hero-secondary" onClick={()=>supabase.auth.signOut()}>SIGN OUT</button>
        <div style={{border:'1px solid #333',borderRadius:14,padding:18,background:'#0d0d10'}}>
          <span className="eyebrow">CANONICAL RUNTIME CONTROL</span>
          <h3 style={{margin:'8px 0'}}>Deploy the current main commit</h3>
          <p style={{margin:'0 0 14px'}}>This uses your real NayaPOWER Supabase session, resolves the exact current <code>main</code> SHA, and sends it through <code>nayanet-github-dispatch</code>. The Edge Function remains the authorization and governance boundary.</p>
          <button className="hero-primary" disabled={dispatchBusy} onClick={dispatchCanonical}>{dispatchBusy?'DISPATCHING…':'DISPATCH CURRENT MAIN'}</button>
          {dispatchResult&&<pre style={{whiteSpace:'pre-wrap',overflowWrap:'anywhere',marginTop:14,padding:14,borderRadius:10,background:'#07070A',fontSize:12}}>{dispatchResult}</pre>}
        </div>
      </div>
    </section>;
  }

  const submit=async(e:FormEvent)=>{e.preventDefault();setBusy(true);setMessage('');const {error}=await supabase.auth.signInWithPassword({email:email.trim(),password});setBusy(false);setMessage(error?error.message:'Signed in.');};
  return <section className="empty-route" aria-label="NayaNET sign in"><span className="eyebrow">REAL SUPABASE AUTHENTICATION</span><h2>Enter the Hub</h2><p>This signs into the real Supabase session. No preview identity is promoted to live access.</p><form onSubmit={submit} style={{display:'grid',gap:12,maxWidth:440,marginTop:20}}><input value={email} onChange={e=>setEmail(e.target.value)} type="email" autoComplete="email" placeholder="Email" required style={{padding:14,borderRadius:10,border:'1px solid #333',background:'#111',color:'#fff'}}/><input value={password} onChange={e=>setPassword(e.target.value)} type="password" autoComplete="current-password" placeholder="Password" required style={{padding:14,borderRadius:10,border:'1px solid #333',background:'#111',color:'#fff'}}/><button className="hero-primary" disabled={busy}>{busy?'SIGNING IN…':'SIGN IN'}</button></form>{message&&<p role="status" style={{marginTop:14}}>{message}</p>}</section>;
}
