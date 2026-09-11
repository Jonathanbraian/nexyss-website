# Nexyss — site institucional

Site institucional da **Nexyss**, plataforma operacional global com IA
(CRM, Educação, Marketing, Finance, HR e Nexyss AI em um único sistema).

## Stack

HTML, CSS e JavaScript puros. Sem framework, sem build step, sem dependências.
Fontes via Google Fonts (Sora, DM Sans, DM Mono).

## Testar localmente

Abra `index.html` direto no navegador — funciona em `file://`.
CSS e JS são compartilhados por `<link>`/`<script src>`, que não dependem de servidor.

Para simular produção:

```bash
python3 -m http.server 8000
```

e acesse `http://localhost:8000/`.

## Estrutura

```
index.html                    Home
plataforma/index.html         Overview da plataforma
plataforma/crm/index.html     Nexyss CRM  (template das páginas de produto)
plataforma/educacao/index.html
assets/nexyss.css             Design system completo — fonte única de estilo
assets/nexyss.js              Header, reveal on scroll, drawer mobile, scrollspy
assets/nexyss-*.png           Logo, versão para fundo escuro e isotipo
baselines/                    Fingerprints anti-regressão (4 páginas × 2 viewports)
```

Cada página carrega `assets/nexyss.css` e `assets/nexyss.js` com caminho relativo
à sua profundidade. Header, drawer e footer são duplicados inline em cada página.

## Verificação anti-regressão

Depois de qualquer mudança em `assets/nexyss.css` ou `assets/nexyss.js`:

```bash
node baselines/tools/run.js /tmp/fp-check
python3 baselines/tools/extract.py /tmp/fp-check - check
```

Os hashes devem bater com `baselines/*.json`. Detalhes em `baselines/README.md`.

## Documentação interna

- `CLAUDE.md` — memória do projeto: design system, arquitetura, decisões e regras.
- `CLAIMS-AUDIT.md` — status de cada afirmação de produto (🟢 Ativo · 🟡 Beta · 🔵 Roadmap · ⚪ Planejado).
- `AUDIT-REPORT.md` — relatório da auditoria de claims.

© Nexyss Group. Todos os direitos reservados.
