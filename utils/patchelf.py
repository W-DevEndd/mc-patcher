from pathlib import Path
import subprocess, shutil

def check_executable():
    if shutil.which("patchelf"):
        return 0
    else:
        raise RuntimeError("\n".join([
            "patchelf is not installed or not executable.",
            "Open https://github.com/NixOS/patchelf to read more infomation",
        ]))

def add_needed(dependacy: Path, target: Path):
    cmd = ["patchelf", "--add-needed", str(dependacy), str((target))]
    print("$", " ".join(cmd))
    return subprocess.run(cmd, check=True)
