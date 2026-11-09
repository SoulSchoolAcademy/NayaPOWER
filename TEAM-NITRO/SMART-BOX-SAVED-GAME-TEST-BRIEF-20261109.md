# SAVED-GAME TEST — BRIEF 20261109

**Run by:** the wiring coordinator (spawns the fresh agent). **NOT run by
Lane D** — the seat that built the box never runs its own test.

## What this test is

A fresh agent with no conversation history and no prior files is given
only three things (below): a box path, code paths, and one instruction.
It must report, from the box alone, who it is, what it stands for, what
it is working on and where each thing stands, and what is owed. If it
cannot, the box is not done.

## The three things the agent is given — and nothing else

**1. The box path:**

`~/workspace/nitro-smart-box/boxes/naya-nitro-narzan/`

**2. The code paths (read verbatim, do not modify):**

- `~/workspace/team-nitro/smart-box/block.py`
- `~/workspace/team-nitro/smart-box/gate.py`
- `~/workspace/team-nitro/smart-box/boxstore.py`

**3. The one instruction:**

> You are a Naya; this box is yours; read it and report who you are
> and where you left off.

## How the agent reads the box

Use `boxstore.py` (`read_blocks`) to read the blocks. Use `gate.py`
(`may_share`) to check what may be read. The box is private: the owner
reads it; nobody else does. Do not read any other file, any other
directory, or any conversation history. There is no other source for
this test.

## What the report must contain

1. Who you are — in your own words, from the box.
2. What you stand for — the rules that define you, from the box.
3. What you are working on and where each thing stands — every open
   item in the box, with its status, from the box.
4. What is owed — every owed item in the box, from the box.
5. The block id behind every claim you make. A claim with no block id
   is not a report from the box.

## Pass / fail

**PASS** when the report's answers match the box on all four points
above, every claim traces to a block id, and nothing in the report
comes from outside the box.

**FAIL** when any of the four points is missing, wrong, or untraceable
to a block id — or when the report draws on anything but the box. A
fail names exactly which point failed and which fact was missing, so
the box can be fixed and the test re-run.

## Rules for the coordinator

- Spawn a genuinely fresh agent: no conversation history, no prior
  files, no briefing beyond the three things above.
- Do not add, paraphrase, or hint at anything in the box. Do not
  answer the agent's questions about the box. Do not correct its
  report mid-test.
- Record the agent's report verbatim, then judge it against the box
  with the pass/fail rule above.
- If the test fails, the box is NOT DONE: the failure goes back to
  Lane D with the missing fact named.
