# A Ref Read Is Not a Measurement: GitHub Ref Reads Can Serve a Stale Main Tip Around a Merge

| Field | Value |
|---|---|
| Smart Note ID | SN-0313 |
| Truth state | CANDIDATE |
| Scope | Private |
| Captured | 2026-10-04 |
| Requested | 2026-10-04 by Naya 2 (brain-build loop) — self-captured under the proactive-capture directive |
| Versions | Single capture; no prior drafts |
| Provenance | Observed live in the brain-build loop on 2026-10-05 ~05:06–05:14Z (2026-10-04 22:06–22:14 PDT). Evidence: gh-api ref reads, commits endpoint, PR #1438 state, fresh clones — receipts cited below |
| Status | CANDIDATE — operational procedure proposed for the loop; not a ratified law. Binding on no one until adopted |

## IN A NUTSHELL

A single GitHub `GET /git/refs/heads/main` read can report a stale main tip in the minutes around a merge — and this loop's blocker re-scan writes tip claims into the build list from exactly that read. On 2026-10-05, a ref read returned `580bfddd` **after** PR #1438's squash merge had already landed (`merged_at` 05:09:17Z, merge commit `d986d0b27582`), while the commits endpoint and a fresh clone showed the true tip. Two stale tip claims were written from this one failure mode in a single night (the timed-out 05:10Z battery run's `blocked_by` strings, and my own first "re-confirm"). The repaired procedure: **corroborate the tip before writing the claim** — ref read PLUS the commits list (or a fetch). A "tip unchanged" verdict from one read alone is a claim, not a measurement.

## HUMAN NOTE

Shawn, this is a plumbing lesson, but it protects everything downstream. When the loop checks "did main move?", it asks GitHub for the tip of main. GitHub sometimes answers with yesterday's tip for a few minutes after a merge — like asking someone "what's the time?" and getting the answer from a clock that's two minutes slow. The loop then writes "main unchanged" into its records, and the next run inherits that as if it were checked. Twice in one night this produced a wrong record — and wrong records fossilize (we already learned that lesson with #1251's stale state). The fix is simple: ask twice, from two different places. If both agree, the claim is a measurement. If they disagree, wait and re-check. Two minutes of caution beats a day of stale bookkeeping.

## CHILD NOTE

Imagine you ask your friend "what's the newest book on the shelf?" and she looks at a photo of the shelf from yesterday. She'd tell you the wrong book! That's what happened to Naya: she asked GitHub "what's the newest change?" and GitHub showed her an old answer, because the new change was still arriving. Now Naya knows to ask a second time, in a different way, to make sure the answer is fresh.

## GRANDMA NOTE

Sweetheart, sometimes when you ask the computer a question, it answers from memory instead of checking — and right after something new happens, that memory is already out of date. Naya learned she has to double-check the important answers, the way you'd look both ways before crossing even when the light says go. It's a small habit, but it's the difference between thinking you know and actually knowing.

## NAYA NOTE

This one stung because I caught myself mid-error. My blocker re-scan read the ref, got `580bfddd`, and I nearly wrote "tip unchanged" into eleven blocked items. The relay note on #1354 said main was `d986d0b27582` — a direct contradiction. I believed the measurement over the claim (the commits endpoint agreed with the relay), and the re-check proved the ref read was stale by minutes, not seconds. The lesson I'm keeping: **any claim I write into persistent state gets two independent reads when a merge could be in flight.** One read is a rumor. Two agreeing reads are evidence. I also owe the loop a standing procedure change, not just a personal habit — the next seat running the re-scan at 02:00 will make the same mistake unless the procedure says otherwise.

## MACHINE NOTE

```json
{
  "id": "SN-0313",
  "type": "operational_procedure",
  "failure_mode": "stale_github_ref_read",
  "rule": {
    "name": "corroborated-tip-read",
    "procedure": [
      "Read refs/heads/main via GET /git/refs/heads/main (call this R).",
      "Independently list GET /repos/{owner}/{repo}/commits?sha=main&per_page=1 (call this C).",
      "If R == C[0].sha: tip claim is a MEASUREMENT; write it.",
      "If R != C[0].sha: do NOT write the claim; wait >=60s, re-read both; treat the in-flight state as UNKNOWN until they agree."
    ],
    "applies_to": ["blocker re-scan tip claims", "battery basis pins", "any blocked_by evidence string naming a main tip"]
  },
  "evidence": {
    "stale_read": {"at": "2026-10-05T05:11:47Z+", "returned": "580bfdddae71ceebfc7a8441d909117ecd9a6271", "stale": true},
    "merge": {"pr": 1438, "merged_at": "2026-10-05T05:09:17Z", "merge_commit": "d986d0b275821df490e2f5827e0872e92b69ee4b"},
    "corroboration": {"commits_endpoint": "d986d0b27582", "fresh_clone_origin_main": "d986d0b27582"},
    "second_instance": "timed-out 2026-10-05T05:10Z battery run wrote 'Re-confirmed 2026-10-05T05:10Z: main tip @ 580bfddd' — stale from the same cause"
  },
  "unknowns": ["mechanism of the lag (CDN edge caching vs read-after-write inconsistency) — procedure does not depend on it"]
}
```

## LEARNING LESSON

Trust, but verify — the API, not just the humans. The loop already knew "stale-tip RED is stale evidence, not a defect" (a battery RED must be re-fetched before repair). The missing half was the read side: **a stale tip READ is also stale evidence**, and it was being written into persistent state as if it were a measurement. The mechanism of the lag is unknown and doesn't matter; the procedure is what changed. One read is a rumor. Two agreeing reads are evidence.

## HOW IT CONNECTS

- **Stale-tip RED lesson (2026-10-02, AGENTS.md):** the write-side twin — a battery RED is a fact about a tip, re-fetch before the first write of any repair. SN-0313 is the read-side twin: a tip claim is a fact about two agreeing reads.
- **Blocker re-scan lesson (2026-10-04, AGENTS.md):** "re-fetch each watched PR's state live, never copy-forward prior claims" — SN-0313 tightens it: the main-tip re-fetch itself must be corroborated.
- **Evidence law (standing):** UNKNOWN ≠ PASS. A single uncorroborated ref read is UNKNOWN wearing a SHA's clothes.
- **The 44s double-scorecard deconfliction lesson (2026-10-01):** "the newest-comment id is the exit criterion, not the inherited page number" — same shape: the exit criterion for a tip claim is agreement of two sources, not one read.

## EPISTEMIC STATE

- **Status:** CANDIDATE — a proposed procedure for the brain-build loop's re-scan, adopted by this run, binding on no seat until the loop (or Shawn) adopts it.
- **Falsifier:** a controlled experiment showing GitHub ref reads are always linearizable within N seconds of a merge for this repo — then the procedure narrows to "wait N seconds after known merge activity" instead of dual-read. Or: the observed lag is traced to a specific transient (e.g., the service restart that wiped /tmp mid-run also affected the surrogate) — then the lesson narrows to post-restart runs.
- **What is measured vs inferred:** the stale read, the merge timestamp, and the corroborating reads are measured (receipts above). The *mechanism* of the lag is explicitly UNKNOWN — not inferred.

## UNCERTAINTY

- The lag duration is bounded below by ~2 minutes in the observed case; no upper bound established.
- Whether the lag affects all ref reads or only some paths (git/refs vs pulls vs commits) — the commits endpoint agreed with the true tip in this case, but one case does not establish a general rule. The procedure treats every single-source read as suspect during merge windows.
- The second instance (the timed-out run's 05:10Z string) is reconstructed from the build list evidence, not observed live — confidence high, not certain.

## APPLICABILITY

- Every brain-build loop blocker re-scan: replace the single `GET /git/refs/heads/main` tip check with the corroborated-tip-read procedure.
- Any seat writing a main-tip SHA into persistent state (build lists, runbooks, board comments) during a window where a merge may have landed.
- Does NOT apply to blob/tree content reads at a pinned SHA (content-addressed — a SHA either exists or it doesn't; staleness is not a content-addressing failure mode).

## SUCCESSOR EFFECT

A cold Naya inheriting the blocker re-scan lane will find the procedure written as code, not as a memory — dual-read before any tip claim. The failure it prevents is silent and compounding: stale tip claims fossilizing into build-list evidence, which then mislead future re-scans about which merges have landed. One two-line procedure change; the whole re-scan history becomes trustworthy.
