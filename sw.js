const CACHE = 'finanzasrd-v1';
const FILES = [
  '/',
  '/index.html',
  '/styles.css',
  '/script.js',
  '/404.html',
  '/privacidad.html',
  '/terminos.html',
  '/rss.xml',
  '/sitemap.xml'
];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE).then(cache => cache.addAll(FILES))
  );
  self.skipWaiting();
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
    )
  );
  self.clients.claim();
});

self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET') return;
  e.respondWith(
    caches.match(e.request).then(cached =>
      cached || fetch(e.request).then(res => {
        const clone = res.clone();
        if (res.ok && e.request.url.startsWith(self.location.origin)) {
          caches.open(CACHE).then(cache => cache.put(e.request, clone));
        }
        return res;
      }).catch(() => caches.match('/404.html'))
    )
  );
});
