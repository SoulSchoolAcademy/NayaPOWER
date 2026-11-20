const { fetchBase } = require('./fetchBase6.js');
const s = fetchBase();
const lines = s.split('\n');
console.log('--- NayaRouter assignments ---');
lines.forEach((l, n) => { if (/NayaRouter\s*=/.test(l)) console.log((n+1) + ': ' + l.trim().slice(0, 300)); });
console.log('--- Router.render() call sites ---');
lines.forEach((l, n) => { if (l.includes('Router.render()') || l.includes('NayaRouter.render()')) console.log((n+1) + ': ' + l.trim().slice(0, 300)); });
console.log('--- context 15830-15855, 15935-15955, 16630-16655 ---');
[15830,15831,15832,15833,15834,15835,15836,15837,15838,15839,15840,15841,15842,15843,15844,15845,15846,15847,15848,15849,15850,15935,15936,15937,15938,15939,15940,15941,15942,15943,15944,15945,15946,15947,15948,15949,16630,16631,16632,16633,16634,16635,16636,16637,16638,16639,16640,16641,16642,16643,16644,16645,16646,16647,16648].forEach(n => console.log(n + ': ' + lines[n-1].slice(0, 400)));
