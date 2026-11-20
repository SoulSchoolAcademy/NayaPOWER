const { fetchBase } = require('./fetchBase6.js');
const s = fetchBase();
const lines = s.split('\n');
for (let i = 10998; i <= 11060; i++) console.log((i) + ': ' + lines[i - 1]);
