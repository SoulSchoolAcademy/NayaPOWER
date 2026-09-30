// Canonical capability vocabulary for the intelligence-commit writer <-> KNOW
// selector contract (repair branch `repair/ai1-capability-carry`).
//
// CANONICAL OWNER: this file. It is the single authoritative definition of the
// bounded capability vocabulary. Two consumers must agree with it:
//
//   1. The commit writer: the Edge Function
//      (`supabase/functions/nayanet-intelligence-commit-runtime/index.ts`)
//      validates captures with `validateCapabilities`, and the SQL writer
//      migration embeds the same bounded set (see the migration header comment).
//      The SQL copy is a mirror, not a second definition: extend THIS file and
//      regenerate the migration; never extend the vocabulary in SQL alone.
//   2. The KNOW selector (`supabase/functions/nayanet-know-runtime/know.ts`)
//      consumes `content.capabilities` as opaque strings via
//      `structuredCapabilities` and is intentionally NOT modified by this
//      repair. Because the selector matches `required_capability` with exact
//      string equality, writer/selector agreement is exactly: the writer
//      persists only vocabulary-conformant strings.
//
// OWNERSHIP (tiny, explicit):
//   - definition:   this file; changed only by a governed repo PR.
//   - addition:     Human-Director-approved PR that extends the bounded set AND
//                   regenerates the SQL mirror AND updates the mirror-agreement
//                   test. No autonomous addition; capture authors MUST NOT mint
//                   production capabilities (the writer rejects unknown names).
//   - deprecation:  removal from the bounded set by PR. Already-persisted
//                   blocks carrying a removed string stay selector-visible (the
//                   selector matches opaquely); new writes with it are rejected.
//   - validation:   writer-side, two layers: edge function (fail fast, 400)
//                   and SQL writer (fail closed, commit rejected).
//   - compatibility: asserted by test — the SQL mirror must contain exactly
//                   this file's values (see tests/ai1-capability-carry.test.mjs).
//
// A capability tag declares PURPOSE ("this block may be useful for X"). It does
// NOT assert correctness for any specific decision, does NOT create authority,
// and does NOT make the intelligence semantically applicable to every task of
// that class. Applicability remains the consumer's judgment.
//
// Written in erasable TypeScript so it runs unchanged under Deno (edge
// function) and under Node type-stripping (repo tests).

export interface CapabilityDefinition {
  /** The exact persisted string. Matched by the selector with === equality. */
  value: string;
  /** One-line semantic definition. The single authoritative meaning. */
  definition: string;
}

export const CAPABILITY_VOCABULARY: readonly CapabilityDefinition[] = [
  {
    value: "governance_triage",
    definition:
      "Intelligence that may inform governed triage decisions (act / read / ask / escalate / decline) under the 6→10 doctrine. Declaring this capability asserts relevance to governance triage, not correctness for any specific decision.",
  },
  {
    value: "compounding_capture",
    definition:
      "Intelligence about capturing, preserving, and compounding learned intelligence across sessions and successors. Declaring this capability asserts relevance to compounding discipline, not universal applicability.",
  },
] as const;

/** The bounded set, in canonical order. Nothing outside this set is valid. */
export const CAPABILITY_VALUES: readonly string[] = CAPABILITY_VOCABULARY.map(
  (c) => c.value,
);

const CAPABILITY_SET: ReadonlySet<string> = new Set(CAPABILITY_VALUES);

/**
 * Normalization rule (single, deterministic):
 *   trim leading/trailing whitespace, then lowercase.
 * Format rule: ^[a-z][a-z0-9_]*$ — the exact shape the selector will compare.
 */
const CAPABILITY_FORMAT = /^[a-z][a-z0-9_]*$/;

export class CapabilityValidationError extends Error {
  code: string;
  detail: string;
  constructor(code: string, detail: string) {
    super(code + ":" + detail);
    this.name = "CapabilityValidationError";
    this.code = code;
    this.detail = detail;
  }
}

/**
 * Normalize and validate one raw entry. Returns the canonical value.
 * Throws CapabilityValidationError("CAPABILITY_MALFORMED", …) for non-strings,
 * empty/whitespace-only strings, and format violations.
 * Throws CapabilityValidationError("CAPABILITY_UNKNOWN", …) for well-formed
 * strings outside the bounded vocabulary — fail closed, never silently broaden
 * retrieval.
 */
export function normalizeCapability(raw: unknown): string {
  if (typeof raw !== "string") {
    throw new CapabilityValidationError(
      "CAPABILITY_MALFORMED",
      "not-a-string:" + String(raw).slice(0, 64),
    );
  }
  const normalized = raw.trim().toLowerCase();
  if (normalized === "" || !CAPABILITY_FORMAT.test(normalized)) {
    throw new CapabilityValidationError(
      "CAPABILITY_MALFORMED",
      "bad-format:" + raw.slice(0, 64),
    );
  }
  if (!CAPABILITY_SET.has(normalized)) {
    throw new CapabilityValidationError("CAPABILITY_UNKNOWN", normalized);
  }
  return normalized;
}

/**
 * Validate the `capabilities` field of an incoming capture.
 *
 * Deterministic handling contract:
 *   - absent (undefined/null)        → null: persist exactly as today
 *     (no `capabilities` key is written; the block is byte-identical to a
 *     pre-repair commit).
 *   - empty array                    → null: safely ignored as absent.
 *   - non-array                      → CAPABILITY_MALFORMED (reject commit).
 *   - any malformed/unknown entry    → reject the whole commit (fail closed).
 *     A typo must never silently produce an un-retrievable block, and an
 *     unknown name must never silently broaden what the selector can match.
 *   - duplicates                     → deduped, first occurrence wins, then
 *     sorted lexicographically, so the persisted representation is fully
 *     deterministic: same capture + same code → same persisted array.
 *
 * Returns null (absent) or the sorted, deduped, vocabulary-conformant array.
 */
export function validateCapabilities(input: unknown): string[] | null {
  if (input === undefined || input === null) return null;
  if (!Array.isArray(input)) {
    throw new CapabilityValidationError("CAPABILITY_MALFORMED", "not-an-array");
  }
  if (input.length === 0) return null;
  const out: string[] = [];
  for (const raw of input) {
    const normalized = normalizeCapability(raw);
    if (!out.includes(normalized)) out.push(normalized);
  }
  out.sort();
  return out;
}

export interface PersistedContentBase {
  lesson: string;
  topic: string;
  category: string;
}

/**
 * Build the exact persisted `content` shape the SQL writer produces:
 * today's `{lesson, topic, category}` plus `capabilities` ONLY when a
 * validated non-empty array was supplied. When `capabilities` is null the
 * returned object is byte-identical to the pre-repair shape.
 */
export function buildPersistedContent(
  base: PersistedContentBase,
  capabilities: string[] | null,
): Record<string, unknown> {
  const content: Record<string, unknown> = {
    lesson: base.lesson,
    topic: base.topic,
    category: base.category,
  };
  if (capabilities !== null) {
    content.capabilities = [...capabilities];
  }
  return content;
}
