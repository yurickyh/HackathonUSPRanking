import csv
import re
import warnings

HEADER_MAP = {
    'Edição': 'Edition',
    'Carimbo de data/hora': 'Datetime',
    'ID': 'id',
    'Selecionado': 'IsSelected',
    'Gênero': 'Gender',
    'Qual a sua escola / faculdade / instituto?': 'College',
    'Qual o seu curso / programa de pós?': 'StudentProgram',
    'Em que ano você está?': 'GraduationYear',
    'Você já participou de quantos hackathons?': 'NHackathon',
    'Qual a sua especialidade?': 'Role',
    'Quais as suas especialidades?': 'Roles',
    'Você já tem equipe formada?': 'HasTeam',
    'Se sim, conte-nos quem são:': 'TeamMembers',
    'Time': 'TeamId',
    'Em que universidade você estuda (ou estudou)?': 'University',
}

ADDITIONAL_COLUMNS = ['TeamSize']


def editCollege(college: str) -> str:
    if college.find('(') > 0 and college.find(')') > 0:
        pattern = '\((.*?)\)'
        return re.search(pattern, college).group(1)
    return college


def editGraduationYear(gradYear: str) -> str:
    gradNumbers = re.findall(r'\d+', gradYear)
    if len(gradNumbers) == 1:
        return gradNumbers.pop()
    warnings.warn('Unable to extract the gradYear=[%s]' % gradYear, Warning)
    return gradYear


def getNumberTeamMembers(teamMembers: str) -> int:
    return len(teamMembers.split(','))


def writeCsv(header: list, rows: list, directory: str, edition: str):
    filename = '../{directory}/{edition}-FormattedRegistrationFile.csv'.format(directory=directory, edition=edition)
    newFile = open(filename, 'w')

    with newFile:
        csv_writer = csv.writer(newFile)
        csv_writer.writerow(getFormattedHeader(header))
        csv_writer.writerows(rows)


def getFormattedHeader(header: list) -> list:
    newHeader = []
    for column in header:
        newHeader.append(HEADER_MAP[column])
    newHeader.extend(ADDITIONAL_COLUMNS)
    return newHeader

def getIndexByColumn(header: list, column: str) -> int:
    for i in range(len(header)):
        if HEADER_MAP[header[i]] == column:
            return i
    raise ValueError("Impossible to get index for column=[{column}]".format(column=column))

def main():
    edition = '2018.1'
    directory = 'data/{edition}'.format(edition=edition)
    filePath = '../{directory}/{edition} - Inscritos.csv'.format(directory=directory, edition=edition)

    with open(filePath) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')

        header = next(csv_reader)

        newRows = []

        for row in csv_reader:
            indexCollege = getIndexByColumn(header, 'College')
            row[indexCollege] = editCollege(row[indexCollege])

            indexGradYear = getIndexByColumn(header, 'GraduationYear')
            row[indexGradYear] = editGraduationYear(row[indexGradYear])

            indexTeamMembers = getIndexByColumn(header, 'TeamMembers')
            row.append(getNumberTeamMembers(row[indexTeamMembers]))

            newRows.append(row)

        writeCsv(header, newRows, directory, edition)


main()
