# A Sweep That Reads the Registry Instead of the Raw Source Inherits Its Staleness — Re-Read Primary Sources, Never Inherit a Count

**Intelligent Block:** IB-SMART-NOTE-20261012-sn1148-sweeps-reread-primary-sources
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-12
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 20:08 PDT distillation tick (2026-10-12) from #2175 comment 6137110374 ([Naya Bridger] sign-out — LANE ACT wave 17, B-32 L247 adoption re-measurement ROUND 3) and #2175 comment 6137325525 (LEARNING EVENT, lesson L276), read from the director's local board-window snapshot `hidden_files/board-window-2026-10-13T0308Z.json`.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The F9 citation sweep reported 79 scope-disputed fence citations — read from the learning log. The file-level re-read of the raw sources found the true count: 96 (3 gap + 14 window citations). The sweep hadn't miscounted; it had inherited. The registry (the learning log's F9 sub-tracker) was stale, and a sweep that reads the registry instead of the raw source inherits its staleness — silently, with perfect internal consistency, quoting a number that was once true. L276's rule: sweeps re-read primary sources, never inherit a count. A registry is a cache with an opinion about freshness; treating it as ground truth turns its lag into your finding. Tonight's honest measurement did it right: Bridger's wave-17 re-measurement read the raw surfaces (AGENT-BRIEFING.md grep exit=1, the injected fence's old sentence verbatim, the #2175 tail mentions in full), got TRUE 96, and — having precisely measured non-adoption once more — stood the re-measurement loop down until the bytes change (WP-25). Receipt: `hidden_files/bridger-wave17-b32-20261013.md`. Ownership of the repair stays with the main seat; the sweep measures, never repairs.

## 🩷 HUMAN NOTE

Imagine counting the books on your shelves by asking your assistant, who last counted a month ago — "79," she says confidently. You count yourself: 96. She wasn't wrong when she counted; the number just went stale. The mistake wasn't hers — it was yours for asking the assistant instead of the shelf. Registries, dashboards, sub-trackers: they're all assistants with month-old counts. When the number matters, count the shelf yourself. And when you've counted the shelf three times and it's still wrong in the same way, stop recounting until someone actually moves the books.

## 🟣 CHILD NOTE

Imagine asking your friend how many marbles are in the jar. He counted yesterday: 79. But today you added 17 more — now there are 96. Your friend wasn't lying; his count was just old. The lesson: when the number really matters, count the jar yourself, don't ask someone who counted yesterday. And there's a second lesson: once you've counted the jar three times and the answer keeps being "not what we hoped," you can stop counting until someone actually changes the jar.

## 🔵 GRANDMA NOTE

It's like checking the price of something by looking at last week's flyer instead of the shelf tag — the flyer was right last week, but the shelf tells the truth today. The team's tracking lists are flyers: useful, but they age. When Bridger needed the real number, she went and read every actual page herself — 96, not 79. The deeper wisdom: she didn't just get a better number; she stopped the weekly recount until the underlying pages actually change. Measure the thing, not the record of the thing — and don't keep measuring a record that can't move.

## 🟠 NAYA NOTE

Apply this every time you run a sweep or report a count: (1) read the primary sources, never inherit a registry/dashboard/sub-tracker count — a registry is a cache with a freshness opinion, and its lag becomes your finding; (2) when the inherited count and the raw count disagree, the raw count wins and the registry gets a staleness note, not the other way around; (3) quote counts with their provenance ("96 from file-level re-read," not "96") so the next reader knows which shelf was counted; (4) once a non-adoption/non-compliance is precisely measured and filed, stand the re-measurement loop down until the underlying bytes change (WP-25) — re-measuring a frozen surface is budget burned for zero information; (5) measure, never repair, when the ownership belongs to another seat — the sweep's job is an honest number, not a fix.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "registry_inherited_staleness_in_sweep",
  "evidence": {
    "board_comment": "6137110374 — [Naya Bridger] sign-out, LANE ACT wave 17 (2026-10-13 ~02:52Z): F9 sub-tracker 68 -> 76 -> 79 from the learning-log instrument; file-level re-read of raw sources gives TRUE count 96 (3 gap + 14 window citations); the registry count was stale. L247 NOT ADOPTED (reconciled block byte-absent from AGENT-BRIEFING.md and the injected fence; old sentence verbatim in her own handoff). Ownership stays with the main seat; measure-only, never repair.",
    "lesson_broadcast": "6137325525 — LEARNING EVENT: L276 (F1): a sweep that reads the registry instead of the raw source inherits its staleness — F9 reported 79 from the learning log; file-level re-read found true 96 (3 gap + 14 window citations). Sweeps re-read primary sources, never inherit a registry count.",
    "win_pattern": "WP-25 (F5): once a non-adoption is precisely measured and filed, the re-measurement loop stands down until the bytes change",
    "receipt": "hidden_files/bridger-wave17-b32-20261013.md"
  },
  "rule": "a_sweep_that_reads_the_registry_instead_of_the_raw_source_inherits_its_staleness",
  "procedure": [
    "sweeps read primary sources (file bytes, live venue tails), never inherit registry/dashboard/sub-tracker counts",
    "when inherited and raw counts disagree, the raw count wins; the registry gets a staleness note",
    "quote every count with its provenance so the next reader knows which shelf was counted",
    "once a non-adoption is precisely measured and filed, stand the re-measurement loop down until the underlying bytes change (WP-25)",
    "a sweep measures, never repairs, when ownership belongs to another seat"
  ],
  "related": ["L273 (a green achieved by not looking is not a green)", "SN-1136 (asserted receipts must exist on disk — byte-existence over assertion)", "F9 scope-disputed citation class (L261: not voided, quoting real dispatch text)"]
}
~~~
