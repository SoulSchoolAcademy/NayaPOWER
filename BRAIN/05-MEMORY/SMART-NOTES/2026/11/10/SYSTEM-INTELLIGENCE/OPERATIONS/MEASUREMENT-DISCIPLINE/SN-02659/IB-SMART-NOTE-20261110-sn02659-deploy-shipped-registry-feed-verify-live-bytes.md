**Intelligent Block:** IB-SMART-NOTE-20261110-sn02659-deploy-shipped-registry-feed-verify-live-bytes
**Smart Note:** SN-2659
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-10
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Staged by the smart-note distillation loop 2026-11-10 22:08 PST. Evidence: PR #3329 "Feed regression: 794 → 338 — wrangler deploy shipped the registry feed; guard + re-bake" merged 2026-11-11T01:44:51Z; CONNECT-DRIVER receipt board #3066 comment 6787124008 (2026-11-11T04:35:09Z); director tick 2026-11-11T04:38Z record in shared-state.json on disk; dir-kernel-2026-11-10.txt. Zero GitHub REST calls this tick for #1354 (capped at 2500 comments, commenting disabled 2026-10-10); App route used only by the staging script.

## ✦ IN A NUTSHELL

A wrangler deploy shipped the registry feed instead of the live feed, and the Hub silently showed 338 cards instead of 794. The deploy itself succeeded — green deploy, wrong artifact. PR #3329 re-baked the feed to 861 cards and added a guard; the CONNECT-DRIVER re-proved it live: the live feed is byte-identical to the tip feed (sha256 7a897493, 6,583,817 bytes, 861 notes), and no tree SN is newer than the feed max anymore (121 newer SNs were missing on Nov 8). The durable rule: a deploy is not proven by a green deploy log — it is proven by the live bytes afterward. After every deploy, fetch the live feed and compare card count + hash against the tip feed; a mismatch means the wrong artifact shipped, no matter what the deploy log says. The registry feed and the live feed are distinct artifacts; a build step that picks the wrong one fails silently, and only the live-byte comparison catches it.

## 🩷 HUMAN NOTE

Shawn — a deploy went out green and the Hub still showed the wrong feed: 338 cards instead of 794, because the deploy bundled the registry feed rather than the live one. It is fixed now — re-baked to 861 cards and verified live, byte for byte against the source. The lesson that stays: a green deploy log is not proof the right thing went live. From here on, every deploy gets proven the same way this one was cured — fetch the live feed and check its count and fingerprint against the source. If they don't match, the deploy didn't land right, whatever the log says.

## 🟣 CHILD NOTE

Imagine you pack your lunchbox for school, but you grab your sister's lunchbox by mistake — same size, same color, wrong lunch inside. The walk to school went fine, nothing spilled, but you still open the wrong lunch. The deploy did the same thing: it carried the wrong feed to the Hub. The fix is simple — after every trip, open the lunchbox and check what's inside before you say lunch is ready.

## 🔵 GRANDMA NOTE

Dear, the delivery van arrived on time and the driver said everything went well — but the boxes on the porch were the wrong ones. The registry list is not the same as the live shelf, and the van carried the list instead of the shelf. We counted what was actually on the porch — 861 cards, matching the shelf exactly — and that is how we knew it was right. The rule for every delivery from now on: don't trust the driver's word alone; count what's on the porch and check it against the shelf.

## 🟠 NAYA NOTE

The verified facts: (1) PR #3329 "Feed regression: 794 → 338 — wrangler deploy shipped the registry feed; guard + re-bake" merged 2026-11-11T01:44:51Z (dir-kernel-2026-11-10.txt; shared-state breach_284_291_20261110 record). (2) CONNECT-DRIVER receipt, board #3066 comment 6787124008, 04:35:09Z (director tick 2026-11-11T04:38Z, shared-state.json on disk): FEED REGRESSION CURED LIVE — live feed byte-identical to tip feed, sha256 7a897493, 6,583,817 B, 861 notes; tree SNs newer than feed max 0 (was 121 on Nov 8); CONNECT 9.2 → 9.3. (3) The failure mode: the deploy step bundled the registry feed artifact where the live feed artifact belonged — a silent wrong-artifact swap, invisible to the deploy log. (4) Honest hole, stated not hidden: this tick verified the cure first-hand from the on-disk director record (live bytes identical, count 861, hash 7a897493); the guard PR #3329 claims is NOT verified from disk this tick — the learn mirror carries BRAIN, not HUB/worker code — so this note's enforcement rests on the demonstrated post-deploy live-byte comparison, not on the guard's internals. The guard's existence and mechanism remain to be verified by a seat that can read the merged PR. (5) Related open hole, not this lesson: 488/861 cards still lack registry entries (same director tick) — the registry chain's job, and a second reason the two feeds must never be confused. Cousins: SN-1947 (the wrong file faithfully proves a false negative — same family: the wrong artifact proves a false state), SN-1995 (a label is not a landing — a green deploy log is a label, live bytes are the landing), SN-2658 (verify a shared field against the repo — same family: verify the claim against the thing itself).

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-2659",
  "slug": "deploy-shipped-registry-feed-verify-live-bytes",
  "title": "A deploy can ship the registry feed instead of the live feed — verify live bytes after every deploy",
  "observation": false,
  "applies_when": [["deploy", "hub-feed"], ["deploy", "wrong-artifact"], ["feed", "registry-vs-live"]],
  "enforcement": "After every wrangler deploy, fetch the live feed and compare card count + sha256 against the tip feed (861 notes, sha256 7a897493, 6,583,817 B at cure time); any mismatch means the wrong artifact shipped — redeploy, do not declare the feed healthy. A deploy receipt that cites only a green deploy log, without the live-byte comparison, fails this gate. Mechanical tripwire: a live feed card count dropping sharply at a deploy boundary (794 -> 338 here) is a wrong-artifact signal until the live bytes prove otherwise.",
  "evidence": "PR #3329 'Feed regression: 794 -> 338 — wrangler deploy shipped the registry feed; guard + re-bake' merged 2026-11-11T01:44:51Z (dir-kernel-2026-11-10.txt; shared-state breach_284_291_20261110). Cure verified live by CONNECT-DRIVER, board #3066 comment 6787124008, 2026-11-11T04:35:09Z (director tick 2026-11-11T04:38Z, shared-state.json on disk): live feed byte-identical to tip feed, sha256 7a897493, 6,583,817 B, 861 notes; tree SNs newer than feed max 0 (was 121 on Nov 8); CONNECT 9.2 -> 9.3. The PR #3329 guard itself is NOT verified from disk this tick (learn mirror carries BRAIN, not HUB/worker code); enforcement rests on the demonstrated post-deploy live-byte comparison.",
  "decision_change": "Any seat declaring a deploy healthy must run the post-deploy live-byte comparison (live feed count + sha256 vs tip feed) first; a deploy declared healthy on the deploy log alone is unproven. The registry feed and the live feed are distinct artifacts and must never be treated as interchangeable in a build or deploy step — a step that picks the wrong one fails silently, and only the live-byte check catches it.",
  "falsifier": "Refuted if the 338-card feed is shown to have been the correct live feed at that time (i.e. the tip feed itself held 338 cards), or if the deploy record shows the live feed artifact was the one bundled. Bounded: the rule fires only when live bytes diverge from tip bytes at a deploy boundary — a future deploy whose live bytes match the tip feed is genuinely healthy, and the rule must not be used to discount it.",
  "cousins": ["SN-1947 (the wrong file faithfully proves a false negative — same family: the wrong artifact proves a false state)", "SN-1995 (a label is not a landing — a green deploy log is a label, live bytes are the landing)", "SN-2658 (verify a shared field against the repo — same family: verify the claim against the thing itself)"],
  "captured": "2026-11-10",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "intent": "CAPTURE_DURABLE_INTELLIGENCE"
}
```
