// Search public Google Maps for a query list -> first place details (name, address, hours, price, rating, coords, cid). Cached.
const fs=require('fs');
const {chromium}=require('/var/tmp/sand-playwright-runtime/164c91ebeb1a9d84bdfd8b8aa7480625/node_modules/playwright-core');
const OUT='/workspace/date-app/data/gm_search_v6.json';const cache=fs.existsSync(OUT)?JSON.parse(fs.readFileSync(OUT)):{};
const qs=JSON.parse(fs.readFileSync(process.argv[2])).filter(q=>!cache[q]||cache[q].error);
console.log('todo',qs.length);
(async()=>{const b=await chromium.launch({executablePath:process.env.HOME+'/.cache/ms-playwright/chromium-1248/chrome-linux64/chrome'});
const ctx=await b.newContext({locale:'vi-VN'});
async function one(p,q){try{await p.goto('https://www.google.com/maps/search/'+encodeURIComponent(q)+'?hl=vi',{waitUntil:'domcontentloaded',timeout:30000});
 await p.waitForSelector('h1',{timeout:12000}).catch(()=>{});await p.waitForTimeout(2500);for(let k=0;k<16&&!/\/place\//.test(p.url());k++)await p.waitForTimeout(500);await p.waitForTimeout(1500);
 const feed=await p.$('div[role="feed"] a[href*="/maps/place/"]');if(feed){await feed.click();await p.waitForTimeout(3500)}
 return await p.evaluate(()=>{const a=s=>{const e=document.querySelector(s);return e?(e.getAttribute('aria-label')||e.textContent).trim():null};
  const L=[...document.querySelectorAll('[aria-label]')].map(e=>e.getAttribute('aria-label'));
  const hrs=L.find(l=>/Thứ (Hai|Ba|Tư)|Chủ Nhật/.test(l)&&/:/.test(l)&&l.length>30)||null;
  const main=(document.querySelector('div[role="main"]')||document.body).innerText;const rm=main.match(/^(\d[,.]\d)\n?\s*\(([\d.,]+)\)/m);
  const price=L.find(l=>/^Giá/.test(l))||null;const rv=L.find(l=>/bài đánh giá|đánh giá$/.test(l)&&/\d/.test(l))||null;const stars=L.find(l=>/sao$/.test(l))||null;const lab=L.filter(l=>/₫|mỗi người/.test(l)).slice(0,5);const pl=main.split('\n').filter(l=>/₫/.test(l)).slice(0,4);
  return {name:a('h1'),address:a('button[data-item-id="address"]'),hours:hrs,category:a('button[jsaction*="category"]'),website:(document.querySelector('a[data-item-id="authority"]')||{}).href||null,
   perm_closed:/Đóng cửa vĩnh viễn/.test(main),temp_closed:/Tạm thời đóng cửa/.test(main),rating:rm?rm[1]:null,reviews:rm?rm[2]:null,price,pl,rv,stars,lab,main:main.slice(0,1500),url:location.href,head:main.slice(0,200)}})}catch(e){return {error:String(e).slice(0,200)}}}
const pages=await Promise.all([...Array(3)].map(()=>ctx.newPage()));let i=0,bl=false;
await Promise.all(pages.map(async p=>{while(i<qs.length&&!bl){const q=qs[i++];const r=await one(p,q);if(/bất thường/.test(r.head||'')){bl=true;console.log('blocked');break}cache[q]=r;fs.writeFileSync(OUT,JSON.stringify(cache,null,1));process.stdout.write('.')}}));
await b.close();console.log('done')})();
