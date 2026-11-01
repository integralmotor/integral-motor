/* Integral Motor: guarda la app en el dispositivo para que abra rápido y sin internet.
   Los datos los sincroniza Firebase; acá solo se guardan los archivos de la app. */
const C='im-v1';
self.addEventListener('install',e=>{self.skipWaiting();e.waitUntil(caches.open(C).then(c=>c.addAll(['./','./manifest.webmanifest','./icon-192.png','./icon-512.png','./apple-touch-icon.png'])))});
self.addEventListener('activate',e=>e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(x=>x!=C).map(x=>caches.delete(x)))).then(()=>self.clients.claim())));
self.addEventListener('fetch',e=>{const r=e.request;if(r.method!='GET')return;const u=new URL(r.url);
 /* la app: primero internet (para tener siempre la última versión), si no hay, lo guardado */
 if(u.origin==location.origin){e.respondWith(fetch(r).then(x=>{if(x.ok){const y=x.clone();caches.open(C).then(c=>c.put(r,y))}return x}).catch(()=>caches.match(r).then(x=>x||caches.match('./'))));return}
 /* librerías con versión fija (PDF, Excel, Firebase): lo guardado, si no, internet */
 if(/^(cdnjs\.cloudflare\.com|www\.gstatic\.com|cdn\.jsdelivr\.net)$/.test(u.hostname)&&/\.js$/.test(u.pathname))
  e.respondWith(caches.match(r).then(x=>x||fetch(r).then(y=>{const z=y.clone();caches.open(C).then(c=>c.put(r,z));return y})))});
