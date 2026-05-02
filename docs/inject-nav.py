#!/usr/bin/env python3
"""Strip Jekyll front matter from synced docs files before MkDocs build.

Nav order and titles are managed in mkdocs.yml, not in file front matter.
This script ensures synced files (which may have been processed before)
don't contain stale front matter that would render as page content.
"""

import re
import yaml
from pathlib import Path

FRONT_MATTER_RE = re.compile(r"^---\n.*?\n---\n\n?", re.DOTALL)

docs_dir = Path(__file__).parent
config_path = docs_dir / "nav-config.yml"

with open(config_path) as f:
    config = yaml.safe_load(f)

for filename in config.get("files", {}):
    path = docs_dir / filename
    if not path.exists():
        print(f"WARNING: {filename} listed in nav-config.yml but not found, skipping")
        continue

    content = path.read_text()
    cleaned = FRONT_MATTER_RE.sub("", content)
    if cleaned != content:
        path.write_text(cleaned)
        print(f"OK: stripped front matter from {filename}")
    else:
        print(f"SKIP: {filename} has no front matter")
