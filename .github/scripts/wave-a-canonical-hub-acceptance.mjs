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
page.on("console",m=>{if(m.type()==="error")consoleErrors.push(m.text())});
page.on("pageerror",e=>consoleErrors.push(String(e)));

await page.goto(runtime+"/?wave_a=canonical",{waitUntil:"networkidle",timeout:60000});
await page.waitForFunction(()=>!!window.NayaAssistantRuntime,{timeout:30000});

const shell=await page.evaluate(()=>({
  title:document.title,
  directNine:document.querySelector('meta[name="nayanet-direct-nine"]')?.content||null,
  reactMarker:document.documentElement.innerHTML.includes("NAYANET-HUB-REACT-CANONICAL"),
  welcome:document.body.innerText.includes("welcome.nayanet.app"),
  nav:[...document.querySelectorAll("button[data-nc]")].map(b=>({kind:b.dataset.nc,text:b.innerText.replace(/\s+/g," ").trim()})),
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
const required=["feed","note","reports","share","lists","spaces","connections","mail","ledger","dream","play","settings"];
if(shell.nav.filter(x=>required.includes(x.kind)).length<12) throw new Error("CANONICAL_HUB_NAV_INCOMPLETE");
if(!shell.search) throw new Error("CANONICAL_HUB_SEARCH_MISSING");
for(const [k,v] of Object.entries(shell.runtime)) if(v!=="function") throw new Error("RUNTIME_CONTRACT_MISSING:"+k);

const auth=await page.evaluate(()=>window.NayaAssistantRuntime.init());
if(!auth.authenticated||auth.user_id!==A.user.id) throw new Error("BROWSER_AUTH_HANDOFF_FAILED");

const title="Wave A canonical Smart Note "+Date.now();
const content="Protected approved Hub browser proof "+crypto.randomUUID()+" — Smart Note must become one canonical event, persist, retrieve, and survive reload.";
const noteButton=page.locator('button[data-nc="note"]').first();
await noteButton.click();
const dialog=page.locator(".nc-modal").last();
await dialog.waitFor({state:"visible",timeout:10000});
await dialog.locator("#nc-title").fill(title);
await dialog.locator("#nc-content").fill(content);
await dialog.locator("#nc-save").click();
await page.waitForFunction(()=>/PERSISTED · EVENT [^ ·]+ · RECEIPT /.test(document.querySelector(".nc-modal #nc-state")?.textContent||""),null,{timeout:30000});
const noteState=await dialog.locator("#nc-state").textContent();
const eventId=noteState.match(/EVENT ([^ ·]+)/)?.[1]||"";
const receiptId=noteState.match(/RECEIPT ([^ ·]+)/)?.[1]||"";
if(!eventId||!receiptId) throw new Error("SMART_NOTE_RECEIPT_NOT_PROVEN:"+noteState);

const runtimeFeed=await page.evaluate(()=>window.NayaAssistantRuntime.smartFeed({stream:"personal",limit:50}));
const items=Array.isArray(runtimeFeed?.items)?runtimeFeed.items:[];
const exact=items.find(x=>x.event_id===eventId);
if(!exact) throw new Error("SMART_NOTE_EVENT_NOT_IN_PERSONAL_SMART_FEED:"+JSON.stringify(items.map(x=>({event_id:x.event_id,title:x.title,source:x.source}))));

await dialog.locator("[data-nc-close]").click();
await page.locator('button[data-nc="feed"]').first().click();
const feedDialog=page.locator(".nc-modal").last();
await feedDialog.waitFor({state:"visible",timeout:10000});
await page.waitForFunction(()=>/LIVE · PERSONAL · \d+ ITEMS · CANONICAL RUNTIME/.test(document.querySelector(".nc-modal #nc-state")?.textContent||""),null,{timeout:30000});
const feedText=await feedDialog.locator("#nc-feed").innerText();
if(!feedText.includes(title)) throw new Error("SMART_FEED_DOM_PROJECTION_MISSING:"+feedText.slice(0,2000));

await page.reload({waitUntil:"networkidle"});
await page.waitForFunction(()=>!!window.NayaAssistantRuntime,{timeout:30000});
const reloaded=await page.evaluate(()=>window.NayaAssistantRuntime.smartFeed({stream:"personal",limit:50}));
const reloadedItems=Array.isArray(reloaded?.items)?reloaded.items:[];
const same=reloadedItems.find(x=>x.event_id===eventId);
if(!same) throw new Error("SMART_NOTE_EVENT_NOT_RETRIEVED_AFTER_RELOAD");
if(same.event_id!==eventId) throw new Error("SMART_NOTE_EVENT_ID_CHANGED_AFTER_RELOAD");
const postReloadAuth=await page.evaluate(()=>window.NayaAssistantRuntime.init());
if(!postReloadAuth.authenticated||postReloadAuth.user_id!==A.user.id) throw new Error("AUTHORITY_CHANGED_AFTER_RELOAD");

const receipt={status:"VERIFIED",hub:{title:shell.title,directNine:shell.directNine,react:false,welcome:false,navCount:shell.nav.length,search:true},identity:{user_id:A.user.id},smartNote:{title,content,event_id:eventId,receipt_id:receiptId},smartFeed:{initial_match:true,dom_projection:true,reload_match:true,same_event_id:true},consoleErrors};
fs.writeFileSync(process.env.RECEIPT_PATH||"wave-a-canonical-receipt.json",JSON.stringify(receipt,null,2));
console.log("WAVE_A_CANONICAL_HUB_SMART_NOTE_PROOF_VERIFIED",JSON.stringify(receipt));
await browser.close();
