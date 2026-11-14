#!/usr/bin/env python3
"""Sessao 2.6 - padrao total de marca e coerencia de copy.

  python3 tools/apply-2-6.py --points 1,2,3,4,5 [--dry-run]

  1  "Nexyss Educação/Educación" -> "Nexyss Education"; "Nexyss Integrações/Integraciones" -> "Nexyss Integrations"
     (PT e ES; o EN ja usa os nomes em ingles)
  2  "consultoria Nexyss" (ordem invertida, PT) -> "Nexyss Consulting"
  3  metas SEO e 2 textos de Integracoes alinhados aos H1 novos (PT, EN, ES)
  4  "Educacao/Educacion" solto que e nome de modulo (27 chaves; 9 de setor/cliente ficam) -> "Education",
     com artigo masculino no PT (no/ao/do Education, como "no Finance")
  5  Overview: plat.modulos.a7 e plat.integracoes.a1 -> "Nexyss Integrations" (sem "& API")

Cada troca confere o texto esperado antes de gravar; se o dicionario ja mudou, para.
Depois: python3 tools/build-i18n.py --lang pt --identity --out src   (sincroniza src/ com o pt.json)
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
points = set(sys.argv[sys.argv.index("--points") + 1].split(",")) if "--points" in sys.argv else {"1", "2", "3", "4", "5"}
dry = "--dry-run" in sys.argv
D = {l: json.load(open(os.path.join(ROOT, "i18n", l + ".json"), encoding="utf-8")) for l in ("pt", "en", "es")}
log = []

# ---------------- ponto 1
P1 = {"pt": [("Nexyss Educação", "Nexyss Education"), ("Nexyss Integrações", "Nexyss Integrations")],
      "es": [("Nexyss Educación", "Nexyss Education"), ("Nexyss Integraciones", "Nexyss Integrations")]}
if "1" in points:
    for l, rules in P1.items():
        for pat, rep in rules:
            for k, v in D[l].items():
                n = v.count(pat)
                if n:
                    D[l][k] = v.replace(pat, rep)
                    log.append((1, l, k, n))

# ---------------- ponto 2 (PT)
P2 = {
    "plat.int.i4.d": ("A consultoria Nexyss conduz", "A Nexyss Consulting conduz"),
    "crm.int.i3.d": ("pela consultoria Nexyss durante", "pela Nexyss Consulting durante"),
    "fin.int.i3.d": ("pela consultoria Nexyss durante", "pela Nexyss Consulting durante"),
    "hr.int.i3.d": ("pela consultoria Nexyss durante", "pela Nexyss Consulting durante"),
    "ai.int.i3.d": ("com a consultoria Nexyss, módulo", "com a Nexyss Consulting, módulo"),
    "int.imp.sub": ("com a consultoria Nexyss ao lado", "com a Nexyss Consulting ao lado"),
    "int.imp.i1.d": ("Pela consultoria Nexyss, com", "Pela Nexyss Consulting, com"),
}
if "2" in points:
    for k, (a, b) in P2.items():
        assert a in D["pt"][k], (k, D["pt"][k])
        D["pt"][k] = D["pt"][k].replace(a, b)
        log.append((2, "pt", k, 1))

# ---------------- ponto 3 (valor completo, PT | EN | ES) com conferencia do texto antigo
P3 = {
 "meta.con.ogdesc": ("fica curta",
   "Consultoria mais objetiva, porque a plataforma já faz o trabalho pesado. Escopo acordado com você, sem garantia de resultados.",
   "More focused consulting, because the platform does the heavy lifting. Scope agreed with you, no guaranteed outcomes.",
   "Consultoría más ágil, porque la plataforma hace el trabajo pesado. Alcance acordado con usted, sin garantizar resultados."),
 "meta.con.twtitle": ("fica curta",
   "Nexyss Consulting - Consultoria mais objetiva",
   "Nexyss Consulting - More focused consulting",
   "Nexyss Consulting - Consultoría más ágil"),
 "meta.con.twdesc": ("fica curta",
   "Consultoria mais objetiva, porque a plataforma já faz o trabalho pesado.",
   "More focused consulting, because the platform does the heavy lifting.",
   "Consultoría más ágil, porque la plataforma hace el trabajo pesado."),
 "meta.ai.ogdesc": ("mora dentro",
   "A IA integrada aos módulos da plataforma, trabalhando com os mesmos dados que você já vê, sem abrir outra aba.",
   "AI built into the platform's modules, working with the same data you already see, without opening another tab.",
   "La IA integrada en los módulos de la plataforma, trabajando con los mismos datos que usted ya ve, sin abrir otra pestaña."),
 "meta.ai.twdesc": ("mora dentro",
   "A IA integrada aos módulos da plataforma, com os mesmos dados que você já vê.",
   "AI built into the platform's modules, using the same data you already see.",
   "La IA integrada en los módulos de la plataforma, con los mismos datos que usted ya ve."),
 "meta.int.ogdesc": ("uma ponte de verdade",
   "Dentro da Nexyss, sem integrações entre módulos. Para sistemas externos, uma conexão de verdade: API, eventos e conectores sobre o mesmo registro.",
   "Within Nexyss, no integrations between modules. For external systems, a genuine connection: API, events and connectors on the same record.",
   "Dentro de Nexyss, sin integraciones entre módulos. Para sistemas externos, una conexión real: API, eventos y conectores sobre el mismo registro."),
 "meta.int.twdesc": ("uma ponte de verdade",
   "Dentro da Nexyss, sem integrações entre módulos. Para sistemas externos, uma conexão de verdade.",
   "Within Nexyss, no integrations between modules. For external systems, a genuine connection.",
   "Dentro de Nexyss, sin integraciones entre módulos. Para sistemas externos, una conexión real."),
 "int.fro.h2": ("nenhuma integração",
   "Dentro, sem integrações entre módulos.<br>Fora, integração de verdade.",
   "Inside, no integrations between modules.<br>Outside, a real integration.",
   "Dentro, sin integraciones entre módulos.<br>Fuera, integración de verdad."),
 "int.fronteira.div1": ("Nenhuma integração",
   "<b>Sem integrações entre módulos.</b> O Finance lê o que o CRM registrou.",
   "<b>No integrations between modules.</b> Finance reads what the CRM recorded.",
   "<b>Sin integraciones entre módulos.</b> Finance lee lo que registró el CRM."),
 "meta.solx.title": ("Quatro caminhos",
   "Soluções Nexyss - Quatro formas de começar na mesma plataforma",
   "Nexyss Solutions - Four ways to get started on the same platform",
   "Soluciones Nexyss - Cuatro formas de comenzar en la misma plataforma"),
 "meta.solx.ogtitle": ("Quatro caminhos",
   "Soluções Nexyss - Quatro formas de começar na mesma plataforma",
   "Nexyss Solutions - Four ways to get started on the same platform",
   "Soluciones Nexyss - Cuatro formas de comenzar en la misma plataforma"),
 "meta.solx.twtitle": ("Quatro caminhos",
   "Soluções Nexyss - Quatro formas de começar",
   "Nexyss Solutions - Four ways to get started",
   "Soluciones Nexyss - Cuatro formas de comenzar"),
}
if "3" in points:
    for k, (probe, pt, en, es) in P3.items():
        assert re.search(probe, D["pt"][k], re.I), (k, D["pt"][k])
        for l, v in (("pt", pt), ("en", en), ("es", es)):
            D[l][k] = v
            log.append((3, l, k, 1))

# ---------------- ponto 4: "Educacao/Educacion" solto que e NOME DE MODULO -> "Education" (decidido por chave)
EDU_PLAIN = ["meta.home.desc", "meta.home.ogdesc", "meta.home.twdesc", "home.hero.p1", "meta.plat.desc", "plat.hero.span2",
             "plat.ia.sub", "plat.ia.div7", "crm.v360.sub", "mkt.rec.f4.d", "fin.hero.sub", "fin.cx.sub", "meta.hr.desc",
             "hr.hero.sub", "meta.ai.desc", "ai.hero.sub", "sobre.faq.a3"]
# artigo + nome em ingles: genero masculino, como "no Finance", "ao Marketing", "IA no CRM"
EDU_ARTICLE = ["mkt.ia.sub", "fin.ia.sub", "hr.ia.sub", "meta.fin.desc", "meta.fin.ogdesc", "meta.hr.ogdesc", "meta.hr.twdesc",
               "edu.ia.eyebrow", "ai.mod.edu.t", "int.mod.edu.t"]
EDU_SECTOR = ["mega.educacao", "footer.educacao", "home.solucoes.span14", "solx.eixos.span17", "meta.sols.title",
              "meta.sols.ogdesc", "sols.nav.edu", "sols.edu.eyebrow", "contato.clientes.edu"]
if "4" in points:
    for l, word in (("pt", "Educação"), ("es", "Educación")):
        for k in EDU_PLAIN + EDU_ARTICLE:
            v = D[l][k]
            if l == "pt" and k in EDU_ARTICLE:
                nv, n = re.subn(r"\b(da|na|à) Educação\b", lambda m: {"da": "do", "na": "no", "à": "ao"}[m.group(1)] + " Education", v)
            else:
                nv, n = re.subn(r"(?<!Nexyss )\b" + word + r"\b", "Education", v)
            assert n == 1, (l, k, v)
            D[l][k] = nv
            log.append((4, l, k, n))
    for k in EDU_SECTOR:   # garantia: setor/cliente nao e tocado
        assert "Education" not in D["pt"][k] and "Education" not in D["es"][k], k

# ---------------- ponto 5: Overview, card e link do nome antigo "Integracoes & API"
P5 = {"plat.modulos.a7": ("Nexyss Integrations",) * 3,
      "plat.integracoes.a1": ("Ver Nexyss Integrations",) * 3}
if "5" in points:
    for k, vals in P5.items():
        for l, v in zip(("pt", "en", "es"), vals):
            assert "API" in D[l][k], (l, k, D[l][k])
            D[l][k] = v
            log.append((5, l, k, 1))

by = {}
for p, l, k, n in log:
    by.setdefault((p, l), [0, 0])
    by[(p, l)][0] += 1
    by[(p, l)][1] += n
for (p, l), (keys, occ) in sorted(by.items()):
    print("ponto %d %s: %d chaves, %d ocorrencias" % (p, l.upper(), keys, occ))
if not dry:
    for l in D:
        json.dump(D[l], open(os.path.join(ROOT, "i18n", l + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        open(os.path.join(ROOT, "i18n", l + ".json"), "a").write("\n")
    print("gravado em i18n/{pt,en,es}.json")
