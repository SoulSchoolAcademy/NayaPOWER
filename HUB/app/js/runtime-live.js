/* LIVE RUNTIME ADAPTER
   Compatibility seam over an injected governed runtime. The UI never assumes
   a method exists, and never upgrades missing data into READY. */
(function(){
  const R=window.NayaRuntime;
  if(!R) throw new Error('NayaRuntime base must load before runtime-live.js');

  const METHOD_MAP={
    feed:['smartFeed'],
    today:['intelligenceToday','dailyIntelligence','today'],
    reports:['smartReports','reports','intelligenceReports'],
    library:['intelligentLibrary','library','knowledgeLibrary'],
    ledger:['smartLedger','ledger','executionLedger'],
    connections:['smartConnections','connections','relationshipIntelligence'],
    lists:['smartLists','lists','intelligenceLists'],
    mail:['smartMail','mail','messages'],
    spaces:['smartSpaces','spaces','contextSpaces'],
    settings:['settingsSnapshot','runtimeSnapshot']
  };

  function bridge(){
    const candidates=[window.NayaAssistantRuntime,window.NayaPowerRuntime,window.NayaRuntimeBridge];
    return candidates.find(x=>x&&x!==R)||null;
  }

  function methodNames(){
    const b=bridge(); if(!b) return[];
    const own=Object.keys(b).filter(k=>typeof b[k]==='function');
    const proto=Object.getPrototypeOf(b);
    const inherited=proto?Object.getOwnPropertyNames(proto).filter(k=>k!=='constructor'&&typeof b[k]==='function'):[];
    return [...new Set([...own,...inherited])];
  }

  async function invoke(candidates,payload){
    const b=bridge();
    if(!b) return {ok:false,state:'not_verified',message:'The governed Hub runtime is not connected in this browser session.',runtime_connected:false};
    const name=candidates.find(n=>typeof b[n]==='function');
    if(!name){
      return {ok:false,state:'not_verified',message:'The runtime is connected, but this room capability is not exposed yet.',runtime_connected:true,available_methods:methodNames()};
    }
    try{
      const out=await b[name](payload);
      if(out==null) return {ok:true,state:'empty',data:[],method:name,runtime_connected:true};
      if(out?.ok===false) return {...out,method:name,runtime_connected:true,state:out.state||'error'};
      return {ok:true,state:out?.state||'ready',data:out?.data??out,method:name,runtime_connected:true,raw:out};
    }catch(err){
      return {ok:false,state:'error',message:err?.message||('Runtime method '+name+' failed.'),method:name,runtime_connected:true};
    }
  }

  R.bridge=bridge;
  R.availableMethods=methodNames;
  R.roomData=async function(roomId,payload={}){
    if(roomId==='connect') return {ok:true,state:'ready',data:{doors:R.DOORS,roadmap:R.DOOR_ROADMAP},method:'registry_projection'};
    return invoke(METHOD_MAP[roomId]||[],payload);
  };

  R.search=async function(query,opts={}){
    const q=String(query||'').trim();
    if(!q) return {ok:false,state:'empty',message:'Ask a question or search the intelligence.'};
    return invoke(['searchIntelligence','askNaya','search','retrieveIntelligence'],{query:q,...opts});
  };

  R.retrieve=async function(id){
    if(!id) return {ok:false,state:'empty',message:'No canonical intelligence ID was supplied.'};
    return invoke(['retrieveIntelligentBlock','getIntelligentBlock','retrieve'],{id});
  };

  R.identitySnapshot=function(){
    const b=bridge();
    if(!b) return {state:'not_verified',display_name:'You',detail:'Identity runtime not connected'};
    const x=b.identity||b.currentIdentity||b.sessionIdentity;
    if(x&&typeof x==='object') return {
      state:x.state||x.status||'ready',
      display_name:x.display_name||x.displayName||x.name||x.alias||'You',
      detail:x.detail||x.scope||'Governed identity'
    };
    return {state:'not_verified',display_name:'You',detail:'Identity available only through the governed runtime'};
  };

  R.runtimeStatus=function(){
    const b=bridge();
    return {connected:!!b,available_methods:methodNames(),adapter_version:'2.0.0'};
  };
  R.version='2.0.0';
})();