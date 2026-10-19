'use strict';
const { test } = require('node:test');
const assert = require('node:assert/strict');
const bridge = require('./supabase-bridge.js');
const member = '11111111-1111-4111-8111-111111111111';
test('missing identity rejects remote fetch before SQL', async () => {
  let hits=0;
  const r=await bridge.getNotes({supabase:{query:async()=>{hits++;return [];}}});
  assert.equal(hits,0);
  assert.equal(r.backend,'none');
  assert.match(r.reason,/AUTHENTICATED_MEMBER_ID_REQUIRED/);
});
test('SQL reads are restricted by member id', async () => {
  let sql='';
  const r=await bridge.getNotes({supabase:{memberId:member,query:async q=>{sql=q;return [];}}});
  assert.equal(r.backend,'supabase');
  assert.ok(sql.includes("member_id = '"+member+"'"));
});
test('REST uses session bearer token and scoped filter', async () => {
  let url='', headers=null;
  const old=global.fetch;
  try {
    global.fetch=async(u,o)=>{url=u;headers=o.headers;return{ok:true,json:async()=>[]};};
    const r=await bridge.getNotes({supabase:{rest:{base:'https://example.test/rest/v1',key:'test-app-key',accessToken:'test-user-jwt',memberId:member}}});
    assert.equal(r.backend,'supabase');
    assert.ok(url.includes('member_id=eq.'+member));
    assert.equal(headers.Authorization,'Bearer test-user-jwt');
    assert.equal(headers.apikey,'test-app-key');
  } finally {global.fetch=old;}
});
test('no user session means no REST traffic or false success', async () => {
  let hits=0;
  const old=global.fetch;
  try {
    global.fetch=async()=>{hits++;return{ok:true,json:async()=>[]};};
    const r=await bridge.getNotes({supabase:{rest:{base:'https://example.test/rest/v1',key:'test-app-key',memberId:member}}});
    assert.equal(hits,0);
    assert.equal(r.backend,'none');
    assert.match(r.reason,/AUTHENTICATED_REST_SESSION_REQUIRED/);
  } finally {global.fetch=old;}
});
test('writes require owner identity and readback to be successful', async () => {
  let statements=[];
  const note={nutshell:'Sample',human_note:'Human',naya_note:'Naya',machine_note:{}};
  const denied=await bridge.persist('SN-TEST',note,{supabase:{query:async q=>{statements.push(q);return[];}}});
  assert.equal(denied.stored,false);
  assert.equal(statements.length,0);
  const pending=await bridge.persist('SN-TEST',note,{supabase:{memberId:member,query:async q=>{
    statements.push(q);
    return q.startsWith('INSERT') ? [{id:'test-record-id'}] : [];
  }}});
  assert.equal(pending.stored,false);
  assert.ok(statements.some(q=>q.startsWith('INSERT')&&q.includes("'"+member+"'")));
  assert.match(pending.reason,/verify-read returned no row/);
});
test('authenticated REST write only succeeds after matching readback', async () => {
  let posted=null;let calls=[];
  const old=global.fetch;
  try {
    global.fetch=async(url,opts)=>{
      calls.push({url,opts});
      if(opts.method==='POST'){
        posted=JSON.parse(opts.body);
        return{ok:true,json:async()=>[{id:'test-row'}]};
      }
      return{ok:true,json:async()=>[{id:'test-row',subject:posted.subject,source_context:posted.source_context,privacy_state:posted.privacy_state,status:posted.status}]};
    };
    const r=await bridge.persist('SN-PROOF',{nutshell:'Trial',human_note:'Human',naya_note:'Naya',machine_note:{key:'value'}},{supabase:{rest:{base:'https://example.test/rest/v1',key:'test-app-key',accessToken:'test-user-jwt',memberId:member}}});
    assert.equal(r.stored,true);
    assert.equal(r.read_back_ok,true);
    assert.equal(posted.member_id,member);
    assert.equal(calls.length,2);
    assert.equal(calls[0].opts.headers.Authorization,'Bearer test-user-jwt');
  } finally {global.fetch=old;}
});
test('unscoped browser queue URL cannot become a live Smart Feed', async () => {
  const oldWindow=global.window, oldDocument=global.document, oldFetch=global.fetch;
  const path=require.resolve('./supabase-bridge.js');
  let hits=0;
  try {
    global.window={NayaBridgeConfig:{queueUrl:'https://example.test/unscoped-queue'}};
    global.document={};
    global.fetch=async()=>{hits++;return{ok:true,text:async()=>'{}'};};
    delete require.cache[path]; require(path);
    assert.equal(typeof global.window.NayaPowerRuntime.smartFeed,'function');
    const result=await global.window.NayaPowerRuntime.smartFeed({});
    assert.equal(result.ok,false);
    assert.equal(result.state,'not_verified');
    assert.equal(hits,0);
  } finally {
    delete require.cache[path];
    if(oldWindow===undefined)delete global.window;else global.window=oldWindow;
    if(oldDocument===undefined)delete global.document;else global.document=oldDocument;
    global.fetch=oldFetch;
  }
});
