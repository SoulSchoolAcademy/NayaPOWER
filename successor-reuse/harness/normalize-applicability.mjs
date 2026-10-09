// Protocol v1.1 §13 reference implementation.
// Canonical normalization for applicability answers before comparison.
// Verifiers MUST apply this (or an equivalent) before exact-match;
// preregistration MUST name the normalization the sealed verifier uses.
export function normalizeApplicability(s) {
  if (typeof s !== 'string') return s;
  let out = s.replace(/\s+/g, ' ').trim();
  out = out.replace(/[.,;:]+$/u, '').trim();
  return out;
}
