from lexer import tokenize

KEYWORDS = {
    "set", "print", "log",
    "if", "else", "end",
    "while",
    "function",
    "return",
    "writefile", "appendfile", "readfile", "deletefile"
}

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

    # Program and statements
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
                # dispatch  of keyword
                if kw == "set":
                    return self._parse_set()
                if kw == "print":
                    return self._parse_print()
                if kw == "log":
                    return self._parse_log()
                if kw == "if":
                    return self._parse_if()
                if kw == "while":
                    return self._parse_while()
                if kw == "writefile":
                    return self._parse_writefile()
                if kw == "appendfile":
                    return self._parse_appendfile()
                if kw == "readfile":
                    return self._parse_readfile()
                if kw == "deletefile":
                    return self._parse_deletefile()
                if kw == "function":
                    return self._parse_function()
                if kw == "return":
                    return self._parse_return()
                if kw in ("else", "end"):
                    raise ParseError(
                        f"'{kw}' está fuera de un bloque if/while en línea {t.line}, col {t.col}"
                    )
            else:
                if self.tokens[self.i + 1].kind == "LPAREN":
                    return self._parse_call()
                else:
                    raise ParseError(
                        f"Instrucción no válida en línea {t.line}, col {t.col} (palabra '{t.value}')."
                    )
        raise ParseError(
            f"Instrucción no válida en línea {t.line}, col {t.col}. "
            f"Se esperaba set, print, log, if, while, return o instrucción de archivo."
        )

    # Individual statement parsers
    
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
                    continue
                elif v == "end":
                    self.take("IDENT")
                    return ("IF", cond_expr, then_block, else_block, kw_if.line, kw_if.col)
            then_block.append(self.parse_stmt())
            self._skip_separadores()
        raise ParseError(
            f"Falta 'end' para cerrar el if iniciado en línea {kw_if.line}, col {kw_if.col}"
        )

    def _parse_while(self):
        kw_while = self.take("IDENT")
        cond_expr = self.parse_expr()
        self._skip_separadores()
        body = []
        while not self.at_eof():
            t = self.peek()
            if t.kind == "IDENT" and t.value.lower() == "end":
                self.take("IDENT")
                return ("WHILE", cond_expr, body, kw_while.line, kw_while.col)
            body.append(self.parse_stmt())
            self._skip_separadores()
        raise ParseError(
            f"Falta 'end' para cerrar el while iniciado en línea {kw_while.line}, col {kw_while.col}"
        )

    def _parse_writefile(self):
        kw = self.take("IDENT")
        path_expr = self.parse_expr()
        self._skip_separadores()
        content_expr = self.parse_expr()
        return ("WRITEFILE", path_expr, content_expr, kw.line, kw.col)

    def _parse_appendfile(self):
        kw = self.take("IDENT")
        path_expr = self.parse_expr()
        self._skip_separadores()
        content_expr = self.parse_expr()
        return ("APPENDFILE", path_expr, content_expr, kw.line, kw.col)

    def _parse_readfile(self):
        kw = self.take("IDENT")
        path_expr = self.parse_expr()
        self._skip_separadores()
        name_tok = self.take("IDENT")
        return ("READFILE", path_expr, name_tok.value, kw.line, kw.col)

    def _parse_deletefile(self):
        kw = self.take("IDENT")
        path_expr = self.parse_expr()
        return ("DELETEFILE", path_expr, kw.line, kw.col)

    def _parse_function(self):
        kw = self.take("IDENT")
        name_tok = self.take("IDENT")
        self.take("LPAREN")
        params = []
        if self.peek().kind != "RPAREN":
            while True:
                param_tok = self.take("IDENT")
                params.append(param_tok.value)
                if self.peek().kind == "COMMA":
                    self.take("COMMA")
                else:
                    break
        self.take("RPAREN")
        self._skip_separadores()
        body = []
        while not self.at_eof():
            t = self.peek()
            if t.kind == "IDENT" and t.value.lower() == "end":
                self.take("IDENT")
                return ("FUNCTION", name_tok.value, params, body, kw.line, kw.col)
            body.append(self.parse_stmt())
            self._skip_separadores()
        raise ParseError(
            f"Falta 'end' para cerrar la función '{name_tok.value}' iniciada en línea {kw.line}, col {kw.col}"
        )

    def _parse_call(self):
        name_tok = self.take("IDENT")
        self.take("LPAREN")
        args = []
        if self.peek().kind != "RPAREN":
            while True:
                args.append(self.parse_expr())
                if self.peek().kind == "COMMA":
                    self.take("COMMA")
                else:
                    break
        self.take("RPAREN")
        return ("CALL", name_tok.value, args, name_tok.line, name_tok.col)

    def _parse_return(self):
        kw = self.take("IDENT")
        expr = self.parse_expr()
        return ("RETURN", expr, kw.line, kw.col)

    # Expressions
    def parse_expr(self):
        """Parse expression with lowest precedence (logical and/or)."""
        return self._parse_logic()

    def _parse_logic(self):
        left = self._parse_comp()
        while True:
            t = self.peek()
            if t.kind == "IDENT" and t.value.lower() in ("and", "or"):
                op = t.value.lower()
                self.take("IDENT")
                right = self._parse_comp()
                left = ("LOGIC", op.upper(), left, right)
            else:
                break
        return left

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
        while self.peek().kind in ("PLUS", "MINUS"):
            op = self.take().kind
            right = self._parse_term()
            left = ("BINOP", op, left, right)
        return left

    def _parse_term(self):
        left = self._parse_factor()
        while self.peek().kind in ("STAR", "SLASH"):
            op = self.take().kind
            right = self._parse_factor()
            left = ("BINOP", op, left, right)
        return left

    def _parse_factor(self):
        t = self.peek()
        if t.kind == "LPAREN":
            self.take("LPAREN")
            expr = self.parse_expr()
            self.take("RPAREN")
            return expr
        if t.kind == "STRING":
            tok = self.take("STRING")
            return ("STRING", self._unquote(tok.value))
        if t.kind == "NUMBER":
            tok = self.take("NUMBER")
            return ("NUMBER", int(tok.value))
        if t.kind == "IDENT":
            name = self.take("IDENT").value
            if self.peek().kind == "LPAREN":
                self.take("LPAREN")
                args = []
                if self.peek().kind != "RPAREN":
                    while True:
                        args.append(self.parse_expr())
                        if self.peek().kind == "COMMA":
                            self.take("COMMA")
                        else:
                            break
                self.take("RPAREN")
                return ("CALL_EXPR", name, args)
            else:
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
