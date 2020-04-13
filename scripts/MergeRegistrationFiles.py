import csv

selectedColumns = [
    'Datetime',
    'Edition',
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
    # 'University',
    'TeamSize'
]

editions = ['2016.1', '2016.2', '2017.1', '2017.2', '2018.1']


def getHeaderMap(header: list, edition: str) -> dict:
    """
    Maps the index of the element in the selectedColumns list
    :param header: list of the columns in the header of the file
    :param edition: edition of the file
    :return: dict column name -> index
    """
    headerMap = {}
    for i in range(len(header)):
        if header[i] in selectedColumns:
            headerMap[header[i]] = i

    headerMap['Edition'] = edition

    setHeaderMap = set(headerMap.keys())
    setSelectedColumns = set(selectedColumns)

    if setHeaderMap != setSelectedColumns:
        missingColumns = setSelectedColumns.difference(setHeaderMap)
        raise RuntimeError('Header is missing the following columns [{columns}]'.format(columns=missingColumns))

    return headerMap

def buildFormattedRow(headerMap: dict, row: list) -> list:
    """
    Build the row according to the selectedColumns list
    :rtype: list
    :param headerMap:
    :param row: a row in the file
    :return: new row formatted according to selectedColumns
    """
    formattedRow = []

    for column in selectedColumns:
        if column == 'Edition':
            formattedRow.append(headerMap[column])
        else:
            columnIndex = headerMap[column]
            formattedRow.append(row[columnIndex])
    return formattedRow


def readAndFormatFile(edition: str) -> list:
    """
    Opens the file and read it to build the new file
    :param edition: edition of the file
    :return: list of formatted rows
    """
    directory = 'data/{edition}'.format(edition=edition)
    filePath = '../{directory}/{edition}-FormattedRegistrationFile.csv'.format(directory=directory, edition=edition)

    newRows = []

    with open(filePath) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        header = next(csv_reader)

        headerMap = getHeaderMap(header, edition)

        for row in csv_reader:
            newRows.append(buildFormattedRow(headerMap, row))

    return newRows


def writeFile():
    filename = '../data/AllRegistrationsFile.csv'
    newFile = open(filename, 'w')

    with newFile:
        csv_writer = csv.writer(newFile)
        csv_writer.writerow(selectedColumns)

        for edition in editions:
            csv_writer.writerows(readAndFormatFile(edition))


def main():
    writeFile()


main()
