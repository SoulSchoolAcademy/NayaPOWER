# Browser Recovery — Record (2026-11-11)

Coordinator: browser recovery maker (subagent, depth 2)
Brief: ~/workspace/team-nitro/BROWSER-RECOVERY-BRIEF-20261111.md (checker 9/9 PASS)
Status: COMPLETE — proof of non-existence delivered. No working launch exists under this VM.

## Nutshell

No browser launches in this VM, and the cause is proven, not guessed: the
container's security filter denies **writable file-backed shared memory
mappings** — `mmap` with `MAP_SHARED` + `PROT_WRITE` on any file descriptor
returns `EPERM`. Both Firefox and Chromium build their inter-process shared
memory exactly that way, so both die at startup, in every configuration
tried. The binaries are healthy. No flag, profile, display, or reinstall
can change a filter that lives outside the binaries. Only a fresh VM — or a
relaxing of that filter by the runtime — fixes it.

## Verifier's checklist (written before the attempts start)

The verifier is a different seat. It re-runs the work itself and confirms it by eye and by bytes — no claim is taken on trust.

**If the outcome is a working launch (fix found):**
1. Re-run the winning launch configuration exactly as recorded (fresh profile dir created first, same flags, same page).
2. Open a real page (not only about:blank) and take a screenshot at 390 and at 1440.
3. Confirm each screenshot is a real render, not a blank or black frame (check the file bytes and look at it).
4. Confirm zero console errors during the load.
5. Confirm the page at 390 has no horizontal overflow.
6. Confirm the --version check still passes on both binaries after any reinstall.
7. Confirm no live page was touched, no merge, no deploy.

**If the outcome is proof of non-existence (no fix) — THIS OUTCOME:**
1. Re-run TWO of the failed configurations itself (fresh profile, same flags) and confirm the same failure (same signal / same error text). Suggested: Attempt 2 (direct Firefox headless screenshot) and Attempt 10 (direct headless-shell screenshot).
2. Re-run the minimal reproducer `~/workspace/team-nitro/browser-recovery-20261111/proof/mmapprobe` (source `mmapprobe.c` beside it) and confirm the same pattern: file-backed `MAP_SHARED` + `PROT_WRITE` → `EPERM`, everything else → OK.
3. Confirm every attempt in the log carries its exact command and its exact result.
4. Confirm the VM-level cause evidence (resource limits, seccomp, dmesg, deployment state) is present and matches what the record claims.
5. Confirm no live page was touched, no merge, no deploy, and no binary was broken (the --version check still passes — verified at the end of the run).

**Human checks H1–H5 (attested via --human-checks FILE):** stranger test · perfect-words law · face quality · test in his head · one ultimate ten. All five PASS + machine clean = OVERALL PASS. His eye is the final gate.

**Design-contract gate (a)–(i):** not applicable as a machine run on this round — `check-gate.py` is a static HTML+CSS checker that takes a `<page.html>`; this round produced no page and no screenshot (nothing rendered). Its own docstring already records the fact this round set out to close: "Playwright is DEAD in this VM since 16:18Z 2026-11-08 (Firefox SIGSEGV / Chromium SIGTRAP on launch)". The verification mechanism for this round is the checklist above.

---

## The VM-level cause (proven)

**The rule, stated exactly:** `mmap(NULL, len, PROT_READ|PROT_WRITE, MAP_SHARED, fd, 0)` returns `EPERM (Operation not permitted)` for every file-backed descriptor — memfd, a file on /tmp, a file on /dev/shm. The same call with `PROT_READ` alone succeeds. With `PROT_EXEC` alone succeeds. Anonymous `MAP_SHARED` (no fd) succeeds. `MAP_PRIVATE` always succeeds. The filter denies precisely **writable file-backed shared mappings**.

**How it kills Firefox (seen in strace, Attempt 24):**
```
memfd_create("mozilla-ipc", MFD_CLOEXEC|MFD_ALLOW_SEALING|MFD_NOEXEC_SEAL) = 27
ftruncate(27, 8) = 0
fcntl(27, F_ADD_SEALS, F_SEAL_SHRINK|F_SEAL_GROW) = 0
mmap(NULL, 8, PROT_READ|PROT_WRITE, MAP_SHARED, 27, 0) = -1 EPERM
--- SIGSEGV {si_signo=SIGSEGV, si_code=SEGV_MAPERR, si_addr=NULL} ---
```
Firefox creates its IPC shared memory, the mapping is denied, the code
dereferences the NULL address, and the process dies with a null-pointer
segfault — then its crash handler re-raises SIGSEGV on itself (the
`rt_sigaction(SIGSEGV, SIG_DFL)` + `tgkill(self, SIGSEGV)` seen in the
trace). The segfault is the symptom; the denied mapping is the cause.

**How it kills Chromium (seen in strace, Attempt 25):**
```
mmap(NULL, 10822000, PROT_READ, MAP_SHARED, 3, 0) = 0x72d440e00000
mmap(NULL, 65568, PROT_READ|PROT_WRITE, MAP_SHARED, 4, 0) = -1 EPERM
--- SIGTRAP {si_signo=SIGTRAP, si_code=SI_KERNEL, si_addr=NULL} ---
```
The read-only shared mapping passes; the writable one is denied; Chromium
hits a failed CHECK and deliberately traps (`IMMEDIATE_CRASH` → SIGTRAP)
before any logging output — which is why `--enable-logging=stderr --v=1`
produced zero lines (Attempt 14).

**Why nothing else helped:** every configuration tried changes the profile,
the display, the sandbox flags, or the process layout — none of them changes
the fact that both browsers set up inter-process shared memory with a
writable file-backed shared mapping. The filter sits outside the browsers,
in the container (seccomp filter mode, 4 filters installed; `NoNewPrivs: 1`;
`dmesg` unreadable). It is the same EPERM machinery behind the intermittent
write failures (the EPERM flake) — but the mmap denial is not intermittent:
3/3 reproducer runs, identical, and both browsers hit it on every launch.

**What only a fresh VM (or the runtime) fixes:** the filter itself. A
reinstall cannot change it; the binaries are healthy and the denied call is
a kernel/container decision, not a binary defect.

---

## Attempts log

(Every attempt: exact command, exact result. Nothing hidden.)

### Environment snapshot (01:06Z)
- Firefox `--version`: `Mozilla Firefox 157.0`, exit 0. Chromium `--version`: `Google Chrome for Testing 156.0.8078.4`, exit 0. Binaries healthy.
- Playwright 1.64.1 (python). Node v24.22.1. gcc available.
- Memory: 7,934 MB total; available drifted 735 MB → 1,373 MB → 1,036 MB across the run (tight but no single hog; largest RSS is the runtime's own `hatch daemon`, 564 MB — not touched). Swap 428–440 / 1,023 MB used. /dev/shm 794 MB, 0% used. Disk 108 GB free.
- `ulimit -a`: core file size 0 (hard limit 0, cannot be raised — see Attempt 22); open files 4096; max user processes 27134; virtual memory unlimited.
- Seccomp: `Seccomp: 2` (filter mode), `Seccomp_filters: 4`. `NoNewPrivs: 1`. `ptrace_scope: 1`.
- `dmesg`: read kernel buffer failed — Operation not permitted.
- `ldd` on Firefox and Chromium binaries: no missing libraries.
- Kernel: `Linux htch-runtime 7.0.0-44-generic` (real kernel, not gVisor). No `/dev/kvm`. User namespaces work (`unshare -U -r true`, exit 0; `unprivileged_userns_clone=1`).
- No system Chrome/Firefox. Xvfb IS installed (`/usr/bin/Xvfb`, `xvfb-run`).
- No `LD_PRELOAD`, no `/etc/ld.so.preload`.

### Attempt 2 — direct Firefox headless screenshot, pre-created profile (01:06Z)
Command:
```
mkdir -p /tmp/ffprof-a2
~/.cache/ms-playwright/firefox-1555/firefox/firefox --headless --profile /tmp/ffprof-a2 --screenshot /tmp/ff-a2.png --window-size=1440,900 about:blank
```
Result: `*** You are running in headless mode.` then **Segmentation fault, exit 139**. No screenshot file created. Profile left with `.startup-incomplete` + `.parentlock` + empty `cookies.sqlite` — crash during early startup, before any page load. This separates the failure from Playwright: Firefox itself segfaults on startup.

### Attempt 3 — direct Firefox headless, all Mozilla sandbox env vars off (01:06Z)
Command:
```
mkdir -p /tmp/ffprof-a3
MOZ_DISABLE_CONTENT_SANDBOX=1 MOZ_DISABLE_GMP_SANDBOX=1 MOZ_DISABLE_SOCKET_PROCESS_SANDBOX=1 MOZ_DISABLE_GPU_SANDBOX=1 MOZ_DISABLE_RDD_SANDBOX=1 MOZ_DISABLE_UTILITY_SANDBOX=1 \
~/.cache/ms-playwright/firefox-1555/firefox/firefox --headless --profile /tmp/ffprof-a3 --screenshot /tmp/ff-a3.png --window-size=1440,900 about:blank
```
Result: same — **Segmentation fault, exit 139**, no screenshot. Disabling Firefox's own sandboxes does not change the outcome; the crash is not in Firefox's sandbox code.

### Attempt 4 — strace the Firefox launch (01:06Z)
Command: `strace -f -tt <firefox headless screenshot, fresh profile /tmp/ffprof-a5>` (tried `-o FILE` in /tmp and in ~/workspace, then stderr redirect to a file).
Result: **strace produced zero trace lines**; Firefox still segfaulted (exit 139). `-o FILE` failed with `Operation not permitted` on the log file itself. First reading: ptrace blocked. Corrected by Attempt 22: strace works fine when its output goes to a pipe; writing its output to a regular file hits the EPERM write flake. The tool was never the problem — the file write was.

### Attempt 6 — Playwright Firefox, default headless (01:07Z)
Script: `~/workspace/team-nitro/browser-recovery-20261111/proof/pw_attempts.py`, attempt A6.
Command (what Playwright ran):
```
~/.cache/ms-playwright/firefox-1555/firefox/firefox -no-remote -headless -profile /tmp/playwright_firefoxdev_profile-HounkG -juggler-pipe -silent
```
Result: `<launched> pid=109752` then `<process did exit: exitCode=null, signal=SIGSEGV>`, 0.9 s. No screenshot.

### Attempt 7 — Playwright Firefox, Mozilla sandboxes off via env + prefs (01:07Z)
Script: `pw_attempts.py`, attempt A7. Launch env added `MOZ_DISABLE_CONTENT_SANDBOX=1`, `MOZ_DISABLE_GMP_SANDBOX=1`, `MOZ_DISABLE_SOCKET_PROCESS_SANDBOX=1`, `MOZ_DISABLE_GPU_SANDBOX=1`, `MOZ_DISABLE_RDD_SANDBOX=1`, `MOZ_DISABLE_UTILITY_SANDBOX=1`; prefs `security.sandbox.content.level: 0`, `security.sandbox.gpu.level: 0`.
Result: `<launched> pid=109795` then `signal=SIGSEGV`, 0.9 s. No screenshot.

### Attempt 8 — Playwright Chromium, sandbox/shm/gpu flags (01:07Z)
Script: `pw_attempts.py`, attempt A8. Args: `--no-sandbox --disable-dev-shm-usage --disable-gpu --single-process --no-zygote`.
Result: `TargetClosedError: BrowserType.launch: Target page, context or browser has been closed`, 1.1 s. Browser died during launch. No screenshot.

### Attempt 9 — Playwright Chromium headless shell (01:07Z)
Script: `pw_attempts.py`, attempt A9. Executable: `chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell`. Args: `--no-sandbox --disable-dev-shm-usage --disable-gpu`.
Result: `TargetClosedError` (same as A8), 1.4 s. No screenshot.

### Attempt 10 — direct chrome-headless-shell screenshot (01:07Z)
Command:
```
mkdir -p /tmp/hsprof-a10
~/.cache/ms-playwright/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell --headless --no-sandbox --disable-dev-shm-usage --disable-gpu --user-data-dir=/tmp/hsprof-a10 --screenshot=/tmp/hs-a10.png --window-size=1440,900 about:blank
```
Result: **Trace/breakpoint trap, exit 133**. No screenshot. (The dbus `Failed to connect to the bus` lines are normal container noise, not the cause.)

### Attempt 11 — direct full Chromium screenshot, single-process (01:07Z)
Command:
```
mkdir -p /tmp/chprof-a11
~/.cache/ms-playwright/chromium-1248/chrome-linux64/chrome --headless=new --no-sandbox --disable-dev-shm-usage --disable-gpu --single-process --user-data-dir=/tmp/chprof-a11 --screenshot=/tmp/ch-a11.png --window-size=1440,900 about:blank
```
Result: **Trace/breakpoint trap, exit 133**. No screenshot. Extra line: `[0100/000000.220261:ERROR:content/zygote/zygote_linux.cc:662] write: Broken pipe (32)` — the browser side writing to a zygote that is already dead.

### Attempt 12 — direct Chromium, seccomp-filter sandbox off (01:07Z)
Command:
```
mkdir -p /tmp/chprof-a12b
~/.cache/ms-playwright/chromium-1248/chrome-linux64/chrome --headless=new --no-sandbox --disable-seccomp-filter-sandbox --disable-namespace-sandbox --disable-setuid-sandbox --no-zygote --disable-dev-shm-usage --disable-gpu --user-data-dir=/tmp/chprof-a12b --screenshot=/tmp/ch-a12b.png --window-size=1440,900 about:blank
```
Result: **Trace/breakpoint trap, exit 133**. No screenshot, zero output lines. Disabling Chromium's own seccomp filter does not help — the denying filter is the container's, not Chromium's. (First run of this attempt piped output through `tail`, which masked the true exit code; re-run without the pipe gave the true 133.)

### Attempt 13 — Firefox --safe-mode headless (01:07Z)
Command:
```
mkdir -p /tmp/ffprof-a13
~/.cache/ms-playwright/firefox-1555/firefox/firefox --headless --safe-mode --profile /tmp/ffprof-a13 --screenshot /tmp/ff-a13.png --window-size=1440,900 about:blank
```
Result: **Segmentation fault, exit 139**. No screenshot. Safe mode changes nothing — the crash is before any extension or setting loads.

### Attempt 14 — Chromium with verbose logging (01:07Z)
Command:
```
mkdir -p /tmp/chprof-a14
~/.cache/ms-playwright/chromium-1248/chrome-linux64/chrome --headless=new --no-sandbox --disable-dev-shm-usage --disable-gpu --enable-logging=stderr --v=1 --user-data-dir=/tmp/chprof-a14 --screenshot=/tmp/ch-a14.png --window-size=1440,900 about:blank
```
Result: **Trace/breakpoint trap, exit 133, zero lines of output** (`/tmp/a14.out` is 0 lines). The trap happens before Chromium's logging initializes — the death is in the earliest startup.

### Attempt 15 — Firefox HEADED under Xvfb (01:07Z)
Command:
```
mkdir -p /tmp/ffprof-a15
timeout 90 xvfb-run -a -s "-screen 0 1440x900x24" ~/.cache/ms-playwright/firefox-1555/firefox/firefox --profile /tmp/ffprof-a15 --screenshot /tmp/ff-a15.png --window-size=1440,900 about:blank
```
Result: exit 1, no screenshot, no output. The headed path does not escape the fault (the run hung to the 90 s timeout inside `xvfb-run`, which then reported 1). Cleaned up by Attempt 15b below.

### Attempt 15b — Firefox HEADED on a manually started Xvfb :99 (01:08Z)
Command:
```
Xvfb :99 -screen 0 1440x900x24   (started in background)
DISPLAY=:99 timeout 45 ~/.cache/ms-playwright/firefox-1555/firefox/firefox --profile /tmp/ffprof-a15b --screenshot /tmp/ff-a15b.png --window-size=1440,900 about:blank
```
Result: **Segmentation fault, exit 139**. No screenshot. A real display changes nothing — the crash does not involve the display path. Xvfb :99 later confirmed stopped (no Xvfb process remains).

### Attempt 16b — Chromium HEADED on Xvfb :99 (01:08Z)
Command:
```
mkdir -p /tmp/chprof-a16b
DISPLAY=:99 timeout 45 ~/.cache/ms-playwright/chromium-1248/chrome-linux64/chrome --no-sandbox --disable-dev-shm-usage --disable-gpu --user-data-dir=/tmp/chprof-a16b --screenshot=/tmp/ch-a16b.png --window-size=1440,900 about:blank
```
Result: **Trace/breakpoint trap, exit 133**. No screenshot.

### Attempt 17 — Firefox with a fresh HOME (01:08Z)
Command:
```
mkdir -p /tmp/fakehome17 /tmp/ffprof-a17
HOME=/tmp/fakehome17 timeout 45 ~/.cache/ms-playwright/firefox-1555/firefox/firefox --headless --profile /tmp/ffprof-a17 --screenshot /tmp/ff-a17.png --window-size=1440,900 about:blank
```
Result: **Segmentation fault, exit 139**. No screenshot. Nothing in the home directory (font cache, Mozilla state) is the cause.

### Attempt 18 — Firefox with TMPDIR under home (01:08Z)
Command:
```
mkdir -p ~/tmp-a18 /tmp/ffprof-a18
TMPDIR=$HOME/tmp-a18 timeout 45 ~/.cache/ms-playwright/firefox-1555/firefox/firefox --headless --profile /tmp/ffprof-a18 --screenshot /tmp/ff-a18.png --window-size=1440,900 about:blank
```
Result: **Segmentation fault, exit 139**. No screenshot. The /tmp tmpfs is not the cause.

### Attempt 19 — Firefox with JIT / WASM off via user.js (01:08Z, redone 01:11Z)
Command:
```
mkdir -p ~/ffprof-a19
printf 'user_pref("javascript.options.ion", false);\nuser_pref("javascript.options.baselinejit", false);\nuser_pref("javascript.options.native_regexp", false);\nuser_pref("javascript.options.wasm", false);\n' > ~/ffprof-a19/user.js
timeout 45 ~/.cache/ms-playwright/firefox-1555/firefox/firefox --headless --profile ~/ffprof-a19 --screenshot /tmp/ff-a19b.png --window-size=1440,900 about:blank
```
Result: **Segmentation fault, exit 139**. No screenshot. (First run of this attempt was invalid: the `printf` redirect to /tmp failed with `Operation not permitted` — the EPERM write flake — so no user.js was written. The redo wrote user.js under HOME successfully and still segfaulted.) The JS engine is not the cause.

### Attempt 20 — catchsegv on Firefox (01:11Z)
Command: `timeout 45 catchsegv ~/.cache/ms-playwright/firefox-1555/firefox/firefox --headless --profile /tmp/ffprof-a20 --screenshot /tmp/ff-a20.png --window-size=1440,900 about:blank`
Result: `catchsegv: No such file or directory`, exit 127. Tool not installed; superseded by the strace work (Attempts 23–25).

### Attempt 21 — Firefox under libSegFault via LD_PRELOAD (01:11Z)
Command: `LD_PRELOAD=/lib/x86_64-linux-gnu/libSegFault.so SEGFAULT_SIGNALS=all SEGFAULT_OUTPUT_NAME=/tmp/segv-a21.log timeout 45 <firefox headless screenshot, profile /tmp/ffprof-a21>`
Result: `ld.so: object '/lib/x86_64-linux-gnu/libSegFault.so' from LD_PRELOAD cannot be preloaded (cannot open shared object file): ignored.` Firefox still segfaulted (139). libSegFault is not present in this image. Superseded by strace.

### Attempt 22 — core dumps + strace sanity (01:11Z)
Commands: `ulimit -c unlimited` in the shell; `prlimit --core=unlimited --pid=$$`; `strace /bin/true 2>/tmp/stt.log`; `strace -f -tt /bin/true 2>&1 | head -5`.
Results:
- `ulimit: core file size: cannot modify limit: Operation not permitted.` `/proc/self/limits` shows `Max core file size 0 0`. `prlimit` also fails EPERM. **No core dumps are obtainable from inside this VM** (hard limit 0, unrais able). `core_pattern` is `core` (plain file), so the blocker is the limit, not the pattern.
- `strace /bin/true 2>/tmp/stt.log` → 0 lines in the file; but `strace -f -tt /bin/true 2>&1 | head -5` → full trace output. **strace works; writing its output to a regular file hits the EPERM write flake, while a pipe works.** This corrected Attempt 4's first reading (ptrace is not blocked).

### Attempt 23 — strace Firefox via pipe, tail (01:11Z)
Command: `timeout 45 strace -f -tt -s 200 <firefox headless screenshot, profile /tmp/ffprof-a23> 2>&1 | tail -50`
Result: the tail shows pid 111277 resetting SIGSEGV to default, unblocking it, and `tgkill(111277, 111277, SIGSEGV)` — **Firefox deliberately re-raises SIGSEGV on itself** after its crash handler runs. The segfault is real, but the tail shows the suicide, not the cause. Led to Attempt 24.

### Attempt 24 — strace Firefox, context before the suicide + crash markers (01:11Z)
Command: `timeout 45 strace -f -tt -s 300 <firefox headless screenshot, profile /tmp/ffprof-a24> 2>&1 | grep -B45 -m1 "tgkill.*SIGSEGV"`; second run piped to `grep -nE "minidump|\.dmp|Crash|MOZ_CRASH|fatal|abort|SIGABRT|SIGSYS|ENOSYS|EPERM"`.
Result — **the smoking gun** (main process, pid 111346):
```
memfd_create("mozilla-ipc", MFD_CLOEXEC|MFD_ALLOW_SEALING|MFD_NOEXEC_SEAL) = 27
openat(AT_FDCWD, "/proc/self/fd/27", O_RDONLY|O_CLOEXEC) = 30
ftruncate(27, 8) = 0
fcntl(27, F_ADD_SEALS, F_SEAL_SHRINK|F_SEAL_GROW) = 0
mmap(NULL, 8, PROT_READ|PROT_WRITE, MAP_SHARED, 27, 0) = -1 EPERM (Operation not permitted)
--- SIGSEGV {si_signo=SIGSEGV, si_code=SEGV_MAPERR, si_addr=NULL} ---
```
The same run also shows the EPERM flake on ordinary writes (`pwrite64` on `cookies.sqlite-journal` → EPERM; `write` of `compatibility.ini` → EPERM; `connect` to `/var/run/nscd/socket` → EPERM; two more `mmap MAP_SHARED` → EPERM) — the write denials are intermittent, the mapping denial is what kills the process.

### Attempt 25 — strace Chromium, MAP_SHARED + trap (01:12Z)
Command: `timeout 45 strace -f -tt -s 200 <chromium headless screenshot, profile /tmp/chprof-a25> 2>&1 | grep -E "MAP_SHARED|SIGTRAP|SIGSYS|IMMEDIATE|traphandler|tgkill|mmap.*EPERM"`
Result — the same mechanism on the other engine:
```
rt_sigaction(SIGTRAP, {sa_handler=SIG_DFL, ...}) = 0
mmap(NULL, 10822000, PROT_READ, MAP_SHARED, 3, 0) = 0x72d440e00000
mmap(NULL, 65568, PROT_READ|PROT_WRITE, MAP_SHARED, 4, 0) = -1 EPERM (Operation not permitted)
--- SIGTRAP {si_signo=SIGTRAP, si_code=SI_KERNEL, si_addr=NULL} ---
```
Read-only shared mapping passes; writable shared mapping is denied; Chromium traps immediately after.

### Attempt 26 — Chromium kitchen-sink (01:12Z)
Command:
```
mkdir -p /tmp/chprof-a26
~/.cache/ms-playwright/chromium-1248/chrome-linux64/chrome --headless=new --no-sandbox --disable-seccomp-filter-sandbox --disable-namespace-sandbox --no-zygote --single-process --in-process-gpu --disable-gpu --disable-dev-shm-usage --disable-gpu-sandbox --disable-software-rasterizer --user-data-dir=/tmp/chprof-a26 --screenshot=/tmp/ch-a26.png --window-size=1440,900 about:blank
```
Result: **Trace/breakpoint trap, exit 133**. No screenshot. Even single-process with the GPU in-process still needs the denied mapping.

### Minimal reproducer — mmapprobe (01:12Z)
Source: `~/workspace/team-nitro/browser-recovery-20261111/proof/mmapprobe.c`; binary beside it. Three runs, identical:
```
memfd MAP_SHARED PROT_READ|WRITE -> FAIL errno=1 (Operation not permitted)
memfd MAP_PRIVATE PROT_READ|WRITE -> OK
anon MAP_SHARED                  -> OK
anon MAP_PRIVATE                 -> OK
/tmp file MAP_SHARED             -> FAIL errno=1 (Operation not permitted)
/tmp file MAP_PRIVATE            -> OK
/dev/shm file MAP_SHARED         -> FAIL errno=1 (Operation not permitted)
/dev/shm file MAP_PRIVATE        -> OK
```
Refined probe (`/tmp/mmapprobe2.c`, two runs, identical):
```
memfd MAP_SHARED PROT_READ       -> OK
memfd MAP_SHARED PROT_READ|WRITE -> FAIL errno=1
memfd MAP_SHARED PROT_EXEC       -> OK
anon  MAP_SHARED PROT_READ|WRITE -> OK
```
The denied combination is exactly **file-backed + MAP_SHARED + PROT_WRITE**.

### Syscall probe — sysprobe (01:11Z)
Source: `~/workspace/team-nitro/browser-recovery-20261111/proof/sysprobe.c`. Result: `clone3` EINVAL (implemented), `openat2` EINVAL (implemented), `pidfd_open` EINVAL, `membarrier` OK, `rseq` EFAULT (implemented), `statx` EFAULT, `bpf` EINVAL, `keyctl` EINVAL, `mount` EFAULT, `clone(userns)` SUCCESS, `getrandom` OK, `futex` EFAULT, `prlimit64` OK, nested `prctl(PR_SET_SECCOMP, FILTER, allow-all)` SUCCESS. `io_uring_setup` EPERM, `perf_event_open` EACCES — both irrelevant to browser startup. **No SIGSYS was trapped on any probe**: the container filter does not kill syscalls with signals; it returns EPERM on the ones it denies. Browsers die because they cannot tolerate the EPERM on the shared-memory mapping, not because a syscall is trapped.

### Attempt 3 (brief order) — fresh cloud browser task: SKIPPED
Per the dispatching task: a fresh cloud browser task needs the parent agent's browser tools; the parent runs that separately. Not attempted here. The queued cloud task's state (queued since 23:05Z, never launched) is unchanged by this round.

### Attempt 4 (brief order) — reinstall: CONSIDERED, NOT PERFORMED
Download path verified first, as the brief requires:
```
$ python3 -m playwright install --dry-run firefox
Firefox 157.0 (playwright firefox v1555)
  Install location:    /home/hatch/.cache/ms-playwright/firefox-1555
  Download url:        https://cdn.playwright.dev/dbazure/download/playwright/builds/firefox/1555/firefox-ubuntu-24.04.zip
  Download fallback 1: https://playwright.download.prss.microsoft.com/dbazure/download/playwright/builds/firefox/1555/firefox-ubuntu-24.04.zip
  Download fallback 2: https://cdn.playwright.dev/builds/firefox/1555/firefox-ubuntu-24.04.zip
```
Dry-run exit 0 — the download path works. The reinstall was **not** performed, on the Five Gates: the cause is proven to be the container's mmap filter, and a fresh copy of a healthy binary would hit the identical EPERM on its first IPC mapping (Gate 1 — it cannot help; Gate 5 — no measurement could show it helping). Reinstalling would also risk the one known-good artifact in this story — the `--version` binaries that still work. Final `--version` sanity after all attempts: Firefox 157.0, Chromium 156.0.8078.4, both exit 0. Binaries untouched.

---

## What was tried, in one table

| # | Engine | Configuration | Result |
|---|--------|---------------|--------|
| 2 | Firefox | direct headless screenshot, fresh profile | SIGSEGV 139 |
| 3 | Firefox | + all Mozilla sandbox env vars off | SIGSEGV 139 |
| 6 | Firefox | Playwright default | SIGSEGV (pid 109752) |
| 7 | Firefox | Playwright + sandbox env off + prefs level 0 | SIGSEGV (pid 109795) |
| 8 | Chromium | Playwright + no-sandbox/dev-shm/gpu/single-process/no-zygote | TargetClosedError (died on launch) |
| 9 | Chromium | Playwright headless shell | TargetClosedError |
| 10 | Chromium | direct headless-shell screenshot | SIGTRAP 133 |
| 11 | Chromium | direct full screenshot, single-process | SIGTRAP 133 |
| 12 | Chromium | + disable-seccomp-filter/namespace/setuid sandbox, no-zygote | SIGTRAP 133 |
| 13 | Firefox | --safe-mode | SIGSEGV 139 |
| 14 | Chromium | + --enable-logging=stderr --v=1 | SIGTRAP 133, zero output |
| 15 | Firefox | headed under xvfb-run | exit 1, no screenshot |
| 15b | Firefox | headed on Xvfb :99 | SIGSEGV 139 |
| 16b | Chromium | headed on Xvfb :99 | SIGTRAP 133 |
| 17 | Firefox | fresh HOME | SIGSEGV 139 |
| 18 | Firefox | TMPDIR under home | SIGSEGV 139 |
| 19 | Firefox | JIT/WASM off via user.js | SIGSEGV 139 |
| 26 | Chromium | kitchen-sink (single-process, in-process GPU, all sandboxes off) | SIGTRAP 133 |

Skipped: brief Attempt 3 (fresh cloud browser task — parent's tools). Considered, not performed: reinstall (download path verified; cause proven to be the container filter).

## NOT-DONE list (honest)

- No working browser launch was found. No screenshot at 390 or 1440 exists — nothing rendered, so there is no proof screenshot to attach.
- The fresh cloud browser task (brief Attempt 3) was not attempted here — it needs the parent agent's browser tools; the parent runs it separately.
- The reinstall was not performed (see above — download path verified, reinstall declined on the evidence).
- The design-contract gate machine was not run — it checks HTML pages and this round produced none.
- The 15-minute browser probe rhythm and the queued eye-checks (pass-11 rendered, invite-route legs, Inviter round-3, My World live pass) still wait on a working browser or the cloud path.
- The EPERM write flake (intermittent `Operation not permitted` on ordinary file writes) is still present and still unexplained in its own right — it shares the EPERM machinery with the mmap denial but is a separate, intermittent fault. It bit this round twice (strace log files, one `printf` redirect) and was worked around with pipes.

## Files

- Record: `~/workspace/team-nitro/browser-recovery-20261111/RECORD.md` (this file)
- Playwright attempts: `~/workspace/team-nitro/browser-recovery-20261111/proof/pw_attempts.py`
- Syscall probe: `~/workspace/team-nitro/browser-recovery-20261111/proof/sysprobe.c`
- Mapping probe: `~/workspace/team-nitro/browser-recovery-20261111/proof/mmapprobe.c` (+ compiled `mmapprobe`)
- Strace log placeholder: `~/workspace/team-nitro/browser-recovery-20261111/proof/ff-strace.log` (0 bytes — the EPERM write flake; the real traces were captured through pipes and are quoted in the log above)
- No live page touched. No merge. No deploy. No binary changed.

## The fix, for the runtime

Allow writable file-backed shared mappings in this cell — i.e. stop returning
EPERM for `mmap` with `MAP_SHARED` + `PROT_WRITE` on a file descriptor
(memfd, tmpfs files) — or move the work to a fresh VM without that filter.
Everything else in the cell already works: the binaries are healthy, the
syscalls browsers need are present, user namespaces work, nested seccomp
install works, and the network path for downloads is verified. One filter
rule is the whole bottleneck.
