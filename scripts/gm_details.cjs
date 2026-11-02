// Fetch public Google Maps place pages (by cid from Bliss Home lists) -> address/hours/status/rating. Low volume, 3 tabs.
const fs=require('fs');
const {chromium}=require('/var/tmp/sand-playwright-runtime/164c91ebeb1a9d84bdfd8b8aa7480625/node_modules/playwright-core');
const D='/workspace/date-app/data/raw_bliss/';const OUT=D+'_gm_details.json';
const cache=fs.existsSync(OUT)?JSON.parse(fs.readFileSync(OUT)):{};
const cids=process.env.ORDER?JSON.parse(fs.readFileSync(process.env.ORDER)).filter(c=>!cache[c]):[...new Set(fs.readdirSync(D).filter(f=>f.endsWith('date.json')).flatMap(f=>JSON.parse(fs.readFileSync(D+f)).map(p=>p.cid)).filter(Boolean))].filter(c=>!cache[c]||cache[c].error);
console.log('todo',cids.length);
(async()=>{const b=await chromium.launch({executablePath:process.env.HOME+'/.cache/ms-playwright/chromium-1248/chrome-linux64/chrome'});
const ctx=await b.newContext({locale:'vi-VN'});
async function one(p,cid){
  try{await p.goto(`https://www.google.com/maps?cid=${cid}&hl=vi`,{waitUntil:'domcontentloaded',timeout:30000});
  await p.waitForSelector('h1',{timeout:15000}).catch(()=>{});await p.waitForTimeout(2500);
  const r=await p.evaluate(()=>{const a=s=>{const e=document.querySelector(s);return e?(e.getAttribute('aria-label')||e.textContent).trim():null};
    const hrs=[...document.querySelectorAll('[aria-label]')].map(e=>e.getAttribute('aria-label')).find(l=>/Thứ (Hai|Ba|Tư)|Chủ Nhật/.test(l)&&/giờ|Mở cửa|Đóng cửa|:/.test(l)&&l.length>30)||null;
    const body=document.body.innerText;const main=(document.querySelector('div[role="main"]')||document.body).innerText;
    const rm=main.match(/^(\d[,.]\d)\n?\s*\(([\d.,]+)\)/m);
    return {name:a('h1'),address:a('button[data-item-id="address"]'),hours:hrs,category:a('button[jsaction*="category"]'),website:(document.querySelector('a[data-item-id="authority"]')||{}).href||null,
      perm_closed:/Đóng cửa vĩnh viễn/.test(main),temp_closed:/Tạm thời đóng cửa/.test(main),rating:rm?rm[1]:null,reviews:rm?rm[2]:null,url:location.href,price:a('[aria-label^="Giá"]'),head:main.slice(0,300)}});
  return r}catch(e){return {error:String(e).slice(0,200)}}}
const N=+(process.env.TABS||3),GAP=+(process.env.GAP_MS||0);const pages=await Promise.all([...Array(N)].map(()=>ctx.newPage()));let i=0,blocked=false;
await Promise.all(pages.map(async p=>{while(i<cids.length&&!blocked){const c=cids[i++];const r=await one(p,c);if(/lưu lượng truy cập bất thường/.test(r.head||'')){blocked=true;console.log('\nrate-limited by Google, stopping');break}cache[c]=r;await p.waitForTimeout(GAP);fs.writeFileSync(OUT,JSON.stringify(cache,null,1));process.stdout.write('.');}}));
await b.close();console.log('\ndone',Object.keys(cache).length)})();
