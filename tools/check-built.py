#!/usr/bin/env python3
"""Protecao contra deriva: o HTML gerado (en/ pt/ es/ + sitemap.xml + robots.txt) tem que ser
exatamente o que o gerador produz hoje a partir de src/ + i18n/*.json.

  python3 tools/check-built.py

Regenera numa pasta temporaria e compara com o repositorio. Sai com 1 se alguem editou HTML gerado a
mao, se faltar arquivo, se sobrar arquivo, ou se src/ e dicionarios mudaram sem regenerar
(rode: python3 tools/build-i18n.py --lang all --site --out .).
"""
import filecmp
import os
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LANGS = ["en", "pt", "es"]
FILES = ["sitemap.xml", "robots.txt"]


def tree(base):
    out = set()
    for l in LANGS:
        for dp, _dn, fns in os.walk(os.path.join(base, l)):
            for f in fns:
                out.add(os.path.relpath(os.path.join(dp, f), base))
    return out


with tempfile.TemporaryDirectory() as tmp:
    r = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "build-i18n.py"), "--lang", "all", "--site", "--out", tmp],
                       capture_output=True, text=True)
    if r.returncode:
        print("FALHOU o gerador:\n" + r.stdout + r.stderr)
        sys.exit(1)
    want, have = tree(tmp) | set(FILES), tree(ROOT) | {f for f in FILES if os.path.exists(os.path.join(ROOT, f))}
    missing, extra = sorted(want - have), sorted(have - want)
    diff = [f for f in sorted(want & have) if not filecmp.cmp(os.path.join(tmp, f), os.path.join(ROOT, f), shallow=False)]
    print("gerados: %d arquivos | no repo: %d" % (len(want), len(have)))
    for tag, lst in (("FALTANDO no repo", missing), ("SOBRANDO no repo (nao gerado)", extra), ("DIFERENTES do gerador", diff)):
        if lst:
            print("%s: %d" % (tag, len(lst)))
            for f in lst[:15]:
                print("   ", f)
    if missing or extra or diff:
        print("\nREPROVADO: regenere com  python3 tools/build-i18n.py --lang all --site --out .   (nao edite HTML gerado a mao)")
        sys.exit(1)
    print("OK: en/ pt/ es/ sitemap.xml robots.txt identicos ao gerador")
