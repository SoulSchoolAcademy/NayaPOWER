/**
 * Extractive composer (SPEC.md §3): chunks → AskResponse. No generation.
 * - keyText is verbatim from the index (no rewording in v1).
 * - beats use the page's existing shapes so renderBoard needs no changes.
 * - No hit above threshold → honest unknown (Trait 47), citing the brain SHA searched.
 */
import { validateAskResponse } from './schema.js';
import { ANSWER_THRESHOLD } from './retrieve.js';

function esc(s) {
  return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

function emphasisFor(speakText) {
  // v1: derive emphasis marks from punctuation, mirroring the demo bank's authored marks.
  const words = speakText.split(/\s+/).length || 1;
  const marks = [];
  const re = /[.!?—;]/g;
  let m;
  while ((m = re.exec(speakText)) && marks.length < 4) {
    marks.push(Math.min(0.95, m.index / speakText.length));
  }
  if (!marks.length) marks.push(0.5);
  return marks;
}

function unknownResponse(question, manifest, backend, degraded) {
  const speakText =
    `That's not in my knowledge yet. I searched the brain at ${manifest.brainSha} ` +
    `and found nothing above the bar. I won't perform certainty I don't have.`;
  return {
    id: 'unknown',
    question,
    answerMode: 'extractive-v1',
    grammar: 'definition',
    color: 'cyan',
    keyText: "That's not in my knowledge yet.",
    beats: [
      {
        kind: 'point',
        html: `<strong>No retrieval above the bar</strong> at brain <span class="mono">${esc(manifest.brainSha)}</span>. Ask me about what's actually in the bank.`,
        cite: 'TRAIT 47 · TRUTH',
        depth: 'standard',
      },
    ],
    sources: [{ title: 'Bank boundary — no match', path: 'BRAIN/', status: 'N/A' }],
    speakText,
    emphasis: emphasisFor(speakText),
    correction: null,
    confidence: 0,
    uncertainty: ['no indexed claim scored above the answer threshold'],
    brainSha: manifest.brainSha,
    indexVersion: manifest.indexVersion,
    degraded,
    backend,
  };
}

export function composeAskResponse({ question, hits, manifest, backend, sessionCtx }) {
  const degraded = backend !== 'MOCK' && manifest.degraded === true;
  if (!hits.length || hits[0].score < ANSWER_THRESHOLD) {
    return unknownResponse(question, manifest, backend, degraded);
  }
  const top = hits[0];
  const doc = top.doc;
  const speakText = doc.claims.join(' ');
  const beats = [];
  if (doc.chips) {
    beats.push({ kind: 'chips', chips: doc.chips });
  }
  // Key claim is beat 0's text on the page; supporting claims become points.
  doc.claims.slice(1).forEach((c, i) => {
    beats.push({
      kind: 'point',
      html: `<span class="pdot"></span><p>${esc(c)}</p>`,
      cite: doc.title.toUpperCase(),
      depth: i === 0 ? 'standard' : 'deep',
    });
  });

  let correction = null;
  if (doc.supersededBy) {
    const s = doc.supersededBy;
    correction = {
      retractText: s.retractText,
      retractCite: s.retractCite,
      newText: s.newText,
      newCite: s.newCite,
      speakText: s.speakText,
    };
  }

  const confidence = Math.max(0.05, Math.min(0.99, top.score / (top.score + 1)));
  const uncertainty = [];
  if (doc.status === 'CANDIDATE') uncertainty.push('source is CANDIDATE, not ratified');
  if (hits.length === 1) uncertainty.push('single source above the bar');
  if (sessionCtx && sessionCtx.lastId === doc.id) uncertainty.push('same answer as previous turn — asked again');

  const response = {
    id: doc.id,
    question,
    answerMode: 'extractive-v1',
    grammar: doc.grammar,
    color: doc.color,
    keyText: doc.claims[0],
    beats,
    sources: [{ title: doc.title, path: doc.path, status: doc.status }],
    speakText,
    emphasis: emphasisFor(speakText),
    correction,
    confidence: Math.round(confidence * 100) / 100,
    uncertainty,
    brainSha: manifest.brainSha,
    indexVersion: manifest.indexVersion,
    degraded,
    backend,
  };
  const v = validateAskResponse(response);
  if (!v.ok) throw new Error('composer produced invalid AskResponse: ' + v.errors.join('; '));
  return response;
}
