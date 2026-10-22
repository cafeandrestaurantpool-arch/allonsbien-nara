document.addEventListener('click',function(e){var b=e.target.closest('.ab-slide');if(!b)return;var sec=b.closest('section');var tr=sec&&sec.querySelector('.ab-slider');if(!tr)return;e.preventDefault();tr.scrollBy({left:(tr.clientWidth*0.8)*(+b.getAttribute('data-dir')),behavior:'smooth'});});
requestAnimationFrame(function(){requestAnimationFrame(function(){document.documentElement.classList.add('ab-anim');});});
(function(){
  var el=document.getElementById('ship'),root=document.documentElement;
  var closed=false;try{closed=sessionStorage.getItem('ship-off')==='1'}catch(e){}
  if(closed)return;
  root.classList.add('ship-on');
  var reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var x=0,y=0,vx=58,vy=44,hover=false,last=0;
  function size(){return el.offsetWidth||96}
  function bounds(){var s=size();return {minX:8,minY:76,maxX:window.innerWidth-s-8,maxY:window.innerHeight-s-70}}
  function park(){var b=bounds();x=b.maxX;y=b.maxY;place();}
  function place(){el.style.transform='translate3d('+x+'px,'+y+'px,0) scale('+(typeof sc==='number'?sc:1)+')';el.style.transformOrigin='100% 100%';}
  var b0=bounds();x=b0.minX+(b0.maxX-b0.minX)*0.72;y=b0.minY+(b0.maxY-b0.minY)*0.25;place();
  if(Math.random()<.5)vx=-vx;
  el.addEventListener('mouseenter',function(){hover=true});
  el.addEventListener('mouseleave',function(){hover=false});
  el.addEventListener('focusin',function(){hover=true});
  el.addEventListener('focusout',function(){hover=false});
  document.getElementById('ship-x').addEventListener('click',function(e){e.preventDefault();e.stopPropagation();root.classList.remove('ship-on');try{sessionStorage.setItem('ship-off','1')}catch(err){}});
  window.addEventListener('resize',function(){var b=bounds();x=Math.min(Math.max(x,b.minX),b.maxX);y=Math.min(Math.max(y,b.minY),b.maxY);place();});
  if(reduce){park();return;}
  var sc=1,zone=false,zt=0;
  function zoneVisible(){var v=document.body;var H=window.innerHeight,as=v.querySelectorAll('a[href*="item.rakuten.co.jp"]');for(var i=0;i<as.length;i++){var r=as[i].getBoundingClientRect();if(r.bottom>H*0.08&&r.top<H*0.92)return true;}return false;}
  function step(t){var dt=last?Math.min((t-last)/1000,0.05):0;last=t;
    if(t-zt>250){zt=t;zone=zoneVisible();}
    if(!hover&&!document.hidden){var b=bounds();
      if(zone){var k=Math.min(1,dt*5);x+=(b.maxX-x)*k;y+=(b.maxY-y)*k;sc+=(0.62-sc)*k;}
      else{sc+=(1-sc)*Math.min(1,dt*5);x+=vx*dt;y+=vy*dt;
      if(x<=b.minX){x=b.minX;vx=Math.abs(vx)}else if(x>=b.maxX){x=b.maxX;vx=-Math.abs(vx)}
      if(y<=b.minY){y=b.minY;vy=Math.abs(vy)}else if(y>=b.maxY){y=b.maxY;vy=-Math.abs(vy)}}
      place();}
    requestAnimationFrame(step);}
  requestAnimationFrame(step);
})();
(function(){
  var root=document.documentElement;var fine=window.matchMedia&&window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  var tg=document.getElementById('aron-toggle');
  if(!fine)return;
  root.classList.add('fine');
  var reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var el=document.getElementById('aron'),dot=document.getElementById('aron-dot');
  var mx=-200,my=-200,x=-200,y=-200,lastX=0,on=true,say=document.getElementById('aron-say');
  function isBuy(t){var h=t.getAttribute&&t.getAttribute('href')||'';return /rakuten/.test(h);}
  try{if(localStorage.getItem('aron-off')==='1')on=false}catch(e){}
  function set(v){on=v;root.classList.toggle('aron-on',on);tg.setAttribute('aria-pressed',on?'true':'false');try{localStorage.setItem('aron-off',on?'0':'1')}catch(e){}}
  set(on);
  tg.addEventListener('click',function(e){e.stopPropagation();set(!on);});
  window.addEventListener('mousemove',function(e){mx=e.clientX;my=e.clientY;dot.style.transform='translate3d('+mx+'px,'+my+'px,0)';
    var t=e.target.closest&&e.target.closest('a,button,[data-go],input,label');el.classList.toggle('is-hover',!!t);
    if(t){say.textContent=isBuy(t)?'買ってみる？':'どうぞ';}},{passive:true});
  window.addEventListener('mousedown',function(e){var t=e.target.closest&&e.target.closest('a,button,[data-go]');if(!t)return;
    if(isBuy(t)){say.textContent='買ってみる！';}
    el.classList.remove('is-press');void el.offsetWidth;el.classList.add('is-press');},{passive:true});
  el.addEventListener('animationend',function(){el.classList.remove('is-press');});
  document.addEventListener('mouseleave',function(){mx=my=-200;});
  function tick(){var k=reduce?1:0.32;x+=(mx-58-x)*k;y+=(my-20-y)*k;
    el.style.transform='translate3d('+x+'px,'+y+'px,0)';requestAnimationFrame(tick);}
  requestAnimationFrame(tick);
})();
