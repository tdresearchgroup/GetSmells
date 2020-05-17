import platform
import sys
import os


IS_WINDOWS = platform.system() == "Windows"
UND_PATH = "und" if IS_WINDOWS else "/Applications/Understand.app/Contents/MacOS/und"
DEFAULT_OUTPUT = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "getsmells-output")

sys.path.append('C:/Program Files/SciTools/bin/pc-win64/Python' if IS_WINDOWS else '/Applications/Understand.app/Contents/MacOS/Python')
