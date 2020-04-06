import csv

selectedColumns = [
    'Datetime',
    'id',
    'IsSelected',
    'Gender',
    'College',
    'StudentProgram',
    'GraduationYear',
    'NHackathon',
    'Role',
    'HasTeam',
    'TeamMembers',
    'TeamId',
    'University',
    'TeamSize'
]

editions = ['2016.1', '2016.2', '2017.1', '2017.2', '2018.1']

def getHeaderMap(header: list) -> dict:
    headerMap = {}
    for i in range(len(header)):
        if header[i] in selectedColumns:
            headerMap[header[i]] = i

    if set(headerMap.keys()) != set(selectedColumns):
        raise RuntimeError('Could not get all required columns from header=[{header}]'.format(header=header))

    return headerMap

def buildFormattedRow(headerMap: dict, row: list) -> list:
    formattedRow = []

    for column in selectedColumns:
        columnIndex = headerMap[column]
        formattedRow.append(row[columnIndex])

    return formattedRow

def openFile(edition: str) -> list:
    directory = 'data/{edition}'.format(edition=edition)
    filePath = '../{directory}/{edition}-FormattedRegistrationFile.csv'.format(directory=directory, edition=edition)

    newRows = []

    with open(filePath) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        header = next(csv_reader)

        headerMap = getHeaderMap(header)

        for row in csv_reader:
            newRows.append(buildFormattedRow(headerMap, row))

    return newRows

def main():
    openFile(editions[0])

main()