const CONTENT_TYPES = {
  html: "text/html; charset=utf-8",
  htm: "text/html; charset=utf-8",
  js: "text/javascript; charset=utf-8",
  mjs: "text/javascript; charset=utf-8",
  css: "text/css; charset=utf-8",
  json: "application/json; charset=utf-8",
  png: "image/png",
  jpg: "image/jpeg",
  jpeg: "image/jpeg",
  gif: "image/gif",
  svg: "image/svg+xml",
  webp: "image/webp",
  ico: "image/x-icon",
  txt: "text/plain; charset=utf-8",
  md: "text/plain; charset=utf-8",
};

export default {
  async fetch(request) {
    const url = new URL(request.url);
    if (url.pathname === "/health") {
      return new Response("naya-proof-host ok", {
        headers: { "content-type": "text/plain; charset=utf-8" },
      });
    }
    const file = url.searchParams.get("file");
    const ref = url.searchParams.get("ref") || "main";
    if (!file) {
      return new Response("Usage: ?file=<repo path>&ref=<branch, default main>", {
        status: 400, headers: { "content-type": "text/plain; charset=utf-8" },
      });
    }
    if (file.includes("..") || file.startsWith("/") || file.includes("://")) {
      return new Response("bad path", {
        status: 400, headers: { "content-type": "text/plain; charset=utf-8" },
      });
    }
    const enc = (p) => p.split("/").map(encodeURIComponent).join("/");
    const gh = `https://raw.githubusercontent.com/SoulSchoolAcademy/NayaPOWER/${enc(ref)}/${enc(file)}`;
    const res = await fetch(gh, { headers: { "User-Agent": "naya-proof-host" } });
    if (!res.ok) {
      return new Response(`GitHub ${res.status} for ${file}@${ref}`, {
        status: res.status, headers: { "content-type": "text/plain; charset=utf-8" },
      });
    }
    const body = await res.arrayBuffer();
    const ext = file.split(".").pop().toLowerCase();
    return new Response(body, {
      headers: {
        "content-type": CONTENT_TYPES[ext] || "text/html; charset=utf-8",
        "cache-control": "no-store",
      },
    });
  },
};
