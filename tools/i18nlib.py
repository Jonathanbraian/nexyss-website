"""Biblioteca compartilhada do pipeline i18n (marcador, extrator e gerador).

Modelo:
  * "unidade"  = elemento com data-i18n="chave". Valor da chave = HTML interno
    sem as "bordas" (espacos + <svg> + elementos que tem chave propria, no inicio
    e no fim), que ficam no template. Assim "Solicitar Demo <svg/>" vira
    "Solicitar Demo" e o badge de um <li> nao entra no texto da linha.
  * atributo   = data-i18n-attr="aria-label:chave;alt:outra"; valor = texto cru do atributo.
  * Todos os valores sao HTML-fonte (entidades como &amp; ficam como estao).
"""
import html
import os
import re
import unicodedata

from htmltree import parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src")

# (caminho em src/, prefixo de chave da pagina)
PAGES = [
    ("index.html", "home"),
    ("plataforma/index.html", "plat"),
    ("plataforma/crm/index.html", "crm"),
    ("plataforma/educacao/index.html", "edu"),
    ("plataforma/marketing/index.html", "mkt"),
    ("plataforma/finance/index.html", "fin"),
    ("plataforma/hr/index.html", "hr"),
    ("plataforma/ai/index.html", "ai"),
    ("plataforma/integracoes/index.html", "int"),
    ("solucoes/index.html", "solx"),
    ("solucoes/por-setor/index.html", "sols"),
    ("solucoes/por-funcao/index.html", "solf"),
    ("solucoes/por-objetivo/index.html", "solo"),
    ("solucoes/por-porte/index.html", "solp"),
    ("consultoria/index.html", "con"),
    ("sobre/index.html", "sobre"),
    ("contato/index.html", "contato"),
    ("contato/obrigado.html", "obrigado"),
]

INLINE = {"span", "a", "b", "strong", "em", "i", "small", "code", "sup", "sub",
          "mark", "abbr", "u", "s", "br", "kbd", "q", "cite", "time"}
SKIP_TAGS = {"script", "style", "svg", "head", "html", "#root"}
TEXT_ATTRS = ("aria-label", "alt", "title", "placeholder")
META_KINDS = {  # (atributo que identifica, valor) -> sufixo da chave
    ("name", "description"): "desc",
    ("property", "og:title"): "ogtitle",
    ("property", "og:description"): "ogdesc",
    ("property", "og:image:alt"): "ogimgalt",
    ("name", "twitter:title"): "twtitle",
    ("name", "twitter:description"): "twdesc",
}
WS = " \t\r\n"


def read(path):
    with open(path, encoding="utf-8", newline="") as f:
        return f.read()


def write(path, s):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(s)


def has_letters(raw):
    txt = html.unescape(raw)
    return any(unicodedata.category(c).startswith("L") for c in txt)


def slug(text, n=40):
    t = html.unescape(re.sub(r"<[^>]+>", " ", text))
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode()
    t = re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")
    return t[:n].strip("-") or "x"


def is_edge(c):
    return c.tag == "svg" or c.get("data-i18n") is not None


def split_edges(src, node):
    """Devolve (a, b): intervalo [a, b) do 'miolo' traduzivel dentro do elemento."""
    s1, e0 = node.s1, node.e0
    kids = node.children
    by_start = {c.s0: c for c in kids}
    by_end = {c.e1: c for c in kids}
    pos = s1
    while True:
        p = pos
        while p < e0 and src[p] in WS:
            p += 1
        c = by_start.get(p)
        if c is not None and is_edge(c):
            pos = c.e1
            continue
        pos = p
        break
    a = pos
    pos = e0
    while True:
        p = pos
        while p > a and src[p - 1] in WS:
            p -= 1
        c = by_end.get(p)
        if c is not None and is_edge(c) and c.s0 >= a:
            pos = c.s0
            continue
        pos = p
        break
    b = max(pos, a)
    return a, b


def attr_span(src, node, name):
    """Posicao [v0, v1) do valor cru do atributo `name` dentro da tag de abertura."""
    tag = src[node.s0:node.s1]
    m = re.search(r'(?<=[\s"\'])' + re.escape(name) + r'\s*=\s*"([^"]*)"', tag)
    if not m:
        return None
    return node.s0 + m.start(1), node.s0 + m.end(1)


def parse_attr_map(val):
    out = []
    for part in (val or "").split(";"):
        if part.strip():
            a, _, k = part.partition(":")
            out.append((a.strip(), k.strip()))
    return out


def in_shell(node):
    """Regiao compartilhada entre paginas (header, drawer, footer, skip-link)."""
    n = node
    while n is not None and n.tag != "#root":
        cls = (n.get("class") or "").split()
        if n.tag == "header" and "site" in cls:
            return "mega" if _under_mega(node) else "nav"
        if n.tag == "footer" and "site" in cls:
            return "footer"
        if "drawer" in cls or "drawer-overlay" in cls:
            return "nav"
        if "skip-link" in cls:
            return "a11y"
        n = n.parent
    return None


def _under_mega(node):
    n = node
    while n is not None:
        if "mega" in (n.get("class") or "").split():
            return True
        n = n.parent
    return False


def ctx_of(node):
    n = node
    while n is not None and n.tag != "#root":
        cls = (n.get("class") or "").split()
        if n.tag == "section":
            if n.get("id"):
                return n.get("id")
            for c in cls:
                if c not in ("block", "tinted", "deeper", "container"):
                    return c
            return "sec"
        if "subnav" in cls:
            return "subnav"
        n = n.parent
    return "page"


def under_keyed(node):
    n = node
    while n is not None and n.tag != "#root":
        if n.get("data-i18n") is not None:
            return n
        n = n.parent
    return None


def has_direct_text(node, src):
    return any(has_letters(src[a:b]) for a, b in node.texts)


def uncovered(tree, src):
    """Texto visivel / atributo traduzivel / meta SEM chave. Lista de (tag, trecho)."""
    out = []
    for n in tree.root.walk():
        if n.tag == "#root":
            continue
        if n.tag not in SKIP_TAGS and not any(
                a.tag in ("svg", "script", "style", "head") for a in _ancestors(n)):
            if under_keyed(n) is None:
                for a, b in n.texts:
                    if has_letters(src[a:b]):
                        out.append((n.tag, src[a:b].strip()[:50]))
        if n.tag == "title" and n.get("data-i18n") is None:
            out.append(("title", "sem chave"))
        if n.tag == "meta":
            for (an, av), _kind in META_KINDS.items():
                if n.get(an) == av and "content" not in {a for a, _ in parse_attr_map(n.get("data-i18n-attr"))}:
                    out.append(("meta", av))
            continue
        covered = {a for a, _ in parse_attr_map(n.get("data-i18n-attr"))}
        for an in TEXT_ATTRS:
            if n.tag == "title" and an == "title":
                continue
            v = n.get(an)
            if v and has_letters(v) and an not in covered:
                out.append((n.tag, an + "=" + v[:40]))
    return out


def _ancestors(n):
    p = n.parent
    while p is not None:
        yield p
        p = p.parent
