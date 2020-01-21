import subprocess
import platform

# Relevant Understand CLI Documentation:
# https://scitools.com/support/commandline/


UND_PATH = "und" if IS_WINDOWS else "/Applications/Understand.app/Contents/MacOS/und"


def makecmd(args):
    return args if IS_WINDOWS else " ".join(args)

def analyzeCode(sourcePath, projectPath):
    try:
        subprocess.check_output(makecmd([UND_PATH, 'version']))
        subprocess.check_output(makecmd([UND_PATH, 'create', '-languages', 'Java', projectPath]))
        subprocess.check_output(makecmd([UND_PATH, 'add', sourcePath, projectPath]))
        subprocess.check_output(makecmd([UND_PATH, 'settings', '-metrics', 'all', projectPath]))
        subprocess.check_output(makecmd([UND_PATH, 'analyze', projectPath]))
    except subprocess.CalledProcessError as e:
        print(e.output)
        return 1

    print("\tMetric analysis complete")

    return 0


if __name__ == '__main__':
    print("Running code analysis and project output on a directory standalone using defaults")

    # Default project and output path
    if platform.system() == "Windows":
        logFile = open("C:/Users/cb1782/understandcli-log.txt", "w+")
        analyzeCode("C:/Users/cb1782/Downloads/apache-tomcat-7.0.82-src/apache-tomcat-7.0.82-src",
                    "C:/Users/cb1782/understandcli-project.udb",
                    logFile)
        logFile.close()
    else:
        logFile = open("/Users/charles/Documents/DIS/understandcli-log.txt", "w+")
        analyzeCode("/Users/charles/Documents/DIS/code/apache-tomcat-8.0.49-src",
                    "/Users/charles/Documents/DIS/understandproject.udb",
                    logFile)
        logFile.close()
