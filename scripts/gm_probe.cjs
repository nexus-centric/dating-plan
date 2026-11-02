const {chromium}=require('/var/tmp/sand-playwright-runtime/164c91ebeb1a9d84bdfd8b8aa7480625/node_modules/playwright-core');
(async()=>{const b=await chromium.launch({executablePath:process.env.HOME+'/.cache/ms-playwright/chromium-1248/chrome-linux64/chrome'}).catch(async e=>{console.log(e.message.slice(0,200));return chromium.launch()});
const p=await b.newPage({locale:'vi-VN'});
await p.goto('https://www.google.com/maps?cid=1290325520960581584&hl=vi',{waitUntil:'domcontentloaded'});
await p.waitForTimeout(5000);
console.log(p.url());
const t=await p.evaluate(()=>{const q=s=>[...document.querySelectorAll(s)].map(e=>e.getAttribute('aria-label')||e.textContent).slice(0,5);return {h1:q('h1'),addr:q('button[data-item-id="address"]'),hours:q('[aria-label*="Giờ"],[data-item-id*="oh"]'),cat:q('button[jsaction*="category"]')}});
console.log(JSON.stringify(t));await b.close()})();
