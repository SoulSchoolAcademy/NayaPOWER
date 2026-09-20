(()=>{'use strict';
// Source-level release self-check. This does not claim deployment or human visual verification.
const expectedWorlds=9, expectedCasts=18;
window.NayaNETReleaseCheck={
 run(){
  const worlds=document.querySelectorAll('#worldMap .world').length;
  const casts=document.querySelectorAll('#castGrid .cast').length;
  const audio=!!document.querySelector('#audio');
  const player=!!document.querySelector('#player');
  const entry=!!document.querySelector('#entryForm');
  const naya=!!document.querySelector('#nayaCore');
  const result={worlds,casts,audio,player,entry,naya,pass:worlds===expectedWorlds&&casts===expectedCasts&&audio&&player&&entry&&naya};
  console.info('[NayaNET 10/10 source check]',result); return result;
 }
};
})();
