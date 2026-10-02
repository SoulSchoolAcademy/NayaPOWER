(function(){
  'use strict';

  const JUNK = [/^pasted text$/i, /^\d{2}\s+naya\b/i, /^[—-]{3,}$/, /^\*{3,}$/];

  function clean(s){
    return (s||'')
      .replace(/\*\*([^*]+)\*\*/g,'$1')
      .replace(/`([^`]+)`/g,'$1')
      .replace(/\\\s*$/,'')
      .replace(/\s*\bPasted text\b\.?/gi,'')
      .replace(/\s*\b\d{2}\s+NAYA\b.*$/gi,'')
      .replace(/\s+/g,' ')
      .trim();
  }
  function isJunk(line){
    const t=clean(line);
    if(!t) return true;
    return JUNK.some(rx=>rx.test(t));
  }
  function firstSentence(s){
    const m=s.match(/^(.+?[.!?])(\s|$)/);
    return m?m[1]:s;
  }
  function truncate(s,n){
    if(s.length<=n) return s;
    const cut=s.slice(0,n);
    const end=Math.max(cut.lastIndexOf('. '),cut.lastIndexOf('! '),cut.lastIndexOf('? '));
    return (end>40?cut.slice(0,end+1):cut).trim();
  }

  function parseMeta(lines){
    const meta={};
    const get=(key)=>{
      const rx=new RegExp('^\\*\\*'+key+':\\*\\*\\s*(.*)$');
      for(const l of lines){ const m=l.match(rx); if(m) return clean(m[1]); }
      const rx2=new RegExp('^'+key+':\\s*(.*)$');
      for(const l of lines){ const m=l.match(rx2); if(m) return clean(m[1]); }
      return '';
    };
    meta.ib=get('Intelligent Block ID');
    meta.id=get('Report ID');
    meta.period=(get('Period type')||'DAILY').toLowerCase();
    meta.date=get('Period date');
    meta.scope=get('Scope');
    meta.status=get('Status');
    return meta;
  }

  function parseSections(lines){
    const sections=[]; let cur=null;
    const push=()=>{ if(cur && (cur.blocks.length)) sections.push(cur); cur=null; };
    for(const raw of lines){
      const h=raw.match(/^(#{1,3})\s+(?:(\d+)\.\s+)?(.+)$/);
      if(h && (h[2] || h[1].length>1)){
        const lb=clean(h[3]);
        if(/canonical intelligence report record/i.test(lb)) continue;
        push(); cur={n:+(h[2]||0), label:lb.toUpperCase(), blocks:[]}; continue;
      }
      if(!cur) continue;
      if(clean(raw) && isJunk(raw)) continue;
      cur.blocks.push(raw);
    }
    push();
    return sections;
  }

  function distillSection(sec){
    const label=sec.label;
    const kind = /SCORECARD/.test(label) ? 'scorecard'
               : /PROMPT/.test(label) ? 'prompt'
               : 'standard';
    const out={label, kind, nutshell:'', points:[], prompt:'', scores:[], chain:[]};

    /* Block grouping: a line opening with **, >, or "N." starts a new block;
       plain lines continue the current block. Junk is dropped first. */
    const blocks=[]; let cur=null;
    const flush=()=>{ if(cur){ const t=clean(cur.lines.join(' ')); if(t && !isJunk(t)) blocks.push({text:t, marker:cur.marker}); } cur=null; };
    for(const l of sec.blocks){
      if(!clean(l)){ flush(); continue; }
      const m = /^\s*\d+\.\s/.test(l) ? 'num' : /^\s*-\s+/.test(l) ? 'bul' : /^\s*>/.test(l) ? 'quote' : /^\s*\*\*/.test(l) ? 'bold' : null;
      if(m){ flush(); cur={marker:m, lines:[l]}; }
      else { if(!cur) cur={marker:'para', lines:[]}; cur.lines.push(l); }
      if(/\\\s*$/.test(l)) flush(); /* markdown hard-break: one item per line */
    }
    flush();

    const stripNum=t=>t.replace(/^\d+\.\s*/,'');
    const stripQuote=t=>t.replace(/^>\s?/,'');
    const sentences=t=>{
      const prot=t.replace(/(\d)\.(\d)/g,'$1<DOT>$2');
      const parts=prot.match(/[^.!?]+[.!?]+/g)||[prot];
      return parts.map(s=>s.replace(/<DOT>/g,'.').trim()).filter(Boolean);
    };

    /* Prompt kind: blockquote becomes the copyable prompt */
    if(kind==='prompt'){
      out.prompt=blocks.filter(b=>b.marker==='quote')
        .map(b=>stripQuote(b.text)).join('\n').trim()
        || blocks.map(b=>b.text).join('\n\n');
    }

    /* Nutshell: first substantial non-numbered block (not for prompts) */
    let nutIdx=-1;
    if(kind!=='prompt'){
      const elig=[];
      blocks.forEach((b,bi)=>{ if(b.marker!=='num' && b.text.length>30 && (b.text.match(/→/g)||[]).length<2 && elig.length<4) elig.push(bi); });
      let cands=elig.filter(bi=>blocks[bi].marker!=='quote');
      if(!cands.length) cands=elig;
      if(cands.length){
        nutIdx=cands[0];
        const first=blocks[nutIdx].text;
        const isFrag=first.length<50 || /:\s*$/.test(first);
        if(isFrag){
          /* a quote right after a thin lead-in usually carries the substance */
          const qi=elig.find(bi=>blocks[bi].marker==='quote' && blocks[bi].text.length>100);
          if(qi!==undefined) nutIdx=qi;
          else if(first.length<50){
            let best=nutIdx;
            cands.forEach(bi=>{ if(blocks[bi].text.length>blocks[best].text.length) best=bi; });
            nutIdx=best;
          }
          /* otherwise keep the frame (e.g. "…all of these are true:") */
        }
        out.nutshell=truncate(blocks[nutIdx].text.replace(/^>\s?/,'').replace(/^-\s*/,'').replace(/^\d+\.\s*/,'').trim(),240);
      }
    }

    /* the → chain: any section whose content carries one gets the pill strip */
    const skipIdx=new Set();
    if(kind!=='prompt'){
      blocks.forEach((b,bi)=>{
        if((b.text.match(/→/g)||[]).length>=2 && !out.chain.length){
          const links=b.text.split('→').map(s=>s.trim()).filter(Boolean);
          if(links.length>=2 && links.every(c=>c.length<=64)){
            out.chain=links;
            skipIdx.add(bi);
          }
        }
      });
    }
    /* Scorecard: X/10 ratings */
    if(kind==='scorecard'){
      const seen=new Set();
      blocks.forEach((b,bi)=>{
        sentences(b.text).forEach(sent=>{
          const rx=/(\d+(?:\.\d+)?(?:\s*[–—-]\s*\d+(?:\.\d+)?)?)\s*\/10/g;
          let m;
          while((m=rx.exec(sent))){
            if(m[1]==='10'||seen.has(m[1])) continue;
            seen.add(m[1]); skipIdx.add(bi);
            let seg=(sent.split(/[,;]/).find(sg=>sg.includes(m[0]))||sent);
            seg=clean(seg).replace(m[0],'')
              .replace(/.*?\b(rate|rating|about|while|closer to|is|the)\b\s+/i,'')
              .replace(/^\s*the\s+/i,'')
              .replace(/(\s*\b(about|closer to|is)\b\s*\.?)+$/i,'').trim();
            out.scores.push({label:seg||'Score', value:m[1]+'/10'});
          }
        });
      });
    }

    /* Points */
    if(kind!=='prompt'){
      blocks.forEach((b,bi)=>{
        if(bi===nutIdx||skipIdx.has(bi)) return;
        let t=b.text;
        if(b.marker==='num') t=stripNum(t);
        if(b.marker==='bul') t=t.replace(/^-\s*/,'');
        if(b.marker==='quote') t=stripQuote(t);
        if(b.marker==='bold'){
          const kv=t.match(/^([^:–—]{2,60}?)\s*[:–—]\s*(.+)$/);
          if(kv && kv[2].length<90){ out.points.push(kv[1].trim()+': '+kv[2].trim()); return; }
        }
        if(t.length<=210){ if(t.length>25) out.points.push(t); return; }
        const ss=sentences(t);
        out.points.push(ss[0].trim()+' — '+truncate(ss.slice(1).join(' ').trim(),130));
      });
      /* Thin sections: split longest blocks into sentences (no invention, finer grain) */
      if(out.points.length<3){
        const extra=[];
        blocks.forEach((b,bi)=>{
          if(skipIdx.has(bi)||b.marker==='num') return;
          sentences(b.text).forEach(s=>{ s=s.trim(); if(s.length>=40 && !out.nutshell.includes(s)) extra.push(s); });
        });
        const have=new Set(out.points);
        for(const s of extra){ if(out.points.length>=4) break; if(!have.has(s)){ out.points.push(s); have.add(s); } }
      }
      out.points=out.points.slice(0,10);
    }
    return out;
  }

  function parseReportMarkdown(md){
    const lines=md.split('\n');
    const meta=parseMeta(lines);

    // Title: first "# " that is not the record header and not numbered
    let title='', dateLabel='', subtitle='';
    for(const l of lines){
      const m=l.match(/^#\s+(?!\d+\.)(.+)$/);
      if(m && !/canonical intelligence report record/i.test(m[1])){ title=clean(m[1]); break; }
    }
    const dm=title.match(/—\s*([A-Za-z]+\s+\d{1,2},\s+\d{4})\s*(?:—\s*(.+))?$/);
    if(dm){ dateLabel=dm[1].trim(); subtitle=(dm[2]||'').trim(); title=clean(title.replace(/—\s*.+$/,'')).trim(); }

    // Big picture: paragraphs between title and first section
    let bi=lines.findIndex(l=>/^#\s+(?!\d+\.)/.test(l) && !/canonical/i.test(l));
    let big='';
    if(bi>=0){
      for(let k=bi+1;k<lines.length;k++){
        if(/^#\s+\d+\./.test(lines[k])) break;
        const t=clean(lines[k]);
        if(t && !isJunk(t)){ big=t.replace(/^Shawn,\s*the big picture is:\s*/i,''); break; }
      }
    }

    const sections=parseSections(lines).map(distillSection);
    const idm=String(meta.id||'').match(/(\d{4})-(\d{2})-(\d{2})/);
    const dateKey=idm?idm[0]:String(meta.date||'').slice(0,10);
    return {
      id:meta.id||'UNKNOWN', ib:meta.ib||'', period:meta.period||'daily',
      date:dateKey||meta.date||'', dateKey:dateKey, dateLabel:dateLabel||meta.date,
      scope:meta.scope||'', status:(meta.status||'CANONICAL').replace(/\s+DAILY REPORT.*$/i,'').trim()||'CANONICAL',
      title:title||'Intelligence Briefing', subtitle:subtitle, bigPicture:big, sections
    };
  }

  window.ReportsAdapter={parse:parseReportMarkdown, clean};})();
