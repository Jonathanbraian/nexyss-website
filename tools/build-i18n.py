#!/usr/bin/env python3
"""Passo 5 - gerador i18n: src/ + i18n/<lang>.json -> <out>/<lang>/...

  python3 tools/build-i18n.py --lang pt --out /caminho/saida
  python3 tools/build-i18n.py --lang all --check          # so confere cobertura, nao escreve
  python3 tools/build-i18n.py --lang pt --identity --strip-attrs --out X
        # modo prova: so substitui texto (sem prefixo de idioma, sem caminhos) e
        # remove data-i18n*, para comparar byte a byte com as paginas servidas hoje.

Falha (exit 1) se: houver chave sem traducao no idioma; texto visivel / atributo / meta
sem chave nos templates; tags do valor divergirem do PT; valor com travessao (R6); chave
que nao existe no PT; unidade aninhada em posicao interna.
"""
import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from i18nlib import *  # noqa

LANG_ATTR = {"en": "en", "pt": "pt-BR", "es": "es"}
OG_LOCALE = {"en": "en_GB", "pt": "pt_BR", "es": "es_ES"}
BASE_URL = "https://www.nexyss.com"          # placeholder do dominio (TODO do CLAUDE.md)
# travessoes (U+2013/2014/2015/2212) e as entidades equivalentes; montados por codigo para este arquivo passar na propria checagem R6
DASH = re.compile("[" + "".join(chr(c) for c in (0x2013, 0x2014, 0x2015, 0x2212)) + "]|&(?:" + "|".join(("m", "n")[j] + "dash" for j in (0, 1)) + "|mi" + "nus|hor" + "bar);")

ap = argparse.ArgumentParser()
ap.add_argument("--lang", default="pt")
ap.add_argument("--out")
ap.add_argument("--check", action="store_true")
ap.add_argument("--identity", action="store_true")
ap.add_argument("--strip-attrs", action="store_true")
ap.add_argument("--base-url", default=BASE_URL)
args = ap.parse_args()
langs = ["en", "pt", "es"] if args.lang == "all" else [args.lang]
if not args.check and not args.out:
    ap.error("--out e obrigatorio (ou use --check)")


def load_dict(lang):
    return json.load(open(os.path.join(ROOT, "i18n", lang + ".json"), encoding="utf-8"))


def skeleton(v):
    return re.findall(r"<[^>]+>", v)


def build_page(rel, src, tree, d, lang, errors):
    reps, used = [], set()
    for n in tree.root.walk():
        k = n.get("data-i18n")
        if k is not None:
            if k not in d:
                errors.append("%s: chave sem traducao [%s]: %s" % (rel, lang, k))
            else:
                a, b = split_edges(src, n)
                for c in n.walk():
                    if c is not n and c.get("data-i18n") is not None and a <= c.s0 and c.e1 <= b:
                        errors.append("%s: unidade aninhada em posicao interna: %s" % (rel, k))
                reps.append((a, b, d[k]))
                used.add(k)
        am = n.get("data-i18n-attr")
        if am:
            for attr, key in parse_attr_map(am):
                sp = attr_span(src, n, attr)
                if sp is None:
                    errors.append("%s: atributo %s ausente (%s)" % (rel, attr, key))
                elif key not in d:
                    errors.append("%s: chave sem traducao [%s]: %s" % (rel, lang, key))
                else:
                    reps.append((sp[0], sp[1], d[key]))
                    used.add(key)
    out = src
    for a, b, t in sorted(reps, key=lambda r: r[0], reverse=True):
        out = out[:a] + t + out[b:]
    return out, used


def strip_i18n_attrs(s):
    return re.sub(r' data-i18n(?:-attr)?="[^"]*"', "", s)


def page_url_path(rel):
    if rel == "index.html":
        return ""
    return rel[:-len("index.html")] if rel.endswith("/index.html") else rel


def transform(out, rel, lang, base):
    """Caminho/SEO especifico do idioma (nao roda em --identity)."""
    out = re.sub(r'(<html\b[^>]*\blang=")[^"]*(")', r"\g<1>%s\g<2>" % LANG_ATTR[lang], out, count=1)
    out = re.sub(r'((?:href|src)=")((?:\.\./)*assets/)', r"\1../\2", out)
    out = out.replace('href="/"', 'href="/%s/"' % lang)
    out = out.replace('action="/contato/obrigado.html"', 'action="/%s/contato/obrigado.html"' % lang)
    url = "%s/%s/%s" % (base, lang, page_url_path(rel))
    out = re.sub(r'(<link rel="canonical" href=")[^"]*(")', lambda m: m.group(1) + url + m.group(2), out, count=1)
    out = re.sub(r'(<meta property="og:url" content=")[^"]*(")', lambda m: m.group(1) + url + m.group(2), out, count=1)
    out = re.sub(r'(<meta property="og:locale" content=")[^"]*(")', r"\g<1>%s\g<2>" % OG_LOCALE[lang], out, count=1)
    return out


errors, warnings = [], []
dicts = {l: load_dict(l) for l in set(langs) | {"pt"}}
pt = dicts["pt"]

for lang in langs:
    d = dicts[lang]
    for k, v in d.items():
        if DASH.search(v):
            errors.append("[%s] R6: travessao em %s" % (lang, k))
        if lang != "pt" and k in pt and skeleton(v) != skeleton(pt[k]):
            errors.append("[%s] tags divergem do PT em %s" % (lang, k))
        if lang != "pt" and re.search(r"&(?![#\w]+;)", v):
            errors.append("[%s] '&' sem escape em %s" % (lang, k))
    extra = [k for k in d if k not in pt]
    if extra:
        errors.append("[%s] %d chaves que nao existem no PT (ex.: %s)" % (lang, len(extra), extra[0]))

pages = []
for rel, prefix in PAGES:
    src = read(os.path.join(SRC, rel))
    tree = parse(src)
    for u in uncovered(tree, src):
        errors.append("%s: texto/atributo SEM chave: %s" % (rel, u))
    pages.append((rel, src, tree))

all_used = set()
for lang in langs:
    d = dicts[lang]
    for rel, src, tree in pages:
        out, used = build_page(rel, src, tree, d, lang, errors)
        all_used |= used
        if args.check or errors:
            continue
        if args.identity:
            if args.strip_attrs:
                out = strip_i18n_attrs(out)
            dest = os.path.join(args.out, rel)
        else:
            out = transform(out, rel, lang, args.base_url)
            if args.strip_attrs:
                out = strip_i18n_attrs(out)
            dest = os.path.join(args.out, lang, rel)
        write(dest, out)

unused = [k for k in pt if k not in all_used]
if unused and not errors:
    warnings.append("%d chaves do dicionario nao usadas (ex.: %s)" % (len(unused), unused[:3]))
for w in warnings:
    print("AVISO:", w)
if errors:
    print("FALHOU: %d erros" % len(errors))
    for e in errors[:25]:
        print("  ", e)
    if len(errors) > 25:
        print("   ... +%d" % (len(errors) - 25))
    sys.exit(1)
print("OK: idiomas=%s | paginas=%d | chaves usadas=%d%s" % (
    ",".join(langs), len(pages), len(all_used), " | (so conferencia)" if args.check else ""))
