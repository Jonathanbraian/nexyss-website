const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');
// Raiz do projeto derivada da localização deste script (baselines/tools/ → ../..)
const SP = path.resolve(process.argv[2]), ROOT = path.resolve(__dirname, '..', '..');
const CHROME = process.env.CHROME || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const pages = [
  ['home', ROOT + '/index.html'],
  ['overview', ROOT + '/plataforma/index.html'],
  ['crm', ROOT + '/plataforma/crm/index.html'],
  ['educacao', ROOT + '/plataforma/educacao/index.html'],
  ['marketing', ROOT + '/plataforma/marketing/index.html'],
  ['finance', ROOT + '/plataforma/finance/index.html'],
  ['hr', ROOT + '/plataforma/hr/index.html'],
  ['contato', ROOT + '/contato/index.html'],
  ['obrigado', ROOT + '/contato/obrigado.html'],
];
const vps = [[1280, 800], [375, 812]];
function one(name, page, w, h) {
  return new Promise((res) => {
    const out = `${SP}/raw-${name}-${w}.html`;
    const fd = fs.openSync(out, 'w');
    const url = `file://${SP}/harness.html?page=file://${page}&w=${w}&h=${h}`;
    const p = spawn(CHROME, ['--headless=new','--disable-gpu','--no-sandbox','--hide-scrollbars',
      '--allow-file-access-from-files',`--user-data-dir=${SP}/profile-${name}-${w}`,
      '--virtual-time-budget=15000','--window-size=1600,1000','--dump-dom', url],
      { stdio: ['ignore', fd, 'ignore'] });
    let done = false;
    const finish = (why) => { if (done) return; done = true; try { p.kill('SIGKILL'); } catch (e) {} 
      try { fs.closeSync(fd); } catch (e) {} console.log(name, w, why); res(); };
    const iv = setInterval(() => {
      let s = ''; try { s = fs.readFileSync(out, 'utf8'); } catch (e) {}
      if (s.includes('FP_END') || s.includes('FP_ERROR')) { clearInterval(iv); finish('ok'); }
    }, 500);
    setTimeout(() => { clearInterval(iv); finish('timeout'); }, 60000);
  });
}
(async () => { for (const [n, pg] of pages) for (const [w, h] of vps) await one(n, pg, w, h); })();
