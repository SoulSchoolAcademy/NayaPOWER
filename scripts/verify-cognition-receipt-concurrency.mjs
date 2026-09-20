import crypto from 'node:crypto';

const base=process.env.SUPABASE_URL;
const key=process.env.SUPABASE_PUBLISHABLE_KEY;
const project='NayaNET-concurrency-proof-'+Date.now()+'-'+crypto.randomBytes(4).toString('hex');

async function req(url,opt={}) {
  const r=await fetch(url,opt);
  const t=await r.text();
  let b; try { b=JSON.parse(t); } catch { b={raw:t}; }
  if(!r.ok) throw new Error(r.status+' '+JSON.stringify(b));
  return b;
}
const h=t=>({apikey:key,authorization:'Bearer '+t,'content-type':'application/json'});

const user=await req(base+'/auth/v1/signup',{
  method:'POST',
  headers:{apikey:key,'content-type':'application/json'},
  body:'{}'
});
if(!user.access_token||!user.user?.id) throw new Error('TEST_USER_CREATION_FAILED');

const write=(i)=>req(base+'/rest/v1/rpc/nayanet_record_cognition_event',{
  method:'POST',
  headers:h(user.access_token),
  body:JSON.stringify({
    p_project_id:project,
    p_event:{
      event_id:'concurrency-'+i+'-'+crypto.randomBytes(6).toString('hex'),
      created_at:new Date().toISOString(),
      type:'intelligence',
      classification:'concurrency_proof',
      title:'Cognition receipt concurrency proof '+i,
      content:'Independent concurrent writer '+i,
      source:'nayanet-concurrency-proof',
      status:'active',
      actor:'system',
      confidence:1,
      tags:['concurrency-proof'],
      source_hash:crypto.createHash('sha256').update(project+':'+i).digest('hex'),
      schema_version:'1.0.0',
      metadata:{proof:'cognition-receipt-concurrency',writer:i}
    },
    p_action:'concurrency_proof',
    p_expected_result:'unique receipt revision',
    p_observed_result:'concurrent write completed',
    p_learning:'[]'
  })
});

const N=8;
const results=await Promise.all(Array.from({length:N},(_,i)=>write(i)));
const receipts=results.map(r=>r.receipt);
const revisions=receipts.map(r=>Number(r.revision)).sort((a,b)=>a-b);
const receiptIds=receipts.map(r=>r.id);
const eventIds=results.map(r=>r.event.event_id);

if(receipts.some(r=>!r?.id)) throw new Error('RECEIPT_MISSING');
if(new Set(receiptIds).size!==N) throw new Error('DUPLICATE_RECEIPT_IDS');
if(new Set(revisions).size!==N) throw new Error('DUPLICATE_RECEIPT_REVISIONS');
for(let i=1;i<revisions.length;i++) if(revisions[i]!==revisions[i-1]+1) throw new Error('NON_CONTIGUOUS_RECEIPT_REVISIONS');
if(new Set(eventIds).size!==N) throw new Error('DUPLICATE_EVENT_IDS');

const rows=await req(base+'/rest/v1/nayanet_execution_receipts?select=id,revision,action&user_id=eq.'+user.user.id+'&project_id=eq.'+encodeURIComponent(project)+'&order=revision.asc',{headers:h(user.access_token)});
if(rows.length!==N) throw new Error('RECEIPT_ROW_COUNT_MISMATCH');
const dbRevisions=rows.map(r=>Number(r.revision));
if(JSON.stringify(dbRevisions)!==JSON.stringify(revisions)) throw new Error('DB_REVISION_SET_MISMATCH');

const state=await req(base+'/rest/v1/nayanet_project_cognition_state?select=revision,status,project_id&user_id=eq.'+user.user.id+'&project_id=eq.'+encodeURIComponent(project),{headers:h(user.access_token)});
if(state.length!==1||Number(state[0].revision)!==N) throw new Error('COGNITION_STATE_REVISION_MISMATCH');

console.log('COGNITION_RECEIPT_CONCURRENCY=PASS');
console.log('CONCURRENT_WRITERS='+N);
console.log('UNIQUE_RECEIPT_IDS='+new Set(receiptIds).size);
console.log('RECEIPT_REVISIONS='+revisions.join(','));
console.log('DB_RECEIPTS='+rows.length);
console.log('COGNITION_STATE_REVISION='+state[0].revision);
console.log('PROJECT='+project);
