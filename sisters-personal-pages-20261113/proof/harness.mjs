// Local harness: serves the rebuilt staging worker on 127.0.0.1:8901 with a
// mock WELCOME_ASSETS KV seeded from the live Box read-backs (12 sisters).
// The worker's Supabase calls go through Node fetch (proxy env) — same as
// the real worker. No Cloudflare account needed; the worker code runs as-is.
// NOTE: lives in the round work dir (durable) — /tmp was wiped by a runtime
// restart mid-round, taking the first copy with it.
import http from "node:http";
import fs from "node:fs";

const worker = (await import("/home/hatch/workspace/team-nitro/walk-questions-10-20261112/walk-beginning-staging-worker.js")).default;

const kv = new Map();
const put = (k, v) => kv.set(k, v);
const get = async (k, type) => {
  const v = kv.get(k);
  if (v === undefined) return null;
  if (type === "arrayBuffer") {
    if (v instanceof ArrayBuffer) return v;
    if (Buffer.isBuffer(v)) return v.buffer.slice(v.byteOffset, v.byteOffset + v.byteLength);
    return new TextEncoder().encode(v).buffer;
  }
  if (typeof v === "string") return v;
  if (Buffer.isBuffer(v)) return v.toString("utf-8");
  return JSON.stringify(v);
};
const env = { WELCOME_ASSETS: { get, put, delete: async (k) => kv.delete(k), list: async () => ({ keys: [...kv.keys()].map((name) => ({ name })) }) } };

// Seed the twelve sisters from the live Box read-backs (re-read 2026-11-13 ~05:00Z,
// saved under proof/ — the /tmp originals were lost in the runtime restart).
const aliases = ["sophia", "thea", "zoe", "astraea", "vera", "wren", "iris", "ruth", "terra", "esme", "mira", "aurelia"];
for (const a of aliases) {
  const d = JSON.parse(fs.readFileSync(`/home/hatch/workspace/team-nitro/sisters-personal-pages-20261113/proof/spp-box-${a}.json`, "utf-8"));
  put("box_" + a, JSON.stringify(d.box));
  for (const pg of d.pages) {
    if (pg) put("page_" + a + "_" + pg.page_kind, JSON.stringify(pg));
  }
}
// Seed the walk pictures + welcome assets from live staging (public assets).
for (const [key, url] of [
  ["wbf-naya-a.jpg", "https://naya-walk-beginning-staging.nayapower.workers.dev/naya-a.jpg"],
  ["wbf-naya-b.jpg", "https://naya-walk-beginning-staging.nayapower.workers.dev/naya-b.jpg"],
  ["wbf-naya-c.jpg", "https://naya-walk-beginning-staging.nayapower.workers.dev/naya-c.jpg"],
  ["wbf-login-obsidian.jpg", "https://naya-walk-beginning-staging.nayapower.workers.dev/login-obsidian.jpg"],
  ["wbf-naya-logo.png", "https://naya-walk-beginning-staging.nayapower.workers.dev/naya-logo.png"],
]) {
  try {
    const r = await fetch(url);
    if (r.ok) { put(key, await r.arrayBuffer()); console.log("seeded", key, r.headers.get("content-length") || ""); }
    else console.log("SEED FAIL", key, r.status);
  } catch (e) { console.log("SEED FAIL", key, String(e).slice(0, 80)); }
}
console.log("KV keys:", kv.size);

const server = http.createServer(async (req, res) => {
  try {
    const url = `http://127.0.0.1:8901${req.url}`;
    const chunks = [];
    for await (const c of req) chunks.push(c);
    const body = chunks.length ? Buffer.concat(chunks) : undefined;
    const request = new Request(url, { method: req.method, headers: req.headers, body: body && req.method !== "GET" && req.method !== "HEAD" ? body : undefined, duplex: "half" });
    const t0 = Date.now();
    const resp = await worker.fetch(request, env, {});
    const ms = Date.now() - t0;
    if (req.url.startsWith("/pages/") || req.url.startsWith("/api/") || resp.status >= 400) {
      console.log(req.method, req.url, "->", resp.status, ms + "ms");
    }
    res.writeHead(resp.status, [...resp.headers.entries()]);
    const buf = Buffer.from(await resp.arrayBuffer());
    res.end(buf);
  } catch (e) {
    console.log("HARNESS ERROR", req.url, String(e && e.stack || e).slice(0, 500));
    res.writeHead(500); res.end("harness error: " + String(e && e.message || e));
  }
});
server.listen(8901, "127.0.0.1", () => console.log("harness up on 127.0.0.1:8901"));
