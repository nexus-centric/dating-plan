// Local preview screenshots (headless Chromium). Usage: node scripts/screenshots.cjs [baseUrl]
const {chromium}=require('/var/tmp/sand-playwright-runtime/164c91ebeb1a9d84bdfd8b8aa7480625/node_modules/playwright-core');
const URL=process.argv[2]||'http://localhost:4173/';const OUT='/workspace/date-app/screenshots/';
const VP={mobile:{width:390,height:844},desktop:{width:1280,height:800}};
(async()=>{const b=await chromium.launch({executablePath:process.env.HOME+'/.cache/ms-playwright/chromium-1248/chrome-linux64/chrome'});
for(const [name,vp] of Object.entries(VP)){
  const ctx=await b.newContext({viewport:vp,deviceScaleFactor:name==='mobile'?2:1,locale:'vi-VN',serviceWorkers:'block'});const p=await ctx.newPage();
  const tab=async l=>{const sel=name==='mobile'?`nav.fixed button:has-text("${l}")`:`header button:has-text("${l}")`;await p.click(sel);await p.waitForTimeout(500)};
  await p.goto(URL,{waitUntil:'networkidle'});await p.waitForTimeout(600);
  await p.screenshot({path:OUT+`${name}-planner-form.png`});
  await p.click('button:has-text("Ăn + Photobooth")');await p.click('button:has-text("500k")');
  await p.click('button:has-text("Lên kèo hẹn hò")');await p.waitForTimeout(900);
  const toPlans=async()=>{await p.evaluate(()=>{const h=[...document.querySelectorAll('h3')].find(e=>e.textContent.includes('Kế hoạch 1'));const y=h.getBoundingClientRect().top+window.scrollY-(window.innerWidth<640?70:80);window.scrollTo(0,y)});await p.waitForTimeout(400)};
  await toPlans();
  await p.screenshot({path:OUT+`${name}-plans-photobooth.png`});
  await p.click('button:has-text("Ăn + Cafe")');await p.click('button:has-text("Lên kèo hẹn hò")');await p.waitForTimeout(900);
  await toPlans();
  await p.screenshot({path:OUT+`${name}-plans.png`});
  await tab('Khám phá');await p.screenshot({path:OUT+`${name}-browse.png`});
  await p.selectOption('select','Fine Dining date');await p.waitForTimeout(800);await p.evaluate(()=>{const g=document.querySelector('.grid.gap-4');window.scrollTo(0,g.getBoundingClientRect().top+window.scrollY-70)});await p.waitForTimeout(800);await p.screenshot({path:OUT+`${name}-browse-photos.png`});
  await tab('Tại nhà');await p.screenshot({path:OUT+`${name}-ideas.png`});
  await ctx.close()}
await b.close();console.log('ok')})();
