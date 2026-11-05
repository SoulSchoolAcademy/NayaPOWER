// naya-link-probe — tiny redirect checker on workers.dev.
// A Worker on the nayanet.app zone cannot reliably fetch nayanet.app
// itself (same-zone subrequests hang), so the claim worker verifies a new
// link's real 302 through this probe, which lives outside the zone.
// Accepts both nayanet.app and nayanet.live short addresses.
// GET /?u=<url>  ->  {"status":302,"location":"..."} or {"error":"..."}
export default {
  async fetch(request) {
    const u = new URL(request.url).searchParams.get('u');
    if (!u || !/^https:\/\/(nayanet\.app|nayanet\.live)\/[a-z0-9][a-z0-9-]*$/.test(u)) {
      return new Response(JSON.stringify({ error: 'bad u' }),
        { status: 400, headers: { 'Content-Type': 'application/json' } });
    }
    try {
      const res = await fetch(u, {
        redirect: 'manual',
        headers: { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36' },
        signal: AbortSignal.timeout(10000)
      });
      return new Response(JSON.stringify({ status: res.status, location: res.headers.get('Location') }),
        { headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' } });
    } catch (e) {
      return new Response(JSON.stringify({ error: String(e).slice(0, 200) }),
        { headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' } });
    }
  }
};
