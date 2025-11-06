from datetime import datetime
from pathlib import Path

class Logger:
    def __init__(self, path="scriptlang.log"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def write(self, msg):
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with self.path.open("a", encoding="utf-8") as f:
            f.write(f"{ts} {msg}\n")
