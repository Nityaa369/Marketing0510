
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1350 } });
  for (const id of process.argv.slice(2)) {
    await p.goto('file://' + __dirname + '/html/cd_art_' + id + '.html');
    await p.evaluate(() => document.fonts.ready);
    const over = await p.evaluate(() => [...document.querySelectorAll('.copy,.banner,.cta,.note')]
      .filter(e => { const r = e.getBoundingClientRect(); return r.right > 1080 || r.left < 0 || r.bottom > 1350; })
      .map(e => e.className));
    if (over.length) console.log('OVERFLOW', id, over.join(','));
    await p.screenshot({ path: __dirname + '/out/cd_art_' + id + '.png' });
  }
  await b.close();
})();
