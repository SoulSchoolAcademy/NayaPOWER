# The Retrieval Authorization Gate — in plain words

*For Shawn — the missing privacy seam on the read path, and the spec for the gate that closes it.*

The system has a rule: "private by default, shared by choice." The write path enforces it — the projector refuses to publish a PRIVATE note to the public brain unless it's on an authenticated private surface. But the **read path** — `retrieve()`, the one function every consumer uses to search lessons — enforces nothing. Any caller can ask any question and get back the full content of any active lesson, including ones marked private. A Lane 5 falsification proved it: an active seed lesson carrying an unauthorized marker was *surfaced as the retrieval winner*. The authorization seam at retrieval doesn't exist. Not broken, not incomplete — nonexistent.

The governance verdict: the fix belongs at the retrieval seam itself (not at promotion time). Three reasons, all evidence-backed: `retrieve()` returns full content — promotion-side gates can't contain a read that ignores them; authority grants are time-bounded but a ratified note keeps surfacing forever after its grant expires; the registry index itself leaks titles and keywords of private notes to anyone who can read it. So the seam mirrors the existing projection-side rule: private-by-default, shared-by-choice, with the private surface required for private notes.

What the spec proposes, concretely: give `retrieve()` an explicit auth context (`caller`); default `None` means unauthenticated public — the most restrictive posture, fail closed. For each registry entry, before scoring: if its publication scope says shared-by-choice (PUBLIC, COLLECTIVE, or PUBLIC_DERIVED_VIEW), it's visible; otherwise it's visible only to an authenticated private surface with a named identity. Unauthorized entries are silently excluded (no refusal code that leaks what was withheld). The module that implements this logic already exists as a CANDIDATE — a different seat verified it: its own test suite passes 25/25, and 9 adversarial probes (forged flags, stale-cache resurrection, self-declared surfaces, unknown scopes) all fail closed. The four-way acceptance proof — the real experiment that decides — is defined and waiting.

**The honest bottom line:** this spec is VERIFIED-CANDIDATE, not ratified. Wiring the gate into `retrieve()` changes who can see what intelligence — an authority/privacy change, which is Shawn's protected gate. It is **BLOCKED until he gives the word: flagged, not executed.** The spec also names seven bypass paths an attacker would use (registry edits, self-declared callers, forged capture scopes, the metadata leak, grant expiry, reading files directly, the phantom field) — named so the acceptance proof can try them, not hidden.

## Circle links

- 📋 Board: https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2537 (live coordination)
- 📜 Master Directive: https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2601
- Owning doc: `BRAIN/00-SPEC/0007-RETRIEVAL-AUTHORIZATION-GATE-SPEC-V1.md`
- Paired tongues: `0007-RETRIEVAL-AUTHORIZATION-GATE-SPEC-V1.ai.md` · `0007-retrieval-authorization-gate-spec-v1.machine.json`
