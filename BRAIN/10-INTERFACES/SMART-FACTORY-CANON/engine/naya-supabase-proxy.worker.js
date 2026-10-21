// NayaPOWER Supabase Proxy v3
const SUPABASE_URL = 'https://dahisasgpfvziswqvmvm.supabase.co';
const ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRhaGlzYXNncGZ2emlzd3F2bXZtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODc2MjM3ODgsImV4cCI6MjEwMzE5OTc4OH0.zX2r3T23sKebUMBdNg-4Noxos8JFOHaK2rRwqAVXU_s';

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const path = url.pathname;
    
    const cors = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    };
    
    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: cors });
    }
    
    // Build queue
    if (path === '/build' && request.method === 'POST') {
      try {
        const contract = await request.json();
        const resp = await fetch(SUPABASE_URL + '/rest/v1/build_queue', {
          method: 'POST',
          headers: {'apikey': ANON_KEY,'Authorization': 'Bearer ' + ANON_KEY,'Content-Type': 'application/json','Prefer': 'return=representation'},
          body: JSON.stringify({contract: contract,status: 'pending'}),
        });
        const data = await resp.json();
        return new Response(JSON.stringify({build_id: data[0]?.id,status: 'pending'}), {headers: {...cors,'Content-Type': 'application/json'}});
      } catch (e) {
        return new Response(JSON.stringify({error: e.message}), {status: 500,headers: {...cors,'Content-Type': 'application/json'}});
      }
    }
    
    if (path.startsWith('/build/') && request.method === 'GET') {
      const buildId = path.slice(7);
      const resp = await fetch(SUPABASE_URL + '/rest/v1/build_queue?id=eq.' + buildId + '&select=*', {headers:{'apikey': ANON_KEY,'Authorization': 'Bearer ' + ANON_KEY}});
      const data = await resp.json();
      return new Response(JSON.stringify(data[0] || {error: 'Not found'}), {headers: {...cors,'Content-Type': 'application/json'}});
    }
    
    // Table routes
    let supabasePath = '';
    if (path.startsWith('/notes')) {
      supabasePath = '/rest/v1/smart_notes' + path.slice(6) + url.search;
    } else if (path.startsWith('/connections')) {
      supabasePath = '/rest/v1/connections' + path.slice(12) + url.search;
    } else if (path.startsWith('/hub-notes')) {
      supabasePath = '/rest/v1/hub_smart_notes' + path.slice(10) + url.search;
    } else {
      return new Response('Not found', {status: 404,headers: cors});
    }
    
    const supabaseReq = new Request(SUPABASE_URL + supabasePath, {
      method: request.method,
      headers:{'apikey': ANON_KEY,'Authorization': 'Bearer ' + ANON_KEY,'Content-Type': 'application/json','Prefer': 'return=representation'},
      body: request.method !== 'GET' && request.method !== 'HEAD' ? await request.text() : undefined,
    });
    
    try {
      const resp = await fetch(supabaseReq);
      const data = await resp.text();
      return new Response(data, {status: resp.status,headers: {...cors,'Content-Type': 'application/json'}});
    } catch (e) {
      return new Response(JSON.stringify({error: e.message}), {status: 500,headers: {...cors,'Content-Type': 'application/json'}});
    }
  }
};
