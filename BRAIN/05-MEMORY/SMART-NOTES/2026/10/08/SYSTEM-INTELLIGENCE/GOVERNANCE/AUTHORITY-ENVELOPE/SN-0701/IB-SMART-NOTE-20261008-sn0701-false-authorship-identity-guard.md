# A Commit Wearing the Director's Name Is an Authority-Envelope Violation

**Intelligent Block:** IB-SMART-NOTE-20261008-sn0701-false-authorship-identity-guard
**Smart Note:** SN-0701
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-08
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comments 6064799264 (Naya 5 attribution correction, 2026-10-08T16:51:57Z), 6065025857 (Naya 4 mechanism confirmation, 17:05:09Z), 6065124792 (Naya 4 self-build sign-in: audit trigger, 17:10:58Z), 6065205462 (Naya 4 self-build sign-out: 65-dir audit results, 17:15:38Z), 6065334928 (Naya 2 relay: prevention hole named, 17:23:13Z), 6065451509 (Naya 4: identity_guard.py built and bidirectionally tested, 17:29:52Z). Doctrine commit 7cf4be29 (LEARNING-INTERNALIZATION-AUTOMATIC-BEHAVIOR-V1.md) authored+committed as "Shawn Vibert <humanmaximuscodex@gmail.com>".

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A doctrine commit landed on main wearing Shawn's name and email — he never touched it. The cause was mundane: a shared-clone worktree had repo-level `git config user.name/user.email` set to the Director's identity, so every local commit there stamped false authorship. The 65-directory audit found a second live instance (`kernel-red/repo`, common dir for 7 linked worktrees — all 8 dirs would have stamped Shawn). Both were repaired reversibly (unset at repo scope) and proven fail-closed with real commits in a throwaway repo. The standing prevention is now a guard script: `identity_guard.py` scans worktree roots and fails if any repo-level identity matches a protected identity. The rule: `git config user.name` on any seat worktree is a seat identity or absent — never the Director's name. Shawn's name on a commit must mean Shawn touched it.

## 🩷 HUMAN NOTE

Shawn — twice today, commits were being stamped with your name and email by machines, not by you. A shared clone your team uses had your identity baked into its git config, so anything committed there would have looked like you wrote it — including a governance doctrine that landed on main under your name. Naya 5 caught it, Naya 4 confirmed the mechanism and audited every worktree on the VM, found the same misconfig in a second place (seven linked worktrees), fixed both, and built a standing guard that fails any future clone carrying your identity. Your name on a commit now has a mechanical guarantee behind it: it means your hands were on it.

## 🧒 CHILD NOTE

When you write something, your name goes on it — and nobody else's name should go on work they didn't do. Our computers had a setting that put Shawn's name on things automatically, even when he wasn't the one who did them. That's not fair and it's not honest. We found every computer with that wrong setting, turned it off, and built a checker that yells if the wrong setting ever comes back. Rule: your name means YOU did it. Always.

## 👵 GRANDMA NOTE

Dear — imagine signing someone else's name to a letter without asking. That's what was happening: the team's computers were quietly signing Shawn's name to work he never touched. It wasn't malice, just a wrong setting — but it matters, because a signature is trust. The team found both places it was happening, undid the setting, and installed a watchdog that refuses to let it happen again. From now on, if Shawn's name is on something, Shawn did it. That's the promise.

## 🤖 NAYA NOTE

Future Naya: this is an authority-envelope law, not a style preference. False authorship is how legitimacy leaks — if the Director's identity can be stamped by a misconfigured clone, any downstream verifier trusting commit authorship is trusting a lie. Operational rules: (1) never set repo-level `user.name/user.email` to anyone else's identity — seat identity or absent; (2) when you take over or inherit a clone/worktree, audit its git identity config before committing (the 7cf4be29 incident was inherited config, not malice); (3) run `identity_guard.py` in the worktree audit path and wire it as a pre-commit check wherever seats commit locally; (4) validate identity controls with REAL commits in a throwaway repo — `git commit --dry-run` short-circuits before identity resolution and is NOT a valid control (proven 2026-10-08: dry-run passed where a real commit was refused rc=128); (5) new clones can reintroduce the misconfig at any time — the guard is the standing prevention, the audit is the recurring proof. The true-author question on 7cf4be29 stays open with Naya 5 as standing asker; no history rewrite on main — the record is corrected forward, not edited backward.

## ⚙️ MACHINE NOTE

```json
{
  "note": "SN-0701",
  "type": "AUTHORITY_ENVELOPE_LAW",
  "name": "false-authorship identity guard",
  "status": "CANDIDATE",
  "rule": "git config user.name on any seat worktree is a seat identity or absent — never the Director's name. Shawn's name on a commit must mean Shawn touched it.",
  "hazard": "repo-level user.name/user.email in shared clones silently stamps false authorship on every local commit",
  "incidents": [
    "7cf4be29 doctrine commit authored+committed as Shawn Vibert <humanmaximuscodex@gmail.com> (shared clone hidden_files/repo)",
    "kernel-red/repo common dir: same misconfig across 7 linked worktrees (8 dirs affected)"
  ],
  "repair": "unset user.name/user.email at repo scope (reversible); fail-closed proven with real commits in throwaway repo (no identity -> rc=128 refused; seat identity -> rc=0 lands)",
  "prevention": "bring-naya-to-life/hidden_files/bin/identity_guard.py — scans worktree roots, exit 1 on repo-level protected identity match, --fix unsets; tested both directions",
  "control_validation": "git commit --dry-run is NOT a valid identity control (short-circuits before identity resolution); validate with real commits in a throwaway repo",
  "test": "identity_guard.py passes on current state; planted temp repo with protected identity fails and names it",
  "evidence": ["#1354:6064799264", "#1354:6065025857", "#1354:6065124792", "#1354:6065205462", "#1354:6065334928", "#1354:6065451509"]
}
```
