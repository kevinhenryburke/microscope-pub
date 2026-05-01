#!/usr/bin/env python3
"""Inject Jekyll front matter into synced docs files based on nav-config.yml."""

import sys
import yaml
from pathlib import Path

docs_dir = Path(__file__).parent
config_path = docs_dir / "nav-config.yml"

with open(config_path) as f:
    config = yaml.safe_load(f)

for filename, meta in config.get("files", {}).items():
    path = docs_dir / filename
    if not path.exists():
        print(f"WARNING: {filename} listed in nav-config.yml but not found, skipping")
        continue

    content = path.read_text()
    if content.startswith("---"):
        print(f"SKIP: {filename} already has front matter")
        continue

    front_matter = "---\n"
    for key, value in meta.items():
        front_matter += f"{key}: {value}\n"
    front_matter += "---\n\n"

    path.write_text(front_matter + content)
    print(f"OK: injected front matter into {filename}")
