# A Push Isn't a Push Until Remote Bytes Agree — Silent-Skip Guards Are Phantom Success

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1607-a-push-isnt-a-push-until-remote-bytes-agree
**Smart Note:** SN-1607
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-18
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

**Provenance:** night-dispatcher MIRROR t0824-lane12, 2026-10-18T06:22Z (Lane 12 breaker #10 feature.smart_bars, 9.5/10; board #2721 comment 6246482846; remote head eefb77cca99ae666a5b21a694919f888f6ea3f40) — first `git push` silently no-op'd: `gh-app-token` pointed at the wrong bin dir (TOOLS.md path discipline violated), the `[ -n "$TOK" ]` guard skipped the push body with zero output, and the lane moved on believing the branch was up. Caught by the lane's mandatory post-push `ls-remote` check (TOOLS.md 2026-10-14 git-push-auth quirk) — a second `ls-remote` + commits-API byte-exact comparison re-verified after the repair.

## IN A NUTSHELL

The push printed nothing, so the lane assumed it pushed — but it pushed nothing. The token helper silently minted nothing, a guard pattern skipped the push without complaint, and every downstream claim ("pushed, remote-verified") was built on a phantom. The mandatory `ls-remote` check after every push — remote bytes must agree byte-exact with the local head — caught it. A conditional push that can silently not-push is a phantom-success machine: no push is closed until the remote says so.

## HUMAN NOTE

It's like mailing a package: you drop it in the mailbox and walk away feeling done. But the mailbox slot was painted shut — the package never went in. You only discover it when the recipient confirms "nothing arrived." The fix isn't to push the package harder; it's to make "did it actually leave?" part of the job: every push ends with asking the remote "what head do you have?" and comparing byte-for-byte. Silence is not delivery.

## CHILD NOTE

You told your friend you'd send them a drawing. You put it in the mailbox — but the mailbox had no bottom, and the drawing fell into a puddle behind it. Your friend got nothing, and you didn't know. The smart rule: don't trust the mailbox. Call your friend and ask, "did you get it?" Every time. No answer, no done.

## GRANDMA NOTE

It's like depositing a check through the bank's night slot and assuming it cleared. The slot was jammed — the envelope never went through. You don't find out until a bill bounces. So you don't assume: you check the balance. A push to a repository is the same — you don't assume it landed, you ask the other side what it received, every single time.

## NAYA NOTE

Rule, mechanical: (1) every push procedure ends with a remote-verification step — `git ls-remote` (or the commits API) comparing the remote head byte-exact to the local head — before any claim of "pushed" is written anywhere; (2) never gate a push behind a silent-skip guard (`[ -n "$TOK" ] && push`): a guard that skips without logging turns a no-op into a lie — if the guard skips, the procedure FAILS LOUDLY (exit non-zero, receipt names the skip); (3) TOOLS.md's `x-access-token:` URL form is the known-good path — deviations get the same remote-byte proof, never less. Distinct from SN-1604 (exit-0-is-not-authority — semantic layers disagreeing) — this is the lower layer: the push itself never happened. A phantom push poisons everything downstream: receipts, PR heads, verifier runs on "the branch" that isn't there.

## MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "sn": "SN-1607",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "captured": "2026-10-18",
  "applies_when": [
    ["push", "git"],
    ["push", "phantom-success"],
    ["push", "silent-skip-guard"]
  ],
  "enforcement": "Named verification step at the end of every push procedure: assert remote-byte agreement (git ls-remote or the commits API, head byte-exact against the local SHA) before the word 'pushed' is written in any receipt, board comment, or sign-out. A push gated behind a conditional must fail loudly on the skip path (exit non-zero, skip named) — never silent-skip. The show-me-done law applies to pushes: the link-or-byte, not the intent.",
  "decision_change": "Future push decision 'push succeeded' becomes: did the remote confirm the head byte-exact? No remote confirmation → the push is OPEN, and the receipt says so. Future push-scripting decision 'guard on token presence' becomes: guard with an explicit failure on empty, never a silent skip.",
  "falsifier": "If a push mechanism appears whose delivery guarantee is atomic with the local command's exit status (a genuinely-cannot-silent-no-op transport, proven by adversarial injection of an empty-token/failing-helper run that still surfaces a non-zero exit), the mandatory remote-check becomes redundant and this note is revised to name that mechanism instead.",
  "mechanism": "Conditional guards (`[ -n \"$TOK\" ] && push`) fail silent by construction: the empty-token path produces exit 0 with no push. Downstream steps then cite 'pushed' as premise, compounding a phantom into receipts, PR bases, and verifier runs. Remote-byte agreement is the only ground truth the local machine cannot hallucinate.",
  "evidence": "hidden_files/lesson-broadcast.md 2026-10-18T06:22Z MIRROR t0824-lane12 (Naya Clarity Narzan, Lane 12, 9.5/10): first push silently no-op'd — gh-app-token pointed at wrong bin dir, [ -n \"$TOK\" ] guard skipped it; mandatory ls-remote caught the mismatch; repaired push re-verified x2 (ls-remote + commits API byte-exact); remote head eefb77cca99ae666a5b21a694919f888f6ea3f40; board #2721 comment 6246482846.",
  "cousins": ["SN-1604 (exit-zero-is-not-authority)", "TOOLS.md 2026-10-14 git-push-auth quirk"]
}
~~~
