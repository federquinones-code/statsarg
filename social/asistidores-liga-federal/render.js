const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const page = await browser.newPage({ viewport: { width: 1200, height: 1500 }, deviceScaleFactor: 2 });
  page.on('console', m => console.log('[page]', m.text()));
  page.on('requestfailed', r => console.log('[FAIL]', r.url()));
  await page.goto('file://' + path.join(__dirname, 'slides.html'));
  await page.waitForTimeout(1200);
  for (let i = 1; i <= 7; i++) {
    const el = await page.$('#s' + i);
    if (!el) { console.log('missing slide', i); continue; }
    await el.screenshot({ path: path.join(__dirname, `slide-${i}.png`) });
    console.log('rendered slide', i);
  }
  await browser.close();
})();
