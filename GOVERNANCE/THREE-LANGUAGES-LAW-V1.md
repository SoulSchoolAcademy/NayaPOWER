# The Three-Languages Law — V1

**Binding law of NayaNET and NayaPOWER. Ordered by Shawn, 2026-10-26.**
**Scope: the whole of NayaNET and GitHub — back end to front end, the whole of everything.**
**Supersedes the page-only three-view shorthand.** The three-view rule for the Project
Intelligence face was this law's first form; this document is the law in full.

**One record underneath. Three forms on top. Every form shows what matters to its
reader — and nothing else. All three forms stay in sync, because they are three
forms of the same thing, never three separate copies.**

---

## 1. HUMAN — in plain words

### What the law is

Everything we build speaks three languages: one for people, one for the AI seats,
and one for the machines. A person sees plain words about what matters to them.
An AI seat sees the working details it needs to do the job. A machine sees the
exact codes, numbers, and records it needs to run. Nobody is shown somebody
else's language.

### Why

Because three different players use this system, and each one deserves service
that fits them. A person should never have to read a machine code to understand
what is going on. An AI seat should never have to guess who owns a piece of work
or what happens next. A machine should never have to read a paragraph to find
an address it needs. When each player gets exactly what fits them, everybody
gets the best possible service — that is the whole point.

### What it means for a person

- You see plain words, clear as day: what is done, what is left, what is moving,
  who is doing what, and everything you gave us — in one place.
- You never see machine codes, long numbers, or our inside words on your screen.
  That detail still exists, one step behind, if you ever want it — but it never
  sits in your way.
- What you see is always up to date, because your view and the machine's view
  come from the same record. If it is not there, it is not done.
- Every page, every message, every list follows this same rule — not just one page.

---

## 2. AI — the working spec

### The rules

1. **ONE RECORD.** Every durable thing has one record of truth. The three forms
   are renderings of that record, never independent copies. If the forms disagree,
   the record wins and the stale form is fixed, not defended.
2. **HUMAN FORM.** Plain words only. What matters to the human: what it is, how
   far along it is, what is left, what is moving, who is doing what, everything
   the human gave. No IDs, hashes, endpoints, raw records, or Naya jargon on the
   human surface. Machine proof lives one step behind the item, never on its face.
3. **AI FORM.** The working view. What matters to a seat: owners, states,
   receipts, next actions, blockers, checklists, evidence links. This is the form
   seats use to do the job and to hand work to each other.
4. **MACHINE FORM.** Exact and structured. What matters to the machine: IDs,
   hashes, endpoints, schemas, raw records, signatures, timestamps in UTC. Kept
   behind the other two forms, machine-readable, never rendered as human text.
5. **DESIGNED FOR EACH, NOT TRANSLATED ONCE.** Each form is designed for its
   reader: written for the human, written for the AI, written for the machine;
   designed for the human, designed for the AI, designed for the machine. A
   machine dump relabelled "human view" is a violation. A paragraph where a
   machine needs a field is a violation.
6. **IN SYNC, ALWAYS.** A change to the record updates all three forms in the
   same motion. A form that lags the record is stale and must say so honestly
   (stale, unproven, or missing — never silently old).
7. **APPLIES TO EVERY LAYER.** Pages, records, documents, code, APIs, and GitHub
   itself (issues, boards, pull requests, comments, files). No layer is exempt.
   The Project Intelligence face goes first; everything after follows Shawn's
   execution order.
8. **VIOLATION IS A SHIP-BLOCKER.** Work that ships only one form, mixes forms
   on the human face, or lets forms drift is not done, whatever else it claims.

### Seat checklist — before calling anything done

- [ ] Human form exists and reads in plain words; a stranger could understand it
      with no inside knowledge.
- [ ] AI form exists with owner, state, next action, blockers, and evidence.
- [ ] Machine form exists, structured, with IDs and endpoints a machine can use
      without reading prose.
- [ ] All three forms trace to the same record; a fresh live read agrees.
- [ ] Nothing machine-only appears on the human surface; nothing human-only
      (unstructured prose) is the machine's only source.
- [ ] Stale or missing forms are labelled honestly (stale / unproven / missing).

### What a seat must do and check

- **Authoring:** write all three forms in the same pass, from the record.
- **Reviewing:** score each form for its own reader (human clarity, AI
  workability, machine exactness). A different seat scores a landing, as always.
- **Fixing drift:** when forms disagree, fix the form from the record and record
  the correction in the open. Never edit the record to match a stale form.
- **Filing:** every durable artifact (law, spec, note, report, page, record)
  follows the three-form template in section 4 of this document.

---

## 3. MACHINE — structured manifest

Layer-to-form mapping. Each layer lists its human, AI, and machine artifacts and
where each lives. This block is the machine-readable contract; parsers read the
JSON, humans read sections 1–2.

```json
{
  "law": "three-languages",
  "version": "1",
  "ordered_by": "shawn",
  "ordered_date": "2026-10-26",
  "supersedes": "page-only three-view shorthand",
  "rule": "one record underneath; three forms on top; each form shows what matters to its reader and nothing else; all forms in sync",
  "layers": {
    "page": {
      "human": {"artifact": "page surface in plain words", "lives": "the rendered page at its real address"},
      "ai": {"artifact": "working view: owners, states, receipts, next actions, blockers, checklists", "lives": "behind the human surface, one step in (per-item door / AI view)"},
      "machine": {"artifact": "state endpoint + raw records (ids, hashes, endpoints, timestamps)", "lives": "the page data endpoint, machine-readable"}
    },
    "record": {
      "human": {"artifact": "plain-words summary of the record", "lives": "the record's human view"},
      "ai": {"artifact": "owner, state, evidence links, next action, blockers", "lives": "the record's AI view"},
      "machine": {"artifact": "the record itself: ids, fields, hashes, signatures, UTC timestamps", "lives": "the system of record (Supabase work_items / ledger / registry)"}
    },
    "doc": {
      "human": {"artifact": "plain-words section: what it is, why, what it means for a person", "lives": "section 1 of the document"},
      "ai": {"artifact": "working spec: rules, checklists, duties", "lives": "section 2 of the document"},
      "machine": {"artifact": "structured manifest block (this JSON)", "lives": "section 3 of the document"}
    },
    "code": {
      "human": {"artifact": "plain-words README: what it does, how to use it", "lives": "beside the code"},
      "ai": {"artifact": "contracts, checklists, runbooks, decision records", "lives": "beside the code / in the spec"},
      "machine": {"artifact": "source, schemas, tests, hashes, endpoint definitions", "lives": "the repo"}
    },
    "api": {
      "human": {"artifact": "plain-words description: what it gives you, in what words", "lives": "the API's human docs"},
      "ai": {"artifact": "request/response contracts, error meanings, next actions on failure", "lives": "the API's working docs"},
      "machine": {"artifact": "endpoint paths, schemas, auth, rate limits, raw examples", "lives": "the API spec (machine-readable)"}
    },
    "github": {
      "human": {"artifact": "plain-words issue/PR/comment summaries: what changed, what it means", "lives": "issue and PR bodies, board summaries"},
      "ai": {"artifact": "owners, states, checklists, receipts, next actions, blockers", "lives": "issue and PR bodies, board comments, PI notes"},
      "machine": {"artifact": "ids, SHAs, refs, timestamps, links, labels", "lives": "issue/PR metadata, commit SHAs, file paths"}
    }
  },
  "sync_rule": "all forms derive from the same record in the same motion; disagreement means the form is stale, never the record",
  "violation": "ship-blocker: single-form work, mixed forms on the human face, or drifted forms are not done"
}
```

---

## 4. THREE-FORM TEMPLATE — every future durable artifact follows this

Copy this shape. One place, one document, three sections, in this order. Keep each
section to its own reader. If a section has nothing yet, write that honestly
(`missing`, `stale`, or `unproven`) — never borrow another section's content.

### HUMAN — what a person needs

- What is this, in plain words?
- Why does it matter to the person reading it?
- What is done, what is left, what is moving, who is doing what?
- No machine codes, no inside words, nothing unexplained.

### AI — what a seat needs to work

- Owner, state, receipts, evidence links.
- Next actions, blockers, checklists.
- Decisions taken, decisions still open (with who decides).
- What to check before calling it done.

### MACHINE — what a machine needs to run

- Structured block (JSON): ids, paths, endpoints, schemas, hashes, timestamps.
- The block must parse. A block that does not parse is a failed artifact.
- Every id and path in the block must resolve to something real.

**Template conformance check:** human section readable by a stranger; AI section
actionable by a seat that did not write it; machine section parses and resolves.
Any failure = the artifact is not done.
