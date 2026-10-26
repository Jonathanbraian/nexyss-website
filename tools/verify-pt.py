#!/usr/bin/env python3
"""Passo 6 - prova PT = atual.

  Prova A (identidade): gerador em modo --identity --strip-attrs vs paginas servidas hoje
                        (com data-i18n* removidos dos dois lados) -> tem que ser byte a byte igual.
  Prova B (/pt/ real):  gerador completo vs paginas servidas hoje -> toda linha diferente tem
                        que cair numa das categorias mapeadas; "nao mapeadas" tem que ser 0.

Uso: python3 tools/verify-pt.py <dir-de-trabalho>
"""
import collections
import difflib
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from i18nlib import PAGES, ROOT, read

work = sys.argv[1]
strip = lambda s: re.sub(r' data-i18n(?:-attr)?="[^"]*"', "", s)
gen = os.path.join(ROOT, "tools", "build-i18n.py")

# ---------- Prova A
ida = os.path.join(work, "identity")
subprocess.run([sys.executable, gen, "--lang", "pt", "--identity", "--strip-attrs", "--out", ida], check=True,
               stdout=subprocess.DEVNULL)
okA = 0
for rel, _ in PAGES:
    a, b = strip(read(os.path.join(ROOT, rel))), read(os.path.join(ida, rel))
    if a == b:
        okA += 1
    else:
        print("A DIFF", rel)
print("Prova A (identidade, byte a byte): %d/%d paginas identicas" % (okA, len(PAGES)))

# ---------- Prova B
pt = os.path.join(work, "real")
subprocess.run([sys.executable, gen, "--lang", "pt", "--strip-attrs", "--out", pt], check=True,
               stdout=subprocess.DEVNULL)
CATS = [
    ("assets +1 nivel (href/src)", lambda o, n: re.sub(r'((?:href|src)=")((?:\.\./)*assets/)', r"\1../\2", o) == n),
    ("logo href=\"/\" -> /pt/", lambda o, n: o.replace('href="/"', 'href="/pt/"') == n),
    ("form action -> /pt/...", lambda o, n: o.replace('action="/contato/obrigado.html"', 'action="/pt/contato/obrigado.html"') == n),
    ("canonical -> /pt/", lambda o, n: '<link rel="canonical"' in o and n == re.sub(r'(href="https://www\.nexyss\.com/)', r"\1pt/", o)),
    ("og:url -> /pt/", lambda o, n: 'property="og:url"' in o and n == re.sub(r'(content="https://www\.nexyss\.com/)', r"\1pt/", o)),
]


def classify(o, n):
    for name, f in CATS:
        if f(o, n):
            return name
    # linha com varias transformacoes juntas (ex.: href=/ e assets na mesma linha)
    t = o
    t = re.sub(r'((?:href|src)=")((?:\.\./)*assets/)', r"\1../\2", t)
    t = t.replace('href="/"', 'href="/pt/"')
    t = t.replace('action="/contato/obrigado.html"', 'action="/pt/contato/obrigado.html"')
    t = re.sub(r'(<link rel="canonical" href="https://www\.nexyss\.com/)', r"\1pt/", t)
    t = re.sub(r'(<meta property="og:url" content="https://www\.nexyss\.com/)', r"\1pt/", t)
    return "combinada (mais de uma categoria na linha)" if t == n else None


tot = collections.Counter()
unm = []
changed_pages = 0
for rel, _ in PAGES:
    a = strip(read(os.path.join(ROOT, rel))).split("\n")
    b = read(os.path.join(pt, "pt", rel)).split("\n")
    assert len(a) == len(b), (rel, len(a), len(b))
    n_changed = 0
    for i, (x, y) in enumerate(zip(a, b), 1):
        if x != y:
            n_changed += 1
            c = classify(x, y)
            if c:
                tot[c] += 1
            else:
                unm.append((rel, i, x[:90], y[:90]))
    changed_pages += 1 if n_changed else 0
print("\nProva B (/pt/ gerado vs pagina atual), linhas diferentes por categoria mapeada:")
for k, v in tot.most_common():
    print("  %-48s %4d" % (k, v))
print("  %-48s %4d" % ("NAO MAPEADAS", len(unm)))
for u in unm[:20]:
    print("   ", u)
print("paginas com alguma diferenca mapeada: %d/%d" % (changed_pages, len(PAGES)))
sys.exit(0 if okA == len(PAGES) and not unm else 1)
