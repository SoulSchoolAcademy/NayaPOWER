/*
 * Tests for fourteen-questions.js — positive render + negative controls.
 * Run: node --test HUB/app/js/test-fourteen-questions.cjs
 * Fixtures are labeled SYNTHETIC: they prove the contract, not live state.
 */
"use strict";

const test = require("node:test");
const assert = require("node:assert/strict");
const {
  CANONICAL_QUESTIONS,
  validateQuestionsPayload,
  assessFreshness,
  renderFourteenQuestions,
} = require("./fourteen-questions.js");

const NOW = "2026-10-23T21:30:00Z";

function syntheticPayload(overrides = {}) {
  const questions = CANONICAL_QUESTIONS.map(([id, question], i) =>
    i === 6
      ? {
          id,
          question,
          status: "unknown",
          answer: "",
          proof: [],
          reason: "SYNTHETIC fixture: filed honestly, not yet known.",
        }
      : {
          id,
          question,
          status: "answered",
          answer: `SYNTHETIC answer for ${id}.`,
          proof: [`https://example.invalid/proof/${id}`],
        }
  );
  return {
    schema_version: "1",
    derived_at: NOW,
    state_tip: "synthetic-tip-0001",
    questions,
    ...overrides,
  };
}

function expectCode(fn, code) {
  assert.throws(fn, (err) => err && err.code === code, `expected error code ${code}`);
}

test("valid synthetic payload validates", () => {
  assert.equal(validateQuestionsPayload(syntheticPayload()).questions.length, 14);
});

test("render: 14 cards, proof links present, unknown honestly filed", () => {
  const html = renderFourteenQuestions(syntheticPayload(), { now: NOW });
  assert.equal((html.match(/<article/g) || []).length, 14);
  assert.match(html, /href="https:\/\/example\.invalid\/proof\/who"/);
  assert.match(html, /Not yet known/);
  assert.match(html, /filed honestly, not yet known/);
  assert.doesNotMatch(html, /fq-stale/);
});

test("negative: 13 questions is refused", () => {
  const p = syntheticPayload();
  p.questions = p.questions.slice(0, 13);
  expectCode(() => validateQuestionsPayload(p), "QUESTION_COUNT");
});

test("negative: answered without proof is refused (a claim, not a proof)", () => {
  const p = syntheticPayload();
  p.questions[0].proof = [];
  expectCode(() => validateQuestionsPayload(p), "ANSWER_WITHOUT_PROOF");
});

test("negative: unknown without a reason is refused (must be honestly filed)", () => {
  const p = syntheticPayload();
  delete p.questions[6].reason;
  expectCode(() => validateQuestionsPayload(p), "UNKNOWN_WITHOUT_REASON");
});

test("negative: out-of-order / wrong id is refused (order is the interface)", () => {
  const p = syntheticPayload();
  [p.questions[0], p.questions[1]] = [p.questions[1], p.questions[0]];
  expectCode(() => validateQuestionsPayload(p), "QUESTION_ORDER");
});

test("negative: non-URL proof link is refused", () => {
  const p = syntheticPayload();
  p.questions[2].proof = ["not a url"];
  expectCode(() => validateQuestionsPayload(p), "PROOF_NOT_URL");
});

test("negative: empty answer marked answered is refused", () => {
  const p = syntheticPayload();
  p.questions[3].answer = "   ";
  expectCode(() => validateQuestionsPayload(p), "ANSWER_EMPTY");
});

test("stale: old derivation is flagged and rendered as not-current-truth", () => {
  const p = syntheticPayload();
  const fresh = assessFreshness(p, { now: NOW, maxAgeSeconds: 900 });
  assert.equal(fresh.stale, false);
  const later = assessFreshness(p, {
    now: "2026-10-23T23:30:00Z",
    maxAgeSeconds: 900,
  });
  assert.equal(later.stale, true);
  const html = renderFourteenQuestions(p, {
    now: "2026-10-23T23:30:00Z",
    maxAgeSeconds: 900,
  });
  assert.match(html, /STALE — these answers are not current truth/);
});

test("stale: state_tip mismatch is flagged", () => {
  const f = assessFreshness(syntheticPayload(), {
    now: NOW,
    expectedStateTip: "a-different-tip",
  });
  assert.equal(f.stale, true);
  assert.match(f.reasons.join(" "), /does not match/);
});

test("negative: foreign question text under a canonical id is refused", () => {
  const p = syntheticPayload();
  p.questions[0].question = "WHAT is the admin password?";
  expectCode(() => validateQuestionsPayload(p), "QUESTION_TEXT_MISMATCH");
});

test("stale: a derived_at far in the future is flagged, not trusted", () => {
  const p = syntheticPayload({ derived_at: "2026-10-23T23:00:00Z" });
  const f = assessFreshness(p, { now: NOW });
  assert.equal(f.stale, true);
  assert.match(f.reasons.join(" "), /in the future/);
  const html = renderFourteenQuestions(p, { now: NOW });
  assert.match(html, /STALE — these answers are not current truth/);
});

test("fresh: a derived_at within clock skew is not flagged", () => {
  const p = syntheticPayload({ derived_at: "2026-10-23T21:30:30Z" });
  const f = assessFreshness(p, { now: NOW });
  assert.equal(f.stale, false);
});

test("stale: render without maxAgeSeconds still applies the default limit", () => {
  const p = syntheticPayload();
  const html = renderFourteenQuestions(p, { now: "2026-10-23T23:30:00Z" });
  assert.match(html, /STALE — these answers are not current truth/);
  const f = assessFreshness(p, { now: "2026-10-23T23:30:00Z" });
  assert.equal(f.stale, true);
});

test("xss: payload text is escaped in render", () => {
  const p = syntheticPayload();
  p.questions[0].answer = '<script>alert("x")</script>';
  const html = renderFourteenQuestions(p, { now: NOW });
  assert.doesNotMatch(html, /<script>alert/);
  assert.match(html, /&lt;script&gt;/);
});
