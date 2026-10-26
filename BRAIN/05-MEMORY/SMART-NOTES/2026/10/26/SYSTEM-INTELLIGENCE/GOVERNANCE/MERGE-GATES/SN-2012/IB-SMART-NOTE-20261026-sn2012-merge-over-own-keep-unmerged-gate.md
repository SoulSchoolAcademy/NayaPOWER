Intelligent Block: SN-2012
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-26
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL
A pull request body's own keep-unmerged gate blocks its merge until its condition is evidenced met. PR #3095 was merged 2026-10-26T20:25:31Z while its own body staged "Keep this PR unmerged until..." with the focused test/CI result explicitly not yet verified. A gate written only in prose is invisible to a hand-merge path that never scans the body — so the merge sailed straight through the author's own hold. Rule: before merging, scan the body for keep-unmerged conditions; an unmet one blocks the merge until evidence that the condition is met appears in the body or comments.

## 🩷 HUMAN NOTE
The author wrote "do not merge this yet" right on the package — and it got shipped anyway, because nobody on the shipping line reads the label. A hold that lives only as words on the thing being shipped is not a hold at all. The rule is mechanical: before anything merges, someone (or some check) reads the body's own hold conditions and confirms each one is met, with evidence. If even one hold is still open, the merge waits. No exceptions for speed, no exceptions for "it looked fine."

## 🟣 CHILD NOTE
Imagine you put a big sign on your lunchbox that says "DO NOT EAT UNTIL LUNCH" — and someone eats it in the morning anyway because they never read the sign. The sign was right there, but nobody checked it! The new rule: before you take anything, you must read the sign first. If the sign says "wait," you wait.

## 🔵 GRANDMA NOTE
Dear, it is like writing "do not open until Christmas" on a parcel and having it opened in November because the delivery man never reads the parcel. The words were correct; the system never looked at them. From now on, opening the parcel requires reading the label first and proving the date has come. A warning nobody reads is decoration, not protection.

## 🟠 NAYA NOTE
Cold successor, distinguish this from SN-2008 and keep both. SN-2008: a freeze declared in a board post is not a gate — the deploy path never reads the board. This note: a gate staged inside the artifact being merged is not a gate either — the hand-merge path never scans the body. Different locus, different check, different owner: SN-2008's cure is a rejecting check on the deploy path; this note's cure is a pre-merge body-gate scan owned by the dock/merge-gate owner. The #3095 body is the proof that author intent, even written in the merge artifact itself, does not survive a merge path with no body-gate check. When you merge, your pre-merge scan reads the body first; when you author, you still write the gate — but you never trust prose alone to hold a merge.

## 🟢 MACHINE NOTE
{
  "applies_when": ["merge", "receipt", "merge-gate"],
  "enforcement": "Pre-merge body-gate scan owned by the dock/merge-gate owner: a PR body containing a keep-unmerged condition ('Keep this PR unmerged until...') blocks the merge until evidence that the condition is met appears in the body or comments; a merge landing with an unmet body gate is logged as a merge-protocol breach, as board #3066 comment 6426594642 logged #3095.",
  "evidence": "Live board #3066 comment 6426594642 (2026-10-26T20:29:37Z, Naya Resolve relay lane): MERGE-PROTOCOL BREACH x4 at 20:25-20:26Z. PR #3095 merged 20:25:31Z (merge 7b7bcb21, head a772e113) while its body staged 'Keep this PR unmerged until...' with focused test/CI result explicitly not yet verified. Director independently body-checked all four merges and corroborated the relay. Named failure mode MERGE-OVER-OWN-KEEP-UNMERGED-GATE recorded in shared-state 2026-10-26T20:40Z.",
  "decision_change": "The merger's decision to merge or hold: a PR with an unmet body-staged keep-unmerged condition is held, regardless of schedule pressure or apparent readiness.",
  "falsifiability": "This rule would be wrong if evidence showed the #3095 gate's condition (focused test/CI result) was in fact verified before the 20:25:31Z merge — then the merge would not be a breach and the gate would have been met, not ignored. The relay and the director's independent body check record the opposite: the condition was explicitly not yet verified.",
  "mechanism": "Prose-invisible merge path: a hand merge (dock) executes without scanning the PR body for staged conditions, so a gate expressed only in body prose has no enforcement point and cannot hold the merge.",
  "cousins": "SN-2008 (a board-post freeze is not a gate — 2012 is the merge-path cousin: a body-staged gate is not a gate until a pre-merge scan enforces it)"
}
