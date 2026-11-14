// Fingerprint de regressao visual (3 idiomas). Uso:
//   node baselines/tools/run.js --all            regrava os baselines (108 compactos + PT completo)
//   node baselines/tools/run.js --check          captura e compara com os baselines gravados (exit 1 se divergir)
//   node baselines/tools/run.js --check --lang es --page crm
// Requer Playwright + Chromium (CHROME=/caminho opcional) e rede (Google Fonts; o JSON grava "fonts").
const fs = require('fs'), path = require('path'), zlib = require('zlib');
const { chromium } = require('playwright');
const ROOT = path.resolve(__dirname, '..', '..'), OUT = path.resolve(__dirname, '..');
const arg = (k) => { const i = process.argv.indexOf('--' + k); return i > 0 ? process.argv[i + 1] : null; };
const has = (k) => process.argv.includes('--' + k);
const LANGS = ['en', 'pt', 'es'];
const PAGES = {
  home: 'index.html', overview: 'plataforma/index.html', crm: 'plataforma/crm/index.html',
  educacao: 'plataforma/educacao/index.html', marketing: 'plataforma/marketing/index.html',
  finance: 'plataforma/finance/index.html', hr: 'plataforma/hr/index.html', ai: 'plataforma/ai/index.html',
  integracoes: 'plataforma/integracoes/index.html', contato: 'contato/index.html', obrigado: 'contato/obrigado.html',
  solucoes: 'solucoes/index.html', porsetor: 'solucoes/por-setor/index.html', porfuncao: 'solucoes/por-funcao/index.html',
  porobjetivo: 'solucoes/por-objetivo/index.html', porporte: 'solucoes/por-porte/index.html',
  consultoria: 'consultoria/index.html', sobre: 'sobre/index.html', clientes: 'clientes/index.html',
};
const VPS = [[1280, 800], [375, 812]];
const PROPS = ['display','position','width','height','margin-top','margin-right','margin-bottom','margin-left','padding-top','padding-right','padding-bottom','padding-left','font-family','font-size','font-weight','line-height','letter-spacing','color','background-color','border-top-width','border-bottom-width','border-radius','opacity','transform','z-index','overflow','text-align','grid-template-columns'];

// roda dentro da pagina: mesma logica do harness antigo (28 props + geometria, animacoes off, .reveal forcado)
function capture(PROPS) {
  function fnv1a(s) { let h = 0x811c9dc5; for (let i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 0x01000193) >>> 0; } return h.toString(16).padStart(8, '0'); }
  const st = document.createElement('style');
  st.textContent = '*,*::before,*::after{animation:none!important;transition:none!important;animation-duration:0s!important}';
  document.head.appendChild(st);
  document.querySelectorAll('.reveal,.reveal-stagger').forEach(e => e.classList.add('in'));
  document.documentElement.offsetHeight;
  const rows = [];
  for (const el of document.querySelectorAll('*')) {
    const r = el.getBoundingClientRect(), cs = getComputedStyle(el), s = {};
    for (const p of PROPS) s[p] = cs.getPropertyValue(p);
    rows.push({ t: el.tagName.toLowerCase(), c: (el.getAttribute('class') || '').trim().replace(/\s+/g, ' '), i: el.id || '',
      g: [Math.round(r.x), Math.round(r.y), Math.round(r.width), Math.round(r.height)], s });
  }
  const ser = rows.map(r => r.t + '|' + r.c + '|' + r.i + '|' + r.g.join(',') + '|' + PROPS.map(p => r.s[p]).join('~')).join('\n');
  const de = document.documentElement;
  return { document: de.scrollWidth + 'x' + de.scrollHeight, overflowX: de.scrollWidth > innerWidth,
    fontsLoaded: document.fonts.status, count: rows.length, fingerprint: rows.length + ':' + fnv1a(ser), props: PROPS, elements: rows };
}

(async () => {
  if (!has('all') && !has('check')) { console.error('use --all ou --check'); process.exit(2); }
  const langs = arg('lang') ? [arg('lang')] : LANGS, pages = arg('page') ? [arg('page')] : Object.keys(PAGES);
  const browser = await chromium.launch(process.env.CHROME ? { executablePath: process.env.CHROME } : {});
  let bad = 0, n = 0, overflow = 0;
  for (const lang of langs) for (const name of pages) for (const [w, h] of VPS) {
    const tag = `${lang}/${name}-${w}`, f = path.join(OUT, lang, `${name}-${w}.json`);
    const once = async () => {
      const ctx = await browser.newContext({ viewport: { width: w, height: h } }), page = await ctx.newPage();
      await page.goto('file://' + path.join(ROOT, lang, PAGES[name]), { waitUntil: 'load' });
      await page.evaluate(() => document.fonts.ready); await page.waitForTimeout(1200);
      const r = await page.evaluate(capture, PROPS); await ctx.close(); return r;
    };
    // ~4% das capturas saem com hash diferente e mesma altura (jitter de layout sob carga, nao reproduzivel):
    // --check aceita se ALGUMA de ate 3 tentativas bater; --all so grava quando 2 capturas seguidas concordam.
    let old = null; try { old = JSON.parse(fs.readFileSync(f, 'utf8')); } catch (e) {}
    let d = await once(); n++;
    if (has('check')) { for (let t = 0; t < 2 && old && d.fingerprint !== old.fp; t++) d = await once(); }
    else { for (let t = 0; t < 4; t++) { const d2 = await once(); if (d2.fingerprint === d.fingerprint) break; d = d2; } }
    const compact = { fp: d.fingerprint, doc: d.document, fonts: d.fontsLoaded };
    if (d.fontsLoaded !== 'loaded') console.warn('AVISO fontes nao carregaram:', tag);
    if (d.overflowX) { overflow++; console.warn('OVERFLOW horizontal:', tag); }
    if (has('check')) {
      if (!old || old.fp !== compact.fp || old.doc !== compact.doc) { bad++; console.log('DIFERE', tag, old ? old.fp + ' ' + old.doc : '(sem baseline)', '->', compact.fp, compact.doc); }
    } else {
      fs.mkdirSync(path.dirname(f), { recursive: true });
      fs.writeFileSync(f, JSON.stringify(compact) + '\n');
      if (lang === 'pt') {   // backup forense completo, so do PT (gzip: o JSON cru passa de 700 KB por captura)
        fs.mkdirSync(path.join(OUT, 'pt-full'), { recursive: true });
        fs.writeFileSync(path.join(OUT, 'pt-full', `${name}-${w}.json.gz`), zlib.gzipSync(JSON.stringify({ page: PAGES[name], viewport: `${w}x${h}`, ...d, overflowX: undefined }, null, 1)));
      }
    }
    process.stdout.write('.');
  }
  await browser.close();
  console.log(`\n${n} capturas | ${has('check') ? bad + ' divergencias' : 'gravadas'} | overflow horizontal: ${overflow}`);
  process.exit(bad || overflow ? 1 : 0);
})();
