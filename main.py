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

arm64 = "arm64-v8a"
arm32 = "armebi-v7a"

apk = setup.out / arm64 / Path(Config.minecraft_apk).name
apk_32 = setup.out / arm32 / Path(Config.minecraft_apk_32).name
mb_lib_so = setup.out / arm64 / Path(Config.mb_libso).name
mb_lib_so_32 = setup.out / arm32 / Path(Config.mb_libso_32).name
mc_lib_so = "libminecraftpe.so"
mc_lib_so_32 = "libminecraftpe.so"

shutil.copyfile(Path(Config.minecraft_apk), apk)
shutil.copyfile(Path(Config.mb_libso), mb_lib_so)
apk_tools.extract(apk, f"lib/{arm64}/{mc_lib_so}", setup.out / arm64)

patchelf.add_needed(mb_lib_so, setup.out / arm64 / mc_lib_so)
apk_tools.push(apk, setup.out / arm64 / mc_lib_so, f"lib/{arm64}/{mc_lib_so}")
apk_tools.push(apk, mb_lib_so, f"lib/{arm64}/{mb_lib_so.name}")

apk_tools.sign(apk)

if Config.make_32:
    shutil.copyfile(Path(Config.minecraft_apk_32), apk_32)
    shutil.copyfile(Path(Config.mb_libso_32), mb_lib_so_32)
    apk_tools.extract(apk, f"lib/{arm32}/{mc_lib_so}", setup.out / arm32)