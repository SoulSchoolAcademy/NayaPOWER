export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    // Canonical Hub root: explicitly resolve `/` to the built React entry artifact.
    // This prevents the SPA fallback from ever selecting a legacy Welcome surface.
    const assetRequest = url.pathname === '/'
      ? new Request(new URL('/index.html', url), request)
      : request;
    const response = await env.ASSETS.fetch(assetRequest);

    if (url.pathname === '/' || url.pathname === '/index.html') {
      const headers = new Headers(response.headers);
      headers.set('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0');
      headers.set('Pragma', 'no-cache');
      headers.set('X-Naya-Canonical-Asset', 'index.html');
      return new Response(response.body, {
        status: response.status,
        statusText: response.statusText,
        headers
      });
    }

    if (url.pathname === '/assistant-runtime.js') {
      const headers = new Headers(response.headers);
      headers.set('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0');
      headers.set('Pragma', 'no-cache');
      headers.set('X-Naya-Runtime-Asset', 'live');
      return new Response(response.body, {
        status: response.status,
        statusText: response.statusText,
        headers
      });
    }

    return response;
  }
};
