"""
"""
# ====================================================== Imports ===================================================== #

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
          f'FROM knn_data '
    db_cursor.execute(sql)
    for away_team_distance_travelled, league_difference, result in db_cursor:
        training_dataset.append([away_team_distance_travelled, league_difference, result])
    test_dataset = []
    sql = f'SELECT * ' \
          f'FROM knn_test_data '
    db_cursor.execute(sql)
    for away_team_distance_travelled, league_difference, result in db_cursor:
        test_dataset.append([away_team_distance_travelled, league_difference, result])
    count = 0
    correct = 0
    for each_test in test_dataset:
        print(f'test_row: {each_test}')
        actual, predicted = get_classification(training_dataset, each_test, 7)
        count = count + 1
        if actual == predicted:
            correct = correct + 1
    print(f'Count: {count}, Correct: {correct}')


# ===================================================== Functions ==================================================== #


def euclidian_distance(point_one, point_two):
    distance = 0
    for x in range(len(point_one)-1):
        distance += pow((point_one[x] - point_two[x]), 2)
    return sqrt(distance)


# ==================================================================================================================== #


def get_k_nearest_neighbors(training_data, new_row, neighbor_num):
    distances = list()
    for training_row in training_data:
        dist = euclidian_distance(new_row, training_row)
        distances.append((training_row, dist))
    distances.sort(key=lambda tup: tup[1])
    neighbors = list()
    for i in range(neighbor_num):
        neighbors.append(distances[i][0])
    return neighbors


# ==================================================================================================================== #


def get_classification(training_data, test_row, neighbor_num):
    neighbors = get_k_nearest_neighbors(training_data, test_row, neighbor_num)
    predictions = []
    for each in neighbors:
        predictions.append(each[-1])
    print(f'Actual: {test_row[-1]}, Predicted: {max(predictions)}')
    return test_row[-1], max(predictions)

# ==================================================================================================================== #


if __name__ == '__main__':
    main()
