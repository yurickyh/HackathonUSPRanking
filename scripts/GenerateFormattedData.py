import csv
import re
import warnings

HEADER_MAP = {
    'Carimbo de data/hora': 'Datetime',
    'ID': 'id',
    'Selecionado': 'IsSelected',
    'Gênero': 'Gender',
    'Qual a sua escola / faculdade / instituto?': 'College',
    'Qual o seu curso / programa de pós?': 'StudentProgram',
    'Em que ano você está?': 'GraduationYear',
    'Você já participou de quantos hackathons?': 'NHackathon',
    'Qual a sua especialidade?': 'Role',
    'Você já tem equipe formada?': 'HasTeam',
    'Se sim, conte-nos quem são:': 'TeamMembers',
    'Time': 'TeamId'
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

def writeCsv(header: list, rows: list, directory: str):
    newFile = open('../{directory}/2018.1-FormattedRegisteredFile.csv'.format(directory=directory), 'w')

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

def main():
    directory = 'data/2018.1'
    filePath = '../{directory}/2018.1 - Inscritos.csv'.format(directory=directory)

    with open(filePath) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter = ';')

        header = next(csv_reader)

        newRows = []

        for row in csv_reader:
            row[4] = editCollege(row[4])
            row[6] = editGraduationYear(row[6])
            row.append(getNumberTeamMembers(row[10]))
            newRows.append(row)

        writeCsv(header, newRows, directory)

main()