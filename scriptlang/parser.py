from lexer import tokenize

KEYWORDS = {"set", "print", "log", "if", "else", "end"}

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
            raise ParseError(
                f"Se esperaba {kind} y llegó {t.kind} en línea {t.line}, col {t.col}"
            )
        self.i += 1
        return t

    def at_eof(self):
        return self.peek().kind == "EOF"

    def _skip_separadores(self):
        while self.peek().kind in ("SEMICOL", "NEWLINE"):
            self.take()

    def parse_program(self):
        stmts = []
        self._skip_separadores()
        while not self.at_eof():
            stmts.append(self.parse_stmt())
            self._skip_separadores()
        return stmts

    def parse_stmt(self):
        t = self.peek()

        if t.kind == "IDENT":
            kw = t.value.lower()
            if kw in KEYWORDS:
                if kw == "set":
                    return self._parse_set()
                elif kw == "print":
                    return self._parse_print()
                elif kw == "log":
                    return self._parse_log()
                elif kw == "if":
                    return self._parse_if()
                elif kw in ("else", "end"):
                    raise ParseError(
                        f"'{kw}' está fuera de un bloque if en línea {t.line}, col {t.col}"
                    )
        raise ParseError(
            f"Instrucción no válida en línea {t.line}, col {t.col}. "
            f"Se esperaba set, print, log o if."
        )

    def _parse_set(self):
        kw = self.take("IDENT")  
        name_tok = self.take("IDENT")
        self.take("EQUAL")
        expr = self.parse_expr()
        return ("SET", name_tok.value, expr, kw.line, kw.col)

    def _parse_print(self):
        kw = self.take("IDENT")  
        expr = self.parse_expr()
        return ("PRINT", expr, kw.line, kw.col)

    def _parse_log(self):
        kw = self.take("IDENT")  
        expr = self.parse_expr()
        return ("LOG", expr, kw.line, kw.col)

    def _parse_if(self):
        kw_if = self.take("IDENT")  
        cond_expr = self.parse_expr()
  
        self._skip_separadores()

        then_block = []
        else_block = None

        while not self.at_eof():
            t = self.peek()
            if t.kind == "IDENT":
                v = t.value.lower()
                if v == "else":
                    self.take("IDENT")
                    self._skip_separadores()
                    else_block = []
                    while not self.at_eof():
                        t2 = self.peek()
                        if t2.kind == "IDENT" and t2.value.lower() == "end":
                            break
                        else_block.append(self.parse_stmt())
                        self._skip_separadores()
                elif v == "end":
                    
                    self.take("IDENT")
                    return ("IF", cond_expr, then_block, else_block, kw_if.line, kw_if.col)

        
            then_block.append(self.parse_stmt())
            self._skip_separadores()

        raise ParseError(
            f"Falta 'end' para cerrar el bloque if iniciado en línea {kw_if.line}, col {kw_if.col}"
        )

    def parse_expr(self):
        return self._parse_comp()

    def _parse_comp(self):
        left = self._parse_sum()
        t = self.peek()
        if t.kind in ("GT", "LT", "GTE", "LTE", "EQEQ", "NEQ"):
            op = self.take().kind
            right = self._parse_sum()
            return ("BINOP", op, left, right)
        return left

    def _parse_sum(self):
        left = self._parse_term()
        while self.peek().kind == "PLUS":
            self.take("PLUS")
            right = self._parse_term()
            left = ("BINOP", "PLUS", left, right)
        return left

    # term := STRING | NUMBER | IDENT
    def _parse_term(self):
        t = self.peek()
        if t.kind == "STRING":
            tok = self.take("STRING")
            return ("STRING", self._unquote(tok.value))
        if t.kind == "NUMBER":
            tok = self.take("NUMBER")
            return ("NUMBER", int(tok.value))
        if t.kind == "IDENT":
            name = self.take("IDENT").value
            return ("VAR", name)
        raise ParseError(
            f"Token inesperado {t.kind} en línea {t.line}, col {t.col}"
        )

    def _unquote(self, s):
        if len(s) >= 2 and s[0] == '"' and s[-1] == '"':
            return bytes(s[1:-1], "utf-8").decode("unicode_escape")
        return s

def parse_text(text):
    p = Parser(tokenize(text))
    return p.parse_program()
