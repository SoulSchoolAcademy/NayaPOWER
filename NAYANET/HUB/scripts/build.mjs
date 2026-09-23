import fs from 'node:fs';
import path from 'node:path';

const root=process.cwd();
const dist=path.join(root,'dist');
fs.rmSync(dist,{recursive:true,force:true});
fs.mkdirSync(dist,{recursive:true});
fs.copyFileSync(path.join(root,'index.html'),path.join(dist,'index.html'));
fs.cpSync(path.join(root,'public'),dist,{recursive:true});
console.log('HUB_BUILD_COMPLETE');
console.log('SOURCE=index.html');
console.log('RUNTIME=public/*');
console.log('ARTIFACT=dist/*');
