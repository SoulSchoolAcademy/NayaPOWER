import { chromium } from "playwright";
import crypto from "node:crypto";
import fs from "node:fs";

const base=process.env.SUPABASE_URL;
const key=process.env.SUPABASE_PUBLISHABLE_KEY || "sb_publishable_oQFKOYFuJ9bT-E9QkJUb4g_lAUyInue";
const runtime=process.env.RUNTIME_URL;
if(!base||!key||!runtime) throw new Error("WAVE_A_ENV_MISSING");

async function req(url,opt={}) {
  const r=await fetch(url,opt);
  const t=await r.text();
  let b; try { b=JSON.parse(t) } catch { b={raw:t} }
  if(!r.ok) throw new Error(r.status+" "+JSON.stringify(b));
  return b;
}
const signup=()=>req(base+"/auth/v1/signup",{method:"POST",headers:{apikey:key,"content-type":"application/json"},body:"{}"});
const A=await signup();
if(!A.access_token||!A.user?.id) throw new Error("AUTH_BOOTSTRAP_FAILED");

const browser=await chromium.launch({headless:true});
const origin=new URL(runtime).origin;
const storageState={cookies:[],origins:[{origin,localStorage:[{name:"nayanet.supabase.auth",value:JSON.stringify(A)}]}]};
const ctx=await browser.newContext({storageState});
const page=await ctx.newPage();
const consoleErrors=[];
page.on("response",r=>{if(r.url().includes("/functions/v1/naya-smart-feed"))console.log("SMART_FEED_RESPONSE",r.status(),r.headers()["content-type"]||"",r.url())});
page.on("requestfailed",r=>{if(r.url().includes("/functions/v1/naya-smart-feed"))console.log("SMART_FEED_REQUEST_FAILED",r.failure()?.errorText||"unknown",r.url())});
page.on("console",m=>{if(m.type()==="error")consoleErrors.push(m.text())});
page.on("pageerror",e=>consoleErrors.push(String(e)));

await page.goto(runtime+"/?wave_a=canonical",{waitUntil:"domcontentloaded",timeout:60000});
await page.waitForFunction(()=>!!window.NayaAssistantRuntime,{timeout:30000});

const shell=await page.evaluate(()=>({
  title:document.title,
  directNine:document.querySelector('meta[name="nayanet-direct-nine"]')?.content||null,
  reactMarker:document.documentElement.innerHTML.includes("NAYANET-HUB-REACT-CANONICAL"),
  welcome:document.body.innerText.includes("welcome.nayanet.app"),
  nav:[...document.querySelectorAll("button[data-naya-surface]")].map(b=>({kind:b.dataset.nayaSurface,text:b.innerText.replace(/\s+/g," ").trim()})),
  search:!!document.querySelector("#search.search"),
  runtime:{
    init:typeof window.NayaAssistantRuntime?.init,
    smartFeed:typeof window.NayaAssistantRuntime?.smartFeed,
    captureSmartNote:typeof window.NayaAssistantRuntime?.captureSmartNote,
    retrieve:typeof window.NayaAssistantRuntime?.retrieve
  }
}));
if(shell.title!=="NayaNET — Intelligent Hub V7 · 509 AAA") throw new Error("CANONICAL_HUB_TITLE_MISMATCH:"+shell.title);
if(shell.directNine!=="verified-static-top-nine") throw new Error("CANONICAL_HUB_MARKER_MISSING");
if(shell.reactMarker) throw new Error("OBSOLETE_REACT_HUB_PRESENT");
if(shell.welcome) throw new Error("WELCOME_FRONT_DOOR_SELECTED_AS_HUB");
const required=["feed","today","reports","library","share","lists","spaces","connections","mail","ledger","dream","play","settings"];
if(shell.nav.filter(x=>required.includes(x.kind)).length<12) throw new Error("CANONICAL_HUB_NAV_INCOMPLETE");
if(!shell.search) throw new Error("CANONICAL_HUB_SEARCH_MISSING");
for(const [k,v] of Object.entries(shell.runtime)) if(v!=="function") throw new Error("RUNTIME_CONTRACT_MISSING:"+k);

const auth=await page.evaluate(()=>window.NayaAssistantRuntime.init());
if(!auth.authenticated||auth.user_id!==A.user.id) throw new Error("BROWSER_AUTH_HANDOFF_FAILED");

const title="Wave A canonical Smart Note "+Date.now();
const content="Protected approved Hub browser proof "+crypto.randomUUID()+" — Smart Note must become one canonical event, persist, retrieve, and survive reload.";
const captureButton=page.locator('[data-testid="capture-smart-note"]').first();
if(!(await captureButton.count())) throw new Error("CANONICAL_CAPTURE_BUTTON_MISSING");
await captureButton.click();
const captureTitle=page.locator('#nayaCaptureTitle');
const captureContent=page.locator('#nayaCaptureContent');
const captureSubmit=page.locator('#nayaCaptureSubmit');
const captureStatus=page.locator('[data-testid="smart-note-capture-status"]');
await captureTitle.fill(title); await captureContent.fill(content); await captureSubmit.click();
await page.waitForFunction(()=>/CAPTURED · PERSISTED · EVENT [^ ·]+ · RECEIPT /.test(document.querySelector('[data-testid="smart-note-capture-status"]')?.textContent||''),null,{timeout:30000});
const noteState=await captureStatus.textContent();
const eventId=noteState.match(/EVENT ([^ ·]+)/)?.[1]||"";
const receiptId=noteState.match(/RECEIPT ([^ ·]+)/)?.[1]||"";
if(!eventId||!receiptId) throw new Error("SMART_NOTE_RECEIPT_NOT_PROVEN:"+noteState);
await page.waitForURL(url=>url.pathname==="/feed" && url.searchParams.get("event_id")===eventId,{timeout:30000});
await page.waitForSelector('[data-event-id="'+eventId+'"]',{timeout:30000});
const rendered=await page.locator('[data-event-id="'+eventId+'"]').evaluate(node=>({eventId:node.getAttribute("data-event-id"),title:node.querySelector("h2")?.textContent||"",schema:node.getAttribute("data-intelligent-block-schema"),blockEventId:node.getAttribute("data-intelligent-block-event-id"),truth:node.getAttribute("data-intelligent-block-truth"),authority:node.getAttribute("data-intelligent-block-authority"),privacy:node.getAttribute("data-intelligent-block-privacy"),lifecycle:node.getAttribute("data-intelligent-block-lifecycle"),hash:node.getAttribute("data-intelligent-block-hash")}));
if(rendered.eventId!==eventId||!String(rendered.title||"").includes(title)) throw new Error("SMART_FEED_DOM_PROJECTION_MISSING:"+JSON.stringify(rendered));
if(rendered.schema!=="NAYANET_INTELLIGENT_BLOCK_V1"||rendered.blockEventId!==eventId||rendered.truth!=="VERIFIED"||rendered.authority!=="AUTHORIZED"||rendered.privacy!=="PRIVATE"||rendered.lifecycle!=="VERIFIED") throw new Error("SMART_FEED_INTELLIGENT_BLOCK_EVIDENCE_MISSING:"+JSON.stringify(rendered));
await page.reload({waitUntil:"networkidle"});
await page.waitForSelector('[data-event-id="'+eventId+'"]',{timeout:30000});
const restored=await page.locator('[data-event-id="'+eventId+'"]').evaluate(node=>({eventId:node.getAttribute("data-event-id"),title:node.querySelector("h2")?.textContent||"",schema:node.getAttribute("data-intelligent-block-schema"),blockEventId:node.getAttribute("data-intelligent-block-event-id")}));
if(restored.eventId!==eventId||restored.blockEventId!==eventId||restored.schema!=="NAYANET_INTELLIGENT_BLOCK_V1") throw new Error("SMART_FEED_RELOAD_IDENTITY_FAILED:"+JSON.stringify(restored));
await page.waitForFunction(()=>!!window.NayaAssistantRuntime,{timeout:30000});
const recovered=await page.evaluate(async({expected})=>{const rows=await window.NayaAssistantRuntime.retrieve(expected);return rows?.find(x=>x?.event_id===expected)||null},{expected:eventId});
if(!recovered||recovered.event_id!==eventId||!recovered.metadata?.intelligent_block_v1) throw new Error("AUTHORIZED_CONTINUATION_RETRIEVAL_FAILED:"+JSON.stringify(recovered));
const postReloadAuth=await page.evaluate(()=>window.NayaAssistantRuntime.init());
if(!postReloadAuth.authenticated||postReloadAuth.user_id!==A.user.id) throw new Error("AUTHORITY_CHANGED_AFTER_RELOAD");

const receipt={status:"VERIFIED",hub:{title:shell.title,directNine:shell.directNine,react:false,welcome:false,navCount:shell.nav.length,search:true},identity:{user_id:A.user.id},smartNote:{title,content,event_id:eventId,receipt_id:receiptId},smartFeed:{initial_match:true,dom_projection:true,reload_match:true,same_event_id:true},consoleErrors};
fs.writeFileSync(process.env.RECEIPT_PATH||"wave-a-canonical-receipt.json",JSON.stringify(receipt,null,2));
console.log("WAVE_A_CANONICAL_HUB_SMART_NOTE_PROOF_VERIFIED",JSON.stringify(receipt));
await browser.close();
