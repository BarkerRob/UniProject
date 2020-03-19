# ====================================================== Imports ===================================================== #

import csv

import mysql.connector

# ===================================================== Variables ==================================================== #

DATA_PATH = 'E:\\Code\\Dev\\Python\\Projects\\UniProject\\data\\'
STADIUM_DATA = ['stadium_data']
RESULTS_DATA = ['premier_league_results_2014-15',
                'premier_league_results_2015-16',
                'premier_league_results_2016-17',
                'premier_league_results_2017-18',
                'premier_league_results_2018-19',
                'premier_league_results_2019-20']
TABLE_DATA = ['premier_league_table_2014-15',
              'premier_league_table_2015-16',
              'premier_league_table_2016-17',
              'premier_league_table_2017-18',
              'premier_league_table_2018-19',
              'premier_league_table_2019-20']


# ======================================================= Main ======================================================= #


def main():
    plepa_db = mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='PLePApw',
        database='plepa'
    )

    cursor = plepa_db.cursor()

    insert_stadium_data(cursor, plepa_db)
    insert_results_data(cursor, plepa_db)
    insert_table_data(cursor, plepa_db)

    plepa_db.close()


# ===================================================== Functions ==================================================== #


def insert_stadium_data(cursor, database):
    """
    A function to insert stadium data for PLePA.

    Args:
        cursor (cursor_type): The cursor used to query the database.
        database (my_sql connection): The connection to the database.
    """
    for each_file in STADIUM_DATA:
        with open(f'{DATA_PATH}{each_file}.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                # do not process the header row, ignore line 0.
                if line_count != 0:
                    stadium_name = row[1].upper()
                    x_coord = float(row[3])
                    y_coord = float(row[2])
                    team = row[0].upper()
                    sql = f'INSERT INTO stadium (stadium_name, x_coord, y_coord) VALUES ("{stadium_name}", {x_coord}, {y_coord})'
                    cursor.execute(sql)
                    database.commit()
                    sql = f'INSERT INTO team (name_pk, stadium_id_fk) SELECT "{team}", stadium_id_pk FROM stadium where stadium_name = "{stadium_name}"'
                    cursor.execute(sql)
                    database.commit()
                line_count += 1


# ==================================================================================================================== #

def insert_results_data(cursor, database):
    pass
    # Do work here


# ==================================================================================================================== #

def insert_table_data(cursor, database):
    pass
    # Do work here


# ==================================================================================================================== #


if __name__ == '__main__':
    main()
