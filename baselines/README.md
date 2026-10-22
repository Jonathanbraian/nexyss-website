# Baselines de fingerprint - Nexyss

## 1. O que são

Cada `.json` aqui é a **assinatura estrutural e visual** de uma página aprovada,
capturada em dois breakpoints: **1280×800** (desktop) e **375×812** (mobile).

São 20 arquivos - 10 páginas × 2 viewports (Marketing, Finance, HR e AI entraram em 14-15/10/2026,
geradas em **Linux**, ver "Ambiente" abaixo):

```
home-1280.json      overview-1280.json    crm-1280.json     educacao-1280.json    contato-1280.json    obrigado-1280.json
home-375.json       overview-375.json     crm-375.json      educacao-375.json     contato-375.json     obrigado-375.json
```

Cada arquivo guarda, para **todo elemento** do DOM: tag, classe, id, geometria
(x, y, largura, altura) e **28 propriedades computadas** (display, position,
tipografia, cor, borda, transform, grid…). A captura roda no Chrome headless com
as animações desligadas e todo `.reveal` forçado para `.in`, para que o resultado
seja determinístico.

No topo de cada JSON:

| Campo | Significado |
|---|---|
| `fingerprint` | `<nº de elementos>:<hash FNV-1a de 32 bits>` - a assinatura |
| `document` | dimensões totais do documento, ex. `1280x7768` |
| `count` | número de elementos capturados |
| `fontsLoaded` | `loaded` se as fontes do Google Fonts carregaram na captura |

> ⚠️ **O fingerprint não cobre texto.** Ele captura estrutura, geometria e estilo.
> Trocar "9 idiomas" por "3 idiomas" **não muda o hash** se o texto ocupar o mesmo
> número de linhas. Mudança de copy precisa ser verificada por `grep`/diff à parte.

## 2. Como usar

```bash
# 1) captura as 6 páginas × 2 viewports num diretório de trabalho
node baselines/tools/run.js /tmp/fp-check

# 2) extrai os hashes (não grava baseline: use "-" como destino)
python3 baselines/tools/extract.py /tmp/fp-check - check
```

Requisitos: `/Applications/Google Chrome.app`, Node e **rede** - sem as fontes do
Google Fonts a geometria muda e o hash não bate (confira `fontsLoaded`).

Para **regravar** os baselines depois de uma mudança aprovada, troque o `-` pelo
diretório `baselines`:

```bash
python3 baselines/tools/extract.py /tmp/fp-check baselines run1
```

**Regravar baseline só depois de aprovação humana da mudança visual.** Baseline
atualizado sem aprovação transforma regressão em "novo normal" silencioso.

## 3. Quando comparar

- **Antes de qualquer commit que toque `assets/nexyss.css` ou `assets/nexyss.js`** -
  são compartilhados: uma regra sem escopo atinge as 4 páginas de uma vez.
- **Depois de aplicar retrofit de badges** ou qualquer edição em lote.
- **Depois de mexer em componente reutilizado** (`.mod-card`, `.impact-strip`,
  `.hero-meta`, `.sol-card`, `.subnav`, `.founding`…).
- **Antes de publicar.**

## 4. Interpretando o delta

| Resultado | Leitura | Ação |
|---|---|---|
| **Zero delta** ✅ | página intocada | seguir |
| **Delta esperado** ✅ | bate com a mudança intencional e documentada | conferir elemento a elemento, depois regravar o baseline |
| **Delta inesperado** ⚠️ | mudou algo que você não pediu | **investigar antes de commitar** - quase sempre é regra CSS sem escopo vazando |

Confirmar que o delta é o esperado quer dizer **contar**: remover um
`.impact-item` tira 4 elementos (o item + `.n` + `<small>` + `.l`); remover a
seção inteira tira 19. Se a conta não fecha, alguma outra coisa mudou junto.

Para diff elemento a elemento entre um baseline e uma captura nova, os scripts em
`tools/` produzem o JSON completo - compare os campos `elements[]` por
`(tag, classe, id)`.

## Ambiente: macOS vs Linux (14/10/2026)

Os hashes dos JSON acima foram gerados no **Chrome do macOS**. No Chromium do
Linux eles **não reproduzem**, mesmo com a árvore intacta: o nº de elementos e a
altura do documento batem nas 12 capturas, mas o hash difere por (a)
`font-family` serializado diferente (`BlinkMacSystemFont` → `"system-ui"`) e (b)
subpixel em larguras de texto inline. Em Linux, compare **antes × depois no
mesmo ambiente**, não contra o JSON do macOS. Use `CHROME=/caminho/do/chrome node
baselines/tools/run.js <dir>`.

Referência Linux atual (Chromium 1194, fontes `loaded`, árvore de 16/10/2026 com a página Integrações). Compare **antes × depois no mesmo
ambiente** contra esta tabela:

| Página | 1280×800 | 375×812 |
|---|---|---|
| Home | `799:dd0853d2` (doc 1280x7961) | `799:72bccf40` (doc 375x13403) |
| Overview | `867:69eebd38` (doc 1280x10735) | `867:416006f4` (doc 375x17477) |
| CRM | `903:c61ea911` (doc 1280x9510) | `903:f3eb3b58` (doc 375x15994) |
| Educação | `1049:1372e9ed` (doc 1280x11702) | `1049:5b62a25b` (doc 375x19321) |
| Contato | `596:ca9e8b0d` (doc 1280x3736) | `596:d2d6a8f7` (doc 375x5833) |
| Obrigado | `448:be53e34c` (doc 1280x1287) | `448:6c494350` (doc 375x2240) |
| Marketing | `868:175f8d9a` (doc 1280x9437) | `868:8dab60e4` (doc 375x16326) |
| Finance | `943:b23ef52a` (doc 1280x9485) | `943:0e2989e2` (doc 375x16176) |
| HR | `908:a1442c32` (doc 1280x9734) | `908:b9cf44c7` (doc 375x16019) |
| AI | `781:a8aedd7d` (doc 1280x9521) | `781:b2319f2e` (doc 375x15900) |
| Integrações | `869:80c999be` (doc 1280x10838) | `869:30a83001` (doc 375x17604) |
| Soluções | `528:bc9ddfa5` (doc 1280x3906) | `528:f2ccf828` (doc 375x5839) |
| Soluções por Setor | `661:32770f37` (doc 1280x8458) | `661:020b475c` (doc 375x12558) |
| **Soluções por Função** (baseline inicial) | `689:762e9e8f` (doc 1280x9799) | `689:e2c53be7` (doc 375x13899) |
| **Soluções por Objetivo** (baseline inicial) | `701:4b357b3d` (doc 1280x9616) | `701:097cc582` (doc 375x13722) |
| **Soluções por Porte** (baseline inicial) | `653:601e2163` (doc 1280x7993) | `653:3e70aeaa` (doc 375x11723) |
| **Nexyss Consultoria** (baseline inicial) | `780:54d73a47` (doc 1280x9858) | `780:0697fe52` (doc 375x16541) |

**7 hashes mudaram com a remoção dos travessões** (o hífen é mais estreito, então
houve reflow). Valores anteriores, da captura Linux de 14/10/2026 antes da troca:

| Página | Viewport | Antes | Depois | Causa |
|---|---|---|---|---|
| Overview | `867:69eebd38` (doc 1280x10735) | `867:416006f4` (doc 375x17477) |
| Educação | `1049:1372e9ed` (doc 1280x11702) | `1049:5b62a25b` (doc 375x19321) |
| Contato | `596:ca9e8b0d` (doc 1280x3736) | `596:d2d6a8f7` (doc 375x5833) |
| CRM | `903:c61ea911` (doc 1280x9510) | `903:f3eb3b58` (doc 375x15994) |
| CRM | `903:c61ea911` (doc 1280x9510) | `903:f3eb3b58` (doc 375x15994) |
| Marketing | `868:175f8d9a` (doc 1280x9437) | `868:8dab60e4` (doc 375x16326) |
| Marketing | `868:175f8d9a` (doc 1280x9437) | `868:8dab60e4` (doc 375x16326) |

Home, Obrigado, Educação 1280, Contato 1280 e Overview 375 ficaram idênticas.
**CRM mudou de novo em 14/10/2026 (fase Finance):** o bullet "Fechamento reconhecido
direto no Finance" passou de Ativo para Roadmap (1280: `915:e334705f` para `915:55bd3f7c`,
largura do badge; 375: `915:a2843876` para `915:b10f55e3`, bullet em 2 linhas, doc +22px).
As demais páginas ficaram idênticas. `crm-*.json` continua sendo o do macOS.

`marketing-*.json` foi regravado depois da troca e vale como baseline inicial em
Linux. Regerar no macOS para uniformizar com os demais. `finance-*.json` segue o mesmo
critério (baseline inicial em Linux, duas passadas idênticas). `hr-*.json` e `ai-*.json` também.
Na fase HR as 16 capturas das 8 páginas anteriores ficaram **idênticas** ao controle.

## Histórico

- **04/09/2026** - baselines v2 criados. Os hashes v1 da Home (`792:…`) foram
  aposentados: o script que os gerou nunca foi salvo e era irreproduzível.
  Ver `CLAUDE.md` → "Teste de regressão - baselines v2".
- **11/09/2026** - v3: correção do logo (só `opacity` em 3 `<img>` por página).
  v4 no mesmo dia: página `/contato/` + `obrigado.html` entram nas ferramentas
  (`run.js`, `extract.py`); CTAs, "Falar com Especialista" e logo wall da Home.
  `extract.py` deixou de criar o diretório `-` quando o destino é `-`.
  `run.js` passou a derivar a raiz de `__dirname` (portátil).
- **14/10/2026** - `/plataforma/marketing/` entra nas ferramentas; `run.js` aceita
  `CHROME=`. Baseline inicial da Marketing (Linux). Delta nas 6 páginas
  existentes: **zero** (13 `href` + CSS/JS aditivos).
- **14/10/2026** (2) - remoção de travessões (regra R6): 7 hashes Linux mudaram por
  reflow, `marketing-*.json` regravado, tabela Linux atualizada (ver "Ambiente").
- **14/10/2026** (3) - `/plataforma/finance/` entra nas ferramentas (`run.js`, `extract.py`).
  Delta nas páginas existentes: zero, exceto a CRM (badge rebaixado). Baseline inicial
  do Finance em Linux.
- **14/10/2026** (4) - `/plataforma/hr/` entra nas ferramentas (`run.js`, `extract.py`).
  Delta nas páginas existentes: **zero**. Baseline inicial do HR em Linux.
- **15/10/2026** - `/plataforma/ai/` entra nas ferramentas (`run.js`, `extract.py`).
  Delta nas 9 páginas existentes: **zero** (18 capturas idênticas). Baseline inicial do AI em Linux.
- **15/10/2026** (2) - CRM: bullet "Health score..." de Ativo para Roadmap. Delta: 1 elemento (o
  badge), sem reflow. CRM 1280 `915:55bd3f7c` para `915:7e771a6d`; 375 `915:b10f55e3` para
  `915:fd098212`. As demais 9 páginas seguem idênticas. `crm-*.json` continua sendo o do macOS.
- **15/10/2026** (3) - Logo wall fictício removido da CRM e da Educação. CRM 915 para 890 elementos,
  Educação 1062 para 1036 (a referência anterior já incluía o `.rm-note` de `#ia`, +1 elemento cada).
  Docs: CRM 1280 9406, 375 15498; Educação 1280 11598, 375 18826. As outras 8 páginas idênticas.
- **16/10/2026** - Fix global do `.ai-visual`: `width: 100%` na regra base, 4 regras escopadas
  removidas. Home, Overview, CRM e Educação mudam de hash nos dois viewports; Marketing, Finance, HR,
  AI, Contato e Obrigado idênticas. Em 1280 o doc não muda (a linha `.ai-inner` já era mais alta
  que o visual); em 375 o doc cresce 335px nas 4 páginas. `home-*`, `overview-*`, `crm-*` e
  `educacao-*.json` foram regravados em Linux (antes eram do macOS); os outros 16 não foram tocados.
- **16/10/2026** (2) - `/plataforma/integracoes/` entra nas ferramentas (`run.js`, `extract.py`).
  Baseline inicial da página (2 viewports). As 10 páginas existentes mudam de hash e de nº de elementos:
  +2 (item novo no footer, `<li>` e `<a>`) e 2 elementos trocados (`.icn-neutral` para `.icn-int`
  no mega-menu e no drawer, só cor). Overview, CRM e Educação ganham +1 (`.rm-note`) e Contato +1
  (opção no select). Home muda o texto do link do card "Conecte tudo". Documento (medido): páginas só
  com footer novo, +36 ou +37px em 1280 e +36 ou +37px em 375 (coluna Plataforma com 7 itens). Com
  `.rm-note` somado: Overview +104 (1280) e +123 (375), CRM +104 e +124, Educação +104 e +123. Os 22
  JSON foram regravados em Linux.
- **22/10/2026** - `/solucoes/` e `/solucoes/por-setor/` entram nas ferramentas (`run.js`, `extract.py`).
  Baseline inicial das 2 páginas (4 capturas), em Linux. Controle capturado numa worktree de `origin/main`
  (`846a4c7`). As 11 páginas existentes mudam de hash em 1280 e 375: +9 elementos cada, medido por diff
  elemento a elemento: 7 do item novo "Ver todas as soluções" no drawer (`a.mega-item`, `div.icn-neutral`,
  `svg`, `path`, `div.txt`, `div.nm`, `div.ds`) e 2 do `li`+`a` "Por Setor" no footer. A Home perde ainda
  2 `.sol-tag` (8 para 6 tags no card "Por Porte & Setor"), saldo +7. Documento: 1280 idêntico em todas;
  375 +37px (um `li` a mais no footer) em todas, exceto a Home (-3px, tags com menos quebra de linha).
- **22/10/2026** (2) - Mesma fase, ajuste final. Home: card "Por Porte & Setor" com 8 tags (4 setores e 4
  portes, +4 `.sol-tag`) e Eirway sem a classe `travel` no logo wall (ícone trocado, 2 `path` para 1):
  794 elementos (+3), doc 1280 inalterado (7877), 375 de 13240 para 13319. Contato: novo `.clients-sector.tech`
  (+7 elementos), `.clients-grid` de 3 para 4 colunas, h2 com "tecnologia": 595 elementos, doc 1280 de 3714
  para 3736 e 375 de 5702 para 5833. As outras 11 páginas (22 capturas) idênticas à captura anterior.
- **22/10/2026** (3) - `/solucoes/por-funcao/`, `/solucoes/por-objetivo/` e `/solucoes/por-porte/` entram nas
  ferramentas (`run.js`, `extract.py`). Baseline inicial das 3 páginas (6 capturas), em Linux. Controle capturado
  numa worktree limpa de `origin/main` (`9cc4b83`); um primeiro controle rodado em paralelo com a edição foi
  descartado por contaminação. Delta nas 12 páginas existentes em 1280: 41 elementos do mega-menu Soluções
  (a coluna Porte ganha uma linha porque "Múltiplas unidades e regras de acesso" quebra; `.mega-solucoes`
  491,9 para 511,2px de altura e colunas de 145,5 para 151px), nº de elementos e altura do documento
  idênticos. Home tem ainda 1 `.sol-tag` (148 para 91px, "Visibilidade"). Em 375 só a Home muda (essa tag).
  `/solucoes/`: +9 elementos (3 links nos cards), doc 1280 de 3909 para 3906 e 375 de 5821 para 5839.
  A página AI em 1280 varia 0,015px em larguras de texto entre capturas (ruído subpixel, não estrutural).
- **22/10/2026** (4) - `/consultoria/` entra nas ferramentas (`run.js`, `extract.py`). Baseline inicial (2
  viewports). Controle capturado numa worktree limpa de `e205c35`. Nas 16 páginas existentes: +1 elemento
  (`span.nav-nx` no item "Nexyss Consultoria" do header) e 1 elemento com geometria alterada (o próprio link). Nas
  5 páginas com seção `#consultoria` (Home e as 4 de eixo de Soluções) mais +4 elementos (o botão "Conhecer Nexyss
  Consultoria": `div`, `a`, `svg`, `path`) e documento +84px em 1280 e em 375; o resto dessas páginas desce 84px.
  Antes de limitar o prefixo do header a 1340px, o rótulo completo reduzia o logo de 139 para 37px entre 1181 e
  1299px (medido); a captura final já reflete a correção. `.nav-menu .nav-con` e o `.consult-cta` ficam no CSS
  compartilhado.
