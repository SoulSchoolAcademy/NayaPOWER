# Intelligent Block
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-15 ~18:10 PDT (Smart Note distillation tick)
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**SN number:** SN-1438
**Provenance:** shared-state.json `mission_snapshot_note` (2026-10-15 17:38 PDT) — director-pass repair of a live snapshot clobber: "a test-probe PUT briefly overwrote the snapshot with 4 bytes; immediately repaired and byte-verified (6883 B). Root cause: push script restricted ENV and dropped proxy vars (fixed; lesson recorded)."

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## IN A NUTSHELL
A test-probe PUT wrote 4 bytes over the live mission snapshot, and the director pass only caught it because it byte-verified the repair (6883 B). Root cause was a two-layer failure: the probe's write target defaulted to the live snapshot path, and the push script restricted ENV — silently dropping the HTTP(S)_PROXY vars the PUT needed, so it bypassed the egress proxy. Lesson: a script's write path is a loaded gun — never aim a probe at a live path, and never restrict ENV before verifying which variables the network path depends on.

## HUMAN NOTE
On 2026-10-15 at ~17:38 PDT, a test-probe PUT overwrote the live mission snapshot with 4 bytes. The damage was discovered and repaired in the same pass — the snapshot was re-written from known-good bytes and byte-verified at 6883 bytes — but the incident exposed a mechanism worth naming. Two things failed at once: first, the probe's write target defaulted to the live snapshot path (a test script aimed at production state); second, the push script ran with a restricted ENV, which silently dropped the HTTP(S)_PROXY variables the PUT required, sending the request around the egress proxy. Either layer alone might have been harmless; together they clobbered live state. The durable rules: probes write to throwaway paths, never to live ones; and if you restrict ENV, you own an inventory of exactly which variables you kept and which the network path needs.

## CHILD NOTE
Imagine testing a water gun — but instead of aiming at a target, you point it at the fish tank. And the "safety" you added (restricting ENV) quietly removed the plug from the hose. The lesson: when you test something, aim it at a safe target — never at the thing everyone depends on. And before you take away a tool (like the proxy settings), check who needs it first.

## GRANDMA NOTE
Darling, they were testing a small tool and it accidentally scribbled over the one important record everyone reads. They fixed it right away — rewrote it perfectly and checked every byte — but it taught them two house rules: never point a test at the real thing, and never take shortcuts with the settings (like hiding the internet route) without checking what breaks. Test in the sandbox, fix in the light, and always double-check the important papers afterward.

## NAYA NOTE
Operational discipline doctrine, earned 2026-10-15 17:38 PDT: (1) The event: a test-probe PUT briefly overwrote the live mission snapshot with 4 bytes; the director pass repaired it immediately and byte-verified the result at 6883 B. (2) The mechanism — two layers, both real: (a) write-target defaulting: the probe's write path aimed at the live snapshot instead of a throwaway target; (b) ENV restriction: the push script's restricted ENV silently dropped HTTP(S)_PROXY vars, so the PUT bypassed the egress proxy. The clobber needed both — a probe aimed at live state plus a broken transport path. (3) The doctrine: treat every script's write path as a loaded gun — probes target throwaway paths by construction (default must be safe, live must be explicit), and restricting ENV requires an inventory: which vars are kept, which the network path needs, verified before the first run. Root cause fixed at the source; repair byte-verified, not asserted. Evidence: shared-state.json mission_snapshot_note (2026-10-15 17:38 PDT).

## MACHINE NOTE
```json
{
  "sn": "SN-1438",
  "slug": "probe-writes-never-touch-live-snapshot",
  "category": "OPERATIONS",
  "sub": "MEASUREMENT-HYGIENE",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "lesson": "A script's write path is a loaded gun: probes must target throwaway paths by construction (safe default, live explicit), and restricting ENV requires an inventory of which variables the network path needs before the first run.",
  "mechanism": "Two-layer clobber: (a) the probe's write target defaulted to the live mission snapshot path; (b) the push script's restricted ENV silently dropped HTTP(S)_PROXY vars, so the PUT bypassed the egress proxy. The 4-byte overwrite required both; the repair re-wrote the snapshot from known-good bytes and byte-verified 6883 B.",
  "decision_change": "Before any probe or push script runs against live paths: audit its ENV handling (does it preserve HTTP(S)_PROXY and any var the transport needs?) and confirm its write target is a throwaway path, never the live snapshot — by construction, not by memory.",
  "falsifiability": "If the 4-byte overwrite never touched live snapshot bytes (byte-verification disproves this) or the proxy-ENV cause is disproven by reproducing the PUT with full ENV and no clobber, the mechanism is wrong and this note is void.",
  "evidence": ["shared-state.json mission_snapshot_note (2026-10-15 17:38 PDT): 'a test-probe PUT briefly overwrote the snapshot with 4 bytes; immediately repaired and byte-verified (6883 B). Root cause: push script restricted ENV and dropped proxy vars (fixed; lesson recorded)'"],
  "related": ["SN-1368 (presence-checking a gate is theater — byte-verify the repair, not the prose)"]
}
```
