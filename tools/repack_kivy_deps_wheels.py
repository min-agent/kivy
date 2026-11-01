"""Create Python-version-independent Windows wheels from kivy_deps cp314 wheels.

The kivy_deps packages contain only DLLs, headers and import libraries, so the
CPython ABI tag is unnecessary. Retagging them as ``py3-none-win_amd64`` lets
the same wheels install on CPython 3.14, 3.15 and later.

Requires ``uvx`` (or the ``wheel`` package) and network access to PyPI.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

PACKAGES = (
    ("kivy-deps-sdl2", "0.8.1"),
    ("kivy-deps-sdl2-dev", "0.8.1"),
    ("kivy-deps-glew", "0.3.2"),
    ("kivy-deps-glew-dev", "0.3.2"),
    ("kivy-deps-angle", "0.5.0"),
    ("kivy-deps-gstreamer", "0.3.4"),
    ("kivy-deps-gstreamer-dev", "0.3.4"),
)


def find_wheel(url: str) -> tuple[str, str]:
    with urllib.request.urlopen(url, timeout=60) as response:
        metadata = json.load(response)
    for item in metadata["urls"]:
        filename = item["filename"]
        if "cp314" in filename and "win_amd64" in filename:
            return item["url"], filename
    raise RuntimeError(f"No cp314 win_amd64 wheel found for {url}")


def retag(wheels: list[Path]) -> None:
    command = [
        "uvx",
        "--from",
        "wheel",
        "wheel",
        "tags",
        "--python-tag",
        "py3",
        "--abi-tag",
        "none",
        "--platform-tag",
        "win_amd64",
        "--remove",
        *map(str, wheels),
    ]
    subprocess.run(command, check=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dest",
        type=Path,
        default=Path("wheelhouse"),
        help="destination directory (default: wheelhouse)",
    )
    args = parser.parse_args()
    dest: Path = args.dest
    dest.mkdir(parents=True, exist_ok=True)

    downloaded = []
    for name, version in PACKAGES:
        url, filename = find_wheel(f"https://pypi.org/pypi/{name}/{version}/json")
        py3_name = filename.replace("cp314-cp314", "py3-none")
        py3_target = dest / py3_name
        if py3_target.exists():
            print(f"have {py3_target}")
            continue
        target = dest / filename
        if target.exists():
            print(f"have {target}")
            downloaded.append(target)
            continue
        print(f"download {filename}")
        with urllib.request.urlopen(url, timeout=120) as response:
            target.write_bytes(response.read())
        downloaded.append(target)

    if shutil.which("uvx") is None:
        print("uvx not found; install wheel and retag manually", file=sys.stderr)
        return 1

    print("retagging as py3-none-win_amd64")
    retag(downloaded)
    for wheel in sorted(dest.glob("*-py3-none-win_amd64.whl")):
        print(wheel)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
