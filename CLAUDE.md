# Nexyss — Memória do Projeto

Pasta do projeto: raiz do repositório `nexyss-website` (onde está este arquivo)
Dono / interlocutor: **Jonathan**
Home aprovada: `index.html` (1956 linhas, single-file, CSS+JS inline)

---

## Sobre a Nexyss

- **O que é:** plataforma operacional global com IA. Um sistema único que unifica
  CRM, Educação, Marketing, Finance e HR, com uma camada de IA transversal
  (Nexyss AI) atravessando todos os módulos.
- **Tagline oficial:** *"Uma plataforma. Múltiplos módulos. Infinitas possibilidades."*
- **Headline da Home:** *"A plataforma operacional que pensa junto com o seu negócio."*
- **Naming:**
  - `Nexyss` → marca principal. **Sempre title case.** Nunca "NEXYSS", nunca "nexyss".
  - `Nexyss Group` → razão social. **Apenas** em rodapé/legal/copyright/termos.
    Uso atual na Home: `© 2026 Nexyss Group. Todos os direitos reservados.`
  - Módulos: `Nexyss CRM`, `Nexyss Educação`, `Nexyss Marketing`,
    `Nexyss Finance`, `Nexyss HR`, `Nexyss AI`.
  - Sub-produtos de IA: `Nexyss Insight`, `Nexyss Assist`, `Nexyss Automate`.
- **Posicionamento:** enterprise. Padrão de referência = **Salesforce, HubSpot,
  Monday.com, Pipedrive, Stripe**. Copy institucional, densidade real de
  conteúdo, hierarquia clara. Nada de tom de landing page de startup.
- **Números institucionais usados na Home** (manter consistentes entre páginas):
  120+ países suportados · 9 idiomas nativos · 99.99% uptime ·
  3.4× ciclo de vendas · 87% redução de silos · $2.1M economia de stack ·
  40+ países atendidos.

---

## Design System

> Extraído verbatim do `:root` e do CSS do `index.html`. **Copiar, não recriar.**

### Tokens de cor

```css
/* Navy scale — do brand book */
--c-navy-deep:  #0B1440;   /* fundo padrão do body, hero topo, footer, .deeper */
--c-navy:       #131E4F;   /* logo wall, .consult-item, base do .tinted */
--c-navy-mid:   #1E285F;   /* topo do gradiente .tinted, hover de consult-item */
--c-navy-light: #2A3985;
--c-navy-hi:    #3A5EAF;

/* Brand blue-violet — wordmark Nexyss */
--c-brand:       #3C50D9;
--c-brand-light: #5B6DE8;

/* Sistema de cores por produto */
--c-crm: #45E599;  --c-crm-deep: #2D9768;   /* Verde   — CRM */
--c-edu: #03DBFF;  --c-edu-deep: #019EC2;   /* Ciano   — Educação */
--c-mkt: #F25D23;  --c-mkt-deep: #C4451A;   /* Laranja — Marketing */
--c-fin: #7C8CE8;  --c-fin-deep: #3C50D9;   /* Violeta — Finance */
--c-hr:  #B84FE5;  --c-hr-deep:  #8E37B8;   /* Magenta — HR */
--c-ai:  #37A7E2;  --c-ai-deep:  #1E7CB8;   /* Azul-elétrico — AI */

/* Neutros dark (o site é dark-only) */
--c-white:      #FFFFFF;
--c-text:       rgba(255,255,255,0.92);
--c-text-soft:  rgba(255,255,255,0.72);
--c-text-mute:  rgba(255,255,255,0.52);
--c-text-faint: rgba(255,255,255,0.35);
--c-line:        rgba(255,255,255,0.08);
--c-line-mid:    rgba(255,255,255,0.14);
--c-line-strong: rgba(255,255,255,0.22);
--c-glass:       rgba(255,255,255,0.04);
--c-glass-hover: rgba(255,255,255,0.07);
--c-success: #45E599;   /* = verde CRM */
```

**Decisões de cor que não são óbvias e devem ser respeitadas:**

1. **O site é dark-only.** Não existe light mode. `body` = `--c-navy-deep`.
2. **Ciano `--c-edu` é o acento institucional global**, não só a cor de Educação.
   Ele é usado em: `.eyebrow` (todos os kickers de seção), hover de links do
   footer, `<small>` dos números de impacto, ícone default de `.sol-icon`,
   glows do hero/CTA/footer. Manter esse papel duplo — **não trocar por brand**.
3. `--c-fin-deep` é literalmente igual a `--c-brand` (#3C50D9). Intencional.
4. `--c-success` é igual ao verde CRM. Estados positivos (deltas ↑, tags "Live",
   checkmarks) usam sempre esse verde.
5. **Cor por produto é aplicada via variável local `--c-color`**, não hardcoded:
   ```css
   .mod-card.crm { --c-color: var(--c-crm); }
   ```
   e todos os filhos consomem `var(--c-color, var(--c-brand))`. Esse é o padrão
   para páginas de produto: setar `--c-color` no wrapper e deixar o componente herdar.
6. Backgrounds de ícone de módulo: cor do produto a **15% de opacidade**
   (exceção: `.icn-fin` usa 18%, porque o violeta é mais fraco em contraste).
7. **Cor de acento por TIPO de página** (regra aprovada em 25/08/2026):

   | Tipo | Páginas | `.eyebrow` | `hero-glow` |
   |---|---|---|---|
   | Institucional | Home, Sobre, Consultoria, Clientes, Recursos, Parceiros, Contato | **ciano** `--c-edu` (mantém) | ciano + brand |
   | Produto | CRM, Educação, Marketing, Finance, HR, AI | **herda `--c-color`** (cor do produto) | `g1` = cor do produto · `g2` = **brand** (âncora institucional) |

   O `g2` em brand é obrigatório: é o que impede a página de produto de perder
   o vínculo visual com a marca.

### Escala, layout e sombras

```css
--r-sm: 8px;  --r-md: 14px;  --r-lg: 22px;  --r-xl: 32px;
--maxw: 1320px;
--pad-x: clamp(20px, 4vw, 56px);
--shadow-sm: 0 1px 2px rgba(0,0,0,.2), 0 2px 6px rgba(0,0,0,.15);
--shadow-md: 0 8px 24px rgba(0,0,0,.25), 0 2px 8px rgba(0,0,0,.15);
--shadow-lg: 0 20px 60px rgba(0,0,0,.35), 0 8px 24px rgba(0,0,0,.2);
--shadow-glow-brand: 0 0 60px rgba(60,80,217,.4);
--shadow-glow-cyan:  0 0 60px rgba(3,219,255,.35);
```

Raios usados na prática: cards de módulo/solução **24px**, mega-menu **20px**,
dashboards **20px**, founding block **32px**, botões e pills **999px**.

### Tipografia

Carregada via Google Fonts em uma chamada:
`DM Sans (opsz 9..40, 300–700)` + `Sora (300–700)` + `DM Mono (400,500)`

```css
--font-sans:    "DM Sans", -apple-system, BlinkMacSystemFont, sans-serif;
--font-display: "Sora", "DM Sans", -apple-system, sans-serif;
--font-mono:    "DM Mono", ui-monospace, "SF Mono", Menlo, monospace;
```

| Elemento | Regra |
|---|---|
| `h1..h4` | Sora, **weight 500** (nunca 700), `line-height 1.05`, cor branca |
| `h1` | `clamp(2.6rem, 6vw, 4.8rem)` · `letter-spacing -0.04em` |
| `h2` | `clamp(2rem, 3.8vw, 3.2rem)` · `-0.032em` |
| `h3` | `clamp(1.2rem, 1.6vw, 1.5rem)` · `-0.018em` |
| body | DM Sans, `line-height 1.55` |
| `.eyebrow` | DM Mono 12px/500, **cor ciano**, `letter-spacing .16em`, uppercase, com `::before` = traço de 24×1px em 60% de opacidade |
| labels de UI | DM Mono, 0.6–0.76rem, uppercase, `letter-spacing .06–.14em`, `--c-text-mute` |

**Assinatura tipográfica:** headings sempre com letter-spacing negativo e peso
médio (500) — nunca bold. Destaques dentro do h1/h2 usam **gradiente em texto +
itálico**:
```css
background: linear-gradient(120deg, var(--c-edu), var(--c-brand-light) 60%, var(--c-crm));
-webkit-background-clip: text; background-clip: text; color: transparent;
font-style: italic;
```

### Componentes principais

| Componente | Classe | Notas |
|---|---|---|
| Header fixo | `header.site` + `.scrolled` | fundo transparente → `rgba(11,20,64,.75)` + `backdrop-filter: saturate(180%) blur(16px)` quando `scrollY > 12` |
| Nav | `.nav` | grid `auto 1fr auto`; logo à esquerda, menu centralizado, CTAs à direita |
| Logo | `.brand img` | 34px de altura, `nexyss-logo-white.png`, **sem filtro**, `opacity: 1` |
| Mega-menu | `.mega` | `min-width 720px` (Plataforma) / `.mega-solucoes` 900px; abre em `:hover` **e** `:focus-within`; `translateY(-8px) → 0` em 250ms |
| Item de menu | `.mega-item` + `.icn icn-{crm,edu,mkt,fin,hr,ai,neutral}` | ícone 32px, texto `.nm` + `.ds` |
| Botões | `.btn` / `.btn-primary` / `.btn-ghost` | pill, altura 48px; primary = fundo branco + texto navy; ghost = glass + borda. Seta `svg.arr` translada 3px no hover |
| Seletor de idioma | `.lang-switch` | pill com bandeira + sigla. **Hoje é estático** (ver pendências) |
| Hero | `.hero` | 3 camadas de fundo empilhadas: `.hero-layers` (4 colunas verticais com raio 40px no topo = *signature* do brand book), `.hero-glow` g1 ciano / g2 brand (blur 80px), e `::before` grid de pontos 32px com máscara radial elíptica |
| Tag do hero | `.hero-tag` | dot verde pulsante + pill branca + texto |
| Dashboards | `.dash` + `.dash-main` / `.dash-mini` / `.dash-side` | mockups flutuantes com float independente; contêm `.kpi`, `.dash-chart` (SVG animado), `.bars` |
| Logo wall | `.logos` / `.logos-grid` | 6 colunas, `opacity .5`, logos como SVG inline + nome |
| Seção base | `section.block` | padding `130px 0`; variantes `.tinted` (gradiente navy→navy-mid) e `.deeper` (navy-deep sólido). **Alternar as variantes entre seções é o ritmo visual da página** |
| Cabeçalho de seção | `.section-head` | `max-width 800px`, `margin-bottom 72px`; eyebrow → h2 → parágrafo |
| Grid de módulos | `.platform-grid` | 12 colunas; `.mod-card` em `.lg`(6) `.md`(4) `.sm`(3) `.wide`(8) |
| Card de módulo | `.mod-card` | barra de 3px no topo na cor do produto (`::before`) + orb radial difuso no canto (`::after`, 12%→22% no hover) + `translateY(-4px)` no hover |
| Card de solução | `.sol-card` | ícone 48px + h3 + descrição + `.sol-tags` (pills que ficam cianas no hover) |
| Visual de IA | `.ai-visual` | 3 órbitas tracejadas concêntricas + núcleo com gradiente radial `ai→brand` + 6 `.ai-node` flutuando |
| Consultoria | `.consult-grid` | 4 colunas com `gap: 1px` sobre fundo `--c-line` = hairlines sem bordas duplicadas |
| Números | `.impact-strip` | 4 colunas, número Sora grande + `<small>` ciano para a unidade |
| Founding Customers | `.founding` | bloco em gradiente `brand → ai-deep`, raio 32px, padrão de pontos mascarado, checkmarks verdes |
| CTA final | `.cta-final` | centralizado, orb radial ciano de 800px atrás |
| Footer | `footer.site` | grid `1.5fr 1fr 1fr 1fr 1fr`; colunas Plataforma / Soluções / Empresa / Recursos; `h5` em DM Mono; links ficam cianos no hover; `.footer-bottom` com o legal "Nexyss Group" |

### Animação e reveal

**Reveal no scroll** — o único JS de animação da Home:
```css
.reveal          { opacity:0; transform:translateY(24px); transition:.8s ease; }
.reveal.in       { opacity:1; transform:translateY(0); }
.reveal-stagger > *   { opacity:0; transform:translateY(20px); transition:.6s ease; }
.reveal-stagger.in > * { opacity:1; transform:translateY(0); }
/* delays: 0 / .08 / .16 / .24 / .32 / .4s — definidos até nth-child(6) */
```
```js
new IntersectionObserver(cb, { threshold: 0.12, rootMargin: '0px 0px -60px 0px' })
// dispara uma vez e chama io.unobserve(el)
```
> Ao criar páginas novas com mais de 6 itens em um `.reveal-stagger`,
> estender os `nth-child` — os itens 7+ herdam delay 0 hoje.

**Keyframes existentes** (reutilizar, não inventar novos):

| Nome | Duração | Onde |
|---|---|---|
| `pulse` | 2.2s ∞ | dot verde do `.hero-tag` |
| `floatA` | 8s ∞ | `.dash-main` (−6px) |
| `floatB` | 7s ∞, delay 1s | `.dash-side` (+8px) |
| `floatC` | 9s ∞, delay .5s | `.dash-mini` (−10px, mantendo `rotate(-1.5deg)`) |
| `draw` | 3s / 3s+.4s | linhas do gráfico via `stroke-dashoffset` |
| `fadeIn` | 1.5s, delay 1.5s | área preenchida do gráfico |
| `barGrow` | 2s | barras do `.dash-mini`, `scaleY` com delays .1s→.7s |
| `nodeY` | 5s ∞ | 6 `.ai-node`, delays 0/.8/1.2/1.6/2/2.4s |

**Padrão de transição geral:** `.2s` para hover de cor/fundo, `.25s` para
sombra/mega-menu, `.3–.35s` para transform de card, `.6–.8s` para reveal.

### Responsivo

Desktop-first, **dois breakpoints apenas**:

- `max-width: 1080px` — heros/grids de 2 colunas viram 1; `.mod-card` (todos os
  tamanhos) vira `span 12`; soluções 1 coluna; consultoria e impacto 2 colunas;
  footer 2 colunas; logos 3 colunas.
- `max-width: 760px` — `.nav-menu`, o CTA do header e o `.lang-switch` são
  escondidos e o `.nav-toggle` aparece; `section.block` cai para `80px 0`;
  hero para `130px 0 70px`; consultoria/impacto/footer em 1 coluna.

---

## Arquitetura de arquivos

```
index.html              # Home — apenas markup + <link> e <script src>
assets/nexyss.css       # DESIGN SYSTEM COMPLETO — fonte unica de verdade
assets/nexyss.js        # header scroll · reveal · drawer mobile
```

**Backup oficial é o git** (decisão de 11/09/2026). O `index.html.bak` foi
removido na limpeza pré-deploy; o estado aprovado de cada página vive no
histórico de commits.

**Toda pagina nova carrega os dois arquivos compartilhados:**
```html
<link rel="stylesheet" href="assets/nexyss.css" />   <!-- ajustar ../ conforme profundidade -->
...
<script src="assets/nexyss.js"></script>             <!-- fim do <body>, sem defer -->
```

`<link rel="stylesheet">` e `<script src>` **funcionam normalmente em `file://`** —
a restricao de `file://` vale para `fetch()`/XHR, nao para subrecursos. Por isso
CSS e JS ja sao compartilhados, enquanto header e footer seguem duplicados inline
(esses precisariam de `fetch`).

Regra: **nunca duplicar CSS dentro de uma pagina.** Estilo especifico de pagina
entra em `assets/nexyss.css` numa secao propria e comentada.

## Assets

```
assets/nexyss-logo-white.png  # lockup p/ FUNDO ESCURO — header, drawer e footer (12 <img>)
assets/nexyss-logo.png        # lockup p/ fundo claro — só og:image / twitter:image
assets/nexyss-mark.png        # isotipo — favicon
```
Os dois lockups são 1080×265 RGBA, pixel a pixel idênticos exceto o wordmark:
**isotipo sempre colorido** (gradiente azul→ciano→verde); wordmark branco
(#E0E0E0) na `-white`, azul-violeta (≈`--c-brand`) na outra.

As duplicatas soltas da raiz (`Logo.png`, `Logo White.png`, `Isotipo.png`,
`Background*.png`) e o `NEXYSS.pdf` (brand book, 5 MB) foram **removidos do
repositório** na limpeza de 11/09/2026 — os PNGs eram cópias byte a byte das
versões em `assets/`. O brand book segue como referência externa, fora do git.

> **Regra: nenhum `filter` sobre o logo.** `brightness(0) invert(1)` achata o
> isotipo num octógono branco chapado (ver bug fix de 11/09/2026 abaixo).
> Para fundo escuro usar a `-white`; para preview de link (fundo claro) usar a
> `nexyss-logo.png`. Se um dia precisar de wordmark colorível por CSS, o caminho
> é SVG separado (isotipo + wordmark), não filtro.

---

## Arquitetura de Páginas

```
/                          Home institucional          ✅ pronta e aprovada
/plataforma/               overview da plataforma       ✅ pronta
  /plataforma/crm/           TEMPLATE de produto          ✅ pronta
  /plataforma/educacao/                                 ✅ pronta (sem #compliance)
  /plataforma/marketing/                                ⬜
  /plataforma/finance/                                  ⬜
  /plataforma/hr/                                       ⬜
  /plataforma/ai/                                       ⬜
  /plataforma/integracoes/                              ⬜
/solucoes/                 overview                     ⬜
  /solucoes/por-funcao/                                 ⬜
  /solucoes/por-objetivo/                               ⬜
  /solucoes/por-porte/                                  ⬜
/consultoria/                                           ⬜
/clientes/                 c/ Founding Customers        ⬜
/recursos/                 blog, casos, guias, webinars ⬜
/parceiros/                                             ⬜
/sobre/                                                 ⬜
/contato/                                               ⬜
```

A Home já contém versões-resumo de `#plataforma`, `#solucoes`, `#ai`,
`#consultoria` e `#clientes`. **As páginas internas devem aprofundar esses
blocos, não repeti-los** — e a copy precisa permanecer consistente com a Home.

---

## Requisitos Técnicos

- **Stack:** HTML + CSS + JS puro. Sem framework, sem build step — por enquanto.
- **Responsivo:** desktop-first (breakpoints 1080 / 760), com mobile completo.
- **Multi-idioma:** PT · EN · ES · FR · IT · DE · JA · ZH · MN
  - detecção pelo idioma do browser
  - seletor manual (`.lang-switch`, já existe no header)
  - persistência em `localStorage`; escolha manual sempre vence a detecção
- **URLs:** flat por enquanto (`/plataforma/crm/`). O prefixo de idioma
  (`/pt/`, `/en/`, …) + `hreflang`/`x-default` entra quando o conteúdo estabilizar.
- **Componentes reutilizáveis:** header e footer ficam **duplicados inline** por
  enquanto (ver decisão 1 abaixo); viram fragmentos depois do hosting.
- **SEO:** title/description por página, Open Graph, Twitter card, canonical,
  structured data (Organization, SoftwareApplication, BreadcrumbList), sitemap.

### Decisões de arquitetura (tomadas em 25/08/2026)

1. **Header/footer duplicados inline** em cada página, por enquanto.
   Motivo: a prioridade é testar abrindo `file://` direto, e fragmentos via
   `fetch()` quebram nesse protocolo. Refatorar para fragmentos servidos por
   HTTP **depois** que o hosting estiver de pé (GitHub + Netlify).
2. **URLs flat**, sem prefixo de idioma: `/plataforma/crm/`, não `/pt/plataforma/crm/`.
   Prefixar só quando o conteúdo estabilizar.
3. **Todo texto visível leva `data-i18n="chave.dot.notation"`** desde já, para
   destravar a tradução depois sem reescrever markup. Convenção de chaves:
   `nav.*`, `mod.<slug>.*`, `sol.<slug>.*`, `cta.*`, `<pagina>.<secao>.<campo>`.
4. **Idioma default: pt-BR.**

### Status das pendências da Home

| # | Pendência | Status |
|---|---|---|
| 1 | `.nav-toggle` sem JS | ✅ **Resolvido** — drawer mobile implementado (ver abaixo) |
| 2 | `.lang-switch` estático | ⏸️ Adiado de propósito — fica só visual até fazermos i18n de fato |
| 3 | Meta tags de SEO | ✅ **Mínimo essencial adicionado** — description mais rica, OG completo, Twitter card, canonical, theme-color. Structured data (JSON-LD) e hreflang ficam para quando o conteúdo estabilizar |
| 4 | `href="#"` em todos os links | ⬜ Ligar conforme as páginas forem nascendo |
| 5 | `<html lang="pt-BR">` fixo | ⬜ Dinamizar junto com o i18n |
| 6 | `.reveal-stagger` só até o 6º filho | ⬜ Estender quando uma página precisar de 7+ |

### TODO — Domínio oficial

Substituir todas as ocorrências de `nexyss.com` (placeholder atual) pelo domínio
real quando confirmado. **Buscar globalmente antes de aplicar** — a lista abaixo é
de 04/09/2026 e pode ficar desatualizada conforme páginas novas nascerem.

**20 ocorrências nas 4 páginas aprovadas — 5 por página, sempre nas mesmas linhas:**

| Linha | Tag |
|---|---|
| 12 | comentário `<!-- TODO -->` |
| 13 | `<link rel="canonical">` |
| 18–19 | `<meta property="og:url">` |
| 22–23 | `<meta property="og:image">` |
| 28–30 | `<meta name="twitter:image">` |

> ⚠️ **`og:image` e `twitter:image` também carregam o domínio** — não estavam na
> lista original ("canonical e og:url"). São 5 tags por página, não 2.

Mais 4 ocorrências em documentação (`CLAUDE.md` ×3, `AUDIT-REPORT.md` ×1), que
devem ser atualizadas junto para a memória não apontar para o placeholder.

Comando de conferência:
```bash
grep -rn 'nexyss\.com' --include='*.html' --include='*.md' . | grep -v baselines/
```

**TODO ABERTO — domínio oficial.** `nexyss.com` está em uso como *placeholder*
no `canonical` e no `og:url`. Jonathan precisa confirmar o domínio real antes de
publicar; quando confirmar, atualizar em todas as páginas já criadas.

**TODOs deixados no `index.html`** (marcados com `<!-- TODO -->`):
domínio oficial no `canonical`/`og:url` (placeholder `https://www.nexyss.com/`)
e uma `og:image` dedicada de 1200×630 (hoje aponta para `assets/nexyss-logo.png`).

### Drawer mobile — padrão a reusar em todas as páginas

Implementado na Home, ativo **somente ≤ 760px**, isolado por
`@media (min-width:761px){ .drawer,.drawer-overlay{display:none!important} }`
— desktop verificado sem nenhuma alteração.

- Markup: `.drawer-overlay#drawerOverlay` + `aside.drawer#mobileDrawer`
  (`.drawer-head` / `.drawer-nav` / `.drawer-foot`), inserido logo após `</header>`.
- Painel de 400px (`min(400px, 88vw)`) deslizando da direita,
  `cubic-bezier(.4,0,.2,1)` em 350ms, sobre overlay com blur.
- Acordeões `.drawer-acc` + `.drawer-panel` usando `grid-template-rows: 0fr → 1fr`
  (altura automática animável, sem `max-height` chutado). Os itens internos
  reusam `.mega-item` e `.icn-*` do mega-menu — mesma linguagem visual.
- Hambúrguer vira "X" via `.nav-toggle.open`.
- **Regra de mega-menu no mobile (aprovada):** mega-menu denso no desktop vira,
  no drawer, **no máximo 3 categorias** com link "Ver todos" apontando para a
  página de índice daquele eixo. Nunca replicar a árvore inteira no drawer.
  Aplicado em Soluções (3 eixos no lugar dos 18 itens folha).
- A11y: `aria-expanded`/`aria-controls`/`aria-hidden`, foco vai para o botão
  fechar ao abrir e volta ao gatilho ao fechar, focus trap no Tab, fecha com
  Esc / clique no overlay / clique em qualquer link, trava o scroll do body
  (`body.drawer-open`) e fecha sozinho se a janela passar de 760px.
- Backup pré-alteração ficou em `index.html.bak` até 11/09/2026; removido — git é o backup.

---

## Template de página de produto (`/plataforma/crm/`)

A CRM é o **molde** das outras 5 páginas de produto. Para criar Educação,
Marketing, Finance, HR ou AI: copiar `plataforma/crm/index.html`, trocar a
classe de tema no `<body>` e substituir conteúdo. Nenhum CSS novo deve ser
necessário.

```html
<body class="theme-crm page-produto">   <!-- theme-edu | theme-mkt | theme-fin | theme-hr | theme-ai -->
```

`theme-*` fornece `--c-color`, `--c-color-deep`, `--c-color-a08/a15/a25`.
`page-produto` faz eyebrow, glow, ícones, tags e foco herdarem a cor do produto.

### Ordem das 12 seções

1. Hero de produto (`.hero` + **Visual A**) · 2. `.subnav` sticky ·
3. `.logos` · 4. `#problema` (3 `.sol-card`) · 5. `#recursos`
(`.platform-grid`, 2 `lg` + 3 `md`) · 6. `#visao-360` (`.ai-inner` +
**Visual B**) · 7. `#ia` (`.ai-inner` + `.ai-visual`) · 8. `#integracoes`
(`.consult-grid`) · 9. `#para-quem` (3 `.sol-card`) · 10. impacto
(`.impact-strip`) · 11. `#clientes` (`.founding`, **sem recolorir**) ·
12. `.cta-final`.

Header, drawer, bloco Founding e footer são **cópias exatas** da Home, com
`assets/` reescrito para `../../assets/`.

### Componentes novos criados junto com a CRM

| Componente | Uso |
|---|---|
| `.subnav` / `.subnav-brand` / `.subnav-links` | navegação secundária sticky |
| `.pipe-board` e filhos (**Visual A**) | quadro kanban do hero |
| `.acct360` / `.acct-*` / `.fc-*` (**Visual B**) | ficha 360º + forecast |
| `.prod-tint` | `.ai-products` reaproveitado fora da seção de IA — ícone assume a cor do produto |
| `.skip-link` | pular para o conteúdo |
| `.theme-*` | os 6 temas de produto |

Novos keyframes (os únicos criados além dos da Home): `growX` (barra de
probabilidade), `pipeDrag` (card em trânsito, preserva o `rotate`) e
`ringDraw` (anel de health score, para em 87%).

### Scrollspy — por que não é `threshold: 0.4` puro

`threshold` mede a fração **da seção** visível. Uma seção mais alta que 2.5× a
viewport nunca chega a 40% visível e a âncora nunca acenderia. Medido em 375px:
`#recursos` alcança no máximo **30%** — com threshold puro ficaria morta.

A implementação usa `rootMargin: '-40% 0px -59% 0px'`, que reduz a viewport a
uma faixa fina posicionada a 40% do topo. Mesmo comportamento pretendido,
funcionando para seção de qualquer altura. Verificado nos dois viewports: a
sequência das âncoras sai correta e monotônica.

### Regra crítica: escopar tudo que for de produto

Todo seletor novo destinado a página de produto **precisa** ser prefixado com
`.page-produto` ou uma classe própria. Um `section[id] { scroll-margin-top }`
sem escopo vazou para a Home e alterou o comportamento das âncoras dela —
pego e corrigido. `assets/nexyss.css` é compartilhado: regra sem escopo atinge
a Home aprovada.

### Teste de regressão — baselines v2 (04/09/2026)

Fingerprint por elemento (geometria + 28 propriedades computadas, animações
desligadas, `.reveal` forçado para `.in`). Depois de qualquer mexida em
`assets/nexyss.css` ou `assets/nexyss.js`, as 4 páginas têm que continuar batendo.
**Ver `baselines/` — JSON por página/viewport + o gerador em `baselines/tools/`.**

| Página | 1280×800 | doc | 375×812 | doc |
|---|---|---|---|---|
| Home | `784:05e853da` | 1280×7777 | `784:f917d2d4` | 375×12724 |
| Overview | `854:60db1f5d` | 1280×10661 | `854:3fdc840f` | 375×16982 |
| CRM | `915:171660d1` | 1280×9574 | `915:8e8775d6` | 375×15692 |
| Educação | `1062:c0084a19` | 1280×11767 | `1062:28bf25a5` | 375×19088 |

> **Baseline v3 — pós-correção do logo (11/09/2026).** Substitui os v2 de
> 04/09. Delta em relação aos v2 verificado elemento a elemento: exatamente
> **3 `<img>` por página, só `opacity 0.95→1`**; geometria, contagem e tamanho
> de documento idênticos nas 8 capturas. Antes de aplicar a correção, os v2
> foram recapturados e bateram 8/8 (referência confiável).
>
> Hashes v2 aposentados: Home `784:82af4c99`/`784:748535f5` · Overview
> `854:8e96f774`/`854:cf1f4838` · CRM `915:f788cb3c`/`915:86526521` ·
> Educação `1062:ecdc7c26`/`1062:6fe10d92`.

> ⚠️ **O fingerprint não cobre `filter` nem `src` de `<img>`.** As 28
> propriedades capturadas não incluem nenhum dos dois. Troca de asset ou de
> filtro CSS com geometria igual passa **invisível** pelo hash — verificar
> por screenshot/DOM à parte.

Formato do hash: `<nº de elementos>:<FNV-1a 32 bits>`. Verificado **determinístico**
em duas passagens independentes (8/8 idênticos).

> **Hashes v1 aposentados.** As baselines antigas da Home (`792:a53ba235` /
> `792:54ebb72b`, doc 8161/13685) foram geradas por um script que **não foi
> salvo** — algoritmo e critério de seleção de elementos desconhecidos (contam
> 792 elementos contra 820 de hoje; o bloco do drawer sozinho tem 99, então a
> diferença não é só o drawer). São **irreproduzíveis** e por isso substituídas,
> não comparadas. A integridade da Home foi confirmada por outro caminho: o texto
> do `<body>` é idêntico ao de `index.html.bak` mais o bloco do drawer, e as
> alterações no CSS compartilhado desde então são puramente aditivas
> (`.status-badge`, que a Home não usa).

**Como regerar:**
```bash
node baselines/tools/run.js <dir-de-trabalho>     # 4 páginas × 2 viewports, Chrome headless
python3 baselines/tools/extract.py <dir> baselines run1
```
Requer `/Applications/Google Chrome.app` e rede (as fontes do Google Fonts
precisam carregar — o JSON grava `fontsLoaded` para flagrar uma captura offline,
que mudaria a geometria).

### Limitação do painel de preview

O painel do Claude Code mantém a aba como `document.visibilityState === "hidden"`,
então **nenhum `IntersectionObserver` dispara** — todo conteúdo `.reveal` fica
invisível e o screenshot não acompanha scroll programático. Para inspecionar
visualmente: forçar `.in` em `.reveal/.reveal-stagger` e isolar a seção no topo
com `display:none` nas irmãs. Não é bug do site.

### Fallbacks de reveal (resolvido em 25/08/2026)

O conteúdo de seção nasce com `opacity: 0` e só aparece com o
`IntersectionObserver`. Dois guards no CSS compartilhado:

1. **Sem JS** — `<html class="no-js">` e um script inline logo após `<head>`
   troca a classe para `js`. Se o JS estiver desligado ou falhar, `.no-js`
   permanece e `.reveal` entra visível e estático.
   > `@supports selector(:has())` foi considerado e descartado: feature query
   > de seletor testa suporte do navegador, não se o JS rodou. Não serve de
   > detector. `.no-js` é o mecanismo confiável.
2. **`prefers-reduced-motion: reduce`** — conteúdo visível, animação zerada.
   Como todas as animações usam `forwards`, colapsar a duração para `0.01ms`
   entrega o **estado final** em vez de congelar no inicial.

Aplicado na Home e na CRM. Toda página nova deve nascer com
`<html lang="pt-BR" class="no-js">` + o script inline no `<head>`.

### SEO por página

Cada página carrega `canonical`, `og:url`, `og:title`, `og:description` e
`twitter:*` **apontando para si mesma**, nunca para a Home.
Home → `https://www.nexyss.com/` · CRM → `https://www.nexyss.com/plataforma/crm/`.
(Domínio ainda é placeholder — ver TODO acima.)

### Pendências da página CRM

- `:focus-visible` está escopado em `.page-produto`. Recomendado promover
  para global depois de validado.

---

## Overview `/plataforma/` — o hub

Página **institucional** (`<body class="page-institucional has-subnav">`):
sem `theme-*`, eyebrow ciano, `hero-glow` ciano + brand. É a única página onde
as 6 cores de produto aparecem lado a lado.

### Como ela se diferencia da `#plataforma` da Home

A seção da Home responde **"o que existe?"**. A overview responde
**"como isso funciona junto, e por onde eu entro?"**. O eixo dela é a
**camada compartilhada** — dado, identidade, permissão, IA — que é o que a
Home afirma ("sem silos") sem provar. **A overview não repete card de módulo
no formato da Home**; cada card ganha a linha `.mod-conn`, que diz com quem
aquele módulo conversa.

### Seções

1. Hero (**Visual A**) · 2. `.subnav` · 3. `#camada` (4 `.consult-item`) ·
4. `#modulos` (6 `.mod-card md`, cada um na sua cor, + `.mod-seventh`) ·
5. `#fluxo` (**Visual B** + frase generalizando o padrão) · 6. `#ia` ·
7. `#integracoes` · 8. `#adocao` · 9. `#comparativo` (`.vs-table`) ·
10. impacto · 11. `#clientes` (`.founding`) · 12. `.cta-final`.

### Componentes novos

| Componente | Uso |
|---|---|
| `.stack-viz` + `.sv-*` (**Visual A**) | 6 chips coloridos → 3 placas empilhadas → faixa Nexyss AI rotacionada |
| `.cascade` + `.cas-*` (**Visual B**) | evento → 4 curvas coloridas → 4 cards por módulo; curvas usam o keyframe `draw` |
| `.mod-conn` | linha "com quem esse módulo conversa" dentro do `.mod-card` |
| `.mod-seventh` | faixa tracejada puxando Integrações & API |
| `.vs-table` + `.vs-wrap` | comparativo; vira cards empilhados ≤760px |
| `.visually-hidden` | texto só para leitor de tela |

Visual A ficou legível sem precisar do plano B (4 chips + 2 em silhueta).

### Classes de página — resumo

| Classe | O que faz |
|---|---|
| `theme-crm` … `theme-ai` | fornece `--c-color` e derivados |
| `page-produto` | eyebrow/glow/ícones/tags herdam a cor do produto |
| `page-institucional` | mantém o acento ciano; habilita `:focus-visible` |
| `has-subnav` | ativa `scroll-margin-top` nas âncoras. **Não usar `page-produto` para isso** — a overview é institucional e também tem subnav |

### Decisões de conteúdo

- **Comparativo genérico** — "Stack montado", sem nomear concorrente.
- **Evento-exemplo é matrícula** (Educação é o vertical live), seguido de uma
  frase generalizando o padrão para contrato fechado, novo funcionário e lead
  qualificado.

### Links pendentes (404 hoje)

`/plataforma/{educacao,marketing,finance,hr,ai,integracoes}/` já estão
linkados na overview e retornam 404. Só `crm/` existe. Falta criar uma
**página 404 amigável** antes de qualquer publicação.


---

## Página `/plataforma/educacao/`

`<body class="theme-edu page-produto has-subnav">` — 13 seções publicadas.

### Argumento central (o que a separa da CRM)

A **CRM argumenta largura**: um cliente visto por todos os módulos no mesmo
instante. A **Educação argumenta duração e multiplicidade**: um aluno
acompanhado por anos, numa operação replicada em muitos campi, moedas e
idiomas. CRM diz "seus dados estão em silos"; Educação diz "sua operação está
fragmentada no tempo e no espaço".

### Persona primária: **mantenedora de rede**

Quem assina em ticket enterprise e para quem multi-campus é dor, não recurso.
O topo da página fala de rede, consolidação e risco. Direção acadêmica e
financeira são convencidas no miolo; secretaria (usuária e **vetadora** na
implantação) é tranquilizada perto do fim. O `#para-quem` usa **4 personas em
`.consult-grid`**, não 3 em `.sol-card`.

### Vocabulário

Aluno, trajetória, campus, rede, mantenedora, mensalidade, bolsa, evasão.
**Nunca** cliente, pipeline, negócio, fatura — esse é o vocabulário da CRM.

### O que difere estruturalmente da CRM

- `#recursos` em **3 clusters** (Acadêmico · Financeiro acadêmico ·
  Experiência e rede) com `.cluster-label`, em vez de lista plana.
- **`#rede` é seção nova** — multi-campus como narrativa central.
- `#visao-360` virou **`#jornada`**: de "uma tela com tudo agora" para
  "uma pessoa ao longo de anos".
- `#ia` foca **evasão**, o caso de uso mais forte do vertical.
- `#integracoes` tem lista própria: LMS, catraca/biometria, boleto/PIX.

### Visuais

| Visual | Onde | Origem |
|---|---|---|
| Trajetória do aluno (`.jr-*`) | hero | 🆕 |
| Painel da rede (`.netpanel`, `.np-*`) | `#rede` | 🆕 |
| Funil de admissões (`.pipe-board`) | `#recursos` | ♻️ **reuso da CRM**, ciano automático via `theme-edu`, zero CSS novo |
| Ficha do aluno (`.acct360` + `.fc-*`) | `#jornada` | ♻️ **reuso da CRM**, conteúdo longitudinal |
| Chip de IA (`.pipe-ai`) | hero | ♻️ reuso |

**Zero keyframes novos.** `growX` (criado na CRM) preenche o trilho e as barras
de ocupação; `draw`, `floatA`, `floatB` e `reveal-stagger` cobrem o resto.

⚠️ **`.reveal-stagger` só define delay até o 6º filho** e o `.platform-grid` da
Home tem 7. Por isso a trajetória usa **6 semestres**, não 7 — estender os
`nth-child` alteraria a animação da Home. Se algum dia precisar de 7+, tem que
ser uma classe nova, não a extensão da existente.

### `#compliance` — NÃO PUBLICADA

Bloqueada aguardando validação do Jonathan. Regra acordada: **SIM** → afirma ·
**ROADMAP** → só com data · **NÃO** → não menciona. Sem as respostas não há o
que afirmar, então a seção foi omitida (e o link tirado da subnav) em vez de
preenchida com copy não verificada. O HTML tem um comentário no lugar com os
4 itens a validar.

### ⚠️ Afirmações de capacidade não validadas (dívida a resolver)

Copy de produto que **Claude escreveu sem validação** e que Jonathan precisa
confirmar antes de qualquer publicação:

| Afirmação | Onde |
|---|---|
| "Residência de dado por região" | CRM |
| "Relatórios auditáveis" / "trilha de auditoria" | CRM, overview |
| "Conectores nativos para os principais ERPs" | CRM, overview |
| "REST documentada, eventos em tempo real, ambiente de testes" | CRM, overview |
| "Sincronização bidirecional com Google Workspace e Microsoft 365" | CRM |
| "Turma e docente sincronizados com o LMS" · "catraca e biometria" · "boleto, cartão, PIX" | Educação |

Números da Home (99.99%, 9 idiomas, 120+ países, 3.4×) são do Jonathan e estão
fora dessa lista.

### Baseline de regressão — resolvido em 04/09/2026

As **4 páginas** (Home, Overview, CRM, Educação) têm fingerprint armazenado em
`baselines/`, nos dois viewports, junto com o gerador. Ver
"Teste de regressão — baselines v2" acima para os hashes e o procedimento.


## Bug fix: logo em branco (11/09/2026)

**Sintoma reportado:** logo "em branco/quebrado" no navegador, nas 4 páginas.

**Causa raiz:** `.brand img` e `.footer-brand img` aplicavam
`filter: brightness(0) invert(1)` sobre `nexyss-logo.png`. O filtro zera o RGB
e inverte — alfa preservado, cor interna destruída. O wordmark azul virava
branco (intenção original), mas o **isotipo** — octógono com gradiente
azul→ciano→verde — virava um octógono branco chapado. Não era caminho quebrado
(4/4 resolviam) nem alfa mal configurado. O comportamento é idêntico em
`file://` e HTTP.

**Correção aplicada (aprovada pelo Jonathan):**
- 12 `<img>` (header + drawer + footer × 4 páginas): `nexyss-logo.png` →
  `nexyss-logo-white.png`.
- `assets/nexyss.css` linhas 200 e 1242: `filter` removido, `opacity 0.95 → 1`.
- `og:image` / `twitter:image` **mantidos** em `nexyss-logo.png` — preview de
  link é sobre fundo claro; wordmark branco ficaria invisível ali.

**Verificação:** fingerprint pré (8/8 = v2) → pós: 3 elementos por página,
só `opacity`. Visual conferido em 1280 (header Home) e 375 (header CRM, drawer)
+ DOM do footer. Baselines regravados como v3.

**Backlog:** extrair vetor do `NEXYSS.pdf` → `nexyss-mark.svg` +
`nexyss-wordmark.svg` com `currentColor` (nítido em retina, mais leve, colorível).

## Regras de Conteúdo e Comercial (definidas em 04/09/2026)

### R1 — Naming e pricing de produtos

- **Nexyss CRM** é o único módulo com **pricing público**: €15,99 / €10,99 /
  Enterprise custom.
- **Todos os outros** — Educação, Marketing, Finance, HR, AI — e a **Consultoria**
  são **venda por projeto / custom**.
- Sempre escrever **"a partir de €X"**. Nunca preço fechado.

### R2 — Preços não aparecem no site

- **Nenhuma página do site institucional expõe preço.** Inclusive a do CRM.
- CTA padrão de todo módulo: **"Falar com Especialista"** ou **"Solicitar Demo"**.
- Os preços do CRM vivem em **materiais comerciais externos** — banners, campanhas,
  PDFs, propostas.
- Racional: alinhamento com o posicionamento enterprise. Salesforce, HubSpot e
  Monday não expõem preço detalhado no site institucional.

### R3 — Métricas quantitativas

- **Proibido inventar número de impacto** — "X% de redução", "Y× mais rápido",
  "$Z de economia". Sem case real medido, o número não existe.
- Métrica de impacto só entra quando houver **case real, medido e publicável**.
- **Métrica técnica verificável é permitida**: uptime/SLA, idiomas suportados,
  número de módulos, cobertura geográfica declarada.

### R4 — Vocabulário de idiomas

- Em **label numérico** (`.impact-strip`, `.hero-meta`): **"Multi-idioma nativo"**.
  Sempre no singular — nunca "Multi-idioma nativos".
- Em **texto corrido**: especificar — **"Português, Inglês e Espanhol"**.
- **Nunca usar `PT · EN · ES` como formato canônico.** (Foi testado em 04/09/2026
  nos labels e revertido: cabia, mas não é o vocabulário da marca.)
- Em contexto muito estreito onde "Multi-idioma nativo" não couber, aceita-se
  **"Multi-idioma"**. Medido: o rótulo completo mede 148px em caixa alta e cabe
  na coluna mais estreita do site hoje (159,5px, `.hero-meta.cols-2` a 375px).

### R5 — Sistema de badges de status

Componente `.status-badge` (em `assets/nexyss.css`), 4 estados:

| Badge | Modificador | Cor | Rótulo |
|---|---|---|---|
| 🟢 | `--live` | verde `--c-crm` | **Ativo** — existe e funciona hoje |
| 🟡 | `--beta` | laranja `--c-mkt` | **Beta** — teste com Founding Customers |
| 🔵 | `--roadmap` | azul `--c-ai` | **Roadmap** — comprometido, com data |
| ⚪ | `--planned` | branco 40% | **Planejado** — no radar, sem data |

- O rótulo 🟢 é **"Ativo"**, nunca "Disponível" — 5 caracteres contra 10, mais
  curto que "Roadmap" (7), o que evita reflow dos bullets. (Trocado em 04/09/2026.)
- **`CLAIMS-AUDIT.md` é a fonte de verdade** de qual claim tem qual status.
  Consultar **antes** de aplicar qualquer badge novo.
- **Sem validação do time técnico = fica 🔵.** Nunca 🟢 por inferência.
  Racional: em due diligence enterprise, afirmar 🟢 e não ter é muito pior que
  o contrário.
- No bloco `.founding` — único fundo claro do site — usar a variante
  `.founding .status-badge` (branco sobre navy 35%). O badge padrão reprova em
  contraste ali (1.57:1 a 2.12:1 contra os 4.5:1 de AA).

#### R5.1 — Badge vs. descrição de serviço

Badge marca **feature específica verificável** — afirmação binária "faz X" /
"não faz X". **Descrição narrativa de serviço ou oferta** (o parágrafo que conta
o que uma prática de consultoria entrega) **não recebe badge**: a existência dela
no site já implica disponibilidade.

| | Exemplo |
|---|---|
| ✅ Badgeável | "Sync bidirecional Google Workspace" → 🟢 Ativo |
| ✅ Badgeável | "Exportação e-MEC" → 🔵 Roadmap |
| ❌ Não badgeável | "Diagnóstico organizacional, roadmap de transformação digital e redesenho de processos com foco em dados e IA" |
| ❌ Não badgeável | descrição institucional, tagline, proposta de valor |

**Adendo — a distinção é a granularidade da afirmação, não o tipo da seção.**
Se uma oferta de serviço passar a listar recursos específicos em bullets (dentro
de Managed Services, por exemplo: "SLA 24/7", "monitoramento proativo"), **esses
bullets voltam a ser badgeáveis**.

## Regras de Trabalho

1. **A Home é território protegido — mudança só por decisão explícita do Jonathan.**
   Nada de refatorar, "melhorar" ou reorganizar o CSS existente por conta própria.
   > Histórico: a regra original era "NUNCA mudar o visual da Home". Ela foi
   > **superada em 04/09/2026** pela auditoria de claims, que o Jonathan mandou
   > aplicar também na Home (remoção do bloco de impacto, idiomas, alcance
   > geográfico, Founding Customers, consultoria). O baseline foi regerado depois.
   > A proteção continua valendo contra mudança **não solicitada**.
2. **SEMPRE reutilizar o design system acima** — mesmos tokens, mesmas classes,
   mesmos keyframes. Nada de variantes novas sem combinar antes.
3. **SEMPRE confirmar antes de criar qualquer arquivo ou página nova.**
4. **SEMPRE mostrar preview/plano antes de gerar código longo.**
5. **Uma página por vez**, validando com o Jonathan entre cada uma.
6. Idioma de trabalho: **português**.
7. Todo texto novo nasce com `data-i18n`.
8. **Nunca inventar métrica de cliente.** Não há clientes reais ainda. Números
   em página só podem ser fatos verificáveis (capacidade de produto, SLA,
   cobertura) ou os já aprovados na Home. Na dúvida, perguntar ao Jonathan.
9. Testar sempre nos dois extremos: **375px** (drawer) e **1280px** (desktop),
   confirmando que o desktop não mudou.
