# Nexyss - Auditoria de Claims (Badges de Status)

## Sobre este documento

**O que é.** O inventário de toda afirmação de capacidade feita nas páginas do
site, com o status de disponibilidade de cada uma. Existe para impedir que o site
prometa o que o produto ainda não faz - e para que a promessa, quando existir,
seja uma escolha registrada em vez de um descuido.

**Consulte este documento antes de aplicar qualquer badge novo.** Um badge só
existe aqui: se a afirmação não estiver na tabela, ela ainda não foi auditada.

**Como ler os símbolos:**

| Símbolo | Modificador CSS | Significado |
|---|---|---|
| 🟢 | `.status-badge--live` | **Ativo** - existe e funciona hoje |
| 🟡 | `.status-badge--beta` | **Beta** - em teste com Founding Customers, sob demanda |
| 🔵 | `.status-badge--roadmap` | **Roadmap** - comprometido, com trimestre/ano |
| ⚪ | `.status-badge--planned` | **Planejado** - no radar, sem data |
| ⚠️ | - | **Precisa de decisão** - de fronteira, ou afirmação não validada pelo time |
| ⛔ | - | **Sem badge por regra** - é copy de argumento, visão ou persona, não capacidade |

**Convenção "Decisões aplicadas em [data]".** Cada rodada de decisões do Jonathan
vira uma seção datada, listando o que mudou de status, o que foi reescrito e o que
foi removido. As tabelas por página continuam sendo o mapa; a seção datada é o
registro do que já foi ao HTML. Quando as duas divergirem, **a seção datada é a
verdade** - ela é escrita depois da aplicação, conferida contra o arquivo.

---

> **Estratégia:** Caminho C - Badges de status, versão B (só em listas de recursos).
> **Regra de segurança:** todo claim badgeado começa como **🔵 Roadmap** até o time
> confirmar. A coluna "Sugestão" é apenas inferência de contexto - **[PRECISA
> VALIDAÇÃO DO TIME]** vale para todas as linhas até o Jonathan revisar item a item.
> Gerado em 2026-09-04. Cobre as 4 páginas existentes: Home, Overview, CRM, Educação.

## Os 4 status

| Badge | Modificador CSS | Cor | Significado |
|---|---|---|---|
| 🟢 Ativo | `.status-badge--live` | verde `--c-crm` #45E599 | existe e funciona hoje |
| 🟡 Beta | `.status-badge--beta` | laranja `--c-mkt` #F25D23 | teste com Founding Customers, sob demanda |
| 🔵 Roadmap | `.status-badge--roadmap` | azul `--c-ai` #37A7E2 | comprometido, com trimestre/ano |
| ⚪ Planejado | `.status-badge--planned` | branco 40% neutro | no radar, sem data |

## Onde o badge APARECE / NÃO aparece

- **APARECE:** bullets de `.mod-features`; cards de recurso (`.sol-card`/`.mod-card` quando listam feature); seções técnicas (Compliance, Integrações, Recursos, API); tabelas comparativas (`.vs-table`).
- **NÃO aparece:** headlines (h1/h2/h3), subtítulos, parágrafos de argumentação, copy conceitual/de visão ("sem silos", "um sistema", etc.).

## Estado do retrofit (lote 1)

- ✅ **Aplicado nesta rodada (todos 🔵 Roadmap):** bullets `.mod-features` da **CRM (15) e Educação (18)**.
- ⛔ **Home NÃO badgeada (revertida):** conflito de instruções - o PASSO 4 pede "as 4 páginas", mas o IMPORTANTE pede "Preserva visual da Home fingerprint" e a Regra #1 do CLAUDE.md é "NUNCA mudar o visual da Home". A Home tem `.mod-features` na seção-resumo `#plataforma`; badgeá-la mudaria o visual aprovado e quebraria o fingerprint. **Apliquei e reverti** (Home voltou ao estado aprovado, `status-badge`=0). Aguardando sua decisão: badgear a Home e re-baselinar o fingerprint, ou deixá-la sem badges (resumo conceitual).
- 🕓 **Candidatas - próximo lote (aguardando OK visual):** Overview inteira (não tem `.mod-features`), Integrações (`.consult-desc`), tabela comparativa (`.vs-table`), tags de card (`.sol-tag`), descrições de produto de IA (`.ai-product .ds`), e as linhas ⚠️ REVISAR abaixo. **Não receberam badge ainda** - precisam da sua decisão de escopo.

---

## HOME - `index.html`  ⛔ (revertida - ver "Estado do retrofit" acima; a tabela abaixo é o mapa, NÃO aplicado)

### 🕓 Mapeadas mas NÃO aplicadas - `.mod-features` (aguardando decisão sobre a Home)

| Linha | Afirmação literal | Card | Sugestão (inferida) |
|---|---|---|---|
| 380 | Pipeline unificado entre times e regiões | CRM | 🟢 |
| 381 | IA conversacional para follow-ups automáticos | CRM | 🟢 |
| 382 | Visão 360º de clientes e prospects | CRM | 🟢 |
| 393 | Currículo, calendário e frequência ao vivo | Educação | 🟢 |
| 394 | Multi-campus, multi-programa, multi-idioma | Educação | 🟢 |
| 395 | Financeiro acadêmico integrado | Educação | 🟢 |
| 406 | Orquestração multi-canal | Marketing | 🟢 |
| 407 | Lead scoring com IA | Marketing | 🟢 |
| 408 | Atribuição multi-touch | Marketing | 🟢 |
| 419 | Consolidação multi-moeda | Finance | 🟢 |
| 420 | Cobrança automatizada | Finance | 🟢 |
| 421 | Relatórios auditáveis | Finance | ⚠️ **UNVALIDATED** (trilha de auditoria - CLAUDE.md) |
| 432 | Ciclo completo de talentos | HR | 🟢 |
| 433 | Performance & feedback contínuos | HR | 🟢 |
| 434 | Aprendizagem corporativa | HR | 🟢 |
| 445 | Analytics preditivo em cada módulo | AI | 🟢 |
| 446 | Assistentes conversacionais para cada time | AI | 🟢 |
| 447 | Workflows inteligentes sem código | AI | 🟢 |

### 🕓 Candidatas (próximo lote) - não badgeadas

| Linha | Afirmação | Local | Nota |
|---|---|---|---|
| 456 | API aberta e webhooks para integrar Nexyss ao seu stack existente. | `.mod-sub` do card API | seção técnica |
| 550 | Analytics preditivo, KPIs e detecção de sinais | `.ai-product` (Insight) `#ai` | descrição de produto IA |
| 559 | Assistentes conversacionais para cada time e cliente | `.ai-product` (Assist) `#ai` | idem |
| 568 | Workflows inteligentes sem código, entre módulos | `.ai-product` (Automate) `#ai` | idem |
| 614 | Deploy da plataforma, migração de legados, integração, change management | `.consult-desc` `#consultoria` | ⚠️ REVISAR - camada de serviço, não feature de produto |
| 630 | Operação assistida, suporte enterprise 24/7, customer success com SLA | `.consult-desc` `#consultoria` | ⚠️ REVISAR - serviço (contém "24/7" e "SLA" verificáveis) |
| 260 | Nexyss AI agora disponível em todos os módulos | `.hero-tag` "Novo" | ⚠️ REVISAR - é claim de disponibilidade, mas fica no hero (fora da regra) |

---

## OVERVIEW - `plataforma/index.html`  🕓 (nenhuma badgeada no lote 1 - sem `.mod-features`)

### Seção técnica `#integracoes` (`.consult-desc`) - candidatas fortes

| Linha | Afirmação literal | Sugestão | Nota |
|---|---|---|---|
| 532 | Ativar um módulo novo não abre projeto de integração. Ele já enxerga tudo que a plataforma registrou até aqui. | 🟢 | |
| 538 | E-mail, calendário, telefonia, assinatura eletrônica, ERPs e gateways de pagamento, prontos para ligar. | ⚠️ **UNVALIDATED** (conectores nativos p/ ERPs - CLAUDE.md) |
| 544 | REST documentada, eventos em tempo real e ambiente de testes para o que o seu time precisar construir por cima. | ⚠️ **UNVALIDATED** (REST/tempo real/sandbox - CLAUDE.md) |
| 550 | A consultoria Nexyss conduz a migração dos sistemas que a plataforma vai substituir, com plano de corte e convivência. | 🟡 | serviço |

### Tabela comparativa `#comparativo` (`.vs-table`, célula Nexyss) - candidatas

| Linha | Célula Nexyss | Critério |
|---|---|---|
| 620 | Um registro só | Cadastro de cliente |
| 625 | Ativação | Novo módulo |
| 630 | Já é a tela | Relatório consolidado |
| 635 | Configurado uma vez | Acesso de um funcionário |
| 640 | A operação inteira | Escopo da IA |
| 645 | Um contrato, um parceiro | Custo e gestão |

### `.mod-conn` (linha "com quem o módulo conversa") - **EXCLUÍDAS por regra** (copy de visão, não capacidade)
Linhas 389, 396, 403, 410, 417, 424 - ex. "Fecha negócio e o Finance já cobra." Conceituais.

### `.mod-sub` (sub-headline por card) - **EXCLUÍDAS** (subtítulo/argumento)
Linhas 388, 395, 402, 409, 416, 423.

### `#camada` (`.consult-desc`) - ⚠️ REVISAR (arquitetura/visão, não capacidade discreta)
Linhas 351, 357, 363, 369 - ex. "Não existe sincronização porque não existe segunda cópia." Exceto **363** ("Quem vê o quê, por unidade, região e país…") que é específica (🟡).

### `#adocao` (`.sol-tag`) - candidatas
Linhas 576 ("Implantação assistida" / "Semanas, não meses"⚠️), 584 ("Zero migração"/"Histórico preservado"), 592 ("Consolidação global"/"Uma fonte da verdade").

---

## CRM - `plataforma/crm/index.html`

### ✅ Badgeadas - `.mod-features` em `#recursos`: **12 🟢 Ativo + 3 🔵 Roadmap** (Cat. 7A antecipada, 04/09; 1 bullet rebaixado em 14/10/2026, ver seção FINANCE)

| Linha | Afirmação literal | Card | Status atual |
|---|---|---|---|
| 434 | Estágios configuráveis por time, sem duplicar processo | Pipeline | 🟢 |
| 435 | Metas por vendedor, unidade, região e global | Pipeline | 🟢 |
| 436 | Conversão entre moedas na taxa da data do fechamento | Pipeline | 🟡 |
| 445 | Histórico unificado de cada interação, por origem | Contas 360º | 🟢 |
| 446 | Health score calculado com dado de todos os módulos | Contas 360º | 🟡 |
| 447 | Hierarquia de grupo, matriz e filiais | Contas 360º | 🟢 |
| 456 | Construtor visual, sem código | Automação | 🟢 |
| 457 | Gatilhos entre módulos | Automação | 🟡 |
| 454 | Trilha de auditoria de cada execução | Automação | 🔵 **mantido** - ⚠️ UNVALIDATED |
| 467 | Comprometido, provável e otimista | Previsão | 🟢 |
| 468 | Comparação com o mesmo ponto do ciclo anterior | Previsão | 🟢 |
| 469 | Fechamento reconhecido direto no Finance | Previsão | 🔵 **rebaixado 14/10/2026** (consistência entre módulos: Finance declara Roadmap) |
| 474 | **Português, Inglês e Espanhol na interface** | Global | 🟢 Ativo - **APLICADO 04/09** |
| 475 | Residência de dado por região | Global | 🔵 **mantido** - ⚠️ UNVALIDATED |
| 480 | Permissões por unidade e por país | Global | 🟢 |

### 🕓 Candidatas (próximo lote) - não badgeadas

| Linha | Afirmação | Local | Nota |
|---|---|---|---|
| 642 | Sincronização bidirecional com Google Workspace e Microsoft 365, registro automático de chamadas e agendamento direto da ficha. | `.consult-desc` `#integracoes` | ⚠️ **UNVALIDATED** |
| 648 | Proposta gerada, enviada e assinada sem sair do negócio - e o estágio avança sozinho quando a assinatura volta. | `.consult-desc` `#integracoes` | 🟡 |
| 654 | Conectores para os principais ERPs do mercado e migração assistida pela consultoria Nexyss durante a implantação. | `.consult-desc` `#integracoes` | ⚠️ **UNVALIDATED** |
| 660 | REST documentada, eventos em tempo real e ambiente de testes - para o que o seu time precisar construir por cima. | `.consult-desc` `#integracoes` | ⚠️ **UNVALIDATED** |
| 683-685 | Próxima ação sugerida · Follow-up redigido · Ficha completa do cliente | `.sol-tag` `#para-quem` (vendedor) | tags de card |
| 695-697 | Três cenários ao vivo · Metas por time e região · Alertas de risco | `.sol-tag` `#para-quem` (líder) | tags de card |
| 707-709 | Consolidação multi-moeda · Trilha de auditoria · Permissão por unidade | `.sol-tag` `#para-quem` (RevOps) | 708 = trilha de auditoria ⚠️ UNVALIDATED |
| 503,510,517,592,599,606 | (health-score/forecast/IA descrições) | `.ai-product .ds` `#visao-360`/`#ia` | descrições de produto IA |

---

## EDUCAÇÃO - `plataforma/educacao/index.html`

### ✅ Badgeadas (lote 1) - `.mod-features` em `#recursos` (3 clusters), todas 🔵 Roadmap

| Linha | Afirmação literal | Cluster · Card | Sugestão |
|---|---|---|---|
| 421 | Currículo e oferta versionados por período | Acadêmico · Vida acadêmica | 🟢 |
| 422 | Frequência e avaliação com regra por programa | Acadêmico · Vida acadêmica | 🟢 |
| 423 | Histórico oficial gerado a partir do registro, não digitado | Acadêmico · Vida acadêmica | 🟢 |
| 432 | Funil de admissão por unidade e oferta | Acadêmico · Admissões | 🟢 |
| 433 | Documentação e validação sem papel | Acadêmico · Admissões | 🟢 |
| 434 | Matrícula que já nasce com plano de pagamento | Acadêmico · Admissões | 🟢 |
| 445 | Política de bolsa por campus e por programa | Financeiro acadêmico · Receita | 🟢 |
| 446 | Convênio corporativo com faturamento próprio | Financeiro acadêmico · Receita | 🟢 |
| 447 | Reajuste e rematrícula em lote | Financeiro acadêmico · Receita | 🟢 |
| 456 | Régua configurável por perfil de aluno | Financeiro acadêmico · Inadimplência | 🟢 |
| 457 | Acordo e parcelamento com acompanhamento | Financeiro acadêmico · Inadimplência | 🟢 |
| 458 | Situação financeira visível para a coordenação | Financeiro acadêmico · Inadimplência | 🟢 |
| 469 | Portal do aluno com histórico, financeiro e oferta | Experiência e rede · Portais | 🟢 |
| 470 | Portal do docente com diário e avaliação | Experiência e rede · Portais | 🟢 |
| 471 | Portal do responsável com escopo restrito | Experiência e rede · Portais | 🟢 |
| 480 | Calendário e oferta por unidade | Experiência e rede · Rede | 🟢 |
| 481 | Moeda e política de preço local | Experiência e rede · Rede | 🟢 |
| 482 | Permissão por campus, programa e função | Experiência e rede · Rede | 🟢 |

### 🕓 Candidatas (próximo lote) - não badgeadas

| Linha | Afirmação | Local | Nota |
|---|---|---|---|
| 544-556 | Calendário/oferta · moeda/preço local · consolidação automática · unidade nova sem projeto | `.ai-product` `#rede` | painel multi-campus |
| 618-626 | Evolução por período · eventos marcados pela origem · histórico que não se perde | `.ai-product` `#jornada` | trajetória |
| 695 | Risco de evasão por aluno e previsão de receita por coorte e por campus | `.ai-product .ds` `#ia` (Insight) | IA |
| 699 | "quais alunos do 3º período estão em risco?" e recebe a lista | `.ai-product .ds` `#ia` (Assist) | IA |
| 703 | Aciona tutoria, avisa a coordenação e dispara o contato do financeiro | `.ai-product .ds` `#ia` (Automate) | IA |
| 736 | Turma, matrícula e docente sincronizados com o ambiente virtual de aprendizagem (LMS) | `.consult-desc` `#integracoes` | ⚠️ **UNVALIDATED** |
| 742 | Catraca, biometria e carteirinha alimentando a frequência sem digitação | `.consult-desc` `#integracoes` | ⚠️ **UNVALIDATED** |
| 748 | Boleto, cartão, PIX e gateways locais em cada país, com baixa automática | `.consult-desc` `#integracoes` | ⚠️ **UNVALIDATED** |
| 754 | Para o que a instituição precisar construir por cima - portal, app ou relatório | `.consult-desc` `#integracoes` | 🔵 técnica/API |
| 790-808 | 4 personas (secretaria/direção acadêmica/financeira/mantenedora) | `.consult-desc` `#para-quem` | ⚠️ REVISAR - benefício de persona, "auditável" (808) é verificável |

---

## ⚠️ REVISAR - precisam da sua decisão (não classificáveis / de fronteira)
- Home: consultoria (614, 630), hero-pill "Nexyss AI disponível" (260).
- Overview: toda `#camada` (351/357/369 conceituais; 363 específica), `.sol-tag` #adocao "Semanas, não meses" (576), célula comparativa vs. escopo.
- CRM: `.ai-product` de `#visao-360`/`#ia`, `.sol-tag` de `#para-quem`.
- Educação: 4 personas de `#para-quem` (790-808), `.ai-product` de `#rede`/`#jornada`.

## Decisões aplicadas - 04/09/2026 (Fase 2, em andamento)

Registro incremental. Atualizado a cada categoria aplicada; o fecho consolidado
entra quando as 7 categorias terminarem.

### Categoria 1 - bloco de impacto (regra R3)
- **Home:** seção de impacto **removida inteira** - `3.4×`, `87%`, `$2.1M`, `40+ países`.
- **CRM `.impact-strip`:** removido `3.4× Mais rápido no ciclo de vendas`; strip passou
  a `.impact-strip.cols-3` com as 3 métricas verificáveis restantes.
- **CRM `.hero-meta`** *(sobra da Cat. 1, aplicada junto da Cat. 2)*: removido o
  `3.4×`; passou a `.hero-meta.cols-2` com `360º De visão por conta` e
  `0 Integrações necessárias`.
- Overview e Educação não usavam nenhuma das 4 métricas proibidas.

### Categoria 2 - idiomas: 9 → 3 (PT · EN · ES)
Formato híbrido aprovado: **numeral continua numeral**, os nomes entram no rótulo;
em texto corrido os nomes substituem o número.

| Página | Local | Antes | Depois |
|---|---|---|---|
| Home | `.hero-meta` | 9 · Idiomas nativos | **3 · Idiomas · PT · EN · ES** |
| Home | `<meta description>` | "120+ países e 9 idiomas" | "120+ países, em português, inglês e espanhol" |
| Overview | `.impact-strip` | 9 · Idiomas nativos | **3 · Idiomas nativos · PT · EN · ES** |
| Overview | novo `.impact-note` | - | "Novos idiomas em roadmap conforme demanda de clientes globais." (sem badge) |
| CRM | `.impact-strip` | 9 · Idiomas nativos na interface | **3 · Idiomas nativos · PT · EN · ES** |
| CRM | `.mod-features` (474) | 🔵 9 idiomas nativos na interface | 🟢 **Português, Inglês e Espanhol na interface** |
| Educação | `.hero-meta` | 9 · Idiomas nativos | **3 · Idiomas · PT · EN · ES** |
| Educação | `.impact-strip` | 9 · Idiomas nativos na interface | **3 · Idiomas nativos · PT · EN · ES** |

> ⚠️ **Promoção antecipada do lote 7A.** O bullet 474 da CRM foi de 🔵 Roadmap para
> 🟢 Ativo **agora**, fora da Categoria 7A, para não editar o mesmo arquivo
> duas vezes. **É o único item 7A já promovido.** Os outros 14 bullets 🔵 da CRM e
> os 18 da Educação continuam 🔵 até a Cat. 7A/7B rodar.

### Categoria 3 - alcance geográfico (regra R3)
O `120+ países` existia em **2 lugares**, ambos slots numéricos de `.hero-meta`.
Educação e CRM não tinham nenhuma contagem de países.

| Página | Local | Antes | Depois |
|---|---|---|---|
| Home | `.hero-meta` | `120+` · Países suportados | **slot removido** → `.hero-meta.cols-2` |
| Home | `<meta description>` | "Opere em 120+ países…" | "Opere na América Latina e na Europa…" |
| Overview | `.hero-meta` | `120+` · Países suportados | **slot removido** → `.hero-meta.cols-2` |

> **Por que remover em vez de trocar por conceito.** O pedido era "conceito
> arquitetural sem número", mas o slot é `num` + `lbl`: um numeral grande em Sora
> com um rótulo pequeno embaixo. `LATAM · Europa` mede 197px num slot de 168px -
> estoura. `2 · Regiões atendidas` cabe, mas um "2" enfraquece o argumento em vez
> de sustentá-lo. O alcance geográfico foi para a `<meta description>`, que é texto
> corrido e comporta a frase inteira. **Nenhum CSS novo foi criado** - o
> `.hero-meta.cols-2` já existia desde a correção do CRM.

### Categoria 7A - ANTECIPADA e CONCLUÍDA (CRM): **13 🟢 + 2 🔵**
Dos 15 bullets `.mod-features` da CRM, **13 estão 🟢 Ativo** e **2 continuam
🔵 Roadmap**. A Cat. 7, quando chegar, processa **somente a 7B (Educação)** -
18 bullets, ainda 🔵.

**Os 2 que permanecem 🔵** (promovidos a 🟢 e **revertidos** em 04/09, a pedido
do Jonathan):

| Bullet | Linha | Por quê |
|---|---|---|
| Trilha de auditoria de cada execução | 454 | nunca validado com o time técnico |
| Residência de dado por região | 475 | nunca validado com o time técnico |

> ### 📌 Critério permanente: **sem validação = fica 🔵**
> Um claim só sobe para 🟢 depois de confirmação explícita do time técnico da
> Nexyss. Na ausência de resposta, o default é 🔵 Roadmap - **nunca** 🟢.
> Racional do Jonathan: em due diligence enterprise, **afirmar 🟢 e não ter é
> muito pior que o contrário**. Vale para todo claim de conformidade, segurança,
> residência de dado e auditoria.

### Vocabulário de idiomas - padrão final (regra R4 do CLAUDE.md)
O formato `PT · EN · ES`, aplicado na Cat. 2, foi **revertido**. O canônico agora é:
- **label numérico** (`.impact-strip`, `.hero-meta`) → **"Multi-idioma nativo"**
- **texto corrido** → **"Português, Inglês e Espanhol"** (o bullet 474 da CRM mantém)

Aplicado em 5 lugares: `.hero-meta` da Home e da Educação, `.impact-strip` da
Overview, da CRM e da Educação. Zero ocorrência residual de `PT · EN · ES`.

### Categoria 4 - Founding Customers (Home)

**Resultado final: reescrita completa da seção - programa em formação, sem
benefícios prometidos.** A lista dos 5 benefícios saiu inteira; nenhum deles era
verificável e badgeá-los apenas carimbaria "Roadmap" cinco vezes numa promessa.

| Elemento | Antes | Depois |
|---|---|---|
| `fbadge` | Programa Founding Customers | *(mantido)* |
| `h2` | "Construa o futuro da sua operação - com quem está construindo o futuro do software." | **"Um convite raro.<br>Um lugar limitado."** |
| `p` | "Estamos formando um grupo seleto… Um convite raro, com benefícios permanentes." | **"Estamos formando o círculo de primeiros clientes… plataformas construídas em parceria, não em transação, vamos conversar."** |
| Benefícios | 5 itens (incl. "Precificação vitalícia especial") | **removidos** |
| CTA | Candidatar-se | *(mantido)* |
| Layout | `.founding-inner` 2 colunas (texto \| lista) | **`.founding-simple`** - coluna única centrada |

A variante `.founding .status-badge` criada antes ficou **sem uso** no HTML - foi
mantida no CSS porque o bloco `.founding` continua sendo o único fundo claro do
site e qualquer badge futuro ali vai precisar dela.

> **Contraste:** o `.founding` é o único fundo claro/colorido do site (gradiente
> `brand → ai-deep`). O badge 🔵 padrão reprovaria - o azul `--c-ai` sobre o
> próprio tint dá **1.57:1 a 2.12:1**, contra os 4.5:1 de AA. Criada a variante
> `.founding .status-badge`: branco sobre navy 35%, **7.47:1** no pior ponto do
> gradiente. A cor por status não se perde porque todos os itens do bloco
> compartilham o mesmo status.

> ⚠️ **O bloco Founding está duplicado nas 4 páginas.** A Cat. 4 foi aplicada
> **só na Home**, conforme o escopo. Overview (691), CRM (758) e Educação (852)
> ainda têm o benefício "Precificação vitalícia especial" e os 4 benefícios sem
> badge. **Decisão pendente do Jonathan:** propagar ou deixar divergir.

### Categoria 5 - Consultoria: **sem badges**

Decisão final: **nenhum badge na seção Consultoria.** As 4 descrições de prática
são **narrativas de serviço**, não features verificáveis - a existência delas no
site já implica disponibilidade. Formalizado como **regra R5.1** no `CLAUDE.md`.

Os 3 badges 🟢 aplicados numa rodada anterior (Strategy, Implementation, Growth)
foram **removidos**. Efeito colateral resolvido junto: os `.consult-title` tinham
passado de 1 para 2 linhas por causa da largura do badge, e voltaram a 1 linha.

> **Managed Services** continua com **"suporte enterprise 24/7"** e **"com SLA"**
> na descrição. Pela R5.1 não leva badge - mas **as duas afirmações seguem sem
> validação**. Se não existirem, o certo é editar o texto, não classificar o status.

### Categoria 6 - cascata da Overview

- **(a)** A cascata **nunca teve badges** - confirmado, `status-badge` = 0 na
  Overview antes desta rodada. Os 5 passos são storytelling, como previsto.
- **(b)** Disclaimer adicionado ao fim de `#fluxo`, reusando **`.impact-note`**
  (mesma spec pedida: DM Mono, 0.78rem, `--c-text-mute`) - **zero CSS novo**:
  > "Exemplo ilustrativo da plataforma unificada em construção. Fluxos individuais
  > dos módulos disponíveis hoje via consultoria e integrações personalizadas."
- **`opacity: 0.7` não foi aplicada** - daria 3.30:1 de contraste, abaixo de AA.
  Mesma decisão da nota de idiomas. A discrição vem da cor, do tamanho e da fonte.
- Posicionado **depois** do parágrafo que generaliza o padrão, como rodapé da
  demonstração inteira, com `margin-top: 32px`.

### Categoria 7B - Educação: **5 🟢 + 13 🔵** (rigor máximo em compliance)

Decisão final do Jonathan: promover **apenas 5 bullets**, um por área confirmada.
Os outros 13 ficam 🔵 Roadmap e formam o **backlog de validação** abaixo.

**Os 5 🟢 Ativo:**

| Linha | Bullet | Área confirmada |
|---|---|---|
| 421 | Currículo e oferta versionados por período | currículo/calendário - acadêmico core |
| 434 | Matrícula que já nasce com plano de pagamento | integração financeira nativa (Educação ↔ Finance) |
| 457 | Acordo e parcelamento com acompanhamento | pagamentos/faturas |
| 471 | Portal do responsável com escopo restrito | auth de responsáveis para menores |
| 482 | Permissão por campus, programa e função | multi-campus |

> ⚠️ **Duas atribuições foram inferidas, não ditadas.** As categorias "multi-campus"
> e "pagamentos/faturas" tinham mais de um bullet candidato:
> - **multi-campus** → escolhi 482 (permissão por campus) sobre 480 (calendário
>   por unidade) e 481 (moeda local)
> - **pagamentos/faturas** → escolhi 457 (acordo e parcelamento) sobre 446
>   (convênio com faturamento próprio) e 456 (régua de cobrança)
>
> Trocar qualquer uma é uma linha.

---

## 🗂️ Backlog de validação - Educação (13 bullets 🔵)

Cada item é respondível numa conversa curta com quem sabe.

### Acadêmico

| # | Linha | Bullet | Por que está 🔵 | Ação para promover |
|---|---|---|---|---|
| 1 | 422 | Frequência e avaliação com regra por programa | motor de regras por programa - não confirmado se a regra é configurável ou fixa | Confirmar com **produto/eng.**: existe configuração de regra de frequência e avaliação por programa hoje? |
| 2 | 423 | Histórico oficial gerado a partir do registro, não digitado | histórico **oficial** tem valor legal - geração automática é claim regulatório | Confirmar com **produto + jurídico**: o histórico gerado é aceito como documento oficial, sem digitação paralela? |
| 3 | 432 | Funil de admissão por unidade e oferta | funil de admissões segmentado por unidade | Confirmar com **produto**: o funil já segmenta por unidade e por oferta, ou é único? |
| 4 | 433 | Documentação e validação sem papel | "sem papel" implica upload + validação digital ponta a ponta | Confirmar com **produto**: existe validação digital de documento, ou só anexo? |

### Financeiro acadêmico

| # | Linha | Bullet | Por que está 🔵 | Ação para promover |
|---|---|---|---|---|
| 5 | 445 | Política de bolsa por campus e por programa | política de bolsa multi-dimensional | Confirmar com **produto**: bolsa é configurável por campus **e** por programa, ou só global? |
| 6 | 446 | Convênio corporativo com faturamento próprio | faturamento B2B separado do aluno - fluxo fiscal distinto | Confirmar com **produto + fiscal**: existe emissão para pagador corporativo hoje? |
| 7 | 447 | Reajuste e rematrícula em lote | operação em lote sobre base financeira | Confirmar com **produto**: reajuste e rematrícula rodam em lote, ou aluno a aluno? |
| 8 | 456 | Régua configurável por perfil de aluno | régua de cobrança segmentada | Confirmar com **produto**: a régua aceita perfis distintos, ou é única? |
| 9 | 458 | Situação financeira visível para a coordenação | cruzamento Finance → Educação com permissão | Confirmar com **produto**: coordenação acadêmica enxerga situação financeira hoje, e sob qual permissão? |

### Experiência e rede

| # | Linha | Bullet | Por que está 🔵 | Ação para promover |
|---|---|---|---|---|
| 10 | 469 | Portal do aluno com histórico, financeiro e oferta | portal com 3 domínios agregados | Confirmar com **produto**: o portal do aluno já reúne os três, ou parte deles? |
| 11 | 470 | Portal do docente com diário e avaliação | diário de classe e lançamento de nota | Confirmar com **produto**: docente lança frequência e nota direto no portal? |
| 12 | 480 | Calendário e oferta por unidade | calendário acadêmico independente por campus | Confirmar com **produto**: cada unidade tem calendário próprio, ou herda um da rede? |
| 13 | 481 | Moeda e política de preço local | multi-moeda com consolidação - depende de câmbio | Confirmar com **produto + financeiro**: multi-moeda existe? Qual a fonte da taxa de câmbio? |

### Pendência pós-auditoria 1 - Founding duplicado: **FECHADA**

O bloco Founding era **byte-idêntico** nas 4 páginas (2.211 caracteres cada). A
reescrita da Cat. 4 foi propagada para Overview, CRM e Educação, e as 4 voltaram a
ser cópia exata - agora com `data-i18n` (`founding.badge`, `founding.h2`,
`founding.p`, `cta.candidatar`), que a versão da Home não tinha.

| Página | Δ elementos | Conta |
|---|---|---|
| Home | **+1** | `<span>` novo dentro do `.fbadge` (para receber `data-i18n`) |
| Overview · CRM · Educação | **-14** cada | -16 (`.founding-benefits` + 5 × [div+svg+path]) +2 (`<span>` do fbadge e `<br>` do h2) |

"Precificação vitalícia especial" não existe mais em nenhuma página. **Regra R2
cumprida em 100% do site.**

### Pendência pós-auditoria 2 - claims em texto corrido: **5 de 6 fechadas**

| # | Página | Antes | Depois |
|---|---|---|---|
| 1 | Educação 736 | "Turma, matrícula e docente **sincronizados** com o ambiente virtual de aprendizagem…" | "**Preparada para conectar** ao ambiente virtual de aprendizagem…" |
| 2 | Educação 742 | "Catraca, biometria e carteirinha **alimentando** a frequência…" | "Frequência que **aceita origem externa** - catraca, biometria ou carteirinha…" |
| 3 | Educação 748 | "**Boleto, cartão, PIX** e gateways locais… com baixa automática." | "**Meios de pagamento locais por país**, com conciliação automática da baixa." |
| 4 | Home 626 | "…suporte enterprise **24/7** e customer success proativo **com SLA**." | "…suporte enterprise e customer success proativo." |
| 6 | CRM 638 | "**Sincronização bidirecional** com Google Workspace e Microsoft 365, **registro automático de chamadas**…" | "**Conexão** com Google Workspace e Microsoft 365 para e-mail, agenda e registro de atividade." |

Nenhuma das 5 estava duplicada em outra página - verificado por grep frase a frase.

> ⏸️ **Item 5 (tese arquitetural) NÃO aplicado.** A varredura global exigida antes
> da aplicação encontrou **~17 outras afirmações** que dependem da mesma tese, em
> todas as 4 páginas. Trocar só a linha 350 deixaria a Overview se contradizendo
> dentro da própria seção. Ver "Tese arquitetural - decisão pendente" no
> `AUDIT-REPORT.md`. **A tese atual do site continua sendo "dado compartilhado".**

### Componentes de CSS criados nestas categorias
`.impact-strip.cols-3` · `.hero-meta.cols-2` · `.impact-note` · `.founding .status-badge` · `.founding-simple` - todos no idioma do
design system, seguindo o `.mega-grid.cols-3` que já existia. A Cat. 3 não precisou
de nenhum componente novo.

> **Nota de acessibilidade.** O `.impact-note` foi especificado com `opacity: .7`
> sobre `--c-text-mute`, o que daria **3.30:1** de contraste - abaixo do mínimo AA
> de 4.5:1 para texto normal. A declaração nunca chegou a valer (o `.reveal.in`
> tem especificidade maior e força `opacity: 1`), então na prática o texto sempre
> renderizou a **5.46:1**. O `opacity` foi removido para o CSS dizer o que o
> navegador faz - sem isso, qualquer reuso do `.impact-note` fora de um `.reveal`
> reprovaria em AA silenciosamente.

---

## 🔴 UNVALIDATED (dívida herdada do CLAUDE.md) - badge sugerido: ⚠️ até validar
| Afirmação | Onde (linha) |
|---|---|
| "Residência de dado por região" | CRM 479 |
| "Relatórios auditáveis" / "Trilha de auditoria" | Home 421, CRM 458 e 708 |
| "Conectores (nativos) para os principais ERPs" | Overview 538, CRM 654 |
| "REST documentada, eventos em tempo real, ambiente de testes" | Overview 544, CRM 660 |
| "Sincronização bidirecional Google Workspace / Microsoft 365" | CRM 642 |
| "Turma e docente sincronizados com o LMS" | Educação 736 |
| "Catraca e biometria" | Educação 742 |
| "Boleto, cartão, PIX" | Educação 748 |
| Marketing (22 bullets 🔵: workflow sem código, SMS/push, sync de anúncios, landing pages/blog/formulários, consentimento, multi-touch, API REST/webhooks…) | Marketing, ver seção "MARKETING" |
| Finance (22 bullets 🔵: razão multi-entidade, DRE/balanço/DFC, notas e obrigações por país, alçadas, régua de cobrança, projeção de caixa, conciliação automática, API REST/webhooks...) | Finance, ver seção "FINANCE" |

## Números aprovados (Jonathan) - NÃO recebem badge
120+ países · 9 idiomas nativos · 99.99% uptime · 3.4× ciclo de vendas · 87% redução de silos · $2.1M economia de stack · 40+ países atendidos · 360º · 6 módulos · 1 base de dados.
> Nota: "99.99% Uptime **garantido em SLA**" repete o número aprovado com um qualificador de SLA - se um dia SLA virar claim badgeável, revisar.

---

## Descoberta pós-auditoria - logo wall fictício da Home (11/09/2026) ✅ FECHADA

**Não constava neste documento.** A seção `.logos` da Home exibia 6 organizações
inventadas - Globaledu · Atlas Academy · Vertex · Polaris · Meridian · Orbital -
sob "Confiado por organizações inovadoras no mundo todo", e estava **no ar**.
Violação direta de R3/R8, invisível para a auditoria de 04/09 porque o mapeamento
cobriu `.mod-features`, `.consult-desc`, `.vs-table` e `.sol-tag`, não `.logo-item`.

**Correção aplicada (aprovada pelo Jonathan):** os 6 fictícios substituídos pelos
5 clientes reais fornecidos por ele, label "Organizações que operam com a Nexyss".

| Setor | Cliente | Onde |
|---|---|---|
| Educação | NED College | Home `.logo-item.edu` · Contato `.client-card[data-client=ned-college]` |
| Esporte | Dublin Volleyball Club | Home `.logo-item.sport` · Contato `dublin-volleyball-club` |
| Esporte | Volley Point | Home `.logo-item.sport` · Contato `volley-point` |
| Turismo | Excursion LTD | Home `.logo-item.travel` · Contato `excursion-ltd` |
| Turismo | Eirway | Home `.logo-item.travel` · Contato `eirway` |

**TODO de substituição:** os 5 são placeholders **textuais** (nome em Sora + ícone
do setor). Quando os SVG/PNG chegarem: `assets/clients/<slug>.svg` e trocar o
`<span class="logo-placeholder">` por `<img>` nos 10 pontos (5 Home + 5 Contato). Sem badge - nome de
cliente não é claim de capacidade (R5.1).

> Nota: "Meridian" continua em `plataforma/crm/index.html` como **nome de negócio
> no mockup do pipeline** (`.pc-name`), não como cliente. Fora do escopo.

## MARKETING - `plataforma/marketing/index.html`  (14/10/2026)

**Regra aplicada: 100% 🔵 Roadmap, todos UNVALIDATED.** Sem validação do time técnico
nada é 🟢 (R5). 22 bullets badgeados; a página abre `#recursos` com a linha de
disclosure *"Os recursos abaixo estão em roadmap. Founding Customers participam da
definição da ordem de entrega."* (não é claim, não leva badge).

### 🔵 `#recursos` - `.mod-features` (15)
| Card | Afirmação literal |
|---|---|
| Automação | Construtor visual de workflows, sem código |
| Automação | Gatilhos por comportamento, estágio de ciclo de vida e evento de outro módulo |
| Automação | Entrega do lead qualificado ao CRM com histórico completo |
| Campanhas | E-mail, SMS e push na mesma campanha |
| Campanhas | Públicos sincronizados com plataformas de anúncios |
| Campanhas | Teste A/B de assunto e conteúdo |
| Conteúdo | Landing pages em editor visual |
| Conteúdo | Blog integrado |
| Conteúdo | Formulários nativos que gravam direto no registro do lead |
| Audiência | Segmentos dinâmicos com dado de todos os módulos |
| Audiência | Lead scoring por perfil e comportamento |
| Audiência | Registro de consentimento e preferências por contato |
| Relatórios | Desempenho por campanha, canal e período |
| Relatórios | Painéis por marca, unidade e país |
| Relatórios | Custo por canal ao lado da receita fechada |

### 🔵 `#atribuicao` - `.ai-product` (3)
Atribuição multi-touch · Receita por canal e campanha (contrato no CRM + fatura no
Finance ligados à campanha de origem) · Custo de aquisição por canal.

### 🔵 `#integracoes` - `.consult-desc` (4)
Plataformas de anúncios (públicos sincronizados + custo por campanha) · E-mail e SMS
(provedores de envio, domínio autenticado, evento registrado no contato) · Site,
pixel e UTM · API aberta e webhooks (**REST documentada e eventos em tempo real** -
mesma afirmação da UNVALIDATED abaixo; fornecedores **não** são nomeados).

### ⛔ Sem badge por regra (R5.1)
Hero e headlines · `#problema` (3 cards) · `#ia` (Insight/Assist/Automate - descrição
narrativa, mesmo critério da CRM) · `#para-quem` (3 personas e suas `.sol-tag`, como
na CRM) · impacto (1 · 3 · 99.99%: arquitetura, R4 e SLA aprovados pelo Jonathan).

### Mockups (Visual A e B) - sem número, marcados "ILUSTRATIVO"
O workflow do hero e o painel de atribuição **não exibem valor numérico** (R3). As
barras de "Receita por canal" têm largura proporcional ilustrativa e **nenhum
percentual ou valor**; o rótulo "ILUSTRATIVO" fica no cabeçalho dos dois painéis.

### Decisões aplicadas - 14/10/2026
- **Sem logo wall** na página (nenhum cliente real usa Marketing - R8).
- `origem` das CTAs corrigido em `nexyss.js` (ver CLAUDE.md → "Bug fix: `origem`").
- **Pendência aberta:** CRM e Educação ainda têm logo wall **fictício**
  (`plataforma/crm/index.html` ~370-375: Globaledu, Atlas Academy, Vertex, Polaris,
  Meridian, Orbital; `plataforma/educacao/index.html` 359-364: Globaledu, Polaris
  College, Rede Meridian, Orbital Schools…). Mesma violação de R3/R8 corrigida na Home
  em 11/09 - **corrigir na próxima sessão**.
- Home, linhas 406-408 (Marketing `.mod-features`): a tabela acima na seção HOME
  sugeria 🟢 por inferência. Ela **nunca foi aplicada** ao HTML e **não vale**: a
  página de Marketing declara 🔵 para as mesmas capacidades. Se a Home um dia for
  badgeada, o status é 🔵.

## FINANCE - `plataforma/finance/index.html`  (14/10/2026)

**Regra aplicada: 100% 🔵 Roadmap, todos UNVALIDATED.** Sem validação do time técnico
nada é 🟢 (R5). 22 bullets badgeados, mesma linha de disclosure do Marketing em
`#recursos` (não é claim, não leva badge).

### 🔵 `#recursos` - `.mod-features` (15)
| Card | Afirmação literal |
|---|---|
| Contábil | Plano de contas e razão por entidade, em várias moedas |
| Contábil | DRE, balanço e DFC gerados do próprio razão |
| Contábil | Fechamento de período com checklist e bloqueio de lançamentos |
| Fiscal | Emissão de notas a partir do contrato ou da venda |
| Fiscal | Apuração de impostos por entidade e por país |
| Fiscal | Geração das obrigações acessórias do período |
| Pagar e receber | Contas a pagar com alçadas de aprovação |
| Pagar e receber | Contas a receber geradas do contrato fechado no CRM |
| Pagar e receber | Régua de cobrança por canal |
| Caixa | Posição de caixa por entidade e por moeda |
| Caixa | Projeção alimentada por contratos, mensalidades e compromissos |
| Caixa | Cenários de caixa comparados lado a lado |
| Conciliação | Importação de extratos bancários |
| Conciliação | Conciliação automática por regra e por sugestão da IA |
| Conciliação | Fila de exceções com responsável |

### 🔵 `#caixa` - `.ai-product` (3)
Projeção alimentada pelos módulos · Cenários por entidade e moeda · Alerta de
cobertura de caixa.

### 🔵 `#integracoes` - `.consult-desc` (4)
Bancos e meios de pagamento (extratos importados, pagamentos enviados) · Obrigações
fiscais por país · Migração assistida (plano de contas, saldos iniciais e histórico,
pela consultoria) · API aberta e webhooks (**REST documentada e eventos em tempo
real**, mesma afirmação da lista UNVALIDATED abaixo).

### Regra do fiscal: genérico, nada nomeado
Fiscal é o claim de maior risco (depende do país). A página diz "por país" e **não
nomeia obrigação, imposto nem padrão** de país nenhum. Qualquer nome específico só
entra depois da validação técnica e entra como 🔵 com data.

### ⛔ Sem badge por regra (R5.1)
Hero e headlines · `#problema` (3 cards) · `#ia` (Insight/Assist/Automate, narrativa,
como na CRM e no Marketing) · `#para-quem` (3 personas e suas `.sol-tag`) · impacto
(1 · 3 · 99.99%: arquitetura, R4 e SLA aprovados pelo Jonathan).

### Mockups (Visual A e B): sem número, marcados "ILUSTRATIVO"
Conciliação e fluxo de caixa usam rótulos genéricos ("Fornecedor 1", "Cliente A",
"Conta A") e barras sem valor. Nenhum número de desempenho (R3).

### Decisões aplicadas - 14/10/2026
- **CRM rebaixada por consistência entre módulos:** o bullet "Fechamento reconhecido
  direto no Finance" (CRM `#recursos`, card Previsão) passou de 🟢 Ativo para 🔵
  Roadmap. Motivo: o Finance declara a capacidade como Roadmap e a CRM seguia como
  Ativo, o que fazia os dois módulos se contradizerem. CRM: **12 🟢 + 3 🔵**.
  O "Financeiro acadêmico" da Educação continua 🟢: roda dentro do módulo Educação.
- **Sem logo wall** (nenhum cliente real usa Finance, R8).
- **"ERP financeiro"** só em title/meta e uma vez no corpo; nunca no H1.
- **Pendência aberta:** CRM e Educação ainda têm logo wall **fictício**
  (violação de R3/R8). Corrigir em sessão própria.
- **Pendência aberta:** fix global do `.ai-visual` (0x0 em Home, Overview, CRM e
  Educação); muda os fingerprints de 4 páginas.

## Página `/contato/` - fora do escopo de badges
A FAQ da página contém compromissos de atendimento ("24 horas úteis", "30-60 min",
"proposta em até 7 dias úteis", "clientes na América Latina e Europa") definidos
pelo Jonathan em 11/09/2026. **Não são claims de produto** - não recebem badge e
não entram no backlog de validação. Registro em CLAUDE.md → "FAQ - compromissos
operacionais".
