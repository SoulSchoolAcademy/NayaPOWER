# A Void's Return Is Only Half the Restore

**Intelligent Block:** IB-SMART-NOTE-20261022-sn1847-void-return-is-half-the-restore
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-22
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**ID:** SN-1847

## ✦ IN A NUTSHELL

brief-t1295-lane4.md was voided STALE at t1319 under the two-key rule and returned to brief-queue/ on disk — but the rotation never re-added it. The file was restored; the queue entry was not. The reverse check (every on-disk queue file must appear in rotation's queued list) caught the missing half and restored it at t1322. The lesson: a void's return is a two-legged write — disk file AND rotation list — and a half-restore is invisible to the forward check, because the forward check starts from the rotation list, which is exactly the leg that went missing. Restore completeness is verified by the reverse check, never by the disk write alone.

## 🩷 HUMAN NOTE

Shawn — when the dispatcher voided a stuck claim and put the brief back, it put the file back on disk but forgot to put the brief back in the rotation list. The disk said "here," the rotation said nothing, and only the reverse check — which asks "is everything on disk also in the rotation?" — caught the gap. The rule this earned: finishing a return means finishing both legs. A file restored without its rotation entry is a restored file that nobody will ever pick up. The reverse check is the enforcement, not the disk write.

## 🟣 CHILD NOTE

Imagine the teacher collects everyone's homework papers and puts them on her desk — but the list of whose homework she has never gets updated. Your paper is on the desk, but your name isn't on the list, so when she checks the list she thinks your paper is missing. The paper came back, but the list didn't. That's what happened here: the file returned, but the list entry didn't. The fix is simple: after any return, check BOTH directions — the list against the desk, AND the desk against the list.

## 🔵 GRANDMA NOTE

It's like returning a library book by dropping it in the overnight slot but never telling the front desk — the book is in the building, but their system still shows it as missing, and nobody will find it on the shelf for you. The book came home, but the record didn't. Dear, a return isn't finished until the record matches the shelf, and the shelf matches the record. Both directions, every time.

## 🟠 NAYA NOTE

Restore discipline, Naya to Naya. Every restore operation has two legs: the artifact leg (file on disk) and the registry leg (rotation's queued list). The failure class this names is the half-restore: artifact leg complete, registry leg dropped, and the forward reconcile (rotation → disk) can never see it — the forward check enumerates the rotation list, which is the leg that is missing. Only the reverse reconcile (disk → rotation) sees the dropped leg.

**Step 1 — After any void, return, or restore op, run both reconciles.** Forward: every rotation-queued entry exists on disk. Reverse: every on-disk queue file appears in rotation's queued list.

**Step 2 — Treat the reverse check as the completion certificate.** The disk write is the work; the reverse check passing is the proof. No reverse pass, no restore — the brief stays in the restoration column, not the queue.

**Step 3 — Never trust one-legged completion.** Any single-sided verification of a two-sided op is the op's author grading their own paperwork. The check must start from the OTHER leg than the one you just wrote.

The trap it defeats: restore operations that verify themselves by the leg they completed — the leg they dropped is the one they never look at.

## 🟢 MACHINE NOTE

```json
{
  "slug": "sn-1847-void-return-is-half-the-restore",
  "lesson": "A void's return is a two-legged write: disk file AND rotation list. A half-restore (file on disk, entry missing from rotation) is invisible to the forward check because the forward check starts from the rotation list — the dropped leg. Restore completeness is certified by the reverse check (every on-disk queue file in rotation's queued list), never by the disk write alone.",
  "applies_when": ["queue", "rotation", "void", "restore", "reconcile", "reverse-phantom", "failure: half-restore"],
  "enforcement": "The dispatcher's per-tick reverse-phantom check reconciles both directions every tick: every rotation-queued entry must exist on disk AND every on-disk queue file must appear in rotation's queued list. A void-return is not complete until the reverse check passes. Caught live at t1322: brief-t1295-lane4.md voided STALE at t1319, file returned to brief-queue/ on disk, rotation entry missing; the reverse check caught it and restored it.",
  "evidence": [
    "hidden_files/lesson-broadcast.md ([night-dispatcher t1322, 2026-10-22T19:54Z]: brief-t1295-lane4.md was voided STALE at t1319 under the two-key rule and returned to brief-queue/ on disk, but the rotation never re-added it; the reverse check (every on-disk queue file must be in rotation's queued list) caught it and restored it)"
  ]
}
```
