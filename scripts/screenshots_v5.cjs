// v5 screenshots. Usage: node scripts/screenshots_v5.cjs [baseUrl]
const {chromium}=require('/var/tmp/sand-playwright-runtime/164c91ebeb1a9d84bdfd8b8aa7480625/node_modules/playwright-core');
const fs=require('fs');const URL=process.argv[2]||'http://localhost:4173/';const OUT='/workspace/date-app/screenshots/v5/';fs.mkdirSync(OUT,{recursive:true})
const IMG='/workspace/date-app/public/images/'+fs.readdirSync('/workspace/date-app/public/images').find(f=>/\.(jpe?g|png|webp)$/i.test(f))
const VP={mobile:{width:390,height:844},desktop:{width:1280,height:800}};
(async()=>{const b=await chromium.launch({executablePath:process.env.HOME+'/.cache/ms-playwright/chromium-1248/chrome-linux64/chrome'});
for(const [name,vp] of Object.entries(VP)){
  const ctx=await b.newContext({viewport:vp,deviceScaleFactor:name==='mobile'?2:1,locale:'vi-VN',serviceWorkers:'block',permissions:['clipboard-read','clipboard-write']});const p=await ctx.newPage();
  await p.addInitScript(()=>{try{delete Navigator.prototype.share}catch{};navigator.share=undefined})
  const shot=async n=>{await p.waitForTimeout(500);await p.screenshot({path:OUT+`${name}-${n}.png`});console.log(name,n)}
  const tab=async l=>{const sel=name==='mobile'?`nav.fixed button:has-text("${l}")`:`header button:has-text("${l}")`;await p.click(sel);await p.waitForTimeout(500)};
  const scrollTo=async sel=>{await p.evaluate(s=>{const e=document.querySelector(s);if(e)window.scrollTo(0,e.getBoundingClientRect().top+window.scrollY-70)},sel);await p.waitForTimeout(300)}
  const form=p.locator('section.card').first()
  const chip=t=>form.locator(`button.chip:has-text("${t}")`).first()
  await p.goto(URL,{waitUntil:'networkidle'});await p.waitForTimeout(600);
  await shot('1-planner-form')
  // 200k results
  await chip('200k').click();await chip('Ăn + Cafe').click();await p.click('button:has-text("Lên kèo hẹn hò")');await p.waitForTimeout(900)
  await scrollTo('#results');await shot('2-results-200k')
  await chip('Ăn + Photobooth').click();await p.click('button:has-text("Lên kèo hẹn hò")');await p.waitForTimeout(900)
  await scrollTo('#results');await shot('2b-results-200k-photobooth')
  // fine dining at 300k → budget hint
  await chip('300k').click();await chip('Fine dining').click();await p.click('button:has-text("Lên kèo hẹn hò")');await p.waitForTimeout(1200)
  await scrollTo('#results');await shot('3-finedining-300k-hint')
  // 3-stop
  await chip('500k').click();await chip('Ăn + Photobooth').click();await form.locator('input[type=checkbox]').check();await chip('T7').click()
  await p.click('button:has-text("Lên kèo hẹn hò")');await p.waitForTimeout(1500);await scrollTo('#results');await shot('4-three-stop-plan')
  await form.locator('input[type=checkbox]').uncheck()
  // empty state Quận 5
  await chip('Ăn + Cafe').click();await chip('Quận 5').click();await scrollTo('#results');
  await p.click('button:has-text("Lên kèo hẹn hò")');await p.waitForTimeout(900);await scrollTo('#results');await shot('5-empty-quan5')
  await p.click('button:has-text("Mở rộng sang quận lân cận")');await p.waitForTimeout(900);await scrollTo('#results');await shot('5b-empty-expanded')
  // share + save
  await p.locator('button:has-text("Chia sẻ")').first().click();await p.waitForTimeout(300);await shot('6-share-copied')
  const txt=await p.evaluate(()=>navigator.clipboard.readText());fs.writeFileSync(OUT+`${name}-share-text.txt`,txt)
  await p.locator('button:has-text("Lưu kèo")').first().click();await p.locator('button:has-text("Lưu kèo")').first().click()
  // open shared link
  const link=txt.match(/https?:\/\/\S+#plan\S+/)[0];const p2=await ctx.newPage();await p2.goto(link,{waitUntil:'networkidle'});await p2.waitForTimeout(800);await p2.screenshot({path:OUT+`${name}-7-shared-link.png`});await p2.close()
  // diary
  await tab('Nhật ký');await shot('8-diary')
  await p.locator('button:has-text("Đánh dấu đã đi")').first().click();await p.locator('textarea').first().fill('Ăn no rồi đi cafe, mưa nhẹ mà vui ghê 💕')
  await p.locator('input[type=file]').first().setInputFiles(IMG);await p.waitForTimeout(1500);await shot('8b-diary-done-photo')
  // reload persists?
  await p.reload({waitUntil:'networkidle'});await tab('Nhật ký');await p.waitForTimeout(800);await shot('8c-diary-after-reload')
  // at home
  await tab('Tại nhà');await p.locator('button.chip:has-text("#chill")').click();await p.click('button:has-text("Gợi ý ngẫu nhiên")');await shot('9-tai-nha-filters')
  await ctx.close()}
await b.close();console.log('ok')})();
