Intelligent Block: SN-01773
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-21
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

Shawn's word, 2026-10-21 ~10:36 PDT, clarifying his pull-request directive from earlier the same morning (~09:18 PDT) after it was misheard as something about "poll requests" and reviews: he did NOT say "no pull requests," and he is not asking for a freeze on creating them. He said: get every open pull request finished and completed until the count is zero — no pile of pull requests waiting. And the real message underneath, in his words: "don't create more work until the work is done." The failure pattern he is naming: the team goes and creates more work — new pull requests, new efforts — without completing the work already open, so the open pile grows and nothing ever reaches done. Zero is reached by COMPLETING, not by avoiding. The order of work for every seat: do the work you are supposed to do — finish the open pull requests first — and only then create new work, which is created to be finished, not to be added to a pile.

## 🩷 HUMAN NOTE

Think of a kitchen counter covered with half-made sandwiches. Nobody can eat a half-made sandwich, and every new one somebody starts makes the counter worse. Shawn's rule is simple: finish the sandwiches on the counter. Hand them out. Get the counter clear. THEN start making more — and when you start one, you finish it. The problem was never that the team makes sandwiches. The problem is forty started and none served.

## 🟣 CHILD NOTE

Finish the puzzle that's already on the table before you open a new box. If you keep opening new boxes, you end up with pieces everywhere and not one finished picture. Done pictures are the point — not opened boxes.

## 🟠 NAYA NOTE

Standing law from Shawn's word (2026-10-21 ~10:36 PDT, chat, clarifying his ~09:18 PDT directive): (1) The open pull-request count is driven to zero BY COMPLETION — merge what is proven at the bar, fix what is fixable, close what is proven dead — never by leaving them sitting and never by a ban on creating. (2) The creation gate: while open pull requests exist that a seat could be advancing, that seat does not open new pull requests or start new work streams; its capacity goes to the unfinished work first. (3) A new pull request is opened only as the vehicle for work that will be carried to done — a pull request is a promise to finish, not a parking spot. This sharpens the no-queue law (2026-10-21 ~08:36 PDT) and its issues+PRs extension (~09:19 PDT): those said no backlog; this one names the mechanism that CREATES the backlog — starting new work ahead of finishing old work — and bans the mechanism, not the work. Standing venues that stay open by function (the live board, the master directive, mission state, the scoreboard) are the workplace, not backlog, and are untouched by this law.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "create-before-complete-backlog-growth",
  "evidence": {
    "receipts": "Shawn's typed words in chat, 2026-10-21 ~10:36 PDT: 'I want to get pull requests so there are zero — no pull requests waiting... that was my request. I didn't say no pull requests. I said get all of them done and completed... what you're really hearing is this: don't create more work until the work is done... you guys go and create more work without completing the work.' Clarifies his directive of 2026-10-21 ~09:18 PDT (PRs to zero, issues to the lowest true number, nothing stale). Open pull requests at the time: 50 verified by live count ~09:20 PDT the same morning. MEMORY.md standing entries: THE NO-QUEUE, FIX-IT LAW and its EXTENDED TO ISSUES + PRs bullet; this note's clarification bullet added the same day."
  },
  "decision_change": "Dispatch order is now finish-first by law: a seat's capacity goes to advancing the oldest completable open pull requests before any new pull request or work stream is opened by that seat. The open-PR count is driven to zero by completions (merge at the bar / fix / proven-dead close) and kept at zero; a rising open count is treated as a creation-discipline failure, not a workload fact.",
  "falsifiability": "If a case arises where opening a new pull request is the only way to complete an existing one (a fix that must land as its own PR, a carrier replacement like PR #2828 replacing the closed #2468), the new PR is the completion vehicle for the old work and is inside the law, not an exception to it. The law is falsified as stated if a seat can show that finishing-first ordering measurably blocks a higher-value completion — the claim is then re-decided on that evidence, not on preference.",
  "mechanism": "Unfinished work compounds: every open pull request holds context, review attention, rebase debt against a moving main, and stale-risk, and each new one opened dilutes the capacity that would have finished the earlier ones — so creation-ahead-of-completion is the engine that manufactures backlogs. Completion converts the same capacity into closed, verified value and frees the context entirely. Zero open pull requests is therefore not an austerity target; it is the natural state of a system that finishes what it starts.",
  "applies_when": ["pull-request", "work-creation", "backlog", "dispatch", "prioritization", "queue"],
  "enforcement": "The continuous count discipline of the no-queue law: the open pull-request count is re-derived live every pass and driven to zero by completions; a seat that opens a new pull request while completable pull requests sit idle is out of law and the new work is paused until the older work is carried. The count is proven from live GitHub bytes each time it is cited, never asserted from memory.",
  "coincidence_check": "cousins SN-01769 (RESOLVED is a proven state, not an asserted one — different: closeout semantics for finishing, not the creation-order gate); SN-01768 (retire by proof, not by paper — different: how stale work is cleared, not whether new work may start); the no-queue law itself (Shawn, 2026-10-21 ~08:36 PDT, MEMORY.md — this note is its mechanism-level sharpening: the earlier law bans the backlog, this one bans creating ahead of completing, which is how the backlog forms). Distinct leg: the finish-before-create ordering rule for all new work."
}
~~~
