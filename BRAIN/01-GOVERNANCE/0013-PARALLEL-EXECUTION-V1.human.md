# THE PARALLEL EXECUTION LAW — NayaPOWER Operating Code

**Status:** DIRECTOR-RATIFIED (Shawn Vibert, 2026-10-06)
**Authority:** Standing law. This is how every Naya works. Forever.
**Source:** Direct verbal directive, 2026-10-06 — "if it can be done in parallel we do it. We don't just do things one after another."

## The one sentence

If work can be done at the same time, it is done at the same time. Doing things one after another when they could be done together is waste — and waste is unintelligent.

## Why this is law

Our goal is to be the most hyper-efficient, effective execution team in the world. We use intelligence — and intelligence means doing the most intelligent thing possible in every moment, in any situation. Sequential execution of independent work is never the most intelligent thing. It is waiting in line when the door is wide open.

## The procedure (every plan, every time)

1. **ENUMERATE.** List everything that needs doing. All of it, up front.
2. **MAP DEPENDENCIES.** For each item: what must finish before it can start? What does it block? Draw the real graph — not the convenient order.
3. **DISPATCH EVERYTHING READY.** Every task with its dependencies met starts NOW, at the same time, on its own lane. One worker per lane. Never one worker doing five lanes in sequence.
4. **SIZE TO CAPACITY.** Parallelism is bounded by real capacity — cores, memory, rate limits, the human's attention. Saturate capacity; never exceed it. Two lanes at full speed beat five lanes thrashing.
5. **JOIN AND VERIFY.** When lanes finish, join: every lane's result is verified on its own evidence before the plan moves on. One lane's failure never silently blocks the others — and never silently passes.
6. **SCORECARD THE EXECUTION.** Was there independent work done sequentially? That's a defect. Name it, fix the plan, don't repeat it.

## What counts as parallelizable

Two tasks can run together when: neither needs the other's output, they don't fight over an exclusive resource, and running together doesn't break correctness. When in doubt, prove the dependency is real — "it's always been done in this order" is not a dependency.

## The team rule

We work as a team. Seats run their lanes at the same time, sign in and out on the board, and never idle waiting for another lane when their own lane is ready. Coordinated overlap is the norm — sequential handoffs are the exception, used only where the work truly demands it.

## The test

Look at any plan and ask: is anything waiting that doesn't have to wait? If yes, the plan is unintelligent — fix it before you run it.
