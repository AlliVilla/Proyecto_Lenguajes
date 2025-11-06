# parser.py
from lexer import tokenize

KEYWORDS = {"set", "print", "log"}

class ParseError(Exception):
    pass

class Parser:
    def __init__(self, tokens):
        self.tokens = list(tokens)
        self.i = 0

    def peek(self):
        return self.tokens[self.i]

    def take(self, kind=None):
        t = self.peek()
        if kind and t.kind != kind:
            raise ParseError(f"Se esperaba {kind} y llegó {t.kind} en línea {t.line}, col {t.col}")
        self.i += 1
        return t

    def at_eof(self):
        return self.peek().kind == "EOF"
    def parse_program(self):
        stmts = []
        while not self.at_eof():
            while self.peek().kind in ("SEMICOL", "NEWLINE"):
                self.take()
                if self.at_eof():
                    return stmts
            if self.at_eof():
                break
            stmts.append(self.parse_stmt())
        return stmts

    def parse_stmt(self):
        t = self.peek()
        if t.kind == "IDENT" and t.value.lower() in KEYWORDS:
            kw = self.take("IDENT").value.lower()
            if kw == "set":
                name = self.take("IDENT")
                self.take("EQUAL")
                expr = self.parse_expr()
                return ("SET", name.value, expr, t.line, t.col)
            elif kw == "print":
                expr = self.parse_expr()
                return ("PRINT", expr, t.line, t.col)
            elif kw == "log":
                expr = self.parse_expr()
                return ("LOG", expr, t.line, t.col)
        raise ParseError(f"Instrucción no válida en línea {t.line}, col {t.col}. "
                         f"Usa: set, print o log.")

    def parse_expr(self):
        left = self.parse_term()
        while self.peek().kind == "PLUS":
            self.take("PLUS")
            right = self.parse_term()
            left = ("BINOP", "+", left, right)
        return left


    def parse_term(self):
        t = self.peek()
        if t.kind == "STRING":
            self.take("STRING")
            return ("STRING", self._unquote(t.value))
        if t.kind == "NUMBER":
            self.take("NUMBER")
            return ("NUMBER", int(t.value))
        if t.kind == "IDENT":
    
            name = self.take("IDENT").value
            return ("VAR", name)
        raise ParseError(f"Token inesperado {t.kind} en línea {t.line}, col {t.col}")

    def _unquote(self, s):

        if len(s) >= 2 and s[0] == '"' and s[-1] == '"':
            return bytes(s[1:-1], "utf-8").decode("unicode_escape")
        return s

def parse_text(text):
    p = Parser(tokenize(text))
    return p.parse_program()
