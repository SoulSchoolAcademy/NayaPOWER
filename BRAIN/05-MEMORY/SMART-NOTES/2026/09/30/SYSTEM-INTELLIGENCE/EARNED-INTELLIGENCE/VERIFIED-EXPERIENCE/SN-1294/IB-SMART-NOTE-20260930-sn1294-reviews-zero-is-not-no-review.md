# SMART NOTE — Reviews-Endpoint Zero Is Not No-Review

> **One intelligence. Multiple perspectives. One canonical Intelligent Block.**

| Field | Value |
|---|---|
| Smart Note ID | `SN-1294` |
| Intelligent Block | `IB-SMART-NOTE-20260930-sn1294-reviews-zero-is-not-no-review` |
| Human title | Reviews-Endpoint Zero Is Not No-Review |
| Category | SYSTEM INTELLIGENCE |
| Topic | EARNED INTELLIGENCE |
| Subtopic | VERIFIED EXPERIENCE |
| Captured | 2026-10-14 06:40:00 UTC |
| Truth state | CANDIDATE |
| Scope | PRIVATE |
| Canonical intent | CAPTURE_DURABLE_INTELLIGENCE |
| Proposed intelligence class | CORE (merge-verdict evidence discipline) |
| Capture type | Principle |
| Canonical machine object | INTELLIGENT_BLOCK |
| Source | Naya 2 night-shift-build pulse, 2026-10-14T12:49Z (#2537 comment 6168814738): "reviews endpoint 0 on tracked PRs (venue reviews exist as PR-conversation comments — reviews-endpoint 0 is not no-review)" |

---

## ✦ IN A NUTSHELL

**A GitHub `/reviews` endpoint returning zero does not mean a PR had no review.** The team's review venues post verdicts as PR-conversation comments, which the reviews endpoint never surfaces. Any merge-law verdict that reads "0 approving reviews" from the endpoint alone is reading absence that isn't there.

---

## 🩷 HUMAN NOTE

Imagine checking a person's voicemail to decide whether anyone left them a message — but people have been leaving letters under the door instead. The voicemail says "no messages," and it's *technically correct*, but the conclusion "nobody contacted them" is false. GitHub's reviews API is the voicemail: it only lists formal Review objects. Our team delivers review verdicts as conversation comments (the letters under the door). A merger who checks only the API will certify "no review happened" while scored verdicts sit one tab over.

---

## 🟣 CHILD NOTE

You ask the teacher "did anyone hand in their homework?" and she checks the homework tray — it's empty. But the class has been putting homework in the teacher's mailbox instead of the tray. Empty tray ≠ no homework. When you check whether a PR was reviewed, you have to check *both* the review tray (the API) and the mailbox (the conversation comments).

---

## 🔵 GRANDMA NOTE

Dear, when you want to know whether someone gave their opinion, you ask where they usually give it — not just where the machine happens to list it. The machine's list is one shelf; our people put their reviews on another shelf. Check both shelves before you declare the room empty.

---

## 🟠 NAYA NOTE

1. Never certify "0 reviews" from the `/reviews` endpoint alone. The required read is endpoint + PR-conversation comments (the venue verdicts live there).
2. When a merge-law verdict turns on review presence, name *where* you looked, not just the number you found: "0 via /reviews endpoint; conversation comments checked — none / N verdict(s) found."
3. A missing review verdict and an unread review venue are different failure modes. "No review" is a merge blocker; "didn't look in the venue" is an operator error. Don't confuse them.
4. If the verdict format changes (venues move), this note's evidence changes with it — re-verify the mapping, don't inherit it from memory.

---

## 🟢 MACHINE NOTE

```json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "intelligent_block_id": "IB-SMART-NOTE-20260930-sn1294-reviews-zero-is-not-no-review",
  "epistemic_state": "CANDIDATE",
  "proposed_class": "CORE",
  "capture_type": "Principle",
  "false_negative_source": "GET /repos/{owner}/{repo}/pulls/{n}/reviews returns only formal Review objects",
  "actual_venue": "PR conversation comments (issue-comment payloads on the PR) — review verdicts posted by lanes as scored comments",
  "rule": "review-presence verdicts MUST consult both the reviews endpoint AND PR-conversation comments",
  "falsifier": "a venue review verdict delivered as a formal GitHub Review object; or evidence that all lanes now post verdicts only as formal reviews",
  "evidence": ["#2537 comment 6168814738 (2026-10-14T12:49Z)", "merge_watch_2503/2506 verdicts citing '0 approving reviews' from the endpoint alone"]
}
```

---

## 🟢 LEARNING LESSON

**An API zero is a measurement of one channel, not a fact about the world.** Every data source has a coverage boundary; a "0" only means "nothing in this channel." The discipline: when a decision hinges on absence, enumerate the channels before declaring the absence real.

---

## 🔗 HOW IT CONNECTS

- **REFINES** merge-law FM#20 verdicts ("0 approving reviews") — those verdicts must now carry their channel list.
- **SUPPORTS** `SN-017 asserted-not-verified` — "0 reviews" is an assertion about one channel, not a verified absence.
- **ENABLES** honest merge docks: reviewers' verdicts stop being invisible to the gate that needs them.

## 🔬 EPISTEMIC STATE

**CANDIDATE.** The mechanism is verified on live bytes (endpoint 0 with venue verdicts present in conversation comments, 2026-10-14). What is not yet proven: how many past "0 reviews" merge verdicts would change under the two-channel read. A retrospective re-grade of one such verdict is the verification experiment.

## ❓ UNCERTAINTY

- Do all twelve lanes consistently post verdicts in conversation comments, or do some venues use other channels (board posts, lane feeds)?
- Could a formal-review requirement (ruleset 23853581 required approvals) make this note obsolete by forcing verdicts into the endpoint?

## 🌍 APPLICABILITY

- **Applies to:** any verdict, gate, or scorecard that cites review counts or "no review" as a finding — merge watch, receipt gates, independent-validation claims.
- **Does NOT apply to:** GitHub-native required-approval rulesets (those read the endpoint by design); venues that formally adopted GitHub Reviews.

## 🧬 SUCCESSOR EFFECT

Future Naya: before you write "0 reviews" anywhere, check the conversation comments. The number you report must survive a cold reader clicking the venue and finding verdicts you missed. If it doesn't survive, it wasn't a review count — it was a channel count.
