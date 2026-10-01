# P3: L2 Evidence Plan for Demo-1 Artifact-Write Claim

**Claim:** `claim-demo1-artifact-written` — "staging.write_file wrote artifact (1082 bytes, sha256:54e359a5...)"

**Current state:** PROVE returns NEED_EVIDENCE (held at UNPROVEN, required L2).

## Exact floor failures (from PROVE's returned reasons)

### G2 (§3.2): Oracle not qualified

**Failure:** "G2 fail: evidence .../artifact.md oracle unqualified (§3.4)"

**What this means:** PROVE's G2 gate requires every evidence item to have
`qualified_oracle: True`. Our P2 evidence honestly sets `qualified_oracle: False`
because it's a direct byte read, not an oracle attestation.

**The contract question:** What IS a "qualified oracle" for the claim
"this frozen package contains these bytes"?

The package is self-contained and content-addressed (seal `e451e95a`).
We verify internal consistency (seal → manifest → per-file hashes).
There is no external oracle that can attest to package-internal bytes
beyond the package itself and its GitHub commit.

**Candidate oracles:**
1. **GitHub commit** (`ac45084d`): immutable, content-addressed. The package
   exists at this commit. Reading via GitHub API is a different source
   than local filesystem.
2. **Coda 2 (independent verifier):** a different agent in a different
   environment re-reading and recomputing. This is the "independent"
   in "independent verification."
3. **The seal itself:** the package seal binds the manifest which binds
   all files. This is cryptographic, not oracle-based.

**Smallest governed resolution:** Coordinate with Coda 2 for independent
observation. Do NOT unilaterally redefine "qualified oracle" to include
"we read the bytes ourselves." That would be lowering the floor.

### G4 (§3.9): Insufficient independent observations

**Failure:** DATA_FLOOR_OBSERVATIONS = 5 required. We have 2 evidence items.

**What this means:** PROVE requires 5 observations that are independent
per §3.9: differ in source, method, or acquisition time AND share no
single failure mode.

**We do NOT:**
- Duplicate the same package read 5 times (same source/method = not independent).
- Invent priors (no prior beliefs to count as observations).
- Relabel dependent observations (e.g., "manifest read" and "file read"
  from the same local filesystem access are not independent).

## Proposed L2 observations (honest independence analysis)

| # | Source | Method | Acquired | Failure mode | Independent? |
|---|--------|--------|----------|--------------|--------------|
| 1 | Local filesystem (Naya 4) | sha256 recompute from bytes | 2026-10-01 | Local disk corruption | — |
| 2 | GitHub API (Naya 4) | HTTPS content fetch + hash | 2026-10-01 | GitHub serving wrong bytes | Yes (≠ source, ≠ method from #1) |
| 3 | Coda 2 environment | Independent recompute | TBD | Coda 2 env compromise | Yes (≠ agent, ≠ environment) |
| 4 | Package manifest | Per-file hash verification | 2026-10-01 | Manifest tampering | **No** — same package as #1, shares failure mode |
| 5 | Receipt chain | Reference integrity check | 2026-10-01 | Receipt forgery | **No** — same package as #1, shares failure mode |

**Honest count:** 3 truly independent observations (#1, #2, #3).
#4 and #5 are valuable consistency checks but NOT independent per §3.9
(they share the "package is compromised" failure mode with #1).

**Gap:** Need 2 more truly independent observations, OR a governed
determination that the floor doesn't fit this claim class.

## The contract question

**Does the 5-observation floor fit a frozen evidence package claim?**

The floor was designed for empirical claims about the external world
(where multiple independent sensors/agents can observe). A frozen
package is a fixed artifact — there are only so many independent ways
to read it:
1. Local filesystem read
2. GitHub API read  
3. Independent agent (Coda 2) read
4. ...? 

There is no 4th or 5th independent source for "what bytes are in this
commit." The claim is about a specific content-addressed artifact, not
a repeatable external phenomenon.

**Options (for governed resolution, not unilateral action):**
- **A:** Accept 3 independent observations + 2 consistency checks as
  sufficient for this claim class (requires PROVE config change — 
  director authority, not Naya 4 unilateral).
- **B:** Define "qualified oracle" to include GitHub's content-addressed
  storage (the commit SHA is the oracle). This would satisfy G2 via #2.
- **C:** Keep the floor; the claim stays at NEED_EVIDENCE until more
  independent verification paths exist. This is honest but may be
  permanently blocking.

**Recommendation:** Option B is the smallest governed resolution.
GitHub's commit SHA (`ac45084d`) IS a qualified oracle for "these bytes
existed at this commit" — it's immutable, content-addressed, and
independently retrievable. This doesn't lower the floor; it correctly
identifies the oracle.

**We do NOT:** Quietly change the claim class, lower the stakes, or
redefine "independent" to manufacture 5 observations. The floor stands
until Shawn or the governing contract changes it.

## Coordination needed

- **Coda 2:** Independent observation #3. Request: read package at
  `ac45084d`, recompute artifact SHA, report source/method/time.
- **Coda 1:** Confirm whether GitHub commit SHA qualifies as an
  oracle under §3.4, or if the battery definition needs amendment.

## What P3 delivers

- [x] Exact floor failures named (G2 oracle, G4 observation count)
- [x] Independence analysis (honest 3, not manufactured 5)
- [x] Contract question documented
- [x] Smallest governed resolution recommended (Option B)
- [x] Coordination requests specified (Coda 2, Coda 1)
- [ ] Coda 2 observation (pending their action)
- [ ] Oracle qualification determination (pending Coda 1 / Shawn)
