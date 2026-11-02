// v6 screenshots (range chips). Usage: node scripts/screenshots_v6.cjs [baseUrl]
const {chromium}=require('/var/tmp/sand-playwright-runtime/164c91ebeb1a9d84bdfd8b8aa7480625/node_modules/playwright-core');
const fs=require('fs');const URL=process.argv[2]||'http://localhost:4173/';const OUT='/workspace/date-app/screenshots/v6/';fs.mkdirSync(OUT,{recursive:true})
const VP={mobile:{width:390,height:844},desktop:{width:1280,height:800}};
(async()=>{const b=await chromium.launch({executablePath:process.env.HOME+'/.cache/ms-playwright/chromium-1248/chrome-linux64/chrome'});
for(const [name,vp] of Object.entries(VP)){
  const ctx=await b.newContext({viewport:vp,deviceScaleFactor:name==='mobile'?2:1,locale:'vi-VN',serviceWorkers:'block',permissions:['clipboard-read','clipboard-write']});const p=await ctx.newPage();
  await p.addInitScript(()=>{try{delete Navigator.prototype.share}catch{};navigator.share=undefined})
  const shot=async n=>{await p.waitForTimeout(500);await p.screenshot({path:OUT+`${name}-${n}.png`});console.log(name,n)}
  const scrollTo=async sel=>{await p.evaluate(s=>{const e=document.querySelector(s);if(e)window.scrollTo(0,e.getBoundingClientRect().top+window.scrollY-70)},sel);await p.waitForTimeout(300)}
  const form=p.locator('section.card').first();const chip=t=>form.locator(`button.chip:has-text("${t}")`).first()
  const go=async n=>{await p.click('button:has-text("Lên kèo hẹn hò")');await p.waitForTimeout(1500);await scrollTo('#results');await shot(n)}
  await p.goto(URL,{waitUntil:'networkidle'});await p.waitForTimeout(600);await scrollTo('[data-testid=ranges]');await shot('1-range-chips-form')
  await chip('200–300k').click();await chip('Ăn vặt + Dạo phố').click();await go('2-plan-200-300k-anvat')
  await chip('200–300k').click();await chip('Ăn + Cafe').click();await go('2b-plan-200-300k-cafe')
  await chip('800–900k').click();await chip('Ăn + Cafe').click();await go('3-plan-800-900k-cafe')
  await chip('600–700k').click();await chip('Ăn + Xem phim').click();await go('4-new-combo-phim-600-700k')
  await chip('400–500k').click();await chip('Vận động + Ăn').click();await go('4b-new-combo-vandong-400-500k')
  await chip('400–500k').click();await chip('Chè/kem + Dạo đêm').click();await form.locator('input[type=checkbox]').check();await go('5-three-stop-chedem')
  await chip('800–900k').click();await chip('Ăn + Karaoke').click();await go('5b-three-stop-karaoke-800-900k')
  await p.locator('button:has-text("Chia sẻ")').first().click();await p.waitForTimeout(300)
  const txt=await p.evaluate(()=>navigator.clipboard.readText());fs.writeFileSync(OUT+`${name}-share-text.txt`,txt)
  const link=txt.match(/https?:\/\/\S+#plan\S+/)[0];const p2=await ctx.newPage();await p2.goto(link,{waitUntil:'networkidle'});await p2.waitForTimeout(800);await p2.screenshot({path:OUT+`${name}-6-shared-link.png`});await p2.close()
  const old=URL+'#plan&s=31.walk.1800~28.cheapmeal.1915&c=anvat&b=300000';const p3=await ctx.newPage();await p3.goto(old,{waitUntil:'networkidle'});await p3.waitForTimeout(800);await p3.screenshot({path:OUT+`${name}-7-old-link-no-range.png`});await p3.close()
  await ctx.close()}
await b.close();console.log('ok')})();
