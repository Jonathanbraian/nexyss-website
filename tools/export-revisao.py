#!/usr/bin/env python3
"""Exporta as strings ESTRATEGICAS (para o Jonathan revisar) como CSV: PT | EN | ES.

  python3 tools/export-revisao.py [--out tools/revisao-estrategica.csv]

Estrategica = H1, sub do hero, CTAs, titulo do CTA final, eyebrow/tag do hero, Founding, tagline,
menu principal e meta title/description. Uma linha por TEXTO PT unico (as chaves que repetem o
mesmo texto aparecem juntas). O CSV tem BOM UTF-8 (abre direto no Excel); a coluna
"revisao" e livre para anotacoes. Volta para os dicionarios com tools/import-revisao.py.
"""
import collections
import csv
import html
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from i18nlib import *  # noqa

out = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else os.path.join(ROOT, "tools", "revisao-estrategica.csv")
load = lambda l: json.load(open(os.path.join(ROOT, "i18n", l + ".json"), encoding="utf-8"))
pt, en, es = load("pt"), load("en"), load("es")

info = {}
for rel, prefix in PAGES:
    s = read(os.path.join(SRC, rel))
    t = parse(s)
    for n in t.root.walk():
        ks = []
        if n.get("data-i18n"):
            ks.append((n.get("data-i18n"), False))
        for a, k in parse_attr_map(n.get("data-i18n-attr")):
            ks.append((k, True))
        for k, is_attr in ks:
            anc, p = [], n
            while p is not None and p.tag != "#root":
                anc.append(p.tag + "." + (p.get("class") or "").replace(" ", ".") + ("#" + p.get("id") if p.get("id") else ""))
                p = p.parent
            d = info.setdefault(k, dict(tag=n.tag, cls=(n.get("class") or "").split(), attr=is_attr, anc=" ".join(anc[:5]), pages=set()))
            d["pages"].add(rel)


def group(k):
    v = info[k]
    if k.startswith("meta."):
        return "Meta SEO (title/description)" if k.endswith((".title", ".desc")) else None
    if v["tag"] == "h1":
        return "H1"
    if "hero-sub" in v["cls"]:
        return "Sub do hero"
    if v["attr"]:
        return None
    if "hero" in v["anc"] and ("eyebrow" in v["cls"] or "hero-tag" in v["anc"] or "pill" in v["cls"]):
        return "Eyebrow/tag do hero"
    if any(c.startswith("btn") for c in v["cls"]) and ("hero" in v["anc"] or "cta-final" in v["anc"] or "founding" in v["anc"]):
        return "CTA"
    if k.startswith(("cta.", "consultoria.cta")):
        return "CTA"
    if "cta-final" in v["anc"] and v["tag"] == "h2":
        return "CTA final (titulo)"
    if k in ("founding.h2", "founding.badge"):
        return "Founding"
    if k.startswith("nav.") and k != "nav.pt":
        return "Menu principal"
    if "Infinitas possibilidades" in pt[k]:
        return "Tagline"
    return None


ORDER = ["H1", "Sub do hero", "Eyebrow/tag do hero", "CTA", "CTA final (titulo)", "Founding", "Tagline",
         "Menu principal", "Meta SEO (title/description)"]
rows = collections.OrderedDict()
for k in pt:
    g = group(k) if k in info else None
    if g:
        r = rows.setdefault((g, pt[k]), dict(keys=[], pages=set()))
        r["keys"].append(k)
        r["pages"] |= info[k]["pages"]


def readable(v):
    v = re.sub(r"<span class=\"accent\">(.*?)</span>", r"[[\1]]", v, flags=re.S)
    v = re.sub(r"<span style=\"[^\"]*\">(.*?)</span>", r"[[\1]]", v, flags=re.S)
    v = re.sub(r"<br\s*/?>", " / ", v)
    v = re.sub(r"<[^>]+>", "", v)
    return re.sub(r"\s+", " ", html.unescape(v)).strip()


os.makedirs(os.path.dirname(out), exist_ok=True)
with open(out, "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f)
    w.writerow(["grupo", "chave", "outras_chaves", "pagina", "PT (original)", "EN (proposta, britanico)", "ES (proposta)", "revisao"])
    n = 0
    for g in ORDER:
        for (gg, v), r in rows.items():
            if gg != g:
                continue
            k = r["keys"][0]
            pg = sorted(r["pages"])
            w.writerow([g, k, len(r["keys"]) - 1, pg[0] if len(pg) == 1 else "%d paginas" % len(pg),
                        readable(v), readable(en[k]), readable(es[k]), ""])
            n += 1
cnt = collections.Counter(g for (g, v) in rows)
print("linhas:", n, dict(cnt), "->", os.path.relpath(out, ROOT))
