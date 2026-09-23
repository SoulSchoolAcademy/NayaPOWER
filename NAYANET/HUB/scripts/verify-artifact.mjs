import fs from 'node:fs';
import crypto from 'node:crypto';
import path from 'node:path';
const root=process.cwd(), dist=path.join(root,'dist');
const pairs=[
 ['index.html','index.html'],
 ['public/assistant-runtime.js','assistant-runtime.js'],
 ['public/hub-completeness.js','hub-completeness.js'],
 ['public/smart-feed.js','smart-feed.js'],
 ['public/smart-tabs.js','smart-tabs.js'],
 ['public/identity.html','identity.html'],
 ['public/name-first-auth-adapter.js','name-first-auth-adapter.js']
];
for(const [src,dst] of pairs){
 const a=path.join(root,src),b=path.join(dist,dst);
 if(!fs.existsSync(a)||!fs.existsSync(b))throw new Error('ARTIFACT_MISSING:'+src+' -> '+dst);
 const ab=fs.readFileSync(a),bb=fs.readFileSync(b);
 if(!ab.equals(bb))throw new Error('ARTIFACT_DRIFT:'+src+' -> '+dst);
 console.log('ARTIFACT_PARITY',src,'=',dst,crypto.createHash('sha256').update(ab).digest('hex'));
}
const rootHash=crypto.createHash('sha256').update(fs.readFileSync(path.join(dist,'index.html'))).digest('hex');
console.log('CANONICAL_ARTIFACT_SHA256='+rootHash);
