# Import libs
from pathlib import Path
from utils import apk_tools, patchelf, setup
import sys, shutil
try:
    from mc_patcher_config import Config
except:
    from resources.config import Config

# Setup project
setup.init()
if (len(sys.argv) > 1):
    if (sys.argv[1] == "clean"): setup.clean()

apk = setup.out / "arm64-v8a" / Path(Config.minecraft_apk).name
apk_32 = setup.out / "arm64-v8a" / Path(Config.minecraft_apk_32).name
mb_lib_so = setup.out / "armebi-v7a" / Path(Config.mb_libso).name
mb_lib_so_32 = setup.out / "armebi-v7a" / Path(Config.mb_libso_32).name

if Path(Config.minecraft_apk).exists():
    shutil.copyfile(Path(Config.minecraft_apk), apk)
if Path(Config.minecraft_apk_32).exists():
    shutil.copyfile(Path(Config.minecraft_apk_32), apk_32)
if Path(Config.mb_libso).exists():
    shutil.copyfile(Path(Config.mb_libso), mb_lib_so)
if Path(Config.mb_libso_32).exists():
    shutil.copyfile(Path(Config.mb_libso_32), mb_lib_so_32)