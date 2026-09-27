import assert from "node:assert/strict";
import testFn from "node:test";

import { evaluateNineNodeKernel, N9_NODE_KEYS } from "../n9_kernel_decision.mjs";

function baseContext() {
  return {
    identity: { authenticated: true, actor: "naya", project: "NayaNET", scope: "SYSTEM" },
    authority: { status: "AUTHORIZED", allowed: true, action: "reversible_kernel_probe" },
    action: { name: "reversible_kernel_probe", reversible: true, risk: "LOW" },
    knowledge: {
      relevant: [{ id: "knowledge-1", claim: "relevant intelligence" }],
      competing: [{ id: "knowledge-2", claim: "competing intelligence" }],
    },
    evidence: {
      source_refs: ["source-1"],
      evidence_refs: ["evidence-1"],
      provenance_bound: true,
    },
    connections: {
      relationships: ["SELF->LAW", "LAW->ACT", "KNOW<->CONNECT"],
      conflicts: [],
      conflict_resolution: "NONE_REQUIRED",
    },
    verification: {
      independent: true,
      method: "independent-outcome-verification",
      plan: "verify observable outcome after action",
    },
    learning: {
      candidate: true,
      target: "kernel-behavior",
      verification_required: true,
    },
    successor: {
      ready: true,
      context: "durable successor context prepared",
      next_action: "continue from verified result",
    },
  };
}

testFn("full kernel executes all nine nodes and permits a safe authorized action", async () => {
  const result = await evaluateNineNodeKernel(baseContext());

  assert.deepEqual(result.runtime_flow, N9_NODE_KEYS);
  assert.equal(result.decision_after, "EXECUTE");
  assert.equal(result.authorization_state, "AUTHORIZED");
  assert.equal(result.node_invocations.length, 9);
  assert.deepEqual(result.node_invocations.map((x) => x.key), N9_NODE_KEYS);
  for (const invocation of result.node_invocations) {
    assert.ok(invocation.invocation_id);
    assert.ok(invocation.input_hash);
    assert.ok(invocation.output_hash);
    assert.ok(Array.isArray(invocation.downstream_consumers));
    assert.equal(invocation.gate, "PASS");
  }
});

for (const key of N9_NODE_KEYS) {
  testFn(`healthy kernel ablation of ${key} materially changes the decision`, async () => {
    const full = await evaluateNineNodeKernel(baseContext());
    const ablated = await evaluateNineNodeKernel(baseContext(), { disabled_node: key });

    assert.equal(full.decision_after, "EXECUTE");
    assert.equal(ablated.decision_after, "BLOCK");
    assert.ok(ablated.block_reasons.includes(`MISSING_NODE:${key}`));
    assert.equal(ablated.node_invocations.some((x) => x.key === key), false);
  });
}

const nodeFailures = {
  SELF: (ctx) => { ctx.identity.authenticated = false; },
  LAW: (ctx) => { ctx.authority.status = "BLOCKED"; ctx.authority.allowed = false; },
  ACT: (ctx) => { ctx.action.reversible = false; },
  KNOW: (ctx) => { ctx.knowledge.relevant = []; },
  PROVE: (ctx) => { ctx.evidence.provenance_bound = false; ctx.evidence.evidence_refs = []; },
  CONNECT: (ctx) => { ctx.connections.conflicts = [{ id: "conflict-1" }]; },
  VERIFY: (ctx) => { ctx.verification.independent = false; },
  LEARN: (ctx) => { ctx.learning.candidate = false; },
  EVOLVE: (ctx) => { ctx.successor.ready = false; },
};

for (const key of N9_NODE_KEYS) {
  testFn(`failed ${key} contributes a blocking reason`, async () => {
    const ctx = baseContext();
    nodeFailures[key](ctx);

    const full = await evaluateNineNodeKernel(ctx);

    assert.equal(full.decision_after, "BLOCK");
    assert.ok(full.failed_nodes.includes(key));
    assert.ok(full.block_reasons.some((x) => x.startsWith(`${key}:`)));
  });
}

testFn("invalid node key is rejected", async () => {
  await assert.rejects(
    () => evaluateNineNodeKernel(baseContext(), { disabled_node: "MN-99" }),
    /UNKNOWN_NODE/
  );
});
