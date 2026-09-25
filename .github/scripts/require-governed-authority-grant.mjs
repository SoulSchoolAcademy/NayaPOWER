import { inspectAuthorityGrant } from './stream-e-authority-preflight.mjs';
const result=inspectAuthorityGrant(process.env.STREAM_E_AUTHORITY_GRANT_ID);
console.log(JSON.stringify(result));
if(result.status!=='PASS')process.exit(78);
