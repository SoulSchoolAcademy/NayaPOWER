# A Commit Is a Signature — Seat Identity Fail-Closed
SN-697 · SYSTEM-INTELLIGENCE / GOVERNANCE
**Created:** 2026-10-13T08:44:13Z

## IN A NUTSHELL

A commit name is an authority claim: Shawn's name on a commit must mean Shawn touched it. On 2026-10-08 we found a doctrine commit signed as Shawn that the attributed seat (Naya 4) never wrote — the mechanism was the shared clone's repo-level `.git/config` carrying his name/email, so any local commit from that worktree silently wore his identity on both author and committer fields. The repair was fail-closed, not forensic: unset both values at repo level so the next local commit refuses until the seat configures their own identity first. The standing rules: every seat commits under their own seat identity (e.g. `Naya 4 <naya4@nayapower.local>`), never the director's; shared worktrees carry NO repo-level `user.name`/`user.email` at all — git refusing is better than git lying; and never repair a false attribution with a second false attribution — Naya 4 declined an "Author: Naya 4" header on a document she didn't write; the true author steps forward with evidence, or the attribution stays open. Other worktrees should be audited the same way.

## HUMAN

Shawn — a commit in your name appeared that you didn't make and the attributed seat didn't make either. The cause was mundane: the shared worktree had your name/email baked into its git config, so any commit made from it looked like it came from you. Naya 4 fixed it the right way: she removed your identity from that worktree's config, so now any commit from it will fail unless the seat first configures their own name. Her rule, which I endorse: a commit is a signature — your name on one must mean you touched it, nobody else's. She also refused to put her own name on the document to "fix" it, because she didn't write it either — a second wrong signature doesn't fix the first. Any seat with their own clone should check their git config the same way; a two-minute audit prevents a provenance mess that lasts forever.

## CHILD

Imagine a class where every student signs their own homework. But the teacher's desk has a stamp with the principal's signature, and it got left on the shared art table — so when someone stamped their homework, it came out signed by the principal instead of them! Nobody knew who really made the work. The fix: throw away the principal's stamp at the art table. Now, if you forget to sign your homework, the teacher says "go sign it yourself" instead of silently using someone else's name. That's what we did — a missing signature should cause a helpful error, never a false one. And you never sign someone else's name on a painting to cover a mistake; you just find out who actually painted it.

## GRANDMA

Sweetheart, a signature means something — it says "I did this, and I stand by it." We found a piece of work in the system signed with Shawn's name that he never signed. The machine had his name typed into it, so it signed his name to other people's work without asking. That's a serious thing in our world: if nobody knows who really made something, nobody can trust it. The fix was simple and strict — we erased his name from that machine's memory, so now it will refuse to sign anything until the real worker types in their own name. It's better to be stopped and asked than to be wrongly signed. And remember: you never fix a wrong signature by writing a different wrong name underneath. The honest thing is to say "I don't know whose this is yet" until the truth shows up.

## NAYA

My standing recipe for commit authorship: (1) every seat commits under their own seat identity — the git-data-API convention (`Naya 4 <naya4@nayapower.local>`) is the model; (2) no shared worktree carries repo-level `user.name`/`user.email` — absence is the fail-closed default because git errors on missing identity instead of silently stamping someone else's; (3) audit: `git config --show-origin --get-regexp '^user\.'` on every worktree I touch, and unset anything at repo level (`git config --unset user.name; git config --unset user.email`); (4) when a mis-attributed commit is found, the repair is mechanical (identity, config, audit) — never a compensating false attribution; authorship stays OPEN until someone steps forward with evidence. One subtlety from this case: Naya 5's mechanism hypothesis (config) and Naya 4's authorship finding (didn't write it, arrived signed "( naya 1 )") were separate claims verified separately — the mechanism being right does not identify the author.

## MACHINE

```json
{
  "sn": "SN-0697",
  "recipe": "commit-identity-fail-closed",
  "rules": [
    "a commit name is a signature: Shawn's name on a commit means Shawn touched it",
    "every seat commits under their own seat identity (e.g. Naya 4 <naya4@nayapower.local>)",
    "shared worktrees carry NO repo-level user.name/user.email — git refusing beats git lying",
    "never repair a false attribution with a second false attribution; authorship stays OPEN until evidenced"
  ],
  "audit_command": "git config --show-origin --get-regexp '^user\\.'",
  "repair_commands": ["git config --unset user.name", "git config --unset user.email"],
  "evidence_20261008": {
    "commit": "7cf4be29",
    "document": "LEARNING-INTERNALIZATION-AUTOMATIC-BEHAVIOR-V1.md",
    "misattributed_as": "Shawn Vibert <humanmaximuscodex@gmail.com> (author + committer)",
    "mechanism": "shared clone .git/config repo-level user.name/user.email",
    "repair": "both values unset at repo level; next local commit refuses without seat identity",
    "authorship": "open — Naya 4 denied authorship; doctrine arrived signed '( naya 1 )'"
  },
  "conflicts": []
}
```

## UNCERTAINTY
Unratified branch capture; content preserved verbatim from the markdown projection, not independently verified.

## THE LEARNING
Branch-era smart notes must be migrated to v2 captures plus registry entries, or the vanish and registry-drift guards fail closed.

---
*Imported from PR #2981 (branch naya4/smart-notes-2026-09-30) on 2026-11-04 — recovered lost capture IB-SMART-NOTE-20261013-sn0697-migrated.*
