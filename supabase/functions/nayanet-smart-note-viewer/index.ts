
import { createClient } from "npm:@supabase/supabase-js@2";

const SUPABASE_URL = Deno.env.get("SUPABASE_URL") ?? "";
const SERVICE_ROLE_KEY = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY") ?? "";
const PUBLISHABLE_KEY = "sb_publishable_oQFKOYFuJ9bT-E9QkJUb4g_lAUyInue";
const REGISTRY_URL = "https://raw.githubusercontent.com/SoulSchoolAcademy/NayaPOWER/main/.naya/memory/smart-notes/index.json";

const BASE_HEADERS = {
  "cache-control": "no-store",
  "x-content-type-options": "nosniff",
  "referrer-policy": "no-referrer",
};

function admin() {
  if (!SUPABASE_URL || !SERVICE_ROLE_KEY) throw new Error("SERVER_AUTH_CONFIG_MISSING");
  return createClient(SUPABASE_URL, SERVICE_ROLE_KEY, { auth: { persistSession: false } });
}

async function registryEntry(ib: string) {
  const response = await fetch(REGISTRY_URL, { headers: { "cache-control": "no-cache" } });
  if (!response.ok) throw new Error("SMART_NOTE_REGISTRY_UNAVAILABLE");
  const registry = await response.json();
  const entry = registry?.entries?.find((item: any) => item?.intelligent_block_id === ib);
  if (!entry) throw new Error("SMART_NOTE_NOT_REGISTERED");
  return entry;
}

async function requireViewer(req: Request) {
  const auth = req.headers.get("authorization") ?? "";
  if (!auth.startsWith("Bearer ")) throw new Error("AUTH_REQUIRED");
  const token = auth.slice(7);
  const client = admin();
  const { data, error } = await client.auth.getUser(token);
  if (error || !data?.user?.id) throw new Error("AUTH_INVALID");
  return { client, user: data.user };
}

function viewerShell(ib: string) {
  const config = JSON.stringify({ url: SUPABASE_URL, key: PUBLISHABLE_KEY, ib });
  const page = [
    "<!doctype html>",
    "<html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>",
    "<title>NayaPOWER Smart Link</title>",
    "<style>",
    "body{margin:0;background:#050507;color:#fff;font:16px/1.55 system-ui,sans-serif}main{max-width:900px;margin:32px auto;padding:16px}.card{background:#0d0b12;border:1px solid #51256f;border-radius:24px;padding:28px;box-shadow:0 0 45px #6e2e8d33}h1{font-size:2.4rem}.muted{color:#b7adc4}.pill{display:inline-block;padding:6px 10px;border:1px solid #4c375b;border-radius:999px;margin:4px}.section{margin-top:26px;padding-top:20px;border-top:1px solid #2c2333}.section h2{color:#d9b8ff;font-size:1rem;text-transform:uppercase;letter-spacing:.08em}input,button{font:inherit;padding:12px;border-radius:12px;border:1px solid #5f3b78;margin:5px}input{background:#09070d;color:#fff}button{background:#6f2d99;color:#fff;font-weight:800}.proof{white-space:pre-wrap;background:#070609;padding:14px;border-radius:12px;font-family:monospace;font-size:.82rem}.path{word-break:break-all;color:#d7b1ff}.ok{color:#46e6a0}",
    "</style></head><body><main><div class='card'>",
    "<div class='muted'>NayaPOWER · Private Smart Link</div><h1>Smart Note</h1>",
    "<div id='status'>Checking NayaNET identity…</div>",
    "<div id='auth' style='display:none' class='section'><h2>Private note · identity required</h2><p class='muted'>Authenticate with the existing email that owns your NayaNET identity.</p><input id='email' type='email' placeholder='NayaNET email'><button id='send'>Send code</button><br><span id='otpBox' style='display:none'><input id='otp' maxlength='6' placeholder='6-digit code'><button id='verify'>Verify & open</button></span><div id='authStatus' class='muted'></div></div>",
    "<div id='note' style='display:none'></div>",
    "</div></main><script src='https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2'></script>",
    "<script>window.NAYA_SMART_LINK_CONFIG=" + config + ";</script>",
    "<script>",
    "const C=window.NAYA_SMART_LINK_CONFIG;const sb=window.supabase.createClient(C.url,C.key,{auth:{persistSession:true,autoRefreshToken:true,detectSessionInUrl:true,storage:localStorage,storageKey:'nayanet.smartlink.auth'}});const E=id=>document.getElementById(id);const X=v=>{const d=document.createElement('div');d.textContent=v??'';return d.innerHTML};const S=(h,b)=>'<div class=section><h2>'+h+'</h2><div>'+b+'</div></div>';",
    "function auth(){E('status').style.display='none';E('auth').style.display='block'}",
    "async function load(){const z=await sb.auth.getSession();const s=z.data.session;if(!s){auth();return}const r=await fetch(location.pathname+'?data=1&ib='+encodeURIComponent(C.ib),{headers:{Authorization:'Bearer '+s.access_token}});if(r.status===401||r.status===403){await sb.auth.signOut();auth();return}const j=await r.json();if(!r.ok){E('status').textContent=j.error||'Unable to open Smart Note';return}E('status').style.display='none';const n=E('note');n.style.display='block';n.innerHTML='<div><span class=pill>'+X(j.truth_state)+'</span><span class=pill>'+X(j.scope)+'</span><span class=pill>'+X(j.category)+'</span><span class=pill>'+X(j.topic)+'</span><span class=pill>'+X(j.subtopic)+'</span></div>'+S('Canonical Brain Path','<div class=path>'+X(j.canonical_path)+'</div>')+S('In a nutshell',X(j.intelligence.essence))+S('What',X(j.intelligence.objective))+S('Why it matters',X(j.intelligence.human_view?.why_it_matters))+S('Human view',X(j.intelligence.human_view?.meaning))+S('Child view',X(j.intelligence.simple_view?.child))+S('Grandma view',X(j.intelligence.simple_view?.grandma))+S('Naya view',X(j.intelligence.naya_view?.purpose))+S('Machine view','<div class=proof>'+X(JSON.stringify(j.intelligence.machine_view,null,2))+'</div>')+S('Decisions','<ul>'+j.intelligence.decisions.map(v=>'<li>'+X(v)+'</li>').join('')+'</ul>')+S('Connections','<ul>'+j.intelligence.connections.map(v=>'<li><b>'+X(v.type)+'</b> → '+X(v.target)+'</li>').join('')+'</ul>')+S('How to apply',X(j.intelligence.human_view?.simple_rule))+S('What it ultimately means',X(j.intelligence.priority))+S('Uncertainty',X(j.intelligence.uncertainty))+S('Proof / provenance','<div class=proof>'+X(JSON.stringify(j.provenance,null,2))+'</div>')}",
    "E('send').onclick=async()=>{const email=E('email').value.trim();E('authStatus').textContent='Sending code…';const q=await sb.auth.signInWithOtp({email,options:{shouldCreateUser:false}});if(q.error){E('authStatus').textContent=q.error.message;return}E('otpBox').style.display='inline';E('authStatus').textContent='Code sent.'};",
    "E('verify').onclick=async()=>{const email=E('email').value.trim();const token=E('otp').value.replace(/\D/g,'').slice(0,6);E('authStatus').textContent='Verifying…';const q=await sb.auth.verifyOtp({email,token,type:'email'});if(q.error){E('authStatus').textContent=q.error.message;return}location.reload()};load();",
    "</script></body></html>"
  ].join("");
  return new Response(page, { status: 200, headers: { ...BASE_HEADERS, "content-type": "text/html; charset=utf-8" } });
}

Deno.serve(async (req) => {
  try {
    if (req.method !== "GET") return new Response(JSON.stringify({ error: "METHOD_NOT_ALLOWED" }), { status: 405, headers: { ...BASE_HEADERS, "content-type": "application/json" } });
    const url = new URL(req.url);
    const ib = url.searchParams.get("ib") ?? "";
    if (!/^IB-[A-Za-z0-9_-]+$/.test(ib)) return new Response(JSON.stringify({ error: "INTELLIGENT_BLOCK_ID_REQUIRED" }), { status: 400, headers: { ...BASE_HEADERS, "content-type": "application/json" } });

    if (url.searchParams.get("data") !== "1") return viewerShell(ib);

    const { client, user } = await requireViewer(req);
    const { data: block, error } = await client
      .from("nayanet_intelligent_blocks")
      .select("intelligent_block_id,owner_id,title,understanding_state,owner_scope,content,provenance,evidence_refs,source_event_ids,created_at")
      .eq("intelligent_block_id", ib)
      .maybeSingle();
    if (error) throw error;
    if (!block) return new Response(JSON.stringify({ error: "SMART_NOTE_NOT_FOUND" }), { status: 404, headers: { ...BASE_HEADERS, "content-type": "application/json" } });
    if (block.owner_id !== user.id) return new Response(JSON.stringify({ error: "SMART_NOTE_FORBIDDEN" }), { status: 403, headers: { ...BASE_HEADERS, "content-type": "application/json" } });

    const entry = await registryEntry(ib);
    const intelligence = JSON.parse(block.content?.lesson ?? "{}");
    const category = entry.category ?? block.content?.category ?? "SMART_NOTE";
    const topic = entry.topic ?? block.content?.topic ?? "GENERAL";
    const subtopic = entry.subtopic ?? "GENERAL";
    const date = String(entry.captured_at ?? block.created_at ?? "").slice(0, 10).replaceAll("-", "/");
    const canonicalPath = ".naya/memory/smart-notes/" + date + "/" +
      String(category).toLowerCase().replaceAll("_", "-") + "/" +
      String(topic).toLowerCase().replaceAll("_", "-") + "/" +
      String(subtopic).toLowerCase().replaceAll("_", "-") + "/" + ib + "/smart-note.md";

    return new Response(JSON.stringify({
      ok: true,
      schema: "naya.private-smart-link.v1",
      intelligent_block_id: ib,
      title: block.title,
      truth_state: block.understanding_state,
      scope: block.owner_scope,
      category,
      topic,
      subtopic,
      canonical_path: canonicalPath,
      intelligence,
      provenance: {
        registry: entry.provenance,
        block_provenance: block.provenance,
        evidence_refs: block.evidence_refs,
        source_event_ids: block.source_event_ids,
        created_at: block.created_at
      }
    }), { status: 200, headers: { ...BASE_HEADERS, "content-type": "application/json" } });
  } catch (error) {
    const message = String((error as Error)?.message ?? error);
    const status = message.startsWith("AUTH_") ? 401 : 400;
    return new Response(JSON.stringify({ error: message }), { status, headers: { ...BASE_HEADERS, "content-type": "application/json" } });
  }
});
