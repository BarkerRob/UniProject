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

    cursor = plepa_db.cursor()

    drop_tables(cursor, plepa_db)
    create_tables(cursor, plepa_db)

    plepa_db.close()


# ===================================================== Functions ==================================================== #


def drop_tables(cursor, database):
    """
    A function to drop all tables in the database.

    Args:
        cursor (cursor_type): The cursor used to query the database.
        database (my_sql connection): The connection to the database.
    """
    sql = f'DROP TABLE game '
    cursor.execute(sql)
    sql = f'DROP TABLE season_overview '
    cursor.execute(sql)
    sql = f'DROP TABLE team '
    cursor.execute(sql)
    sql = f'DROP TABLE stadium '
    cursor.execute(sql)
    database.commit()


# ==================================================================================================================== #

def create_tables(cursor, database):
    """
    A function to create all tables for the database.

    Args:
        cursor (cursor_type): The cursor used to query the database.
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
    cursor.execute(sql)
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
    cursor.execute(sql)
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
    cursor.execute(sql)
    sql = f'''
    CREATE TABLE game (
        home_team_id_pk_fk INT,
        away_team_id_pk_fk INT,
        season_pk INT,
        home_team_score INT,
        away_team_score INT,
        PRIMARY KEY (home_team_id_pk_fk, away_team_id_pk_fk, season_pk),
        CONSTRAINT fk_home_team_id
        FOREIGN KEY (home_team_id_pk_fk)
            REFERENCES team(team_id_pk),
        CONSTRAINT fk_away_team_id
        FOREIGN KEY (away_team_id_pk_fk)
            REFERENCES team(team_id_pk)
    ) 
    '''
    cursor.execute(sql)
    database.commit()


# ==================================================================================================================== #


if __name__ == '__main__':
    main()
