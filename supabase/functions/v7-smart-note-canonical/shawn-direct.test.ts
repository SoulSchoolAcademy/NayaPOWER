// Tests for the SN-0782 shawn_direct receiver change.
// A capture carrying a valid shawn_direct verification marker writes ACTIVE with
// verification_method shawn_direct_verification; malformed markers fail soft to
// CANDIDATE with the refusal recorded. Replays/existing rows are never upgraded.

import { assertEquals, assert } from "https://deno.land/std@0.208.0/assert/mod.ts";

// Mirror of validateShawnDirectMarker in v7-smart-note-canonical/index.ts
async function sha256Hex(value: unknown): Promise<string> {
  const canonicalize = (v: unknown): unknown => {
    if (Array.isArray(v)) return v.map(canonicalize);
    if (v && typeof v === "object")
      return Object.fromEntries(
        Object.entries(v as Record<string, unknown>)
          .sort(([a], [b]) => a.localeCompare(b))
          .map(([k, val]) => [k, canonicalize(val)]),
      );
    return v;
  };
  const encoded = new TextEncoder().encode(JSON.stringify(canonicalize(value)));
  const digest = await crypto.subtle.digest("SHA-256", encoded);
  return [...new Uint8Array(digest)].map((b) => b.toString(16).padStart(2, "0")).join("");
}

async function validateShawnDirectMarker(
  raw: unknown,
  now: string,
): Promise<{ ok: boolean; directive_digest: string | null; refusal: string | null; record: Record<string, string> }> {
  const v = (raw && typeof raw === "object" ? raw : null) as Record<string, unknown> | null;
  const refused = (code: string) => ({ ok: false, directive_digest: null, refusal: code, record: {} });
  if (!v) return refused("NOT_SHAWN_VERIFIED");
  if (String(v.source ?? "") !== "shawn_direct") return refused("NOT_SHAWN_VERIFIED");
  if (String(v.verifier ?? "") !== "Shawn") return refused("NOT_SHAWN_VERIFIED");
  const quote = String(v.quote ?? "").trim();
  if (quote.length < 8) return refused("MALFORMED_MARKER_QUOTE");
  const directedAt = String(v.directed_at ?? "");
  const directedMs = Date.parse(directedAt);
  if (!directedAt || Number.isNaN(directedMs)) return refused("MALFORMED_MARKER_TIME");
  if (directedMs > Date.parse(now) + 60000) return refused("FUTURE_DIRECTED_AT");
  const directiveRef = String(v.directive_ref ?? "");
  const chatRef = /^chat:[A-Za-z0-9_.:-]{1,128}$/.test(directiveRef);
  const feedRef = /^feed:\d+#issuecomment-\d+$/.test(directiveRef);
  if (!chatRef && !feedRef) return refused("MALFORMED_MARKER_REF");
  const directiveDigest = await sha256Hex({ quote, directed_at: directedAt, directive_ref: directiveRef });
  return {
    ok: true,
    directive_digest: directiveDigest,
    refusal: null,
    record: {
      source: "shawn_direct",
      verifier: "Shawn",
      quote: quote.slice(0, 2000),
      directed_at: directedAt,
      directive_ref: directiveRef,
      directive_digest: directiveDigest,
      verified_at: now,
    },
  };
}

// Mirror of the insert decision in v7-smart-note-canonical/index.ts
function decideInsert(
  shawnDirect: { ok: boolean; directive_digest: string | null; refusal: string | null; record: Record<string, string> },
  existing: boolean,
) {
  if (existing) return { action: "skip" as const }; // replays never upgraded
  return {
    action: "insert" as const,
    status: shawnDirect.ok ? "ACTIVE" : "CANDIDATE",
    verification_method: shawnDirect.ok ? "shawn_direct_verification" : "PENDING_OUTCOME_VERIFICATION",
    refusal: shawnDirect.refusal,
    hasRecord: Object.keys(shawnDirect.record).length > 0,
  };
}

const NOW = "2026-10-09T18:00:00.000Z";
const validChat = {
  source: "shawn_direct",
  verifier: "Shawn",
  quote: "smart note this: the river must flow",
  directed_at: "2026-10-09T17:59:00.000Z",
  directive_ref: "chat:01JABCD2EFGH3",
};
const validFeed = { ...validChat, directive_ref: "feed:1354#issuecomment-6086458465" };

Deno.test("valid chat marker activates", async () => {
  const r = await validateShawnDirectMarker(validChat, NOW);
  assertEquals(r.ok, true);
  assertEquals(r.refusal, null);
  assert(r.directive_digest && r.directive_digest.length === 64);
  assertEquals(r.record.verifier, "Shawn");
  assertEquals(r.record.directive_ref, validChat.directive_ref);
});

Deno.test("valid feed marker activates", async () => {
  const r = await validateShawnDirectMarker(validFeed, NOW);
  assertEquals(r.ok, true);
  assertEquals(r.record.directive_ref, validFeed.directive_ref);
});

Deno.test("missing verification fails soft, never lost", async () => {
  const r = await validateShawnDirectMarker(null, NOW);
  assertEquals(r.ok, false);
  assertEquals(r.refusal, "NOT_SHAWN_VERIFIED");
  const d = decideInsert(r, false);
  assertEquals(d.status, "CANDIDATE"); // fail-soft: capture still 200s, note kept
  assertEquals(d.verification_method, "PENDING_OUTCOME_VERIFICATION");
});

Deno.test("wrong source refused", async () => {
  const r = await validateShawnDirectMarker({ ...validChat, source: "agent_self" }, NOW);
  assertEquals(r.refusal, "NOT_SHAWN_VERIFIED");
});

Deno.test("wrong verifier refused", async () => {
  const r = await validateShawnDirectMarker({ ...validChat, verifier: "Naya-5" }, NOW);
  assertEquals(r.refusal, "NOT_SHAWN_VERIFIED");
});

Deno.test("short quote refused", async () => {
  const r = await validateShawnDirectMarker({ ...validChat, quote: "note it" }, NOW);
  assertEquals(r.refusal, "MALFORMED_MARKER_QUOTE");
});

Deno.test("unparseable directed_at refused", async () => {
  const r = await validateShawnDirectMarker({ ...validChat, directed_at: "sometime" }, NOW);
  assertEquals(r.refusal, "MALFORMED_MARKER_TIME");
});

Deno.test("future directed_at refused", async () => {
  const r = await validateShawnDirectMarker({ ...validChat, directed_at: "2026-10-10T18:00:00.000Z" }, NOW);
  assertEquals(r.refusal, "FUTURE_DIRECTED_AT");
});

Deno.test("malformed directive_ref refused", async () => {
  const r = await validateShawnDirectMarker({ ...validChat, directive_ref: "feed:abc#issuecomment-x" }, NOW);
  assertEquals(r.refusal, "MALFORMED_MARKER_REF");
});

Deno.test("digest binds content: different quote, different digest", async () => {
  const a = await validateShawnDirectMarker(validChat, NOW);
  const b = await validateShawnDirectMarker({ ...validChat, quote: "smart note this: something else" }, NOW);
  assert(a.directive_digest !== b.directive_digest, "replayed marker on different content must not collide");
});

Deno.test("digest is idempotent for identical content", async () => {
  const a = await validateShawnDirectMarker(validChat, NOW);
  const b = await validateShawnDirectMarker(validChat, NOW);
  assertEquals(a.directive_digest, b.directive_digest);
});

Deno.test("mocked insert matrix: valid -> ACTIVE, malformed -> CANDIDATE, replay -> skip", async () => {
  const good = decideInsert(await validateShawnDirectMarker(validChat, NOW), false);
  assertEquals(good.action, "insert");
  assertEquals(good.status, "ACTIVE");
  assertEquals(good.verification_method, "shawn_direct_verification");
  assertEquals(good.hasRecord, true);

  const bad = decideInsert(await validateShawnDirectMarker({ ...validChat, quote: "x" }, NOW), false);
  assertEquals(bad.status, "CANDIDATE");
  assertEquals(bad.refusal, "MALFORMED_MARKER_QUOTE");

  const replay = decideInsert(await validateShawnDirectMarker(validChat, NOW), true);
  assertEquals(replay.action, "skip"); // existing rows never upgraded
});

Deno.test("status vocabulary: ACTIVE only, never VERIFIED", async () => {
  const good = decideInsert(await validateShawnDirectMarker(validFeed, NOW), false);
  const status = String((good as { status?: unknown }).status);
  assert(status === "ACTIVE", "valid marker must write ACTIVE per decision receipt R1");
  const forbidden: string = "VERIFIED";
  assert(status !== forbidden, "VERIFIED would violate the check constraint and be invisible to readers");
});
