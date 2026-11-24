/* NayaNET settings — minimal install worker: cache this page + the N icons, nothing more. */
const CACHE = 'naya-settings-v1';
const ASSETS = ['business-settings2.html', 'manifest.json', 'naya-icon-192.png', 'naya-icon-512.png', 'naya-icon-180.png'];
self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(ASSETS)).catch(() => {}));
});
self.addEventListener('fetch', (e) => {
  e.respondWith(caches.match(e.request).then((r) => r || fetch(e.request)));
});
