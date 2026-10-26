#!/usr/bin/env python3
"""Passo 3 - marca em src/ todo texto visivel e atributo traduzivel que ainda nao tem chave.

Idempotente: so insere data-i18n / data-i18n-attr onde faltam. Nao toca em mais nada
(o HTML continua byte a byte o mesmo, fora os atributos inseridos).

Uso: python3 tools/mark-keys.py [--dry-run] [--report arquivo.json]
"""
import collections
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from i18nlib import *  # noqa

dry = "--dry-run" in sys.argv
report_path = sys.argv[sys.argv.index("--report") + 1] if "--report" in sys.argv else None

pages = []
registry = {}      # chave -> valor (miolo)
conflicts = []


def reg(key, val, where):
    if key in registry and registry[key] != val:
        conflicts.append((key, where, registry[key][:60], val[:60]))
    registry.setdefault(key, val)


for rel, prefix in PAGES:
    src = read(os.path.join(SRC, rel))
    tree = parse(src)
    pages.append((rel, prefix, src, tree))
    for n in tree.root.walk():
        k = n.get("data-i18n")
        if k is not None and n.e0 is not None:
            a, b = split_edges(src, n)
            reg(k, src[a:b], rel)
        am = n.get("data-i18n-attr")
        if am:
            for attr, key in parse_attr_map(am):
                sp = attr_span(src, n, attr)
                if sp:
                    reg(key, src[sp[0]:sp[1]], rel)


def alloc(base, val, reuse):
    """Escolhe a chave: reaproveita a existente se o valor for igual (shell), senao sufixa."""
    k, i = base, 1
    while True:
        if k not in registry:
            registry[k] = val
            return k
        if reuse and registry[k] == val:
            return k
        i += 1
        k = "%s-%d" % (base, i)


def find_unit(n, src):
    u = n
    while u.tag in INLINE:
        p = u.parent
        if p is None or p.tag in ("#root", "body"):
            break
        if has_direct_text(p, src) or p.tag in INLINE:
            u = p
            continue
        break
    return u


stats = collections.OrderedDict()
warnings = []
total_edits = 0
for rel, prefix, src, tree in pages:
    edits = collections.defaultdict(list)   # posicao de insercao -> [texto]
    counters = collections.Counter()
    st = collections.Counter()
    new_units = {}                          # id(node) -> (node, key)

    def insert_at(node, text):
        raw = src[node.s0:node.s1]
        pos = node.s1 - (2 if raw.endswith("/>") else 1)
        edits[pos].append(text)

    # a) badges sem chave
    for n in tree.root.walk():
        cls = (n.get("class") or "").split()
        if "status-badge" in cls and n.get("data-i18n") is None and n.e0 is not None:
            mod = [c for c in cls if c.startswith("status-badge--")]
            state = mod[0].split("--")[1] if mod else "x"
            a, b = split_edges(src, n)
            key = alloc("badge." + state, src[a:b], True)
            insert_at(n, ' data-i18n="%s"' % key)
            new_units[id(n)] = n
            st["badge"] += 1

    # b) head: <title> e metas
    for n in tree.root.walk():
        if n.tag == "title" and n.get("data-i18n") is None:
            a, b = split_edges(src, n)
            key = alloc("meta.%s.title" % prefix, src[a:b], False)
            insert_at(n, ' data-i18n="%s"' % key)
            new_units[id(n)] = n
            st["meta"] += 1
        elif n.tag == "meta" and not n.get("data-i18n-attr"):
            for (an, av), kind in META_KINDS.items():
                if n.get(an) == av:
                    sp = attr_span(src, n, "content")
                    key = alloc("meta.%s.%s" % (prefix, kind), src[sp[0]:sp[1]], False)
                    insert_at(n, ' data-i18n-attr="content:%s"' % key)
                    st["meta"] += 1

    # c) unidades de texto
    for n in tree.root.walk():
        if n.tag in SKIP_TAGS or n.tag == "title" or n.tag == "#root":
            continue
        anc = n
        skip = False
        while anc is not None and anc.tag != "#root":
            if anc.tag in ("svg", "script", "style", "head"):
                skip = True
                break
            anc = anc.parent
        if skip or not any(has_letters(src[a:b]) for a, b in n.texts):
            continue
        if under_keyed(n) is not None and n.get("data-i18n") is None:
            # texto dentro de unidade ja chaveada (ou se o proprio no ja tem chave): coberto
            continue
        if n.get("data-i18n") is not None:
            continue
        u = find_unit(n, src)
        if id(u) in new_units or under_keyed(u) is not None:
            continue
        if u.tag in ("body", "html"):
            warnings.append((rel, "texto solto em <%s>" % u.tag, src[n.texts[0][0]:n.texts[0][1]][:50]))
            continue
        a, b = split_edges(src, u)
        val = src[a:b]
        region = in_shell(u)
        if region:
            key = alloc("%s.%s" % (region, slug(val)), val, True)
            st[region] += 1
        else:
            c = ctx_of(u)
            counters[(c, u.tag)] += 1
            while True:
                base = "%s.%s.%s%d" % (prefix, c, u.tag, counters[(c, u.tag)])
                if base not in registry:
                    break
                counters[(c, u.tag)] += 1
            key = alloc(base, val, False)
            st["corpo"] += 1
        new_units[id(u)] = u
        insert_at(u, ' data-i18n="%s"' % key)

    # d) atributos traduzivei
    for n in tree.root.walk():
        if n.tag in ("#root", "meta") or n.e0 is None and n.tag not in ("img", "input"):
            continue
        todo = []
        existing = {a for a, _ in parse_attr_map(n.get("data-i18n-attr"))}
        for an in TEXT_ATTRS:
            if an == "title" and n.tag in ("title",):
                continue
            v = n.get(an)
            if v and has_letters(v) and an not in existing:
                todo.append(an)
        if not todo:
            continue
        region = in_shell(n)
        parts = []
        for an in todo:
            sp = attr_span(src, n, an)
            val = src[sp[0]:sp[1]]
            if region:
                key = alloc("a11y." + slug(val), val, True)
                st["a11y"] += 1
            else:
                c = ctx_of(n)
                counters[(c, an)] += 1
                while True:
                    base = "%s.%s.%s%d" % (prefix, c, an.replace("aria-label", "aria"), counters[(c, an)])
                    if base not in registry:
                        break
                    counters[(c, an)] += 1
                key = alloc(base, val, False)
                st["attr"] += 1
            parts.append("%s:%s" % (an, key))
        insert_at(n, ' data-i18n-attr="%s"' % ";".join(parts))

    # e) avisos estruturais: unidade nova contendo outra unidade em posicao interna
    for u in new_units.values():
        if u.e0 is None:
            continue
        a, b = split_edges(src, u)
        for c in u.walk():
            if c is u:
                continue
            if c.get("data-i18n") is not None and a <= c.s0 and c.e1 <= b:
                warnings.append((rel, "unidade aninhada em posicao interna", c.get("data-i18n")))
        if u.tag not in INLINE:
            for c in u.children:
                if c.tag not in INLINE and c.tag != "svg" and c.get("data-i18n") is None and any(
                        has_letters(src[x:y]) for d in c.walk() for x, y in d.texts) and has_direct_text(u, src):
                    warnings.append((rel, "bloco com texto proprio e filhos-bloco com texto", u.tag + ":" + (u.get("class") or "")))
                    break

    stats[rel] = dict(st)
    stats[rel]["_novas"] = sum(len(v) for v in edits.values())
    total_edits += stats[rel]["_novas"]

    if edits and not dry:
        out = src
        for pos in sorted(edits, reverse=True):
            out = out[:pos] + "".join(edits[pos]) + out[pos:]
        write(os.path.join(SRC, rel), out)

print("%-38s %6s  %s" % ("pagina", "novas", "detalhe"))
for rel, st in stats.items():
    print("%-38s %6d  %s" % (rel, st["_novas"], {k: v for k, v in st.items() if k != "_novas"}))
print("total de insercoes:", total_edits, "| chaves no registro:", len(registry))
print("conflitos de valor (chave igual, texto diferente):", len(conflicts))
for c in conflicts[:15]:
    print("  ", c)
print("avisos:", len(warnings))
for w in warnings[:40]:
    print("  ", w)
if report_path:
    json.dump({"stats": stats, "warnings": warnings, "conflicts": conflicts,
               "registry_size": len(registry)}, open(report_path, "w"), ensure_ascii=False, indent=1)
