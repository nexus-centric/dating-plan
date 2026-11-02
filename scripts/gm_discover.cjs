// b13 discovery: Google Maps search per query -> feed place links -> open each place page -> details. Cached/resumable.
// node scripts/gm_discover.cjs data/b13/queries.json   (out: data/b13/links.json, data/b13/places.json)
const fs=require('fs');const {chromium}=require('/tmp/pw/node_modules/playwright');
const D='/workspace/date-app/data/b13/',LK=D+'links.json',PL=D+'places.json';
const qs=JSON.parse(fs.readFileSync(process.argv[2]));const links=fs.existsSync(LK)?JSON.parse(fs.readFileSync(LK)):{};const places=fs.existsSync(PL)?JSON.parse(fs.readFileSync(PL)):{};
const PER=+(process.env.PER||8);
(async()=>{const b=await chromium.launch();const ctx=await b.newContext({locale:'vi-VN',viewport:{width:1280,height:900}});
const pages=await Promise.all([...Array(+(process.env.TABS||1))].map(()=>ctx.newPage()));let bl=false;
// 1) search
let qi=0;const todoQ=qs.filter(q=>!links[q]);
await Promise.all(pages.map(async p=>{while(qi<todoQ.length&&!bl){const q=todoQ[qi++];try{await p.goto('https://www.google.com/maps/search/'+encodeURIComponent(q)+'?hl=vi',{waitUntil:'domcontentloaded',timeout:30000});
 await p.waitForSelector('div[role="feed"]',{timeout:12000}).catch(()=>{});await p.waitForTimeout(2000);
 const f=await p.$('div[role="feed"]');if(f){await f.evaluate(e=>e.scrollBy(0,2000));await p.waitForTimeout(1500)}
 if(/bất thường|unusual traffic/.test(await p.content())){bl=true;console.log('BLOCKED');break}
 links[q]=await p.$$eval('a.hfpxzc',as=>as.map(a=>({name:a.getAttribute('aria-label'),href:a.href})));}catch(e){links[q]=[]}
 fs.writeFileSync(LK,JSON.stringify(links,null,1));process.stdout.write('q')}}));
// 2) details
const hrefs=[...new Map(Object.values(links).flatMap(l=>l.slice(0,PER)).map(x=>[x.href.split('?')[0],x])).values()].filter(x=>!places[x.href.split('?')[0]]);
console.log('\nplaces todo',hrefs.length);let k=0;
await Promise.all(pages.map(async p=>{while(k<hrefs.length&&!bl){const x=hrefs[k++];const key=x.href.split('?')[0];try{await p.goto(x.href+(x.href.includes('?')?'&':'?')+'hl=vi',{waitUntil:'domcontentloaded',timeout:30000});
 await p.waitForSelector('h1.DUwDvf',{timeout:12000}).catch(()=>{});await p.waitForTimeout(2200);
 if(/\/sorry\//.test(p.url())){bl=true;console.log('RATE-LIMITED');break}
 const r=await p.evaluate(()=>{const a=s=>{const e=document.querySelector(s);return e?(e.getAttribute('aria-label')||e.textContent).trim():null};const L=[...document.querySelectorAll('[aria-label]')].map(e=>e.getAttribute('aria-label'));
  const main=(document.querySelector('div[role="main"]')||document.body).innerText;const rm=main.match(/^(\d[,.]\d)\n?\s*\(([\d.,]+)\)/m);
  const hero=document.querySelector('button[jsaction*="heroHeaderImage"] img, .RZ66Rb img');
  return {name:a('h1.DUwDvf'),address:a('button[data-item-id="address"]'),category:a('button[jsaction*="category"]'),rating:rm?rm[1]:((L.find(l=>/^\d,\d sao/.test(l))||'').match(/\d,\d/)||[null])[0],reviews:rm?rm[2]:null,
   price:L.find(l=>/^Giá/.test(l))||null,pl:main.split('\n').filter(l=>/₫/.test(l)).slice(0,3),hours:L.find(l=>/Thứ (Hai|Ba|Tư)|Chủ Nhật/.test(l)&&/:/.test(l)&&l.length>30)||null,
   website:(document.querySelector('a[data-item-id="authority"]')||{}).href||null,perm_closed:/Đóng cửa vĩnh viễn/.test(main),temp_closed:/Tạm thời đóng cửa/.test(main.slice(0,800)),
   photo:hero?hero.src:null,url:location.href}});
 const m=r.url.match(/!3d(-?[\d.]+)!4d(-?[\d.]+)/);r.lat=m?+m[1]:null;r.lng=m?+m[2]:null;r.href=x.href;places[key]=r}catch(e){places[key]={error:String(e).slice(0,100),href:x.href}}
 fs.writeFileSync(PL,JSON.stringify(places,null,1));process.stdout.write('.');await p.waitForTimeout(+(process.env.GAP||4000))}}));
await b.close();console.log('\ndone',Object.keys(places).length)})();
