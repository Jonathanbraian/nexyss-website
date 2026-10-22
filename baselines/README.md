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
| Home | `794:2e659598` (doc 1280x7877) | `794:81042cbd` (doc 375x13319) |
| Overview | `866:9417ceb0` (doc 1280x10735) | `866:7afa9e2d` (doc 375x17477) |
| CRM | `902:7e6d6a61` (doc 1280x9510) | `902:23bdc5e1` (doc 375x15994) |
| Educação | `1048:62bb01ef` (doc 1280x11702) | `1048:f51df686` (doc 375x19321) |
| Contato | `595:8f91074b` (doc 1280x3736) | `595:9b52ce8a` (doc 375x5833) |
| Obrigado | `447:f5fd2928` (doc 1280x1287) | `447:82cd9a7d` (doc 375x2240) |
| Marketing | `867:071d2bbc` (doc 1280x9437) | `867:60d6ff63` (doc 375x16326) |
| Finance | `942:57d0e804` (doc 1280x9485) | `942:90d115ef` (doc 375x16176) |
| HR | `907:a1ad50ba` (doc 1280x9734) | `907:2c0fee36` (doc 375x16019) |
| AI | `780:5ce32281` (doc 1280x9521) | `780:80595fff` (doc 375x15900) |
| Integrações | `868:32f09424` (doc 1280x10838) | `868:f3f34adc` (doc 375x17604) |
| **Soluções** (baseline inicial) | `518:bd21afab` (doc 1280x3909) | `518:e8f54afe` (doc 375x5821) |
| **Soluções por Setor** (baseline inicial) | `656:1a5926c1` (doc 1280x8374) | `656:95b1d978` (doc 375x12474) |

**7 hashes mudaram com a remoção dos travessões** (o hífen é mais estreito, então
houve reflow). Valores anteriores, da captura Linux de 14/10/2026 antes da troca:

| Página | Viewport | Antes | Depois | Causa |
|---|---|---|---|---|
| Overview | 1280 | `854:b0b131d6` | `854:9e1e965f` | `hero-sub` perdeu 1 linha (doc -30px) |
| Educação | 375 | `1062:7fd0c36a` | `1062:8ab43d28` | 1 parágrafo de `section-head` perdeu 1 linha (doc -28px) |
| Contato | 375 | `576:8602edf7` | `576:01a4e2b7` | `.hint` do formulário perdeu 1 linha (doc -17px) |
| CRM | 1280 | `915:c9eb3dd9` | `915:e334705f` | largura do trecho `.accent` do h1 (doc igual) |
| CRM | 375 | `915:21db6a6c` | `915:a2843876` | largura do `.accent` (doc igual) |
| Marketing | 1280 | `856:f5c3c742` | `856:f5b18501` | largura do `.accent` (doc igual) |
| Marketing | 375 | `856:27202f09` | `856:3aa08760` | largura do `.accent` (doc igual) |

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
