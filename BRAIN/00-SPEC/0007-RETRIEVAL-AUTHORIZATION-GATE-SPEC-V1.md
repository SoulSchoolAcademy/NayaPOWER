# 0007 — Retrieval Authorization Gate Spec V1

**Status: VERIFIED-CANDIDATE — the candidate gate module passed its own acceptance suite (see §9). NOT RATIFIED. Wiring into production code remains BLOCKED until the Human Director gives his word (authority/privacy change is a protected gate).**
**Seat:** Naya Sentinel (Lane 8 — Governance), tick t912, 2026-10-11.
**Verification seat:** Naya Seeker (Lane 5 — Retrieval), tick t942, 2026-10-11.
**Supersedes:** nothing. **Follows from:** Lane 5 t902 falsification (grand-list item 7, second half).

---

## 1. The problem, in plain words

The system has a rule — "private by default, shared by choice" — and a write path that enforces it (`render()` refuses to project PRIVATE notes to the public BRAIN unless an authenticated private surface is used). But the **read path**, `retrieve()`, enforces nothing. Any caller can ask any question and receive the full content of any ACTIVE lesson, including lessons marked PRIVATE.

At tick t902, Naya Seeker (Lane 5) proved this with a four-way experiment: an ACTIVE seed lesson carrying a `retrieval_authorized=false` marker was **surfaced** as the retrieval winner. There is no authorization seam at retrieval — not broken, not incomplete, **nonexistent**.

---

## 2. Governance verdict: the fix is a retrieval-side gate (Option A)

The alternative was a documented decision that authorization lives at promotion time only. That argument fails on the evidence:

1. `retrieve()` **returns full content** — it reads the winner's projection file from disk and returns it as `explanation` (`tools/smart_note_v2.py`, `retrieve()`, body of the winner-read). Promotion-side gates control state labels; they cannot contain a read that ignores them.
2. **Write-time gates cannot bound read-time disclosure.** Elevation grants are time-bounded (default 7 days, `make_grant()`) and consulted only during `apply_elevation()`. A RATIFIED note keeps surfacing from `retrieve()` forever after its grant expires. Authority bounded at elevation is unbounded at read.
3. The registry index itself **leaks metadata** — titles, keywords, topic taxonomy of every entry, including PRIVATE ones — to anyone who can read `.naya/memory/smart-notes/index.json`. Promotion-side machinery touches none of this.
4. Standing law (repo `AGENTS.md`, HUMAN AUTHORITY): *"Private by default. Shared by choice. Collective by consent. Public by decision."* A read path that ignores `owner_scope` violates the default directly.

Therefore the authorization seam belongs at the retrieval seam, mirroring the existing projection-side rule in `render()`. Promotion stays as the truth-state authority; retrieval gains a disclosure authority.

**What this does NOT do:** it does not change the elevation ladder, grants, or the truth-state guard. It does not invent authority. It enforces the privacy boundary the designers already encoded at projection time (`render()`, lines 453–458) at the one read seam every consumer uses.

---

## 3. Exact-code citations of the authorization seam(s) as they exist today

All citations verified at repo HEAD `235a61f0b8f0c09ef8f2791fbd02cea3e11db39a`, branch `naya/eight-retrieval-auth-seam` (local only).

### 3.1 The missing seam — `retrieve()` reads no authorization field

- `tools/smart_note_v2.py:646` — `def retrieve(query):` takes a query and nothing else. No caller, no credential, no surface, no context parameter anywhere in the signature or body.
- `tools/smart_note_v2.py:652` — the only exclusion before scoring: `inactive = {"SUPERSEDED", "ARCHIVED", "REVOKED"}`, then `if str(e.get("lifecycle_state", "ACTIVE")).upper() in inactive: continue` (line 658). **This is the whole filter.** It reads `lifecycle_state` only.
- A repo-wide grep for `retrieval_authorized` returns **zero matches in any pre-existing code, schema, or docs** (the only matches after this spec was written are this spec file itself) — the field Lane 5 used in its probe is not defined anywhere in the codebase. There is no seam to be broken; the claim "unauthorized lessons are excluded" was never implemented.
- `retrieve()` likewise never reads `scope`, `publication_scope`, `owner_scope`, `human_director_authorized_publication`, or elevation grants (`BRAIN/01-GOVERNANCE/elevation-grants/`).

### 3.2 The projection-side privacy boundary that `retrieve()` bypasses

- `tools/smart_note_v2.py:453–458` (`render()`): `scope = str(block.get("owner_scope", "PRIVATE")).upper()`; `public_authorized = bool(projection_meta.get("human_director_authorized_publication")) or publication_scope in {"PUBLIC","COLLECTIVE","PUBLIC_DERIVED_VIEW"}`; if `scope == "PRIVATE" and not public_authorized` → requires `private_root` (an authenticated private surface) or raises `SystemExit("PRIVATE_PROJECTION_REQUIRES_AUTHENTICATED_PRIVATE_SURFACE")` (line 458).
- `tools/smart_note_v2.py:576–581` (`_update_registry_locked()`): registry entries record `scope`, `publication_scope`, and `smart_link_status` — `"ACTIVE_AUTH_GATED"` when a PRIVATE-scope note is projected to the public BRAIN path. The label *names* an auth gate; no code implements one at read time.

### 3.3 The elevation grant machinery (promotion-time only)

- `tools/truth_state_guard.py` — `apply_elevation(entry, new_state, authority, evidence, ...)` enforces authority + evidence at write time. Elevation grants are required **only** for `VERIFIED->RATIFIED` (`check_elevation_grant`, lines ~248–275; `apply_elevation` calls it only in the `old == "VERIFIED" and new == "RATIFIED"` branch). Retrieval never consults grants, grant expiry, or `elevation_history`.
- `tools/truth_state_guard.py` `audit_registry_semantics()` — detective, not preventive. Finds escalation already on disk; cannot stop a read.
- `BRAIN/01-GOVERNANCE/README.md:9` — canonical governance doctrine: *"No retrieval result grants authority."* Retrieval is deliberately decoupled from authority — which is exactly why a **disclosure** gate (not an authority grant) is the right shape here.

---

## 4. The gate spec

### 4.1 Seam and signature

Change `tools/smart_note_v2.py:646`:

```python
def retrieve(query, *, caller=None):
    ...
    for e in registry.get("entries", []):
        if str(e.get("lifecycle_state", "ACTIVE")).upper() in inactive:
            continue
        if not _retrieval_visible(e, caller):   # <-- NEW: authorization filter
            continue
        ...
```

`caller` is an explicit auth context, e.g. `{"surface": "private_authenticated", "identity": "<named party>"}`. **Default `None` means unauthenticated public — the most restrictive posture (fail closed).** Backward compatibility is deliberately broken at the seam: all existing single-arg callers (`tools/know_measure/harness.py:109`, `scripts/gate-learning-compounding.py:152` and its embedded harness at line 301, the cold-retrieve drill) must pass an explicit caller context. Silent legacy default = silent leak.

### 4.2 Visibility rule — `_retrieval_visible(entry, caller)`

Evaluated per entry, **before scoring** (same placement as the lifecycle filter — Lane 5's A2 arm proved exclusion-by-filter, not ranking, is what holds):

```
scope           = str(entry.get("scope") or "PRIVATE").upper()      # private by default; missing field = PRIVATE
pub_scope       = str(entry.get("publication_scope") or "").upper()
public_authorized = pub_scope in {"PUBLIC", "COLLECTIVE", "PUBLIC_DERIVED_VIEW"}
                  # (human_director_authorized_publication lives on the capture's
                  #  projection block at render time; the registry's publication_scope
                  #  is its persisted projection of that decision)

if public_authorized:
    return True                                    # shared by choice / consent / decision

private_surface = (isinstance(caller, dict)
                   and caller.get("surface") == "private_authenticated"
                   and str(caller.get("identity") or "").strip() != "")
return bool(private_surface)                       # PRIVATE notes need the authenticated private surface
```

This mirrors `render()`'s rule (3.2) exactly: the same `scope` default, the same publication-scope vocabulary, the same private-surface requirement — moved to the read seam. **Authority never promotes irrelevance** stays intact: the gate filters the corpus; relevance still dominates ranking inside the visible set.

### 4.3 Failure discipline

- Unauthorized entries are **silently excluded from the corpus**. If nothing remains, the existing `SystemExit("NO_RELEVANT_INTELLIGENCE")` fires — identical to the lifecycle-filter path. Rationale: a refusal code that names the withheld note leaks existence; the lifecycle filter already established silent-exclusion as the house pattern (proven t902).
- No new refusal codes. No logging of withheld note IDs to stdout (log only counts, if anything, to the existing promotion/ledger surfaces).

### 4.4 Integration requirements (non-negotiable with the wiring)

1. Every current `retrieve()` caller passes an explicit `caller` (list in 4.1); the cold-retrieve drill passes `{"surface": "private_authenticated", ...}` since it runs in-process with full corpus access.
2. The `caller` surface claim must be **bound by the runtime to an authenticated surface** (like `render()`'s `private_root`); a self-declared dict from an untrusted context is a claim, not proof (see bypass path B2).
3. Registry write paths must never let a PRIVATE-scope entry be projected to a public path with `smart_link_status: ACTIVE` (the `ACTIVE_AUTH_GATED` label at 3.2 must become a mechanically-checked invariant, audited by extending `audit_registry_semantics()`).

---

## 5. Bypass paths an attacker would use (named, so the acceptance proof can try them)

- **B1 — Registry edit.** `index.json` is a JSON file on disk. Anyone with write access can point `projection_path` at a private note's file, or flip `scope` to `COLLECTIVE`. The gate is a *process* seam; `audit_registry_semantics()` is detective-only. Mitigation belongs to file integrity (append-only/receipted writes like `kernel/memory_store.py`), not this gate.
- **B2 — Self-declared caller.** The `caller` dict is asserted, not attested. A malicious in-process caller passes `surface: private_authenticated` with a fabricated identity. Requires runtime binding (4.4.2).
- **B3 — Forged scope at capture.** Nothing validates `owner_scope` claims at capture time — capture is trust-first. A note captured with forged `scope: COLLECTIVE` passes the gate legitimately. Capture-time provenance integrity is out of scope for this gate.
- **B4 — Registry metadata leak.** Titles, keywords, taxonomy of PRIVATE notes remain readable from `index.json` by anyone with filesystem access, with or without this gate. The gate covers *content retrieval through `retrieve()`*; the index's own disclosure surface needs its own decision.
- **B5 — Grant expiry at read.** A RATIFIED note whose elevation grant expired still surfaces after this gate (grants are write-time only). If time-bounded authority must bound reads, grants need a read-side consultation — a separate spec.
- **B6 — Bypassing `retrieve()` entirely.** Reading projection files or Supabase rows directly. Filesystem/DB access equals access; no process-level gate survives that. The gate protects the *canonical retrieval seam*, not the storage layer.
- **B7 — The `retrieval_authorized` phantom.** Any future code that reads a `retrieval_authorized` field must define it first — today it exists nowhere (3.1). Do not wire a gate to a field with no writer; fields with no writer are attacker-controlled defaults.

---

## 6. Acceptance proof (definition — to be executed after wiring, under Shawn's word)

Re-run of **Lane 1's four-way experiment template** (`~/workspace/goals/bring-naya-to-life/hidden_files/four-way-template/run_four_way.py`, built t892, used t902) on the unauthorized arm, against the wired gate:

- **Control:** zero-relevance query → `NO_RELEVANT_INTELLIGENCE` (fail-closed baseline holds).
- **Treatment:** hyper-relevant ACTIVE seed with real field `scope=PRIVATE` (not the phantom `retrieval_authorized`).
  - `caller=None` (public) → seed **must not surface** (excluded by filter).
  - `caller={"surface": "private_authenticated", "identity": "<named>"}` → seed **must surface**.
  - A query matching *only* the seed's unique token with public caller → `NO_RELEVANT_INTELLIGENCE` (proves exclusion is by the filter, not ranking — the t902 A2 pattern).
- **Adversarial:** B3 (forged `scope=COLLECTIVE` seed — record outcome honestly; expected: surfaces, and that is a capture-integrity finding, not a gate failure) and B5 (RATIFIED note with expired grant — expected: surfaces; recorded as known residual for the grants-read-side spec).
- **Successor:** a cold child agent with only the claim + repo access reproduces the decisive answers independently (sealed expectations before arms, per the template's blinded protocol).

**Pass criterion:** treatment arm exact (both caller postures), adversarial arms honestly recorded with named mechanisms, successor agreement. Partial credit is a falsification — report it as one.

---

## 7. What needs the Human Director's word (BLOCKED — flagged, not executed)

- Wiring this gate into `retrieve()` is an **authority/privacy change** (protected gate): it changes who can see what intelligence, breaks every current caller, and redefines the default disclosure posture. **Do not implement until Shawn says the word.**
- The `ACTIVE_AUTH_GATED` smart-link invariant (4.4.3) and any read-side grant consultation (B5) are separate authority decisions — also his.
- The registry metadata leak (B4) is a disclosure-policy decision — his.

---

## 9. Candidate-module verification (t942 — added by Naya Seeker, Lane 5)

Lane 8's t912 receipt (8.5/10) named the successor arm of the acceptance proof as
blocked on a wired gate. This section records what a DIFFERENT seat verified
without wiring, per the dispatcher's t942 brief (candidate module only).

**Branch:** `naya/five-retrieval-auth-gate-t942` (local only, unpushed — parented on
main tip `1b6f72defa9b7eea98acc822fe80ab307db1aff2`). **No production code
touched:** `tools/smart_note_v2.py::retrieve()` is byte-identical to main tip;
no production path imports the candidate module (grep-verified).

**RED-first (hole proven on the unwired seam):**
- `tools/red_demo_t942.py` — applies retrieve()'s exact lifecycle-only predicate
  to four probe entries: 1/4 excluded (superseded via the pre-existing filter —
  the t902 A1/A2 arm). The unauthorized ACTIVE seed (`retrieval_authorized=false`),
  the stale-cache copy, and the tampered flag (`"yes"`) all PASS THROUGH.
  Static check: `retrieval_authorized` appears nowhere in `smart_note_v2.py`.
- `tools/test_retrieval_authorization_gate.py` written before the module existed:
  first run fails on `ModuleNotFoundError` (the gate does not exist) — RED recorded.

**Candidate module:** `tools/retrieval_authorization_gate.py` (CANDIDATE, stdlib-only,
no I/O). Implements this spec §4 exactly, with one resolution of bypass path B7
(the `retrieval_authorized` phantom): the candidate DEFINES the writer contract —
only the exact boolean `True` authorizes, only the exact boolean `False` denies;
everything else (missing, `None`, `"yes"`, `1`) is UNKNOWN and fails closed.
Truthy-but-not-True is never treated as authorization.

**GREEN (module's own suite — positive, negative, adversarial):**
- `pytest tools/test_retrieval_authorization_gate.py` → **25/25 PASS**.
- Adversarial probe run (9 probes): unauthorized seed with valid-looking
  metadata → EXCLUDED; superseded resurrected via stale cache → EXCLUDED
  (registry is the source of truth); tampered flags (`"yes"`, `1`) →
  FAIL_CLOSED; revoked-after-capture → EXCLUDED; unknown scope value with
  public caller → EXCLUDED; self-declared surface without identity (B2) →
  EXCLUDED. Positive controls hold (authorized PRIVATE + bound private caller
  visible; authorized PUBLIC + public caller visible).

**What the module does NOT cover (named, not hidden):**
- Spec §4.4.2 — the `caller` surface claim is asserted, not attested; runtime
  binding to an authenticated surface is a wiring-time requirement.
- B5 (grant expiry at read) — untouched; needs the separate read-side-grants spec.
- B4 (registry metadata leak) — out of scope for this gate (disclosure-policy decision).
- Corpus migration: today's 617-entry index has no `retrieval_authorized`
  writer — with the fail-closed default, wiring would exclude everything until
  a stamping migration runs. That migration is itself an authority decision.

**Verdict for the spec status:** CANDIDATE → VERIFIED-CANDIDATE. The gate's
logic is proven against its own contract; the four-way acceptance proof (§6)
still requires the wiring decision, which remains **BLOCKED pending Shawn's
word — flagged, not executed.**

## 8. Provenance

- Trigger: Lane 5 t902 falsification — receipt `~/workspace/goals/bring-naya-to-life/hidden_files/twelve-lane-receipts/t902-lane5.md`.
- Audit method: read `tools/smart_note_v2.py` (1291 lines) and `tools/truth_state_guard.py` (452 lines) in full; repo-wide grep for `retrieval_authorized` (0 hits), `retrieve(` callers, and `owner_scope` usage; `BRAIN/01-GOVERNANCE/README.md` doctrine.
- No production code touched. No tests run (spec's internal consistency checked only: all cited line numbers verified against HEAD bytes — see receipt).
- Branch: `naya/eight-retrieval-auth-seam` (local only, no push, no PR, no merge).
