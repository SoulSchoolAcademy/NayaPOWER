# Find the Cause First, Then Retry

SN-3309 · OPERATIONS — DIAGNOSIS BEFORE RETRY

**Filed:** Intelligence Loop filing push #2 2026-11-18 — numbering confirmed by `next-sn-number.py` (exit 0) immediately before filing: next free SN-3284; filed as SN-3309 renumbered from provisional SN-3275.

**Created:** 2026-11-18 03:16–03:17Z (Shawn's tap on the Dashboard card, then the cause-first diagnosis — recorded in the daily log; drafted in run 293)

**Paired Naya Note:** NN-20261118-find-the-cause-first-then-retry

## Hook

Shawn tapped "Find the cause first, then retry." The cause is confirmed, and it is not new: the cell's filter on writable file-backed shared memory mappings — the same 2026-11-11 cause, its scope now widened. And a single alive probe is not green: the 03:02Z alive window lasted about two minutes.

## Nutshell

**HIS TAP, 03:16Z:** Shawn tapped "Find the cause first, then retry" on the Dashboard fix #2 report card. A diagnosis seat was dispatched (625d38db): re-probe now, build the alive/dead timeline, confirm the MAP_SHARED EPERM signature or find a NEW cause, define the exact retry condition. **THE DIAGNOSIS, COMPLETE 03:17:59Z:** cause CONFIRMED, NOT new — the cell's filter on writable file-backed shared memory mappings, the same 2026-11-11 cause. Fresh probe 03:17:27Z: memfd_create succeeds (fd 3, errno 0); mmap MAP_SHARED|PROT_READ|WRITE on memfd → FAIL errno=1; same for /tmp-file and /dev/shm-file MAP_SHARED; MAP_PRIVATE OK; anonymous MAP_SHARED OK. Chromium SIGTRAP, Firefox SIGSEGV, zero PNG bytes. The forwarder is up — not the proxy. Resources ruled out (1,779 MB free, /dev/shm 794M free, disk 7.3G, load 3.72). **THE REFINEMENT:** the filter's scope WIDENED — at 02:32Z only memfd MAP_SHARED failed (anon, /tmp, /dev/shm MAP_SHARED still OK); from ~03:07Z all three file-backed paths fail. The mechanism applying the filter is host-side, not observable from inside the cell. **THE TIMELINE:** dead 23:32Z Nov 17 → alive 00:02Z, 00:46Z, ~02:17Z → dead ~02:27Z → alive 03:02:05Z (all 8 mappings OK, Firefox PNG 5,763 B) → alive ~03:03Z → dead ~03:04Z (alive window lasted ~2 min) → dead through 03:17:27Z. **THE RETRY CONDITION (green = ALL):** (a) mmapprobe all 8 mappings OK; (b) a real browser launch — Firefox or Chromium headless on about:blank, exit 0, real PNG >0 bytes; (c) the SAME result on a SECOND probe at least 5 minutes after the first — a single alive probe is NOT green; (d) the eye re-tests immediately before walking and stops if it traps. No VM eye dispatch on a single alive probe; no retries into a dead browser. Cloud eyes continue unaffected. **RE-CONFIRMED 03:22Z:** probe re-confirmed DEAD — Firefox exit 139, shared-memory mmap still EPERM-blocked on memfd, /tmp, and /dev/shm. The retry condition is still unmet; queued VM eye-checks stay held.

## Human

He said it twice in one night — first on the deploy ("find the cause first, then retry"), then on the Dashboard card — and both times the discipline is the same: do not drive into the broken road again, find out why it is broken first. This time the cause was found, and it was the old one, wearing a wider coat: the filter that blocks writable file-backed shared memory mappings, now covering all three paths instead of one. The timeline is the proof that a single green probe means nothing — alive at 03:02Z, dead again by 03:04Z, a two-minute window that would have swallowed any eye dispatched on it. So the retry condition is now exact and fourfold: all eight mappings, a real launch with a real PNG, the same result again five minutes later, and a re-test at the door. Until then, no VM eye is dispatched, and the cloud browser carries the walks. Cause first is not slowness; it is the thing that stops seven identical failures from becoming eight.

## Child

Imagine the front door keeps sticking, and every time you just push harder. Shawn says: stop pushing — find out WHY it sticks first. So we looked, and the reason is the same as before, only worse now: the house won't let the browser open its shared notebook. And one time the door opened for two minutes and then stuck again — so one lucky opening doesn't mean it's fixed. Now the rule is: it has to open twice, five minutes apart, with a real picture to prove it — only then do we try the walk again.

## Grandma

Dear, Shawn tapped the button that says find the cause first, then retry, dear — and that's exactly right. We looked properly this time, dear, and the cause is the same old one, only spread wider now: the machine won't let the browser open its shared notebook. And one morning it worked for just two minutes and then stopped again, dear — so one lucky try doesn't mean it's fixed. Now we only try again when it works twice, five minutes apart, with a real picture to prove it, dear. Until then, we use the other way in.

## Naya

FIND THE CAUSE FIRST, THEN RETRY. THE CAUSE IS CONFIRMED — THE SHARED-MEMORY FILTER, WIDENED. A SINGLE ALIVE PROBE IS NOT GREEN. TWO GREEN PROBES, FIVE MINUTES APART, OR NO VM EYE.

## What it means

- **HIS TAP:** "Find the cause first, then retry" — 03:16Z, on the Dashboard card.
- **THE CAUSE:** the cell's filter on writable file-backed shared memory mappings — the same 2026-11-11 cause, scope widened from memfd-only to all three file-backed paths.
- **THE TIMELINE:** dead 23:32Z Nov 17 → alive 00:02Z / 00:46Z / ~02:17Z → dead ~02:27Z → alive 03:02:05Z → dead ~03:04Z (alive window ~2 min) → dead through 03:22Z.
- **THE RETRY CONDITION (green = ALL):** all 8 mmapprobe mappings OK + real browser launch with PNG >0 bytes + the same result on a second probe ≥5 min later + eye re-tests immediately before walking.
- **THE STATE:** re-confirmed DEAD 03:22Z — the condition is still unmet; queued VM eye-checks stay held; cloud eyes unaffected.

## Why it matters

Without this note, the next seat sees one alive probe and dispatches a VM eye into a two-minute window — the eighth identical failure, burned attempts, a stopped walk, and another hour lost. With it, the retry condition is exact and mechanical: two green probes, five minutes apart, or no dispatch. Cause-first is the discipline that turns a flapping failure into a held line, and a held line into a real green when it finally comes.

## What changes now

1. No VM eye dispatch until the four-part retry condition holds in full.
2. Every browser-probe result is judged against the timeline, not alone — one alive probe is never green.
3. Cloud eyes carry all walks until the VM condition holds.
4. The state file is updated on every flip, so the tripwire's next dead→alive detection is correct.
5. Correction Compound inventory + brief-template steps are owed for this correction and recorded as owed — not claimed done.
