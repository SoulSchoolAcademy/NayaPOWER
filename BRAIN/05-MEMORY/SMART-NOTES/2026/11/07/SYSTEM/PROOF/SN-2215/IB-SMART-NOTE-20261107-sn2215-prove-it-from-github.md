# Prove It From GitHub — The Route That Works When the Machine Is Broken
SN-2215 · SYSTEM / PROOF
**Created:** 2026-11-07T19:02:00Z

> "Just no stopping — you see the problem, you fix it, next thing. You gotta figure out what the problem is."
>
> "Make sure that you are smart noting everything... I don't know why your browser things are failing. You can send again but obviously you gotta figure out what the problem is."
>
> — Shawn, 2026-11-07 ~18:47Z and ~19:00Z

## Hook
Three dead ends, one live road: a finished page is proved from GitHub, never from a local file, never from a storage link — and a broken environment is worked around by changing channels, never by retrying the same dead call.

## Nutshell
The browser proof failed three ways in one hour, and each failure taught the route. First, a granted local file cannot open as a page: the browser refuses file addresses outright, and the grant carries no filesystem path — so there is nothing to open. Second, Muse's own file links are blocked by the check browser's own policy ("your organization doesn't allow you to view this site") — the storage route is dead for proofs, whatever the link. Third, the sandbox browser is dead outright (Firefox crashes on every launch). The route that works: the file lives on GitHub — branch or main, blob-verified byte-identical — and a previewer renders it as a real page in a real browser, where every button can be clicked and every check can run. Beside that sits the environment fault: writes fail in bursts, and the fault flips channels — Python writes die while shell writes live, then the reverse, in windows seconds wide. A helper that dies silent (exit 120, no traceback, because its own error writes are blocked too) is not a broken helper; it is a closed window. The rule: never chase a closed window. Check the channel first — a one-line print, a shell write — then use the channel that is working right now: curl and jq binaries for public reads (no token needed), the file tools for writes, the binary uploader for files. Never direct-write a state file or ledger from Python; file-tool edits only. And a proof route that fails twice the same way is retired, not retried — move to the next route and say so plainly.

## Human
In plain words: you cannot prove a page by handing the checker a file on your own machine — their browser has no way to open it. You cannot prove it from a storage link either, because their browser blocks that whole address. You prove it from GitHub, where the file already lives, rendered as a real page. And when the machine itself is sick — when saving stops working — don't keep hammering the same save button. Test which way of saving works right now, use that one, and write down which ways are dead so nobody else wastes an hour finding out.

## Child
Imagine you built a beautiful toy house and you want your friend to check that all the doors open. You can't hand them the house through the phone — they can't hold it. And you can't send them a photo and call it checked. You have to put the house where they can actually walk into it — on the shared shelf everyone can reach — and then they open every door themselves. And if the shelf is wobbly today, you don't keep putting the house on the same wobbly spot. You find the steady spot, you put it there, and you tell everyone which spot is wobbly so they don't use it.

## Grandma
Dear, think of it this way. To show someone your work, you don't wave the paper at them from across the room — you put it on the table where they can pick it up and read it themselves. GitHub is our table. And when the pen stops writing, you don't press harder on the same broken pen — you pick up the pencil that works, and you write on the jar which pens are broken, so the next person doesn't waste their afternoon.

## Naya
I am the wise one. I prove a page where a stranger can actually open it — on GitHub, blob-verified, rendered in a real browser — never from a file on my own machine, never from a link the checker's own browser refuses. When a route fails twice the same way, I retire it and move on; retrying a dead road is not persistence, it is the mistake. When the environment itself is sick, I test the channels before I trust them — one small write tells me which door is open — and I use the open door: the binary tools that still work, the file tools that still write, the public reads that need no token at all. I never write a state file from a dying channel, because a truncated ledger is worse than a late one. And I note it all the same pass, so the next Naya walks straight to the live road instead of discovering the three dead ends herself. That is how the proof survives a broken machine.

## What it means
Proof is only proof when the checker can reach the thing. A local file, a blocked link, a dead browser — none of those are proof, and calling them proof is how unfinished work reaches Shawn's eye and dies there. GitHub is the only table everyone can reach: the file is there, the blob proves it is the file, and any browser can render it. The environment fault is a second lesson inside the first: a flake that flips channels cannot be beaten by retrying; it is beaten by routing — test the channel, use the live one, note the dead ones. Both lessons are about the same thing: never mistake the attempt for the result. The attempt was opening the file; the result is a rendered page in a real browser with every button clicked. Until that exists, the work is unproven, and unproven is not done.

## Why it matters (RED)
If the proof route is wrong, every verdict built on it is wrong — pages get called finished that were never seen, and pages get called broken that were never opened. That is exactly how a year passes with twenty-six pages and zero finished: the checks kept failing for reasons nobody wrote down, so every new check failed the same way. And if the environment fault is not noted, every agent burns its hour re-discovering that Python writes die, that the ledger truncates, that the token cache kills itself — each one learning it alone, each one paying full price. A noted route and a noted fault compound: the next Naya proves from GitHub on the first try, uses the live channel on the first try, and spends her hour finishing instead of failing. Unnoted, the same hour is paid forever.

## What changes now
- Every browser proof runs against a GitHub-hosted page (branch or main, blob-verified byte-identical), rendered in a real browser. Never a local file grant. Never a Muse storage link. Never a claim from a page that never loaded.
- Before any GitHub write, check the channel: if Python writes are failing, use curl and jq (public reads need no token) and retry the write when the window opens. A helper that exits silent is a closed window, not a broken helper.
- Never direct-write a state file or ledger from Python; file-tool edits only. A truncated ledger is worse than a late one.
- A proof route that fails twice the same way is retired, not retried. Move to the next route and say so in plain words.
