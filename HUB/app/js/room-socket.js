/* ROOM SOCKET — the single projection seam every Hub room uses.
   It carries context into the governed runtime and records UI-side lifecycle evidence only. */
(function(){
  'use strict';
  const R=window.NayaRuntime;
  const C=window.NayaRoomContract;
  if(!R||!C) throw new Error('Room socket requires runtime + room contract.');
  const trace=[];
  let active=null;
  const MAX_TRACE=80;
  function record(op,roomId,detail={}){
    trace.push(Object.freeze({op,room_id:roomId,at:new Date().toISOString(),...detail}));
    if(trace.length>MAX_TRACE) trace.splice(0,trace.length-MAX_TRACE);
  }
  function contract(roomId){
    const found=C.get(roomId);
    if(!found) throw new Error('Unknown NayaNET room: '+roomId);
    return found;
  }
  function context(roomId,extra={}){
    const c=contract(roomId);
    return Object.freeze({
      room_id:c.id,
      route:c.route,
      mode:R.mode||null,
      identity:R.identitySnapshot?.()||{state:'not_verified',display_name:'You'},
      authority:{model:'runtime-governed',assumed:false},
      ...extra
    });
  }
  function enter(roomId,extra={}){
    const next=contract(roomId);
    const previous=active?.room_id||null;
    active=Object.freeze({room_id:next.id,route:next.route,entered_at:new Date().toISOString(),previous_room_id:previous});
    record('enter',next.id,{previous_room_id:previous});
    return Object.freeze({contract:next,context:context(next.id,extra),lifecycle:active});
  }
  function leave(roomId,reason='navigation'){
    if(active?.room_id===roomId){
      record('leave',roomId,{reason});
      active=null;
    }
  }
  async function query(roomId,payload={}){
    const c=contract(roomId);
    const roomContext=context(roomId);
    record('query',roomId,{query:c.primary_intelligence_query});
    return R.roomData(c.id,{...payload,room_context:roomContext});
  }
  async function search(roomId,queryText,opts={}){
    contract(roomId);
    record('search',roomId,{has_query:!!String(queryText||'').trim()});
    return R.search(queryText,{...opts,room_context:context(roomId)});
  }
  async function retrieve(roomId,id){
    contract(roomId);
    record('retrieve',roomId,{canonical_id:String(id||'')});
    return R.retrieve(id);
  }
  async function act(roomId,payload={}){
    const c=contract(roomId);
    record('act',roomId,{canonical_id:String(payload.id||payload.intelligent_block_id||''),authority:c.authority_requirements});
    return R.performIntelligenceAction({...payload,room_context:context(roomId)});
  }
  const socket=Object.freeze({
    schema:'nayanet.hub.room-socket.v1',
    version:'1.0.0',
    registry:()=>C.list(),
    contract,
    context,
    enter,
    leave,
    query,
    search,
    retrieve,
    act,
    active:()=>active,
    trace:()=>trace.slice()
  });
  R.roomSocket=socket;
  window.NayaRoomSocket=socket;
})();