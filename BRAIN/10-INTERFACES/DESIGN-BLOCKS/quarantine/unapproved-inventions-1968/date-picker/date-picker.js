/* forms/date-picker — Smart Block interaction
 * Open/close popup, month nav, select, keyboard support.
 * Scoped root: .dp-root  (trigger .dp-trigger, popup .dp-popup)
 */
(function(){
  "use strict";

  var MONTHS = ["January","February","March","April","May","June","July",
                "August","September","October","November","December"];
  var WDAYS  = ["Mo","Tu","We","Th","Fr","Sa","Su"];

  function pad(n){ return (n < 10 ? "0" : "") + n; }
  function fmt(d){ return MONTHS[d.getMonth()] + " " + d.getDate() + ", " + d.getFullYear(); }

  function init(root){
    var trigger = root.querySelector(".dp-trigger");
    var popup   = root.querySelector(".dp-popup");
    var label   = root.querySelector(".dp-label");
    var monthEl = root.querySelector(".dp-month");
    var grid    = root.querySelector(".dp-grid");
    var prevBtn = root.querySelector("[data-dp-prev]");
    var nextBtn = root.querySelector("[data-dp-next]");

    var view   = new Date();                 // month being shown
    view.setDate(1);
    var selected = null;                     // Date or null
    var focusDate = new Date();              // keyboard cursor
    var open = false;

    /* ---------- render ---------- */
    function render(){
      monthEl.textContent = MONTHS[view.getMonth()] + " " + view.getFullYear();
      grid.innerHTML = "";
      var y = view.getFullYear(), m = view.getMonth();
      var first = (new Date(y, m, 1).getDay() + 6) % 7; // Monday-first
      var start = new Date(y, m, 1 - first);
      var today = new Date(); today.setHours(0,0,0,0);
      for (var i = 0; i < 42; i++){
        (function(){
          var d = new Date(start.getFullYear(), start.getMonth(), start.getDate() + i);
          var b = document.createElement("button");
          b.type = "button"; b.className = "dp-day";
          b.textContent = d.getDate();
          var dc = new Date(d); dc.setHours(0,0,0,0);
          if (dc.getTime() === today.getTime()) b.classList.add("dp-today");
          if (d.getMonth() !== m) b.classList.add("dp-dim");
          if (selected && dc.getTime() === selected.getTime()) b.classList.add("dp-selected");
          b.dataset.dpDate = d.getFullYear() + "-" + pad(d.getMonth()+1) + "-" + pad(d.getDate());
          b.setAttribute("aria-label", fmt(d));
          b.addEventListener("click", function(){
            select(new Date(d));
          });
          grid.appendChild(b);
        })();
      }
    }

    /* ---------- open / close ---------- */
    function setOpen(v){
      open = v;
      popup.classList.toggle("dp-show", v);
      trigger.classList.toggle("dp-open", v);
      trigger.setAttribute("aria-expanded", v ? "true" : "false");
      if (v){
        view = selected ? new Date(selected) : new Date();
        view.setDate(1);
        focusDate = selected ? new Date(selected) : new Date();
        render();
      }
    }
    trigger.addEventListener("click", function(){ setOpen(!open); });
    document.addEventListener("click", function(e){
      if (open && !root.contains(e.target)) setOpen(false);
    });
    document.addEventListener("keydown", function(e){
      if (e.key === "Escape" && open){ setOpen(false); trigger.focus(); }
    });

    /* ---------- select ---------- */
    function select(d){
      selected = new Date(d); selected.setHours(0,0,0,0);
      label.textContent = fmt(selected);
      label.classList.remove("dp-empty");
      setOpen(false);
      trigger.focus();
    }

    /* ---------- month nav ---------- */
    prevBtn.addEventListener("click", function(){ view.setMonth(view.getMonth()-1); render(); });
    nextBtn.addEventListener("click", function(){ view.setMonth(view.getMonth()+1); render(); });

    /* ---------- keyboard: arrows move, Enter selects ---------- */
    popup.addEventListener("keydown", function(e){
      var move = 0;
      if (e.key === "ArrowLeft")  move = -1;
      else if (e.key === "ArrowRight") move = 1;
      else if (e.key === "ArrowUp")    move = -7;
      else if (e.key === "ArrowDown")  move = 7;
      else if (e.key === "Enter" && document.activeElement.classList.contains("dp-day")){
        document.activeElement.click(); return;
      } else return;
      e.preventDefault();
      focusDate.setDate(focusDate.getDate() + move);
      if (focusDate.getMonth() !== view.getMonth() || focusDate.getFullYear() !== view.getFullYear()){
        view = new Date(focusDate); view.setDate(1);
        render();
      }
      var key = focusDate.getFullYear() + "-" + pad(focusDate.getMonth()+1) + "-" + pad(focusDate.getDate());
      var cell = grid.querySelector('[data-dp-date="' + key + '"]');
      if (cell) cell.focus();
    });

    render();
  }

  document.querySelectorAll(".dp-root").forEach(init);
})();
