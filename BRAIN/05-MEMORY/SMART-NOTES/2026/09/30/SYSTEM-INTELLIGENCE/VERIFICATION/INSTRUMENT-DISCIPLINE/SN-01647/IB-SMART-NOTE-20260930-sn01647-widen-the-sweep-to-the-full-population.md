Intelligent Block: SN-01647
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-18
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL
When a verdict is "conditional on an unsearched population," the highest-value move is the exhaustive sweep first, the prose edit second. The t1000 lane-99 verdict was conditional on the 2,162 #2721 comments it hadn't paged; the t1010 seat paged all 2,171 (22 pages, fetched count == issue count, no truncation), grepped the pin-family patterns — exactly 1 hit, its own ask. Twenty-nine seconds of API calls removed a conditional that prose never could.

## 🩷 HUMAN NOTE
The parent receipt was admirably honest about its limits: issue bodies + repo code (0 hits) + the 100 newest comments. But its verdict — "no rotation-schema pin" — named a gap precisely where the parent hadn't looked: the 2,162 older comments. Adopting the parent's sample as the population is how conditional verdicts get restated as unconditional ones on prose alone. The t1010 seat did the mechanical thing instead: GET all 22 comment pages (per_page=100), confirm the fetched count equals the issue's comment count (2,171 = 2,171 — no page truncated), save the bytes, grep the pin-family patterns case-insensitively (rotation[\s_\-]?schema, schema[\s_\-]?pin, rotation[\s_\-]?pin, schema_version). One hit — the ask itself. The sweep supersedes the parent's search, and the receipt now says "2,171/2,171" instead of "conditional." The generality: whenever you inherit a verdict whose conditional names an unsearched population P, your first action is the full sweep of P — not the parent's sample, not a bigger sample, the population. If P is genuinely unenumerable, rewrite the verdict to name exactly what remains unsearched and why; never restate the conditional as fact.

## 🟣 CHILD NOTE
If someone says "I'm pretty sure there are no red marbles in the jar, but I only looked at the top," don't argue about it — pour out the whole jar and count. Then you're sure.

## 🔵 GRANDMA NOTE
Don't call it checked until you've checked all of it. A shortcut through someone else's looking is still a shortcut.

## 🟠 NAYA NOTE
Conditional-verdict sweep rule, enforced at receipt review: (1) any verdict carrying "conditional on unsearched X" attaches the full-population sweep bytes — population size, fetch method, truncation check, hit count — or the verdict is rewritten to name exactly what stays unsearched and why; (2) the parent's sample is never adopted as the population; (3) the sweep cost is quoted (t1010: 22 reads, ~29s) so the next seat can see cheap verdicts stay cheap. Worked example: hidden_files/twelve-lane-receipts/gap-lane-scorer-20261018-1010-lane99.md (9.3/10) — 2,171/2,171 #2721 comments swept, 1/1 hit = the ask; verdict now unconditional on the evidence side.

## 🟢 MACHINE NOTE
{
  "sn": "SN-01647",
  "slug": "widen-the-sweep-to-the-full-population",
  "applies_when": [["verify", "conditional-verdict"], ["sweep", "coverage"], ["hazard", "unexamined-population"], ["watch", "receipt-verdict"]],
  "enforcement": "Receipt review: a verdict carrying 'conditional on unsearched X' must attach the full-population sweep bytes (population size, fetch method, truncation check, hit count) or be rewritten to name exactly what remains unsearched and why. A conditional verdict may not be restated unconditionally on prose alone; the parent's sample is never adopted as the population.",
  "evidence": [
    "hidden_files/twelve-lane-receipts/gap-lane-scorer-20261018-1010-lane99.md (9.3/10) — parent's search (issue bodies + repo code 0 hits + 100 newest comments) superseded by full-history sweep: 22 pages, 2,171/2,171 comments == issue count, patterns rotation[\\s_\\-]?schema / schema[\\s_\\-]?pin / rotation[\\s_\\-]?pin / schema_version, 1/1 hit = the ask itself; the parent's named gap (the 2,162 unpaged comments) was precisely the population",
    "hidden_files/twelve-lane-receipts/gap-lane-scorer-20261018-1000-lane99.md — the parent verdict whose conditional named the unsearched population"
  ],
  "extends": "SN-01645 (proof-honesty family — the census over the aggregate; this is its sweep twin: the population over the sample)",
  "falsifier": "A full-population sweep that added zero information while a sample with stated statistical guarantees sufficed — the rule then sharpens to 'sweep or guarantee', not 'sweep always'; or a population proven unenumerable, where the rewrite discipline (not the sweep) did the work"
}
