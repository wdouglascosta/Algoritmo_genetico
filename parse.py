import pandas as pd
pd.read_csv('run.log', sep='\t').to_csv('planilha.csv')

var = []
var = pd.read_csv('run.log', sep='\t')

print(var)


# import csv

# with open('run.log') as csvfile:
#     readCSV = csv.reader(csvfile, delimiter='\t')
#     soma = 0
#     for row in readCSV:
#         if (row[3] == 'JobRuntime'):
#             pass
#         else:
#             soma += float(row[3])
#         print(row[3])
#     print(soma)
# csvfile.close()

