"""
"""
# ====================================================== Imports ===================================================== #

import math

import mysql.connector


# ===================================================== Variables ==================================================== #


# ======================================================= Main ======================================================= #


def main():
    plepa_db = mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='PLePApw',
        database='plepa'
    )
    db_cursor = plepa_db.cursor(buffered=True)

    sql = f'SELECT * ' \
          f'FROM game ' \
          f'WHERE season_pk IN (2019)'
    db_cursor.execute(sql)
    games = []
    for game_id, db_team_one, db_team_two, season, db_team_one_score, db_team_two_score in db_cursor:
        games.append([game_id, db_team_one, db_team_two, season, db_team_one_score, db_team_two_score])
    for game_id, db_team_one, db_team_two, season, db_team_one_score, db_team_two_score in games:
        team_one = db_team_one
        team_two = db_team_two
        team_one_score = db_team_one_score
        team_two_score = db_team_two_score
        distance_travelled_result = distance_travelled(team_one, team_two, db_cursor)
        season_league_difference_result = season_league_difference(team_one, team_two, season,
                                                                     db_cursor)
        if team_one_score > team_two_score:
            actual_result = 'WIN'
        elif team_two_score > team_one_score:
            actual_result = 'LOSE'
        else:
            actual_result = 'DRAW'
        sql = f"INSERT INTO knn_test_data values (" \
              f"{distance_travelled_result}, " \
              f"{season_league_difference_result}, " \
              f"'{actual_result}') "
        db_cursor.execute(sql)
        plepa_db.commit()
    plepa_db.close()


# ===================================================== Functions ==================================================== #


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
    # Max distance between clubs is ~ 600
    if distance < 0:
        distance = 0
    return distance


# ==================================================================================================================== #


def season_league_difference(team_id_one, team_id_two, season, db_cursor):
    sql = f'SELECT position ' \
          f'FROM plepa.season_overview ' \
          f'WHERE team_id_pk_fk =  {team_id_one} ' \
          f'AND season_pk = {season} '
    db_cursor.execute(sql)
    # Set default to 20 just in case unable to determine
    team_one_league_position = 20
    team_two_league_position = 20
    for last_league_position in db_cursor:
        team_one_league_position = last_league_position[0]
    sql = f'SELECT position ' \
          f'FROM plepa.season_overview ' \
          f'WHERE team_id_pk_fk =  {team_id_two} ' \
          f'AND season_pk = {season} '
    db_cursor.execute(sql)
    for last_league_position in db_cursor:
        team_two_league_position = last_league_position[0]
    league_diff = team_two_league_position - team_one_league_position
    return league_diff


# ==================================================================================================================== #


def calculate_distance(x_coord_one, y_coord_one, x_coord_two, y_coord_two):
    r = 6372800  # Earth radius in meters

    phi1, phi2 = math.radians(y_coord_one), math.radians(y_coord_two)
    dphi = math.radians(y_coord_two - y_coord_one)
    dlambda = math.radians(x_coord_two - x_coord_one)

    a = math.sin(dphi / 2) ** 2 + \
        math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2

    return 2 * r * math.atan2(math.sqrt(a), math.sqrt(1 - a)) / 1000


# ==================================================================================================================== #


if __name__ == '__main__':
    main()
