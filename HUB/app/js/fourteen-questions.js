/*
 * fourteen-questions.js — the 14Q living board (Wave 2 item 3, Project Intelligence).
 *
 * The Fourteen Questions are NayaNET's minimum viable intelligence interface
 * (SN-0834): every seat must be able to answer them FROM LIVE STATE.
 * This module is the board's contract + renderer:
 *
 *   validateQuestionsPayload(payload)  — fail-closed validation of a
 *     questions.json payload as emitted by the Project Intelligence
 *     derivation. An "answered" question MUST carry at least one proof
 *     link; a question that cannot be answered MUST be honestly filed
 *     (status "unknown" + a reason). Anything else is rejected.
 *   assessFreshness(payload, opts)     — SN-0834's machine rule:
 *     STALE = INVALID. An answer sourced from an old derivation or a
 *     different state_tip is flagged stale, never shown as current truth.
 *     Freshness is NOT opt-in: when the caller supplies no maxAgeSeconds,
 *     DEFAULT_MAX_AGE_SECONDS applies, and a derived_at more than
 *     MAX_CLOCK_SKEW_SECONDS in the future is stale too (a timestamp
 *     from the future is not current truth either).
 *   renderFourteenQuestions(payload, opts) — pure string rendering
 *     (no DOM), every payload string HTML-escaped, so the face can drop
 *     the output into its page and Node tests can verify it headlessly.
 *
 * Payload contract (questions.json):
 *   {
 *     "schema_version": "1",
 *     "derived_at": "<ISO-8601>",
 *     "state_tip": "<derivation revision>",
 *     "questions": [
 *       { "id": "who", "question": "WHO are we?",
 *         "status": "answered", "answer": "<text>",
 *         "proof": ["https://..."] },
 *       { "id": "unknown", "question": "WHAT is unknown?",
 *         "status": "unknown", "answer": "",
 *         "proof": [], "reason": "<why this cannot be answered yet>" }
 *     ]
 *   }
 * Exactly the 14 canonical ids, in canonical order — the order IS the
 * interface (briefing § THE 14 QUESTIONS). The canonical question TEXT
 * is bound too: an id carrying foreign text is refused, because the
 * text is part of each question's identity — the face must never render
 * a foreign question under the board's valid seal.
 */
"use strict";

const CANONICAL_QUESTIONS = [
  ["who", "WHO are we?"],
  ["what", "WHAT are we building?"],
  ["why", "WHY are we building it?"],
  ["success", "WHAT does success mean?"],
  ["truth_now", "WHAT is true right now?"],
  ["proven", "WHAT has already been proven?"],
  ["unknown", "WHAT is unknown?"],
  ["authority", "WHAT authority exists?"],
  ["history", "WHAT happened previously?"],
  ["lessons", "WHAT did we learn?"],
  ["next", "WHAT should happen next?"],
  ["proof_method", "HOW do I prove it?"],
  ["record_location", "WHERE do I record it?"],
  ["continuation", "HOW does the next Naya continue?"],
];

const CANONICAL_IDS = CANONICAL_QUESTIONS.map(([id]) => id);

// Freshness defaults (VERIFY fix round on PR #3016, card 6375665310):
// a caller that supplies no limit still gets one, and small clock skew
// is tolerated but a materially future timestamp is stale.
const DEFAULT_MAX_AGE_SECONDS = 900;
const MAX_CLOCK_SKEW_SECONDS = 60;

function fail(code, message) {
  const err = new Error(message);
  err.code = code;
  throw err;
}

function isHttpUrl(value) {
  if (typeof value !== "string") return false;
  try {
    const u = new URL(value);
    return u.protocol === "https:" || u.protocol === "http:";
  } catch {
    return false;
  }
}

function validateQuestionsPayload(payload) {
  if (!payload || typeof payload !== "object" || Array.isArray(payload)) {
    fail("PAYLOAD_NOT_OBJECT", "questions payload must be an object");
  }
  if (payload.schema_version !== "1") {
    fail("SCHEMA_VERSION", 'schema_version must be "1"');
  }
  if (typeof payload.derived_at !== "string" || Number.isNaN(Date.parse(payload.derived_at))) {
    fail("DERIVED_AT", "derived_at must be an ISO-8601 timestamp string");
  }
  if (typeof payload.state_tip !== "string" || payload.state_tip.length === 0) {
    fail("STATE_TIP", "state_tip must be a non-empty string");
  }
  const qs = payload.questions;
  if (!Array.isArray(qs)) {
    fail("QUESTIONS_NOT_ARRAY", "questions must be an array");
  }
  if (qs.length !== CANONICAL_IDS.length) {
    fail(
      "QUESTION_COUNT",
      `expected exactly ${CANONICAL_IDS.length} questions, got ${qs.length}`
    );
  }
  qs.forEach((q, i) => {
    const expectedId = CANONICAL_IDS[i];
    if (!q || typeof q !== "object") {
      fail("QUESTION_NOT_OBJECT", `questions[${i}] must be an object`);
    }
    if (q.id !== expectedId) {
      fail(
        "QUESTION_ORDER",
        `questions[${i}].id must be "${expectedId}" (canonical order), got "${q.id}"`
      );
    }
    if (typeof q.question !== "string" || q.question.trim().length === 0) {
      fail("QUESTION_TEXT", `questions[${i}].question must be non-empty text`);
    }
    if (q.question !== CANONICAL_QUESTIONS[i][1]) {
      fail(
        "QUESTION_TEXT_MISMATCH",
        `questions[${i}].question must be the canonical "${CANONICAL_QUESTIONS[i][1]}" for id "${expectedId}", got "${q.question}"`
      );
    }
    if (!Array.isArray(q.proof)) {
      fail("PROOF_NOT_ARRAY", `questions[${i}].proof must be an array`);
    }
    q.proof.forEach((link, j) => {
      if (!isHttpUrl(link)) {
        fail("PROOF_NOT_URL", `questions[${i}].proof[${j}] is not an http(s) URL`);
      }
    });
    if (q.status === "answered") {
      if (typeof q.answer !== "string" || q.answer.trim().length === 0) {
        fail("ANSWER_EMPTY", `questions[${i}] is "answered" but its answer is empty`);
      }
      if (q.proof.length === 0) {
        fail(
          "ANSWER_WITHOUT_PROOF",
          `questions[${i}] is "answered" but carries no proof link — a claim, not a proof`
        );
      }
    } else if (q.status === "unknown") {
      if (typeof q.reason !== "string" || q.reason.trim().length === 0) {
        fail(
          "UNKNOWN_WITHOUT_REASON",
          `questions[${i}] is "unknown" but carries no reason — it must be honestly filed`
        );
      }
    } else {
      fail(
        "STATUS_INVALID",
        `questions[${i}].status must be "answered" or "unknown", got "${q.status}"`
      );
    }
  });
  return payload;
}

function assessFreshness(payload, opts = {}) {
  const now = opts.now ? new Date(opts.now) : new Date();
  const derivedAt = new Date(payload.derived_at);
  const ageSeconds = (now.getTime() - derivedAt.getTime()) / 1000;
  const maxAgeSeconds =
    opts.maxAgeSeconds != null ? opts.maxAgeSeconds : DEFAULT_MAX_AGE_SECONDS;
  const reasons = [];
  if (ageSeconds < -MAX_CLOCK_SKEW_SECONDS) {
    reasons.push(
      `derived_at is ${Math.round(-ageSeconds)}s in the future (skew limit ${MAX_CLOCK_SKEW_SECONDS}s)`
    );
  }
  if (ageSeconds > maxAgeSeconds) {
    reasons.push(
      `derived_at is ${Math.round(ageSeconds)}s old (limit ${maxAgeSeconds}s)`
    );
  }
  if (opts.expectedStateTip != null && payload.state_tip !== opts.expectedStateTip) {
    reasons.push(
      `state_tip "${payload.state_tip}" does not match current "${opts.expectedStateTip}"`
    );
  }
  return { stale: reasons.length > 0, ageSeconds, reasons };
}

function escapeHtml(value) {
  return String(value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

function renderQuestion(q, index) {
  const num = index + 1;
  const heading = `<h3><span class="fq-num">${num}</span> ${escapeHtml(q.question)}</h3>`;
  if (q.status === "unknown") {
    return (
      `<article class="fq-card fq-unknown" data-question-id="${escapeHtml(q.id)}">` +
      heading +
      `<p class="fq-status">Not yet known</p>` +
      `<p class="fq-reason">${escapeHtml(q.reason)}</p>` +
      `</article>`
    );
  }
  const proofs = q.proof
    .map(
      (link, j) =>
        `<li><a href="${escapeHtml(link)}" rel="noopener">proof ${j + 1}</a></li>`
    )
    .join("");
  return (
    `<article class="fq-card fq-answered" data-question-id="${escapeHtml(q.id)}">` +
    heading +
    `<p class="fq-answer">${escapeHtml(q.answer)}</p>` +
    `<ul class="fq-proof">${proofs}</ul>` +
    `</article>`
  );
}

function renderFourteenQuestions(payload, opts = {}) {
  validateQuestionsPayload(payload);
  const freshness = assessFreshness(payload, opts);
  const cards = payload.questions.map(renderQuestion).join("\n");
  const banner = freshness.stale
    ? `<p class="fq-stale" role="alert">STALE — these answers are not current truth: ${escapeHtml(
        freshness.reasons.join("; ")
      )}</p>`
    : "";
  return (
    `<section class="fq-board" data-state-tip="${escapeHtml(payload.state_tip)}">` +
    banner +
    cards +
    `</section>`
  );
}

const api = {
  CANONICAL_QUESTIONS,
  CANONICAL_IDS,
  DEFAULT_MAX_AGE_SECONDS,
  MAX_CLOCK_SKEW_SECONDS,
  validateQuestionsPayload,
  assessFreshness,
  renderFourteenQuestions,
  escapeHtml,
};

if (typeof module !== "undefined" && module.exports) {
  module.exports = api;
}
if (typeof window !== "undefined") {
  window.FourteenQuestions = api;
}
