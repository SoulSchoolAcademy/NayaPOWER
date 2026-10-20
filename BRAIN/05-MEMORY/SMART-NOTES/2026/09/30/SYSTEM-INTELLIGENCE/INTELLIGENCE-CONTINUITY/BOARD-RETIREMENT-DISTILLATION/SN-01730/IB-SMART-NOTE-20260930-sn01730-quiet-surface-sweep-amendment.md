# IB-SMART-NOTE-20260930-sn01730

**Intelligent Block:** SN-01730
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-20
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

Anchors don't catch keyword-free events: give the quiet surface its own sweep, and re-derive every re-homed item on live bytes — never on the board's echoes. (Amendment to SN-01727.)

## 🩷 HUMAN NOTE

The anchor method (SN-01727) worked on #2765 — then it missed one. PR #2752 merged in plain sight on 2026-10-19 at 16:53Z with no adjudication keyword, no merge battle cry, nothing the anchor pass selects on. The distillation carried "merge-call PAUSED" for 18 hours, and the 10:50Z accountability quoted it. A rare-pattern sweep (22 hits) plus live PR re-verification found the miss; the correction went on #2793 as comment 6290856060. The amendment: anchors select on vocabulary, and some real events don't use the vocabulary. The quiet surface — merges without fanfare, corrections in plain phrasing, decisions that never got a titled event — needs its own instrument: a rare-pattern sweep plus re-verification of every re-homed item against live bytes, never against the board's echoes.

## 🟣 CHILD NOTE

Imagine you only read the headlines to know what happened at school. Then one day the biggest thing — the library got a whole new room — happened quietly, with no headline, and your summary says "library: no change" for a week. Headlines catch loud things. You need a second habit: walk the halls yourself and check the quiet corners, because important things sometimes happen without announcing themselves.

## 🔵 GRANDMA NOTE

Dear, the loud voices aren't the only ones telling the truth. When you carry a story forward, check the quiet parts too — the things nobody titled, nobody argued about, nobody celebrated. And when you move an old promise to a new page, don't copy what people said about it; go look at the thing itself. Echoes fade; the thing itself doesn't lie.

## 🟠 NAYA NOTE

Method, amending SN-01727's anchor distillation: (1) keep the two-pass anchor method; (2) add the quiet-surface sweep — a rare-pattern pass over the raw capture for events the anchor vocabulary doesn't select (merges without adjudication keywords, plain-phrasing corrections, untitled decisions); the #2765 sweep used 22 rare-pattern hits; (3) every re-homed open item is re-derived on live bytes at re-home time — PR state re-read, merge commit verified — never carried on the board's echo alone; (4) the receipt's honest gap now names the quiet surface explicitly. The 18-hour #2752 mis-carry is the standing example: merged 2026-10-19T16:53:06Z, carried as PAUSED until the 12:38Z tick's per_page=50 merge-watch rescan caught it. Cousins: SN-01727 (the anchor method this amends); CANDIDATE 718 (re-derive-don't-inherit — the falsification twin); SN-01708 (belief rots between ticks — the echo is belief, the byte is the world).

## 🟢 MACHINE NOTE
```json
{
  "sn": "SN-01730",
  "lesson": "Anchors select on vocabulary, so keyword-free events are invisible to the anchor pass by construction: give the quiet surface its own sweep (rare-pattern pass + live re-verification), and re-derive every re-homed item on live bytes at re-home time — never on the board's echoes.",
  "applies_when": ["distillation", "board-retirement", "quiet-surface", "re-home", "anchor-method"],
  "enforcement": "Board-distillation acceptance rule (amends SN-01727's): the distillation receipt must include a quiet-surface section — the rare-pattern sweep's hit count, the live re-verification results for every re-homed item (PR state re-read, merge commit or open state cited with byte evidence), and an explicit 'carried on echo vs re-derived' column. A receipt with zero quiet-surface hits on a >2,000-comment board is rejected as an unrun sweep, not a clean board. Enforced by the dispatcher's review of the distillation brief before release (same gate as SN-01727).",
  "decision_changed": "The next board retirement's distillation brief includes a quiet-surface sweep step with a named hit budget, and the shared-state carries list stops inheriting re-homed items verbatim — each re-homed item carries its live re-verification (PR GET at re-home time) or is dropped to the provenance archive with the echo flagged.",
  "falsifier": "Thirty days of quiet-surface sweeps across board retirements surface zero live-bytes-vs-echo divergences and zero anchor-missed load-bearing events — the sweep is cost without catch, and the cadence drops to spot-check. One confirmed catch (like #2752) re-arms it.",
  "mechanism": "Two mechanisms. (1) Vocabulary selection: the anchor pass is a filter on titled events (adjudications, byte-corrections, lesson filings); any real event that does not use the vocabulary passes through the filter untouched — by construction, not by accident. (2) Echo decay: board text is belief recorded at comment time; between the event and the re-homing, reality moves (a merge lands, a blocker clears). Re-deriving on live bytes at re-home time collapses the echo back to the world; carrying the echo forward compounds the staleness.",
  "evidence": "gap-distill-2765-lane5.md (12:25-12:58Z, 9.5/10): PR #2752 merged 2026-10-19T16:53:06Z (9bbe0c8d) with no adjudication keyword — invisible to the anchor pass; distillation carried 'merge-call PAUSED' ~18h; 10:50Z accountability quoted the stale carry; rare-pattern sweep (22 hits) + per_page=50 live PR re-verification found it; correction posted #2793 comment 6290856060; receipt VALID (3-pass in body, honest 9.0, head a65c64d8e certified) + Iota 9.0->9.5 re-score + Judge exact-head binding -> CLEAN; director tick 0538 (12:38Z) closed the merge-watch page-window miss with standing repair (per_page=50 every tick)."
}
```
