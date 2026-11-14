"""Parser HTML com offsets exatos (sem reserializar), para o gerador i18n.

Nao usa BeautifulSoup de proposito: reserializar muda bytes. Aqui a arvore guarda
posicoes no texto-fonte, e toda edicao e feita por substituicao de trechos.
"""
import re
from html.parser import HTMLParser

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link",
        "meta", "param", "source", "track", "wbr"}
RAW = {"script", "style"}


class Node:
    __slots__ = ("tag", "attrs", "s0", "s1", "e0", "e1", "parent", "children",
                 "texts", "raw_start")

    def __init__(self, tag, attrs, s0, s1, parent):
        self.tag, self.attrs = tag, attrs
        self.s0, self.s1 = s0, s1          # start tag [s0, s1)
        self.e0 = self.e1 = None           # end tag [e0, e1)  (None p/ void)
        self.parent = parent
        self.children = []
        self.texts = []                    # (a, b) trechos de texto direto

    def inner(self, src):
        return src[self.s1:self.e0] if self.e0 is not None else ""

    def get(self, name, default=None):
        for k, v in self.attrs:
            if k == name:
                return v
        return default

    def walk(self):
        yield self
        for c in self.children:
            yield from c.walk()


class Tree(HTMLParser):
    def __init__(self, src):
        super().__init__(convert_charrefs=False)
        self.src = src
        self.root = Node("#root", [], 0, 0, None)
        self.root.e0 = self.root.e1 = len(src)
        self.stack = [self.root]
        self.line_off = [0]
        for m in re.finditer("\n", src):
            self.line_off.append(m.end())
        self.doctype = None
        self.implicit = []
        self.feed(src)
        self.close()
        if len(self.stack) != 1:
            raise ValueError("tags nao fechadas: " + ",".join(n.tag for n in self.stack[1:]))

    def _pos(self):
        l, c = self.getpos()
        return self.line_off[l - 1] + c

    def handle_starttag(self, tag, attrs):
        s0 = self._pos()
        raw = self.get_starttag_text()
        s1 = s0 + len(raw)
        n = Node(tag, attrs, s0, s1, self.stack[-1])
        self.stack[-1].children.append(n)
        if tag in VOID or raw.rstrip().endswith("/>"):
            n.e0 = n.e1 = s1
            return
        self.stack.append(n)
        if tag in RAW:
            self.set_cdata_mode(tag)

    def handle_startendtag(self, tag, attrs):
        s0 = self._pos()
        raw = self.get_starttag_text()
        n = Node(tag, attrs, s0, s0 + len(raw), self.stack[-1])
        n.e0 = n.e1 = n.s1
        self.stack[-1].children.append(n)

    def handle_endtag(self, tag):
        e0 = self._pos()
        m = re.compile(r"</\s*" + re.escape(tag) + r"\s*>", re.I).match(self.src, e0)
        if not m:
            raise ValueError("end tag ilegivel em %d: %s" % (e0, tag))
        if tag not in [n.tag for n in self.stack[1:]]:
            raise ValueError("end tag sem abertura em %d: </%s>" % (e0, tag))
        # Fechamento implicito (como o navegador): o que estiver aberto por cima
        # fecha com largura zero na posicao deste end tag. Registrado em .implicit.
        while self.stack[-1].tag != tag:
            n = self.stack.pop()
            n.e0 = n.e1 = e0
            self.implicit.append((n.tag, e0))
        top = self.stack.pop()
        top.e0, top.e1 = e0, m.end()

    def _text(self, data):
        if not data:
            return
        a = self._pos()
        self.stack[-1].texts.append((a, a + len(data)))

    def handle_data(self, data):
        self._text(data)

    def handle_entityref(self, name):
        self._text("&%s;" % name)

    def handle_charref(self, name):
        self._text("&#%s;" % name)

    def handle_comment(self, data):
        pass

    def handle_decl(self, decl):
        pass

    def unknown_decl(self, data):
        pass


def parse(src):
    return Tree(src)
