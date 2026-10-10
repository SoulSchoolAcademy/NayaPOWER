/* NayaNET SmartTabs Teaching Kit v10 (candidate, demonstration-only integration).
   Compatible public operations with the user-supplied SmartTabs v9 API:
   mount(selector, options) => {el, list, set, add, update, remove, destroy}
   + openAdd() and reset() convenience methods. Browser-only local state; not a server sync.
   Safety: user text via textContent; route validated to relative path/hash; native buttons/dialog. */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.SmartTabs = factory();
})(typeof window !== 'undefined' ? window : this, function () {
  'use strict';
  const DEFAULT = [
    {id:'today',label:'Today',route:'#today',heart:true,star:false},
    {id:'spaces',label:'Smart Spaces',route:'#spaces',heart:false,star:false},
    {id:'reports',label:'Reports',route:'#reports',heart:false,star:true},
    {id:'library',label:'Library',route:'#library',heart:false,star:false},
    {id:'connections',label:'Connections',route:'#connections',heart:false,star:false}
  ];
  const HUES = ['#9d75ff','#55b9ee','#35e39b','#ed42c4','#ff8c42'];
  const svg = {
    dots: '<svg viewBox="0 0 24 24" aria-hidden="true" fill="currentColor"><circle cx="5" cy="12" r="1.8"/><circle cx="12" cy="12" r="1.8"/><circle cx="19" cy="12" r="1.8"/></svg>',
    plus:'<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round"><path d="M12 4v16M4 12h16"/></svg>',
    heart:'<svg viewBox="0 0 24 24" aria-hidden="true" fill="currentColor"><path d="M20.8 7.5a5 5 0 0 0-8.8-2 5 5 0 0 0-8.8 2C1.4 13 6.3 17 12 21c5.7-4 10.6-8 8.8-13.5Z"/></svg>',
    star:'<svg viewBox="0 0 24 24" aria-hidden="true" fill="currentColor"><path d="m12 2.5 2.9 6 6.6 1-4.8 4.7 1.1 6.7-5.8-3.1-5.8 3.1 1.1-6.7-4.8-4.7 6.6-1Z"/></svg>'
  };
  function element(tag, className, text) {
    const e = document.createElement(tag);
    if(className) e.className = className;
    if(text !== undefined) e.textContent = text;
    return e;
  }
  function normalize(item, i) {
    const label=String(item && item.label || '').trim().slice(0,40) || `Shortcut ${i+1}`;
    const raw=String(item && item.route || '').trim().slice(0,250);
    const route=(raw.startsWith('#') || (raw.startsWith('/') && !raw.startsWith('//'))) ? raw : ('/search?q='+encodeURIComponent(label));
    return {id:String(item && item.id || ('shortcut-'+i)).slice(0,80),label,route,heart:!!(item&&item.heart),star:!!(item&&item.star)&&!(item&&item.heart)};
  }
  function mount(target, options) {
    const root=typeof target==='string'?document.querySelector(target):target;
    if(!root) throw Error('SmartTabs mount target not found');
    const opt=Object.assign({storageKey:'nayanet_smarttabs_v10_demo',initial:DEFAULT,routeMap:{},onNavigate:null},options||{});
    let state=opt.initial.map(normalize),storageAvailable=true;
    try {let prior=JSON.parse(localStorage.getItem(opt.storageKey));if(Array.isArray(prior)) state=prior.slice(0,30).map(normalize);}catch(e){storageAvailable=false;}
    function routeFrom(label){const known=opt.routeMap[String(label).trim().toLowerCase()];return known || ('/search?q='+encodeURIComponent(label));}
    let previousFocus=null,menuAnchor=null,currentId=null,createMode=false;
    root.replaceChildren();
    const nav=element('nav','st-ribbon');nav.setAttribute('aria-label','Your Smart Tabs shortcuts');root.appendChild(nav);
    const row=element('div','st-ribbon__scroll');nav.appendChild(row);
    const menu=element('div','st-menu');menu.setAttribute('role','menu');menu.setAttribute('aria-label','Shortcut actions');menu.hidden=true;
    const acts=[['edit','Edit shortcut'],['heart','Purple Heart'],['star','Gold Star'],['remove','Remove shortcut']];
    acts.forEach(([id,label])=>{const b=element('button','st-menu__item',label);b.type='button';b.dataset.act=id;b.setAttribute('role','menuitem');menu.appendChild(b);});
    document.body.appendChild(menu);
    const dialog=element('dialog','st-dialog');
    const heading=element('h2','','Add a Smart Tab');heading.id='st-dialog-title';dialog.setAttribute('aria-labelledby',heading.id);
    const form=element('form','st-form');form.noValidate=true;
    const info=element('p','st-form__intro','Choose a name and destination. Your shortcuts stay in this browser.');
    const labelL=element('label','st-form__label','Name');const labelInput=element('input','st-form__input');labelInput.name='label';labelInput.required=true;labelInput.maxLength=40;labelInput.placeholder='e.g. My Reports';labelL.appendChild(labelInput);
    const routeL=element('label','st-form__label','Destination');const routeInput=element('input','st-form__input');routeInput.name='route';routeInput.placeholder='#reports or /reports';routeL.appendChild(routeInput);
    const toggles=element('div','st-form__toggles');
    const heartL=element('label','st-form__toggle');const heartInput=element('input');heartInput.type='checkbox';heartInput.name='heart';heartL.append(heartInput,document.createTextNode(' Purple Heart'));
    const starL=element('label','st-form__toggle');const starInput=element('input');starInput.type='checkbox';starInput.name='star';starL.append(starInput,document.createTextNode(' Gold Star'));
    toggles.append(heartL,starL);
    heartInput.addEventListener('change',()=>{if(heartInput.checked)starInput.checked=false;});starInput.addEventListener('change',()=>{if(starInput.checked)heartInput.checked=false;});
    const formButtons=element('div','st-form__buttons');const cancel=element('button','st-button st-button--secondary','Cancel');cancel.type='button';
    const save=element('button','st-button st-button--primary','Save shortcut');save.type='submit';formButtons.append(cancel,save);
    form.append(info,labelL,routeL,toggles,formButtons);dialog.append(heading,form);document.body.appendChild(dialog);
    function emit() {let data=list();nav.dispatchEvent(new CustomEvent('change',{detail:data,bubbles:true}));if(typeof opt.onChange==='function')opt.onChange(data,storageAvailable);}
    function persist(){try{localStorage.setItem(opt.storageKey,JSON.stringify(state));storageAvailable=true;}catch(e){storageAvailable=false;} emit();}
    function list(){return state.map(x=>({...x}));}
    function rank(x){return x.heart?2:(x.star?1:0);}
    function rendered(){return state.map((s,i)=>({...s,index:i})).sort((a,b)=>rank(b)-rank(a)||a.index-b.index);}
    function safeChange(items){state=items.slice(0,30).map(normalize);persist();render();}
    function set(arr){if(!Array.isArray(arr))throw TypeError('SmartTabs.set expects an array');safeChange(arr);}
    function add(item){safeChange([...state,normalize({...item,id:item?.id||'st-'+Date.now().toString(36)},state.length)]);}
    function update(id,patch){safeChange(state.map(s=>s.id===id?normalize({...s,...patch,id},0):s));}
    function remove(id){safeChange(state.filter(s=>s.id!==id));}
    function closeMenu(){menu.hidden=true;menuAnchor=null;}
    function openMenu(btn,id){closeMenu();menuAnchor=btn;currentId=id;menu.hidden=false;const r=btn.getBoundingClientRect();let w=menu.offsetWidth||200;menu.style.left=Math.max(8,Math.min(innerWidth-w-8,r.right-w))+'px';menu.style.top=Math.min(innerHeight-menu.offsetHeight-8,r.bottom+8)+'px';menu.querySelector('button').focus();}
    function openEditor(mode,id){const returnTo=menuAnchor||document.activeElement;closeMenu();createMode=mode==='add';currentId=id||null;previousFocus=returnTo;
      const item=state.find(s=>s.id===id)||{label:'',route:'',heart:false,star:false};
      heading.textContent=createMode?'Add a Smart Tab':'Edit your Smart Tab';labelInput.value=createMode?'':item.label;routeInput.value=createMode?'':item.route;heartInput.checked=item.heart;starInput.checked=item.star;
      dialog.showModal();labelInput.focus();}
    function closeEditor(){if(dialog.open)dialog.close();previousFocus?.focus?.();}
    form.addEventListener('submit',e=>{e.preventDefault();if(!labelInput.reportValidity())return;let label=labelInput.value.trim();if(!label){labelInput.focus();return;}
      const raw=routeInput.value.trim()||routeFrom(label);
      if(!(raw.startsWith('#')||(raw.startsWith('/')&&!raw.startsWith('//')))){routeInput.setCustomValidity('Use a route starting with / or #');routeInput.reportValidity();return;}
      routeInput.setCustomValidity('');let item={label,route:raw,heart:heartInput.checked,star:starInput.checked};
      if(createMode) add(item);else update(currentId,item);closeEditor();});
    routeInput.addEventListener('input',()=>routeInput.setCustomValidity(''));
    cancel.addEventListener('click',closeEditor);
    dialog.addEventListener('close',()=>previousFocus?.focus?.());
    dialog.addEventListener('click',e=>{if(e.target===dialog)closeEditor();});
    function render(){row.replaceChildren();const sorted=rendered();sorted.forEach((s,i)=>{
      const wrap=element('div','st-shortcut');wrap.dataset.id=s.id;wrap.style.setProperty('--tab-color',HUES[i%HUES.length]);
      const main=element('button','st-shortcut__main');main.type='button';main.title='Open '+s.label;
      main.appendChild(element('span','st-shortcut__diamond'));
      main.appendChild(element('span','st-shortcut__label',s.label));
      if(s.heart||s.star){const icon=element('span','st-shortcut__fav');icon.innerHTML=svg[s.heart?'heart':'star'];icon.dataset.kind=s.heart?'heart':'star';icon.setAttribute('aria-label',s.heart?'Purple Heart':'Gold Star');main.appendChild(icon);}
      main.addEventListener('click',()=>{closeMenu();if(typeof opt.onNavigate==='function')opt.onNavigate(s.route,{...s});else if(s.route.startsWith('#'))document.querySelector(s.route)?.scrollIntoView({behavior:'smooth'});});
      const more=element('button','st-shortcut__more');more.type='button';more.title='Options for '+s.label;more.setAttribute('aria-label','Options for '+s.label);more.innerHTML=svg.dots;
      more.addEventListener('click',()=>openMenu(more,s.id));wrap.addEventListener('contextmenu',e=>{e.preventDefault();openMenu(more,s.id)});
      wrap.append(main,more);row.appendChild(wrap);
    });
    const plus=element('button','st-shortcut st-shortcut--add');plus.type='button';plus.innerHTML=svg.plus;plus.appendChild(element('span','','Add a tab'));plus.addEventListener('click',()=>openEditor('add'));row.appendChild(plus);
    }
    menu.addEventListener('keydown',e=>{if(!['ArrowDown','ArrowUp','Home','End'].includes(e.key))return; e.preventDefault();const all=[...menu.querySelectorAll('button')];const index=all.indexOf(document.activeElement);const target=e.key==='Home'?0:e.key==='End'?all.length-1:e.key==='ArrowDown'?(index+1)%all.length:(index+all.length-1)%all.length;all[target].focus();});
    menu.addEventListener('click',e=>{const b=e.target.closest('button[data-act]');if(!b)return;const id=currentId;const action=b.dataset.act;closeMenu();if(action==='edit')openEditor('edit',id);if(action==='heart')update(id,{heart:true,star:false});if(action==='star')update(id,{heart:false,star:true});if(action==='remove')remove(id);});
    function outside(e){if(!menu.hidden&&!menu.contains(e.target)&&!nav.contains(e.target))closeMenu();}
    function keydown(e){if(e.key==='Escape'&&!menu.hidden){const anchor=menuAnchor;closeMenu();anchor?.focus();}}
    document.addEventListener('pointerdown',outside);document.addEventListener('keydown',keydown);
    render();
    return {el:nav,list,set,add,update,remove,openAdd:()=>openEditor('add'),reset:()=>safeChange(opt.initial),destroy(){closeMenu();document.removeEventListener('pointerdown',outside);document.removeEventListener('keydown',keydown);menu.remove();dialog.remove();root.replaceChildren();}};
  }
  return {mount};
});
