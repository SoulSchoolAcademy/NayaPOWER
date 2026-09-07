export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === '/' || url.pathname === '/index.html' || url.pathname.startsWith('/intelligence/')) {
      const response = await env.ASSETS.fetch(new Request(new URL('/index.html', request.url), request));
      return new Response(response.body, { status: response.status, headers: new Headers(response.headers) });
    }
    return env.ASSETS.fetch(request);
  }
};
