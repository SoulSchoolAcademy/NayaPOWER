/* forms/dropdown — Smart Block interaction
 * Toggle menu, select option, keyboard nav, type-ahead, Escape/click-outside.
 * Scoped root: .dd-root  (trigger .dd-trigger, menu .dd-menu)
 */
(function(){
  "use strict";

  function init(root){
    var trigger = root.querySelector(".dd-trigger");
    var label   = root.querySelector(".dd-label");
    var menu    = root.querySelector(".dd-menu");
    var options = Array.prototype.slice.call(menu.querySelectorAll(".dd-option"));
    var open = false, hoverIdx = -1, typeBuf = "", typeTimer = null;

    function setOpen(v){
      open = v;
      menu.classList.toggle("dd-show", v);
      trigger.classList.toggle("dd-open", v);
      trigger.setAttribute("aria-expanded", v ? "true" : "false");
      if (v){ setHover(selectedIdx()); }
      else { setHover(-1); }
    }

    function selectedIdx(){
      return options.findIndex(function(o){ return o.classList.contains("dd-selected"); });
    }

    function setHover(i){
      hoverIdx = i;
      options.forEach(function(o, k){ o.classList.toggle("dd-hover", k === i); });
    }

    function choose(o){
      options.forEach(function(x){ x.classList.remove("dd-selected"); });
      o.classList.add("dd-selected");
      label.textContent = o.querySelector(".dd-text").textContent;
      trigger.setAttribute("aria-label", "Selected: " + label.textContent);
      setOpen(false); trigger.focus();
    }

    trigger.addEventListener("click", function(){ setOpen(!open); });
    options.forEach(function(o){ o.addEventListener("click", function(){ choose(o); }); });

    document.addEventListener("click", function(e){
      if (open && !root.contains(e.target)) setOpen(false);
    });

    /* ---------- keyboard ---------- */
    root.addEventListener("keydown", function(e){
      if (!open && (e.key === "ArrowDown" || e.key === "ArrowUp" || e.key === "Enter" || e.key === " ")){
        e.preventDefault(); setOpen(true); return;
      }
      if (!open) return;
      if (e.key === "Escape"){ e.preventDefault(); setOpen(false); trigger.focus(); return; }
      if (e.key === "ArrowDown"){ e.preventDefault(); setHover((hoverIdx + 1) % options.length); return; }
      if (e.key === "ArrowUp"){ e.preventDefault(); setHover((hoverIdx - 1 + options.length) % options.length); return; }
      if (e.key === "Enter" && hoverIdx >= 0){ e.preventDefault(); choose(options[hoverIdx]); return; }
      /* type-ahead */
      if (e.key.length === 1 && !e.metaKey && !e.ctrlKey){
        typeBuf += e.key.toLowerCase();
        clearTimeout(typeTimer);
        typeTimer = setTimeout(function(){ typeBuf = ""; }, 600);
        var hit = options.findIndex(function(o){
          return o.querySelector(".dd-text").textContent.toLowerCase().indexOf(typeBuf) === 0;
        });
        if (hit >= 0) setHover(hit);
      }
    });
  }

  document.querySelectorAll(".dd-root").forEach(init);
})();
