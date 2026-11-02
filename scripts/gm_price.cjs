// Re-visit public Google Maps place pages (cid) to read the price range shown on the page (e.g. "₫100–200 N"). Cached/resumable.
const fs=require('fs');
const {chromium}=require('/var/tmp/sand-playwright-runtime/164c91ebeb1a9d84bdfd8b8aa7480625/node_modules/playwright-core');
const OUT='/workspace/date-app/data/gm_price.json';const cache=fs.existsSync(OUT)?JSON.parse(fs.readFileSync(OUT)):{};
const items=JSON.parse(fs.readFileSync('/workspace/date-app/src/data.json'));
const cids=[...new Set(items.map(i=>(i.maps_url||'').match(/cid=(\d+)/)).filter(Boolean).map(m=>m[1]))].filter(c=>!cache[c]||cache[c].error);
console.log('todo',cids.length);
(async()=>{const b=await chromium.launch({executablePath:process.env.HOME+'/.cache/ms-playwright/chromium-1248/chrome-linux64/chrome'});
const ctx=await b.newContext({locale:'vi-VN'});
async function one(p,cid){try{await p.goto(`https://www.google.com/maps?cid=${cid}&hl=vi`,{waitUntil:'domcontentloaded',timeout:30000});
 await p.waitForSelector('h1',{timeout:15000}).catch(()=>{});await p.waitForTimeout(3000);
 return await p.evaluate(()=>{const main=(document.querySelector('div[role="main"]')||document.body).innerText;
  const lab=[...document.querySelectorAll('[aria-label]')].map(e=>e.getAttribute('aria-label')).filter(l=>/₫|Giá|mỗi người/.test(l)).slice(0,8);
  const lines=main.split('\n').filter(l=>/₫/.test(l)).slice(0,6);
  return {name:(document.querySelector('h1')||{}).textContent||null,url:location.href,lab,lines,head:main.slice(0,400)}})}catch(e){return {error:String(e).slice(0,200)}}}
const pages=await Promise.all([...Array(3)].map(()=>ctx.newPage()));let i=0,n=0;
await Promise.all(pages.map(async p=>{while(i<cids.length){const c=cids[i++];const r=await one(p,c);if(/bất thường/.test(r.head||'')){console.log('blocked');process.exit(1)}cache[c]=r;if(++n%10==0){fs.writeFileSync(OUT,JSON.stringify(cache,null,1));console.log(n)}}}));
fs.writeFileSync(OUT,JSON.stringify(cache,null,1));await b.close();console.log('done')})();
