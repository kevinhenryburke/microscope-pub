#!/usr/bin/env python3
"""Inject Jekyll front matter and optional TOC into synced docs files based on nav-config.yml."""

import yaml
from pathlib import Path

TOC_BLOCK = (
    "<details markdown=\"block\">\n"
    "  <summary>Contents</summary>\n"
    "- TOC\n"
    "{:toc}\n"
    "</details>\n"
)

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

    inject_toc = meta.pop("toc", False)

    front_matter = "---\n"
    for key, value in meta.items():
        front_matter += f"{key}: {value}\n"
    front_matter += "---\n\n"

    if inject_toc:
        # Insert TOC block after the first h1 heading line
        lines = content.splitlines(keepends=True)
        insert_at = None
        for i, line in enumerate(lines):
            if line.startswith("# "):
                insert_at = i + 1
                break
        if insert_at is not None:
            lines.insert(insert_at, "\n" + TOC_BLOCK + "\n")
            content = "".join(lines)

    path.write_text(front_matter + content)
    print(f"OK: injected front matter into {filename}" + (" with TOC" if inject_toc else ""))
