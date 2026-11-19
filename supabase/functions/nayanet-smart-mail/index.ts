// nayanet-smart-mail — Smart Mail send, server-side.
// v35 (2026-11-19). Replaces the lost v34 source: the deployed v34 function
// rejected every payload shape with RECIPIENT_BODY_IDEMPOTENCY_REQUIRED and
// its source was never filed to the repo. This version is the filed source
// of record for the slug `nayanet-smart-mail`.
//
// What it does:
//   Browser pages call this function with their Supabase Auth JWT
//   (verify_jwt: true — the gateway rejects calls without a valid JWT).
//   The function reads the sender's smart_alias from the JWT claims,
//   resolves the recipient alias, and writes the message to the live
//   Smart Mail tables (smart_mail_threads / smart_mail_messages) using
//   the service_role key — exactly the write path the mail helper proved
//   (test send landed, no 42501).
//
// The service key lives ONLY in the function runtime env
// (SUPABASE_SERVICE_ROLE_KEY, auto-provisioned by Supabase). It NEVER
// appears in this source, in the repo, in logs, or in any browser payload.
//
// What it does NOT do:
//   - No privacy-rule change. Reads are unchanged; this function sends.
//   - No v7 tables: the v7 mail tables (v7_mail_threads/messages) and the
//     RPC nayanet_send_smart_mail from migration 20260826000501 do NOT
//     exist in the live database (verified 2026-11-19 via the Management
//     API query endpoint). The live mail system is the alias-based
//     smart_mail_* tables only, so this function writes those directly.
//
// Idempotency: the message id is a deterministic UUIDv5 of
// (sender, recipient, body, idempotency_key); a replayed send returns
// status REPLAY with the original ids instead of writing a duplicate.
// The thread id is a deterministic UUIDv5 of (sender, recipient, subject),
// so a replay reuses the same thread.
//
// Interface (POST, JSON):
//   { "recipient": "<alias or uuid>", "subject": "<text>", "body": "<text>",
//     "idempotency_key": "<uuid or unique string>", "kind": "<optional>" }
// Response: { "ok": true, "status": "SENT" | "REPLAY",
//             "thread_id": "<uuid>", "message_id": "<uuid>" }
// Errors: 405 METHOD_NOT_ALLOWED · 400 INVALID_JSON ·
//         401 AUTH_INVALID · 400 RECIPIENT_BODY_IDEMPOTENCY_REQUIRED ·
//         400 BODY_TOO_LONG · 400 SENDER_IS_RECIPIENT ·
//         404 RECIPIENT_NOT_FOUND · 502 MAIL_WRITE_FAILED

const SUPABASE_URL = Deno.env.get("SUPABASE_URL") ?? "";
const SERVICE_KEY = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY") ?? "";
const MAX_BODY = 10_000;
const UUID_RE =
  /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;

function json(body: unknown, status = 200): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: {
      "Content-Type": "application/json",
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Headers":
        "authorization, apikey, content-type, x-client-info",
      "Access-Control-Allow-Methods": "POST, OPTIONS",
    },
  });
}

function b64urlDecode(input: string): string {
  const s = input.replace(/-/g, "+").replace(/_/g, "/");
  const pad = s.length % 4 === 0 ? "" : "=".repeat(4 - (s.length % 4));
  return atob(s + pad);
}

function jwtClaims(authHeader: string | null): Record<string, unknown> | null {
  if (!authHeader || !authHeader.startsWith("Bearer ")) return null;
  const token = authHeader.slice("Bearer ".length).trim();
  const parts = token.split(".");
  if (parts.length !== 3) return null;
  try {
    return JSON.parse(b64urlDecode(parts[1])) as Record<string, unknown>;
  } catch {
    return null;
  }
}

function claimAlias(claims: Record<string, unknown>): string | null {
  for (const key of ["user_metadata", "app_metadata"]) {
    const md = claims[key];
    if (md && typeof md === "object") {
      const alias = (md as Record<string, unknown>)["smart_alias"];
      if (typeof alias === "string" && alias.trim()) return alias.trim();
    }
  }
  const direct = claims["smart_alias"];
  if (typeof direct === "string" && direct.trim()) return direct.trim();
  return null;
}

async function uuidV5(namespace: string, name: string): Promise<string> {
  const data = new TextEncoder().encode(namespace + ":" + name);
  const hash = new Uint8Array(await crypto.subtle.digest("SHA-256", data));
  const b = Array.from(hash.slice(0, 16));
  b[6] = (b[6] & 0x0f) | 0x50; // version 5
  b[8] = (b[8] & 0x3f) | 0x80; // variant RFC 4122
  const hex = b.map((x) => x.toString(16).padStart(2, "0")).join("");
  return `${hex.slice(0, 8)}-${hex.slice(8, 12)}-${hex.slice(12, 16)}-${hex.slice(16, 20)}-${hex.slice(20, 32)}`;
}

type RestResult = { ok: boolean; status: number; rows: unknown };

async function rest(
  method: string,
  path: string,
  body?: unknown,
  extraHeaders?: Record<string, string>,
): Promise<RestResult> {
  const res = await fetch(`${SUPABASE_URL}/rest/v1${path}`, {
    method,
    headers: {
      apikey: SERVICE_KEY,
      Authorization: `Bearer ${SERVICE_KEY}`,
      "Content-Type": "application/json",
      Prefer: "return=representation",
      ...(extraHeaders ?? {}),
    },
    body: body === undefined ? undefined : JSON.stringify(body),
  });
  let rows: unknown = null;
  const text = await res.text();
  if (text) {
    try {
      rows = JSON.parse(text);
    } catch {
      rows = text;
    }
  }
  return { ok: res.ok, status: res.status, rows };
}

// Does the recipient alias exist? Check smart_mail_aliases first, then any
// auth user carrying the alias in smart_alias metadata.
async function recipientExists(alias: string): Promise<boolean> {
  if (UUID_RE.test(alias)) return true; // a uuid is used as-is
  const byTable = await rest(
    "GET",
    `/smart_mail_aliases?alias=eq.${encodeURIComponent(alias)}&select=alias`,
  );
  if (byTable.ok && Array.isArray(byTable.rows) && byTable.rows.length > 0) {
    return true;
  }
  // Auth Admin API: list users, match user_metadata/app_metadata smart_alias.
  for (let page = 1; page <= 5; page++) {
    const res = await fetch(
      `${SUPABASE_URL}/auth/v1/admin/users?page=${page}&per_page=100`,
      {
        headers: {
          apikey: SERVICE_KEY,
          Authorization: `Bearer ${SERVICE_KEY}`,
        },
      },
    );
    if (!res.ok) return false;
    const data = (await res.json()) as {
      users?: Array<{
        user_metadata?: Record<string, unknown>;
        app_metadata?: Record<string, unknown>;
      }>;
    };
    const users = data.users ?? [];
    for (const u of users) {
      for (const md of [u.user_metadata, u.app_metadata]) {
        if (md && md["smart_alias"] === alias) return true;
      }
    }
    if (users.length < 100) break;
  }
  return false;
}

Deno.serve(async (req: Request): Promise<Response> => {
  if (req.method === "OPTIONS") {
    return new Response(null, {
      status: 204,
      headers: {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers":
          "authorization, apikey, content-type, x-client-info",
        "Access-Control-Allow-Methods": "POST, OPTIONS",
      },
    });
  }
  if (req.method !== "POST") {
    return json({ ok: false, error: "METHOD_NOT_ALLOWED" }, 405);
  }
  if (!SUPABASE_URL || !SERVICE_KEY) {
    return json({ ok: false, error: "MAIL_WRITE_FAILED" }, 502);
  }

  let payload: Record<string, unknown>;
  try {
    payload = (await req.json()) as Record<string, unknown>;
  } catch {
    return json({ ok: false, error: "INVALID_JSON" }, 400);
  }

  // Sender identity comes from the JWT, never from the body.
  const claims = jwtClaims(req.headers.get("Authorization"));
  const senderAlias = claims ? claimAlias(claims) : null;
  if (!claims || claims["role"] !== "authenticated" || !senderAlias) {
    return json({ ok: false, error: "AUTH_INVALID" }, 401);
  }

  const recipientRaw = payload["recipient"];
  const bodyRaw = payload["body"];
  const idemRaw = payload["idempotency_key"];
  if (
    typeof recipientRaw !== "string" || !recipientRaw.trim() ||
    typeof bodyRaw !== "string" || !bodyRaw.trim() ||
    typeof idemRaw !== "string" || !idemRaw.trim()
  ) {
    return json(
      { ok: false, error: "RECIPIENT_BODY_IDEMPOTENCY_REQUIRED" },
      400,
    );
  }
  const recipient = recipientRaw.trim();
  const body = bodyRaw;
  const idempotencyKey = idemRaw.trim();
  const subjectRaw = payload["subject"];
  const subject = typeof subjectRaw === "string" && subjectRaw.trim()
    ? subjectRaw.trim()
    : "(no subject)";

  if (body.length > MAX_BODY) {
    return json({ ok: false, error: "BODY_TOO_LONG" }, 400);
  }
  if (recipient === senderAlias) {
    return json({ ok: false, error: "SENDER_IS_RECIPIENT" }, 400);
  }
  if (!(await recipientExists(recipient))) {
    return json({ ok: false, error: "RECIPIENT_NOT_FOUND" }, 404);
  }

  const threadId = await uuidV5("nayanet-smart-mail-thread", [
    senderAlias,
    recipient,
    subject,
  ].join("|"));
  const messageId = await uuidV5("nayanet-smart-mail-message", [
    threadId,
    idempotencyKey,
    body,
  ].join("|"));

  // Idempotency: if this exact send already landed, replay it, don't duplicate.
  const existing = await rest(
    "GET",
    `/smart_mail_messages?id=eq.${messageId}&select=id,thread_id`,
  );
  if (existing.ok && Array.isArray(existing.rows) && existing.rows.length > 0) {
    return json({
      ok: true,
      status: "REPLAY",
      thread_id: threadId,
      message_id: messageId,
    });
  }

  // Thread: reuse if the deterministic thread already exists.
  const threadCheck = await rest(
    "GET",
    `/smart_mail_threads?id=eq.${threadId}&select=id`,
  );
  if (!(threadCheck.ok && Array.isArray(threadCheck.rows) && threadCheck.rows.length > 0)) {
    const created = await rest("POST", "/smart_mail_threads", {
      id: threadId,
      subject,
      from_alias: senderAlias,
      to_alias: recipient,
      preview: body.slice(0, 120),
    });
    if (!created.ok) {
      return json(
        { ok: false, error: "MAIL_WRITE_FAILED", status: created.status },
        502,
      );
    }
  }

  const sent = await rest("POST", "/smart_mail_messages", {
    id: messageId,
    thread_id: threadId,
    from_alias: senderAlias,
    body,
  });
  if (!sent.ok) {
    return json(
      { ok: false, error: "MAIL_WRITE_FAILED", status: sent.status },
      502,
    );
  }

  return json({
    ok: true,
    status: "SENT",
    thread_id: threadId,
    message_id: messageId,
  });
});
