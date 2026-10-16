# Nexyss - Memória do Projeto

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
/* Navy scale - do brand book */
--c-navy-deep:  #0B1440;   /* fundo padrão do body, hero topo, footer, .deeper */
--c-navy:       #131E4F;   /* logo wall, .consult-item, base do .tinted */
--c-navy-mid:   #1E285F;   /* topo do gradiente .tinted, hover de consult-item */
--c-navy-light: #2A3985;
--c-navy-hi:    #3A5EAF;

/* Brand blue-violet - wordmark Nexyss */
--c-brand:       #3C50D9;
--c-brand-light: #5B6DE8;

/* Sistema de cores por produto */
--c-crm: #45E599;  --c-crm-deep: #2D9768;   /* Verde   - CRM */
--c-edu: #03DBFF;  --c-edu-deep: #019EC2;   /* Ciano   - Educação */
--c-mkt: #F25D23;  --c-mkt-deep: #C4451A;   /* Laranja - Marketing */
--c-fin: #7C8CE8;  --c-fin-deep: #3C50D9;   /* Violeta - Finance */
--c-hr:  #B84FE5;  --c-hr-deep:  #8E37B8;   /* Magenta - HR */
--c-hr-text: #CA7BEC;   /* tom de TEXTO do HR (contraste AA), usado só em .theme-hr */
--c-ai:  #37A7E2;  --c-ai-deep:  #1E7CB8;   /* Azul-elétrico - AI */

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
   glows do hero/CTA/footer. Manter esse papel duplo - **não trocar por brand**.
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
8. **Tom de texto derivado do HR (14/10/2026).** O magenta puro reprova AA em texto
   pequeno (4,45:1 sobre navy-deep). `--c-hr-text: #CA7BEC` (6,4:1) é o primeiro tom
   derivado de cor de produto, criado por motivo técnico e usado só sob `.theme-hr`.
   Ver a seção da página `/plataforma/hr/`.

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
`DM Sans (opsz 9..40, 300-700)` + `Sora (300-700)` + `DM Mono (400,500)`

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
| labels de UI | DM Mono, 0.6-0.76rem, uppercase, `letter-spacing .06-.14em`, `--c-text-mute` |

**Assinatura tipográfica:** headings sempre com letter-spacing negativo e peso
médio (500) - nunca bold. Destaques dentro do h1/h2 usam **gradiente em texto +
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

**Reveal no scroll** - o único JS de animação da Home:
```css
.reveal          { opacity:0; transform:translateY(24px); transition:.8s ease; }
.reveal.in       { opacity:1; transform:translateY(0); }
.reveal-stagger > *   { opacity:0; transform:translateY(20px); transition:.6s ease; }
.reveal-stagger.in > * { opacity:1; transform:translateY(0); }
/* delays: 0 / .08 / .16 / .24 / .32 / .4s - definidos até nth-child(6) */
```
```js
new IntersectionObserver(cb, { threshold: 0.12, rootMargin: '0px 0px -60px 0px' })
// dispara uma vez e chama io.unobserve(el)
```
> Ao criar páginas novas com mais de 6 itens em um `.reveal-stagger`,
> estender os `nth-child` - os itens 7+ herdam delay 0 hoje.

**Keyframes existentes** (reutilizar, não inventar novos):

| Nome | Duração | Onde |
|---|---|---|
| `pulse` | 2.2s ∞ | dot verde do `.hero-tag` |
| `floatA` | 8s ∞ | `.dash-main` (-6px) |
| `floatB` | 7s ∞, delay 1s | `.dash-side` (+8px) |
| `floatC` | 9s ∞, delay .5s | `.dash-mini` (-10px, mantendo `rotate(-1.5deg)`) |
| `draw` | 3s / 3s+.4s | linhas do gráfico via `stroke-dashoffset` |
| `fadeIn` | 1.5s, delay 1.5s | área preenchida do gráfico |
| `barGrow` | 2s | barras do `.dash-mini`, `scaleY` com delays .1s→.7s |
| `nodeY` | 5s ∞ | 6 `.ai-node`, delays 0/.8/1.2/1.6/2/2.4s |

**Padrão de transição geral:** `.2s` para hover de cor/fundo, `.25s` para
sombra/mega-menu, `.3-.35s` para transform de card, `.6-.8s` para reveal.

### Responsivo

Desktop-first, **dois breakpoints apenas**:

- `max-width: 1080px` - heros/grids de 2 colunas viram 1; `.mod-card` (todos os
  tamanhos) vira `span 12`; soluções 1 coluna; consultoria e impacto 2 colunas;
  footer 2 colunas; logos 3 colunas.
- `max-width: 760px` - `.nav-menu`, o CTA do header e o `.lang-switch` são
  escondidos e o `.nav-toggle` aparece; `section.block` cai para `80px 0`;
  hero para `130px 0 70px`; consultoria/impacto/footer em 1 coluna.

---

## Arquitetura de arquivos

```
index.html              # Home - apenas markup + <link> e <script src>
assets/nexyss.css       # DESIGN SYSTEM COMPLETO - fonte unica de verdade
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

`<link rel="stylesheet">` e `<script src>` **funcionam normalmente em `file://`** -
a restricao de `file://` vale para `fetch()`/XHR, nao para subrecursos. Por isso
CSS e JS ja sao compartilhados, enquanto header e footer seguem duplicados inline
(esses precisariam de `fetch`).

Regra: **nunca duplicar CSS dentro de uma pagina.** Estilo especifico de pagina
entra em `assets/nexyss.css` numa secao propria e comentada.

## Assets

```
assets/nexyss-logo-white.png  # lockup p/ FUNDO ESCURO - header, drawer e footer (12 <img>)
assets/nexyss-logo.png        # lockup p/ fundo claro - só og:image / twitter:image
assets/nexyss-mark.png        # isotipo - favicon
```
Os dois lockups são 1080×265 RGBA, pixel a pixel idênticos exceto o wordmark:
**isotipo sempre colorido** (gradiente azul→ciano→verde); wordmark branco
(#E0E0E0) na `-white`, azul-violeta (≈`--c-brand`) na outra.

As duplicatas soltas da raiz (`Logo.png`, `Logo White.png`, `Isotipo.png`,
`Background*.png`) e o `NEXYSS.pdf` (brand book, 5 MB) foram **removidos do
repositório** na limpeza de 11/09/2026 - os PNGs eram cópias byte a byte das
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
  /plataforma/marketing/                                ✅ pronta (14/10/2026 - 22 bullets, todos 🔵)
  /plataforma/finance/                                  ✅ pronta (14/10/2026 - 22 bullets, todos 🔵)
  /plataforma/hr/                                       ✅ pronta (14/10/2026 - 22 bullets, todos 🔵)
  /plataforma/ai/                                       ✅ pronta (15/10/2026 - 20 bullets, todos 🔵)
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
/contato/                  formulário Netlify + canais   ✅ pronta (11/09/2026)
  /contato/obrigado.html   página de sucesso (noindex)   ✅ pronta
```

A Home já contém versões-resumo de `#plataforma`, `#solucoes`, `#ai`,
`#consultoria` e `#clientes`. **As páginas internas devem aprofundar esses
blocos, não repeti-los** - e a copy precisa permanecer consistente com a Home.

---

## Requisitos Técnicos

- **Stack:** HTML + CSS + JS puro. Sem framework, sem build step - por enquanto.
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
| 1 | `.nav-toggle` sem JS | ✅ **Resolvido** - drawer mobile implementado (ver abaixo) |
| 2 | `.lang-switch` estático | ⏸️ Adiado de propósito - fica só visual até fazermos i18n de fato |
| 3 | Meta tags de SEO | ✅ **Mínimo essencial adicionado** - description mais rica, OG completo, Twitter card, canonical, theme-color. Structured data (JSON-LD) e hreflang ficam para quando o conteúdo estabilizar |
| 4 | `href="#"` em todos os links | ⬜ Ligar conforme as páginas forem nascendo |
| 5 | `<html lang="pt-BR">` fixo | ⬜ Dinamizar junto com o i18n |
| 6 | `.reveal-stagger` só até o 6º filho | ⬜ Estender quando uma página precisar de 7+ |

### TODO - Domínio oficial

Substituir todas as ocorrências de `nexyss.com` (placeholder atual) pelo domínio
real quando confirmado. **Buscar globalmente antes de aplicar** - a lista abaixo é
de 04/09/2026 e pode ficar desatualizada conforme páginas novas nascerem.

**20 ocorrências nas 4 páginas aprovadas - 5 por página, sempre nas mesmas linhas** (a lista é de 04/09; desde então `plataforma/marketing/` trouxe mais 5, no mesmo padrão, e `contato/` tem 7 + `obrigado.html` 5 - rodar o grep abaixo):

| Linha | Tag |
|---|---|
| 12 | comentário `<!-- TODO -->` |
| 13 | `<link rel="canonical">` |
| 18-19 | `<meta property="og:url">` |
| 22-23 | `<meta property="og:image">` |
| 28-30 | `<meta name="twitter:image">` |

> ⚠️ **`og:image` e `twitter:image` também carregam o domínio** - não estavam na
> lista original ("canonical e og:url"). São 5 tags por página, não 2.

Mais 4 ocorrências em documentação (`CLAUDE.md` ×3, `AUDIT-REPORT.md` ×1), que
devem ser atualizadas junto para a memória não apontar para o placeholder.

Comando de conferência:
```bash
grep -rn 'nexyss\.com' --include='*.html' --include='*.md' . | grep -v baselines/
```

**TODO ABERTO - domínio oficial.** `nexyss.com` está em uso como *placeholder*
no `canonical` e no `og:url`. Jonathan precisa confirmar o domínio real antes de
publicar; quando confirmar, atualizar em todas as páginas já criadas.

**TODOs deixados no `index.html`** (marcados com `<!-- TODO -->`):
domínio oficial no `canonical`/`og:url` (placeholder `https://www.nexyss.com/`)
e uma `og:image` dedicada de 1200×630 (hoje aponta para `assets/nexyss-logo.png`).

### Drawer mobile - padrão a reusar em todas as páginas

Implementado na Home, ativo **somente ≤ 760px**, isolado por
`@media (min-width:761px){ .drawer,.drawer-overlay{display:none!important} }` - desktop verificado sem nenhuma alteração.

- Markup: `.drawer-overlay#drawerOverlay` + `aside.drawer#mobileDrawer`
  (`.drawer-head` / `.drawer-nav` / `.drawer-foot`), inserido logo após `</header>`.
- Painel de 400px (`min(400px, 88vw)`) deslizando da direita,
  `cubic-bezier(.4,0,.2,1)` em 350ms, sobre overlay com blur.
- Acordeões `.drawer-acc` + `.drawer-panel` usando `grid-template-rows: 0fr → 1fr`
  (altura automática animável, sem `max-height` chutado). Os itens internos
  reusam `.mega-item` e `.icn-*` do mega-menu - mesma linguagem visual.
- Hambúrguer vira "X" via `.nav-toggle.open`.
- **Regra de mega-menu no mobile (aprovada):** mega-menu denso no desktop vira,
  no drawer, **no máximo 3 categorias** com link "Ver todos" apontando para a
  página de índice daquele eixo. Nunca replicar a árvore inteira no drawer.
  Aplicado em Soluções (3 eixos no lugar dos 18 itens folha).
- A11y: `aria-expanded`/`aria-controls`/`aria-hidden`, foco vai para o botão
  fechar ao abrir e volta ao gatilho ao fechar, focus trap no Tab, fecha com
  Esc / clique no overlay / clique em qualquer link, trava o scroll do body
  (`body.drawer-open`) e fecha sozinho se a janela passar de 760px.
- Backup pré-alteração ficou em `index.html.bak` até 11/09/2026; removido - git é o backup.

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
| `.prod-tint` | `.ai-products` reaproveitado fora da seção de IA - ícone assume a cor do produto |
| `.skip-link` | pular para o conteúdo |
| `.theme-*` | os 6 temas de produto |

Novos keyframes (os únicos criados além dos da Home): `growX` (barra de
probabilidade), `pipeDrag` (card em trânsito, preserva o `rotate`) e
`ringDraw` (anel de health score, para em 87%).

### Scrollspy - por que não é `threshold: 0.4` puro

`threshold` mede a fração **da seção** visível. Uma seção mais alta que 2.5× a
viewport nunca chega a 40% visível e a âncora nunca acenderia. Medido em 375px:
`#recursos` alcança no máximo **30%** - com threshold puro ficaria morta.

A implementação usa `rootMargin: '-40% 0px -59% 0px'`, que reduz a viewport a
uma faixa fina posicionada a 40% do topo. Mesmo comportamento pretendido,
funcionando para seção de qualquer altura. Verificado nos dois viewports: a
sequência das âncoras sai correta e monotônica.

### Regra crítica: escopar tudo que for de produto

Todo seletor novo destinado a página de produto **precisa** ser prefixado com
`.page-produto` ou uma classe própria. Um `section[id] { scroll-margin-top }`
sem escopo vazou para a Home e alterou o comportamento das âncoras dela -
pego e corrigido. `assets/nexyss.css` é compartilhado: regra sem escopo atinge
a Home aprovada.

### Teste de regressão - baselines v2 (04/09/2026)

Fingerprint por elemento (geometria + 28 propriedades computadas, animações
desligadas, `.reveal` forçado para `.in`). Depois de qualquer mexida em
`assets/nexyss.css` ou `assets/nexyss.js`, as 6 páginas têm que continuar batendo.
**Ver `baselines/` - JSON por página/viewport + o gerador em `baselines/tools/`.**

| Página | 1280×800 | doc | 375×812 | doc |
|---|---|---|---|---|
| Home | `782:3c05db58` | 1280×7841 | `782:1107c885` | 375×12871 |
| Overview | `854:2d8170bb` | 1280×10661 | `854:0c24e753` | 375×16982 |
| CRM | `915:c44675df` | 1280×9574 | `915:f8f31696` | 375×15692 |
| Educação | `1062:dff0ebc7` | 1280×11767 | `1062:5333e4f7` | 375×19088 |
| Contato | `576:e2641d7b` | 1280×3677 | `576:ab9ec9e1` | 375×5646 |
| Obrigado | `436:645a517a` | 1280×1250 | `436:2ae400ed` | 375×2167 |

> **Baseline v4 - página de contato + CTAs + logo wall (11/09/2026).** Substitui
> os v3 do mesmo dia. Delta v3→v4 verificado elemento a elemento:
> - **Overview, CRM, Educação:** só o botão "Falar com Especialista" (175→207px)
>   e o botão vizinho deslocando 16px para manter o centro. Nada mais.
> - **Home:** contagem 784→782 (logo wall: 6 `.logo-item` → 5 com classe de setor,
>   layout 3+2). Antes do wall: só o botão renomeado do hero. Depois do wall,
>   **todos os elementos deslocam +64px (1280) / +147px (375) em y** - translação
>   pura, a segunda linha do wall; nenhuma outra mudança de tamanho além dos botões.
> - **Contato / Obrigado:** baseline inicial.
> - Verificação cruzada: depois dos ajustes finais no CSS compartilhado (wall 3+2,
>   `.hero-inner` no form), Overview/CRM/Educação/Obrigado recapturados **idênticos**.
>
> Hashes v3 aposentados: Home `784:05e853da`/`784:f917d2d4` · Overview
> `854:60db1f5d`/`854:3fdc840f` · CRM `915:171660d1`/`915:8e8775d6` ·
> Educação `1062:c0084a19`/`1062:28bf25a5`.

> ⚠️ **O fingerprint não cobre `filter` nem `src` de `<img>`.** As 28
> propriedades capturadas não incluem nenhum dos dois. Troca de asset ou de
> filtro CSS com geometria igual passa **invisível** pelo hash - verificar
> por screenshot/DOM à parte.

Formato do hash: `<nº de elementos>:<FNV-1a 32 bits>`. Verificado **determinístico**
em duas passagens independentes (8/8 idênticos).

> **Hashes v1 aposentados.** As baselines antigas da Home (`792:a53ba235` /
> `792:54ebb72b`, doc 8161/13685) foram geradas por um script que **não foi
> salvo** - algoritmo e critério de seleção de elementos desconhecidos (contam
> 792 elementos contra 820 de hoje; o bloco do drawer sozinho tem 99, então a
> diferença não é só o drawer). São **irreproduzíveis** e por isso substituídas,
> não comparadas. A integridade da Home foi confirmada por outro caminho: o texto
> do `<body>` é idêntico ao de `index.html.bak` mais o bloco do drawer, e as
> alterações no CSS compartilhado desde então são puramente aditivas
> (`.status-badge`, que a Home não usa).

**Como regerar:**
```bash
node baselines/tools/run.js <dir-de-trabalho>     # 6 páginas × 2 viewports, Chrome headless
python3 baselines/tools/extract.py <dir> baselines run1
```
Requer `/Applications/Google Chrome.app` e rede (as fontes do Google Fonts
precisam carregar - o JSON grava `fontsLoaded` para flagrar uma captura offline,
que mudaria a geometria).

### Screenshots full-page (11/09/2026)
Chrome headless `--screenshot` com `--window-size=<largura>,<altura do doc>` dá a
página inteira - mas o Chrome **não aceita janela com menos de ~500px** de
largura: um "375" sai cortado de um layout mais largo. Para mobile, embrulhar
a página num `<iframe width="375">` (mesmo truque do `harness.html` do
fingerprint) e recortar a imagem. Puppeteer não está instalado.

### Limitação do painel de preview

O painel do Claude Code mantém a aba como `document.visibilityState === "hidden"`,
então **nenhum `IntersectionObserver` dispara** - todo conteúdo `.reveal` fica
invisível e o screenshot não acompanha scroll programático. Para inspecionar
visualmente: forçar `.in` em `.reveal/.reveal-stagger` e isolar a seção no topo
com `display:none` nas irmãs. Não é bug do site.

### Fallbacks de reveal (resolvido em 25/08/2026)

O conteúdo de seção nasce com `opacity: 0` e só aparece com o
`IntersectionObserver`. Dois guards no CSS compartilhado:

1. **Sem JS** - `<html class="no-js">` e um script inline logo após `<head>`
   troca a classe para `js`. Se o JS estiver desligado ou falhar, `.no-js`
   permanece e `.reveal` entra visível e estático.
   > `@supports selector(:has())` foi considerado e descartado: feature query
   > de seletor testa suporte do navegador, não se o JS rodou. Não serve de
   > detector. `.no-js` é o mecanismo confiável.
2. **`prefers-reduced-motion: reduce`** - conteúdo visível, animação zerada.
   Como todas as animações usam `forwards`, colapsar a duração para `0.01ms`
   entrega o **estado final** em vez de congelar no inicial.

Aplicado na Home e na CRM. Toda página nova deve nascer com
`<html lang="pt-BR" class="no-js">` + o script inline no `<head>`.

### SEO por página

Cada página carrega `canonical`, `og:url`, `og:title`, `og:description` e
`twitter:*` **apontando para si mesma**, nunca para a Home.
Home → `https://www.nexyss.com/` · CRM → `https://www.nexyss.com/plataforma/crm/`.
(Domínio ainda é placeholder - ver TODO acima.)

### Pendências da página CRM

- `:focus-visible` está escopado em `.page-produto`. Recomendado promover
  para global depois de validado.

---

## Overview `/plataforma/` - o hub

Página **institucional** (`<body class="page-institucional has-subnav">`):
sem `theme-*`, eyebrow ciano, `hero-glow` ciano + brand. É a única página onde
as 6 cores de produto aparecem lado a lado.

### Como ela se diferencia da `#plataforma` da Home

A seção da Home responde **"o que existe?"**. A overview responde
**"como isso funciona junto, e por onde eu entro?"**. O eixo dela é a
**camada compartilhada** - dado, identidade, permissão, IA - que é o que a
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

### Classes de página - resumo

| Classe | O que faz |
|---|---|
| `theme-crm` … `theme-ai` | fornece `--c-color` e derivados |
| `page-produto` | eyebrow/glow/ícones/tags herdam a cor do produto |
| `page-institucional` | mantém o acento ciano; habilita `:focus-visible` |
| `has-subnav` | ativa `scroll-margin-top` nas âncoras. **Não usar `page-produto` para isso** - a overview é institucional e também tem subnav |

### Decisões de conteúdo

- **Comparativo genérico** - "Stack montado", sem nomear concorrente.
- **Evento-exemplo é matrícula** (Educação é o vertical live), seguido de uma
  frase generalizando o padrão para contrato fechado, novo funcionário e lead
  qualificado.

### Links pendentes (404 hoje)

`/plataforma/{educacao,marketing,finance,hr,ai,integracoes}/` já estão
linkados na overview e retornam 404. Só `crm/` existe. Falta criar uma
**página 404 amigável** antes de qualquer publicação.


---

## Página `/plataforma/educacao/`

`<body class="theme-edu page-produto has-subnav">` - 13 seções publicadas.

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
**Nunca** cliente, pipeline, negócio, fatura - esse é o vocabulário da CRM.

### O que difere estruturalmente da CRM

- `#recursos` em **3 clusters** (Acadêmico · Financeiro acadêmico ·
  Experiência e rede) com `.cluster-label`, em vez de lista plana.
- **`#rede` é seção nova** - multi-campus como narrativa central.
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
Home tem 7. Por isso a trajetória usa **6 semestres**, não 7 - estender os
`nth-child` alteraria a animação da Home. Se algum dia precisar de 7+, tem que
ser uma classe nova, não a extensão da existente.

### `#compliance` - NÃO PUBLICADA

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

### Baseline de regressão - resolvido em 04/09/2026

As **4 páginas** (Home, Overview, CRM, Educação) têm fingerprint armazenado em
`baselines/`, nos dois viewports, junto com o gerador. Ver
"Teste de regressão - baselines v2" acima para os hashes e o procedimento.


## Página `/plataforma/marketing/` (14/10/2026)

`<body class="theme-mkt page-produto has-subnav">` - 12 seções, 788 linhas. Molde: CRM.
Header, drawer, Founding e footer são cópias exatas (com `../../assets/`).

### Argumento central
A CRM argumenta **largura** (um cliente visto por todos os módulos), a Educação
**duração** (um aluno por anos). Marketing argumenta **prestação de contas**: o
relatório de campanha que termina onde o contrato começa. O diferencial é a
atribuição ligada a CRM e Finance - receita vinda do contrato e da fatura, não
estimada. Posicionamento "hub completo" (automação, campanhas multi-canal,
conteúdo/CMS, analytics e atribuição), **sem nomear concorrente** (mesma decisão
do comparativo da Overview).

### Seções
Hero (**Visual A `.wf-*`**) · `.subnav` (O problema · Recursos · Atribuição ·
Nexyss AI · Integrações) · `#problema` (3 `.sol-card`) · `#recursos` (2 `lg` + 3
`md`: Automação, Campanhas, Conteúdo, Audiência, Relatórios) · `#atribuicao`
(`.ai-inner` + **Visual B `.attr-*`**, no lugar do `#visao-360` da CRM) · `#ia` ·
`#integracoes` (4 itens) · `#para-quem` (3 `.sol-card`) · impacto (1 · 3 ·
99.99%) · `#clientes` (Founding, sem recolorir) · `.cta-final`.
**Sem logo wall** - decisão de 14/10: nenhum cliente real usa o Marketing (R8), e
o bloco do molde era fictício.

### Badges: 22 bullets, TODOS 🔵 Roadmap
Rigor máximo - sem validação do time técnico não há 🟢. Badgeados: 15 bullets de
`#recursos`, 3 itens de `#atribuicao`, 4 de `#integracoes`. **Sem badge** (R5.1):
hero, headlines, `#problema`, `#ia` (descrições narrativas, como na CRM) e
`#para-quem` (`.sol-tag` de persona, como na CRM). Inventário em CLAIMS-AUDIT.md.

**Linha de disclosure** (`.rm-note`, DM Mono, `--c-text-mute`) abaixo do título de
`#recursos`: *"Os recursos abaixo estão em roadmap. Founding Customers participam
da definição da ordem de entrega."* Não é claim - é transparência estratégica, e
amarra o Founding ao produto. Texto aprovado literalmente.

### CTAs (padrão novo: módulo em `interesse`, CTA em `origem`)
`../../contato/?interesse=marketing&origem=demo|especialista|founding`.
Cobre header, drawer, subnav, hero, Founding e CTA final.

### Componentes novos (seção `=== PÁGINA MARKETING ===` ao fim de `nexyss.css`)
| Componente | Uso |
|---|---|
| `.wf-*` (**Visual A**) | canvas de workflow no hero: gatilho → pontuação → e-mail → condição → CRM / reenvio. 3×3 no desktop, conectores em SVG de fundo (`draw`); ≤760px vira **pilha vertical** e o chip `.pipe-ai` desce para baixo do quadro |
| `.attr-*` (**Visual B**) | dentro de `.acct360`: linha do tempo `.acct-tl` (`.m-mkt/.m-crm/.m-fin`) + barras de receita por canal (`growX`). **Sem valores numéricos** (R3) e marcado "ILUSTRATIVO". As barras só animam ao entrar na tela (`animation-play-state` ligado a `.reveal.in`) |
| `.rm-note` | disclosure de roadmap |

**Zero keyframes novos** (`draw`, `growX`, `floatA`, `floatB`). Tudo escopado em
`.page-produto` (exceto `.theme-mkt .ai-visual`, abaixo).
Gotcha: no mobile o override do `grid-area` precisa de seletor de **mesma
especificidade** que `.wf-node.nN` e vir depois (`.wf-nodes > .wf-node`) - com
`.wf-node` simples o canvas não empilhava.

### 🐞 Bug pré-existente descoberto: `.ai-visual` colapsa para 0×0
O visual de órbitas da Nexyss AI mede **0×0 na Home, Overview, CRM e Educação**
(já nas baselines aprovadas: `ai-visual … [x, y, 0, 0]`). Causa: item de grid com
`margin: 0 auto` + `aspect-ratio` e só filhos absolutos → encolhe a 0. Os
`.ai-node` flutuam sem órbita nem núcleo. **Corrigido só na Marketing**
(`.theme-mkt .ai-visual { width: 100% }`). O conserto global (`.ai-visual { width:
100% }`) mexe na Home e muda os 8 fingerprints das páginas aprovadas -
**aguarda decisão do Jonathan**.

### Bug fix: `origem` do formulário (14/10/2026)
`nexyss.js` gravava em `origem` o valor cru de `?interesse=`; com
`?interesse=marketing&origem=demo` o painel registraria `marketing` e perderia a
CTA. Agora `origem = ?origem= || ?interesse= || 'direto'`, e a mensagem do
Founding dispara com `interesse=founding` **ou** `origem=founding`. As CTAs antigas
(`?interesse=demo`) seguem iguais. Testado em 8 cenários no Chromium.

### Ligações de Marketing nas páginas existentes
13 `href="#"` → página nova: mega-menu, drawer e footer de Home, Overview, CRM e
Educação (12) + card "Explorar" da Home. O card da Overview já apontava para
`marketing/`. Os links irmãos (CRM, Educação…) **continuam `href="#"`**.

### Baselines - ambiente Linux (14/10/2026)
O fingerprint rodou no Chromium do container, **não no Chrome do macOS**, e os
hashes v4 **não reproduzem** em Linux mesmo com a árvore intacta: mesmo nº de
elementos e mesma altura de documento nas 12 capturas, mas o hash difere por
(a) serialização de `font-family` (`BlinkMacSystemFont` → `"system-ui"`) e (b)
subpixel em larguras de texto inline. Procedimento: controle **antes** de editar,
comparação por delta no mesmo ambiente. Resultado: as 12 capturas das páginas
existentes ficaram **idênticas ao controle**. Os hashes Linux estão em
`baselines/README.md`. `baselines/marketing-*.json` são **baseline inicial em
Linux** - a regerar no macOS para entrar na tabela v4 acima. `run.js` aceita
`CHROME=/caminho/do/chrome`.

### Pendências registradas aqui
- **CRM e Educação ainda têm logo wall fictício** (CRM: Globaledu, Atlas Academy,
  Vertex, Polaris, Meridian, Orbital; Educação: Globaledu, Polaris College, Rede
  Meridian, Orbital Schools…). Violação de R3/R8 - corrigir na próxima sessão.
- **Mega-menu de CRM/Educação/Overview ainda tem links irmãos como `href="#"`.**
  Corrigir de uma vez quando criarmos Finance/HR/AI (padronização única).
- ~~`.ai-visual` 0×0 em 4 páginas~~ (corrigido globalmente em 16/10/2026).
- **Demo de módulo em roadmap:** o CTA "Solicitar Demo" do Marketing precisa de
  definição do que a demo mostra, já que 100% dos recursos são 🔵.
- **Recorte do itálico** no último glifo de uma linha dentro de `.accent`
  (`background-clip: text`): pré-existente (Educação tem o mesmo), cosmético.

## Página `/plataforma/finance/` (14/10/2026)

`<body class="theme-fin page-produto has-subnav">` - 12 seções, 812 linhas. Molde: Marketing.
Header, drawer, Founding e footer são cópias exatas (com `../../assets/`).

### Argumento central
CRM argumenta largura, Educação duração, Marketing prestação de contas. Finance
argumenta **fechamento sem reconciliar**: o razão recebe, no instante em que acontecem,
o que os demais módulos já registraram. Headline pensada para o **CFO** (visão
estratégica, controle); o corpo convence o **Controller** (operacional, dia a dia).
H1 aprovado: *"O fechamento que acontece durante o mês, não depois dele."*
Posicionamento "ERP financeiro" **sem nomear concorrente** (mesma decisão do
comparativo da Overview).

### Regra de uso da palavra "ERP"
Entra em `<title>`, `description`, `og:title`/`og:description` e
`twitter:title`/`twitter:description`, e **uma única vez** no corpo (subtítulo de
`#recursos`). **Nunca no H1.** Conferir: `grep -v '<meta\|<title' plataforma/finance/index.html | grep -c ERP` deve dar 1.

### Seções
Hero (**Visual A `.rec-*`**) · `.subnav` (O problema · Recursos · Fluxo de caixa ·
Nexyss AI · Integrações) · `#problema` (3 `.sol-card`) · `#recursos` (2 `lg` + 3 `md`:
Contábil, Fiscal, Pagar e receber, Caixa, Conciliação) · `#caixa` (`.ai-inner` +
**Visual B `.cf-*`**, no lugar do `#atribuicao` do Marketing) · `#ia` · `#integracoes`
(4 itens) · `#para-quem` (CFO, Controller, Tesouraria) · impacto (1 · 3 · 99.99%) ·
`#clientes` (Founding, sem recolorir) · `.cta-final`. **Sem logo wall** (nenhum
cliente real usa o Finance, R8).

### Badges: 22 bullets, TODOS 🔵 Roadmap
15 em `#recursos`, 3 em `#caixa`, 4 em `#integracoes`. Sem badge (R5.1): hero,
headlines, `#problema`, `#ia` e `#para-quem`. Mesma linha de disclosure `.rm-note`
do Marketing, texto idêntico. Inventário em CLAIMS-AUDIT.md.

### Fiscal genérico (decisão de 14/10/2026)
O módulo fiscal é o claim de maior risco: depende do país e a Nexyss opera na
Irlanda, na América Latina e na Europa. A página diz apenas "por país" e
**não nomeia nenhuma obrigação** (nem nota fiscal eletrônica, nem declaração
acessória, nem imposto sobre valor agregado, nem padrão de pagamento europeu, nem
open banking). Só entra nome específico depois que o time técnico validar.

### CTAs
`../../contato/?interesse=finance&origem=demo|especialista|founding`. O select do
contato e o `MAP` do `nexyss.js` já aceitavam `finance`.

### Componentes novos (seção `=== PÁGINA FINANCE ===` ao fim de `nexyss.css`)
| Componente | Uso |
|---|---|
| `.rec-*` (**Visual A**) | conciliação bancária no hero: linhas de 3 colunas (extrato, vínculo, lançamento), 4 pares casados e 1 exceção (laranja = estado de alerta, como no formulário, não a cor do Marketing). Vínculo é SVG por linha com `draw`. Funciona igual no mobile, só encolhe; o chip `.pipe-ai` desce para baixo do quadro |
| `.cf-*` (**Visual B**) | dentro de `.acct360`: barras empilhadas por período (realizado sólido, projetado hachurado, marcador "Hoje") com 3 contas em tons da família violeta, e ao lado a origem da projeção em `.acct-tl` (`.m-crm/.m-edu/.m-mkt/.m-fin`). Reusa `barGrow`; anima só ao entrar na tela |

**Zero keyframes novos.** Mockups sem número: rótulos genéricos ("Fornecedor 1",
"Cliente A", "Conta A") e marca ILUSTRATIVO. Barras de valor no lugar de valores.
Tudo escopado em `.page-produto`, exceto `.theme-fin .ai-visual` (abaixo).

### Rebaixamento de badge na CRM (consistência entre módulos)
O bullet "Fechamento reconhecido direto no Finance" (CRM, `#recursos`, Previsão) era
🟢 Ativo. Como o Finance declara tudo como Roadmap, a CRM passou a 🔵 Roadmap:
rebaixo por consistência entre módulos. A CRM ficou com 12 🟢 + 3 🔵. O "Financeiro
acadêmico" da Educação **não** foi rebaixado: roda dentro do módulo Educação.
Efeito no fingerprint da CRM: rótulo "Roadmap" é mais largo que "Ativo" (+14px no
badge) e no 375px o bullet quebra em 2 linhas (+22px no documento).

### `.ai-visual` 0x0 continua nas 4 páginas
`.theme-fin .ai-visual { width: 100% }` repete o conserto escopado do Marketing.
**Fase dedicada ao fix global do `.ai-visual` pendente**: os fingerprints de 4
páginas (Home, Overview, CRM, Educação) vão mudar quando for resolvido.

### Ligações de Finance nas páginas existentes
16 `href="#"` trocados pela página nova: mega-menu, drawer e footer de Home,
Overview, CRM, Educação e Marketing (15) + card "Explorar" da Home. O card da
Overview já apontava para `finance/`. Total coberto: 17 pontos. Os links irmãos
(CRM, Educação, HR, AI) **continuam `href="#"`**; o Marketing agora também liga para
o Finance e o Finance para o Marketing.

### Baselines (Linux)
Controle capturado antes de editar e comparado depois no mesmo ambiente: as 14
capturas das 7 páginas anteriores ficaram **idênticas**, exceto a CRM (rebaixamento).
`baselines/finance-*.json` são baseline inicial em Linux (duas passadas idênticas).
Tabela de referência atualizada em `baselines/README.md`.

### Pendências registradas aqui
- ~~Fix global do `.ai-visual`~~ (feito em 16/10/2026).
- ~~CRM e Educação ainda têm logo wall fictício~~ (removido em 15/10/2026).
- **Links irmãos `href="#"`** no menu: padronizar de uma vez quando HR e AI existirem.
- **Demo de módulo em roadmap:** definir o que a demo do Finance mostra.
- **Validação técnica** dos 22 bullets do Finance antes de qualquer promoção a 🟢.
- **Contraste do eyebrow violeta** sobre o ponto mais claro do `.tinted`: 4,44:1
  (abaixo de 4,5 por 0,06). Mesmo comportamento de outros temas; cosmético.

## Página `/plataforma/hr/` (14/10/2026)

`<body class="theme-hr page-produto has-subnav">` - 12 seções, 799 linhas. Molde: Finance.
Header, drawer, Founding e footer são cópias exatas (com `../../assets/`).

### Argumento central: "a organização viva"
CRM argumenta largura, Educação duração, Marketing prestação de contas, Finance
fechamento sem reconciliar. HR argumenta **a organização viva: quem está onde, quanto
custa e quando muda, sempre no estado de hoje.**
H1 aprovado: *"A organização inteira no mesmo registro, atualizada no dia em que muda."*

**Por que não "o funcionário inteiro, da candidatura ao desligamento" como eixo:** esse
é o eixo da Educação (uma pessoa acompanhada por anos), e a timeline do ciclo seria,
na estrutura, o hero `.jr-*` da Educação. A frase fica como **mecanismo** (o registro
único que não perde histórico), e o eixo passa a ser a organização inteira e o efeito
de cada mudança nos demais módulos. Persona: **CHRO** pelo panorama (estrutura, custo,
vagas, rotatividade); coordenador e business partner no dia a dia dos cards.

### Seções
Hero (**Visual A `.org-*`**) · `.subnav` (O problema · Recursos · Panorama · Nexyss AI
· Integrações) · `#problema` (3 `.sol-card`) · `#recursos` (2 `lg` + 3 `md`:
Recrutamento e seleção, Admissão e onboarding, Folha e benefícios, Desempenho e
desenvolvimento, Desligamento, na ordem do ciclo) · `#panorama` (`.ai-inner` +
**Visual B `.hc-*`**, no lugar do `#caixa` do Finance) · `#ia` · `#integracoes` (4) ·
`#para-quem` (CHRO, business partner, departamento pessoal) · impacto (1 · 3 · 99.99%)
· `#clientes` (Founding, sem recolorir) · `.cta-final`. **Sem logo wall** (R8).

### Badges: 22 bullets, TODOS 🔵 Roadmap
15 em `#recursos`, 3 em `#panorama`, 4 em `#integracoes`. Sem badge (R5.1): hero,
headlines, `#problema`, `#ia` e `#para-quem`. Mesma linha de disclosure `.rm-note`.
Inventário em CLAIMS-AUDIT.md.

### Folha genérica e zero claim de privacidade
Folha, encargos e obrigações trabalhistas variam por país e dado de funcionário é
dado pessoal. A página diz "por entidade e por país", **não nomeia obrigação, encargo
nem lei**, e **não afirma privacidade nem conformidade**. Sem concorrente nomeado.
"RH" só em texto corrido; o módulo é "Nexyss HR".

### Componentes novos (seção `=== PÁGINA HR ===` ao fim de `nexyss.css`)
| Componente | Uso |
|---|---|
| `.org-*` (**Visual A**) | organograma vivo no hero: Diretoria, 3 áreas e 2 equipes por área. Pessoas são pontos, sem número. 1 equipe com **vaga aberta** (contorno pontilhado magenta, fundo opaco para o conector não aparecer por dentro). Grid de 7 linhas fixas + SVG de fundo com `draw`. No mobile mantém as 3 colunas e só encolhe; o chip `.pipe-ai` desce para baixo do quadro |
| `.hc-*` (**Visual B**) | dentro de `.acct360`: barras horizontais por área divididas em Júnior, Pleno e Sênior (3 tons de magenta), sem eixo e sem valor, mais "quem muda, o que muda" em `.acct-tl`. Reusa `growX` e os tons `cf-s1/cf-s2` do Finance; anima só ao entrar na tela |
| `.acct-tl .m-hr` | cor magenta na linha do tempo (a regra não existia) |

**Zero keyframes novos.** Mockups sem número (rótulos "Área A", "Equipe 4") e marca
ILUSTRATIVO. Tudo escopado em `.page-produto`.

### Token novo: `--c-hr-text: #CA7BEC` (primeiro tom derivado de cor de produto)
O magenta puro `#B84FE5` dá 4,45:1 sobre navy-deep, 3,99:1 sobre navy e 3,47:1 sobre
navy-mid: passa para ícone e gráfico (3:1), mas **reprova AA em texto pequeno**
(eyebrow de 12px). O tom `#CA7BEC` (75% magenta, 25% branco) dá 6,4 / 5,7 / 5,0.
Declarado em `:root` junto de `--c-hr`, mas **só é usado sob `.theme-hr`**: eyebrow,
`<small>` do impacto, `.attr-note b`, hover de `.sol-tag`, rótulo `.src` do `.m-hr`,
e o texto das marcas do organograma. Foi criado por motivo técnico de contraste, não
estético. Se outro tema de produto reprovar o contraste, a decisão é caso a caso.
Contraste dos demais sobre navy-deep: Educação 10,6:1, Finance 5,7:1, Marketing 5,4:1 (passam).

### Consistência entre módulos: zero rebaixamento
Varredura de todos os 🟢 (CRM 12, Educação 5, demais 0): nenhum afirma capacidade de
HR. "Permissões por unidade e por país" (CRM) e "Permissão por campus, programa e
função" (Educação) são da camada compartilhada de identidade, não do HR. **Nenhum
badge foi rebaixado.** Narrativas sem badge sobre HR na Overview ("Contrata e o
acesso já existe no dia um", "um novo funcionário (HR para todos)") e o card de HR da
Home ficam como estão, pela precedente do Finance e pela R5.1.

### CTAs
`../../contato/?interesse=hr&origem=demo|especialista|founding`. O select e o `MAP`
do `nexyss.js` já aceitavam `hr`.

### `.ai-visual` 0x0 continua nas 4 páginas
`.theme-hr .ai-visual { width: 100% }` repete o conserto escopado. **Fase dedicada ao
fix global pendente**: os fingerprints de 4 páginas vão mudar quando for resolvido.

### Ligações de HR nas páginas existentes
19 `href="#"` trocados pela página nova: mega-menu, drawer e footer de Home, Overview,
CRM, Educação, Marketing e Finance (18) + card "Explorar" da Home. O card da Overview
já apontava para `hr/`. Total: 20 pontos. Dos links irmãos, só o de AI continua `#`
em todas as páginas (CRM e Educação seguem `#` nos próprios tiles).

### Baselines (Linux)
Controle capturado antes de editar: as 16 capturas das 8 páginas anteriores ficaram
**idênticas** (zero delta, inclusive a CRM). `baselines/hr-*.json` são baseline inicial
em Linux (duas passadas idênticas). Tabela de referência em `baselines/README.md`.

### Pendências registradas aqui
- ~~Fix global do `.ai-visual`~~ (feito em 16/10/2026).
- ~~CRM e Educação ainda têm logo wall fictício~~ (removido em 15/10/2026).
- **Links irmãos `href="#"`**: falta só a página de AI para padronizar tudo de uma vez.
- **Demo de módulo em roadmap:** definir o que a demo do HR mostra.
- **Validação técnica** dos 22 bullets do HR antes de qualquer promoção a 🟢.
- **H1 longo:** com a copy aprovada o H1 quebra em 6 a 7 linhas no desktop (hero alto).
  Funciona, mas é o hero mais comprido do site.

## Página `/plataforma/ai/` (15/10/2026)

`<body class="theme-ai page-produto has-subnav">` - 12 seções, 731 linhas. Molde: HR.
Header, drawer, Founding e footer são cópias exatas (com `../../assets/`).
**Fecha as 6 páginas de módulo de produto** (CRM, Educação, Marketing, Finance, HR, AI).

### Posicionamento e argumento central
A Nexyss AI é o **motor da plataforma, não um módulo separado**: a camada que atravessa
os demais módulos, não um produto de IA para vender à parte. Frase canônica aprovada:
*"a IA que já está onde você trabalha, não a aba que você precisa abrir"*.
H1 aprovado: *"A IA que mora dentro do seu CRM, do seu Finance e da sua gestão de pessoas
- não em uma aba separada."* Persona: **CEO** na headline (diferencial estratégico) e
**CTO** no corpo (uma camada em vez de uma integração por módulo).

Nota de risco registrada: "mora dentro" e "já está" descrevem **arquitetura**, mas podem
ser lidos como disponibilidade. A página inteira está sob a linha de disclosure de roadmap
em `#recursos` e todos os 20 bullets são 🔵. Evitar reforçar a leitura de disponibilidade
("desde o dia zero", "sem configurar", "já disponível") em qualquer texto novo.

### Seções
Hero (órbita `.ai-visual` + chip `.pipe-ai`) · `.subnav` (O problema · Capacidades · No
registro · Módulos · Integrações) · `#problema` (3 `.sol-card`) · `#recursos` (**4 grupos
pedagógicos** em 4 `.mod-card lg`: Entende, Acelera, Vigia, Decide) · `#registro`
(`.ai-inner` + `.acct360` com `.acct-tl`) · `#modulos` (5 `.mod-card`, cada um na cor do
módulo, **só com link para o `#ia` de cada página**) · `#integracoes` (4) · `#para-quem`
(CEO, CTO, líder de área) · impacto (1 · 3 · 99.99%) · `#clientes` (Founding) ·
`.cta-final`. **Sem logo wall** (R8).

### Os 4 grupos (20 bullets, TODOS 🔵 Roadmap)
- **Entende** (4): linguagem natural, classificação, extração de dados de documentos, busca por significado.
- **Acelera** (4): rascunho, resumo, preenchimento sugerido, resposta a perguntas.
- **Vigia** (4): anomalia, score por registro, previsão de risco e resultado, alertas.
- **Decide** (4): recomendação, otimização, agente, ação registrada no mesmo histórico.
- Mais 4 em `#integracoes` (fontes externas, sistemas do cliente, implantação assistida,
  API e webhooks). Total 20 (16 + 4). Sem badge (R5.1): hero, headlines, `#problema`,
  `#registro`, `#modulos` e `#para-quem`. Mesma linha `.rm-note` das demais páginas.

### ZERO componentes CSS novos (decisão arquitetural)
IA não é produto separado, então a página não tem visual próprio. Reusa `.ai-visual` +
`.ai-orbit*` + `.ai-center` + `.ai-node` (4 nós: n1 a n4, um por grupo), `.pipe-ai`,
`.mod-card`, `.acct360`, `.acct-tl`, `.consult-grid`, `.sol-card`, `.rm-note`. O único CSS
novo é `.theme-ai .ai-visual { width: 100% }` (seção `=== PÁGINA AI ===`), o conserto
escopado do bug 0x0, que aqui é o próprio visual do hero. **Zero keyframes novos.**
O `.ai-chip` citado no briefing **não existe** no CSS; o chip é o `.pipe-ai`.

### Compromisso implícito sobre dados (decisão de 15/10/2026)
A página **não afirma nada sobre modelos, provedores ou armazenamento**. Não usa
privacidade, LGPD, GDPR nem soberania, não nomeia fornecedor nem modelo, e não usa a
palavra "modelo". A linguagem é "a IA opera dentro do mesmo registro que você vê" e
"cada ação fica no mesmo lugar que todo o resto". Deixa porta aberta a qualquer
arquitetura futura. Conferência: `grep -iE 'openai|anthropic|mistral|gemini|llama|gpt|claude|privacid|lgpd|gdpr|soberania|\bmodelo' plataforma/ai/index.html` só pode
acertar o link legal "Privacidade" do rodapé compartilhado.

### Limites de claim (regras que valem para qualquer texto de IA)
Sem número de desempenho, sem "mais rápido" ou "mais barato", sem concorrente nomeado, sem
modelo específico. A página **não reivindica o que a CRM tem como Ativo** ("Construtor
visual, sem código", "Gatilhos entre módulos"): o Decide é agente e recomendação, não
construtor de regra.

### CTAs
`../../contato/?interesse=ai&origem=demo|especialista|founding`. O select e o `MAP` do
`nexyss.js` já aceitavam `ai`.

### Ligações de AI nas páginas existentes
22 `href="#"` trocados pela página nova: mega-menu, drawer e footer de Home, Overview,
CRM, Educação, Marketing, Finance e HR (21) + card "Conhecer Nexyss AI" da Home. Na
Overview o card e o link do `#ia` já apontavam para `ai/`. Total: 24 pontos. Continuam
`href="#"` os tiles de CRM e Educação em todas as páginas e "Integrações & API".

### Baselines (Linux)
Controle capturado antes de editar: as 18 capturas das 9 páginas anteriores ficaram
**idênticas** (zero delta). `baselines/ai-*.json` são baseline inicial em Linux (duas
passadas idênticas). Tabela de referência em `baselines/README.md`.

### Rebaixamento cross-módulo aplicado (15/10/2026)
CRM, bullet "Health score calculado com dado de todos os módulos": 🟢 para 🔵. Motivo: o
grupo Vigia da página de AI declara "Score por registro" como Roadmap, e o score da CRM
depende de dado de Finance e Marketing (Roadmap). CRM: **11 🟢 + 4 🔵**. Mantidos 🟢 os
limítrofes sem termo de IA (forecast em cenários, construtor sem código, gatilhos entre
módulos). Educação, Marketing, Finance e HR: nada a rebaixar. O briefing citava 12 e depois
14 rebaixamentos; a conferência achou 1 (os 2 itens do Finance não existem). Detalhes em
CLAIMS-AUDIT.md. Efeito no fingerprint da CRM: só o badge, sem reflow.

### Pendências registradas aqui
- ~~Home, hero "agora disponível" e `#ia` de CRM e Educação sem disclosure~~ **Resolvido em
  15/10/2026** (seção seguinte).
- ~~Fix global do `.ai-visual`~~ (feito em 16/10/2026).
- ~~Logo wall fictício na CRM e na Educação~~ **Removido em 15/10/2026** (seção seguinte).
- **Links irmãos `href="#"`:** CRM e Educação ligados em 16/10/2026 (mega-menu, drawer e cards). Sobram "Integrações & API", o item "Educação" do mega-menu Soluções e o footer inteiro de CRM e Educação.
- **Contraste do link `.mod-link` por módulo** em `#modulos` (e na Overview): HR magenta
  e Finance violeta ficam entre 3,5 e 4,4:1 em texto de 12px sobre o card. Padrão
  pré-existente do `.mod-card`; o tom `--c-hr-text` só existe sob `.theme-hr`.
- **H1 longo** (7 linhas no desktop), o hero mais alto do site.
- **Perguntas técnicas de CTO sem resposta na página** (backlog de validação): uso de dado
  do cliente em treinamento, retenção, residência, escolha e troca de modelo.

## Correção pós página AI: Home, CRM e Educação (15/10/2026)

Correção pós página AI publicada: resolve a contradição entre a promessa de IA disponível
e a realidade Roadmap (a página de AI tem 20 bullets, todos 🔵).

- **Home, hero** (`.hero-tag`): "Nexyss AI agora disponível em todos os módulos" passou a
  "Nexyss AI em construção, chegando em todos os módulos". Mantém a promessa, honesto sobre
  o estado. Única mudança na Home (o pill "Novo" não foi tocado).
- **CRM e Educação, `#ia`**: nova linha `.rm-note` (mesma classe e texto da Marketing, Finance,
  HR e AI) logo abaixo do parágrafo de abertura da seção e antes de `.ai-products`. Chaves
  `crm.ia.note` e `edu.ia.note`. Nenhuma copy existente foi reescrita; zero CSS novo.
  Nesses `#ia` a estrutura é `.ai-inner`, não `.section-head`; o `.rm-note` herda a cor do
  produto pela borda esquerda via `--c-color`, como nas demais páginas.
- **Fingerprint (Linux, controle antes de editar):** Home mesmo nº de elementos e mesma altura
  (só a largura do texto do hero muda); CRM e Educação +1 elemento cada. As outras 7 páginas
  (14 capturas) idênticas.

## Remoção do logo wall fictício da CRM e da Educação (15/10/2026)

As duas páginas exibiam 6 organizações inventadas cada (CRM: Globaledu, Atlas Academy, Vertex,
Polaris, Meridian, Orbital; Educação: as mesmas com sufixos, como "Rede Meridian") sob
"operam na Nexyss". Violação de R3 e R8, aberta desde a fase Marketing.

- **Decisão:** remover a `<section class="logos">` inteira nas duas páginas, sem substituir.
  Mesmo critério de Marketing, Finance, HR e AI: nenhum cliente real está confirmado como
  usuário do módulo, e associar os 5 clientes reais sem confirmação repetiria a violação.
  O `#clientes` (Founding) continua fechando a página.
- **Escopo:** 14 linhas removidas em cada página. Zero CSS, zero mudança na Home. O CSS
  `.logos` segue em uso pela Home. A ordem de seções do molde (item 3, `.logos`) passa a
  valer só para quem tiver cliente real confirmado.
- **Mockups preservados:** "Meridian", "Atlas Academy" etc. dentro do kanban e da ficha 360
  da CRM são nomes de negócio de exemplo, não claim de cliente.
- **Fingerprint (Linux, controle antes de editar):** CRM 916 para 890 elementos, doc 1280
  -236px, 375 -302px. Educação 1063 para 1036, 1280 -236px, 375 -321px. As outras 8
  páginas (16 capturas) idênticas.
- **Para reintroduzir** quando houver cliente real do módulo: recriar a seção como na Home
  (`.logos-grid.centered`, `data-client`, placeholder textual até chegar o logo).

## Fix de navegação CRM e Educação (16/10/2026)

Relato: os links de CRM e Educação no menu não abriam. As duas páginas existem e estão
versionadas (`plataforma/crm/index.html` 51564 bytes e `plataforma/educacao/index.html` 59519 bytes).

- **Causa raiz:** os links nunca foram ligados. Estavam como `href="#"` desde a criação do
  mega-menu e do drawer, deixados de propósito para "padronizar de uma vez" (pendência dos
  links irmãos). Não era `href="./"` apontando para a página atual: o diagnóstico mediu `#`.
- **Alcance antes:** 88 links com texto ou destino de CRM ou Educação nas 10 páginas
  publicadas (as 9 do roteiro mais `contato/obrigado.html`). Só 4 funcionavam (cards
  "Explorar" da Overview e links "Ver a IA no..." da página de AI).
- **Correção (42 links, só o atributo `href`):** mega-menu Plataforma, drawer e cards
  "Explorar" da Home, em todas as 10 páginas. Caminhos relativos pela profundidade:
  Home `plataforma/crm/`; Overview `crm/`; páginas `plataforma/*/` `../crm/`; a própria
  página usa `./`; `contato/` `../plataforma/crm/`. Mesma lógica para Educação.
- **Não tocado, por decisão:** footer (ver abaixo), "Integrações & API", e o item "Educação"
  do mega-menu Soluções (por setor, página ainda inexistente).
- **Correção de premissa:** o briefing dizia que os links do footer já estavam corretos. A
  medição mostrou que o footer de CRM e Educação também é `href="#"` (3 por página, nas 10
  páginas). Ficou para decisão do Jonathan.
- **Validação:** script resolve cada href contra o disco: 46 links para CRM ou Educação fora
  do footer, todos resolvem (0 quebrados). Normalizando todos os `href`, as 10 páginas ficam
  byte a byte iguais ao antes. Fingerprint das 10 páginas, 20 capturas, idêntico ao controle.

## Fix global do `.ai-visual` (16/10/2026)

Fecha a dívida técnica do `.ai-visual` 0×0 (Home, Overview, CRM e Educação).

- **Causa raiz (confirmada por medição):** `.ai-visual` é item de grid (`.ai-inner`) com
  `margin: 0 auto` + `aspect-ratio: 1` e só filhos `position: absolute`. Sem largura
  explícita, a largura vira "ajustar ao conteúdo" (zero) e a altura herda zero pelo ratio.
- **Correção:** `width: 100%` na regra base `.ai-visual` (`assets/nexyss.css`), com
  comentário explicando o porquê. O `max-width: 480px` existente limita no desktop.
- **Removidas as 4 regras escopadas** (`.theme-mkt`, `.theme-fin`, `.theme-hr`, `.theme-ai`),
  todas idênticas (`width: 100%`, uma linha cada) e agora redundantes. A seção `=== PÁGINA AI ===`
  do CSS ficou só com o comentário de cabeçalho.
- **Alternativa testada e descartada:** `min-height: 420px`. Medido em Chromium: funciona
  só porque o `aspect-ratio` converte a altura mínima em largura mínima, encolhe Marketing,
  Finance e HR de 480 para 420 e passa de 335px no container mobile. Não existe `.ai-stage`.
- **Medição (computada, 8 páginas):** 480×480 em 1280 e 335×335 em 375, em todas. Sem
  transbordo horizontal (`scrollWidth` igual à viewport).
- **Fingerprint (Linux, controle antes de editar):** Home, Overview, CRM e Educação mudam de
  hash nos dois viewports, sem mudar nº de elementos. Em 1280 o documento não muda de altura
  (a linha do grid já era mais alta que o visual); em 375 cresce 335px nas 4. Marketing, Finance,
  HR, AI, Contato e Obrigado idênticas.
- **Baselines:** `home-*`, `overview-*`, `crm-*` e `educacao-*.json` regravados em Linux.
- **Home:** mudança aprovada explicitamente pelo Jonathan nesta fase (a órbita passa a
  aparecer na seção Nexyss AI).
- **Registro de um erro de processo:** em sessão anterior a pendência foi descrita como
  "fantasma" (já renderizando 480×480 e 335×335 nas 4 páginas antigas), com base em dados
  que não correspondiam ao código (medidas, markup e versão de navegador citados não
  existem). A medição real de 16/10/2026 na `main` `ce5bfb6` confirmou o bug: Home,
  Overview, CRM e Educação em 0×0 nos dois viewports, e só Marketing, Finance, HR e AI em
  480×480 e 335×335 (por causa das regras escopadas). Foi isso que viabilizou o fix.
- **Medição pós-fix (8 páginas com `.ai-visual`):** 480×480 em 1280 e 335×335 em 375 em
  todas, e `scrollWidth` igual à viewport (zero transbordo horizontal).

## Bug fix: logo em branco (11/09/2026)

**Sintoma reportado:** logo "em branco/quebrado" no navegador, nas 4 páginas.

**Causa raiz:** `.brand img` e `.footer-brand img` aplicavam
`filter: brightness(0) invert(1)` sobre `nexyss-logo.png`. O filtro zera o RGB
e inverte - alfa preservado, cor interna destruída. O wordmark azul virava
branco (intenção original), mas o **isotipo** - octógono com gradiente
azul→ciano→verde - virava um octógono branco chapado. Não era caminho quebrado
(4/4 resolviam) nem alfa mal configurado. O comportamento é idêntico em
`file://` e HTTP.

**Correção aplicada (aprovada pelo Jonathan):**
- 12 `<img>` (header + drawer + footer × 4 páginas): `nexyss-logo.png` →
  `nexyss-logo-white.png`.
- `assets/nexyss.css` linhas 200 e 1242: `filter` removido, `opacity 0.95 → 1`.
- `og:image` / `twitter:image` **mantidos** em `nexyss-logo.png` - preview de
  link é sobre fundo claro; wordmark branco ficaria invisível ali.

**Verificação:** fingerprint pré (8/8 = v2) → pós: 3 elementos por página,
só `opacity`. Visual conferido em 1280 (header Home) e 375 (header CRM, drawer)
+ DOM do footer. Baselines regravados como v3.

**Backlog:** extrair vetor do `NEXYSS.pdf` → `nexyss-mark.svg` +
`nexyss-wordmark.svg` com `currentColor` (nítido em retina, mais leve, colorível).

## Página `/contato/` (11/09/2026)

`<body class="page-institucional page-contato">` - 5 seções: hero compacto
(1 coluna, sem CTA - a página inteira é o CTA) · `#formulario` (form + canais no
**próprio `.hero-inner`** - zero componente novo; 1.45fr/1fr no desktop,
1 coluna ≤1080; coluna direita sticky) · `#clientes`
(3 setores) · `#faq` (4 `<details>` nativos, sem JS) · footer. Sem subnav.
Sucesso: `/contato/obrigado.html` (`noindex`, reusa o hero, CTA WhatsApp + Home).

### Contatos oficiais
- E-mail: `contato@nexyss.com` · WhatsApp Business: `+353 83 094 7907` (Irlanda,
  `wa.me/353830947907`) · LinkedIn: `linkedin.com/company/nexyss-group`.
- **Na página só o e-mail está publicado** (decisão 11/09/2026): WhatsApp e
  LinkedIn foram removidos da coluna de canais, do CTA da `obrigado.html` e da
  resposta 1 da FAQ porque os dois links **não foram validados**. A coluna
  direita ficou: e-mail · "Respondemos em até 24 horas úteis" · "O que acontece
  depois" (3 passos, reusando `.founding-benefits`). Grid do form passou a
  `1.45fr / 1fr` (form ganha peso) - e esse override **precisa ser repetido dentro
  do `@media (max-width:1080px)` com `1fr`**, senão vence o colapso base do
  `.hero-inner` (bug pego no screenshot mobile em 11/09, corrigido).

### Netlify Forms - como está e o que precisa no painel
`<form name="contato" method="POST" action="/contato/obrigado.html"
data-netlify="true" netlify-honeypot="bot-field">` + `<input type="hidden"
name="form-name" value="contato">` (explícito porque não há build) + honeypot
como a doc pede: **input de texto** dentro de `<p class="visually-hidden">`
(`type="hidden"` alguns bots ignoram). Campos: `nome` (req, minlength 3) ·
`email` (req, type=email) · `empresa` (**opcional**, asterisco de "recomendado")
· `interesse` (select req, 9 opções, valor = rótulo em PT) · `mensagem`
(req, minlength 10) · hidden `origem`.

**`/form-detect.html` na raiz** (comentário no topo: *do not link, do not delete*):
cópia estática só com os campos do form, para o Netlify registrar "contato" no
deploy mesmo que a página de contato mude. Mesmos 8 `name=` do form real -
**se divergirem, o painel mostra o último conjunto lido**. Não linkado; 404 via
`netlify.toml`. Redundante para site estático (o Netlify já lê `contato/index.html`),
mas inofensivo.

⚠️ **Detecção de formulário é opt-in no painel** (Site configuration → Forms →
Enable form detection) **e exige redeploy depois de ativar**. Sem isso o POST
retorna 404. Não existe chave no `netlify.toml` para isso. Free: 100 envios/mês.

### `?interesse=` - pré-seleção (JS em `nexyss.js`, guardado por `if (form)`)
`demo` e `founding` → "Plataforma completa" · `especialista` → "Ainda não tenho
certeza" · slugs de módulo (`crm`, `educacao`, `marketing`, `finance`, `hr`,
`ai`, `consultoria`, `plataforma`) → o módulo. O hidden `origem` recebe o
valor de `?origem=` se houver, senão o cru de `?interesse=`, senão `direto`
(fix de 14/10/2026), para o painel dizer qual CTA gerou o lead. Links por
produto usam os dois: `?interesse=marketing&origem=demo`.
`founding` (em `interesse` **ou** em `origem`) também pré-escreve na mensagem
"Tenho interesse no programa Founding Customers." (editável).

### Validação
HTML5 nativa (bolha do navegador continua). Estilo de erro em **laranja
`--c-mkt`** - aqui é *estado*, não a cor do módulo Marketing: a paleta não tem
vermelho e não criamos token (decisão 11/09). `:user-invalid` e
`.show-errors :invalid` em regras **separadas** (navegador sem `:user-invalid`
descartaria a lista inteira). O JS liga `.show-errors` no evento `invalid`
(capture) e desliga quando o form volta a ser válido.

### CTAs unificadas (31 links nas 4 páginas + contato)
| CTA | Destino (relativo à profundidade da página) |
|---|---|
| "Solicitar Demo" (18, inclui os 6 `#demo` de hero/subnav) | `contato/?interesse=demo` |
| "Falar com Vendas" → **renomeado** "Falar com Especialista" (5, `data-i18n` `cta.especialista`) | `contato/?interesse=especialista` |
| "Candidatar-se" (4) | `contato/?interesse=founding` |
| Footer "Contato" (4) | `contato/` |

Na própria `/contato/`, header e drawer apontam para `#formulario` (não
recarregar a página com o form preenchido). Links **relativos** para continuar
funcionando em `file://`; só o `action` do form é raiz-absoluto (POST não roda
em `file://` de qualquer forma).

### Clientes reais (fornecidos pelo Jonathan, 11/09/2026)
| Setor | Cor (token existente) | Clientes |
|---|---|---|
| Educação | `--c-edu` ciano | NED College |
| Esporte | `--c-crm` verde | Dublin Volleyball Club · Volley Point |
| Turismo | `--c-ai` azul-elétrico | Excursion LTD · Eirway |

Placeholders textuais (`.client-card > .logo-placeholder`, Sora 600 1.2rem) na
página de contato e `.logo-item.{edu,sport,travel}` no logo wall da Home
(`.logos-grid.centered` - **3 na primeira linha + 2 centralizados** no desktop,
coluna única ≤760; sem card inventado para fechar 6, por R3). **Troca por logo
real = substituir o `<span class="logo-placeholder">`/texto pelo
`<img src="assets/clients/<slug>.svg">`**; o container fica igual. Slugs em `data-client`.
FAQ: cada `<details class="faq-item">`.

### Logo wall fictício da Home - violação de R3 corrigida
A Home no ar exibia 6 clientes **inventados** (Globaledu, Atlas Academy, Vertex,
Polaris, Meridian, Orbital) sob "Confiado por organizações inovadoras no mundo
todo". A auditoria de 04/09 não pegou. Substituídos pelos 5 reais em 11/09 com
o label "Organizações que operam com a Nexyss". (O "Meridian" que sobra no CRM é
nome de negócio no mockup do pipeline, não claim de cliente.)

### FAQ - compromissos operacionais do Jonathan Braian (não são claims auditáveis)
"24 horas úteis", "minutos no horário comercial (Dublin, GMT)", "conversa de
30-60 min", "proposta em até 7 dias úteis", "clientes na América Latina e
Europa" são **compromissos de atendimento assumidos pelo Jonathan em 11/09/2026**,
não métricas de produto. Fora do escopo de R3 e do CLAIMS-AUDIT. Se algum deixar
de ser cumprível, mudar a FAQ - não badgear.

### TODOs abertos desta página
- **Reintroduzir WhatsApp Business e LinkedIn quando validar
  `wa.me/353830947907` e `linkedin.com/company/nexyss-group`.** Endereços
  exatos: `contato@nexyss.com` · `wa.me/353830947907` (+353 83 094 7907) ·
  `linkedin.com/company/nexyss-group`. Onde voltam: coluna `.contact-side`
  (dois `.ai-product` depois do e-mail - ícones já existiam no commit anterior
  ao 11/09, ver histórico do git), CTA primário da `obrigado.html` ("Adiantar
  pelo WhatsApp") e resposta 1 da FAQ ("Se é urgente, use o WhatsApp - atendemos
  em minutos durante o horário comercial").
- **Configurar a caixa `contato@nexyss.com`** (Google Workspace / Zoho) antes
  de trocar o domínio placeholder pelo real - hoje o `mailto:` faz bounce.
- **Substituir os placeholders textuais** dos 5 clientes por SVG/PNG quando chegarem
  (`assets/clients/`, 7 pontos: 5 na contato + 5 no wall da Home - mesmo slug).
- Menu do header nas páginas internas aponta para `#consultoria`/`#clientes`,
  âncoras que só existem na Home - pré-existente, fora deste escopo.

## Regras de Conteúdo e Comercial (definidas em 04/09/2026)

### R1 - Naming e pricing de produtos

- **Nexyss CRM** é o único módulo com **pricing público**: €15,99 / €10,99 /
  Enterprise custom.
- **Todos os outros** - Educação, Marketing, Finance, HR, AI - e a **Consultoria**
  são **venda por projeto / custom**.
- Sempre escrever **"a partir de €X"**. Nunca preço fechado.

### R2 - Preços não aparecem no site

- **Nenhuma página do site institucional expõe preço.** Inclusive a do CRM.
- CTA padrão de todo módulo: **"Falar com Especialista"** ou **"Solicitar Demo"**.
- Os preços do CRM vivem em **materiais comerciais externos** - banners, campanhas,
  PDFs, propostas.
- Racional: alinhamento com o posicionamento enterprise. Salesforce, HubSpot e
  Monday não expõem preço detalhado no site institucional.

### R3 - Métricas quantitativas

- **Proibido inventar número de impacto** - "X% de redução", "Y× mais rápido",
  "$Z de economia". Sem case real medido, o número não existe.
- Métrica de impacto só entra quando houver **case real, medido e publicável**.
- **Métrica técnica verificável é permitida**: uptime/SLA, idiomas suportados,
  número de módulos, cobertura geográfica declarada.

### R4 - Vocabulário de idiomas

- Em **label numérico** (`.impact-strip`, `.hero-meta`): **"Multi-idioma nativo"**.
  Sempre no singular - nunca "Multi-idioma nativos".
- Em **texto corrido**: especificar - **"Português, Inglês e Espanhol"**.
- **Nunca usar `PT · EN · ES` como formato canônico.** (Foi testado em 04/09/2026
  nos labels e revertido: cabia, mas não é o vocabulário da marca.)
- Em contexto muito estreito onde "Multi-idioma nativo" não couber, aceita-se
  **"Multi-idioma"**. Medido: o rótulo completo mede 148px em caixa alta e cabe
  na coluna mais estreita do site hoje (159,5px, `.hero-meta.cols-2` a 375px).

### R5 - Sistema de badges de status

Componente `.status-badge` (em `assets/nexyss.css`), 4 estados:

| Badge | Modificador | Cor | Rótulo |
|---|---|---|---|
| 🟢 | `--live` | verde `--c-crm` | **Ativo** - existe e funciona hoje |
| 🟡 | `--beta` | laranja `--c-mkt` | **Beta** - teste com Founding Customers |
| 🔵 | `--roadmap` | azul `--c-ai` | **Roadmap** - comprometido, com data |
| ⚪ | `--planned` | branco 40% | **Planejado** - no radar, sem data |

- O rótulo 🟢 é **"Ativo"**, nunca "Disponível" - 5 caracteres contra 10, mais
  curto que "Roadmap" (7), o que evita reflow dos bullets. (Trocado em 04/09/2026.)
- **`CLAIMS-AUDIT.md` é a fonte de verdade** de qual claim tem qual status.
  Consultar **antes** de aplicar qualquer badge novo.
- **Sem validação do time técnico = fica 🔵.** Nunca 🟢 por inferência.
  Racional: em due diligence enterprise, afirmar 🟢 e não ter é muito pior que
  o contrário.
- No bloco `.founding` - único fundo claro do site - usar a variante
  `.founding .status-badge` (branco sobre navy 35%). O badge padrão reprova em
  contraste ali (1.57:1 a 2.12:1 contra os 4.5:1 de AA).

#### R5.1 - Badge vs. descrição de serviço

Badge marca **feature específica verificável** - afirmação binária "faz X" /
"não faz X". **Descrição narrativa de serviço ou oferta** (o parágrafo que conta
o que uma prática de consultoria entrega) **não recebe badge**: a existência dela
no site já implica disponibilidade.

| | Exemplo |
|---|---|
| ✅ Badgeável | "Sync bidirecional Google Workspace" → 🟢 Ativo |
| ✅ Badgeável | "Exportação e-MEC" → 🔵 Roadmap |
| ❌ Não badgeável | "Diagnóstico organizacional, roadmap de transformação digital e redesenho de processos com foco em dados e IA" |
| ❌ Não badgeável | descrição institucional, tagline, proposta de valor |

**Adendo - a distinção é a granularidade da afirmação, não o tipo da seção.**
Se uma oferta de serviço passar a listar recursos específicos em bullets (dentro
de Managed Services, por exemplo: "SLA 24/7", "monitoramento proativo"), **esses
bullets voltam a ser badgeáveis**.

### R6 - Sem travessões (definida em 14/10/2026)

Nunca usar U+2014 (travessão longo), U+2013 (travessão curto), U+2015 (barra
horizontal) nem U+2212 (sinal de menos tipográfico) em texto novo, nem as entidades
HTML equivalentes (mdash, ndash, minus, horbar). Usar hífen ASCII simples (-).

- **Motivo:** o travessão longo virou "assinatura visual" de texto gerado por AI, e
  muitos leitores conservadores julgam negativamente sem conhecer os benefícios.
- **Escopo:** copy visível, meta tags (SEO, og, twitter), comentários de HTML, CSS,
  JS e toml, e documentação interna (`*.md`).
- Em intervalos numéricos também vale o hífen: `30-60 min`, `300-700`.
- Cuidado em markdown: linha que **começa** com hífen vira bullet. Se uma frase
  continua na linha seguinte, juntar as linhas em vez de abrir a linha com `-`.
- **Conferência** (tem que dar zero; os caracteres vão por escape para esta linha
  não se autodenunciar):
  ```bash
  LC_ALL=C.UTF-8 grep -rnP '[\x{2013}\x{2014}\x{2015}\x{2212}]' --exclude-dir=.git --exclude='*.png' .
  ```
  O mesmo vale para as entidades `&` + `mdash;`/`ndash;`/`minus;`.
- A remoção inicial (498 caracteres em 16 arquivos, mais 5 entidades) foi mecânica:
  hífen é mais estreito que o travessão, então alguns títulos e parágrafos reflowaram.

## Regras de Trabalho

1. **A Home é território protegido - mudança só por decisão explícita do Jonathan.**
   Nada de refatorar, "melhorar" ou reorganizar o CSS existente por conta própria.
   > Histórico: a regra original era "NUNCA mudar o visual da Home". Ela foi
   > **superada em 04/09/2026** pela auditoria de claims, que o Jonathan mandou
   > aplicar também na Home (remoção do bloco de impacto, idiomas, alcance
   > geográfico, Founding Customers, consultoria). O baseline foi regerado depois.
   > A proteção continua valendo contra mudança **não solicitada**.
2. **SEMPRE reutilizar o design system acima** - mesmos tokens, mesmas classes,
   mesmos keyframes. Nada de variantes novas sem combinar antes.
3. **SEMPRE confirmar antes de criar qualquer arquivo ou página nova.**
4. **SEMPRE mostrar preview/plano antes de gerar código longo.**
5. **Uma página por vez**, validando com o Jonathan entre cada uma.
6. Idioma de trabalho: **português**.
7. Todo texto novo nasce com `data-i18n`.
8. **Nunca inventar métrica nem nome de cliente.** Os únicos clientes citáveis
   são os 5 fornecidos pelo Jonathan em 11/09/2026 (ver "Clientes reais" abaixo).
   Números em página só podem ser fatos verificáveis (capacidade de produto,
   SLA, cobertura) ou os já aprovados na Home. Na dúvida, perguntar ao Jonathan.
9. Testar sempre nos dois extremos: **375px** (drawer) e **1280px** (desktop),
   confirmando que o desktop não mudou.
