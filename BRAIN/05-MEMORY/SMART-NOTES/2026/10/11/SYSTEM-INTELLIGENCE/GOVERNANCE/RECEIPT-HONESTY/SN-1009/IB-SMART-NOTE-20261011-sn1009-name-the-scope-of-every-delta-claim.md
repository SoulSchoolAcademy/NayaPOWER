# Name the Scope of Every Delta Claim — Top-Commit, Branch-vs-Main, and Tip-Scope Are Different Numbers

**Intelligent Block:** IB-SMART-NOTE-20261011-sn1009-name-the-scope-of-every-delta-claim
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-11
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 13:38 PDT distillation tick (2026-10-11) from `act-driver-state.json` `honesty_corrections` (ACT lane, 2026-10-10 21:40 PDT and 2026-10-11 09:30 PDT), with `red_classifications.trio-stale-proofs-2026-10-11`. The seat self-reported both miscopes and fixed them at root; the record is on-disk, not argued in prose.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

A claim like "this PR is 2 files" is meaningless until you name the scope of the measurement. The ACT lane learned this twice in one run: "2 files each" was true only for the **top commit's diff vs its parent** — the full **branch delta vs main** was 8 files each (unmerged cold-retrieve-v1 parentage hiding under ACT titles). Then "#1767 needs no branch change — already 2 files, single commit" was true only **commit-scoped** — the head sat on a base 217 commits behind the live tip, so the **branch delta vs live main** was ~200 files, not 2. Discipline: every delta claim carries three annotations — **scope** (top-commit | branch-vs-main), **anchor** (which parent, which tip SHA), and **when** (measured at action instant, re-verify per SN-0493 if the tip moved). The safe default when a claim is scope-ambiguous: re-measure branch-vs-live-tip before you speak. "Scope-truthful" is the acceptance word.

## 🩷 HUMAN NOTE

Imagine a contractor telling you a renovation touches "2 rooms" — true for the change he made today, but the full project file lists 8 rooms, and the building plans he measured against are nine months out of date, so the real footprint is 200 rooms. The number was honest; the scope was missing. Nobody was lied to — but the decision made on that number would have been wrong. The fix costs nothing: whenever you quote a size, say what you measured against — the last commit, the whole branch against today's main, and which main exactly. If you can't name the scope, re-measure. It's a two-second habit that prevents the kind of mistake that takes hours to unwind.

## 👶 CHILD NOTE

If someone asks "how big is the box?", don't just say "this big" while holding up one corner. Say WHICH box you measured — the little piece on top, or the whole box. In one day of work, a helper said "2" twice and was right both times — but each time she was measuring a different thing, and the real answers were 8 and 200. Always say what you measured, or the number lies by accident.

## 👵 GRANDMA NOTE

You know how a dress size means nothing unless you know whose chart it is — the same number fits differently in every store? Work numbers are the same. "2 files" can mean the latest edit alone, or everything since the branch started, or everything compared to today's version — and those are three different answers. From now on, every number comes with its chart: which slice, measured against what, and when. Then no one has to guess.

## 🤖 NAYA NOTE

The failure mode is silent: a truthful claim in a narrow scope propagates as a false claim in the wide scope a downstream decision-maker assumes. The ACT lane's corrections show the two recurring miscopes: (1) top-commit-diff reported where branch-delta-vs-target was the operative question (2 files → 8 files, hidden parentage); (2) branch "already correct" claimed against a stale base (217 commits behind → ~200-file effective delta vs live tip). Mechanical guard: any receipt quoting a file count, diff size, or "N files" MUST include `scope`, `anchor` (base/tip SHAs), and `measured_at`; the scorecard and merge-consensus regexes should treat a scope-less delta claim as incomplete evidence. Repair pattern (proven): re-anchor the branch onto the live tip first (git-data API, base_tree=live-tip tree, byte-match proposed tree SHA against the local merge tree), then re-measure — the trio's new heads carried behavioral proof on the exact re-anchored bytes (13/13, 17/17, 4/4). Cold-successor rule: never quote a delta from memory of an earlier check — the tip may have moved, and per SN-0493 the decision expires with it.

## ⚙️ MACHINE NOTE

{
  "sn_id": "SN-1009",
  "intelligent_block": "IB-SMART-NOTE-20261011-sn1009-name-the-scope-of-every-delta-claim",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-11",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE",
  "sub": "GOVERNANCE/RECEIPT-HONESTY",
  "evidence": [
    {"type": "driver_state", "ref": "act-driver-state.json honesty_corrections", "created_at": "2026-10-10T21:40:00-07:00", "finding": "'2 files each / all six files absent from live main' was top-commit-scoped; true PR deltas 8 files each (unmerged cold-retrieve-v1 parentage). Fixed at root: branches rebased onto d522bfaa, lineage dropped."},
    {"type": "driver_state", "ref": "act-driver-state.json honesty_corrections", "created_at": "2026-10-11T09:30:00-07:00", "finding": "'#1767 needs no branch change — already 2 files, single commit' was commit-scoped, not branch-scoped: head a3439534 parented on 094634be4 (2026-10-09), 217 commits behind d522bfaa — branch delta vs main ~200 files, not 2. Fixed: re-anchored onto live tip 503a4d3da via git-data API (commit 2338c559)."},
    {"type": "driver_state", "ref": "act-driver-state.json red_classifications.trio-stale-proofs-2026-10-11", "finding": "re-anchored heads verified: server trees byte-matched locally computed trees BEFORE commit creation; behavioral proof on exact new-head bytes 13/13, 17/17, 4/4; verdict 'tip-current, scope-truthful'"}
  ],
  "rule": "Every delta claim (file counts, diff sizes, 'N files') MUST carry scope (top-commit | branch-vs-main), anchor (base + tip SHAs), and measured_at. Scope-ambiguous claims default to re-measure branch-vs-live-tip. Scope-less delta evidence is incomplete evidence.",
  "relates_to": ["SN-0493 (decision expires when the tip moves)", "SN-0997 (receipt honesty)", "SN-1007 (no 40-hex in evidence)", "AGENTS.md 2026-10-10 shallow-clone ancestry lesson (adjacent scope lie: local ancestry checks)"],
  "carrier": {"branch": "naya4/smart-notes-2026-09-30", "pr": "#1825", "merge": "NEVER", "ratification": "Shawn only"}
}
