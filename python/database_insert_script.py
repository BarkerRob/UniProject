# ====================================================== Imports ===================================================== #

import csv
import sys

import mysql.connector

# ===================================================== Variables ==================================================== #

DATA_PATH = 'E:\\Code\\Dev\\Python\\Projects\\UniProject\\data\\'
STADIUM_DATA = ['stadium_data']
GAME_DATA = ['premier_league_results_2014-15',
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

    insert_data('stadium_team', STADIUM_DATA, cursor, plepa_db)
    insert_data('game', GAME_DATA, cursor, plepa_db)
    insert_data('table', TABLE_DATA, cursor, plepa_db)

    plepa_db.close()


# ===================================================== Functions ==================================================== #


def insert_data(data_type, data, cursor, database):
    """
    A function to insert data into the MySQL database for PLePA.
    Must use stadium_team, game or table for data_type.

    Args:
        data_type (str): The type of data to be inserted. i.e. stadium_team, game or table.
        data (list): A list of names of CSV sheets to be inserted into the database.
        cursor (cursor_type): The cursor used to query the database.
        database (my_sql connection): The connection to the database.
    """
    for each_file in data:
        with open(f'{DATA_PATH}{each_file}.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                # do not process the header row, ignore line 0.
                if line_count != 0:
                    if data_type == 'stadium_team':
                        pass
                        stadium_name = row[1].upper()
                        x_coord = float(row[3])
                        y_coord = float(row[2])
                        team = row[0].upper()
                        sql = f'INSERT INTO stadium (stadium_name, x_coord, y_coord) ' \
                              f'VALUES ("{stadium_name}", {x_coord}, {y_coord})'
                        cursor.execute(sql)
                        database.commit()
                        sql = f'INSERT INTO team (name_pk, stadium_id_fk) ' \
                              f'SELECT "{team}", stadium_id_pk ' \
                              f'FROM stadium ' \
                              f'WHERE stadium_name = "{stadium_name}"'
                        cursor.execute(sql)
                        database.commit()
                    elif data_type == 'game':
                        # Todo fix bug mysql.connector.errors.ProgrammingError: 1054 (42S22): Unknown column 'Norwich' in 'field list'
                        home_team = row[3].upper()
                        away_team = row[4].upper()
                        season = row[0]
                        home_team_score = row[5]
                        away_team_score = row[6]
                        sql = f'INSERT INTO game (home_team_id_pk_fk, away_team_id_pk_fk, season_pk, home_team_score, away_team_score) ' \
                              f'SELECT team1.team_id_pk, team2.team_id_pk, "{season}", {home_team_score}, {away_team_score} ' \
                              f'FROM team team1, team team2 ' \
                              f'WHERE team1.name_pk = "{home_team}" ' \
                              f'AND team2.name_pk = "{away_team}"'
                        cursor.execute(sql)
                        database.commit()
                    elif data_type == 'table':
                        # Todo insert table data here
                        pass
                    else:
                        print('Invalid data type sent in!')
                        raise sys.exit
                line_count += 1


# ==================================================================================================================== #


if __name__ == '__main__':
    main()
