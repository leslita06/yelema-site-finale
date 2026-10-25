
/* Envoi des formulaires vers contact@yelema.ai, sans serveur a tenir.
   YL_COLLECTE reste vide tant qu'aucun classeur n'est branche : le jour ou il
   l'est, la meme charge part AUSSI dans le classeur, sans rien changer ici.
   ylEnvoyer ne dit jamais « c'est parti » avant la reponse du service : un
   accuse de reception affiche trop tot serait un mensonge a la visiteuse. */
var YL_MAIL="https://formsubmit.co/ajax/contact@yelema.ai";
var YL_COLLECTE="";
function ylEnvoyer(charge,fait,rate){
  charge.Page=location.pathname.split('/').pop()||'index.html';
  if(YL_COLLECTE){
    try{ fetch(YL_COLLECTE,{method:'POST',mode:'no-cors',
      headers:{'Content-Type':'text/plain;charset=utf-8'},
      body:JSON.stringify(charge)}); }catch(e){}
  }
  var m={},k;
  for(k in charge){ if(charge.hasOwnProperty(k)&&String(charge[k]).trim()) m[k]=charge[k]; }
  m._captcha='false'; m._template='table';
  fetch(YL_MAIL,{method:'POST',
      headers:{'Content-Type':'application/json','Accept':'application/json'},
      body:JSON.stringify(m)})
    .then(function(r){ return r.json(); })
    .then(function(d){ if(d&&String(d.success)==='true'){ fait(); } else { rate(); } })
    .catch(function(){ rate(); });
}

const menu=document.getElementById('menu'),burger=document.getElementById('burger');
burger.addEventListener('click',()=>{menu.classList.toggle('open');burger.classList.toggle('open');burger.setAttribute('aria-expanded',menu.classList.contains('open'));});
function topRoute(id){return id.startsWith('expert-')?'experts':id;}
function route(){
 let id=(location.hash.replace('#','')||'accueil');
 /* #demo ouvre le formulaire par-dessus la page contact, depuis n'importe quelle page. */
 if(id==='demo') id='contact';
 /* #projet ouvre sa fenêtre par-dessus la page en cours (p189). */
 if(id==='projet'){ if(window.ylVu) return; id='offres'; }
 if(!document.getElementById('view-'+id)) id=document.getElementById('view-accueil')?'accueil':((document.querySelector('.view.active')||document.querySelector('.view')||{id:'view-'}).id.slice(5));
 if(!document.getElementById('view-'+id)) return;
 document.querySelectorAll('.view').forEach(v=>v.classList.remove('active'));
 document.getElementById('view-'+id).classList.add('active');
 let t=topRoute(id);
 document.querySelectorAll('.menu a').forEach(a=>a.classList.toggle('on',a.dataset.route===t));
 menu.classList.remove('open');
 burger.classList.remove('open');
 burger.setAttribute('aria-expanded','false');
 window.scrollTo({top:0,behavior:'auto'});
 window.ylVu=1;
}
document.addEventListener('click',function(e){
 const a=e.target.closest('a[href^="#"]');
 if(!a) return;
 const target=a.getAttribute('href').slice(1);
 if(!target) return;
 e.preventDefault();
 e.stopPropagation();
 if(location.hash==='#'+target){route();}else{location.hash=target;}
});
window.addEventListener('hashchange',route);route();


(function(){
 var m=document.getElementById('ylmodal');
 if(!m) return;
 var dernier=null;
 function ouvrir(e){ if(e) e.preventDefault(); dernier=document.activeElement;
   m.hidden=false; document.body.style.overflow='hidden';
   var p=m.querySelector('input'); if(p) p.focus(); }
 function fermer(){ m.hidden=true; document.body.style.overflow='';
   if(dernier&&dernier.focus) dernier.focus(); }
 document.querySelectorAll('a[href="#demo"],[data-demo]').forEach(function(a){
   a.addEventListener('click',ouvrir);
 });
 /* Arrivee directe sur #demo (lien depuis une page autonome ou lien partage). */
 function surHash(){ if(location.hash==='#demo'&&m.hidden) ouvrir(); }
 window.addEventListener('hashchange',surHash); surHash();
 m.querySelectorAll('[data-close]').forEach(function(b){b.addEventListener('click',fermer);});
 document.addEventListener('keydown',function(e){ if(e.key==='Escape'&&!m.hidden) fermer(); });
 document.getElementById('ylmform').addEventListener('submit',function(e){
   e.preventDefault();
   var d=new FormData(this), l=[], f=this,
       z=document.getElementById('ylm-ok'),
       b=f.querySelector('button[type=submit]');
   d.forEach(function(v,k){ if(String(v).trim()) l.push(k+' : '+v); });
   if(b){ b.disabled=true; b.textContent='Envoi en cours…'; }
   function rendre(){ if(b){ b.disabled=false; b.textContent='Demander une démo'; } }
   ylEnvoyer({_subject:'Demande de démonstration, '+(d.get('societe')||''),
       'Société':d.get('societe')||'', 'Nom':d.get('nom')||'',
       'email':d.get('email')||'',
       'Téléphone':String(d.get('tel')||'').trim()
         ? (d.get('indicatif')||'')+' '+String(d.get('tel')).trim() : '',
       'Métier':d.get('metier')||'', 'Métier (autre)':d.get('metier_autre')||'',
       'Effectif':d.get('effectif')||'', 'Message':d.get('message')||''},
     function(){ if(z){ z.hidden=false; } f.reset(); rendre(); },
     function(){ rendre();
       var corps=encodeURIComponent("Demande de démonstration\n\n"+l.join("\n"));
       window.location.href='mailto:contact@yelema.ai?subject='
         +encodeURIComponent('Demande de démonstration, '+(d.get('societe')||''))
         +'&body='+corps; });
 });
})();

/* Le metier « Autre » ouvre un champ libre, et sa reponse part avec le reste :
   sans lui, le formulaire perdait le seul metier qu'on ne propose pas encore. */
(function(){
 var s=document.querySelector('#ylmform select[name=metier]'),
     b=document.getElementById('yl-mautre');
 if(!s||!b) return;
 var i=b.querySelector('input');
 s.addEventListener('change',function(){
   var ouvert=(s.value==='Autre');
   b.hidden=!ouvert; i.required=ouvert;
   if(ouvert){i.focus();}else{i.value='';}
 });
})();

/* La lettre d'information n'etait branchee sur rien : le formulaire rechargeait
   la page et l'adresse etait perdue. Elle part maintenant par courriel. */
(function(){
 var f=document.getElementById('yl-news'); if(!f) return;
 var msg=document.getElementById('yl-news-msg');
 f.addEventListener('submit',function(e){
   e.preventDefault();
   var c=f.querySelector('input[name=email]'), v=(c.value||'').trim();
   if(!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(v)){
     if(msg) msg.textContent='Il manque une adresse valide.'; c.focus(); return; }
   if(msg) msg.textContent='Envoi en cours…';
   ylEnvoyer({_subject:'Inscription aux nouveautés Yelema',
       email:v, Demande:'Rester au courant des nouveautés', Source:'pied de page'},
     function(){ if(msg) msg.textContent='Merci, votre adresse est bien enregistrée.'; f.reset(); },
     function(){
       if(msg) msg.textContent='Merci, votre inscription part par e-mail.';
       window.location.href='mailto:contact@yelema.ai?subject='
         +encodeURIComponent('Inscription aux nouveautés Yelema')
         +'&body='+encodeURIComponent('Merci de m\'inscrire aux nouveautés Yelema.\n\nAdresse : '+v);
       f.reset(); });
 });
})();


/* 22/09/2026 : la fenêtre des projets sur mesure. Même mécanique que celle de la
   démonstration, un champ de description en plus. Un projet spécifique ne se traite
   pas avec le formulaire de démonstration : ni les mêmes questions, ni le même suivi. */
(function(){
 var m=document.getElementById('ylprojet');
 if(!m) return;
 var dernier=null;
 function ouvrir(e){ if(e) e.preventDefault(); dernier=document.activeElement;
   m.hidden=false; document.body.style.overflow='hidden';
   var p=m.querySelector('textarea'); if(p) p.focus(); }
 function fermer(){ m.hidden=true; document.body.style.overflow='';
   if(dernier&&dernier.focus) dernier.focus(); }
 document.querySelectorAll('a[href="#projet"],[data-projet]').forEach(function(a){
   a.addEventListener('click',ouvrir);
 });
 function surHash(){ if(location.hash==='#projet'&&m.hidden) ouvrir(); }
 window.addEventListener('hashchange',surHash); surHash();
 m.querySelectorAll('[data-close]').forEach(function(b){b.addEventListener('click',fermer);});
 document.addEventListener('keydown',function(e){ if(e.key==='Escape'&&!m.hidden) fermer(); });
 document.getElementById('ylpform').addEventListener('submit',function(e){
   e.preventDefault();
   var d=new FormData(this), l=[], f=this,
       z=document.getElementById('ylp-ok'),
       b=f.querySelector('button[type=submit]');
   d.forEach(function(v,k){ if(String(v).trim()) l.push(k+' : '+v); });
   if(b){ b.disabled=true; b.textContent='Envoi en cours…'; }
   function rendre(){ if(b){ b.disabled=false; b.textContent='Envoyer mon projet'; } }
   ylEnvoyer({_subject:'Projet sur mesure, '+(d.get('societe')||''),
       'Société':d.get('societe')||'', 'Nom':d.get('nom')||'',
       'email':d.get('email')||'',
       'Téléphone':String(d.get('tel')||'').trim()
         ? (d.get('indicatif')||'')+' '+String(d.get('tel')).trim() : '',
       'Secteur':d.get('secteur')||'', 'Échéance':d.get('echeance')||'',
       'Projet':d.get('projet')||''},
     function(){ if(z){ z.hidden=false; } f.reset(); rendre(); },
     function(){ rendre();
       var corps=encodeURIComponent("Projet sur mesure\n\n"+l.join("\n"));
       window.location.href='mailto:contact@yelema.ai?subject='
         +encodeURIComponent('Projet sur mesure, '+(d.get('societe')||''))
         +'&body='+corps; });
 });
})();
