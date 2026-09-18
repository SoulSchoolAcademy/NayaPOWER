export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    if (url.pathname === '/__naya_cache_purge') {
      await ctx.cache.purge({ purgeEverything: true });
      return new Response('NAYA_CACHE_PURGED', { headers: { 'Cache-Control': 'no-store' } });
    }
    const response = await env.ASSETS.fetch(new Request(url.toString(), request));
    if (url.pathname === '/' || url.pathname === '/index.html' || url.pathname === '/assistant-runtime.js') {
      const headers = new Headers(response.headers);
      headers.set('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0');
      headers.set('Pragma', 'no-cache');
      headers.set('X-Naya-Canonical-Asset', 'live');
      return new Response(response.body, { status: response.status, statusText: response.statusText, headers });
    }
    return response;
  }
};
