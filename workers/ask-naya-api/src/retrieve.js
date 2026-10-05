/**
 * RetrievalBackend interface (SPEC.md §2):
 *   loadIndex(env)          -> Promise<{ manifest, documents, backend }>
 *   search(index, query, k) -> [{ doc, score, matched }]
 *
 * v1 scoring is BM25-lite: dependency-free, deterministic, explainable.
 * The MOCK backend is the default in this scaffold. The R2 path is stubbed
 * with explicit TODOs — it activates only when BRAIN_INDEX_BUCKET is bound.
 */
import { MOCK_DOCS, MOCK_MANIFEST } from './mock-data.js';

function tokenize(s) {
  return (s.toLowerCase().match(/[a-z0-9']+/g) || []).filter((t) => t.length > 1);
}

function buildTermStats(documents) {
  // document frequency per term, for idf
  const df = new Map();
  const docTerms = documents.map((d) => {
    const terms = tokenize([d.title, d.text, ...(d.claims || [])].join(' '));
    const uniq = new Set(terms);
    for (const t of uniq) df.set(t, (df.get(t) || 0) + 1);
    return terms;
  });
  return { df, docTerms };
}

function bm25Lite(queryTerms, docTerms, df, nDocs) {
  const k1 = 1.2;
  const tf = new Map();
  for (const t of docTerms) tf.set(t, (tf.get(t) || 0) + 1);
  const avgLen = 60; // fixed normalizer keeps the mock deterministic
  let score = 0;
  for (const q of queryTerms) {
    const f = tf.get(q) || 0;
    if (!f) continue;
    const idf = Math.log(1 + (nDocs - (df.get(q) || 0) + 0.5) / ((df.get(q) || 0) + 0.5));
    const norm = f / (f + k1 * (0.25 + 0.75 * (docTerms.length / avgLen)));
    score += idf * norm;
  }
  return score;
}

export async function loadIndex(env) {
  // Production path (SPEC.md §2, option B): versioned snapshot in R2.
  // TODO(deploy): fetch `${snapshot}/brain-index.json` from BRAIN_INDEX_BUCKET,
  // verify manifest.brainSha, cache in-memory keyed by indexVersion.
  if (env && env.BRAIN_INDEX_BUCKET) {
    throw new Error('R2 index path not yet implemented in scaffold — bind BRAIN_INDEX_BUCKET and implement per SPEC.md §2');
  }
  const { df, docTerms } = buildTermStats(MOCK_DOCS);
  return {
    backend: 'MOCK',
    manifest: MOCK_MANIFEST,
    documents: MOCK_DOCS,
    _stats: { df, docTerms },
  };
}

export function search(index, query, k = 5) {
  const qTerms = tokenize(query);
  const nDocs = index.documents.length;
  const hits = index.documents
    .map((doc, i) => {
      const score = bm25Lite(qTerms, index._stats.docTerms[i], index._stats.df, nDocs);
      const matched = qTerms.filter((t) => index._stats.docTerms[i].includes(t));
      return { doc, score, matched };
    })
    .filter((h) => h.score > 0)
    .sort((a, b) => b.score - a.score)
    .slice(0, k);
  return hits;
}

/** Minimum score for an answer; below it → honest unknown (Trait 47). Tuned for the mock corpus. */
export const ANSWER_THRESHOLD = 0.15;
