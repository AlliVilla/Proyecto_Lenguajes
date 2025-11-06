import sys
from pathlib import Path
from parser import parse_text
from interpreter import Interpreter
from log_module import Logger

def main():
    if len(sys.argv) != 2:
        print("Uso: python scriptlang.py <archivo.sl>")
        sys.exit(1)

    script_path = Path(sys.argv[1])
    if not script_path.exists():
        print(f"No se encuentra el archivo: {script_path}")
        sys.exit(1)

    text = script_path.read_text(encoding="utf-8")

    log_dir = script_path.parent / "logs"
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / (script_path.stem + ".log")

    try:
        program = parse_text(text)
    except Exception as e:
        print(f"[Error de sintaxis] {e}")
        sys.exit(2)

    try:
        interp = Interpreter(logger=Logger(log_file))
        interp.run(program)
    except Exception as e:
        print(f"[Error en ejecución] {e}")
        sys.exit(3)

if __name__ == "__main__":
    main()
