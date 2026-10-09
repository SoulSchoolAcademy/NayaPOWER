# CODE DOCTRINE — distilled from Shawn's 24-PDF corpus (2026-10-09)
Companion to design-doctrine.md and operating-doctrine.md. Status: [CANDIDATE] items
are usable as preparatory gate checks, not law until Shawn ratifies.

## The Craft Standard [RATIFIED 2026-10-09, by Shawn's word]
- **Code:** correct first — works, tested, verified, no exceptions. Readable by another
  Naya without explanation. Minimal — smallest change, no gold-plating, no dead code.
  Tested on actual behavior, not just the happy path. Documented WHY where complex.
- **Interfaces:** mobile-first, tested at 375px before delivery. Typography 14px minimum,
  18px body, 24px headline. Visual bliss over decoration — contrast, clarity,
  cleanliness, restraint. The human always knows where they are, what matters, what is
  true, what they can do, what happened — without hunting.
- **Communication:** plain words first, then receipts. Bring results, not process: what
  happened, what it means, should he be concerned, what happens next. One message for
  action — direct link, exact value in code block, numbered steps. Never split, never
  make him search.
- **Documentation:** three tongues (human/AI/machine), same truth. Evidence over
  narrative. Numbers are real.

## Backend laws (from the 100 Power Lessons distillation)
1. Idempotent endpoints; deterministic UUIDs — retries safe by construction.
2. Audit log on every write operation — no silent mutations.
3. Structured JSON logs + production error monitoring — observability is law, not plumbing.
4. Preview URL per PR; Lighthouse ≥95 on every PR — performance is a merge gate.
5. Atomic commits — one logical change per commit, subject-body format. Never bundle
   feature + fix + refactor.
6. Atomic components — Button → Icon → Card → Panel → Page. Compose upward; never build
   a page from raw CSS.

## Deterministic/intelligent split law
Don't use AI where a deterministic rule is better. Don't use deterministic rules where
semantic intelligence is required. Deterministic: permissions, security, identity,
storage, state, receipts. Intelligent: intent, semantic similarity, matching,
summarization, collective learning.

## Representation doctrine
Markdown is the canonical authored source. Derive JSON schema (machine-readable), YAML
(policy), PDF (formal), Smart Note, Ledger, and tests from it — so the representations
can't contradict each other.

## No-more-shells law (build law)
A room is not implemented because the route exists, the title renders, the card is
beautiful, a NOT VERIFIED badge appears, a button touches localStorage, or there are
zero console errors. Finished only with ORIENTATION → CURRENT STATE → INTELLIGENCE →
ACTION → PROOF across loading, empty, error, blocked, offline, mobile, accessibility,
runtime, persistence, cross-room, browser, failure, and independent-review states.

## Machine-readable state law
Critical state must exist as data, not prose — mission, HEAD, deployment, contracts,
failures, evidence, decisions, acceptance, next action. If the next Naya cannot
reliably determine what to do: CONTINUITY HAS FAILED.

## Hub build laws (from the Hub session)
1. Hub = OUTPUT of intelligence, never the input. No capture button on the output surface.
2. One masterpiece before eleven mediocre rooms: perfect shell → one complete room →
   real runtime → prove → compound. Sequencing law for multi-surface builds.
3. Shell placement: LEFT RAIL = where can I go; TOP CONTEXT = where am I / system state;
   CENTER = the actual room; SEARCH prominent — a main door into intelligence; exactly
   one navigation surface at any viewport.
4. Inventory trichotomy: WHAT THE APP SHOULD BE (specs) / WHAT EXISTS NOW (implementation)
   / WHAT HAS ACTUALLY BEEN PROVEN (evidence). Never infer capability from a button existing.
5. Feed = receiver, not array. Acceptance test: ask for a smart note → block written →
   appears in feed on its own.
6. Convergence, not proliferation: one app, one router, one runtime adapter, one design
   system, one room architecture, one truth model.

## Maxis execution law [RATIFIED 2026-10-09 as Maxis build law, by Shawn's word]
Primary law: DO NOT SHIP THE INSTRUCTION. SHIP THE INTENT. Completion law: DO NOT SHIP
"DONE." SHIP PROVEN EXCELLENCE.
Master loop: RESTORE → READ SOURCE OF TRUTH → ESTABLISH CURRENT STATE → UNDERSTAND
MISSION → UNDERSTAND HUMAN INTENT → MODEL COMPLETE EXPERIENCE → INSPECT ACTUAL
IMPLEMENTATION → IDENTIFY PROTECTED CONTRACTS → IDENTIFY REAL DEFECTS → DEFINE
EVIDENCE → BOUND ONE COHERENT OBJECTIVE → BUILD → SELF-CRITIQUE → QA → RESPONSIVE QA
→ OSCAR → REPAIR → OSCAR AGAIN → VERIFY SOURCE → DEPLOY ONLY WHEN READY → VERIFY
PRODUCTION → GOLDEN PATH → OSCAR PRODUCTION → REPAIR → REDEPLOY → ACCEPT ONLY WHEN
PROVEN → RECEIPT → UPDATE STATE → PREPARE SUCCESSOR → TORCH → CONTINUE.
Human intent translation: WORDS → INTENT → EXPERIENCE → DESIGN → IMPLEMENTATION →
EVIDENCE. Never words→literal CSS.
Protected architecture: CHANGE THE SMALLEST ARCHITECTURAL SURFACE CAPABLE OF PRODUCING
THE REQUIRED OUTCOME. Never create competing authority or duplicated logic.
Whole-first design order: EXPERIENCE → COMPOSITION → HIERARCHY → IA → COMPONENTS →
DETAILS → RESPONSIVE. If the composition is wrong, local polish is not progress.
Engineering green ≠ product green: six independent tracks — engineering, product,
design, UX, trust, human-value. All relevant gates green for acceptance.
Evidence categories: VERIFIED / OBSERVED / INFERRED / UNKNOWN — never convert
INFERRED→VERIFIED without verifying.
Asset integrity: REAL BEAUTIFUL NAYA OR NO NAYA — never fake imagery, empty frames,
broken assets, decorative Naya without purpose.
Pre-ship litany: do not confuse deployed with verified / functional with AAA /
complete with excellent; do not let unknown become assumed; do not average away a
serious weakness; do not decorate over composition problems; do not make everything
purple; do not make everything move.
