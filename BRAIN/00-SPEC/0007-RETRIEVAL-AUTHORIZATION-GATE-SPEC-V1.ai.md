# 0007-RETRIEVAL-AUTHORIZATION-GATE-SPEC-V1 — AI decision framing

## Reach for this when

You are touching the retrieval path (`smart_note_v2.retrieve()`), privacy scoping, or anything that reads lessons on behalf of a caller — and need to know what the authorization rule is, what's proven, and what is BLOCKED on Shawn's word.

## The proven problem (decision fact)

`retrieve(query)` takes a query and nothing else — no caller, no credential, no surface, no context. Its only filter reads `lifecycle_state`. A repo-wide grep for `retrieval_authorized` returned zero hits in pre-existing code: the field the t902 probe used is not defined anywhere. **The claim "unauthorized lessons are excluded" was never implemented.** Status: VERIFIED-CANDIDATE — the candidate module passed its own acceptance suite (25/25 tests + 9 adversarial probes, second-seat verified t942). NOT RATIFIED. Wiring into production code remains BLOCKED until Shawn gives his word (authority/privacy change = protected gate).

## The rule (exact — implement this, not a paraphrase)

Change `retrieve(query)` → `retrieve(query, *, caller=None)`. `caller` is `{"surface": "private_authenticated", "identity": "<named party>"}`. **Default `None` = unauthenticated public = most restrictive posture (fail closed).** Per entry, BEFORE scoring:

- `scope = str(entry.get("scope") or "PRIVATE").upper()` — private by default; missing field = PRIVATE.
- `public_authorized = publication_scope in {"PUBLIC", "COLLECTIVE", "PUBLIC_DERIVED_VIEW"}`.
- If `public_authorized` → visible. Otherwise → visible only to a bound authenticated private surface with a non-empty named identity.
- This mirrors `render()`'s projection rule exactly (same default, same vocabulary, same surface requirement) — moved to the read seam.
- Authority never promotes irrelevance: the gate filters the corpus; relevance still dominates ranking inside the visible set.
- Backward compatibility is deliberately broken: all existing single-arg callers must pass an explicit caller. Silent legacy default = silent leak.

## Failure discipline

Unauthorized entries are **silently excluded** — no refusal code that names the withheld note (it would leak existence). If nothing remains, the existing `SystemExit("NO_RELEVANT_INTELLIGENCE")` fires. No new refusal codes. Log counts, never withheld note IDs.

## The seven bypass paths (named — the acceptance proof must try them)

B1 registry edit (process seam, not file integrity) · B2 self-declared caller (asserted, not attested — needs runtime binding) · B3 forged scope at capture (capture is trust-first) · B4 registry metadata leak (titles/keywords of PRIVATE notes readable from index.json — a separate disclosure decision) · B5 grant expiry at read (needs the read-side-grants spec) · B6 bypassing `retrieve()` entirely (filesystem access = access) · B7 the `retrieval_authorized` phantom (no writer exists — never wire a gate to a field with no writer). The candidate module resolves B7 by definition: only exact boolean `True` authorizes, exact `False` denies; everything else fails closed.

## The dos

- Any `retrieve()` caller you add or keep MUST pass an explicit `caller` — fail closed by default.
- The caller's surface claim must be bound by the runtime to an authenticated surface (like `render()`'s `private_root`); a self-declared dict from an untrusted context is a claim, not proof.
- Registry write paths must never project a PRIVATE-scope entry to a public path with `smart_link_status: ACTIVE` — the `ACTIVE_AUTH_GATED` label must become a mechanically-checked invariant.

## The don'ts (hard stops)

- **Do NOT wire this gate into production until Shawn gives the word.** Flagged, not executed. This is a protected gate.
- Do NOT wire a gate to a field with no writer (B7).
- Do NOT change the elevation ladder, grants, or the truth-state guard in the name of this spec — it does not invent authority, it enforces the existing privacy boundary at the read seam.

## Acceptance proof (definition — executed after wiring, under his word)

Lane 1's four-way experiment template against the wired gate: control (zero-relevance query → `NO_RELEVANT_INTELLIGENCE`) · treatment (`scope=PRIVATE` seed: public caller must NOT surface; bound private caller MUST surface; unique-token query with public caller → `NO_RELEVANT_INTELLIGENCE`, proving exclusion is by the filter not ranking) · adversarial (B3 forged COLLECTIVE seed and B5 expired-grant RATIFIED note: expected to surface — recorded as capture-integrity / grants-read-side findings, not gate failures) · successor (cold child agent reproduces independently, sealed expectations before arms). Pass = treatment arm exact + adversarial arms honestly recorded + successor agreement. Partial credit is a falsification.

## Circle links

- 📋 Board: https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2537 (live coordination)
- 📜 Master Directive: https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2601
- Owning doc: `BRAIN/00-SPEC/0007-RETRIEVAL-AUTHORIZATION-GATE-SPEC-V1.md`
- Paired tongues: `0007-RETRIEVAL-AUTHORIZATION-GATE-SPEC-V1.human.md` · `0007-retrieval-authorization-gate-spec-v1.machine.json`
