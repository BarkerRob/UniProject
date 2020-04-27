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

import math
import random

import mysql.connector

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
    db_cursor = plepa_db.cursor(buffered=True)

    sql = f'SELECT * ' \
          f'FROM plepa.thresholds '
    db_cursor.execute(sql)

    # Thresholds
    # loss is always 0
    loss = 0
    win = 0
    draw = 0
    for thresholds in db_cursor:
        win = thresholds[0]
        draw = thresholds[1]

    team_one = 1
    team_two = 2

    sql = f'SELECT * ' \
          f'FROM game ' \
          f'WHERE season_pk = {CURRENT_SEASON}'
    db_cursor.execute(sql)
    games = []
    game_counter = 0
    correct_prediction_counter = 0
    for game_id, db_team_one, db_team_two, season, db_team_one_score, db_team_two_score in db_cursor:
        games.append([game_id, db_team_one, db_team_two, season, db_team_one_score, db_team_two_score])
    for game_id, db_team_one, db_team_two, season, db_team_one_score, db_team_two_score in games:
        game_counter = game_counter + 1
        team_one = db_team_one
        team_two = db_team_two
        team_one_score = db_team_one_score
        team_two_score = db_team_two_score
        predicted_score = 0
        function_dict = {}
        for i in range(3):
            function_chooser = random.randint(1, 5)
            if function_chooser == 1:
                recent_form_result = recent_form(team_one, team_two, db_cursor)
                predicted_score = predicted_score + recent_form_result
                function_dict[f"recent_form {i + 1}"] = recent_form_result
            elif function_chooser == 2:
                form_against_team_result = form_against_team(7, 13, db_cursor)
                predicted_score = predicted_score + form_against_team_result
                function_dict[f"form_against_team {i + 1}"] = form_against_team_result
            elif function_chooser == 3:
                distance_travelled_result = distance_travelled(team_one, team_two, db_cursor)
                predicted_score = predicted_score + distance_travelled_result
                function_dict[f"distance_travelled {i + 1}"] = distance_travelled_result
            elif function_chooser == 4:
                league_difference_result = league_difference(team_one, team_two, db_cursor)
                predicted_score = predicted_score + league_difference_result
                function_dict[f"league_difference {i + 1}"] = league_difference_result
            elif function_chooser == 5:
                current_league_difference_result = current_league_difference(team_one, team_two, db_cursor)
                predicted_score = predicted_score + current_league_difference_result
                function_dict[f"current_league_difference {i + 1}"] = current_league_difference_result
        if team_one_score > team_two_score:
            actual_result = 'WIN'
        elif team_two_score < team_one_score:
            actual_result = 'LOSE'
        else:
            actual_result = 'DRAW'
        if predicted_score < draw:
            predicted_result = 'LOSE'
        elif predicted_score < win:
            predicted_result = 'DRAW'
        else:
            predicted_result = 'WIN'
        if actual_result == predicted_result:
            correct_prediction_counter = correct_prediction_counter + 1
        else:
            sql = 'UPDATE thresholds '
            second_sql = ''
            if predicted_result == 'WIN' and actual_result == 'DRAW':
                sql = sql + 'SET win = win + 0.001'
            elif predicted_result == 'WIN' and actual_result == 'LOSE':
                sql = sql + 'SET win = win + 0.002'
            elif predicted_result == 'DRAW' and actual_result == 'WIN':
                sql = sql + 'SET win = win - 0.001'
            elif predicted_result == 'DRAW' and actual_result == 'LOSE':
                sql = sql + 'SET draw = draw + 0.001'
            elif predicted_result == 'LOSE' and actual_result == 'DRAW':
                sql = sql + 'SET draw = draw - 0.001'
            elif predicted_result == 'LOSE' and actual_result == 'WIN':
                sql = sql + 'SET draw = draw - 0.0001'
                second_sql = 'UPDATE thresholds ' \
                             'SET win = win - 0.0001'
            db_cursor.execute(sql)
            plepa_db.commit()
            if second_sql != '':
                db_cursor.execute(second_sql)
                plepa_db.commit()
        print(actual_result, predicted_result)
    print(correct_prediction_counter/game_counter)
    plepa_db.close()


# ===================================================== Functions ==================================================== #


def recent_form(team_id_one, team_id_two, db_cursor):
    sql = f'SELECT * ' \
          f'FROM plepa.game ' \
          f'WHERE home_team_id_pk_fk = {team_id_one}  OR away_team_id_pk_fk = {team_id_one} ' \
          f'ORDER BY game_pk DESC ' \
          f'LIMIT 5'
    db_cursor.execute(sql)
    team_one_form = 0
    for game_nr, home_team_id, away_team_id, season, home_team_score, away_team_score in db_cursor:
        if home_team_id == team_id_one:
            result = home_team_score - away_team_score
        else:
            result = away_team_score - home_team_score
        if result > 0:
            team_one_form = team_one_form + 0.2
        elif result == 0:
            team_one_form = team_one_form + 0.1
    sql = f'SELECT * ' \
          f'FROM plepa.game ' \
          f'WHERE home_team_id_pk_fk = {team_id_two}  OR away_team_id_pk_fk = {team_id_two} ' \
          f'ORDER BY game_pk DESC ' \
          f'LIMIT 5'
    db_cursor.execute(sql)
    team_two_form = 0
    for game_nr, home_team_id, away_team_id, season, home_team_score, away_team_score in db_cursor:
        if home_team_id == team_id_two:
            result = home_team_score - away_team_score
        else:
            result = away_team_score - home_team_score
        if result > 0:
            team_two_form = team_two_form + 0.2
        elif result == 0:
            team_two_form = team_two_form + 0.1
    form = team_one_form - (team_two_form / 3)
    return form


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
            form = form + 0.066
    return form


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
    # Max distance between clubs is ~ 600
    distance = round(0.5 + (distance / 1200), 2)
    if distance < 0:
        distance = 0
    return distance


# ==================================================================================================================== #


def league_difference(team_id_one, team_id_two, db_cursor):
    sql = f'SELECT position ' \
          f'FROM plepa.season_overview ' \
          f'WHERE team_id_pk_fk =  {team_id_one} ' \
          f'AND season_pk = {CURRENT_SEASON} - 1 '
    db_cursor.execute(sql)
    # Set default to 20 because newly promoted teams have a previous league position of 20.
    team_one_league_position = 20
    team_two_league_position = 20
    for last_league_position in db_cursor:
        team_one_league_position = last_league_position[0]
    sql = f'SELECT position ' \
          f'FROM plepa.season_overview ' \
          f'WHERE team_id_pk_fk =  {team_id_two} ' \
          f'AND season_pk = {CURRENT_SEASON} - 1 '
    db_cursor.execute(sql)
    for last_league_position in db_cursor:
        team_two_league_position = last_league_position[0]
    league_diff = team_two_league_position - team_one_league_position
    if league_diff > 0:
        league_diff = 0.5 + round((league_diff / 38), 2)
    else:
        league_diff = round(1 + (league_diff / 19), 2)
    return league_diff


# ==================================================================================================================== #


def current_league_difference(team_id_one, team_id_two, db_cursor):
    sql = f'SELECT position ' \
          f'FROM plepa.season_overview ' \
          f'WHERE team_id_pk_fk =  {team_id_one} ' \
          f'AND season_pk = {CURRENT_SEASON} '
    db_cursor.execute(sql)
    # Set default to 20 just in case unable to determine
    team_one_league_position = 20
    team_two_league_position = 20
    for last_league_position in db_cursor:
        team_one_league_position = last_league_position[0]
    sql = f'SELECT position ' \
          f'FROM plepa.season_overview ' \
          f'WHERE team_id_pk_fk =  {team_id_two} ' \
          f'AND season_pk = {CURRENT_SEASON} '
    db_cursor.execute(sql)
    for last_league_position in db_cursor:
        team_two_league_position = last_league_position[0]
    league_diff = team_two_league_position - team_one_league_position
    if league_diff > 0:
        league_diff = 0.5 + round((league_diff / 38), 2)
    else:
        league_diff = 0.5 + round(league_diff / 38, 2)
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
