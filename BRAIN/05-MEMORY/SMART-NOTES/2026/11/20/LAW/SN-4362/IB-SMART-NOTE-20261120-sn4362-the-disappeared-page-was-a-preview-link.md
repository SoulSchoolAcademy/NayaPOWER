# SN-4362 — The Disappeared Page Was a Preview Link

**Category:** LAW — assurance first; a preview link is not a live page; 2026-11-20 ~16:52 MST

*Paired Naya Note: NN-20261120-the-disappeared-page-was-a-preview-link — the verbatim record of his question and answer.*

**Filed:** SN-4362 — Intelligence Loop run 434, 2026-11-20. His question on call f3737da1, recorded in MEMORY.md. Correction Compound runs with this note: inventory + brief-template + PI + GitHub, same pass.

## In a Nutshell

The disappeared page was not a live page — it was the agreement preview share link, returning HTTP 403 and 0 bytes. Every live page was verified byte-for-byte intact. He does not need the link back: "I don't need it. I just wanted to make sure that everything was still there." Assurance was the ask; the live check already answered it.

## The Lesson

When he asks whether something disappeared, check the live bytes first and the preview links second, and name which one it is. A 403 on a share link is a link problem, not a missing page — the artifact record still said shared=true while the link itself refused. And when he says he does not need it, believe him: do not rebuild a link nobody asked to keep. The work is "let's just get this done," not a recovery nobody wants. Also: never re-share a preview mid-build — the buttons/portraits build was still running, and re-sharing then could have served a half-built version. The live agreement at nayanet.app/agreement (v28, verified) is the safe current copy until the build lands and the link is refreshed.

## Why It Matters

Panic about a missing page costs a whole call if the check is not run. The check takes minutes: six live pages, byte-for-byte, all as recorded. Run it before anything else, and say the result in plain words.

## How to Use It

On any "a page disappeared" report: fetch every live page and compare bytes and hashes against the record; then check the staged and preview links separately; report which one it is — live or link — and what he actually needs before rebuilding anything.

## His Order, As Recorded

> "One of the pages disappeared that used to be. Did you put everything live or something?"

> "Well, it was on a year out that you made like one of your temporary URLs."

> "I don't need it. I just wanted to make sure that everything was still there." / "Let's just get this done."

## Owed from This Dictation

- Refresh the agreement preview link once the running build (agent 541a5467) lands — not mid-build. Live v28 at nayanet.app/agreement is the safe current copy meanwhile.
