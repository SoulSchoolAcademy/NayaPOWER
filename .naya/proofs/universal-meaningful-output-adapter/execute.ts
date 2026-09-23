const BASE_URL = Deno.env.get("NAYANET_FUNCTION_URL") ?? "https://dahisasgpfvziswqvmvm.supabase.co/functions/v1/nayanet-compound-intelligence";
const ACCESS_TOKEN = Deno.env.get("NAYANET_TEST_ACCESS_TOKEN") ?? "";
if (!ACCESS_TOKEN) throw new Error("NAYANET_TEST_ACCESS_TOKEN_REQUIRED");

const idempotencyKey = "umo-tool-result-proof-001";
const input = {
  output_id: "tool-result:adapter-proof-001",
  output_version: 1,
  event_at: "2026-09-23T20:00:00Z",
  source_ref: "tool-result:adapter-proof-001",
  source_type: "tool_result",
  title: "Canonical resolver lesson",
  content: "Use the existing canonical resolver instead of creating a parallel intelligence destination.",
  meaning: "Prevents duplicate memory paths and preserves one authoritative intelligence system.",
  materiality: "REUSABLE",
  proposed_use: "Apply the canonical resolver rule when routing future meaningful outputs.",
  applicable_scope: "NayaNET intelligence routing only.",
  uncertainties: [],
  provenance_refs: ["tool-result:adapter-proof-001"],
  evidence_state: "OBSERVED",
  privacy: "PRIVATE",
  requested_action: "ROUTE_IF_AUTHORIZED",
  destination_class: "existing_intelligence"
};

function commitBody() {
  return {
    action: "universal_meaningful_output",
    idempotency_key: idempotencyKey,
    title: input.title,
    content: input.content,
    category: "INTELLIGENCE",
    topic: "UNIVERSAL_MEANINGFUL_OUTPUT_ADAPTER",
    tags: ["universal-adapter", "tool-result", "bounded-proof"],
    confidence: 0.8,
    applicable_scope: input.applicable_scope,
    learning_claim: input.meaning,
    authority_scope: "PERSONAL_INTELLIGENCE_ONLY",
    next_use: input.proposed_use,
    unknown: input.uncertainties,
    value_context: {
      source_type: input.source_type,
      output_id: input.output_id,
      output_version: input.output_version,
      source_ref: input.source_ref,
      provenance_refs: input.provenance_refs,
      evidence_state: input.evidence_state,
      privacy: input.privacy,
      destination_class: input.destination_class
    }
  };
}

async function callCommit() {
  const r = await fetch(BASE_URL, {
    method: "POST",
    headers: {
      Authorization: "Bearer " + ACCESS_TOKEN,
      "Content-Type": "application/json",
      "x-idempotency-key": idempotencyKey
    },
    body: JSON.stringify(commitBody())
  });
  const data = await r.json().catch(() => ({}));
  if (!r.ok) throw new Error("INTELLIGENCE_COMMIT_HTTP_" + r.status + "::" + JSON.stringify(data));
  return data;
}

const first = await callCommit();
if (first?.status !== "CAPTURED_INTEGRATED_CHECKPOINTED") {
  throw new Error("PROMOTION_STATUS_ASSERTION_FAILED");
}
if (first?.source_event?.event_id !== "intelligence:" + idempotencyKey) {
  throw new Error("CANONICAL_EVENT_ID_ASSERTION_FAILED");
}
if (first?.checkpoint?.checkpoint_id !== "checkpoint:" + idempotencyKey) {
  throw new Error("CHECKPOINT_ID_ASSERTION_FAILED");
}
if (!first?.checkpoint?.receipt_id && !first?.checkpoint?.receipt?.id) {
  throw new Error("CHECKPOINT_RECEIPT_ASSERTION_FAILED");
}

const second = await callCommit();
if (second?.source_event?.event_id !== first?.source_event?.event_id) {
  throw new Error("IDEMPOTENT_EVENT_ID_ASSERTION_FAILED");
}
if (second?.checkpoint?.checkpoint_id !== first?.checkpoint?.checkpoint_id) {
  throw new Error("IDEMPOTENT_CHECKPOINT_ASSERTION_FAILED");
}

console.log(JSON.stringify({
  proof_id: "UMOA-TOOLRESULT-001",
  status: "COMMIT_BOUNDARY_PASSED",
  event_id: first.source_event.event_id,
  checkpoint_id: first.checkpoint.checkpoint_id,
  receipt_id: first.checkpoint.receipt_id ?? first.checkpoint.receipt?.id ?? null,
  replay_event_id: second.source_event.event_id,
  next_required: "independent DB provenance/index/block/retrieval assertions"
}, null, 2));
