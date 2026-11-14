#!/usr/bin/env bash
# Testa as regras de idioma do netlify.toml contra um deploy (preview ou producao).
#
#   bash tools/test-redirects.sh https://<preview>--nexyss-website.netlify.app
#
# Para cada caso envia uma requisicao com os cabecalhos indicados (sem seguir redirect) e confere o
# codigo HTTP e o destino (Location). Imprime PASS/FAIL por caso e um resumo; sai com 1 se algum falhar.
# O pais e simulado pelo cookie nf_country (suporte a confirmar no preview, ver caso 4).
# Cole a saida inteira de volta na conversa.

BASE="${1:?uso: bash tools/test-redirects.sh https://<deploy>.netlify.app}"
BASE="${BASE%/}"
pass=0; fail=0; n=0

# t <numero-descricao> <esperado-codigo> <esperado-location-ou-> <caminho> [curl args...]
t() {
  local desc="$1" want_code="$2" want_loc="$3" path="$4"; shift 4
  n=$((n+1))
  local out code loc
  out=$(curl -sS -o /dev/null -w '%{http_code} %{redirect_url}' --max-time 20 "$@" "$BASE$path" 2>&1)
  code="${out%% *}"; loc="${out#* }"; loc="${loc#"$BASE"}"
  if [ "$code" = "$want_code" ] && { [ "$want_loc" = "-" ] || [ "$loc" = "$want_loc" ]; }; then
    printf 'PASS  %2d  %-52s %s %s\n' "$n" "$desc" "$code" "$loc"; pass=$((pass+1))
  else
    printf 'FAIL  %2d  %-52s obtido: %s %s | esperado: %s %s\n' "$n" "$desc" "$code" "$loc" "$want_code" "$want_loc"; fail=$((fail+1))
  fi
}

echo "== Deteccao na raiz (302) =="
t "sem Accept-Language (ex.: Googlebot) -> /en/"        302 /en/ "/" -H 'User-Agent: Googlebot/2.1'
t "en-GB -> /en/"                                       302 /en/ "/" -H 'Accept-Language: en-GB,en;q=0.9'
t "pt-BR -> /pt/"                                       302 /pt/ "/" -H 'Accept-Language: pt-BR,pt;q=0.9,en;q=0.5'
t "pt-PT em Portugal (nf_country=PT) -> /en/"           302 /en/ "/" -H 'Accept-Language: pt-PT,pt;q=0.9' -H 'Cookie: nf_country=PT'
t "es-ES -> /es/ (Espanha fica no ES)"                  302 /es/ "/" -H 'Accept-Language: es-ES,es;q=0.9'
t "es-MX -> /es/"                                       302 /es/ "/" -H 'Accept-Language: es-MX,es;q=0.9'
t "fr-FR (sem idioma do site) -> /en/"                  302 /en/ "/" -H 'Accept-Language: fr-FR,fr;q=0.9'
echo
echo "== Escolha manual (cookie vence o Accept-Language) =="
t "cookie nx_l_pt + Accept-Language en -> /pt/"         302 /pt/ "/" -H 'Accept-Language: en-GB' -H 'Cookie: nx_l_pt=1'
t "cookie nx_l_es + Accept-Language pt-BR -> /es/"      302 /es/ "/" -H 'Accept-Language: pt-BR' -H 'Cookie: nx_l_es=1'
t "cookie nx_l_en + Accept-Language pt-BR -> /en/"      302 /en/ "/" -H 'Accept-Language: pt-BR' -H 'Cookie: nx_l_en=1'
echo
echo "== Paginas internas nunca redirecionam por idioma =="
t "/pt/ com Accept-Language en -> 200"                  200 -    "/pt/" -H 'Accept-Language: en-GB'
t "/en/plataforma/crm/ com Accept-Language pt -> 200"   200 -    "/en/plataforma/crm/" -H 'Accept-Language: pt-BR'
echo
echo "== URLs planas antigas (301 para /pt/, preservando a query) =="
t "/plataforma/crm/?interesse=demo"                     301 "/pt/plataforma/crm/?interesse=demo" "/plataforma/crm/?interesse=demo"
t "/plataforma (sem barra)"                             301 /pt/plataforma/ "/plataforma"
t "/solucoes/por-setor/"                                301 /pt/solucoes/por-setor/ "/solucoes/por-setor/"
t "/contato/obrigado.html"                              301 /pt/contato/obrigado.html "/contato/obrigado.html"
t "/consultoria/"                                       301 /pt/consultoria/ "/consultoria/"
echo
echo "== 404 por idioma =="
t "/en/nao-existe -> 404"                               404 -    "/en/nao-existe"
t "/es/nao/existe -> 404"                               404 -    "/es/nao/existe"
for p in en:"Page not found" pt:"Página não encontrada" es:"Página no encontrada"; do
  l="${p%%:*}"; txt="${p#*:}"; n=$((n+1))
  if curl -sS --max-time 20 "$BASE/$l/nao-existe" | grep -q "$txt"; then
    printf 'PASS  %2d  %-52s corpo da 404 em %s\n' "$n" "/$l/nao-existe mostra a 404 traduzida" "$l"; pass=$((pass+1))
  else
    printf 'FAIL  %2d  %-52s corpo sem "%s"\n' "$n" "/$l/nao-existe mostra a 404 traduzida" "$txt"; fail=$((fail+1))
  fi
done
t "/src/ continua fechado -> 404"                       404 -    "/src/index.html"
t "sitemap.xml -> 200"                                  200 -    "/sitemap.xml"
t "robots.txt -> 200"                                   200 -    "/robots.txt"

echo
echo "RESUMO: $pass PASS, $fail FAIL, de $n"
[ "$fail" -eq 0 ]
