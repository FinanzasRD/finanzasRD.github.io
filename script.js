(function(){'use strict';var d=document,w=window;
function q(s){return d.querySelector(s)}
function qa(s){return d.querySelectorAll(s)}
function id(s){return d.getElementById(s)}
function addE(el,ev,fn){if(el)el.addEventListener(ev,fn)}

var toggle=id('menuToggle'),nav=id('mainNav');
if(toggle&&nav){
  addE(toggle,'click',function(){
    toggle.classList.toggle('active');
    nav.classList.toggle('active');
    toggle.setAttribute('aria-expanded',nav.classList.contains('active'));
  });
  nav.querySelectorAll('.header__link').forEach(function(l){
    addE(l,'click',function(){
      toggle.classList.remove('active');
      nav.classList.remove('active');
      toggle.setAttribute('aria-expanded','false');
    });
  });
}

var header=id('header');
addE(w,'scroll',function(){
  header.style.boxShadow=w.scrollY>50?'0 2px 24px rgba(0,0,0,0.08)':'none';
});

function calcAhorro(m,m2){return m*m2}
function calcCompuesto(c,ap,t,a){
  var r=t/100/12,n=a*12;
  if(r===0)return c+ap*n;
  return c*Math.pow(1+r,n)+ap*((Math.pow(1+r,n)-1)/r);
}
function calcPrestamo(m,i,n){
  var r=i/100/12;
  if(r===0)return m/n;
  var f=Math.pow(1+r,n);
  return m*(r*f)/(f-1);
}
function calcConv(d,t){return d*t}

function fmtM(v){return 'RD$ '+Math.round(v).toLocaleString('es-DO')}
function fmtMS(v){
  if(v>=1e6)return 'RD$ '+(v/1e6).toFixed(2)+'M';
  return 'RD$ '+Math.round(v).toLocaleString('es-DO');
}
function fmtD(v){return 'RD$ '+v.toLocaleString('es-DO',{minimumFractionDigits:2,maximumFractionDigits:2})}

qa('.calcular-btn').forEach(function(b){
  addE(b,'click',function(){
    switch(b.dataset.calc){
      case'ahorro':{
        var m=parseFloat(id('ahorroMonto').value)||0,mes=parseInt(id('ahorroMeses').value)||1;
        q('#ahorroResult .result-value').textContent=fmtM(calcAhorro(m,mes));
        break;
      }
      case'compuesto':{
        var c=parseFloat(id('compCapital').value)||0,ap=parseFloat(id('compAporte').value)||0,t=parseFloat(id('compTasa').value)||0,a=parseInt(id('compAnios').value)||1;
        q('#compResult .result-value').textContent=fmtMS(calcCompuesto(c,ap,t,a));
        break;
      }
      case'prestamo':{
        var m2=parseFloat(id('prestamoMonto').value)||0,i=parseFloat(id('prestamoInteres').value)||0,p=parseInt(id('prestamoPlazo').value)||1;
        q('#prestamoResult .result-value').textContent=fmtM(calcPrestamo(m2,i,p));
        break;
      }
      case'presupuesto':{
        var i=parseFloat(id('presupIngreso').value)||0;
        id('presupNec').textContent=fmtM(i*0.5);
        id('presupDes').textContent=fmtM(i*0.3);
        id('presupAho').textContent=fmtM(i*0.2);
        break;
      }
      case'conversor':{
        var d=parseFloat(id('convDolares').value)||0,tr=parseFloat(id('convTasa').value)||0;
        q('#convResult .result-value').textContent=fmtD(calcConv(d,tr));
        break;
      }
    }
  });
});

function fetchLiveRate(){
  var inp=id('convTasa');
  fetch('https://open.er-api.com/v6/latest/USD').then(function(r){return r.json()}).then(function(d){
    if(d&&d.rates&&d.rates.DOP){
      inp.value=d.rates.DOP.toFixed(2);
      var dl=parseFloat(id('convDolares').value)||0;
      q('#convResult .result-value').textContent=fmtD(calcConv(dl,d.rates.DOP));
    }
  }).catch(function(){});
}
fetchLiveRate();

function runInit(){
  var aM=parseFloat(id('ahorroMonto').value)||0,aMes=parseInt(id('ahorroMeses').value)||1;
  q('#ahorroResult .result-value').textContent=fmtM(calcAhorro(aM,aMes));
  var cC=parseFloat(id('compCapital').value)||0,cA=parseFloat(id('compAporte').value)||0,cT=parseFloat(id('compTasa').value)||0,cAn=parseInt(id('compAnios').value)||1;
  q('#compResult .result-value').textContent=fmtMS(calcCompuesto(cC,cA,cT,cAn));
  var pM=parseFloat(id('prestamoMonto').value)||0,pI=parseFloat(id('prestamoInteres').value)||0,pP=parseInt(id('prestamoPlazo').value)||1;
  q('#prestamoResult .result-value').textContent=fmtM(calcPrestamo(pM,pI,pP));
  var dD=parseFloat(id('convDolares').value)||0,dT=parseFloat(id('convTasa').value)||0;
  q('#convResult .result-value').textContent=fmtD(calcConv(dD,dT));
  var pI=parseFloat(id('presupIngreso').value)||0;
  if(pI){id('presupNec').textContent=fmtM(pI*0.5);id('presupDes').textContent=fmtM(pI*0.3);id('presupAho').textContent=fmtM(pI*0.2)}
}
runInit();

qa('.calculadora__form input').forEach(function(inp){
  addE(inp,'keydown',function(e){
    if(e.key==='Enter'){
      var btn=inp.closest('.calculadora__form').querySelector('.calcular-btn');
      if(btn)btn.click();
    }
  });
});

var coopBody=id('coopBody'),addBtn=id('addCoopBtn');
function addRow(n,t,p,b){
  var tr=d.createElement('tr');
  tr.innerHTML='<td><input type="text" value="'+n+'" class="coop-input" placeholder="Nombre" aria-label="Nombre de cooperativa"></td><td><input type="number" value="'+t+'" class="coop-input" step="0.1" placeholder="0" aria-label="Tasa de inter\u00e9s"></td><td><input type="number" value="'+p+'" class="coop-input" placeholder="0" aria-label="Plazo en meses"></td><td><input type="number" value="'+b+'" class="coop-input" step="100" placeholder="0" aria-label="Beneficio en RD$"></td><td><button class="btn-delete" aria-label="Eliminar cooperativa">\u2715</button></td>';
  tr.querySelector('.btn-delete').addEventListener('click',function(){tr.remove()});
  coopBody.appendChild(tr);
}
qa('.btn-delete').forEach(function(btn){
  addE(btn,'click',function(){btn.closest('tr').remove()});
});
addE(addBtn,'click',function(){addRow('','','','')});

var pMod=id('privacyModal'),tMod=id('termsModal'),ov=id('modalOverlay');
function openM(m){m.classList.add('active');ov.classList.add('active');d.body.style.overflow='hidden'}
function closeAll(){pMod.classList.remove('active');tMod.classList.remove('active');ov.classList.remove('active');d.body.style.overflow=''}
addE(id('privacyLink'),'click',function(e){e.preventDefault();openM(pMod)});
addE(id('termsLink'),'click',function(e){e.preventDefault();openM(tMod)});
addE(id('privacyClose'),'click',closeAll);
addE(id('termsClose'),'click',closeAll);
addE(ov,'click',closeAll);
addE(d,'keydown',function(e){if(e.key==='Escape')closeAll()});

var form=id('contactForm');
addE(form,'submit',function(e){
  e.preventDefault();
  var n=id('contactNombre').value.trim(),em=id('contactEmail').value.trim(),msg=id('contactMensaje').value.trim();
  if(n&&em&&msg){
    fetch(form.getAttribute('action'),{method:'POST',body:new FormData(form),headers:{'Accept':'application/json'}}).then(function(){alert('\u2713 Mensaje enviado con \u00e9xito. Te responderemos pronto.');form.reset()}).catch(function(){alert('Error al enviar. Intenta de nuevo.');});
  }else alert('Por favor completa todos los campos.');
});

qa('a[href^="#"]').forEach(function(a){
  addE(a,'click',function(e){
    var h=this.getAttribute('href');
    if(h==='#')return;
    e.preventDefault();
    var t=q(h);
    if(t)t.scrollIntoView({behavior:'smooth',block:'start'});
  });
});

if('serviceWorker' in navigator){
  navigator.serviceWorker.register('sw.js').catch(function(){});
}

var cc=id('cookieConsent');
if(cc&&!localStorage.getItem('cookieConsent')){
  setTimeout(function(){cc.classList.add('show');},500);
  addE(id('cookieAccept'),'click',function(){
    localStorage.setItem('cookieConsent','accepted');
    cc.classList.remove('show');
  });
  addE(id('cookieMore'),'click',function(){
    w.location.href='privacidad.html';
  });
}

var tasasMonto=id('tasasMonto');
if(tasasMonto){
  function updTasas(){
    var m=parseFloat(tasasMonto.value)||0;
    d.querySelectorAll('.tasas-ganancia').forEach(function(el){
      var txt=el.textContent.trim();
      if(txt==='—')return;
      var pct=parseFloat(txt.replace(/[RD$\s,]/g,''));
      if(pct&&m)el.textContent='RD$ '+Math.round(m*pct/100).toLocaleString('es-DO');
    });
  }
  addE(tasasMonto,'input',updTasas);
  updTasas();
}

d.addEventListener('DOMContentLoaded',function(){
  var imgs=d.querySelectorAll('img[loading="lazy"]');
  if('loading' in HTMLImageElement.prototype){}
  else{
    var io=new IntersectionObserver(function(entries){
      entries.forEach(function(e){
        if(e.isIntersecting){
          var img=e.target;
          img.src=img.dataset.src;
          io.unobserve(img);
        }
      });
    });
    imgs.forEach(function(img){io.observe(img)});
  }

  var catBtns=d.querySelectorAll('.blog__cat-btn');
  var blogCards=d.querySelectorAll('.blog__card[data-cat]');
  catBtns.forEach(function(btn){
    addE(btn,'click',function(){
      catBtns.forEach(function(b){b.classList.remove('blog__cat-btn--active')});
      btn.classList.add('blog__cat-btn--active');
      var cat=btn.dataset.cat;
      blogCards.forEach(function(card){
        card.style.display=(cat==='all'||card.dataset.cat===cat)?'block':'none';
      });
    });
  });
});
})();