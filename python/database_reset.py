# ====================================================== Imports ===================================================== #

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

    db_cursor = plepa_db.db_cursor()

    drop_tables(db_cursor, plepa_db)
    create_tables(db_cursor, plepa_db)

    plepa_db.close()


# ===================================================== Functions ==================================================== #


def drop_tables(db_cursor, database):
    """
    A function to drop all tables in the database.

    Args:
        db_cursor (db_cursor_type): The db_cursor used to query the database.
        database (my_sql connection): The connection to the database.
    """
    sql = f'DROP TABLE game '
    db_cursor.execute(sql)
    sql = f'DROP TABLE season_overview '
    db_cursor.execute(sql)
    sql = f'DROP TABLE team '
    db_cursor.execute(sql)
    sql = f'DROP TABLE stadium '
    db_cursor.execute(sql)
    database.commit()


# ==================================================================================================================== #

def create_tables(db_cursor, database):
    """
    A function to create all tables for the database.

    Args:
        db_cursor (db_cursor_type): The db_cursor used to query the database.
        database (my_sql connection): The connection to the database.
    """
    sql = f'''
        CREATE TABLE stadium
        (
            stadium_id_pk INT AUTO_INCREMENT PRIMARY KEY,
            stadium_name VARCHAR(255) NOT NULL, 
            x_coord DECIMAL(13, 8) NOT NULL,
            y_coord DECIMAL(13, 8) NOT NULL
        )
        '''
    db_cursor.execute(sql)
    sql = f'''
        CREATE TABLE team 
        (
            team_id_pk INT AUTO_INCREMENT PRIMARY KEY,
            name_pk VARCHAR(255) NOT NULL,
            stadium_id_fk INT,
            CONSTRAINT fk_stadium
            FOREIGN KEY (stadium_id_fk)
                REFERENCES stadium(stadium_id_pk)
        )
        '''
    db_cursor.execute(sql)
    sql = f'''
    CREATE TABLE season_overview 
    (
        team_id_pk_fk INT,
        season_pk INT,
        position INT,
        goals_for INT,
        goals_against INT,
        wins INT,
        draws INT,
        losses INT,
        PRIMARY KEY (team_id_pk_fk, season_pk),
        CONSTRAINT fk_team_id
        FOREIGN KEY (team_id_pk_fk)
            REFERENCES team(team_id_pk)
    )
    '''
    db_cursor.execute(sql)
    sql = f'''
    CREATE TABLE game (
        game_pk INT AUTO_INCREMENT,
        home_team_id_pk_fk INT,
        away_team_id_pk_fk INT,
        season_pk INT,
        home_team_score INT,
        away_team_score INT,
        PRIMARY KEY (game_pk, home_team_id_pk_fk, away_team_id_pk_fk, season_pk),
        CONSTRAINT fk_home_team_id
        FOREIGN KEY (home_team_id_pk_fk)
            REFERENCES team(team_id_pk),
        CONSTRAINT fk_away_team_id
        FOREIGN KEY (away_team_id_pk_fk)
            REFERENCES team(team_id_pk)
    ) 
    '''
    db_cursor.execute(sql)
    sql = f'''
    CREATE TABLE thresholds (
        win DECIMAL(5, 4),
        draw DECIMAL(5, 4)
    )
    '''
    db_cursor.execute(sql)
    sql = f'''
    CREATE TABLE random_forest_results (
        test_id INT AUTO_INCREMENT PRIMARY KEY,
        team_one_id INT,
        team_two_id INT,
        function_one_name VARCHAR(255),
        function_one_value DECIMAL(5, 4),
        function_two_name VARCHAR(255),
        function_two_value DECIMAL(5, 4),
        function_three_name VARCHAR(255),
        function_three_value DECIMAL(5, 4),
        total_predicted_value DECIMAL(5, 4),
        predicted_result VARCHAR(255),
        actual_result VARCHAR(255),
        correct BOOLEAN
    )
    '''
    db_cursor.execute(sql)
    database.commit()





# ==================================================================================================================== #


if __name__ == '__main__':
    main()
