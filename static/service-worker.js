self.addEventListener('install', event => {
    event.waitUntil(
        caches.open('vox-videos-cache').then(cache => {
            return cache.addAll([
                '/',
                '/static/logo/logo.png',
                // Añadir más recursos estáticos si es necesario
            ]);
        })
    );
});

self.addEventListener('fetch', event => {
    event.respondWith(
        caches.match(event.request).then(response => {
            return response || fetch(event.request);
        })
    );
});
