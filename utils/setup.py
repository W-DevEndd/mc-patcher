from pathlib import Path
import os, shutil, sys

files = Path("files")
config = Path(".config.py")
out = Path(".out")

def init():
    if config.exists(): return

    (files / "armebi-v7a").mkdir(parents=True, exist_ok=True)
    (files / "arm64-v8a").mkdir(parents=True, exist_ok=True)
    (out / "arm64-v8a").mkdir(parents=True, exist_ok=True)
    (out / "armebi-v7a").mkdir(parents=True, exist_ok=True)

    shutil.copyfile(Path("resources") / "config.py", config)

    print("\n".join([
        "Successfully setup mb-patcher.",
        "Open ``.config.py`` for configuration.",
    ]))
    sys.exit(0)

def clean():
    shutil.rmtree(files, ignore_errors=True)
    os.remove(config)
    shutil.rmtree(out, ignore_errors=True)

    print("cleaned the workspace, restart script to setup.")
    exit(0)
