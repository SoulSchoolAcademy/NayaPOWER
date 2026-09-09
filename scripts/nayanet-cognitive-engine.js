/* NayaNET Cognitive Engine — V1
 * Persistent-by-design client cognition layer for the Intelligent Hub.
 * No secrets. No destructive migration. Safe to embed once.
 */
(function(global){
  'use strict';
  const VERSION='1.0.0';
  const NS='nayanet:cognition:v1';
  const MAX_EVENTS=5000;
  const clean=v=>String(v??'').trim();
  const now=()=>new Date().toISOString();
  const uid=(p='evt')=>p+'_'+Date.now().toString(36)+'_'+Math.random().toString(36).slice(2,10);
  const safeRead=()=>{try{return JSON.parse(localStorage.getItem(NS)||'{}')}catch{return{}}};
  const safeWrite=s=>{try{localStorage.setItem(NS,JSON.stringify(s));return true}catch{return false}};
  const shaLike=s=>{let h=2166136261;for(let i=0;i<s.length;i++){h^=s.charCodeAt(i);h=Math.imul(h,16777619)}return('00000000'+(h>>>0).toString(16)).slice(-8)};
  const classify=(text='')=>{const t=text.toLowerCase();if(/bug|error|fail|broken|fix|test/.test(t))return'failure';if(/decision|choose|approved|agree|law|rule/.test(t))return'decision';if(/idea|imagine|could|vision|create|build/.test(t))return'idea';if(/todo|task|next|implement|ship/.test(t))return'action';if(/learn|research|explain|knowledge/.test(t))return'knowledge';return'observation'};
  const normalize=(input={})=>{const content=clean(input.content||input.text||input.title);const t=now();return{event_id:input.event_id||uid(),created_at:input.created_at||t,updated_at:t,type:input.type||'intelligence',classification:input.classification||classify(content),content,title:clean(input.title)||content.slice(0,100),source:clean(input.source)||'nayanet-hub',project:clean(input.project)||'NayaNET',status:input.status||'active',actor:input.actor||'human',confidence:Number.isFinite(input.confidence)?input.confidence:1,tags:Array.isArray(input.tags)?input.tags:[],parent_event_id:input.parent_event_id||null,source_hash:shaLike(content),schema_version:VERSION,receipt_id:input.receipt_id||uid('rcpt')}};
  function read(){const s=safeRead();s.events=Array.isArray(s.events)?s.events:[];s.receipts=Array.isArray(s.receipts)?s.receipts:[];s.successor=s.successor||null;s.index=s.index||{};return s}
  function commit(s){s.events=s.events.slice(-MAX_EVENTS);s.index=buildIndex(s.events);safeWrite(s);return s}
  function buildIndex(events){const idx={byType:{},byProject:{},byClass:{},byStatus:{},bySource:{},byDay:{}};events.forEach(e=>{[['byType',e.type],['byProject',e.project],['byClass',e.classification],['byStatus',e.status],['bySource',e.source],['byDay',(e.created_at||'').slice(0,10)]].forEach(([bucket,key])=>{key=clean(key)||'unknown';(idx[bucket][key]||(idx[bucket][key]=[])).push(e.event_id)})});return idx}
  function receipt(event,action='record'){return{receipt_id:event.receipt_id||uid('rcpt'),event_id:event.event_id,action,at:now(),source:event.source,source_hash:event.source_hash,schema_version:VERSION,verified:true}}
  const api={
    version:VERSION,
    record(input){const s=read();const e=normalize(input);const duplicate=s.events.find(x=>x.source_hash===e.source_hash&&x.project===e.project&&x.classification===e.classification&&Math.abs(new Date(x.created_at)-new Date(e.created_at))<5000);if(duplicate)return{event:duplicate,receipt:receipt(duplicate,'deduplicated'),deduplicated:true};s.events.push(e);s.receipts.push(receipt(e));commit(s);return{event:e,receipt:s.receipts.at(-1),deduplicated:false}},
    search(query='',filters={}){const s=read();const q=clean(query).toLowerCase();return s.events.filter(e=>{if(filters.type&&e.type!==filters.type)return false;if(filters.project&&e.project!==filters.project)return false;if(filters.classification&&e.classification!==filters.classification)return false;if(filters.status&&e.status!==filters.status)return false;if(filters.source&&e.source!==filters.source)return false;if(filters.from&&e.created_at<filters.from)return false;if(filters.to&&e.created_at>filters.to)return false;if(!q)return true;return [e.title,e.content,e.project,e.source,e.classification,...e.tags].join(' ').toLowerCase().includes(q)}).sort((a,b)=>b.created_at.localeCompare(a.created_at))},
    handoff(reason='successor-session'){const s=read();const recent=s.events.slice(-25).map(e=>({event_id:e.event_id,title:e.title,classification:e.classification,project:e.project,status:e.status,created_at:e.created_at,source:e.source}));s.successor={handoff_id:uid('handoff'),created_at:now(),reason,recent,open_count:s.events.filter(e=>e.status==='active').length,last_event_id:s.events.at(-1)?.event_id||null,schema_version:VERSION};safeWrite(s);return s.successor},
    getSuccessor(){return read().successor},
    stats(){const s=read();return{version:VERSION,events:s.events.length,receipts:s.receipts.length,projects:new Set(s.events.map(e=>e.project)).size,last_event:s.events.at(-1)?.created_at||null,indexed:true}},
    verify(){const s=read();const valid=s.events.every(e=>e.event_id&&e.created_at&&e.schema_version&&e.source_hash);return{valid,events:s.events.length,receipts:s.receipts.length,indexed:Object.keys(s.index.byDay||{}).length>0}},
    optimize(){const s=read();const before=s.events.length;const seen=new Set();s.events=s.events.filter(e=>{const k=e.source_hash+'|'+e.project+'|'+e.classification;if(seen.has(k))return false;seen.add(k);return true});commit(s);return{before,after:s.events.length,removed:before-s.events.length}},
    export(){return JSON.stringify(read(),null,2)},
    clear(){localStorage.removeItem(NS)}
  };
  global.NayaNetCognition=api;
  global.dispatchEvent(new CustomEvent('nayanet:cognition-ready',{detail:api}));
})(window);
