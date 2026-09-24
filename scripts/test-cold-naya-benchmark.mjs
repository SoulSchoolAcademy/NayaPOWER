import assert from "node:assert/strict";
const required=["SUPERBRAIN/AI-BOOT/START-HERE.md","SUPERBRAIN/MASTER-NOTES/NAYAPOWER-CANONICAL-SOURCE-MAP.md",".naya/codex/11-RUNTIME-CONSTITUTION.md",".naya/control-plane/MAP.json",".naya/control-plane/STATE.json",".naya/control-plane/BLOCKS.json",".naya/control-plane/PROOF.json",".naya/control-plane/BATON.json"];
for(const p of required) assert.ok((await import("node:fs")).existsSync(p),"missing "+p);
console.log("cold-naya-benchmark smoke test PASS");