// nayanet-github-intake
// The receiving door for GitHub webhooks.
//
// Before this function existed, GitHub events reached the brain only when a
// worker polled for them (10-15 minute lanes). This function is the doorbell:
// GitHub POSTs every event here the moment it happens, and the shared secret
// (GITHUB_WEBHOOK_SECRET, set by Shawn in the Edge Function secrets and in
// the GitHub webhook's Secret field) proves the knock is really GitHub's.
//
// Contract:
//   request:  GitHub webhook delivery (POST, application/json), headers
//             X-Hub-Signature-256: sha256=<hex HMAC of the raw body>,
//             X-GitHub-Event: <event name>, X-GitHub-Delivery: <uuid>
//   success:  200 { ok:true, received:true, event, delivery }
//             (ping deliveries answer { ok:true, pong:true })
//   failure:  fail-closed, always receipted in the response body:
//             secret unset        -> 503 { ok:false, error:"INTAKE_NOT_CONFIGURED" }
//             signature missing   -> 401 { ok:false, error:"SIGNATURE_MISSING" }
//             signature mismatch  -> 401 { ok:false, error:"SIGNATURE_INVALID" }
//             non-POST            -> 405 { ok:false, error:"METHOD_NOT_ALLOWED" }
//
// v1 scope (deliberate): verify + accept + acknowledge. Event persistence
// and routing into the brain intake is the named follow-up; this function
// never pretends to have stored or routed what it only received.

const cors = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers":
    "authorization, x-client-info, apikey, content-type, x-hub-signature-256, x-github-event, x-github-delivery",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};

function json(body: unknown, status = 200): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { ...cors, "Content-Type": "application/json" },
  });
}

async function hmacSha256Hex(secret: string, rawBody: string): Promise<string> {
  const key = await crypto.subtle.importKey(
    "raw",
    new TextEncoder().encode(secret),
    { name: "HMAC", hash: "SHA-256" },
    false,
    ["sign"],
  );
  const sig = await crypto.subtle.sign(
    "HMAC",
    key,
    new TextEncoder().encode(rawBody),
  );
  return Array.from(new Uint8Array(sig))
    .map((b) => b.toString(16).padStart(2, "0"))
    .join("");
}

// Constant-time comparison so a forged signature leaks nothing through timing.
function timingSafeEqual(a: string, b: string): boolean {
  if (a.length !== b.length) return false;
  let diff = 0;
  for (let i = 0; i < a.length; i++) {
    diff |= a.charCodeAt(i) ^ b.charCodeAt(i);
  }
  return diff === 0;
}

Deno.serve(async (req: Request): Promise<Response> => {
  if (req.method === "OPTIONS") {
    return new Response(null, { status: 204, headers: cors });
  }
  if (req.method !== "POST") {
    return json({ ok: false, error: "METHOD_NOT_ALLOWED" }, 405);
  }

  const secret = Deno.env.get("GITHUB_WEBHOOK_SECRET") ?? "";
  if (!secret) {
    // Fail closed: an unconfigured intake accepts nothing, from anyone.
    return json({ ok: false, error: "INTAKE_NOT_CONFIGURED" }, 503);
  }

  const presented = req.headers.get("x-hub-signature-256") ?? "";
  if (!presented.startsWith("sha256=")) {
    return json({ ok: false, error: "SIGNATURE_MISSING" }, 401);
  }

  // The signature covers the RAW body — read text before any JSON parsing.
  const rawBody = await req.text();
  const expected = await hmacSha256Hex(secret, rawBody);
  if (!timingSafeEqual(presented.slice("sha256=".length), expected)) {
    return json({ ok: false, error: "SIGNATURE_INVALID" }, 401);
  }

  const event = req.headers.get("x-github-event") ?? "unknown";
  const delivery = req.headers.get("x-github-delivery") ?? "";

  if (event === "ping") {
    return json({ ok: true, pong: true, delivery });
  }

  // Verified as genuinely GitHub's. v1 acknowledges receipt; persistence
  // and routing are the follow-up named in the landing PR.
  let action = "";
  try {
    const payload = JSON.parse(rawBody) as { action?: unknown };
    action = typeof payload.action === "string" ? payload.action : "";
  } catch {
    // A signed-but-unparseable body is still acknowledged: GitHub delivered
    // it and retrying will not fix the payload's shape.
  }

  return json({ ok: true, received: true, event, action, delivery });
});
