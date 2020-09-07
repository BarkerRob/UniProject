"""
"""
# ====================================================== Imports ===================================================== #
import csv
from math import exp
from math import pi
from math import sqrt

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
    summary = label_summary(training_dataset)
    db_cursor.execute(sql)

    training_dataset = []
    for away_team_distance_travelled, league_difference, result in db_cursor:
        result_label = 0
        if result == 'WIN':
            result_label = 1
        else:
            result_label = 0
        training_dataset.append([int(away_team_distance_travelled), int(league_difference), result_label])
    summary_for_two = label_summary(training_dataset)

    test_dataset = []
    sql = f'SELECT * ' \
          f'FROM nv_test_data '
    db_cursor.execute(sql)
    for away_team_distance_travelled, league_difference, result in db_cursor:
        test_dataset.append([int(away_team_distance_travelled), int(league_difference), result])
    win_counter = 0
    lose_counter = 0
    draw_counter = 0
    with open(f'../algorithm results/naive_bayes/nb_3class_results.csv', 'w',
              newline='') as csv_file:
        algorithm_writer = csv.writer(csv_file, delimiter=',')
        algorithm_writer.writerow(['prediction', 'actual_result'])
        for each_data in test_dataset:
            probabilities = calculate_label_probability(summary, each_data)
            predicted_result = ''
            win = probabilities.get(3)
            draw = probabilities.get(1)
            lose = probabilities.get(0)
            if draw > win and draw > lose:
                predicted_result = 'DRAW'
                draw_counter = draw_counter + 1
            elif win > lose:
                predicted_result = 'WIN'
                win_counter = win_counter + 1
            else:
                predicted_result = 'LOSE'
                lose_counter = lose_counter + 1
            print(each_data[2], predicted_result, probabilities)
            algorithm_writer.writerow([predicted_result, each_data[2]])

    db_cursor.execute(sql)
    with open(f'../algorithm results/naive_bayes/nb_2class_results.csv', 'w',
              newline='') as csv_file:
        algorithm_writer = csv.writer(csv_file, delimiter=',')
        algorithm_writer.writerow(['prediction', 'actual_result'])
        win_counter = 0
        draw_lose_counter = 0
        for each_data in test_dataset:
            probabilities = calculate_label_probability(summary_for_two, each_data)
            predicted_result = ''
            win = probabilities.get(1)
            else_result = probabilities.get(0)
            if else_result > win:
                predicted_result = 'DRAW/LOSE'
                draw_lose_counter = draw_lose_counter + 1
            else:
                predicted_result = 'WIN'
                win_counter = win_counter + 1
            algorithm_writer.writerow([predicted_result, each_data[2]])

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
    mean = sum(list_of_vals) / float(len(list_of_vals))
    return mean


# ==================================================================================================================== #


def calculate_stdev(list_of_vals):
    average = calculate_mean(list_of_vals)
    variance = sum([(x - average) ** 2 for x in list_of_vals]) / float(len(list_of_vals) - 1)
    return sqrt(variance)


# ==================================================================================================================== #


def calculate_data(data):
    summarized_data = [(calculate_mean(column), calculate_stdev(column), len(column)) for column in zip(*data)]
    del (summarized_data[-1])
    return summarized_data


# ==================================================================================================================== #


def label_summary(dataset):
    sorted_data = sort_data_by_label(dataset)
    summary = dict()
    for class_value, rows in sorted_data.items():
        summary[class_value] = calculate_data(rows)
    return summary


# ==================================================================================================================== #


def calculate_probability(x, mean, stdev):
    exponent = exp(-((x - mean) ** 2 / (2 * stdev ** 2)))
    return (1 / (sqrt(2 * pi) * stdev)) * exponent

# ==================================================================================================================== #


def calculate_label_probability(summaries, row):
    total_rows = sum([summaries[label][0][2] for label in summaries])
    probabilities = dict()
    for class_value, class_summaries in summaries.items():
        probabilities[class_value] = summaries[class_value][0][2]/float(total_rows)
        for i in range(len(class_summaries)):
            mean, stdev, count = class_summaries[i]
            probabilities[class_value] *= calculate_probability(row[i], mean, stdev)
    return probabilities

# ==================================================================================================================== #


if __name__ == '__main__':
    main()
