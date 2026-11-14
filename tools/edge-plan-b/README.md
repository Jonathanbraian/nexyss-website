# Plano B: Edge Function para a raiz "/"

Usar so se o deploy preview reprovar as regras declarativas de `/` no `netlify.toml` (condicao `Cookie` ou
`Language`). A logica esta em `lang.ts` (funcao `decide`, testada em `test-decide.mjs`).

Para ativar:
1. Copiar `lang.ts` para `netlify/edge-functions/lang.ts`.
2. Apagar do `netlify.toml` as 7 regras `[[redirects]]` com `from = "/"` (as de cookie, idioma, pais e a final).
3. Fazer deploy e rodar `bash tools/test-redirects.sh <url>` de novo.

O `index.html` da raiz (fallback com 3 botoes) continua valendo se a funcao falhar.

Teste local da logica: `node --experimental-strip-types tools/edge-plan-b/test-decide.mjs`.
