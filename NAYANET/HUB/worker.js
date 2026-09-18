export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === '/' || url.pathname === '/index.html') {
      const release = env.NAYA_RELEASE || 'nayanet-live-r3';
      const releaseUrl = new URL('/releases/' + encodeURIComponent(release) + '/index.html', url);
      const response = await env.ASSETS.fetch(new Request(releaseUrl.toString(), request));
      const headers = new Headers(response.headers);
      headers.set('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0');
      headers.set('Pragma', 'no-cache');
      headers.set('X-Naya-Canonical-Asset', release);
      return new Response(response.body, { status: response.status, statusText: response.statusText, headers });
    }
    const response = await env.ASSETS.fetch(request);
    if (url.pathname === '/assistant-runtime.js') {
      const headers = new Headers(response.headers);
      headers.set('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0');
      headers.set('Pragma', 'no-cache');
      headers.set('X-Naya-Runtime-Asset', 'live');
      return new Response(response.body, { status: response.status, statusText: response.statusText, headers });
    }
    return response;
  }
};
