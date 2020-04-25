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
SEASON_OVERVIEW_DATA = ['premier_league_table_2014-15',
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

    db_cursor = plepa_db.db_cursor()

    insert_data('stadium_team', STADIUM_DATA, db_cursor, plepa_db)
    insert_data('game', GAME_DATA, db_cursor, plepa_db)
    insert_data('season_overview', SEASON_OVERVIEW_DATA, db_cursor, plepa_db)

    plepa_db.close()


# ===================================================== Functions ==================================================== #


def insert_data(data_type, data, db_cursor, database):
    """
    A function to insert data into the MySQL database for PLePA.
    Must use stadium_team, game or season_overview for data_type.

    Args:
        data_type (str): The type of data to be inserted. i.e. stadium_team, game or season_overview.
        data (list): A list of names of CSV sheets to be inserted into the database.
        db_cursor (db_cursor_type): The db_cursor used to query the database.
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
                        db_cursor.execute(sql)
                        database.commit()
                        sql = f'INSERT INTO team (name_pk, stadium_id_fk) ' \
                              f'SELECT "{team}", stadium_id_pk ' \
                              f'FROM stadium ' \
                              f'WHERE stadium_name = "{stadium_name}"'
                        db_cursor.execute(sql)
                        database.commit()
                    elif data_type == 'game':
                        home_team = row[3].upper()
                        away_team = row[4].upper()
                        season = row[0]
                        home_team_score = row[5]
                        away_team_score = row[6]
                        sql = f'INSERT INTO game (home_team_id_pk_fk, away_team_id_pk_fk, season_pk, home_team_score, away_team_score) ' \
                              f'SELECT team1.team_id_pk, team2.team_id_pk, {season}, {home_team_score}, {away_team_score} ' \
                              f'FROM team team1, team team2 ' \
                              f'WHERE team1.name_pk = "{home_team}" ' \
                              f'AND team2.name_pk = "{away_team}"'
                        db_cursor.execute(sql)
                        database.commit()
                    elif data_type == 'season_overview':
                        team = row[2]
                        season = row[0]
                        position = row[1]
                        goals_for = row[7]
                        goals_against = row[8]
                        wins = row[4]
                        draws = row[5]
                        losses = row[6]
                        sql = f'INSERT INTO season_overview (team_id_pk_fk, season_pk, position, goals_for, goals_against, wins, draws, losses) ' \
                              f'SELECT team.team_id_pk, {season}, {position}, {goals_for}, {goals_against}, {wins}, {draws}, {losses} ' \
                              f'FROM team ' \
                              f'WHERE name_pk = "{team}" '
                        db_cursor.execute(sql)
                        database.commit()
                    else:
                        print('Invalid data type sent in!')
                        raise sys.exit
                line_count += 1


# ==================================================================================================================== #


if __name__ == '__main__':
    main()
