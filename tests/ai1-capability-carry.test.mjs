import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import test from "node:test";
import {
  CAPABILITY_VALUES,
  CapabilityValidationError,
  buildPersistedContent,
  validateCapabilities,
} from "../supabase/functions/nayanet-intelligence-commit-runtime/capability-vocabulary.ts";
import {
  deriveCapabilities,
  isEligibleBlock,
  selectKnowContext,
} from "../supabase/functions/nayanet-know-runtime/know.ts";

// AI1 capability carry (repair/ai1-capability-carry): contract tests for the
// writer <-> selector capability seam.
//
// What these tests prove, and what they do NOT prove:
//   - They import the ACTUAL selector (know.ts) and the ACTUAL vocabulary
//     module. Nothing is reimplemented; there is no synthetic fallback.
//   - The persisted-shape builder (buildPersistedContent) is the reference
//     implementation the SQL writer mirrors. The SQL itself cannot execute
//     here (no database in this environment); the migration text is asserted
//     separately (mirror-agreement test), and live-SQL execution remains a
//     reviewer-verified step. That limitation is stated, not hidden.
//   - Fixture blocks that need servability use understanding_state VERIFIED
//     and are labeled TEST-ONLY: the real writer persists CANDIDATE, which is
//     honestly NOT servable (proven by the non-servable negative below). The
//     repair manufactures no servability.
//   - No alternate retrieval path is exercised: only selectKnowContext.

const OWNER = "owner-ai1-test";
const NAYA_ID = "NAYA-NODE-0001";

// A block row shaped EXACTLY as the SQL writer stamps it (post this repair's
// migration): content carries capabilities only when declared; provenance
// carries the declaration record only then; everything else is the
// pre-existing writer shape.
const writerRow = (overrides = {}) => ({
  intelligent_block_id: "IB-AI1-000101",
  owner_id: OWNER,
  status: "DURABLE",
  // TEST-ONLY servability: the real writer stamps CANDIDATE (unservable).
  // Servable states here exist solely to isolate the CAPABILITY seam from the
  // STATE seam; the CANDIDATE negative proves the state gate still holds.
  understanding_state: "VERIFIED",
  owner_scope: "PRIVATE",
  applicable_scope: { target: NAYA_ID, project_id: "NayaNET" },
  content: { lesson: "L", topic: "T", category: "C" },
  provenance: { stage: "CAPTURE+PERSIST", source: "nayanet" },
  evidence_refs: [{ receipt: "ai1-receipt-1" }],
  superseded_by_block_id: null,
  updated_at: "2026-09-30T00:00:00Z",
  connections: [],
  ...overrides,
});

const knowReq = (overrides = {}) => ({
  owner_id: OWNER,
  naya_id: NAYA_ID,
  task_id: "AI1-TEST-001",
  task_class: "GOVERNANCE_TRIAGE",
  required_capability: "governance_triage",
  ...overrides,
});

// Doctrine-like lesson text in the spirit of SN-013 (6→10 doctrine). It must
// NOT contain the legacy fallback pattern ("preserve provenance..."), so any
// selectability comes from carried capabilities, never the fallback.
const DOCTRINE_LIKE_LESSON =
  "Before acting, assess blast radius, reversibility, and risk versus reward. " +
  "A clear improvement with no plausible path to harm may proceed without asking; " +
  "uncertain direction or plausible harm requires asking first.";

// ---------------------------------------------------------------------------
// 1. Vocabulary testability: valid / unknown / empty / duplicate / wrong-type /
//    combination — all deterministic.
// ---------------------------------------------------------------------------

test("AI1-VOCAB-01: valid capability is accepted", () => {
  assert.deepEqual(validateCapabilities(["governance_triage"]), ["governance_triage"]);
  assert.deepEqual(validateCapabilities(["compounding_capture"]), ["compounding_capture"]);
});

test("AI1-VOCAB-02: unknown capability fails closed (commit must be rejected)", () => {
  assert.throws(() => validateCapabilities(["teleportation"]), (e) =>
    e instanceof CapabilityValidationError && e.code === "CAPABILITY_UNKNOWN");
  assert.throws(() => validateCapabilities(["governance_triage", "mind_control"]), (e) =>
    e instanceof CapabilityValidationError && e.code === "CAPABILITY_UNKNOWN");
});

test("AI1-VOCAB-03: empty input is deterministic (treated as absent)", () => {
  assert.equal(validateCapabilities([]), null);
  assert.equal(validateCapabilities(undefined), null);
  assert.equal(validateCapabilities(null), null);
});

test("AI1-VOCAB-04: duplicates are deterministic (deduped, sorted)", () => {
  assert.deepEqual(
    validateCapabilities(["compounding_capture", "governance_triage", "compounding_capture"]),
    ["compounding_capture", "governance_triage"],
  );
  assert.deepEqual(validateCapabilities(["governance_triage", "governance_triage"]), ["governance_triage"]);
});

test("AI1-VOCAB-05: wrong types fail closed", () => {
  assert.throws(() => validateCapabilities("governance_triage"), (e) =>
    e instanceof CapabilityValidationError && e.code === "CAPABILITY_MALFORMED");
  assert.throws(() => validateCapabilities([42]), (e) =>
    e instanceof CapabilityValidationError && e.code === "CAPABILITY_MALFORMED");
  assert.throws(() => validateCapabilities([null]), (e) =>
    e instanceof CapabilityValidationError && e.code === "CAPABILITY_MALFORMED");
  assert.throws(() => validateCapabilities([""]), (e) =>
    e instanceof CapabilityValidationError && e.code === "CAPABILITY_MALFORMED");
  assert.throws(() => validateCapabilities(["   "]), (e) =>
    e instanceof CapabilityValidationError && e.code === "CAPABILITY_MALFORMED");
});

test("AI1-VOCAB-06: normalization is deterministic (trim + lowercase); bad format rejected", () => {
  assert.deepEqual(validateCapabilities([" Governance_Triage "]), ["governance_triage"]);
  assert.deepEqual(validateCapabilities(["COMPOUNDING_CAPTURE"]), ["compounding_capture"]);
  // Hyphenated look-alikes are malformed: they must not silently become near-miss tags.
  assert.throws(() => validateCapabilities(["governance-triage"]), (e) =>
    e instanceof CapabilityValidationError && e.code === "CAPABILITY_MALFORMED");
});

test("AI1-VOCAB-07: unsupported combination fails closed; supported combination is deterministic", () => {
  assert.deepEqual(
    validateCapabilities(["governance_triage", "compounding_capture"]),
    ["compounding_capture", "governance_triage"],
  );
  assert.throws(() => validateCapabilities(["governance_triage", "unknown_combo"]), (e) =>
    e instanceof CapabilityValidationError && e.code === "CAPABILITY_UNKNOWN");
});

test("AI1-VOCAB-08: vocabulary is exactly the bounded pilot set", () => {
  assert.deepEqual([...CAPABILITY_VALUES].sort(), ["compounding_capture", "governance_triage"]);
});

// ---------------------------------------------------------------------------
// 2. Writer carry: capture -> persisted content shape.
// ---------------------------------------------------------------------------

test("AI1-WRITE-01: capture with capabilities persists them at content.capabilities", () => {
  const caps = validateCapabilities(["governance_triage"]);
  const content = buildPersistedContent(
    { lesson: DOCTRINE_LIKE_LESSON, topic: "doctrine", category: "governance" },
    caps,
  );
  assert.deepEqual(content.capabilities, ["governance_triage"]);
  assert.equal(content.lesson, DOCTRINE_LIKE_LESSON);
});

test("AI1-WRITE-02: no capabilities -> persisted shape byte-identical to pre-repair", () => {
  const content = buildPersistedContent(
    { lesson: DOCTRINE_LIKE_LESSON, topic: "doctrine", category: "governance" },
    validateCapabilities(undefined),
  );
  assert.deepEqual(content, {
    lesson: DOCTRINE_LIKE_LESSON,
    topic: "doctrine",
    category: "governance",
  });
  assert.ok(!("capabilities" in content), "no capabilities key may be written when absent");
});

test("AI1-WRITE-03: same capture + same code -> same persisted representation", () => {
  const once = JSON.stringify(buildPersistedContent(
    { lesson: "L", topic: "T", category: "C" },
    validateCapabilities(["governance_triage", "compounding_capture", "governance_triage"]),
  ));
  const twice = JSON.stringify(buildPersistedContent(
    { lesson: "L", topic: "T", category: "C" },
    validateCapabilities(["compounding_capture", "governance_triage"]),
  ));
  assert.equal(once, twice);
});

test("AI1-WRITE-04: writer has ONE canonical capability field; applicable_scope untouched", () => {
  // Canonical capability storage location = content.capabilities.
  // The writer must never write applicable_scope.capabilities (legacy
  // compatibility read-path only; forbidden for new writes).
  const content = buildPersistedContent(
    { lesson: "L", topic: "T", category: "C" },
    validateCapabilities(["governance_triage"]),
  );
  assert.ok(!("applicable_scope" in content));
});

test("AI1-WRITE-05: SQL mirror agrees with the canonical vocabulary (no second taxonomy)", () => {
  const migration = readFileSync(
    new URL("../supabase/migrations/20260930235959_ai1_capability_carry_v1.sql", import.meta.url),
    "utf8",
  );
  assert.match(migration, /capability-vocabulary\.ts/, "migration must name its canonical owner");
  for (const v of CAPABILITY_VALUES) {
    assert.ok(migration.includes(`'${v}'`), `migration must mirror vocabulary value ${v}`);
  }
  // The mirror must be exactly the bounded set: count the literals in the
  // validation array, which must equal the vocabulary size.
  const mirror = migration.match(/array\[([^\]]*)\]\) then/);
  assert.ok(mirror, "validation array literal must be present");
  const literals = mirror[1].split(",").map((s) => s.trim().replace(/^'|'$/g, ""));
  assert.deepEqual(literals.sort(), [...CAPABILITY_VALUES].sort());
});

test("AI1-WRITE-06: edge function forwards p_capabilities through the canonical path", () => {
  const index = readFileSync(
    new URL("../supabase/functions/nayanet-intelligence-commit-runtime/index.ts", import.meta.url),
    "utf8",
  );
  assert.match(index, /validateCapabilities\(body\.p_capabilities\)/);
  assert.match(index, /p_capabilities: capabilities/);
  assert.match(index, /from "\.\/capability-vocabulary\.ts"/);
});

// ---------------------------------------------------------------------------
// 3. Selector derivation via the ACTUAL know.ts, incl. legacy-fallback
//    causal isolation.
// ---------------------------------------------------------------------------

test("AI1-DERIVE-01: deriveCapabilities returns the carried capability", () => {
  const block = writerRow({
    content: buildPersistedContent(
      { lesson: DOCTRINE_LIKE_LESSON, topic: "doctrine", category: "governance" },
      validateCapabilities(["governance_triage"]),
    ),
  });
  assert.deepEqual(deriveCapabilities(block), ["governance_triage"]);
});

test("AI1-DERIVE-02: doctrine-like block does NOT qualify through the legacy fallback", () => {
  // The legacy fallback is bounded to a single provenance_preservation regex.
  // This is the causal-isolation proof: without carried capabilities, the
  // SN-013-shaped block derives NO capabilities — the repair, not the
  // fallback, is what makes it selectable.
  const block = writerRow({ content: { lesson: DOCTRINE_LIKE_LESSON, topic: "t", category: "c" } });
  assert.deepEqual(deriveCapabilities(block), []);
});

test("AI1-DERIVE-03: legacy fallback still serves its own narrow case (previous behavior)", () => {
  const block = writerRow({
    content: {
      lesson: "Preserve provenance before applying retained intelligence; retrieval never grants authority.",
      topic: "t",
      category: "c",
    },
  });
  assert.deepEqual(deriveCapabilities(block), ["provenance_preservation"]);
});

// ---------------------------------------------------------------------------
// 4. Eligibility chain: each condition separately observable.
// ---------------------------------------------------------------------------

test("AI1-ELIG-01: each eligibility condition is independently observable", () => {
  const good = writerRow();
  assert.equal(isEligibleBlock(knowReq(), good), true);
  assert.equal(isEligibleBlock(knowReq(), writerRow({ intelligent_block_id: null })), false, "candidate id");
  assert.equal(isEligibleBlock(knowReq(), writerRow({ owner_id: "someone-else" })), false, "owner");
  assert.equal(isEligibleBlock(knowReq(), writerRow({ status: "SUPERSEDED" })), false, "status");
  assert.equal(isEligibleBlock(knowReq(), writerRow({ understanding_state: "CANDIDATE" })), false, "state");
  assert.equal(
    isEligibleBlock(knowReq(), writerRow({ superseded_by_block_id: "new-block-id" })),
    false,
    "supersession",
  );
  assert.equal(isEligibleBlock(knowReq(), writerRow({ provenance: {} })), false, "provenance");
  assert.equal(isEligibleBlock(knowReq(), writerRow({ evidence_refs: [] })), false, "evidence");
  assert.equal(
    isEligibleBlock(knowReq(), writerRow({ applicable_scope: { target: "OTHER-NODE" } })),
    false,
    "scope target",
  );
});

// ---------------------------------------------------------------------------
// 5. Selection through the ACTUAL selectKnowContext: positive, four precision
//    negatives, superseded regression, injection resistance.
// ---------------------------------------------------------------------------

test("AI1-SELECT-01 (positive): valid block + correct capability -> HIT, zero authority", () => {
  const block = writerRow({
    intelligent_block_id: "IB-AI1-POSITIVE",
    content: buildPersistedContent(
      { lesson: DOCTRINE_LIKE_LESSON, topic: "doctrine", category: "governance" },
      validateCapabilities(["governance_triage"]),
    ),
  });
  const out = selectKnowContext(knowReq(), [block]);
  assert.equal(out.status, "HIT");
  assert.equal(out.selected_block_id, "IB-AI1-POSITIVE");
  assert.equal(out.retrieval_creates_authority, false, "capability metadata creates zero authority");
});

test("AI1-SELECT-02 (negative: wrong capability): valid block + wrong required_capability -> MISS", () => {
  const block = writerRow({
    intelligent_block_id: "IB-AI1-WRONGCAP",
    content: buildPersistedContent(
      { lesson: DOCTRINE_LIKE_LESSON, topic: "doctrine", category: "governance" },
      validateCapabilities(["governance_triage"]),
    ),
  });
  const out = selectKnowContext(knowReq({ required_capability: "compounding_capture" }), [block]);
  assert.equal(out.status, "MISS");
  assert.equal(out.selected_block_id, null);
});

test("AI1-SELECT-03 (negative: superseded regression): superseded block cannot be selected", () => {
  const block = writerRow({
    intelligent_block_id: "IB-AI1-SUPERSEDED",
    superseded_by_block_id: "IB-AI1-SUCCESSOR",
    content: buildPersistedContent(
      { lesson: DOCTRINE_LIKE_LESSON, topic: "doctrine", category: "governance" },
      validateCapabilities(["governance_triage"]),
    ),
  });
  const out = selectKnowContext(knowReq(), [block]);
  assert.equal(out.status, "MISS", "superseded rows are excluded even with a matching capability");
});

test("AI1-SELECT-04 (negative: non-servable state): CANDIDATE block is excluded", () => {
  // This is the honest state barrier: the real writer stamps CANDIDATE, which
  // the selector refuses. The repair does not manufacture servability.
  const block = writerRow({
    intelligent_block_id: "IB-AI1-CANDIDATE",
    understanding_state: "CANDIDATE",
    content: buildPersistedContent(
      { lesson: DOCTRINE_LIKE_LESSON, topic: "doctrine", category: "governance" },
      validateCapabilities(["governance_triage"]),
    ),
  });
  const out = selectKnowContext(knowReq(), [block]);
  assert.equal(out.status, "MISS");
});

test("AI1-SELECT-05 (negative: wrong owner): cross-owner block is excluded", () => {
  const block = writerRow({
    intelligent_block_id: "IB-AI1-WRONGOWNER",
    owner_id: "different-owner",
    content: buildPersistedContent(
      { lesson: DOCTRINE_LIKE_LESSON, topic: "doctrine", category: "governance" },
      validateCapabilities(["governance_triage"]),
    ),
  });
  const out = selectKnowContext(knowReq(), [block]);
  assert.equal(out.status, "MISS");
});

test("AI1-SELECT-06 (negative: unknown capability): unknown names cannot silently select", () => {
  // The governed writer path rejects unknown names, so no block carrying one
  // can be produced through the canonical commit. Even adversarially, the
  // selector only matches exact strings: a request for a real capability
  // never matches an unrelated tag.
  assert.throws(() => validateCapabilities(["governance_triagee"]), (e) =>
    e instanceof CapabilityValidationError && e.code === "CAPABILITY_UNKNOWN");
  const smuggled = writerRow({
    intelligent_block_id: "IB-AI1-SMUGGLED",
    content: { lesson: "L", topic: "t", category: "c", capabilities: ["governance_triagee"] },
  });
  const out = selectKnowContext(knowReq({ required_capability: "governance_triage" }), [smuggled]);
  assert.equal(out.status, "MISS");
});

test("AI1-SELECT-07 (negative: injection): capability words in lesson text do not select", () => {
  // No heuristic inference: the words "governance_triage" appearing in lesson
  // prose must not make the block retrievable for that capability.
  const block = writerRow({
    intelligent_block_id: "IB-AI1-INJECT",
    content: {
      lesson: "This lesson mentions governance_triage in prose but declares nothing.",
      topic: "t",
      category: "c",
    },
  });
  assert.deepEqual(deriveCapabilities(block), [], "prose is not metadata");
  const out = selectKnowContext(knowReq(), [block]);
  assert.equal(out.status, "MISS");
});

test("AI1-SELECT-08 (backward compatibility): no-capability block keeps previous behavior", () => {
  const block = writerRow({
    intelligent_block_id: "IB-AI1-LEGACY",
    content: { lesson: "An ordinary lesson with no tags and no legacy pattern.", topic: "t", category: "c" },
  });
  const out = selectKnowContext(knowReq(), [block]);
  assert.equal(out.status, "MISS", "identical to pre-repair behavior for untagged blocks");
});

// ---------------------------------------------------------------------------
// 6. Two independent pilots (TEST fixtures): full chain per capability.
//    Chain: capture -> validate -> persist shape -> derive -> select.
//    Servability state is VERIFIED here ONLY as a test fixture; the honest
//    production state for fresh commits is CANDIDATE (unservable), proven by
//    AI1-SELECT-04. The repair changes no states.
// ---------------------------------------------------------------------------

const pilotChain = (pilotId, capability, lesson) => {
  const validated = validateCapabilities([capability]);
  const content = buildPersistedContent({ lesson, topic: "pilot", category: "pilot" }, validated);
  // Registry-style content hash (canonical JSON, sorted keys, compact).
  const canonical = JSON.stringify(
    Object.fromEntries(Object.entries(content).sort(([a], [b]) => (a < b ? -1 : 1))),
  );
  const contentHash = createHash("sha256").update(canonical, "utf8").digest("hex");
  const block = writerRow({ intelligent_block_id: pilotId, content });
  const derived = deriveCapabilities(block);
  const result = selectKnowContext(
    knowReq({ task_id: `AI1-PILOT-${capability}`, required_capability: capability }),
    [block],
  );
  return { blockId: pilotId, contentHash, capabilityMetadata: content.capabilities, derived, result };
};

test("AI1-PILOT-01: governance_triage full chain", () => {
  const p = pilotChain("IB-AI1-PILOT-GT", "governance_triage", DOCTRINE_LIKE_LESSON);
  assert.deepEqual(p.capabilityMetadata, ["governance_triage"]);
  assert.deepEqual(p.derived, ["governance_triage"]);
  assert.equal(p.result.status, "HIT");
  assert.equal(p.result.selected_block_id, "IB-AI1-PILOT-GT");
  assert.equal(p.result.retrieval_creates_authority, false);
  assert.match(p.contentHash, /^[0-9a-f]{64}$/);
});

test("AI1-PILOT-02: compounding_capture full chain (independent)", () => {
  const lesson =
    "Capture substantive work products as durable intelligence so successors compound rather than restart.";
  const p = pilotChain("IB-AI1-PILOT-CC", "compounding_capture", lesson);
  assert.deepEqual(p.capabilityMetadata, ["compounding_capture"]);
  assert.deepEqual(p.derived, ["compounding_capture"]);
  assert.equal(p.result.status, "HIT");
  assert.equal(p.result.selected_block_id, "IB-AI1-PILOT-CC");
  assert.equal(p.result.retrieval_creates_authority, false);
  assert.match(p.contentHash, /^[0-9a-f]{64}$/);
});

test("AI1-PILOT-03: pilots are independent (cross-capability isolation)", () => {
  const gt = pilotChain("IB-AI1-X-GT", "governance_triage", DOCTRINE_LIKE_LESSON);
  const cc = pilotChain("IB-AI1-X-CC", "compounding_capture", "Capture discipline lesson.");
  // A governance_triage query must select the GT pilot, never the CC pilot.
  const out = selectKnowContext(
    knowReq({ task_id: "AI1-X", required_capability: "governance_triage" }),
    [
      writerRow({ intelligent_block_id: gt.blockId, content: { lesson: "l", topic: "t", category: "c", capabilities: gt.capabilityMetadata } }),
      writerRow({ intelligent_block_id: cc.blockId, content: { lesson: "l", topic: "t", category: "c", capabilities: cc.capabilityMetadata } }),
    ],
  );
  assert.equal(out.status, "HIT");
  assert.equal(out.selected_block_id, "IB-AI1-X-GT");
});

// ---------------------------------------------------------------------------
// 5. Dual-field contract: four cases + disagreement.
//
// The selector unions applicable_scope.capabilities (legacy compatibility
// path) with content.capabilities (canonical writer field) via
// structuredCapabilities(). These tests PIN the current deterministic
// behavior of the ACTUAL know.ts — they do not design new semantics.
// A future contract decision (union vs canonical-precedence vs fail-closed)
// changes code + tests together; until then, silence is replaced by pinned,
// deterministic, observed behavior.
// ---------------------------------------------------------------------------

const fieldRow = (contentCaps, scopeCaps) =>
  writerRow({
    intelligent_block_id: "IB-AI1-FIELD",
    content: {
      lesson: "l",
      topic: "t",
      category: "c",
      ...(contentCaps ? { capabilities: contentCaps } : {}),
    },
    applicable_scope: {
      target: NAYA_ID,
      project_id: "NayaNET",
      ...(scopeCaps ? { capabilities: scopeCaps } : {}),
    },
  });

const hitFor = (capability, block) =>
  selectKnowContext(knowReq({ task_id: `AI1-FIELD-${capability}`, required_capability: capability }), [block]).status;

test("AI1-FIELD-01: canonical-only -> derived has canonical; canonical query HITs, other MISSes", () => {
  const b = fieldRow(["governance_triage"], null);
  assert.deepEqual(deriveCapabilities(b), ["governance_triage"]);
  assert.equal(hitFor("governance_triage", b), "HIT");
  assert.equal(hitFor("compounding_capture", b), "MISS");
});

test("AI1-FIELD-02: alternate-only -> legacy compatibility path still serves; alternate query HITs", () => {
  const b = fieldRow(null, ["compounding_capture"]);
  assert.deepEqual(deriveCapabilities(b), ["compounding_capture"]);
  assert.equal(hitFor("compounding_capture", b), "HIT");
  assert.equal(hitFor("governance_triage", b), "MISS");
});

test("AI1-FIELD-03: both fields -> deterministic union; either query HITs", () => {
  const b = fieldRow(["governance_triage"], ["compounding_capture"]);
  assert.deepEqual(deriveCapabilities(b).sort(), ["compounding_capture", "governance_triage"]);
  assert.equal(hitFor("governance_triage", b), "HIT");
  assert.equal(hitFor("compounding_capture", b), "HIT");
});

test("AI1-FIELD-04: neither field -> no capability derived; both queries MISS", () => {
  const b = fieldRow(null, null);
  assert.deepEqual(deriveCapabilities(b), []);
  assert.equal(hitFor("governance_triage", b), "MISS");
  assert.equal(hitFor("compounding_capture", b), "MISS");
});

test("AI1-FIELD-05: disagreement (canonical vs alternate conflict) -> deterministic union, never nondeterministic", () => {
  const b = fieldRow(["governance_triage"], ["compounding_capture"]);
  const first = deriveCapabilities(b).sort();
  // Repeated derivation is identical: no nondeterminism across calls.
  for (let i = 0; i < 3; i++) assert.deepEqual(deriveCapabilities(b).sort(), first);
  assert.deepEqual(first, ["compounding_capture", "governance_triage"]);
  assert.equal(hitFor("governance_triage", b), "HIT");
  assert.equal(hitFor("compounding_capture", b), "HIT");
});
