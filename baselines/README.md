# Baselines de fingerprint - Nexyss (3 idiomas)

Assinatura estrutural e visual de cada página publicada, para flagrar regressão depois de mexer em
`assets/nexyss.css`, `assets/nexyss.js`, no gerador ou nos dicionários. Regravada em 14/11/2026 para a
árvore gerada `/en/`, `/pt/` e `/es/` (a partir da Sessão 3e do i18n). Os baselines antigos (páginas planas, macOS)
foram removidos: o histórico do git os guarda.

## Layout

```
baselines/
  en/<pagina>-<vp>.json      compacto, 38 arquivos
  pt/<pagina>-<vp>.json      compacto, 38 arquivos
  es/<pagina>-<vp>.json      compacto, 38 arquivos
  pt-full/<pagina>-<vp>.json.gz   completo (todo elemento), só PT, 38 arquivos, backup forense
  tools/run.js               gerador e comparador
```

19 páginas × 2 viewports (1280×800 e 375×812) × 3 idiomas = **114 baselines compactos**. As 19 páginas são as da
árvore (home, overview, crm, educacao, marketing, finance, hr, ai, integracoes, contato, obrigado, solucoes, porsetor,
porfuncao, porobjetivo, porporte, consultoria, sobre, clientes). A `404.html` não entra (é servida em qualquer URL).

## Formato

Compacto (~60 bytes):

```json
{"fp":"823:4cde23a6","doc":"1280x7881","fonts":"loaded"}
```

| Campo | Significado |
|---|---|
| `fp` | `<nº de elementos>:<hash FNV-1a 32 bits>` de tag, classe, id, geometria e 28 propriedades computadas de todo elemento |
| `doc` | largura × altura do documento |
| `fonts` | `loaded` se o Google Fonts carregou (se não carregou, a geometria muda e o hash não vale) |

O `pt-full` guarda os mesmos dados **por elemento** (gzip, `zcat baselines/pt-full/home-1280.json.gz`), para diff elemento a elemento
quando um hash do PT divergir. EN e ES derivam do PT: se um hash de EN/ES divergir, compare primeiro o do PT.

> O fingerprint **não cobre texto, `filter` nem `src` de `<img>`**. Mudança de copy ou troca de asset com a mesma geometria
> passa invisível; verifique por `grep` ou screenshot à parte. Para texto, `tools/qa-i18n.py` e `tools/qa-site.py`.

## Comandos

```bash
node baselines/tools/run.js --check                        # captura as 114 e compara (exit 1 se divergir ou houver overflow horizontal)
node baselines/tools/run.js --check --lang es --page crm   # um recorte
node baselines/tools/run.js --all                          # REGRAVA (só depois de aprovação humana da mudança visual)
```

Requisitos: Node, Playwright com Chromium (`CHROME=/caminho` se for outro binário) e **rede** (Google Fonts). Dura ~4 minutos.
Antes de capturar, rode `python3 tools/build-i18n.py --lang all --site --out .` (o `run.js` lê os HTML gerados em `en/ pt/ es/`).

**Regravar baseline só depois de aprovação humana.** Baseline atualizado sem aprovação transforma regressão em "novo normal" silencioso.

## Interpretando o delta

| Resultado | Leitura | Ação |
|---|---|---|
| Zero delta | página intocada | seguir |
| Delta esperado | bate com a mudança intencional | confirmar contando elementos, depois regravar |
| Delta inesperado | mudou algo não pedido | investigar antes de commitar (quase sempre CSS sem escopo vazando) |

A altura do documento difere entre idiomas (EN, PT e ES têm textos de comprimentos diferentes): compare cada idioma com o próprio baseline.

## Ambiente

Capturado no **Chromium do Linux** (Playwright), não no Chrome do macOS: os hashes antigos do macOS não reproduzem aqui. Compare sempre
antes × depois no mesmo ambiente. **Jitter conhecido:** cerca de 4% das capturas (5 de 108 na verificação) saem com hash diferente e mesmo nº de elementos e mesma altura, sem causa reproduzível em captura isolada (layout sob carga). Por isso `--check` aceita a página se uma de até 3 tentativas bater, e `--all` só grava quando 2 capturas seguidas concordam. Uma divergência que persiste nas 3 tentativas é real.

## Adicionar um idioma novo

1. Criar `i18n/<l>.json` e incluir `<l>` em `LANGS`, `HREFLANG`, `LANG_ATTR`, `OG_LOCALE` e `LANG_NAMES` de `tools/build-i18n.py`.
2. Gerar o site (`--lang all --site --out .`); o seletor, o hreflang e o sitemap acompanham.
3. Incluir `<l>` em `LANGS` de `baselines/tools/run.js` e rodar `--all --lang <l>` (grava só o compacto).
4. Regras do `/` no `netlify.toml` e `tools/test-redirects.sh` (cookie `nx_l_<l>`).

## Referência: 1280×800 (14/11/2026)

| Página | EN 1280 | PT 1280 | ES 1280 |
|---|---|---|---|
| home | `823:142f4c19` (1280x7855) | `823:4cde23a6` (1280x7881) | `823:c1500169` (1280x7944) |
| overview | `891:037b3a7c` (1280x11080) | `891:30612e5e` (1280x10845) | `891:ea3cf9cc` (1280x10850) |
| crm | `927:e1e5ca70` (1280x9573) | `927:fc58066c` (1280x9606) | `927:fbe50d6a` (1280x9754) |
| educacao | `1073:bb99385a` (1280x11858) | `1073:ee2c65bd` (1280x11702) | `1073:56592a35` (1280x12115) |
| marketing | `892:dd79ce14` (1280x9548) | `892:62257b6d` (1280x9505) | `892:7bc75d70` (1280x9652) |
| finance | `967:cf155b19` (1280x9823) | `967:01f1fa43` (1280x9633) | `967:3fea3d6d` (1280x9709) |
| hr | `932:7d7f80fb` (1280x9954) | `932:ab547535` (1280x9720) | `932:7a473da1` (1280x10123) |
| ai | `805:492a1485` (1280x9524) | `805:4cf9909e` (1280x9440) | `805:31ea9065` (1280x9464) |
| integracoes | `893:8b382ac3` (1280x11057) | `893:13ea6000` (1280x10890) | `893:3f39dc6f` (1280x10927) |
| contato | `621:f10544de` (1280x3671) | `621:ea2823d3` (1280x3736) | `621:c8de60f8` (1280x3736) |
| obrigado | `468:fd49b07a` (1280x1368) | `468:6e0e867b` (1280x1287) | `468:9ac8a9a0` (1280x1368) |
| solucoes | `552:f5aa6b18` (1280x3634) | `552:039c5316` (1280x3906) | `552:af36df81` (1280x3877) |
| porsetor | `685:5ff2e8a5` (1280x8462) | `685:ed4d037b` (1280x8458) | `685:02754c8a` (1280x8583) |
| porfuncao | `713:90de75b9` (1280x9740) | `713:a70bb18e` (1280x9799) | `713:5bca5788` (1280x9821) |
| porobjetivo | `725:ed0c1b30` (1280x9531) | `725:86f98b87` (1280x9616) | `725:a8273100` (1280x9507) |
| porporte | `677:2a73ebda` (1280x7867) | `677:ba750706` (1280x7993) | `677:dfe6256a` (1280x7891) |
| consultoria | `804:30bf1de1` (1280x9847) | `804:cb6db01b` (1280x9939) | `804:31a2a7d9` (1280x9943) |
| sobre | `640:e0f97ac1` (1280x7128) | `640:85074578` (1280x7186) | `640:da08008e` (1280x7129) |

Os de 375×812 estão nos próprios JSON.
