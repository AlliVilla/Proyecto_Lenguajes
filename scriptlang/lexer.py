import re

TOKEN_SPEC = [
    ("SKIP",      r"[ \t]+"),
    ("NEWLINE",   r"\n"),
    ("COMMENT",   r"#.*"),

    ("EQEQ",      r"=="),
    ("GTE",       r">="),
    ("LTE",       r"<="),
    ("NEQ",       r"!="),
    ("GT",        r">"),
    ("LT",        r"<"),

    ("STRING",    r"\"([^\"\\]|\\.)*\""),
    ("NUMBER",    r"\d+"),
    ("IDENT",     r"[A-Za-z_][A-Za-z0-9_]*"),
    ("PLUS",      r"\+"),
    ("EQUAL",     r"="),
    ("SEMICOL",   r";"),
]

MASTER_RE = re.compile("|".join(f"(?P<{name}>{pat})" for name, pat in TOKEN_SPEC))

class Token:
    def __init__(self, kind, value, line, col):
        self.kind = kind
        self.value = value
        self.line = line
        self.col = col

    def __repr__(self):
        return f"Token({self.kind},{self.value!r},{self.line},{self.col})"

def tokenize(text):
    line = 1
    col = 1
    pos = 0
    n = len(text)
    while pos < n:
        m = MASTER_RE.match(text, pos)
        if not m:
            ch = text[pos]
            raise SyntaxError(f"Caracter inesperado '{ch}' en línea {line}, col {col}")
        kind = m.lastgroup
        val = m.group()

        if kind == "NEWLINE":
            line += 1
            col = 1
        elif kind in ("SKIP", "COMMENT"):
    
            pass
        else:
            yield Token(kind, val, line, col)

        pos = m.end()
        if kind != "NEWLINE":
            col += len(val)


    yield Token("EOF", "", line, col)
