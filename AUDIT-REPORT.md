# Auditoria de Claims — Relatório Final

**Data:** 04/09/2026 · **Escopo:** as 4 páginas aprovadas (Home, Overview, CRM, Educação)
**Detalhe item a item:** `CLAIMS-AUDIT.md` · **Regras permanentes:** `CLAUDE.md` (R1–R5.1)

---

## 1. Status das 7 categorias

| # | Categoria | Status | Resumo |
|---|---|---|---|
| 1 | Bloco de impacto | ✅ Completa | Seção removida inteira na Home; `3.4×` removido da `.impact-strip` e da `.hero-meta` do CRM |
| 2 | Idiomas 9 → 3 | ✅ Completa | 5 lugares padronizados; formato final "Multi-idioma nativo" (R4) |
| 3 | Alcance geográfico | ✅ Completa | `120+ países` removido dos 2 heros; "América Latina e Europa" na meta description |
| 4 | Founding Customers | ✅ Completa | Reescrita como convite enxuto; os 5 benefícios removidos |
| 5 | Consultoria | ✅ Completa | Decisão: **sem badges** — descrição de serviço não é badgeável (R5.1) |
| 6 | Cascata da Overview | ✅ Completa | Nunca teve badges; disclaimer de "exemplo ilustrativo" adicionado |
| 7A | CRM features | ✅ Completa | 13 🟢 + 2 🔵 (os 2 não validados retidos) |
| 7B | Educação features | ✅ Completa | 5 🟢 + 13 🔵 (rigor máximo; 13 viraram backlog de validação) |

**Nenhuma categoria bloqueada.** As pendências que sobraram são de conteúdo, não de execução.

## 2. Distribuição de badges (final)

| Página | 🟢 Ativo | 🟡 Beta | 🔵 Roadmap | ⚪ Planejado | Sem badge |
|---|---|---|---|---|---|
| Home | 0 | 0 | 0 | 0 | página inteira |
| Overview | 0 | 0 | 0 | 0 | página inteira |
| CRM | **13** | 0 | **2** | 0 | resto da página |
| Educação | **5** | 0 | **13** | 0 | resto da página |
| **Total** | **18** | **0** | **15** | **0** | — |

Home e Overview não têm badge por decisão: a Home é resumo conceitual e a Overview
argumenta arquitetura — nenhuma das duas lista feature discreta.

## 3. Backlog de validação

**20 afirmações** precisam de confirmação do time técnico. Nenhuma pode subir para
🟢 por inferência (R5).

### CRM — compliance (2)

| # | Afirmação | Linha | Ação |
|---|---|---|---|
| 1 | "Trilha de auditoria de cada execução" | 454 | **Produto + jurídico:** existe log imutável de quem alterou o quê e quando, exportável para auditoria? |
| 2 | "Residência de dado por região" | 475 | **Infra + jurídico:** o dado pode ser fixado por região hoje? Quais regiões? |

### Educação — produto (13)

Os 13 bullets 🔵, com pergunta específica para cada um, estão em
`CLAIMS-AUDIT.md` → **"🗂️ Backlog de validação — Educação"**. Agrupados em:
**Acadêmico** (4: regra por programa, histórico oficial, funil por unidade,
validação sem papel) · **Financeiro acadêmico** (5: bolsa por campus, convênio
com faturamento, lote, régua por perfil, visibilidade para coordenação) ·
**Experiência e rede** (4: portal do aluno, portal do docente, calendário por
unidade, multi-moeda).

### Educação — integrações (3) ⚠️ sem badge

| # | Afirmação | Linha | Ação |
|---|---|---|---|
| 15 | "Turma, matrícula e docente sincronizados com o ambiente virtual de aprendizagem" | 736 | **Produto:** existe conector de LMS? Quais? |
| 16 | "Catraca, biometria e carteirinha alimentando a frequência" | 742 | **Produto:** existe integração de controle de acesso? |
| 17 | "Boleto, cartão, PIX e gateways locais em cada país" | 748 | **Produto + financeiro:** quais meios e quais países? |

### Home — consultoria (1) ⚠️ sem badge

| # | Afirmação | Linha | Ação |
|---|---|---|---|
| 18 | "suporte enterprise 24/7" e "customer success proativo com SLA" | 630 | **Operações:** existe plantão 24/7 e SLA assinável? Se não, **editar o texto** — pela R5.1 não cabe badge aqui |

### Overview / CRM — arquitetura (2) ⚠️ sem badge

| # | Afirmação | Onde | Ação |
|---|---|---|---|
| 19 | "Não existe sincronização porque não existe segunda cópia" | Overview `#camada` | **Arquitetura:** o modelo de dado único é fato hoje? Sustenta as 4 páginas |
| 20 | "Sincronização bidirecional Google Workspace / Microsoft 365" | CRM `#integracoes` | **Produto:** existe? É bidirecional? |

> **Ponto cego conhecido:** 6 dos 20 (itens 15–20) estão em `.consult-desc` ou
> `.mod-sub`, que pela R5.1 não recebem badge. Ficam afirmados sem qualificação.
> Para esses, a correção é **editar o texto**, não classificar status.

## 4. Regras registradas no CLAUDE.md

| Regra | Descrição |
|---|---|
| **R1** | Naming e pricing — só o CRM tem preço público; o resto é venda por projeto; sempre "a partir de €X" |
| **R2** | Nenhum preço no site institucional; CTA padrão "Falar com Especialista" / "Solicitar Demo" |
| **R3** | Proibido inventar métrica de impacto; métrica técnica verificável é permitida |
| **R4** | Idiomas: "Multi-idioma nativo" em label; "Português, Inglês e Espanhol" em texto corrido |
| **R5** | Sistema de badges: 4 estados, rótulo 🟢 = "Ativo", `CLAIMS-AUDIT.md` é a fonte de verdade, **sem validação = fica 🔵** |
| **R5.1** | Badge marca feature verificável; descrição narrativa de serviço não recebe badge — a distinção é a granularidade, não o tipo de seção |

Além disso, a Regra de Trabalho #1 foi reescrita: a Home passou de "nunca mudar"
para **"território protegido contra mudança não solicitada"**, com o histórico da
decisão de 04/09 anotado.

## 5. Métricas técnicas

| Métrica | Valor |
|---|---|
| Arquivos tocados | **8** (4 HTML, `nexyss.css`, `CLAUDE.md`, `CLAIMS-AUDIT.md`, `baselines/README.md`) |
| Arquivos criados | **12** (8 baselines JSON, 3 ferramentas, este relatório) |
| Fingerprints capturados | **104** (13 passagens × 4 páginas × 2 viewports) |
| Componentes CSS novos | **4** — `.impact-strip.cols-3`, `.hero-meta.cols-2`, `.impact-note`, `.founding-simple` (+ variante `.founding .status-badge`) |
| Home | 783 → **735 linhas** · 45.124 → **43.025 bytes** (−4,7%) |
| CRM | 862 → **854 linhas** · 54.140 → **53.701 bytes** |
| Overview | 784 → **788 linhas** (+ disclaimer) |
| Educação | **945 linhas** (inalterado — só trocas de badge) |
| `nexyss.css` | 2.558 → **2.611 linhas** (+53, todas escopadas) |
| Altura da Home @375 | 13.685 → **12.724 px** (−961 px, −7%) |

> Não há git no projeto, então não existe contagem exata de linhas alteradas.
> Os números acima são deltas de arquivo medidos antes e depois.

**Espaço:** nada foi apagado (os backups que a auditoria previa remover não
existiam). `baselines/` adiciona **7,0 MB** de JSON.

## 6. Estado do CLAIMS-AUDIT.md

**Atualizado e consolidado** — 445 linhas.

| | |
|---|---|
| Claims mapeados | ~86 |
| Resolvidos | **66** — removidos, reescritos, ou classificados definitivamente |
| Pendentes de validação | **20** (seção 3) |
| Seções datadas | "Decisões aplicadas — 04/09/2026", com uma entrada por categoria |
| Backlog | "🗂️ Backlog de validação — Educação", 13 itens com pergunta e responsável |

## 6.1 Pendências pós-auditoria — fechadas em 04/09/2026

| # | Pendência | Status |
|---|---|---|
| 1 | Founding duplicado em 3 páginas | ✅ **Fechada** — reescrita propagada; as 4 páginas voltaram a ser cópia exata, agora com `data-i18n` |
| 2 | 6 claims em texto corrido, fora do alcance do badge | ⚠️ **5 de 6 fechadas** — o item 5 (tese arquitetural) virou decisão de posicionamento, ver 6.2 |
| 3 | Domínio placeholder | ✅ **Mapeado** — 20 ocorrências nas páginas + 4 na documentação, registradas no `CLAUDE.md` |

**Baselines pós-P1:**

| Página | 1280×800 | 375×812 |
|---|---|---|
| Home | `784:82af4c99` | `784:748535f5` |
| Overview | `854:8e96f774` | `854:cf1f4838` |
| CRM | `915:6942b7c2` | `915:0d105c69` |
| Educação | `1062:497613ee` | `1062:dd259014` |

## 6.2 Tese arquitetural — DECISÃO PENDENTE

A reescrita aprovada para a linha 350 da Overview troca a tese do site:

| | Tese |
|---|---|
| **Hoje** | *"Não existe sincronização porque não existe segunda cópia"* — **dado compartilhado**: os módulos leem e escrevem o mesmo registro |
| **Proposta** | *"Módulos que conversam desde o dia zero"* — **integração nativa**: os módulos são distintos e já vêm conectados |

São afirmações **diferentes e incompatíveis**. A varredura global pedida antes da
aplicação encontrou **17 outras frases** que sustentam a tese forte. **Nada foi
aplicado** — trocar só a linha 350 deixaria a seção `#camada` se contradizendo em
três linhas consecutivas.

### As 17 dependentes

**Overview — a página inteira é construída sobre a tese**

| Linha | Frase |
|---|---|
| 8 / 261 | `<title>` e h1: "Seis módulos, um sistema, **nenhuma integração**" |
| 265 | "os módulos **não trocam dados entre si, eles compartilham o mesmo dado**" |
| 278 | `.hero-meta`: "1 · **Base de dados compartilhada**" |
| 321 / 340 | label e h2 da seção: "**Camada compartilhada**" |
| 342 | "Trocar dado entre sistemas é integração. **Nascer do mesmo dado é outra coisa.**" |
| 349 | "Um cliente é **um registro só**" — título do card cuja descrição é a linha 350 |
| 535 | "Ativar um módulo novo **não abre projeto de integração**" |
| 586 | "**Sem migração e sem projeto de integração**: os dados que ele precisa já estão na plataforma" |
| 623 | `.vs-table`: "Duplicado em cada ferramenta" **vs.** "**Um registro só**" |
| 660 / 661 | `.impact-strip`: "6 · Módulos sobre a **mesma base**" · "1 · **Fonte da verdade**" |

**Home**

| Linha | Frase |
|---|---|
| 366 | "juntos formam um sistema operacional único: mesma identidade, **mesmos dados**, mesma inteligência. **Sem integrações, sem silos**, sem fricção." |

**CRM**

| Linha | Frase |
|---|---|
| 269 | "já conectados ao financeiro, ao marketing e ao suporte. **Sem integração**, sem exportação, sem três versões da verdade." |
| 439 | "Negócios, faturas, campanhas, tickets e matrículas **na mesma ficha**. Vindo dos módulos — **não de integração noturna**." |
| 718 | `.impact-strip`: "1 · **Fonte da verdade** para toda a operação" |

**Educação**

| Linha | Frase |
|---|---|
| 419 | "Currículo, grade, turmas… **na mesma estrutura** em todos os campi" |
| 612 | "Em sistemas separados isso são cinco registros que ninguém consegue costurar. **Aqui é uma trajetória só.**" |
| 796 | "comparáveis entre campi **porque nascem da mesma estrutura**" |

### O que isso significa

A frase da linha 350 não é um claim isolado — é **a formulação mais explícita de
um argumento que estrutura as 4 páginas**. Trocá-la sozinha não reduz risco:
deixa a contradição no lugar do problema.

**Três caminhos:**

1. **A tese é verdadeira** → nada muda. A linha 350 fica, e o item 5 sai do backlog.
2. **A tese é falsa** → não é uma reescrita, é um **reposicionamento**: as 18 frases
   mudam juntas, incluindo `<title>` e h1 da Overview, e a tagline do CLAUDE.md.
   É trabalho de uma sessão inteira, não de uma linha.
3. **A tese é parcialmente verdadeira** (alguns módulos compartilham, outros
   integram) → a formulação honesta é a do meio, e vale reescrever as 18 com esse
   grau, em vez de escolher entre dois absolutos.

**Enquanto não houver decisão, o site continua afirmando a tese forte.** É o
estado de maior risco do projeto — e o único que a auditoria não conseguiu fechar.

## 7. Próximos passos sugeridos

Ordenado por **valor comercial ÷ custo de construção**.

| Ordem | Página | Custo | Por quê |
|---|---|---|---|
| **1** | **404 amigável** | ~1h | A Overview já linka 5 URLs que retornam 404. É o menor esforço do projeto e o único bug **visível** hoje |
| **2** | `/plataforma/marketing/` | baixo | O molde da CRM está pronto e validado; `theme-mkt` já existe. É copiar, trocar tema e escrever conteúdo. Marketing é o módulo com público mais amplo |
| **3** | `/plataforma/finance/` | baixo | Mesmo custo. Finance é o módulo que aparece em **todas** as narrativas cross-módulo já escritas (matrícula → cobrança, negócio → fatura) — a página tem apoio pronto |
| **4** | `/contato/` | baixo | Toda CTA do site aponta para `href="#"`. Sem página de contato, **nenhum lead é capturável** — é o maior furo comercial aberto |
| **5** | `/plataforma/hr/` e `/plataforma/ai/` | baixo | Fecham os 6 módulos e destravam a Overview inteira. AI tem apelo alto mas o conteúdo é o mais difícil de sustentar sem produto |
| **6** | `/plataforma/integracoes/` | médio | Muito citada, e é onde vivem 4 dos claims não validados. **Só depois da validação técnica** — senão só multiplica a dívida |
| **7** | `/consultoria/` | médio | Consultoria é a parte mais madura da Nexyss. Página própria é a que tem maior chance de gerar receita **este trimestre** — mas depende de responder o "24/7 e SLA" |
| **8** | `/solucoes/*` (3 eixos) | alto | Três páginas que dependem das 6 de produto existirem para referenciar |
| **9** | `/clientes/`, `/sobre/`, `/parceiros/`, `/recursos/` | médio | Institucionais. `/clientes/` só faz sentido quando houver Founding Customers reais |

**A recomendação forte é inverter 3 e 4 se a captação de lead for prioridade
neste trimestre:** hoje o site inteiro termina em `href="#"`. Uma página de
produto a mais não converte nada enquanto não houver onde o visitante deixar o
contato.

**Antes de qualquer publicação**, três coisas continuam abertas:
1. O **domínio real** (`nexyss.com` é placeholder em canonical e og:url das 4 páginas)
2. O **bloco Founding duplicado e desatualizado** em Overview, CRM e Educação
3. O **backlog de 20 validações** da seção 3
