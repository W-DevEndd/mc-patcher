# Import libs
from pathlib import Path
from utils import apk_tools, patchelf, setup
import sys

# Setup project
setup.init()
if (len(sys.argv) > 1):
    if (sys.argv[1] == "clean"): setup.clean()