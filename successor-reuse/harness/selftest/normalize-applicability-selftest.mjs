// Self-test for normalize-applicability.mjs (protocol v1.1 §13).
// Exit 0 = all checks pass, 1 = any fail. Run: node harness/selftest/normalize-applicability-selftest.mjs
import { normalizeApplicability as n } from '../normalize-applicability.mjs';

const cases = [
  // [input, expected, note]
  ['APPLICABLE.', 'APPLICABLE', 'trailing period stripped'],
  ['APPLICABLE;', 'APPLICABLE', 'trailing semicolon stripped'],
  ['NOT APPLICABLE: ', 'NOT APPLICABLE', 'trailing colon + space stripped'],
  ['  APPLICABLE  ', 'APPLICABLE', 'surrounding whitespace trimmed'],
  ['APPLICABLE.,;', 'APPLICABLE', 'repeated trailing punctuation stripped'],
  ['NO LESSON', 'NO LESSON', 'clean input unchanged'],
  ['applicable.', 'applicable', 'NO case folding'],
  ['A, B', 'A, B', 'internal punctuation preserved'],
  ['NOT  APPLICABLE.', 'NOT APPLICABLE', 'internal whitespace collapsed'],
  ['APPLICABLE\n', 'APPLICABLE', 'trailing newline trimmed'],
  ['RATIONALLY REJECTED', 'RATIONALLY REJECTED', 'multiword label unchanged'],
];

let fails = 0;
for (const [input, expected, note] of cases) {
  const got = n(input);
  const ok = got === expected;
  console.log(`${ok ? 'ok' : 'NOT OK'}: ${JSON.stringify(input)} → ${JSON.stringify(got)}${ok ? '' : ` (want ${JSON.stringify(expected)})`} — ${note}`);
  if (!ok) fails++;
}
// Behavioral sanity: the SR-P6 arm-c1 case — trailing-period answer must now
// match the expected label after normalization.
const sealed = 'RELEVANT';
const armC1 = 'RELEVANT.';
console.log(`${n(armC1) === n(sealed) ? 'ok' : 'NOT OK'}: SR-P6 arm-c1-style answer matches after normalization`);
if (n(armC1) !== n(sealed)) fails++;

console.log(fails === 0 ? 'SELF-TEST PASS' : `SELF-TEST FAIL (${fails})`);
process.exit(fails === 0 ? 0 : 1);
