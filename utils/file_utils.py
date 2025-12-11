import json
import threading
from pathlib import Path
from datetime import datetime
from typing import Any

_file_lock = threading.Lock()

def read_json(path: str) -> Any:
    p = Path(path)
    if not p.exists():
        return None
    with _file_lock:
        with p.open("r", encoding="utf-8") as f:
            return json.load(f)

def write_json(path: str, data: Any) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with _file_lock:
        tmp = p.with_suffix(".tmp")
        with tmp.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        tmp.replace(p)

def timestamp() -> str:
    return datetime.utcnow().isoformat() + "Z"
