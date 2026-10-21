/* NayaNET Hub service worker — naya-hub-shell-v1.
   Precache the shell + manifest + icons; serve same-scope GETs cache-first
   with network fallback. Scope-guarded to "/" — never touches /rooms/* workers. */
const CACHE = 'naya-hub-shell-v1';
const SHELL = ['/', '/manifest.json', '/icons/naya-icon-192.png', '/icons/naya-icon-512.png', '/icons/apple-touch-icon.png'];

self.addEventListener('install', function (e) {
  e.waitUntil(caches.open(CACHE).then(function (c) { return c.addAll(SHELL); }).then(function () { return self.skipWaiting(); }));
});

self.addEventListener('activate', function (e) {
  e.waitUntil(
    caches.keys().then(function (keys) {
      return Promise.all(keys.map(function (k) { return k === CACHE ? null : caches.delete(k); }));
    }).then(function () { return self.clients.claim(); })
  );
});

self.addEventListener('fetch', function (e) {
  if (e.request.method !== 'GET') return;
  var url = new URL(e.request.url);
  if (url.origin !== self.location.origin) return;
  e.respondWith(
    caches.match(e.request, { ignoreSearch: false }).then(function (hit) {
      var network = fetch(e.request).then(function (res) {
        if (res && (res.status === 200 || res.status === 0)) {
          var copy = res.clone();
          caches.open(CACHE).then(function (c) { c.put(e.request, copy); });
        }
        return res;
      }).catch(function () { return hit; });
      return hit || network;
    })
  );
});
