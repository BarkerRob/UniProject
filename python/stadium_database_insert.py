import mysql.connector
import csv

plepa_db = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='PLePApw',
    database='plepa'
)

cursor = plepa_db.cursor()

with open('E:\\Code\\Dev\\Python\\Projects\\UniProject\\data\\stadium_data.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        # do not process the header row, ignore line 0.
        if line_count != 0:
            stadium_name = row[1].upper()
            x_coord = float(row[3])
            y_coord = float(row[2])
            sql = f'INSERT INTO stadium (stadium_name, x_coord, y_coord) VALUES ("{stadium_name}", {x_coord}, {y_coord})'
            cursor.execute(sql)
            plepa_db.commit()
        line_count += 1
