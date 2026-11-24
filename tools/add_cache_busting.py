"""Update the cache-busting query string (?v=...) in index.html."""

import datetime
import re
from pathlib import Path

INDEX_FILE = Path(__file__).resolve().parent.parent / "index.html"


def bump_cache_buster(version: str | None = None) -> str:
    if not version:
        version = datetime.datetime.now().strftime("%Y%m%d%H%M")
    content = INDEX_FILE.read_text(encoding="utf-8")
    updated, count = re.subn(r"\+ 'v=[^']+'", f"+ 'v={version}'", content)
    if count == 0:
        raise RuntimeError("Could not find imgSrc cache-busting token in index.html")
    INDEX_FILE.write_text(updated, encoding="utf-8")
    print(f"Updated cache-busting version to v={version} ({count} occurrence)")
    return version


if __name__ == "__main__":
    bump_cache_buster()
