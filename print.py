import csv

with open('QQQ.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)
