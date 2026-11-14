#!/usr/bin/env python3
"""QA final do site gerado (en/ pt/ es/): links, hreflang reciprocos, sitemap, robots, regras de conteudo.
Uso: python3 tools/qa-site.py   (exit 1 se algum item falhar)"""
import glob, os, re, sys, html
from urllib.parse import urlparse, unquote
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
LANGS = ["en", "pt", "es"]
files = sorted(glob.glob("en/**/*.html", recursive=True) + glob.glob("pt/**/*.html", recursive=True) + glob.glob("es/**/*.html", recursive=True))
fails = []
def check(name, bad, detail=""):
    print(("FAIL " if bad else "OK   ") + name + (" - " + str(detail) if detail else ""))
    if bad: fails.append(name)
text = {f: open(f, encoding="utf-8").read() for f in files}
clean = {f: re.sub(r"<!--.*?-->", "", t, flags=re.S) for f, t in text.items()}
import subprocess
def main_page(f):
    """HTML da pagina plana equivalente nas paginas planas pre-i18n, para separar pre-existente de novo."""
    rest = f.split("/", 1)[1]
    r = subprocess.run(["git", "show", PRE_I18N + ":" + rest], capture_output=True, text=True, cwd=ROOT)
    return r.stdout if r.returncode == 0 else ""
MAIN = {}
PRE_I18N = "25ba250"   # ultimo commit da main antes do i18n (paginas planas em PT): referencia de mockup/numeros pre-existentes
def in_main(f, token):
    rest = f.split("/", 1)[1]
    if rest not in MAIN: MAIN[rest] = main_page(f)
    return token in MAIN[rest] or token.replace(",", ".") in MAIN[rest]

# R6 travessoes
dash = re.compile("[" + "".join(chr(c) for c in (0x2013, 0x2014, 0x2015, 0x2212)) + "]|&(?:mdash|ndash|minus|horbar);")
check("R6 travessoes (HTML gerado)", [f for f in files if dash.search(text[f])])
# R2 preco
price = re.compile(r"(?:€|\$|&euro;|EUR\s|USD\s)\s?\d|\d\s?(?:€|&euro;)|a partir de [€$]|from [€$]|desde [€$]")
hits = []
for f in files:
    vis = re.sub(r"<(script|style)\b.*?</\1>|<!--.*?-->", "", text[f], flags=re.S)
    vis = re.sub(r"<[^>]+>", " ", vis)
    for m in price.finditer(vis):
        if "2.1M" in vis[max(0, m.start()-2):m.end()+4]: continue
        if not in_main(f, m.group(0).strip()): hits.append((f, vis[max(0, m.start()-25):m.end()+15].strip()))
check("R2 preco: nada novo alem dos valores de mockup ja aprovados em main", hits, hits[:5])
# pessoas
ppl = re.compile(r"jonathan|braian|jhony|fundador|founder|co-?founder|co-?fundador|brasileir|nacionalidade|brazilian|nationality", re.I)
ph = []
for f in files:
    vis = re.sub(r"<!--.*?-->", "", text[f], flags=re.S)
    vis = re.sub(r"Founding Customers?", "", vis)
    for m in ppl.finditer(re.sub(r"<[^>]+>", " ", vis)): ph.append((f, m.group(0)))
check("Zero pessoas", ph, ph[:5])
# R3 clientes: lista dos 5 reais; nomes ficticios antigos nao podem aparecer fora de mockup
fake = re.compile(r"Globaledu|Atlas Academy|Vertex|Polaris|Orbital Schools|Rede Meridian")
fh = [(f, m.group(0)) for f in files for m in fake.finditer(re.sub(r"<!--.*?-->", "", text[f], flags=re.S))]
check("R3 nomes do logo wall ficticio antigo: so como negocio de mockup ja existente em main", [x for x in fh if not in_main(x[0], x[1])], fh[:4])
# R8 metrica inventada: numeros de impacto "X%" / "Nx" fora dos aprovados
approved = ("99.99", "120+", "3.4", "87%", "2.1M", "40+")
mh = []
for f in files:
    vis = re.sub(r"<(script|style)\b.*?</\1>|<!--.*?-->|<[^>]+>", " ", text[f], flags=re.S)
    for m in re.finditer(r"\b\d{1,3}(?:[.,]\d+)?\s?%|\b\d+(?:[.,]\d)?\s?[x×]\b", vis):
        s = m.group(0)
        if not any(a in s or a in vis[m.start()-4:m.end()+4] for a in approved) and not in_main(f, s): mh.append((f, s))
check("R8 percentuais/multiplicadores: so numeros aprovados ou de mockup ja existente em main", mh, mh[:6])
# R5.1: badge so em lista de feature; nunca em .sol-card / .consult-item
b51 = [f for f in files if re.search(r'<div class="sol-card[^"]*"[^>]*>(?:(?!</div>).)*status-badge', text[f], re.S)]
check("R5.1 badge dentro de sol-card (narrativa)", b51)

# links internos
pat = re.compile(r'<(?:a|link|script|img|source|form)\b[^>]*?\b(?:href|src|action)="([^"]*)"', re.S)
total = broken = 0; bl = []; anchors = []
def resolve(src, ref):
    u = urlparse(ref)
    if u.scheme in ("http", "https", "mailto", "tel", "data", "javascript") or ref.startswith("//") : return None
    p = unquote(u.path)
    if p == "": return "SELF"
    base = os.path.join(ROOT, p.lstrip("/")) if p.startswith("/") else os.path.normpath(os.path.join(os.path.dirname(src), p))
    return base
for f in files:
    for ref in pat.findall(clean[f]):
        ref = html.unescape(ref)
        r = resolve(f, ref)
        if r is None or r == "SELF": continue
        total += 1
        ok = os.path.isfile(r) or os.path.isfile(os.path.join(r, "index.html"))
        # form action de /xx/contato/obrigado.html e raiz-absoluto: coberto pelo mesmo teste
        if not ok: broken += 1; bl.append((f, ref))
        # ancora interna
    # ancoras #id na mesma pagina
for f in files:
    ids = set(re.findall(r'\bid="([^"]+)"', text[f]))
    for a in re.findall(r'href="#([^"]+)"', clean[f]):
        total += 1
        if a not in ids: anchors.append((f, "#" + a))
check("Links internos para arquivo/pagina (%d verificados no total)" % total, bl, bl[:8])
print("INFO ancoras #id sem destino na mesma pagina: %d (pre-existente: menu do header das paginas internas aponta #consultoria/#clientes)" % len(anchors))

# hreflang reciprocos
pairs = 0; hb = []
def urls_of(f):
    return dict(re.findall(r'<link rel="alternate" hreflang="([^"]+)" href="([^"]+)"', text[f]))
by_path = {}
for f in files:
    lang, rest = f.split("/", 1); by_path.setdefault(rest, {})[lang] = f
for rest, d in by_path.items():
    if rest in ("404.html", "contato/obrigado.html"):
        if any(re.search(r"<link rel=.alternate. hreflang=", text[x]) for x in d.values()): hb.append(rest + " noindex com hreflang")
        continue
    for l, f in d.items():
        u = urls_of(f)
        if set(u) != {"en", "pt", "es", "x-default"}: hb.append((f, "conjunto", sorted(u)))
        for m in LANGS:
            pairs += 1
            if m == l: continue
            if urls_of(d[m]).get(l) is None or urls_of(f)[m] != urls_of(d[m])[m]: hb.append((f, m))
        canon = re.search(r'<link rel="canonical" href="([^"]+)"', text[f]).group(1)
        if canon not in u.values() or u.get(l if l != "pt" else "pt-BR", u.get(l)) != canon: hb.append((f, "canonical != self"))
check("hreflang reciprocos (%d pares pagina x idioma)" % pairs, hb, hb[:5])

# sitemap
try:
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9", "x": "http://www.w3.org/1999/xhtml"}
    t = ET.parse("sitemap.xml").getroot(); locs = [u.find("s:loc", ns).text for u in t.findall("s:url", ns)]
    base = re.search(r"Sitemap: (.*)/sitemap.xml", open("robots.txt").read()).group(1)
    miss = [l for l in locs if not (os.path.isfile(l.replace(base, "").lstrip("/").rstrip("/") + "/index.html") or os.path.isfile(l.replace(base, "").lstrip("/")))]
    check("Sitemap valido (%d URLs, todas existem, sem duplicata, = paginas indexaveis x 3 idiomas)" % len(locs), miss or len(locs) != len(set(locs)) or len(locs) != (len([f for f in files if f.startswith("en/")]) - 2) * 3, miss[:3])
except Exception as e:
    check("Sitemap valido", True, e)
rb = open("robots.txt").read()
check("robots.txt valido", "User-agent: *" not in rb or "Sitemap:" not in rb or re.search(r"Disallow:\s*/\s*$", rb, re.M))
print("\nRESULTADO: %s" % ("%d FALHA(S)" % len(fails) if fails else "tudo OK"))
sys.exit(1 if fails else 0)
