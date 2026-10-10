"""NayaPOWER Node Orchestrator — durable event → nine-node execution.

Naya 1's assembly-plan step 3: "each completed stage emits a durable result,
the next stage consumes that result, and failures become explicit, recoverable
states. A saved note must not silently stop at the filing stage."

This package is the state machine. It does NOT implement node logic — it binds
and executes the real implementations:

  SELF    → kernel/self_node.py (Python, in-process)
  LAW     → supabase/functions/nayanet-law-runtime/law.ts (node bridge)
  ACT     → supabase/functions/nayanet-act-runtime/act.ts (node bridge)
  KNOW    → supabase/functions/nayanet-know-runtime/know.ts (node bridge)
  PROVE   → supabase/functions/nayanet-prove-runtime/prove.ts (node bridge)
  CONNECT → tools/connect_node.py::ConnectNode.build_graph (in-process Python)
  VERIFY  → tools/learning_admission_gate.py (pinned behavioral twin of the
            WO3 TypeScript gate; production binding targets the TS gate
            endpoint once merged and deployed)
  LEARN   → NOT_IMPLEMENTED (no implementation exists in the repository)
  EVOLVE  → NOT_IMPLEMENTED (no implementation exists in the repository)

Laws honored here:
- No silent fallback to PASS. A missing stage reports NOT_IMPLEMENTED loudly.
- Failures are explicit, named, recoverable states — never silent drops.
- Idempotent event obligation: the same capture committed twice yields one event.
- A run is SUCCESS only when every stage completed. Anything less is
  INCOMPLETE (missing stages) or FAILED/BLOCKED/REJECTED — never SUCCESS.
"""

from .orchestrator import NodeOrchestrator, RunStatus, StageStatus
from .event_store import EventStore, commit_event
from .run_state import RunStore

__all__ = [
    "NodeOrchestrator",
    "RunStatus",
    "StageStatus",
    "EventStore",
    "commit_event",
    "RunStore",
]
