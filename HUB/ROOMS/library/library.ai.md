# Intelligent Library — Builder Spec (AI)

**Status:** PROPOSED. **Route:** `hub/library`, domain view `hub/library/<domain>`. **Accent:** lime. **Build order:** 3.

## Shell contract

Sidebar + Naya rail unchanged; center swaps. Domain navigation stays inside the room (no shell reload).

## Component tree

1. `LibraryHero` — title, tagline, `HeroSearch` (large, instant, truth-sealed results).
2. `FeaturedIntelligence` — three huge cards: MOST RELEVANT / RECENTLY DEVELOPED / NEEDS ATTENTION.
3. `DomainShelf` — rich domain cards: name, record count, developing count, unresolved count, updated-relative-time.
4. `DomainRoom` (on select) — domain title + sections: What I know / What I've learned / What I'm uncertain about / Related intelligence / Recent discoveries / Smart Notes / Questions + "Ask Naya: what am I missing here?"
5. `ReadingView` — full Smart Note board: jewel, title, nutshell, perspective tabs, provenance footer.

## Data bindings

- Domains ← canonical knowledge store (58-domain foundation and growing).
- Featured ← relevance engine (real signals), recency, gap computation.
- Reading view ← single intelligence record with perspectives + provenance.

## States

- `loading`: skeleton cards. `empty_domain`: honest copy. `no_results`: search suggests related domains. `offline`: cached records with stamps.

## Interactions

- Search → instant ranked results; Enter → first result's reading view.
- Domain card → DomainRoom (center morphs; URL updates; back returns to shelf).
- Perspective tab → same record, different depth — no data loss between tabs.
- Save to list → pointer, never copy; toast.
- "What am I missing here?" → Naya gap analysis in-panel, citing real records.

## Design tokens

Lime edge-light on obsidian; jewel-spined cards; oversized domain typography. Reading view: generous line length, 15px+ body.

## Acceptance

Search answers in <300ms perceived; domain room covers all seven sections; perspectives preserve the record; gap analysis cites real records; 9.0+.
