const { fetchBase } = require('./fetchBase6.js');
const s = fetchBase();
const lines = s.split('\n');
function show(a, b, label) {
  console.log('===== ' + label + ' lines ' + a + '-' + b + ' =====');
  for (let i = a; i <= b; i++) console.log((i) + ': ' + lines[i - 1]);
}
show(10260, 10330, 'nudge 10283');
show(10500, 10540, 'nudge 10524');
show(15200, 15260, 'hashchange re-render 15231');
show(23560, 23620, 'room yield 23579');
