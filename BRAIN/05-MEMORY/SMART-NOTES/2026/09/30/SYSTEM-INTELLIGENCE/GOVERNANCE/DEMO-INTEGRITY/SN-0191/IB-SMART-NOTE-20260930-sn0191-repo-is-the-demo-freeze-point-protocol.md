# The Repo Is the Demo — the Freeze-Point Protocol

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0191-repo-is-the-demo-freeze-point-protocol
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-02
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Shawn-directed doctrine, announced on `#554` by Naya 2 (5953833712, 2026-10-02 13:49:40Z): **no disconnect between what's shown and what's in GitHub.** First application inside the same hour — Naya 3's Room 02 build receipt (`#554` 5954125488) froze review SHA `1a586e9dbb7fa9d7eff8a38f24b8d488e23bbecb` and bound its browser-QA evidence (Hub App Completion Gate run `37016607962`, artifact digest `sha256:d59961a523fee1fc2685fbb57b9e3e23dbf5cb18690b978f6139dfb21c4e35ac`) to that exact commit.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Four rules, mechanical:

1. **Code lands in GitHub first.** Every shareable checkpoint is a pushed commit on a branch — that commit SHA is the freeze point.
2. **What Shawn views = the frozen SHA.** Via the Cloudflare-synced live version or by downloading the HTML from GitHub at that commit — his choice.
3. **Nothing shown outside GitHub that isn't pushed.** If a preview appears in chat or the feed, it is rendered FROM the frozen commit — never a side copy, never a mockup that drifts.
4. **Naya 1 judges the same SHA Shawn viewed.** One SHA, one review, one gate.

The failure this kills: "the demo looked different from the repo." When the demo is a side copy, the judge scores a fiction, the director reacts to a fiction, and the repair targets a fiction. The freeze point collapses view, review, and repair onto one pushed commit. Note what the protocol does NOT say: it does not say the build is good — Naya 4's Room 01 v1 (PR `#1325`, verified mergeable at `e5a99831`) followed the spirit of the protocol and was still scrapped on Shawn's verdict (SN-0193). The protocol guarantees everyone is looking at the same thing, not that the thing passes. It is the sibling of SN-061 (verdicts die at every new SHA) and SN-043/100 (compare at one commit): those bind *verdicts* to SHAs; this binds the *demo itself* to a pushed commit.

## 🩷 HUMAN NOTE

Shawn — a standing rule from the room-build round, stated mechanically: the repo IS the demo. Code lands in GitHub first, every checkpoint is a frozen commit SHA, what you view is exactly that SHA, and Naya 1 judges the same SHA you viewed. One SHA, one review, one gate. Naya 3's Room 02 receipt already follows it — frozen SHA plus QA evidence bound to that exact commit. No more "the demo looked different from the repo."

## 🟣 CHILD NOTE

Imagine if you took a photo of your homework, but the photo was from yesterday's homework. Your teacher would grade the wrong page! The new rule: nobody looks at a copy. Everyone looks at the one real thing in one place, at one moment in time. Same picture, same grade.

## 👵 GRANDMA NOTE

You know how we never trust a copy of a copy? Same idea here: from now on, nobody is shown a side copy of the work. Everything Shawn looks at comes straight from the one real repository, at one exact saved moment — and the person grading it looks at that same moment. No more "but the demo looked different."

## 🤖 NAYA NOTE

Enforce the freeze-point protocol on every shareable build checkpoint: (1) push first, name the commit SHA as the freeze point; (2) every view link (Cloudflare-synced live, downloaded HTML, feed preview) is rendered FROM that exact commit — never a side copy, never a mockup; (3) the judging seat (Naya 1) reviews the identical SHA the director viewed; (4) board announcements of builds name the frozen SHA and bind evidence (CI runs, artifact digests) to it. This is the operational complement to SN-061 (verdicts die at every new SHA): SN-061 binds verdicts to SHAs, the freeze-point protocol binds the demo itself to a pushed commit. Passing the protocol is not passing the gate — PR `#1325` was freeze-point-clean and still scrapped on verdict (SN-0193); the protocol guarantees everyone looks at the same thing, not that it passes.

## ⚙️ MACHINE NOTE

{"sn": "SN-0191", "title": "The Repo Is the Demo — the Freeze-Point Protocol", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-02", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "GOVERNANCE", "DEMO-INTEGRITY"], "extends": ["SN-043", "SN-061", "SN-100"], "evidence": {"doctrine": "5953833712", "authority": "Shawn-directed, announced by Naya 2", "rules": ["code lands in GitHub first; freeze point = pushed commit SHA", "director views = frozen SHA", "nothing shown outside GitHub that isn't pushed", "judge reviews the same SHA the director viewed"], "first_adoption": "5954125488 (Room 02 receipt: frozen SHA 1a586e9dbb7fa9d7eff8a38f24b8d488e23bbecb + QA run 37016607962 + artifact digest bound to it)", "non_claim": "freeze-point-clean != passing; PR #1325 scrapped on verdict (SN-0193)"}, "rule": "one SHA, one review, one gate — the repo is the demo"}
