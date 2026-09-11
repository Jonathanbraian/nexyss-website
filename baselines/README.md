# Baselines de fingerprint — Nexyss

## 1. O que são

Cada `.json` aqui é a **assinatura estrutural e visual** de uma página aprovada,
capturada em dois breakpoints: **1280×800** (desktop) e **375×812** (mobile).

São 12 arquivos — 6 páginas × 2 viewports:

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
| `fingerprint` | `<nº de elementos>:<hash FNV-1a de 32 bits>` — a assinatura |
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

Requisitos: `/Applications/Google Chrome.app`, Node e **rede** — sem as fontes do
Google Fonts a geometria muda e o hash não bate (confira `fontsLoaded`).

Para **regravar** os baselines depois de uma mudança aprovada, troque o `-` pelo
diretório `baselines`:

```bash
python3 baselines/tools/extract.py /tmp/fp-check baselines run1
```

**Regravar baseline só depois de aprovação humana da mudança visual.** Baseline
atualizado sem aprovação transforma regressão em "novo normal" silencioso.

## 3. Quando comparar

- **Antes de qualquer commit que toque `assets/nexyss.css` ou `assets/nexyss.js`** —
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
| **Delta inesperado** ⚠️ | mudou algo que você não pediu | **investigar antes de commitar** — quase sempre é regra CSS sem escopo vazando |

Confirmar que o delta é o esperado quer dizer **contar**: remover um
`.impact-item` tira 4 elementos (o item + `.n` + `<small>` + `.l`); remover a
seção inteira tira 19. Se a conta não fecha, alguma outra coisa mudou junto.

Para diff elemento a elemento entre um baseline e uma captura nova, os scripts em
`tools/` produzem o JSON completo — compare os campos `elements[]` por
`(tag, classe, id)`.

## Histórico

- **04/09/2026** — baselines v2 criados. Os hashes v1 da Home (`792:…`) foram
  aposentados: o script que os gerou nunca foi salvo e era irreproduzível.
  Ver `CLAUDE.md` → "Teste de regressão — baselines v2".
- **11/09/2026** — v3: correção do logo (só `opacity` em 3 `<img>` por página).
  v4 no mesmo dia: página `/contato/` + `obrigado.html` entram nas ferramentas
  (`run.js`, `extract.py`); CTAs, "Falar com Especialista" e logo wall da Home.
  `extract.py` deixou de criar o diretório `-` quando o destino é `-`.
  `run.js` passou a derivar a raiz de `__dirname` (portátil).
