#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import { execFileSync } from "node:child_process";
const root=process.cwd();
const files=execFileSync("git",["ls-files"],{encoding:"utf8"}).split(/\r?\n/).filter(Boolean);
const groups=new Map();
const classify=p=>{const x=p.toLowerCase();if(/(^|\/)(archive|archived|historical|legacy)(\/|$)/.test(x))return"HISTORICAL";if(/(^|\/)(dist|build|generated)(\/|$)/.test(x))return"DERIVED";if(/(^|\/)(test|tests|fixtures|proof)(\/|$)/.test(x))return"EVIDENCE_OR_TEST";if(/(^|\/)(superbrain|\.naya\/control-plane)(\/|$)/.test(x))return"CANONICAL_OR_CONTROL";return"UNCLASSIFIED"};
for(const rel of files){const p=path.join(root,rel);let st;try{st=fs.statSync(p)}catch{continue}if(!st.isFile()||st.size>5_000_000)continue;const h=crypto.createHash("sha256").update(fs.readFileSync(p)).digest("hex");if(!groups.has(h))groups.set(h,[]);groups.get(h).push(rel)}
const exactDuplicates=[...groups.values()].filter(x=>x.length>1).map(paths=>({paths,classes:paths.map(classify)}));
const artifact={schema:"NAYANET_ARCHITECTURAL_GARBAGE_INVENTORY_V1",status:"PROPOSAL_ONLY",deletion_performed:false,tracked_files_scanned:files.length,exact_duplicate_groups:exactDuplicates.length,exact_duplicates:exactDuplicates.slice(0,100),rules:["No deletion is performed.","Exact duplicates are candidates only; canonicality must be proven before retirement.","Historical/derived/test classifications are heuristics, not authority.","Any retirement requires explicit authorization and archive/recovery proof."]};
fs.writeFileSync("architectural-garbage-inventory.json",JSON.stringify(artifact,null,2)+"\n");console.log(JSON.stringify(artifact,null,2));