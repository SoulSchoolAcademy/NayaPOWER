# Route the External Red to Its Canonical Owner — Never Spoof, Never Weaken, Never Merge Around

**Intelligent Block:** IB-SMART-NOTE-20261005-sn0380-external-check-red-to-canonical-owner
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-05
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 6000736256 ([NAYA 3][INFRA HANDOFF], 2026-10-05T18:36:57Z): `Workers Builds: maxresults` and `maxess-e01` traced and classified — both are Cloudflare Workers and Pages GitHub-App checks, not repo workflows; both absent from NayaPOWER source/config; both fail repository-wide on recent commits; neither is required by GitHub rulesets. Classified UNRESOLVED_COMPETING_EXTERNAL_RELEASE_LANE / FAIL-CLOSED, routed to release-authority issue #255 with the owning-lane next action: prove/repair each Worker as canonical, or disconnect/retire its NayaPOWER Git association so the false repository-wide RED stops at the source. PR #1495 stays HOLD (source green, Kernel + Collective green) until the external red is cleared at its source — no check spoofing, no gate weakening. Backed by the operating law restated in the same sign-out chain (6000380502): "do not merge with red CI. Ever."

## ✦ IN A NUTSHELL

When a repository-wide RED comes from a check the repo does not own — an external app's checks (here, Cloudflare Workers/Pages GitHub-App checks `maxresults` and `maxess-e01`) that exist in no source file, no config, and no ruleset — it is a competing external release lane, not repo debt, and it must be routed to its canonical owning authority, not absorbed by the lane that happens to see it. The discipline has four hard parts: classify it FAIL-CLOSED and say so on the record; route it to the owning authority with the exact repair-or-retire options written down (prove/repair each Worker as canonical, or disconnect its Git association); hold your own merge until the source is fixed — "do not merge with red CI. Ever." is not reinterpreted away because the red is inconvenient; and never spoof a check, never weaken a required gate, never merge around the red to make the dashboard look green. A red retired at its source stays fixed; a red merged around returns forever.

## 🩷 HUMAN NOTE

Shawn — two Cloudflare checks have been failing on everything for days, and they're not ours: they don't exist in our code, our config, or our rulesets. They're coming from a separate Cloudflare release lane that's hooked into our repo. The right move isn't to bend our gates around them — it's to hand them to their actual owner with a clear choice: prove each check is real and fix it, or disconnect it from our repo so the false alarm stops at the source. Nothing merges until that's resolved; we don't fake checks green and we don't weaken gates to get unblocked.

## 🟣 CHILD NOTE

Imagine a neighbor's fire alarm is wired into your house, and it keeps ringing even though there's no fire. The wrong moves: take the batteries out of YOUR alarm, pretend the ringing is fine, or move out so you don't hear it. The right move: call the neighbor and say "your alarm is wired into my house — either prove there's a fire and put it out, or unplug it from my wall." The ringing stops at the source, and your alarm keeps working for real fires.

## 👵 GRANDMA NOTE

When something outside your house keeps setting off your alarms, you don't disconnect your own alarm or learn to ignore the sound — that's how you miss a real fire. You find out who owns the other alarm and tell them plainly: either show me it's working and fix it, or unhook it from my property. The noise stops where it starts. And you never, ever weaken your own protection just to make the noise go away.

## 💜 NAYA NOTE

Note to future me: when a check is red across unrelated PRs and commits, check its provenance before touching the repo — is it a repo workflow, a required ruleset check, or an external app's check with no presence in source/config? If the latter, stop lane work on it immediately: it is UNRESOLVED_COMPETING_EXTERNAL_RELEASE_LANE, fail closed, and the next action belongs to the owning authority, recorded on the owning issue with the two options spelled out (prove/repair as canonical, or disconnect/retire the association). The three things I never do, even under time pressure: spoof a check to green, weaken a required gate to unblock a lane, or merge around a red and normalize it. The operating law is blunt for a reason — "do not merge with red CI. Ever." — and it applies hardest exactly when the red is someone else's, because that's when the temptation to merge around it is strongest. Today's debt, if unresolvable now, gets the ratchet: named, dated, fail-closed, owned — never silently absorbed.

## ⚙️ MACHINE NOTE

{"sn": "SN-0380", "title": "Route the External Red to Its Canonical Owner — Never Spoof, Never Weaken, Never Merge Around", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-05", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "GOVERNANCE", "OWNERSHIP-MAP"], "cousins": ["SN-0159", "SN-0240", "SN-0352"], "evidence": {"board": "#1354 6000736256 ([NAYA 3][INFRA HANDOFF], 2026-10-05T18:36:57Z): Workers Builds maxresults + maxess-e01 are Cloudflare Workers/Pages GitHub-App checks, absent from NayaPOWER source/config, failing repository-wide, not required by GitHub rulesets; classified UNRESOLVED_COMPETING_EXTERNAL_RELEASE_LANE / FAIL-CLOSED; routed to release-authority issue #255 with owning-lane next action (prove/repair each Worker as canonical, or disconnect/retire its NayaPOWER Git association); #1495 (source green, Kernel + Collective green) stays HOLD; no check spoofing, no gate weakening"}, "rule": "a repository-wide red from a check with no provenance in repo source/config/rulesets is a competing external release lane: classify FAIL-CLOSED, route to the canonical owning authority with repair-or-retire options written down, hold merges until the source resolves it, and never spoof, weaken, or merge around the red"}
