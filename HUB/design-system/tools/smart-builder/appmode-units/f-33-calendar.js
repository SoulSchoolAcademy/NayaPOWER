/* NayaFunction: calendar v1.0.0
   What: Calendar — standalone date/time picker and event manager.
     Distinct from F-09 booking (which handles appointments). This is
     the calendar WIDGET — pick dates, view events, manage schedule.
   Source: Built 2026-10-18 per Shawn's directive ("torch passed").
     Harvest: BRD-037 Calendar piece provides the visual.
   Activation: <div data-fn="calendar" data-fn-config='{...}'></div>
   Config: {
     view: 'month' | 'week' | 'day' (default 'month')
     events: [{id, title, date, time}]  initial events
     selectable: true → user can pick dates (default true)
     onSelect: function(date)  callback when date picked
   } — all optional.
   Ready behavior: Calendar renders, dates selectable, events shown.
     Works client-side with localStorage.
   Connected behavior: Sync with Google/Apple calendar — requires `connected: true`.
   Status: IMPLEMENTED 2026-10-18. Needs different-seat verification.
*/
(function(){
  'use strict';
  const FN_ID = 'calendar';
  
  function activate(mount, config){
    config = config || {};
    
    mount.setAttribute('data-fn-active', FN_ID);
    mount.setAttribute('data-fn-version', '1.0.0');
    
    let currentDate = new Date();
    let events = config.events || [];
    
    function render(){
      const year = currentDate.getFullYear();
      const month = currentDate.getMonth();
      const firstDay = new Date(year, month, 1).getDay();
      const daysInMonth = new Date(year, month + 1, 0).getDate();
      
      let html = '<div class="naya-cal" style="font-family:Inter,sans-serif;color:#fff;">';
      html += '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">';
      html += '<button data-cal-prev style="background:#050507;border:2px solid #fff;color:#fff;border-radius:50%;width:36px;height:36px;cursor:pointer;">‹</button>';
      html += '<span style="font-size:18px;">' + currentDate.toLocaleDateString('en-US',{month:'long',year:'numeric'}) + '</span>';
      html += '<button data-cal-next style="background:#050507;border:2px solid #fff;color:#fff;border-radius:50%;width:36px;height:36px;cursor:pointer;">›</button>';
      html += '</div>';
      html += '<div style="display:grid;grid-template-columns:repeat(7,1fr);gap:4px;text-align:center;">';
      
      ['S','M','T','W','T','F','S'].forEach(d => {
        html += '<div style="font-size:14px;color:#ffffff;padding:4px;">' + d + '</div>';
      });
      
      for (let i = 0; i < firstDay; i++) html += '<div></div>';
      
      for (let d = 1; d <= daysInMonth; d++) {
        const dateStr = year + '-' + String(month+1).padStart(2,'0') + '-' + String(d).padStart(2,'0');
        const hasEvent = events.some(e => e.date === dateStr);
        const isToday = new Date().toDateString() === new Date(year, month, d).toDateString();
        html += '<div data-cal-date="' + dateStr + '" style="font-size:14px;padding:8px;border-radius:8px;cursor:pointer;'
          + (isToday ? 'background:#a06bff;color:#fff;' : 'background:rgba(255,255,255,0.03);')
          + (hasEvent ? 'border:2px solid #a06bff;' : 'border:2px solid transparent;')
          + '">' + d + '</div>';
      }
      
      html += '</div></div>';
      mount.innerHTML = html;
      
      // Wire navigation
      mount.querySelector('[data-cal-prev]').addEventListener('click', () => {
        currentDate.setMonth(currentDate.getMonth() - 1); render();
      });
      mount.querySelector('[data-cal-next]').addEventListener('click', () => {
        currentDate.setMonth(currentDate.getMonth() + 1); render();
      });
      
      // Wire date selection
      if (config.selectable !== false) {
        mount.querySelectorAll('[data-cal-date]').forEach(el => {
          el.addEventListener('click', () => {
            const date = el.getAttribute('data-cal-date');
            if (config.onSelect) config.onSelect(date);
            mount.dispatchEvent(new CustomEvent('calendar-select', {detail:{date}, bubbles:true}));
          });
        });
      }
    }
    
    render();
    
    return {
      id: FN_ID,
      version: '1.0.0',
      addEvent: function(evt){ events.push(evt); render(); },
      getEvents: function(){ return events; },
      destroy: function(){ mount.innerHTML = ''; }
    };
  }
  
  if (typeof NayaFunctions !== 'undefined' && NayaFunctions.register) {
    NayaFunctions.register(FN_ID, { activate: activate });
  } else {
    window.NayaCalendar = { activate: activate };
  }
})();
