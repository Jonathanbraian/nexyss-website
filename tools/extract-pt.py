#!/usr/bin/env python3
"""Passo 4 - extrai o dicionario PT (i18n/pt.json) das paginas de src/.

Le todo data-i18n e data-i18n-attr, grava {chave: valor} na ordem de aparicao
(paginas na ordem de PAGES). Falha se uma mesma chave tiver dois valores diferentes.

Uso: python3 tools/extract-pt.py [--out i18n/pt.json]
"""
import collections
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from i18nlib import *  # noqa

out = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else os.path.join(ROOT, "i18n", "pt.json")

d = collections.OrderedDict()
kind = {}
pages_of = collections.defaultdict(set)
bad = []
for rel, prefix in PAGES:
    src = read(os.path.join(SRC, rel))
    tree = parse(src)
    for n in tree.root.walk():
        k = n.get("data-i18n")
        if k is not None:
            if n.e0 is None or n.e0 == n.s1:
                bad.append((rel, k, "elemento sem conteudo"))
                continue
            a, b = split_edges(src, n)
            v = src[a:b]
            if not v:
                bad.append((rel, k, "valor vazio"))
            if k in d and d[k] != v:
                bad.append((rel, k, "valor divergente"))
            d.setdefault(k, v)
            kind.setdefault(k, "meta" if k.startswith("meta.") else "texto")
            pages_of[k].add(rel)
        am = n.get("data-i18n-attr")
        if am:
            for attr, key in parse_attr_map(am):
                sp = attr_span(src, n, attr)
                if sp is None:
                    bad.append((rel, key, "atributo %s ausente" % attr))
                    continue
                v = src[sp[0]:sp[1]]
                if key in d and d[key] != v:
                    bad.append((rel, key, "valor divergente (attr)"))
                d.setdefault(key, v)
                kind.setdefault(key, "meta" if key.startswith("meta.") else "atributo")
                pages_of[key].add(rel)

if bad:
    print("ERRO:", len(bad), "problemas")
    for b in bad[:30]:
        print("  ", b)
    sys.exit(1)

write(out, json.dumps(d, ensure_ascii=False, indent=1) + "\n")

# ---- relatorio
def cat(k):
    p = k.split(".")[0]
    if p in ("nav", "mega", "footer", "a11y", "mod", "sol", "badge", "cta", "founding"):
        return "shell/comum (" + p + ")"
    if p == "meta":
        return "meta (SEO)"
    return "pagina (" + p + ")"

byc = collections.Counter(cat(k) for k in d)
print("chaves no pt.json:", len(d), "->", os.path.relpath(out, ROOT))
print("por tipo:", dict(collections.Counter(kind.values())))
print("com HTML interno (<tag>):", sum(1 for v in d.values() if "<" in v))
print("com quebra de linha interna:", sum(1 for v in d.values() if "\n" in v))
print("compartilhadas por 2+ paginas:", sum(1 for k in d if len(pages_of[k]) > 1))
words = sum(len(re.sub(r"<[^>]+>", " ", v).split()) for v in d.values())
print("palavras (dicionario, sem repeticao):", words)
print()
groups = collections.Counter()
for k in d:
    groups[k.split(".")[0]] += 1
print("prefixos:", dict(groups.most_common()))
print()
for c, n in sorted(byc.items(), key=lambda x: -x[1])[:60]:
    print("  %-28s %5d" % (c, n))
