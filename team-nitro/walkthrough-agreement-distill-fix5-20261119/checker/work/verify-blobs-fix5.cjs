#!/usr/bin/env node
// Fix-5 checker: fresh git blob API reads via gh-direct.py (never contents API)
const { execFileSync } = require('child_process');
const crypto = require('crypto');
const fs = require('fs');
const path = require('path');
const CK = '/home/hatch/workspace/team-nitro/walkthrough-agreement-distill-fix5-20261119/checker';
const OUT = CK + '/work/blob-verify.json';
const GH = '/home/hatch/workspace/team-nitro/gh-direct.py';
const REPO = 'SoulSchoolAcademy/NayaPOWER';
const BRANCH = 'walkthrough/agreement-distill-fix5-20261119';
const EXPECT_TIP = 'f38e63402823ef884e439a9ed6e4550a7f2e296a';
const PARENT_TIP = 'd5003b2fd5c59e352b84169294b2773263876e01';
const EXPECT = {
  'team-nitro/agreement-unfold-fix-20261117/agreement-unfold-fixed.html': {bytes:142532, sha256:'a3b3907f2f80d09a14c1e7e8bfb7a00c63332a7b26ac2707912c39436e177b98', blob:'1f0b04747e3315be6f1b619c1411e5e14fbdc1bb'},
  'team-nitro/walk-v23-assembly-20261114/welcome-staged.html': {bytes:1930947, sha256:'57ebe2d295b494ebe8d0e8d3c23de0a89d0025089991a7422ffa514cc4a636d6', blob:'00082c3d65801997f1dcb035bea6ee51bf600737'},
  'team-nitro/walk-v23-assembly-20261114/walk-beginning-fixed.html': {bytes:4363683, sha256:'856d392c439ebb5cb97aac27f34abc3b97b52b8b6bdc55b50abac9768e198b4d', blob:'2f7a5e3ef599e00cb39c1e577bcb42563cd7ed81'},
  'team-nitro/walk-v23-assembly-20261114/identity-fixed.html': {bytes:404147, sha256:'fef65d2cdbf2f1e8c096548df9adcdb465ac38a628f299c8e7cee2fb57703f52', blob:'b3e5af088ef1d516079d96eeaa61d811d7889b8e'},
  'team-nitro/walk-v23-assembly-20261114/walk-beginning-staging-worker.js': {bytes:8463055, sha256:'c9bc8fedcbad3299654c85bd17832aa5a0b205e238dedf53aa98ac1f03b33586', blob:'0413500982bc14dfbe5534cbe82cd9c75a68696a'},
  'team-nitro/walk-v23-assembly-20261114/build-v23-staging-worker.py': {bytes:96371, sha256:'7ce1a895051cd6e48f9c30cfde0a1b3f7392e16e9c7e5cb604d9beefb90aea77', blob:'2299b99155e442257ca46eeb2c777ad4816ff6b0'},
};
function gh(p){
  const out = execFileSync('python3',[GH,'GET',p],{encoding:'utf8',maxBuffer:64*1024*1024,timeout:120000});
  const i = out.indexOf('{');
  return JSON.parse(out.slice(i));
}
function getBlob(sha){
  const j = gh(`/repos/${REPO}/git/blobs/${sha}`);
  if(!j.content) throw new Error('empty blob content for '+sha+' encoding='+j.encoding);
  return Buffer.from(j.content.replace(/\n/g,''),'base64');
}
const result = {branch:BRANCH, expectedTip:EXPECT_TIP, expectedParent:PARENT_TIP, ref:null, files:{}, errors:[]};
try{
  const ref = gh(`/repos/${REPO}/git/ref/heads/${BRANCH}`);
  result.ref = {ref:ref.ref, sha:ref.object && ref.object.sha, type:ref.object && ref.object.type};
  result.tipMatch = result.ref.sha === EXPECT_TIP;
  console.log('REF', JSON.stringify(result.ref), 'tipMatch', result.tipMatch);
}catch(e){ result.errors.push('ref: '+e.message); console.log('REF ERROR', e.message); }
let tip = result.ref && result.ref.sha;
if(tip){
  try{
    const commit = gh(`/repos/${REPO}/git/commits/${tip}`);
    result.commitMessage = commit.message;
    result.treeSha = commit.tree.sha;
    result.parents = commit.parents && commit.parents.map(p=>p.sha);
    result.parentMatch = (result.parents||[]).includes(PARENT_TIP);
    console.log('PARENTS', JSON.stringify(result.parents), 'parentMatch', result.parentMatch);
    const tree = gh(`/repos/${REPO}/git/trees/${commit.tree.sha}?recursive=1`);
    const byPath = {};
    for(const e of tree.tree||[]) byPath[e.path]=e;
    for(const [p,exp] of Object.entries(EXPECT)){
      const ent = byPath[p];
      const rec = {treeBlob: ent?ent.sha:null, treeSize: ent?ent.size:null, expectedBlob:exp.blob, blobMatch: ent?ent.sha===exp.blob:null};
      try{
        const buf = getBlob(exp.blob);
        rec.bytes = buf.length;
        rec.sha256 = crypto.createHash('sha256').update(buf).digest('hex');
        rec.bytesMatch = buf.length===exp.bytes;
        rec.shaMatch = rec.sha256===exp.sha256;
        rec.gitHash = crypto.createHash('sha1').update(Buffer.concat([Buffer.from(`blob ${buf.length}\0`),buf])).digest('hex');
        rec.gitHashMatch = rec.gitHash===exp.blob;
        fs.writeFileSync(path.join(CK,'work','fix5-'+path.basename(p)), buf);
      }catch(e){ rec.error = e.message; result.errors.push(p+': '+e.message); }
      result.files[p]=rec;
      console.log(p, JSON.stringify(rec));
    }
  }catch(e){ result.errors.push('tree: '+e.message); console.log('TREE ERROR', e.message); }
}
fs.writeFileSync(OUT, JSON.stringify(result,null,2));
console.log('WROTE', OUT);
