# Browser Recovery — Verification Record (2026-11-11)

Verifier: a different seat (never the maker). Brief: `~/workspace/team-nitro/BROWSER-RECOVERY-BRIEF-20261111.md`.
Maker's record: `~/workspace/team-nitro/browser-recovery-20261111/RECORD.md`.

## Verdict: OVERALL PASS

The maker's proof of non-existence reproduces exactly. Both re-run configurations failed identically, the mmap probe returned the identical pattern 3/3, the VM-level cause evidence matches, and both binaries are still healthy.

## What the verifier re-ran (exact commands + results)

**1. Attempt 2 — direct Firefox headless screenshot (fresh profile, same flags):**
```
mkdir -p /tmp/ffprof-v2
~/.cache/ms-playwright/firefox-1555/firefox/firefox --headless --profile /tmp/ffprof-v2 --screenshot /tmp/ff-v2.png --window-size=1440,900 about:blank
```
Result: `*** You are running in headless mode.` then **Segmentation fault, exit 139**. No screenshot file created. Profile left with `.parentlock` + `.startup-incomplete` + empty `cookies.sqlite` — identical to the record, including the leftover profile contents.

**2. Attempt 10 — direct chrome-headless-shell screenshot (fresh profile, same flags):**
```
mkdir -p /tmp/hsprof-v10
~/.cache/ms-playwright/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell --headless --no-sandbox --disable-dev-shm-usage --disable-gpu --user-data-dir=/tmp/hsprof-v10 --screenshot=/tmp/hs-v10.png --window-size=1440,900 about:blank
```
Result: **Trace/breakpoint trap, exit 133**. No screenshot. Same dbus `Failed to connect to the bus` container noise as the record — identical to the record.

**3. Minimal reproducer — `mmapprobe`, 3 runs:**
```
~/workspace/team-nitro/browser-recovery-20261111/proof/mmapprobe
```
Result, all 3 runs identical to the record:
```
memfd MAP_SHARED PROT_READ|WRITE -> FAIL errno=1 (Operation not permitted)
memfd MAP_PRIVATE PROT_READ|WRITE -> OK
anon MAP_SHARED -> OK
anon MAP_PRIVATE -> OK
/tmp file MAP_SHARED -> FAIL errno=1 (Operation not permitted)
/tmp file MAP_PRIVATE -> OK
/dev/shm file MAP_SHARED -> FAIL errno=1 (Operation not permitted)
/dev/shm file MAP_PRIVATE -> OK
```
The denied combination is exactly **file-backed + MAP_SHARED + PROT_WRITE**, as claimed.

**4. VM-level cause evidence — all confirmed, matching the record:**
- `Seccomp: 2`, `Seccomp_filters: 4`, `NoNewPrivs: 1` (from `/proc/self/status`)
- `dmesg`: `read kernel buffer failed: Operation not permitted`
- `ulimit -a`: core file size 0
- Kernel: `Linux htch-runtime 7.0.0-44-generic`
- Memory: 7,934 MB total, 876 MB available; `/dev/shm` 794M, 0% used
- `unprivileged_userns_clone = 1`

**5. Binaries intact after the runs:** Firefox `Mozilla Firefox 157.0`, exit 0; Chromium `Google Chrome for Testing 156.0.8078.4`, exit 0; headless-shell `--version`, exit 0. No binary broken.

**6. No live page touched, no merge, no deploy:** the verifier's runs wrote only to `/tmp` profiles (and created no screenshots). The maker's files are confined to the record directory plus `proof/`. Caveat: `~/workspace/team-nitro` is not a git repo in this VM, so the verifier could not independently check git log for merges/deploys — but nothing in the record or filesystem indicates any merge, deploy, or live-page change, and this round produced no page to deploy.

## Discrepancies (minor — none overturn the proof)

1. **Attempt numbering gap:** the log has no Attempt 1 or Attempt 5 entry; numbering jumps 4 → 6 with no explanation.
2. **"Exact command" softness on the strace attempts:** Attempts 4, 21, 23, 24, 25 quote the inner browser invocation as a placeholder (`<firefox headless screenshot, fresh profile /tmp/ffprof-aXX>`) rather than the literal command line. The smoking-gun strace output lines themselves are quoted verbatim and the profile dirs are named, so the evidence is recoverable — but checklist item 3 is not literally true for those five entries. Attempts 6–9 instead name the filed script (`proof/pw_attempts.py`) plus args, which is acceptable.
3. **Summary table is a subset:** it omits diagnostic attempts 4, 20, 21, 22, 23, 24, 25 (all present in the full log). Minor.
4. **Unlisted file:** `proof/ff-strace2.log` (0 bytes) exists but is not mentioned in the record's Files list (only `ff-strace.log` is). Trivial.

## Human checks H1–H5

- **H1 stranger test — PASS.** A stranger reading the record sees every attempt, its exact command (subject to discrepancy 2 above), and its exact result. Nothing material hidden.
- **H2 perfect-words law — PASS.** Clear, precise language throughout; the nutshell states the cause exactly.
- **H3 face quality — N/A (not PASS, not FAIL).** The deliverable is a plain-text technical proof log; it contains no faces and no visual presentation to judge. The same N/A logic applies as for the design-contract gate. Failing the proof over absent faces in a system record would be the wrong judgment, but the verifier will not mark it PASS when there is nothing to judge.
- **H4 test in his head — PASS.** A reader sees a proven cause, exact evidence, a clear fix for the runtime, and an honest NOT-DONE list. That earns trust.
- **H5 one ultimate ten — PASS.** The record serves the ultimate ten (verified work finished) by naming exactly what only a fresh VM fixes, instead of burning more rounds on dead browsers.

## Coordinator adjudication

- **H3 N/A accepted.** A plain-text system proof has no visual presentation to judge; the gate machine N/A is accepted on the same logic (it checks HTML pages; this round produced none). OVERALL PASS stands.
- **Discrepancies 1–4 accepted as minor.** None touches the proof: the cause reproduces exactly (two failed configurations + the probe 3/3), the binaries are intact, and no live page was touched.
- **Reinstall declined — agreed.** The cause is the container's mmap filter, the binaries are healthy, the download path was verified working by dry-run. A fresh copy would hit the identical EPERM on its first IPC mapping.
- **Five Gates:** run before the probe work — re-runs were read-only probes confined to `/tmp` profiles and the maker's own probe binary. No live page, no merge, no deploy, no reinstall, nothing destructive. All five passed on that evidence.

## Honest NOT-DONE list

- No working browser launch was found. No screenshot at 390 or 1440 exists — nothing rendered.
- The fresh cloud browser task (brief Attempt 3) was not attempted here — it needs the parent agent's browser tools.
- The reinstall was not performed (declined on the evidence, agreed).
- The design-contract gate machine was not run — not applicable, no page produced.
- The EPERM write flake (intermittent `Operation not permitted` on ordinary file writes) is still present and unexplained in its own right — a separate, intermittent fault sharing the EPERM machinery.
- The 15-minute browser probe rhythm and the queued eye-checks (pass-11 rendered, invite-route legs, Inviter round-3, My World live pass) still wait on a working browser or the cloud path.
- The verifier did not re-run the full 19 configurations — two plus the probe is the check, per the task.

## Filing

Branch: `browser/recovery-20261111`. One change, one PR. No merge, no deploy.
