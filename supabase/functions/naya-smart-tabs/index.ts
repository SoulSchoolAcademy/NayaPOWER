import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2.57.2";

const url = Deno.env.get("SUPABASE_URL")!;
const anon = Deno.env.get("SUPABASE_ANON_KEY")!;
const cors = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, apikey, content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS"
};

Deno.serve(async (req: Request) => {
  if (req.method === "OPTIONS") return new Response(null, { status: 204, headers: cors });
  const auth = req.headers.get("authorization") ?? "";
  if (!auth.toLowerCase().startsWith("bearer ")) return json({ error: "UNAUTHORIZED_NO_AUTH_HEADER" }, 401);
  const userSupabase = createClient(url, anon, { global: { headers: { Authorization: auth } } });
  const { data: { user }, error: userError } = await userSupabase.auth.getUser();
  if (userError || !user) return json({ error: "UNAUTHORIZED_INVALID_TOKEN" }, 401);

  let body: Record<string, unknown> = {};
  try { body = await req.json(); } catch {}
  const op = String(body.op ?? "list");
  const db = userSupabase;

  if (op === "list") {
    const { data, error } = await db.from("nayanet_smart_tabs")
      .select("id,label,target_type,target,scope,favorite,priority,position,created_at,updated_at")
      .order("position", { ascending: true }).order("created_at", { ascending: true });
    if (error) return json({ error: error.message }, 400);
    return json({ tabs: data ?? [] });
  }

  if (op === "create") {
    const label = String(body.label ?? "").trim();
    const target_type = String(body.target_type ?? "route").trim();
    const target = String(body.target ?? "").trim();
    if (!label || !target) return json({ error: "LABEL_AND_TARGET_REQUIRED" }, 400);
    const { data, error } = await db.from("nayanet_smart_tabs").insert({
      owner_id: user.id, label, target_type, target, scope: "private",
      favorite: body.favorite === true,
      priority: Number.isFinite(body.priority) ? Number(body.priority) : 0,
      position: Number.isFinite(body.position) ? Number(body.position) : 0
    }).select().single();
    if (error) return json({ error: error.message }, 400);
    return json({ tab: data }, 201);
  }

  if (op === "update") {
    const id = String(body.id ?? "");
    if (!id) return json({ error: "TAB_ID_REQUIRED" }, 400);
    const patch: Record<string, unknown> = { updated_at: new Date().toISOString() };
    for (const key of ["label", "target_type", "target", "favorite", "priority", "position"]) {
      if (body[key] !== undefined) patch[key] = body[key];
    }
    const { data, error } = await db.from("nayanet_smart_tabs").update(patch).eq("id", id).select().single();
    if (error) return json({ error: error.message }, 400);
    return json({ tab: data });
  }

  if (op === "delete") {
    const id = String(body.id ?? "");
    if (!id) return json({ error: "TAB_ID_REQUIRED" }, 400);
    const { data, error } = await db.from("nayanet_smart_tabs").delete().eq("id", id).select("id").maybeSingle();
    if (error) return json({ error: error.message }, 400);
    if (!data) return json({ error: "TAB_NOT_FOUND_OR_NOT_AUTHORIZED" }, 404);
    return json({ deleted: data.id });
  }

  return json({ error: "UNSUPPORTED_OPERATION" }, 400);
});

function json(payload: unknown, status = 200) {
  return new Response(JSON.stringify(payload), {
    status, headers: { ...cors, "content-type": "application/json", "cache-control": "no-store" }
  });
}
