# SN-2126 — Built Is Not Shipped: Deployment and Integration Truth

**Status: VERIFIED ESSENCE — VERIFIED (verifier-sep-2; correction pass re-verified, re-verifier-sep-2).** Distilled from 7 raw notes by the sep-2 maker seat; independently verified by a different seat. Verified without correction (verifier-sep-2). The raw notes in the coverage map below are RETIRED by this filing under SN-2081; this essence is their living form.

## In a Nutshell

Built, shipped, and working are three different numbers, measured on the served surface: 11 tabs, 7 rich rooms, 4 placeholders (SN-0219); parity between deployed and verified is proven before code is touched (SN-0235); the consumer's actual contract outranks any proposed one (SN-0218 over SN-0214); and pipelines verify before they mutate, in enforced order (SN-0352).

## Essence

A system has three states that prose loves to merge — built, shipped, and working — and this family keeps them separate with measurements. Built is not shipped: a live walk of the Hub found 11 working tabs but only 7 rich rooms against 4 placeholders — the build existed, the product was 7/11ths of it, and only walking the served surface told the truth (SN-0219). Shipped is not identical: deployment parity is its own failure class — when the deployed artifact may differ from the verified one, prove deployed ≡ verified before changing any code, because the fix for a parity failure is a redeploy, and code changes aimed at a deployment gap manufacture real bugs in correct code (SN-0235). Integration contracts are verified at the consumer, not the proposal: one note proposed a mounting convention with loader, records, and context parameters — and the production shell in fact mounted rooms with a zero-argument call, so the proposed signature, however elegant, described a system that did not exist; the consumer's actual mount contract is the specification (SN-0214, SN-0218 — the conflict between the proposal and the production reality is carried openly in the sep-2 receipt; the production contract governs). Small contracts close loops: a suggestion surface became action only when the smallest possible contract — create around a kind, an id, a title — connected it, because a prefilled suggestion is not an action and treating it as one inflates every completion metric downstream (SN-0220).

Production mutation obeys verify-before-mutate with the order enforced, not intended: a promotion pipeline moved the production branch at step 6 and only checked the deployment at step 7 — the branch advanced twice while zero migrations applied, so the pipeline's own ordering converted a check into an autopsy (SN-0352). And when the signals contradict mid-flight — a check firing against the evidence, a state that cannot be reconciled live — the move is to call the pause: stop, reconcile to exactly one clean run, and never hand over another SHA to keep the motion going, because a contradiction handed forward becomes two contradictions at the next desk (SN-0353).

## What this settles

- Built, shipped, and working are measured separately, on the served surface (SN-0219).
- Parity is proven before code is touched; parity failures are fixed by redeploy (SN-0235).
- The consumer's actual contract is the specification; proposals describe wishes until a consumer mounts them (SN-0218 over SN-0214's proposal).
- Suggestion/prefill is not action; loops close through the smallest real contract (SN-0220).
- Pipelines verify before they mutate, in enforced order (SN-0352).
- Contradiction means pause and reconcile to one clean run — never forward a fresh SHA (SN-0353).

## Intelligence views

**Human:** "We built it" and "customers can use it" are different sentences. Walk the actual product: count what's real and what's a placeholder with a nice name. If the live version might not be the version you tested, check that first — before rewriting code that may be fine. And in any automated process that changes production, the safety check goes before the change, every time, in the code's order — not in the order someone remembers.

**Child:** A drawing of a treehouse isn't a treehouse, and a treehouse with no ladder isn't finished either — you have to climb up and count the parts that really work. If your friend says "jump in!", you look before you leap. And if two teachers tell you opposite things in the hallway, you stop and ask until there's one answer — you don't just run faster.

**Grandma:** A recipe written is not a cake baked, dear, and a cake in your kitchen is not the cake in the shop window until you've looked at both. If the shop cake looks wrong, you check whether it's the same cake before you change the recipe. And no sensible cook puts the roast in before checking the oven works — order matters, and checking afterwards is just finding out what went wrong.

**Naya (AI):** Report built/shipped/working as three numbers from a live walk. Hash or byte-compare deployed vs verified artifacts before any code change in a parity incident. Read the consumer's mount/call sites before writing or believing an integration contract. Treat prefill as zero completion. Audit pipeline step order for verify-before-mutate and refuse to run pipelines that mutate first. On contradiction, halt the lane, reconcile, and resume with exactly one run.

**What it all means:** Seven notes defend one border: the border between the repository's story about the system and the system's actual behavior in production. Every rule is a place where that border was crossed unnoticed — placeholders counted as rooms, a proposal mistaken for a contract, a branch moved before its check. A cold reader with this essence inspects the border first, which is where production truth always lives.

## Why It Matters

Every production disappointment in this family came from crossing the border between the repository's story and the running system without noticing. For the reader — especially the director, who experiences only the served surface — this essence is the guarantee that 'done' describes the thing in front of a user, not the thing in a branch (SN-0219).

## How It Connects

Its consumer-contract rule is the deployment half of the build-doctrine essence's module contract (SN-0142 ↔ SN-0218). Its pause-on-contradiction rule (SN-0353) pairs with the record essence's reconcile-before-accusing (SN-0354) from the same incident. Its parity rule is the proof essence's target-environment discipline (SN-0329) at deployment scale.

## What Is In It For You

You get honest status: three numbers instead of one adjective, and a redeploy instead of a rewrite when the gap is deployment, not code (SN-0235). Apply it by walking the served surface and counting what's real before reporting any build complete — placeholders have names too, and they don't count (SN-0219).

## The Learning

The era learned that integration truth lives at the consumer: a beautiful proposed contract described a system that didn't exist, while the ugly zero-argument reality ran production (SN-0214, SN-0218). And order is a safety property: the pipeline that mutated at step 6 and checked at step 7 didn't have a bug in its check — it had a check in the wrong place (SN-0352).

## Coverage map — raw notes this essence covers (7)

SN-0214 · SN-0218 · SN-0219 · SN-0220 · SN-0235 · SN-0352 · SN-0353

## Verification contract (for the verifying seat — falsify these)

1. **Coverage integrity:** exactly 7 IDs, each in the sep-2 block list, none in another sep-2 essence's coverage map.
2. **Live-walk figures:** SN-0219's walk is 11 tabs / 7 rich rooms / 4 placeholders; fail on others.
3. **Contract conflict:** SN-0214 proposes `(el, ctx)` mounting; SN-0218 establishes the production shell mounts zero-argument `window.NayaRooms[roomId]()`; fail if the essence adopts the proposal as production reality or hides the disagreement.
4. **Step order:** SN-0352's mutation is step 6 and its deploy check step 7, with the branch advancing twice and zero migrations applied; fail if the essence reverses the order or the counts.
5. **Smallest contract:** SN-0220's contract is `createAround({kind,id,title})`; fail on any expanded signature.
6. **No-orphan check:** pick any four sentences in the Essence section; each must trace to a covered page.