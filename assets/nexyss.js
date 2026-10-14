/* ============================================================
   NEXYSS — Comportamento compartilhado
   Header scroll · Reveal on scroll · Drawer mobile
   Carregar no fim do <body>, sem defer.
   ============================================================ */

// Header scroll state
const header = document.getElementById('siteHeader');
window.addEventListener('scroll', () => {
  if (window.scrollY > 12) header.classList.add('scrolled');
  else header.classList.remove('scrolled');
}, { passive: true });

// Reveal on scroll
const io = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      e.target.classList.add('in');
      io.unobserve(e.target);
    }
  });
}, { threshold: 0.12, rootMargin: '0px 0px -60px 0px' });
document.querySelectorAll('.reveal, .reveal-stagger').forEach(el => io.observe(el));
// ============ MOBILE DRAWER ============
(function () {
  const drawer   = document.getElementById('mobileDrawer');
  const overlay  = document.getElementById('drawerOverlay');
  const toggle   = document.getElementById('navToggle');
  const closeBtn = document.getElementById('drawerClose');
  if (!drawer || !overlay || !toggle) return;

  const FOCUSABLE = 'a[href], button:not([disabled])';
  let lastFocus = null;

  function isOpen() { return drawer.classList.contains('open'); }

  function openDrawer() {
    lastFocus = document.activeElement;
    overlay.hidden = false;
    requestAnimationFrame(() => overlay.classList.add('in'));
    drawer.classList.add('open');
    drawer.setAttribute('aria-hidden', 'false');
    toggle.classList.add('open');
    toggle.setAttribute('aria-expanded', 'true');
    document.body.classList.add('drawer-open');
    closeBtn.focus();
  }

  function closeDrawer() {
    overlay.classList.remove('in');
    setTimeout(() => { if (!isOpen()) overlay.hidden = true; }, 300);
    drawer.classList.remove('open');
    drawer.setAttribute('aria-hidden', 'true');
    toggle.classList.remove('open');
    toggle.setAttribute('aria-expanded', 'false');
    document.body.classList.remove('drawer-open');
    if (lastFocus) lastFocus.focus();
  }

  toggle.addEventListener('click', () => isOpen() ? closeDrawer() : openDrawer());
  closeBtn.addEventListener('click', closeDrawer);
  overlay.addEventListener('click', closeDrawer);

  // Acordeões internos
  drawer.querySelectorAll('.drawer-acc').forEach(btn => {
    btn.addEventListener('click', () => {
      const panel = document.getElementById(btn.getAttribute('aria-controls'));
      const open  = btn.getAttribute('aria-expanded') === 'true';
      btn.setAttribute('aria-expanded', String(!open));
      panel.classList.toggle('open', !open);
    });
  });

  // Fecha ao navegar
  drawer.querySelectorAll('a[href]').forEach(a => {
    a.addEventListener('click', closeDrawer);
  });

  // Esc + focus trap
  document.addEventListener('keydown', (e) => {
    if (!isOpen()) return;
    if (e.key === 'Escape') { closeDrawer(); return; }
    if (e.key !== 'Tab') return;
    const items = [...drawer.querySelectorAll(FOCUSABLE)]
      .filter(el => el.offsetParent !== null);
    if (!items.length) return;
    const first = items[0], last = items[items.length - 1];
    if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
    else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
  });

  // Volta pro desktop com o drawer aberto
  window.addEventListener('resize', () => {
    if (isOpen() && window.innerWidth > 760) closeDrawer();
  }, { passive: true });
})();

// ============ SCROLLSPY DA SUBNAV ============
// Marca a ancora quando a secao cruza a linha de 40% da viewport.
//
// Por que nao "threshold: 0.4" puro: threshold mede a fracao DA SECAO que
// esta visivel. Uma secao mais alta que 2.5x a viewport nunca alcanca 40%
// visivel e a ancora nunca acenderia — o que acontece em varias secoes no
// mobile. A faixa de rootMargin abaixo reduz a viewport a uma linha fina
// posicionada a 40% do topo, entregando o mesmo comportamento pretendido
// e funcionando para secao de qualquer altura.
(function () {
  const links = document.querySelectorAll('.subnav-links a[href^="#"]');
  if (!links.length) return;

  const map = new Map();   // ordem de insercao = ordem no documento
  links.forEach(a => {
    const el = document.getElementById(a.getAttribute('href').slice(1));
    if (el) map.set(el, a);
  });
  if (!map.size) return;

  function setActive(a) {
    links.forEach(l => {
      const on = l === a;
      l.classList.toggle('active', on);
      if (on) l.setAttribute('aria-current', 'true');
      else l.removeAttribute('aria-current');
    });
  }

  const visible = new Set();
  const spy = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) visible.add(e.target);
      else visible.delete(e.target);
    });
    if (!visible.size) return;
    let last = null;
    map.forEach((_, el) => { if (visible.has(el)) last = el; });
    if (last) setActive(map.get(last));
  }, { threshold: 0, rootMargin: '-40% 0px -59% 0px' });

  map.forEach((_, el) => spy.observe(el));

  // Clique na ancora acende na hora, sem esperar o scroll terminar
  links.forEach(a => a.addEventListener('click', () => setActive(a)));
})();

// ============ CONTATO — pré-seleção via querystring + estado de erro ============
// Só roda na página que tem o formulário. Nenhum efeito nas outras.
(function () {
  const form = document.querySelector('form[name="contato"]');
  if (!form) return;

  const params    = new URLSearchParams(location.search);
  const interesse = (params.get('interesse') || '').trim().toLowerCase();
  // ?origem= identifica a CTA que gerou o lead (demo, especialista, founding).
  // Links por produto usam os dois: ?interesse=marketing&origem=demo.
  const origemCta = (params.get('origem') || '').trim().toLowerCase();

  // ?interesse= (vindo das CTAs do site) → opção do dropdown.
  // demo/founding → "Plataforma completa" · especialista → "Ainda não tenho certeza".
  // Slugs de módulo também funcionam, para links futuros por produto.
  const MAP = {
    demo: 'Plataforma completa',
    founding: 'Plataforma completa',
    especialista: 'Ainda não tenho certeza',
    plataforma: 'Plataforma completa',
    crm: 'Nexyss CRM',
    educacao: 'Nexyss Educação',
    marketing: 'Nexyss Marketing',
    finance: 'Nexyss Finance',
    hr: 'Nexyss HR',
    ai: 'Nexyss AI',
    consultoria: 'Consultoria'
  };

  const sel    = form.querySelector('select[name="interesse"]');
  const origem = form.querySelector('input[name="origem"]');
  const msg    = form.querySelector('textarea[name="mensagem"]');

  // Rastreia a CTA de origem no painel do Netlify (valor cru do parâmetro).
  // ?origem= vence; sem ele vale ?interesse= (CTAs antigas); sem nenhum, 'direto'.
  if (origem) origem.value = origemCta || interesse || 'direto';

  if (sel && MAP[interesse]) {
    const opt = [...sel.options].find(o => o.value === MAP[interesse]);
    if (opt) sel.value = opt.value;
  }

  // Founding Customers: abre a mensagem já contextualizada (editável)
  if ((interesse === 'founding' || origemCta === 'founding') && msg && !msg.value) {
    msg.value = 'Tenho interesse no programa Founding Customers.';
  }

  // Estado de erro: o evento "invalid" dispara por campo antes de o navegador
  // bloquear o envio (não borbulha — por isso o capture: true). A classe
  // liga o estilo .show-errors; a mensagem nativa do navegador continua.
  form.addEventListener('invalid', () => form.classList.add('show-errors'), true);
  form.addEventListener('input', () => {
    if (form.classList.contains('show-errors') && form.checkValidity()) {
      form.classList.remove('show-errors');
    }
  });
})();
