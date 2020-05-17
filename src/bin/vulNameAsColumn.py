import argparse
import csv
from copy import deepcopy

DEFAULT_HEADER = ['Name', 'Version'] + \
                 ['CVE_ID', 'Last_Affected_Version', 'Revision_No', 'File']


def main(defectListPath):
    """
    The motivation of this tool is making unique vulnerability names as columns.
    And each row(class) has different count in these columns.

    :param defectListPath: the path of vulnerability data
    :return: None
    """

    print("Start combining vulnerability data")
    outPath = defectListPath.replace('.csv', '-processed.csv')

    with open(defectListPath, 'r') as vulIn, open(outPath, 'w') as vulOut:
        defectRows = list(csv.DictReader(vulIn))
        defectNames = _getDefectNames(defectRows)
        outputRow = _getOutputRow(defectNames)

        rd = {}

        # initialize empty table
        for row in defectRows:
            rd[(row['Name'], row['Version'])] = deepcopy(outputRow)
        vulIn.seek(0)

        # update empty table
        for row in defectRows:
            rd[(row['Name'], row['Version'])]['Name'] = row['Name']
            rd[(row['Name'], row['Version'])]['Version'] = row['Version']

            rd[(row['Name'], row['Version'])]['CVE_ID'].append(row['CVE_ID'])
            rd[(row['Name'], row['Version'])]['Last_Affected_Version'].append(row['Last_Affected_Version'])
            rd[(row['Name'], row['Version'])]['Revision_No'].append(row['Revision_No'])
            rd[(row['Name'], row['Version'])]['File'].append(row['File'])

            rd[(row['Name'], row['Version'])][row['Vul_Name']] += 1
            rd[(row['Name'], row['Version'])]['Vul_Count'] += 1

        writer = csv.DictWriter(vulOut, fieldnames=outputRow.keys(), delimiter=",")
        writer.writeheader()
        writer.writerows(rd.values())

    print("Combining vulnerability data done")


def _getDefectNames(defectLists):
    return list({x['Vul_Name'] for x in defectLists})


def _getOutputRow(defectNames):
    outputRow = {x: [] for x in DEFAULT_HEADER}
    outputRow.update({x: 0 for x in defectNames})
    outputRow['Vul_Count'] = 0
    return outputRow


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="python3 vulNameAsColumn xx/xxx.csv")
    parser.add_argument("vulData", help="The path to the data file containing these columns: "
                                        "\n[CVE_ID, Vul_Name, Version, Last_Affected_Version, Revision_No, File, Name]")
    args = parser.parse_args()
    main(args.vulData)
