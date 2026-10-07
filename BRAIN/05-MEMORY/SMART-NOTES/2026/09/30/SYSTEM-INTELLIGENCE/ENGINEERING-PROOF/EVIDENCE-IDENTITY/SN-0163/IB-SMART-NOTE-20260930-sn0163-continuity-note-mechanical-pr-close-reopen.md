# Narrate Mechanically-Induced State Transitions — the PR That Closed Itself

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0163-continuity-note-mechanical-pr-close-reopen
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-02
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #554 comment 5945564401 (2026-10-02T04:23:21Z, [NAYA][CONTINUITY NOTE]): to make #1310 exact-current-main before applying the converged artifacts, its head branch was reset to current main `ae2fd838d092ae1ae7414aa239fe486e1a5eef46`; GitHub automatically closed the draft PR during the brief zero-diff state; after the five converged files were reapplied, #1310 was explicitly reopened as OPEN + DRAFT (exact head `5d78aa434200d8b854fa10b4aaa2d2844d3bdddd`, ahead 5 / behind 0, no merge performed).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Platform side effects write audit-trail events that look like governance decisions. Resetting a PR branch to main to re-base a convergence produced a zero-diff moment — and GitHub auto-closed the draft PR, then it was reopened with the files reapplied. To a later reader that close/reopen pair reads exactly like a governance act (closed → reopened = decision → reversal). The lane posted an explicit continuity note: what was mechanical, what the exact states were, and that no merge was performed. The rule: any operation with a visible side effect on shared state (PR open/close, branch reset, rebase) gets a one-paragraph continuity note at the moment it happens — mechanical or it will be misread as deliberate. Cousin map: SN-082 (execution identity is not content identity) distinguishes runs from results; this note distinguishes *platform-side-effect* events from *governance* events in the same audit stream.

## 🩷 HUMAN NOTE

Shawn — picture a security camera recording a room where someone trips a light switch by leaning on it. A week later the footage shows the lights going off and on — and without context, it looks like someone signaled. That's what happened on #1310: a routine branch reset to current main made the PR briefly empty, and GitHub — automatically — closed it. It was reopened a minute later with the files back. But the board's history now shows "closed / reopened," which to any later reader (or cold successor) looks exactly like a decision was made and reversed. The lane caught it in real time and wrote a continuity note: here's what was mechanical, here's the exact before/after state, no merge happened. The lesson: whenever you do something whose side effect is visible to everyone — resetting a branch, closing or reopening a PR — write one paragraph saying what you did and why, *right then*. If the record doesn't carry the explanation, the record will be read as a governance decision later. And unexplained decisions in the record are how future work gets built on sand.

## 🟣 CHILD NOTE

Imagine you tidy your desk and the class attendance chart falls off the wall and lands face-down. Later your teacher sees it face-down and thinks you quit the class! The board here is the #554 issue — everything the team does is written there so anyone can read the story later. A team member moved a branch (like moving the chart back on the wall), and GitHub — the computer — automatically closed the PR (like the chart falling face-down). Anyone reading later would think "they closed the PR as a decision!" So they wrote a quick note: "I didn't decide to close it — the computer did it when I moved the branch. I opened it back up. Nothing was merged." The rule: if you do something that *looks* like a big decision but was actually just the computer doing its thing, write down what really happened, right away. Otherwise the story gets read wrong.

## 🔵 GRANDMA NOTE

It's like a library book that slides off the shelf and lands in the returns bin. The librarian sees it in the bin and thinks someone returned it — but really, gravity did that, not a person. On GitHub, when a team's work branch was lined up with the main branch, the code briefly became identical — and GitHub, being automatic, closed the request as if the team had decided to withdraw it. They opened it right back up and wrote a plain note: "No decision was made here; the platform closed it because of a momentary empty state; here's exactly what the branch looks like now." The lesson: automatic things leave footprints that look like deliberate decisions. Write a sentence saying "this was automatic, not a decision" while it's fresh — because months from now, nobody will be able to tell the difference, and people plan real work around what the record seems to say.

## 🟠 NAYA NOTE

Apply this before every branch/PR operation with visible side effects: (1) anticipate what the platform will do — branch reset to main base ⇒ zero-diff window ⇒ GitHub auto-closes open PRs; know the side-effect graph before you act; (2) the moment a mechanical event lands in the shared record, post a continuity note with: what was mechanical, the exact before/after refs (branch head SHAs, PR state), and what was NOT done (no merge, no decision); (3) never let the audit stream carry an unexplained close/reopen/reset — an unexplained governance-shaped event *is* a governance-shaped lie; (4) keep continuity notes mechanical and timestamped — no interpretation, just state; (5) when reviewing a lane's history, check for continuity notes before reading close/reopen events as decisions.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "misread platform side effects (mechanically-induced PR close/reopen recorded without narration, readable later as a governance decision/reversal)",
  "evidence": {
    "board": "#554 5945564401 (2026-10-02T04:23:21Z) — [NAYA][CONTINUITY NOTE]: #1310 head branch reset to current main ae2fd838d092ae1ae7414aa239fe486e1a5eef46 before applying converged artifacts; GitHub auto-closed the draft PR during the brief zero-diff state; five converged files reapplied; #1310 explicitly reopened OPEN + DRAFT at 5d78aa434200d8b854fa10b4aaa2d2844d3bdddd, ahead 5 / behind 0; no merge performed; note exists so the close/reopen is not misread as a design/governance decision."
  },
  "rule": [
    "narrate mechanically-induced state transitions in the shared record at the moment they happen — a PR close/reopen/reset without a continuity note is a governance-shaped lie",
    "know the platform's side-effect graph before operating: resetting a branch to its base creates a zero-diff window and GitHub auto-closes open PRs",
    "continuity notes carry exact state (refs, PR status, what was not done), zero interpretation, and are posted with the event, not reconstructed later"
  ],
  "lesson_line": "Platform side effects write audit-trail events that look like governance decisions — narrate every mechanical state transition in the shared record the moment it happens, with exact refs and what was not done."
}
~~~
