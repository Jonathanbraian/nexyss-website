#!/usr/bin/env python3
"""Aplica a planilha revisada (CSV do Jonathan) em i18n/pt.json, en.json e es.json.

  python3 tools/apply-revisao.py tools/revisao-estrategica-aplicada.csv [--dry-run] [--report arq.json]

Regras:
  * "Verificado" -> mantem o dicionario atual (so confere e reporta divergencia).
  * "Revisado"   -> grava PT, EN e ES da planilha em TODAS as chaves que compartilham o texto PT atual.
  * [[destaque]] volta a ser o <span> do valor atual; " / " volta a ser <br>.
  * R6: travessao (U+2013/U+2014) vira hifen com espacos; o Excel/edicao costuma reintroduzi-lo.
  * Defeito conhecido da planilha corrigido: "usually be introduced", "usually are typically introduced".
"""
import collections
import csv
import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
csv_path = sys.argv[1]
dry = "--dry-run" in sys.argv
rep_path = sys.argv[sys.argv.index("--report") + 1] if "--report" in sys.argv else None
D = {l: json.load(open(os.path.join(ROOT, "i18n", l + ".json"), encoding="utf-8")) for l in ("pt", "en", "es")}
DASH = "[" + chr(0x2013) + chr(0x2014) + "]"
FIX_EN = [("usually be introduced first", "are usually introduced first"),
          ("usually are typically introduced first", "are usually introduced first")]
SPECIAL = {  # chaves cujo HTML tem estrutura propria (header: o prefixo "Nexyss " some abaixo de 1340px)
    "nav.nexyss-consultoria": '<span class="nav-nx">Nexyss </span>Consulting',
}


def readable(v):
    v = re.sub(r"<span class=\"accent\">(.*?)</span>", r"[[\1]]", v, flags=re.S)
    v = re.sub(r"<span style=\"[^\"]*\">(.*?)</span>", r"[[\1]]", v, flags=re.S)
    v = re.sub(r"<br\s*/?>", " / ", v)
    v = re.sub(r"<[^>]+>", "", v)
    return re.sub(r"\s+", " ", html.unescape(v)).strip()


def norm(s):
    s = re.sub(r"\s*" + DASH + r"\s*", " - ", s)
    return re.sub(r"\s+", " ", s).strip()


def esc(t):
    return re.sub(r"&(?![#\w]+;)", "&amp;", t)


def to_html(new, cur):
    """Reconstroi o HTML do valor a partir do texto legivel da planilha, usando o valor atual como molde."""
    opens = re.findall(r"<span (?:class=\"accent\"|style=\"[^\"]*\")>", cur)
    parts = re.split(r"\[\[(.*?)\]\]", new)
    n_acc = (len(parts) - 1) // 2
    if n_acc != len(opens):
        raise ValueError("destaque: planilha tem %d, valor atual tem %d" % (n_acc, len(opens)))
    if cur.count("<br>") != new.count(" / "):
        raise ValueError("quebras: planilha tem %d, valor atual tem %d" % (new.count(" / "), cur.count("<br>")))
    others = re.sub(r"<span (?:class=\"accent\"|style=\"[^\"]*\")>.*?</span>|<br>", "", cur, flags=re.S)
    if re.search(r"<[^>]+>", others):
        raise ValueError("valor atual tem outras tags: " + others[:60])
    out, a = [], 0
    for i, p in enumerate(parts):
        seg = esc(p).replace(" / ", "<br>")
        if i % 2:
            out.append(opens[a] + seg + "</span>")
            a += 1
        else:
            out.append(seg)
    return "".join(out)


rows = list(csv.DictReader(open(csv_path, encoding="utf-8-sig")))
stat = collections.Counter()
by_group = collections.defaultdict(collections.Counter)
pt_diffs, mismatches, errors, dashes, fixed_en = [], [], [], [], []
changes = {"pt": {}, "en": {}, "es": {}}
for r in rows:
    k, g = r["chave"], r["grupo"]
    status = r["revisao"].split(" ")[0]
    cur = {l: D[l][k] for l in D}
    same_pt = [x for x in D["pt"] if D["pt"][x] == cur["pt"]]
    if len(same_pt) != int(r["outras_chaves"]) + 1:
        mismatches.append((k, "grupo de chaves: planilha %d, dicionario %d" % (int(r["outras_chaves"]) + 1, len(same_pt))))
    sheet = {"pt": r["PT (original)"], "en": r["EN (proposta, britanico)"], "es": r["ES (proposta)"]}
    if status == "Verificado":
        by_group[g]["Verificado"] += 1
        for l in D:                         # conferencia: o que o Jonathan chamou de verificado bate com o dicionario?
            if norm(sheet[l]) != norm(readable(cur[l])):
                mismatches.append((k, "Verificado mas %s difere: dic=%r planilha=%r" % (l.upper(), readable(cur[l])[:70], sheet[l][:70])))
        continue
    by_group[g]["Revisado"] += 1
    for l in D:
        s = sheet[l]
        if re.search(DASH, s):
            dashes.append((k, l))
        s = norm(s)
        if l == "en":
            for a, b in FIX_EN:
                if a in s:
                    fixed_en.append(k)
                    s = s.replace(a, b)
        try:
            new_html = SPECIAL[k] if k in SPECIAL else to_html(s, cur[l])
        except ValueError as e:
            errors.append((k, l, str(e)))
            continue
        if readable(new_html) != readable(cur[l]):
            for x in same_pt:
                changes[l][x] = new_html
            if l == "pt":
                pt_diffs.append((k, readable(cur[l]), readable(new_html), len(same_pt)))
stat = {l: len(changes[l]) for l in changes}
print("Linhas:", len(rows), dict(collections.Counter(r["revisao"].split(" ")[0] for r in rows)))
print("\nPor grupo (Verificado / Revisado):")
for g, c in by_group.items():
    print("  %-30s %3d / %3d" % (g, c["Verificado"], c["Revisado"]))
print("\nChaves que mudam (com propagacao de textos repetidos): PT %d | EN %d | ES %d" % (stat["pt"], stat["en"], stat["es"]))
print("Linhas com travessao na planilha (convertido para hifen):", len({k for k, l in dashes}), "| celulas:", len(dashes))
print("Defeitos de EN corrigidos:", len(set(fixed_en)), sorted(set(fixed_en)))
print("Erros de reconstrucao HTML:", len(errors))
for e in errors:
    print("  ", e)
print("Divergencias em 'Verificado' / grupos:", len(mismatches))
for m in mismatches[:20]:
    print("  ", m)
if rep_path:
    json.dump({"pt_diffs": pt_diffs, "stat": stat, "mismatches": mismatches, "errors": errors,
               "dashes": dashes, "fixed_en": sorted(set(fixed_en))}, open(rep_path, "w"), ensure_ascii=False, indent=1)
if errors:
    sys.exit(1)
if not dry:
    for l in D:
        D[l].update(changes[l])
        json.dump(D[l], open(os.path.join(ROOT, "i18n", l + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        open(os.path.join(ROOT, "i18n", l + ".json"), "a").write("\n")
    print("\nAplicado em i18n/{pt,en,es}.json")
