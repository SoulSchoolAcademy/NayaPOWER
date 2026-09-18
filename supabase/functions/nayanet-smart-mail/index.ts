import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2.57.0";

type SendBody = {
  recipient_user_id: string;
  body: string;
  subject?: string;
  kind?: "direct" | "room" | "group" | "list";
  idempotency_key: string;
  project_id?: string;
};

const json = (payload: unknown, status = 200) =>
  new Response(JSON.stringify(payload), {
    status,
    headers: { "content-type": "application/json", "cache-control": "no-store" },
  });

Deno.serve(async (req) => {
  if (req.method !== "POST") return json({ ok: false, error: "METHOD_NOT_ALLOWED" }, 405);

  const authHeader = req.headers.get("authorization");
  if (!authHeader?.startsWith("Bearer ")) return json({ ok: false, error: "AUTH_REQUIRED" }, 401);

  const url = Deno.env.get("SUPABASE_URL")!;
  const anon = Deno.env.get("SUPABASE_ANON_KEY")!;
  const service = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
  const userClient = createClient(url, anon, { global: { headers: { Authorization: authHeader } } });
  const admin = createClient(url, service);

  const { data: userData, error: userError } = await userClient.auth.getUser();
  if (userError || !userData.user) return json({ ok: false, error: "AUTH_INVALID" }, 401);
  const senderId = userData.user.id;

  let input: SendBody;
  try { input = await req.json(); } catch { return json({ ok: false, error: "INVALID_JSON" }, 400); }

  if (!input?.recipient_user_id || !input?.body || !input?.idempotency_key) {
    return json({ ok: false, error: "RECIPIENT_BODY_IDEMPOTENCY_REQUIRED" }, 400);
  }
  if (input.recipient_user_id === senderId) return json({ ok: false, error: "SELF_RECIPIENT_NOT_ALLOWED" }, 400);
  if (input.body.length > 10000) return json({ ok: false, error: "BODY_TOO_LARGE" }, 400);

  const { data: recipient } = await admin.auth.admin.getUserById(input.recipient_user_id);
  if (!recipient?.user) return json({ ok: false, error: "RECIPIENT_NOT_FOUND" }, 404);

  const { data: existing } = await admin
    .from("v7_mail_messages")
    .select("id,thread_id,sender_id,body,metadata,created_at")
    .eq("sender_id", senderId)
    .eq("metadata->>idempotency_key", input.idempotency_key)
    .maybeSingle();

  if (existing) {
    return json({
      ok: true, status: "REPLAY",
      correlation_id: existing.metadata?.correlation_id ?? null,
      thread_id: existing.thread_id,
      message_id: existing.id,
      execution_receipt_id: existing.metadata?.execution_receipt_id ?? null,
    });
  }

  const correlationId = crypto.randomUUID();
  const kind = input.kind ?? "direct";
  const { data: thread, error: threadError } = await admin
    .from("v7_mail_threads")
    .insert({ created_by: senderId, kind, subject: input.subject ?? "NayaNET P0 communication proof" })
    .select("id")
    .single();
  if (threadError) return json({ ok: false, error: "THREAD_CREATE_FAILED", detail: threadError.message }, 500);

  const { error: membersError } = await admin.from("v7_mail_members").insert([
    { thread_id: thread.id, user_id: senderId },
    { thread_id: thread.id, user_id: input.recipient_user_id },
  ]);
  if (membersError) return json({ ok: false, error: "MEMBER_CREATE_FAILED", detail: membersError.message }, 500);

  const metadata = {
    schema_version: "NAYANET_SMART_MAIL_P0_V1",
    correlation_id: correlationId,
    idempotency_key: input.idempotency_key,
    sender_id: senderId,
    receiver_id: input.recipient_user_id,
    governance: {
      capability: "SMART_MAIL_SEND",
      authorization_basis: "authenticated_sender_session",
      model_authority: false,
      authority_changed: false,
    },
    lifecycle: ["PROPOSED", "INVESTIGATING", "READY", "AUTHORIZED", "EXECUTING", "EXECUTED", "OBSERVED", "VERIFIED"],
  };

  const { data: message, error: messageError } = await admin
    .from("v7_mail_messages")
    .insert({ thread_id: thread.id, sender_id: senderId, body: input.body, metadata })
    .select("id,thread_id,created_at")
    .single();
  if (messageError) return json({ ok: false, error: "MESSAGE_CREATE_FAILED", detail: messageError.message }, 500);

  const eventId = `smart-mail-proof-${correlationId.replaceAll("-", "")}`;
  const { data: event, error: eventError } = await admin
    .from("nayanet_cognition_events")
    .insert({
      user_id: senderId,
      project_id: input.project_id ?? "NayaNET",
      event_id: eventId,
      type: "communication",
      classification: "observation",
      title: "NayaNET Smart Mail P0 transaction",
      content: input.body,
      source: "nayanet-smart-mail",
      status: "active",
      actor: "human",
      confidence: 1,
      tags: ["smart-mail", "p0", "sender-receiver-proof"],
      source_hash: "",
      schema_version: "1.0.0",
      metadata: { correlation_id: correlationId, message_id: message.id, receiver_id: input.recipient_user_id },
    })
    .select("id")
    .single();
  if (eventError) return json({ ok: false, error: "COGNITION_CAPTURE_FAILED", detail: eventError.message }, 500);

  const { data: receipt, error: receiptError } = await admin
    .from("nayanet_execution_receipts")
    .insert({
      user_id: senderId,
      project_id: input.project_id ?? "NayaNET",
      revision: 1,
      action: "smart_mail_send",
      expected_result: "Authenticated sender message is delivered to authorized receiver and remains retrievable.",
      observed_result: "Thread, members, message and cognition event persisted.",
      status: "SUCCESS",
      evidence: [{
        correlation_id: correlationId,
        thread_id: thread.id,
        message_id: message.id,
        cognition_event_id: event.id,
        sender_id: senderId,
        receiver_id: input.recipient_user_id,
        observed_at: new Date().toISOString(),
      }],
      learning: [{ status: "captured", statement: "Smart Mail P0 sender transaction persisted through the canonical cognition boundary." }],
    })
    .select("id")
    .single();
  if (receiptError) return json({ ok: false, error: "RECEIPT_CREATE_FAILED", detail: receiptError.message }, 500);

  const finalMetadata = { ...metadata, execution_receipt_id: receipt.id, cognition_event_id: event.id };
  await admin.from("v7_mail_messages").update({ metadata: finalMetadata }).eq("id", message.id);

  return json({
    ok: true,
    status: "CREATED",
    correlation_id: correlationId,
    thread_id: thread.id,
    message_id: message.id,
    cognition_event_id: event.id,
    execution_receipt_id: receipt.id,
    authority_changed: false,
  });
});
