const { fetchBase } = require('./fetchBase6.js');
const s = fetchBase();
const lines = s.split('\n');
function show(a, b, label) {
  console.log('===== ' + label + ' lines ' + a + '-' + b + ' =====');
  for (let i = a; i <= b; i++) console.log((i) + ': ' + lines[i - 1]);
}
show(10880, 11060, 'Router definition');
