const https = require('https');
const STAGE = 'naya-walk-beginning-staging.nayapower.workers.dev';
function get(p){return new Promise((res,rej)=>{const req=https.get({hostname:STAGE,path:p,headers:{'User-Agent':'Mozilla/5.0'}},(r)=>{const b=[];r.on('data',(c)=>b.push(c));r.on('end',()=>res(Buffer.concat(b).toString('utf8')));r.on('error',rej);});req.setTimeout(60000,()=>req.destroy(new Error('timeout')));req.on('error',rej);});}
(async()=>{
 const WK = await get('/welcome');
 // boot region: showDoor call at 4358157 and surrounding boot code 4357800..4361200
 console.log(WK.slice(4357800, 4361300));
})().catch(e=>{console.error('FATAL',e);process.exit(1);});
