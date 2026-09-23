// Network-first: edits pushed to GitHub show up on next open; cached copy is used offline.
const CACHE = 'zaryadka-v9';
const ASSETS = ['./', './index.html', './workouts.json', './manifest.webmanifest', './icons/icon.svg', './icons/icon-192.png', './icons/icon-512.png', './icons/icon-maskable-v4-512.png'];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(ASSETS)));
  self.skipWaiting();
});

self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))));
  self.clients.claim();
});

self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET' || new URL(req.url).origin !== location.origin) return;
  // cache: 'no-cache' revalidates with the server (cheap 304s) instead of reusing the browser's HTTP cache,
  // which GitHub Pages lets serve for 10 minutes — that's what made a fresh launch show the old app.
  e.respondWith(
    fetch(req.url, { cache: 'no-cache', credentials: 'same-origin' })
      .then(r => { if (r.ok) { const copy = r.clone(); caches.open(CACHE).then(c => c.put(req.url, copy)); } return r; })
      .catch(() => caches.match(req, { ignoreSearch: true }))
  );
});
