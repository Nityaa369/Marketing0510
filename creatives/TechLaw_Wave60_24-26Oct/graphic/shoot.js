// Screenshots every html/<name>.html listed in html/jobs_<camp>.json to out/<name>.jpg.
// Run: NODE_PATH=$(npm root -g) node shoot.js c1
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const camp = process.argv[2], dir = __dirname;
  const jobs = JSON.parse(fs.readFileSync(path.join(dir, 'html', `jobs_${camp}.json`)));
  fs.mkdirSync(path.join(dir, 'out'), { recursive: true });
  const b = await chromium.launch();
  for (const j of jobs) {
    const p = await b.newPage({ viewport: { width: j.w, height: j.h } });
    await p.goto('file://' + path.join(dir, 'html', j.name + '.html'));
    await p.evaluate(() => document.fonts.ready);
    await p.waitForTimeout(150);
    await p.screenshot({ path: path.join(dir, 'out', j.name + '.jpg'), type: 'jpeg', quality: 90 });
    await p.close();
  }
  await b.close();
  console.log('shot', jobs.length);
})();
