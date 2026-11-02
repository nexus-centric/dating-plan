// overflow check: node scripts/overflow_check.cjs <tag>  -> screenshots/b14/<tag>-*.png
const {chromium}=require('/tmp/pw/node_modules/playwright');const OUT='/workspace/date-app/screenshots/b14/';const tag=process.argv[2]||'x';
(async()=>{const b=await chromium.launch();let bad=0;
for(const w of [360,390,430,1280]){const ctx=await b.newContext({viewport:{width:w,height:w>1000?800:844},deviceScaleFactor:w>1000?1:2,locale:'vi-VN',serviceWorkers:'block'});const p=await ctx.newPage();
 await p.goto('http://localhost:4173/',{waitUntil:'networkidle'});
 const chk=async name=>{const r=await p.evaluate(()=>{const de=document.documentElement;const vw=de.clientWidth;const off=[...document.querySelectorAll('body *')].filter(e=>{const b=e.getBoundingClientRect();return b.width&&b.right>vw+0.5&&getComputedStyle(e).position!=='fixed'&&!e.closest('.clouds')}).slice(0,5).map(e=>e.tagName+'.'+String(e.className).slice(0,60)+' r='+Math.round(e.getBoundingClientRect().right));return {sw:de.scrollWidth,cw:vw,off}});
  const ok=r.sw===r.cw&&!r.off.length;if(!ok)bad++;console.log(w,name,ok?'OK':'FAIL',r.sw,r.cw,r.off.join(' | '))}
 await chk('plan');await p.click('button:has-text("Lên kèo hẹn hò")');await p.waitForTimeout(1500);await chk('plan-result');
 if(w<1000) await p.locator('nav[aria-label="Điều hướng"] button',{hasText:'Khám phá'}).click(); else await p.locator('button',{hasText:'Khám phá'}).first().click();
 await p.waitForTimeout(800);await p.locator('input').first().fill('chicken');await p.waitForTimeout(1200);await chk('explore');
 await p.evaluate(()=>window.scrollBy(0,700));await p.waitForTimeout(800);await p.screenshot({path:`${OUT}${tag}-explore-${w}.png`});await ctx.close()}
await b.close();console.log('FAILS',bad)})();
