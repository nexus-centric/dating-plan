// v7 screenshots. Usage: node scripts/screenshots_v7.cjs [baseUrl]
const {chromium}=require('/var/tmp/sand-playwright-runtime/164c91ebeb1a9d84bdfd8b8aa7480625/node_modules/playwright-core');
const fs=require('fs');const URL=process.argv[2]||'http://localhost:4173/';const OUT='/workspace/date-app/screenshots/v7/';fs.mkdirSync(OUT,{recursive:true})
const VP={mobile:{width:390,height:844},desktop:{width:1280,height:800}};
(async()=>{const b=await chromium.launch({executablePath:process.env.HOME+'/.cache/ms-playwright/chromium-1248/chrome-linux64/chrome'});
for(const [name,vp] of Object.entries(VP)){
  const ctx=await b.newContext({viewport:vp,deviceScaleFactor:name==='mobile'?2:1,locale:'vi-VN',serviceWorkers:'block'});const p=await ctx.newPage();
  const shot=async n=>{await p.waitForTimeout(800);await p.screenshot({path:OUT+`${name}-${n}.png`});console.log(name,n)}
  const scrollTo=async sel=>{await p.evaluate(s=>{const e=document.querySelector(s);if(e)window.scrollTo(0,e.getBoundingClientRect().top+window.scrollY-70)},sel);await p.waitForTimeout(300)}
  const form=p.locator('section.card').first();const chip=t=>form.locator(`button.chip:has-text("${t}")`).first()
  const go=async n=>{await p.click('button:has-text("Lên kèo hẹn hò")');await p.waitForTimeout(1800);await scrollTo('#results');await shot(n)}
  await p.goto(URL,{waitUntil:'networkidle'});await p.waitForTimeout(600)
  await chip('200–300k').click();await chip('Cafe thú cưng').click();await go('1-plan-petcafe-200-300k')
  await chip('600–700k').click();await chip('Kịch / Nhạc sống').click();await go('2-plan-kich-nhacsong-600-700k')
  await chip('400–500k').click();await chip('Kịch / Nhạc sống').click();await go('2b-plan-kich-nhacsong-400-500k')
  await p.locator(`button:has-text("Khám phá"):visible`).first().click();await p.waitForTimeout(1500);await p.evaluate(()=>window.scrollTo(0,0));await shot('3-kham-pha-grid')
  const sel=p.locator('select:visible').first();const opts=await sel.locator('option').allTextContents()
  for(const [kw,n] of [['thú cưng','3b-kham-pha-thu-cung'],['kịch','3c-kham-pha-kich'],['bình dân','3d-kham-pha-moi']]){const o=opts.find(t=>t.toLowerCase().includes(kw));if(o){await sel.selectOption({label:o});await p.waitForTimeout(800);await p.evaluate(()=>window.scrollTo(0,250));await shot(n)}}
  await ctx.close()}
await b.close();console.log('ok')})();
