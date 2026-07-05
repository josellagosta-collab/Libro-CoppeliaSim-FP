const CACHE_NAME = "coppeliasim-fp-v1";
const APP_SHELL = [
  "./",
  "./manifest.webmanifest",
  "./assets/css/coppeliasim-fp.css",
  "./assets/js/coppeliasim-fp.js",
  "./assets/js/portada.js",
  "./assets/logos/favicon.png",
  "./assets/icons/icon-192.png",
  "./assets/icons/icon-512.png",
  "./assets/icons/maskable-512.png"
];

self.addEventListener("install", function (event) {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(function (cache) {
        return cache.addAll(APP_SHELL);
      })
      .then(function () {
        return self.skipWaiting();
      })
  );
});

self.addEventListener("activate", function (event) {
  event.waitUntil(
    caches.keys()
      .then(function (names) {
        return Promise.all(
          names
            .filter(function (name) {
              return name !== CACHE_NAME;
            })
            .map(function (name) {
              return caches.delete(name);
            })
        );
      })
      .then(function () {
        return self.clients.claim();
      })
  );
});

self.addEventListener("fetch", function (event) {
  const request = event.request;

  if (request.method !== "GET" || new URL(request.url).origin !== location.origin) {
    return;
  }

  if (request.mode === "navigate") {
    event.respondWith(networkFirst(request));
    return;
  }

  event.respondWith(cacheFirst(request));
});

function cacheFirst(request) {
  return caches.match(request).then(function (cached) {
    if (cached) {
      return cached;
    }

    return fetch(request).then(function (response) {
      const copy = response.clone();

      if (response.ok) {
        caches.open(CACHE_NAME).then(function (cache) {
          cache.put(request, copy);
        });
      }

      return response;
    });
  });
}

function networkFirst(request) {
  return fetch(request)
    .then(function (response) {
      const copy = response.clone();

      if (response.ok) {
        caches.open(CACHE_NAME).then(function (cache) {
          cache.put(request, copy);
        });
      }

      return response;
    })
    .catch(function () {
      return caches.match(request).then(function (cached) {
        return cached || caches.match("./");
      });
    });
}
