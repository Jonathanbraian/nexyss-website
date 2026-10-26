#!/usr/bin/env python3
"""Controle de qualidade dos dicionarios EN/ES contra o PT.

  python3 tools/qa-i18n.py            # relatorio; exit 1 se houver ERRO (regras duras)
  python3 tools/qa-i18n.py --verbose  # lista tambem os avisos (revisao humana)

ERRO  = regra do projeto violada (glossario, R2, R3/R8, zero-pessoas, concorrente/IA, vazamento de PT).
AVISO = candidato a revisao (igual ao PT, numero divergente, grafia americana, comprimento).
"""
import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
verbose = "--verbose" in sys.argv
load = lambda l: json.load(open(os.path.join(ROOT, "i18n", l + ".json"), encoding="utf-8"))
pt, en, es = load("pt"), load("en"), load("es")
text = lambda v: html.unescape(re.sub(r"<[^>]+>", " ", v))
errors, warns = [], []

# --- vocabulario que NAO pode aparecer fora do PT
PT_LEAK = re.compile(r"[ãõç]|\b(não|você|vocês|seu|sua|seus|suas|uma|são|está|estão|também|módulo|módulos|operação|plataforma|"
                     r"para o|para a|com o|com a|dos|das|nos|nas|pelo|pela|mais de|já)\b", re.I)
ES_LEAK_ONLY_PT = re.compile(r"[ãõ]|\b(você|vocês|não|também|operação|plataforma|módulo|são|está)\b", re.I)  # 'plataforma','módulo' existem em ES, filtrados abaixo
WORDS_BAD = {
    "en": ["Educação", "Consultoria", "Integrações", "Ativo", "Ativa", "organization", "organizations", "program ",
           "programs", "center", "color", "optimize", "optimise-", "analyze", "digitize", "behavior", "license ",
           "enroll ", "enrollment", "catalog", "favor", "whilst", "customize", "personalize", "recognize"],
    "es": ["Educação", "Consultoria", "Integrações", "Ativo", "Ativa", "Roadmaps",
           # espanhol neutro puro (decisao Q5): nada de regionalismo marcado
           "cobranza", "Cobranza", "costos", "Costos", "costo ", "Costo ", "ontraloría", "planilla", "Agende", "Agendamos",
           "egresad", "Currículo", "currículo", "digitación", "digitar", "retrabajo", "casa matriz", "tablero",
           "Postularse", "postulación", "pagados", "Estado de resultados"],
}
FORBID = re.compile(r"\b(fundador|founder|co-?founder|co-?fundador|cofundador|nationality|nacionalidad|brasile|brazilian|owner|"
                    r"dueño|propietario|openai|anthropic|chatgpt|\bgpt\b|gemini|llama ?\d|mistral|claude|salesforce|hubspot|"
                    r"monday\.com|pipedrive|stripe|zoho|sap\b|oracle|netsuite|totvs)\b", re.I)
PRICE = re.compile(r"(€|\bR\$|\bUSD\b|\bEUR\b|\bGBP\b)\s*\d|\d\s*(€|EUR\b)|a partir de\s*[€$]|starting (at|from)\s*[€$]|from\s*€", re.I)
NUM = re.compile(r"\d[\d.,]*")


def nums(v):
    return sorted(re.sub(r"[.,]", "", n) for n in NUM.findall(text(v)))


for lang, d in (("en", en), ("es", es)):
    for k, v in d.items():
        p = pt[k]
        t = text(v)
        tn = t.replace("São Paulo", "")      # nome proprio, nao e vazamento de PT
        # ---- erros
        if "Founding Customers" in p and "Founding Customers" not in v:
            errors.append((lang, k, "Founding Customers deve ficar sem traducao"))
        if re.search(r"roadmap", p, re.I) and not re.search(r"roadmap", v, re.I):
            errors.append((lang, k, "Roadmap deve ficar sem traducao"))
        for w in WORDS_BAD[lang]:
            if w in v and w not in p.replace("Educação", "\0"):
                errors.append((lang, k, "termo proibido/grafia: %r" % w))
        if FORBID.search(t) and not FORBID.search(text(p)):
            errors.append((lang, k, "termo proibido (pessoa/concorrente/IA): %s" % FORBID.search(t).group(0)))
        if PRICE.search(t) and not PRICE.search(text(p)):
            errors.append((lang, k, "possivel preco (R2)"))
        if lang == "en" and PT_LEAK.search(tn) and v != p:
            errors.append((lang, k, "possivel PT no EN: %s" % PT_LEAK.search(tn).group(0)))
        if lang == "es" and re.search(r"[ãõçêô]|\b(você|vocês|não|também|operação|operações|são|seu|sua|uma)\b", tn, re.I) and v != p:
            errors.append((lang, k, "possivel PT no ES: %s" % re.search(r"[ãõçêô]|\b(você|vocês|não|também|operação|operações|são|seu|sua|uma)\b", tn, re.I).group(0)))
        if re.search(r"Nexsyss|NEXYSS|nexyss(?!\.com|\.netlify)", v):
            errors.append((lang, k, "grafia da marca"))
        # ---- avisos
        if v == p and len(t.split()) >= 3:
            warns.append((lang, k, "igual ao PT: " + t.strip()[:70]))
        if nums(v) != nums(p):
            warns.append((lang, k, "numeros divergem: %s vs %s" % (nums(p), nums(v))))
        if len(t) > 40 and len(t) > 1.6 * len(text(p)):
            warns.append((lang, k, "texto %.1fx mais longo que o PT" % (len(t) / len(text(p)))))

# glossario de identidade (nomes de modulo)
need = {"en": ("Nexyss Education", "Nexyss Consulting", "Nexyss Integrations"),
        "es": ("Nexyss Educación", "Nexyss Consulting", "Nexyss Integraciones")}
# marca "Nexyss Consulting" nos 3 idiomas (decisao de 26/10/2026): "Nexyss Consultoria/Consultoría" nao pode voltar
for lang, d in (("pt", pt), ("en", en), ("es", es)):
    for k, v in d.items():
        if re.search(r"Nexyss\s+Consultor|</span>Consultor", v):
            errors.append((lang, k, "marca deve ser 'Nexyss Consulting'"))

for lang, d in (("en", en), ("es", es)):
    for want in need[lang]:
        n = sum(1 for v in d.values() if want in v)
        print("[%s] ocorrencias de '%s': %d" % (lang, want, n))

print("\nERROS: %d | AVISOS: %d" % (len(errors), len(warns)))
for e in errors[:60]:
    print("  ERRO ", e)
if verbose:
    for w in warns:
        print("  aviso", w)
else:
    from collections import Counter
    print("  avisos por tipo:", dict(Counter(w[2].split(":")[0].split(" ")[0] for w in warns)))
sys.exit(1 if errors else 0)
