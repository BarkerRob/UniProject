"""
"""
# ====================================================== Imports ===================================================== #

from sklearn import svm
import mysql.connector
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
style.use("ggplot")

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
    training_dataset = []
    training_to_plot = []
    sql = f'SELECT * ' \
          f'FROM svm_data '
    db_cursor.execute(sql)
    for away_team_distance_travelled, league_difference, result in db_cursor:
        training_dataset.append([away_team_distance_travelled, league_difference, result])
        training_to_plot.append([away_team_distance_travelled, league_difference])
    result_plot = []
    training_plot = np.array(training_to_plot)
    for result in training_dataset:
        if result[2] == 'WIN':
            result_plot.append(1)
        else:
            result_plot.append(0)
    clf = svm.SVC(kernel='linear', C=1.0)
    clf.fit(training_plot, result_plot)
    w = clf.coef_[0]
    print(w)
    a = -w[0] / w[1]
    xx = np.linspace(0, 12)
    yy = a * xx - clf.intercept_[0] / w[1]
    h0 = plt.plot(xx, yy, 'k-', label="non weighted div")
    plt.scatter(training_plot[:, 0], training_plot[:, 1], c=result_plot)
    plt.legend()
    plt.show()

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
