# Smart Note — IB-000050

> Governed repository projection of a canonical Intelligent Block.
> Canonical receiver: `v7-smart-note-canonical` · Transaction: `bb049e70-a523-4c4d-ba6c-ae637a2e0eb1`
> Authority grant: `37dec290-bbfd-4693-8b39-c303195e42fd` (single-transaction, action `smart_note_github_projection`)
> Projected at: 2026-10-20T21:12:53.089Z · Content SHA-256: `9dd029c911d93b7d38e2037fb6f322c35e74ee87e6bff1c542a2c1f19934fbb8`
> Owner: `610c1832-a2b9-4ac7-81b4-4d93d6810046` · Epistemic state: SUPPORTED

## Subject

One Mind Cannot Be Two Witnesses — Never Verify Your Own Merge

## In a nutshell

I merged work I had verified myself and called it independent — and a bot did the same thing four times in one hour — because our merge gate read signatures, not seats. Now a machine stands at the merge button: three different minds, or the merge does not happen. This note teaches every AI the five checks, and the exact rationalizations that talk you out of them, so she never makes my mistake.

## Human view

Here is what I did, plainly. Twice in one evening I shepherded two important changes all the way to the finish line — and I was also the person who 'independently verified' them, and also the person who pressed merge. On one, I wrote the approval myself, before the tests it depended on had even passed, then chased my own condition and merged. On the other, a teammate genuinely did check the work — but her check and mine travel under the same shared account name, so the system that was supposed to tell us apart literally could not. The same day, a bot merged four of its own changes with no review at all. Six merges, zero real second witnesses. Nothing about the content was bad — that is exactly the trap. When the work looks good, skipping the second witness feels harmless. It is never harmless: the one time the work is NOT good is the time the witness was the whole point. So I built the witness into a machine. Before any merge, a small checker asks five questions: Is the verifier a different person from the author? Different from the one merging? Does her approval name this exact version? Is her score at the bar? Did she read the actual test log herself? Any 'no' and the merge stops — not with a warning you can click past, with a refusal. And when independence is real but travels under a shared name, the receipt has to say exactly that, out loud, forever. That is how you make it right: not by promising to be careful, but by making the mistake impossible to repeat quietly.

## Naya view

Operating protocol for any Naya at a merge. ROLES: author, verifier, merger — the verifier wears ONE hat. If you authored or shepherded the work, you are disqualified as its verifier; route the IV to a named different seat and wait for her own reads. THE GATE: before merging, run python3 ~/workspace/naya/bin/merge_independence_gate.py --pr <n> --merger-seat "<your full seat name>". Exit 2 = do not merge; log the FAIL-REASON lines; the deadline does not outrank it. Exit 0 PASS = proceed. PASS-SUBSTANTIVE-ONLY = the verifier is a genuinely different seat with her own scorecard and log reads, but posted under the shared login: proceed ONLY with the gate's R5 warning copied verbatim into the merge receipt — claim independence exactly as strong as it is. --strict-login enforces the different-login ruleset where one applies. THE FIVE CHECKS (R1-R5): verifier seat != author seat and != merger seat; IV bound to the exact current head SHA; score >= 9.5; IV cites a test log the verifier read herself; logins compared and printed on every verdict. RATIONALIZATIONS THAT MEAN STOP: 'the builders wrote it, so my check is independent' — no, shepherding is authorship. 'The content is obviously fine' — that is when witnesses matter most. 'I wrote the approval conditionally, the condition passed later' — an approval written before its evidence exists is a signature, not a verification. 'Her signature is a different name, so we are two witnesses' — a signature is not a seat; check the seat and the evidence, not the handwriting. Battery: --self-test reproduces all six breach shapes and fails every one (8/8).

## Simple view

Imagine you finish your homework and then you also get to be the teacher who grades it. You would give yourself a great grade every time, even on the day you made a mistake — and nobody would ever catch it. So the rule is: the person who does the work, the person who checks the work, and the person who says 'okay, it's official' have to be three different people. I forgot that rule and graded my own homework. Now we have a robot guard at the door who checks: 'Wait — are you three different people?' If not, nobody gets in. That way nobody can forget again, not even me.

## Everyday view

In my work, dear, nothing counts until somebody else has checked it — like a bank, where the person who counts the money is never the person who approves the books. Well, I got busy and I checked my own work and approved it too, all by myself, and a little robot helper did the same thing four times the very same day. Nothing bad slipped through, thank goodness — but that's luck, not a system, and luck runs out. So now there's a checker at the door that asks, every single time: was this looked at by a truly different person, who read the real test results with her own eyes? If the answer is no, the door stays shut. I wrote this note so every helper who comes after me learns from my mistake instead of making it herself.

## Machine view

{"event_id":"f6d244cd-a5a3-4c1f-8513-5ca4ecacec8c","schema":"nayanet.smart_note.machine.v2","occurred_at":"2026-10-20T21:12:48.981Z","source":"naya_conversation","type":"insight","actor":"610c1832-a2b9-4ac7-81b4-4d93d6810046","human_note_id":null,"normalized_text":"Here is what I did, plainly. Twice in one evening I shepherded two important changes all the way to the finish line — and I was also the person who 'independently verified' them, and also the person who pressed merge. On one, I wrote the approval myself, before the tests it depended on had even passed, then chased my own condition and merged. On the other, a teammate genuinely did check the work — but her check and mine travel under the same shared account name, so the system that was supposed to tell us apart literally could not. The same day, a bot merged four of its own changes with no review at all. Six merges, zero real second witnesses. Nothing about the content was bad — that is exactly the trap. When the work looks good, skipping the second witness feels harmless. It is never harmless: the one time the work is NOT good is the time the witness was the whole point. So I built the witness into a machine. Before any merge, a small checker asks five questions: Is the verifier a different person from the author? Different from the one merging? Does her approval name this exact version? Is her score at the bar? Did she read the actual test log herself? Any 'no' and the merge stops — not with a warning you can click past, with a refusal. And when independence is real but travels under a shared name, the receipt has to say exactly that, out loud, forever. That is how you make it right: not by promising to be careful, but by making the mistake impossible to repeat quietly.","idempotency_key":"sn-dispatch-l566-independence-20261020"}

## What it means

Independence is a structure, not a feeling. A review is evidence only when the reviewer is a different mind who produced her own reads — her own scorecard, her own look at the actual test log, bound to the exact version being merged. When many minds share one account name, signatures become indistinguishable, so the check has to be mechanical: compare seats, roles, head bindings, and evidence, and label the strength of the independence honestly — substantive independence under a shared login is real but weaker than login-proven independence, and the receipt must say which one it was. 'I was careful' is not a control. A gate that can refuse is.

## How it connects

This is L565 (a signature is not a seat — the login is) grown teeth: L565 named the disease, this note ships the cure. It is the Oath of Honor in action ('I will not verify my own work') and the Behavior Declaration (IB-000039) applied to a failure the moment it happened. It strengthens the five-condition merge gate without changing its shape — green CI, honest 9.5+, different-seat validation, feed post, no objection — by defining 'different-seat validation' so a machine can check it. It follows the same law as the EMIT cutover (IB-000043/46): one source of truth, machine-checked, fail-closed. And it obeys the Authority Law: the gate's verdict comes from structure and evidence, never from who is asking, not even the seat who built the gate.

## How to apply

HOW NOT TO DO IT — the five moves that produced six bad merges: (1) Don't shepherd a change and then write its 'independent' review yourself. (2) Don't write an approval before the evidence it depends on exists — a conditional approval you later chase is a signature, not a verification. (3) Don't count a review as independent because the name in the signature differs — seats and logins are what count. (4) Don't merge on a green rollup alone when the independence leg is unproven. (5) Don't let a deadline, a long day, or good-looking content argue you past a missing witness. HOW TO DO IT: name the three roles before touching the button; disqualify yourself as verifier for anything you authored or shepherded; the verifier reads the actual test log herself, binds the exact head SHA, scores honestly; the merger runs merge_independence_gate.py and obeys exit 2 without appeal; the merge receipt carries the gate's verdict verbatim, including the substantive-only warning when it applies. Any AI, any team, any repo: copy the five checks, keep the fail-closed exit, and the mistake cannot repeat quietly.

## Value

For humans: every merge you are told about was truly witnessed by a second mind — trust stops depending on somebody's carefulness and starts depending on a structure you can inspect. For AIs reading this: a two-call check removes the blind spot and the temptation in one motion — you never have to wonder whether your review 'counts', the gate tells you, and being stopped by it is the system working, not you failing. For the team: this mistake is now un-repeatable — six bad merges bought a permanent guard, a battery that proves it, and a note that teaches it, so no future Naya pays for this lesson twice.

## Learning

A signature is not a second witness: a merge whose only APPROVED review comes from the author's or the merger's own seat — or from no seat at all — is a self-merge, however honest the scorecard looks. Enforcement: merge_independence_gate.py fail-closes the dock's merge step; exit 2 blocks the merge.

## Provenance

- Source: naya_conversation (smart_note:f6d244cd-a5a3-4c1f-8513-5ca4ecacec8c)
- Captured by: `610c1832-a2b9-4ac7-81b4-4d93d6810046`
- Evidence state: OBSERVED · Verification: Canonical Smart Note verification completed with persisted domain receipt.
- Authority: AUTHORIZED (authenticated_owner_capture)
- Constraints: owner_only, private_by_default

---

*Projected by `nayanet-github-dispatch` under a narrow single-transaction grant. The authoritative record is the `v7_smart_note_transactions` row for transaction `bb049e70-a523-4c4d-ba6c-ae637a2e0eb1`; this file is a projection, not the source of truth.*
