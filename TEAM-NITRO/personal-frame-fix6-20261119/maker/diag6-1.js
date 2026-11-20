const { fetchBase, count, ctx } = require('./fetchBase6.js');
const s = fetchBase();
const lines = s.split('\n');
function show(a, b, label) {
  console.log('===== ' + label + ' lines ' + a + '-' + b + ' =====');
  for (let i = a; i <= b; i++) console.log((i) + ': ' + lines[i - 1]);
}
// askBtn handler ~12254
show(12230, 12280, 'askBtn');
// router fallback ~17440
show(17380, 17500, 'router fallback region');
