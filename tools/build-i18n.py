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
BASE_URL = "https://nexyss-website.netlify.app"   # dominio provisorio (decisao D1, 26/10/2026): trocar aqui quando o dominio oficial existir
PLACEHOLDER = "https://www.nexyss.com"            # dominio placeholder que ainda esta nos templates de src/
LANGS = ["en", "pt", "es"]
HREFLANG = {"en": "en", "pt": "pt", "es": "es"}
X_DEFAULT = "en"
NO_SEO = {"contato/obrigado.html", "404.html"}    # noindex: sem hreflang, fora do sitemap
# travessoes (U+2013/2014/2015/2212) e as entidades equivalentes; montados por codigo para este arquivo passar na propria checagem R6
DASH = re.compile("[" + "".join(chr(c) for c in (0x2013, 0x2014, 0x2015, 0x2212)) + "]|&(?:" + "|".join(("m", "n")[j] + "dash" for j in (0, 1)) + "|mi" + "nus|hor" + "bar);")

ap = argparse.ArgumentParser()
ap.add_argument("--lang", default="pt")
ap.add_argument("--out")
ap.add_argument("--check", action="store_true")
ap.add_argument("--identity", action="store_true")
ap.add_argument("--strip-attrs", action="store_true")
ap.add_argument("--base-url", default=BASE_URL)
ap.add_argument("--site", action="store_true", help="tambem gera sitemap.xml e robots.txt em --out")
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


def page_urls(rel, base):
    """URL absoluta de cada versao (idioma) da pagina."""
    return {l: "%s/%s/%s" % (base, l, page_url_path(rel)) for l in LANGS}


LANG_NAMES = {"en": "English", "pt": "Portugu\u00eas", "es": "Espa\u00f1ol"}
ARR = '<svg width="10" height="10" viewBox="0 0 10 10" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M2.5 4l2.5 2.5L7.5 4"/></svg>'


def lang_links(rel, lang, cls_a):
    """3 links reais para a MESMA pagina nos outros idiomas (gerados no build, nao em runtime)."""
    path = "" if rel == "404.html" else page_url_path(rel)     # a 404 e servida em qualquer URL: vai para a Home
    rows = []
    for l in LANGS:
        cur = ' aria-current="true"' if l == lang else ""
        rows.append('<a%s href="/%s/%s" hreflang="%s" lang="%s" data-lang="%s"%s><b>%s</b><span>%s</span></a>'
                    % (cls_a, l, path, HREFLANG[l], HREFLANG[l], l, cur, l.upper(), LANG_NAMES[l]))
    return rows


def lang_widgets(out, rel, lang):
    label = dicts[lang]["a11y.idioma"]
    rows = lang_links(rel, lang, "")
    menu = "".join("<li>%s</li>" % r for r in rows)
    header = ('<div class="lang-switch"><button type="button" class="lang-btn" aria-label="%s: %s">'
              '<span>%s</span>%s</button><ul class="lang-menu">%s</ul></div>'
              % (label, LANG_NAMES[lang], lang.upper(), ARR, menu))
    drawer = '<div class="drawer-lang" role="group" aria-label="%s">%s</div>' % (label, "".join(lang_links(rel, lang, "")))
    out = out.replace("<!--NX:LANGSWITCH-->", header).replace("<!--NX:DRAWERLANG-->", drawer)
    return out


def transform(out, rel, lang, base):
    """Caminho/SEO especifico do idioma (nao roda em --identity)."""
    out = lang_widgets(out, rel, lang)
    out = re.sub(r'(<html\b[^>]*\blang=")[^"]*(")', r"\g<1>%s\g<2>" % LANG_ATTR[lang], out, count=1)
    out = re.sub(r'((?:href|src)=")((?:\.\./)*assets/)', r"\1../\2", out)     # assets sobem um nivel (so relativos)
    out = out.replace("/__LANG__/", "/%s/" % lang)                              # 404: links absolutos, servida em qualquer URL
    out = out.replace('href="/"', 'href="/%s/"' % lang)
    out = out.replace('action="/contato/obrigado.html"', 'action="/%s/contato/obrigado.html"' % lang)
    urls = page_urls(rel, base)
    out = re.sub(r'(<link rel="canonical" href=")[^"]*(")', lambda m: m.group(1) + urls[lang] + m.group(2), out, count=1)
    out = re.sub(r'(<meta property="og:url" content=")[^"]*(")', lambda m: m.group(1) + urls[lang] + m.group(2), out, count=1)
    # og:locale + alternates
    alts = "".join('\n<meta property="og:locale:alternate" content="%s" />' % OG_LOCALE[l] for l in LANGS if l != lang)
    out = re.sub(r'(<meta property="og:locale" content=")[^"]*("[^>]*>)',
                 lambda m: m.group(1) + OG_LOCALE[lang] + m.group(2) + alts, out, count=1)
    # hreflang (+ x-default) logo apos o canonical; nao em paginas noindex
    if rel not in NO_SEO:
        tags = "".join('\n<link rel="alternate" hreflang="%s" href="%s" />' % (HREFLANG[l], urls[l]) for l in LANGS)
        tags += '\n<link rel="alternate" hreflang="x-default" href="%s" />' % urls[X_DEFAULT]
        out = re.sub(r'(<link rel="canonical" href="[^"]*" />)', lambda m: m.group(1) + tags, out, count=1)
    # dominio placeholder remanescente (og:image, twitter:image) e comentario
    out = out.replace(PLACEHOLDER, base)
    out = re.sub(r"<!-- TODO: confirmar dominio oficial antes de publicar \(placeholder: nexyss\.com\) -->",
                 "<!-- BASE_URL provisorio (netlify.app): trocar em tools/build-i18n.py quando o dominio oficial for confirmado -->", out)
    return out


def sitemap_xml(base):
    rows = ['<?xml version="1.0" encoding="UTF-8"?>',
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for rel, _prefix in PAGES:
        if rel in NO_SEO:
            continue
        urls = page_urls(rel, base)
        for l in LANGS:
            rows.append("  <url>")
            rows.append("    <loc>%s</loc>" % urls[l])
            for m in LANGS:
                rows.append('    <xhtml:link rel="alternate" hreflang="%s" href="%s"/>' % (HREFLANG[m], urls[m]))
            rows.append('    <xhtml:link rel="alternate" hreflang="x-default" href="%s"/>' % urls[X_DEFAULT])
            rows.append("  </url>")
    rows.append("</urlset>")
    return "\n".join(rows) + "\n"


def robots_txt(base):
    # obrigado.html e 404 ficam FORA do Disallow de proposito: o noindex so funciona se o robo puder ler a pagina
    return "User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % base


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

if args.site and not args.check and not errors:
    write(os.path.join(args.out, "sitemap.xml"), sitemap_xml(args.base_url))
    write(os.path.join(args.out, "robots.txt"), robots_txt(args.base_url))

unused = [k for k in pt if k not in all_used and k != "a11y.idioma"]   # a11y.idioma e lido pelo gerador (seletor)
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
