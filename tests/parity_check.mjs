// Parity check: run the TS port against every fixture, compare with Python verdicts.
import { readFileSync } from "fs";
import { admit_candidate } from "../supabase/functions/nayanet-learning-verify/admission_gate.ts";

const fixtures = JSON.parse(readFileSync(new URL("./admission_gate_fixtures.json", import.meta.url), "utf-8"));

let pass = 0, fail = 0;
const failures = [];
for (const fx of fixtures) {
  let got;
  try {
    got = admit_candidate(fx.input);
  } catch (e) {
    got = { error: String(e && e.message || e) };
  }
  const exp = fx.expected;
  const match =
    got.admitted === exp.admitted &&
    got.admitted_as === exp.admitted_as &&
    JSON.stringify(got.reasons || []) === JSON.stringify(exp.reasons);
  if (match) {
    pass++;
  } else {
    fail++;
    failures.push({ name: fx.name, expected: exp, got });
  }
}
console.log(`parity: ${pass} pass, ${fail} fail of ${fixtures.length}`);
for (const f of failures) {
  console.log(`MISMATCH ${f.name}`);
  console.log(`  expected: ${JSON.stringify(f.expected)}`);
  console.log(`  got:      ${JSON.stringify(f.got)}`);
}
process.exit(fail > 0 ? 1 : 0);
