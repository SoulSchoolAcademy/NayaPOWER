// Candidate bounded tests; run node --test tools/qa/activation_receipt_consistency.test.mjs
import test from "node:test";
import assert from "node:assert/strict";
import {checkActivationReceipt} from "./activation_receipt_consistency.mjs";
const A="a".repeat(40), B="b".repeat(40), C="c".repeat(40), D="d".repeat(40), G="e".repeat(64), F="f".repeat(64), R="1".repeat(64);
const now="2026-10-09T14:55:00.000Z";
const valid={"schema":"naya.activation.receipt.v2","status":"ACTIVATED","session_id":"cold-naya-1","naya_identity":"Naya QA","human_authority":"Human Director","repository":"SoulSchoolAcademy/NayaPOWER","job":"test","gates":["law"],"proof_plan":"independent tests","main_sha":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","loaded":{"design_blob":"bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb","blocks_blob":"cccccccccccccccccccccccccccccccccccccccc","goals_digest":"eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee","feed_digest":"ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"},"activated_at":"2026-10-09T14:00:00.000Z"};
const expected={"main_sha":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","design_blob":"bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb","blocks_blob":"cccccccccccccccccccccccccccccccccccccccc","goals_digest":"eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee","feed_digest":"ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff","receipt_sha256":"1111111111111111111111111111111111111111111111111111111111111111"};
const marker="<!-- NAYA-ACTIVATION-RECEIPT-SHA256:"+R+" -->";
const scenarios=[
["valid",valid,expected,marker,"CONSISTENT_FOR_INDEPENDENT_REVIEW"],
["missing",null,expected,marker,"REJECT"],
["missing trusted state",valid,null,marker,"REJECT"],
["stale main",valid,{...expected,main_sha:D},marker,"REJECT"],
["design drift",{...valid,loaded:{...valid.loaded,design_blob:D}},expected,marker,"REJECT"],
["block drift",{...valid,loaded:{...valid.loaded,blocks_blob:D}},expected,marker,"REJECT"],
["goal drift",{...valid,loaded:{...valid.loaded,goals_digest:"9".repeat(64)}},expected,marker,"REJECT"],
["feed drift",{...valid,loaded:{...valid.loaded,feed_digest:"8".repeat(64)}},expected,marker,"REJECT"],
["expired",{...valid,activated_at:"2026-10-09T08:00:00.000Z"},expected,marker,"REJECT"],
["future",{...valid,activated_at:"2026-10-09T16:00:00.000Z"},expected,marker,"REJECT"],
["missing citation",valid,expected,"<main>hi</main>","REJECT"],
["missing proof",{...valid,proof_plan:""},expected,marker,"REJECT"],
["wrong status",{...valid,status:"ACTIVE"},expected,marker,"REJECT"],
["untrusted digest",valid,{...expected,receipt_sha256:"INVALID"},marker,"REJECT"]
];
for(const [name,receipt,state,artifact,result] of scenarios)test(name,()=>{
  const output=checkActivationReceipt(receipt,state,artifact,now);
  assert.equal(output.readiness,result);
  assert.equal(output.authorized,false);
  assert.equal(output.verified,false);
  if(result==="REJECT")assert.ok(output.violations.length>0);
});
