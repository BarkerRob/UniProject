"""
"""
# ====================================================== Imports ===================================================== #

import matplotlib.pyplot as plt
import mysql.connector
import numpy as np
from matplotlib import style
from sklearn import svm

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
    fignum = 1
    for kernel in ('linear', 'rbf'):
        clf = svm.SVC(kernel=kernel, gamma=2)
        clf.fit(training_plot, result_plot)
        plt.figure(fignum)
        plt.clf()
        plt.scatter(clf.support_vectors_[:, 0], clf.support_vectors_[:, 1], s=80, facecolors='none', zorder=10,
                    edgecolors='k')
        plt.scatter(training_plot[:, 0], training_plot[:, 1], c=result_plot, zorder=10, cmap=plt.cm.Paired, edgecolors='k')
        plt.axis('tight')
        x_min = 0
        x_max = 500
        y_min = -20
        y_max = 20
        XX, YY = np.mgrid[x_min:x_max:200j, y_min:y_max:200j]
        Z = clf.decision_function(np.c_[XX.ravel(), YY.ravel()])

        # Put the result into a color plot
        Z = Z.reshape(XX.shape)
        plt.figure(fignum, figsize=(4, 3))
        plt.pcolormesh(XX, YY, Z > 0, cmap=plt.cm.Paired)
        plt.contour(XX, YY, Z, colors=['k', 'k', 'k'], linestyles=['--', '-', '--'],
                    levels=[-.5, 0, .5])

        plt.xlim(x_min, x_max)
        plt.ylim(y_min, y_max)

        plt.xticks(())
        plt.yticks(())
        fignum = fignum + 1
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
