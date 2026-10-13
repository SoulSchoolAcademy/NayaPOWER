# Retrieval-Authorization Wiring Packet — t0537 (Naya Smith, Lane 9)

**STATUS: AWAITING-SHAWN — no wiring until Shawn's word.** This packet is a
candidate branch: migration draft + refusal-point contract + mechanical tests.
Nothing here is merged; nothing here touches the production retrieval path.
Wiring is a protected human gate (authority/privacy change).

- **Packet branch:** `naya/nine-retrieval-auth-wire-packet-t0537`
- **Base:** main tip `512a8439923adbf133a1d0ac28726f2ddc961925` (pinned via
  `git ls-remote` at t0597 action time; tip commit 2026-10-13 00:14:35 PDT;
  re-pin before merge)
- **Re-anchor (t0597):** re-based from branch head `9a7c6024` onto the live
  tip. Packet tools files are byte-identical to their original pins below
  (sha256 re-proven at re-anchor time); only this doc's header pins moved.
  Previous anchor `9a7c6024` (base `dbe06f9e`) preserved in receipt history.
- **Gate candidate (already on main):**
  `tools/retrieval_authorization_gate.py` — sha256
  `fbe6ee29482fdc57345e6ba03f6252061764fa015a5d7a86f562bd345c69a28f`
  (matches t952 Lane 1's verified pin byte-for-byte)
- **Spec 0007 (on main):**
  `BRAIN/00-SPEC/0007-RETRIEVAL-AUTHORIZATION-GATE-SPEC-V1.md` — sha256
  `821a10784add98db9dcce4c8e238d17292572eb22149034dbca6ac3d701e63c7`
  (status VERIFIED-CANDIDATE per t942/t952; not ratified; re-verified
  t0597: byte-identical on main@`512a8439` and on the never-merged
  `naya/five-retrieval-auth-gate-t942`@`e654f16e` — quarantine reference)
- **Packet files (this branch only):**
  - `tools/refusal_point_t0537.py` — sha256
    `e8254132d38c0c39a0a6c42f7b63a0bc08435bef730e2f3602ed5ed897e5d2be`
  - `tools/test_refusal_predicate_t0537.py` — sha256
    `ea0affe808d155ad1a5276ee8f4b98295a4a8f62f97f3bab0e1b2f010735af15`
    (18/18 green)
  - `tools/red_demo_refusal_t0537.py` — sha256
    `9d9b0182a513aada99f67716a8e5ea81a21222f47f8de5738d4920973adaaf96`

## In a nutshell

The retrieval gate has a verdict but no mouth: it can say "refuse" and there
is no mechanical place where that refusal happens. This packet gives it the
mouth — a refusal point as code — plus the step-by-step plan for wiring it
in, so that when Shawn says the word, wiring is one human click, not a
research project.

## What the packet is / is not

- IS: the refusal-point contract as code (candidate), mechanical tests that
  prove the predicate fires, the migration draft for wiring, and the
  provenance pins a merger needs.
- IS NOT: a merge request, a wiring, a ratification, or a stamping of the
  corpus. `retrieve()` is byte-identical to the base tip. No production code
  imports any packet file.

## The refusal-point contract (summary)

Full text: the module docstring of `tools/refusal_point_t0537.py`. The three
parts Lane 9's t0531 verdict required:

- **WRITE PATH** — the disposition/index commit point: any path that makes a
  note entry retrievable by, or projectable to, a surface beyond its
  authorization. On tip `512a8439` (all `tools/smart_note_v2.py`, sha256
  `92d8b2be…` byte-identical to the t0580b/t0585 pin):
  - W1 `​_update_registry_locked` (line 545) — registry index write; an entry
    committed here becomes visible to `retrieve()`'s corpus filter.
  - W2 `render` (line 454) — projection commit; PUBLIC projection of a
    PRIVATE note is the write the `ACTIVE_AUTH_GATED` label names.
- **EXIT PROTOCOL** — refusal raises `RefusalError`. The guarded commit is
  NEVER invoked on refusal: nothing written, nothing leaked. Codes are
  silent-exclusion codes (spec 0007 §4.3 — name a code, never content, ids, or
  existence detail). The CLI harness exits 2 on refusal, 0 on permit, 3 on
  malformed packet: exit non-zero blocks the disposition close (FP-003
  falsifier-suite rule).
- **HOOK LOCATION** — where wiring installs the guard (on Shawn's word):
  - H1 read side: `retrieve` (line 810) at the lifecycle filter (~line 753):
    `guard_disclose` wraps the per-entry verdict before scoring.
  - H2 write side: `_update_registry_locked` (line 545), before the entry is
    appended to `registry["entries"]`: `guard_write`.
  - H3 projection side: `render` (line 454), before a PRIVATE note commits to
    a public projection path: `guard_write`.

## Migration draft (the wiring plan — NOT executed)

- **M1 — the seam change.** In `retrieve()` (`tools/smart_note_v2.py:810`),
  add the authorization verdict at the lifecycle filter (~line 753), before
  scoring, mirroring the candidate's `filter_corpus` order (lifecycle →
  supersession → tri-state → scope). New signature per spec §4.1:
  `retrieve(query, areas=None, task_contexts=None, *, caller=None)`; default
  `None` = unauthenticated public = most restrictive (fail closed).
- **M2 — caller updates (line numbers verified on tip `512a8439`; the file
  is byte-identical to the pinned seam, so all line numbers hold).**
  - `tools/know_measure/harness.py:109` — `res = sn2.retrieve(query)`
  - `scripts/gate-learning-compounding.py:152` —
    `return mod.retrieve(" ".join(expanded))`
  - the cold-retrieve drill harness — passes an explicit private-surface
    caller (it runs in-process with full corpus access).
  Every current caller passes an explicit `caller`; a silent legacy default
  would be a silent leak (spec §4.4.1).
- **M3 — corpus-stamping migration (authority decision, NOT done here).**
  Today's index has no `retrieval_authorized` writer: the strict tri-state
  treats missing/None as UNKNOWN → fail closed. Wiring tomorrow excludes
  EVERYTHING until a stamping migration stamps each entry. The migration needs
  Shawn's authority decision: who may stamp, what evidence each stamp carries,
  and the grandfathering rule for historical entries. This packet's test
  `test_missing_authorization_field_write_is_refused` is the mechanical proof
  M3 is required, not optional.
- **M4 — registry invariant.** `audit_registry_semantics()` is extended so
  the `ACTIVE_AUTH_GATED` label becomes a mechanically-checked invariant
  (spec §4.4.3): a PRIVATE-scope entry projected to a public path fails the
  audit — detective today, wired to the refusal point at H2.
- **M5 — runtime caller binding.** A self-declared `caller` dict is a claim,
  not proof (spec bypass B2). Wiring time must bind the surface claim to an
  authenticated surface the way `render()` binds `private_root`; until then
  the packet's contract treats claims without identity as refused.

## Single-click checklist (for Shawn's word)

1. Shawn's word to wire (protected gate) + the M3 stamping authority decision.
2. Merge this packet branch under the Scorecard Law machinery (2+ seats,
   9.0+, exact-head pin) — the refusal tests re-run on the merged bytes.
3. A build seat applies M1 + M2 + H2 (+H3 at the projection commit); no other
   production file is touched by this packet.
4. A verification seat re-runs Lane 1's four-way template on the WIRED bytes
   (t952 proved the candidate; the seam stays open until the wired proof).
5. M4 audit extension + M5 caller binding land as named follow-ups before any
   production deploy.

## Provenance

- Candidate built Lane 5 t942, branch
  `naya/five-retrieval-auth-gate-t942` @ `e654f16e8a49e9a26309fd852695a0bef202673d`
  (pushed since t942); module bytes on main match the t952 pins exactly.
- Independently verified Lane 1 t952: candidate-level ACCEPTED; seam open
  until wiring ("as built, closes the t902 hole at the read seam" OVERCLAIMED
  and correctly marked EXPERIMENT_FAILS on that wording).
- Refusal contract Lane 9 t0537 (this packet): the missing mouth, now on disk.
