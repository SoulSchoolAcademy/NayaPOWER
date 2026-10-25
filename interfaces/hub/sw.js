/* NayaNET Hub service worker — BUILT, not recovered.
   The original sw.js source was not found on any box, so this file was
   built from the Hub's known structure: a single-page Hub shell with
   Hub rooms, dashboard, mail, and Supabase-backed data.
   Rules, in order:
   1. Never cache anything that moves money, mail, identity, or live data.
      API, Supabase, auth, and mail requests are network-only, always.
   2. Navigations are network-first, with a cached shell fallback.
   3. Same-origin static assets are cache-first, updated in the background.
   4. No secrets, no keys, no hardcoded service URLs in this file.
   Registration is NEW, not existing: Nitro checked the Hub file and it has
   NO service worker registration at all, so there is no existing line to
   confirm against. Adding registration is Shawn's call, and the landing seat
   adds this line once, only on that call:
     if ("serviceWorker" in navigator) navigator.serviceWorker.register("/sw.js");
*/
const CACHE = "nayanet-hub-v1";
// CORRECTED by Nitro's check (2026-10-24): the Hub's own shell is just its
// front page. Hub pages inside it are states inside the app, not separate
// documents, and the dashboard is served separately — so neither /hub/ nor
// /dashboard belongs in this shell list. Do not re-add them without a check.
const SHELL = ["/"];

const NETWORK_ONLY = ["/api/", "supabase.co", "/auth/", "/smart-mail", "/mail/send"];
function isNetworkOnly(url) {
  return NETWORK_ONLY.some((p) => url.includes(p));
}
function isStatic(url, dest) {
  return dest === "style" || dest === "script" || dest === "font" ||
    /\.(css|js|png|jpg|jpeg|webp|svg|woff2?)$/i.test(url.pathname);
}
const OFFLINE_HTML = "<!doctype html><title>NayaNET Hub — offline</title>" +
  "<body style=\"background:#07070d;color:#fff;font-family:system-ui;padding:24px\">" +
  "<h1>You're offline</h1><p>The Hub will reload the moment your connection returns. " +
  "Nothing was lost — your mail, notes, and pages live in the system, not on this device.</p></body>";

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE).then((cache) => cache.addAll(SHELL).catch(() => {}))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (event) => {
  const req = event.request;
  if (req.method !== "GET") return;
  const url = new URL(req.url);
  if (isNetworkOnly(req.url)) return; // network-only, no cache read, no cache write

  if (req.mode === "navigate") {
    event.respondWith(
      fetch(req).then((res) => {
        const copy = res.clone();
        caches.open(CACHE).then((c) => c.put(req, copy)).catch(() => {});
        return res;
      }).catch(() => caches.match(req).then((hit) => hit ||
        new Response(OFFLINE_HTML, { headers: { "Content-Type": "text/html" } })))
    );
    return;
  }

  if (url.origin === self.location.origin && isStatic(url, req.destination)) {
    event.respondWith(
      caches.match(req).then((hit) => {
        const net = fetch(req).then((res) => {
          if (res.ok) {
            const copy = res.clone();
            caches.open(CACHE).then((c) => c.put(req, copy)).catch(() => {});
          }
          return res;
        }).catch(() => hit);
        return hit || net;
      })
    );
  }
});
