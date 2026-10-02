function share(){
  var DOORS = [
    { id:'hub', name:'NayaNET Hub', who:'You, here, now', status:'ACTIVE', color:'#55e39a',
      desc:'This app. Your cockpit — every room, every board, one intelligence. You are already inside.' },
    { id:'invite', name:'Human Invite', who:'People you trust', status:'AVAILABLE', color:'#55b9ee',
      desc:'Bring someone in with a governed invite. They see what you share — nothing more, nothing less.' },
    { id:'ai', name:'AI Door', who:'Other AI minds', status:'COMING SOON', color:'#9d75ff',
      desc:'Let another AI read and contribute through a governed door. Connection never implies permission to act.' },
    { id:'machine', name:'Machine Door', who:'Devices & systems', status:'COMING SOON', color:'#ff9a5a',
      desc:'Sensors, servers, pipelines — machines that report to the Hub through receipts, not silent writes.' },
    { id:'webhook', name:'Webhook Door', who:'Your other apps', status:'COMING SOON', color:'#f1d75a',
      desc:'Events in, intelligence out. Every door registered, receipted, and revocable.' }
  ];
  var reqs = NayaHub.d.requests;
  var cards = DOORS.map(function(dr){
    var mine = reqs.filter(function(r){ return r.door === dr.id; }).length;
    var act = dr.status === 'ACTIVE'
      ? '<span class="hub-chip on">CONNECTED</span>'
      : '<button data-hub-action="req-access" data-v="'+dr.id+'">REQUEST ACCESS'+(mine ? ' ('+mine+')' : '')+'</button>';
    return '<article class="ws-card" style="--accent:'+dr.color+'"><h3>'+dr.name+'</h3>'
      + '<p><b>'+dr.who+'</b> · <span class="hub-chip">'+dr.status+'</span></p>'
      + '<p class="hub-dim">'+dr.desc+'</p>'
      + '<div class="ws-actions">'+act+'</div></article>';
  }).join('');
  return head(S.share)
    + '<div class="ws-grid">'+cards+'</div>'
    + '<p class="hub-note">One brain. Many doors. Every request is recorded as a ledger receipt — connection never implies permission to act.</p>';
}
