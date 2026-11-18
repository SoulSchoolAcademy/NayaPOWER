import fs from 'node:fs';
import crypto from 'node:crypto';
import worker from '/tmp/pricing-worker-src.mjs';

const expectFile = process.argv[2];
const resp = await worker.fetch(new Request('https://nayanet.app/pricing'));
const text = await resp.text();
const expected = fs.readFileSync(expectFile, 'utf-8');
const gotBuf = Buffer.from(text, 'utf-8');
const expBuf = Buffer.from(expected, 'utf-8');
console.log('served bytes:', gotBuf.length, 'expected bytes:', expBuf.length);
console.log('served sha256:', crypto.createHash('sha256').update(gotBuf).digest('hex'));
console.log('expected sha256:', crypto.createHash('sha256').update(expBuf).digest('hex'));
console.log('MATCH:', gotBuf.equals(expBuf));
if (!gotBuf.equals(expBuf)) process.exit(1);
