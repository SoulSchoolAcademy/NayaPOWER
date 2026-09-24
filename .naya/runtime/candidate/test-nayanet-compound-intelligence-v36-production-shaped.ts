import { readTextFile } from "node:fs/promises";
const source=await readTextFile(new URL("./nayanet-compound-intelligence-v36-production-shaped.ts",import.meta.url));
const checks=[
 ["exact v35 mission/source structure retained",source.includes("NAYANET_PROJECT_INTELLIGENCE_RESTORE_V2")],
 ["portable verifier exists",source.includes("verifyV36PortableArtifact")],
 ["portable verifier precedes capture record",source.indexOf("verifyV36PortableArtifact") < source.indexOf("captureReceipt=await record")],
 ["portable artifact required",source.includes("body.portable_authorization")],
 ["portable artifact hash required",source.includes("body.portable_authorization_artifact_hash")],
 ["Ed25519 verification",source.includes("crypto.subtle.verify({name:\"Ed25519\"}")],
 ["existing authority validation retained",source.includes('nayanet_validate_authority_grant')],
 ["receipt carries portable artifact",source.includes("portable_authorization:portableEvidence.portable_authorization")],
 ["receipt carries artifact hash",source.includes("portable_authorization_artifact_hash:portableEvidence.portable_authorization_artifact_hash")],
 ["existing record RPC remains downstream",source.indexOf("captureReceipt=await record") < source.indexOf("const projection=await projectIntelligence")]
];
for(const [n,ok] of checks)if(!ok)throw new Error("FAIL:"+n);
console.log("V36_PRODUCTION_SHAPED_FUNCTION_STATIC_HARNESS=PASS");
console.log("all execution-seam ordering/binding guards: PASS");
console.log("production deployment: NOT RUN");
console.log("production mutation: NOT RUN");
console.log("live intelligence_commit: NOT RUN");
