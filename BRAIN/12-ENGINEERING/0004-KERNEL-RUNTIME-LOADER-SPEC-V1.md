# Kernel Runtime Loader Specification V1

**Status:** PROPOSED CANONICAL — HUMAN DIRECTOR RATIFICATION REQUIRED

## Purpose

The Kernel Runtime Loader is the engineering component responsible for consuming `MANIFEST.json` and `RUNTIME-REGISTRY` to boot the nine-node semantic kernel. It bridges the gap between canonical specification and living runtime behavior.

## Boot Sequence

The loader executes the following sequence during cold boot:

```
1. READ MANIFEST.json
   → Validate schema
   → Extract node declarations and dependencies

2. READ RUNTIME-REGISTRY
   → Validate registry entries
   → Map node contracts to runtime implementations

3. RESOLVE DEPENDENCIES
   → Verify all required node contracts exist
   → Check dependency graph for cycles
   → Establish initialization order

4. INITIALIZE NODES
   → SELF: establish identity context
   → LAW: load governance contracts
   → ACT: prepare execution context
   → KNOW: restore intelligence substrate
   → PROVE: load proof records
   → CONNECT: build relationship graph
   → VERIFY: prepare outcome tracking
   → LEARN: restore verified learning
   → EVOLVE: construct successor context

5. VERIFY HEALTH
   → All nine nodes report READY
   → Dependency satisfaction confirmed
   → No unresolved critical errors

6. EMIT BOOT RECEIPT
   → Timestamp, node states, dependency graph, health status
```

## Loading Protocol

### Manifest Validation

The loader MUST validate `MANIFEST.json` against the following requirements:

| Field | Requirement |
|---|---|
| `schema` | Must match `naya.kernel.manifest.v1` |
| `nodes` | Must contain exactly 9 node declarations |
| `dependencies` | Must form a DAG (no cycles) |
| `node_contracts` | Each reference must resolve to an existing file |

### Registry Validation

The loader MUST validate `RUNTIME-REGISTRY` against the following requirements:

| Field | Requirement |
|---|---|
| `node_id` | Must match a node in MANIFEST |
| `implementation` | Must resolve to available runtime component |
| `health_endpoint` | Must be reachable for health checks |
| `status` | Must be `ACTIVE` or `DEGRADED` |

### Node Initialization Order

Nodes initialize in dependency order:

```
SELF (no dependencies)
→ LAW (depends on SELF)
→ ACT (depends on SELF, LAW)
→ KNOW (depends on SELF)
→ PROVE (depends on KNOW)
→ CONNECT (depends on KNOW, PROVE)
→ VERIFY (depends on ACT, PROVE)
→ LEARN (depends on VERIFY)
→ EVOLVE (depends on LEARN, SELF)
```

## Health Check

After initialization, the loader performs a health check on each node:

| Check | Pass Criteria | Fail Criteria |
|---|---|---|
| Identity | SELF reports valid identity context | Missing or corrupt identity |
| Authority | LAW can resolve authority | Cannot load governance contracts |
| Execution | ACT can receive authorized actions | Execution context unavailable |
| Knowledge | KNOW can retrieve canonical intelligence | Intelligence substrate unavailable |
| Proof | PROVE can assess claims | Proof records unavailable |
| Connection | CONNECT can resolve relationships | Relationship graph unavailable |
| Verification | VERIFY can compare outcomes | Outcome tracking unavailable |
| Learning | LEARN can access verified learning | Learning records unavailable |
| Evolution | EVOLVE can construct successor context | Continuity context unavailable |

### Health States

| State | Meaning | Loader Behavior |
|---|---|---|
| `READY` | Node fully operational | Proceed |
| `DEGRADED` | Node partially operational | Log warning; continue with reduced capability |
| `UNAVAILABLE` | Node cannot initialize | Halt boot; emit failure receipt |
| `FAILED` | Node failed during operation | Halt dependent nodes; emit failure receipt |

## Failure States

| Failure | Detection | Behavior |
|---|---|---|
| MANIFEST invalid | Schema validation | Halt boot; emit validation error |
| RUNTIME-REGISTRY invalid | Schema validation | Halt boot; emit validation error |
| Missing node contract | File resolution | Halt boot; emit missing contract error |
| Dependency cycle | Graph analysis | Halt boot; emit cycle detection error |
| Node initialization failure | Timeout or error | Mark node UNAVAILABLE; halt dependents |
| Health check failure | Health endpoint | Mark node DEGRADED or UNAVAILABLE |
| Intelligence substrate unavailable | KNOW health check | Mark KNOW UNAVAILABLE; halt PROVE, CONNECT |
| Governance contracts unavailable | LAW health check | Mark LAW UNAVAILABLE; halt ACT, EVOLVE |
| Boot receipt failure | Receipt generation | Log error; boot may continue with warning |

## Acceptance Criteria

- A cold boot completes with all nine nodes in READY or DEGRADED state.
- All dependency relationships are satisfied before node initialization.
- Health checks pass or produce explicit DEGRADED/UNAVAILABLE states.
- Boot receipt is emitted with complete node states and timestamps.
- Any failure produces an explicit failure receipt with diagnostic information.
- The loader never guesses or fabricates missing components.
