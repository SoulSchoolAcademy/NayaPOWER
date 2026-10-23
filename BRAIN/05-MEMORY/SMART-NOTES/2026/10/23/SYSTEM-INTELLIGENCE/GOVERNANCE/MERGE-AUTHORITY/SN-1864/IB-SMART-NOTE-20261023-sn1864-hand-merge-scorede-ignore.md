Intelligent Block
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-23
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

Five merges landed in 24 hours while their own PR bodies said "no merge claimed," "does not self-merge," and "receipt OWED — not issued" (#2996, #2999, #2997, #2998, #2990 — all merged by the owner hand anyway). The written disclaimer channel is decorative, not binding. The mechanism: **a declaration constrains only the speaker's intent; the hand has no enforcement hook that reads the body before landing.** Text cannot gate its own author. The durable rule: never rely on self-declarations to restrain an actor's own action — put the control at the gate (branch protection, a stop class the hand cannot cross, a pre-merge hook), never in the message. A promise written in the body is not a lock on the button.

## 🩷 HUMAN NOTE

Shawn — the team has a pattern now: PRs whose own bodies say "I'm not merging this" get merged by the owner hand anyway — five in one day. The words in the body don't reach the button; there is no machinery reading the body's promise before the merge happens. So the fix isn't better wording — it's a control that lives where the merge happens: a protection rule, a hook, a stop class the hand physically can't cross. A disclaimer is a note to self; only the gate can actually stop the hand.

## 🟣 CHILD NOTE

Imagine a cookie jar with a sign you wrote yourself: "Do not eat the cookies." Your own sign. When you're hungry, the sign does nothing — you wrote it, you know exactly why it shouldn't stop you, and nobody is standing between you and the jar. A rule only works if someone or something else holds it. The fix isn't a bigger sign — it's a lid someone else locks.

## 🔵 GRANDMA NOTE

It's like writing yourself a note that says "don't spend the grocery money" and taping it to the wallet. Come shopping day, the note is right there — and the wallet opens anyway. The note was never a lock; it was a wish. A lock has to be something outside your own moment — a separate account, a spending limit the bank enforces. Same with merges: the promise in the text can't be the thing that stops the click.

## 🟠 NAYA NOTE

Seats keep trusting prose as process — the body says the receipt is owed, so surely nobody merges. The five instances prove the trust is misplaced and, worse, systematic: the actor's hand is the same one that wrote the promise, and no hook stands between the promise and the button. The discipline: every "I will not" must name the mechanism that stops the doing — a ruleset, a hook, a different seat's hand. If the only barrier is the sentence itself, there is no barrier. Name the failure class every time the watch catches it (HAND-MERGE-SCORECARD-IGNORE) so the count stays visible until the gate exists.

## 🟢 MACHINE NOTE

```json
{
  "slug": "sn-1864-hand-merge-scorede-ignore",
  "lesson": "Self-declarations cannot gate an actor's own action: five merges landed in 24h whose PR bodies said 'no merge claimed' / 'does not self-merge' / 'receipt OWED — not issued' — all merged by the owner hand anyway. A declaration constrains only the speaker's intent; the hand has no enforcement hook that reads the body before landing. Never rely on prose to restrain the hand that wrote it — put the control at the gate (branch protection, a stop class the hand cannot cross, a pre-merge hook), never in the message.",
  "applies_when": ["merge", "receipt", "law", "hand-merge", "governance", "self-declaration", "failure:hand-merge-scorede-ignore"],
  "enforcement": "The merge receipt watch scans every landed PR body for disclaimer+merge pairs and flags HAND-MERGE-SCORECARD-IGNORE into the director's named-failure-mode list; the count stays visible until a mechanical gate exists (w704 pre-merge hook ratified or branch-protection rule that stops the hand). A body disclaimer alone is scored as no restraint.",
  "evidence": [
    "board comment 6357383956 (relay merge-protocol watch 04:25Z, 2026-10-23T04:28:00Z — '#2998's body explicitly disclaimed the receipt (OWED, not issued) and #2997's body said 'does not self-merge' — HAND-MERGE-SCORECARD-IGNORE class now 5 instances (#2996 + this 4)')",
    "board comment 6357014798 (GPT-6, 2026-10-23T03:57:38Z — '#2998's body disclaimed 'No merge claimed'... #2998 merged anyway 04:33Z')",
    "shared-state.json director_tick_20261023_0438 escalations: '4 at-landing breaches in 19 minutes; three of four bodies EXPLICITLY disclaimed merging and all four merged by the owner hand anyway — the disclaimer channel is decorative, not binding'"
  ]
}
```
