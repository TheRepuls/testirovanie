import os
from datetime import datetime

def setup_logger():
    logs_dir = "logs"
    os.makedirs(logs_dir, exist_ok=True)
    filename = datetime.now().strftime("parser_%Y-%m-%d_%H-%M.txt")
    path = os.path.join(logs_dir, filename)
    return path

LOG_PATH = setup_logger()

def log(message, level="INFO"):
    timestamp = datetime.now().strftime("[%H:%M:%S]")
    prefix = {
        "INFO": "ℹ️ ",
        "SUCCESS": "✅ ",
        "WARNING": "⚠️ ",
        "ERROR": "❌ ",
        "ACTION": "➡️ ",
    }.get(level, "")
    
    text = f"{timestamp} {prefix}{message}"
    with open(LOG_PATH, "a", encoding="utf-8") as file:
        file.write(text + "\n")
