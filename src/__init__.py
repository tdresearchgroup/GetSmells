import platform
import sys
from os import path

IS_WINDOWS = platform.system() == "Windows"
UND_PATH = "und" if IS_WINDOWS else "/Applications/Understand.app/Contents/MacOS/und"
PROJECT_PATH = path.dirname(path.dirname(path.realpath(__file__)))
DEFAULT_OUTPUT = path.join(PROJECT_PATH, "getsmells-output")

sys.path.append('C:/Program Files/SciTools/bin/pc-win64/Python' if IS_WINDOWS else '/Applications/Understand.app/Contents/MacOS/Python')
