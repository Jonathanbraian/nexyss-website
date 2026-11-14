// PLANO B (nao ativo): Edge Function da Netlify que decide o idioma na raiz "/".
// Equivale as 7 regras declarativas de "/" do netlify.toml. Ver README.md desta pasta.
//
// Ordem de decisao:
//   1. cookie nx_l_<idioma> (escolha manual do seletor) vence tudo
//   2. Accept-Language: o primeiro idioma suportado da lista, em ordem de preferencia (es, pt, en)
//   3. pt em Portugal (pais PT) vai para en: o PT do site e o do Brasil
//   4. sem nada suportado, ou sem Accept-Language (Googlebot): en

export type Lang = "en" | "pt" | "es";
const SUPPORTED = ["es", "pt", "en"];

export function decide(cookie: string, acceptLanguage: string, country: string): Lang {
  for (const l of ["pt", "es", "en"]) {
    if (new RegExp("(?:^|;\\s*)nx_l_" + l + "=").test(cookie)) return l as Lang;
  }
  const prefs = acceptLanguage
    .split(",")
    .map((p) => {
      const [tag, q] = p.trim().split(";q=");
      return { lang: tag.toLowerCase().split("-")[0], q: q ? parseFloat(q) : 1 };
    })
    .filter((p) => SUPPORTED.includes(p.lang) && p.q > 0)
    .sort((a, b) => b.q - a.q);
  const lang = (prefs[0]?.lang ?? "en") as Lang;
  return lang === "pt" && country === "PT" ? "en" : lang;
}

// Handler da Netlify (so roda no edge; nao e importado pelo teste).
export default async (request: Request, context: { geo?: { country?: { code?: string } } }) => {
  const lang = decide(
    request.headers.get("cookie") ?? "",
    request.headers.get("accept-language") ?? "",
    context.geo?.country?.code ?? "",
  );
  return new Response(null, { status: 302, headers: { Location: "/" + lang + "/" } });
};

export const config = { path: "/" };
