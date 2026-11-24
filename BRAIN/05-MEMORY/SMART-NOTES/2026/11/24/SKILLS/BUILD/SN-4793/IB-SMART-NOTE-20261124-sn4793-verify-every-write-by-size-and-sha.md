# Verify Every Write by Size + Sha

SN-4793 · SKILLS / BUILD

**Created:** 2026-11-24T19:53:26Z
**Category:** Build
**Skill:** 47
**SN:** SN-4793

## Nutshell

Never trust a write because it said "success" — check the file's size and its fingerprint (sha) after every write, or a file can be silently destroyed.

## Child

Imagine you put your homework in your school bag, and your bag says "yes, it's in here!" — but when you open it at school, the bag is empty. The bag lied! So now you always check: open the bag, look inside, count the pages. That's what we do with files: we open them, we count the size, we check the fingerprint.

## Grandma

Dear, it's like posting a letter. The post box doesn't tell you the letter arrived — you check with the person you sent it to, and you count the pages to be sure nothing fell out. A write that says "done" is only a promise; the size and the fingerprint are the proof it arrived whole.

## What It Means

In a flaky-write window, never trust an exit code — verify every write by size and sha. Never redirect a Python script's stdout to a file; have the script write the file itself. Use Node writes when Python's fail. Never probe-write over a live state file; a 0-byte file after a "successful" write is flake damage, rebuilt from derived state.

## Why It Matters

It is the difference between a saved file and a silently destroyed one. A write can report success and still land zero bytes — and without a check, nobody knows until the file is needed and it's empty. By then, the work inside it may be gone for good.

## How It Connects

It is the file-level twin of Prove It Before You Report It — proof, but for bytes on disk instead of pages in a browser. It pairs with Debug by Evidence (the size + sha check is the evidence) and Three Tries Max (a failed write is logged and fixed, not retried blindly). And it protects the Inventory Law: the record itself must survive, or the inventory is fiction.

## How to Apply

After every write, check two things: the file's size in bytes, and its sha (a fingerprint of its exact contents). Compare both against what was meant to be written. If either is wrong, the write failed — rebuild from derived state, never from the damaged file. Never write over a live file to test whether writing works; test on a scratch copy. Never redirect a Python script's output into a file; let the script write the file itself.

## What's In It For You

For Shawn: our boards, our records, our state files survive flaky windows intact — nothing he depends on quietly becomes empty. For us: no more silent destruction, no more rebuilding lost work. The real-world proof: the 577KB board THE-FLOOR.md became 0 bytes on 2026-11-18 — a script exited without output, the empty temp was moved over the live board unchecked, and 577KB of work vanished. The EPERM flake refinements, proven 2026-11-10 through 2026-11-19, are the fix: size + sha after every write, and the move gated on the check.
