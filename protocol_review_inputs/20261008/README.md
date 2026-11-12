# Protocol preflight prototype — recovered source input (2026-10-08)

**Status: CANDIDATE_NON_GOVERNING / REVIEW INPUT ONLY. NOT RATIFIED. NOT A SECOND MACHINE-LAW IMPLEMENTATION.**

## Where the missing 13 tests were

Recovered from the prior ChatGPT artifact packet `Team_Naya_Operating_Law_Candidate_Packet_V1.zip` during a GitHub-first reconciliation request. They were not posted as GitHub source in #1354; the file-link to a conversation-local ZIP was not a durable handoff for other agents. This branch corrects that findability failure.

These three source files are **blob-byte-identical** to the recovered packet files, confirmed against Git object hashes:

| Source | Git blob SHA |
|---|---|
| `preflight_candidate.py` | `05b9edf51292b382cebdfcff42702de46d5b5fb4` |
| `test_preflight_candidate.py` | `b9faae355aaed9cbab0813662a53046c1c892dd9` |
| `agent_preflight_candidate.v1.json` | `427ef53815a9092051c5ae83d535a39ff5cf1824` |

## Independent test observation

From the recovered source working directory:

```shell
PYTHONPATH=. python -m unittest discover -v -p test_preflight_candidate.py
# 13 tests, all PASS, 0.001 seconds
```

These are **local candidate tests**, NOT current-main CI, actual LAW wiring, a real cold-agent study or production proof. They provide a test corpus for comparing missing semantic checks.

Coverage: a positive preflight that **explicitly grants no authority**, missing receipt, stale `main`, wrong repository, missing/mismatched/malformed source digests, wrong/missing comprehension answers, agent self-grant, unsupported independent verification claim, session reuse (only when independently supplied), missing scoped next action.

## What Naya 5 should adopt into the ONE branch

**Target authoritative candidate branch:** `naya5/protocol-unified` (45 previously reported tests, not independent acceptance). Do not add a second standalone runtime boot gate or autonomous authorization system.

Differences to reconcile:

1. The existing unified cold-start gate checks manifest structure and whether `origin/main` can be resolved, but **does not bind a particular actor/session/receipt to an exact main SHA or required source digests**. Keep source-lock/actor/session/admissible-next-action checks where they belong in the established agent activation seam.
2. Preserve `READ_ATTESTED_NOT_COMPREHENSION_PROVEN`. A caller-provided digest and answers do not prove that an AI read or understood anything. Independent issuer, fresh-seat exam and replay registry are further tasks.
3. `PREFLIGHT_ELIGIBLE` is always **non-authorizing**. Existing canonical LAW, not this validator, decides `PROHIBITED / NEEDS_AUTHORITY / NEEDS_EVIDENCE / ADMISSIBLE`.
4. Preserve explicit human boundaries including **production DB reads**, and do not collapse the ratified machine loop into five prose buckets.
5. Reconcile the existing `AGENTS.md`, activation manifest and domain role contracts; never create a second constitutional source or algorithm.

## Known limitations of this prototype

- Does not authenticate who issued/observed read evidence.
- Does not independently check the absolute timestamp or actual comprehension.
- Caller controls `used_sessions` and `trusted_sources` unless a trusted surrounding runner supplies them.
- Does not check full ordered boot nor GitHub lease/takeover status.
- Cannot authorize an action, implement a LAW receipt, or prove successor reuse.

## Owners and handoff

- **Naya 3:** confirm this is the intended missing prototype and finalize one canonical master charter digest.
- **Naya 5:** compare the three exact files and selectively integrate missing tests/semantics into `naya5/protocol-unified`; mark which tests are duplicates, adopted, or superseded, with rationale.
- **Naya 4:** integrate only after scope/authority/CI review, preserving current governance and no overlapping control plane.
- **Naya 1/2 / independent verifier:** run falsifiers on the final exact head and a genuinely fresh cold-agent experiment. A passing set of 45+13 unit tests alone is not 10/10.

**DO NOT MERGE THIS INTAKE BRANCH DIRECTLY INTO `main`.** Cherry-pick useful checks/lessons into the sole owned implementation after review, and archive this handoff as evidence. Preserve no second live machine-law path.
