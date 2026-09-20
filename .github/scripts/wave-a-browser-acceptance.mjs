          import { chromium } from 'playwright';
          import crypto from 'node:crypto';
          import fs from 'node:fs';
          const base=process.env.SUPABASE_URL,key=process.env.SUPABASE_PUBLISHABLE_KEY || "sb_publishable_oQFKOYFuJ9bT-E9QkJUb4g_lAUyInue";
          const runtime=process.env.RUNTIME_URL,spaceId=process.env.NAYA_EXISTING_SPACE_ID;
          const project='NayaNET-WaveA-Browser-'+process.env.GITHUB_RUN_ID+'-'+crypto.randomBytes(4).toString('hex');
          async function req(url,opt={}){const r=await fetch(url,opt);const t=await r.text();let b;try{b=JSON.parse(t)}catch{b={raw:t}}if(!r.ok)throw Error(r.status+' '+JSON.stringify(b));return b}
          const h=t=>({apikey:key,authorization:'Bearer '+t,'content-type':'application/json'});
          const signup=()=>req(base+'/auth/v1/signup',{method:'POST',headers:{apikey:key,'content-type':'application/json'},body:'{}'});
          const A=await signup(),B=await signup(),C=await signup();
          if(!A.access_token||!B.access_token||!C.access_token)throw Error('AUTH_BOOTSTRAP_FAILED');
          const join=async u=>req(base+'/rest/v1/rpc/nayanet_join_space',{method:'POST',headers:h(u.access_token),body:JSON.stringify({p_space_id:spaceId})});
          await join(A);await join(B);await join(C);
          const save=async(u,target)=>req(base+'/rest/v1/rpc/nayanet_save_connection',{method:'POST',headers:h(u.access_token),body:JSON.stringify({p_target_member_id:target,p_space_id:spaceId})});
          // Smart Mail's canonical relationship gate requires a mutual active connection.
          // Establish the reciprocal leg through the existing connection RPC before the UI send proof.
          await save(B,A.user.id);
          const grant=await req(base+'/rest/v1/rpc/nayanet_issue_authority_grant',{method:'POST',headers:h(A.access_token),body:JSON.stringify({p_subject_id:A.user.id,p_source_event_id:'wavea-browser-authority-'+project,p_mission_id:'Wave A live Hub acceptance',p_scope:{project_id:'NayaNET',target:B.user.id,space_id:spaceId},p_actions:['smart_mail_send'],p_constraints:{mode:'human-facing-acceptance',no_external_side_effects:false},p_expires_at:new Date(Date.now()+15*60*1000).toISOString(),p_evidence:{authorization_type:'explicit_wave_a_browser_acceptance',space_id:spaceId},p_parent_authority:null})});
          if(!grant?.grant_id)throw Error('AUTHORITY_GRANT_FAILED');
          const browser=await chromium.launch({headless:true});
          async function contextFor(session){const origin=new URL(runtime).origin;const storageState={cookies:[],origins:[{origin,localStorage:[{name:'nayanet.supabase.auth',value:JSON.stringify(session)}]}]};const c=await browser.newContext({storageState});const p=await c.newPage();await p.goto(runtime+'/',{waitUntil:'domcontentloaded',timeout:60000});await p.waitForFunction(()=>!!window.NayaAssistantRuntime,{timeout:30000});const auth=await p.evaluate(async({base,key})=>{const sdk=await import('https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/+esm');const c=sdk.createClient(base,key,{auth:{persistSession:true,autoRefreshToken:true,storage:localStorage,storageKey:'nayanet.supabase.auth'}});const r=await c.auth.getUser();if(r.error)throw r.error;return r.data.user?.id},{base,key});if(auth!==session.user.id)throw Error('BROWSER_SESSION_HANDOFF_MISMATCH');return {c,p}}
          const Actx=await contextFor(A),ap=Actx.p;
ap.on('console',m=>{if(m.text().includes('NAYA_RECORD_TRACE'))console.log('LEDGER_TRACE_CONSOLE',m.text())});
ap.on('request',r=>{if(r.url().includes('nayanet_record_cognition_event'))console.log('LEDGER_TRACE_REQUEST',r.method(),r.url(),r.postData()||'')});
ap.on('response',async r=>{if(r.url().includes('nayanet_record_cognition_event'))console.log('LEDGER_TRACE_RESPONSE',r.status(),r.url(),(await r.text().catch(()=>'' )).slice(0,1200))});
          const aAuth=await ap.evaluate(()=>window.NayaAssistantRuntime.init());if(aAuth.user_id!==A.user.id||!aAuth.authenticated)throw Error('A_AUTHENTICATED_HANDOFF_FAILED');
          let connectDialogStep=0;
          ap.on('dialog',async dialog=>{if(dialog.type()!=='prompt')throw Error('UNEXPECTED_CONNECT_DIALOG:'+dialog.type());connectDialogStep+=1;await dialog.accept(connectDialogStep===1?B.user.id:spaceId);});
          const spaces=await ap.evaluate(()=>window.NayaAssistantRuntime.listSpaces());if(!spaces.some(x=>x.id===spaceId))throw Error('SPACE_VISIBILITY_FAILED');
          const members=await ap.evaluate(id=>window.NayaAssistantRuntime.listSpaceMembers(id),spaceId);if(!members.some(x=>x.member_id===A.user.id)||!members.some(x=>x.member_id===B.user.id))throw Error('AB_MEMBERSHIP_UI_FAILED');
          const connectionsBefore=await ap.evaluate(()=>window.NayaAssistantRuntime.listConnections());if(connectionsBefore.some(x=>x.connected_member_id===B.user.id&&x.status==='active'))throw Error('CONNECTION_PREEXISTING');
          const connectButton=ap.getByRole('button',{name:'↔ CONNECT',exact:true}).first();await connectButton.click();await ap.waitForTimeout(250);
          await ap.locator('.sfb-related-list button').first().click();await ap.waitForTimeout(900);
          const connectStatus=await ap.locator('.sfb-status').textContent().catch(()=> '');
          if(!String(connectStatus||'').includes('CONNECTION CREATED · CANONICAL ID '))throw Error('CANONICAL_CONNECTION_CREATE_NOT_PROVEN:'+String(connectStatus||'NO_STATUS'));
          const connectionId=String(connectStatus).match(/CANONICAL ID ([0-9a-f-]{36})/i)?.[1];if(!connectionId)throw Error('CANONICAL_CONNECTION_ID_MISSING');
          const connections=await ap.evaluate(()=>window.NayaAssistantRuntime.listConnections());const ab=connections.find(x=>x.id===connectionId&&x.owner_member_id===A.user.id&&x.connected_member_id===B.user.id&&x.status==='active'&&x.source_space_id);
          if(!ab||ab.source_space_id!==spaceId)throw Error('CANONICAL_CONNECTION_RUNTIME_RETRIEVAL_FAILED:'+JSON.stringify(connections));
          await ap.reload({waitUntil:'networkidle'});await ap.waitForTimeout(700);
          const reloadedConnections=await ap.evaluate(()=>window.NayaAssistantRuntime.listConnections());const reloaded=reloadedConnections.find(x=>x.id===connectionId&&x.connected_member_id===B.user.id&&x.status==='active');
          if(!reloaded)throw Error('CANONICAL_CONNECTION_NOT_RETRIEVED_AFTER_RELOAD');
          const navRoot=ap.viewportSize()?.width<=760?ap.locator('.mobile-nav'):ap.locator('.nav-section');
          const connectionsNav=navRoot.locator('button').filter({hasText:'Your Connections'});await connectionsNav.scrollIntoViewIfNeeded();await connectionsNav.click();await ap.waitForTimeout(700);
          if(!ap.url().includes('/connections'))throw Error('CONNECTIONS_ROUTE_FAILED');
          const connectionSurfaceText=await ap.locator('.feature-surface').first().innerText();if(!connectionSurfaceText.includes(B.user.id))throw Error('CONNECTION_NOT_VISIBLE_IN_SURFACE');
          console.log('CANONICAL_CONNECTION_CREATE_RELOAD_RETRIEVE_SURFACE_VERIFIED',JSON.stringify({connectionId,ownerMemberId:A.user.id,targetMemberId:B.user.id,spaceId}));

          const navLists=navRoot.locator('button').filter({hasText:'Smart Lists'});await navLists.scrollIntoViewIfNeeded();await navLists.click();await ap.waitForTimeout(700);
          if(!ap.url().includes('/lists'))throw Error('SMART_LIST_ROUTE_FAILED');
          const listName='Wave A live acceptance '+project;
          const createListButton=ap.getByRole('button',{name:'＋ CREATE SMART LIST',exact:true});await createListButton.click();
          await ap.getByRole('dialog').getByLabel('LIST NAME').fill(listName);
          await ap.getByRole('dialog').getByRole('button',{name:'CREATE SMART LIST',exact:true}).click();
          await ap.waitForTimeout(700);
          const listCard=ap.locator('.feature-card').filter({hasText:listName}).first();if(await listCard.count()!==1)throw Error('SMART_LIST_CREATE_NOT_VISIBLE');
          const smartLists=await ap.evaluate(()=>window.NayaAssistantRuntime.listSmartLists());const createdList=smartLists.find(x=>x.name===listName);if(!createdList?.id)throw Error('SMART_LIST_RUNTIME_RETRIEVAL_FAILED');
          const actionEvents=await ap.evaluate(async()=>window.NayaAssistantRuntime.retrieve());const listAction=actionEvents.find(x=>x.metadata?.action==='create_smart_list'&&x.metadata?.list_id===createdList.id);if(!listAction)throw Error('SMART_LIST_ACTION_RECEIPT_NOT_RETRIEVED');
          const listReceiptId=listAction.receipt_id||listAction.metadata?.receipt_id||'';if(!listReceiptId)throw Error('SMART_LIST_RECEIPT_ID_NOT_BOUND');
          await ap.reload({waitUntil:'networkidle'});await ap.waitForTimeout(700);
          if(!(await ap.locator('h1').filter({hasText:'Smart Lists'}).count()))throw Error('SMART_LIST_RELOAD_SURFACE_FAILED');
          if(await ap.locator('.feature-card').filter({hasText:listName}).count()!==1)throw Error('SMART_LIST_NOT_RETRIEVED_AFTER_RELOAD');
          console.log('CANONICAL_SMART_LIST_CREATE_RECEIPT_RELOAD_RETRIEVE_SURFACE_VERIFIED',JSON.stringify({listId:createdList.id,listName,receiptId:listReceiptId}));

          // Smart Share: human click → canonical publication → publication retrieval → reload → Smart Share surface.
          const navFeed=navRoot.locator('button').filter({hasText:'Smart Feed'});await navFeed.scrollIntoViewIfNeeded();await navFeed.click();await ap.waitForTimeout(700);
          if(!(await ap.locator('h1').filter({hasText:'Intelligence'}).count()))throw Error('SMART_FEED_ROUTE_FOR_SHARE_FAILED');
          const shareSetupTitle='Wave A Smart Share source '+project;const shareSetupContent='Authenticated runtime intelligence created solely as the source for the canonical Smart Share browser proof. '+project;const shareSetup=await ap.evaluate(async ({title,content})=>window.NayaAssistantRuntime.captureSmartNote({title,content}),{title:shareSetupTitle,content:shareSetupContent});if(!shareSetup)throw Error('SMART_SHARE_SETUP_CAPTURE_FAILED');const capturedSourceEventId=String(shareSetup?.event_id||shareSetup?.event?.event_id||'').trim();if(!capturedSourceEventId)throw Error('SMART_SHARE_CAPTURE_EVENT_ID_MISSING');await ap.goto(runtime+'/feed?event_id='+encodeURIComponent(capturedSourceEventId),{waitUntil:'networkidle',timeout:60000});await ap.waitForTimeout(800);const shareBoard=ap.locator('.smart-feed-board[data-event-id="'+capturedSourceEventId+'"]');await shareBoard.waitFor({state:'visible',timeout:10000});
          const shareSourceEventId=String(await shareBoard.getAttribute('data-event-id')||'');if(shareSourceEventId!==capturedSourceEventId)throw Error('SMART_SHARE_SOURCE_EVENT_ID_MISMATCH');
          const shareButton=shareBoard.getByRole('button',{name:'＋ SHARE',exact:true});await shareButton.click();
          await ap.waitForFunction(()=>Array.from(document.querySelectorAll('.sfb-status')).some(x=>/SHARE PUBLISHED|SHARE BLOCKED/.test(String(x.textContent||''))),null,{timeout:15000});
          const shareStatus=String(await ap.locator('.sfb-status').textContent().catch(()=>''));if(!shareStatus.includes('SHARE PUBLISHED · PUBLICATION '))throw Error('SMART_SHARE_PUBLICATION_NOT_PROVEN:'+shareStatus);
          const publicationId=shareStatus.match(/PUBLICATION ([0-9a-f-]{36})/i)?.[1];if(!publicationId)throw Error('SMART_SHARE_PUBLICATION_ID_MISSING');
          const shareEventId=shareStatus.match(/EVENT ([^ ·]+)/)?.[1]||'';if(!shareEventId)throw Error('SMART_SHARE_RECEIPT_EVENT_ID_MISSING');
          const collective=await ap.evaluate(()=>window.NayaAssistantRuntime.smartFeed({stream:'collective',limit:50}));const publishedItem=(collective?.items||[]).find(x=>x.publication_id===publicationId&&x.id===shareSourceEventId);if(!publishedItem)throw Error('SMART_SHARE_PUBLICATION_RUNTIME_RETRIEVAL_FAILED');
          const shareReceipts=await ap.evaluate(()=>window.NayaAssistantRuntime.retrieve());const shareReceiptEvent=shareReceipts.find(x=>x.event_id===shareEventId&&x.source==='nayanet-hub.smart-share.publication'&&x.metadata?.publication_id===publicationId);if(!shareReceiptEvent)throw Error('SMART_SHARE_RECEIPT_RETRIEVAL_FAILED');
          await ap.reload({waitUntil:'networkidle'});await ap.waitForTimeout(700);
          const navShare=ap.viewportSize()?.width<=760?ap.locator('.mobile-nav'):ap.locator('.nav-section');const shareNav=navShare.locator('button').filter({hasText:'Smart Share'});await shareNav.scrollIntoViewIfNeeded();await shareNav.click();await ap.waitForTimeout(900);
          if(!ap.url().includes('/share'))throw Error('SMART_SHARE_ROUTE_FAILED');
          const shareSurface=ap.locator('.feature-surface').first();await shareSurface.waitFor({state:'visible'});const shareSurfaceText=await shareSurface.innerText();if(!shareSurfaceText.includes(String(publishedItem.title||publishedItem.source?.label||shareSourceEventId)))throw Error('SMART_SHARE_NOT_VISIBLE_AFTER_RELOAD');
          console.log('CANONICAL_SMART_SHARE_PUBLICATION_RECEIPT_RELOAD_RETRIEVE_SURFACE_VERIFIED',JSON.stringify({sourceEventId:shareSourceEventId,publicationId,receiptEventId:shareEventId}));

          // Smart Ledger Inspect Evidence: human click → existing runtime authority → record → receipt → reload → retrieval.
          const navLedger=navRoot.locator('button').filter({hasText:'Smart Ledger'});await navLedger.scrollIntoViewIfNeeded();await navLedger.click();await ap.waitForTimeout(700);
          if(!(await ap.locator('h1').filter({hasText:'Smart Ledger'}).count()))throw Error('SMART_LEDGER_ROUTE_FAILED');
          const ledgerCards=ap.locator('.feature-card');if(await ledgerCards.count()<1)throw Error('SMART_LEDGER_NO_RECORDS');
          await ledgerCards.first().getByRole('button',{name:/Inspect evidence/i}).click();
          const inspectModal=ap.getByRole('dialog').last();await inspectModal.waitFor({state:'visible'});
          const inspectButton=inspectModal.getByRole('button',{name:/Inspect evidence/i});await inspectButton.click();
          await ap.waitForFunction(()=>Array.from(document.querySelectorAll('[role="dialog"] button')).some(b=>/INSPECT PERSISTED|LEDGER_INSPECT_FAILED|AUTH_REQUIRED/.test(String(b.textContent||''))),null,{timeout:10000});
          const inspectStatus=String(await inspectModal.getByRole('button',{name:/INSPECT PERSISTED|LEDGER_INSPECT_FAILED|AUTH_REQUIRED/i}).textContent().catch(()=>''));if(!inspectStatus.includes('INSPECT PERSISTED'))throw Error('SMART_LEDGER_INSPECT_NOT_PERSISTED:'+inspectStatus);
          const inspectEvents=await ap.evaluate(()=>window.NayaAssistantRuntime.retrieve());const inspectEvent=inspectEvents.find(x=>x.source==='nayanet-hub.smart-ledger.inspect'&&x.metadata?.action==='inspect_evidence'&&x.metadata?.ledger_event_id);
          if(!inspectEvent)throw Error('SMART_LEDGER_INSPECT_RETRIEVAL_FAILED');
          const ledgerEventId=String(inspectEvent.metadata?.ledger_event_id||'');if(!ledgerEventId)throw Error('SMART_LEDGER_INSPECT_LEDGER_EVENT_ID_MISSING');const inspectReceipt=inspectEvent.receipt_id||inspectEvent.metadata?.receipt_id||'';if(!inspectReceipt)throw Error('SMART_LEDGER_INSPECT_RECEIPT_MISSING');
          await ap.reload({waitUntil:'networkidle'});await ap.waitForTimeout(700);
          const afterReload=await ap.evaluate(()=>window.NayaAssistantRuntime.retrieve());const retrievedInspect=afterReload.find(x=>x.event_id===inspectEvent.event_id&&x.metadata?.action==='inspect_evidence');
          if(!retrievedInspect||retrievedInspect.receipt_id!==inspectReceipt)throw Error('SMART_LEDGER_INSPECT_NOT_RETRIEVED_AFTER_RELOAD');
          console.log('SMART_LEDGER_INSPECT_RECEIPT_RELOAD_RETRIEVE_VERIFIED',JSON.stringify({ledgerEventId,eventId:inspectEvent.event_id,receiptId:inspectReceipt}));

          // Unauthorized failure proof against the same canonical runtime.record() boundary.
          const unauthCtx=await browser.newContext();const unauth=await unauthCtx.newPage();await unauth.goto(runtime+'/',{waitUntil:'domcontentloaded',timeout:60000});await unauth.waitForFunction(()=>!!window.NayaAssistantRuntime,{timeout:30000});
          const blocked=await unauth.evaluate(async ledgerEventId=>{try{await window.NayaAssistantRuntime.record({title:'Smart Ledger evidence inspection',content:JSON.stringify({ledger_event_id:ledgerEventId}),source:'nayanet-hub.smart-ledger.inspect',project:'NayaNET',status:'active',actor:'human',tags:['intelligent-hub','smart-ledger','inspect-evidence'],metadata:{action:'inspect_evidence',ledger_event_id:ledgerEventId,persistence_boundary:'authenticated-canonical-runtime'}});return 'NO_BLOCK'}catch(e){return e instanceof Error?e.message:String(e)}},ledgerEventId);
          if(blocked!=='AUTH_REQUIRED')throw Error('SMART_LEDGER_UNAUTHORIZED_PERSISTENCE_NOT_BLOCKED:'+blocked);
          await unauthCtx.close();console.log('SMART_LEDGER_UNAUTHORIZED_PERSISTENCE_BLOCK_VERIFIED',blocked);

          const created=await ap.evaluate(async name=>window.NayaAssistantRuntime.createSmartList(name),'Wave A legacy runtime '+project);const listId=created?.list_id||created?.id||created?.list?.id;if(!listId)throw Error('SMART_LIST_CREATE_FAILED');
          await ap.evaluate(async x=>window.NayaAssistantRuntime.addConnectionToList(x.listId,x.connectionId),{listId,connectionId:ab.id});const lists=await ap.evaluate(()=>window.NayaAssistantRuntime.listSmartLists());if(!lists.some(x=>x.id===listId&&x.members?.some(m=>m.connection_id===ab.id)))throw Error('SMART_LIST_UI_FAILED');
          const mail=await ap.evaluate(async x=>window.NayaAssistantRuntime.sendSmartMail({receiver_id:x.receiver,body:'Wave A live Hub acceptance.',subject:'Wave A acceptance',authority_grant_id:x.grant,idempotency_key:x.key}),{receiver:B.user.id,grant:grant.grant_id,key:'wavea-browser-mail-'+project});if(!mail?.message_id)throw Error('SMART_MAIL_UI_FAILED');
          const threadsA=await ap.evaluate(()=>window.NayaAssistantRuntime.listMailThreads());if(!threadsA.some(x=>x.id===mail.thread_id))throw Error('SMART_MAIL_RENDER_FAILED');
          const Bctx=await contextFor(B),bp=Bctx.p;const bAuth=await bp.evaluate(()=>window.NayaAssistantRuntime.init());if(bAuth.user_id!==B.user.id)throw Error('B_AUTH_HANDOFF_FAILED');
          const verified=await bp.evaluate(id=>window.NayaAssistantRuntime.verifySmartMail(id),mail.message_id);if(!verified?.ok)throw Error('B_RECEIVER_VERIFICATION_UI_FAILED');
          const bThreads=await bp.evaluate(()=>window.NayaAssistantRuntime.listMailThreads());if(!bThreads.some(x=>x.id===mail.thread_id))throw Error('B_RETRIEVAL_UI_FAILED');
          const intelligence=await bp.evaluate(()=>window.NayaAssistantRuntime.retrieve());if(!Array.isArray(intelligence)||intelligence.length<1)throw Error('INTELLIGENCE_UI_FAILED');
          const mailCognition=await req(base+'/rest/v1/nayanet_cognition_events?select=id,event_id,receipt_id&id=eq.'+mail.cognition_event_id,{headers:h(A.access_token)});if(mailCognition.length!==1||mailCognition[0].receipt_id!==mail.execution_receipt_id)throw Error('SMART_MAIL_COGNITION_LINEAGE_FAILED');
          const mailReceipt=await req(base+'/rest/v1/nayanet_execution_receipts?select=id,status,evidence,learning,value&id=eq.'+mail.execution_receipt_id,{headers:h(A.access_token)});if(mailReceipt.length!==1||mailReceipt[0].status!=='SUCCESS'||mailReceipt[0].value?.verified!==true)throw Error('SMART_MAIL_RECEIPT_VALUE_FAILED');
          const learningTarget='wave-a-smart-mail-'+mail.message_id;
          const evidence=await req(base+'/rest/v1/learning_evidence',{method:'POST',headers:{...h(A.access_token),'Prefer':'return=representation'},body:JSON.stringify({member_id:A.user.id,target_id:learningTarget,level:'E1_UNDERSTANDS',provenance:'VERIFICATION',status:'ACTIVE',claim:'A verified Smart Mail outcome can be reused by a later Naya decision without changing authority.',observed_value:{message_id:mail.message_id,receipt_id:mail.execution_receipt_id,cognition_event_id:mail.cognition_event_id,verified_value:mailReceipt[0].value.verified_value},verification_method:'authenticated receiver verification + execution receipt + cognition lineage',source_event_id:mailCognition[0].event_id})});if(!Array.isArray(evidence)||evidence.length!==1)throw Error('LEARNING_EVIDENCE_FAILED');
          const applied=await req(base+'/functions/v1/naya-learning-apply',{method:'POST',headers:h(A.access_token),body:JSON.stringify({evidence_id:evidence[0].id})});if(!applied.ok||!applied.learning?.learner_state_version)throw Error('LEARNING_APPLY_FAILED');
          const reused=await req(base+'/functions/v1/naya-decision-context',{method:'POST',headers:h(A.access_token),body:JSON.stringify({target_id:learningTarget})});if(!reused.ok||reused.decision?.decision!=='USE_VERIFIED_LEARNING_CONTEXT'||reused.decision?.influenced!==true)throw Error('LEARNING_REUSE_NOT_INFLUENCED');if(reused.decision?.authority?.changed!==false||reused.decision?.authority?.granted!==false)throw Error('LEARNING_REUSE_AUTHORITY_CHANGED');
          const Cctx=await contextFor(C),cp=Cctx.p;const cAuth=await cp.evaluate(()=>window.NayaAssistantRuntime.init());if(cAuth.user_id!==C.user.id)throw Error('C_AUTH_HANDOFF_FAILED');
          const cThreads=await cp.evaluate(()=>window.NayaAssistantRuntime.listMailThreads());if(cThreads.some(x=>x.id===mail.thread_id))throw Error('C_ISOLATION_UI_FAILED');
          const receipt={schema:'nayanet.wave-a.browser-acceptance.v1',status:'VERIFIED',run_id:process.env.GITHUB_RUN_ID,project,space_id:spaceId,checks:{authenticated_browser_handoff:'PASS',production_space_visible:'PASS',ab_membership_visible:'PASS',connections:'PASS',smart_list:'PASS',smart_share:'PASS',smart_mail:'PASS',b_retrieval:'PASS',intelligence_retrieval:'PASS',c_isolation:'PASS',execution_receipt:'PASS',cognition_lineage:'PASS',learning_evidence:'PASS',learning_applied:'PASS',learning_reuse:'PASS',learning_authority_unchanged:'PASS'},identities:{A:A.user.id,B:B.user.id,C:C.user.id},message_id:mail.message_id,execution_receipt_id:mail.execution_receipt_id,cognition_event_id:mail.cognition_event_id,smart_share_source_event_id:shareSourceEventId,smart_share_publication_id:publicationId,smart_share_receipt_event_id:shareEventId,activity_event_id:null,learning_evidence_id:evidence[0].id,learner_state_version:applied.learning.learner_state_version,learning_reuse_decision:reused.decision.decision};fs.writeFileSync(process.env.RECEIPT_PATH,JSON.stringify(receipt,null,2));console.log('WAVE_A_BROWSER_ACCEPTANCE=PASS');console.log(JSON.stringify(receipt));await browser.close();
