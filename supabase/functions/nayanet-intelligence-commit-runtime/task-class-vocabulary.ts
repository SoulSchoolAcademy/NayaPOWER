// Canonical task-class vocabulary for the declared_task_classes writer <->
// learning-verify reader contract (H8-7 writer closure).
//
// CANONICAL OWNER (writer side): this file. It is the single authoritative
// definition of the bounded task-class vocabulary a governed capture may
// declare. Three consumers must agree with it:
//
//   1. The commit writer: the Edge Function
//      (`supabase/functions/nayanet-intelligence-commit-runtime/index.ts`)
//      validates captures with `validateTaskClasses`, and the SQL writer
//      migration embeds the same bounded set (see the migration header
//      comment). The SQL copy is a mirror, not a second definition: extend
//      THIS file and regenerate the migration; never extend the vocabulary
//      in SQL alone.
//   2. The graph reader (`supabase/functions/nayanet-learning-verify/index.ts`
//      `TASK_CLASS_REGISTRY`, H8-7 repair) consumes
//      `block.provenance.declared_task_classes` as opaque strings and marks a
//      relationship APPLICABLE only when at least one declared class is a
//      registry member. The reader is intentionally NOT modified by this
//      repair: writer/reader agreement is exactly that the writer persists
//      only vocabulary-conformant strings, and the reader independently
//      filters to its registry (defense in depth).
//
// OWNERSHIP (tiny, explicit):
//   - definition:   this file; changed only by a governed repo PR.
//   - addition:     Human-Director-approved PR that extends the bounded set AND
//                   regenerates the SQL mirror AND updates the mirror-agreement
//                   test. No autonomous addition; capture authors MUST NOT mint
//                   production task classes (the writer rejects unknown names).
//   - deprecation:  removal from the bounded set by PR. Already-persisted
//                   blocks carrying a removed string stay reader-visible (the
//                   reader filters opaquely); new writes with it are rejected.
//   - validation:   writer-side, two layers: edge function (fail fast, 400)
//                   and SQL writer (fail closed, commit rejected).
//   - compatibility: asserted by test — the SQL mirror must contain exactly
//                   this file's values (see tests/task-class-declaration.test.mjs).
//
// A declared task class asserts the AUTHOR'S governed intent: "this lesson is
// offered as applicable to tasks of this class." It does NOT assert the lesson
// is correct for any specific task, does NOT create authority, and does NOT
// bypass the reader's fail-closed gates (registry membership, VERIFIED +
// ACTIVE relationship, temporal validity, consent, task-class match at
// selection time). Lesson text alone can never yield APPLICABLE — the H8-7
// law holds.
//
// Written in erasable TypeScript so it runs unchanged under Deno (edge
// function) and under Node type-stripping (repo tests).

export interface TaskClassDefinition {
  /** The exact persisted string. Matched by the reader with === equality. */
  value: string;
  /** One-line semantic definition. The single authoritative meaning. */
  definition: string;
}

export const TASK_CLASS_VOCABULARY: readonly TaskClassDefinition[] = [
  {
    value: "provenance_sensitive",
    definition:
      "Intelligence that is materially relevant only where provenance preservation matters. Declaring this class asserts the lesson carries provenance obligations, not that it applies to every provenance-adjacent task.",
  },
  {
    value: "repository_correction",
    definition:
      "Intelligence about correcting the repository within guardrails (act-first, ask-when-uncertain). Declaring this class does not create authority; LAW must independently authorize consequential action.",
  },
  {
    value: "active_intelligence_sensitive",
    definition:
      "Intelligence that distinguishes persisted memory from active, verified intelligence. Declaring this class asserts relevance to the stored-vs-proven distinction, never verification or authority by itself.",
  },
  {
    value: "learning_reuse",
    definition:
      "Intelligence about reusing verified learning across sessions and successors. Declaring this class reuses verified learning only; it is never a standalone authority claim.",
  },
  {
    value: "contextual_retrieval",
    definition:
      "Intelligence offered as retrieval context for related tasks. Declaring this class provides context only; it does not alter verification or authority state.",
  },
] as const;

/** The bounded set, in canonical order. Nothing outside this set is valid. */
export const TASK_CLASS_VALUES: readonly string[] = TASK_CLASS_VOCABULARY.map(
  (c) => c.value,
);

const TASK_CLASS_SET: ReadonlySet<string> = new Set(TASK_CLASS_VALUES);

/**
 * Normalization rule (single, deterministic):
 *   trim leading/trailing whitespace, then lowercase.
 * Format rule: ^[a-z][a-z0-9_]*$ — the exact shape the reader will compare.
 */
const TASK_CLASS_FORMAT = /^[a-z][a-z0-9_]*$/;

export class TaskClassValidationError extends Error {
  code: string;
  detail: string;
  constructor(code: string, detail: string) {
    super(code + ":" + detail);
    this.name = "TaskClassValidationError";
    this.code = code;
    this.detail = detail;
  }
}

/**
 * Normalize and validate one raw entry. Returns the canonical value.
 * Throws TaskClassValidationError("TASK_CLASS_MALFORMED", …) for non-strings,
 * empty/whitespace-only strings, and format violations.
 * Throws TaskClassValidationError("TASK_CLASS_UNKNOWN", …) for well-formed
 * strings outside the bounded vocabulary — fail closed, never silently admit
 * an ungoverned class into the applicability contract.
 */
export function normalizeTaskClass(raw: unknown): string {
  if (typeof raw !== "string") {
    throw new TaskClassValidationError(
      "TASK_CLASS_MALFORMED",
      "not-a-string:" + String(raw).slice(0, 64),
    );
  }
  const normalized = raw.trim().toLowerCase();
  if (normalized === "" || !TASK_CLASS_FORMAT.test(normalized)) {
    throw new TaskClassValidationError(
      "TASK_CLASS_MALFORMED",
      "bad-format:" + raw.slice(0, 64),
    );
  }
  if (!TASK_CLASS_SET.has(normalized)) {
    throw new TaskClassValidationError("TASK_CLASS_UNKNOWN", normalized);
  }
  return normalized;
}

/**
 * Validate the `declared_task_classes` field of an incoming capture.
 *
 * Deterministic handling contract:
 *   - absent (undefined/null)        → null: persist exactly as today
 *     (no `declared_task_classes` key is written; the block is byte-identical
 *     to a pre-repair commit).
 *   - empty array                    → null: safely ignored as absent.
 *   - non-array                      → TASK_CLASS_MALFORMED (reject commit).
 *   - any malformed/unknown entry    → reject the whole commit (fail closed).
 *     A typo must never silently produce a block the graph reader cannot
 *     classify, and an unknown name must never silently enter the governed
 *     applicability contract.
 *   - duplicates                     → deduped, first occurrence wins, then
 *     sorted lexicographically, so the persisted representation is fully
 *     deterministic: same capture + same code → same persisted array.
 *
 * Returns null (absent) or the sorted, deduped, vocabulary-conformant array.
 */
export function validateTaskClasses(input: unknown): string[] | null {
  if (input === undefined || input === null) return null;
  if (!Array.isArray(input)) {
    throw new TaskClassValidationError("TASK_CLASS_MALFORMED", "not-an-array");
  }
  if (input.length === 0) return null;
  const out: string[] = [];
  for (const raw of input) {
    const normalized = normalizeTaskClass(raw);
    if (!out.includes(normalized)) out.push(normalized);
  }
  out.sort();
  return out;
}

export interface ProvenanceBase {
  stage: string;
  source: string;
  authority_grant_id: string;
  source_event_id: string;
}

/**
 * Build the exact persisted `provenance` shape the SQL writer produces:
 * today's `{stage, source, authority_grant_id, source_event_id}` plus
 * `declared_task_classes` (raw array = the reader contract) and
 * `task_class_declaration` (attestation record) ONLY when a validated
 * non-empty array was supplied. When `taskClasses` is null the returned
 * object is byte-identical to the pre-repair shape.
 */
export function buildDeclaredProvenance(
  base: ProvenanceBase,
  taskClasses: string[] | null,
): Record<string, unknown> {
  const provenance: Record<string, unknown> = {
    stage: base.stage,
    source: base.source,
    authority_grant_id: base.authority_grant_id,
    source_event_id: base.source_event_id,
  };
  if (taskClasses !== null) {
    provenance.declared_task_classes = [...taskClasses];
    provenance.task_class_declaration = {
      source: "intelligence_commit_capture",
      values: [...taskClasses],
    };
  }
  return provenance;
}
