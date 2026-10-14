# Reproduce the Gate With the Gate's Own Code, in the Gate's Own Context

**Intelligent Block:** IB-SMART-NOTE-20261013-sn1263-reproduce-the-gate-in-its-own-context
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-13
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** lesson-broadcast.md [t0719] entry (Dispatcher mirror, t0712-lane3 #2566 independent scorecard, 9.0/10, 2026-10-13) — the receipt-gate run outside a git repo reported "7 dead handles"; inside the repo it was 4 real ones. A checker in the wrong cwd produces confident, exact-looking, wrong verdicts. Sanity-check every reproduced failure against one known-true fact before believing the reproduction.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The #2566 independent scorecard nearly certified a false defect count: the receipt gate, run from outside a git repo, reported **7 dead handles**; the same gate, run inside the repo, reported **4 real ones**. The reproduction was confident, exact-looking, and wrong — because the checker was measuring the wrong world. Two rules fall out: **reproduce the gate with the gate's own code, in the gate's own context** (the repo the gate reads, the cwd it expects), and **sanity-check every reproduced failure against one known-true fact** before believing the reproduction. The bytes included the verifier's own instrument — live-bytes discipline applies to the tool, not just the target.

Why this is brain-grade: independent verification is the system's trust anchor, and a mis-contextualized checker is a trusted liar. The failure mode is insidious precisely because the output looks rigorous — numbered handles, exact paths — while the ground beneath it is a different filesystem. "The gate said so" is only as good as "the gate ran where it lives."

## 🩷 HUMAN NOTE

Shawn — the scorecard on #2566 nearly reported seven broken evidence handles instead of four. The checker was fine; it was just run from the wrong directory, outside the repo it was built to read — so it measured a different world and answered confidently about it. The lesson is now discipline: run every gate where the gate lives, and before trusting a reproduced failure, check it against one thing you already know is true. Verification has to verify its own feet are on the ground.

## 🟣 CHILD NOTE

Imagine a detective dusting a photocopy of a crime scene for fingerprints — they'd find nothing and declare "no fingerprints!" But the real scene, with real fingerprints, is across town. The detective's kit was fine; they just used it on the wrong copy. The new rule: always dust the real scene, and before you believe what the kit says, test it on one fingerprint you already know is there.

## 👵 GRANDMA NOTE

A thermometer is only honest in the room you're measuring. The lane ran a perfectly good checker in the wrong directory — like taking the oven's temperature while standing in the hallway — and got a confident, exact, wrong number. The fix is old-fashioned: do the measuring where the thing lives, and before you trust a surprising reading, check the instrument against something you already know.

## 🧠 NAYA NOTE

Note to future me: when I reproduce a gate's verdict, the reproduction inherits the gate's context requirements — repo root, git metadata, working-tree paths. A run outside that context isn't a reproduction, it's a different experiment wearing the same name. My checklist before reporting a reproduced failure: (1) am I in the directory this checker was built to read? (2) does at least one known-true fact survive the reproduction (a handle I know is live still reads live)? If either fails, the verdict is about my setup, not the code.

## ⚙️ MACHINE NOTE

{"sn": "SN-1263", "title": "Reproduce the Gate With the Gate's Own Code, in the Gate's Own Context", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-13", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "ENGINEERING-PROOF", "VERIFY-COVERAGE"], "cousins": ["SN-1256", "SN-1160"], "evidence": {"finding": "t0712-lane3 #2566 independent scorecard (2026-10-13, lesson-broadcast.md [t0719], dispatcher mirror 9.0/10): receipt-gate run outside a git repo reported 7 dead handles; inside the repo, 4 real ones. Lesson: a checker in the wrong cwd produces confident, exact-looking, wrong verdicts; sanity-check every reproduced failure against one known-true fact before believing the reproduction"}, "decision_change": "verification seats run every gate reproduction inside the gate's own repo context and anchor each reproduced failure against one known-true fact before reporting it as a defect", "falsifier": "an out-of-context reproduction proven right while the in-context run is proven wrong on the same input - then context is not the mechanism", "mechanism": "checkers read repo state (git metadata, working-tree paths); outside the repo they measure a different filesystem world, so the verdict is exact about the wrong world", "rule": "reproduce the gate with the gate's own code, in the gate's own context; sanity-check every reproduced failure against one known-true fact"}
