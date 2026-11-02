// b13: verify candidate places on live Google Maps (search "name address" -> place page). Resumable cache data/b13/verify.json
// node scripts/gm_verify.cjs data/b13/verify_todo.json   (array of {key,q})
const fs=require('fs');const {chromium}=require('/tmp/pw/node_modules/playwright');
const OUT='/workspace/date-app/data/b13/verify.json';const cache=fs.existsSync(OUT)?JSON.parse(fs.readFileSync(OUT)):{};
const todo=JSON.parse(fs.readFileSync(process.argv[2])).filter(t=>!cache[t.key]);console.log('todo',todo.length);
(async()=>{const b=await chromium.launch();const p=await (await b.newContext({locale:'vi-VN',viewport:{width:1280,height:900}})).newPage();
for(const t of todo){try{await p.goto('https://www.google.com/maps/search/'+encodeURIComponent(t.q)+'?hl=vi',{waitUntil:'domcontentloaded',timeout:30000});
 if(/\/sorry\//.test(p.url())){console.log('RATE-LIMITED');break}
 await p.waitForSelector('h1.DUwDvf, a.hfpxzc',{timeout:12000}).catch(()=>{});await p.waitForTimeout(1500);
 if(!(await p.$('h1.DUwDvf'))){const a=await p.$('a.hfpxzc');if(a){await a.click();await p.waitForSelector('h1.DUwDvf',{timeout:10000}).catch(()=>{});await p.waitForTimeout(1500)}}
 const r=await p.evaluate(()=>{const a=s=>{const e=document.querySelector(s);return e?(e.getAttribute('aria-label')||e.textContent).trim():null};const L=[...document.querySelectorAll('[aria-label]')].map(e=>e.getAttribute('aria-label'));const main=(document.querySelector('div[role="main"]')||document.body).innerText;
  return {name:a('h1.DUwDvf'),address:a('button[data-item-id="address"]'),category:a('button[jsaction*="category"]'),rating:((L.find(l=>/^\d,\d sao/.test(l))||'').match(/\d,\d/)||[null])[0],
  perm_closed:/Đóng cửa vĩnh viễn/.test(main),temp_closed:/Tạm thời đóng cửa/.test(main.slice(0,800)),url:location.href}});
 const m=r.url.match(/!3d(-?[\d.]+)!4d(-?[\d.]+)/);r.lat=m?+m[1]:null;r.lng=m?+m[2]:null;cache[t.key]=r}catch(e){cache[t.key]={error:String(e).slice(0,100)}}
 fs.writeFileSync(OUT,JSON.stringify(cache,null,1));process.stdout.write('.');await p.waitForTimeout(+(process.env.GAP||5000))}
await b.close();console.log('\ncached',Object.keys(cache).length)})();
