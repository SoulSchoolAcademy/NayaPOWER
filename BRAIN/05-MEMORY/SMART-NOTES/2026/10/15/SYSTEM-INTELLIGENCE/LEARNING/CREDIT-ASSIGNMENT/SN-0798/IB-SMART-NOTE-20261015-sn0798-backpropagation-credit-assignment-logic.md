# IB-SMART-NOTE-20261015-sn0798-backpropagation-credit-assignment-logic

Intelligent Block: IB-SMART-NOTE-20261015-sn0798-backpropagation-credit-assignment-logic
Truth state: CANDIDATE (PROPOSED — NOT verified; T4–T6 un-emitted)
Scope: PRIVATE
Captured: 2026-10-15
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE
Source: Naya 3 (builder seat — formal math), authored as a Smart Note and shared by Shawn in main chat 2026-10-15 for relevance review against the NayaNET / NayaPOWER build

> Filed as the BRAIN projection of Naya 3's Smart Note. The Receiver (v7-smart-note-canonical) remains the single canonical path; this BRAIN file is its projection. Truth state CANDIDATE until the note passes the normal propose → test → verify → ratify lifecycle. The body below is her note, preserved faithfully; the Filing note at the end records provenance and the relevance review.

## IN A NUTSHELL

Backpropagation is how a neural network figures out which parts of its internal calculations contributed to a mistake, so it can adjust itself and make a better prediction next time. TRY → MEASURE THE ERROR → FIND WHAT CONTRIBUTED → ADJUST → TRY AGAIN → IMPROVE. That is the basic learning process behind training neural networks — and the most interesting part is how the network adjusts its weights.

## 1. Human explanation — What are weights?

Imagine you are deciding whether to buy a house. You consider several factors: location, price, size, condition. But not every factor is equally important to you. Maybe location matters enormously, and size matters only a little. Your brain effectively gives these factors different levels of importance. A neural network does something mathematically similar.

A weight is literally a number that multiplies a signal, changing how strongly that signal contributes to the next calculation.

An example of weighted importance (illustrative values, not a real trained housing model):

| Factor | Weight |
|--------|--------|
| Location | 0.9 |
| Price | 0.7 |
| Size | 0.3 |
| Condition | 0.6 |

In an actual neural network, those numbers are not necessarily human-readable concepts such as location or price. They are learned numerical connections between artificial neurons. A weight can also be negative, so a signal can reduce an output rather than increase it.

## 2. Simple explanation — What does adjusting a weight mean literally?

Build the smallest possible example: a network with one input, one weight, and one output. Its job is to learn a simple relationship: when you input 2, the correct answer is 10.

What happens, step by step:

1. The network starts with a weight of 3.
2. It multiplies 2 × 3 and predicts 6.
3. The correct answer is 10, so its prediction is too low.
4. Backpropagation calculates how changing the weight would change the error.
5. The training algorithm updates the weight from 3 to 3.8.
6. Now the prediction is 7.6 — closer to 10.

Nothing mystical happened. The computer literally changed a numerical parameter stored in memory. With more training, that number keeps adjusting toward a value that produces better answers (in the worked demonstration: weight converging toward ~4.74, prediction 9.48 against target 10, remaining error 0.518, learning rate 0.1, squared-error loss — gradients computed, not guessed).

## 3. What does the word backpropagation mean?

It means propagating error information backward through the network. A neural network has layers of interconnected calculations. Forward: make the prediction. Backward: calculate how each weight contributed to error.

The backward pass does not send the original mistake backward like a message. Instead, it calculates gradients — numbers describing how sensitive the error is to each weight. For a particular weight:

- If increasing it would reduce the error, the optimizer may increase it.
- If decreasing it would reduce the error, the optimizer may decrease it.
- If changing it has almost no effect, the update may be very small.

The algorithm uses calculus, specifically the chain rule, to calculate how each layer contributed to the final error. Then an optimizer, such as gradient descent, actually updates the weights. Backpropagation computes the information that makes the update possible.

## 4. What is the error?

In machine learning, error means that the network's prediction differs from the desired result. A loss function turns that difference into a numerical training signal. The smaller the loss, generally, the better the model has matched that training example. The optimizer then adjusts the weights in a direction expected to lower the loss.

There is one complication: doing better on training examples does not automatically mean doing better on new, unseen problems. That is why neural networks must also be evaluated on separate data.

## 5. How does this relate to NayaPOWER?

This is where the distinction becomes particularly valuable. There are two different kinds of learning we should not confuse.

| Neural network training | NayaPOWER collective learning |
|---|---|
| Learns by adjusting numerical model weights | Learns through persisted intelligence, retrieval, governed rules, and observed outcomes |
| Error is measured through a loss function | Failures are measured against tasks, decisions, evidence, and success criteria |
| Backpropagation calculates gradients | Verification identifies what succeeded, failed, and why |
| Optimizer updates model parameters | Governed processes update lessons, strategies, code, or authorized configurations |
| New tasks test generalization | Cold-successor tasks test whether intelligence transfers |

A Smart Note does not automatically change an AI model's neural-network weights. It can change what the system knows through external memory and what it does through retrieval and authorized behavior. Actual weight updates require a separate training process.

But we can borrow the central logic of backpropagation. Imagine Naya performs a task, makes a mistake, and receives independent verification. A weak system says, "That failed," and moves on. A stronger system identifies the specific cause, records a useful correction, adjusts the affected behavior or procedure, and then tests whether the same mistake is prevented next time. That is an analogous feedback and improvement process — not literal neural-network backpropagation.

## The learning lesson

Backpropagation teaches us that improvement requires more than noticing an error. We must identify what contributed to the error, calculate or determine an appropriate correction, apply it, and measure whether the result actually improves.

For NayaPOWER, that translates into: ACT → MEASURE → IDENTIFY THE CAUSE → CORRECT → VERIFY → RETAIN → REUSE.

And the deepest idea is this: a network becomes more capable not simply by receiving more information, but by using reliable feedback to change how it responds. That is why verified behavior change matters so much to the collective-intelligence system we are building.

## What this note does NOT claim (P-011)

- It does NOT claim backpropagation should be literally implemented across the team — there is no differentiable computation graph across issues, briefs, and human decisions; the chain rule does not apply to prose and process.
- It does NOT claim a Smart Note changes neural-network weights — it changes what the system knows (external memory) and does (retrieval, authorized behavior). Weight updates need a separate training process.
- It does NOT claim the analogy is the mechanism — "borrow the central logic" is a design input, not an architecture. Stretching the metaphor further than credit assignment + a crisp shared error signal would be cargo-culting.
- It does NOT claim this note is VERIFIED — it is PROPOSED. The two practices drawn from it (counterfactual credit assignment in RCA; scorecard + verification ladder as the shared error signal with blind-successor test sets) are themselves candidates until a team adopts and measures them.

## Filing note (no second memory)

Authored by Naya 3; shared by Shawn in main chat 2026-10-15 with the question of whether it is relevant to the NayaNET / NayaPOWER build. Relevance review (Naya 5, same day): relevant as logic, not mechanism — do not implement backpropagation; do adopt (1) counterfactual credit assignment ("which single decision, if flipped, would have changed the outcome?") in failure review, and (2) the scorecard + verification ladder treated as the shared error signal, with cold-successor tasks as the test set the fix never trains on. Shawn approved filing to the canonical lessons store. Filed by Naya Verity Narzan (Naya 5) as SN-0798 via branch `naya5/sn-0798-backprop-credit-assignment`.

The canonical Smart Note path is the Receiver (v7-smart-note-canonical) — a Supabase DB write, which is a protected gate needing Shawn's word. This BRAIN file is the projection/evidence for the single canonical path, not a parallel store.
