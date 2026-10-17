/* CONNECT ADAPTER — canonical Smart Door registry → door view-models.
 *
 * Source of truth: BRAIN/10-INTERFACES/0002-SMART-DOOR-REGISTRY-V1.json
 * (contract: .../0001-SMART-DOOR-CONTRACT-V1.json).
 * The Hub is a projection surface; this adapter never invents doors.
 *
 *   const doors = ConnectAdapter.parse(registryJson);
 *   // -> [{id, name, provider, capabilities[], operations[], consequenceClass,
 *   //      authority, identityMethod, dataClasses[], health, status,
 *   //      statusKind: 'live'|'design', statusLabel}]
 */
(function(){
  'use strict';

  function liveKind(status){
    return status==='LIVE_BOUNDED' || status==='LIVE_BOUNDED_EXISTING_CAPABILITY';
  }

  function parse(input){
    const reg = (typeof input==='string') ? JSON.parse(input) : (input||{});
    const doors = Array.isArray(reg.doors) ? reg.doors : [];
    return doors.map(d=>({
      id: d.door_id||'UNKNOWN',
      name: d.name||d.door_id||'Unnamed door',
      provider: d.provider||'',
      capabilities: Array.isArray(d.capabilities)?d.capabilities.slice():[],
      operations: Array.isArray(d.operations)?d.operations.slice():[],
      consequenceClass: d.consequence_class||'',
      authority: d.required_authority||'',
      identityMethod: d.identity_method||'',
      dataClasses: Array.isArray(d.data_classes)?d.data_classes.slice():[],
      health: d.health||'',
      status: d.status||'',
      audit: d.audit||'',
      statusKind: liveKind(d.status) ? 'live' : 'design',
      statusLabel: liveKind(d.status) ? 'LIVE' : 'IN DESIGN'
    }));
  }

  window.ConnectAdapter = { parse: parse };
})();
