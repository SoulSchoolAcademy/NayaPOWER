# Stamp Provenance at Vendor Time — A Vendored Copy Without a Source Commit Is a Drift Vector

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1590-stamp-provenance-at-vendor-time
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-17
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** hidden_files/twelve-lane-receipts/gap-lane-scorer-20261017-1850-lane0.md (Naya Clarity Narzan, Lane 0 hat — self 9.5/10) — closed the H3 gap (t0800): vendored hidden_files/js/supabase-bridge.js as a byte-copy of HUB/app/js/supabase-bridge.js at commit 8dad8451b9c5b39f0edd2278c8155eaad11a1b0b (blob SHA 262fa3ae4282af72325453b3f87f1530ce492542e962022769efb9ca5d39c939), committed alongside hidden_files/js/supabase-bridge.PROVENANCE naming the source commit + blob SHA + the re-vendor drift rule ("when HUB/app/js/supabase-bridge.js changes upstream, re-copy and re-stamp; SHA check command is in the file"). Receipt's Pass-2 (−0.3): "vendored copy = drift risk by construction; mitigated with the PROVENANCE file + re-vendor rule, but the canonical home stays the repo." Also logged as learning-event candidate, 2026-10-17 19:20 PDT hour.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A vendored copy is a snapshot that starts rotting the moment it's taken. The 1850 gap seat needed the t0800 Supabase bridge inside the goal tree's feed page, so she vendored it: a byte-copy of HUB/app/js/supabase-bridge.js pinned at commit 8dad8451b9c5b39f0edd2278c8155eaad11a1b0b with blob SHA 262fa3ae…. What makes this a discipline instead of a convenience is the second file committed in the same action: hidden_files/js/supabase-bridge.PROVENANCE, which names the source commit, the blob SHA, and the re-vendor rule — "when the upstream changes, re-copy and re-stamp; the SHA check command lives in this file." Rule: vendoring is a two-file operation — the copy and its provenance stamp, same commit, always. Without the stamp, drift is silent and the copy's origin becomes archaeology; with it, drift is detectable and the refresh path is mechanical. The canonical home stays the repo; the vendored copy is a convenience with an expiry contract.

Why this is brain-grade: teams vendor code constantly — bridges, shims, polyfills — and the failure mode is always the same slow one: upstream moves, the copy doesn't, and six months later nobody can tell which upstream commit the copy came from or whether it's safe to refresh. The provenance stamp converts that failure from archaeology into arithmetic: run the embedded SHA check, compare against upstream, re-copy if different. The stamp costs one small file at vendor time and saves a forensics expedition later.

## 🩷 HUMAN NOTE

Shawn — small process discipline from tonight's feed-page bridge work. I copied the Supabase bridge file into the goal tree so the feed page could use it — but a copied file drifts: the original keeps evolving and the copy quietly goes stale. So the copy shipped with a companion file that says exactly which upstream commit it came from, its fingerprint, and the rule: when the original changes, re-copy and re-stamp. The check command is baked into that file, so proving whether the copy is current is one command, not a forensics expedition. Standing rule from here on: every vendored file gets its provenance stamp in the same commit — no stamp, no vendor.

## 🟣 CHILD NOTE

Imagine you photocopy a recipe from your friend's cookbook. Six months later your friend updates the recipe — but your photocopy still has the old one, and you've forgotten which cookbook it came from. That's the problem with copies! The smart move: staple a little note to your photocopy that says "copied from this cookbook, this page, on this date — if the cookbook changes, re-copy and update the note." Then you always know exactly where your copy came from and whether it's still fresh. Copies always get their little note. Always.

## 👵 GRANDMA NOTE

Dear, there's wisdom in labeling things at the source. Tonight someone needed a copy of a bridge file for the feed page — and instead of just copying it and hoping for the best, they attached a little card to it: where it came from, its fingerprint, and what to do when the original changes. It's the same instinct as dating a jar of preserves: future you will be grateful. Copies without provenance rot silently; copies with provenance are honest about their age.

## 🧠 NAYA NOTE

Vendoring discipline, copy this exactly: (1) the vendoring commit contains TWO files — the byte-copy and the <name>.PROVENANCE file; (2) the PROVENANCE file names the source path, source commit SHA, blob SHA of the copy, and the re-vendor rule with the SHA-check command spelled out; (3) the canonical home stays the upstream repo — the copy is a convenience, never the source of truth; (4) the honest scorecard names the drift risk (−0.3) and the mitigation, not just the mitigation. When re-vendoring, re-stamp in the same commit — never refresh the copy and leave the old stamp. Enforcement hook: any review that finds a vendored file without a same-commit PROVENANCE file bounces the PR until the stamp exists. Drift is inevitable; un-stamped drift is the failure.

## ⚙️ MACHINE NOTE

```json
{
  "sn": "SN-1590",
  "applies_when": ["vendor", "provenance"], ["drift", "vendored-copy"], ["copy", "upstream-sync"],
  "enforcement": "the <name>.PROVENANCE file's embedded SHA-check command (compare copy blob SHA against upstream source at the named commit) — run it to detect drift; every vendoring commit must carry the PROVENANCE file in the same commit. A vendored file without a same-commit PROVENANCE file fails the review check.",
  "falsifier": "A vendored copy whose source commit cannot be named, or that diverges from upstream without the drift being detectable by the embedded SHA check, proves the stamp was missing or stale — the failure the rule exists to prevent.",
  "mechanism": "A provenance stamp converts drift from archaeology into arithmetic: the embedded check makes staleness detectable and the re-vendor rule makes the refresh mechanical; an un-stamped copy's origin decays into rumor.",
  "decision_change": "Any vendoring action becomes a two-file commit (copy + PROVENANCE stamp with source commit, blob SHA, re-vendor rule and SHA-check command) — instead of a bare copy.",
  "related": ["SN-0688", "SN-0692", "SN-1588"],
  "provenance": "hidden_files/twelve-lane-receipts/gap-lane-scorer-20261017-1850-lane0.md; hidden_files/js/supabase-bridge.js; hidden_files/js/supabase-bridge.PROVENANCE (source commit 8dad8451b9c5b39f0edd2278c8155eaad11a1b0b, blob SHA 262fa3ae4282af72325453b3f87f1530ce492542e962022769efb9ca5d39c939)"
}
```
