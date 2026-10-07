/* forms/radio-check — Smart Block interaction
 * Visuals are pure CSS over native inputs. This file only adds
 * a JS-ready hook and keeps rows keyboard-discoverable.
 * Scoped root: .rc-group
 */
(function(){
  "use strict";
  document.querySelectorAll(".rc-group").forEach(function(group){
    group.dataset.rcReady = "true";
  });
})();
