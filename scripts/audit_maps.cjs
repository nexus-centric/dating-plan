// Audit pass 2: open each visible place's maps_url in headless Chromium, record resolved name/address/status/category.
// Resumable: cache tmp/audit_maps.json; BATCH env (default 40) places per run. Playwright from /tmp/pw.
const fs=require('fs');const {chromium}=require('/tmp/pw/node_modules/playwright');
const ROOT='/workspace/date-app',OUT=ROOT+'/tmp/audit_maps.json';
const d=JSON.parse(fs.readFileSync(ROOT+'/src/data.json'));const cache=fs.existsSync(OUT)?JSON.parse(fs.readFileSync(OUT)):{};
const todo=d.map((x,i)=>[i,x]).filter(([i,x])=>!['closed','hidden'].includes(x.status)&&x.type!=='idea'&&!x.out_of_area&&x.maps_url&&!cache[i]).slice(0,+(process.env.BATCH||40));
console.log('todo',todo.length);
(async()=>{const b=await chromium.launch();const ctx=await b.newContext({locale:'vi-VN'});
async function one(p,url){try{const resp=await p.goto(url.replace(/&hl=\w+/,'')+(url.includes('?')?'&':'?')+'hl=vi',{waitUntil:'domcontentloaded',timeout:30000});
 await p.waitForSelector('h1',{timeout:12000}).catch(()=>{});await p.waitForTimeout(2000);
 // search URL may show a result list: click first result
 if(!(await p.$('h1.DUwDvf'))){const a=await p.$('a.hfpxzc');if(a){await a.click();await p.waitForSelector('h1.DUwDvf',{timeout:10000}).catch(()=>{});await p.waitForTimeout(1500);}}
 return await p.evaluate(s=>{const a=q=>{const e=document.querySelector(q);return e?(e.getAttribute('aria-label')||e.textContent).trim():null};const main=(document.querySelector('div[role="main"]')||document.body).innerText;
  return {status:s,name:a('h1.DUwDvf')||a('h1'),address:a('button[data-item-id="address"]'),category:a('button[jsaction*="category"]'),perm_closed:/Đóng cửa vĩnh viễn|Permanently closed/.test(main),temp_closed:/Tạm thời đóng cửa|Temporarily closed/.test(main),moved:/Đã chuyển đến|Moved to/.test(main),url:location.href,blocked:/lưu lượng truy cập bất thường|unusual traffic/.test(document.body.innerText)}},resp?resp.status():0)}catch(e){return {error:String(e).slice(0,150)}}}
const pages=await Promise.all([0,1,2].map(()=>ctx.newPage()));let k=0,blocked=false;
await Promise.all(pages.map(async p=>{while(k<todo.length&&!blocked){const [i,x]=todo[k++];const r=await one(p,x.maps_url);if(r.blocked){blocked=true;console.log('BLOCKED');break}cache[i]={...r,data_name:x.name};fs.writeFileSync(OUT,JSON.stringify(cache,null,1));process.stdout.write('.')}}));
await b.close();console.log('\ncached',Object.keys(cache).length)})();
