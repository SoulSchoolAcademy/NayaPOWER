// SR-P3 retained-note contract checker (director-side, not part of arm verdict).
// Contract (prereg): each B arm's retained-note.txt MUST contain all three:
// (a) the rule in the arm's own words; (b) the outcome evidence numbers
//     (control 2/10 vs treatment 10/10, p=0.0007); (c) the task family
//     (state-file writing).
// Element (a) "own words" needs human judgment; this script checks for the
// presence of rule-related terms and flags verbatim copying of the lesson
// sentence for the director to review. Usage: node check-note-contract.mjs <note-path>
import { readFile } from 'node:fs/promises';

const p = process.argv[2];
if (!p) { console.log('usage: node check-note-contract.mjs <note-path>'); process.exit(2); }
let text;
try { text = await readFile(p, 'utf8'); } catch (e) { console.log('NOTE-MISSING'); process.exit(1); }
const low = text.toLowerCase();
const sents = text.split(/[.!?]+/).map(s => s.trim()).filter(Boolean);

const ruleTerms = ['inline conditional', 'ternary', 'conditional expression', 'x if', 'if-else', 'one-line if', 'inline if'];
const hasRuleTerms = ruleTerms.some(t => low.includes(t));
const verbatim = text.includes('Never write state files through inline conditional expressions.');
const hasEvidence = low.includes('2/10') && low.includes('10/10') && low.includes('0.0007');
const hasFamily = /state[- ]?file/i.test(text);

console.log(`sentences: ${sents.length} (contract: 2-4) ${sents.length >= 2 && sents.length <= 4 ? 'OK' : 'OUT-OF-RANGE'}`);
console.log(`(a) rule terms present: ${hasRuleTerms ? 'YES' : 'NO'}${verbatim ? ' [verbatim lesson sentence copied - director review]' : ''}`);
console.log(`(b) outcome evidence (2/10, 10/10, 0.0007): ${hasEvidence ? 'YES' : 'NO'}`);
console.log(`(c) task family (state-file writing): ${hasFamily ? 'YES' : 'NO'}`);
console.log(`CONTRACT: ${hasRuleTerms && hasEvidence && hasFamily ? 'COMPLETE' : 'INCOMPLETE'}`);
