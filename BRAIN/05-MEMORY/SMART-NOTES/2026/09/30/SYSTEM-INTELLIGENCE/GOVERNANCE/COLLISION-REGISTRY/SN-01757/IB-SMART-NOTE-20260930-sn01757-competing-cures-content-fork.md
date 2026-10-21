# Same Outcome, Different Bytes — Competing Cures on the Same Registry IDs Are a Content Fork, Not Two Fixes

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01757-competing-cures-content-fork
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-21
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

PR #2839 and PR #2831 both restored the same five registry entry IDs (SN-0800/0805/0806/0807/0808) with identical page_hashes but all-5 DIFFERENT content_hashes — re-distilled captures vs canonical-reconstruction. Same outcome intent, different restored content: a last-write-wins content fork. Both cures cannot land — the second would silently overwrite the first's entries. VERIFY proved the divergence on live bytes (board 6312255918: 5/5 content_hash re-derived MATCH, red control cited, non-vacuity via #2831 sabotage; verdict CURE REAL 9.5, content-divergent). The main-seat adjudication (6312255661) HELD #2839 until Naya 4 corrects/withdraws provenance or closes as superseded by #2831 (CURE VERIFIED 9.5, gate-format verdict on the PR). The rule: same entry IDs + divergent content_hash across open cure PRs = content fork; hold both, route to adjudication, land exactly one after the canonical content is named. This is the registry-content dimension of the collision family — SN-0176 covers the ID-number dimension; this note covers the entry-content dimension. Pair with SN-1756 (the same incident's deletion-claim lesson).

## 🩷 HUMAN NOTE

Shawn — tonight two cure PRs tried to fix the same five registry entries, and both were "green" on their own. The problem: they restored different content for the same IDs — landing both means the second silently overwrites the first. VERIFY caught it by comparing hashes, and the adjudication held one PR (#2839) until the canonical version (#2831) is confirmed. The standing rule: when two fixes compete on the same entries, we stop and name the one true content before anything lands. No silent overwrites, ever.

## 🟣 CHILD NOTE

Two kids each re-copy five pages of the class notebook that got smudged. Both notebooks look "fixed" — but the kids wrote different words on the same five pages. If you put both notebooks on the shelf, you still have one shelf: one copy has to win, and it has to be the right one. The rule: when two fixes cover the same pages, you stop, compare them word by word, and the teacher picks the real pages. You never file both.

## 🔵 GRANDMA NOTE

Like two neighbors both re-knitting the same five squares of your quilt, each in a different pattern. Both squares are "fixed" — but a quilt can't wear two different squares in the same spot. If you sew both in, one covers the other and the work underneath is gone, silently. So you hold both quilts, lay the squares side by side, and pick the true pattern before a single stitch lands. Same spots, different stitches: stop and choose.

## 🟠 NAYA NOTE

Dock/verifier discipline: before landing any registry-cure PR, compare content_hash of the same entry IDs across all open cure PRs. The detector is byte-exact: identical page_hashes (same entry identity) + differing content_hashes (different restored content) = content fork — last-write-wins would silently decide the registry's truth. On a fork: HOLD all competing cures, route to adjudication with the divergence table (entry IDs, page_hash match, content_hash per PR), and land exactly one only after adjudication names the canonical content. Tonight's shape to copy: VERIFY receipt 6312255918 named the divergence byte-proven (5/5 content_hash MATCH at exact head, red control + sabotage), and the adjudication 6312255661 named the canonical side (#2831, CURE VERIFIED 9.5) while holding #2839 pending provenance correction or close-as-superseded. Do not merge a cure PR that the divergence table flags — the Receipt gate fails the landing.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1757",
  "title": "Competing cures on the same registry IDs are a content fork — hold both, adjudicate the canonical content",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "applies_when": [
    ["merge", "competing-cure"],
    ["verify", "registry"],
    ["dock", "queue"],
    ["adjudication", "registry"]
  ],
  "enforcement": "Before landing any registry-cure PR, the dock runs the divergence table: same entry IDs across open cure PRs compared by content_hash; identical page_hashes + differing content_hashes = content fork -> HOLD all competitors, route to adjudication; adjudication names the canonical content before any one lands. A cure landing without the divergence table fails the Receipt gate.",
  "evidence": {
    "divergence": "#2793 comment 6312255918 (2026-10-21): #2839 VERIFY receipt — same 5 SN IDs as #2831, identical page_hashes, all-5 different content_hashes (re-distilled vs canonical-reconstruction); verdict CURE REAL 9.5, CONTENT-DIVERGENT; routed to adjudication",
    "adjudication": "#2793 comment 6312255661 (2026-10-21): #2839 HELD until Naya 4 corrects/withdraws provenance or closes as superseded by #2831 (CURE VERIFIED 9.5, gate-format verdict on the PR)",
    "base_cure": "#2793 comment 6310156804 (#2831 IV: head f1ed1803 = 31/31 PASS, sabotage non-vacuity, CURE VERIFIED 9.5)"
  },
  "decision_change": "When two cure PRs compete on the same registry entries, the dock no longer lands the first-green one — it holds both and routes the divergence table to adjudication. This changes merge sequencing: canonical-content-naming precedes landing.",
  "falsifier": "If two competing cures with same-ID/different-content_hash both land and the registry stays consistent with no overwrite (e.g. a future registry that versions entries instead of last-write-wins), the hold rule is over-broad and this note is wrong for that registry design.",
  "mechanism": "content_hash is computed on the exact restored bytes; page_hash identifies the entry. Same identity + different content = two candidate truths for one slot. Registries with last-write-wins semantics resolve the conflict by silence (the second landing wins, the first's content is lost without a record) — the hold forces the choice into the open where adjudication can name the canonical bytes.",
  "related": ["SN-1756 (never-registered is not deleted — same incident)", "SN-0176 (cross-partition content fork — ID-number dimension; this note is the entry-content dimension)"]
}
```
