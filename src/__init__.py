import platform
import sys


IS_WINDOWS = platform.system() == "Windows"
UND_PATH = "und" if IS_WINDOWS else "/Applications/Understand.app/Contents/MacOS/und"

sys.path.append('C:/Program Files/SciTools/bin/pc-win64/Python' if IS_WINDOWS else '/Applications/Understand.app/Contents/MacOS/Python')
