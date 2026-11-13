// naya-auto-translate-staging — Step 0 worker for the Auto-Translate round
// (Area #41, 2026-11-13). Staged only. One endpoint: POST /translate.
// Calls Workers AI @cf/meta/m2m100-1.2b. No secrets, no storage, no keys.
// The page translates on tap, one note at a time; the translation is a
// labelled view — the citizen's words are never stored here.
export default {
  async fetch(request, env) {
    const cors = {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
    };
    if (request.method === "OPTIONS") {
      return new Response(null, { status: 204, headers: cors });
    }
    const url = new URL(request.url);
    if (request.method !== "POST" || url.pathname !== "/translate") {
      return new Response(JSON.stringify({ ok: false, error: "POST /translate only" }), {
        status: 404, headers: { ...cors, "Content-Type": "application/json" },
      });
    }
    let body;
    try { body = await request.json(); } catch (e) {
      return new Response(JSON.stringify({ ok: false, error: "bad json" }), {
        status: 400, headers: { ...cors, "Content-Type": "application/json" },
      });
    }
    const source = String(body.source_lang || "").toLowerCase();
    const target = String(body.target_lang || "").toLowerCase();
    const langs = ["en", "es", "fr", "de"];
    if (!langs.includes(source) || !langs.includes(target) || source === target) {
      return new Response(JSON.stringify({ ok: false, error: "source/target must be two different of en/es/fr/de" }), {
        status: 400, headers: { ...cors, "Content-Type": "application/json" },
      });
    }
    // Segments: the client splits multi-sentence notes before sending
    // (m2m100 drops sentences on long input). Accept an array or one text.
    let segments = Array.isArray(body.segments) ? body.segments : (body.text ? [body.text] : []);
    segments = segments.map((s) => String(s)).filter((s) => s.trim().length > 0).slice(0, 20);
    const total = segments.join(" ").length;
    if (!segments.length || total > 5000) {
      return new Response(JSON.stringify({ ok: false, error: "empty or too long (max 5000 chars, 20 segments)" }), {
        status: 400, headers: { ...cors, "Content-Type": "application/json" },
      });
    }
    try {
      const out = [];
      for (const seg of segments) {
        const r = await env.AI.run("@cf/meta/m2m100-1.2b", {
          text: seg, source_lang: source, target_lang: target,
        });
        out.push(r && r.translated_text ? String(r.translated_text) : "");
      }
      if (out.some((t) => !t)) {
        return new Response(JSON.stringify({ ok: false, error: "a segment came back empty", partial: out }), {
          status: 502, headers: { ...cors, "Content-Type": "application/json" },
        });
      }
      return new Response(JSON.stringify({ ok: true, source_lang: source, target_lang: target, segments: out, translated_text: out.join(" ") }), {
        headers: { ...cors, "Content-Type": "application/json" },
      });
    } catch (e) {
      return new Response(JSON.stringify({ ok: false, error: "translation failed: " + String(e && e.message || e) }), {
        status: 502, headers: { ...cors, "Content-Type": "application/json" },
      });
    }
  },
};
