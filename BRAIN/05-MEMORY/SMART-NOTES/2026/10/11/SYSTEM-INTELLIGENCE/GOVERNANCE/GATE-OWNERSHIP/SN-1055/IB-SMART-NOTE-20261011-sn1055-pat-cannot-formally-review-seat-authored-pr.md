# A PAT Cannot Formally Approve a Seat-Authored PR — the GitHub App PEM Is the Wall, and It's Shawn's Gate

**Intelligent Block:** IB-SMART-NOTE-20261011-sn1055-pat-cannot-formally-review-seat-authored-pr
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-11
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Naya Verity (Lane 1) tick t1342, 2026-10-11 23:15 PDT — PR #2452 drift-heal 2-seat bar; formal APPROVE review submission platform-blocked, PAT 422 self-approval; receipt hidden_files/twelve-lane-receipts/t1342-lane1.md; scorecard posted ON the PR, #2175 comment 6118785140. Related: SN-0993 (declare author seat for mechanical consensus).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Formal APPROVE review submission on a seat-authored PR is **platform-blocked**: the shared seat account authored the PR, so GitHub returns 422 self-approval — a personal access token cannot formally review what its own account authored, no matter how independent the human behind the seat is. Retrying the same POST will fail the same way forever.

The only path to a real formal review is a different identity: the GitHub App installation token. And the App PEM is **not installed** — that install is Shawn's gate. So the standing position, until his clicks land: any lane needing a formal approving review on a seat-authored PR hits this wall today. Do not re-attempt the submission expecting a different result; do not burn actions on it. The working substitute is the one the team already uses — independent scorecard receipts posted as comments (Lane 9 + Lane 1 both 9.0/10 on #2452, pin-exact) — and the formal review waits on the App.

## 🩷 HUMAN NOTE

Shawn — one platform wall the team hit tonight, worth knowing once. A lane tried to submit a formal "approved" review on a pull request our shared account had authored, and GitHub refused — you can't formally approve your own account's work, and our login token can't get around that. The fix is the GitHub App install (a separate identity, on your click list) — until then, lanes use posted scorecard reviews instead, which is what happened tonight. Nothing to do; just don't want anyone surprised by the 422.

## 🟣 CHILD NOTE

Imagine you write a story and want a grown-up to stamp it "approved." But the only stamp in the house is yours, and the rule is you can't stamp your own story. The grown-up can still write a note saying "I read it, it's great" — and that's what happened tonight: two lanes wrote full review notes on the PR instead of using the stamp. The stamp itself needs a new identity card (the GitHub App), and only Shawn can issue that one.

## 👵 GRANDMA NOTE

It's like trying to notarize your own signature — the notary's rulebook says no, even when everything is honest. The workaround is a different notary (the GitHub App), and getting that notary commissioned is Shawn's errand. Until then, the team does what honest people do: two independent lanes read the work carefully and put their full written reviews on the record, stamp or no stamp. The review is real; only the rubber stamp waits.

## 💜 NAYA NOTE

I hit the 422 tonight on #2452 and I will not hit it again blindly: a PAT reviewing its own account's PR is self-approval by definition, and the platform says no. The App PEM is the only other identity, and it is not installed — Shawn's gate, not mine to work around. So my lanes stop attempting formal submissions on seat-authored PRs; the independent scorecard receipts in the comments are the review until the App exists. Knowing which walls are real is how we stop spending the budget on doors that don't open.

## 🤖 MACHINE NOTE
```json
{
  "sn": "SN-1055",
  "lesson": "pat-cannot-formally-review-seat-authored-pr",
  "rule": "A PAT cannot submit a formal approving review on a PR authored by the same account (422 self-approval). The GitHub App installation token is the only alternate identity; the App PEM is not installed (Shawn-gated). Until then, independent scorecard receipts posted as comments are the review substitute — do not re-attempt formal submission.",
  "instances": [
    "t1342-lane1: formal APPROVE on PR #2452 (seat-authored) → 422 self-approval; independent scorecards posted instead — Lane 9 9.0/10 (6118588834) + Lane 1 9.0/10 (6118785140), pin-exact on c4bfd252"
  ],
  "evidence": {
    "receipt": "hidden_files/twelve-lane-receipts/t1342-lane1.md",
    "scorecard_on_pr": "PR #2452 comment 6118785140"
  },
  "related": ["SN-0993"]
}
```
