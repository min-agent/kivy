import os
from pathlib import Path

from setuptools import setup

ROOT = Path(__file__).resolve().parents[2]
DATA_FILE_PREFIX = "share/kivy-"
ALLOWED_EXT = {
    "readme",
    "py",
    "wav",
    "png",
    "jpg",
    "svg",
    "json",
    "avi",
    "gif",
    "txt",
    "ttf",
    "obj",
    "mtl",
    "kv",
    "mpg",
    "glsl",
    "zip",
}

version = {}
exec((ROOT / "kivy" / "_version.py").read_text(encoding="utf-8"), version)

examples = {}
for dirpath, _dirnames, filenames in os.walk(ROOT / "examples"):
    for filename in filenames:
        if filename.rsplit(".", 1)[-1].lower() not in ALLOWED_EXT:
            continue
        path = Path(dirpath) / filename
        directory = DATA_FILE_PREFIX + path.parent.relative_to(ROOT).as_posix()
        examples.setdefault(directory, []).append(str(path))

setup(
    version=version["__version__"],
    data_files=list(examples.items()),
)
