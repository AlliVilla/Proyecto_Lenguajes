import sys
from pathlib import Path
from parser import parse_text, ParseError
from interpreter import Interpreter, RuntimeErrorSL
from log_module import Logger

def main():
    if len(sys.argv) != 2:
        print("Uso: python scriptlang.py <archivo.sl>")
        sys.exit(1)

    script_path = Path(sys.argv[1])
    if not script_path.exists():
        print(f"No se encuentra el archivo: {script_path}")
        sys.exit(1)

    try:
        text = script_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"No se pudo leer el archivo: {e}")
        sys.exit(1)

    # Log al lado del script, en carpeta logs
    log_dir = script_path.parent / "logs"
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / (script_path.stem + ".log")

    try:
        program = parse_text(text)
    except ParseError as e:
        print(f"[Error de sintaxis] {e}")
        sys.exit(2)
    except SyntaxError as e:
        print(f"[Error de análisis léxico] {e}")
        sys.exit(2)

    try:
        interp = Interpreter(logger=Logger(log_file))
        interp.run(program)
    except RuntimeErrorSL as e:
        print(f"[Error en ejecución] {e}")
        sys.exit(3)
    except Exception as e:
        print(f"[Error inesperado] {e}")
        sys.exit(3)

if __name__ == "__main__":
    main()
