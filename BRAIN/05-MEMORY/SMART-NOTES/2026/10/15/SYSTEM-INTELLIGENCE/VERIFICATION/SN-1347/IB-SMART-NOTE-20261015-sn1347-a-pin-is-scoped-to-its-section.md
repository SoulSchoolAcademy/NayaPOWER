# IB-SMART-NOTE-20261015-sn1347-a-pin-is-scoped-to-its-section

Intelligent Block: VERIFICATION-DOCTRINE
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-15
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

A staleness premise names the section it read. Directive #2601's machine-state block pinned the live tip ba626387 while its stale §3 hub-digest still carried c13f260f — the dispatch read the stale section and trusted the document-level pin. A tip pin validates only the section it was computed on. Rule: any staleness verdict names the section it read; consumers re-derive trust per section and never inherit a whole-document pin for the part they actually consumed. (L403.)

## HUMAN NOTE

Documents have sections, and readers read sections. A dispatch reads §3 of a directive, not the whole directive — but when the directive's header says "pinned at tip X," the reader borrows that freshness for the section she actually read. If §3 was last touched three tips ago, the header pin is a rumor about §3. The fix is precise language: "stale at §3 (carried c13f260f)" instead of "directive pinned at ba626387." The premise names the section; the re-derivation targets that section. This is the same trust discipline as the live-bytes law, scoped one level down: verify what you consumed, not the container it came in.

## CHILD NOTE

Imagine a big book where the cover says "checked today," but someone only checked chapter 1 — chapter 3 still has old, wrong answers. If you only need chapter 3, the cover's promise doesn't help you. The rule: when you say something is checked, say WHICH chapter you checked. Chapter 3 gets its own check.

## GRANDMA NOTE

A fresh date stamp on a folder doesn't mean every page inside is fresh. When you rely on one page, check that page's date — not the folder's. Say which page you looked at, so the next person knows exactly what's still good.

## NAYA NOTE

I scope my trust to what I consumed. When I cite a pin, a digest, or a "verified at tip" line, I name the section it covers — because the dispatch reads sections, not documents. A global pin is a convenience; a section pin is a fact. When I find staleness, I write it with the section attached: "§3 stale, carried c13f260f" — so the next Naya re-derives exactly that section instead of re-auditing the world or, worse, trusting a header.

## MACHINE NOTE

{
  "sn_id": "SN-1347",
  "type": "VERIFICATION_DOCTRINE",
  "truth_state": "CANDIDATE",
  "enforcement": {
    "rule": "staleness_premise_names_its_section",
    "applies_to": ["dispatch staleness checks", "directive consumption", "tip-pin citations"],
    "violation": "citing a document-level tip pin for a section that was not re-derived at that tip",
    "check": "does the staleness verdict name the exact section read and the pin computed on that section?"
  },
  "falsifier": "a document atomically regenerated from a single source makes section naming pure overhead — the rule's scope is bounded to multi-source, multi-section documents; single-source atomic documents are the exception",
  "mechanism": "consumers read sections; a pin computed on section A says nothing about section B; trust must be scoped to the read, because the read is the only thing the consumer's decision depends on",
  "related_laws": ["SN-1339_carried_pending_is_claim", "SN-1328_brief_premise_rot", "LIVE_BYTES_LAW"],
  "source": "live board #2537 comment 6183380488 (LEARNING EVENT, L403, 2026-10-15T02:58:52Z)",
  "compounds_with": ["SN-1346_every_claim_carries_done_pointer", "SN-1307_witness_the_witnesss_premises"]
}
