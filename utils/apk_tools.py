import zipfile, shutil, subprocess, random
from pathlib import Path

KEYSTORE_P = ".keystore.jks"
ALIAS = "mb-patcher"
PASS_P = ".passwd"

if not Path(PASS_P).exists():
    with open(Path(PASS_P), "w")as f:
        f.write("".join(map(str, [ random.randrange(0,9) for _ in range(8)])))
        f.close()

PASS = open(PASS_P, "r").read()


def check(apk_p: Path):
    if not zipfile.is_zipfile(apk_p): raise ValueError("The files is not zip.")

def extract(apk_p: Path, member: str, dest_dir: Path):
    check(apk_p)
    with zipfile.ZipFile(apk_p) as apk:
        with apk.open(member, "r") as src:
            dest_dir.mkdir(parents=True, exist_ok=True)
            with open(dest_dir / Path(member).name, "wb") as dst:
                shutil.copyfileobj(src, dst)

def add(apk_p: Path, file: Path, to_member: str):
    check(apk_p)
    with zipfile.ZipFile(apk_p, "a") as apk:
        apk.write(file, to_member)

def _align(apk_p: Path):
    check(apk_p)

    if not shutil.which("zipalign"):
        raise RuntimeError("\n".join([
            "zipalign is not installed in system or not executable.",
            "Open https://developer.android.com/studio or use package manager to innstall",
        ]))
    
    shutil.move(apk_p, apk_p.with_suffix(apk_p.suffix + ".bak"))
    cmd = ["zipalign", "-v", "-p", "4", str(apk_p.with_suffix(apk_p. suffix + ".bak")), str(apk_p)]
    print("$", " ".join(cmd))
    result = subprocess.run(cmd, check=True)
    return result

def _ensure_keystore():
    if Path(KEYSTORE_P).exists():
        return
    if not shutil.which("keytool"):
        raise RuntimeError("\n".join([
            "keytool is not installed in system or not executable.",
            "Open https://developer.android.com/studio or use package manager to install",
        ]))
    
    cmd = [
        "keytool", "-genkey", "-v",
        "-keystore", KEYSTORE_P,
        "-alias", ALIAS,
        "-keyalg", "RSA", "-keysize", "2048", "-validity", "10000",
        "-storepass", PASS, "-keypass", PASS,
        "-dname", "CN=MBB, OU=Patcher, O=Dev, L=VN, S=ST, C=VN"
    ]
    print("$", " ".join(cmd))
    return subprocess.run(cmd, check=True)

def sign(apk_p: Path):
    check(apk_p)
    _ensure_keystore()
    _align(apk_p)

    if not shutil.which("apksigner"):
        raise RuntimeError("\n".join([
            "apksigner is not installed in system or not executable.",
            "Open https://developer.android.com/studio or use package manager to install",
        ]))
    
    shutil.move(apk_p, apk_p.with_suffix(apk_p.suffix + ".bak"))

    cmd = ["apksigner", "sign", "--ks", KEYSTORE_P, "--ks-pass", f"pass:{PASS}", "--out", str(apk_p) , str(apk_p.with_suffix(apk_p.suffix + ".bak"))]
    print("$", " ".join(cmd))
    result = subprocess.run(cmd, check=True)

    verify(apk_p)
    return result

def verify(apk_p: Path):
    check(apk_p)

    if not shutil.which("apksigner"):
        raise RuntimeError("\n".join([
            "apksigner is not installed in system or not executable.",
            "Open https://developer.android.com/studio or use package manager to install",
        ]))
    
    cmd = ["apksigner", "verify", "-v", str(apk_p)]
    print("$", " ".join(cmd))
    return subprocess.run(cmd, check=True)