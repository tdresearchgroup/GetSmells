import argparse
import os.path

from app import App


def main(sourcePath, outputPath, includeMetricsInCsv):
    projectName = os.path.split(sourcePath)[-1]
    sourcePath = os.path.normcase(sourcePath)
    outputPath = os.path.normcase(outputPath or
                                  os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "getsmells-output"))

    if not os.path.isdir(sourcePath):
        print("Error: The specified source path either does not exist or is not a directory")
        return

    app = App(sourcePath, outputPath)

    print(f"Starting GetSmells on '{sourcePath}' (output at '{outputPath})\n")
    print(f"Step 1/2: Creating an Understand Project for '{projectName}'")
    app.analyzeCode()

    print(f"Step 2/2: Extracting code smells from metrics on '{projectName}'")
    app.extractSmells(includeMetricsInCsv)

    print("GetSmells complete!")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("sourcePath", help="The path to the directory with a single project's code")
    parser.add_argument("-o", "--outputPath", help="The directory to output the CSVs with code smells")
    parser.add_argument("-m", "--metricsInclude", action="store_true", help="Include metrics in CSV file")
    args = parser.parse_args()

    main(args.sourcePath, args.outputPath, args.metricsInclude)

