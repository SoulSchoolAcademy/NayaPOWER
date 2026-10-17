/**
 * AskResponse schema (v1) — mirrors SPEC.md §3.
 * The page's renderBoard consumes: grammar, color, keyText, beats[], sources[],
 * speakText, emphasis[], correction. The Worker must never emit a shape the
 * page cannot render; validate before every response.
 */

export const GRAMMARS = ['definition', 'comparison', 'process', 'principles'];
export const COLORS = ['cyan', 'lime', 'gold', 'magenta', 'purple', 'white'];
export const ANSWER_MODES = ['extractive-v1'];

const BEAT_KINDS = ['point', 'chips', 'fields', 'steps'];

function isStr(x) { return typeof x === 'string' && x.length > 0; }

function validateBeat(b, i, errors) {
  if (!b || typeof b !== 'object') { errors.push(`beats[${i}]: not an object`); return; }
  if (!BEAT_KINDS.includes(b.kind)) { errors.push(`beats[${i}]: bad kind ${b.kind}`); return; }
  if (b.kind === 'point') {
    if (!isStr(b.html)) errors.push(`beats[${i}]: point missing html`);
    if (b.cite !== undefined && typeof b.cite !== 'string') errors.push(`beats[${i}]: bad cite`);
  }
  if (b.kind === 'chips') {
    if (!Array.isArray(b.chips) || b.chips.length === 0) errors.push(`beats[${i}]: chips empty`);
    else for (const [j, c] of b.chips.entries()) {
      if (!isStr(c.n) || !isStr(c.name)) errors.push(`beats[${i}].chips[${j}]: bad chip`);
    }
  }
  if (b.kind === 'fields') {
    if (!Array.isArray(b.fields) || b.fields.length === 0) errors.push(`beats[${i}]: fields empty`);
  }
  if (b.kind === 'steps') {
    if (!Array.isArray(b.steps) || b.steps.length === 0) errors.push(`beats[${i}]: steps empty`);
  }
}

export function validateAskResponse(r) {
  const errors = [];
  if (!r || typeof r !== 'object') return { ok: false, errors: ['response not an object'] };
  if (!isStr(r.id)) errors.push('missing id');
  if (!isStr(r.question)) errors.push('missing question');
  if (!ANSWER_MODES.includes(r.answerMode)) errors.push(`bad answerMode ${r.answerMode}`);
  if (!GRAMMARS.includes(r.grammar)) errors.push(`bad grammar ${r.grammar}`);
  if (!COLORS.includes(r.color)) errors.push(`bad color ${r.color}`);
  if (!isStr(r.keyText)) errors.push('missing keyText');
  if (!isStr(r.speakText)) errors.push('missing speakText');
  if (!Array.isArray(r.beats)) errors.push('beats not an array');
  else r.beats.forEach((b, i) => validateBeat(b, i, errors));
  if (!Array.isArray(r.sources)) errors.push('sources not an array');
  else for (const [i, s] of r.sources.entries()) {
    if (!isStr(s.title) || !isStr(s.path)) errors.push(`sources[${i}]: need title+path`);
  }
  if (r.correction !== null && r.correction !== undefined) {
    const c = r.correction;
    for (const k of ['retractText', 'newText', 'speakText']) {
      if (!isStr(c[k])) errors.push(`correction missing ${k}`);
    }
  }
  if (typeof r.confidence !== 'number' || r.confidence < 0 || r.confidence > 1) {
    errors.push('confidence must be 0..1');
  }
  if (!Array.isArray(r.uncertainty)) errors.push('uncertainty not an array');
  if (!isStr(r.brainSha)) errors.push('missing brainSha — provenance is mandatory');
  if (!isStr(r.indexVersion)) errors.push('missing indexVersion');
  if (typeof r.degraded !== 'boolean') errors.push('degraded must be boolean');
  if (!isStr(r.backend)) errors.push('missing backend label (MOCK or r2-snapshot)');
  return { ok: errors.length === 0, errors };
}
