/* forms/range-slider — Smart Block interaction
 * Pointer drag, keyboard arrows, fill + bubble + value sync.
 * Scoped root: .rs-root  (data-min / data-max / data-value / data-step)
 */
(function(){
  "use strict";

  function init(root){
    var track  = root.querySelector(".rs-track");
    var fill   = root.querySelector(".rs-fill");
    var thumb  = root.querySelector(".rs-thumb");
    var bubble = root.querySelector(".rs-bubble");
    var input  = root.querySelector(".rs-input");
    var out    = root.querySelector(".rs-value");

    var min  = parseFloat(root.dataset.min  || "0");
    var max  = parseFloat(root.dataset.max  || "100");
    var step = parseFloat(root.dataset.step || "1");
    var val  = parseFloat(root.dataset.value != null ? root.dataset.value : ((min + max) / 2));
    var suffix = root.dataset.suffix || "";

    function clamp(v){ return Math.min(max, Math.max(min, v)); }
    function snap(v){
      var n = Math.round((v - min) / step) * step + min;
      return Math.round(n * 1e6) / 1e6;
    }

    function render(){
      var pct = ((val - min) / (max - min)) * 100;
      fill.style.width  = pct + "%";
      thumb.style.left  = pct + "%";
      bubble.style.left = pct + "%";
      var text = (Number.isInteger(val) ? String(val) : val.toFixed(1)) + suffix;
      bubble.textContent = text;
      if (out) out.textContent = text;
      if (input){ input.value = val; input.setAttribute("aria-valuenow", val); }
    }

    function setVal(v){
      var nv = snap(clamp(v));
      if (nv !== val){ val = nv; render(); root.dispatchEvent(new CustomEvent("rs-change", { detail:{ value: val } })); }
    }

    /* ---------- pointer drag ---------- */
    function valFromEvent(e){
      var r = track.getBoundingClientRect();
      var p = (e.clientX - r.left) / r.width;
      return min + p * (max - min);
    }
    function onMove(e){ setVal(valFromEvent(e)); }
    function onUp(){
      thumb.classList.remove("rs-drag");
      window.removeEventListener("pointermove", onMove);
      window.removeEventListener("pointerup", onUp);
      window.removeEventListener("pointercancel", onUp);
    }
    track.addEventListener("pointerdown", function(e){
      e.preventDefault();
      track.setPointerCapture && track.setPointerCapture(e.pointerId);
      thumb.classList.add("rs-drag");
      setVal(valFromEvent(e));
      window.addEventListener("pointermove", onMove);
      window.addEventListener("pointerup", onUp);
      window.addEventListener("pointercancel", onUp);
      thumb.focus();
    });

    /* ---------- keyboard ---------- */
    function keyTarget(){
      if (input){
        input.min = min; input.max = max; input.step = step;
        input.setAttribute("role", "slider");
        input.setAttribute("aria-valuemin", min);
        input.setAttribute("aria-valuemax", max);
        return input;
      }
      thumb.tabIndex = 0;
      thumb.setAttribute("role", "slider");
      return thumb;
    }
    var kt = keyTarget();
    kt.addEventListener("keydown", function(e){
      var d = 0;
      var big = (max - min) / 10;
      if (e.key === "ArrowRight" || e.key === "ArrowUp") d = step;
      else if (e.key === "ArrowLeft" || e.key === "ArrowDown") d = -step;
      else if (e.key === "PageUp") d = big;
      else if (e.key === "PageDown") d = -big;
      else if (e.key === "Home"){ setVal(min); e.preventDefault(); return; }
      else if (e.key === "End"){ setVal(max); e.preventDefault(); return; }
      else return;
      e.preventDefault(); setVal(val + d);
    });

    render();
  }

  document.querySelectorAll(".rs-root").forEach(init);
})();
