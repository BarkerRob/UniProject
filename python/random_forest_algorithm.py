"""
Notes:
    Result criteria
    0 - 1.2 is a loss
    1.11 - 1.89 is a draw
    1.9 - 3.0 is a win

    Criteria to determine the result:
        Recent form, last 5 games
        Form against opponent, last 5 games, if possible
        Distance travelled, calculated by distance between stadiums
        Last years league position compared to opponents
        Current league position compared to opponents

        Possible inclusions:
            Goal difference of current season compared to opponent

Possible implementation:
    Function for each criteria, they can return a value between 0-1 each. The final value is determined from 3
    A main function which chooses, at random, 3 criteria - this is the random forest element to the code.
    The main function returns the result
    Example of this:
        Main:
            Recent form - returns 0.9
            Distance travelled - returns 0.1
            Form against opponent - returns 0.7
            Total is 1.7 which is a draw according to result criteria at the top.
"""
# ====================================================== Imports ===================================================== #

import mysql.connector
import math

# ===================================================== Variables ==================================================== #

CURRENT_SEASON = 2019


# ======================================================= Main ======================================================= #


def main():
    plepa_db = mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='PLePApw',
        database='plepa'
    )
    db_cursor = plepa_db.cursor()

    # TODO need to remove the 1 passing into this function, it needs to be passed in dynamically
    recent_form(1, db_cursor)
    form_against_team(1, 2, db_cursor)
    distance_travelled(1, 2, db_cursor)

    plepa_db.close()


# ===================================================== Functions ==================================================== #


def recent_form(team_id, db_cursor):
    sql = f'SELECT * ' \
          f'FROM plepa.game ' \
          f'WHERE home_team_id_pk_fk = {team_id}  OR away_team_id_pk_fk = {team_id} ' \
          f'ORDER BY game_pk DESC ' \
          f'LIMIT 5'
    db_cursor.execute(sql)
    form = 0
    for game_nr, home_team_id, away_team_id, season, home_team_score, away_team_score in db_cursor:
        if home_team_id == team_id:
            result = home_team_score - away_team_score
        else:
            result = away_team_score - home_team_score
        if result > 0:
            form = form + 0.2
        elif result == 0:
            form = form + 0.1
    print(form)


# ==================================================================================================================== #


def form_against_team(team_id_one, team_id_two, db_cursor):
    sql = f'SELECT * ' \
          f'FROM plepa.game ' \
          f'WHERE ((home_team_id_pk_fk = {team_id_one} AND away_team_id_pk_fk = {team_id_two}) ' \
          f'    OR (home_team_id_pk_fk = {team_id_two} AND away_team_id_pk_fk = {team_id_one})) ' \
          f'ORDER BY game_pk DESC ' \
          f'LIMIT 5'
    db_cursor.execute(sql)
    form = 0
    for game_nr, home_team_id, away_team_id, season, home_team_score, away_team_score in db_cursor:
        if home_team_id == team_id_one:
            result = home_team_score - away_team_score
        else:
            result = away_team_score - home_team_score
        if result > 0:
            form = form + 0.2
        elif result == 0:
            form = form + 0.666
    print(form)


# ==================================================================================================================== #


def distance_travelled(team_id_one, team_id_two, db_cursor):
    team_one_x = 0
    team_one_y = 0
    team_two_x = 0
    team_two_y = 0
    sql = f'SELECT x_coord, y_coord ' \
          f'FROM plepa.stadium, plepa.team ' \
          f'WHERE stadium_id_pk = stadium_id_fk ' \
          f'AND team_id_pk = {team_id_one} '
    db_cursor.execute(sql)
    for team_one_x_sql, team_one_y_sql in db_cursor:
        team_one_x = team_one_x_sql
        team_one_y = team_one_y_sql
    sql = f'SELECT x_coord, y_coord ' \
          f'FROM plepa.stadium, plepa.team ' \
          f'WHERE stadium_id_pk = stadium_id_fk ' \
          f'AND team_id_pk = {team_id_two} '
    db_cursor.execute(sql)
    for team_two_x_sql, team_two_y_sql in db_cursor:
        team_two_x = team_two_x_sql
        team_two_y = team_two_y_sql
    distance = calculate_distance(team_one_x, team_one_y, team_two_x, team_two_y)
    print(distance)


# ==================================================================================================================== #


def calculate_distance(x_coord_one, y_coord_one, x_coord_two, y_coord_two):
    r = 6372800  # Earth radius in meters

    phi1, phi2 = math.radians(y_coord_one), math.radians(y_coord_two)
    dphi = math.radians(y_coord_two - y_coord_one)
    dlambda = math.radians(x_coord_two - x_coord_one)

    a = math.sin(dphi / 2) ** 2 + \
        math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2

    return round(2 * r * math.atan2(math.sqrt(a), math.sqrt(1 - a))/1000)


# ==================================================================================================================== #


if __name__ == '__main__':
    main()
