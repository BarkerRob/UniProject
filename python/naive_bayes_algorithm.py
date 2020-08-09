"""
"""
# ====================================================== Imports ===================================================== #

import mysql.connector
from math import sqrt


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
    sql = f'SELECT * ' \
          f'FROM nv_data '
    db_cursor.execute(sql)
    for away_team_distance_travelled, league_difference, result in db_cursor:
        result_label = 0
        if result == 'WIN':
            result_label = 3
        elif result == 'DRAW':
            result_label = 1
        else:
            result_label = 0
        training_dataset.append([int(away_team_distance_travelled), int(league_difference), result_label])
    summary = calculate_data(training_dataset)
    print(summary)

    test_dataset = []
    sql = f'SELECT * ' \
          f'FROM nv_test_data '
    db_cursor.execute(sql)
    for away_team_distance_travelled, league_difference, result in db_cursor:
        test_dataset.append([away_team_distance_travelled, league_difference, result])


# ===================================================== Functions ==================================================== #


def sort_data_by_label(data):
    sorted_data = dict()
    for i in range(len(data)):
        vector = data[i]
        label = vector[-1]
        if label not in sorted_data:
            sorted_data[label] = list()
        sorted_data[label].append(vector)
    return sorted_data


# ==================================================================================================================== #


def calculate_mean(list_of_vals):
    mean = sum(list_of_vals)/float(len(list_of_vals))
    return mean


# ==================================================================================================================== #


def calculate_stdev(list_of_vals):
    average = calculate_mean(list_of_vals)
    variance = sum([(x-average)**2 for x in list_of_vals]) / float(len(list_of_vals)-1)
    return sqrt(variance)


# ==================================================================================================================== #


def calculate_data(data):
    summarized_data = [(calculate_mean(column), calculate_stdev(column), len(column)) for column in zip(*data)]
    del(summarized_data[-1])
    return summarized_data

# ==================================================================================================================== #


if __name__ == '__main__':
    main()
