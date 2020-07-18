"""
"""
# ====================================================== Imports ===================================================== #

import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm, datasets
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
    iris = datasets.load_iris()
    training_dataset = []
    sql = f'SELECT * ' \
          f'FROM svm_data '
    db_cursor.execute(sql)
    for away_team_distance_travelled, league_difference, result in db_cursor:
        training_dataset.append([away_team_distance_travelled, league_difference, result])
    test_dataset = []
    sql = f'SELECT * ' \
          f'FROM svm_test_data '
    db_cursor.execute(sql)
    for away_team_distance_travelled, league_difference, result in db_cursor:
        test_dataset.append([away_team_distance_travelled, league_difference, result])


# ===================================================== Functions ==================================================== #


"""def new_function(arg1, arg2):
    return 0"""


# ==================================================================================================================== #


# ==================================================================================================================== #


if __name__ == '__main__':
    main()
