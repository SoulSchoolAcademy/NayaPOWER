# Verification Is Read-Only — Never Execute a Build Script to Check It

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01632-verification-is-read-only
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-18
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A lane-scorer ran a lane's build/merge script as a "determinism check" — and the script did what build scripts do: it wrote. `t0907-merge-catalog.py` rewrote `block-catalog.json` and `index-by-use-case.json` mid-verification, destroying the evidence the scorer was checking. Restored clean: the 478-record converged version pulled from `origin naya4/hubdrive-block-catalog`, byte-identical before/after (sha `823be4bd6406cf1922e5`). The standing discipline: verification is read-only. A build or merge script is a write instrument by design — executing it to "check" something turns a read into a write, and a verification that mutates its own artifact is self-sabotage. Verify with read-only copies and read-only tooling; build scripts stay unexecuted during verification, always.

## 🩷 HUMAN NOTE

A quality inspector ran the factory's assembly machine "just to check it was deterministic" — and the machine, being a machine that builds things, built things. It overwrote the catalog mid-inspection with a regenerated copy, and the evidence the inspector was checking was gone. The inspector caught it, pulled the true original from the archive, and proved byte-for-byte that the restored file matched. The lesson is permanent and simple: checking is reading, and reading must never write. The tools that build things are write tools by design — running one during an inspection turns the inspection into a construction project. From now on, verification uses read-only copies: look, compare, hash, never execute. The check that proves a build is deterministic is reading its output twice — never running the builder a third time on the real thing.

## 🟣 CHILD NOTE

Looking at something and changing it are different jobs. If your job is to LOOK, use only tools that look. Never press the button that builds — it will build, even when you only meant to check.

## 🔵 GRANDMA NOTE

An inspector inspects; she doesn't operate the machinery. The moment she flips the factory switch "just to see," the factory makes something and the thing she came to inspect is gone. Look with your eyes and your camera, never with the start button.

## 🟠 NAYA NOTE

Verification-discipline class (2026-10-18, lane-scorer tick ~06:05 PDT): the scorer ran `hidden_files/t0907-merge-catalog.py` as a "determinism check"; the script rewrote `block-catalog.json` + `index-by-use-case.json` (its designed function — it is a merge script). Recovered clean: restored the 478-record converged version from `origin naya4/hubdrive-block-catalog`, sha `823be4bd6406cf1922e5`, byte-identical before/after the restore; t0907's receipt-era 457-record bytes are superseded by the converged 478 anyway, so the clobber touched a live artifact with stale-era content. The scorer's own standing rule, stated in the receipt: never execute a lane's build/merge script during scoring verification — read-only copies only. This is the instrument-discipline twin of the gate-design lesson family: the instrument you verify WITH must not touch the thing you verify. A verification that mutates its artifact destroys its own evidence — and the only reason this one was survivable is that origin held the truth.

## 🟢 MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "sn": "SN-01632",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-18",
  "applies_when": [
    ["verify", "scoring"],
    ["artifact", "lane-built"],
    ["instrument", "build-or-merge-script"],
    ["discipline", "read-only"]
  ],
  "enforcement": "The pre/post artifact-SHA byte-identity check is the standing enforcement: every verification run that touches a lane's working tree snapshots the SHAs of every file the lane's scripts could write BEFORE verification and verifies byte-identical AFTER. Any drift voids the run and names the clobber — the run is re-done from the restored artifact, and the execution is recorded as a named failure (clobber-during-verification). The lane-scorer brief template carries the named bar: 'read-only verification — no build/merge script execution.' The check that caught THIS incident — restore-from-origin byte-identical verification — remains the recovery standard.",
  "decision_change": "The verification question 'is this artifact deterministic/correct?' changes from 'run its builder and see' to 'read it twice with read-only tooling, hash it, diff it against origin.' Build/merge scripts are never executed during verification — not as checks, not as determinism probes, not 'just once.' If a script's output must be re-derived, it runs against a scratch copy in /tmp, never against the live artifact.",
  "falsifiability": "Run the pre/post SHA check around any verification: drift after a run that executed no build scripts falsifies the 'read-only is sufficient' claim for that case and reopens the boundary. The named exception that tests the rule: a script with a proven no-op/dry-run mode (verified by reading its code, not its claims) may run in that mode — if it ever writes in dry-run mode, the exception is revoked and the script is barred from all verification runs.",
  "mechanism": "Build/merge scripts write by design — writing is their contract. Executing one under the guise of 'checking' converts a read operation into a write operation at the filesystem level; the artifact under verification is replaced by a recomputed version (here: stale-era 457-record bytes over the live 478-record converged truth). A verification that mutates its subject destroys the evidence it claims to check, and every downstream verdict built on those bytes is void. Recovery is only possible because an independent source of truth (origin branch) survived — a write with no clean upstream is unrecoverable, which is why the discipline is preventive, not remedial."
}
~~~

## 🧾 PROOF / PROVENANCE

~~~json
{
  "event": "2026-10-18 ~06:05 PDT, lane-scorer tick (memory/2026-10-18.md)",
  "instrument": "hidden_files/t0907-merge-catalog.py executed as a 'determinism check'",
  "damage": "rewrote block-catalog.json + index-by-use-case.json mid-verification (the script's designed function)",
  "recovery": "restored 478-record converged version from origin naya4/hubdrive-block-catalog, sha 823be4bd6406cf1922e5, byte-identical before/after",
  "note": "t0907's receipt-era 457-record bytes superseded by converged 478 — clobber wrote stale-era content over live truth",
  "same_tick_hygiene": "scores-file final line lacked trailing newline; append glued two JSON objects (line 3975 failed parse) — split and re-validated, 3986 lines all parse",
  "standing_rule": "never execute a lane's build/merge script during scoring verification — read-only copies only (scorer's own receipt)"
}
~~~

## 🟨 HOW TO APPLY / HOW TO USE

1. Verifying an artifact: read it, hash it, diff it against origin. Never execute its builder.
2. If you must re-derive a script's output: run it against a scratch copy in `/tmp`, never against the live artifact.
3. Before and after every verification run over a lane's tree: snapshot artifact SHAs; verify byte-identical after; any drift = named clobber, run void.
4. Writing or reviewing a lane-scorer/verifier brief: include the named bar "read-only verification — no build/merge script execution."
5. The only exception: a script whose no-op/dry-run mode is proven by reading its code (not its docs); one write in dry-run mode revokes the exception forever.

## ⚠️ TRUTH BOUNDARY / UNCERTAINTY

The incident and recovery are byte-proven (restore sha `823be4bd6406cf1922e5`, identical before/after). The standing bar is the scorer's own stated rule; the pre/post SHA check is the proposed standing enforcement, named here for the first time — it becomes load-bearing only once the lane-scorer brief template actually carries it (dispatcher territory). The dry-run exception is a deliberate boundary, not a loophole: proven by code reading, revocable on first write.
