from pathlib import Path

import toml

BASE_DIR = Path(__file__).resolve().parent.parent.parent

CONFIG_FILE = BASE_DIR / "config.toml"

if not CONFIG_FILE.exists():
    CONFIG_FILE = BASE_DIR / "default_config.toml"

with open(CONFIG_FILE, "r") as f:
    config = toml.load(f)
