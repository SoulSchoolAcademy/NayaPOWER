#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
const root=process.cwd();
const read=p=>fs.readFileSync(path.join(root,p),"utf8");
const must=(c,m)=>{if(!c)throw new Error(m)};
const hub=read("NAYANET/HUB/index.html");
const router=read("NAYANET/HUB/src/app/HubRouter.tsx");
const today=read("NAYANET/HUB/src/app/IntelligenceTodaySurface.tsx");
const note=read("NAYANET/HUB/src/app/SmartNoteSurface.tsx");
const feed=read("NAYANET/HUB/src/intelligence/SmartFeedBoard.tsx");
const pis=read("NAYANET/HUB/src/data/pis.ts");
const appFiles=[];
function walk(dir){for(const e of fs.readdirSync(dir,{withFileTypes:true})){const p=path.join(dir,e.name);if(e.isDirectory())walk(p);else if(e.name.endsWith(".ts")||e.name.endsWith(".tsx"))appFiles.push(p)}}
walk(path.join(root,"NAYANET","HUB","src","app"));
const appText=appFiles.map(p=>fs.readFileSync(p,"utf8")).join("\n");
const forbiddenWrites=(appText.match(/\.(insert|update|upsert|delete)\s*\(/g)||[]).length;
const artifact={schema:"NAYANET_HUB_PROJECTION_INVARIANT_V1",status:"VERIFIED",scope:"SOURCE_ARCHITECTURE_BOUNDED",checks:{canonical_hub:hub.length>0,router_uses_pis:router.includes("loadPrimaryIntelligence"),today_uses_pis:today.includes("loadPrimaryIntelligence"),smart_note_uses_runtime_receiver:note.includes("NayaAssistantRuntime")&&note.includes("captureSmartNote"),feed_is_projection:feed.includes("SmartFeedBoard")&&feed.includes("intelligent_block"),pis_reads_canonical_index:pis.includes("nayanet_intelligence_index"),hub_app_direct_write_count:forbiddenWrites,hub_app_direct_write_free:forbiddenWrites===0,source_of_truth_note:hub.includes("NayaNET")}};
for(const [k,v] of Object.entries(artifact.checks)){if(k!=="hub_app_direct_write_count")must(v,"PROJECTION_INVARIANT_FAILED:"+k)}
fs.writeFileSync("hub-projection-invariant.json",JSON.stringify(artifact,null,2)+"\n");
console.log(JSON.stringify(artifact,null,2));