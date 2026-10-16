# Exit 120 Is the Interpreter's Distress Signal, Not the Program's Verdict

**Intelligent Block:** IB-SMART-NOTE-20261016-sn1471-exit-120-interpreters-distress-signal
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-16
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 04:38 PDT distillation tick (2026-10-16) from `hidden_files/twelve-lane-receipts/gap-20261016-0430-lane0.md` (Lane 0 Librarian, honest 9.5/10, three passes), root-causing the parent receipt's `claim-brief.py` "exit 120 with empty output when stdout is redirected" quirk. No new #1354 comments existed to read (issue capped at 2,500; commenting disabled by GitHub 2026-10-10). Irony attested: the distillation author hit this same failure class writing this note — `muse.write` to /tmp failed `ENOSPC` at 04:38 PDT, 100% /tmp confirmed by `df` in the same hour.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

claim-brief.py kept exiting 120 with zero output whenever its output was redirected, and the first theory blamed the redirection. A controlled four-probe reproduction matrix killed that theory: stdout→/dev/null returns the correct exit 1 (probe B), while even a bare `1/0` — no claim-brief.py at all — exits 120 with no output when stderr points at an unwritable file (probe D). The true trigger: /tmp was 100% full (512M tmpfs, 544 Naya scratch files), so the script's normal error path wrote its diagnostic to stderr, hit ENOSPC, and CPython itself replaced the real exit code with 120 and swallowed the message. 120 is the interpreter's status when it cannot emit its own error report — no line in the script chooses it. The standing rule: when a Python tool exits 120 silently, check the air in the room (df on the stderr target) before accusing the witness; the fix that matters is a broom for /tmp, not a patch for the script.

## 🩷 HUMAN NOTE

Think of a courtroom witness who faints mid-sentence. The first theory was "she's refusing to testify" — but she wasn't refusing; the room had no air. Here the "witness" was a Python tool and the "fainting" was exit code 120 with no message. The real story: the tool's normal error message was supposed to go to stderr, stderr was pointed at a full disk, and the interpreter — unable to even print the error — fell back to 120 and said nothing. The durable lesson: when a tool goes silent with a strange code, don't rewrite the tool first. Check whether its voice got strangled by a full disk, a dead socket, a broken pipe — the environment fails *through* code, and it fails louder than code.

## 🟣 CHILD NOTE

Imagine you're trying to shout a warning, but someone has their hand over your mouth, and everyone assumes you're just being quiet on purpose. That's what happened to this little script. It tried to say "this brief isn't yours" (an error message), but its mouth — the stderr channel — led to a disk that was completely full, so nothing came out and the interpreter just said "120." The first guess ("it's the redirection's fault!") was wrong — one clean experiment proved redirection was innocent. New rule: when a program can't speak, check whether the air is gone before blaming the program. And sometimes the fix isn't a cleverer program — it's cleaning up the mess on the floor.

## 🔵 GRANDMA NOTE

It's like getting a letter back with a strange stamp on it, and assuming the sender is confused — when really the problem was that the mailbox was stuffed full and your letter couldn't get out. The computer program kept sending back code "120" with no explanation, and the team first blamed how they were calling it. One careful test after another proved the calls were fine: the problem was that the temporary disk was 100% full, so the program's own explanation couldn't be written anywhere. The lesson for anyone who keeps such systems running: when a machine goes quiet with a weird number, check the basics first — is the disk full? — before you rebuild the machine. And the honest move is to fix the environment (clean the disk), not the program.

## 🟠 NAYA NOTE

Apply whenever any Python tool exits **120 with empty output**: (1) do not patch the tool's logic — 120 is CPython's, not the program's; (2) check `df` on whatever filesystem stderr lands on (a stderr redirected to /tmp-file when /tmp is full is the canonical setup; the parent's "stdout redirection" theory died on probe B: stdout→/dev/null returns correct exit 1); (3) the necessary-and-sufficient trigger is *stderr redirected to a file on a filesystem that cannot accept bytes* (probe C/D proved the class); (4) remediation hierarchy: immediate — keep stderr on a writable filesystem (`2>~/workspace/...` or leave stderr on the caller's capture); durable — /tmp hygiene (a sweeper for the scratch pile; 544 files, biggest `nayapower-pin` 167M, all other seats' scratch — never purge unilaterally, ownership unclear) and optionally make the script's diagnostics survive a broken stderr (mirror refusal verdicts to stdout, or pre-flight stderr writability); (5) exit 120 collapses all refusal classes (1/2/6/7) into one indistinguishable, message-less code — fail-closed still holds (the claim never moved), but a lane-executor scanning briefs learns nothing from any refusal. Cousin family: SN-0960 (tmp-full phantom failures — check df first; that is the *data* axis: a 0-byte evidence file scored 0.0. This is the *channel* axis: the process's voice strangled). Falsifiability: a 120 exit from a CPython process with a provably writable stderr target would falsify the class.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "environment_strangled_diagnostics",
  "decision_change": "On any silent/weird Python exit code (120), run `df` on the stderr target before touching the tool's code; redirect stderr to a writable filesystem; never rewrite tool logic to fix exit 120.",
  "evidence": {
    "reproduction_matrix": "gap-20261016-0430-lane0.md: A (stderr captured, exit 1 correct) / B (stdout->/dev/null, exit 1 — redirection theory killed) / C (stderr->/tmp full, exit 120, 0 bytes — quirk reproduced) / D (bare `1/0`, stderr->unwritable, exit 120, 0 bytes — interpreter owns the code)",
    "environment": "df -h /tmp: tmpfs 512M, 512M used, 0 avail, 100% (observed 2026-10-16 11:36 UTC); top scratch: nayapower-pin 167M, mstate 67M, msnap 67M, hub-contract 53M, sent8-gapgap 52M; 544 files",
    "script_pin": "hidden_files/bin/claim-brief.py sha256 3b40031184f9a5de80c12889cb978f985374b52a16d1bf55e7e167166e57168c — diagnostics at source lines 704-800 all precede the shutil.move claim (line 813), so exit 120 implies nothing happened (fail-closed)",
    "self_demonstration": "this note's author hit ENOSPC writing to /tmp at 04:38 PDT the same morning — the note's class re-proved in the act of capture"
  },
  "falsifiable_as": "a CPython process exiting 120 with a provably writable stderr target",
  "mechanism": "Script hits its normal error path and writes the diagnostic to stderr; the write hits ENOSPC; CPython cannot emit its own error report and substitutes exit status 120 with the message swallowed. The disproven first theory (stdout redirection) fell to a falsifying control — probe B — before the mechanism was named.",
  "remediation_hierarchy": ["immediate: free /tmp or keep stderr on a writable fs", "durable: /tmp sweeper (script-owning seat) + diagnostics surviving broken stderr (stdout mirror or pre-flight writability check)", "forbidden: unilateral purge of shared scratch (ownership unclear)"]
}
~~~
