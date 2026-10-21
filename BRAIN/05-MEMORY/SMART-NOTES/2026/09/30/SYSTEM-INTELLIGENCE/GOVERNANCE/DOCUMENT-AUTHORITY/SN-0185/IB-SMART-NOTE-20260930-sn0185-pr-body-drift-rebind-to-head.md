# A PR Body Is a Decaying Document — Rebind It to the Head at Every Material Change

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0185-pr-body-drift-rebind-to-head
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-02
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #554 comment 5952925388 (SoulSchoolAcademy, 2026-10-02T13:00:38Z) — brain-build loop rebasing canonical repair PR #1312 onto main tip `d6278ee0`: the PR body described `21->25` on base `ae2fd838` while the head carried `21->26` on base `25268675`; "body described 21->25/base `ae2fd838`; head carried 21->26/base `25268675`" — the body had "drifted five ways from its own head". Remedy taken: title + body rewritten to current truth, byte-verified on the new head (`84525e77`), `--check` OK and 546/3/0 on exact bytes.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A PR description is a state document with a decay window, not a log entry. Every material mutation — rebase, base-tip move, repair-class change, count-ledger bump — rewrites the head's meaning while leaving the body frozen at the moment it was last written. PR #1312's body told reviewers "21->25 on ae2fd838" while the actual bytes said "21->26 on 25268675": a reviewer reading the body alone would evaluate a change that no longer exists. The drift is silent: nothing marks a body stale, and no CI fails on a stale body. The durable rule: the body's claims (base pin, counts, test results, repair class, supersession list) are bound to the head SHA they describe, and every material change must re-derive them from the new head — title, counts, base pin, verification numbers, all of it, in the same motion as the mutation. The lane's own repair discipline already says to verify exact bytes (SN-100, verdict-SHA-binding); this extends the binding to the *description*: if the head moved, the description is a different document until it is rewritten. Practical discipline: (1) never rebase-and-push without re-reading your own body; (2) PR bodies carry an implicit "as of head X" stamp — write it explicitly; (3) a body describing a superseded head is a stale document — treat it with the same suspicion as a stale SHA in a verification claim (SN-057/100 family).

## 🩷 HUMAN NOTE

Shawn — a small but sharp lesson from the brain-build loop today: PR #1312's description said "21->25 on old base" while the actual code was "21->26 on new base." The description had drifted five ways from its own code, and nothing flags that. The rule going forward: every time a PR is rebased or its base moves, the description must be rewritten from the new code — the write-up expires the moment the code changes.

## 🟣 CHILD NOTE

Imagine a label on a jar that says "cookies" but someone replaced the cookies with marbles — and nobody updated the label. Everyone reaching for cookies gets marbles. The new rule: every time you change what's in the jar, rewrite the label. Labels expire when jars change.

## 👵 GRANDMA NOTE

You know how a map from last year won't get you to the new grocery store? Same with those little write-ups attached to the code changes — once the code moves, the old write-up is an old map. We now rewrite the note every time the code changes, so nobody follows an old map.

## 🤖 NAYA NOTE

PR bodies are unversioned, un-checked state documents — treat them as SN-057/SN-100-class hazards. Before reviewing or relaying a PR's claims, re-derive them from the live head SHA; never quote a body as current without checking it against the head. When mutating a PR (rebase, count bump, base move), rewriting title+body is part of the mutation, not an optional follow-up. A body-vs-head diff that shows drift is itself review evidence — cite it like any other diff.

## ⚙️ MACHINE NOTE

{"sn": "SN-0185", "title": "A PR Body Is a Decaying Document — Rebind It to the Head at Every Material Change", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-02", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "GOVERNANCE", "DOCUMENT-AUTHORITY"], "extends": ["SN-043", "SN-057", "SN-100"], "evidence": {"comment": "5952925388", "at": "2026-10-02T13:00:38Z", "pr": 1312, "body_claimed": {"counts": "21->25", "base": "ae2fd838"}, "head_carried": {"counts": "21->26", "base": "25268675"}, "remedy": {"rebased_to": "d6278ee0", "new_head": "84525e77", "body_rewritten": true, "check": "OK", "pytest": "546/3/0"}}, "rule": "PR body claims are bound to the head SHA they describe; every material mutation must re-derive the body from the new head in the same motion; stamp bodies 'as of head X'"}