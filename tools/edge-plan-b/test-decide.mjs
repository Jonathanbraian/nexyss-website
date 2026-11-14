// node --experimental-strip-types tools/edge-plan-b/test-decide.mjs
import { decide } from "./lang.ts";
const cases = [
  ["", "", "", "en"],
  ["", "en-GB,en;q=0.9", "", "en"],
  ["", "pt-BR,pt;q=0.9,en;q=0.5", "BR", "pt"],
  ["", "pt-PT,pt;q=0.9", "PT", "en"],
  ["", "es-ES,es;q=0.9", "ES", "es"],
  ["", "es-MX,es;q=0.9", "MX", "es"],
  ["", "fr-FR,fr;q=0.9", "FR", "en"],
  ["", "fr-FR,es;q=0.5,pt;q=0.8", "FR", "pt"],
  ["nx_l_pt=1", "en-GB", "", "pt"],
  ["a=b; nx_l_es=1", "pt-BR", "", "es"],
  ["nx_l_en=1", "pt-BR", "BR", "en"],
  ["nx_l_pt=1", "en", "PT", "pt"],
];
let fail = 0;
for (const [c, a, p, want] of cases) {
  const got = decide(c, a, p);
  if (got !== want) { fail++; console.log("FAIL", { c, a, p, want, got }); }
}
console.log(fail ? fail + " falha(s)" : "OK: " + cases.length + " casos");
process.exit(fail ? 1 : 0);
