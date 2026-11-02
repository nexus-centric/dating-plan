// b14 screenshot: Explore tab searched for "chicken" (mobile). node scripts/screenshot_b14.cjs
const {chromium}=require('/tmp/pw/node_modules/playwright');const fs=require('fs');const OUT='/workspace/date-app/screenshots/b14/';fs.mkdirSync(OUT,{recursive:true});
(async()=>{const b=await chromium.launch();const ctx=await b.newContext({viewport:{width:390,height:844},deviceScaleFactor:2,locale:'vi-VN',serviceWorkers:'block'});const p=await ctx.newPage();
await p.goto('http://localhost:4173/',{waitUntil:'networkidle'});
const nav=p.locator('nav[aria-label="Điều hướng"] button');const n=await nav.count();const labels=[];for(let i=0;i<n;i++)labels.push(await nav.nth(i).innerText());console.log(labels);
await nav.filter({hasText:/Khám phá|Explore/}).first().click();await p.waitForTimeout(800);
const inp=p.locator('input[type="search"], input[placeholder]').first();await inp.fill('chicken');await p.waitForTimeout(1500);
await p.screenshot({path:OUT+'mobile-explore-chicken.png'});
await p.evaluate(()=>window.scrollBy(0,700));await p.waitForTimeout(1200);await p.screenshot({path:OUT+'mobile-explore-chicken-2.png'});await b.close()})();
