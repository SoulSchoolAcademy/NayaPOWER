"use strict";
(() => {
  const SUPABASE_URL = "https://dahisasgpfvziswqvmvm.supabase.co";
  const SUPABASE_KEY = "sb_publishable_oQFKOYFuJ9bT-E9QkJUb4g_lAUyInue";
  const LOCAL_KEY = "nayanet:intelligence:v1";
  const RUNTIME_SRC = "/nayanet-10.js";
  const FEED_SRC = "/nayanet-intelligence-feed.js";
  const FRONT_DOOR_SRC = "/nayanet-front-door.js";
  let client = null, memberId = null, ready = false, internalWrite = false;
  let runtimeStarted = false;

  const uuid = () => crypto.randomUUID();
  function localState() { try { return JSON.parse(localStorage.getItem(LOCAL_KEY) || "{}"); } catch { return {}; } }
  function remember() { return localStorage.getItem("nayanetName") || localState().name || ""; }
  function slug(name) { return (name || "friend").toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "") || "friend"; }
  function writeLocal(key, value) { internalWrite = true; try { localStorage.setItem(key, value); } finally { internalWrite = false; } }
  function notify() { window.dispatchEvent(new CustomEvent("naya:data-ready", { detail: { memberId, ready } })); }
  function loadFeed() {
    const existing = document.querySelector(`script[src="${FEED_SRC}"]`);
    if (existing) return;
    const feed = document.createElement("script");
    feed.src = FEED_SRC;
    feed.async = false;
    document.body.appendChild(feed);
  }
  function startRuntime() {
    if (runtimeStarted) return;
    runtimeStarted = true;
    const existing = document.querySelector(`script[src="${RUNTIME_SRC}"]`);
    if (existing) { loadFeed(); return; }
    const script = document.createElement("script");
    script.src = RUNTIME_SRC;
    script.async = false;
    script.onload = loadFeed;
    document.body.appendChild(script);
  }
  function loadFrontDoor() {
    if (document.querySelector(`script[src="${FRONT_DOOR_SRC}"]`)) return;
    const script = document.createElement("script");
    script.src = FRONT_DOOR_SRC;
    script.async = false;
    document.body.appendChild(script);
  }
  async function boot() {
    try {
      const mod = await import("https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/+esm");
      client = mod.createClient(SUPABASE_URL, SUPABASE_KEY, { auth: { persistSession: true, autoRefreshToken: true, detectSessionInUrl: false } });
      let { data: { session } } = await client.auth.getSession();
      if (!session) { const r = await client.auth.signInAnonymously(); session = r.data?.session || null; if (r.error) throw r.error; }
      if (!session?.user?.id) throw new Error("No authenticated session");
      memberId = session.user.id;
      const name = remember();
      if (name) {
        await client.from("members").upsert({ id: memberId, display_name: name }, { onConflict: "id" });
        await client.from("nayanet_profiles").upsert({ member_id: memberId, smart_id: `naya/${slug(name)}`, public_alias: name }, { onConflict: "member_id" });
      }
      ready = true;
      await hydrate();
      notify();
    } catch (error) {
      ready = false;
      console.warn("NayaNET persistence bridge unavailable; local continuity remains active.", error);
      notify();
    } finally { loadFrontDoor(); startRuntime(); }
  }
  async function hydrate() {
    if (!client || !memberId) return;
    const [notes, challenge, spaces, profile] = await Promise.all([
      client.from("nayanet_notes").select("id,note_type,human_note,created_at").eq("member_id", memberId).order("created_at", { ascending: false }).limit(100),
      client.from("nayanet_challenges").select("goal,current_day,completed_days").eq("member_id", memberId).maybeSingle(),
      client.from("nayanet_spaces").select("id,name,purpose,created_at").eq("owner_member_id", memberId).order("created_at", { ascending: false }).limit(50),
      client.from("nayanet_profiles").select("smart_id,public_alias").eq("member_id", memberId).maybeSingle()
    ]);
    const s = localState();
    if (notes.data?.length) s.notes = notes.data.map(n => ({ id: n.id, type: n.note_type, text: n.human_note, at: new Date(n.created_at).getTime() }));
    if (challenge.data) s.challenge = { day: challenge.data.current_day, goal: challenge.data.goal, done: challenge.data.completed_days || [] };
    if (spaces.data?.length) s.spaces = spaces.data.map(x => ({ id: x.id, name: x.name, purpose: x.purpose, at: new Date(x.created_at).getTime() }));
    if (profile.data?.public_alias) { s.name = profile.data.public_alias; writeLocal("nayanetName", profile.data.public_alias); }
    writeLocal(LOCAL_KEY, JSON.stringify({ ...s, lastSeen: Date.now() }));
  }
  async function sync() {
    if (!client || !memberId) return;
    const s = localState();
    if (Array.isArray(s.notes) && s.notes.length) {
      const rows = s.notes.map(n => ({ id: n.id || uuid(), member_id: memberId, note_type: n.type || "Insight", human_note: n.text || "", created_at: new Date(n.at || Date.now()).toISOString() }));
      s.notes = rows.map(n => ({ id: n.id, type: n.note_type, text: n.human_note, at: new Date(n.created_at).getTime() }));
      await client.from("nayanet_notes").upsert(rows, { onConflict: "id" });
    }
    if (s.challenge) await client.from("nayanet_challenges").upsert({ member_id: memberId, goal: s.challenge.goal || "", current_day: s.challenge.day || 1, completed_days: s.challenge.done || [] }, { onConflict: "member_id" });
    if (Array.isArray(s.spaces) && s.spaces.length) {
      const rows = s.spaces.map(x => ({ id: x.id || uuid(), owner_member_id: memberId, name: x.name, purpose: x.purpose, visibility: "private", created_at: new Date(x.at || Date.now()).toISOString() }));
      s.spaces = rows.map(x => ({ id: x.id, name: x.name, purpose: x.purpose, at: new Date(x.created_at).getTime() }));
      await client.from("nayanet_spaces").upsert(rows, { onConflict: "id" });
    }
    if (s.name) {
      await client.from("members").upsert({ id: memberId, display_name: s.name }, { onConflict: "id" });
      await client.from("nayanet_profiles").upsert({ member_id: memberId, smart_id: `naya/${slug(s.name)}`, public_alias: s.name }, { onConflict: "member_id" });
    }
    writeLocal(LOCAL_KEY, JSON.stringify({ ...s, lastSeen: Date.now() }));
  }
  window.NayaData = { get ready() { return ready; }, get memberId() { return memberId; }, sync, hydrate };
  const originalSet = Storage.prototype.setItem;
  Storage.prototype.setItem = function(key, value) { originalSet.call(this, key, value); if (key === LOCAL_KEY && ready && !internalWrite) queueMicrotask(() => sync()); };
  window.addEventListener("naya:data-save", () => sync());
  boot();
})();
