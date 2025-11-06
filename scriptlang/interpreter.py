# interpreter.py
from datetime import datetime

class RuntimeErrorSL(Exception):
    pass

class Interpreter:
    def __init__(self, logger=None):
        self.env = {}
        self.logger = logger

    def run(self, program):
        for stmt in program:
            op = stmt[0]
            if op == "SET":
                _, name, expr, line, col = stmt
                val = self.eval_expr(expr)
                self.env[name] = val
                if self.logger:
                    self.logger.write(f"[SET] {name} = {val!r}")
            elif op == "PRINT":
                _, expr, line, col = stmt
                val = self.eval_expr(expr)
                print(val)
                if self.logger:
                    self.logger.write(f"[PRINT] {val}")
            elif op == "LOG":
                _, expr, line, col = stmt
                val = self.eval_expr(expr)
                if self.logger:
                    self.logger.write(f"[LOG] {val}")
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
            if op == "+":
                
                if isinstance(a, str) or isinstance(b, str):
                    return str(a) + str(b)
                return a + b
        raise RuntimeErrorSL(f"Expresión no soportada: {node}")
