class RuntimeErrorSL(Exception):
    pass

class Interpreter:
    def __init__(self, logger=None):
        self.env = {}      
        self.logger = logger

    def run(self, program):
        for stmt in program:
            self._exec_stmt(stmt)

    def _exec_stmt(self, stmt):
        op = stmt[0]

        if op == "SET":
            _, name, expr, line, col = stmt
            val = self.eval_expr(expr)
            self.env[name] = val
            self._log(f"[SET] {name} = {val!r}")

        elif op == "PRINT":
            _, expr, line, col = stmt
            val = self.eval_expr(expr)
            print(val)
            self._log(f"[PRINT] {val}")

        elif op == "LOG":
            _, expr, line, col = stmt
            val = self.eval_expr(expr)
            self._log(f"[LOG] {val}")

        elif op == "IF":
            _, cond_expr, then_block, else_block, line, col = stmt
            cond_val = self.eval_expr(cond_expr)
            if cond_val:
                for s in then_block:
                    self._exec_stmt(s)
            elif else_block is not None:
                for s in else_block:
                    self._exec_stmt(s)
        else:
            raise RuntimeErrorSL(f"Instrucción desconocida: {op}")

    def eval_expr(self, node):
        kind = node[0]

        if kind == "STRING":
            return node[1]

        if kind == "NUMBER":
            return node[1]

        if kind == "VAR":
            name = node[1]
            if name in self.env:
                return self.env[name]
            raise RuntimeErrorSL(f"Variable no definida: {name}")

        if kind == "BINOP":
            _, op, left, right = node
            a = self.eval_expr(left)
            b = self.eval_expr(right)

            # Suma / concatenación
            if op == "PLUS":
                if isinstance(a, str) or isinstance(b, str):
                    return str(a) + str(b)
                return a + b

            # Comparaciones
            if op == "GT":
                return a > b
            if op == "LT":
                return a < b
            if op == "GTE":
                return a >= b
            if op == "LTE":
                return a <= b
            if op == "EQEQ":
                return a == b
            if op == "NEQ":
                return a != b

        raise RuntimeErrorSL(f"Expresión no soportada: {node}")

    def _log(self, msg):
        if self.logger is not None:
            self.logger.write(msg)
