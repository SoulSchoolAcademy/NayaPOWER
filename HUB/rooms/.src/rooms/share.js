function share(){
  /* Canonical 10 doors — PROJECT-INTELLIGENCE.md Phase 4. Door Law: every door is its
     own themed, elevated object — what it is, who it's for, live status, and the
     connect action with a real causal path. Connection ≠ permission to act. */
  var DOORS = [
    { id:'mcp', name:'MCP', who:'AI agents → NayaPOWER tools & context', status:'AVAILABLE', color:'#9d75ff',
      desc:'The priority door. Agents call NayaPOWER tools and read context through the Model Context Protocol.',
      can:'Invoke the tools you expose, within the scopes you grant.',
      cannot:'Act outside granted scopes. Persist anything. Reach private rooms. Learn from you without receipt.' },
    { id:'rest', name:'REST / OpenAPI', who:'Apps & agents', status:'AVAILABLE', color:'#55b9ee',
      desc:'The programmatic door. Anything that speaks HTTP can read and write governed intelligence.',
      can:'Read and write through scoped API calls, every one receipted.',
      cannot:'Bypass the authority envelope. Escalate scopes silently.' },
    { id:'github', name:'GitHub App', who:'Coding & repository agents', status:'AVAILABLE', color:'#f1d75a',
      desc:'Works with the GitHub setup — the app we create. Repositories become governable work surfaces.',
      can:'Open PRs, file issues, run checks inside repos you connect.',
      cannot:'Merge, deploy, or touch production — those stay Shawn\u2019s word alone.' },
    { id:'webhooks', name:'Webhooks', who:'Systems → NayaPOWER events', status:'AVAILABLE', color:'#ff9a5a',
      desc:'Events in, intelligence out. External systems knock; every knock is registered and receipted.',
      can:'Deliver event payloads to registered endpoints.',
      cannot:'Read anything back. Impersonate a human or a Naya.' },
    { id:'sdk', name:'SDK', who:'Developers embed NayaPOWER', status:'AVAILABLE', color:'#55e39a',
      desc:'Build NayaPOWER into other software with the governed client libraries.',
      can:'Use the same doors and receipts as every other client.',
      cannot:'Skip the ledger. Any call without a receipt is a bug, not a feature.' },
    { id:'a2a', name:'A2A', who:'Agent ↔ agent collaboration', status:'COMING SOON', color:'#d86cff',
      desc:'Nayas and other agents coordinate through governed agent-to-agent channels.',
      can:'Exchange governed work packets with mutual receipts.',
      cannot:'Inherit each other\u2019s authority. Authority is never transferable.' },
    { id:'browser', name:'Browser / Web Hub', who:'Humans — this Hub is a door', status:'ACTIVE', color:'#6675ff',
      desc:'You are already inside. The Hub itself is the human door into NayaPOWER.',
      can:'Everything this app can do, as you.',
      cannot:'Anything outside your authority envelope.' },
    { id:'email', name:'Email & Messaging', who:'Human & network communication', status:'COMING SOON', color:'#55b9ee',
      desc:'Reach the Hub from the channels you already live in — mail and messaging adapters.',
      can:'Send and receive governed messages with provenance.',
      cannot:'Act on your behalf from an unverified sender. Ever.' },
    { id:'enterprise', name:'Enterprise Identity', who:'Organization-level authorization', status:'LATER', color:'#aaa4b1',
      desc:'Whole organizations connect with their own authority trees. Later — the home door comes first.',
      can:'(Defined when the door opens.)',
      cannot:'Exist yet.' },
    { id:'tunnel', name:'Private MCP Tunnel', who:'Private / on-prem agents', status:'COMING SOON', color:'#b8ee57',
      desc:'For minds that live on private iron — a specialized, encrypted tunnel into NayaPOWER.',
      can:'The MCP surface, over a private channel you control.',
      cannot:'Phone home. The tunnel carries work, not telemetry.' }
  ];
  var reqs = NayaHub.d.requests;
  var pending = NayaHub.d.prefs.pendingDoor || null;
  var cards = DOORS.map(function(dr){
    var mine = reqs.filter(function(r){ return r.door === dr.id; }).length;
    var st = dr.status === 'ACTIVE' ? 'READY' : (dr.status === 'LATER' ? 'BLOCKED' : 'NOT_VERIFIED');
    var act;
    if (dr.status === 'ACTIVE') act = '<span class="hub-chip on">CONNECTED</span>';
    else if (dr.status === 'LATER') act = '<span class="hub-chip">NOT YET OPEN</span>';
    else act = '<button data-hub-action="door-scope" data-v="'+dr.id+'">REQUEST ACCESS'+(mine ? ' ('+mine+')' : '')+'</button>';
    var html = '<article class="ws-card" style="--accent:'+dr.color+'"><h3>'+dr.name+'</h3>'
      + '<p><b>'+dr.who+'</b></p>'
      + '<span class="hub-state" data-s="'+st+'">'+dr.status+'</span>'
      + '<p class="hub-dim">'+dr.desc+'</p>'
      + '<div class="ws-actions">'+act+'</div></article>';
    if (pending === dr.id){
      html += '<div class="hub-scope" id="hubDoorScope"><h4>Before you open the '+NayaHub.esc(dr.name)+' door</h4>'
        + '<p class="can">CAN — '+dr.can+'</p>'
        + '<p class="cannot">CANNOT — '+dr.cannot+'</p>'
        + '<p class="hub-dim">Connection never implies permission to act. This request is recorded as a ledger receipt.</p>'
        + '<div class="ws-actions"><button data-hub-action="door-confirm">CONFIRM REQUEST</button>'
        + '<button data-hub-action="door-cancel">CANCEL</button></div></div>';
    }
    return html;
  }).join('');
  return head(S.share)
    + '<div class="ws-grid">'+cards+'</div>'
    + '<p class="hub-note">One brain. Many doors. Connection ≠ permission to act — that distinction is architectural law.</p>';
}
