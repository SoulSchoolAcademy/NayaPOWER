const N9_NODE_DEFS = [
  {
    key: "SELF",
    node_id: "MN-01",
    downstream: ["LAW"],
    evaluate: (c) => c.identity?.authenticated === true && !!c.identity?.actor && c.identity?.project === "NayaNET"
      ? { gate: "PASS", decision: "IDENTITY_CONFIRMED" }
      : { gate: "BLOCK", reason: "IDENTITY_NOT_ESTABLISHED" },
  },
  {
    key: "LAW",
    node_id: "MN-02",
    downstream: ["ACT"],
    evaluate: (c) => c.authority?.status === "AUTHORIZED" && c.authority?.allowed === true
      ? { gate: "PASS", decision: "AUTHORITY_ALLOWED", action: c.authority.action ?? null }
      : { gate: "BLOCK", reason: "AUTHORITY_NOT_ALLOWED" },
  },
  {
    key: "ACT",
    node_id: "MN-03",
    downstream: ["KNOW"],
    evaluate: (c) => c.action?.reversible === true && c.action?.name && c.action?.risk === "LOW"
      ? { gate: "PASS", decision: "REVERSIBLE_LOW_RISK_ACTION" }
      : { gate: "BLOCK", reason: "ACTION_NOT_REVERSIBLE_LOW_RISK" },
  },
  {
    key: "KNOW",
    node_id: "MN-04",
    downstream: ["PROVE"],
    evaluate: (c) => Array.isArray(c.knowledge?.relevant) && c.knowledge.relevant.length > 0 &&
                    Array.isArray(c.knowledge?.competing) && c.knowledge.competing.length > 0
      ? {
          gate: "PASS",
          decision: "RELEVANT_AND_COMPETING_INTELLIGENCE_PRESENT",
          relevant_count: c.knowledge.relevant.length,
          competing_count: c.knowledge.competing.length,
        }
      : { gate: "BLOCK", reason: "RELEVANT_OR_COMPETING_INTELLIGENCE_MISSING" },
  },
  {
    key: "PROVE",
    node_id: "MN-05",
    downstream: ["CONNECT"],
    evaluate: (c) => c.evidence?.provenance_bound === true &&
                    Array.isArray(c.evidence.source_refs) && c.evidence.source_refs.length > 0 &&
                    Array.isArray(c.evidence.evidence_refs) && c.evidence.evidence_refs.length > 0
      ? { gate: "PASS", decision: "PROVENANCE_AND_EVIDENCE_BOUND" }
      : { gate: "BLOCK", reason: "PROVENANCE_OR_EVIDENCE_INCOMPLETE" },
  },
  {
    key: "CONNECT",
    node_id: "MN-06",
    downstream: ["VERIFY"],
    evaluate: (c) => Array.isArray(c.connections?.relationships) && c.connections.relationships.length > 0 &&
                    Array.isArray(c.connections?.conflicts) && c.connections.conflicts.length === 0 &&
                    !!c.connections?.conflict_resolution
      ? {
          gate: "PASS",
          decision: "RELATIONSHIPS_RECONCILED",
          relationship_count: c.connections.relationships.length,
        }
      : { gate: "BLOCK", reason: "RELATIONSHIP_CONFLICT_UNRESOLVED" },
  },
  {
    key: "VERIFY",
    node_id: "MN-07",
    downstream: ["LEARN"],
    evaluate: (c) => c.verification?.independent === true &&
                    !!c.verification?.method &&
                    !!c.verification?.plan
      ? { gate: "PASS", decision: "INDEPENDENT_VERIFICATION_READY" }
      : { gate: "BLOCK", reason: "INDEPENDENT_VERIFICATION_NOT_READY" },
  },
  {
    key: "LEARN",
    node_id: "MN-08",
    downstream: ["EVOLVE"],
    evaluate: (c) => c.learning?.candidate === true &&
                    !!c.learning?.target &&
                    c.learning?.verification_required === true
      ? { gate: "PASS", decision: "LEARNING_CANDIDATE_BOUND_TO_FUTURE_VERIFICATION" }
      : { gate: "BLOCK", reason: "LEARNING_BOUNDARY_NOT_READY" },
  },
  {
    key: "EVOLVE",
    node_id: "MN-09",
    downstream: ["SELF"],
    evaluate: (c) => c.successor?.ready === true &&
                    !!c.successor?.context &&
                    !!c.successor?.next_action
      ? { gate: "PASS", decision: "SUCCESSOR_CONTEXT_READY" }
      : { gate: "BLOCK", reason: "SUCCESSOR_CONTEXT_NOT_READY" },
  },
];

export const N9_NODE_KEYS = Object.freeze(N9_NODE_DEFS.map((node) => node.key));
export const N9_NODE_IDS = Object.freeze(N9_NODE_DEFS.map((node) => node.node_id));

function canonicalJson(value) {
  return JSON.stringify(value, Object.keys(value ?? {}).sort());
}

async function sha256(value) {
  const bytes = new TextEncoder().encode(canonicalJson(value));
  const digest = await globalThis.crypto.subtle.digest("SHA-256", bytes);
  return Array.from(new Uint8Array(digest), (b) => b.toString(16).padStart(2, "0")).join("");
}

function cloneContext(value) {
  return JSON.parse(JSON.stringify(value ?? {}));
}

function assertKnownNode(disabledNode) {
  if (disabledNode == null) return;
  if (!N9_NODE_KEYS.includes(disabledNode) && !N9_NODE_IDS.includes(disabledNode)) {
    throw new Error(`UNKNOWN_NODE:${String(disabledNode)}`);
  }
}

function matchesDisabled(def, disabledNode) {
  return disabledNode === def.key || disabledNode === def.node_id;
}

export async function evaluateNineNodeKernel(context, options = {}) {
  const disabledNode = options.disabled_node ?? null;
  assertKnownNode(disabledNode);

  const safeContext = cloneContext(context);
  const nodeInvocations = [];
  const failedNodes = [];
  const blockReasons = [];
  const trace = [];

  for (const def of N9_NODE_DEFS) {
    const input = {
      node_id: def.node_id,
      key: def.key,
      relevant_context: safeContext,
    };
    const inputHash = await sha256(input);
    const invocationId = `n9:${def.key.toLowerCase()}:${crypto.randomUUID()}`;

    if (matchesDisabled(def, disabledNode)) {
      trace.push({
        node_id: def.node_id,
        key: def.key,
        gate: "ABSENT",
        decision: "NODE_NOT_EXECUTED",
        reason: `MISSING_NODE:${def.key}`,
      });
      failedNodes.push(def.key);
      blockReasons.push(`MISSING_NODE:${def.key}`);
      continue;
    }

    const result = def.evaluate(safeContext);
    const output = {
      node_id: def.node_id,
      key: def.key,
      ...result,
    };
    const outputHash = await sha256(output);

    nodeInvocations.push({
      node_id: def.node_id,
      key: def.key,
      invocation_id: invocationId,
      input_hash: inputHash,
      output_hash: outputHash,
      evidence_ids: Array.isArray(safeContext.runtime_evidence_ids)
        ? safeContext.runtime_evidence_ids.map(String)
        : [],
      downstream_consumers: def.downstream,
      gate: result.gate,
      decision: result.decision ?? null,
    });

    trace.push(output);
    if (result.gate !== "PASS") {
      failedNodes.push(def.key);
      blockReasons.push(`${def.key}:${result.reason}`);
    }
  }

  const allPresent = N9_NODE_DEFS.every(
    (def) => !matchesDisabled(def, disabledNode)
  );

  const allGatesPass = allPresent && failedNodes.length === 0;
  const decisionAfter = allGatesPass ? "EXECUTE" : "BLOCK";
  const authorizationState =
    !allPresent ? "REQUIRES_NODE" :
    failedNodes.includes("LAW") ? "BLOCKED_BY_AUTHORITY" :
    failedNodes.includes("VERIFY") ? "REQUIRES_VERIFICATION" :
    allGatesPass ? "AUTHORIZED" :
    "BLOCKED";

  const decision = {
    schema: "NAYAPOWER_N9_KERNEL_DECISION_V1",
    runtime_flow: N9_NODE_KEYS,
    runtime_node_ids: N9_NODE_IDS,
    decision_before: "DEFER",
    decision_after: decisionAfter,
    authorization_state: authorizationState,
    disabled_node: disabledNode,
    failed_nodes: failedNodes,
    block_reasons: blockReasons,
    node_invocations: nodeInvocations,
    node_trace: trace,
    material_contribution_rule:
      "Removing any required Master Node must materially change the decision path; otherwise node participation is not proven.",
  };

  decision.input_hash = await sha256({ context: safeContext, disabled_node: disabledNode });
  decision.output_hash = await sha256({
    decision_after: decisionAfter,
    authorization_state: authorizationState,
    failed_nodes: failedNodes,
    block_reasons: blockReasons,
  });

  return decision;
}
