# Glossario i18n (PT | EN britanico | ES)

Fonte de verdade dos termos travados. O `tools/qa-i18n.py` confere parte destas regras.
Chaves e HTML interno nunca mudam; so o texto. Valores com `&` usam `&amp;` em EN e ES.

## Nao traduz
| Termo | Regra |
|---|---|
| Nexyss | sempre assim; nunca NEXYSS, nexyss, Nexsyss |
| Founding Customers | fica igual nos 3 idiomas |
| Roadmap / roadmap | fica igual nos 3 idiomas (caixa como no PT) |
| CRM, Marketing, Finance, HR, AI | nomes de modulo ficam iguais |
| Nexyss Insight / Assist / Automate | sub-produtos de IA, iguais |
| Strategy & Transformation, Implementation & Enablement, Growth & Performance, Managed Services | nomes das praticas, ja em ingles no PT |
| Nomes de cliente real, cidades de mockup | iguais |

## Identidade traduzida
| PT | EN | ES |
|---|---|---|
| Nexyss Educação | Nexyss Education | Nexyss Educación |
| Nexyss Consultoria (ate 26/10/2026) | Nexyss Consulting | Nexyss Consulting |
| Nexyss Integrações | Nexyss Integrations | Nexyss Integraciones |
| Ativo / Beta / Roadmap | Active / Beta / Roadmap | Activo / Beta / Roadmap |
| Português, Inglês e Espanhol (R4) | Portuguese, English and Spanish | portugués, inglés y español |
| Multi-idioma nativo | Native multilingual | Multiidioma nativo |
| Solicitar Demo | Request a Demo | Solicitar una demo |
| Falar com Especialista | Speak to an Expert | Hablar con un especialista |
| Candidatar-se | Apply | Presentar candidatura |
| Plataforma / Soluções / Clientes / Recursos / Parceiros / Sobre | Platform / Solutions / Customers / Resources / Partners / About | Plataforma / Soluciones / Clientes / Recursos / Partners / Nosotros |

## Vocabulario de Educação
| PT | EN | ES |
|---|---|---|
| aluno | student | estudiante |
| trajetória | journey | trayectoria |
| rede | network | red |
| mantenedora | network operator | entidad titular |
| secretaria | registrar's office | secretaría (académica) |
| evasão | dropout | deserción |
| trancamento | leave of absence | suspensión de matrícula |
| mensalidade | tuition fee | mensualidad |
| bolsa | scholarship | beca |
| colação / formando | graduation / graduate | graduación / egresado |
| matrícula | enrolment | matrícula |

## Vocabulario de Finance e HR
| PT | EN | ES |
|---|---|---|
| razão | ledger | libro mayor |
| fechamento | close | cierre |
| contas a pagar / a receber | accounts payable / receivable | cuentas a pagar / a cobrar |
| conciliação | reconciliation | conciliación |
| cobrança | collections | cobro |
| controladoria | controllership | control de gestión |
| folha | payroll | nómina |
| admissão | hiring | incorporación |
| desligamento | offboarding | desvinculación |
| diretoria / conselho | board / board | dirección / consejo |
| planilha | spreadsheet | hoja de cálculo |

## Estilo
- EN: ortografia britanica/irlandesa (organisation, programme, enrolment, digitise, optimisation).
- ES: neutro puro (decisao Q5), tratamento formal (usted). Sem regionalismo marcado: cobro (nao cobranza), coste (nao costo),
  control de gestión (nao contraloría), hoja de cálculo (nao planilla), plan de estudios (nao currículo), graduado (nao egresado),
  sede central (nao casa matriz), plaza (nao cupo), panel (nao tablero), programe (nao agende), introducir (nao digitar),
  trabajo repetido (nao retrabajo), cuentas a pagar/a cobrar, cuenta de resultados, ausencias (nao licencias), dirección (nao gerencia).
  O `qa-i18n.py` reprova a volta desses termos.
- PT: `Nexyss` + `Group` apenas em rodape/legal.
- R6: nenhum travessao; hifen simples com espacos ( - ) quando a frase precisa de pausa.
- E-mails: contact@ (EN), contato@ (PT), contacto@ (ES), so no texto visivel; o `mailto:` entra na sessao de formularios.

## Marca do servico (26/10/2026)
`Nexyss Consulting` nos 3 idiomas, inclusive no PT (decisao do Jonathan). A URL /consultoria/ nao muda. A palavra
comum "consultoria/consultoría/consulting" segue como substantivo em frases. O QA reprova "Nexyss Consultoria" e
"Nexyss Consultoría". Pendente: Educação e Integrações acompanham? (hoje PT/ES mantêm o nome local, com 5 textos
da planilha usando "Nexyss Integrations").
