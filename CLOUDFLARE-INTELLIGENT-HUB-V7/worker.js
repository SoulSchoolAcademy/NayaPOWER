export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === '/' || url.pathname === '/index.html' || url.pathname.startsWith('/intelligence/')) {
      const response = await env.ASSETS.fetch(new Request(new URL('/index.html', request.url), request));
      const headers = new Headers(response.headers);
      headers.set('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0');
      headers.set('Pragma', 'no-cache');
      headers.set('X-NayaNET-Release', 'V7-INTELLIGENT-HUB');
      return new Response(response.body, { status: response.status, headers });
    }
    return env.ASSETS.fetch(request);
  }
};
// V7_IDENTITY_DIAGNOSTIC_TRIGGER=2026-09-08T00:21Z
