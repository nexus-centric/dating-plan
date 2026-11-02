// Grab hero photo URL from public Google Maps for items without image. Usage: node scripts/gm_photo.cjs <fromIdx> <outResult.json>
const fs=require('fs');
const {chromium}=require('/var/tmp/sand-playwright-runtime/164c91ebeb1a9d84bdfd8b8aa7480625/node_modules/playwright-core');
const d=JSON.parse(fs.readFileSync('/workspace/date-app/src/data.json'));const from=+process.argv[2];const OUT=process.argv[3];
const todo=d.map((x,i)=>({x,i})).filter(({x,i})=>i>=from&&!x.image&&x.type!=='idea');console.log('todo',todo.length);
(async()=>{const b=await chromium.launch({executablePath:process.env.HOME+'/.cache/ms-playwright/chromium-1248/chrome-linux64/chrome'});
const ctx=await b.newContext({locale:'vi-VN',viewport:{width:1200,height:900}});const res=[];
const pages=await Promise.all([...Array(3)].map(()=>ctx.newPage()));let k=0;
await Promise.all(pages.map(async p=>{while(k<todo.length){const {x,i}=todo[k++];
 const url=x.maps_url||('https://www.google.com/maps/search/'+encodeURIComponent(x.name+' '+(x.address||x.area||'')));
 try{await p.goto(url+(url.includes('?')?'&':'?')+'hl=vi',{waitUntil:'domcontentloaded',timeout:30000});await p.waitForTimeout(3000);
  const feed=await p.$('div[role="feed"] a[href*="/maps/place/"]');if(feed){await feed.click();await p.waitForTimeout(3500)}
  for(let j=0;j<10&&!(await p.$('button img[src*="googleusercontent"]'));j++)await p.waitForTimeout(500);
  const r=await p.evaluate(()=>{const im=[...document.querySelectorAll('button img[src*="googleusercontent"]')].map(e=>e.src).find(s=>/lh[35]\.googleusercontent/.test(s));
   return {h1:(document.querySelector('h1')||{}).textContent||null,img:im||null,url:location.href,blocked:/bất thường/.test(document.body.innerText)}});
  if(r.blocked){console.log('blocked');process.exit(2)}
  res.push({idx:i,name:x.name,status:r.img?'ok':'no_photo',image_url:r.img,contributor:null,place_url:x.maps_kind==='direct'?x.maps_url:r.url,note:'maps h1: '+r.h1})
 }catch(e){res.push({idx:i,name:x.name,status:'error',image_url:null,contributor:null,place_url:url,note:String(e).slice(0,100)})}
 fs.writeFileSync(OUT,JSON.stringify(res,null,1));process.stdout.write('.')}}));
await b.close();console.log('done')})();
