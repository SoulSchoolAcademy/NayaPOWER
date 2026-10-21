# The Search Index Is a Lagging Projection — Index Hits Are Stale-Index Evidence, Not Current-File Content

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0188-search-index-stale-evidence
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-02
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** `#554` consensus-verification correction (comment 5953501324, 2026-10-02 13:32:24Z): after the `undefined`-placeholder cleanup of the 11 living room contracts, the GitHub code-search index still returned stale matches for the pre-cleanup snapshot era, while direct fetches of the live main file bytes for all 11 room contracts (`HUB/ROOMS/01-FEED.md` … `11-SETTINGS.md` at main tip `5eaec742fa908163e288ac42615b9731a80fc5bf`) showed the literal `undefined` artifact gone from every room. Classified there verbatim: "The search-index mismatch is classified as stale index evidence, not current-file content."

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A code-search index is not the tree. It is a lagging projection of the tree, indexed at some past point, and it can keep showing content the tree no longer holds. The durable rule: **a claim about what a file contains NOW must be verified against live file bytes** (contents API / raw fetch at the ref), never against search results. Search is for discovery — "where might this be?" — not for proof — "what is in the file at this ref?". When a search hit and the live bytes disagree, that is not a contradiction to resolve between two equal sources: the index is stale-index evidence with its own known staleness semantics, and the live bytes win. Name the evidence source and its staleness when you report: "search index still returns pre-cleanup matches for `80dfc7d2` snapshots; direct fetches of all 11 files at `5eaec742` show zero `undefined` hits." That one sentence does three jobs: it states what was checked, at which ref, and why the conflicting signal is expected rather than alarming. Cold successors will keep tripping on this because search feels like reading — it isn't. It is reading a snapshot.

## 🩷 HUMAN NOTE

Shawn — one mechanical evidence rule from this tick's room-contract verification: when a code-search hit disagrees with the actual file, trust the file. GitHub's search index lags the tree and kept showing the pre-cleanup snapshot even after the `undefined` placeholders were gone from all 11 room contracts. The verification lane classified it as stale-index evidence and re-verified against live bytes. Rule of thumb: search finds things; only reading the bytes proves them.

## 🟣 CHILD NOTE

Imagine asking the library computer where a book is — it says "shelf 5" — but the book was moved to shelf 2 yesterday. The computer isn't wrong on purpose; it just hasn't been told yet. The new rule: if the computer says one thing but your eyes on the shelf say another, your eyes win. Always check the actual shelf.

## 👵 GRANDMA NOTE

You know how the phone book is printed once a year, but people's numbers change? Searching online is the same — it's a copy that can be out of date. The rule we wrote down: when the copy and the real thing disagree, believe the real thing. And say which one you checked.

## 🤖 NAYA NOTE

Treat every evidence source as having its own staleness semantics. Code search, cached PR diffs, board-side snapshots, and search indexes are all lagging projections — fine for discovery, never proof of current content. Any claim of the form "file X contains Y at ref R" must be verified against live bytes at R (contents/raw API, fetched at claim time). When a lagging source disagrees with live bytes, record the disagreement as "stale-index evidence, not current-file content" — expected and classified, not a contradiction. This is the search-index member of the SN-057 temporal-attribution family, alongside SN-100 (verdicts die at every new SHA) and SN-061 (verify at the pin).

## ⚙️ MACHINE NOTE

{"sn": "SN-0188", "title": "The Search Index Is a Lagging Projection — Index Hits Are Stale-Index Evidence, Not Current-File Content", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-02", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "ENGINEERING-PROOF", "INDEPENDENT-VERIFICATION"], "extends": ["SN-057", "SN-061", "SN-100"], "evidence": {"board": "5953501324", "verbatim_classification": "The search-index mismatch is classified as stale index evidence, not current-file content", "stale_matches": "pre-cleanup 80dfc7d2 snapshots via GitHub code-search", "live_verification": "direct fetches of all 11 HUB/ROOMS/*.md file bytes at main tip 5eaec742fa908163e288ac42615b9731a80fc5bf — literal undefined gone from every room", "related_repair": "5953436017"}, "rule": "a content claim must be verified against live file bytes at the ref; search-index hits are lagging-projection discovery, never proof; name the source and its staleness on any disagreement"}
