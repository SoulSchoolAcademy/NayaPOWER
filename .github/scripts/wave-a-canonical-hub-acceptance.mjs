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
  let b; try{b=JSON.parse(t)}catch{b={raw:t}}
  if(!r.ok) throw new Error(r.status+" "+JSON.stringify(b));
  return b;
}

const signup=()=>req(base+"/auth/v1/signup",{
  method:"POST",
  headers:{apikey:key,"content-type":"application/json"},
  body:"{}"
});

const A=await signup();
if(!A.access_token||!A.user?.id) throw new Error("AUTH_BOOTSTRAP_FAILED");

const browser=await chromium.launch({headless:true});
const origin=new URL(runtime).origin;
const storageState={cookies:[],origins:[{origin,localStorage:[{name:"nayanet.supabase.auth",value:JSON.stringify(A)}]}]};
const ctx=await browser.newContext({storageState,viewport:{width:1440,height:1000}});
const page=await ctx.newPage();
const consoleErrors=[];
page.on("console",m=>{if(m.type()==="error")consoleErrors.push(m.text())});
page.on("pageerror",e=>consoleErrors.push(String(e)));
page.on("response",r=>{
  if(r.url().includes("/functions/v1/naya-smart-feed")) console.log("SMART_FEED_RESPONSE",r.status(),r.url());
});
page.on("requestfailed",r=>{
  if(r.url().includes("/functions/v1/naya-smart-feed")) console.log("SMART_FEED_REQUEST_FAILED",r.failure()?.errorText||"unknown",r.url());
});

await page.goto(runtime+"/?wave_a=canonical-current",{waitUntil:"domcontentloaded",timeout:60000});
await page.waitForFunction(()=>!!window.NayaAssistantRuntime,{timeout:30000});

const shell=await page.evaluate(()=>({
  title:document.title,
  directNine:document.querySelector('meta[name="nayanet-direct-nine"]')?.content||null,
  reactMarker:document.documentElement.innerHTML.includes("NAYANET-HUB-REACT-CANONICAL"),
  welcome:document.body.innerText.includes("welcome.nayanet.app"),
  search:!!document.querySelector("#search.search"),
  nav:[...document.querySelectorAll(".rail.left [data-page]")].map(x=>({page:x.dataset.page,text:x.innerText.replace(/\s+/g," ").trim()})),
  feed:[...document.querySelectorAll(".feedNav button")].map(x=>({feed:x.dataset.feed,text:x.innerText.trim(),active:x.classList.contains("active")})),
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
const required=["home","notes","reports","intelligence","collective","evidence","connections","mail","settings"];
for(const kind of required) if(!shell.nav.some(x=>x.page===kind)) throw new Error("CANONICAL_HUB_NAV_MISSING:"+kind);
if(shell.feed.length!==3) throw new Error("CANONICAL_FEED_NAV_INCOMPLETE:"+JSON.stringify(shell.feed));
if(!shell.search) throw new Error("CANONICAL_HUB_SEARCH_MISSING");
for(const [k,v] of Object.entries(shell.runtime)) if(v!=="function") throw new Error("RUNTIME_CONTRACT_MISSING:"+k);

const auth=await page.evaluate(()=>window.NayaAssistantRuntime.init());
if(!auth.authenticated||auth.user_id!==A.user.id) throw new Error("BROWSER_AUTH_HANDOFF_FAILED");

const navChecks={};
for(const kind of ["reports","intelligence","evidence","connections","mail","settings"]){
  await page.locator('.rail.left [data-page="'+kind+'"]').click();
  await page.locator(".naya-functional-backdrop").waitFor({state:"visible",timeout:10000});
  const heading=await page.locator(".naya-functional-panel h2").textContent();
  navChecks[kind]=heading;
  await page.locator(".naya-functional-panel [data-close]").click();
}
await page.locator('.rail.left [data-page="home"]').click();

await page.locator('.rail.left [data-page="notes"]').click();
await page.locator(".naya-functional-backdrop").waitFor({state:"visible",timeout:10000});
await page.locator("#fn-title").fill("Wave A canonical Smart Note "+Date.now());
const title=await page.locator("#fn-title").inputValue();
const content="Protected canonical Hub acceptance "+crypto.randomUUID()+" — Smart Note must persist through the governed receiver, appear in Smart Feed, survive reload, and remain retrievable.";
await page.locator("#fn-content").fill(content);
const loadPromise=page.waitForEvent("load",{timeout:30000});
await page.locator("#fn-save").click();
await page.locator("#fn-status").waitFor({state:"visible",timeout:10000});
await page.waitForFunction(()=>/CAPTURED — /.test(document.querySelector("#fn-status")?.textContent||""),null,{timeout:30000});
const statusBeforeReload=await page.locator("#fn-status").textContent();
const eventId=statusBeforeReload.match(/CAPTURED — ([^\s]+)/)?.[1]||"";
if(!eventId) throw new Error("SMART_NOTE_EVENT_ID_MISSING:"+statusBeforeReload);
await loadPromise.catch(()=>{});
await page.waitForTimeout(700);
await page.waitForFunction(()=>!!window.NayaAssistantRuntime,{timeout:30000});

const apiInitial=await page.evaluate(()=>window.NayaAssistantRuntime.smartFeed({stream:"personal",limit:50}));
const initialItems=Array.isArray(apiInitial?.items)?apiInitial.items:[];
const apiExact=initialItems.find(x=>String(x?.event_id||x?.id||"")===eventId);
if(!apiExact) throw new Error("SMART_FEED_RUNTIME_API_PROJECTION_MISSING:"+JSON.stringify(initialItems.slice(0,10).map(x=>({event_id:x.event_id,id:x.id,title:x.title}))));
if(!apiExact.metadata?.intelligent_block_v1) throw new Error("SMART_FEED_INTELLIGENT_BLOCK_METADATA_MISSING");

const personal=page.locator('.feedNav button[data-feed="personal"]');
await personal.click();
await page.waitForFunction(()=>document.documentElement.dataset.nayaCanonicalSmartFeed==="live",{timeout:30000});
await page.waitForFunction(id=>[...document.querySelectorAll(".blocks .block")].some(b=>String(b.dataset.intelligenceId||"")===id),eventId,{timeout:30000});

const rendered=await page.locator('.blocks .block').filter({hasText:title}).first().evaluate(node=>({
  intelligenceId:node.dataset.intelligenceId||"",
  feed:node.dataset.nayaFeed||"",
  provenance:node.dataset.provenance||"",
  title:node.querySelector("h3")?.textContent||"",
  truth:node.querySelector(".truth")?.textContent||"",
  nutshell:node.querySelector(".nutshell p")?.textContent||""
}));
if(rendered.intelligenceId!==eventId||rendered.feed!=="personal"||rendered.provenance!=="Canonical runtime"||!rendered.title.includes(title)||!rendered.truth) throw new Error("SMART_FEED_CANONICAL_DOM_PROJECTION_FAILED:"+JSON.stringify(rendered));

for(const stream of ["collective","activity","personal"]){
  await page.locator('.feedNav button[data-feed="'+stream+'"]').click();
  await page.waitForFunction(expected=>[...document.querySelectorAll(".feedNav button")].some(b=>b.dataset.feed===expected&&b.classList.contains("active")),stream,{timeout:10000});
  await page.waitForFunction(()=>document.documentElement.dataset.nayaCanonicalSmartFeed==="live",{timeout:30000});
}

await page.reload({waitUntil:"networkidle"});
await page.waitForFunction(()=>!!window.NayaAssistantRuntime,{timeout:30000});
await page.locator('.feedNav button[data-feed="personal"]').click();
await page.waitForFunction(id=>[...document.querySelectorAll(".blocks .block")].some(b=>String(b.dataset.intelligenceId||"")===id),eventId,{timeout:30000});

const recovered=await page.evaluate(async expected=>{
  const rows=await window.NayaAssistantRuntime.retrieve(expected);
  return rows?.find(x=>String(x?.event_id||x?.id||"")===expected)||null;
},eventId);
if(!recovered||String(recovered.event_id||recovered.id||"")!==eventId||!recovered.metadata?.intelligent_block_v1) throw new Error("AUTHORIZED_CONTINUATION_RETRIEVAL_FAILED");

const postReloadAuth=await page.evaluate(()=>window.NayaAssistantRuntime.init());
if(!postReloadAuth.authenticated||postReloadAuth.user_id!==A.user.id) throw new Error("AUTHORITY_CHANGED_AFTER_RELOAD");

const receipt={
  status:"VERIFIED",
  source:"canonical static Hub",
  hub:{title:shell.title,directNine:shell.directNine,react:false,welcome:false,navCount:shell.nav.length,feedModes:shell.feed.map(x=>x.feed),search:true},
  sidebar:navChecks,
  identity:{user_id:A.user.id},
  smartNote:{title,content,event_id:eventId,status:statusBeforeReload},
  smartFeed:{api_match:true,intelligent_block_metadata:true,dom_projection:true,three_mode_switch:true,reload_match:true,retrieval_match:true,same_event_id:true},
  consoleErrors
};
fs.writeFileSync(process.env.RECEIPT_PATH||"wave-a-canonical-receipt.json",JSON.stringify(receipt,null,2));
console.log("WAVE_A_CANONICAL_HUB_SMART_NOTE_PROOF_VERIFIED",JSON.stringify(receipt));
await browser.close();
