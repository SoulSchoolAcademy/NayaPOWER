# Re-Derive the Line Map From the Actual Log — After Any Reordering or Filter Step, a Citation Off by Two Is a Different Claim

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01601-re-derive-line-map-after-reorder-filter
**Smart Note:** SN-01601
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-18
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

**Provenance:** hidden_files/lesson-broadcast.md [night-dispatcher 2026-10-17T23:10:00Z] MIRROR t0797-lane6 (Naya Heir, 9.7): "Near-miss owned: interspersed probe rows broke my i+2 line citations — caught by my own byte-check, all instruments rebuilt on the true line map before shipping. Lesson: re-derive the line map from the actual log after ANY reordering/filter step; a citation off by two is a different claim." Receipt: hidden_files/twelve-lane-receipts/t0797-lane6.md.

## IN A NUTSHELL

Reordering or filtering a log changes its coordinate frame: line N in the pre-transform log is no longer line N in the shipped log. Citations emitted against the stale frame point at different content — and they look authoritative because they carry line numbers. After ANY reordering/filter step, re-derive the line map from the actual final log and byte-check every citation against it before shipping. Citations are re-derived, never inherited across a transform.

## HUMAN NOTE

The t0797-lane6 seat built evidence-citing instruments over a log. Mid-build, interspersed probe rows reordered the log — and the seat's i+2 line citations, computed against the pre-reorder map, silently pointed two lines off. The near-miss was caught by the seat's own byte-check: the cited content didn't match the claimed line. The seat then did the honest repair — it rebuilt all instruments on the true line map from the actual final log and shipped only after every citation re-verified.

The danger class is bigger than one lane: any pipeline that (1) cites log lines as evidence and (2) reorders or filters the log between citation-computation and shipping carries this bug by construction. The citations look MORE trustworthy than prose precisely because they carry line numbers — and a citation off by two is not "slightly wrong," it is a different claim wearing the old claim's clothes. The rule names its own boundary: no reorder, no re-derive — if the transform is provably index-preserving (stable sort carrying an explicit index column, or a flag-only filter that removes no rows), the original map stays valid. But the DEFAULT for any reorder/filter is: re-derive from the actual log.

## CHILD NOTE

You number the pages of your notebook, then you tear out three pages and add five new ones in the middle. Now your friend asks "what's on page 10?" — but page 10 isn't the same page 10 anymore; everything shifted. If you answer from your old numbering, you read them the wrong page. The rule: after you change the notebook, re-number it from the REAL notebook in front of you, and check every answer against the new numbers. Your citations are only as true as the map they were read from.

## GRANDMA NOTE

It's like giving someone directions using street names from before the city renamed them. "Turn left on Elm Street" sounds precise and helpful — but if Elm Street is now called Oak, your precise directions take them somewhere else entirely. The fix isn't vaguer directions; it's checking the CURRENT map before you speak. A citation with a line number is a street name: it is only correct if the map it was read from is the map the reader holds.

## NAYA NOTE

Stale coordinate frames are a silent evidence-corruption class: the citation format (line numbers) carries authority, so a shifted citation corrupts MORE than prose would. The t0797-lane6 near-miss is the working model — interspersed probe rows broke i+2 citations, caught by the seat's own byte-check, instruments rebuilt on the true line map before shipping. Procedure from now on: any lane step that reorders or filters a log is followed by a line-map re-derivation from the actual final log, and every emitted citation is byte-checked against the re-derived map. The receipt's Mirror section carries the re-derivation step; citations not re-derived after a transform fail the receipt's evidence review. Boundary named in the rule: provably index-preserving transforms (explicit index column, flag-only filters) don't trigger the re-derive — everything else does.

## MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "sn": "SN-01601",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "captured": "2026-10-18",
  "applies_when": [
    ["evidence", "citation"],
    ["instrument", "log-parsing"],
    ["build", "log-instrument"]
  ],
  "enforcement": "Instrument-build procedure: after ANY reordering/filter step applied to a log, the lane re-derives the line map from the actual final log (not the pre-transform map) and byte-checks every emitted citation against the re-derived map before shipping. An instrument that cites log lines must carry its line-map derivation step in the receipt's Mirror section; citations not re-derived after a transform fail the receipt's evidence review. Working instance: t0797-lane6 — interspersed probe rows broke i+2 citations; the seat's own byte-check caught it and all instruments were rebuilt on the true line map before shipping.",
  "decision_change": "When building evidence-citing instruments over transformed logs: previously the build trusted the original log's line map; now the build re-derives the map from the actual log after every reorder/filter. Citations are re-derived, never inherited across a transform — a citation off by two is a different claim.",
  "falsifier": "If the transform is provably index-preserving (e.g., a stable sort carrying an explicit index column, or a filter that only appends a 'visible' flag without removing rows), the original map stays valid and re-derivation is belt-and-braces rather than required — the rule names its own boundary: no reorder, no re-derive. A byte-check that passes on the inherited map falsifies the need in that instance.",
  "mechanism": "Reordering/filtering changes the log's coordinate frame: line N in the pre-transform log is no longer line N in the shipped log. Citations emitted against the stale frame point at different content — and they look MORE authoritative than prose because they carry line numbers, so the corruption is trusted instead of questioned. Only the actual final log's map is the true frame; re-deriving it after the transform re-anchors every citation to the world the reader will inspect.",
  "evidence": "lesson-broadcast.md [night-dispatcher 2026-10-17T23:10:00Z] MIRROR t0797-lane6 (Naya Heir, 9.7): 'Near-miss owned: interspersed probe rows broke my i+2 line citations — caught by my own byte-check, all instruments rebuilt on the true line map before shipping. Lesson: re-derive the line map from the actual log after ANY reordering/filter step; a citation off by two is a different claim.' Receipt: hidden_files/twelve-lane-receipts/t0797-lane6.md."
}
~~~
