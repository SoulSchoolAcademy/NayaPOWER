# Dry-Run Is Not the Control — A Fail-Closed Test Must Exercise the Failure Path

**Intelligent Block:** IB-SMART-NOTE-20261008-sn0708-dry-run-is-not-the-control
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-08
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Filed by:** distillation loop, #1354 6065205462 (2026-10-08).
**Provenance:** #1354 6065205462 ([NAYA 4] Self-build loop cycle — SIGN-OUT, worktree identity audit, 2026-10-08T17:15:38Z). The cycle repaired a repo-level `user.name=Shawn Vibert` / `user.email=humanmaximuscodex@gmail.com` misconfig on the `~/workspace/kernel-red/repo` common dir (8 dirs, 7 linked worktrees stamping the Director as author on any local commit), then proved the fix fail-closed: real commits in a throwaway /tmp scratch repo — no identity → rc=128 "Author identity unknown" (REFUSED); seat identity set → rc=0 commit lands. Explicitly noted: "`git commit --dry-run` short-circuits before identity resolution — it is NOT a valid identity control." Standing guard: `bring-naya-to-life/hidden_files/bin/identity_guard.py` (scan → exit 1 on protected identity, `--fix` unsets reversibly; both-direction tested, 41 repos PASS). Cousins: SN-0429 (verify with the instrument CI uses), SN-0341 (the instrument lies), SN-0658 (use is not definition).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

When Naya 4's identity audit proved the misconfig repair fail-closed, one possible test path — `git commit --dry-run` — was rejected as invalid: dry-run short-circuits before identity resolution, so it can never exercise the identity control. **A test that bypasses the control's code path is not evidence of the control.** The proof that counted was the real failure path: actual commits in a throwaway repo, one with no identity (refused, rc=128) and one with a seat identity (lands, rc=0). The standing rule: for every fail-closed gate, the verification must go through the exact mechanism that would refuse — shortcuts that skip it (dry-run flags, mock paths, cached results) produce confidence without evidence. **Test the refusal, not the rehearsal.**

## 🩷 HUMAN NOTE

Shawn — small but sharp lesson from the identity audit: when a seat proved the fix actually refuses bad commits, she caught that `git commit --dry-run` would have been a fake proof — it quits before the identity check even runs, so it can never show the refusal working. She did the real thing instead: made actual commits in a throwaway repo, watched one get refused and one land. The rule for everyone now: to prove something fails closed, you have to walk the real failure path — no shortcuts. Rehearsals don't prove locks.

## 🟣 CHILD NOTE

Imagine testing whether a door is locked. You could just *pretend* to push it (a dry run) — but if you stop before your hand touches the door, you've learned nothing. You have to actually push. When we fixed the computer mix-up that was stamping your name on other people's work, we could have done the pretend-push. Instead we really tried to commit with no name — the computer said "no" — and then with a proper name — it said "yes." That's how you know the lock works: you pushed the door, both ways.

## 👵 GRANDMA NOTE

Dear, this one is simple: to know a lock works, you must actually try the door. Pretending to try — turning the handle halfway, testing it in a dream — tells you nothing. When the team fixed that mix-up that was putting Shawn's name on work he never touched, they didn't settle for the pretend test. They made a real try with no name (refused!) and a real try with the right name (allowed!). Both directions, for real. That's the only kind of test you can trust: the one that actually walks the path it claims to check.

## 🟢 NAYA NOTE

Apply this to every fail-closed control I verify: enumerate the exact code path the control takes to refuse, and verify the test reaches it — a test that short-circuits before the control is vacuous by construction. The `identity_guard.py` standing guard was tested both directions (41 repos PASS clean; planted violation FAIL correctly, exit 1, violator named). When writing or reviewing a verification, ask: "does this test ever reach the refusal point?" If the honest answer is no — dry-run flags, mocks that skip resolution, caches that pre-answer — the test proves nothing and must be replaced with the real path (or the honest admission that the control is unverified). A shortcut that can never fail is a rehearsal, not a proof.

## 🤖 MACHINE NOTE

```json
{
  "sn": "SN-0708",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-08",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "law": "a test that bypasses the control's code path is not evidence of the control — test the refusal, not the rehearsal",
  "mechanism": "git commit --dry-run short-circuits before identity resolution; cannot exercise the identity fail-closed control",
  "valid_proof": "real commits in throwaway repo: no identity -> rc=128 REFUSED; seat identity -> rc=0 lands",
  "standing_guard": "bring-naya-to-life/hidden_files/bin/identity_guard.py (exit 1 on protected identity, --fix reversibly unsets; both-direction tested)",
  "test_design_rule": "for every fail-closed gate, the verification must reach the exact mechanism that refuses",
  "family": ["SN-0341 instrument lies", "SN-0429 verify with the instrument CI uses", "SN-0658 use is not definition"]
}
```
