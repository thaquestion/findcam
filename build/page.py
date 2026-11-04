import json,sys
import os,sys
HERE=os.path.dirname(os.path.abspath(__file__))
data=open(os.path.join(HERE,'data.json')).read()
html=r'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Run With Cam | Breaking 42</title>
<meta name="description" content="Find when Cameron Balser will be near you on his Breaking 42 run across America, and where to meet him to run a few miles together.">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<style>
:root{--bg:#f5f2eb;--panel:#fbf9f4;--fg:#171c16;--muted:#5e625b;--line:#e3ddd0;--ink:#171c16;--ink2:#1e2820;--gold:#d9b46a;--accent:#171c16;--accent-soft:#efe7d4;--link:#7a5d1f;--ok:#2f6b3b}
html,body{margin:0;background:var(--bg);color:var(--fg);font-family:"Inter",system-ui,-apple-system,Segoe UI,sans-serif;line-height:1.45}
*{box-sizing:border-box}
</style></head>
<body>
<header style="background:#f8f5ee;border-bottom:1px solid var(--line)">
<div style="max-width:1100px;margin:0 auto;padding:18px 16px;display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap">
<a href="https://camerondeanbalser.com/" style="color:var(--fg);text-decoration:none;font-weight:800;font-size:17px">Cameron Balser</a>
<nav style="display:flex;gap:22px;font-size:14px;letter-spacing:.06em;text-transform:uppercase"><a href="https://camerondeanbalser.com/#tracker" style="color:var(--fg);text-decoration:none">Live</a><a href="https://camerondeanbalser.com/route/" style="color:var(--fg);text-decoration:none">Route</a><a href="https://camerondeanbalser.com/adventures/" style="color:var(--fg);text-decoration:none">Adventures</a></nav>
</div>
</header>
<section style="max-width:1100px;margin:28px auto 0;padding:0 16px">
<div style="background:var(--ink);color:#fbfcf6;border-radius:22px;padding:40px 28px;overflow:hidden">
<p style="margin:0 0 14px;font-size:12px;font-weight:800;letter-spacing:.18em;text-transform:uppercase;color:var(--gold)">2026 Trans-America FKT</p>
<p style="margin:0 0 6px;font-size:clamp(22px,3.5vw,30px);line-height:1;font-weight:900;letter-spacing:-.03em;color:var(--gold)">Breaking 42</p>
<h1 style="margin:0 0 14px;font-size:clamp(36px,7vw,64px);line-height:1;font-weight:900;letter-spacing:-.045em">Run a few miles with Cam.</h1>
<p style="margin:0;max-width:640px;font-size:18px;color:#d8dbd2">Type your town, or pick the day you're free, and see when Cameron Balser will be near you and which crew stops to meet him at. The crew stops about every 4 miles, which is the easiest place to join him.</p>
</div>
</section>
<style>
.wrap{max-width:1100px;margin:0 auto;padding:0 16px 48px}
.card{background:var(--panel);border:1px solid var(--line);border-radius:18px;padding:22px;margin-top:18px}
h2{font-weight:900;letter-spacing:-.03em}h3{font-weight:800;letter-spacing:-.01em}
.eyebrow{margin:0 0 8px;font-size:12px;font-weight:800;letter-spacing:.18em;text-transform:uppercase;color:#8a6a24}
#map{height:420px;border-radius:14px;border:1px solid var(--line);margin-top:12px;background:#ece8dd}
.leg{display:flex;gap:16px;flex-wrap:wrap;margin-top:10px;font-size:13px;color:var(--muted)}.leg i{display:inline-block;width:22px;height:5px;border-radius:3px;vertical-align:middle;margin-right:6px}
.tiles{filter:grayscale(.85) contrast(.95) brightness(1.04)}.leaflet-container{font-family:"Inter",system-ui,sans-serif}.camdot{width:18px;height:18px;border-radius:50%;background:var(--gold);border:3px solid var(--ink);box-shadow:0 0 0 6px rgba(217,180,106,.35)}
.row{display:flex;gap:8px;flex-wrap:wrap}
.row input{flex:1 1 220px;min-width:0;font:inherit;font-size:17px;padding:12px 14px;border-radius:10px;border:1px solid var(--line);background:var(--bg);color:var(--fg)}
button{font:inherit;font-size:16px;font-weight:800;padding:12px 22px;border-radius:999px;border:0;background:var(--ink);color:#fbfcf6;cursor:pointer}
button.ghost{background:transparent;color:var(--ink);border:1.5px solid var(--ink)}
.small{font-size:13px;color:var(--muted)}
.big{font-size:26px;line-height:1.15;font-weight:900;letter-spacing:-.03em;margin:6px 0 8px}
.pill{display:inline-block;background:var(--accent-soft);color:#6b5119;border-radius:999px;padding:3px 10px;font-size:13px;font-weight:600}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin-top:12px}
.stat{border:1px solid var(--line);border-radius:10px;padding:10px 12px}
.stat b{display:block;font-size:18px}
ul.spots{margin:8px 0 0;padding-left:18px}
ul.spots li{margin:4px 0}
a{color:var(--link)}
table{width:100%;border-collapse:collapse;font-size:14px}
th,td{text-align:left;padding:7px 6px;border-bottom:1px solid var(--line)}
th{color:var(--muted);font-weight:600;font-size:12px;text-transform:uppercase;letter-spacing:.04em}
.tablewrap{overflow-x:auto}
</style>
<main class="wrap">
<section class="card" id="mapcard">
<p class="eyebrow">Live map</p>
<h2 style="margin:0 0 6px;font-size:26px" id="maphead">Where Cam is right now</h2>
<p style="margin:0;color:var(--muted)" id="mapsub"></p>
<div id="map" role="img" aria-label="Map of Cam's route ahead to New York"></div>
<div class="leg"><span><i style="background:var(--gold)"></i>Today's stretch</span><span><i style="background:var(--ink)"></i>Road ahead to NYC</span><span><i style="background:#ffffff;border:2px solid var(--ink);width:10px;height:10px;border-radius:50%"></i>Where each day ends</span></div>
<p class="small" style="margin:8px 0 0" id="mapnote">The gold dot is our best guess of where Cam is, updated from his tracker every few minutes. Tap a dot for the day and town.</p>
</section>
<section class="card">
<label for="q" style="font-weight:600;display:block;margin-bottom:8px">Where are you?</label>
<div class="row"><input id="q" list="townlist" placeholder="e.g. Marion, IN" autocomplete="off"></div>
<label for="dist" style="font-weight:600;display:block;margin:14px 0 8px">How far do you want to run with him?</label>
<div class="row"><select id="dist" style="flex:1 1 220px;font:inherit;font-size:17px;padding:12px 14px;border-radius:10px;border:1px solid var(--line);background:var(--bg);color:var(--fg)">
<option value="2">2 miles</option><option value="4" selected>4 miles (one crew stop to the next)</option><option value="8">8 miles</option><option value="12">12 miles</option><option value="half">Half a day (about 37 miles)</option><option value="full">A full day (about 75 miles)</option></select></div>
<label for="dt" style="font-weight:600;display:block;margin:14px 0 8px">Have a day in mind? <span class="small" style="font-weight:400">(optional)</span></label>
<div class="row"><select id="dt" style="flex:1 1 220px;font:inherit;font-size:17px;padding:12px 14px;border-radius:10px;border:1px solid var(--line);background:var(--bg);color:var(--fg)"><option value="">Whenever he's closest to me</option></select><button id="go">Find Cam</button></div>
<datalist id="townlist"></datalist>
<div class="row" style="margin-top:10px;align-items:center"><button class="ghost" id="geo">Use my location</button><span class="small">You can also type coordinates, like 40.56, -85.66, or leave the town blank and just pick a day.</span></div>
<p id="err" class="small" style="color:var(--accent);margin:10px 0 0"></p>
</section>
<section class="card" id="result" hidden></section>
<section class="card" id="need" hidden>
<h2 style="margin:0 0 8px;font-size:18px">What you'll need</h2>
<ul style="margin:0;padding-left:18px"><li>Transportation, or a plan for getting there and back. Easiest is to come with a friend or friends: one drives, the others run.</li><li>Fuel and hydration for the distance you plan to run, and a place to store them</li><li>A smile and a positive attitude</li><li>To be ready for the experience of a lifetime</li></ul>
<p style="margin:10px 0 0;font-weight:600">The goal is to be part of something epic.</p>
</section>
<section class="card" id="now"></section>
<section class="card">
<h2 style="margin:0 0 8px;font-size:18px">Where he'll be each day</h2>
<p class="small" style="margin:0 0 8px" id="schednote"></p>
<div class="tablewrap"><table><thead><tr><th>Day</th><th>Date</th><th>From</th><th>To</th></tr></thead><tbody id="sched"></tbody></table></div>
</section>
<section class="card" id="faq">
<h2 style="margin:0 0 8px;font-size:18px">Good to know</h2>
<p style="margin:0 0 4px">First and foremost, Cam is so excited to have you. He values nothing more than human connection, and people are the highlight of his journeys. Everything below is here to give you as much time on your feet with him as possible and to make the experience great for you. It all comes with love.</p>
<h3 style="margin:12px 0 4px;font-size:15px">Will he wait while I get ready?</h3>
<p style="margin:0">No. Cam's day is planned to the minute, so he leaves each stop right away. Arrive with your vest, belt and shoes sorted, or you'll be playing catch-up.</p>
<h3 style="margin:12px 0 4px;font-size:15px">What happens at the 4-mile stops?</h3>
<p style="margin:0">He refuels and sometimes changes clothes. Those stops are tightly timed and he knows exactly how long each one takes. Just roll with the vibes.</p>
<h3 style="margin:12px 0 4px;font-size:15px">Can the crew help me out?</h3>
<p style="margin:0">Please be self-sufficient. The crew's job is to keep Cam moving and fed all day, which keeps him on schedule and stacking up miles.</p>
<h3 style="margin:12px 0 4px;font-size:15px">Cam looks pretty beat up. Is he okay?</h3>
<p style="margin:0">Running 75 miles a day for six weeks takes a real toll, so he might look worn down, walk a little stiff or have some tape and bandages. That comes with an effort like this, and his team keeps a close eye on his health. Please don't offer medical advice or suggest fixes. The best thing you can bring him is good company and good energy.</p>
<h3 style="margin:12px 0 4px;font-size:15px">Can I wait in the van during breaks?</h3>
<p style="margin:0">No, the van is for Cam and his crew. Bring clothes to stay warm and dry while you wait.</p>
</section>
<section class="card" id="donts">
<h2 style="margin:0 0 8px;font-size:18px">Please don't</h2>
<p style="margin:0 0 6px">Please don't ask the crew for any of these:</p>
<ul style="margin:0;padding-left:18px;columns:2;max-width:420px"><li>Rides</li><li>Storage</li><li>Food</li><li>Water</li><li>Shelter</li><li>Clothing</li><li>Supplements</li></ul>
<p style="margin:12px 0 0">If there's time, the crew can take a photo for you. Please don't interrupt the media team while they're shooting photos or video.</p>
</section>
<section class="card">
<h2 style="margin:0 0 8px;font-size:18px">Before you head out</h2>
<ul style="margin:0;padding-left:18px">
<li>Check <a href="https://share.garmin.com/HJZZX" target="_blank" rel="noopener">his live Garmin map</a> right before you leave.</li>
<li>Park well off the road at a gas station, church lot or park, never on the shoulder ahead of him.</li>
<li>Bring your own water and food so the crew doesn't have to look after you.</li>
<li>After dark, wear a headlamp and something reflective.</li>
</ul>
<h3 style="margin:16px 0 6px;font-size:15px">How the estimate works</h3>
<p class="small" style="margin:0" id="method">From his last GPS ping, the rest of today uses today's average pace including stops. Later days start at 5 am local from the planned day starts, use each day's terrain-adjusted pace, and follow his usual slowdown late in the day, built from his last seven days of two-hour splits. The window widens about half an hour for every day further out, since small daily differences add up. Today's route in Iowa is the exact course. Past Osceola the route is drawn town to town between the planned day finishes, so the closest point can be off by a few miles until the full route file is added.</p>
<p class="small" id="asof" style="margin:10px 0 0"></p>
</section>
</main>
<script>
const D=__DATA__;
const $=s=>document.querySelector(s);
const R=3958.8,rad=x=>x*Math.PI/180;
function hav(a,b,c,d){const x=Math.sin(rad(c-a)/2)**2+Math.cos(rad(a))*Math.cos(rad(c))*Math.sin(rad(d-b)/2)**2;return 2*R*Math.asin(Math.sqrt(x));}
const EAST=2247.5,FINISH=3005.9,STOP=4;
const tzOff=m=>m>=EAST?-5:-6, tzName=m=>m>=EAST?'Eastern':'Central';
const DAYS=['Sun','Mon','Tue','Wed','Thu','Fri','Sat'],MON=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
const loc=(ms,off)=>new Date(ms+off*3600e3);
function fmtT(ms,off){const d=loc(ms,off);let h=d.getUTCHours(),m=Math.round(d.getUTCMinutes()/10)*10;if(m==60){m=0;h=(h+1)%24}const ap=h<12?'am':'pm';h=h%12||12;return h+':'+String(m).padStart(2,'0')+' '+ap;}
function fmtD(ms,off){const d=loc(ms,off);return DAYS[d.getUTCDay()]+' '+MON[d.getUTCMonth()]+' '+d.getUTCDate();}
const mm=x=>Math.floor(x)+':'+String(Math.round((x%1)*60)).padStart(2,'0');
// last week's average day
const wk=D.recent7, AVG=wk.reduce((a,r)=>a+r.miles,0)/wk.length, AVGH=wk.reduce((a,r)=>a+r.hrs,0)/wk.length;
const shapeTot=D.shape.reduce((a,b)=>a+b,0);
// hours after 5am to cover x miles of an average day (slower late in the day, from his two-hour splits)
function rawHours(x){let m=x*shapeTot/AVG,h=0;for(const b of D.shape){if(m<=b)return h+2*m/b;m-=b;h+=2}return h+2*m/D.shape[D.shape.length-1];}
const SCALE=AVGH/rawHours(AVG);
const planAvg=D.days.reduce((a,d)=>a+d.pace,0)/D.days.length;
function terrain(mile){for(const d of D.days)if(mile>=d.sm&&mile<d.em)return d.pace/planAvg;return 1;}
const T0=D.todayStartMile, asof=Date.parse(D.asof), todayStartMs=Date.parse(D.firstPing);
const dayNo0=D.days[0].day;
// day k (0 = today) runs from T0+k*AVG
const dayStart=k=>T0+k*AVG, dayEnd=k=>Math.min(FINISH,T0+(k+1)*AVG);
function startMs(k){const ds=new Date(Date.parse(D.days[0].date+'T00:00:00Z')+k*864e5);const off=tzOff(dayStart(k));return Date.UTC(ds.getUTCFullYear(),ds.getUTCMonth(),ds.getUTCDate(),5-off);}
const todayFactor=((asof-todayStartMs)/3600e3)/(rawHours(D.lastMile-T0)*SCALE);
function eta(mile){
 if(mile<=D.lastMile)return null;
 const k=Math.floor((mile-T0)/AVG);const x=mile-dayStart(k);
 if(k==0){return {ms:asof+(rawHours(x)-rawHours(D.lastMile-T0))*SCALE*todayFactor*3600e3,k};}
 return {ms:startMs(k)+rawHours(x)*SCALE*terrain(mile)*3600e3,k};
}
const winMin=k=>20+25*k;
const route=D.route.filter(p=>p[0]>=T0);
function pointAt(mile){for(let i=1;i<route.length;i++){const a=route[i-1],b=route[i];if(mile<=b[0]){const f=(mile-a[0])/((b[0]-a[0])||1);return [mile,a[1]+f*(b[1]-a[1]),a[2]+f*(b[2]-a[2])];}}return route[route.length-1];}
function closest(lat,lon){let best=null;for(let i=1;i<route.length;i++){const a=route[i-1],b=route[i];for(let s=0;s<=4;s++){const f=s/4,p=[a[0]+f*(b[0]-a[0]),a[1]+f*(b[1]-a[1]),a[2]+f*(b[2]-a[2])];const d=hav(lat,lon,p[1],p[2]);if(!best||d<best.d)best={d,p};}}return best;}
function nearTown(p){let b=null;for(const t of D.towns){const d=hav(p[1],p[2],t[2],t[3]);if(!b||d<b.d)b={d,t};}return b;}
const placeOf=p=>{const n=nearTown(p);return n.d<3?'in '+n.t[0]+', '+n.t[1]:Math.round(n.d)+' mi from '+n.t[0]+', '+n.t[1];};
const mapUrl=p=>'https://www.google.com/maps/search/?api=1&query='+p[1].toFixed(5)+','+p[2].toFixed(5);
function el(tag,attrs,...kids){const e=document.createElement(tag);for(const k in attrs||{}){if(k=='text')e.textContent=attrs[k];else e.setAttribute(k,attrs[k]);}kids.forEach(k=>e.append(k));return e;}
// crew stops of day k: every 4 miles from that day's start, plus the finish
function stops(k){const out=[],s=dayStart(k),e=dayEnd(k);for(let m=s+STOP;m<e-0.5;m+=STOP)out.push(m);out.push(e);return out.filter(m=>m>D.lastMile);}
function stopRow(m,me){const p=pointAt(m),e=eta(m-1e-6),off=tzOff(m-1e-6);const r={m,p,e,off,place:placeOf(p)};if(me)r.dist=hav(me.lat,me.lon,p[1],p[2]);return r;}
function stopTable(rows,best){const t=el('table');const hd=el('tr');['Stop','Time','Where',''].concat(rows[0]&&rows[0].dist!=null?['From you']:[]).forEach(h=>hd.append(el('th',{text:h})));t.append(el('thead',{},hd));const tb=el('tbody');
 rows.forEach(r=>{const tr=el('tr');if(best&&r===best)tr.setAttribute('style','background:var(--accent-soft)');
  tr.append(el('td',{text:'Mile '+Math.round(r.m).toLocaleString()}),el('td',{text:fmtT(r.e.ms,r.off)}),el('td',{text:r.place}));
  const td=el('td');td.append(el('a',{href:mapUrl(r.p),target:'_blank',rel:'noopener',text:'Map'}));tr.append(td);
  if(r.dist!=null)tr.append(el('td',{text:Math.round(r.dist)+' mi'}));tb.append(tr);});t.append(tb);const w=el('div',{class:'tablewrap'});w.append(t);return w;}

const parkUrl=p=>'https://www.google.com/maps/search/parking/@'+p[1].toFixed(5)+','+p[2].toFixed(5)+',15z';
function planBox(start){
 const box=el('div',{style:'margin-top:16px;border:1px solid var(--line);border-radius:12px;padding:14px'});
 const v=$('#dist').value;const k=start.e.k;
 const full=v=='full',half=v=='half';
 const n=full?(dayEnd(k)-dayStart(k)):half?Math.round(AVG/2):+v;
 let sm=start.m; if(full)sm=Math.max(dayStart(k),D.lastMile);
 if(full&&k==0){box.append(el('h3',{style:'margin:0 0 6px;font-size:16px',text:'Your run'}),el('p',{text:'Today is already under way. Pick another day to run the whole thing with him.'}));return box;}
 const em=Math.min(sm+n,dayEnd(k));const sp=pointAt(sm),ep=pointAt(em);
 const t1=full?startMs(k):eta(sm-1e-6).ms,t2=eta(em-1e-6).ms,off=tzOff(sm),off2=tzOff(em);
 const miles=Math.round(em-sm);
 box.append(el('h3',{style:'margin:0 0 6px;font-size:16px',text:'Your '+(full?'full day':miles+' miles')+' with Cam'}));
 const ul=el('ul',{style:'margin:0;padding-left:18px'});const li=(...parts)=>{const l=el('li',{style:'margin:5px 0'});parts.forEach(x=>l.append(typeof x=='string'?document.createTextNode(x):x));ul.append(l);};
 const a=(href,text)=>el('a',{href,target:'_blank',rel:'noopener',text});
 if(n<=4){
  li('Park near mile '+Math.round(sm).toLocaleString()+', '+placeOf(sp)+'. ',a(parkUrl(sp),'Find parking there'),'. Be there by '+fmtT(t1-15*60e3,off)+'.');
  li('Cam should come through around '+fmtT(t1,off)+'. Join him and run '+miles+' miles'+(miles>=4?' to his next crew stop':'')+', which he should reach around '+fmtT(t2,off2)+'.');
  li('Then turn around and run '+miles+' miles back to your car on your own, so plan on '+(2*miles)+' miles total.');
 } else if(!full&&!half){
  li('Start near mile '+Math.round(sm).toLocaleString()+', '+placeOf(sp)+', around '+fmtT(t1,off)+'. ',a(parkUrl(sp),'Find parking there'),'.');
  li('Run '+miles+' miles with him to mile '+Math.round(em).toLocaleString()+', '+placeOf(ep)+', around '+fmtT(t2,off2)+'. ',a(mapUrl(ep),'Map of that spot'),'.');
  li('Getting back: the easiest way is to bring a friend or friends, with one driving and the others running. Otherwise run it as an out and back, which makes it '+(2*miles)+' miles total.');
 } else {
  li((full?'He starts around 5 am '+tzName(sm)+' ':'Join him around '+fmtT(t1,off)+' ')+placeOf(sp)+(full?'':' (mile '+Math.round(sm).toLocaleString()+')')+' and finishes around '+fmtT(t2,off2)+' '+placeOf(ep)+'. That is about '+miles+' miles and '+Math.round((t2-t1)/3600e3)+' hours on your feet.');
  li('You need your own way back. Best plan: come with a friend or friends, with one driving along and the others running. Or have someone drop you off and pick you up at the end.');
  li('Carry or arrange your own food, water and gear for the whole stretch.');
 }
 box.append(ul);
 if(n>4)box.append(el('p',{class:'small',style:'margin:10px 0 0',text:"A heads-up: the crew's whole job is looking after Cam, so they can't drive runners back to their cars or carry gear for them. Plan your ride before you come."}));
 return box;
}
const dark=(ms,off)=>{const h=loc(ms,off).getUTCHours();return h>=18||h<7;};
const dayLabel=k=>k==0?'Today':k==1?'Tomorrow':'In '+k+' days';
function showWhere(me){
 const res=$('#result');res.hidden=false;res.replaceChildren();$('#need').hidden=false;
 const c=closest(me.lat,me.lon);const mile=c.p[0];
 if(mile<=D.lastMile+0.5){res.append(el('span',{class:'pill',text:'Already passed'}),el('p',{class:'big',text:'Cam is already past '+me.label+'.'}),el('p',{class:'small',text:'His route came closest '+placeOf(c.p)+'. He is heading east now, so pick a day or a town further along.'}));return;}
 const e=eta(mile);const off=tzOff(mile),w=winMin(e.k);const lo=e.ms-w*60e3,hi=e.ms+w*60e3;
 const win=fmtD(lo,off)==fmtD(hi,off)?fmtT(lo,off)+' and '+fmtT(hi,off):fmtT(lo,off)+' '+fmtD(lo,off)+' and '+fmtT(hi,off)+' '+fmtD(hi,off);
 res.append(el('span',{class:'pill',text:dayLabel(e.k)}));
 res.append(el('p',{class:'big',text:'Cameron Balser will be closest to '+me.label+' on '+fmtD(e.ms,off)+', between '+win+' '+tzName(mile)+'.'}));
 res.append(el('p',{class:'small',text:'His route passes about '+Math.max(1,Math.round(c.d))+' miles from you at its closest, '+placeOf(c.p)+'.'+(c.d>40?' Plan on a drive.':'')}));
 const dayEndMs=eta(dayEnd(e.k)-0.01);
 if(dayEndMs&&(dayEndMs.ms-e.ms)<1.5*3600e3)res.append(el('p',{class:'small',text:'That is near the end of his day. If he finishes a few miles short, he will pass you early the next morning instead.'}));
 // stops around the closest point
 const all=[];for(let k=Math.max(0,e.k-1);k<=e.k+1;k++)stops(k).forEach(m=>all.push(stopRow(m,me)));
 all.sort((a,b)=>a.dist-b.dist);const best=all[0];const near=all.filter(r=>Math.abs(r.m-best.m)<=STOP*2+0.1).sort((a,b)=>a.m-b.m);
 res.append(el('h3',{style:'margin:16px 0 4px;font-size:15px',text:'Crew stops closest to you'}));
 res.append(el('p',{class:'small',style:'margin:0 0 6px',text:'The highlighted stop is your best bet. Each stop is a few minutes, so get there early and park well off the road.'}));
 res.append(stopTable(near,best));
 res.append(planBox(best));
 mapShow(me,near,best);
 if(dark(best.e.ms,best.off))res.append(el('p',{class:'small',style:'margin-top:10px',text:'He may pass in the dark, so bring a headlamp and something reflective.'}));
 res.scrollIntoView({behavior:'smooth',block:'start'});
}
function showDay(k,me){
 const res=$('#result');res.hidden=false;res.replaceChildren();$('#need').hidden=false;
 const rows=stops(k).map(m=>stopRow(m,me));if(!rows.length){res.append(el('p',{text:'He has already finished that day.'}));return;}
 const off=tzOff(dayStart(k)),sm=Math.max(dayStart(k),D.lastMile);
 const from=placeOf(pointAt(sm)),to=placeOf(pointAt(dayEnd(k)));
 res.append(el('span',{class:'pill',text:dayLabel(k)}));
 res.append(el('p',{class:'big',text:'On '+fmtD(startMs(k),off)+', Cam runs from '+from.replace(/^in /,'')+' to '+to.replace(/^in /,'')+'.'}));
 let best=null;
 if(me){best=rows.slice().sort((a,b)=>a.dist-b.dist)[0];res.append(el('p',{class:'small',text:'The closest stop to '+me.label+' that day is mile '+Math.round(best.m).toLocaleString()+', '+best.place+', around '+fmtT(best.e.ms,best.off)+' '+tzName(best.m)+', about '+Math.round(best.dist)+' miles from you.'}));}
 res.append(el('p',{class:'small',text:(k==0?'He is on the road now. ':'He starts around 5 am '+tzName(dayStart(k))+'. ')+'Times can move by about '+winMin(k)+' minutes either way.'}));
 res.append(el('h3',{style:'margin:16px 0 4px;font-size:15px',text:'Crew stops that day'}));
 res.append(stopTable(rows,best));
 mapShow(me,rows,best);
 res.append(planBox(best||rows[0]));
 res.scrollIntoView({behavior:'smooth',block:'start'});
}
function parse(q){q=q.trim();if(!q)return null;const m=q.match(/^(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)$/);if(m)return {lat:+m[1],lon:+m[2],label:'your spot'};
 const parts=q.split(',').map(s=>s.trim().toLowerCase());const name=parts[0].replace(/^st\.? /,'saint ');const st=(parts[1]||'').replace(/indiana/,'in').replace(/illinois/,'il').replace(/iowa/,'ia').replace(/ohio/,'oh').replace(/pennsylvania/,'pa').replace(/new jersey/,'nj').replace(/new york/,'ny').slice(0,2);
 const hits=D.towns.filter(t=>t[0].toLowerCase()==name&&(!st||t[1].toLowerCase()==st));if(!hits.length)return undefined;
 hits.sort((a,b)=>closest(a[2],a[3]).d-closest(b[2],b[3]).d);const t=hits[0];return {lat:t[2],lon:t[3],label:t[0]+', '+t[1]};}
let geoMe=null;
function go(){ $('#err').textContent='';let me=geoMe;const q=$('#q').value;if(q.trim()){me=parse(q);if(me===undefined){$('#err').textContent="I couldn't find that town. Try a nearby bigger town, add the state like Marion, IN, or use your location.";return;}}
 const k=$('#dt').value;if(k!=='')return showDay(+k,me);if(!me){$('#err').textContent='Type your town or pick a day.';return;}showWhere(me);}
$('#go').addEventListener('click',go);$('#dist').addEventListener('change',()=>{if(!$('#result').hidden)go();});$('#q').addEventListener('keydown',e=>{if(e.key=='Enter')go();});$('#q').addEventListener('input',()=>{geoMe=null;});
$('#geo').addEventListener('click',()=>{if(!navigator.geolocation){$('#err').textContent="Your browser can't share location here. Type your town instead.";return;}
 navigator.geolocation.getCurrentPosition(p=>{geoMe={lat:p.coords.latitude,lon:p.coords.longitude,label:'you'};$('#q').value='';go();},()=>{$('#err').textContent="Location wasn't shared. Type your town instead.";},{timeout:10000});});
const dl=$('#townlist');D.towns.forEach(t=>dl.append(el('option',{value:t[0]+', '+t[1]})));
const nDays=Math.ceil((FINISH-T0)/AVG);
const sel=$('#dt');for(let k=0;k<nDays;k++)sel.append(el('option',{value:String(k),text:fmtD(startMs(k),tzOff(dayStart(k)))+' (day '+(dayNo0+k)+')'}));
// now card
const offNow=tzOff(D.lastMile);
const nw=$('#now');nw.append(el('h2',{style:'margin:0 0 6px;font-size:18px',text:'Where Cam is now'}));
const nst=el('div',{class:'stats'});const nx=(k,v)=>nst.append(el('div',{class:'stat'},el('span',{class:'small',text:k}),el('b',{text:v})));
nx('Last ping',fmtT(asof,offNow)+' '+tzName(D.lastMile)+', '+fmtD(asof,offNow));nx('Today so far',D.todayMiles.toFixed(1)+' mi since '+fmtT(todayStartMs,offNow));
nx('Pace today',mm(D.todayPace)+' /mi with stops');nx('Last 7 days',AVG.toFixed(1)+' mi a day');
nw.append(nst);
(function(){const gp=el('p',{style:'margin:10px 0 0'});nw.append(gp);
 const tick=()=>{const now=Date.now();if(now<=asof+10*60e3){gp.textContent='';return;}let lo=D.lastMile,hi=FINISH;const t=m=>{const e=eta(m);return e?e.ms:asof;};if(t(lo+0.01)>now){gp.textContent='';return;}
 for(let i=0;i<40;i++){const mid=(lo+hi)/2;if(t(mid)<now)lo=mid;else hi=mid;}
 const k=Math.floor((lo-T0)/AVG),endMs=eta(dayEnd(k)-0.01).ms;const mins=Math.round((now-asof)/60e3);
 gp.textContent=now>endMs?'Best guess right now: done for the day '+placeOf(pointAt(dayEnd(k)))+'.':'Best guess right now, '+mins+' min after his last ping at today\'s pace: about mile '+Math.round(lo).toLocaleString()+', '+placeOf(pointAt(lo))+'. Check his live Garmin map to be sure.';};
 tick();setInterval(tick,60e3);})();
const tb=$('#sched');for(let k=0;k<nDays;k++){const tr=el('tr');[ 'Day '+(dayNo0+k), fmtD(startMs(k),tzOff(dayStart(k))), placeOf(pointAt(Math.max(dayStart(k),T0))).replace(/^in /,''), placeOf(pointAt(dayEnd(k))).replace(/^in /,'')].forEach(v=>tr.append(el('td',{text:v})));tb.append(tr);}
$('#schednote').textContent='Cam starts around 5 am local and has averaged '+AVG.toFixed(1)+' miles a day over the last week. Times are local to where he is.';
$('#method').textContent='From his last GPS ping, the rest of today follows his pace so far. Each later day starts at 5 am local where the previous one ended and covers his last-week average of '+AVG.toFixed(1)+' miles in about '+AVGH.toFixed(1)+' hours, with his usual slowdown late in the day from his two-hour splits and a small adjustment for hills. Crew stops are counted every 4 miles from each day\'s start. The window is plus or minus 20 minutes today and widens about 25 minutes for every day further out. The route follows the crew\'s course: the exact line today, then the planned day starts with a few points in between, so a closest point can be off by a mile or two.';
$('#asof').textContent='Data as of his '+fmtT(asof,offNow)+' '+tzName(D.lastMile)+' ping on '+fmtD(asof,offNow)+'. Record deadline: '+D.recordDeadline+'.';
// ---- map ----
let MAP=null,meLayer=null,camMk=null;
function guessMile(){const now=Date.now();let lo=D.lastMile,hi=FINISH;const t=m=>{const e=eta(m);return e?e.ms:asof;};if(t(lo+0.01)>now)return D.lastMile;for(let i=0;i<40;i++){const mid=(lo+hi)/2;if(t(mid)<now)lo=mid;else hi=mid;}const k=Math.floor((lo-T0)/AVG);return Math.min(lo,dayEnd(k));}
(function(){
 const fin=eta(FINISH-0.01);const offF=tzOff(FINISH);
 $('#mapsub').textContent=Math.round(D.lastMile).toLocaleString()+' miles down from San Francisco, about '+Math.round(FINISH-D.lastMile).toLocaleString()+' to go to New York City Hall.'+(fin?' At this pace he finishes around '+fmtD(fin.ms,offF)+'.':'');
 if(typeof L==='undefined'){$('#map').style.display='none';$('#mapnote').textContent='The map could not load. The schedule below has every day.';return;}
 MAP=L.map('map',{scrollWheelZoom:false,zoomControl:true});
 L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png',{maxZoom:18,attribution:'&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',className:'tiles'}).addTo(MAP);
 const seg=(a,b)=>{const pts=[pointAt(a)];for(const p of route)if(p[0]>a&&p[0]<b)pts.push(p);pts.push(pointAt(b));return pts.map(p=>[p[1],p[2]]);};
 const gm=guessMile();
 L.polyline(seg(Math.max(gm,dayEnd(0)),FINISH),{color:'#171c16',weight:4,opacity:.85}).addTo(MAP);
 if(gm<dayEnd(0))L.polyline(seg(gm,dayEnd(0)),{color:'#d9b46a',weight:7,opacity:1}).addTo(MAP);
 for(let k=0;k<nDays;k++){const m=dayEnd(k);if(m>=FINISH-0.5)break;const p=pointAt(m),off=tzOff(m);
  L.circleMarker([p[1],p[2]],{radius:5,color:'#171c16',weight:2,fillColor:'#ffffff',fillOpacity:1}).addTo(MAP).bindTooltip(fmtD(startMs(k),tzOff(dayStart(k)))+': ends '+placeOf(p).replace(/^in /,'')+' (day '+(dayNo0+k)+')');}
 const f=pointAt(FINISH);L.circleMarker([f[1],f[2]],{radius:8,color:'#171c16',weight:3,fillColor:'#d9b46a',fillOpacity:1}).addTo(MAP).bindTooltip('Finish: New York City Hall',{permanent:true,direction:'left'});
 const cp=pointAt(gm);
 camMk=L.marker([cp[1],cp[2]],{icon:L.divIcon({className:'',html:'<div class="camdot"></div>',iconSize:[24,24],iconAnchor:[12,12]}),zIndexOffset:1000}).addTo(MAP).bindTooltip('Cam is about here',{permanent:true,direction:'top',offset:[0,-12]});
 MAP.fitBounds(L.latLngBounds(seg(Math.max(T0,gm-10),FINISH)),{padding:[24,24]});
 setInterval(()=>{const p=pointAt(guessMile());camMk.setLatLng([p[1],p[2]]);},60e3);
})();
function mapShow(me,rows,best){
 if(!MAP)return;if(!meLayer)meLayer=L.layerGroup().addTo(MAP);meLayer.eachLayer(l=>{l.unbindTooltip();});meLayer.clearLayers();const b=[];
 if(me){L.circleMarker([me.lat,me.lon],{radius:7,color:'#7a5d1f',weight:3,fillColor:'#fbf9f4',fillOpacity:1}).addTo(meLayer).bindTooltip('You: '+me.label,{permanent:true,direction:'right'});b.push([me.lat,me.lon]);}
 for(const r of rows){if(!r.e)continue;const p=pointAt(r.m);const isB=best&&r.m===best.m;L.circleMarker([p[1],p[2]],{radius:isB?8:5,color:'#171c16',weight:2,fillColor:isB?'#d9b46a':'#ffffff',fillOpacity:1}).addTo(meLayer).bindTooltip('Crew stop, about '+fmtT(r.e.ms,r.off)+(isB?' (your best bet)':''),isB?{permanent:true,direction:'top'}:{});b.push([p[1],p[2]]);}
 if(b.length)MAP.fitBounds(L.latLngBounds(b),{padding:[40,40],maxZoom:12});
}
</script>
</body></html>'''
open(os.path.join(HERE,'meet-cam.html'),'w').write(html.replace('__DATA__',data))
