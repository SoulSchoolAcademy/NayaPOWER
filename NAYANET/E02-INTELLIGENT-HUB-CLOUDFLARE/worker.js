const cors = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET,HEAD,OPTIONS",
  "Access-Control-Allow-Headers": "Range,Content-Type",
  "Access-Control-Expose-Headers": "Accept-Ranges,Content-Length,Content-Range,Content-Type,ETag,Last-Modified"
};

function withCors(headers = {}) {
  const out = new Headers(headers);
  Object.entries(cors).forEach(([k,v]) => out.set(k,v));
  return out;
}

function isDriveId(value) {
  return /^[A-Za-z0-9_-]{10,}$/.test(value || "");
}

async function driveFetch(id, request) {
  const range = request.headers.get("Range");
  const headers = new Headers();
  headers.set("User-Agent", "Mozilla/5.0");
  headers.set("Accept", "audio/*,application/octet-stream;q=0.9,*/*;q=0.1");
  if (range) headers.set("Range", range);

  const targets = [
    `https://drive.usercontent.google.com/download?id=${encodeURIComponent(id)}&export=download&confirm=t`,
    `https://drive.google.com/uc?export=download&id=${encodeURIComponent(id)}&confirm=t`
  ];

  let last = null;
  for (const target of targets) {
    const r = await fetch(target, {
      method: request.method === "HEAD" ? "HEAD" : "GET",
      headers,
      redirect: "follow"
    });
    last = r;

    const type = (r.headers.get("content-type") || "").toLowerCase();
    if (!type.includes("text/html") && !type.includes("application/xhtml")) return r;

    if (request.method === "HEAD") continue;

    const html = await r.clone().text();
    const token =
      html.match(/name=["']confirm["']\s+value=["']([^"']+)["']/i)?.[1] ||
      html.match(/[?&]confirm=([0-9A-Za-z_-]+)/i)?.[1];

    if (token) {
      const retryHeaders = new Headers(headers);
      const cookie = r.headers.get("set-cookie");
      if (cookie) retryHeaders.set("Cookie", cookie.split(";")[0]);
      const retryUrl = `https://drive.usercontent.google.com/download?id=${encodeURIComponent(id)}&export=download&confirm=${encodeURIComponent(token)}`;
      const retry = await fetch(retryUrl, {method:"GET",headers:retryHeaders,redirect:"follow"});
      last = retry;
      const retryType = (retry.headers.get("content-type") || "").toLowerCase();
      if (!retryType.includes("text/html") && !retryType.includes("application/xhtml")) return retry;
    }
  }
  return last;
}

async function handleAudio(request, id) {
  if (!isDriveId(id)) {
    return new Response(JSON.stringify({ok:false,error:"Invalid Google Drive file id"}), {
      status:400,
      headers:withCors({"Content-Type":"application/json; charset=utf-8"})
    });
  }

  try {
    const upstream = await driveFetch(id, request);
    if (!upstream) throw new Error("No upstream response from Google Drive");

    const upstreamType = upstream.headers.get("content-type") || "";
    const lower = upstreamType.toLowerCase();
    if (lower.includes("text/html") || lower.includes("application/xhtml")) {
      return new Response(JSON.stringify({ok:false,error:"Google Drive returned HTML instead of audio bytes",upstreamStatus:upstream.status,upstreamContentType:upstreamType || null}), {
        status:502,
        headers:withCors({"Content-Type":"application/json; charset=utf-8","Cache-Control":"no-store"})
      });
    }

    const headers = withCors(upstream.headers);
    headers.set("Accept-Ranges","bytes");
    headers.set("Content-Disposition","inline");
    headers.set("Cache-Control","public, max-age=300, s-maxage=3600");
    if (!headers.get("Content-Type")) headers.set("Content-Type","audio/mpeg");

    return new Response(request.method === "HEAD" ? null : upstream.body, {
      status:upstream.status,
      headers
    });
  } catch (error) {
    return new Response(JSON.stringify({ok:false,error:String(error?.message || error)}), {
      status:502,
      headers:withCors({"Content-Type":"application/json; charset=utf-8","Cache-Control":"no-store"})
    });
  }
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (request.method === "OPTIONS") return new Response(null,{status:204,headers:withCors()});

    if (url.pathname === "/health") {
      return new Response(JSON.stringify({ok:true,service:"nayanet-powercast",version:"proven-drive-bridge-v2"}), {
        headers:withCors({"Content-Type":"application/json; charset=utf-8","Cache-Control":"no-store"})
      });
    }

    if (url.pathname === "/audio" || url.pathname === "/audio/") {
      if (request.method !== "GET" && request.method !== "HEAD") return new Response("Method Not Allowed",{status:405,headers:withCors({Allow:"GET,HEAD,OPTIONS"})});
      return handleAudio(request,url.searchParams.get("id") || "");
    }

    if (url.pathname.startsWith("/audio/")) {
      if (request.method !== "GET" && request.method !== "HEAD") return new Response("Method Not Allowed",{status:405,headers:withCors({Allow:"GET,HEAD,OPTIONS"})});
      return handleAudio(request,decodeURIComponent(url.pathname.slice("/audio/".length)));
    }

    if (url.pathname === "/" || url.pathname === "") return env.ASSETS.fetch(new Request(new URL("/index.html",request.url),request));
    return env.ASSETS.fetch(request);
  }
};
